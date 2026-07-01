#!/usr/bin/env python3
"""Build a legal Modrinth .mrpack from the live VKPack client profile.

The script hashes active client binaries, resolves exact files through the
Modrinth hash API, writes audit manifests, and only emits a FINAL .mrpack when
no unresolved third-party binaries remain.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

USER_AGENT = "VKPackPublicResolver/1.0.0 (https://github.com/Leonardo-V02/VKPack)"
MODRINTH_HASH_URL = "https://api.modrinth.com/v2/version_files"
DEFAULT_GAME_VERSION = "1.21.1"
DEFAULT_NEOFORGE_VERSION = "21.1.233"
FIRST_PARTY_RESOURCEPACKS = {"grindinggear visual atlas.zip"}

CLIENT_ONLY_HINTS = (
    "appleskin", "betterf3", "blur", "citresewn", "cloth-config", "controlling",
    "dynamic_fps", "embeddium", "entity_model_features", "entity_texture_features",
    "iris", "jade", "jei", "just_enough", "justenough", "modmenu", "mouse", "oculus",
    "searchables", "sodium", "sodiumdynamiclights", "sodium-extra", "sodium_extra",
    "xaero", "zoom", "resourcepackoverrides", "skinlayers", "watut",
)

@dataclass
class LocalFile:
    path: str
    full_path: str
    size: int
    sha1: str
    sha512: str
    env: dict[str, str]
    category: str


def norm_path(path: Path) -> str:
    return path.as_posix()


def hash_file(path: Path) -> tuple[str, str]:
    sha1 = hashlib.sha1()
    sha512 = hashlib.sha512()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            sha1.update(chunk)
            sha512.update(chunk)
    return sha1.hexdigest(), sha512.hexdigest()


def env_for(rel: str) -> dict[str, str]:
    lower = rel.lower()
    if lower.startswith("resourcepacks/") or lower.startswith("shaderpacks/"):
        return {"client": "required", "server": "unsupported"}
    name = Path(rel).name.lower()
    if any(hint in name for hint in CLIENT_ONLY_HINTS):
        return {"client": "required", "server": "unsupported"}
    return {"client": "required", "server": "required"}


def collect_files(client: Path) -> list[LocalFile]:
    candidates: list[tuple[Path, str]] = []
    for folder, pattern, category in (
        ("mods", "*.jar", "mod"),
        ("resourcepacks", "*.zip", "resourcepack"),
        ("shaderpacks", "*.zip", "shaderpack"),
    ):
        root = client / folder
        if not root.exists():
            continue
        for item in sorted(root.glob(pattern), key=lambda p: p.name.lower()):
            if folder == "resourcepacks" and item.name.lower() in FIRST_PARTY_RESOURCEPACKS:
                continue
            candidates.append((item, category))

    files: list[LocalFile] = []
    for full, category in candidates:
        rel = norm_path(full.relative_to(client))
        sha1, sha512 = hash_file(full)
        files.append(LocalFile(rel, str(full), full.stat().st_size, sha1, sha512, env_for(rel), category))
    return files


def post_modrinth_hashes(hashes: list[str], retries: int = 4) -> dict[str, Any]:
    payload = json.dumps({"hashes": hashes, "algorithm": "sha1"}).encode("utf-8")
    req = urllib.request.Request(
        MODRINTH_HASH_URL,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        method="POST",
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt + 1 < retries:
                time.sleep(2 + attempt * 2)
                continue
            raise
        except urllib.error.URLError:
            if attempt + 1 < retries:
                time.sleep(2 + attempt * 2)
                continue
            raise
    return {}


def resolve_modrinth(files: list[LocalFile], batch_size: int = 100) -> dict[str, Any]:
    resolved: dict[str, Any] = {}
    hashes = [f.sha1 for f in files]
    for idx in range(0, len(hashes), batch_size):
        batch = hashes[idx: idx + batch_size]
        print(f"Resolving hashes {idx + 1}-{idx + len(batch)} of {len(hashes)}...")
        resolved.update(post_modrinth_hashes(batch))
    return resolved


def file_entry(local: LocalFile, version: dict[str, Any]) -> dict[str, Any]:
    files = version.get("files") or []
    selected = None
    for candidate in files:
        if (candidate.get("hashes") or {}).get("sha1") == local.sha1:
            selected = candidate
            break
    if selected is None and files:
        selected = files[0]
    downloads = []
    if selected and selected.get("url"):
        downloads.append(selected["url"])
    return {
        "path": local.path,
        "hashes": {"sha1": local.sha1, "sha512": local.sha512},
        "env": local.env,
        "downloads": downloads,
        "fileSize": local.size,
    }


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def load_manual_entries(repo: Path) -> dict[str, dict[str, Any]]:
    sources = [
        repo / "manifest" / "manual-downloads.public.json",
        repo / "manifest" / "manual-downloads.local.json",
    ]
    result: dict[str, dict[str, Any]] = {}
    for source in sources:
        if not source.exists():
            continue
        data = json.loads(source.read_text(encoding="utf-8"))
        entries = data.get("files", data if isinstance(data, list) else [])
        for entry in entries:
            path = entry.get("path")
            downloads = entry.get("downloads") or []
            hashes = entry.get("hashes") or {}
            if path and downloads and hashes.get("sha1"):
                result[path] = entry
    return result


def merge_manual(local: LocalFile, entry: dict[str, Any]) -> dict[str, Any] | None:
    hashes = entry.get("hashes") or {}
    if hashes.get("sha1") != local.sha1:
        return None
    if "sha512" in hashes and hashes.get("sha512") != local.sha512:
        return None
    downloads = entry.get("downloads") or []
    if not downloads:
        return None
    return {
        "path": local.path,
        "hashes": {"sha1": local.sha1, "sha512": local.sha512},
        "env": entry.get("env") or local.env,
        "downloads": downloads,
        "fileSize": local.size,
    }


def make_index(files: list[dict[str, Any]], summary: str) -> dict[str, Any]:
    return {
        "formatVersion": 1,
        "game": "minecraft",
        "versionId": "1.0.0",
        "name": "VKPack",
        "summary": summary,
        "files": sorted(files, key=lambda e: e["path"].lower()),
        "dependencies": {
            "minecraft": DEFAULT_GAME_VERSION,
            "neoforge": DEFAULT_NEOFORGE_VERSION,
        },
    }


def allowed_override(path: Path, rel: str) -> bool:
    lower = rel.replace("\\", "/").lower()
    if "/.git/" in lower or lower.startswith(".git/"):
        return False
    if lower.endswith(".jar") or lower.endswith(".mrpack"):
        return False
    if lower.endswith(".zip"):
        return False
    if "__pycache__" in lower:
        return False
    return True


def build_mrpack(repo: Path, index: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    overrides = repo / "overrides"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        zf.writestr("modrinth.index.json", json.dumps(index, indent=2, ensure_ascii=True) + "\n")
        if overrides.exists():
            for full in sorted(overrides.rglob("*")):
                if not full.is_file():
                    continue
                rel = norm_path(full.relative_to(overrides))
                if not allowed_override(full, rel):
                    continue
                zf.write(full, "overrides/" + rel)


def write_manual_docs(repo: Path, unresolved: list[LocalFile]) -> None:
    manifest = repo / "manifest"
    template = {
        "schema": 1,
        "description": "Files below were not resolved by exact SHA-1 through Modrinth. Add only legal direct-download URLs whose contents match the hashes, or replace the file with a Modrinth-hosted equivalent and rerun tools/build_public_mrpack.py.",
        "files": [
            {
                "path": item.path,
                "fileSize": item.size,
                "hashes": {"sha1": item.sha1, "sha512": item.sha512},
                "env": item.env,
                "downloads": [],
                "notes": "Needs legal direct URL for this exact file, or a pack replacement.",
            }
            for item in unresolved
        ],
    }
    write_json(manifest / "manual-downloads.template.json", template)

    lines = [
        "# Manual Downloads Required",
        "",
        "These active VKPack 1.0.0 files did not resolve by exact SHA-1 through the Modrinth API.",
        "A public `.mrpack` cannot be final until each has a legal automatic download URL, or the pack replaces/removes that file.",
        "",
        "| Path | Size | SHA-1 |",
        "| --- | ---: | --- |",
    ]
    for item in unresolved:
        lines.append(f"| `{item.path}` | {item.size} | `{item.sha1}` |")
    lines.append("")
    (manifest / "MANUAL_DOWNLOADS_REQUIRED.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True, type=Path)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--no-network", action="store_true")
    args = parser.parse_args()

    client = args.client.resolve()
    repo = args.repo.resolve()
    output = args.output or (repo / "pack" / "VKPack-1.0.0-public.mrpack")

    local_files = collect_files(client)
    print(f"Collected {len(local_files)} third-party binary candidates from {client}")

    if args.no_network:
        resolved = {}
    else:
        resolved = resolve_modrinth(local_files)

    manual = load_manual_entries(repo)
    entries: list[dict[str, Any]] = []
    resolved_audit: list[dict[str, Any]] = []
    unresolved: list[LocalFile] = []
    manual_used: list[str] = []

    for item in local_files:
        version = resolved.get(item.sha1)
        if version:
            entry = file_entry(item, version)
            if entry["downloads"]:
                entries.append(entry)
                resolved_audit.append({
                    "path": item.path,
                    "sha1": item.sha1,
                    "source": "modrinth-hash",
                    "project_id": version.get("project_id"),
                    "version_id": version.get("id"),
                    "version_number": version.get("version_number"),
                    "downloads": entry["downloads"],
                })
                continue
        manual_entry = manual.get(item.path)
        if manual_entry:
            merged = merge_manual(item, manual_entry)
            if merged:
                entries.append(merged)
                manual_used.append(item.path)
                continue
        unresolved.append(item)

    summary = "VKPack 1.0.0 Stable public installer. Downloads third-party files from legal source URLs and applies first-party VKPack overrides."
    index = make_index(entries, summary)
    write_json(repo / "pack" / "modrinth.index.json", index)
    write_json(repo / "pack" / "modrinth.index.resolved-only.json", index)
    write_json(repo / "manifest" / "MODRINTH_RESOLVED_FILES.json", resolved_audit)
    write_json(repo / "manifest" / "MODRINTH_RESOLUTION_SUMMARY.json", {
        "pack": "VKPack",
        "version": "1.0.0",
        "client": str(client),
        "candidate_files": len(local_files),
        "resolved_by_modrinth": len(resolved_audit),
        "resolved_by_public_or_local_sources": len(manual_used),
        "unresolved": len(unresolved),
        "output": str(output),
    })
    write_manual_docs(repo, unresolved)

    if unresolved:
        draft_output = output.with_name(output.stem + "-resolved-only-DRAFT" + output.suffix)
        build_mrpack(repo, index, draft_output)
        print(f"UNRESOLVED={len(unresolved)}")
        print(f"Wrote draft resolved-only mrpack: {draft_output}")
        print(f"See: {repo / 'manifest' / 'MANUAL_DOWNLOADS_REQUIRED.md'}")
        return 2

    build_mrpack(repo, index, output)
    print("UNRESOLVED=0")
    print(f"Wrote final mrpack: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

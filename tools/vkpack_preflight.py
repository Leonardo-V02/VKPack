#!/usr/bin/env python3
"""VKPack preflight checks for local client/server payloads.

This script is intentionally conservative. It catches hard failures such as bad
JSON and missing namespaces in item-modification scripts, and it reports probable
issues without treating every static-analysis guess as fatal.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


ID_RE = re.compile(r"""['"]([a-z0-9_.-]+:[a-z0-9_./-]+)['"]""")
KUBEJS_CREATE_RE = re.compile(r"""event\.create\(\s*['"]([a-z0-9_.-]+(?::[a-z0-9_./-]+)?)['"]""")
MOD_ID_RE = re.compile(r"""modId\s*=\s*["']([a-z0-9_.-]+)["']""", re.IGNORECASE)
PLATFORM_GUARD_RE = re.compile(r"""Platform\.isLoaded\(\s*['"]([a-z0-9_.-]+)['"]\s*\)""")

LOG_PATTERNS = {
    "kubejs_errors": re.compile(r"KubeJS startup script errors|Failed to read ingredient|Error in 'ItemEvents"),
    "options_load": re.compile(r"Failed to load options|NumberFormatException: For input string"),
    "diagonalwalls_bake": re.compile(r"Unable to bake model: 'diagonalwalls:architects_palette/"),
    "invalid_scancode": re.compile(r"Invalid scancode"),
    "disconnected": re.compile(r"Client disconnected with reason: Disconnected"),
}

RISKY_OPTION_PATTERNS = {
    "raw_scancode": re.compile(r"scancode\."),
    "high_mouse_button": re.compile(r"key\.mouse\.10\d"),
    "malformed_mekanism_shift_bind": re.compile(r"key_key\.mekanism\.description:key\.keyboard\.[^:\r\n]+:SHIFT"),
}


@dataclass
class Finding:
    severity: str
    message: str


def note(findings: list[Finding], severity: str, message: str) -> None:
    findings.append(Finding(severity, message))


def existing_path(value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    return path if path.exists() else None


def default_client_path() -> Path | None:
    candidate = Path.home() / "AppData/Roaming/ModrinthApp/profiles/VKPack"
    return candidate if candidate.exists() else None


def read_zip_text(zf: zipfile.ZipFile, name: str) -> str:
    try:
        return zf.read(name).decode("utf-8", "replace")
    except Exception:
        return ""


def collect_jar_index(mods_dir: Path, findings: list[Finding]) -> tuple[set[str], set[str], int]:
    namespaces: set[str] = set()
    likely_items: set[str] = set()
    jar_count = 0

    if not mods_dir.exists():
        note(findings, "WARN", f"No mods directory found at {mods_dir}")
        return namespaces, likely_items, jar_count

    for jar in sorted(mods_dir.glob("*.jar")):
        jar_count += 1
        try:
            with zipfile.ZipFile(jar) as zf:
                names = zf.namelist()
                for meta_name in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml"):
                    if meta_name in names:
                        for mod_id in MOD_ID_RE.findall(read_zip_text(zf, meta_name)):
                            namespaces.add(mod_id)
                for name in names:
                    parts = name.split("/")
                    if len(parts) >= 2 and parts[0] in {"assets", "data"}:
                        namespaces.add(parts[1])
                    if name.startswith("assets/") and "/models/item/" in name and name.endswith(".json"):
                        ns = parts[1]
                        item_path = name.split("/models/item/", 1)[1][:-5]
                        likely_items.add(f"{ns}:{item_path}")
                    if name.startswith("assets/") and "/textures/item/" in name and name.endswith(".png"):
                        ns = parts[1]
                        item_path = name.split("/textures/item/", 1)[1][:-4]
                        likely_items.add(f"{ns}:{item_path}")
        except zipfile.BadZipFile:
            note(findings, "FAIL", f"Bad jar file: {jar}")
        except Exception as exc:
            note(findings, "WARN", f"Could not inspect jar {jar.name}: {exc}")

    return namespaces, likely_items, jar_count


def collect_kubejs_created_ids(kubejs_root: Path) -> set[str]:
    created: set[str] = set()
    for script_dir in ("startup_scripts", "server_scripts"):
        root = kubejs_root / script_dir
        if not root.exists():
            continue
        for script in root.rglob("*.js"):
            text = script.read_text(encoding="utf-8", errors="replace")
            for raw in KUBEJS_CREATE_RE.findall(text):
                if ":" in raw:
                    created.add(raw)
                else:
                    created.add(f"kubejs:{raw}")
    return created


def scan_kubejs_ids(
    kubejs_root: Path,
    namespaces: set[str],
    likely_items: set[str],
    findings: list[Finding],
    broad: bool = False,
) -> None:
    if not kubejs_root.exists():
        note(findings, "WARN", f"No KubeJS folder found at {kubejs_root}")
        return

    created = collect_kubejs_created_ids(kubejs_root)
    namespaces = set(namespaces)
    namespaces.add("minecraft")
    namespaces.add("kubejs")

    for script_dir in ("startup_scripts", "server_scripts", "client_scripts"):
        root = kubejs_root / script_dir
        if not root.exists():
            continue
        for script in root.rglob("*.js"):
            text = script.read_text(encoding="utf-8", errors="replace")
            if not broad and "ItemEvents.modification" not in text and ".modify(" not in text:
                continue
            guarded_namespaces = set(PLATFORM_GUARD_RE.findall(text))
            for item_id in sorted(set(ID_RE.findall(text))):
                namespace = item_id.split(":", 1)[0]
                if namespace in guarded_namespaces:
                    continue
                if namespace not in namespaces and item_id not in created:
                    note(findings, "FAIL", f"{script}: references {item_id}, but namespace '{namespace}' is not present in active jars")
                elif item_id not in likely_items and item_id not in created and namespace not in {"c", "forge", "minecraft"}:
                    note(findings, "WARN", f"{script}: could not confirm item asset for {item_id}; verify it exists before using item modification")


def validate_json(root: Path, findings: list[Finding]) -> int:
    checked = 0
    if not root.exists():
        return checked

    for file in root.rglob("*.json"):
        checked += 1
        try:
            json.loads(file.read_bytes().decode("utf-8-sig"))
        except Exception as exc:
            note(findings, "FAIL", f"Invalid JSON: {file}: {exc}")
    return checked


def scan_options(options_file: Path | None, findings: list[Finding]) -> None:
    if not options_file or not options_file.exists():
        return
    text = options_file.read_text(encoding="utf-8", errors="replace")
    for label, pattern in RISKY_OPTION_PATTERNS.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            note(findings, "WARN", f"{options_file}:{line}: risky keybind/options pattern '{label}'")


def scan_latest_log(log_file: Path | None, findings: list[Finding]) -> None:
    if not log_file or not log_file.exists():
        return
    text = log_file.read_text(encoding="utf-8", errors="replace")
    for label, pattern in LOG_PATTERNS.items():
        count = len(pattern.findall(text))
        if count:
            severity = "FAIL" if label == "kubejs_errors" else "WARN"
            note(findings, severity, f"{log_file}: {count} occurrence(s) of {label}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run VKPack client/server preflight checks.")
    parser.add_argument("--repo", default=".", help="VKPack repository root")
    parser.add_argument("--client", default=None, help="Live client profile path")
    parser.add_argument("--server", default=None, help="Unpacked server payload path")
    parser.add_argument("--no-log", action="store_true", help="Skip latest.log scan")
    parser.add_argument(
        "--broad-kubejs-id-scan",
        action="store_true",
        help="Scan every namespace:path string in KubeJS scripts instead of item-modification scripts only",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    client = existing_path(args.client) or default_client_path()
    server = existing_path(args.server)
    findings: list[Finding] = []

    jar_source = client or repo
    namespaces, likely_items, jar_count = collect_jar_index(jar_source / "mods", findings)
    print(f"[INFO] Indexed {jar_count} active jar(s), {len(namespaces)} namespace(s), {len(likely_items)} likely item asset(s).")

    checked_json = 0
    for label, kubejs_root in (
        ("repo", repo / "overrides/kubejs"),
        ("client", client / "kubejs" if client else None),
        ("server", server / "kubejs" if server else None),
    ):
        if kubejs_root and kubejs_root.exists():
            checked_json += validate_json(kubejs_root, findings)
            scan_kubejs_ids(kubejs_root, namespaces, likely_items, findings, broad=args.broad_kubejs_id_scan)
            print(f"[INFO] Checked {label} KubeJS at {kubejs_root}")

    checked_json += validate_json(repo / "pack/VKPack-Guardrails-ResourcePack", findings)
    print(f"[INFO] Validated {checked_json} JSON file(s).")

    if client:
        scan_options(client / "options.txt", findings)
        if not args.no_log:
            scan_latest_log(client / "logs/latest.log", findings)

    fails = [f for f in findings if f.severity == "FAIL"]
    warns = [f for f in findings if f.severity == "WARN"]

    for finding in findings:
        print(f"[{finding.severity}] {finding.message}")

    if fails:
        print(f"[FAIL] Preflight found {len(fails)} failure(s) and {len(warns)} warning(s).")
        return 1

    print(f"[OK] Preflight passed with {len(warns)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

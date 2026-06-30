# VKPack

VKPack is the public source release for the current client pack profile. It keeps the parts that make the pack *our pack* in source control: KubeJS scripts, balance/data edits, selected configs, first-party GrindingGear source, and release manifests.

This repository intentionally does **not** commit third-party mod jars, worlds, logs, caches, screenshots, account files, server lists, or generated crash/debug artifacts.

## What is included

- `overrides/kubejs` - gameplay scripts, recipes, SilentGear/Apotheosis data, generated assets, and pack integration edits.
- `overrides/config` - curated pack configs, with local credentials and binary update jars excluded.
- `overrides/resourcepacks/GrindingGear Visual Atlas` - first-party generated visuals for the custom material work.
- `grindinggear` - source/docs for the first-party GrindingGear mod work. Build outputs live in GitHub Releases, not in git history.
- `manifest` - active mod list, resolved Modrinth files, manual download requirements, and override hashes.

## What is not included

- `mods/` jars from third-party projects.
- `saves/`, `logs/`, `crash-reports/`, `screenshots/`, backups, profile caches, and local server data.
- Secret-ish generated config like `config/resourceful-config-web.json`.
- Update-cache jars such as `config/Veinminer/update/*.jar`.

## Installing as a player

1. Install Minecraft 1.21.1 with NeoForge 21.1.233 in Modrinth App.
2. Use the official VKPack `.mrpack` release once it is published.
3. If using the draft manifest in this repo, install all files listed in `manifest/MANUAL_DOWNLOADS_REQUIRED.md` from their official pages before joining the server.
4. Client and server must use the same KubeJS folder and the same first-party release artifacts.

## Maintaining server compatibility

The server must receive the same `kubejs`, relevant `config`, and first-party GrindingGear release version as the client. A plain mods-folder dump is not enough; most of our compatibility work lives in KubeJS/data/config, not only jars.

## Publishing flow

1. Commit this source tree to GitHub.
2. Attach release artifacts from `release-assets-2026-06-30` to a GitHub Release.
3. For one-click Modrinth install, resolve the files in `manifest/MANUAL_DOWNLOADS_REQUIRED.md` using legal upstream URLs or Modrinth-hosted replacements, then build the final `.mrpack`.

## License

Pack-specific scripts, docs, and first-party generated configs in this repo are released under the license in `LICENSE`. Third-party mods, mod assets, and external resource/shader packs remain under their own licenses.

# VKPack

**VKPack 1.0.0 Stable** is the official first stable release of the VKPack NeoForge 1.21.1 modpack.

VKPack contains the pack-owned pieces: KubeJS scripts, balance/data edits, selected configs, GrindingGear source/data, setup docs, and release manifests. Third-party mod jars are not kept in normal Git history.

## Download VKPack 1.0.0 Stable

| Goal | GitHub Release Asset | Size | Use It For |
|---|---:|---:|---|
| Play on Windows/Modrinth App | `VKPack-Client-1.0.0.zip` | 1306.1 MB | Extract into a NeoForge 1.21.1 Modrinth profile. |
| Host on Ubuntu | `VKPack-Ubuntu-Server-1.0.0.zip` | 1376.37 MB | Copy to the Starbook/Ubuntu server and run the included scripts. |
| Verify downloads | `SHA256SUMS.txt` | tiny | Check file integrity. |

Release page: https://github.com/Leonardo-V02/VKPack/releases/tag/v1.0.0

A future public distribution pass can convert this to a final `.mrpack`/packwiz-style installer where every third-party download is resolved legally and automatically. For this private/friends-server stable release, the full zips are the working path.

## 1.0.0 Stable Fixes

- BDD dragon fallback skins added for `null_male` / `null_female` texture lookups.
- Coal Coke configured as furnace fuel at `3200` ticks, twice vanilla coal.
- Immersive Portals and Portal Gun disabled from active client/server mods.
- Client defaults set to 22 render distance, 8 simulation distance, VSync off, and 240 FPS cap.
- Ubuntu server defaults set to 84 GB max heap, 64 GB soft heap, and 85 percent active CPU target.
- Server defaults remain 25 players, 12 view distance, 5 simulation distance.

## Install

Start with [INSTALL.md](INSTALL.md). The short version:

1. Download `VKPack-Client-1.0.0.zip` from Releases.
2. Open Modrinth App and create/open a NeoForge 1.21.1 profile.
3. Extract the zip contents into that profile folder.
4. Launch.

Server setup is documented in [docs/SETUP_SPECS_AND_OPERATIONS.md](docs/SETUP_SPECS_AND_OPERATIONS.md).

## What Is Included In Source

- `overrides/kubejs` - KubeJS scripts, recipes, custom data, BDD dragon fallback textures, Silent Gear/Apotheosis integration.
- `overrides/config` - curated configs with local caches/history removed.
- `overrides/defaultconfigs` - default world/server configs.
- `grindinggear` - first-party GrindingGear source/data/docs.
- `manifest` - active mod lists, sync notes, disabled-mod ledger, and release audit.
- `tools` - existing pack audit/build/publish scripts.

## What Is Not Kept In Git History

- third-party `mods/` jars,
- full server `libraries/`,
- saves, logs, crash reports, screenshots, local credentials, RCON passwords, and private runtime data.

## Release Integrity

```text
46fcafd6a6c7cf38020015759e5ad9f656b22e6100ef1a3f22eec78d14edd61d  VKPack-Client-1.0.0.zip
75b159bb6783a0f80c29d7547fb09a42ba419399ba0dedbe078512bd6e40f438  VKPack-Ubuntu-Server-1.0.0.zip
```

## License Boundary

Pack-specific scripts, docs, and first-party config/data work follow this repository's license. Third-party mods, mod assets, shaders, and resource packs remain under their own licenses.

# VKPack

VKPack is a NeoForge `1.21.1` modpack built for our server: heavy tech, magic, building, exploration, Silent Gear/Apotheosis depth, and enough performance work to keep the whole thing from melting down.

`1.0.0 Stable` is the first release where the client and Ubuntu server packs are meant to match. If you just want to play, use the release zips. This repo is for the pack-owned work: KubeJS, configs, docs, GrindingGear, manifests, and build scripts. Third-party mod jars do not live in normal Git history.

## Download

Release page: <https://github.com/Leonardo-V02/VKPack/releases/tag/v1.0.0>

| File | Size | Use |
| --- | ---: | --- |
| `VKPack-Client-1.0.0.zip` | 1306.1 MB | Windows/Modrinth App client profile. |
| `VKPack-Ubuntu-Server-1.0.0.zip` | 1376.37 MB | Ubuntu server deploy pack. |
| `SHA256SUMS.txt` | tiny | Verify the zips before trusting them. |

Do not use GitHub's automatic `Source code.zip` as a playable pack. It is source, not a complete client.

## Quick Install

Client:

1. Download `VKPack-Client-1.0.0.zip` from the release page.
2. Create or open a NeoForge `1.21.1` profile in Modrinth App.
3. Extract the zip contents into that profile folder.
4. Launch.

Server:

1. Download `VKPack-Ubuntu-Server-1.0.0.zip`.
2. Follow [INSTALL.md](INSTALL.md) and [docs/SETUP_SPECS_AND_OPERATIONS.md](docs/SETUP_SPECS_AND_OPERATIONS.md).
3. Set your RCON password before exposing the server.

## What Changed In 1.0.0

- Added fallback skins for BDD dragons that were rendering black/missing.
- Made Coal Coke work as furnace fuel at `3200` ticks, twice vanilla coal.
- Disabled Immersive Portals and Portal Gun in the active client/server pack.
- Set client defaults around 22 render distance, 8 simulation distance, VSync off, and 240 FPS cap.
- Set Ubuntu server defaults to 25 players, 12 view distance, 5 simulation distance, 84 GB max heap, 64 GB soft heap, and an 85 percent CPU target.
- Kept the KubeJS, Silent Gear, Apotheosis, GrindingGear, recipe, texture, and performance work synced between client and server.

## Public Installer Status

We are converting VKPack into a proper `.mrpack` path so players can install it through legal automatic downloads instead of sharing a giant zip forever.

Current state:

- `tools/build_public_mrpack.py` builds the public Modrinth installer manifest from the live client profile.
- `483` of `502` third-party files now resolve through Modrinth or verified official FTB Maven URLs.
- `19` files still need a legal exact download source or a tested replacement; they are listed in [manifest/MANUAL_DOWNLOADS_REQUIRED.md](manifest/MANUAL_DOWNLOADS_REQUIRED.md).
- Until that list reaches zero, the full release zips are still the reliable way to play with friends.

## Repo Layout

- `overrides/kubejs` - recipes, tags, startup scripts, data fixes, textures, Silent Gear/Apotheosis integration.
- `overrides/config` - curated client/server config.
- `overrides/defaultconfigs` - world/server defaults.
- `grindinggear` - first-party GrindingGear source, data, and docs.
- `manifest` - mod lists, audits, disabled-mod ledger, installer reports.
- `pack` - generated Modrinth pack indexes and draft `.mrpack` output.
- `tools` - audit, build, validation, and release scripts.

## Not In Git

This repo intentionally leaves out:

- third-party mod jars,
- full server libraries,
- saves,
- logs and crash reports,
- screenshots,
- local credentials,
- RCON passwords,
- private runtime data.

## Checksums

```text
46fcafd6a6c7cf38020015759e5ad9f656b22e6100ef1a3f22eec78d14edd61d  VKPack-Client-1.0.0.zip
75b159bb6783a0f80c29d7547fb09a42ba419399ba0dedbe078512bd6e40f438  VKPack-Ubuntu-Server-1.0.0.zip
```

## License Boundary

VKPack's scripts, configs, docs, and first-party data follow this repo's license. Mods, shaders, and resource packs stay under their own licenses.
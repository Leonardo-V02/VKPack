# Client/Server Sync Rules

VKPack is not reproducible from the mods folder alone.

Sync these between client and server whenever releasing:

- `kubejs/`
- server-relevant files in `config/`
- `defaultconfigs/` when present
- first-party GrindingGear release artifacts, if/when installed as a mod jar
- the exact third-party mod versions in `manifest/MODLIST_ACTIVE.md`

The latest local server pack checked during this export was `Gigani-Ubuntu-Starbook-ServerPack-2026-06-28_204658` with 476 server-side mod jars. It did not contain an active `GrindingGear*.jar`; current custom gameplay appears to be driven primarily through KubeJS plus existing mods.

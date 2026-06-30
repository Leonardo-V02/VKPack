# Contributing

Keep changes reproducible and client/server-safe.

Before opening a pull request:

1. Do not commit third-party jars or generated binary caches.
2. Update `manifest/MODLIST_ACTIVE.md` if mod versions change.
3. Keep KubeJS changes compatible with both client and server.
4. Test a fresh client profile and a fresh server boot when changing recipes, tags, registries, dimensions, or SilentGear materials.
5. Document any manual-download-only files in `manifest/MANUAL_DOWNLOADS_REQUIRED.md`.

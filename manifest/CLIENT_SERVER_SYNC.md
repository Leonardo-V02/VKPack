# Client / Server Sync

Release: `20260701-055459`

| Area | Client | Server |
|---|---:|---:|
| Active jars | 490 | 480 |
| BDD null fallback textures | 20 | 20 |
| Coal Coke fuel KubeJS script | yes | yes |
| Immersive Portals / Portal Gun active jars | 0 | 0 |

The server intentionally has server-side tools that clients do not need, including Chunky and server admin/performance helpers. The client intentionally has client-side renderer/UI/resource features the server does not need.

## Critical Shared Folders

Keep these synchronized between matching client/server releases:

- `kubejs`
- `config`
- `defaultconfigs`
- `grindinggear` / GrindingGear release assets

## Runtime Notes

- Client default render distance is 22 chunks, but the server view-distance cap is 12.
- Server simulation distance is 5 for public stability.
- Server max players is 25 for the Starbook deployment target.

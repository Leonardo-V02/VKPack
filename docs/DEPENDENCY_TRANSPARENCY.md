# Dependency Transparency

VKPack does not publish third-party jars in git. Instead, Modrinth pack files reference upstream downloads.

## Counts From Current Export

- Active client mod jars: `498`
- Modrinth-resolved installable files: `487`
- Unresolved manual/download-policy files: `23`
- Override files included: `21613`

## Why This Matters

A `.mrpack` is not supposed to be a giant jar dump. It is a manifest plus overrides. That keeps GitHub clean, respects upstream authors, and makes installs reproducible.

## Current Unresolved Files

| File | SHA1 |
|---|---|
| `mods/alltheores-3.1.5_neoforge_1.21.1.jar` | `b5c5719384d0334fe553bf5f3f1b2f3e31588a50` |
| `mods/Apotheosis-1.21.1-8.5.4.jar` | `24c28cdf26514148a92f7b8c620ec54a2cd2c9ca` |
| `mods/ApothicAttributes-1.21.1-2.9.1.jar` | `e7f669e1b45d75076200436f37c40a6dd3b6a6ff` |
| `mods/ApothicEnchanting-1.21.1-1.5.3.jar` | `751276a13db49a5f2202e50715b8864f5ae40cb6` |
| `mods/ApothicSpawners-1.21.1-1.3.4.jar` | `26d701238bdb76a497a64f588409419ad067e557` |
| `mods/ars_elemental-1.21.1-0.7.9.4.jar` | `2c68a37fa122bdf80b57d3cd583483c0445770d6` |
| `mods/BiomesOPlenty-neoforge-1.21.1-21.1.0.13.jar` | `a0dec78a9c1bb7e0167e5326aaf3c58a94f3aa86` |
| `mods/create_more_automation-0.5.2-neoforge-1.21.1.jar` | `125b266b569b320c6a652da4381b56c4838c7353` |
| `mods/create_titan-6.1.1-neoforge-1.21.1.jar` | `0e12d866f9fdfbb7c9907c8262aa0396e4d4c070` |
| `mods/culturaldelights-0.17.8.jar` | `5c6504abf92e19b6a5b81f998a405104cad61e8f` |
| `mods/FluxNetworks-1.21.1-8.0.0.jar` | `183342f454428084748f2784c8efd748664a9f9c` |
| `mods/ftb-ez-crystals-21.1.1.jar` | `ff23b7d68c8ef8039d905675ef4412652750b683` |
| `mods/ftb-library-neoforge-2101.1.28.jar` | `de7e0fb584de4915cbab0019275adb746a7d85c0` |
| `mods/ftb-ranks-neoforge-2101.1.2.jar` | `e7c97dab02a9453c3ac00e674127b0b699fcb005` |
| `mods/ftb-ultimine-neoforge-2101.1.15.jar` | `c96a7cc0b52bf919660ea61c1536cebd9d5773b3` |
| `mods/GlitchCore-neoforge-1.21.1-2.1.0.0.jar` | `8bce11b0b5233146051bb7b7a227247e03fe88b2` |
| `mods/inventorysorter-1.21.1-24.0.24.jar` | `8c842959ecb1927e1c7049d41d024fadf329a584` |
| `mods/justenoughbreeding-neoforge-1.21.1-3.1.0.jar` | `57efe71d4f66af02ad733d59f0f0e746697f1ce0` |
| `mods/moremekasuitmodules-1.2-release.jar` | `8e7fbe0da086937648604b08149b35fc4c771542` |
| `mods/oaksdelight-1.0.9-neoforge-1.21.1.jar` | `970adbb0aa122403ce381e2a714b33bacb36289a` |
| `mods/pamhc2foodextended-NEOFORGE-1.21.1-1.0.0.jar` | `73ddcbb8a4772a36d9d4d469fdd5744fb1ede610` |
| `mods/ZeroCore2-1.21.1-2.4.21.jar` | `7df2558f45c3e41bebe86a5ee2b28d56007bdbda` |
| `resourcepacks/FA+Objects-v1.1.1.zip` | `67a08b2463761c3da201444a0a61f7d4c689e6c3` |

Each unresolved file needs one of three decisions:

1. Add a legal direct download URL to `manifest/manual-downloads.local.json`.
2. Replace the file with a Modrinth-hosted project/version.
3. Remove or replace the mod if automated redistribution/download is not allowed.



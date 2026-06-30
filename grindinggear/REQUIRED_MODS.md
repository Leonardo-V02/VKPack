# GrindingGear Required Mods

Target runtime:

- Minecraft: 1.21.1
- Loader: NeoForge 21.1.233 or newer 21.1.x

Hard required mods:

- Silent Gear 4.2.1.1 or newer compatible 4.2.x
- Silent Lib 10.6.0 or newer compatible 10.6.x
- Apotheosis 8.5.4 or newer compatible 8.5.x

Hard required through Apotheosis:

- Placebo 9.9.1 or newer compatible 9.9.x
- Apothic Attributes 2.7.0 or newer compatible 2.7.x
- Apothic Spawners 1.3.0 or newer compatible 1.3.x
- Apothic Enchanting 1.5.2 or newer compatible 1.5.x

Not required:

- KubeJS is not required by this jar. GrindingGear registers the formerly KubeJS-created items itself.

Important migration note:

- This jar keeps the generated item ids as kubejs:* for world and recipe compatibility.
- If your pack still has KubeJS scripts that register the same generated items, disable those scripts before installing GrindingGear.
- In the Gigani profile, the conflicting scripts are:
  - kubejs/startup_scripts/gigani_custom_alloys.js
  - kubejs/startup_scripts/gigani_silentgear_depth_items.js
  - kubejs/startup_scripts/gigani_mercury_titanium_depth_items.js

Optional compatibility providers:

These are not hard requirements. GrindingGear uses common tags, optional tag entries, and pattern-based loot hooks so these mods can enrich the material system when installed:

- Oritech and Oritech Things
- Mekanism
- EvilCraft
- Malum
- Forbidden & Arcanus
- Theurgy
- The Undergarden
- Silent Gems
- AllTheOres
- Actually Additions
- Applied Energistics 2 / Advanced AE / Extended AE
- Avaritia-style endgame material providers
- Farmer's Delight-style food and material tag providers where present
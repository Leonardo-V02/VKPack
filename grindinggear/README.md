# GrindingGear

GrindingGear is a focused Silent Gear and Apotheosis compatibility mod built from the Gigani pack's custom material system.

It adds a broad, balanced material layer for heavily modded NeoForge 1.21.1 packs:

- 104 craftable alloy ingots, including carbide steels, tungsten steels, matrix steels, conductive alloys, radiant alloys, void alloys, dark alloys, resonant alloys, arcane alloys, flux alloys, catalytic alloys, and practical bearing/light/superalloy families.
- 14 advanced Silent Gear crafting components for linings, bindings, cores, coatings, and late-game part identity.
- 405 Silent Gear material definitions covering ingots, gems, alloy composites, bindings, tips, linings, coatings, rods, and specialty parts.
- 71 custom data-driven Silent Gear traits for metallurgy, crystal optics, dimensional fields, reactor materials, occult conduits, and organic/soft composites.
- 104 Silent Gear alloy forge recipes that let the custom alloy system feel native to Silent Gear without removing the existing machine paths.
- A generated visual atlas with per-material part icons, tool previews, armor previews, and armor-layer placeholder textures for resource-pack and future renderer work.
- Apotheosis gem integration for Fluxite Lens, Adamant Core, Deorum Heart, Dark Power Prism, and Soul Anchor.
- Tag-first recipes so other mods can provide metals, gems, sulfur, salts, carbon, arcane crystals, and endgame materials without this mod becoming a hard dependency web.
- Loot and acquisition hooks that connect late-game gems to thematic source content when those mods are present.

GrindingGear intentionally registers its generated items under the kubejs:* namespace. That preserves compatibility with worlds and recipes that were originally prototyped in KubeJS. Do not run the old KubeJS startup item-registration scripts at the same time as this jar, or the duplicate item ids will crash during registry setup.

## Required Mods

See REQUIRED_MODS.md for the exact hard requirements and optional compatibility providers.

## Included Content

- Generated item registry: 145 items under kubejs:*
- Silent Gear material JSON files: 418
- Custom alloy recipes: 130
- Silent Gear alloy forge recipes: 130
- Silent Gear depth recipes: 14
- Apotheosis bridge recipes: 5
- Apotheosis custom gems: 5

## Build

Run from the profile root:

    powershell -ExecutionPolicy Bypass -File .\codex_build_grindinggear.ps1

The publishable jar is written to:

    grindinggear/dist/GrindingGear-1.0.0+mc1.21.1-neoforge.jar
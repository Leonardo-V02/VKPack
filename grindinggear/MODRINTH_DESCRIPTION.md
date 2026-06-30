# GrindingGear

GrindingGear is a NeoForge 1.21.1 compatibility expansion for packs that want Silent Gear and Apotheosis to become a real long-form progression system instead of a pile of unconnected ingots.

It adds 104 custom alloy ingots, 14 advanced Silent Gear crafting components, 405 Silent Gear material definitions, 71 custom data-driven Silent Gear traits, 104 Silent Gear alloy forge recipes, and five custom Apotheosis gems. The material design is intentionally grounded: carbide steels are hard and wear-resistant, tungsten blends are dense and powerful, conductor alloys lean into speed and energy flavor, resonant alloys reward precision, and weaker metals stay useful without pretending to be endgame.

The recipes are tag-first. If your pack has tungsten, titanium, nickel, osmium, iridium, platinum, uranium, sulfur, salts, cinnabar, fluorite, ruby, sapphire, peridot, or other common modded materials, GrindingGear tries to give them a Silent Gear identity.

## Features

- 100 alloy ingots built for Silent Gear crafting.
- 14 late-game cores, linings, and bindings.
- 405 Silent Gear material definitions with varied stats, traits, and part roles.
- 71 custom traits covering metallurgy, crystals, dimensional materials, reactor chemistry, soft composites, bearings, and occult materials.
- Generated visual atlas assets for 405 materials, including part roles, tool previews, armor previews, and armor-layer placeholder textures.
- Note: Silent Gear 4.2 material data only exposes color plus high/low contrast texture types; using every generated silhouette live on gear requires a client renderer hook.
- Apotheosis gems: Fluxite Lens, Adamant Core, Deorum Heart, Dark Power Prism, and Soul Anchor.
- Apotheosis bridge recipes for socketing, withdrawal, rebirth, enhancement, and gem-fused slate.
- Optional acquisition hooks for Oritech, EvilCraft, Malum, Theurgy, Undergarden, and similar high-depth packs.
- Keeps original kubejs:* item ids to preserve worlds made with earlier KubeJS prototypes.

## Required

- Minecraft 1.21.1
- NeoForge 21.1.233+
- Silent Gear 4.2.1.1+
- Silent Lib 10.6.0+
- Apotheosis 8.5.4+ and its normal dependencies

KubeJS is not required.

## Pack Authors

If migrating from the original KubeJS prototype, disable any startup scripts that register the same custom alloy/depth items. Leaving both active will cause duplicate item id registry crashes.
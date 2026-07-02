# VKPack Final Polish Pass

This pass keeps the stable mod list intact and only adjusts pack-owned data/resources.

## Gameplay bridges

- Added final Silent Gear material definitions for bismuth, brass, bronze, electrum, enderium, invar, lumium, nickel, osmium, platinum, signalum, silver, and tin.
- Added tag aliases so `c:ingots/titanium_carbide` and `c:ingots/vanadium_steel` resolve to the installed Electrodynamics `titaniumcarbide` and `vanadiumsteel` ingots.
- Added dust smelting/blasting recipes for all tagged dusts that had an obvious matching ingot output but no pack-owned dust furnace bridge.
- Hardened coal coke burn-time support for Immersive Engineering, Electrodynamics, Railcraft-style, and Modern Industrialization-style item IDs.

## Visual polish

- Replaced BDD dragon `null_male` / `null_female` fallback textures with real base skins from the active BDD jar, preventing black-purple missing-texture silhouettes when a dragon variant falls back to `null`.

## Performance position

- Client: use the VKPack Modrinth instance memory override profile (`50G` max, ZGC, 17 logical CPUs on this machine). Restart Modrinth after applying the profile.
- Server: use `run-java-server.sh`, which reads `.server.env`, targets `84G` max heap, `64G` soft heap, and computes `85%` of available CPUs with `-XX:ActiveProcessorCount`.
- GPU/iGPU: the client benefits from Iris/Sodium/Embeddium-side rendering settings; the dedicated server does not use GPU for TPS work. Server tick performance is CPU, memory, disk, worldgen, and entity/chunk workload.

## Spin-up order

1. Pull the latest GitHub repo on the server laptop.
2. Copy/sync `overrides/kubejs` into the server pack `kubejs` folder if using the unpacked server payload.
3. Start the server with `./run-java-server.sh`.
4. Start the client from Modrinth after restarting the Modrinth app.
5. Join, then run Spark if blocks/entities still delay: `/spark profiler --timeout 120`.

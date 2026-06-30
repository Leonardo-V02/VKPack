# Gigani Public Release Plan

Date: 2026-06-24

This is the release-focused plan for getting the Gigani pack ready for a public Modrinth/server launch. It separates balance, polish, performance, and publishing so we do not keep solving every problem by adding another mod.

## Current Release Baseline

- Active jar count: 511.
- Disabled jar count: 98.
- Latest known focus: the pack loads and plays, but public release needs balance guardrails, clean docs, repeatable startup/world testing, and a final performance profile.
- KubeJS JSON validation must remain clean before export.
- GrindingGear must be rebuilt whenever KubeJS material, trait, tag, recipe, or asset data changes.

## Balance Guardrails

- Advanced materials may specialize hard, but should not beat endgame materials across multiple major stats.
- Endgame materials may be excessive only when gated by bosses, rare dimensions, high-tier machines, expensive alloys, or rare late-game resources.
- Low-tier metals and gems should stay useful through part roles, coatings, bindings, linings, settings, enchantment value, magic stats, or unique traits instead of raw damage alone.
- Fast advanced alloys are capped so they stay exciting without erasing late-game tools.
- Silent Gear alloy forge recipes are allowed, but machine recipes remain the primary industrial progression path.

## Polish Targets Before Upload

- Keep the pack name and icon consistent across the Modrinth profile, server files, and launcher metadata.
- Remove or archive local-only artifacts before packaging: crash reports, old Spark profiles, screenshots, backups, world saves, local database backups, and Codex scratch files.
- Keep `mods-disabled` outside the published pack unless it is intentionally documented for server admins.
- Add a short public description that explains the identity: huge tech/magic/building pack, Silent Gear/Apotheosis depth, cozy/pets/food, late-game bosses and machinery, shaders supported.
- Add a "known heavy pack" note with RAM guidance and a recommendation to pregen chunks before opening a public server.

## Required Test Pass

- Fresh client launch to main menu.
- Fresh singleplayer world creation.
- Five-minute in-world smoke test: open inventory, open a chest, use JEI, break blocks, fight a mob, sleep/pass time, teleport or travel a few chunks.
- Server launch with the exported pack.
- Join server with a fresh client profile.
- Run Spark for at least 10 minutes under normal play.
- Run Chunky pregen for the public spawn radius before inviting players.

## Performance Release Policy

- Do not raise simulation distance for public launch until Spark shows stable TPS.
- Keep shaders optional and client-side.
- Pregenerate spawn and common travel regions.
- Keep entity farms, chunk loaders, quarry systems, and high-throughput automation behind server rules or claim limits.
- Use Spark reports to tune actual tick sources instead of guessing.

## Next Good Passes

- Create a clean Modrinth export without local logs/saves/backups.
- Write a short public changelog for version 1.0.0.
- Build or refresh the GrindingGear jar after every material-system change.
- Review late-game recipe paths for the highest-tier weapons, missiles, quarries, chunk loaders, and infinite-resource systems.
- Add quest/progression guidance so players understand what to pursue first.

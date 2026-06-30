# Installing VKPack from GitHub into Modrinth

This page is for players. You should not need to clone this repo, install Git, copy KubeJS folders, or manually assemble a mods folder.

## Visual Overview

![VKPack GitHub to Modrinth setup flow](docs/assets/github-to-modrinth-flow.svg)

For the full picture walkthrough, see [docs/PLAYER_SETUP_TUTORIAL.md](docs/PLAYER_SETUP_TUTORIAL.md).

## The Simple Path

1. Go to the VKPack GitHub **Releases** page.
2. Download the asset ending in `FINAL.mrpack`.
3. Open Modrinth App.
4. Click **Create Profile**.
5. Choose **Import from file**.
6. Select the `.mrpack` you downloaded.
7. Wait for Modrinth to download the referenced mods.
8. Launch the profile.

That `.mrpack` is the single file you want. It contains the pack overrides and a manifest telling Modrinth where to retrieve the allowed upstream downloads.

## What Not To Download

Do not use GitHub's automatic `Source code.zip` / `Source code.tar.gz` buttons to play the pack. Those are source snapshots for maintainers and will not create a playable Modrinth profile by themselves.

## Draft vs Final

A release may also contain something named like:

`VKPack-2026-06-30-resolved-only-DRAFT.mrpack`

That file is transparent but incomplete. It includes all Modrinth-resolved dependencies and the VKPack overrides, but it intentionally does not pretend the unresolved files are solved. At the time this guide was written, `23` files still needed legal direct-download resolution or Modrinth-hosted replacements.

Use the draft only if you are helping test packaging. Regular players should wait for `FINAL.mrpack`.

## What A Working Final Release Guarantees

A final VKPack `.mrpack` should include:

- Minecraft `1.21.1`,
- NeoForge `21.1.233`,
- all Modrinth-resolved dependency download references,
- legal direct download references or approved replacements for non-Modrinth files,
- `kubejs/` overrides,
- selected `config/` overrides,
- GrindingGear visual assets,
- first-party GrindingGear jar as a release asset if the pack requires it.

## Server Compatibility

The public client pack and the server pack must use matching KubeJS/config/GrindingGear versions. If you get a missing registry, missing item, or mismatch error, check that the server owner is running the server release matching the client `.mrpack` tag.


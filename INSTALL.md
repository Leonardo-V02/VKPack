# Installing VKPack 1.0.0 Stable

## Player Client

Use the release asset named:

`VKPack-Client-1.0.0.zip`

1. Install or open the Modrinth App.
2. Create a NeoForge `1.21.1` profile named `VKPack`, or open your existing profile folder.
3. Extract the zip contents directly into that profile folder.
4. In Modrinth, allocate memory:
   - 12-16 GB for strong PCs without heavy shaders.
   - 16-24 GB for high-resolution shaders or longer sessions.
   - More than 24 GB usually does not help the client much.
5. Launch the profile.

Do not use GitHub's automatic `Source code.zip` to play. That is source for maintainers, not a complete playable profile.

## Ubuntu Server

Use the release asset named:

`VKPack-Ubuntu-Server-1.0.0.zip`

```bash
sudo apt update
sudo apt install openjdk-21-jre-headless unzip screen tmux
unzip VKPack-Ubuntu-Server-1.0.0.zip -d vkpack-server
cd vkpack-server
chmod +x *.sh
printf 'eula=true\n' > eula.txt
./install-neoforge-server.sh
nano .server.env
./start-server.sh
```

Set a private RCON password before opening the server publicly.

Optional maintainer check before launch:

```bash
python3 tools/vkpack_preflight.py --repo . --server /path/to/vkpack-server
```

On the Windows client machine, run the same check with the client profile path before publishing a new build:

```powershell
python tools/vkpack_preflight.py --client "$env:APPDATA\ModrinthApp\profiles\VKPack"
```

## Expected Server Defaults

- `max-players=25`
- `view-distance=12`
- `simulation-distance=5`
- `GIGANI_XMX=84G`
- `GIGANI_SOFT_MAX_HEAP=64G`
- `GIGANI_CPU_PERCENT=85`

## Public Installer Status

The repo now includes `tools/build_public_mrpack.py`, which builds a Modrinth-style installer manifest from the live client profile.

Current public installer state:

- `483` of `502` third-party files resolve through Modrinth or verified official FTB Maven URLs.
- `19` files still need a legal exact download source or a tested replacement.
- The blocker list is in `manifest/MANUAL_DOWNLOADS_REQUIRED.md`.

Until that list reaches zero, use the full client/server release zips above for actual play.


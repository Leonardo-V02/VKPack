# Installing VKPack / Gigani

## Player Client: Current Working Path

Use the release asset named:

`Gigani-Client-20260701-055459.zip`

1. Install or open the Modrinth App.
2. Create a NeoForge `1.21.1` profile named `Gigani`, or open your existing profile folder.
3. Extract the zip contents directly into that profile folder.
4. In Modrinth, allocate memory:
   - 12-16 GB for strong PCs without heavy shaders.
   - 16-24 GB for high-resolution shaders or longer sessions.
   - More than 24 GB usually does not help the client much.
5. Launch the profile.

Do not use GitHub's automatic `Source code.zip` to play. That is source for maintainers, not a complete playable profile.

## Ubuntu Server

Use the release asset named:

`Gigani-Ubuntu-Server-20260701-055459.zip`

```bash
sudo apt update
sudo apt install openjdk-21-jre-headless unzip screen tmux
unzip Gigani-Ubuntu-Server-20260701-055459.zip -d gigani-server
cd gigani-server
chmod +x *.sh
printf 'eula=true\n' > eula.txt
./install-neoforge-server.sh
nano .server.env
./start-server.sh
```

Set a private RCON password before opening the server publicly.

## Expected Server Defaults

- `max-players=25`
- `view-distance=12`
- `simulation-distance=5`
- `GIGANI_XMX=84G`
- `GIGANI_SOFT_MAX_HEAP=64G`
- `GIGANI_CPU_PERCENT=85`

## Future One-Click Public Path

A final `.mrpack` or packwiz installer is still the cleanest public distribution target. That pass should resolve every third-party dependency through Modrinth/public URLs instead of shipping jars in a zip.

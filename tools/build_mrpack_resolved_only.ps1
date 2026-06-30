$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$index = Join-Path $root 'pack\modrinth.index.resolved-only.json'
$outDir = Join-Path (Split-Path -Parent $root) 'artifacts'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$stage = Join-Path $env:TEMP ('vkpack-mrpack-' + [guid]::NewGuid())
New-Item -ItemType Directory -Force -Path $stage | Out-Null
Copy-Item -LiteralPath $index -Destination (Join-Path $stage 'modrinth.index.json')
Copy-Item -LiteralPath (Join-Path $root 'overrides') -Destination (Join-Path $stage 'overrides') -Recurse
$out = Join-Path $outDir 'VKPack-2026-06-30-resolved-only-DRAFT.mrpack'
if (Test-Path -LiteralPath $out) { Remove-Item -LiteralPath $out -Force }
Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $out -Force
Remove-Item -LiteralPath $stage -Recurse -Force
Write-Host "Wrote draft mrpack: $out"
Write-Host "This draft omits files listed in manifest/MANUAL_DOWNLOADS_REQUIRED.md and is not server-complete until those are resolved."

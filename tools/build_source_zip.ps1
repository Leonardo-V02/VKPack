$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$name = Split-Path -Leaf $root
$out = Join-Path (Split-Path -Parent $root) "$name-source.zip"
if (Test-Path -LiteralPath $out) { Remove-Item -LiteralPath $out -Force }
Compress-Archive -LiteralPath $root -DestinationPath $out -Force
Write-Host "Wrote $out"

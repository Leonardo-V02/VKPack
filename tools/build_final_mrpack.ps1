param(
  [string]$Version = "2026.06.30",
  [string]$OutDir = "..\release-assets-2026-06-30"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$IndexPath = Join-Path $Root 'pack\modrinth.index.resolved-only.json'
$ManualTemplatePath = Join-Path $Root 'manifest\manual-downloads.template.json'
$ManualLocalPath = Join-Path $Root 'manifest\manual-downloads.local.json'
$Overrides = Join-Path $Root 'overrides'
$OutputDir = Resolve-Path -LiteralPath (Join-Path $Root $OutDir)
$Output = Join-Path $OutputDir "VKPack-$Version-FINAL.mrpack"

if (!(Test-Path -LiteralPath $ManualLocalPath)) {
  throw "Missing manifest/manual-downloads.local.json. Copy manifest/manual-downloads.template.json to that filename and fill legal download URLs first."
}

$index = Get-Content -LiteralPath $IndexPath -Raw | ConvertFrom-Json
$template = @(Get-Content -LiteralPath $ManualTemplatePath -Raw | ConvertFrom-Json)
$local = @(Get-Content -LiteralPath $ManualLocalPath -Raw | ConvertFrom-Json)
$byPath = @{}
foreach ($entry in $local) { if ($entry.path) { $byPath[$entry.path] = $entry } }

$missing = @()
foreach ($entry in $template) {
  if (!$byPath.ContainsKey($entry.path)) { $missing += $entry.path; continue }
  $resolved = $byPath[$entry.path]
  if (!$resolved.downloads -or $resolved.downloads.Count -lt 1) { $missing += $entry.path; continue }
  if (!$resolved.sha1 -or !$resolved.sha512 -or !$resolved.size) { $missing += $entry.path; continue }
  $env = @{ client = 'required'; server = 'required' }
  if ($resolved.path.StartsWith('resourcepacks/') -or $resolved.path.StartsWith('shaderpacks/')) {
    $env = @{ client = 'required'; server = 'unsupported' }
  }
  $fileEntry = [ordered]@{
    path = $resolved.path
    hashes = [ordered]@{ sha1 = $resolved.sha1; sha512 = $resolved.sha512 }
    env = $env
    downloads = @($resolved.downloads)
    fileSize = [int64]$resolved.size
  }
  $index.files += $fileEntry
}

if ($missing.Count -gt 0) {
  Write-Host "Cannot build FINAL .mrpack. Missing/resolution-incomplete entries:" -ForegroundColor Red
  $missing | ForEach-Object { Write-Host " - $_" }
  exit 2
}

$index.versionId = $Version
$index.summary = "VKPack final Modrinth import pack. Includes all resolved dependency URLs plus KubeJS/config overrides."

$Stage = Join-Path $env:TEMP ('vkpack-final-mrpack-' + [guid]::NewGuid())
New-Item -ItemType Directory -Force -Path $Stage | Out-Null
try {
  $indexJson = $index | ConvertTo-Json -Depth 80
  [System.IO.File]::WriteAllText((Join-Path $Stage 'modrinth.index.json'), $indexJson, [System.Text.UTF8Encoding]::new($false))
  Copy-Item -LiteralPath $Overrides -Destination (Join-Path $Stage 'overrides') -Recurse
  if (Test-Path -LiteralPath $Output) { Remove-Item -LiteralPath $Output -Force }
  Compress-Archive -Path (Join-Path $Stage '*') -DestinationPath $Output -Force
  Write-Host "Built FINAL mrpack: $Output" -ForegroundColor Green
}
finally {
  if (Test-Path -LiteralPath $Stage) { Remove-Item -LiteralPath $Stage -Recurse -Force }
}

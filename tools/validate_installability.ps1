$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Template = Join-Path $Root 'manifest\manual-downloads.template.json'
$Local = Join-Path $Root 'manifest\manual-downloads.local.json'
$Audit = Join-Path $Root 'manifest\RELEASE_AUDIT.json'

$manual = @()
if (Test-Path -LiteralPath $Template) {
  $manual = @(Get-Content -LiteralPath $Template -Raw | ConvertFrom-Json)
}
$localEntries = @()
if (Test-Path -LiteralPath $Local) {
  $localEntries = @(Get-Content -LiteralPath $Local -Raw | ConvertFrom-Json)
}

$resolved = @{}
foreach ($entry in $localEntries) {
  if ($entry.path) { $resolved[$entry.path] = $entry }
}

$missing = @()
foreach ($entry in $manual) {
  if (!$resolved.ContainsKey($entry.path)) {
    $missing += $entry.path
    continue
  }
  $candidate = $resolved[$entry.path]
  if (!$candidate.downloads -or $candidate.downloads.Count -lt 1) { $missing += $entry.path }
  if (!$candidate.sha1 -or !$candidate.sha512 -or !$candidate.size) { $missing += $entry.path }
}

if (Test-Path -LiteralPath $Audit) {
  $auditObj = Get-Content -LiteralPath $Audit -Raw | ConvertFrom-Json
  if ($auditObj.blocked_binary_files_in_source.Count -gt 0) {
    Write-Host "Blocked binary/runtime files are present in source:" -ForegroundColor Red
    $auditObj.blocked_binary_files_in_source
    exit 1
  }
}

if ($missing.Count -gt 0) {
  Write-Host "Installability status: DRAFT only" -ForegroundColor Yellow
  Write-Host "$($missing.Count) manual downloads still unresolved. Final one-click .mrpack should not be published yet." -ForegroundColor Yellow
  $missing | ForEach-Object { Write-Host " - $_" }
  exit 2
}

Write-Host "Installability status: FINAL-ready. All manual downloads have local URL/hash entries." -ForegroundColor Green

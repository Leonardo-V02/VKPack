param(
  [string]$RepoName = "VKPack",
  [string]$Owner = "",
  [string]$ArtifactsDir = "..\release-assets-2026-06-30",
  [string]$Tag = "v2026.06.30",
  [switch]$Private
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$PortableGh = Join-Path (Split-Path -Parent $Root) "tools\bin\gh.exe"
$Gh = if (Test-Path -LiteralPath $PortableGh) { $PortableGh } else { "gh" }
$BundledGit = "C:\Users\V02\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe"
$Git = if (Test-Path -LiteralPath $BundledGit) { $BundledGit } else { "git" }

Push-Location $Root
try {
  & $Gh auth status *> $null
  if ($LASTEXITCODE -ne 0) {
    Write-Host "GitHub login is required. Follow the browser/device-code flow." -ForegroundColor Yellow
    & $Gh auth login --hostname github.com --git-protocol https --web
  }

  if ([string]::IsNullOrWhiteSpace($Owner)) {
    $Owner = (& $Gh api user --jq .login).Trim()
  }
  $RepoFull = "$Owner/$RepoName"
  $Visibility = if ($Private) { "--private" } else { "--public" }

  $RepoExists = $false
  try {
    & $Gh repo view $RepoFull *> $null
    $RepoExists = ($LASTEXITCODE -eq 0)
  } catch {
    $RepoExists = $false
  }

  if (!$RepoExists) {
    & $Gh repo create $RepoFull $Visibility --description "VKPack public source release: KubeJS, configs, manifests, and first-party GrindingGear source."
  }

  try { & $Git remote remove origin 2>$null } catch {}
  & $Git remote add origin "https://github.com/$RepoFull.git"
  & $Git push -u origin main

  & $Git tag -l $Tag | ForEach-Object { if ($_ -eq $Tag) { & $Git tag -d $Tag | Out-Null } }
  & $Git tag -a $Tag -m "VKPack public source release $Tag"
  & $Git push origin $Tag --force

  $BuildSourceZip = Join-Path $Root "tools\build_source_zip.ps1"
  if (Test-Path -LiteralPath $BuildSourceZip) {
    & $BuildSourceZip -OutDir $ArtifactsDir
  }

  $ArtifactPath = (Resolve-Path -LiteralPath (Join-Path $Root $ArtifactsDir)).Path
  $AuditSource = Join-Path $Root "manifest\RELEASE_AUDIT.json"
  if (Test-Path -LiteralPath $AuditSource) {
    Copy-Item -LiteralPath $AuditSource -Destination (Join-Path $ArtifactPath "RELEASE_AUDIT.json") -Force
  }

  $ManualTemplate = Join-Path $Root "manifest\manual-downloads.template.json"
  $UnresolvedCount = "unknown"
  if (Test-Path -LiteralPath $ManualTemplate) {
    $UnresolvedCount = @((Get-Content -LiteralPath $ManualTemplate -Raw | ConvertFrom-Json)).Count
  }

  $Notes = Join-Path $ArtifactPath "GITHUB_RELEASE_NOTES.md"
  @"
# VKPack $Tag

This release contains the open-source pack source snapshot and release artifacts.

For players: use `VKPack-...-FINAL.mrpack` when present. Import it into Modrinth App; do not use GitHub's source-code zip to play.

Current note: `VKPack-2026-06-30-resolved-only-DRAFT.mrpack` is a draft import pack. It resolves the Modrinth-hosted dependency set and includes overrides, but `$UnresolvedCount` files listed in `manifest/MANUAL_DOWNLOADS_REQUIRED.md` still need legal direct-download resolution or Modrinth-hosted replacements before this is truly one-click/server-complete.

Attached/download notes:
- Source zip: safe GitHub source snapshot.
- GrindingGear jar: first-party mod jar owned by this pack.
- Draft mrpack: not final until manual-download blockers are resolved.
- Final mrpack, if present: the player-facing Modrinth import file.

Visual setup tutorial: see `docs/PLAYER_SETUP_TUTORIAL.md` in the source repo.
"@ | Set-Content -LiteralPath $Notes -Encoding UTF8

  $FixedAssets = @(
    Join-Path $ArtifactPath "VKPack-GitHub-Source-2026-06-30-source.zip",
    Join-Path $ArtifactPath "GrindingGear-1.0.0+mc1.21.1-neoforge.jar",
    Join-Path $ArtifactPath "VKPack-2026-06-30-resolved-only-DRAFT.mrpack",
    Join-Path $ArtifactPath "RELEASE_AUDIT.json"
  )
  $FinalMrpacks = @(Get-ChildItem -LiteralPath $ArtifactPath -File -Filter "VKPack-*-FINAL.mrpack" -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName })
  $Assets = @($FixedAssets + $FinalMrpacks) | Where-Object { Test-Path -LiteralPath $_ }

  $ReleaseExists = $false
  try {
    & $Gh release view $Tag --repo $RepoFull *> $null
    $ReleaseExists = ($LASTEXITCODE -eq 0)
  } catch {
    $ReleaseExists = $false
  }

  if ($ReleaseExists) {
    & $Gh release upload $Tag @Assets --repo $RepoFull --clobber
  } else {
    & $Gh release create $Tag @Assets --repo $RepoFull --title "VKPack $Tag" --notes-file $Notes
  }

  Write-Host "Published: https://github.com/$RepoFull/releases/tag/$Tag" -ForegroundColor Green
}
finally {
  Pop-Location
}



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

  & $Gh repo view $RepoFull *> $null
  if ($LASTEXITCODE -ne 0) {
    & $Gh repo create $RepoFull $Visibility --source $Root --remote origin --description "VKPack public source release: KubeJS, configs, manifests, and first-party GrindingGear source." --push
  } else {
    & $Git remote remove origin 2>$null
    & $Git remote add origin "https://github.com/$RepoFull.git"
    & $Git push -u origin main
  }

  & $Git tag -l $Tag | ForEach-Object { if ($_ -eq $Tag) { & $Git tag -d $Tag | Out-Null } }
  & $Git tag -a $Tag -m "VKPack public source release $Tag"
  & $Git push origin $Tag --force

  $ArtifactPath = Resolve-Path -LiteralPath (Join-Path $Root $ArtifactsDir)
  $Notes = Join-Path $ArtifactPath "GITHUB_RELEASE_NOTES.md"
  if (!(Test-Path -LiteralPath $Notes)) {
    @"
# VKPack $Tag

This release contains the open-source pack source snapshot and release artifacts.

Important: `VKPack-2026-06-30-resolved-only-DRAFT.mrpack` is a draft import pack. It resolves the Modrinth-hosted dependency set and includes overrides, but files listed in `manifest/MANUAL_DOWNLOADS_REQUIRED.md` still need legal direct-download resolution or Modrinth-hosted replacements before this is truly one-click/server-complete.

Attach/download notes:
- Source zip: safe GitHub source snapshot.
- GrindingGear jar: first-party mod jar owned by this pack.
- Draft mrpack: not final until manual-download blockers are resolved.
"@ | Set-Content -LiteralPath $Notes -Encoding UTF8
  }

  $Assets = @(
    Join-Path $ArtifactPath "VKPack-GitHub-Source-2026-06-30-source.zip",
    Join-Path $ArtifactPath "GrindingGear-1.0.0+mc1.21.1-neoforge.jar",
    Join-Path $ArtifactPath "VKPack-2026-06-30-resolved-only-DRAFT.mrpack",
    Join-Path $ArtifactPath "RELEASE_AUDIT.json"
  ) | Where-Object { Test-Path -LiteralPath $_ }

  & $Gh release view $Tag --repo $RepoFull *> $null
  if ($LASTEXITCODE -eq 0) {
    & $Gh release upload $Tag @Assets --repo $RepoFull --clobber
  } else {
    & $Gh release create $Tag @Assets --repo $RepoFull --title "VKPack $Tag" --notes-file $Notes
  }

  Write-Host "Published: https://github.com/$RepoFull/releases/tag/$Tag" -ForegroundColor Green
}
finally {
  Pop-Location
}
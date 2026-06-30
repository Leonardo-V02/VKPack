param(
  [string]$OutDir = "..\release-assets-2026-06-30"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Name = Split-Path -Leaf $Root
$OutputDirPath = Join-Path $Root $OutDir
if (!(Test-Path -LiteralPath $OutputDirPath)) {
  New-Item -ItemType Directory -Force -Path $OutputDirPath | Out-Null
}
$OutputDir = (Resolve-Path -LiteralPath $OutputDirPath).Path
$Out = Join-Path $OutputDir "$Name-source.zip"
$TempOut = "$Out.tmp"

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
if (Test-Path -LiteralPath $Out) { Remove-Item -LiteralPath $Out -Force }
if (Test-Path -LiteralPath $TempOut) { Remove-Item -LiteralPath $TempOut -Force }

$RootFull = (Resolve-Path -LiteralPath $Root).Path.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
$ExcludedTopLevelDirs = @('.git', '.agents', '.codex')
$ExcludedRelativeFiles = @('manifest/manual-downloads.local.json')

$Zip = [System.IO.Compression.ZipFile]::Open($TempOut, [System.IO.Compression.ZipArchiveMode]::Create)
try {
  Get-ChildItem -LiteralPath $Root -Recurse -Force -File | ForEach-Object {
    $Relative = $_.FullName.Substring($RootFull.Length).TrimStart([char[]]@('\', '/')).Replace('\', '/')
    $Top = ($Relative -split '/')[0]
    if ($ExcludedTopLevelDirs -contains $Top) { return }
    if ($ExcludedRelativeFiles -contains $Relative) { return }

    $EntryName = "$Name/$Relative"
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
      $Zip,
      $_.FullName,
      $EntryName,
      [System.IO.Compression.CompressionLevel]::Optimal
    ) | Out-Null
  }
}
finally {
  $Zip.Dispose()
}

Move-Item -LiteralPath $TempOut -Destination $Out -Force
Write-Host "Wrote $Out"




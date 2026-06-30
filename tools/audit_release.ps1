$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$badExt = @('*.jar','*.mrpack','*.zip','*.7z','*.rar','*.sqlite','*.db','*.log','*.sparkprofile')
$bad = @()
foreach ($pattern in $badExt) {
  $bad += Get-ChildItem -LiteralPath $root -Recurse -File -Filter $pattern -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\.git\' }
}
if ($bad.Count -gt 0) {
  Write-Host "Blocked binary/runtime files found:" -ForegroundColor Red
  $bad | Select-Object FullName,Length | Format-Table -AutoSize
  exit 1
}
$secretHits = rg -n -i "(token|secret|password|api[_-]?key|bearer|oauth|session)" "$root\overrides" 2>$null
if ($LASTEXITCODE -eq 0 -and $secretHits) {
  Write-Host "Review possible secret-like strings:" -ForegroundColor Yellow
  $secretHits
}
Write-Host "Release audit passed: no blocked binary/runtime files in source tree." -ForegroundColor Green

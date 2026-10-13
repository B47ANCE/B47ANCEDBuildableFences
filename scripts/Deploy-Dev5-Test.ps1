# Explicitly authorized local test deployment only. No launch or Workshop writes.
$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$sourceRoot = Join-Path $projectRoot 'src\B47ANCEDBuildableFences\42'
$overlayRoot = Join-Path $projectRoot 'prototypes\cohesive\42'
$modsRoot = 'C:\Users\willi\Zomboid\mods'
$testTarget = 'C:\Users\willi\Zomboid\mods\B47ANCEDBuildableFences'
$version = (Get-Content -LiteralPath (Join-Path $projectRoot 'VERSION') -Raw).Trim()
if ($version -ne '1.1.0-dev.5') { throw 'This bounded deployment requires source dev.5.' }
$resolvedMods = (Resolve-Path -LiteralPath $modsRoot).Path.TrimEnd('\')
$resolvedTarget = (Resolve-Path -LiteralPath $testTarget).Path.TrimEnd('\')
if ($resolvedTarget -ne ($resolvedMods + '\B47ANCEDBuildableFences')) { throw 'Unexpected test target.' }
if ((Get-Item -LiteralPath $testTarget).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Refusing a linked test target.' }
$beforeInfo = Get-Content -LiteralPath (Join-Path $testTarget '42\mod.info') -Raw
if ($beforeInfo -notmatch '(?m)^modversion=1\.1\.0-dev\.4\r?$') { throw 'Expected installed dev.4 before replacement.' }
$recordPath = Join-Path $projectRoot 'docs\evidence\test-deployment-dev.5.json'
if (Test-Path -LiteralPath $recordPath) { throw 'Deployment record already exists; do not overwrite historical evidence.' }
$stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
$backupBase = Join-Path $projectRoot 'docs\evidence\test-install-backups'
$backupRoot = [IO.Path]::GetFullPath((Join-Path $backupBase ('1.1.0-dev.4-' + $stamp)))
if (-not $backupRoot.StartsWith(([IO.Path]::GetFullPath($backupBase) + '\'), [StringComparison]::OrdinalIgnoreCase)) { throw 'Backup escaped intended directory.' }
$stageBase = Join-Path $projectRoot '.local-test-deploy'
$stageRoot = [IO.Path]::GetFullPath((Join-Path $stageBase ('dev.5-' + $stamp)))
if (-not $stageRoot.StartsWith(([IO.Path]::GetFullPath($stageBase) + '\'), [StringComparison]::OrdinalIgnoreCase)) { throw 'Stage escaped workspace.' }
if ((Test-Path -LiteralPath $backupRoot) -or (Test-Path -LiteralPath $stageRoot)) { throw 'Archive/stage already exists.' }
$expected = @{}
New-Item -ItemType Directory -Path (Join-Path $stageRoot '42'), (Join-Path $stageRoot 'common') -Force | Out-Null
foreach ($inputRoot in @($sourceRoot, $overlayRoot)) {
    foreach ($file in Get-ChildItem -LiteralPath $inputRoot -Recurse -File) {
        $relative = [IO.Path]::GetRelativePath($inputRoot, $file.FullName)
        $stageFile = Join-Path (Join-Path $stageRoot '42') $relative
        New-Item -ItemType Directory -Path ([IO.Path]::GetDirectoryName($stageFile)) -Force | Out-Null
        Copy-Item -LiteralPath $file.FullName -Destination $stageFile -Force
        $expected[$relative] = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash
    }
}
$obsolete = '42\media\lua\shared\B47_CohesiveCursor.lua'
$newCursor = '42\media\lua\server\B47_CohesiveCursor.lua'
if (Test-Path -LiteralPath (Join-Path $stageRoot $obsolete)) { throw 'Obsolete shared cursor in staged source.' }
if (-not (Test-Path -LiteralPath (Join-Path $stageRoot $newCursor))) { throw 'Missing server-phase cursor.' }
$afterInfo = Get-Content -LiteralPath (Join-Path $stageRoot '42\mod.info') -Raw
if ($afterInfo -notmatch '(?m)^modversion=1\.1\.0-dev\.5\r?$') { throw 'Wrong staged version.' }
foreach ($relative in $expected.Keys) {
    if ((Get-FileHash -LiteralPath (Join-Path (Join-Path $stageRoot '42') $relative) -Algorithm SHA256).Hash -ne $expected[$relative]) { throw "Stage hash mismatch: $relative" }
}
New-Item -ItemType Directory -Path $backupBase -Force | Out-Null
$consolePath = 'C:\Users\willi\Zomboid\console.txt'
$priorLog = Join-Path $projectRoot ('docs\evidence\pre-dev5-console-' + $stamp + '.txt')
if (Test-Path -LiteralPath $consolePath) { Copy-Item -LiteralPath $consolePath -Destination $priorLog }
# Checked absolute targets above; all moves use native PowerShell throughout.
Move-Item -LiteralPath $testTarget -Destination $backupRoot
try { Move-Item -LiteralPath $stageRoot -Destination $testTarget }
catch { if (-not (Test-Path -LiteralPath $testTarget)) { Move-Item -LiteralPath $backupRoot -Destination $testTarget }; throw }
$installed = @(Get-ChildItem -LiteralPath (Join-Path $testTarget '42') -Recurse -File)
if ($installed.Count -ne $expected.Count) { throw 'Installed file count differs.' }
$files = foreach ($file in $installed) {
    $relative = [IO.Path]::GetRelativePath((Join-Path $testTarget '42'), $file.FullName)
    $hash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash
    if ($hash -ne $expected[$relative]) { throw "Installed hash mismatch: $relative" }
    [ordered]@{ path = $relative; sha256 = $hash }
}
if (Test-Path -LiteralPath (Join-Path $testTarget $obsolete)) { throw 'Stale shared cursor survived deployment.' }
$record = [ordered]@{
    version = $version; timestamp_utc = $stamp; target = $testTarget
    prior_version = '1.1.0-dev.4'; prior_metadata = $beforeInfo; backup = $backupRoot
    source = $sourceRoot; overlay = $overlayRoot; deployed_metadata = $afterInfo
    obsolete_shared_cursor_absent = $true; server_cursor_present = $true
    file_count = $installed.Count; hash_verification = 'PASS'; files = @($files | Sort-Object path)
    common_directory = 'Empty, for Build 42 discovery'; workshop_files = 'Untouched'
    game_or_server_launched = $false; existing_game_process = 'Detected before deployment; restart required'
    runtime_loaded_version = 'UNKNOWN'; runtime_validation = 'NOT TESTED; manual retest required'
    previous_console_snapshot = $priorLog
}
$record | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $recordPath -Encoding utf8
Write-Output ('Deployed ' + $version + ' to ' + $testTarget)
Write-Output ('Archived prior test copy: ' + $backupRoot)
Write-Output ('Hash verified files: ' + $installed.Count)
Write-Output 'Obsolete shared cursor absent; server-phase cursor present. Native retest required.'

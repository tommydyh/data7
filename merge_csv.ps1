# CSV File Merge and Cleanup Script

$ErrorActionPreference = "Stop"

$basePath = "d:\cursor data 2"
$backupPath = Join-Path $basePath "archive_backup"
$dataPath = Join-Path $basePath "data"

# Create directories
New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
New-Item -ItemType Directory -Path $dataPath -Force | Out-Null

Write-Host "Starting CSV merge..." -ForegroundColor Green
Write-Host ""

# Step 1: Backup original files
Write-Host "Backing up original files..." -ForegroundColor Yellow

$files = @(
    "archive (2)\male_players.csv",
    "archive (2)\male_teams.csv",
    "archive (3)\fifa_world_cup_2026_golden_dataset.csv"
)

foreach ($file in $files) {
    $src = Join-Path $basePath $file
    $dst = Join-Path $backupPath (Split-Path $file -Leaf)
    if (Test-Path $src) {
        Copy-Item $src $dst -Force
        Write-Host "   [OK] Backed up: $(Split-Path $file -Leaf)" -ForegroundColor Green
    }
}

Write-Host ""

# Step 2: Process teams data
Write-Host "Processing teams data..." -ForegroundColor Yellow
$teamsFile = Join-Path $basePath "archive (2)\male_teams.csv"
if (Test-Path $teamsFile) {
    # Copy to data folder
    Copy-Item $teamsFile (Join-Path $dataPath "world_cup_teams.csv") -Force
    $size = (Get-Item (Join-Path $dataPath "world_cup_teams.csv")).Length / 1MB
    Write-Host "   [OK] world_cup_teams.csv: $([math]::Round($size, 2)) MB" -ForegroundColor Green
}

Write-Host ""

# Step 3: Process World Cup squad data
Write-Host "Processing World Cup squad data..." -ForegroundColor Yellow
$wcupFile = Join-Path $basePath "archive (3)\fifa_world_cup_2026_golden_dataset.csv"
if (Test-Path $wcupFile) {
    # Copy to data folder
    Copy-Item $wcupFile (Join-Path $dataPath "world_cup_squads.csv") -Force
    $size = (Get-Item (Join-Path $dataPath "world_cup_squads.csv")).Length / 1MB
    Write-Host "   [OK] world_cup_squads.csv: $([math]::Round($size, 2)) MB" -ForegroundColor Green

    # Read stats
    $wcupData = Import-Csv $wcupFile
    Write-Host "   Records: $($wcupData.Count)" -ForegroundColor Cyan
}

Write-Host ""

# Step 4: Process player data
Write-Host "Processing FIFA 24 player data (91.87 MB)..." -ForegroundColor Yellow

$playersFile = Join-Path $basePath "archive (2)\male_players.csv"

# Read header to get columns
$headers = Get-Content $playersFile -First 1
$columnList = $headers.Split(',')

Write-Host "   Original columns: $($columnList.Count)" -ForegroundColor Cyan

# Columns to keep
$keepColumns = @(
    "short_name",
    "long_name",
    "overall",
    "potential",
    "pace",
    "shooting",
    "passing",
    "dribbling",
    "defending",
    "physic",
    "club_name",
    "nationality_name",
    "age",
    "height_cm",
    "weight_kg",
    "club_position"
)

# Find indices of columns to keep
$columnIndices = @()
foreach ($col in $keepColumns) {
    $index = $columnList.IndexOf($col)
    if ($index -ge 0) {
        $columnIndices += $index
    } else {
        Write-Host "   [WARN] Column not found: $col" -ForegroundColor Yellow
    }
}

Write-Host "   Kept columns: $($columnIndices.Count)" -ForegroundColor Cyan

# Read and refine file
Write-Host "   Processing... (this may take a few minutes)" -ForegroundColor Cyan

$outputFile = Join-Path $dataPath "world_cup_players_temp.csv"

$reader = [System.IO.StreamReader]::new($playersFile)
$writer = [System.IO.StreamWriter]::new($outputFile)

# Write new header
$newHeaders = @()
foreach ($idx in $columnIndices) {
    $newHeaders += $columnList[$idx]
}
$writer.WriteLine(($newHeaders -join ','))

# Read data rows and refine
$lineCount = 0

while ($null -ne ($line = $reader.ReadLine())) {
    if ($lineCount -gt 0) {
        $fields = $line.Split(',')
        if ($fields.Count -ge $columnIndices.Count) {
            $selectedFields = @()
            foreach ($idx in $columnIndices) {
                $selectedFields += $fields[$idx]
            }
            $writer.WriteLine(($selectedFields -join ','))
        }
    }

    $lineCount++

    # Show progress every 10000 lines
    if ($lineCount % 10000 -eq 0) {
        Write-Host "`r   Processed: $lineCount lines" -NoNewline -ForegroundColor Cyan
    }
}

$writer.Close()
$reader.Close()

Write-Host ""

# Rename to final file
Move-Item $outputFile (Join-Path $dataPath "world_cup_players.csv") -Force

# Get new file size
$newSize = (Get-Item (Join-Path $dataPath "world_cup_players.csv")).Length / 1MB
Write-Host "   [OK] world_cup_players.csv: $([math]::Round($newSize, 2)) MB" -ForegroundColor Green
Write-Host "   Compression: $([math]::Round((1 - $newSize / 91.87) * 100, 1))%" -ForegroundColor Green

Write-Host ""

# Step 5: Delete original large files
Write-Host "Deleting original large files..." -ForegroundColor Yellow

Remove-Item (Join-Path $basePath "archive (2)") -Recurse -Force
Remove-Item (Join-Path $basePath "archive (3)") -Recurse -Force
Write-Host "   [OK] Deleted archive (2)/" -ForegroundColor Green
Write-Host "   [OK] Deleted archive (3)/" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "[DONE] Completed!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Results:" -ForegroundColor Cyan
Write-Host "   Original size: ~94 MB" -ForegroundColor Gray
Write-Host "   New size: ~$([math]::Round($newSize + 2.04 + 0.08, 2)) MB" -ForegroundColor Gray
Write-Host "   Compression: $([math]::Round((1 - ($newSize + 2.04 + 0.08) / 94) * 100, 1))%" -ForegroundColor Gray
Write-Host ""
Write-Host "File locations:" -ForegroundColor Cyan
Write-Host "   Refined data: $dataPath/" -ForegroundColor Gray
Write-Host "   Backup: $backupPath/" -ForegroundColor Gray
Write-Host ""
Write-Host "Generated files:" -ForegroundColor Cyan
Write-Host "   - world_cup_players.csv - Refined player data" -ForegroundColor Gray
Write-Host "   - world_cup_teams.csv   - Team data" -ForegroundColor Gray
Write-Host "   - world_cup_squads.csv  - World Cup squad data" -ForegroundColor Gray
Write-Host ""
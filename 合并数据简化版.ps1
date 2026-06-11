# CSV 文件合并与精简脚本（PowerShell 版本）

$ErrorActionPreference = "Stop"

$basePath = "d:\cursor data 2"
$backupPath = Join-Path $basePath "archive_backup"
$dataPath = Join-Path $basePath "data"

# 创建目录
New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
New-Item -ItemType Directory -Path $dataPath -Force | Out-Null

Write-Host "🚀 开始合并 CSV 文件..." -ForegroundColor Green
Write-Host ""

# 步骤 1: 备份原始文件
Write-Host "📦 备份原始文件..." -ForegroundColor Yellow

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
        Write-Host "   ✅ 备份: $(Split-Path $file -Leaf)" -ForegroundColor Green
    }
}

Write-Host ""

# 步骤 2: 读取团队数据（小文件，直接复制）
Write-Host "📊 处理团队数据..." -ForegroundColor Yellow
$teamsFile = Join-Path $basePath "archive (2)\male_teams.csv"
if (Test-Path $teamsFile) {
    # 只读取前 5 行查看结构
    $teamsSample = Get-Content $teamsFile -First 5
    Write-Host "   结构预览:"
    $teamsSample | ForEach-Object { Write-Host "      $_" -ForegroundColor Gray }

    # 复制到 data 文件夹
    Copy-Item $teamsFile (Join-Path $dataPath "world_cup_teams.csv") -Force
    $size = (Get-Item (Join-Path $dataPath "world_cup_teams.csv")).Length / 1MB
    Write-Host "   ✅ world_cup_teams.csv: $([math]::Round($size, 2)) MB" -ForegroundColor Green
}

Write-Host ""

# 步骤 3: 读取世界杯数据（小文件，直接复制）
Write-Host "📊 处理世界杯阵容数据..." -ForegroundColor Yellow
$wcupFile = Join-Path $basePath "archive (3)\fifa_world_cup_2026_golden_dataset.csv"
if (Test-Path $wcupFile) {
    # 复制到 data 文件夹
    Copy-Item $wcupFile (Join-Path $dataPath "world_cup_squads.csv") -Force
    $size = (Get-Item (Join-Path $dataPath "world_cup_squads.csv")).Length / 1MB
    Write-Host "   ✅ world_cup_squads.csv: $([math]::Round($size, 2)) MB" -ForegroundColor Green

    # 读取统计
    $wcupData = Import-Csv $wcupFile
    Write-Host "   记录数: $($wcupData.Count)" -ForegroundColor Cyan
}

Write-Host ""

# 步骤 4: 处理球员数据（大文件，需要精简）
Write-Host "📊 处理 FIFA 24 球员数据（91.87 MB）..." -ForegroundColor Yellow

$playersFile = Join-Path $basePath "archive (2)\male_players.csv"

# 读取头部获取列名
$headers = Get-Content $playersFile -First 1
$columnList = $headers.Split(',')

Write-Host "   原始列数: $($columnList.Count)" -ForegroundColor Cyan

# 保留的列（只保留关键属性）
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

# 找到这些列的索引
$columnIndices = @()
foreach ($col in $keepColumns) {
    $index = $columnList.IndexOf($col)
    if ($index -ge 0) {
        $columnIndices += $index
    } else {
        Write-Host "   ⚠️  未找到列: $col" -ForegroundColor Yellow
    }
}

Write-Host "   保留列数: $($columnIndices.Count)" -ForegroundColor Cyan

# 现在读取并精简文件
Write-Host "   正在精简...（这可能需要几分钟）" -ForegroundColor Cyan

$outputFile = Join-Path $dataPath "world_cup_players_temp.csv"

# 读取文件并写入精简版本
$reader = [System.IO.StreamReader]::new($playersFile)
$writer = [System.IO.StreamWriter]::new($outputFile)

# 写入新标题
$newHeaders = @()
foreach ($idx in $columnIndices) {
    $newHeaders += $columnList[$idx]
}
$writer.WriteLine(($newHeaders -join ','))

# 读取数据行并精简
$lineCount = 0
$totalBytes = (Get-Item $playersFile).Length
$processedBytes = 0

while ($null -ne ($line = $reader.ReadLine())) {
    if ($lineCount -gt 0) {  # 跳过标题行
        $fields = $line.Split(',')
        if ($fields.Count -ge $columnIndices.Count) {
            # 提取需要的列
            $selectedFields = @()
            foreach ($idx in $columnIndices) {
                $selectedFields += $fields[$idx]
            }
            $writer.WriteLine(($selectedFields -join ','))
        }
    }

    $lineCount++

    # 每 10000 行显示进度
    if ($lineCount % 10000 -eq 0) {
        $processedBytes = $reader.BaseStream.Position
        $percent = [math]::Round(($processedBytes / $totalBytes) * 100, 1)
        Write-Host "`r   进度: $lineCount 行 ($percent%)" -NoNewline -ForegroundColor Cyan
    }
}

$writer.Close()
$reader.Close()

Write-Host ""

# 重命名为最终文件
Move-Item $outputFile (Join-Path $dataPath "world_cup_players.csv") -Force

# 获取新文件大小
$newSize = (Get-Item (Join-Path $dataPath "world_cup_players.csv")).Length / 1MB
Write-Host "   ✅ world_cup_players.csv: $([math]::Round($newSize, 2)) MB" -ForegroundColor Green
Write-Host "   精简率: $([math]::Round((1 - $newSize / 91.87) * 100, 1))%" -ForegroundColor Green

Write-Host ""

# 步骤 5: 删除原始大文件
Write-Host "🗑️  删除原始大文件..." -ForegroundColor Yellow

Remove-Item (Join-Path $basePath "archive (2)") -Recurse -Force
Remove-Item (Join-Path $basePath "archive (3)") -Recurse -Force
Write-Host "   ✅ 已删除 archive (2)/" -ForegroundColor Green
Write-Host "   ✅ 已删除 archive (3)/" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "✅ 完成！" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "📊 结果统计:" -ForegroundColor Cyan
Write-Host "   原始总大小: ~94 MB" -ForegroundColor Gray
Write-Host "   精简后大小: ~$([math]::Round($newSize + 2.04 + 0.08, 2)) MB" -ForegroundColor Gray
Write-Host "   压缩率: $([math]::Round((1 - ($newSize + 2.04 + 0.08) / 94) * 100, 1))%" -ForegroundColor Gray
Write-Host ""
Write-Host "📁 文件位置:" -ForegroundColor Cyan
Write-Host "   精简数据: $dataPath/" -ForegroundColor Gray
Write-Host "   原始备份: $backupPath/" -ForegroundColor Gray
Write-Host ""
Write-Host "📋 生成的文件:" -ForegroundColor Cyan
Write-Host "   • world_cup_players.csv - 精简后的球员数据" -ForegroundColor Gray
Write-Host "   • world_cup_teams.csv   - 团队数据" -ForegroundColor Gray
Write-Host "   • world_cup_squads.csv  - 世界杯阵容数据" -ForegroundColor Gray
Write-Host ""
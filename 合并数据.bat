@echo off
chcp 65001 >nul
title 🔄 合并并精简 CSV 文件

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         🔄 合并 CSV 文件 - 生成精简数据集                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📋 此脚本将：
echo    • 读取 3 个 CSV 文件（共 ~94 MB）
echo    • 提取必要的列，删除无用数据
echo    • 生成精简数据集
echo    • 原始文件备份到 archive_backup/
echo    • 删除原始大文件
echo.
echo ⚠️  操作不可撤销，请确认！
echo.
echo ══════════════════════════════════════════════════════════════
echo.
set /p confirm=确认执行？(输入 Y 继续):

if /i not "%confirm%"=="Y" (
    echo.
    echo ❌ 操作已取消
    pause
    exit /b 0
)

echo.
echo ══════════════════════════════════════════════════════════════
echo 🚀 开始处理...
echo ══════════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

powershell -ExecutionPolicy Bypass -File "merge_csv.ps1"

if errorlevel 1 (
    echo.
    echo ❌ 处理失败！
) else (
    echo.
    echo ══════════════════════════════════════════════════════════════
    echo ✅ 处理完成！
    echo ══════════════════════════════════════════════════════════════
    echo.
    echo 📁 精简数据保存在: data/ 文件夹
    echo 📁 原始备份保存在: archive_backup/ 文件夹
    echo.
    echo 📋 下一步：
    echo    1. 检查 data/ 文件夹中的新文件
    echo    2. 测试仪表盘是否正常工作
    echo    3. 推送到 GitHub（文件变小了！）
    echo.
)

pause
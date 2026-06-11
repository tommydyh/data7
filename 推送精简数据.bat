@echo off
chcp 65001 >nul
title 📤 推送精简数据到 GitHub

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         📤 推送精简数据到 GitHub                          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📊 数据精简完成！
echo    原始大小: 94 MB
echo    精简大小: 19.13 MB
echo    压缩率: 79.6%
echo.
echo 📁 生成的文件:
echo    data/world_cup_players.csv  (17.01 MB)
echo    data/world_cup_teams.csv    (2.04 MB)
echo    data/world_cup_squads.csv   (0.08 MB)
echo.
echo ══════════════════════════════════════════════════════════════
echo.
set /p confirm=确认推送到 GitHub？(输入 Y 继续):

if /i not "%confirm%"=="Y" (
    echo.
    echo ❌ 操作已取消
    pause
    exit /b 0
)

echo.
echo ══════════════════════════════════════════════════════════════
echo 🚀 开始推送...
echo ══════════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

REM 检查 Git
where git >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到 Git，请先安装
    pause
    exit /b 1
)

echo ✅ Git 已就绪
echo.

REM 添加所有更改
echo 📂 正在添加文件...
git add .

if errorlevel 1 (
    echo ❌ Git add 失败
    pause
    exit /b 1
)

echo ✅ 文件已添加
echo.

REM 创建提交
echo 💾 正在创建提交...
git commit -m "feat: 添加精简的 2026 World Cup 数据集

- 合并 3 个 CSV 文件
- 精简球员数据（109 列 -> 16 列）
- 压缩率: 79.6%（94 MB -> 19.13 MB）
- 修复 Streamlit Cloud 部署路径问题
- 添加云端环境路径检测"

if errorlevel 1 (
    echo ℹ️  没有新的更改
)

echo.
echo ══════════════════════════════════════════════════════════════
echo 🚀 正在推送到 GitHub...
echo ══════════════════════════════════════════════════════════════
echo.

git push origin main

if errorlevel 1 (
    echo.
    echo ❌ 推送失败！
    echo.
    echo 可能原因：
    echo 1. 需要输入 GitHub 凭证
    echo 2. 网络连接问题
    echo.
    echo 请检查后重试
) else (
    echo.
    echo ══════════════════════════════════════════════════════════════
    echo ✅ 推送成功！
    echo ══════════════════════════════════════════════════════════════
    echo.
    echo 📋 下一步：在 Streamlit Cloud 重新部署
    echo.
    echo 1. 访问：https://share.streamlit.io
    echo 2. 找到您的应用
    echo 3. 点击 "Manage app"
    echo 4. 点击 "Re-deploy"
    echo.
    echo 🎉 应该可以成功部署了！
    echo.
    echo 🔗 您的仓库：
    echo    https://github.com/tommydyh/dongyaohua-sport-task
)

echo.
pause
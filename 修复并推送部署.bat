@echo off
chcp 65001 >nul
title 🔧 修复 Streamlit Cloud 部署问题

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         🔧 修复 Streamlit Cloud 部署路径问题                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo ❌ 问题：Streamlit Cloud 找不到 world_cup_squads.csv
echo ✅ 修复：更新 get_data_path() 正确处理 data/ 子目录
echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo 📋 修复内容：
echo    • 更新 src/data_pipeline.py 中的路径解析逻辑
echo    • 云端环境现在正确返回 data/world_cup_squads.csv
echo    • 本地环境仍然正常工作
echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo 🚀 正在准备推送到 GitHub...
echo.

cd /d "%~dp0"

REM 检查 Git
where git >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到 Git
    pause
    exit /b 1
)

echo ✅ Git 已就绪
echo.

REM 添加修改的文件
echo 📂 正在添加文件...
git add src/data_pipeline.py

if errorlevel 1 (
    echo ❌ Git add 失败
    pause
    exit /b 1
)

echo ✅ 文件已添加
echo.

REM 创建提交
echo 💾 正在创建提交...
git commit -m "fix: 修正 Streamlit Cloud 部署路径问题

- 更新 get_data_path() 以正确处理 data/ 子目录
- 修复云端环境下文件路径解析错误
- 支持本地和云端环境的路径自动检测

Error: FileNotFoundError on world_cup_squads.csv
Fix: 现在正确返回 data/world_cup_squads.csv

Refs: course-data-4 Streamlit Cloud deployment"

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
    echo 3. 代理设置问题（已修复）
    echo.
    echo 请检查后重试
) else (
    echo.
    echo ══════════════════════════════════════════════════════════════
    echo ✅ 推送成功！
    echo ══════════════════════════════════════════════════════════════
    echo.
    echo 📋 Streamlit Cloud 将自动重新部署
    echo.
    echo 🔗 您的应用地址：
    echo    https://course-data-4-xkgwklnkppxuyfm8kkkqrw.streamlit.app/
    echo.
    echo 📊 预计 1-2 分钟后可访问
    echo.
    echo 🎉 部署完成后，错误应该解决了！
)

echo.
pause
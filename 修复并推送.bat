@echo off
chcp 65001 >nul
title 🔧 修复并推送到 GitHub

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         🔧 修复 Streamlit Cloud 部署问题                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo ✅ 已修复的问题：
echo    - 硬编码路径 → 改为相对路径
echo    - 缺少依赖 → 已添加到 requirements.txt
echo    - secrets.toml → 已创建
echo    - GitHub Actions → 已更新配置
echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo 📤 正在准备推送修复...
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
git commit -m "fix: 修复 Streamlit Cloud 部署问题

- 修复硬编码的 Windows 路径
- 添加缺失的依赖（joblib, threadpoolctl）
- 更新 GitHub Actions CI 配置
- 创建 .streamlit/secrets.toml
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
    echo ✅ 修复已成功推送到 GitHub！
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
)

echo.
pause
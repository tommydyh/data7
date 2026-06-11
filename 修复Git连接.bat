@echo off
chcp 65001 >nul
title 🔧 修复 Git 连接问题

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         🔧 修复 Git 连接 GitHub 的问题                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo ❌ 问题：Git 配置了代理，但代理无法连接
echo.
echo 📋 日志显示的错误：
echo    • Failed to connect to github.com port 443 via 127.0.0.1
echo    • Could not resolve proxy: socks5
echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo 🚀 正在修复...
echo.

cd /d "%~dp0"

REM 检查当前代理配置
echo 📊 检查 Git 代理配置...
git config --global --get http.proxy
git config --global --get https.proxy

echo.
echo ─────────────────────────────────────────────────────────────
echo.
echo 🛠️  取消 Git 代理设置...
echo.

REM 取消代理设置
git config --global --unset http.proxy 2>nul
git config --global --unset https.proxy 2>nul

echo ✅ 已取消代理设置
echo.

REM 显示当前配置
echo 📊 当前 Git 配置：
echo.
echo    Remote URL:
git config --get remote.origin.url
echo.

echo ─────────────────────────────────────────────────────────────
echo.
echo 🧪 测试连接...
echo.

git ls-remote https://github.com/tommydyh/dongyaohua-sport-task.git HEAD

if errorlevel 1 (
    echo.
    echo ❌ 连接测试失败！
    echo.
    echo 可能原因：
    echo 1. 网络连接问题
    echo 2. VPN 未正确配置
    echo 3. 需要手动配置正确的代理
    echo.
) else (
    echo.
    echo ══════════════════════════════════════════════════════════════
    echo ✅ 修复成功！
    echo ══════════════════════════════════════════════════════════════
    echo.
    echo 📋 现在可以正常推送到 GitHub 了！
    echo.
    echo 🚀 尝试推送：
    echo    git push origin main
    echo.
    echo 或双击运行：推送精简数据.bat
    echo.
)

pause
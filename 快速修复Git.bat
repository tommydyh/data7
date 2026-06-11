@echo off
chcp 65001 >nul
title 🔧 快速修复 Git

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         🔧 快速修复 Git 连接问题                           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 问题：Git 配置了代理，但代理无法连接
echo 解决：取消 Git 代理设置
echo.

cd /d "%~dp0"

echo 🛠️  正在取消代理设置...
git config --global --unset http.proxy 2>nul
git config --global --unset https.proxy 2>nul

if errorlevel 1 (
    echo ℹ️  未设置代理
) else (
    echo ✅ 已取消代理
)

echo.
echo 🧪 测试连接...

git ls-remote https://github.com/tommydyh/dongyaohua-sport-task.git HEAD >nul 2>&1

if errorlevel 1 (
    echo.
    echo ❌ 连接失败
    echo.
    echo 请尝试：
    echo 1. 检查 VPN 是否开启
    echo 2. 检查网络连接
    echo 3. 查看 Git连接问题修复.md
    echo.
) else (
    echo.
    echo ══════════════════════════════════════════════════════════════
    echo ✅ 连接成功！
    echo ══════════════════════════════════════════════════════════════
    echo.
    echo 🚀 现在可以推送代码了！
    echo.
    echo    双击：推送精简数据.bat
    echo.
    pause
    exit /b 0
)

pause
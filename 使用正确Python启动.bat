@echo off
chcp 65001 >nul
title 🚀 使用正确 Python 启动仪表盘

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         🚀 2026 World Cup Dashboard - 启动                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo ✅ 使用正确的 Python 环境
echo.
echo 📋 Python 信息:
echo    路径: D:\python\python.exe
echo    版本: Python 3.13.9 (Anaconda)
echo.
echo 📦 已安装的库:
echo    • streamlit: 1.51.0
echo    • pandas: 2.3.3
echo    • numpy: 2.3.5
echo    • sklearn: 1.7.2
echo    • plotly: 6.3.0
echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo 🚀 正在启动仪表盘...
echo.

cd /d "%~dp0"

D:\python\python.exe -m streamlit run app.py

if errorlevel 1 (
    echo.
    echo ❌ 启动失败！
    echo.
    echo 可能原因:
    echo 1. 缺少某些依赖
    echo 2. 数据文件未找到
    echo.
    echo 解决方案:
    echo    D:\python\python.exe -m pip install -r requirements.txt
    echo.
) else (
    echo.
    echo ✅ 仪表盘已关闭
)

pause
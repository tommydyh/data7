@echo off
chcp 65001 >nul
title 🧪 测试 Dashboard

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         🧪 测试 2026 World Cup Dashboard                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 正在运行测试...
echo.

cd /d "%~dp0"

python test_dashboard.py

if errorlevel 1 (
    echo.
    echo ❌ 测试失败！
    echo.
    echo 请检查上面的错误信息。
) else (
    echo.
    echo ══════════════════════════════════════════════════════════════
    echo ✅ 测试成功！
    echo ══════════════════════════════════════════════════════════════
    echo.
    echo 🚀 现在可以启动仪表盘了：
    echo.
    echo    双击：启动仪表盘.bat
    echo    或运行：streamlit run app.py
    echo.
)

pause
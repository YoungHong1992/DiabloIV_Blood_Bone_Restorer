@echo off
chcp 65001 >nul
title 一键启用暗黑破坏神IV Agent模式
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🔥 暗黑破坏神IV Agent模式一键启用器 🔥         ║
echo ║                                                              ║
echo ║  ⚡ 超级简单: 双击运行，一键完成                             ║
echo ║  🔒 安全可靠: 只创建配置文件，不修改游戏文件                 ║
echo ║  📱 用户友好: 专为小白用户设计                               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: 询问用户是否直接开始
echo 🚀 即将自动检测游戏目录并配置Agent模式
echo.
set /p start_now="按Enter键开始配置，或输入n取消: "
if /i "%start_now%"=="n" goto :end

echo.
echo 🔍 正在自动检测游戏安装目录...
echo.

:: 快速路径检测
set "game_dir="
for %%p in ("%ProgramFiles%\Battle.net\Diablo IV" "%ProgramFiles(x86)%\Battle.net\Diablo IV") do (
    if exist "%%~p" (
        set "game_dir=%%~p"
        goto :found
    )
)

:found
if "%game_dir%"=="" (
    echo ❌ 自动检测失败
    echo.
    echo 💡 请确保暗黑破坏神IV已正确安装
    echo    标准安装路径:
    echo    • C:\Program Files\Battle.net\Diablo IV\
    echo    • C:\Program Files (x86)\Battle.net\Diablo IV\
    echo.
    echo 📂 请手动输入安装目录:
    set /p game_dir="请输入路径 (如: C:\Program Files\Battle.net\Diablo IV): "
    if "%game_dir%"=="" goto :end
    if not exist "%game_dir%" (
        echo ❌ 目录不存在: %game_dir%
        goto :end
    )
)

echo ✅ 找到游戏目录: %game_dir%
echo.

:: 快速配置
echo ⚡ 正在自动配置Agent模式...
set "wtf_dir=%game_dir%\WTF"
set "config_file=%wtf_dir%\Config.wtf"

echo 📁 创建配置目录...
if not exist "%wtf_dir%" mkdir "%wtf_dir%"

echo 📄 创建配置文件...
echo SET OverrideArchive "0" > "%config_file%"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                      ✅ 配置完成！                            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🎯 接下来请按顺序操作:
echo.
echo 1️⃣  打开战网客户端
echo 2️⃣  点击 左上角战网标志 → 选项 → 游戏设置
echo 3️⃣  找到"暗黑破坏神IV"并点击
echo 4️⃣  勾选"额外命令行参数" 
echo 5️⃣  输入参数: -enableagentmanager
echo 6️⃣  点击"应用"或"确定"
echo.
echo 🚀 完成！现在可以启动游戏享受Agent模式了！
echo.

:: 询问是否打开战网
set /p launch_bnet="是否现在打开战网客户端? (y/n): "
if /i "%launch_bnet%"=="y" (
    start "" "C:\Program Files (x86)\Battle.net\Battle.net.exe" 2>nul || start "" "C:\Program Files\Battle.net\Battle.net.exe" 2>nul
    if errorlevel 1 (
        echo.
        echo ℹ️  手动打开战网客户端即可
    )
)

echo.
echo 感谢使用！按任意键退出...
pause >nul

:end
cls
echo.
echo 👋 欢迎回来！需要帮助请联系相关文档
pause >nul
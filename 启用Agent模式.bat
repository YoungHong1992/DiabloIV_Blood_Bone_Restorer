@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ==========================================
:: 暗黑破坏神IV Agent模式启用器 - 轻量版
:: 版本: 1.0
:: 开发者: MiniMax Agent
:: 日期: 2025-11-10
:: ==========================================

title 暗黑破坏神IV Agent模式启用器
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                暗黑破坏神IV Agent模式启用器                  ║
echo ║                        轻量版 v1.0                          ║
echo ║                                                              ║
echo ║  本工具将帮您自动配置暗黑破坏神IV的Agent模式                 ║
echo ║  让您可以安全地使用游戏助手功能                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  检测到非管理员权限
    echo.
    echo 📋 建议以管理员身份运行本工具以确保正常创建文件
    echo 📋 右键点击本文件，选择"以管理员身份运行"
    echo.
    set /p continue="是否继续运行? (y/n): "
    if /i "!continue!" neq "y" goto :end
    echo.
)

:: 搜索暗黑破坏神IV安装目录
echo 🔍 正在搜索暗黑破坏神IV安装目录...
echo.

set "found_paths="
set "search_paths[0]=%ProgramFiles%\Battle.net\Diablo IV"
set "search_paths[1]=%ProgramFiles(x86)%\Battle.net\Diablo IV"

:: 检查64位路径
if exist "%ProgramFiles%\Battle.net\Diablo IV" (
    set "diablo_path=%ProgramFiles%\Battle.net\Diablo IV"
    set "found_paths=!found_paths! ✓ %ProgramFiles%\Battle.net\Diablo IV!LF!"
    echo ✅ 找到游戏目录: %ProgramFiles%\Battle.net\Diablo IV
)

:: 检查32位路径
if exist "%ProgramFiles(x86)%\Battle.net\Diablo IV" (
    if "!diablo_path!"=="" (
        set "diablo_path=%ProgramFiles(x86)%\Battle.net\Diablo IV"
        set "found_paths=!found_paths! ✓ %ProgramFiles(x86)%\Battle.net\Diablo IV!LF!"
        echo ✅ 找到游戏目录: %ProgramFiles(x86)%\Battle.net\Diablo IV
    )
)

:: 如果都没找到，让用户手动选择
if "!diablo_path!"=="" (
    echo ❌ 未找到自动检测到游戏安装目录
    echo.
    echo 📂 请手动选择暗黑破坏神IV的安装目录
    echo.
    set /p diablo_path="请输入游戏安装目录路径 (或按Enter跳过): "
    if "!diablo_path!"=="" (
        echo.
        echo ℹ️  您可以稍后手动运行本工具或使用以下路径参考:
        echo    - C:\Program Files\Battle.net\Diablo IV\
        echo    - C:\Program Files (x86)\Battle.net\Diablo IV\
        echo.
        set /p manual_input="按Enter键退出或输入任意键继续: "
        goto :end
    )
)

:: 验证目录有效性
if not exist "!diablo_path!" (
    echo ❌ 指定的目录不存在: !diablo_path!
    set /p retry="是否要重新输入路径? (y/n): "
    if /i "!retry!"=="y" goto :input_path
    goto :end
)

echo.
echo 📂 使用游戏目录: !diablo_path!
echo.

:: 确认继续
set /p confirm="确认要在此目录启用Agent模式吗? (y/n): "
if /i "!confirm!" neq "y" (
    echo.
    echo ℹ️  操作已取消
    goto :end
)

echo.
echo 🔧 正在配置Agent模式，请稍候...
echo.

:: 步骤1: 创建WTF目录
set "wtf_path=!diablo_path!\WTF"
echo [1/4] 创建WTF目录...
if not exist "!wtf_path!" (
    mkdir "!wtf_path!" 2>nul
    if !errorlevel! neq 0 (
        echo ❌ 创建WTF目录失败，请检查权限
        goto :end
    )
    echo ✅ WTF目录创建成功
) else (
    echo ✅ WTF目录已存在
)

:: 步骤2: 创建Config.wtf文件
set "config_path=!wtf_path!\Config.wtf"
echo [2/4] 创建Config.wtf配置文件...
echo SET OverrideArchive "0" > "!config_path!"
if !errorlevel! neq 0 (
    echo ❌ 创建配置文件失败
    goto :end
)
echo ✅ Config.wtf文件创建成功

:: 步骤3: 验证文件内容
echo [3/4] 验证配置文件...
if not exist "!config_path!" (
    echo ❌ 配置文件验证失败
    goto :end
)

for /f "tokens=*" %%i in ('type "!config_path!" 2^>nul') do set "file_content=%%i"
if "!file_content!"=="SET OverrideArchive \"0\"" (
    echo ✅ 配置文件内容验证成功
) else (
    echo ❌ 配置文件内容不正确
    echo 当前内容: !file_content!
    goto :end
)

:: 步骤4: 显示结果
echo [4/4] 配置完成！
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                     ✅ 自动配置完成                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📁 创建的文件:
echo    目录: !wtf_path!
echo    文件: !config_path!
echo.

echo ⚠️  重要提醒: 还有最后一步需要您手动完成！
echo.
echo 📋 手动操作步骤:
echo    1. 打开战网客户端
echo    2. 进入: 游戏设置 ^> 暗黑破坏神IV
echo    3. 勾选: "额外命令行参数"
echo    4. 添加参数: -enableagentmanager
echo    5. 点击"完成"按钮
echo.
echo 🚀 配置完成后即可启动游戏享受Agent模式！
echo.

:: 询问是否打开战网客户端设置页面
set /p open_settings="是否要帮您打开战网客户端? (y/n): "
if /i "!open_settings!"=="y" (
    start "" "C:\Program Files (x86)\Battle.net\Battle.net.exe" || start "" "C:\Program Files\Battle.net\Battle.net.exe"
    if !errorlevel! neq 0 (
        echo.
        echo ⚠️  无法自动打开战网客户端，请手动打开
        echo    安装路径可能不是默认路径
    )
)

:: 询问是否查看配置文件
set /p view_config="是否要查看创建的配置文件? (y/n): "
if /i "!view_config!"=="y" (
    echo.
    echo 📄 配置文件内容:
    echo ═════════════════════════════════════════════════════════════
    type "!config_path!"
    echo ═════════════════════════════════════════════════════════════
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                      配置摘要                                ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║ 游戏目录: !diablo_path!                     ║
echo ║ WTF目录 : !wtf_path!         ║
echo ║ 配置文件: Config.wtf                       ║
echo ║ 文件内容: SET OverrideArchive "0"           ║
echo ║ 状态     : ✅ 配置完成                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🎉 恭喜！Agent模式自动配置已完成！
echo    只需按上述步骤配置战网客户端即可开始使用！
echo.

:end
echo.
echo 感谢使用暗黑破坏神IV Agent模式启用器！
echo 按任意键退出...
pause >nul
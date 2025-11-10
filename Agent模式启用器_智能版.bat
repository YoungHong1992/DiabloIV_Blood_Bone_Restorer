@echo off
setlocal DisableDelayedExpansion
:: ==========================================
:: Diablo IV Agent Mode Enabler - Smart Edition
:: Compatible with multiple language Windows
:: Version: 1.1
:: ==========================================

title Diablo IV Agent Mode Enabler
color 0A

echo.
echo ============================================================
echo           Diablo IV Agent Mode Enabler
echo ============================================================
echo.

:: Detect system language
for /f "tokens=3" %%a in ('wmic os get OSLanguage /value 2^>nul') do set "sys_lang=%%a"

if "%sys_lang%"=="2052" (
    :: Chinese Simplified
    chcp 936 >nul 2>&1
    goto :chinese
) else (
    :: English or other languages
    chcp 1252 >nul 2>&1
    goto :english
)

:chinese
echo [自动检测] 检测到简体中文系统
echo.
echo 正在搜索暗黑破坏神IV安装目录...
echo.

set "found_paths="
set "search_paths[0]=%ProgramFiles%\Battle.net\Diablo IV"
set "search_paths[1]=%ProgramFiles(x86)%\Battle.net\Diablo IV"

if exist "%ProgramFiles%\Battle.net\Diablo IV" (
    set "diablo_path=%ProgramFiles%\Battle.net\Diablo IV"
    echo [成功] 找到游戏目录: %ProgramFiles%\Battle.net\Diablo IV
    goto :config
)

if exist "%ProgramFiles(x86)%\Battle.net\Diablo IV" (
    set "diablo_path=%ProgramFiles(x86)%\Battle.net\Diablo IV"
    echo [成功] 找到游戏目录: %ProgramFiles(x86)%\Battle.net\Diablo IV
    goto :config
)

echo [错误] 未找到自动检测到游戏安装目录
echo.
echo 请手动选择暗黑破坏神IV的安装目录
set /p diablo_path="请输入游戏安装目录路径: "
if "!diablo_path!"=="" goto :end
if not exist "!diablo_path!" (
    echo [错误] 指定的目录不存在: !diablo_path!
    goto :end
)
echo [成功] 使用目录: !diablo_path!
goto :config

:english
echo [Auto Detect] English system detected
echo.
echo Searching for Diablo IV installation directory...
echo.

set "diablo_path="
if exist "%ProgramFiles%\Battle.net\Diablo IV" (
    set "diablo_path=%ProgramFiles%\Battle.net\Diablo IV"
    echo [Success] Found: %ProgramFiles%\Battle.net\Diablo IV
    goto :config
)

if exist "%ProgramFiles(x86)%\Battle.net\Diablo IV" (
    set "diablo_path=%ProgramFiles(x86)%\Battle.net\Diablo IV
    echo [Success] Found: %ProgramFiles(x86)%\Battle.net\Diablo IV
    goto :config
)

echo [Error] Could not find game installation
echo.
echo Please enter Diablo IV installation path manually
set /p diablo_path="Enter path: "
if "%diablo_path%"=="" goto :end
if not exist "%diablo_path%" (
    echo [Error] Directory not found: %diablo_path%
    goto :end
)
echo [Success] Using: %diablo_path%
goto :config

:config
echo.
echo ============================================================
echo                  Configuration Progress
echo ============================================================
echo.

:: Create WTF directory
set "wtf_path=!diablo_path!\WTF"
echo Creating WTF directory...
if not exist "!wtf_path!" (
    mkdir "!wtf_path!" 2>nul
    if !errorlevel! neq 0 (
        echo [Error] Failed to create directory
        goto :end
    )
    echo [Success] WTF directory created
) else (
    echo [Success] WTF directory already exists
)

:: Create Config.wtf
set "config_path=!wtf_path!\Config.wtf"
echo Creating Config.wtf...
echo SET OverrideArchive "0" > "!config_path!"
if !errorlevel! neq 0 (
    echo [Error] Failed to create config file
    goto :end
)
echo [Success] Config.wtf created

echo.
echo ============================================================
echo                    Configuration Complete!
echo ============================================================
echo.

if "%sys_lang%"=="2052" (
    echo 下一步操作:
    echo 1. 打开战网客户端
    echo 2. 游戏设置 ^> 暗黑破坏神IV
    echo 3. 勾选"额外命令行参数"
    echo 4. 输入: -enableagentmanager
    echo 5. 点击确定
    echo.
    echo 按任意键退出...
) else (
    echo Next steps:
    echo 1. Open Battle.net client
    echo 2. Game Settings ^> Diablo IV
    echo 3. Check "Additional command line arguments"
    echo 4. Enter: -enableagentmanager
    echo 5. Click OK
    echo.
    echo Press any key to exit...
)

pause >nul
goto :end

:end
cls
echo.
if "%sys_lang%"=="2052" (
    echo 感谢使用！
) else (
    echo Thank you for using!
)
echo.

@echo off
rem =====================================================
rem Diablo IV Agent Mode Setup - Simple English Version
rem Compatible with ALL Windows versions
rem =====================================================

title Diablo4 Agent Setup
color 0A

echo.
echo Diablo IV Agent Mode Setup
echo ============================
echo.

echo Step 1: Finding game directory...
echo.

set GAME_DIR=
if exist "C:\Program Files\Battle.net\Diablo IV" (
    set GAME_DIR=C:\Program Files\Battle.net\Diablo IV
    echo Found: C:\Program Files\Battle.net\Diablo IV
    goto :make_config
)

if exist "C:\Program Files (x86)\Battle.net\Diablo IV" (
    set GAME_DIR=C:\Program Files (x86)\Battle.net\Diablo IV
    echo Found: C:\Program Files (x86)\Battle.net\Diablo IV
    goto :make_config
)

echo.
echo Auto-detection failed.
echo Please enter Diablo IV installation path:
set /p GAME_DIR="Path: "

if "%GAME_DIR%"=="" goto :end
if not exist "%GAME_DIR%" (
    echo ERROR: Directory not found
    goto :end
)

:make_config
echo.
echo Step 2: Creating config files...
echo.

set WTF_DIR=%GAME_DIR%\WTF
if not exist "%WTF_DIR%" (
    mkdir "%WTF_DIR%"
    if errorlevel 1 (
        echo ERROR: Cannot create directory
        goto :end
    )
    echo Created: %WTF_DIR%
) else (
    echo Exists: %WTF_DIR%
)

set CONFIG_FILE=%WTF_DIR%\Config.wtf
echo SET OverrideArchive "0" > "%CONFIG_FILE%"
if errorlevel 1 (
    echo ERROR: Cannot create file
    goto :end
)
echo Created: %CONFIG_FILE%

echo.
echo SUCCESS! Configuration complete.
echo.
echo Next steps:
echo 1. Open Battle.net
echo 2. Options ^> Game Settings
echo 3. Select Diablo IV
echo 4. Check "Additional command line arguments"
echo 5. Enter: -enableagentmanager
echo 6. Click OK
echo.
echo Configuration files created:
echo   Directory: %WTF_DIR%
echo   File: Config.wtf
echo.

set /p OPEN="Open Battle.net now? (y/n): "
if /i "%OPEN%"=="y" (
    start "" "C:\Program Files (x86)\Battle.net\Battle.net.exe" 2>nul
    start "" "C:\Program Files\Battle.net\Battle.net.exe" 2>nul
)

echo.
echo Done. Press any key to exit.
pause >nul

:end
cls
echo.
echo Goodbye!
echo.

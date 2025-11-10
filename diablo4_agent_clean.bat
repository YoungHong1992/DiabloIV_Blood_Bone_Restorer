@echo off
rem =====================================================
rem Diablo IV Agent Setup - Clean ASCII Version
rem =====================================================

title Diablo IV Agent Setup
color 0A

echo.
echo ===========================================
echo      Diablo IV Agent Mode Setup
echo ===========================================
echo.

echo [Step 1] Finding Diablo IV directory...
echo.

set GAME_PATH=
if exist "C:\Program Files\Battle.net\Diablo IV" (
    set GAME_PATH=C:\Program Files\Battle.net\Diablo IV
    echo Found: C:\Program Files\Battle.net\Diablo IV
    goto :create_files
)

if exist "C:\Program Files (x86)\Battle.net\Diablo IV" (
    set GAME_PATH=C:\Program Files (x86)\Battle.net\Diablo IV
    echo Found: C:\Program Files (x86)\Battle.net\Diablo IV
    goto :create_files
)

echo.
echo [Info] Auto-detection failed
echo Please enter the full path to Diablo IV:
set /p GAME_PATH="Path: "

if "%GAME_PATH%"=="" goto :exit
if not exist "%GAME_PATH%" (
    echo [Error] Directory not found
    goto :exit
)

:create_files
echo.
echo [Step 2] Creating configuration...
echo.

set WTF_PATH=%GAME_PATH%\WTF
if not exist "%WTF_PATH%" (
    mkdir "%WTF_PATH%"
    if errorlevel 1 (
        echo [Error] Cannot create WTF directory
        echo Check if you have administrator rights
        goto :exit
    )
    echo [OK] Created: %WTF_PATH%
) else (
    echo [OK] Directory exists: %WTF_PATH%
)

set CONFIG_PATH=%WTF_PATH%\Config.wtf
echo SET OverrideArchive "0" > "%CONFIG_PATH%"
if errorlevel 1 (
    echo [Error] Cannot create config file
    goto :exit
)
echo [OK] Created: %CONFIG_PATH%

echo.
echo ===========================================
echo         Configuration Complete!
echo ===========================================
echo.
echo Files created:
echo   Directory: %WTF_PATH%
echo   File name: Config.wtf
echo   Content  : SET OverrideArchive "0"
echo.
echo Next steps to enable Agent mode:
echo.
echo 1. Open Battle.net desktop app
echo 2. Go to: Options ^> Game Settings
echo 3. Find "Diablo IV" in the list
echo 4. Check "Additional command line arguments"
echo 5. Type: -enableagentmanager
echo 6. Click OK
echo.
echo ===========================================
echo.

set /p OPEN="Open Battle.net now? (y/n): "
if /i "%OPEN%"=="y" (
    start "" "C:\Program Files (x86)\Battle.net\Battle.net.exe" 2>nul
    start "" "C:\Program Files\Battle.net\Battle.net.exe" 2>nul
    echo [Info] Attempted to open Battle.net
)

echo.
echo Setup complete! Press any key to exit.
pause >nul 2>&1

:exit
cls
echo.
echo Thank you for using this tool!
echo.

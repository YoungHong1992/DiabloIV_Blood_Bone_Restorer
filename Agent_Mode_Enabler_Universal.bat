@echo off
chcp 437 >nul 2>&1
title Diablo IV Agent Mode Enabler - Universal Edition
color 0B

echo.
echo ================================================================
echo                Diablo IV Agent Mode Enabler
echo                     Universal Edition
echo ================================================================
echo.
echo This tool works on ANY Windows system (English/Chinese/etc)
echo No encoding issues, no character problems
echo.

echo.
echo [1/3] Searching for Diablo IV installation...
echo.

set "diablo_path="
if exist "%ProgramFiles%\Battle.net\Diablo IV" (
    set "diablo_path=%ProgramFiles%\Battle.net\Diablo IV"
    echo [OK] Found: %ProgramFiles%\Battle.net\Diablo IV
    goto :create_config
)

if exist "%ProgramFiles(x86)%\Battle.net\Diablo IV" (
    set "diablo_path=%ProgramFiles(x86)%\Battle.net\Diablo IV
    echo [OK] Found: %ProgramFiles(x86)%\Battle.net\Diablo IV
    goto :create_config
)

echo.
echo [WARNING] Could not auto-detect game
echo.
echo Please enter the full path to Diablo IV installation directory
echo (e.g., C:\Program Files\Battle.net\Diablo IV)
echo.
set /p diablo_path="Enter path: "

if "%diablo_path%"=="" (
    echo [CANCEL] Operation cancelled
    goto :end
)

if not exist "%diablo_path%" (
    echo [ERROR] Directory does not exist: %diablo_path%
    goto :end
)

echo [OK] Using: %diablo_path%

:create_config
echo.
echo ================================================================
echo [2/3] Creating configuration files...
echo ================================================================
echo.

:: Create WTF directory
set "wtf_dir=%diablo_path%\WTF"
echo Creating directory: %wtf_dir%
if not exist "%wtf_dir%" (
    mkdir "%wtf_dir%" 2>nul
    if errorlevel 1 (
        echo [ERROR] Failed to create directory (check permissions)
        goto :end
    )
    echo [OK] Directory created successfully
) else (
    echo [OK] Directory already exists
)

:: Create Config.wtf
set "config_file=%wtf_dir%\Config.wtf"
echo.
echo Creating file: %config_file%
echo SET OverrideArchive "0" > "%config_file%"
if errorlevel 1 (
    echo [ERROR] Failed to create config file
    goto :end
)
echo [OK] Config file created successfully

echo.
echo ================================================================
echo [3/3] Configuration Complete!
echo ================================================================
echo.
echo [SUCCESS] All files created successfully
echo.
echo File details:
echo   Directory: %wtf_dir%
echo   File Name: Config.wtf
echo   Content  : SET OverrideArchive "0"
echo.
echo ================================================================
echo                    NEXT STEPS
echo ================================================================
echo.
echo To enable Agent Mode in Diablo IV, please follow these steps:
echo.
echo 1. Open Battle.net desktop app
echo 2. Click: Battle.net icon (top left) ^> Options ^> Game Settings
echo 3. Find "Diablo IV" in the list
echo 4. Check the box: "Additional command line arguments"
echo 5. In the text field, enter: -enableagentmanager
echo 6. Click "Apply" or "OK" button
echo.
echo After that, you can launch Diablo IV with Agent mode enabled!
echo.
echo ================================================================
echo.

:: Ask to open Battle.net
set /p launch_bnet="Would you like to open Battle.net now? (y/n): "
if /i "%launch_bnet%"=="y" (
    start "" "C:\Program Files (x86)\Battle.net\Battle.net.exe" 2>nul
    start "" "C:\Program Files\Battle.net\Battle.net.exe" 2>nul
    echo [INFO] Attempted to open Battle.net
    echo        (If it didn't open, please open it manually)
)

echo.
echo Thank you for using Diablo IV Agent Enabler!
echo.
echo Press any key to exit...
pause >nul 2>&1

:end
cls
echo.
echo ================================================================
echo                     Goodbye!
echo ================================================================
echo.

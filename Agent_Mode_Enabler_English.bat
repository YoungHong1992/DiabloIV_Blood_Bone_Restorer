@echo off
chcp 437 >nul 2>&1
title Diablo IV Agent Mode Enabler - English Version
color 0B

echo.
echo ================================================================
echo                Diablo IV Agent Mode Enabler
echo                        English Version
echo ================================================================
echo.
echo This tool will automatically configure Agent mode for Diablo IV
echo It's fully compatible with English Windows systems
echo.

echo Searching for Diablo IV installation...
echo.

set "diablo_path="
if exist "%ProgramFiles%\Battle.net\Diablo IV" (
    set "diablo_path=%ProgramFiles%\Battle.net\Diablo IV
    echo [SUCCESS] Found: %ProgramFiles%\Battle.net\Diablo IV
    goto :config
)

if exist "%ProgramFiles(x86)%\Battle.net\Diablo IV" (
    set "diablo_path=%ProgramFiles(x86)%\Battle.net\Diablo IV
    echo [SUCCESS] Found: %ProgramFiles(x86)%\Battle.net\Diablo IV
    goto :config
)

echo [WARNING] Could not auto-detect game installation
echo.
echo Please enter Diablo IV installation path manually
set /p diablo_path="Enter installation path: "
if "%diablo_path%"=="" goto :end
if not exist "%diablo_path%" (
    echo [ERROR] Directory does not exist: %diablo_path%
    goto :end
)
echo [SUCCESS] Using: %diablo_path%

:config
echo.
echo ================================================================
echo                     Configuration in Progress
echo ================================================================
echo.

:: Create WTF directory
set "wtf_dir=%diablo_path%\WTF"
echo Creating WTF directory...
if not exist "%wtf_dir%" (
    mkdir "%wtf_dir%" 2>nul
    if errorlevel 1 (
        echo [ERROR] Failed to create directory
        goto :end
    )
    echo [SUCCESS] WTF directory created
) else (
    echo [SUCCESS] WTF directory already exists
)

:: Create Config.wtf file
set "config_file=%wtf_dir%\Config.wtf"
echo Creating Config.wtf file...
echo SET OverrideArchive "0" > "%config_file%"
if errorlevel 1 (
    echo [ERROR] Failed to create config file
    goto :end
)
echo [SUCCESS] Config.wtf file created

echo.
echo ================================================================
echo                    Configuration Complete!
echo ================================================================
echo.
echo File created:
echo   Directory: %wtf_dir%
echo   File: Config.wtf
echo   Content: SET OverrideArchive "0"
echo.
echo Next steps to enable Agent mode:
echo.
echo 1. Open Battle.net client
echo 2. Click: Battle.net logo (top left) ^> Options ^> Game Settings
echo 3. Find "Diablo IV" and click it
echo 4. Check "Additional command line arguments" box
echo 5. Enter parameter: -enableagentmanager
echo 6. Click "Apply" or "OK"
echo.
echo ================================================================
echo You can now launch the game with Agent mode enabled!
echo ================================================================
echo.

:: Ask to open Battle.net
set /p launch_bnet="Would you like to open Battle.net now? (y/n): "
if /i "%launch_bnet%"=="y" (
    start "" "C:\Program Files (x86)\Battle.net\Battle.net.exe" 2>nul || start "" "C:\Program Files\Battle.net\Battle.net.exe" 2>nul
    if errorlevel 1 (
        echo.
        echo [INFO] Battle.net is not in default location
        echo        Please open it manually
    )
)

echo.
echo Thank you for using Diablo IV Agent Enabler!
echo Press any key to exit...
pause >nul

:end
cls
echo.
echo Goodbye!
echo.

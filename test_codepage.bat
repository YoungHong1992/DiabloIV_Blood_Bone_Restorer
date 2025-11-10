@echo off
:: Code Page Test Script
:: This script tests different code pages to find the one that works

echo.
echo ==========================================
echo        CODE PAGE COMPATIBILITY TEST
echo ==========================================
echo.

echo [Test 1] Current code page:
chcp
echo.

echo [Test 2] English Windows - Code Page 437:
chcp 437 >nul 2>&1
title Test 437
echo Current code page: 437
echo ABCDEFGHIJKLMNOPQRSTUVWXYZ
echo 0123456789
echo !@#$%%^&*()
echo.

echo [Test 3] English Windows - Code Page 1252:
chcp 1252 >nul 2>&1
title Test 1252
echo Current code page: 1252
echo ABCDEFGHIJKLMNOPQRSTUVWXYZ
echo 0123456789
echo !@#$%%^&*()
echo.

echo [Test 4] Chinese Windows - Code Page 936:
chcp 936 >nul 2>&1
title Test 936
echo Current code page: 936
echo ABCDEFGHIJKLMNOPQRSTUVWXYZ
echo 0123456789
echo !@#$%%^&*()
echo.

echo [Test 5] UTF-8 - Code Page 65001:
chcp 65001 >nul 2>&1
title Test 65001
echo Current code page: 65001
echo ABCDEFGHIJKLMNOPQRSTUVWXYZ
echo 0123456789
echo !@#$%%^&*()
echo.

echo ==========================================
echo Test complete! Check which code page shows
echo characters correctly on your system.
echo ==========================================
echo.

pause

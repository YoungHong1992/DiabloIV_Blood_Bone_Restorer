@echo off
chcp 936 >nul 2>&1
title 暗黑破坏神IV Agent模式启用器 - 中文版
color 0A

echo.
echo ================================================================
echo                暗黑破坏神IV Agent模式启用器
echo                        中文版本
echo ================================================================
echo.
echo 本工具将自动为暗黑破坏神IV配置Agent模式
echo 专为简体中文Windows系统优化
echo.

echo 正在搜索暗黑破坏神IV安装目录...
echo.

set "diablo_path="
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

echo [警告] 无法自动检测到游戏安装
echo.
echo 请手动输入暗黑破坏神IV的安装目录
set /p diablo_path="请输入安装目录路径: "
if "%diablo_path%"=="" goto :end
if not exist "%diablo_path%" (
    echo [错误] 目录不存在: %diablo_path%
    goto :end
)
echo [成功] 使用目录: %diablo_path%

:config
echo.
echo ================================================================
echo                      配置进行中
echo ================================================================
echo.

:: 创建WTF目录
set "wtf_dir=%diablo_path%\WTF"
echo 正在创建WTF目录...
if not exist "%wtf_dir%" (
    mkdir "%wtf_dir%" 2>nul
    if errorlevel 1 (
        echo [错误] 创建目录失败
        goto :end
    )
    echo [成功] WTF目录创建成功
) else (
    echo [成功] WTF目录已存在
)

:: 创建Config.wtf文件
set "config_file=%wtf_dir%\Config.wtf"
echo 正在创建Config.wtf文件...
echo SET OverrideArchive "0" > "%config_file%"
if errorlevel 1 (
    echo [错误] 创建配置文件失败
    goto :end
)
echo [成功] Config.wtf文件创建成功

echo.
echo ================================================================
echo                    配置完成！
echo ================================================================
echo.
echo 创建的文件:
echo   目录: %wtf_dir%
echo   文件: Config.wtf
echo   内容: SET OverrideArchive "0"
echo.
echo 接下来请按以下步骤操作:
echo.
echo 1. 打开战网客户端
echo 2. 点击: 左上角战网标志 ^> 选项 ^> 游戏设置
echo 3. 找到"暗黑破坏神IV"并点击
echo 4. 勾选"额外命令行参数"复选框
echo 5. 输入参数: -enableagentmanager
echo 6. 点击"应用"或"确定"
echo.
echo ================================================================
echo 配置完成！现在可以启动游戏使用Agent模式了！
echo ================================================================
echo.

:: 询问是否打开战网
set /p launch_bnet="现在打开战网客户端吗? (y/n): "
if /i "%launch_bnet%"=="y" (
    start "" "C:\Program Files (x86)\Battle.net\Battle.net.exe" 2>nul || start "" "C:\Program Files\Battle.net\Battle.net.exe" 2>nul
    if errorlevel 1 (
        echo.
        echo [信息] 战网不在默认位置
        echo        请手动打开战网客户端
    )
)

echo.
echo 感谢使用暗黑破坏神IV Agent模式启用器！
echo 按任意键退出...
pause >nul

:end
cls
echo.
echo 再见！
echo.

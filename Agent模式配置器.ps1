# ==========================================
# 暗黑破坏神IV Agent模式配置器
# PowerShell高级版 v1.0
# 开发者: MiniMax Agent
# 日期: 2025-11-10
# ==========================================

param(
    [switch]$Auto,
    [string]$Path,
    [switch]$Verbose
)

# 设置控制台
$Host.UI.RawUI.WindowTitle = "暗黑破坏神IV Agent模式配置器"
if ($Verbose) { $VerbosePreference = "Continue" }

function Show-Banner {
    Clear-Host
    Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║                暗黑破坏神IV Agent模式配置器                  ║
║                        PowerShell版 v1.0                    ║
║                                                              ║
║  本工具将帮您自动配置暗黑破坏神IV的Agent模式                 ║
║  让您可以安全地使用游戏助手功能                              ║
╚══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan
    Write-Host
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Find-DiabloIV {
    param()
    
    Write-Verbose "开始搜索暗黑破坏神IV安装目录..."
    
    $searchPaths = @(
        "${env:ProgramFiles}\Battle.net\Diablo IV",
        "${env:ProgramFiles(x86)}\Battle.net\Diablo IV"
    )
    
    $foundPaths = @()
    
    foreach ($path in $searchPaths) {
        if (Test-Path $path) {
            $foundPaths += $path
            Write-Host "✅ 找到游戏目录: $path" -ForegroundColor Green
        }
    }
    
    return $foundPaths
}

function Create-Config {
    param(
        [string]$GamePath
    )
    
    Write-Host "`n🔧 正在配置Agent模式..." -ForegroundColor Yellow
    
    $wtfPath = Join-Path $GamePath "WTF"
    $configPath = Join-Path $wtfPath "Config.wtf"
    
    try {
        # 创建WTF目录
        Write-Verbose "创建WTF目录: $wtfPath"
        if (-not (Test-Path $wtfPath)) {
            New-Item -ItemType Directory -Path $wtfPath -Force | Out-Null
        }
        
        # 创建配置文件
        Write-Verbose "创建配置文件: $configPath"
        $configContent = 'SET OverrideArchive "0"'
        Set-Content -Path $configPath -Value $configContent -Encoding UTF8 -Force
        
        # 验证文件
        if (Test-Path $configPath) {
            $actualContent = Get-Content $configPath -Raw
            if ($actualContent -eq $configContent) {
                Write-Host "✅ 配置文件创建成功并验证通过" -ForegroundColor Green
                return $true
            } else {
                Write-Host "❌ 配置文件内容验证失败" -ForegroundColor Red
                return $false
            }
        } else {
            Write-Host "❌ 配置文件创建失败" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ 配置过程中出现错误: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Show-ManualSteps {
    Write-Host "`n⚠️  重要提醒: 还有最后一步需要您手动完成！" -ForegroundColor Yellow
    Write-Host "`n📋 手动操作步骤:" -ForegroundColor Cyan
    
    @"
    1. 打开战网客户端
    2. 进入: 游戏设置 → 暗黑破坏神IV  
    3. 勾选: "额外命令行参数"
    4. 添加参数: -enableagentmanager
    5. 点击"完成"按钮
    
🚀 配置完成后即可启动游戏享受Agent模式！"@
    
    Write-Host
}

function Show-Summary {
    param(
        [string]$GamePath,
        [bool]$Success
    )
    
    $wtfPath = Join-Path $GamePath "WTF"
    $configPath = Join-Path $wtfPath "Config.wtf"
    
    Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                     配置摘要" -ForegroundColor Yellow
    Write-Host "╠══════════════════════════════════════════════════════════════╣" -ForegroundColor Yellow
    
    $status = if ($Success) { "✅ 成功" } else { "❌ 失败" }
    Write-Host "║ 配置状态: $status" -ForegroundColor $(if($Success){"Green"}else{"Red"})
    Write-Host "║ 游戏目录: $GamePath" -ForegroundColor Gray
    Write-Host "║ WTF目录 : $wtfPath" -ForegroundColor Gray  
    Write-Host "║ 配置文件: Config.wtf" -ForegroundColor Gray
    Write-Host "║ 文件内容: SET OverrideArchive ""0""" -ForegroundColor Gray
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
}

function Start-Configuration {
    param(
        [string]$GamePath
    )
    
    Show-Banner
    
    # 检查权限
    if (-not (Test-Administrator)) {
        Write-Host "⚠️  检测到非管理员权限" -ForegroundColor Yellow
        Write-Host "建议以管理员身份运行以确保正常创建文件" -ForegroundColor Yellow
        $response = Read-Host "`n是否继续运行? (y/n)"
        if ($response -ne "y" -and $response -ne "Y") {
            return
        }
    }
    
    Write-Host "📂 使用游戏目录: $GamePath" -ForegroundColor Green
    
    # 确认操作
    $confirm = Read-Host "`n确认要在此目录启用Agent模式吗? (y/n)"
    if ($confirm -ne "y" -and $confirm -ne "Y") {
        Write-Host "ℹ️  操作已取消" -ForegroundColor Gray
        return
    }
    
    # 执行配置
    $success = Create-Config -GamePath $GamePath
    
    # 显示结果
    if ($success) {
        Write-Host "`n🎉 恭喜！Agent模式自动配置已完成！" -ForegroundColor Green
        Show-ManualSteps
        Show-Summary -GamePath $GamePath -Success $true
        
        # 询问是否打开战网
        $openBnet = Read-Host "`n是否要打开战网客户端? (y/n)"
        if ($openBnet -eq "y" -or $openBnet -eq "Y") {
            try {
                $bnetPaths = @(
                    "${env:ProgramFiles(x86)}\Battle.net\Battle.net.exe",
                    "${env:ProgramFiles}\Battle.net\Battle.net.exe"
                )
                
                foreach ($path in $bnetPaths) {
                    if (Test-Path $path) {
                        Start-Process $path
                        Write-Host "✅ 已启动战网客户端" -ForegroundColor Green
                        break
                    }
                }
            }
            catch {
                Write-Host "ℹ️  无法自动打开战网客户端，请手动打开" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "`n❌ 配置失败，请检查权限和路径" -ForegroundColor Red
        Show-Summary -GamePath $GamePath -Success $false
    }
}

# 主程序
try {
    if ($Auto) {
        # 自动模式
        Show-Banner
        Write-Host "🤖 自动模式: 正在自动检测和配置..." -ForegroundColor Cyan
        
        $foundPaths = Find-DiabloIV
        if ($foundPaths.Count -eq 0) {
            Write-Host "❌ 未找到暗黑破坏神IV安装目录" -ForegroundColor Red
            Write-Host "请确保游戏已正确安装，或使用 -Path 参数指定路径" -ForegroundColor Yellow
            exit 1
        }
        
        if ($foundPaths.Count -eq 1) {
            Start-Configuration -GamePath $foundPaths[0]
        } else {
            Write-Host "`n找到多个安装目录，请选择:" -ForegroundColor Yellow
            for ($i = 0; $i -lt $foundPaths.Count; $i++) {
                Write-Host "$($i+1). $($foundPaths[$i])" -ForegroundColor Gray
            }
            
            $choice = Read-Host "`n请选择 (1-$($foundPaths.Count))"
            $index = [int]$choice - 1
            if ($index -ge 0 -and $index -lt $foundPaths.Count) {
                Start-Configuration -GamePath $foundPaths[$index]
            } else {
                Write-Host "❌ 无效选择" -ForegroundColor Red
            }
        }
    } elseif ($Path) {
        # 指定路径模式
        if (-not (Test-Path $Path)) {
            Write-Host "❌ 指定的路径不存在: $Path" -ForegroundColor Red
            exit 1
        }
        Start-Configuration -GamePath $Path
    } else {
        # 交互模式
        Show-Banner
        
        Write-Host "🔍 正在搜索暗黑破坏神IV安装目录..." -ForegroundColor Cyan
        $foundPaths = Find-DiabloIV
        
        if ($foundPaths.Count -eq 0) {
            Write-Host "`n❌ 未找到游戏安装目录" -ForegroundColor Red
            $manualPath = Read-Host "`n请手动输入游戏安装目录路径"
            
            if ($manualPath -and (Test-Path $manualPath)) {
                Start-Configuration -GamePath $manualPath
            } else {
                Write-Host "❌ 路径无效或不存在" -ForegroundColor Red
                exit 1
            }
        } elseif ($foundPaths.Count -eq 1) {
            $useFound = Read-Host "`n使用找到的目录: $($foundPaths[0]) (y/n)"
            if ($useFound -eq "y" -or $useFound -eq "Y") {
                Start-Configuration -GamePath $foundPaths[0]
            } else {
                $manualPath = Read-Host "请输入其他路径"
                if ($manualPath -and (Test-Path $manualPath)) {
                    Start-Configuration -GamePath $manualPath
                } else {
                    exit 1
                }
            }
        } else {
            Write-Host "`n找到多个安装目录:" -ForegroundColor Yellow
            for ($i = 0; $i -lt $foundPaths.Count; $i++) {
                Write-Host "$($i+1). $($foundPaths[$i])" -ForegroundColor Gray
            }
            
            $choice = Read-Host "`n请选择 (1-$($foundPaths.Count))"
            $index = [int]$choice - 1
            if ($index -ge 0 -and $index -lt $foundPaths.Count) {
                Start-Configuration -GamePath $foundPaths[$index]
            } else {
                Write-Host "❌ 无效选择" -ForegroundColor Red
            }
        }
    }
}
catch {
    Write-Host "`n❌ 程序执行出错: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
finally {
    Write-Host "`n感谢使用暗黑破坏神IV Agent模式配置器！" -ForegroundColor Cyan
    Write-Host "按任意键退出..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
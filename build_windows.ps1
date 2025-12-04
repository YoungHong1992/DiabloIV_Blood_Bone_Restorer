param(
    [string]$Name = "DiabloIV_BBR"
)

Write-Host "Starting local build for $Name"

# 首先删除旧的虚拟环境并重新创建
if (Test-Path ".venv") {
    Write-Host "Removing existing virtual environment..."
    Remove-Item -Recurse -Force .venv
}

Write-Host "Creating new virtual environment..."
python -m venv .venv

# 激活虚拟环境
Write-Host "Activating virtual environment..."
.venv\Scripts\Activate.ps1

# 确保pip可用
Write-Host "Ensuring pip is available..."
python -m ensurepip --upgrade

# 升级pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# 安装依赖
if (Test-Path requirements.txt) { 
    Write-Host "Installing requirements..."
    python -m pip install -r requirements.txt 
}

# 安装pyinstaller
Write-Host "Installing pyinstaller..."
python -m pip install pyinstaller

# 使用python -m pyinstaller而不是直接调用pyinstaller
Write-Host "Running pyinstaller..."
python -m PyInstaller --noconfirm --onefile --windowed --name $Name DiabloIV_Blood_Bone_Restorer.py

if (Test-Path "dist\$Name.exe") {
    Write-Host "Build successful: dist\$Name.exe"
} else {
    Write-Host "Build finished but exe not found." -ForegroundColor Red
    exit 1
}

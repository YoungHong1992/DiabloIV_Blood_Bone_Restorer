param(
    [string]$Name = "DiabloIV_BBR"
)

Write-Host "Starting local build for $Name"
python -m pip install --upgrade pip
if (Test-Path requirements.txt) { pip install -r requirements.txt }
pip install pyinstaller PySide6

$plugins = python - <<'PY'
import PySide6, os
print(os.path.join(os.path.dirname(PySide6.__file__), 'plugins'))
PY

Write-Host "Detected PySide6 plugins at: $plugins"

pyinstaller --noconfirm --onefile --windowed --name $Name --add-data "$plugins;PySide6_plugins" DiabloIV_Blood_Bone_Restorer.py

if (Test-Path "dist\$Name.exe") {
    Write-Host "Build successful: dist\$Name.exe"
} else {
    Write-Host "Build finished but exe not found." -ForegroundColor Red
    exit 1
}

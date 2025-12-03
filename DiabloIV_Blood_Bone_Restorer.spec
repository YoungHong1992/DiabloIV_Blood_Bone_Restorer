# -*- mode: python ; coding: utf-8 -*-
import os
import PySide6
from PyInstaller.utils.hooks import collect_submodules

# 自动定位 PySide6 的 plugins 目录并把所有文件作为 datas 包含进去
pyside_plugins_dir = os.path.join(os.path.dirname(PySide6.__file__), 'plugins')
datas = []
if os.path.isdir(pyside_plugins_dir):
    for root, _, files in os.walk(pyside_plugins_dir):
        for f in files:
            src = os.path.join(root, f)
            # 目标路径放到 PySide6_plugins 下，保持子目录结构
            rel_dir = os.path.relpath(root, pyside_plugins_dir)
            dest_dir = os.path.join('PySide6_plugins', rel_dir) if rel_dir != '.' else 'PySide6_plugins'
            datas.append((src, dest_dir))

# 收集 PySide6 可能需要的隐藏导入
hiddenimports = collect_submodules('PySide6')

block_cipher = None

a = Analysis(
    ['DiabloIV_Blood_Bone_Restorer.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='DiabloIV_BBR',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='DiabloIV_BBR',
)

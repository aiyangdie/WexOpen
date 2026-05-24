# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec — 纯净版 + 商业版"""

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None
root = Path(SPECPATH)
icon = str(root / "assets" / "icon.ico")

datas = collect_data_files("customtkinter")
datas += [(str(root / "assets"), "assets")]
hiddenimports = collect_submodules("customtkinter")

common = dict(
    pathex=[str(root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a_pure = Analysis([str(root / "main.py")], **common)
a_business = Analysis([str(root / "main_business.py")], **common)

pyz_pure = PYZ(a_pure.pure, a_pure.zipped_data, cipher=block_cipher)
pyz_business = PYZ(a_business.pure, a_business.zipped_data, cipher=block_cipher)

# ── 纯净版 免安装 ──
exe_portable = EXE(
    pyz_pure, a_pure.scripts, a_pure.binaries, a_pure.zipfiles, a_pure.datas,
    [],
    name="WexOpen-Portable",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=icon,
)

# ── 商业版 免安装 ──
exe_business = EXE(
    pyz_business, a_business.scripts, a_business.binaries, a_business.zipfiles, a_business.datas,
    [],
    name="WexOpen-Business-Portable",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=icon,
)

# ── 纯净版 安装包目录 ──
exe_installer = EXE(
    pyz_pure, a_pure.scripts,
    [],
    exclude_binaries=True,
    name="WexOpen",
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon=icon,
)

coll = COLLECT(
    exe_installer, a_pure.binaries, a_pure.zipfiles, a_pure.datas,
    strip=False, upx=True, name="WexOpen",
)

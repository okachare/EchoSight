# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules

app_root = r"C:\GetiCSAMInstallerBuild\app"
wrapper_root = app_root + r"\deployment\Detection\python"
datas, binaries, hiddenimports = collect_all("model_api")
hiddenimports += ["demo_package"]
hiddenimports += collect_submodules("demo_package")

a = Analysis(
    [app_root + r"\EchoSight.py"],
    pathex=[wrapper_root],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="EchoSight",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name="EchoSight",
)

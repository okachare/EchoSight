# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Determine the location of EchoSight.py - could be in Deployment/EchoSight_Inference_GUI/ or adjacent
possible_locations = [
    "Deployment/EchoSight_Inference_GUI/EchoSight.py",
    os.path.join(os.path.dirname(__file__), "Deployment/EchoSight_Inference_GUI/EchoSight.py"),
]
echosight_py = None
for loc in possible_locations:
    if os.path.exists(loc):
        echosight_py = os.path.abspath(loc)
        break

if not echosight_py:
    raise FileNotFoundError("Cannot find EchoSight.py in expected locations")

spec_dir = os.path.dirname(echosight_py)

datas = []
binaries = []
hiddenimports = [
    "cv2",
    "PIL",
    "numpy",
    "tkinter",
    "tkinter.filedialog",
    "tkinter.messagebox",
    "tkinter.ttk",
    "openvino",
    "openvino.model_api",
]

# Collect OpenVINO runtime libraries
try:
    import openvino
    ov_lib_path = os.path.dirname(openvino.__file__)
    if os.path.exists(ov_lib_path):
        datas.append((ov_lib_path, 'openvino'))
except ImportError:
    pass

a = Analysis(
    [echosight_py],
    pathex=[spec_dir],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["matplotlib", "scipy", "pandas", "plotly"],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EchoSight',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='EchoSight',
)

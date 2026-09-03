# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all, collect_submodules, get_module_file_attribute

# Get the directory where this spec file is located
spec_dir = os.path.dirname(os.path.abspath(__file__))

# Collect all necessary hidden imports and data
hiddenimports = [
    "cv2",
    "PIL",
    "numpy",
    "openvino",
    "openvino.model_api",
    "openvino.model_api.models",
]

# Ensure tkinter modules are included
hiddenimports += [
    "tkinter",
    "tkinter.filedialog",
    "tkinter.messagebox",
    "tkinter.ttk",
]

# Collect OpenVINO runtime libraries
datas = []
try:
    import openvino
    ov_lib_path = os.path.dirname(openvino.__file__)
    if os.path.exists(ov_lib_path):
        datas.append((ov_lib_path, 'openvino'))
except ImportError:
    pass

a = Analysis(
    [os.path.join(spec_dir, 'EchoSight.py')],
    pathex=[spec_dir],
    binaries=[],
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

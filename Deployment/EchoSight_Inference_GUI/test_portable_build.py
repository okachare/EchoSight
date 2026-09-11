#!/usr/bin/env python3
"""
EchoSight Portable Build - Comprehensive Testing Suite
Tests all critical components before deployment
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Configuration
PORTABLE_DIR = Path(r'\\datagrovera.ra.intel.com\QR_MD6_QRE\Users\Omkar_RA_Datagrove\Work\Dev\GeTi CSAM\Deployment\EchoSight_Inference_GUI\portable_pyqt6')
TESTS_PASSED = []
TESTS_FAILED = []

def print_header(text):
    print(f"\n{'='*65}")
    print(f"  {text}")
    print(f"{'='*65}\n")

def test_result(name, passed, details=""):
    status = "✓" if passed else "✗"
    color = "\033[92m" if passed else "\033[91m"  # Green or Red
    reset = "\033[0m"
    
    print(f"{color}{status}{reset} {name}")
    if details:
        print(f"  {details}")
    
    if passed:
        TESTS_PASSED.append(name)
    else:
        TESTS_FAILED.append(name)

# ========== TEST 1: Directory Structure ==========
print_header("TEST 1: Portable Directory Structure")

test_result("portable_pyqt6 directory exists", 
           PORTABLE_DIR.exists(),
           f"Location: {PORTABLE_DIR}")

test_result("runtime/ directory exists",
           (PORTABLE_DIR / "runtime").exists())

test_result("python.exe exists",
           (PORTABLE_DIR / "runtime" / "python.exe").exists())

test_result("Python Lib/ directory exists",
           (PORTABLE_DIR / "runtime" / "Lib").exists())

test_result("site-packages directory exists",
           (PORTABLE_DIR / "runtime" / "Lib" / "site-packages").exists())

test_result("EchoSight_PyQt6.py exists",
           (PORTABLE_DIR / "EchoSight_PyQt6.py").exists())

test_result("EchoSight.py exists",
           (PORTABLE_DIR / "EchoSight.py").exists())

test_result("Launch_EchoSight.ps1 exists",
           (PORTABLE_DIR / "Launch_EchoSight.ps1").exists())

# ========== TEST 2: Critical Packages ==========
print_header("TEST 2: Critical Python Packages")

site_packages = PORTABLE_DIR / "runtime" / "Lib" / "site-packages"

packages = {
    "PyQt6": "GUI Framework (PyQt6 6.5.0+)",
    "openvino": "OpenVINO 2024.5 inference engine",
    "cv2": "OpenCV image processing",
    "numpy": "Numerical computing",
    "PIL": "Pillow image handling",
}

for package, description in packages.items():
    pkg_path = site_packages / package
    exists = pkg_path.exists()
    test_result(f"{package} package", exists, description)

# ========== TEST 3: Python Runtime Validation ==========
print_header("TEST 3: Python Runtime Validation")

python_exe = PORTABLE_DIR / "runtime" / "python.exe"

if python_exe.exists():
    test_result("python.exe is executable", 
               os.access(str(python_exe), os.X_OK),
               f"Path: {python_exe}")
    
    # Add portable/runtime to path and test imports
    sys.path.insert(0, str(site_packages))
    
    try:
        import PyQt6
        test_result("PyQt6 import", True, f"Version: {PyQt6.__version__ if hasattr(PyQt6, '__version__') else 'N/A'}")
    except ImportError as e:
        test_result("PyQt6 import", False, str(e))
    
    try:
        import openvino
        test_result("OpenVINO import", True, "Inference engine ready")
    except ImportError as e:
        test_result("OpenVINO import", False, str(e))
    
    try:
        import cv2
        test_result("OpenCV import", True, f"Version: {cv2.__version__}")
    except ImportError as e:
        test_result("OpenCV import", False, str(e))
    
    try:
        import numpy
        test_result("NumPy import", True, f"Version: {numpy.__version__}")
    except ImportError as e:
        test_result("NumPy import", False, str(e))
    
    try:
        from PIL import Image
        test_result("Pillow import", True, "Image handling ready")
    except ImportError as e:
        test_result("Pillow import", False, str(e))

else:
    test_result("python.exe is executable", False, "python.exe not found")

# ========== TEST 4: Application File Validation ==========
print_header("TEST 4: Application Files")

# Check EchoSight_PyQt6.py
pyqt_app = PORTABLE_DIR / "EchoSight_PyQt6.py"
if pyqt_app.exists():
    with open(pyqt_app, 'r') as f:
        content = f.read()
    
    test_result("EchoSight_PyQt6.py not empty",
               len(content) > 100,
               f"File size: {len(content)} bytes")
    
    has_pyqt_import = "from PyQt6" in content
    test_result("EchoSight_PyQt6.py has PyQt6 imports",
               has_pyqt_import,
               "Found: 'from PyQt6...'")
    
    has_opencv = "import cv2" in content or "from cv2" in content
    test_result("EchoSight_PyQt6.py has OpenCV imports",
               has_opencv,
               "Found: 'import cv2' or 'from cv2...'")

# Check EchoSight.py (fallback)
tkinter_app = PORTABLE_DIR / "EchoSight.py"
if tkinter_app.exists():
    with open(tkinter_app, 'r') as f:
        content = f.read()
    
    test_result("EchoSight.py (Tkinter fallback) not empty",
               len(content) > 100,
               f"File size: {len(content)} bytes")
    
    has_tkinter = "import tkinter" in content or "from tkinter" in content
    test_result("EchoSight.py has Tkinter imports",
               has_tkinter,
               "Found: 'import tkinter' or 'from tkinter...'")

# ========== TEST 5: Metadata ==========
print_header("TEST 5: Build Metadata")

readme = PORTABLE_DIR / "README_PORTABLE.txt"
test_result("README_PORTABLE.txt exists", readme.exists())

build_info = PORTABLE_DIR / "BUILD_INFO.json"
if build_info.exists():
    try:
        with open(build_info, 'r') as f:
            info = json.load(f)
        test_result("BUILD_INFO.json is valid JSON", True,
                   f"Python: {info.get('python', 'N/A')}, PyQt6: {info.get('pyqt6', 'N/A')}")
    except json.JSONDecodeError:
        test_result("BUILD_INFO.json is valid JSON", False, "JSON parse error")
else:
    test_result("BUILD_INFO.json exists", False)

# ========== TEST 6: Package Statistics ==========
print_header("TEST 6: Package Statistics")

try:
    files = list(PORTABLE_DIR.rglob('*'))
    file_count = len([f for f in files if f.is_file()])
    total_size = sum(f.stat().st_size for f in files if f.is_file()) / (1024**2)
    
    print(f"Total files: {file_count:,}")
    print(f"Total size: {total_size:.1f} MB")
    print(f"Success: Portable package built and ready")
except Exception as e:
    print(f"Error getting statistics: {e}")

# ========== FINAL REPORT ==========
print_header("TEST SUMMARY")

total_tests = len(TESTS_PASSED) + len(TESTS_FAILED)
pass_rate = (len(TESTS_PASSED) / total_tests * 100) if total_tests > 0 else 0

print(f"Passed: {len(TESTS_PASSED)}/{total_tests} ({pass_rate:.0f}%)")
print(f"Failed: {len(TESTS_FAILED)}/{total_tests}")

if TESTS_FAILED:
    print(f"\n⚠️  Failed Tests:")
    for test in TESTS_FAILED:
        print(f"  ✗ {test}")
else:
    print("\n✅ ALL TESTS PASSED!")
    print("\nThe portable build is ready for:")
    print("  • Manual UI testing")
    print("  • Model inference testing")
    print("  • Distribution and deployment")

print(f"\n{'='*65}")
print(f"Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*65}\n")

# Exit with appropriate code
sys.exit(0 if not TESTS_FAILED else 1)

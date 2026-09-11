"""
EchoSight setup configuration for pip installation.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="echosight",
    version="1.0.0",
    author="Omkar Kachare",
    description="Model-agnostic image inference and inspection GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/okachare/EchoSight",
    project_urls={
        "Bug Tracker": "https://github.com/okachare/EchoSight/issues",
        "Documentation": "https://github.com/okachare/EchoSight#readme",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Manufacturing",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "Pillow>=10.0",
        "numpy>=1.26",
        "opencv-python>=4.10",
        "openvino==2024.5",
        "openvino-model-api==0.2.5",
        "openvino-dev==2024.5",
    ],
    entry_points={
        "console_scripts": [
            "echosight=echosight.EchoSight:main",
        ],
    },
)

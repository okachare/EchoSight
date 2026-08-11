param(
	[string]$PythonExe = "python"
)

$ErrorActionPreference = "Stop"

function Invoke-Step {
	param(
		[string]$Description,
		[scriptblock]$Action
	)

	Write-Host $Description
	& $Action
	if ($LASTEXITCODE -ne 0) {
		throw "Step failed: $Description"
	}
}

Write-Host "[1/4] Cleaning previous build artifacts..."
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "TiffSplitter.spec") { Remove-Item -Force "TiffSplitter.spec" }

Invoke-Step "[2/4] Upgrading pip..." { & $PythonExe -m pip install --upgrade pip }
Invoke-Step "[3/4] Installing dependencies..." { & $PythonExe -m pip install -r requirements.txt }
Invoke-Step "[4/4] Building single-file EXE with PyInstaller..." { & $PythonExe -m PyInstaller --noconfirm --clean --onefile --windowed --name TiffSplitter TiffSplitter.py }

Write-Host "Build complete."
Write-Host "Output: .\dist\TiffSplitter.exe"

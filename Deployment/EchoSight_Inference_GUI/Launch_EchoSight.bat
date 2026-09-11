@echo off
setlocal

set "GUI_DIR=%~dp0"
set "APP_PYQT6=%GUI_DIR%EchoSight_PyQt6.py"
set "APP_TKINTER=%GUI_DIR%EchoSight.py"
set "APP=%APP_PYQT6%"

if exist "%GUI_DIR%runtime\pythonw.exe" if exist "%GUI_DIR%runtime\Lib\site-packages\openvino\__init__.py" if exist "%GUI_DIR%deployment\Detection\model\model.xml" goto portable_root
if exist "%GUI_DIR%portable\runtime\pythonw.exe" if exist "%GUI_DIR%portable\runtime\Lib\site-packages\openvino\__init__.py" if exist "%GUI_DIR%portable\deployment\Detection\model\model.xml" goto portable_nested
goto development_runtime

:portable_root
set "PYTHON=%GUI_DIR%runtime\pythonw.exe"
set "RUNTIME=%GUI_DIR%runtime\Lib\site-packages"
set "DEPLOYMENT=%GUI_DIR%deployment\Detection\python"
set "GETI_DEFAULT_DEPLOYMENT=%GUI_DIR%deployment"
goto launch

:portable_nested
set "PYTHON=%GUI_DIR%portable\runtime\pythonw.exe"
set "RUNTIME=%GUI_DIR%portable\runtime\Lib\site-packages"
set "DEPLOYMENT=%GUI_DIR%portable\deployment\Detection\python"
set "GETI_DEFAULT_DEPLOYMENT=%GUI_DIR%portable\deployment"
goto launch

:development_runtime
set "PYTHON=%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
set "RUNTIME=C:\GetiCSAMInstallerBuild\site"
set "DEPLOYMENT=%GUI_DIR%..\Test_Run_Detect\deployment\Detection\python"
set "GETI_DEFAULT_DEPLOYMENT=%GUI_DIR%..\Test_Run_Detect"

if not exist "%PYTHON%" (
    echo Compatible Python 3.9 was not found:
    echo %PYTHON%
    pause
    exit /b 1
)
if not exist "%RUNTIME%\openvino\__init__.py" (
    echo Compatible OpenVINO runtime was not found:
    echo %RUNTIME%
    echo.
    echo Run the deployment runtime setup before launching the GUI.
    pause
    exit /b 1
)

:launch
set "PYTHONPATH=%RUNTIME%;%DEPLOYMENT%"
echo Starting EchoSight...
echo Runtime: %RUNTIME%
echo Deployment: %GETI_DEFAULT_DEPLOYMENT%
echo.
echo Attempting to launch PyQt6 version (modern UI with Apple-like polish)...

REM Try PyQt6 with output capture to see any errors
"%PYTHON%" "%APP_PYQT6%" 2>nul
if not errorlevel 1 goto end

echo.
echo PyQt6 version unavailable or failed. Falling back to Tkinter...
echo.

REM Fall back to Tkinter
"%PYTHON%" "%APP_TKINTER%"
if errorlevel 1 (
    echo.
    echo ERROR: Both versions failed to launch.
    echo Python: %PYTHON%
    echo PyQt6 app: %APP_PYQT6%
    echo Tkinter app: %APP_TKINTER%
    echo.
    pause
)

:end
exit /b 0

@echo off
REM ============================================================================
REM CADMIES Public Setup — Windows
REM ============================================================================
REM Installs everything needed to run CADMIES. Double-click or run from cmd.
REM Usage: setup.bat
REM ============================================================================

echo ============================================
echo   CADMIES Setup
echo   The mycelium welcomes you. 🌱🍄
echo ============================================
echo.

echo 👋 Hey! Detected: Windows
echo    This'll take about 30 seconds. Grab a sip of coffee. ☕
echo.

REM ----------------------------------------
REM Step 1: Check Python
REM ----------------------------------------
echo [1/4] Checking Python...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found. Please install Python 3.10+ first:
    echo    https://www.python.org/downloads/
    echo    Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)
python --version
echo    ✅ Found
echo.

REM ----------------------------------------
REM Step 2: Create virtual environment
REM ----------------------------------------
echo [2/4] Setting up virtual environment...
if not exist "venv\" (
    python -m venv venv
    echo    ✅ Created venv\
) else (
    echo    ⏭️  venv\ already exists — skipping
)

call venv\Scripts\activate.bat
echo    ✅ Activated
echo.

REM ----------------------------------------
REM Step 3: Install Python dependencies
REM ----------------------------------------
echo [3/4] Installing Python dependencies...
pip install --quiet --upgrade pip
pip install --quiet dag_cbor
echo    ✅ dag_cbor installed
echo.

REM ----------------------------------------
REM Step 4: Optional — Ollama for AI features
REM ----------------------------------------
echo [4/4] AI features (optional)...
where ollama >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    ✅ Ollama already installed
) else (
    echo    💡 Want the AI features? Install Ollama:
    echo       https://ollama.com/download/windows
    echo       Then: ollama pull mistral:7b
    echo    Or skip this — the map and library work without it.
)
echo.

REM ----------------------------------------
REM Done
REM ----------------------------------------
echo ============================================
echo   ✅ All done!
echo ============================================
echo.
echo   Next steps:
echo   1. Download cadmies_latest.car from:
echo      https://github.com/Hieros-CADMIES/CADMIES/releases
echo   2. Drop it in the incoming_cars\ folder
echo   3. Run: python tools/import_from_car.py incoming_cars/cadmies_latest.car
echo   4. Run: python tools/generate_mycelium_map.py
echo   5. Open mycelium_map.html in your browser
echo.
echo   The garden is alive. 🌱🍄
echo.
pause
@echo off
chcp 65001 >nul
echo ========================================
echo  🍅 Pomodoro Timer Pro - Creazione EXE
echo  (con UV Package Manager)
echo ========================================
echo.

REM Controlla se l'ambiente virtuale esiste
if not exist ".venv" (
    echo Ambiente virtuale non trovato!
    echo Esegui prima setup_uv.bat
    pause
    exit /b 1
)

REM Attiva ambiente virtuale
call .venv\Scripts\activate.bat

echo Verifica PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller non trovato. Installazione...
    uv pip install pyinstaller
)

echo.
echo ✅ PyInstaller pronto!
echo.
echo Creazione dell'eseguibile in corso...
echo Questo potrebbe richiedere qualche minuto...
echo.

REM Crea l'eseguibile
pyinstaller --onefile --windowed --name "PomodoroTimer" pomodoro_timer.py

if errorlevel 1 (
    echo.
    echo ❌ ERRORE durante la creazione dell'eseguibile
    pause
    exit /b 1
)

echo.
echo ========================================
echo  ✅ COMPLETATO CON SUCCESSO!
echo ========================================
echo.
echo Il file PomodoroTimer.exe si trova in:
echo %CD%\dist\PomodoroTimer.exe
echo.
echo 📦 Dimensione: 
dir dist\PomodoroTimer.exe | find "PomodoroTimer.exe"
echo.
echo Puoi copiare questo file ovunque e avviarlo!
echo.

REM Apri la cartella dist se esiste
if exist "dist" (
    echo Apertura cartella dist...
    explorer dist
)

echo.
echo Premi un tasto per chiudere...
pause >nul
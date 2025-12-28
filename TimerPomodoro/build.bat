@echo off
chcp 65001 >nul
echo ========================================
echo  🍅 Creazione Pomodoro Timer EXE
echo ========================================
echo.

REM Verifica file Python
if not exist "main.py" (
    echo ❌ ERRORE: File main.py non trovato!
    echo.
    echo Assicurati di essere nella cartella corretta.
    echo I file necessari sono:
    echo   - main.py
    echo   - ui.py
    echo   - timer.py
    echo   - config.py
    echo   - sound.py
    echo.
    pause
    exit /b 1
)

echo ✅ File trovati
echo.

REM Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python non installato!
    echo Scarica da: https://python.org
    pause
    exit /b 1
)

echo ✅ Python trovato
echo.

REM Installa PyInstaller se necessario
echo Controllo PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installazione PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Errore installazione PyInstaller
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller OK
echo.
echo Creazione eseguibile...
echo Attendere 2-3 minuti...
echo.

REM Pulisci vecchi build
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec

REM Crea exe
python -m PyInstaller --onefile --windowed --name "PomodoroTimer" main.py

if errorlevel 1 (
    echo.
    echo ❌ ERRORE creazione exe
    pause
    exit /b 1
)

echo.
echo ========================================
echo  ✅ EXE CREATO CON SUCCESSO!
echo ========================================
echo.
echo 📂 Percorso: %CD%\dist\PomodoroTimer.exe
echo.
dir dist\PomodoroTimer.exe | find "PomodoroTimer.exe"
echo.
echo Puoi copiare l'exe ovunque e usarlo!
echo.

REM Apri cartella dist
if exist "dist" explorer dist

pause
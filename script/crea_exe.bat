@echo off
chcp 65001 >nul
echo ========================================
echo  🍅 Pomodoro Timer Pro - Creazione EXE
echo  (con UV Package Manager)
echo ========================================
echo.

REM Controlla se il file Python esiste
if not exist "pomodoro_timer.py" (
    echo ❌ ERRORE: File pomodoro_timer.py non trovato!
    echo.
    echo Assicurati che:
    echo 1. Il file pomodoro_timer.py sia nella stessa cartella di questo script
    echo 2. Stai eseguendo questo script dalla cartella corretta
    echo.
    echo Cartella corrente: %CD%
    echo.
    pause
    exit /b 1
)

REM Controlla se l'ambiente virtuale esiste
if not exist ".venv" (
    echo ❌ Ambiente virtuale non trovato!
    echo.
    echo Devi prima eseguire setup.bat per configurare l'ambiente.
    echo.
    pause
    exit /b 1
)

echo ✅ File Python trovato: pomodoro_timer.py
echo ✅ Ambiente virtuale trovato
echo.

REM Attiva ambiente virtuale
echo Attivazione ambiente virtuale...
call .venv\Scripts\activate.bat

REM Verifica PyInstaller
echo Verifica PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller non trovato. Installazione in corso...
    uv pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Errore installazione PyInstaller
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller pronto!
echo.
echo ========================================
echo  Creazione eseguibile in corso...
echo  Questo potrebbe richiedere 2-3 minuti
echo ========================================
echo.

REM Rimuovi vecchi file build se esistono
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec

REM Crea l'eseguibile
pyinstaller --onefile --windowed --name "PomodoroTimerPro" --icon=NONE pomodoro_timer.py

if errorlevel 1 (
    echo.
    echo ❌ ERRORE durante la creazione dell'eseguibile
    echo.
    echo Possibili cause:
    echo - Antivirus che blocca PyInstaller
    echo - Spazio su disco insufficiente
    echo - Permessi mancanti
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  ✅ ESEGUIBILE CREATO CON SUCCESSO!
echo ========================================
echo.
echo 📂 Percorso:
echo    %CD%\dist\PomodoroTimerPro.exe
echo.
echo 📊 Informazioni file:
dir dist\PomodoroTimerPro.exe | find "PomodoroTimerPro.exe"
echo.
echo ========================================
echo  📦 COSA FARE ORA
echo ========================================
echo.
echo 1. Trova l'exe in: dist\PomodoroTimerPro.exe
echo 2. Puoi copiarlo ovunque vuoi
echo 3. Eseguilo con doppio click
echo 4. Non servono altre dipendenze!
echo.
echo ⚠ NOTA: L'antivirus potrebbe segnalarlo come
echo    falso positivo (è normale per exe creati
echo    con PyInstaller). Aggiungi un'eccezione.
echo.

REM Apri la cartella dist
if exist "dist" (
    echo Apertura cartella con l'eseguibile...
    timeout /t 2 /nobreak >nul
    explorer dist
)

echo.
echo Premi un tasto per chiudere...
pause >nul

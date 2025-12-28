@echo off
chcp 65001 >nul
echo ========================================
echo  📦 Pomodoro Timer Pro - Setup
echo  (Installazione con UV Package Manager)
echo ========================================
echo.

REM Controlla se UV è installato
echo Controllo installazione UV...
uv --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠ UV non trovato. Installazione in corso...
    echo.
    
    REM Installa UV usando PowerShell
    powershell -ExecutionPolicy ByPass -Command "irm https://astral.sh/uv/install.ps1 | iex"
    
    if errorlevel 1 (
        echo.
        echo ❌ ERRORE: Impossibile installare UV
        echo.
        echo Soluzioni alternative:
        echo 1. Installa manualmente da: https://github.com/astral-sh/uv
        echo 2. Oppure usa pip: pip install pyinstaller
        echo.
        pause
        exit /b 1
    )
    
    echo.
    echo ✅ UV installato con successo!
    echo.
    echo ⚠ IMPORTANTE: Chiudi e riapri questo Prompt dei Comandi
    echo poi riesegui questo script.
    echo.
    pause
    exit /b 0
) else (
    echo ✅ UV è già installato!
    uv --version
    echo.
)

REM Crea ambiente virtuale se non esiste
if not exist ".venv" (
    echo Creazione ambiente virtuale Python...
    uv venv
    if errorlevel 1 (
        echo ❌ Errore creazione ambiente virtuale
        pause
        exit /b 1
    )
    echo ✅ Ambiente virtuale creato!
    echo.
) else (
    echo ✅ Ambiente virtuale già esistente!
    echo.
)

REM Attiva ambiente virtuale e installa dipendenze
echo Installazione dipendenze...
call .venv\Scripts\activate.bat

REM Installa le dipendenze dal pyproject.toml
uv pip install -e .

if errorlevel 1 (
    echo.
    echo ❌ Errore installazione dipendenze
    pause
    exit /b 1
)

echo.
echo ========================================
echo  ✅ SETUP COMPLETATO CON SUCCESSO!
echo ========================================
echo.
echo L'ambiente è pronto per l'uso!
echo.
echo 📝 Prossimi passi:
echo 1. Chiudi questa finestra
echo 2. Esegui "crea_exe.bat" per creare l'eseguibile
echo.
echo Oppure esegui direttamente l'app Python:
echo   .venv\Scripts\python.exe pomodoro_timer.py
echo.
pause

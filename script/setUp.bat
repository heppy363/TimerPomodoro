@echo off
chcp 65001 >nul
echo ========================================
echo  📦 Setup Pomodoro Timer Pro con UV
echo ========================================
echo.

REM Controlla se UV è installato
uv --version >nul 2>&1
if errorlevel 1 (
    echo UV non trovato. Installazione in corso...
    echo.
    
    REM Installa UV usando PowerShell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    
    if errorlevel 1 (
        echo.
        echo ERRORE: Impossibile installare UV
        echo Prova a installarlo manualmente da: https://github.com/astral-sh/uv
        pause
        exit /b 1
    )
    
    echo.
    echo ✅ UV installato con successo!
    echo Riavvia questo script per continuare.
    pause
    exit /b 0
)

echo ✅ UV trovato!
echo.

REM Crea ambiente virtuale se non esiste
if not exist ".venv" (
    echo Creazione ambiente virtuale...
    uv venv
    echo ✅ Ambiente virtuale creato!
    echo.
)

REM Attiva ambiente virtuale e installa dipendenze
echo Installazione dipendenze...
call .venv\Scripts\activate.bat
uv pip install -e .

echo.
echo ========================================
echo  ✅ SETUP COMPLETATO!
echo ========================================
echo.
echo Ambiente pronto per l'uso!
echo.
echo Per creare l'EXE esegui: crea_exe_uv.bat
echo.
pause
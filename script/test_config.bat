@echo off
chcp 65001 >nul
echo ╔════════════════════════════════════════════════╗
echo ║  🔍 Test Configurazione Pomodoro Timer        ║
echo ╚════════════════════════════════════════════════╝
echo.

REM Test 1: Controlla file Python
echo [1/5] Controllo file pomodoro_timer.py...
if exist "pomodoro_timer.py" (
    echo      ✅ File Python trovato
) else (
    echo      ❌ File Python NON trovato!
    echo      Soluzione: Scarica pomodoro_timer.py
    goto :error
)

REM Test 2: Controlla pyproject.toml
echo [2/5] Controllo pyproject.toml...
if exist "pyproject.toml" (
    echo      ✅ File configurazione trovato
) else (
    echo      ❌ File pyproject.toml NON trovato!
    goto :error
)

REM Test 3: Controlla Python
echo [3/5] Controllo installazione Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo      ❌ Python NON installato!
    echo      Soluzione: Installa Python da python.org
    goto :error
) else (
    for /f "tokens=*" %%i in ('python --version') do echo      ✅ %%i installato
)

REM Test 4: Controlla UV
echo [4/5] Controllo UV package manager...
uv --version >nul 2>&1
if errorlevel 1 (
    echo      ⚠ UV non installato (verrà installato da setup.bat)
) else (
    for /f "tokens=*" %%i in ('uv --version') do echo      ✅ %%i installato
)

REM Test 5: Controlla ambiente virtuale
echo [5/5] Controllo ambiente virtuale...
if exist ".venv" (
    echo      ✅ Ambiente virtuale già configurato
    echo      Puoi procedere con crea_exe.bat
) else (
    echo      ⚠ Ambiente virtuale non trovato
    echo      Esegui setup.bat per configurarlo
)

echo.
echo ╔════════════════════════════════════════════════╗
echo ║  ✅ TEST COMPLETATI                            ║
echo ╚════════════════════════════════════════════════╝
echo.
echo 📝 Prossimi passi:
echo    1. Se UV non è installato → Esegui setup.bat
echo    2. Se tutto è OK → Esegui crea_exe.bat
echo.
pause
exit /b 0

:error
echo.
echo ╔════════════════════════════════════════════════╗
echo ║  ❌ ERRORI RILEVATI                            ║
echo ╚════════════════════════════════════════════════╝
echo.
echo Controlla i messaggi sopra e risolvi i problemi.
echo Poi riesegui questo test.
echo.
pause
exit /b 1

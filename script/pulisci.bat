@echo off
chcp 65001 >nul
echo ╔════════════════════════════════════════════════╗
echo ║  🧹 Pulizia File Temporanei                   ║
echo ╚════════════════════════════════════════════════╝
echo.
echo Questo script rimuoverà:
echo   - Cartella build/
echo   - Cartella dist/
echo   - File .spec
echo   - Cache Python (__pycache__)
echo.
echo ⚠ L'eseguibile verrà eliminato!
echo.
set /p confirm="Continuare? (S/N): "
if /i not "%confirm%"=="S" (
    echo Operazione annullata.
    pause
    exit /b 0
)

echo.
echo Pulizia in corso...

if exist "build" (
    echo Rimozione build/...
    rmdir /s /q build
    echo ✅ build/ rimosso
)

if exist "dist" (
    echo Rimozione dist/...
    rmdir /s /q dist
    echo ✅ dist/ rimosso
)

if exist "*.spec" (
    echo Rimozione file .spec...
    del /q *.spec
    echo ✅ File .spec rimossi
)

if exist "__pycache__" (
    echo Rimozione __pycache__/...
    rmdir /s /q __pycache__
    echo ✅ __pycache__/ rimosso
)

REM Pulizia cache Python ricorsiva
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo Rimozione %%d...
    rmdir /s /q "%%d"
)

echo.
echo ╔════════════════════════════════════════════════╗
echo ║  ✅ PULIZIA COMPLETATA                         ║
echo ╚════════════════════════════════════════════════╝
echo.
echo Per ricreare l'eseguibile, esegui crea_exe.bat
echo.
pause

@echo off
chcp 65001 >nul
echo ========================================
echo  🧹 Pulizia File Temporanei
echo ========================================
echo.
echo Verranno rimossi:
echo   - build/
echo   - dist/
echo   - __pycache__/
echo   - *.spec
echo.
set /p confirm="Continuare? (S/N): "
if /i not "%confirm%"=="S" (
    echo Annullato.
    pause
    exit /b 0
)

echo.
echo Pulizia in corso...
echo.

if exist "build" (
    rmdir /s /q build
    echo ✅ build/ rimosso
)

if exist "dist" (
    rmdir /s /q dist
    echo ✅ dist/ rimosso
)

if exist "*.spec" (
    del /q *.spec
    echo ✅ *.spec rimossi
)

if exist "__pycache__" (
    rmdir /s /q __pycache__
    echo ✅ __pycache__/ rimosso
)

REM Pulisci cache Python ricorsiva
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" 2>nul

echo.
echo ========================================
echo  ✅ PULIZIA COMPLETATA
echo ========================================
echo.
pause
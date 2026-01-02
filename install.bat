@echo off
REM Instalator SOKE dla Windows (wersja Batch)
REM Uruchamia skrypt PowerShell

echo ================================================
echo   SOKE - Instalator Windows
echo   System Optymalizacji Kosztow Energii
echo ================================================
echo.

cd /d "%~dp0"

REM Sprawdź czy PowerShell jest dostępny
powershell -Command "Get-Host" >nul 2>&1
if errorlevel 1 (
    echo Blad: PowerShell nie jest dostepny.
    pause
    exit /b 1
)

REM Uruchom skrypt PowerShell
powershell -ExecutionPolicy Bypass -File "%~dp0install.ps1"

if errorlevel 1 (
    echo.
    echo Instalacja nie powiodla sie.
    pause
    exit /b 1
)

echo.
pause


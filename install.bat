@echo off
REM Instalator SOKE dla Windows (wersja Batch)
REM Przyjazny dla osób niekomputerowych - automatyczna instalacja
REM Wystarczy kliknąć dwukrotnie ten plik!

echo.
echo ================================================
echo   SOKE - Instalator Windows
echo   System Optymalizacji Kosztow Energii
echo ================================================
echo.
echo Instalacja rozpocznie sie za chwile...
echo Proszę czekac, moze to potrwac kilka minut.
echo.
echo UWAGA: Instalator moze poprosic o potwierdzenie
echo        instalacji Pythona - kliknij "Tak" lub "T"
echo.
timeout /t 3 /nobreak >nul

cd /d "%~dp0"

REM Sprawdź czy PowerShell jest dostępny
powershell -Command "Get-Host" >nul 2>&1
if errorlevel 1 (
    echo.
    echo BLAD: PowerShell nie jest dostepny.
    echo.
    echo Proszę zaktualizowac Windows lub skontaktowac sie z administratorem.
    echo.
    pause
    exit /b 1
)

REM Uruchom skrypt PowerShell z automatyczną instalacją Pythona
powershell -ExecutionPolicy Bypass -File "%~dp0install.ps1" -AutoInstallPython

if errorlevel 1 (
    echo.
    echo ================================================
    echo   Instalacja nie powiodla sie.
    echo ================================================
    echo.
    echo Proszę sprawdzic komunikaty powyzej.
    echo Jesli problem sie powtarza, skontaktuj sie z administratorem.
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo   Instalacja zakonczona!
echo ================================================
echo.
pause


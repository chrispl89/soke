@echo off
REM Skrypt uruchomieniowy SOKE
REM Wystarczy kliknąć dwukrotnie ten plik, aby uruchomić aplikację!

echo.
echo ================================================
echo   Uruchamianie SOKE...
echo ================================================
echo.

cd /d "%~dp0"

REM Sprawdź czy środowisko wirtualne istnieje
if not exist ".venv\Scripts\activate.bat" (
    echo BLAD: Aplikacja nie jest zainstalowana!
    echo.
    echo Proszę najpierw uruchomic instalator:
    echo   - Kliknij dwukrotnie: install.bat
    echo.
    pause
    exit /b 1
)

REM Aktywuj środowisko wirtualne i uruchom aplikację
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo BLAD: Nie mozna aktywowac srodowiska wirtualnego.
    echo.
    echo Proszę uruchomic instalator ponownie: install.bat
    echo.
    pause
    exit /b 1
)

echo Aplikacja uruchamia sie...
echo Otworzy sie automatycznie w przegladarce.
echo.
echo Aby zatrzymac aplikacje, zamknij to okno.
echo.

streamlit run src/soke/app.py

if errorlevel 1 (
    echo.
    echo BLAD: Nie mozna uruchomic aplikacji.
    echo.
    pause
)


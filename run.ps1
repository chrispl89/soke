# Skrypt uruchomieniowy dla SOKE
# Przyjazny dla osób niekomputerowych

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Uruchamianie SOKE..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Sprawdź czy środowisko wirtualne istnieje
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "BLAD: Aplikacja nie jest zainstalowana!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Proszę najpierw uruchomic instalator:" -ForegroundColor Yellow
    Write-Host "  - Kliknij dwukrotnie: install.bat" -ForegroundColor Cyan
    Write-Host "  - Lub uruchom: .\install.ps1" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Naciśnij Enter, aby zakończyć"
    exit 1
}

Write-Host "Aplikacja uruchamia sie..." -ForegroundColor Yellow
Write-Host "Otworzy sie automatycznie w przegladarce." -ForegroundColor Gray
Write-Host ""
Write-Host "Aby zatrzymac aplikacje, zamknij to okno lub naciśnij Ctrl+C" -ForegroundColor Gray
Write-Host ""

try {
    & .\.venv\Scripts\Activate.ps1
    streamlit run src/soke/app.py
} catch {
    Write-Host ""
    Write-Host "BLAD: Nie mozna uruchomic aplikacji." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Proszę sprawdzic czy instalacja zostala zakonczona poprawnie." -ForegroundColor Yellow
    Read-Host "Naciśnij Enter, aby zakończyć"
    exit 1
}


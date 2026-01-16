# Instalator SOKE dla Windows
# Instaluje Pythona (jeśli potrzebny) i wszystkie zależności projektu
# Przyjazny dla osób niekomputerowych - automatyczna instalacja

param(
    [switch]$SkipPythonCheck = $false,
    [switch]$AutoInstallPython = $true
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  SOKE - Instalator Windows" -ForegroundColor Cyan
Write-Host "  System Optymalizacji Kosztów Energii" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ten instalator automatycznie:" -ForegroundColor White
Write-Host "  • Sprawdzi czy Python jest zainstalowany" -ForegroundColor Gray
Write-Host "  • Zainstaluje Pythona (jeśli potrzeba)" -ForegroundColor Gray
Write-Host "  • Zainstaluje wszystkie potrzebne programy" -ForegroundColor Gray
Write-Host "  • Przygotuje aplikację do uruchomienia" -ForegroundColor Gray
Write-Host ""
Write-Host "Proszę czekać, instalacja może potrwać kilka minut..." -ForegroundColor Yellow
Write-Host ""

# Funkcja sprawdzająca czy Python jest zainstalowany
function Test-PythonInstalled {
    try {
        $pythonVersionOutput = & python --version 2>&1
        if ($LASTEXITCODE -eq 0 -or $?) {
            $versionString = $pythonVersionOutput.ToString()
            if ($versionString -match "Python (\d+)\.(\d+)") {
                $major = [int]$matches[1]
                $minor = [int]$matches[2]
                if ($major -ge 3 -and $minor -ge 11) {
                    Write-Host "✓ Python $($matches[0]) jest zainstalowany" -ForegroundColor Green
                    return $true
                } else {
                    Write-Host "✗ Python jest za stary (wymagany 3.11+, znaleziono $($matches[0]))" -ForegroundColor Red
                    return $false
                }
            }
        }
    } catch {
        # Python nie jest w PATH lub nie jest zainstalowany
    }
    return $false
}

# Funkcja instalacji Pythona przez winget
function Install-PythonWinget {
    Write-Host "Próba instalacji Pythona przez winget..." -ForegroundColor Yellow
    
    try {
        $wingetCheck = winget --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Instalowanie Pythona 3.11+ przez winget..." -ForegroundColor Yellow
            winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Python zainstalowany przez winget" -ForegroundColor Green
                # Odświeżenie PATH
                $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
                return $true
            }
        }
    } catch {
        Write-Host "winget nie jest dostępny" -ForegroundColor Yellow
    }
    return $false
}

# Funkcja pobierania i instalacji Pythona
function Install-PythonManual {
    Write-Host "Przygotowuję instrukcje ręcznej instalacji Pythona..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Automatyczna instalacja nie powiodła się." -ForegroundColor Red
    Write-Host "Proszę zainstalować Pythona ręcznie:" -ForegroundColor Yellow
    Write-Host "1. Pobierz Pythona 3.11+ z: https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host "2. Podczas instalacji zaznacz: 'Add Python to PATH'" -ForegroundColor Cyan
    Write-Host "3. Uruchom ponownie ten skrypt" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Naciśnij Enter, aby otworzyć stronę pobierania Pythona..." -ForegroundColor Yellow
    Read-Host
    Start-Process "https://www.python.org/downloads/"
    exit 1
}

# KROK 1: Sprawdzenie Pythona
Write-Host "[1/4] Sprawdzanie instalacji Pythona..." -ForegroundColor Cyan
if (-not $SkipPythonCheck) {
    if (-not (Test-PythonInstalled)) {
        Write-Host "Python nie jest zainstalowany lub wersja jest za stara (wymagany 3.11+)" -ForegroundColor Yellow
        Write-Host ""
        
        if ($AutoInstallPython) {
            Write-Host "Próbuję zainstalować Pythona automatycznie..." -ForegroundColor Yellow
            if (-not (Install-PythonWinget)) {
                Write-Host ""
                Write-Host "Automatyczna instalacja nie powiodła się." -ForegroundColor Red
                Write-Host "Przechodzę do instrukcji ręcznej instalacji..." -ForegroundColor Yellow
                Install-PythonManual
            } else {
                # Sprawdź ponownie po instalacji
                Write-Host "Oczekiwanie na zakończenie instalacji Pythona..." -ForegroundColor Yellow
                Start-Sleep -Seconds 3
                # Odświeżenie PATH
                $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
                
                if (-not (Test-PythonInstalled)) {
                    Write-Host ""
                    Write-Host "Python został zainstalowany, ale nie jest jeszcze dostępny w terminalu." -ForegroundColor Yellow
                    Write-Host "Proszę:" -ForegroundColor Yellow
                    Write-Host "  1. Zamknąć to okno" -ForegroundColor Cyan
                    Write-Host "  2. Otworzyć nowe okno PowerShell lub wiersz poleceń" -ForegroundColor Cyan
                    Write-Host "  3. Uruchomić instalator ponownie" -ForegroundColor Cyan
                    Write-Host ""
                    Write-Host "Naciśnij Enter, aby zakończyć..." -ForegroundColor Yellow
                    Read-Host
                    exit 1
                }
            }
        } else {
            $installPython = Read-Host "Czy chcesz zainstalować Pythona automatycznie? (T/N)"
            if ($installPython -eq "T" -or $installPython -eq "t" -or $installPython -eq "Y" -or $installPython -eq "y") {
                if (-not (Install-PythonWinget)) {
                    Install-PythonManual
                }
                # Sprawdź ponownie po instalacji
                Start-Sleep -Seconds 3
                $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
                if (-not (Test-PythonInstalled)) {
                    Write-Host "Proszę zrestartować terminal i uruchomić skrypt ponownie" -ForegroundColor Yellow
                    exit 1
                }
            } else {
                Write-Host "Instalacja przerwana. Python jest wymagany do dalszej pracy." -ForegroundColor Red
                exit 1
            }
        }
    }
} else {
    Write-Host "Pomijam sprawdzanie Pythona (--SkipPythonCheck)" -ForegroundColor Yellow
}

# KROK 2: Tworzenie środowiska wirtualnego
Write-Host ""
Write-Host "[2/4] Tworzenie środowiska wirtualnego..." -ForegroundColor Cyan
if (Test-Path ".venv") {
    Write-Host "Środowisko wirtualne już istnieje. Usuwam stare..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .venv
}

python -m venv .venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Błąd podczas tworzenia środowiska wirtualnego" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Środowisko wirtualne utworzone" -ForegroundColor Green

# KROK 3: Aktualizacja pip
Write-Host ""
Write-Host "[3/4] Aktualizacja pip..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Błąd podczas aktualizacji pip" -ForegroundColor Red
    exit 1
}
Write-Host "✓ pip zaktualizowany" -ForegroundColor Green

# KROK 4: Instalacja zależności projektu
Write-Host ""
Write-Host "[4/4] Instalacja zależności projektu..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Błąd podczas instalacji zależności" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Wszystkie zależności zainstalowane" -ForegroundColor Green

# Podsumowanie
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  ✓ Instalacja zakończona pomyślnie!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Aplikacja jest gotowa do uruchomienia!" -ForegroundColor White
Write-Host ""
Write-Host "Aby uruchomić aplikację:" -ForegroundColor Cyan
Write-Host "  • Kliknij dwukrotnie plik: run.bat" -ForegroundColor Yellow
Write-Host "  • Lub uruchom: .\run.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "Aplikacja otworzy się automatycznie w przeglądarce." -ForegroundColor Gray
Write-Host ""
Write-Host "Naciśnij Enter, aby zakończyć..." -ForegroundColor Gray
Read-Host


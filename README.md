# SOKE – System Optymalizacji Kosztów Energii (Streamlit)

## Instalacja

### Nowa instalacja (Windows)

**Najłatwiej:** Uruchom automatyczny instalator:
```powershell
.\install.ps1
```

Lub kliknij dwukrotnie: `install.bat`

Instalator automatycznie:
- ✅ Sprawdzi/zainstaluje Pythona 3.11+ (przez winget, jeśli dostępny)
- ✅ Utworzy środowisko wirtualne (`.venv`)
- ✅ Zainstaluje wszystkie zależności projektu

📖 **Szybki start:** [QUICKSTART.md](QUICKSTART.md)  
📚 **Szczegółowe instrukcje:** [INSTALL.md](INSTALL.md)

## Start

### Szybkie uruchomienie (Windows)

**Metoda 1: Skrypt PowerShell** (zalecane)
```powershell
.\run.ps1
```

**Metoda 2: Skrypt BAT**
```cmd
run.bat
```

**Metoda 3: Ręczne uruchomienie**
```powershell
.\.venv\Scripts\python.exe -m streamlit run src/soke/app.py
```

### Instalacja (jeśli jeszcze nie zainstalowano)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Dane stawek
Pliki YAML: `src/soke/data/tariffs/2026/*.yaml`

## Pipeline PDF
- `src/soke/scripts/fetch_tariffs.py` pobiera PDF-y taryf (linki w kodzie).
- `extract_stub.py` to miejsce na ekstrakcję tabel do YAML (na start ręcznie uzupełniamy YAML).

## Testy
```powershell
pytest tests/ -v
```

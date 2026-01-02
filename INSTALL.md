# Instalacja SOKE na Windows

## Automatyczna instalacja (zalecana)

### Opcja 1: Skrypt PowerShell (najłatwiejsze)

1. Kliknij prawym przyciskiem na `install.ps1`
2. Wybierz "Uruchom w programie PowerShell"
3. Postępuj zgodnie z instrukcjami

Lub uruchom w PowerShell:
```powershell
.\install.ps1
```

### Opcja 2: Skrypt Batch (jeśli PowerShell ma problemy)

1. Kliknij dwukrotnie na `install.bat`
2. Postępuj zgodnie z instrukcjami

Lub uruchom w wierszu poleceń:
```cmd
install.bat
```

## Co robi instalator?

1. **Sprawdza instalację Pythona** (wymagany 3.11+)
   - Jeśli Python nie jest zainstalowany, zaproponuje automatyczną instalację przez `winget`
   - Jeśli `winget` nie jest dostępny, wyświetli instrukcje ręcznej instalacji

2. **Tworzy środowisko wirtualne** (`.venv`)

3. **Aktualizuje pip** do najnowszej wersji

4. **Instaluje wszystkie zależności** projektu (w tym Streamlit, Pydantic, Pandas, Plotly itd.)

## Ręczna instalacja (jeśli automatyczna nie działa)

### Krok 1: Instalacja Pythona

1. Pobierz Pythona 3.11+ z: https://www.python.org/downloads/
2. **Ważne**: Podczas instalacji zaznacz opcję **"Add Python to PATH"**
3. Zakończ instalację

### Krok 2: Weryfikacja instalacji Pythona

Otwórz PowerShell i sprawdź:
```powershell
python --version
```

Powinno pokazać: `Python 3.11.x` lub nowsze

### Krok 3: Instalacja projektu

```powershell
# Przejdź do katalogu projektu
cd C:\Users\Krzysiek\Programowanie\soke

# Utwórz środowisko wirtualne
python -m venv .venv

# Aktywuj środowisko
.\.venv\Scripts\Activate.ps1

# Zainstaluj zależności
pip install -e .[dev]
```

## Uruchomienie po instalacji

```powershell
.\run.ps1
```

Lub:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run src/soke/app.py
```

## Rozwiązywanie problemów

### Problem: "Execution Policy"

Jeśli PowerShell blokuje uruchomienie skryptu:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: Python nie jest rozpoznawany po instalacji

1. Zrestartuj terminal/komputer
2. Sprawdź, czy Python jest w PATH: `python --version`
3. Jeśli nie, dodaj ręcznie:
   - Wyszukaj "Zmienne środowiskowe" w Windows
   - Dodaj `C:\Users\[TwojaNazwa]\AppData\Local\Programs\Python\Python3XX` do PATH

### Problem: winget nie jest dostępny

`winget` jest dostępny domyślnie w Windows 10 (1809+) i Windows 11.
Jeśli nie masz winget, użyj ręcznej instalacji Pythona (patrz wyżej).

### Problem: Błędy podczas instalacji zależności

Spróbuj:
```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .[dev]
```

## Wymagania systemowe

- **Windows 10/11** (zalecane)
- **Python 3.11+** (zostanie zainstalowany automatycznie)
- **Połączenie z internetem** (do pobrania zależności)
- **~500 MB miejsca na dysku** (Python + zależności)

## Weryfikacja instalacji

Po instalacji możesz sprawdzić, czy wszystko działa:

```powershell
.\.venv\Scripts\python.exe -c "import streamlit; import soke; print('OK')"
```

Powinno wyświetlić: `OK`


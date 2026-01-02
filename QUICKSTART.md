# Szybki Start - SOKE

## Dla nowych użytkowników (pierwsza instalacja)

### Krok 1: Instalacja

**Windows:**
```powershell
.\install.ps1
```

Lub kliknij dwukrotnie: `install.bat`

Instalator automatycznie:
- ✅ Sprawdzi czy Python 3.11+ jest zainstalowany
- ✅ Jeśli nie - zaproponuje instalację przez winget
- ✅ Utworzy środowisko wirtualne (`.venv`)
- ✅ Zainstaluje wszystkie zależności

### Krok 2: Uruchomienie

```powershell
.\run.ps1
```

Lub kliknij dwukrotnie: `run.bat`

Aplikacja otworzy się automatycznie w przeglądarce na `http://localhost:8501`

---

## Dla użytkowników z już zainstalowanym Pythonem

Jeśli masz już Python 3.11+, możesz pominąć automatyczną instalację:

```powershell
# Utwórz venv
python -m venv .venv

# Aktywuj
.\.venv\Scripts\Activate.ps1

# Zainstaluj zależności
pip install -e .[dev]

# Uruchom
streamlit run src/soke/app.py
```

---

## Sprawdzenie czy wszystko działa

```powershell
.\.venv\Scripts\python.exe -c "import streamlit; import soke; print('OK - wszystko działa!')"
```

---

## Rozwiązywanie problemów

### Problem: PowerShell blokuje skrypty

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: Python nie jest rozpoznawany

1. Zrestartuj terminal
2. Sprawdź: `python --version`
3. Jeśli nie działa - uruchom `install.ps1` ponownie

### Problem: Błędy podczas instalacji

```powershell
# Usuń stare środowisko
Remove-Item -Recurse -Force .venv

# Uruchom instalator ponownie
.\install.ps1
```

---

## Więcej informacji

- 📖 Pełna dokumentacja instalacji: [INSTALL.md](INSTALL.md)
- 📚 Dokumentacja projektu: [README.md](README.md)


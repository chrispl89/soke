"""Miejsce na ekstrakcję tabel stawek z PDF do YAML.

W praktyce (polecane podejście):
1) pobierz PDF (fetch_tariffs.py),
2) wyciągnij tabele (pdfplumber) -> CSV/JSON,
3) zmapuj do naszego schematu YAML.

Na MVP: uzupełnij wartości w src/soke/data/tariffs/2026/*.yaml ręcznie.
"""

def main() -> None:
    print("TODO: parse PDF and output YAML stubs")

if __name__ == "__main__":
    main()

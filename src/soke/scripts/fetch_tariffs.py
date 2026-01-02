from __future__ import annotations
from pathlib import Path
import requests

OUT = Path(__file__).resolve().parents[2] / "data" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

PDFS = {
    "pge_2026.pdf": "https://bip.ure.gov.pl/download/3/20345/PGEDystrybucja.pdf",
    "energa_2026.pdf": "https://bip.ure.gov.pl/download/3/20347/EnergaOperator.pdf",
    "enea_2026.pdf": "https://bip.ure.gov.pl/download/3/20348/ENEAOperator.pdf",
    "stoen_2026.pdf": "https://bip.ure.gov.pl/download/3/20339/StoenOperator.pdf",
    "tauron_2026.pdf": "https://www.tauron-dystrybucja.pl/-/media/offer-documents/dystrybucja/aktualna-taryfa/taryfa-tauron-dystrybucja-2026.ashx",
}

def main() -> None:
    for name, url in PDFS.items():
        path = OUT / name
        print(f"Downloading {name} ...")
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        path.write_bytes(r.content)
        print(f"OK -> {path}")

if __name__ == "__main__":
    main()

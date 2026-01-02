from __future__ import annotations
from pathlib import Path
import yaml
from soke.domain.models import OperatorTariffs, TariffGroupRates

DATA_DIR = Path(__file__).resolve().parent
TARIFFS_DIR = DATA_DIR / "tariffs"

def load_operator_tariffs(operator: str, year: int) -> OperatorTariffs:
    op_key = operator.strip().lower()
    path = TARIFFS_DIR / str(year) / f"{op_key}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Brak pliku taryfy: {path}")

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    groups = {k: TariffGroupRates(**v) for k, v in raw["groups"].items()}
    return OperatorTariffs(operator=raw["operator"], year=raw["year"], groups=groups)

# re-export for typing in ui
OperatorTariffs = OperatorTariffs

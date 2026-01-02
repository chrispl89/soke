from dataclasses import dataclass
from soke.domain.models import ClientInput, OperatorTariffs

@dataclass(frozen=True)
class ModuleCResult:
    loss_overordered_pln: float
    risk_penalty_pln: float

def calc_module_c(client: ClientInput, tariffs: OperatorTariffs, ordered_kw: float, peak_kw: float) -> ModuleCResult:
    rates = tariffs.groups.get(client.tariff_group)
    if not rates:
        raise ValueError(f"Brak stawek dla grupy {client.tariff_group} w YAML.")

    fixed = rates.contracted_power_fixed_pln_per_kw_per_month
    loss = max(ordered_kw - peak_kw, 0.0) * fixed * 12.0
    risk = max(peak_kw - ordered_kw, 0.0) * (10.0 * fixed)
    return ModuleCResult(loss_overordered_pln=float(loss), risk_penalty_pln=float(risk))

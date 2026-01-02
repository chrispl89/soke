from dataclasses import dataclass
from soke.domain.models import ClientInput, OperatorTariffs

@dataclass(frozen=True)
class ModuleBResult:
    cost_c11_pln: float
    cost_c12a_pln: float
    delta_pln: float  # dodatnie = C12a tańsza

def calc_module_b(client: ClientInput, tariffs: OperatorTariffs, offpeak_share: float) -> ModuleBResult:
    offpeak_share = max(0.0, min(1.0, offpeak_share))
    peak_share = 1.0 - offpeak_share

    c11 = tariffs.groups.get("C11")
    c12a = tariffs.groups.get("C12a")
    if not c11 or not c12a:
        raise ValueError("Brak stawek C11/C12a w taryfach operatora (YAML).")

    cost_c11 = client.annual_kwh * c11.c11_variable_pln_per_kwh
    cost_c12a = client.annual_kwh * (
        peak_share * c12a.c12a_day_pln_per_kwh + offpeak_share * c12a.c12a_offpeak_pln_per_kwh
    )

    delta = cost_c11 - cost_c12a
    return ModuleBResult(cost_c11_pln=float(cost_c11), cost_c12a_pln=float(cost_c12a), delta_pln=float(delta))

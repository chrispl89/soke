from dataclasses import dataclass
from soke.domain.models import ClientInput, OperatorTariffs

@dataclass(frozen=True)
class ModuleDResult:
    inductive_penalty_pln: float
    capacitive_penalty_pln: float
    avoidable_pln: float
    estimated_total_bill_pln: float

def calc_module_d(client: ClientInput, tariffs: OperatorTariffs, tg_phi: float, reactive_units: float) -> ModuleDResult:
    rates = tariffs.groups.get(client.tariff_group)
    if not rates:
        raise ValueError(f"Brak stawek dla grupy {client.tariff_group} w YAML.")

    inductive = 0.0
    if tg_phi > rates.tg_phi_limit:
        inductive = reactive_units * rates.inductive_penalty_pln_per_unit

    capacitive = reactive_units * rates.capacitive_penalty_pln_per_unit
    avoidable = inductive + capacitive

    est_active = client.annual_kwh * client.old_energy_price_pln_per_kwh
    est_total = est_active + avoidable

    return ModuleDResult(
        inductive_penalty_pln=float(inductive),
        capacitive_penalty_pln=float(capacitive),
        avoidable_pln=float(avoidable),
        estimated_total_bill_pln=float(est_total),
    )

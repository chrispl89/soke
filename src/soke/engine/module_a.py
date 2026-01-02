from dataclasses import dataclass
from soke.domain.models import ClientInput

@dataclass(frozen=True)
class ModuleAResult:
    annual_saving_pln: float

def calc_module_a(client: ClientInput) -> ModuleAResult:
    saving = (client.old_energy_price_pln_per_kwh - client.new_energy_price_pln_per_kwh) * client.annual_kwh
    return ModuleAResult(annual_saving_pln=float(saving))

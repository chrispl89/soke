from dataclasses import dataclass
from soke.domain.models import ClientInput

@dataclass(frozen=True)
class ModulePVResult:
    autoconsumption_kwh: float
    self_consumption_percent: float

def calc_module_pv(client: ClientInput) -> ModulePVResult:
    """
    Oblicza:
    1. Autokonsumpcję: produkcja całkowita minus energia oddana do sieci
    2. Udział produkcji własnej w całkowitym zapotrzebowaniu (w %)
    """
    # Autokonsumpcja = produkcja - energia oddana do sieci
    autoconsumption = client.pv_annual_production_kwh - client.pv_energy_sold_to_grid_kwh
    autoconsumption = max(0.0, autoconsumption)  # Nie może być ujemna
    
    # Udział produkcji własnej w całkowitym zapotrzebowaniu (w %)
    # Obliczany jako stosunek autokonsumpcji do całkowitego zużycia energii
    if client.annual_kwh > 0:
        self_consumption_percent = (autoconsumption / client.annual_kwh) * 100.0
    else:
        self_consumption_percent = 0.0
    
    return ModulePVResult(
        autoconsumption_kwh=float(autoconsumption),
        self_consumption_percent=float(self_consumption_percent)
    )

from __future__ import annotations
from pydantic import BaseModel, Field

class ClientInput(BaseModel):
    operator: str
    tariff_year: int
    tariff_group: str
    annual_kwh: float = Field(ge=0)

    old_energy_price_pln_per_kwh: float = Field(ge=0)
    new_energy_price_pln_per_kwh: float = Field(ge=0)

class TariffGroupRates(BaseModel):
    # MVP: tylko to, czego potrzebują moduły A–D
    c11_variable_pln_per_kwh: float
    c12a_day_pln_per_kwh: float
    c12a_offpeak_pln_per_kwh: float

    # Moduł C:
    contracted_power_fixed_pln_per_kw_per_month: float

    # Moduł D (MVP, docelowo per OSD dokładny wzór z taryfy):
    tg_phi_limit: float = 0.4
    inductive_penalty_pln_per_unit: float = 0.0
    capacitive_penalty_pln_per_unit: float = 0.0

class OperatorTariffs(BaseModel):
    operator: str
    year: int
    groups: dict[str, TariffGroupRates]

    def available_groups(self) -> list[str]:
        return sorted(self.groups.keys())

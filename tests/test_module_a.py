import pytest
from soke.domain.models import ClientInput
from soke.engine.module_a import calc_module_a

def test_module_a_basic():
    client = ClientInput(
        operator="PGE",
        tariff_year=2026,
        tariff_group="C11",
        annual_kwh=1000,
        old_energy_price_pln_per_kwh=1.0,
        new_energy_price_pln_per_kwh=0.7,
    )
    res = calc_module_a(client)
    assert res.annual_saving_pln == pytest.approx(300.0, rel=1e-9)

from soke.domain.models import ClientInput, OperatorTariffs, TariffGroupRates
from soke.engine.module_b import calc_module_b

def test_module_b_offpeak_split():
    tariffs = OperatorTariffs(
        operator="X",
        year=2026,
        groups={
            "C11": TariffGroupRates(
                c11_variable_pln_per_kwh=0.4,
                c12a_day_pln_per_kwh=0.0,
                c12a_offpeak_pln_per_kwh=0.0,
                contracted_power_fixed_pln_per_kw_per_month=6.0,
            ),
            "C12a": TariffGroupRates(
                c11_variable_pln_per_kwh=0.0,
                c12a_day_pln_per_kwh=0.5,
                c12a_offpeak_pln_per_kwh=0.2,
                contracted_power_fixed_pln_per_kw_per_month=6.0,
            ),
        },
    )

    client = ClientInput(
        operator="X",
        tariff_year=2026,
        tariff_group="C11",
        annual_kwh=1000,
        old_energy_price_pln_per_kwh=1.0,
        new_energy_price_pln_per_kwh=1.0,
    )

    res = calc_module_b(client, tariffs, offpeak_share=0.5)
    assert res.cost_c11_pln == 400.0
    assert res.cost_c12a_pln == 350.0
    assert res.delta_pln == 50.0

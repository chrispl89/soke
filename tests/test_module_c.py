from soke.domain.models import ClientInput, OperatorTariffs, TariffGroupRates
from soke.engine.module_c import calc_module_c

def test_module_c_loss_and_risk():
    tariffs = OperatorTariffs(
        operator="X",
        year=2026,
        groups={
            "C11": TariffGroupRates(
                c11_variable_pln_per_kwh=0.4,
                c12a_day_pln_per_kwh=0.0,
                c12a_offpeak_pln_per_kwh=0.0,
                contracted_power_fixed_pln_per_kw_per_month=10.0,
            ),
        },
    )
    client = ClientInput(
        operator="X",
        tariff_year=2026,
        tariff_group="C11",
        annual_kwh=0,
        old_energy_price_pln_per_kwh=0,
        new_energy_price_pln_per_kwh=0,
    )

    res = calc_module_c(client, tariffs, ordered_kw=100, peak_kw=60)
    assert res.loss_overordered_pln == 40 * 10 * 12
    assert res.risk_penalty_pln == 0.0

    res2 = calc_module_c(client, tariffs, ordered_kw=60, peak_kw=80)
    assert res2.loss_overordered_pln == 0.0
    assert res2.risk_penalty_pln == 20 * (10 * 10)

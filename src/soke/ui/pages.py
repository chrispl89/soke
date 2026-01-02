import streamlit as st
import pandas as pd
import plotly.express as px

from soke.domain.models import ClientInput
from soke.data.operators import OperatorTariffs
from soke.engine.module_a import calc_module_a
from soke.engine.module_b import calc_module_b
from soke.engine.module_c import calc_module_c
from soke.engine.module_d import calc_module_d
from soke.engine.summary import calc_summary, store_results
from soke.ui.components import kpi_card, section_title

def render_header() -> None:
    st.markdown("# SOKE – System Optymalizacji Kosztów Energii")
    st.caption("Czerwone = straty / ryzyko. Zielone = oszczędności. Niebieskie = dane techniczne.")

def render_tabs(client: ClientInput, tariffs: OperatorTariffs) -> None:
    tab_a, tab_b, tab_c, tab_d = st.tabs(
        ["Moduł A – Energia czynna", "Moduł B – Taryfy", "Moduł C – Moc", "Moduł D – Moc bierna"]
    )

    with tab_a:
        section_title("Zakup energii czynnej – szybki strzał")
        res = calc_module_a(client)
        store_results(module="A", payload=res.__dict__)

        c1, c2 = st.columns([1, 2])
        with c1:
            kpi_card("Roczna oszczędność", f"{res.annual_saving_pln:,.0f} zł", "Różnica ceny * zużycie", "gain")
        with c2:
            df = pd.DataFrame(
                [
                    {"Parametr": "Stara cena (zł/kWh)", "Wartość": client.old_energy_price_pln_per_kwh},
                    {"Parametr": "Nowa cena (zł/kWh)", "Wartość": client.new_energy_price_pln_per_kwh},
                    {"Parametr": "Roczne zużycie (kWh)", "Wartość": client.annual_kwh},
                ]
            )
            st.dataframe(df, use_container_width=True)

    with tab_b:
        section_title("Bitwa taryf – C11 vs C12a")
        pct_offpeak = st.slider("% zużycia w pozaszczycie (noc/weekend)", 0, 100, 40)
        res = calc_module_b(client, tariffs, offpeak_share=pct_offpeak / 100.0)
        store_results(module="B", payload=res.__dict__)

        c1, c2, c3 = st.columns(3)
        with c1:
            kpi_card("Koszt roczny C11", f"{res.cost_c11_pln:,.0f} zł", "Strefa jedna", "tech")
        with c2:
            kpi_card("Koszt roczny C12a", f"{res.cost_c12a_pln:,.0f} zł", "Dzień / noc", "tech")
        with c3:
            tone = "gain" if res.delta_pln > 0 else "loss"
            label = "Oszczędność na C12a" if res.delta_pln > 0 else "Strata na C12a"
            kpi_card(label, f"{abs(res.delta_pln):,.0f} zł", "C11 minus C12a", tone)

        chart_df = pd.DataFrame([{"Taryfa": "C11", "Koszt": res.cost_c11_pln}, {"Taryfa": "C12a", "Koszt": res.cost_c12a_pln}])
        fig = px.bar(chart_df, x="Taryfa", y="Koszt", title="Porównanie kosztu rocznego")
        st.plotly_chart(fig, use_container_width=True)

        st.info("Stawki pobieramy z YAML dla wybranego operatora (rok 2026). Pipeline z PDF jest w `scripts/`.")

    with tab_c:
        section_title("Audyt mocy – płacisz za to, co używasz?")
        ordered_kw = st.number_input("Moc zamówiona (kW)", min_value=0.0, value=100.0, step=1.0)
        peak_kw = st.number_input("Realny szczyt / Pik (kW)", min_value=0.0, value=60.0, step=1.0)

        res = calc_module_c(client, tariffs, ordered_kw=ordered_kw, peak_kw=peak_kw)
        store_results(module="C", payload=res.__dict__)

        c1, c2 = st.columns(2)
        with c1:
            if res.loss_overordered_pln > 0:
                kpi_card("Strata (nadmiar mocy)", f"{res.loss_overordered_pln:,.0f} zł/rok", "Zamówiona > Pik", "loss")
            else:
                kpi_card("Nadmiar mocy", "0 zł/rok", "Brak straty z nadmiaru", "gain")
        with c2:
            if res.risk_penalty_pln > 0:
                kpi_card("Ryzyko kary", f"{res.risk_penalty_pln:,.0f} zł", "Pik > Zamówiona (10×)", "loss")
            else:
                kpi_card("Ryzyko kary", "0 zł", "Pik nie przekracza zamówionej", "gain")

        chart_df = pd.DataFrame(
            [
                {"Wartość": "To co kupujesz (zamówiona kW)", "kW": ordered_kw},
                {"Wartość": "To co realnie potrzebujesz (pik kW)", "kW": peak_kw},
            ]
        )
        fig = px.bar(chart_df, x="Wartość", y="kW", title="Moc: zamówiona vs realna")
        st.plotly_chart(fig, use_container_width=True)

    with tab_d:
        section_title("Moc bierna – ciche złodzieje")
        tg_phi = st.number_input("tg φ (jeśli masz)", min_value=0.0, value=0.55, step=0.01)
        reactive_units = st.number_input("Jednostki mocy biernej z faktury (np. kvarh)", min_value=0.0, value=1200.0, step=10.0)

        res = calc_module_d(client, tariffs, tg_phi=tg_phi, reactive_units=reactive_units)
        store_results(module="D", payload=res.__dict__)

        c1, c2, c3 = st.columns(3)
        with c1:
            kpi_card(
                "Kara indukcyjna (szacunek)",
                f"{res.inductive_penalty_pln:,.0f} zł/rok",
                "tgφ > 0,4",
                "loss" if res.inductive_penalty_pln > 0 else "gain",
            )
        with c2:
            kpi_card(
                "Kara pojemnościowa (szacunek)",
                f"{res.capacitive_penalty_pln:,.0f} zł/rok",
                "100% kary / jednostkę",
                "loss" if res.capacitive_penalty_pln > 0 else "gain",
            )
        with c3:
            kpi_card("Potencjał do uniknięcia", f"{res.avoidable_pln:,.0f} zł/rok", "po kompensacji", "gain")

        pie_df = pd.DataFrame(
            [
                {"Składnik": "Kary do uniknięcia", "PLN": res.avoidable_pln},
                {"Składnik": "Pozostała część", "PLN": max(res.estimated_total_bill_pln - res.avoidable_pln, 0.0)},
            ]
        )
        fig = px.pie(pie_df, names="Składnik", values="PLN", title="Udział kar w rachunku (szacunek)")
        st.plotly_chart(fig, use_container_width=True)

def render_footer(client: ClientInput, tariffs: OperatorTariffs) -> None:
    st.divider()
    st.markdown("## Podsumowanie roczne")
    summary = calc_summary(client, tariffs)

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Suma strat (czerwone)", f"{summary.total_losses_pln:,.0f} zł/rok", "kary + ryzyka + nadmiar mocy", "loss")
    with c2:
        kpi_card("Suma oszczędności (zielone)", f"{summary.total_savings_pln:,.0f} zł/rok", "po optymalizacji", "gain")
    with c3:
        kpi_card("ROI / czas zwrotu", summary.roi_label, "jeśli inwestycja (np. kompensator)", "tech")

    st.caption("Źródła stawek: taryfy OSD na 2026 r. zatwierdzone przez Prezesa URE (obowiązują od 01.01.2026).")

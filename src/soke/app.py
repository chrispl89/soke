import streamlit as st
from soke.ui.theme import inject_theme
from soke.ui.pages import render_header, render_tabs, render_footer
from soke.data.operators import load_operator_tariffs
from soke.domain.models import ClientInput

def main() -> None:
    st.set_page_config(
        page_title="SOKE – System Optymalizacji Kosztów Energii",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_theme()

    render_header()

    with st.sidebar:
        st.markdown("### Dane wejściowe")
        operator = st.selectbox("Operator (OSD)", ["Energa", "Enea", "Tauron", "PGE", "Stoen"])
        year = st.selectbox("Rok taryfy", [2026], index=0)

        tariffs = load_operator_tariffs(operator=operator, year=year)

        tariff_group = st.selectbox("Grupa taryfowa (biznes)", tariffs.available_groups(), index=0)

        annual_kwh = st.number_input("Roczne zużycie (kWh)", min_value=0.0, value=120000.0, step=1000.0)
        old_energy_price = st.number_input("Stara cena energii czynnej (zł/kWh)", min_value=0.0, value=0.85, step=0.01)
        new_energy_price = st.number_input("Nowa cena energii czynnej (zł/kWh)", min_value=0.0, value=0.72, step=0.01)
        
        st.divider()
        st.markdown("### Fotowoltaika (opcjonalnie)")
        pv_annual_production = st.number_input("Roczny wolumen produkcji z PV (kWh)", min_value=0.0, value=0.0, step=1000.0, help="Całkowita roczna produkcja z instalacji fotowoltaicznej")
        pv_energy_sold = st.number_input("Energia oddana do sieci (kWh)", min_value=0.0, value=0.0, step=1000.0, help="Ilość energii oddanej do sieci w ciągu roku")
        
        st.divider()
        st.markdown("### Inwestycja (opcjonalnie)")
        investment_pln = st.number_input("Koszt inwestycji (zł)", min_value=0.0, value=0.0, step=1000.0, help="Np. koszt kompensatora mocy biernej")
        st.session_state["soke_investment_pln"] = investment_pln

        client = ClientInput(
            operator=operator,
            tariff_year=year,
            tariff_group=tariff_group,
            annual_kwh=annual_kwh,
            old_energy_price_pln_per_kwh=old_energy_price,
            new_energy_price_pln_per_kwh=new_energy_price,
            pv_annual_production_kwh=pv_annual_production,
            pv_energy_sold_to_grid_kwh=pv_energy_sold,
        )

    render_tabs(client=client, tariffs=tariffs)
    render_footer(client=client, tariffs=tariffs)

if __name__ == "__main__":
    main()

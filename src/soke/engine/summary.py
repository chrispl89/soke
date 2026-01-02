from __future__ import annotations
from dataclasses import dataclass
import streamlit as st
from soke.domain.models import ClientInput, OperatorTariffs

KEY = "soke_results"

def store_results(module: str, payload: dict) -> None:
    if KEY not in st.session_state:
        st.session_state[KEY] = {}
    st.session_state[KEY][module] = payload

@dataclass(frozen=True)
class SummaryResult:
    total_losses_pln: float
    total_savings_pln: float
    roi_label: str

def calc_summary(client: ClientInput, tariffs: OperatorTariffs) -> SummaryResult:
    results = st.session_state.get(KEY, {})

    # Straty: moduł C (nadmiar mocy + ryzyko) + moduł D (kary)
    loss_c = float(results.get("C", {}).get("loss_overordered_pln", 0.0)) + float(results.get("C", {}).get("risk_penalty_pln", 0.0))
    loss_d = float(results.get("D", {}).get("inductive_penalty_pln", 0.0)) + float(results.get("D", {}).get("capacitive_penalty_pln", 0.0))
    total_losses = loss_c + loss_d

    # Oszczędności: moduł A (zmiana ceny energii) + moduł B (jeśli C12a tańsza)
    save_a = float(results.get("A", {}).get("annual_saving_pln", 0.0))
    delta_b = float(results.get("B", {}).get("delta_pln", 0.0))
    save_b = max(delta_b, 0.0)
    total_savings = save_a + save_b

    # ROI: jeśli user poda koszt inwestycji (np. kompensator) - MVP: stałe pole
    # Trzymamy w session_state, żeby UI mogło go ustawiać w przyszłości.
    investment = float(st.session_state.get("soke_investment_pln", 0.0))
    if investment > 0 and total_savings > 0:
        years = investment / total_savings
        roi_label = f"{years:.2f} roku"
    elif investment > 0 and total_savings <= 0:
        roi_label = "brak zwrotu"
    else:
        roi_label = "—"

    return SummaryResult(total_losses_pln=total_losses, total_savings_pln=total_savings, roi_label=roi_label)

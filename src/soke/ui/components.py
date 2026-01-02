import streamlit as st

def kpi_card(title: str, value: str, subtitle: str, tone: str) -> None:
    st.markdown(
        f'''
        <div class="soke-card">
          <div class="soke-sub">{title}</div>
          <div class="soke-kpi {tone}">{value}</div>
          <div class="soke-sub">{subtitle}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

def section_title(text: str) -> None:
    st.markdown(f"### {text}")

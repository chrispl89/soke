import streamlit as st

def inject_theme() -> None:
    st.markdown(
        '''
        <style>
        :root {
          --bg: #0B0F14;
          --card: #111827;
          --text: #E5E7EB;
          --muted: #9CA3AF;

          --loss: #EF4444;
          --gain: #22C55E;
          --tech: #60A5FA;
          --accent: #A78BFA;
        }

        html, body, [data-testid="stAppViewContainer"] {
          background: var(--bg);
          color: var(--text);
        }

        [data-testid="stSidebar"] {
          background: #0A0E13;
        }

        .soke-card {
          background: var(--card);
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 16px;
          padding: 16px 18px;
        }

        .soke-kpi {
          font-size: 42px;
          font-weight: 800;
          line-height: 1.1;
        }
        .soke-sub {
          color: var(--muted);
          font-size: 13px;
        }

        .loss { color: var(--loss); }
        .gain { color: var(--gain); }
        .tech { color: var(--tech); }
        </style>
        ''',
        unsafe_allow_html=True,
    )

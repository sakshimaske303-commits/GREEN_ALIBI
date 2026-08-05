import streamlit as st

# ============================================================
# GREEN ALIBI — Custom Theme v2
# Palette: deep navy (base) + magenta + hot pink + teal + black
# ============================================================

NAVY_DARK = "#0A1128"      # main background
NAVY_MED = "#101B3D"       # sidebar / card background
MAGENTA = "#E91E8C"        # primary accent — headers, highlights
PINK = "#FF6EC7"           # secondary accent
TEAL = "#00D9C0"           # tertiary accent — borders, buttons, links
BLACK = "#000000"          # deep contrast
TEXT_LIGHT = "#F2F2F5"     # main body text on dark background


def apply_custom_style():
    st.markdown(f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

    /* ---- Keep header visible (needed for the sidebar
    open/close button) but hide only the Deploy button ---- */
    [data-testid="stHeader"] {{
        background-color: {NAVY_DARK} !important;
        height: 3rem !important;
    }}
    [data-testid="stAppDeployButton"] {{
        display: none !important;
    }}
    [data-testid="stDecoration"] {{
        display: none !important;
    }}
    #MainMenu {{
        visibility: hidden !important;
    }}
    .block-container {{
        padding-top: 1rem !important;
    }}

    /* ---- Sidebar collapse/expand button — safety net
    covering every naming variant Streamlit has used
    across versions, since it's invisible-by-default on
    a dark theme and hard to see on mobile otherwise ---- */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="baseButton-header"],
    [data-testid="stHeader"] button,
    [data-testid*="ollapse" i],
    button[kind="header"] {{
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
    }}
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"] {{
        position: fixed !important;
        top: 12px !important;
        left: 12px !important;
        background: {NAVY_MED} !important;
        border: 1.5px solid {TEAL} !important;
        border-radius: 8px !important;
        padding: 4px !important;
    }}
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="baseButton-header"] svg,
    [data-testid="stHeader"] button svg,
    button[kind="header"] svg {{
        fill: {TEAL} !important;
        stroke: {TEAL} !important;
        opacity: 1 !important;
    }}

    /* ---- Base app ---- */
    .stApp {{
        background-color: {NAVY_DARK};
        color: {TEXT_LIGHT};
        font-family: 'Poppins', sans-serif;
    }}

    /* ---- Sidebar — same dark-gradient nav-pill language used
    across the whole portfolio (matched to Double Jeopardy) ---- */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {NAVY_MED} 0%, {NAVY_DARK} 100%);
        border-right: 1px solid rgba(0, 217, 192, 0.2);
    }}
    section[data-testid="stSidebar"] * {{
        color: {TEXT_LIGHT} !important;
    }}
    section[data-testid="stSidebar"] a {{
        border-radius: 8px !important;
        padding: 8px 14px !important;
        transition: all 0.2s ease;
    }}
    section[data-testid="stSidebar"] a:hover {{
        background: rgba(0, 217, 192, 0.12) !important;
        border-left: 3px solid {TEAL};
    }}
    section[data-testid="stSidebar"] a[aria-current="page"],
    section[data-testid="stSidebar"] [aria-selected="true"] {{
        background: rgba(233, 30, 140, 0.18) !important;
        border-left: 3px solid {MAGENTA};
        font-weight: 700 !important;
    }}

    /* ---- Headers ---- */
    h1 {{
        color: {MAGENTA} !important;
        font-weight: 800 !important;
        border-bottom: 3px solid {TEAL};
        text-align: center !important;
        padding-bottom: 0.4rem;
    }}
    h2 {{
        color: {TEAL} !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin-top: 1.5rem !important;
    }}
    h3 {{
        color: {PINK} !important;
        text-align: center !important;
        font-weight: 600 !important;
    }}

    /* ---- Body text ---- */
    p, li, span, label, .stMarkdown {{
        color: {TEXT_LIGHT} !important;
    }}

    /* ---- Metric cards ---- */
    div[data-testid="stMetric"] {{
        background-color: {NAVY_MED};
        border: 1px solid {TEAL};
        border-left: 5px solid {MAGENTA};
        border-radius: 8px;
        padding: 12px 16px;
    }}
    div[data-testid="stMetricLabel"] {{
        color: {TEAL} !important;
        font-weight: 600;
    }}
    div[data-testid="stMetricValue"] {{
        color: {TEXT_LIGHT} !important;
    }}

    /* ---- Info / warning / success callouts ---- */
    div[data-testid="stAlert"] {{
        background-color: {NAVY_MED} !important;
        border-radius: 8px;
        border-left: 5px solid {TEAL};
        color: {TEXT_LIGHT} !important;
    }}

    /* ---- Buttons ---- */
    .stButton > button {{
        background-color: {TEAL};
        color: {BLACK};
        border-radius: 6px;
        border: none;
        font-weight: 700;
    }}
    .stButton > button:hover {{
        background-color: {MAGENTA};
        color: white;
    }}

    /* ---- Tables / dataframes ---- */
    div[data-testid="stDataFrame"] {{
        border: 1px solid {TEAL};
        border-radius: 6px;
    }}

    /* ---- Tabs ---- */
    button[data-baseweb="tab"] {{
        color: {TEXT_LIGHT};
        font-weight: 600;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {MAGENTA};
        border-bottom: 3px solid {TEAL};
    }}

    /* ---- Horizontal rule ---- */
    hr {{
        border-top: 2px solid {TEAL};
    }}

    </style>
    """, unsafe_allow_html=True)


def section_divider():
    st.markdown(f"<hr style='border-top: 2px solid {TEAL}; margin: 1.5rem 0;'>", unsafe_allow_html=True)


def styled_caption(text):
    st.markdown(
        f"<p style='color:{PINK}; font-style:italic; text-align:center; margin-top:-10px;'>{text}</p>",
        unsafe_allow_html=True
    )


def page_footer():
    """Standard footer used on app.py — name, role, and GitHub link, in a styled card."""
    st.markdown(f"""
    <div style='
        background-color:{NAVY_MED};
        border: 2px solid {TEAL};
        border-radius: 14px;
        padding: 28px 32px;
        margin-top: 2.5rem;
        text-align: center;
    '>
        <p style='font-size:2rem; font-weight:800; color:{MAGENTA}; margin-bottom:4px;'>
            Sakshi D. Maske
        </p>
        <p style='font-size:1.05rem; color:{TEXT_LIGHT}; margin-top:0; margin-bottom:18px;'>
            Independent Geospatial Researcher
        </p>
        <a href='https://github.com/sakshimaske303-commits/GREEN_ALIBI' target='_blank' style='
            display:inline-block;
            background-color:{TEAL};
            color:{BLACK};
            font-weight:700;
            padding:12px 26px;
            border-radius:8px;
            text-decoration:none;
            font-size:1rem;
        '>
            🔗 View Full Project on GitHub
        </a>
    </div>
    """, unsafe_allow_html=True)
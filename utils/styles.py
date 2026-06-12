"""utils/styles.py — inject the exact CSS matching the screenshot UI"""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ── Reset & base ─────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── Page background ───────────────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background: #f5f5f0;
}
[data-testid="stMain"] {
    background: #f5f5f0;
}

/* ── Sidebar — dark green matching screenshot ───────────────── */
[data-testid="stSidebar"] {
    background: #1a2e22 !important;
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: #d4e8d8 !important;
}
[data-testid="stSidebar"] .sidebar-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 20px 16px 6px;
}
[data-testid="stSidebar"] .sidebar-logo-icon {
    width: 36px; height: 36px; border-radius: 10px;
    background: #2d6a4f;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
[data-testid="stSidebar"] .sidebar-brand {
    font-size: 15px; font-weight: 700; color: #ffffff !important;
    line-height: 1.2;
}
[data-testid="stSidebar"] .sidebar-sub {
    font-size: 11px; color: #8ab89a !important;
}
[data-testid="stSidebar"] .sidebar-section {
    font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
    color: #5a8a6a !important; padding: 16px 16px 4px;
    text-transform: uppercase;
}
[data-testid="stSidebar"] .stRadio label {
    color: #b8d4be !important; font-size: 14px !important;
}
[data-testid="stSidebar"] .sidebar-user {
    display: flex; align-items: center; gap: 10px;
    padding: 12px 16px; border-top: 1px solid #2a4a32;
    margin-top: 8px;
}
[data-testid="stSidebar"] .sidebar-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    background: #2d6a4f;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 700; color: #ffffff !important;
}
[data-testid="stSidebar"] .sidebar-username {
    font-size: 13px; font-weight: 600; color: #ffffff !important;
}
[data-testid="stSidebar"] .sidebar-usertag {
    font-size: 11px; color: #7aaa8a !important;
}

/* ── Streamlit radio → sidebar nav style ────────────────────── */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 2px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 8px 14px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: background 0.15s !important;
    font-size: 14px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #2a3d2e !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] + div label {
    background: #2d5e3a !important; color: #ffffff !important;
}

/* ── Top page header ────────────────────────────────────────── */
.page-header {
    display: flex; justify-content: space-between; align-items: flex-start;
    margin-bottom: 20px;
}
.page-title { font-size: 26px; font-weight: 700; color: #1a1a1a; margin: 0; }
.page-subtitle { font-size: 14px; color: #666; margin: 2px 0 0; }
.phase-badge {
    background: #e8f5ee; color: #1a7a5e;
    border: 1px solid #b8e0cc;
    border-radius: 20px; padding: 5px 14px; font-size: 13px; font-weight: 600;
    display: flex; align-items: center; gap: 5px;
}

/* ── Metric summary cards (top row) ──────────────────────────── */
.metric-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 18px 20px;
    border: 1px solid #e8e8e0;
    height: 100%;
}
.metric-label { font-size: 13px; color: #888; font-weight: 500; margin-bottom: 6px; }
.metric-value-green { font-size: 28px; font-weight: 700; color: #1a7a5e; line-height: 1; }
.metric-value-amber { font-size: 28px; font-weight: 700; color: #c17f24; line-height: 1; }
.metric-value-blue  { font-size: 28px; font-weight: 700; color: #2c5fa8; line-height: 1; }
.metric-value-gray  { font-size: 28px; font-weight: 700; color: #444; line-height: 1; }
.metric-sub { font-size: 12px; color: #999; margin-top: 4px; }

/* ── Section card (white panel) ─────────────────────────────── */
.section-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 20px 22px;
    border: 1px solid #e8e8e0;
    margin-bottom: 16px;
}
.section-title {
    font-size: 15px; font-weight: 600; color: #1a1a1a;
    margin: 0 0 16px; display: flex; align-items: center; gap: 8px;
}

/* ── Skill bar row ──────────────────────────────────────────── */
.skill-row {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 10px;
}
.skill-name { font-size: 13px; color: #444; width: 72px; flex-shrink: 0; }
.skill-bar-wrap {
    flex: 1; height: 8px; background: #f0f0ea;
    border-radius: 4px; overflow: hidden;
}
.skill-bar-fill { height: 100%; border-radius: 4px; }
.skill-pct { font-size: 12px; color: #888; width: 36px; text-align: right; flex-shrink: 0; }

/* ── Skill gap row ──────────────────────────────────────────── */
.gap-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 9px 0; border-bottom: 1px solid #f2f2ec;
}
.gap-skill { font-size: 14px; color: #222; }
.badge {
    font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 6px;
}
.badge-missing  { background: #fff0ee; color: #c0392b; }
.badge-partial  { background: #fffbe6; color: #9a6c00; }
.badge-strong   { background: #e8f5ee; color: #1a7a5e; }

/* ── Roadmap week card ──────────────────────────────────────── */
.week-card {
    background: #fafaf8; border: 1px solid #e8e8e0;
    border-radius: 12px; padding: 14px 16px;
}
.week-label { font-size: 11px; color: #999; font-weight: 600; margin-bottom: 4px; }
.week-title { font-size: 14px; font-weight: 700; color: #1a1a1a; margin-bottom: 6px; }
.week-desc  { font-size: 12px; color: #666; line-height: 1.5; }

/* ── Interview question card ────────────────────────────────── */
.iq-card {
    background: #fafaf8; border: 1px solid #e8e8e0;
    border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;
}
.iq-label { font-size: 11px; color: #999; font-weight: 600; margin-bottom: 5px; }
.iq-text  { font-size: 14px; color: #1a1a1a; line-height: 1.5; }

/* ── Job recommendation row ────────────────────────────────── */
.job-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 0; border-bottom: 1px solid #f2f2ec;
}
.job-title  { font-size: 14px; font-weight: 600; color: #1a1a1a; }
.job-meta   { font-size: 12px; color: #888; margin-top: 1px; }
.job-pct-green  { font-size: 14px; font-weight: 700; color: #1a7a5e; }
.job-pct-amber  { font-size: 14px; font-weight: 700; color: #c17f24; }
.job-pct-blue   { font-size: 14px; font-weight: 700; color: #2c5fa8; }

/* ── CTA button ─────────────────────────────────────────────── */
.cta-btn {
    display: block; text-align: center;
    background: transparent; border: 1.5px solid #ccc;
    border-radius: 10px; padding: 11px 0; font-size: 14px;
    font-weight: 600; color: #222; cursor: pointer; margin-top: 12px;
    text-decoration: none;
}

/* ── Streamlit buttons ──────────────────────────────────────── */
.stButton > button {
    background: #1a2e22 !important; color: #ffffff !important;
    border: none !important; border-radius: 10px !important;
    padding: 10px 24px !important; font-weight: 600 !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #2d5e3a !important; color: #ffffff !important;
}

/* ── Streamlit inputs ───────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] select {
    border-radius: 8px !important;
    border: 1px solid #ddd !important;
    background: #ffffff !important;
}

/* ── Divider ────────────────────────────────────────────────── */
hr { border-color: #e8e8e0 !important; margin: 16px 0 !important; }

/* ── Info/warning boxes ─────────────────────────────────────── */
.info-pill {
    background: #e8f5ee; color: #1a7a5e;
    border-radius: 8px; padding: 10px 14px;
    font-size: 13px; margin-bottom: 14px;
    border-left: 3px solid #1a7a5e;
}
.warn-pill {
    background: #fff8e6; color: #9a6c00;
    border-radius: 8px; padding: 10px 14px;
    font-size: 13px; margin-bottom: 14px;
    border-left: 3px solid #e8b84b;
}

/* ── Progress bar override ───────────────────────────────────── */
.stProgress > div > div { border-radius: 6px; }
</style>
"""


def inject():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

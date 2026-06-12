"""app.py — AI Career Copilot main entry point"""
import streamlit as st

st.set_page_config(
    page_title="Career Copilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject global CSS before anything else
from utils.styles import inject
inject()

from utils.session import get_user, has_dashboard

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo + brand
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🚀</div>
        <div>
            <div class="sidebar-brand">Career Copilot</div>
            <div class="sidebar-sub">AI-Powered Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # MAIN section
    st.markdown('<div class="sidebar-section">MAIN</div>', unsafe_allow_html=True)
    main_page = st.radio(
        "main_nav",
        ["🏠  Dashboard", "📄  Resume", "📊  Skill Gap", "🗺️  Roadmap"],
        label_visibility="collapsed",
        key="main_nav",
    )

    # ADVANCED section
    st.markdown('<div class="sidebar-section">ADVANCED</div>', unsafe_allow_html=True)
    adv_page = st.radio(
        "adv_nav",
        ["🎤  Interview AI", "🐙  GitHub Score", "💼  Jobs"],
        label_visibility="collapsed",
        key="adv_nav",
    )

    st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # User info at bottom
    user_name = get_user()
    initials  = user_name[:1].upper() if user_name else "G"
    st.markdown(f"""
    <div class="sidebar-user">
        <div class="sidebar-avatar">{initials}</div>
        <div>
            <div class="sidebar-username">{user_name}</div>
            <div class="sidebar-usertag">AIML Student</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Determine active page ─────────────────────────────────────────────────────
# nav_override lets dashboard buttons navigate programmatically
override = st.session_state.pop("nav_override", None)

if override:
    active = override
elif adv_page and st.session_state.get("adv_nav_prev") != adv_page:
    active = adv_page
    st.session_state["adv_nav_prev"] = adv_page
    st.session_state["main_nav_prev"] = None
elif main_page and st.session_state.get("main_nav_prev") != main_page:
    active = main_page
    st.session_state["main_nav_prev"] = main_page
    st.session_state["adv_nav_prev"] = None
else:
    # Default: whichever was last clicked
    active = st.session_state.get("active_page", "🏠  Dashboard")

st.session_state["active_page"] = active

# ── Route to page ─────────────────────────────────────────────────────────────
if "Dashboard" in active:
    from pages.dashboard    import show
elif "Resume" in active:
    from pages.resume       import show
elif "Skill Gap" in active:
    from pages.skill_gap    import show
elif "Roadmap" in active:
    from pages.roadmap      import show
elif "Interview" in active:
    from pages.interview_ai import show
elif "GitHub" in active:
    from pages.github_score import show
elif "Jobs" in active:
    from pages.jobs         import show
else:
    from pages.dashboard    import show

show()

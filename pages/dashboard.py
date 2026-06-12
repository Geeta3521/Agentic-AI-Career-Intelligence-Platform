"""pages/dashboard.py — matches the screenshot exactly"""
import streamlit as st
from utils.session import get_dashboard, has_dashboard, get_user, get_role
from utils.ai_engine import ai_json


def _skill_bar(name, pct, color):
    bar_color = {"green": "#1a7a5e", "amber": "#c17f24", "red": "#c0392b"}.get(color, "#1a7a5e")
    st.markdown(f"""
    <div class="skill-row">
        <span class="skill-name">{name}</span>
        <div class="skill-bar-wrap">
            <div class="skill-bar-fill" style="width:{pct}%;background:{bar_color}"></div>
        </div>
        <span class="skill-pct">{pct}%</span>
    </div>
    """, unsafe_allow_html=True)


def _gap_row(skill, status):
    badge_cls = {"Missing": "badge-missing", "Partial": "badge-partial", "Strong": "badge-strong"}.get(status, "badge-missing")
    icon = {"Missing": "✕", "Partial": "—", "Strong": "✓"}.get(status, "✕")
    st.markdown(f"""
    <div class="gap-row">
        <span style="font-size:13px;color:#888;margin-right:8px">{icon}</span>
        <span class="gap-skill">{skill}</span>
        <span class="badge {badge_cls}">{status}</span>
    </div>
    """, unsafe_allow_html=True)


def show():
    if not has_dashboard():
        st.markdown("""
        <div style="background:#fff;border-radius:14px;padding:48px;text-align:center;border:1px solid #e8e8e0;margin-top:20px">
            <div style="font-size:48px;margin-bottom:16px">🚀</div>
            <h2 style="color:#1a1a1a;margin:0 0 8px">Welcome to AI Career Copilot</h2>
            <p style="color:#666;font-size:15px;margin:0 0 24px">
                Upload your resume to generate your personalized placement dashboard
            </p>
            <div style="background:#e8f5ee;border-radius:10px;padding:14px 20px;
                        display:inline-block;color:#1a7a5e;font-size:14px;font-weight:600">
                👈 Go to Resume in the sidebar to get started
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    d = get_dashboard()
    role = get_role()
    user = get_user()

    # ── Page header ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="page-header">
        <div>
            <div class="page-title">Dashboard</div>
            <div class="page-subtitle">Your placement readiness at a glance</div>
        </div>
        <div class="phase-badge">✦ Phase 1 Active</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Top metric cards ─────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    ats   = d.get("ats_score", 78)
    match = d.get("skill_match", 72)
    ready = d.get("readiness_score", 82)
    gh    = d.get("github_score", 64)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ATS Score</div>
            <div class="metric-value-green">{ats}<span style="font-size:16px;color:#888">/100</span></div>
            <div class="metric-sub">Good · {d.get('ats_gaps', 3)} gaps</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Skill Match</div>
            <div class="metric-value-amber">{match}<span style="font-size:16px;color:#888">%</span></div>
            <div class="metric-sub">{role} role</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Readiness</div>
            <div class="metric-value-blue">{ready}<span style="font-size:16px;color:#888">/100</span></div>
            <div class="metric-sub">Placement score</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">GitHub Score</div>
            <div class="metric-value-gray">{gh}<span style="font-size:16px;color:#888">/100</span></div>
            <div class="metric-sub">{d.get('github_suggestions', 3)} suggestions</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Row 2: Skill Proficiency + Skill Gap ─────────────────────────────────
    col_left, col_right = st.columns([1.1, 1])

    with col_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 Skill Proficiency</div>', unsafe_allow_html=True)
        skills = d.get("skill_proficiency", [
            {"name": "Python",  "pct": 90, "color": "green"},
            {"name": "ML / DL", "pct": 80, "color": "green"},
            {"name": "NLP",     "pct": 65, "color": "amber"},
            {"name": "FastAPI", "pct": 30, "color": "red"},
            {"name": "Docker",  "pct": 20, "color": "red"},
            {"name": "AWS",     "pct": 15, "color": "red"},
            {"name": "MLOps",   "pct": 25, "color": "red"},
        ])
        for s in skills:
            _skill_bar(s["name"], s["pct"], s["color"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">🎯 Skill Gap — {role}</div>', unsafe_allow_html=True)
        gaps = d.get("skill_gaps", [
            {"skill": "FastAPI", "status": "Missing"},
            {"skill": "Docker",  "status": "Missing"},
            {"skill": "NLP",     "status": "Partial"},
            {"skill": "MLOps",   "status": "Missing"},
            {"skill": "Python",  "status": "Strong"},
        ])
        for g in gaps:
            _gap_row(g["skill"], g["status"])
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 3: Roadmap ───────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🗺️ 4-Week Personalized Roadmap</div>', unsafe_allow_html=True)

    weeks = d.get("roadmap", [
        {"week": "Week 1", "title": "FastAPI Basics",       "desc": "Build REST APIs, request handling, and deploy a simple ML endpoint"},
        {"week": "Week 2", "title": "Deploy ML Project",    "desc": "Package Eye Disease model into an API with Streamlit frontend"},
        {"week": "Week 3", "title": "Docker + MLOps",       "desc": "Dockerize your app, add CI/CD pipeline on GitHub Actions"},
        {"week": "Week 4", "title": "Mock Interviews",      "desc": "Use AI Interview Simulator daily — Eye Disease, NLP, system design"},
    ])
    w_cols = st.columns(len(weeks))
    for col, w in zip(w_cols, weeks):
        with col:
            st.markdown(f"""
            <div class="week-card">
                <div class="week-label">{w['week']}</div>
                <div class="week-title">{w['title']}</div>
                <div class="week-desc">{w['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Row 4: Interview Simulator preview + Job Recommendations ─────────────
    col_int, col_jobs = st.columns([1.1, 1])

    with col_int:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎤 AI Interview Simulator</div>', unsafe_allow_html=True)
        project_name = d.get("top_project", "Eye Disease Detection")
        st.markdown(f'<p style="font-size:13px;color:#888;margin:-8px 0 12px">Based on your {project_name} project</p>', unsafe_allow_html=True)

        qs = d.get("preview_questions", [
            {"cat": "Technical",       "q": "Why did you choose EfficientNetB0 over ResNet or VGG for your eye disease classifier?"},
            {"cat": "Explainability",  "q": "Walk me through how Grad-CAM works and what it showed in your model's predictions."},
            {"cat": "Challenges",      "q": "What data imbalance issues did you face and how did you address them?"},
        ])
        for item in qs:
            st.markdown(f"""
            <div class="iq-card">
                <div class="iq-label">{item['cat']}</div>
                <div class="iq-text">{item['q']}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Start Mock Interview ↗", key="dash_interview"):
            st.session_state["nav_override"] = "🎤 Interview AI"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_jobs:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💼 Job Recommendations</div>', unsafe_allow_html=True)

        jobs = d.get("job_recommendations", [
            {"title": "AI/ML Intern",       "meta": "TCS · Bengaluru",     "pct": 92, "color": "green"},
            {"title": "ML Engineer Intern",  "meta": "Infosys · Remote",    "pct": 87, "color": "green"},
            {"title": "Data Analyst",        "meta": "Wipro · Pune",        "pct": 74, "color": "amber"},
            {"title": "Software Developer",  "meta": "Startup · Hyderabad", "pct": 68, "color": "amber"},
        ])
        for j in jobs:
            pct_cls = f"job-pct-{j['color']}"
            st.markdown(f"""
            <div class="job-row">
                <div>
                    <div class="job-title">{j['title']}</div>
                    <div class="job-meta">{j['meta']}</div>
                </div>
                <div class="{pct_cls}">{j['pct']}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<a class="cta-btn">View all matches ↗</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

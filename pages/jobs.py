"""pages/jobs.py — Placement Readiness + Job Recommendations"""
import streamlit as st
from utils.session import get_dashboard, has_dashboard, get_role, get_user


def show():
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-title">Jobs</div>
            <div class="page-subtitle">Placement readiness score and job recommendations tailored to you</div>
        </div>
        <div class="phase-badge">✦ Phase 2</div>
    </div>
    """, unsafe_allow_html=True)

    if not has_dashboard():
        st.markdown('<div class="warn-pill">⚠️ Please upload your resume first on the <b>Resume</b> page.</div>', unsafe_allow_html=True)
        return

    d     = get_dashboard()
    role  = get_role()
    user  = get_user()
    score = d.get("readiness_score", 82)
    level = d.get("readiness_level", "Almost Ready")

    # ── Readiness score hero ──────────────────────────────────────────────────
    level_colors = {
        "Not Ready":      "#c0392b",
        "Getting Started":"#e67e22",
        "Almost Ready":   "#c17f24",
        "Ready":          "#1a7a5e",
        "Highly Ready":   "#0d5e3a",
    }
    lc = level_colors.get(level, "#1a7a5e")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#e8f5ee,#d1ead8);border-radius:16px;
                padding:30px;text-align:center;margin-bottom:20px;border:1px solid #b8dfc4">
        <div style="font-size:72px;font-weight:700;color:{lc};line-height:1">{score}</div>
        <div style="font-size:18px;color:#333;margin-top:6px">/ 100 &nbsp; Placement Readiness Score</div>
        <div style="display:inline-block;background:{lc}22;color:{lc};
                    padding:6px 20px;border-radius:20px;font-weight:700;font-size:15px;
                    border:1px solid {lc}55;margin-top:10px">{level}</div>
        <p style="color:#3a8a5a;font-size:14px;margin-top:12px">
            Hey {user}! You're well on your way — close the remaining skill gaps and you'll be placement-ready.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Breakdown bars ────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Readiness Breakdown</div>', unsafe_allow_html=True)

    breakdown_labels = {
        "resume_quality":      "Resume Quality",
        "technical_skills":    "Technical Skills",
        "project_portfolio":   "Project Portfolio",
        "dsa_problem_solving": "DSA & Problem Solving",
        "communication":       "Communication",
        "online_presence":     "Online Presence",
    }
    for key, label in breakdown_labels.items():
        val       = d.get("readiness_breakdown", {}).get(key, 70)
        bar_color = "#1a7a5e" if val >= 75 else "#c17f24" if val >= 50 else "#c0392b"
        st.markdown(f"""
        <div class="skill-row">
            <span style="font-size:13px;color:#444;width:180px;flex-shrink:0">{label}</span>
            <div class="skill-bar-wrap">
                <div class="skill-bar-fill" style="width:{val}%;background:{bar_color}"></div>
            </div>
            <span class="skill-pct">{val}/100</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Immediate actions ─────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ Do These This Week</div>', unsafe_allow_html=True)
    for i, action in enumerate(d.get("immediate_actions", []), 1):
        st.markdown(f"""
        <div style="display:flex;gap:12px;padding:12px 14px;margin:6px 0;
                    background:#fafaf8;border-radius:10px;border:1px solid #e8e8e0">
            <span style="width:26px;height:26px;background:#e8f5ee;border-radius:50%;
                         display:flex;align-items:center;justify-content:center;
                         font-weight:700;color:#1a7a5e;font-size:12px;flex-shrink:0">{i}</span>
            <span style="font-size:14px;color:#222;align-self:center">{action}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # ── Job Recommendations ───────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💼 Job Recommendations</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:13px;color:#888;margin:-8px 0 14px">Best matches for your profile targeting <b>{role}</b></p>', unsafe_allow_html=True)

    jobs = d.get("job_recommendations", [
        {"title":"AI/ML Intern",       "meta":"TCS · Bengaluru",     "pct":92,"color":"green"},
        {"title":"ML Engineer Intern",  "meta":"Infosys · Remote",    "pct":87,"color":"green"},
        {"title":"Data Analyst",        "meta":"Wipro · Pune",        "pct":74,"color":"amber"},
        {"title":"Software Developer",  "meta":"Startup · Hyderabad", "pct":68,"color":"amber"},
    ])

    for j in jobs:
        pct   = j.get("pct", 0)
        color = "#1a7a5e" if pct >= 80 else "#c17f24" if pct >= 60 else "#c0392b"
        bg    = "#e8f5ee" if pct >= 80 else "#fffbe6" if pct >= 60 else "#fff0ee"
        st.markdown(f"""
        <div class="job-row">
            <div>
                <div class="job-title">{j.get('title','')}</div>
                <div class="job-meta">{j.get('meta','')}</div>
            </div>
            <div style="text-align:right">
                <div style="font-size:20px;font-weight:700;color:{color}">{pct}%</div>
                <div style="font-size:10px;color:#aaa">match</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Companies to target + salary ─────────────────────────────────────────
    col_comp, col_sal = st.columns(2)

    with col_comp:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🏢 Companies to Target</div>', unsafe_allow_html=True)
        for c in d.get("companies_to_target", ["TCS","Infosys","Wipro","Mu Sigma","Tiger Analytics","Fractal Analytics"]):
            st.markdown(f'<span style="background:#eff6ff;color:#2c5fa8;border-radius:6px;padding:4px 10px;font-size:12px;margin:3px;display:inline-block">🏢 {c}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_sal:
        sal = d.get("salary_range", {"min":400000,"max":900000,"note":"Bengaluru 2026 market"})
        st.markdown(f"""
        <div class="section-card" style="text-align:center">
            <div class="section-title" style="justify-content:center">💰 Expected Salary Range</div>
            <div style="font-size:28px;font-weight:700;color:#1a7a5e;margin:8px 0">
                ₹{sal.get('min',0):,} – ₹{sal.get('max',0):,}
            </div>
            <div style="font-size:13px;color:#888">per year &nbsp;·&nbsp; {sal.get('note','')}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── ATS quick summary ─────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📄 ATS Quick Summary</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**✅ Keywords Found**")
        for kw in d.get("present_keywords", []):
            st.markdown(f'<span style="background:#e8f5ee;color:#1a7a5e;border-radius:5px;padding:3px 9px;font-size:12px;margin:2px;display:inline-block">✓ {kw}</span>', unsafe_allow_html=True)
    with c2:
        st.markdown("**❌ Missing Keywords**")
        for kw in d.get("missing_keywords", []):
            st.markdown(f'<span style="background:#fff0ee;color:#c0392b;border-radius:5px;padding:3px 9px;font-size:12px;margin:2px;display:inline-block">✕ {kw}</span>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top:16px;display:flex;gap:10px;align-items:center">
        <div style="font-size:32px;font-weight:700;color:#1a7a5e">{d.get('ats_score',78)}</div>
        <div>
            <div style="font-size:14px;font-weight:600;color:#1a1a1a">ATS Score / 100</div>
            <div style="font-size:13px;color:#888">{d.get('ats_gaps',3)} keywords to add</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

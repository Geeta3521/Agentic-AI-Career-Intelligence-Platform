"""pages/skill_gap.py"""
import streamlit as st
from utils.session import get_dashboard, has_dashboard, get_role


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
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-title">Skill Gap</div>
            <div class="page-subtitle">See exactly what skills you need to land your target role</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not has_dashboard():
        st.markdown('<div class="warn-pill">⚠️ Please upload your resume first on the <b>Resume</b> page.</div>', unsafe_allow_html=True)
        return

    d = get_dashboard()
    role = get_role()
    match = d.get("skill_match", 72)

    # ── Match score banner ────────────────────────────────────────────────────
    match_color = "#1a7a5e" if match >= 75 else "#c17f24" if match >= 50 else "#c0392b"
    st.markdown(f"""
    <div class="section-card" style="text-align:center;padding:28px">
        <div style="font-size:64px;font-weight:700;color:{match_color};line-height:1">{match}%</div>
        <div style="font-size:16px;color:#444;margin-top:6px">Current Match for <b>{role}</b></div>
        <div style="font-size:13px;color:#888;margin-top:4px">
            {'Strong — apply now!' if match >= 75 else 'Almost there — close a few gaps!' if match >= 55 else 'Add missing skills to boost your match'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # ── Two columns: have vs need ─────────────────────────────────────────────
    col_have, col_need = st.columns(2)

    with col_have:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">✅ Skills You Have</div>', unsafe_allow_html=True)
        for s in d.get("skills_you_have", []):
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:8px 0;border-bottom:1px solid #f2f2ec">
                <span style="color:#1a7a5e;font-weight:600">✓</span>
                <span style="font-size:14px;color:#222">{s}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_need:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">🎯 Skill Gap — {role}</div>', unsafe_allow_html=True)
        for g in d.get("skill_gaps", []):
            _gap_row(g["skill"], g["status"])
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Skills to learn — prioritized ────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📚 Skills to Learn — Prioritized Action Plan</div>', unsafe_allow_html=True)

    priority_colors = {
        "High":   ("badge-missing", "#fff0ee", "#c0392b"),
        "Medium": ("badge-partial", "#fffbe6", "#c17f24"),
        "Low":    ("badge-strong",  "#e8f5ee", "#1a7a5e"),
    }

    for skill_data in d.get("skills_to_learn", []):
        skill    = skill_data.get("skill", "")
        priority = skill_data.get("priority", "Medium")
        time_est = skill_data.get("time", "")
        why      = skill_data.get("why", "")
        badge_cls, bg, fc = priority_colors.get(priority, priority_colors["Medium"])

        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:space-between;
                    padding:14px 16px;border-radius:10px;border:1px solid #e8e8e0;
                    margin-bottom:8px;background:#fafaf8">
            <div>
                <span style="font-size:15px;font-weight:600;color:#1a1a1a">{skill}</span>
                <span style="font-size:12px;color:#888;margin-left:10px">⏱ {time_est}</span>
                <div style="font-size:13px;color:#666;margin-top:3px">{why}</div>
            </div>
            <span class="badge {badge_cls}">{priority} Priority</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Skill proficiency bars ────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Skill Proficiency Overview</div>', unsafe_allow_html=True)

    for s in d.get("skill_proficiency", []):
        bar_color = {"green": "#1a7a5e", "amber": "#c17f24", "red": "#c0392b"}.get(s.get("color", "green"), "#1a7a5e")
        st.markdown(f"""
        <div class="skill-row">
            <span class="skill-name">{s['name']}</span>
            <div class="skill-bar-wrap">
                <div class="skill-bar-fill" style="width:{s['pct']}%;background:{bar_color}"></div>
            </div>
            <span class="skill-pct">{s['pct']}%</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Jobs reachable ────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💼 Jobs You Can Apply For Right Now</div>', unsafe_allow_html=True)

    jobs = d.get("job_recommendations", [])
    cols = st.columns(len(jobs)) if jobs else []
    for col, j in zip(cols, jobs):
        pct = j.get("pct", 0)
        color = "#1a7a5e" if pct >= 80 else "#c17f24" if pct >= 60 else "#c0392b"
        col.markdown(f"""
        <div style="background:#fafaf8;border-radius:12px;padding:16px;text-align:center;
                    border:1px solid #e8e8e0">
            <div style="font-size:28px;font-weight:700;color:{color}">{pct}%</div>
            <div style="font-size:13px;font-weight:600;color:#1a1a1a;margin-top:4px">{j.get('title','')}</div>
            <div style="font-size:11px;color:#888;margin-top:2px">{j.get('meta','')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

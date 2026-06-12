"""pages/roadmap.py"""
import streamlit as st
from utils.session import get_dashboard, has_dashboard, get_role


def show():
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-title">Roadmap</div>
            <div class="page-subtitle">Your week-by-week personalized learning plan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not has_dashboard():
        st.markdown('<div class="warn-pill">⚠️ Please upload your resume first on the <b>Resume</b> page.</div>', unsafe_allow_html=True)
        return

    d = get_dashboard()
    role = get_role()

    # ── Goal banner ───────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#e8f5ee,#d1ead8);border-radius:14px;
                padding:20px 24px;margin-bottom:20px;border:1px solid #b8dfc4">
        <div style="font-size:15px;font-weight:600;color:#1a5e3a;margin-bottom:4px">🎯 Your Goal</div>
        <div style="font-size:14px;color:#2a6e44;line-height:1.6">
            Land a <b>{role}</b> role by mastering the missing skills from your gap analysis — 
            one focused week at a time.
        </div>
        <div style="font-size:13px;color:#3a8a5a;margin-top:8px">⏱ Daily commitment: <b>2–3 hours/day</b></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick 4-week overview (matching screenshot style) ─────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🗺️ 4-Week Overview</div>', unsafe_allow_html=True)

    weeks_4 = d.get("roadmap", [])
    w_cols = st.columns(len(weeks_4)) if weeks_4 else st.columns(4)
    for col, w in zip(w_cols, weeks_4):
        with col:
            st.markdown(f"""
            <div class="week-card">
                <div class="week-label">{w.get('week','')}</div>
                <div class="week-title">{w.get('title','')}</div>
                <div class="week-desc">{w.get('desc','')}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Detailed 8-week plan ──────────────────────────────────────────────────
    st.markdown('<div class="section-title" style="font-size:16px;font-weight:700;color:#1a1a1a;margin-bottom:12px">📅 Detailed 8-Week Plan</div>', unsafe_allow_html=True)

    week_border_colors = ["#1a7a5e","#2c5fa8","#c17f24","#c0392b","#7c3aed","#1a7a5e","#2c5fa8","#c17f24"]

    for w in d.get("roadmap_8week", []):
        wnum  = w.get("week", 1)
        color = week_border_colors[(wnum - 1) % len(week_border_colors)]

        with st.expander(f"Week {wnum} — {w.get('theme','')}", expanded=(wnum <= 2)):
            st.markdown(f"""
            <div style="background:#fafaf8;border-radius:10px;padding:14px 18px;
                        border-left:4px solid {color};margin-bottom:12px">
                <b style="color:{color};font-size:15px">{w.get('theme','')}</b>
                <p style="color:#444;font-size:14px;margin:5px 0 0">Focus: {w.get('focus','')}</p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**📚 Topics**")
                for t in w.get("topics", []):
                    st.markdown(f"- {t}")

                st.markdown("**🎯 Milestone**")
                st.markdown(f"""
                <div style="background:#e8f5ee;border-radius:8px;padding:10px 14px;
                            border:1px solid #b8dfc4;font-size:13px;color:#1a5e3a">
                    ✅ {w.get('milestone','')}
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown("**🔗 Resources**")
                for res in w.get("resources", []):
                    icon = {"YouTube":"▶️","Course":"📖","Book":"📚","Website":"🌐","Tool":"🛠","Article":"📄","GitHub":"🐙"}.get(res.get("type",""), "🔗")
                    url  = res.get("url","#")
                    st.markdown(f"""
                    <div style="padding:6px 0;border-bottom:1px solid #f2f2ec;font-size:13px">
                        {icon} <a href="{url}" target="_blank"
                           style="color:#2c5fa8;text-decoration:none">{res.get('name','')}</a>
                        <span style="color:#aaa;font-size:11px;margin-left:4px">[{res.get('type','')}]</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("**🔨 Build This**")
                st.markdown(f"""
                <div style="background:#fffbe6;border-radius:8px;padding:10px 14px;
                            border:1px solid #fde68a;font-size:13px;color:#92400e">
                    {w.get('project','')}
                </div>
                """, unsafe_allow_html=True)

    # ── Tools + GitHub projects ───────────────────────────────────────────────
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    col_tools, col_projs = st.columns(2)

    with col_tools:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚙️ Tools to Install First</div>', unsafe_allow_html=True)
        tools = ["Python 3.10+", "VS Code", "Docker Desktop", "Git", "Postman", "AWS CLI"]
        for t in tools:
            st.markdown(f'<span style="background:#f1f5f9;color:#334155;border-radius:6px;padding:4px 10px;font-size:12px;margin:3px;display:inline-block">⚙️ {t}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_projs:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🐙 GitHub Projects to Build</div>', unsafe_allow_html=True)
        projs = [
            "Eye Disease API (FastAPI + EfficientNetB0)",
            "AI Career Copilot (this project!)",
            "DSA Solutions Repository",
            "Docker ML App",
            "AWS Deployed ML Service",
        ]
        for p in projs:
            st.markdown(f"""
            <div style="display:flex;gap:8px;padding:8px 0;border-bottom:1px solid #f2f2ec;font-size:13px;color:#222">
                🚀 {p}
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

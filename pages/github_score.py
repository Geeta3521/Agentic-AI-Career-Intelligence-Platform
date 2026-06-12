"""pages/github_score.py — Phase 4: GitHub Analyzer"""
import streamlit as st
import requests
from utils.ai_engine import ai_json
from utils.session import get_dashboard, has_dashboard


def _fetch(username: str) -> dict:
    headers = {"Accept": "application/vnd.github.v3+json"}
    base    = "https://api.github.com"
    user, repos = {}, []
    try:
        r = requests.get(f"{base}/users/{username}", headers=headers, timeout=10)
        if r.status_code == 200:
            user = r.json()
        r2 = requests.get(f"{base}/users/{username}/repos?sort=stars&per_page=30",
                          headers=headers, timeout=10)
        if r2.status_code == 200:
            repos = r2.json()
    except Exception:
        pass
    return {"user": user, "repos": repos}


def show():
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-title">GitHub Score</div>
            <div class="page-subtitle">AI analysis of your GitHub profile for placement readiness</div>
        </div>
        <div class="phase-badge">✦ Phase 4</div>
    </div>
    """, unsafe_allow_html=True)

    uname = st.text_input("GitHub Username", placeholder="e.g. Geeta3521",
                           label_visibility="collapsed")

    if st.button("🔍  Analyze GitHub Profile", use_container_width=True) and uname.strip():
        with st.spinner(f"Fetching {uname}'s GitHub data…"):
            gh_data = _fetch(uname.strip())

        user  = gh_data.get("user", {})
        repos = gh_data.get("repos", [])

        if not user:
            st.error(f"GitHub user '{uname}' not found.")
            return

        repo_summary = [
            {"name": r.get("name"), "desc": r.get("description",""),
             "lang": r.get("language",""), "stars": r.get("stargazers_count",0),
             "forks": r.get("forks_count",0), "topics": r.get("topics",[])}
            for r in repos[:15]
        ]
        langs = list(set(r.get("language","") for r in repos if r.get("language","")))

        with st.spinner("AI is scoring the profile…"):
            try:
                result = ai_json(f"""
You are a GitHub profile expert reviewing profiles for 2026 tech placements.
Analyze this profile for placement readiness.

Username: {uname}
Name: {user.get('name', uname)}
Bio: {user.get('bio','')}
Public Repos: {user.get('public_repos',0)}
Followers: {user.get('followers',0)}
Blog/Website: {user.get('blog','')}
Languages used: {langs}
Repositories: {repo_summary}

Return ONLY valid JSON (no markdown):
{{
  "overall_score": <0-100>,
  "breakdown": {{
    "profile_completeness": <0-100>,
    "code_quality": <0-100>,
    "project_variety": <0-100>,
    "documentation": <0-100>,
    "activity": <0-100>,
    "tech_range": <0-100>
  }},
  "strengths": ["s1","s2","s3"],
  "red_flags": ["f1","f2"],
  "top_repos": [
    {{"name":"repo","why":"why impressive","fix":"one improvement"}}
  ],
  "missing_elements": ["Missing 1","Missing 2","Missing 3"],
  "suggestions": [
    {{"priority":"High","action":"Do this","impact":"why it matters"}},
    {{"priority":"High","action":"Do this","impact":"why it matters"}},
    {{"priority":"Medium","action":"Do this","impact":"why it matters"}}
  ],
  "languages": ["Python","JavaScript"],
  "recruiter_view": "2 sentence recruiter impression",
  "verdict": "One sentence overall verdict"
}}
""")
                st.session_state["gh_result"] = result
                st.session_state["gh_user"]   = user
                st.session_state["gh_repos"]  = repos
                st.session_state["gh_uname"]  = uname
            except Exception as e:
                st.error(f"Analysis error: {e}")
                return

    if "gh_result" not in st.session_state:
        st.markdown("""
        <div style="background:#fafaf8;border-radius:14px;padding:40px;text-align:center;
                    border:1px dashed #d0d0c8;margin-top:16px">
            <div style="font-size:44px">🐙</div>
            <h3 style="color:#1a1a1a;margin:12px 0 6px">Analyze Any GitHub Profile</h3>
            <p style="color:#888;font-size:14px;max-width:380px;margin:0 auto">
                Enter a GitHub username above. AI fetches real repo data and gives you
                a placement-readiness score with specific improvement actions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    r     = st.session_state["gh_result"]
    user  = st.session_state["gh_user"]
    repos = st.session_state["gh_repos"]
    uname = st.session_state["gh_uname"]
    score = r.get("overall_score", 0)

    st.markdown("---")

    # ── Profile header card ───────────────────────────────────────────────────
    sc_color = "#1a7a5e" if score >= 75 else "#c17f24" if score >= 50 else "#c0392b"
    avatar   = user.get("avatar_url","")

    st.markdown(f"""
    <div class="section-card" style="display:flex;gap:20px;align-items:center">
        {'<img src="'+avatar+'" style="width:68px;height:68px;border-radius:50%;border:2px solid #e8e8e0">' if avatar else '<div style="width:68px;height:68px;border-radius:50%;background:#e8f5ee;display:flex;align-items:center;justify-content:center;font-size:28px">🐙</div>'}
        <div style="flex:1">
            <div style="font-size:20px;font-weight:700;color:#1a1a1a">{user.get('name', uname)}</div>
            <a href="https://github.com/{uname}" target="_blank"
               style="font-size:13px;color:#2c5fa8;text-decoration:none">github.com/{uname}</a>
            <span style="color:#aaa;font-size:13px"> &nbsp;·&nbsp; 📍 {user.get('location','Unknown')}</span>
            <div style="font-size:13px;color:#444;margin-top:4px">{user.get('bio','No bio set')}</div>
            <div style="margin-top:8px">
                <span style="background:#e8f5ee;color:#1a7a5e;border-radius:6px;padding:3px 10px;font-size:12px;margin-right:6px">📦 {user.get('public_repos',0)} repos</span>
                <span style="background:#eff6ff;color:#2c5fa8;border-radius:6px;padding:3px 10px;font-size:12px;margin-right:6px">👥 {user.get('followers',0)} followers</span>
                <span style="background:#f1f5f9;color:#334155;border-radius:6px;padding:3px 10px;font-size:12px">{user.get('blog','No website') or 'No website'}</span>
            </div>
        </div>
        <div style="text-align:center;min-width:80px">
            <div style="font-size:48px;font-weight:700;color:{sc_color};line-height:1">{score}</div>
            <div style="font-size:12px;color:#888">/100</div>
            <div style="font-size:12px;color:{sc_color};font-weight:600">{'Strong' if score>=75 else 'Average' if score>=50 else 'Needs Work'}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # recruiter view
    st.markdown(f'<div class="info-pill">🤖 Recruiter view: {r.get("recruiter_view","")}</div>', unsafe_allow_html=True)

    # ── Score breakdown bars ──────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Score Breakdown</div>', unsafe_allow_html=True)
    labels = {
        "profile_completeness": "Profile Completeness",
        "code_quality":         "Code Quality",
        "project_variety":      "Project Variety",
        "documentation":        "Documentation",
        "activity":             "Activity & Consistency",
        "tech_range":           "Technology Range",
    }
    for key, label in labels.items():
        val = r.get("breakdown", {}).get(key, 0)
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

    # ── Strengths + Red flags ─────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">✅ Strengths</div>', unsafe_allow_html=True)
        for s in r.get("strengths", []):
            st.markdown(f"""
            <div style="display:flex;gap:8px;padding:8px 0;border-bottom:1px solid #f2f2ec">
                <span style="color:#1a7a5e">✓</span>
                <span style="font-size:14px;color:#222">{s}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🚨 Issues Found</div>', unsafe_allow_html=True)
        for f in r.get("red_flags", []):
            st.markdown(f"""
            <div style="display:flex;gap:8px;padding:8px;margin:4px 0;
                        background:#fff0ee;border-radius:8px">
                <span style="color:#c0392b">⚠️</span>
                <span style="font-size:13px;color:#8a1a1a">{f}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div style="margin-top:12px"><div class="section-title" style="font-size:13px">❌ Missing Elements</div>', unsafe_allow_html=True)
        for m in r.get("missing_elements", []):
            st.markdown(f'<span style="background:#fff0ee;color:#c0392b;border-radius:6px;padding:3px 10px;font-size:12px;margin:2px;display:inline-block">✕ {m}</span>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Top repos ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌟 Top Repository Analysis</div>', unsafe_allow_html=True)
    for repo in r.get("top_repos", []):
        st.markdown(f"""
        <div style="background:#fafaf8;border-radius:10px;padding:14px 16px;
                    margin-bottom:10px;border:1px solid #e8e8e0">
            <b style="font-size:15px;color:#1a1a1a">📁 {repo.get('name','')}</b>
            <p style="color:#1a7a5e;font-size:13px;margin:6px 0">✅ {repo.get('why','')}</p>
            <p style="color:#c17f24;font-size:13px;margin:0">💡 Fix: {repo.get('fix','')}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Action plan ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Action Plan — Improve Your GitHub Score</div>', unsafe_allow_html=True)
    priority_colors = {"High":"badge-missing","Medium":"badge-partial","Low":"badge-strong"}
    for sug in r.get("suggestions", []):
        badge_cls = priority_colors.get(sug.get("priority","Medium"),"badge-partial")
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;justify-content:space-between;
                    padding:14px 16px;border-radius:10px;border:1px solid #e8e8e0;
                    margin-bottom:8px;background:#fafaf8">
            <div>
                <div style="font-size:14px;font-weight:600;color:#1a1a1a">🔧 {sug.get('action','')}</div>
                <div style="font-size:13px;color:#888;margin-top:3px">📈 {sug.get('impact','')}</div>
            </div>
            <span class="badge {badge_cls}">{sug.get('priority','')} Priority</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Languages detected ────────────────────────────────────────────────────
    st.markdown("**🔤 Languages Detected**")
    for lang in r.get("languages", []):
        st.markdown(f'<span style="background:#ede9fe;color:#5b21b6;border-radius:6px;padding:4px 10px;font-size:12px;margin:3px;display:inline-block">{lang}</span>', unsafe_allow_html=True)

    # ── Real repos list ───────────────────────────────────────────────────────
    if repos:
        st.markdown("---")
        st.markdown("**📦 All Repositories**")
        for repo in repos[:12]:
            stars = repo.get("stargazers_count", 0)
            lang  = repo.get("language","")
            desc  = repo.get("description","") or "No description"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:10px 0;
                        border-bottom:1px solid #f2f2ec;align-items:center">
                <div>
                    <a href="https://github.com/{uname}/{repo.get('name','')}" target="_blank"
                       style="font-weight:600;color:#2c5fa8;font-size:14px;text-decoration:none">
                        {repo.get('name','')}
                    </a>
                    <div style="font-size:12px;color:#888;margin-top:2px">{desc[:80]}{'…' if len(desc)>80 else ''}</div>
                </div>
                <div style="text-align:right;min-width:110px">
                    {f'<span style="background:#ede9fe;color:#5b21b6;border-radius:4px;padding:2px 7px;font-size:11px">{lang}</span>' if lang else ''}
                    <span style="background:#fffbe6;color:#92400e;border-radius:4px;padding:2px 7px;font-size:11px;margin-left:4px">⭐ {stars}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

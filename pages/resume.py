"""pages/resume.py — Upload PDF or paste, AI parses everything, builds dashboard data"""
import streamlit as st
from utils.session import save_resume, save_role, save_user, save_dashboard, get_resume, get_role
from utils.ai_engine import ai_json
from utils.pdf_parser import extract_pdf

ROLES = [
    "AI Engineer", "ML Engineer", "Data Scientist", "Data Analyst",
    "NLP Engineer", "MLOps Engineer", "Computer Vision Engineer",
    "Software Developer", "Backend Developer", "Full Stack Developer",
    "DevOps Engineer", "Cloud Engineer", "GenAI Engineer",
]


def _build_dashboard_data(resume: str, role: str) -> dict:
    """Single AI call that produces ALL dashboard + page data."""
    return ai_json(f"""
You are an expert career coach and ATS specialist for 2026 tech placements.
Analyze this resume for the role "{role}" and return a COMPLETE analysis.

Resume:
{resume}

Return ONLY valid JSON (no markdown, no backticks):
{{
  "candidate_name": "Full Name",
  "email": "email",
  "phone": "phone",
  "location": "city",
  "github": "github.com/username or empty",
  "linkedin": "linkedin.com/in/x or empty",
  "summary": "2-sentence professional summary",
  "education": [{{"degree":"B.Tech CSE","institution":"Univ","year":"2025","cgpa":"8.5"}}],
  "skills_all": ["Python","TensorFlow","OpenCV"],
  "programming_languages": ["Python","C++"],
  "frameworks": ["TensorFlow","FastAPI"],
  "tools": ["Git","Docker"],
  "projects": [
    {{"name":"Project","tech":["Python"],"description":"what it does","highlights":["X","Y"]}}
  ],
  "certifications": ["Cert 1"],
  "achievements": ["Achievement 1"],
  "experience": [
    {{"title":"Role","company":"Co","duration":"Jun–Aug 2024","points":["Did X"]}}
  ],

  "ats_score": <0-100>,
  "ats_gaps": <integer count of missing keywords>,
  "ats_breakdown": {{
    "keyword_match": <0-100>,
    "formatting": <0-100>,
    "experience_relevance": <0-100>,
    "education": <0-100>,
    "skills_depth": <0-100>
  }},
  "missing_keywords": ["FastAPI","Docker","AWS","MLOps","Kubernetes"],
  "present_keywords": ["Python","TensorFlow","OpenCV","SQL"],
  "ats_strengths": ["Strong ML projects","Good education"],
  "ats_fixes": ["Add FastAPI experience","Quantify project results"],
  "ats_tips": ["Use keywords from JD","Add GitHub link"],

  "skill_match": <0-100>,
  "skill_proficiency": [
    {{"name":"Python","pct":90,"color":"green"}},
    {{"name":"ML / DL","pct":80,"color":"green"}},
    {{"name":"NLP","pct":65,"color":"amber"}},
    {{"name":"FastAPI","pct":30,"color":"red"}},
    {{"name":"Docker","pct":20,"color":"red"}},
    {{"name":"AWS","pct":15,"color":"red"}},
    {{"name":"MLOps","pct":25,"color":"red"}}
  ],
  "skill_gaps": [
    {{"skill":"FastAPI","status":"Missing"}},
    {{"skill":"Docker","status":"Missing"}},
    {{"skill":"NLP","status":"Partial"}},
    {{"skill":"MLOps","status":"Missing"}},
    {{"skill":"Python","status":"Strong"}}
  ],
  "skills_you_have": ["Python","TensorFlow","OpenCV","SQL","Git"],
  "skills_to_learn": [
    {{"skill":"FastAPI","priority":"High","time":"1 week","why":"Core for ML APIs"}},
    {{"skill":"Docker","priority":"High","time":"1 week","why":"Industry standard"}},
    {{"skill":"MLOps","priority":"Medium","time":"2 weeks","why":"Deployment skills"}},
    {{"skill":"AWS","priority":"Medium","time":"2 weeks","why":"Cloud ML"}},
    {{"skill":"Kubernetes","priority":"Low","time":"3 weeks","why":"Advanced deployment"}}
  ],

  "readiness_score": <0-100>,
  "github_score": <0-100>,
  "github_suggestions": <integer count>,
  "readiness_breakdown": {{
    "resume_quality": <0-100>,
    "technical_skills": <0-100>,
    "project_portfolio": <0-100>,
    "dsa_problem_solving": <0-100>,
    "communication": <0-100>,
    "online_presence": <0-100>
  }},
  "readiness_level": "Almost Ready",
  "immediate_actions": ["Action 1","Action 2","Action 3"],

  "roadmap": [
    {{"week":"Week 1","title":"FastAPI Basics","desc":"Build REST APIs, request handling, deploy simple ML endpoint"}},
    {{"week":"Week 2","title":"Deploy ML Project","desc":"Package your ML model into an API with Streamlit frontend"}},
    {{"week":"Week 3","title":"Docker + MLOps","desc":"Dockerize your app, add CI/CD pipeline on GitHub Actions"}},
    {{"week":"Week 4","title":"Mock Interviews","desc":"Use AI Interview Simulator daily — projects, NLP, system design"}}
  ],
  "roadmap_8week": [
    {{"week":1,"theme":"FastAPI Basics","focus":"REST APIs for ML","topics":["Path params","Pydantic","Deploy model"],"project":"Serve your ML model as API","milestone":"Working ML API endpoint","resources":[{{"type":"YouTube","name":"FastAPI Crash Course","url":"https://youtube.com"}}]}},
    {{"week":2,"theme":"Deploy ML Project","focus":"Productionize","topics":["Streamlit","HuggingFace Spaces","Render"],"project":"Deploy Eye Disease app online","milestone":"Live app with public URL","resources":[{{"type":"Course","name":"Streamlit Docs","url":"https://docs.streamlit.io"}}]}},
    {{"week":3,"theme":"Docker Basics","focus":"Containerization","topics":["Dockerfile","docker-compose","volumes"],"project":"Dockerize your ML app","milestone":"Running app in Docker container","resources":[{{"type":"YouTube","name":"Docker for Beginners","url":"https://youtube.com"}}]}},
    {{"week":4,"theme":"MLOps Intro","focus":"CI/CD pipelines","topics":["GitHub Actions","DVC","experiment tracking"],"project":"Add CI pipeline to your project","milestone":"Automated tests + deployment","resources":[{{"type":"Course","name":"MLOps Zoomcamp","url":"https://github.com/DataTalksClub/mlops-zoomcamp"}}]}},
    {{"week":5,"theme":"AWS Cloud","focus":"Cloud deployment","topics":["EC2","S3","SageMaker basics"],"project":"Deploy model on AWS","milestone":"Cloud-hosted ML service","resources":[{{"type":"Course","name":"AWS Free Tier","url":"https://aws.amazon.com/free"}}]}},
    {{"week":6,"theme":"DSA Practice","focus":"Interview prep","topics":["Arrays","Trees","DP patterns"],"project":"Solve 30 LeetCode problems","milestone":"50+ LeetCode problems solved","resources":[{{"type":"Website","name":"LeetCode","url":"https://leetcode.com"}}]}},
    {{"week":7,"theme":"System Design","focus":"Architecture","topics":["ML system design","Scalability","Caching"],"project":"Design an ML recommendation system","milestone":"Can explain system design clearly","resources":[{{"type":"Book","name":"Designing ML Systems","url":"https://oreilly.com"}}]}},
    {{"week":8,"theme":"Mock Interviews","focus":"Final prep","topics":["Behavioral","Technical","Project walk-through"],"project":"10 mock interviews with AI Simulator","milestone":"Confident in all interview types","resources":[{{"type":"Tool","name":"AI Interview Simulator","url":"#"}}]}}
  ],

  "top_project": "Eye Disease Detection",
  "preview_questions": [
    {{"cat":"Technical",      "q":"Why did you choose EfficientNetB0 over ResNet or VGG for your eye disease classifier?"}},
    {{"cat":"Explainability", "q":"Walk me through how Grad-CAM works and what it showed in your model's predictions."}},
    {{"cat":"Challenges",     "q":"What data imbalance issues did you face and how did you address them?"}}
  ],
  "interview_questions": [
    {{"id":1,"question":"Why did you choose EfficientNetB0 for your Eye Disease project?","category":"Technical","difficulty":"Medium","hint":"Compare architectures — accuracy, params, speed"}},
    {{"id":2,"question":"Explain how Grad-CAM visualization works in your model.","category":"Explainability","difficulty":"Medium","hint":"Cover gradients, feature maps, heatmap generation"}},
    {{"id":3,"question":"How did you handle class imbalance in your dataset?","category":"Challenges","difficulty":"Medium","hint":"Oversampling, augmentation, class weights"}},
    {{"id":4,"question":"What is the difference between precision and recall? When would you prioritize each?","category":"Conceptual","difficulty":"Easy","hint":"Medical diagnosis context — false negatives are costly"}},
    {{"id":5,"question":"How would you deploy your Eye Disease model as a production API?","category":"System Design","difficulty":"Hard","hint":"FastAPI + Docker + cloud + monitoring"}}
  ],

  "job_recommendations": [
    {{"title":"AI/ML Intern",      "meta":"TCS · Bengaluru",     "pct":92,"color":"green"}},
    {{"title":"ML Engineer Intern","meta":"Infosys · Remote",    "pct":87,"color":"green"}},
    {{"title":"Data Analyst",      "meta":"Wipro · Pune",        "pct":74,"color":"amber"}},
    {{"title":"Software Developer","meta":"Startup · Hyderabad", "pct":68,"color":"amber"}}
  ],
  "companies_to_target": ["TCS","Infosys","Wipro","Mu Sigma","Tiger Analytics","Fractal Analytics"],
  "salary_range": {{"min":400000,"max":900000,"note":"Based on Bengaluru 2026 market"}},

  "github_breakdown": {{
    "profile_completeness": <0-100>,
    "code_quality": <0-100>,
    "project_variety": <0-100>,
    "documentation": <0-100>,
    "activity": <0-100>,
    "tech_range": <0-100>
  }},
  "github_strengths": ["Good projects","Active commits"],
  "github_fixes": ["Add deployment links","Improve README","Add screenshots"]
}}
""")


def show():
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-title">Resume</div>
            <div class="page-subtitle">Upload your resume — AI extracts everything & builds your dashboard</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_pdf, tab_text = st.tabs(["📁  Upload PDF", "✏️  Paste Text"])

    resume_text = ""
    with tab_pdf:
        uploaded = st.file_uploader("Upload your resume PDF", type=["pdf"], label_visibility="collapsed")
        if uploaded:
            with st.spinner("Extracting text from PDF..."):
                resume_text = extract_pdf(uploaded)
            if resume_text and resume_text != "Could not extract text from PDF.":
                st.markdown(f'<div class="info-pill">✅ PDF extracted — {len(resume_text):,} characters</div>', unsafe_allow_html=True)
                with st.expander("Preview extracted text"):
                    st.text(resume_text[:1800] + ("…" if len(resume_text) > 1800 else ""))
            else:
                st.markdown('<div class="warn-pill">⚠️ Could not extract text. Try pasting manually in the other tab.</div>', unsafe_allow_html=True)

    with tab_text:
        resume_text = st.text_area(
            "Paste resume",
            height=320,
            placeholder="""Name: Geeta Sharma
Email: geeta@email.com | Phone: +91 9876543210 | Location: Bengaluru
GitHub: github.com/Geeta3521

SKILLS
Python, TensorFlow, OpenCV, PyTorch, scikit-learn, SQL, Git, Streamlit

PROJECTS
Eye Disease Detection — EfficientNetB0, Grad-CAM visualization, 96% accuracy
AI Chatbot — LangChain, OpenAI API, Streamlit frontend

EDUCATION
B.Tech CSE (AI/ML) — XYZ University — 2025 — CGPA: 8.7

CERTIFICATIONS
Google ML Crash Course | TensorFlow Developer Certificate""",
            label_visibility="collapsed",
        )

    st.markdown("### 🎯 Target Role")
    col1, col2 = st.columns([2, 1])
    with col1:
        existing = get_role()
        idx = ROLES.index(existing) if existing in ROLES else 0
        role = st.selectbox("Role", ROLES, index=idx, label_visibility="collapsed")
    with col2:
        custom = st.text_input("Custom role", placeholder="e.g. GenAI Engineer", label_visibility="collapsed")
    final_role = custom.strip() if custom.strip() else role

    st.markdown("---")
    if st.button("🤖  Analyze Resume with AI", use_container_width=True):
        text = resume_text.strip()
        if not text:
            st.markdown('<div class="warn-pill">⚠️ Please upload a PDF or paste your resume text.</div>', unsafe_allow_html=True)
            return

        save_resume(text)
        save_role(final_role)

        with st.spinner("AI is analyzing your resume — building full dashboard… (20-30 sec)"):
            try:
                data = _build_dashboard_data(text, final_role)
                save_user(data.get("candidate_name", "Student"))
                save_dashboard(data)
                st.success("✅ Analysis complete! Go to Dashboard to see your results.")
                st.balloons()
            except Exception as e:
                st.error(f"Analysis error: {e}")
                return

    # ── Show parsed profile if already done ─────────────────────────────────
    from utils.session import get_dashboard, has_dashboard
    if not has_dashboard():
        return

    d = get_dashboard()
    st.markdown("---")
    st.markdown("### 👤 Parsed Profile")

    name = d.get("candidate_name", "")
    st.markdown(f"""
    <div class="section-card">
        <div style="display:flex;align-items:center;gap:16px">
            <div style="width:52px;height:52px;border-radius:50%;background:#e8f5ee;
                        display:flex;align-items:center;justify-content:center;
                        font-size:22px;font-weight:700;color:#1a7a5e">{name[:1].upper() if name else "?"}</div>
            <div>
                <div style="font-size:18px;font-weight:700;color:#1a1a1a">{name}</div>
                <div style="font-size:13px;color:#888;margin-top:2px">
                    {d.get("email","")} &nbsp;·&nbsp; {d.get("phone","")} &nbsp;·&nbsp; {d.get("location","")}
                </div>
                <div style="font-size:13px;color:#1a7a5e;margin-top:2px">
                    {d.get("github","")} &nbsp;|&nbsp; {d.get("linkedin","")}
                </div>
            </div>
        </div>
        <p style="margin-top:14px;font-size:14px;color:#444;line-height:1.6">{d.get("summary","")}</p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("**💻 Languages**")
        for s in d.get("programming_languages", []):
            st.markdown(f'<span style="background:#e8f5ee;color:#1a7a5e;border-radius:6px;padding:3px 10px;font-size:12px;margin:2px;display:inline-block">{s}</span>', unsafe_allow_html=True)
    with col_b:
        st.markdown("**🛠 Frameworks**")
        for s in d.get("frameworks", []):
            st.markdown(f'<span style="background:#ede9fe;color:#5b21b6;border-radius:6px;padding:3px 10px;font-size:12px;margin:2px;display:inline-block">{s}</span>', unsafe_allow_html=True)
    with col_c:
        st.markdown("**⚙️ Tools**")
        for s in d.get("tools", []):
            st.markdown(f'<span style="background:#f1f5f9;color:#334155;border-radius:6px;padding:3px 10px;font-size:12px;margin:2px;display:inline-block">{s}</span>', unsafe_allow_html=True)

    st.markdown("**🚀 Projects**")
    for p in d.get("projects", []):
        tech_html = "".join(f'<span style="background:#dbeafe;color:#1e40af;border-radius:4px;padding:2px 8px;font-size:11px;margin:2px;display:inline-block">{t}</span>' for t in p.get("tech", []))
        pts_html  = "".join(f'<li style="font-size:13px;color:#444">{h}</li>' for h in p.get("highlights", []))
        st.markdown(f"""
        <div class="section-card" style="margin-bottom:10px">
            <b style="font-size:15px">{p.get('name','')}</b>
            <p style="font-size:13px;color:#666;margin:5px 0">{p.get('description','')}</p>
            <div>{tech_html}</div>
            <ul style="margin:8px 0 0 16px">{pts_html}</ul>
        </div>
        """, unsafe_allow_html=True)

    col_edu, col_cert = st.columns(2)
    with col_edu:
        st.markdown("**🎓 Education**")
        for e in d.get("education", []):
            st.markdown(f"""
            <div class="section-card" style="margin-bottom:8px">
                <b>{e.get('degree','')}</b> — {e.get('institution','')} ({e.get('year','')})
                <div style="font-size:12px;color:#888">CGPA: {e.get('cgpa','N/A')}</div>
            </div>""", unsafe_allow_html=True)
    with col_cert:
        st.markdown("**🏆 Certifications**")
        for c in d.get("certifications", []):
            st.markdown(f'<span style="background:#fef3c7;color:#92400e;border-radius:6px;padding:4px 10px;font-size:12px;margin:2px;display:inline-block">🎖 {c}</span>', unsafe_allow_html=True)

    st.markdown('<div class="info-pill" style="margin-top:16px">✅ Resume parsed! Go to <b>Dashboard</b> to see your full placement intelligence report.</div>', unsafe_allow_html=True)

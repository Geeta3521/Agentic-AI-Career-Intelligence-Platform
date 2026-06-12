# 🚀 AI Career Copilot
### Personalized Placement & Career Intelligence Platform

---

## 🚀 Run in 3 Steps

### Step 1 — Get FREE Gemini API Key
👉 https://aistudio.google.com/app/apikey → Click "Create API Key" → Copy it

### Step 2 — Add your key
Open `.streamlit/secrets.toml` and replace the placeholder:
```
GEMINI_API_KEY = "paste-your-actual-key-here"
```

### Step 3 — Install & Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
Opens at **http://localhost:8501** ✅

---

## 📁 Project Structure

```
career_copilot/
├── app.py                     ← Run this
├── requirements.txt
├── README.md
├── .streamlit/
│   ├── secrets.toml           ← Add your API key here
│   └── config.toml
├── pages/
│   ├── dashboard.py           ← Home dashboard (matches screenshot)
│   ├── resume.py              ← Phase 1: PDF upload + AI parsing
│   ├── skill_gap.py           ← Phase 1: Skill gap analysis
│   ├── roadmap.py             ← Phase 1: 4/8-week roadmap
│   ├── interview_ai.py        ← Phase 3: AI Interview Simulator ⭐
│   ├── github_score.py        ← Phase 4: GitHub Analyzer
│   └── jobs.py                ← Phase 2: Placement score + jobs
└── utils/
    ├── ai_engine.py           ← Gemini API calls
    ├── pdf_parser.py          ← PDF text extraction
    ├── session.py             ← Session state helpers
    └── styles.py              ← Global CSS (matches screenshot UI)
```

---

## ✨ Features

| Page | Phase | Feature |
|------|-------|---------|
| Dashboard | All | ATS score, skill match, readiness, roadmap preview, interview questions, job recommendations |
| Resume | 1 | Upload PDF or paste text — AI parses everything |
| Skill Gap | 1 | Skill match %, proficiency bars, skills to learn |
| Roadmap | 1 | 4-week overview + detailed 8-week plan with resources |
| Interview AI | 3 ⭐ | Resume-based questions + AI scoring + feedback |
| GitHub Score | 4 | Real GitHub API + AI scoring + improvement plan |
| Jobs | 2 | Placement readiness score + job recommendations + salary |

---

## 🔑 Environment Variables

| Variable | Required | Where to get |
|----------|----------|--------------|
| `GEMINI_API_KEY` | ✅ Yes | https://aistudio.google.com/app/apikey (FREE) |

---

## 🌐 Deploy to Streamlit Cloud (Free)

1. Push to GitHub
2. Go to https://share.streamlit.io
3. Connect repo → set main file: `app.py`
4. Add `GEMINI_API_KEY` in Secrets
5. Deploy!

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `GEMINI_API_KEY not found` | Add key to `.streamlit/secrets.toml` |
| PDF not extracting | Paste text manually in the Resume page |
| JSON parse error | Retry — Gemini occasionally formats differently |
| Slow first load | Normal — first Gemini call takes ~20 seconds |

---

*Built for AIML students targeting 2026 placements 🚀*

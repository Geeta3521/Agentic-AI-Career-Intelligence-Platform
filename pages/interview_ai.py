"""pages/interview_ai.py — Phase 3: AI Interview Simulator"""
import streamlit as st
from utils.session import get_dashboard, has_dashboard, get_role, get_resume
from utils.ai_engine import ai_json


def _evaluate(question: str, answer: str, role: str) -> dict:
    return ai_json(f"""
You are a strict but fair senior interviewer at a top tech company evaluating a candidate for "{role}".

Question: {question}
Candidate's Answer: {answer}

Return ONLY valid JSON (no markdown):
{{
  "score": <integer 0-10>,
  "verdict": "Excellent / Good / Average / Below Average / Poor",
  "strengths": ["what was good"],
  "gaps": ["what was missing"],
  "ideal_points": ["key point 1","key point 2","key point 3"],
  "follow_up": "A natural follow-up question",
  "tip": "One specific improvement tip"
}}
""")


def show():
    st.markdown("""
    <div class="page-header">
        <div>
            <div class="page-title">Interview AI</div>
            <div class="page-subtitle">AI-generated questions from YOUR resume — get instant scored feedback</div>
        </div>
        <div class="phase-badge">✦ Phase 3</div>
    </div>
    """, unsafe_allow_html=True)

    if not has_dashboard():
        st.markdown('<div class="warn-pill">⚠️ Please upload your resume first on the <b>Resume</b> page.</div>', unsafe_allow_html=True)
        return

    d    = get_dashboard()
    role = get_role()
    project_name = d.get("top_project", "your project")

    # ── Preview questions from dashboard ─────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">🎤 AI Interview Simulator</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:13px;color:#888;margin:-8px 0 14px">Based on your {project_name} project</p>', unsafe_allow_html=True)

    for item in d.get("preview_questions", []):
        st.markdown(f"""
        <div class="iq-card">
            <div class="iq-label">{item.get('cat','')}</div>
            <div class="iq-text">{item.get('q','')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Settings ──────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### ⚙️ Interview Settings")
    c1, c2, c3 = st.columns(3)
    with c1:
        num_q = st.slider("Number of questions", 3, 10, 5)
    with c2:
        q_type = st.selectbox("Question type", [
            "Mixed (All Types)", "Technical Only",
            "Behavioral Only", "Project-Based Only", "Conceptual Only"
        ])
    with c3:
        difficulty = st.selectbox("Difficulty", ["Mixed", "Easy", "Medium", "Hard"])

    if st.button("🎙️  Start Mock Interview", use_container_width=True):
        resume = get_resume()
        with st.spinner("Generating personalized questions from your resume…"):
            try:
                result = ai_json(f"""
You are a senior technical interviewer. Generate {num_q} {q_type} interview questions
for this candidate applying for "{role}". Questions MUST reference their actual resume —
their real projects, skills, and experience.

Resume:
{resume}

Return ONLY valid JSON:
{{
  "questions": [
    {{
      "id": 1,
      "question": "Real question referencing their resume",
      "category": "Technical/Behavioral/Project/Conceptual",
      "difficulty": "Easy/Medium/Hard",
      "hint": "What a good answer should include"
    }}
  ],
  "focus": "One sentence about what this interview focuses on based on resume"
}}
""")
                st.session_state["ivq"]       = result.get("questions", [])
                st.session_state["iv_focus"]  = result.get("focus", "")
                st.session_state["iv_answers"] = {}
                st.session_state["iv_evals"]   = {}
                st.session_state["iv_active"]  = True
            except Exception as e:
                st.error(f"Error generating questions: {e}")
                return

    if not st.session_state.get("iv_active"):
        st.markdown("""
        <div style="background:#fafaf8;border-radius:14px;padding:36px;text-align:center;
                    border:1px dashed #d0d0c8;margin-top:8px">
            <div style="font-size:42px">🎤</div>
            <h3 style="color:#1a1a1a;margin:12px 0 6px">Ready to practice?</h3>
            <p style="color:#888;font-size:14px;max-width:400px;margin:0 auto">
                Questions are generated from YOUR actual resume and projects — not generic questions.
                Answer each one and get an AI score with detailed feedback.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    questions = st.session_state.get("ivq", [])
    answers   = st.session_state.get("iv_answers", {})
    evals     = st.session_state.get("iv_evals", {})
    focus     = st.session_state.get("iv_focus", "")

    if focus:
        st.markdown(f'<div class="info-pill">🎯 Interview focus: {focus}</div>', unsafe_allow_html=True)

    answered = len(evals)
    st.progress(answered / len(questions) if questions else 0,
                text=f"Progress: {answered}/{len(questions)} answered")

    # ── Each question ─────────────────────────────────────────────────────────
    diff_colors = {"Easy":"#1a7a5e","Medium":"#c17f24","Hard":"#c0392b"}
    diff_bgs    = {"Easy":"#e8f5ee","Medium":"#fffbe6","Hard":"#fff0ee"}

    for q in questions:
        qid  = str(q["id"])
        diff = q.get("difficulty","Medium")
        cat  = q.get("category","")
        dc   = diff_colors.get(diff,"#888")
        db   = diff_bgs.get(diff,"#f5f5f5")

        st.markdown(f"""
        <div style="background:#eff6ff;border-radius:12px 12px 0 0;padding:16px 20px;
                    border:1px solid #bfdbfe;margin-top:18px">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                <span style="font-size:12px;color:#888">Question {q['id']} of {len(questions)}</span>
                <div>
                    <span style="background:{db};color:{dc};border-radius:5px;
                                 padding:2px 9px;font-size:11px;font-weight:600">{diff}</span>
                    <span style="background:#f1f5f9;color:#334155;border-radius:5px;
                                 padding:2px 9px;font-size:11px;font-weight:600;margin-left:5px">{cat}</span>
                </div>
            </div>
            <div style="font-size:16px;font-weight:600;color:#1a1a1a">{q['question']}</div>
            <div style="font-size:12px;color:#888;margin-top:6px;font-style:italic">
                💡 Hint: {q.get('hint','')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if qid not in evals:
            ans = st.text_area(
                f"Answer {qid}",
                key=f"ans_{qid}",
                height=110,
                placeholder="Type your answer here… Be specific and include examples from your projects.",
                label_visibility="collapsed"
            )
            if st.button(f"✅  Submit Answer {q['id']}", key=f"sub_{qid}"):
                if not ans.strip():
                    st.warning("Please type your answer first.")
                else:
                    with st.spinner("AI is evaluating your answer…"):
                        try:
                            ev = _evaluate(q["question"], ans, role)
                            st.session_state["iv_answers"][qid] = ans
                            st.session_state["iv_evals"][qid]   = ev
                            st.rerun()
                        except Exception as e:
                            st.error(f"Evaluation error: {e}")
        else:
            ev    = evals[qid]
            score = ev.get("score", 0)
            sc    = "#1a7a5e" if score >= 8 else "#c17f24" if score >= 6 else "#c0392b"

            # submitted answer
            st.markdown(f"""
            <div style="background:#f8f8f4;padding:12px 16px;border:1px solid #e8e8e0;
                        border-top:none;font-size:13px;color:#444">
                <b>Your answer:</b> {answers.get(qid,'')}
            </div>
            """, unsafe_allow_html=True)

            # evaluation
            strengths_html = "".join(f'<p style="font-size:12px;color:#374151;margin:3px 0">• {s}</p>' for s in ev.get("strengths", []))
            gaps_html      = "".join(f'<p style="font-size:12px;color:#374151;margin:3px 0">• {g}</p>' for g in ev.get("gaps", []))
            ideal_html     = "".join(f'<p style="font-size:12px;color:#1a5e3a;margin:3px 0">✓ {p}</p>' for p in ev.get("ideal_points", []))

            st.markdown(f"""
            <div style="background:#fff;border-radius:0 0 12px 12px;padding:18px 20px;
                        border:1px solid #e8e8e0;border-top:none">
                <div style="display:flex;align-items:center;gap:16px;margin-bottom:14px">
                    <div style="width:56px;height:56px;border-radius:50%;
                                background:{sc}22;border:2.5px solid {sc};
                                display:flex;align-items:center;justify-content:center">
                        <span style="font-size:18px;font-weight:700;color:{sc}">{score}/10</span>
                    </div>
                    <div>
                        <div style="font-size:15px;font-weight:700;color:{sc}">{ev.get('verdict','')}</div>
                        <div style="font-size:12px;color:#888">AI Score</div>
                    </div>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
                    <div>
                        <div style="font-size:12px;font-weight:700;color:#1a7a5e;margin-bottom:5px">✅ Strengths</div>
                        {strengths_html}
                    </div>
                    <div>
                        <div style="font-size:12px;font-weight:700;color:#c0392b;margin-bottom:5px">❌ Gaps</div>
                        {gaps_html}
                    </div>
                </div>
                <div style="margin-top:12px;background:#e8f5ee;border-radius:8px;
                            padding:10px 14px;border:1px solid #b8dfc4">
                    <div style="font-size:12px;font-weight:700;color:#1a5e3a;margin-bottom:5px">📌 Ideal answer should include:</div>
                    {ideal_html}
                </div>
                <div style="margin-top:10px;background:#fffbe6;border-radius:8px;
                            padding:10px 14px;border:1px solid #fde68a">
                    <span style="font-size:12px;font-weight:700;color:#92400e">💡 Tip: </span>
                    <span style="font-size:12px;color:#92400e">{ev.get('tip','')}</span>
                </div>
                <div style="margin-top:10px;font-size:13px;color:#666;font-style:italic">
                    ❓ Follow-up: <b>{ev.get('follow_up','')}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Session summary ───────────────────────────────────────────────────────
    if len(evals) == len(questions) and questions:
        st.markdown("---")
        st.markdown("## 📊 Session Summary")

        scores  = [ev.get("score", 0) for ev in evals.values()]
        avg     = sum(scores) / len(scores)
        avg_pct = int(avg * 10)
        verdict = "🟢 Ready for interviews!" if avg >= 7.5 else "🟡 Keep practising" if avg >= 5 else "🔴 More preparation needed"

        c1, c2, c3 = st.columns(3)
        c1.metric("Average Score", f"{avg:.1f}/10")
        c2.metric("Questions Done", len(questions))
        c3.metric("Performance",    f"{avg_pct}%")

        st.markdown(f"""
        <div style="background:#e8f5ee;border-radius:12px;padding:20px;text-align:center;
                    border:1px solid #b8dfc4;margin-top:12px">
            <div style="font-size:18px;font-weight:700;color:#1a5e3a">{verdict}</div>
            <p style="color:#888;font-size:13px;margin-top:6px">
                Review your weak areas in the <b>Roadmap</b> and practice again tomorrow.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄  Start New Session", use_container_width=True):
            for k in ["ivq","iv_focus","iv_answers","iv_evals","iv_active"]:
                st.session_state.pop(k, None)
            st.rerun()

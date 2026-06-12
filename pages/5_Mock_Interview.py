"""
Page 5: AI Interview Agent
"""

import streamlit as st
from agents.interview_agent import generate_interview_questions, evaluate_answer

st.set_page_config(page_title="Mock Interview", page_icon="🎤", layout="wide")

st.title("🎤 AI Interview Agent")
st.markdown("Practice with AI-generated questions and get scored feedback on your answers.")

target_role = st.session_state.get("target_role", "AI/ML Engineer")
st.caption(f"Target role: **{target_role}** (change this in the sidebar on the Home page)")

extracted_skills = st.session_state.get("extracted_skills", [])
default_skills = ", ".join(extracted_skills) if extracted_skills else ""

skills_input = st.text_area(
    "Your skills (comma-separated)",
    value=default_skills,
    height=80,
    placeholder="e.g., Python, SQL, TensorFlow, Streamlit, Git",
)

num_questions = st.slider("Number of questions", min_value=3, max_value=8, value=5)

if st.button("Generate Mock Interview Questions", type="primary"):
    skills_list = [s.strip() for s in skills_input.split(",") if s.strip()]
    with st.spinner("Generating interview questions..."):
        try:
            result = generate_interview_questions(target_role, skills_list, num_questions)
            st.session_state.interview_questions = result.get("questions", [])
            st.session_state.interview_results = [None] * len(st.session_state.interview_questions)
        except Exception as e:
            st.error(f"Error: {e}")

questions = st.session_state.get("interview_questions")
if questions:
    st.markdown("---")
    st.subheader("Your Mock Interview")

    for i, q in enumerate(questions):
        with st.container(border=True):
            qtype = q.get("type", "")
            badge = {"Technical": "🔧", "Behavioral": "🧠", "HR": "🤝"}.get(qtype, "❓")
            st.markdown(f"**Q{i+1}. {badge} [{qtype}]** {q.get('question', '')}")

            answer = st.text_area("Your answer:", key=f"answer_{i}", height=100)

            if st.button(f"Evaluate Answer {i+1}", key=f"eval_btn_{i}"):
                if not answer.strip():
                    st.warning("Please type an answer first.")
                else:
                    with st.spinner("Evaluating..."):
                        try:
                            eval_result = evaluate_answer(q.get("question", ""), answer, target_role)
                            st.session_state.interview_results[i] = eval_result
                        except Exception as e:
                            st.error(f"Error: {e}")

            eval_result = st.session_state.interview_results[i] if i < len(st.session_state.interview_results) else None
            if eval_result and not eval_result.get("parse_error"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Technical", f"{eval_result.get('technical_score', 0)}/10")
                col2.metric("Communication", f"{eval_result.get('communication_score', 0)}/10")
                col3.metric("Confidence", f"{eval_result.get('confidence_score', 0)}/10")

                st.info(f"Feedback: {eval_result.get('feedback', '')}")

                ideal_points = eval_result.get("ideal_answer_points", [])
                if ideal_points:
                    st.markdown("**An ideal answer would cover:**")
                    for p in ideal_points:
                        st.markdown(f"- {p}")
            elif eval_result and eval_result.get("parse_error"):
                st.error("Could not parse evaluation. Raw response:")
                st.write(eval_result.get("raw_response"))

    # Overall summary
    completed = [r for r in st.session_state.interview_results if r and not r.get("parse_error")]
    if completed:
        st.markdown("---")
        st.subheader("Overall Performance")
        avg_tech = sum(r.get("technical_score", 0) for r in completed) / len(completed)
        avg_comm = sum(r.get("communication_score", 0) for r in completed) / len(completed)
        avg_conf = sum(r.get("confidence_score", 0) for r in completed) / len(completed)

        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Technical", f"{avg_tech:.1f}/10")
        col2.metric("Avg Communication", f"{avg_comm:.1f}/10")
        col3.metric("Avg Confidence", f"{avg_conf:.1f}/10")

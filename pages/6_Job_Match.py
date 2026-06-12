"""
Page 6: Job Matching Agent
"""

import streamlit as st
from agents.job_match_agent import match_job
from utils.pdf_utils import extract_text_from_pdf

st.set_page_config(page_title="Job Match", page_icon="💼", layout="wide")

st.title("💼 Job Matching Agent")
st.markdown("Paste a job description to see how well your resume matches it.")

resume_text = st.session_state.get("resume_text", "")

if resume_text:
    st.success("Using resume from your earlier analysis. You can also paste a different one below.")

resume_override = st.text_area(
    "Resume text (auto-filled if you analyzed your resume earlier)",
    value=resume_text,
    height=150,
)

uploaded_file = st.file_uploader("Or upload a different resume PDF", type=["pdf"])
if uploaded_file is not None:
    resume_override = extract_text_from_pdf(uploaded_file)
    st.info("Using uploaded PDF content.")

job_description = st.text_area("Paste the job description here", height=200)

if st.button("Check Match", type="primary"):
    if not resume_override.strip() or not job_description.strip():
        st.warning("Please provide both your resume and the job description.")
    else:
        with st.spinner("AI is comparing your resume to the job description..."):
            try:
                result = match_job(resume_override, job_description)
                st.session_state.job_match_result = result
            except Exception as e:
                st.error(f"Error: {e}")

result = st.session_state.get("job_match_result")
if result:
    if result.get("parse_error"):
        st.error("Could not parse AI response. Raw response below:")
        st.write(result.get("raw_response"))
    else:
        st.markdown("---")
        score = result.get("match_score", 0)
        st.metric("Job Match Score", f"{score}%")
        st.progress(min(max(score, 0), 100) / 100)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Matching Points")
            for m in result.get("matching_points", []):
                st.markdown(f"- {m}")

        with col2:
            st.subheader("Missing Requirements")
            for m in result.get("missing_requirements", []):
                st.markdown(f"- {m}")

        st.markdown("---")
        st.subheader("Recommendation")
        st.info(result.get("recommendation", ""))

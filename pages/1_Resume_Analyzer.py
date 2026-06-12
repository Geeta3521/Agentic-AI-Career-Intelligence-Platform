"""
Page 1: Resume Analyzer Agent
"""

import streamlit as st
from agents.resume_agent import analyze_resume
from utils.pdf_utils import extract_text_from_pdf

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 Resume Analyzer Agent")
st.markdown("Upload your resume to get an ATS score, identify weak areas, and find missing keywords.")

target_role = st.session_state.get("target_role", "AI/ML Engineer")
st.caption(f"Analyzing for target role: **{target_role}** (change this in the sidebar on the Home page)")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

col1, col2 = st.columns([1, 1])
with col1:
    analyze_btn = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)
with col2:
    paste_text = st.checkbox("Paste resume text instead of uploading PDF")

resume_text_input = ""
if paste_text:
    resume_text_input = st.text_area("Paste your resume text here", height=250)

if analyze_btn:
    resume_text = ""
    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF..."):
            resume_text = extract_text_from_pdf(uploaded_file)
    elif resume_text_input.strip():
        resume_text = resume_text_input.strip()

    if not resume_text:
        st.warning("Please upload a PDF or paste your resume text first.")
    else:
        st.session_state.resume_text = resume_text
        with st.spinner("AI is analyzing your resume... (this may take 10-20 seconds)"):
            try:
                result = analyze_resume(resume_text, target_role)
                st.session_state.resume_analysis = result
                if "extracted_skills" in result:
                    st.session_state.extracted_skills = result["extracted_skills"]
            except Exception as e:
                st.error(f"Error: {e}")

# Display results
result = st.session_state.get("resume_analysis")
if result:
    if result.get("parse_error"):
        st.error("Could not parse AI response. Raw response below:")
        st.write(result.get("raw_response"))
    else:
        st.markdown("---")
        score = result.get("ats_score", 0)

        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.metric("ATS Score", f"{score}/100")
            if score >= 80:
                st.success("Excellent!")
            elif score >= 60:
                st.warning("Good, can improve")
            else:
                st.error("Needs work")

        with col2:
            st.subheader("Strengths")
            for s in result.get("strengths", []):
                st.markdown(f"- {s}")

        with col3:
            st.subheader("Weak Areas")
            for w in result.get("weak_areas", []):
                st.markdown(f"- {w}")

        st.markdown("---")

        col4, col5 = st.columns(2)
        with col4:
            st.subheader("Missing Keywords")
            for k in result.get("missing_keywords", []):
                st.markdown(f"- `{k}`")

        with col5:
            st.subheader("Suggestions")
            for sug in result.get("suggestions", []):
                st.markdown(f"- {sug}")

        st.markdown("---")
        st.subheader("Extracted Skills")
        skills = result.get("extracted_skills", [])
        if skills:
            st.write(", ".join(f"`{s}`" for s in skills))
        else:
            st.write("No skills extracted.")

        st.success("These extracted skills will be used automatically by other agents (Skill Gap, Roadmap, Project Recommender, Interview).")

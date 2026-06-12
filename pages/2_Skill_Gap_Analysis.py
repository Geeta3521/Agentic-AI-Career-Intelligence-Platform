"""
Page 2: Skill Gap Agent
"""

import streamlit as st
from agents.skill_gap_agent import analyze_skill_gap

st.set_page_config(page_title="Skill Gap Analysis", page_icon="🧩", layout="wide")

st.title("🧩 Skill Gap Agent")
st.markdown("Compare your current skills against your target role and find what's missing.")

target_role = st.session_state.get("target_role", "AI/ML Engineer")
st.caption(f"Target role: **{target_role}** (change this in the sidebar on the Home page)")

extracted_skills = st.session_state.get("extracted_skills", [])

default_skills = ", ".join(extracted_skills) if extracted_skills else ""
if extracted_skills:
    st.success("Skills auto-loaded from your analyzed resume. You can edit them below.")

skills_input = st.text_area(
    "Your current skills (comma-separated)",
    value=default_skills,
    height=100,
    placeholder="e.g., Python, SQL, TensorFlow, Streamlit, Git",
)

if st.button("Analyze Skill Gap", type="primary"):
    skills_list = [s.strip() for s in skills_input.split(",") if s.strip()]
    if not skills_list:
        st.warning("Please enter at least one skill.")
    else:
        with st.spinner("AI is analyzing skill gaps..."):
            try:
                result = analyze_skill_gap(skills_list, target_role)
                st.session_state.skill_gap_result = result
            except Exception as e:
                st.error(f"Error: {e}")

result = st.session_state.get("skill_gap_result")
if result:
    if result.get("parse_error"):
        st.error("Could not parse AI response. Raw response below:")
        st.write(result.get("raw_response"))
    else:
        st.markdown("---")
        match_pct = result.get("match_percentage", 0)
        st.metric(f"Skill Match for {target_role}", f"{match_pct}%")
        st.progress(min(max(match_pct, 0), 100) / 100)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Matched Skills")
            for s in result.get("matched_skills", []):
                st.markdown(f"- {s}")

            st.subheader("All Required Skills")
            for s in result.get("required_skills", []):
                st.markdown(f"- {s}")

        with col2:
            st.subheader("Missing Skills")
            for s in result.get("missing_skills", []):
                st.markdown(f"- {s}")

            st.subheader("Priority: Learn These First")
            for i, s in enumerate(result.get("priority_skills", []), 1):
                st.markdown(f"{i}. **{s}**")

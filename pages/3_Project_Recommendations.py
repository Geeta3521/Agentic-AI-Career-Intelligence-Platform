"""
Page 3: Project Recommendation Agent
"""

import streamlit as st
from agents.project_agent import recommend_projects

st.set_page_config(page_title="Project Recommendations", page_icon="🚀", layout="wide")

st.title("🚀 Project Recommendation Agent")
st.markdown("Get personalized portfolio project ideas based on your skills and target role.")

target_role = st.session_state.get("target_role", "AI/ML Engineer")
st.caption(f"Target role: **{target_role}** (change this in the sidebar on the Home page)")

extracted_skills = st.session_state.get("extracted_skills", [])
default_skills = ", ".join(extracted_skills) if extracted_skills else ""

skills_input = st.text_area(
    "Your current skills (comma-separated)",
    value=default_skills,
    height=100,
    placeholder="e.g., Python, SQL, TensorFlow, Streamlit, Git",
)

domain_interest = st.text_input(
    "Domain interest (optional)",
    placeholder="e.g., Healthcare AI, Finance, NLP, Computer Vision",
)

if st.button("Recommend Projects", type="primary"):
    skills_list = [s.strip() for s in skills_input.split(",") if s.strip()]
    with st.spinner("AI is generating project ideas..."):
        try:
            result = recommend_projects(skills_list, target_role, domain_interest)
            st.session_state.project_recs = result
        except Exception as e:
            st.error(f"Error: {e}")

result = st.session_state.get("project_recs")
if result:
    if result.get("parse_error"):
        st.error("Could not parse AI response. Raw response below:")
        st.write(result.get("raw_response"))
    else:
        st.markdown("---")
        projects = result.get("projects", [])
        for i, p in enumerate(projects, 1):
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{i}. {p.get('title', 'Untitled Project')}")
                with col2:
                    diff = p.get("difficulty", "")
                    color = {"Beginner": "🟢", "Intermediate": "🟡", "Advanced": "🔴"}.get(diff, "")
                    st.markdown(f"**{color} {diff}**")

                st.write(p.get("description", ""))

                tech_stack = p.get("tech_stack", [])
                if tech_stack:
                    st.markdown("**Tech Stack:** " + ", ".join(f"`{t}`" for t in tech_stack))

                resume_value = p.get("resume_value", "")
                if resume_value:
                    st.info(f"Why it stands out: {resume_value}")

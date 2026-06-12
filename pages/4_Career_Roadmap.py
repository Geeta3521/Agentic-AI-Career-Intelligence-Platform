"""
Page 4: Roadmap Generator Agent
"""

import streamlit as st
from agents.roadmap_agent import generate_roadmap

st.set_page_config(page_title="Career Roadmap", page_icon="🗺️", layout="wide")

st.title("🗺️ Career Roadmap Agent")
st.markdown("Generate a month-by-month preparation plan tailored to your goals.")

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

months = st.slider("Number of months to plan for", min_value=2, max_value=6, value=4)

if st.button("Generate Roadmap", type="primary"):
    skills_list = [s.strip() for s in skills_input.split(",") if s.strip()]
    with st.spinner("AI is generating your roadmap..."):
        try:
            result = generate_roadmap(skills_list, target_role, months)
            st.session_state.roadmap_result = result
        except Exception as e:
            st.error(f"Error: {e}")

result = st.session_state.get("roadmap_result")
if result:
    if result.get("parse_error"):
        st.error("Could not parse AI response. Raw response below:")
        st.write(result.get("raw_response"))
    else:
        st.markdown("---")
        roadmap = result.get("roadmap", [])

        for item in roadmap:
            month = item.get("month", "")
            with st.container(border=True):
                st.subheader(f"Month {month}")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Focus Areas:**")
                    for f in item.get("focus_areas", []):
                        st.markdown(f"- {f}")

                with col2:
                    st.markdown("**Tasks:**")
                    for t in item.get("tasks", []):
                        st.checkbox(t, key=f"task_{month}_{t[:20]}")

                milestone = item.get("milestone", "")
                if milestone:
                    st.success(f"Milestone: {milestone}")

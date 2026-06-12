"""
Page 7: GitHub Profile Analysis Agent
"""

import streamlit as st
from agents.github_agent import analyze_github_profile

st.set_page_config(page_title="GitHub Analyzer", page_icon="🐙", layout="wide")

st.title("🐙 GitHub Profile Analyzer")
st.markdown("Get AI feedback on your GitHub profile's placement readiness.")

target_role = st.session_state.get("target_role", "AI/ML Engineer")
st.caption(f"Target role: **{target_role}** (change this in the sidebar on the Home page)")

username = st.text_input(
    "GitHub username",
    value=st.session_state.get("github_username", ""),
    placeholder="e.g., Geeta3521",
)

if st.button("Analyze GitHub Profile", type="primary"):
    if not username.strip():
        st.warning("Please enter a GitHub username.")
    else:
        st.session_state.github_username = username.strip()
        with st.spinner("Fetching repos and analyzing profile..."):
            try:
                result = analyze_github_profile(username.strip(), target_role)
                st.session_state.github_analysis = result
            except Exception as e:
                st.error(f"Error: {e}")

result = st.session_state.get("github_analysis")
if result:
    if result.get("error"):
        st.error(result["error"])
    elif result.get("parse_error"):
        st.error("Could not parse AI response. Raw response below:")
        st.write(result.get("raw_response"))
    else:
        st.markdown("---")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("Public Repos", result.get("repo_count", 0))
            rating = result.get("overall_rating", "N/A")
            st.metric("Overall Rating", rating)

        with col2:
            standout = result.get("standout_repos", [])
            if standout:
                st.markdown("**Repos to Pin/Highlight:**")
                for s in standout:
                    st.markdown(f"- ⭐ `{s}`")

        st.markdown("---")
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Strengths")
            for s in result.get("strengths", []):
                st.markdown(f"- {s}")

        with col4:
            st.subheader("Improvements")
            for imp in result.get("improvements", []):
                st.markdown(f"- {imp}")

        st.markdown("---")
        st.subheader("Your Repositories")
        repos = result.get("repos_summary", [])
        if repos:
            for r in repos:
                with st.expander(f"{r['name']} ({r.get('language') or 'N/A'}) - {r.get('stars', 0)} stars"):
                    st.write(r.get("description") or "No description")
                    st.caption(f"Last updated: {r.get('updated_at', 'N/A')}")

"""utils/session.py — shared state across pages"""
import streamlit as st


def set(key, val):       st.session_state[key] = val
def get(key, default=None): return st.session_state.get(key, default)
def has(key):            return bool(st.session_state.get(key))

def save_resume(text):   set("resume_text", text)
def get_resume():        return get("resume_text", "")
def has_resume():        return bool(get("resume_text", "").strip())

def save_role(role):     set("target_role", role)
def get_role():          return get("target_role", "AI Engineer")

def save_user(name):     set("user_name", name)
def get_user():          return get("user_name", "Student")

def save_dashboard(d):   set("dashboard_data", d)
def get_dashboard():     return get("dashboard_data", {})
def has_dashboard():     return bool(get("dashboard_data", {}))

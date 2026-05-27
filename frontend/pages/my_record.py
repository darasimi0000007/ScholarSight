import streamlit as st
import pandas as pd
from utils import inject_css, render_sidebar, require_login, get_user, api_get_student

st.set_page_config(page_title="ScholarSight – My Record", page_icon="📋", layout="wide")
inject_css()
require_login()
render_sidebar()

user = get_user()
student_id = user.get("student_id", "")

st.markdown("""
<div class="page-header">
    <h2>📋 My Academic Record</h2>
    <p>View your stored academic profile and prediction result.</p>
</div>
""", unsafe_allow_html=True)

if not student_id:
    st.markdown("""
    <div class="alert-error">
        ⚠️ No student ID associated with your account. Please contact administration.
    </div>
    """, unsafe_allow_html=True)
else:
    with st.spinner("Loading your record..."):
        student_data, err = api_get_student(student_id)

    if err:
        st.markdown(f"""
        <div class="alert-error">
            ❌ Could not load your record: {err}
        </div>
        """, unsafe_allow_html=True)
    elif student_data:
        # ── Profile Summary ──────────────────────────────────────────────────
        st.markdown('<div class="ss-card-accent">', unsafe_allow_html=True)
        st.markdown("#### 🎓 Your Academic Profile")

        col1, col2, col3 = st.columns(3)

        prediction = str(student_data.get("Prediction", "")).lower()
        is_pass = prediction in ("pass", "1", "true")
        badge_color = "#4ade80" if is_pass else "#f87171"
        badge_text = "PASS ✅" if is_pass else "FAIL ❌"

        with col1:
            st.markdown(f"""
            <div class="stat-tile">
                <div class="stat-value" style="font-size:1.5rem;color:{badge_color};">{badge_text}</div>
                <div class="stat-label">Prediction</div>
            </div>""", unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="stat-tile">
                <div class="stat-value">{student_data.get('age', 'N/A')}</div>
                <div class="stat-label">Age</div>
            </div>""", unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="stat-tile">
                <div class="stat-value">{student_data.get('health', 'N/A')}/5</div>
                <div class="stat-label">Health Rating</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

        # ── Detailed Information ──────────────────────────────────────────────
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Detailed Information")

        # Create a cleaner display of student data
        display_data = {}
        for key, value in student_data.items():
            if key not in ["_sa_instance_state", "id"]:
                # Format the key name
                formatted_key = key.replace("_", " ").title()
                display_data[formatted_key] = value

        # Display in columns
        col_left, col_right = st.columns(2)

        items = list(display_data.items())
        mid_point = len(items) // 2

        with col_left:
            for key, value in items[:mid_point]:
                st.markdown(f"""
                <p style="color:#94A3B8;font-size:0.88rem;margin-bottom:0.5rem;">
                    <strong>{key}:</strong> {value}
                </p>
                """, unsafe_allow_html=True)

        with col_right:
            for key, value in items[mid_point:]:
                st.markdown(f"""
                <p style="color:#94A3B8;font-size:0.88rem;margin-bottom:0.5rem;">
                    <strong>{key}:</strong> {value}
                </p>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── View Analysis Button ──────────────────────────────────────────────
        st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

        col_button, _ = st.columns([1, 3])
        with col_button:
            if st.button("🧠 View My SHAP Analysis", use_container_width=True):
                st.session_state["analysis_student_id"] = student_id
                st.switch_page("pages/my_analysis.py")

    else:
        st.markdown("""
        <div class="ss-card" style="text-align:center;padding:3rem 1rem;">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">📭</div>
            <div style="color:#94A3B8;margin-bottom:0.5rem;font-size:0.9rem;">No record found</div>
            <div style="color:#64748B;font-size:0.8rem;">Your prediction record will appear here once a prediction is made.</div>
        </div>""", unsafe_allow_html=True)

# ── Info box ──────────────────────────────────────────────────────────────────
st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="ss-card" style="display:flex;gap:1.5rem;align-items:flex-start;">
    <div style="font-size:2rem;flex-shrink:0;">ℹ️</div>
    <div style="font-size:0.85rem;color:#94A3B8;line-height:1.7;">
        <strong style="color:#CBD5E1;">Your Prediction Explanation</strong>
        Click on "View My SHAP Analysis" to understand which of your academic characteristics
        had the most impact on your prediction. This will show you exactly why the model
        made the prediction it did.
    </div>
</div>
""", unsafe_allow_html=True)

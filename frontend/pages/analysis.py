import streamlit as st
from utils import inject_css, render_sidebar, require_staff, api_get_student, api_get_shap_chart

st.set_page_config(page_title="ScholarSight – SHAP Analysis", page_icon="🧠", layout="wide")
inject_css()
require_staff()
render_sidebar()

st.markdown("""
<div class="page-header">
    <h2>🧠 SHAP Feature Analysis</h2>
    <p>Understand how features influence student performance predictions using SHAP values.</p>
</div>
""", unsafe_allow_html=True)

# ── Input form ───────────────────────────────────────────────────────────────
st.markdown('<div class="ss-card">', unsafe_allow_html=True)
st.markdown("#### 🔍 Select Student for Analysis")

# Check if we have a pre-selected student from predict page
analysis_student_id = st.session_state.get("analysis_student_id", "")

student_id = st.text_input(
    "Enter Student ID",
    value=analysis_student_id,
    placeholder="e.g. STU001",
    help="Enter the ID of the student whose prediction you want to analyze"
)

st.markdown('</div>', unsafe_allow_html=True)

# ── Fetch and display analysis ────────────────────────────────────────────────
if student_id.strip():
    student_id = student_id.strip()

    with st.spinner("Fetching student data and generating SHAP analysis..."):
        student_data, student_err = api_get_student(student_id)
        shap_chart, shap_err = api_get_shap_chart(student_id)

    # Display student info
    if not student_err and student_data:
        st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### 📋 Student Information")

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown(f"""
            <p style="color:#94A3B8;font-size:0.88rem;"><strong>Student ID:</strong> {student_data.get('student_id', 'N/A')}</p>
            <p style="color:#94A3B8;font-size:0.88rem;"><strong>Age:</strong> {student_data.get('age', 'N/A')}</p>
            <p style="color:#94A3B8;font-size:0.88rem;"><strong>Address:</strong> {student_data.get('address', 'N/A')}</p>
            """, unsafe_allow_html=True)

        with col_right:
            prediction = str(student_data.get("Prediction", "")).lower()
            is_pass = prediction in ("pass", "1", "true")
            badge_color = "#4ade80" if is_pass else "#f87171"
            badge_text = "PASS ✅" if is_pass else "FAIL ❌"

            st.markdown(f"""
            <p style="color:#94A3B8;font-size:0.88rem;"><strong>Prediction:</strong> <span style="color:{badge_color};font-weight:600;">{badge_text}</span></p>
            <p style="color:#94A3B8;font-size:0.88rem;"><strong>Health Rating:</strong> {student_data.get('health', 'N/A')}/5</p>
            <p style="color:#94A3B8;font-size:0.88rem;"><strong>Absences:</strong> {student_data.get('absences', 'N/A')}</p>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    elif student_err:
        st.markdown(f'<div class="alert-error">❌ Could not fetch student data: {student_err}</div>', unsafe_allow_html=True)

    # Display SHAP chart
    if not shap_err and shap_chart:
        st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 SHAP Feature Importance")
        st.markdown("""
        <p style="color:#94A3B8;font-size:0.85rem;line-height:1.6;">
            This chart shows the most impactful features in determining the prediction.
            <br>Features on the right (red) pushed the prediction toward <strong style="color:#f87171;">FAIL</strong>,
            while features on the left (blue) pushed toward <strong style="color:#4ade80;">PASS</strong>.
        </p>
        """, unsafe_allow_html=True)

        st.image(shap_chart, caption="SHAP Summary Plot (Bar)", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif shap_err:
        st.markdown(f'<div class="alert-error">❌ Could not generate SHAP analysis: {shap_err}</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="ss-card" style="text-align:center;padding:3rem 1rem;">
        <div style="font-size:2.5rem;margin-bottom:0.8rem;">🧠</div>
        <div style="color:#94A3B8;margin-bottom:0.5rem;font-size:0.9rem;">Enter a Student ID above</div>
        <div style="color:#64748B;font-size:0.8rem;">View detailed SHAP analysis of their prediction.</div>
    </div>""", unsafe_allow_html=True)

# ── Info box ──────────────────────────────────────────────────────────────────
st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="ss-card" style="display:flex;gap:1.5rem;align-items:flex-start;">
    <div style="font-size:2rem;flex-shrink:0;">💡</div>
    <div style="font-size:0.85rem;color:#94A3B8;line-height:1.7;">
        <strong style="color:#CBD5E1;">What is SHAP Analysis?</strong>
        SHAP (SHapley Additive exPlanations) is a game-theoretic approach to explain predictions.
        It shows which features had the most influence on the model's decision — whether pushing
        toward Pass or Fail. This makes predictions transparent and auditable.
    </div>
</div>
""", unsafe_allow_html=True)

import streamlit as st
from utils import inject_css, render_sidebar, require_teacher, api_predict

st.set_page_config(page_title="ScholarSight – Predict", page_icon="🔮", layout="wide")
inject_css()
require_teacher()
render_sidebar()

st.markdown("""
<div class="page-header">
    <h2>🔮 Make a Prediction</h2>
    <p>Enter a student's academic characteristics to generate a performance prediction.</p>
</div>
""", unsafe_allow_html=True)

# ── Form ─────────────────────────────────────────────────────────────────────
col_form, col_result = st.columns([1.1, 0.9], gap="large")

with col_form:
    # st.markdown('<div class="ss-card">', unsafe_allow_html=True)
    st.markdown("#### 🎓 Student Academic Profile")
    st.markdown('<p style="color:#64748B;font-size:0.83rem;margin-bottom:1.2rem;">Fill in all fields. Hover labels for details.</p>', unsafe_allow_html=True)

    # Row 1 – Identity
    c1, c2, c3, c4= st.columns(4)
    with c1:
        student_id = st.text_input("Student ID *", placeholder="e.g. STU001", help="Unique student identifier")
    with c2:
        sex = st.selectbox("Gender", ["M", "F"], help="Student's gender")
    with c3:
        age = st.number_input("Age", min_value=10, max_value=30, value=17, step=1)
    with c4:
        address = st.selectbox("Address(Rural(R) or Urban(U)))", ["U", "R"], help="Student's residential area")

    # Row 2 – personal and family details
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        famsize = st.selectbox("Family Size", ["LE3", "GT3"], help="Size of the student's family: (Greater than 3 or Less than 3)")
    with c2:
        pstatus = st.selectbox("Parental Status", ["T", "A"], help ="Whether parents live together (T) or apart (A)")
    with c3:
        guardian = st.selectbox("Student's Guardian", ["mother", "father", "other"])
    with c4:
        traveltime = st.selectbox("TravelTime to School", [1, 2, 3, 4], help = "less than 15 minutes(1), between 15 minutes and 30 minutes(2), between 30 minutes and 1 hour(3), more than 1 hour(4)")

    # Row 3 – Exam scores
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        studytime = st.selectbox("StudyTime", [1, 2, 3, 4], help = "less than 2 hours(1), between 2 hours and 5 hours(2), between 5 hours and 10 hours(3), more than 10 hours(4)")
    with c2:
        failures = st.selectbox("Failures", [0, 1, 2, 3], help = "None(0), One(1), Two(2), Three or More(3)")
    with c3:
        schoolsup = st.selectbox("Private Tutoring", ["yes", "no"])
    with c4:
        famsup = st.selectbox("Familial Support", ["yes", "no"], help = "Student getting familial support from parents or guardian?")

    # Row 4 – Behavioural / socio
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        activities  = st.selectbox("Extracurriculars", ["yes", "no"], help= "Is student into any extracurriculars?")
    with c2:
        nursery = st.selectbox("Attended Nursery School", ["yes", "no"])
    with c3:
        famrel = st.selectbox("Familial Relationship with Student", [1, 2, 3, 4, 5], help = "Very Poor(1), Poor(2), Average(3), Good(4), Very Good(5)")
    with c4:
        health = st.selectbox("Student's Health", [1, 2, 3, 4, 5], help = "Very Poor(1), Poor(2), Average(3), Good(4), Very Good(5)")


    c1, c2, c3 = st.columns(3)
    with c1:
        absences = st.number_input("School Absences", min_value = 0, max_value = 70, value = 3, step = 1)
    with c2:
        freetime = st.selectbox("Free Time after School", [1, 2, 3, 4, 5], help = "Very Low(1), Low(2), Average(3), Free(4), Very Free(5)")
    with c3:
        goout = st.selectbox("Student's Social Life", [1, 2, 3, 4, 5], help = "Very Low(1), Low(2), Average(3), Free(4), Very Free(5)")



    # Row 5 – freeform JSON for extra fields
    c1, c2 = st.columns(2)
    with c1:
        internet = st.selectbox("Student's Internet Access", ["yes", "no"])
    with c2:
        romantic = st.selectbox("Student in Romantic Relationship", ["yes", "no"])

   

    st.markdown('</div>', unsafe_allow_html=True)

    submit = st.button("Generate Prediction  →", width="stretch", key="predict_btn")

# ── Result panel ─────────────────────────────────────────────────────────────
with col_result:
    st.markdown('<div class="ss-card" style="min-height:420px;">', unsafe_allow_html=True)
    st.markdown("#### 🧾 Prediction Result")

    result_placeholder = st.empty()

    if not submit:
        result_placeholder.markdown("""
        <div style="text-align:center;padding:3rem 0;color:#475569;">
            <div style="font-size:3rem;margin-bottom:0.8rem;">🔮</div>
            <div style="font-size:0.9rem;">Fill in the form and click<br><strong style="color:#64748B;">Generate Prediction</strong> to see results here.</div>
        </div>
        """, unsafe_allow_html=True)

    if submit:
        if not student_id.strip():
            st.markdown('<div class="alert-error">⚠️ Student ID is required.</div>', unsafe_allow_html=True)
        else:
            # Build payload
            payload = {
                "student_id":       student_id.strip(),
                "sex":              sex,
                "age":              age,
                "address":       address,
                "famsize":       famsize,
                "Pstatus":      pstatus,
                "guardian":    guardian,
                "traveltime": traveltime,
                "studytime":       studytime,
                "failures":         failures,
                "schoolsup":         schoolsup,
                "famsup":              famsup,
                "activities":    activities,
                "nursery":           nursery,
                "famrel":           famrel,
                "health":           health,
                "absences":       absences,
                "freetime":       freetime,
                "goout":           goout,
                "internet":       internet,
                "romantic":       romantic,
            }

            with st.spinner("Running prediction model…"):
                res, err = api_predict(payload)

            if err:
                result_placeholder.markdown(f'<div class="alert-error">❌ {err}</div>', unsafe_allow_html=True)
            elif res:
                prediction = res.get("prediction", res.get("result", ""))
                confidence = res.get("confidence", res.get("probability", None))
                is_pass    = str(prediction).lower() in ("pass", "1", "true")

                badge_cls = "prediction-pass" if is_pass else "prediction-fail"
                label     = "PASS ✅" if is_pass else "FAIL ❌"
                color     = "#4ade80" if is_pass else "#f87171"

                conf_html = ""
                if confidence is not None:
                    pct = round(float(confidence) * 100, 1) if float(confidence) <= 1 else round(float(confidence), 1)
                    conf_html = f'<p style="color:#94A3B8;margin:0.4rem 0 0;font-size:0.88rem;">Confidence: <strong style="color:{color};">{pct}%</strong></p>'

                result_placeholder.markdown(f"""
                <div class="{badge_cls}">
                    <div style="font-size:0.78rem;color:#94A3B8;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;">Predicted Outcome</div>
                    <div style="font-size:2.8rem;font-weight:800;color:{color};line-height:1;">{label}</div>
                    <div style="font-size:0.85rem;color:#94A3B8;margin-top:0.6rem;">Student ID: <code style="color:#CBD5E1;">{student_id}</code></div>
                    {conf_html}
                </div>
                """, unsafe_allow_html=True)

                # Show raw response
                # st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
                # with st.expander("📄 Full API Response"):
                #     st.json(res)

                # st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
                # if st.button("🧠 View SHAP Analysis for this Student", width="stretch"):
                #     st.session_state["analysis_student_id"] = student_id.strip()
                #     st.switch_page("pages/analysis.py")
            else:
                result_placeholder.markdown('<div class="alert-error">❌ Unexpected error: no response data.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Info box ─────────────────────────────────────────────────────────────────
st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="ss-card" style="display:flex;gap:1.5rem;align-items:flex-start;">
    <div style="font-size:2rem;flex-shrink:0;">💡</div>
    <div style="font-size:0.85rem;color:#94A3B8;line-height:1.7;">
        <strong style="color:#CBD5E1;">How this works:</strong>
        The submitted features are sent to the FastAPI backend, which passes them through the
        <em>Gradient Boosting Classifier</em>. The model returns a binary Pass/Fail prediction along
        with a probability score. Once a prediction is stored, you can generate a
        <strong style="color:#CBD5E1;">SHAP analysis</strong> to understand which features drove that outcome.
    </div>
</div>
""", unsafe_allow_html=True)

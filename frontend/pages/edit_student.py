import streamlit as st
from utils import inject_css, render_sidebar, require_teacher, api_get_student, api_update_student



st.set_page_config(page_title="ScholarSight – Edit Student", page_icon="✏️", layout="wide")
inject_css()
require_teacher()
render_sidebar()

st.markdown("""
<div class="page-header">
    <h2>✏️ Edit Student Record</h2>
    <p>Load a student's existing record and update any fields. The prediction is automatically re-run on save.</p>
</div>
""", unsafe_allow_html=True)

# ── Step 1: ID lookup ─────────────────────────────────────────────────────────
# st.markdown('<div class="ss-card">', unsafe_allow_html=True)
st.markdown("#### 🔍 Look Up Student")

# Pre-fill from session if coming from another page
prefill_id = st.session_state.pop("edit_student_id", "")

lookup_id = st.text_input(
    "Student ID",
    value=prefill_id,
    placeholder="e.g. STU001",
    help="Enter the student ID whose record you want to edit",
    key="edit_lookup_id",
)

col_load, _ = st.columns([1, 4])
with col_load:
    load_clicked = st.button("Load Record →", width="stretch", key="load_student_btn")

st.markdown('</div>', unsafe_allow_html=True)

# ── Step 2: Load + render form ────────────────────────────────────────────────
if load_clicked and lookup_id.strip():
    st.session_state["_edit_loaded_id"] = lookup_id.strip().upper()
    st.session_state.pop("_edit_data", None)   # clear stale data on a fresh load

if "_edit_loaded_id" not in st.session_state:
    st.markdown("""
    <div class="ss-card" style="text-align:center;padding:3rem 1rem;">
        <div style="font-size:2.5rem;margin-bottom:0.8rem;">✏️</div>
        <div style="color:#94A3B8;margin-bottom:0.5rem;font-size:0.9rem;">Enter a Student ID above and click Load Record</div>
        <div style="color:#64748B;font-size:0.8rem;">All existing values will be pre-filled so you only change what you need.</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

target_id = st.session_state["_edit_loaded_id"]

# Fetch once and cache in session so the form doesn't re-fetch on every widget interaction
if "_edit_data" not in st.session_state:
    with st.spinner(f"Loading record for {target_id}…"):
        student_data, fetch_err = api_get_student(target_id)
    if fetch_err:
        st.markdown(f'<div class="alert-error">❌ {fetch_err}</div>', unsafe_allow_html=True)
        st.stop()
    if not student_data:
        st.markdown('<div class="alert-error">❌ No record found for that ID.</div>', unsafe_allow_html=True)
        st.stop()
    st.session_state["_edit_data"] = student_data

d = st.session_state["_edit_data"]

# ── Current prediction banner ─────────────────────────────────────────────────
prediction = str(d.get("Prediction", "")).lower()
is_pass = prediction in ("pass", "1", "true")
pred_color = "#4ade80" if is_pass else "#f87171"
pred_label = "PASS ✅" if is_pass else "FAIL ❌"

st.markdown(f"""
<div class="ss-card-accent" style="display:flex;align-items:center;gap:1.5rem;margin-bottom:1rem;">
    <div style="font-size:2rem;">🎓</div>
    <div>
        <div style="font-size:0.78rem;color:#64748B;text-transform:uppercase;letter-spacing:0.08em;">Editing record for</div>
        <div style="font-size:1.1rem;font-weight:700;color:#F1F5F9;">{target_id}</div>
        <div style="font-size:0.85rem;color:#94A3B8;margin-top:2px;">
            Current prediction: <strong style="color:{pred_color};">{pred_label}</strong>
            &nbsp;·&nbsp; Saving will re-run the model and may change this.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

# ── Edit form ─────────────────────────────────────────────────────────────────
# st.markdown('<div class="ss-card">', unsafe_allow_html=True)
st.markdown("#### 📝 Update Fields")
st.markdown('<p style="color:#64748B;font-size:0.83rem;margin-bottom:1.2rem;">All fields are pre-filled with the current stored values. Change only what needs updating.</p>', unsafe_allow_html=True)

# helpers to find current index in option lists
def _idx(options, current):
    try:
        return options.index(current)
    except ValueError:
        return 0

SEX_OPTS        = ["M", "F"]
ADDR_OPTS       = ["U", "R"]
FAMSIZE_OPTS    = ["LE3", "GT3"]
PSTATUS_OPTS    = ["T", "A"]
GUARDIAN_OPTS   = ["mother", "father", "other"]
TT_OPTS         = [1, 2, 3, 4]
ST_OPTS         = [1, 2, 3, 4]
YESNO_OPTS      = ["yes", "no"]
FAIL_OPTS       = [0, 1, 2, 3]
FAMREL_OPTS     = [1, 2, 3, 4, 5]
HEALTH_OPTS     = [1, 2, 3, 4, 5]
FREETIME_OPTS   = [1, 2, 3, 4, 5]
GOOUT_OPTS      = [1, 2, 3, 4, 5]

# Row 1 – Identity / Demographics
c1, c2, c3, c4 = st.columns(4)
with c1:
    sex = st.selectbox("Gender", SEX_OPTS,
                       index=_idx(SEX_OPTS, d.get("sex", "M")),
                       help="M or F")
with c2:
    age = st.number_input("Age", min_value=10, max_value=30,
                          value=int(d.get("age", 17)), step=1)
with c3:
    address = st.selectbox("Address (U/R)", ADDR_OPTS,
                           index=_idx(ADDR_OPTS, d.get("address", "U")),
                           help="Urban or Rural")
with c4:
    famsize = st.selectbox("Family Size", FAMSIZE_OPTS,
                           index=_idx(FAMSIZE_OPTS, d.get("famsize", "LE3")),
                           help="LE3 = ≤3 members, GT3 = >3 members")

# Row 2 – Family
c1, c2, c3, c4 = st.columns(4)
with c1:
    pstatus = st.selectbox("Parental Status", PSTATUS_OPTS,
                           index=_idx(PSTATUS_OPTS, d.get("Pstatus", "T")),
                           help="T = Together, A = Apart")
with c2:
    guardian = st.selectbox("Guardian", GUARDIAN_OPTS,
                            index=_idx(GUARDIAN_OPTS, d.get("guardian", "mother")))
with c3:
    famrel = st.selectbox("Family Relationship", FAMREL_OPTS,
                          index=_idx(FAMREL_OPTS, int(d.get("famrel", 3))),
                          help="1=Very Poor … 5=Very Good")
with c4:
    famsup = st.selectbox("Family Support", YESNO_OPTS,
                          index=_idx(YESNO_OPTS, d.get("famsup", "yes")))

# Row 3 – School logistics
c1, c2, c3, c4 = st.columns(4)
with c1:
    traveltime = st.selectbox("Travel Time", TT_OPTS,
                              index=_idx(TT_OPTS, int(d.get("traveltime", 1))),
                              help="1=<15 min, 2=15–30 min, 3=30 min–1 hr, 4=>1 hr")
with c2:
    studytime = st.selectbox("Study Time", ST_OPTS,
                             index=_idx(ST_OPTS, int(d.get("studytime", 2))),
                             help="1=<2 hrs, 2=2–5 hrs, 3=5–10 hrs, 4=>10 hrs")
with c3:
    failures = st.selectbox("Past Failures", FAIL_OPTS,
                            index=_idx(FAIL_OPTS, int(d.get("failures", 0))),
                            help="0=None, 1=One, 2=Two, 3=Three or more")
with c4:
    absences = st.number_input("Absences", min_value=0, max_value=60,
                               value=int(d.get("absences", 0)), step=1)

# Row 4 – Support & activities
c1, c2, c3, c4 = st.columns(4)
with c1:
    schoolsup = st.selectbox("Private Tutoring", YESNO_OPTS,
                             index=_idx(YESNO_OPTS, d.get("schoolsup", "no")))
with c2:
    activities = st.selectbox("Extracurriculars", YESNO_OPTS,
                              index=_idx(YESNO_OPTS, d.get("activities", "no")))
with c3:
    nursery = st.selectbox("Attended Nursery", YESNO_OPTS,
                           index=_idx(YESNO_OPTS, d.get("nursery", "yes")))
with c4:
    internet = st.selectbox("Internet Access", YESNO_OPTS,
                            index=_idx(YESNO_OPTS, d.get("internet", "yes")))

# Row 5 – Lifestyle
c1, c2, c3, c4 = st.columns(4)
with c1:
    health = st.selectbox("Health", HEALTH_OPTS,
                          index=_idx(HEALTH_OPTS, int(d.get("health", 3))),
                          help="1=Very Poor … 5=Very Good")
with c2:
    freetime = st.selectbox("Free Time", FREETIME_OPTS,
                            index=_idx(FREETIME_OPTS, int(d.get("freetime", 3))),
                            help="1=Very Low … 5=Very Free")
with c3:
    goout = st.selectbox("Goes Out", GOOUT_OPTS,
                         index=_idx(GOOUT_OPTS, int(d.get("goout", 3))),
                         help="1=Very Low … 5=Very High")
with c4:
    romantic = st.selectbox("Romantic Relationship", YESNO_OPTS,
                            index=_idx(YESNO_OPTS, d.get("romantic", "no")))

st.markdown('</div>', unsafe_allow_html=True)

# ── Save button ───────────────────────────────────────────────────────────────
st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

col_save, col_cancel, _ = st.columns([1, 1, 3])

with col_save:
    save_clicked = st.button("💾 Save Changes", width="stretch", key="save_edit_btn")

with col_cancel:
    if st.button("✕ Cancel", width="stretch", key="cancel_edit_btn"):
        st.session_state.pop("_edit_loaded_id", None)
        st.session_state.pop("_edit_data", None)
        st.switch_page("pages/records.py")

if save_clicked:
    payload = {
        "sex":        sex,
        "age":        age,
        "address":    address,
        "famsize":    famsize,
        "Pstatus":    pstatus,
        "guardian":   guardian,
        "traveltime": traveltime,
        "studytime":  studytime,
        "failures":   failures,
        "schoolsup":  schoolsup,
        "famsup":     famsup,
        "activities": activities,
        "nursery":    nursery,
        "famrel":     famrel,
        "health":     health,
        "absences":   absences,
        "freetime":   freetime,
        "goout":      goout,
        "internet":   internet,
        "romantic":   romantic,
    }

    with st.spinner("Saving and re-running prediction…"):
        result, err = api_update_student(target_id, payload)

    if err:
        st.markdown(f'<div class="alert-error">❌ {err}</div>', unsafe_allow_html=True)
    else:
        # Clear cached data so next load fetches fresh values
        st.session_state.pop("_edit_data", None)
        st.markdown(f"""
        <div class="alert-success">
            ✅ Record for <strong>{target_id}</strong> updated successfully.
            The prediction has been re-run based on the new values.
        </div>
        """, unsafe_allow_html=True)

        # col_view, col_shap, _ = st.columns([1, 1, 2])
        # with col_view:
        #     if st.button("🗂️ Back to Records", width="stretch"):
        #         st.session_state.pop("_edit_loaded_id", None)
        #         st.switch_page("pages/records.py")
        # with col_shap:
        #     if st.button("🧠 View SHAP Analysis", width="stretch"):
        #         st.session_state["analysis_student_id"] = target_id
        #         st.switch_page("pages/analysis.py")

# ── Info box ──────────────────────────────────────────────────────────────────
st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="ss-card" style="display:flex;gap:1.5rem;align-items:flex-start;">
    <div style="font-size:2rem;flex-shrink:0;">💡</div>
    <div style="font-size:0.85rem;color:#94A3B8;line-height:1.7;">
        <strong style="color:#CBD5E1;">How partial updates work:</strong>
        Only the fields you change are sent to the backend. The backend then re-runs the
        Gradient Boosting model on the full updated record and stores the new prediction.
        This means even changing a single field (e.g. absences) will update the prediction result.
    </div>
</div>
""", unsafe_allow_html=True)

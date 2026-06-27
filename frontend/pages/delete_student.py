import streamlit as st
from utils import inject_css, render_sidebar, require_teacher, api_get_student, api_delete_student

st.set_page_config(page_title="ScholarSight – Delete Student", page_icon="🗑️", layout="wide")
inject_css()
require_teacher()
render_sidebar()

st.markdown("""
<div class="page-header">
    <h2>🗑️ Delete Student Record</h2>
    <p>Permanently remove a student's prediction record from the system.</p>
</div>
""", unsafe_allow_html=True)

# ── Danger-zone CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
.danger-card {
    background: linear-gradient(135deg, #7f1d1d18 0%, #1E293B 100%);
    border: 1px solid #dc262644;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.danger-card:hover { border-color: #dc2626aa; }

.confirm-banner {
    background: #7f1d1d22;
    border: 2px solid #dc262666;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
}

.stButton > button[data-testid="delete_confirm_btn"] {
    background: #dc2626 !important;
}
.stButton > button[data-testid="delete_confirm_btn"]:hover {
    background: #b91c1c !important;
    box-shadow: 0 4px 16px #dc262644 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Step 1: ID lookup ─────────────────────────────────────────────────────────
st.markdown('<div class="ss-card">', unsafe_allow_html=True)
st.markdown("#### 🔍 Find Student Record")

prefill_id = st.session_state.pop("delete_student_id", "")

lookup_id = st.text_input(
    "Student ID",
    value=prefill_id,
    placeholder="e.g. STU001",
    help="Enter the student ID you want to delete",
    key="delete_lookup_id",
)

col_find, _ = st.columns([1, 4])
with col_find:
    find_clicked = st.button("Find Record →", width="stretch", key="find_student_btn")

st.markdown('</div>', unsafe_allow_html=True)

if find_clicked and lookup_id.strip():
    st.session_state["_del_target_id"] = lookup_id.strip().upper()
    st.session_state["_del_confirmed"] = False
    st.session_state.pop("_del_student_data", None)

if "_del_target_id" not in st.session_state:
    st.markdown("""
    <div class="ss-card" style="text-align:center;padding:3rem 1rem;">
        <div style="font-size:2.5rem;margin-bottom:0.8rem;">🗑️</div>
        <div style="color:#94A3B8;margin-bottom:0.5rem;font-size:0.9rem;">Enter a Student ID above and click Find Record</div>
        <div style="color:#64748B;font-size:0.8rem;">You will be shown the record details before confirming deletion.</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

target_id = st.session_state["_del_target_id"]

# Fetch and cache
if "_del_student_data" not in st.session_state:
    with st.spinner(f"Fetching record for {target_id}…"):
        student_data, fetch_err = api_get_student(target_id)
    if fetch_err:
        st.markdown(f'<div class="alert-error">❌ {fetch_err}</div>', unsafe_allow_html=True)
        st.stop()
    if not student_data:
        st.markdown('<div class="alert-error">❌ No record found for that ID.</div>', unsafe_allow_html=True)
        st.stop()
    st.session_state["_del_student_data"] = student_data

d = st.session_state["_del_student_data"]

# ── Step 2: Show record summary ───────────────────────────────────────────────
prediction = str(d.get("Prediction", "")).lower()
is_pass = prediction in ("pass", "1", "true")
pred_color = "#4ade80" if is_pass else "#f87171"
pred_label = "PASS ✅" if is_pass else "FAIL ❌"

st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
st.markdown('<div class="danger-card">', unsafe_allow_html=True)
st.markdown("#### 📋 Record to be Deleted")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="stat-value" style="font-size:1.3rem;">{d.get('student_id', target_id)}</div>
        <div class="stat-label">Student ID</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="stat-value" style="font-size:1.5rem;color:{pred_color};">{pred_label}</div>
        <div class="stat-label">Prediction</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="stat-value">{d.get('age', 'N/A')}</div>
        <div class="stat-label">Age</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="stat-value">{d.get('absences', 'N/A')}</div>
        <div class="stat-label">Absences</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

# Full record detail (collapsed by default)
with st.expander("📄 View Full Record Details"):
    col_left, col_right = st.columns(2)
    items = [(k, v) for k, v in d.items() if k not in ("_sa_instance_state",)]
    mid = len(items) // 2
    with col_left:
        for key, value in items[:mid]:
            st.markdown(f'<p style="color:#94A3B8;font-size:0.85rem;margin-bottom:0.3rem;"><strong>{key}:</strong> {value}</p>', unsafe_allow_html=True)
    with col_right:
        for key, value in items[mid:]:
            st.markdown(f'<p style="color:#94A3B8;font-size:0.85rem;margin-bottom:0.3rem;"><strong>{key}:</strong> {value}</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Step 3: Confirmation gate ─────────────────────────────────────────────────
st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

if not st.session_state.get("_del_confirmed", False):
    st.markdown(f"""
    <div class="confirm-banner">
        <div style="font-size:1.1rem;font-weight:700;color:#f87171;margin-bottom:0.5rem;">
            ⚠️ This action is permanent and cannot be undone
        </div>
        <div style="color:#94A3B8;font-size:0.88rem;">
            You are about to permanently delete the record for
            <strong style="color:#F1F5F9;">{target_id}</strong>.
            All stored data and prediction history for this student will be lost.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_confirm, col_cancel, _ = st.columns([1, 1, 3])
    with col_confirm:
        if st.button("🗑️ Yes, Delete Permanently", width="stretch", key="delete_confirm_btn"):
            st.session_state["_del_confirmed"] = True
            st.rerun()
    with col_cancel:
        if st.button("✕ Cancel", width="stretch", key="delete_cancel_btn"):
            st.session_state.pop("_del_target_id", None)
            st.session_state.pop("_del_student_data", None)
            st.session_state.pop("_del_confirmed", None)
            st.switch_page("pages/records.py")

# ── Step 4: Execute deletion ──────────────────────────────────────────────────
else:
    with st.spinner(f"Deleting record for {target_id}…"):
        success, err = api_delete_student(target_id)

    if err:
        st.markdown(f'<div class="alert-error">❌ Deletion failed: {err}</div>', unsafe_allow_html=True)
        # Reset confirmation so they can retry or cancel
        st.session_state["_del_confirmed"] = False
    else:
        # Clear all deletion state
        st.session_state.pop("_del_target_id", None)
        st.session_state.pop("_del_student_data", None)
        st.session_state.pop("_del_confirmed", None)

        st.markdown(f"""
        <div class="alert-success">
            ✅ Record for <strong>{target_id}</strong> has been permanently deleted.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

        # col_records, col_new, _ = st.columns([1, 1, 2])
        # with col_records:
        #     if st.button("🗂️ Back to Records", width="stretch", key="post_del_records_btn"):
        #         st.switch_page("pages/records.py")
        # with col_new:
        #     if st.button("🔮 New Prediction", width="stretch", key="post_del_predict_btn"):
        #         st.switch_page("pages/predict.py")

# ── Info box ──────────────────────────────────────────────────────────────────
st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="ss-card" style="display:flex;gap:1.5rem;align-items:flex-start;">
    <div style="font-size:2rem;flex-shrink:0;">⚠️</div>
    <div style="font-size:0.85rem;color:#94A3B8;line-height:1.7;">
        <strong style="color:#CBD5E1;">Important:</strong>
        Deleting a student record removes all stored academic data and the associated prediction.
        If you only want to correct a field, consider using <strong style="color:#CBD5E1;">Edit Student Record</strong> instead.
        Deletion cannot be reversed.
    </div>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from utils import inject_css, render_sidebar, require_teacher, api_get_all_students, api_delete_student, get_role

st.set_page_config(page_title="ScholarSight – Student Records", page_icon="🗂️", layout="wide")
inject_css()
require_teacher()
render_sidebar()

st.markdown("""
<div class="page-header">
    <h2>🗂️ Student Records</h2>
    <p>View, search, and manage all student prediction records in the system.</p>
</div>
""", unsafe_allow_html=True)

# ── Fetch all records ─────────────────────────────────────────────────────────
data, err = api_get_all_students()

if err:
    st.markdown(f'<div class="alert-error">❌ Error loading records: {err}</div>', unsafe_allow_html=True)
else:
    students = data.get("students", []) if isinstance(data, dict) else data or []

    # ── Stats row ─────────────────────────────────────────────────────────────
    if students:
        df = pd.DataFrame(students)
        total = len(students)
        pass_count = sum(1 for s in students if str(s.get("Prediction", "")).lower() in ("pass", "1", "true"))
        fail_count = sum(1 for s in students if str(s.get("Prediction", "")).lower() in ("fail", "0", "false"))
        pass_rate = round((pass_count / total * 100), 1) if total else 0

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="stat-tile">
                <div class="stat-value">{total}</div>
                <div class="stat-label">Total Records</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="stat-tile">
                <div class="stat-value" style="color:#4ade80;">{pass_count}</div>
                <div class="stat-label">Pass Predictions</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="stat-tile">
                <div class="stat-value" style="color:#f87171;">{fail_count}</div>
                <div class="stat-label">Fail Predictions</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class="stat-tile">
                <div class="stat-value">{pass_rate}%</div>
                <div class="stat-label">Pass Rate</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

        # ── Search & Filter ───────────────────────────────────────────────────
        # st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### 🔍 Search & Filter")

        col_search, col_export = st.columns([2, 1])
        with col_search:
            search_term = st.text_input("Search by Student ID", placeholder="Enter student ID...")
        with col_export:
            st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)
            if st.button("📥 Export as CSV", width="stretch"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="student_records.csv",
                    mime="text/csv",
                    width="stretch"
                )

        # Filter based on search
        if search_term:
            df_filtered = df[df["student_id"].astype(str).str.contains(search_term, case=False, na=False)]
        else:
            df_filtered = df

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

        # ── Records Table ─────────────────────────────────────────────────────
        # st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown(f"#### 📋 Records ({len(df_filtered)} of {len(df)})")

        # Display dataframe
        display_df = df_filtered.copy()

        # Format prediction column with badges
        if "Prediction" in display_df.columns:
            def pred_badge(val):
                v = str(val).lower()
                if v in ("pass", "1", "true"):
                    return "✅ PASS"
                elif v in ("fail", "0", "false"):
                    return "❌ FAIL"
                return val

            display_df["Prediction"] = display_df["Prediction"].apply(pred_badge)

        st.dataframe(
            display_df,
            width="stretch",
            hide_index=True,
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Admin-only actions ────────────────────────────────────────────────
        if get_role() == "admin":
            st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
            # st.markdown('<div class="ss-card">', unsafe_allow_html=True)
            st.markdown("#### ⚙️ Admin Actions")

            col_delete, col_space = st.columns([1, 3])
            with col_delete:
                student_to_delete = st.text_input("Delete Student ID", placeholder="Enter ID to delete...", key="delete_student_id")

            if student_to_delete:
                col_confirm, col_cancel = st.columns(2)
                with col_confirm:
                    if st.button("🗑️ Confirm Delete", width="stretch", type="primary"):
                        success, msg = api_delete_student(student_to_delete)
                        if success:
                            st.markdown(f'<div class="alert-success">✅ {msg}</div>', unsafe_allow_html=True)
                            st.rerun()
                        else:
                            st.markdown(f'<div class="alert-error">❌ {msg}</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="ss-card" style="text-align:center;padding:3rem 1rem;">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">📭</div>
            <div style="color:#94A3B8;margin-bottom:0.5rem;font-size:0.9rem;">No records found</div>
            <div style="color:#64748B;font-size:0.8rem;">Create a prediction to see records here.</div>
        </div>""", unsafe_allow_html=True)

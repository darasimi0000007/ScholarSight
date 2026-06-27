import streamlit as st
import pandas as pd
from utils import inject_css, render_sidebar, require_login, get_role, get_user, api_get_all_students

st.set_page_config(page_title="ScholarSight – Dashboard", page_icon="📊", layout="wide")
inject_css()
require_login()
render_sidebar()

role = get_role()
user = get_user()

# ── Page header ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <h2>📊 Dashboard</h2>
    <p>Welcome back, <strong>{user.get('institution_id', 'User').upper()}</strong>. Here's an overview of ScholarSight.</p>
</div>
""", unsafe_allow_html=True)

# ── Teacher Dashboard ─────────────────────────────────────────────────────────
students = []
fetch_error = None

if role == "teacher":
    data, err = api_get_all_students()
    if err:
        fetch_error = err
    elif data:
        students = data if isinstance(data, list) else data.get("students", [])

# ── Stats row ────────────────────────────────────────────────────────────────
if role == "teacher":
    total     = len(students)
    pass_count = sum(1 for s in students if str(s.get("Prediction", "")).lower() in ("pass", "1", "true"))
    fail_count = sum(1 for s in students if str(s.get("Prediction", "")).lower() in ("fail", "0", "false"))
    pass_rate  = round((pass_count / total * 100), 1) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="stat-tile">
            <div class="stat-value">{total}</div>
            <div class="stat-label">Total Students</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-tile">
            <div class="stat-value" style="color:#4ade80;">{pass_count}</div>
            <div class="stat-label">Predicted Pass</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-tile">
            <div class="stat-value" style="color:#f87171;">{fail_count}</div>
            <div class="stat-label">Predicted Fail</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="stat-tile">
            <div class="stat-value">{pass_rate}%</div>
            <div class="stat-label">Pass Rate</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

    if fetch_error:
        st.markdown(f'<div class="alert-error">⚠️ Could not load records: {fetch_error}</div>', unsafe_allow_html=True)

    # ── Recent students table ────────────────────────────────────────────────
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### 🗂️ Recent Student Records")

        if students:
            df = pd.DataFrame(students)
            # render prediction column with coloured badges
            def pred_badge(val):
                v = str(val).lower()
                if v in ("pass", "1", "true"):
                    return "✅ PASS"
                elif v in ("fail", "0", "false"):
                    return "❌ FAIL"
                return val

            display_df = df.copy()
            if "prediction" in display_df.columns:
                display_df["prediction"] = display_df["prediction"].apply(pred_badge)

            st.dataframe(
                display_df.head(10),
                width="stretch",
                hide_index=True,
            )
            if len(students) > 10:
                st.caption(f"Showing 10 of {len(students)} records. View all in Student Records.")
        else:
            st.markdown('<div class="alert-info">No student records found. Start by making a prediction.</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### ⚡ Quick Actions")

        st.markdown("""
        <p style="color:#94A3B8;font-size:0.85rem;">Jump to the most common tasks:</p>
        """, unsafe_allow_html=True)

        if st.button("🔮 New Prediction", width="stretch"):
            st.switch_page("pages/predict.py")
        if st.button("🗂️ View All Records", width="stretch"):
            st.switch_page("pages/records.py")
        if st.button("✏️ Edit Student Record", width="stretch"):
            st.switch_page("pages/edit_student.py")
        if st.button("🗑️ Delete Student Record", width="stretch"):
            st.switch_page("pages/delete_student.py")
        if st.button("🧠 Run SHAP Analysis", width="stretch"):
            st.switch_page("pages/analysis.py")
        if st.button("📊 View Students' Analysis Data", width="stretch"):
            st.switch_page("pages/charts.py")

        st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

        st.markdown("#### ℹ️ About ScholarSight")
        st.markdown("""
        <div style="color:#94A3B8;font-size:0.83rem;line-height:1.65;">
            ScholarSight uses a <strong style="color:#CBD5E1;">Gradient Boosting Classifier</strong>
            trained on historical academic data.<br><br>
            Predictions are explained using <strong style="color:#CBD5E1;">SHAP</strong>
            (SHapley Additive exPlanations), making results fully transparent and auditable.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Pass/Fail distribution chart ─────────────────────────────────────────
    if students and pass_count + fail_count > 0:
        import plotly.graph_objects as go

        st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
        st.markdown("#### 📈 Prediction Distribution")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            fig = go.Figure(data=[go.Pie(
                labels=["Pass", "Fail"],
                values=[pass_count, fail_count],
                hole=0.55,
                marker=dict(colors=["#16a34a", "#dc2626"],
                            line=dict(color="#0F172A", width=2)),
                textfont=dict(family="Space Grotesk", size=13),
            )])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94A3B8", family="Space Grotesk"),
                legend=dict(font=dict(color="#94A3B8")),
                margin=dict(t=10, b=10, l=10, r=10),
                height=280,
                showlegend=True,
            )
            fig.add_annotation(
                text=f"<b>{pass_rate}%</b><br>Pass",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="#F1F5F9", family="Space Grotesk"),
            )
            st.plotly_chart(fig, width="stretch")

        with chart_col2:
            # Grade distribution if available
            if "grade" in (df.columns if students else []):
                grade_counts = df["grade"].value_counts().reset_index()
                grade_counts.columns = ["grade", "count"]
                fig2 = go.Figure(data=[go.Bar(
                    x=grade_counts["grade"],
                    y=grade_counts["count"],
                    marker_color="#2563EB",
                    marker_line_color="#0F172A",
                    marker_line_width=1.5,
                )])
                fig2.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#94A3B8", family="Space Grotesk"),
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=280,
                    xaxis=dict(gridcolor="#1E293B"),
                    yaxis=dict(gridcolor="#334155"),
                )
                st.plotly_chart(fig2, width="stretch")
            else:
                st.markdown(f"""
                <div class="ss-card" style="text-align:center;padding:3rem 1rem;">
                    <div style="font-size:2.5rem;">🎯</div>
                    <div style="color:#94A3B8;margin-top:0.5rem;font-size:0.9rem;">
                        {total} records analyzed
                    </div>
                    <div style="color:#64748B;font-size:0.8rem;margin-top:0.3rem;">
                        Grade breakdown available when grade field is present
                    </div>
                </div>""", unsafe_allow_html=True)

# ── Student Dashboard ─────────────────────────────────────────────────────────
else:  # student role
    st.markdown('<div class="ss-card-accent">', unsafe_allow_html=True)
    st.markdown(f"""
    #### 👋 Welcome, {user.get('institution_id', 'Student').upper()}!
    
    Get started with ScholarSight to understand your academic performance and get predictions about your success.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### 🔮 Make a Prediction")
        st.markdown("""
        Enter your personal and academic details to get a prediction about your performance 
        for the current term/semester.
        """)
        if st.button("Start Prediction", key="student_predict", width="stretch"):
            st.switch_page("pages/predict.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### 🔍 View My Analysis")
        st.markdown("""
        See the SHAP analysis for your predictions to understand which factors 
        influence your academic performance the most.
        """)
        if st.button("View Analysis", key="student_analysis", width="stretch"):
            st.switch_page("pages/my_analysis.py")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

    st.markdown("""
    <div class="ss-card">
    
    #### 💡 How ScholarSight Works
    
    1. **Enter Your Details** - Provide your personal and academic information
    2. **Get Prediction** - Our AI model predicts your performance (Pass/Fail)
    3. **Understand Why** - SHAP analysis explains which factors matter most
    4. **Take Action** - Use insights to improve your academic performance
    
    </div>
    """, unsafe_allow_html=True)

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
    <p>Welcome back, <strong>{user.get('name','')}</strong>. Here's an overview of ScholarSight.</p>
</div>
""", unsafe_allow_html=True)

# ── Fetch records (staff only pulls all) ─────────────────────────────────────
students = []
fetch_error = None

if role in ("teacher", "admin"):
    data, err = api_get_all_students()
    if err:
        fetch_error = err
    elif data:
        students = data if isinstance(data, list) else data.get("students", [])

# ── Stats row ────────────────────────────────────────────────────────────────
if role in ("teacher", "admin"):
    total     = len(students)
    pass_count = sum(1 for s in students if str(s.get("prediction", "")).lower() in ("pass", "1", "true"))
    fail_count = sum(1 for s in students if str(s.get("prediction", "")).lower() in ("fail", "0", "false"))
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
                use_container_width=True,
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

        if st.button("🔮 New Prediction", use_container_width=True):
            st.switch_page("pages/predict.py")
        if st.button("🗂️ View All Records", use_container_width=True):
            st.switch_page("pages/records.py")
        if st.button("🧠 Run SHAP Analysis", use_container_width=True):
            st.switch_page("pages/analysis.py")

        st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

        st.markdown("#### ℹ️ About the Model")
        st.markdown("""
        <div style="color:#94A3B8;font-size:0.83rem;line-height:1.65;">
            ScholarSight uses a <strong style="color:#CBD5E1;">Gradient Boosting Classifier</strong>
            trained on historical academic data.<br><br>
            Prediction explanations are generated with <strong style="color:#CBD5E1;">SHAP</strong>
            (SHapley Additive exPlanations), making every prediction fully transparent and auditable.
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
            st.plotly_chart(fig, use_container_width=True)

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
                st.plotly_chart(fig2, use_container_width=True)
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

# ── Student view ─────────────────────────────────────────────────────────────
else:
    student_id = user.get("student_id", "")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="stat-tile">
            <div class="stat-value" style="font-size:1.5rem;">📋</div>
            <div class="stat-label">My Academic Record</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="stat-tile">
            <div class="stat-value" style="font-size:1.5rem;">🔍</div>
            <div class="stat-label">Prediction Insights</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="stat-tile">
            <div class="stat-value" style="font-size:1.5rem;">🧠</div>
            <div class="stat-label">SHAP Explanation</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown('<div class="ss-card-accent">', unsafe_allow_html=True)
        st.markdown("#### 📋 My Record")
        st.markdown(f"""
        <p style="color:#94A3B8;font-size:0.88rem;">
            View your academic profile and prediction result using your student ID.
        </p>
        <p style="color:#64748B;font-size:0.82rem;">Your registered ID: <code style="color:#60a5fa;">{student_id or 'N/A'}</code></p>
        """, unsafe_allow_html=True)
        if st.button("View My Record →", use_container_width=True):
            st.switch_page("pages/my_record.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="ss-card-accent">', unsafe_allow_html=True)
        st.markdown("#### 🧠 My SHAP Analysis")
        st.markdown("""
        <p style="color:#94A3B8;font-size:0.88rem;">
            Understand <em>why</em> the model predicted your outcome — which factors helped or hurt your score.
        </p>
        """, unsafe_allow_html=True)
        if st.button("View My Analysis →", use_container_width=True):
            st.switch_page("pages/my_analysis.py")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="ss-card" style="margin-top:0.5rem;">
        <div style="font-size:0.88rem;color:#64748B;line-height:1.7;">
            <strong style="color:#94A3B8;">About ScholarSight Predictions</strong><br>
            Your performance prediction is generated by a <em>Gradient Boosting Classifier</em>
            trained on historical academic data from your institution.
            Each prediction is accompanied by a SHAP explanation chart that highlights exactly
            which features — such as attendance, past grades, or study hours — had the greatest
            impact on your result. This system is designed to support your learning journey,
            not define it.
        </div>
    </div>
    """, unsafe_allow_html=True)

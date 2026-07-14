import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import inject_css, render_sidebar, require_teacher, api_get_all_students

st.set_page_config(page_title="ScholarSight – Analytics", page_icon="📈", layout="wide")
inject_css()
require_teacher()
render_sidebar()

st.markdown("""
<div class="page-header">
    <h2>📈 Records Analytics</h2>
    <p>Visual breakdown of every student record stored in the system.</p>
</div>
""", unsafe_allow_html=True)

# ── Shared chart styling ───────────────────────────────────────────────────
def style_fig(fig, height=300):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8", family="Space Grotesk"),
        margin=dict(t=30, b=10, l=10, r=10),
        height=height,
        legend=dict(font=dict(color="#94A3B8")),
    )
    return fig

# ── Fetch data ───────────────────────────────────────────────────────────────
data, err = api_get_all_students()

if err:
    st.markdown(f'<div class="alert-error">❌ Error loading records: {err}</div>', unsafe_allow_html=True)
else:
    students = data.get("students", []) if isinstance(data, dict) else data or []

    if not students:
        st.markdown("""
        <div class="ss-card" style="text-align:center;padding:3rem 1rem;">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">📭</div>
            <div style="color:#94A3B8;margin-bottom:0.5rem;font-size:0.9rem;">No records found</div>
            <div style="color:#64748B;font-size:0.8rem;">Charts will appear here once predictions have been made.</div>
        </div>""", unsafe_allow_html=True)
    else:
        df = pd.DataFrame(students)

        # Normalized helper columns. "Prediction" matches the actual DB column casing
        # (see models.Blog.Prediction) — using a lowercase key here silently zeroes
        # out every count, same bug that was already fixed on the main dashboard.
        df["Prediction_norm"] = df.get("Prediction", "").astype(str).str.lower()
        df["age_num"] = pd.to_numeric(df.get("age"), errors="coerce")

        total = len(df)
        pass_count = int(df["Prediction_norm"].isin(["pass", "1", "true"]).sum())
        fail_count = int(df["Prediction_norm"].isin(["fail", "0", "false"]).sum())
        pass_rate = round((pass_count / total * 100), 1) if total else 0

        # ── Stat tiles ───────────────────────────────────────────────────────
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="stat-tile"><div class="stat-value">{total}</div><div class="stat-label">Total Records</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="stat-tile"><div class="stat-value" style="color:#4ade80;">{pass_count}</div><div class="stat-label">Predicted Pass</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="stat-tile"><div class="stat-value" style="color:#f87171;">{fail_count}</div><div class="stat-label">Predicted Fail</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="stat-tile"><div class="stat-value">{pass_rate}%</div><div class="stat-label">Pass Rate</div></div>""", unsafe_allow_html=True)

        st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)

        # ── Row 1: Pass/Fail + Gender ──────────────────────────────────────
        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            # st.markdown('<div class="ss-card">', unsafe_allow_html=True)
            st.markdown("#### ✅ Pass / Fail Distribution")
            fig = go.Figure(data=[go.Pie(
                labels=["Pass", "Fail"],
                values=[pass_count, fail_count],
                hole=0.55,
                marker=dict(colors=["#16a34a", "#dc2626"], line=dict(color="#0F172A", width=2)),
                textfont=dict(family="Space Grotesk", size=13),
            )])
            fig.add_annotation(text=f"<b>{pass_rate}%</b><br>Pass", x=0.5, y=0.5, showarrow=False,
                                font=dict(size=15, color="#F1F5F9", family="Space Grotesk"))
            st.plotly_chart(style_fig(fig), width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)

        with row1_col2:
            # st.markdown('<div class="ss-card">', unsafe_allow_html=True)
            st.markdown("#### 🚻 Gender Distribution")
            if "sex" in df.columns and df["sex"].notna().any():
                gender_counts = df["sex"].value_counts()
                labels = ["Male" if g == "M" else "Female" if g == "F" else g for g in gender_counts.index]
                fig = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=gender_counts.values,
                    hole=0.55,
                    marker=dict(colors=["#2563EB", "#0ea5e9", "#7c3aed"], line=dict(color="#0F172A", width=2)),
                    textfont=dict(family="Space Grotesk", size=13),
                )])
                st.plotly_chart(style_fig(fig), width="stretch")
            else:
                st.markdown('<div class="alert-info">No gender data available.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Row 2: Age + Absences ───────────────────────────────────────────
        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            # st.markdown('<div class="ss-card">', unsafe_allow_html=True)
            st.markdown("#### 🎂 Age Distribution")
            age_counts = df["age_num"].dropna().astype(int).value_counts().sort_index()
            if not age_counts.empty:
                fig = go.Figure(data=[go.Bar(
                    x=age_counts.index.astype(str), y=age_counts.values,
                    marker_color="#2563EB", marker_line_color="#0F172A", marker_line_width=1.5,
                )])
                fig.update_xaxes(title_text="Age", gridcolor="#1E293B")
                fig.update_yaxes(title_text="Students", gridcolor="#334155")
                st.plotly_chart(style_fig(fig), width="stretch")
            else:
                st.markdown('<div class="alert-info">No age data available.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with row2_col2:
            # st.markdown('<div class="ss-card">', unsafe_allow_html=True)
            st.markdown("#### 📅 Absences Distribution")
            if "absences" in df.columns:
                absences_num = pd.to_numeric(df["absences"], errors="coerce").dropna()
                if not absences_num.empty:
                    fig = go.Figure(data=[go.Histogram(
                        x=absences_num, marker_color="#0ea5e9", marker_line_color="#0F172A", marker_line_width=1,
                        nbinsx=12,
                    )])
                    fig.update_xaxes(title_text="Absences", gridcolor="#1E293B")
                    fig.update_yaxes(title_text="Students", gridcolor="#334155")
                    st.plotly_chart(style_fig(fig), width="stretch")
                else:
                    st.markdown('<div class="alert-info">No absences data available.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-info">No absences data available.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Row 3: Failures + Health ─────────────────────────────────────────
        row3_col1, row3_col2 = st.columns(2)

        with row3_col1:
            # st.markdown('<div class="ss-card">', unsafe_allow_html=True)
            st.markdown("#### ⚠️ Past Failures Breakdown")
            if "failures" in df.columns:
                failures_counts = pd.to_numeric(df["failures"], errors="coerce").dropna().astype(int).value_counts().sort_index()
                if not failures_counts.empty:
                    fig = go.Figure(data=[go.Bar(
                        x=[str(i) for i in failures_counts.index], y=failures_counts.values,
                        marker_color="#dc2626", marker_line_color="#0F172A", marker_line_width=1.5,
                    )])
                    fig.update_xaxes(title_text="Number of Past Failures", gridcolor="#1E293B")
                    fig.update_yaxes(title_text="Students", gridcolor="#334155")
                    st.plotly_chart(style_fig(fig), width="stretch")
                else:
                    st.markdown('<div class="alert-info">No failures data available.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-info">No failures data available.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with row3_col2:
            # st.markdown('<div class="ss-card">', unsafe_allow_html=True)
            st.markdown("#### 💪 Health Rating Distribution")
            if "health" in df.columns:
                health_counts = pd.to_numeric(df["health"], errors="coerce").dropna().astype(int).value_counts().sort_index()
                if not health_counts.empty:
                    fig = go.Figure(data=[go.Bar(
                        x=[str(i) for i in health_counts.index], y=health_counts.values,
                        marker_color="#16a34a", marker_line_color="#0F172A", marker_line_width=1.5,
                    )])
                    fig.update_xaxes(title_text="Health Rating (1=Very Poor, 5=Very Good)", gridcolor="#1E293B")
                    fig.update_yaxes(title_text="Students", gridcolor="#334155")
                    st.plotly_chart(style_fig(fig), width="stretch")
                else:
                    st.markdown('<div class="alert-info">No health data available.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-info">No health data available.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Row 4: Study time vs outcome (full width) ────────────────────────
        # st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### 📚 Study Time vs Predicted Outcome")
        if "studytime" in df.columns:
            study_df = df.copy()
            study_df["studytime_num"] = pd.to_numeric(study_df["studytime"], errors="coerce")
            study_df = study_df.dropna(subset=["studytime_num"])
            study_df["outcome"] = study_df["Prediction_norm"].apply(
                lambda v: "Pass" if v in ("pass", "1", "true") else ("Fail" if v in ("fail", "0", "false") else "Unknown")
            )

            if not study_df.empty:
                grouped = study_df.groupby(["studytime_num", "outcome"]).size().unstack(fill_value=0).sort_index()

                fig = go.Figure()
                if "Pass" in grouped.columns:
                    fig.add_trace(go.Bar(name="Pass", x=[str(int(i)) for i in grouped.index], y=grouped["Pass"], marker_color="#16a34a"))
                if "Fail" in grouped.columns:
                    fig.add_trace(go.Bar(name="Fail", x=[str(int(i)) for i in grouped.index], y=grouped["Fail"], marker_color="#dc2626"))
                fig.update_layout(barmode="group")
                fig.update_xaxes(title_text="Study Time (1=<2hrs, 2=2-5hrs, 3=5-10hrs, 4=>10hrs)", gridcolor="#1E293B")
                fig.update_yaxes(title_text="Students", gridcolor="#334155")
                st.plotly_chart(style_fig(fig, height=340), width="stretch")
            else:
                st.markdown('<div class="alert-info">No study time data available.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-info">No study time data available.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

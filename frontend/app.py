import streamlit as st
from utils import inject_css, login, is_logged_in, get_role

st.set_page_config(
    page_title="ScholarSight – Login",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)
inject_css()

# Already logged in → go to dashboard
if is_logged_in():
    st.switch_page("./pages/dashboard.py")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* hide sidebar toggle on login page */
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

.login-hero {
    text-align: center;
    padding: 3rem 0 2rem;
}
.login-logo-icon {
    width: 72px; height: 72px;
    background: linear-gradient(135deg, #2563EB, #0ea5e9);
    border-radius: 18px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 2.2rem;
    box-shadow: 0 8px 30px #2563eb55;
    margin-bottom: 1.2rem;
}
.login-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #F1F5F9;
    letter-spacing: -0.02em;
    margin-bottom: 0.4rem;
}
.login-subtitle {
    color: #64748B;
    font-size: 0.95rem;
    letter-spacing: 0.03em;
}
.login-box {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 2.2rem 2.5rem;
    max-width: 420px;
    margin: 0 auto;
    box-shadow: 0 20px 60px #00000055;
}
.divider-text {
    text-align: center;
    color: #475569;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    margin: 1.2rem 0;
    position: relative;
}
.divider-text::before, .divider-text::after {
    content: "";
    position: absolute;
    top: 50%;
    width: 38%;
    height: 1px;
    background: #334155;
}
.divider-text::before { left: 0; }
.divider-text::after  { right: 0; }

.demo-grid {
    display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.6rem;
    margin-top: 0.5rem;
}
.demo-tile {
    background: #0F172A;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 0.65rem 0.5rem;
    text-align: center;
    cursor: pointer;
}
.demo-tile .dt-role { font-size: 0.68rem; color: #64748B; text-transform:uppercase; letter-spacing:0.06em; }
.demo-tile .dt-user { font-size: 0.82rem; font-weight:600; color:#CBD5E1; margin:3px 0; }
.demo-tile .dt-pass { font-size: 0.72rem; color:#475569; font-family:'DM Mono',monospace; }
</style>

<div class="login-hero">
    <div class="login-logo-icon">🎓</div>
    <div class="login-title">ScholarSight</div>
    <div class="login-subtitle">ACADEMIC INTELLIGENCE PLATFORM</div>
</div>
""", unsafe_allow_html=True)

# ── Login form ────────────────────────────────────────────────────────────────
_, col, _ = st.columns([0.5, 3, 0.5])
with col:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    st.markdown('<p style="color:#94A3B8;font-size:0.9rem;margin-bottom:1rem;font-weight:600;">Sign in to your account</p>', unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter username", key="login_username")
    password = st.text_input("Password", placeholder="Enter password", type="password", key="login_password")

    if st.button("Sign In  →", use_container_width=True, key="login_btn"):
        if not username or not password:
            st.markdown('<div class="alert-error">Please enter both username and password.</div>', unsafe_allow_html=True)
        else:
            user = login(username, password)
            if user:
                st.session_state["user"] = user
                st.success(f"Welcome back, {user['name']}!")
                st.switch_page("./pages/dashboard.py")
            else:
                st.markdown('<div class="alert-error">Invalid credentials. Please try again.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="divider-text">DEMO ACCOUNTS</div>
    <div class="demo-grid">
        <div class="demo-tile">
            <div class="dt-role">Admin</div>
            <div class="dt-user">admin</div>
            <div class="dt-pass">admin123</div>
        </div>
        <div class="demo-tile">
            <div class="dt-role">Teacher</div>
            <div class="dt-user">teacher</div>
            <div class="dt-pass">teacher123</div>
        </div>
        <div class="demo-tile">
            <div class="dt-role">Student</div>
            <div class="dt-user">student</div>
            <div class="dt-pass">student123</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<p style="text-align:center;color:#334155;font-size:0.75rem;margin-top:2rem;">
    ScholarSight v1.0 &nbsp;·&nbsp; Powered by Gradient Boosting + SHAP
</p>
""", unsafe_allow_html=True)

import streamlit as st
import requests
from utils import inject_css, is_logged_in, restore_session, persist_session
from dotenv import load_dotenv
import os



load_dotenv()

st.set_page_config(
    page_title="ScholarSight – Login",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_css()

# Redirect if already logged in
restore_session()
if is_logged_in():
    st.switch_page("./pages/dashboard.py")


ALLOWED_ORIGINS = os.getenv("BACKEND_URL", "http://localhost:8000").split(",")
API_BASE = ALLOWED_ORIGINS[0]  

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
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

.divider-line {
    height: 1px;
    background: linear-gradient(90deg, #334155 0%, #33415500 100%);
    margin: 1.5rem 0;
    border: none;
}
.signup-link {
    text-align: center;
    color: #94A3B8;
    font-size: 0.9rem;
    margin-top: 1.5rem;
}
.signup-link a {
    color: #2563EB;
    text-decoration: none;
    font-weight: 600;
}
.signup-link a:hover {
    text-decoration: underline;
}
.form-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #CBD5E1;
    margin-bottom: 0.4rem;
    display: block;
}
</style>



""", unsafe_allow_html=True)  


# ── Display Logo ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="login-hero">
    <div class="login-logo-icon">🎓</div>
    <div class="login-title">ScholarSight</div>
    <div class="login-subtitle">ACADEMIC INTELLIGENCE PLATFORM</div>
</div>
""", unsafe_allow_html=True)

# ── Login Form ────────────────────────────────────────────────────────────────
_, col_main, _ = st.columns([0.5, 3, 0.5])

with col_main:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    st.markdown('<p style="color:#94A3B8;font-size:0.9rem;margin-bottom:1.5rem;font-weight:600;">Sign in to your account</p>', unsafe_allow_html=True)

    # # Institution ID field
    # st.markdown('<p class="form-label">Institution ID</p>', unsafe_allow_html=True)
    # institution_id = st.text_input(
    #     label="Institution ID",
    #     placeholder="STU001234 or TEA005678",
    #     key="login_institution_id",
    #     label_visibility="collapsed",
    #     help="Your institution ID (starts with STU or TEA)"
    # )

    # Email login field
    st.markdown('<p class="form-label">Email Address</p>', unsafe_allow_html=True)
    email = st.text_input(
        label="Email",
        placeholder="your.email@institution.com",
        key="login_email",
        label_visibility="collapsed",
        help="The email you registered with"
    )

    # Password field
    st.markdown('<p class="form-label">Password</p>', unsafe_allow_html=True)
    password = st.text_input(
        label="Password",
        type="password",
        placeholder="••••••••",
        key="login_password",
        label_visibility="collapsed"
    )

    if st.button("Sign In  →", width="stretch", key="login_btn"):
        if not email or not password:
            st.markdown('<div class="alert-error">❌ Please fill in all fields.</div>', unsafe_allow_html=True)
        else:
            # Call backend login endpoint
            try:
                # Use form-data format for OAuth2PasswordRequestForm compatibility
                login_data = {
                    "username": email,  # Backend expects username field for email
                    "password": password
                }
                
                response = requests.post(
                    f"{API_BASE}/auth/login",
                    data=login_data,  # form-encoded instead of JSON
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    access_token = data.get("access_token")
                    
                    # Store user session with token and institution_id
                    st.session_state["user"] = {
                        "email": email,
                        "institution_id": data.get("institution_id"),
                        "access_token": access_token,
                        "token_type": data.get("token_type", "bearer")
                    }
                    persist_session(st.session_state["user"])
                    
                    st.markdown('<div class="alert-success">✅ Login successful! Redirecting to dashboard...</div>', unsafe_allow_html=True)
                    st.switch_page("./pages/dashboard.py")
                else:
                    error_detail = response.json().get("detail", "Invalid credentials")
                    st.markdown(f'<div class="alert-error">❌ {error_detail}</div>', unsafe_allow_html=True)
            except requests.exceptions.ConnectionError:
                st.markdown('<div class="alert-error">❌ Cannot reach the backend server. Is FastAPI running on port 8000?</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="alert-error">❌ Error: {str(e)}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider-line">', unsafe_allow_html=True)

    col_signup_left, col_signup_right = st.columns([1, 1])
    with col_signup_right:
        if st.button("Create Account →", key="signup_link_btn", width="stretch"):
            st.switch_page("./pages/signup.py")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<p style="text-align:center;color:#334155;font-size:0.75rem;margin-top:2rem;">
    ScholarSight v1.0 &nbsp;&nbsp; Powered by Gradient Boosting + SHAP
</p>
""", unsafe_allow_html=True)


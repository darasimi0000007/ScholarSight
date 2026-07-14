import streamlit as st
import requests
from utils import inject_css, is_logged_in
from dotenv import load_dotenv
import os
from typing import cast, Any

load_dotenv()

st.set_page_config(
    page_title="ScholarSight – Sign Up",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_css()

# Redirect if already logged in
if is_logged_in():
    st.switch_page("./pages/dashboard.py")

ALLOWED_ORIGINS = os.getenv("BACKEND_URL", "http://localhost:8000").split(",")
API_BASE = ALLOWED_ORIGINS[0]

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<style>

.signup-hero {
    text-align: center;
    padding: 3rem 0 2rem;
}
.signup-logo-icon {
    width: 72px; height: 72px;
    background: linear-gradient(135deg, #2563EB, #0ea5e9);
    border-radius: 18px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 2.2rem;
    box-shadow: 0 8px 30px #2563eb55;
    margin-bottom: 1.2rem;
}
.signup-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #F1F5F9;
    letter-spacing: -0.02em;
    margin-bottom: 0.4rem;
}
.signup-subtitle {
    color: #64748B;
    font-size: 0.95rem;
    letter-spacing: 0.03em;
}

.step-indicator {
    background: #1E293B;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    margin-bottom: 1.5rem;
    border: 1px solid #334155;
}
.step-number {
    font-size: 0.75rem;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.3rem;
}
.step-title {
    font-size: 1rem;
    font-weight: 600;
    color: #CBD5E1;
}
.info-message {
    background: #2563eb18;
    border: 1px solid #2563eb44;
    border-radius: 10px;
    padding: 1rem;
    color: #93c5fd;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}
.success-message {
    background: #16a34a18;
    border: 1px solid #16a34a44;
    border-radius: 10px;
    padding: 1rem;
    color: #4ade80;
    text-align: center;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}
.role-badge {
    display: inline-block;
    background: #7c3aed22;
    color: #a78bfa;
    border: 1px solid #7c3aed55;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-top: 0.3rem;
}
.role-badge.student {
    background: #0ea5e922;
    color: #38bdf8;
    border-color: #0ea5e955;
}
.form-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #CBD5E1;
    margin-bottom: 0.4rem;
    display: block;
    margin-top: 1rem;
}
.form-label:first-of-type {
    margin-top: 0;
}
</style>

            

""", unsafe_allow_html=True)



# ── Display Logo ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="signup-hero">
    <div class="signup-logo-icon">🎓</div>
    <div class="signup-title">ScholarSight</div>
    <div class="signup-subtitle">ACADEMIC INTELLIGENCE PLATFORM</div>
</div>
""", unsafe_allow_html=True)

# ── Signup Flow ───────────────────────────────────────────────────────────────
_, col_main, _ = st.columns([0.5, 3, 0.5])

with col_main:
    # Initialize session state
    if "signup_step" not in st.session_state:
        st.session_state.signup_step = "institution_id"
    if "signup_institution_id" not in st.session_state:
        st.session_state.signup_institution_id = ""
    if "signup_token" not in st.session_state:
        st.session_state.signup_token = None
    if "signup_role" not in st.session_state:
        st.session_state.signup_role = None

    st.markdown('<div class="signup-box">', unsafe_allow_html=True)

    # ── STEP 1: Institution ID Verification ───────────────────────────────────
    if st.session_state.signup_step == "institution_id":
        st.markdown("""
        <div class="step-indicator">
            <div class="step-number">STEP 1 OF 2</div>
            <div class="step-title">Verify Your Role</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-message">
            <strong>🔐 Enter your Institution ID</strong><br>
            This identifies whether you are a Student (STU prefix) or Teacher (TEA prefix).
        </div>
        """, unsafe_allow_html=True)

        institution_id = st.text_input(
            label="Institution ID",
            placeholder="e.g., STU001 or TEA345",
            key="signup_inst_input",
            help="Your unique institutional identifier (e.g., STU001 for students, TEA345 for teachers)"
        )

        if st.button("Verify & Continue →", key="verify_role_btn", width="stretch"):
            if not institution_id or len(institution_id) < 3:
                st.markdown('<div class="alert-error">❌ Please enter a valid institution ID (e.g., STU001 or TEA345)</div>', unsafe_allow_html=True)
            else:
                # Call backend to verify role
                try:
                    response = requests.post(
                        f"{API_BASE}/user/verify-role",
                        params={"institution_id": institution_id},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.signup_institution_id = (institution_id or "").upper()
                        st.session_state.signup_token = data.get("token")
                        # Extract role from message: "Verified as student" or "Verified as teacher"
                        message = data.get("message", "").lower()
                        if "student" in message:
                            st.session_state.signup_role = "student"
                        elif "teacher" in message:
                            st.session_state.signup_role = "teacher"
                        st.session_state.signup_step = "signup_form"
                        st.rerun()
                    else:
                        error_detail = response.json().get("detail", "Invalid institution ID format")
                        st.markdown(f'<div class="alert-error">❌ {error_detail}</div>', unsafe_allow_html=True)
                except requests.exceptions.ConnectionError:
                    st.markdown('<div class="alert-error">❌ Cannot reach the backend server. Is FastAPI running on port 8000?</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="alert-error">❌ Error: {str(e)}</div>', unsafe_allow_html=True)

        st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
        col_back_login, col_spacer = st.columns([1, 1])
        with col_back_login:
            if st.button("← Back to Login", key="back_to_login_from_verify", width="stretch"):
                st.switch_page("pages/login.py")

    # ── STEP 2: Signup Form ───────────────────────────────────────────────────
    elif st.session_state.signup_step == "signup_form":
        st.markdown(f"""
        <div class="step-indicator">
            <div class="step-number">STEP 2 OF 2</div>
            <div class="step-title">Create Your Account</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-message">
            <strong>Institution ID:</strong> {st.session_state.signup_institution_id}<br>
            <strong>Role:</strong> <span class="role-badge {'student' if st.session_state.signup_role == 'student' else ''}">{(st.session_state.signup_role or '').upper()}</span>
        </div>
        """, unsafe_allow_html=True)

        # Personal information
        st.markdown('<p class="form-label">👤 Personal Information</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            firstname = st.text_input("First Name", placeholder="John", key="signup_firstname")
        with col2:
            lastname = st.text_input("Last Name", placeholder="Doe", key="signup_lastname")

        # Email
        st.markdown('<p class="form-label">✉️ Email Address</p>', unsafe_allow_html=True)
        email = st.text_input(
            "Email",
            placeholder="john.doe@institution.com",
            key="signup_email",
            label_visibility="collapsed",
            help="Your institutional or personal email"
        )

        # Password
        st.markdown('<p class="form-label">🔐 Password</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••",
                key="signup_password",
                label_visibility="collapsed",
                help="Minimum 6 characters"
            )
        with col2:
            confirm_password = st.text_input(
                "Confirm",
                type="password",
                placeholder="••••••••",
                key="signup_confirm_password",
                label_visibility="collapsed"
            )

        col_back, col_submit = st.columns(2)

        with col_back:
            if st.button("← Back", key="back_to_verify", width="stretch"):
                st.session_state.signup_step = "institution_id"
                st.session_state.signup_token = None
                st.session_state.signup_role = None
                st.rerun()

        with col_submit:
            if st.button("Create Account →", key="create_account_btn", width="stretch"):
                # Validation
                if not firstname or not lastname or not email or not password or not confirm_password:
                    st.markdown('<div class="alert-error">❌ All fields are required</div>', unsafe_allow_html=True)
                elif len(password) < 6:
                    st.markdown('<div class="alert-error">❌ Password must be at least 6 characters</div>', unsafe_allow_html=True)
                elif password != confirm_password:
                    st.markdown('<div class="alert-error">❌ Passwords do not match</div>', unsafe_allow_html=True)
                elif "@" not in email:
                    st.markdown('<div class="alert-error">❌ Please enter a valid email address</div>', unsafe_allow_html=True)
                else:
                    # Call backend signup endpoint
                    try:
                        headers = {
                            "X-Verify-Token": st.session_state.signup_token
                        }
                        
                        payload = {
                            "firstname": firstname,
                            "lastname": lastname,
                            "email": email,
                            "password": password,
                            "confirm_password": confirm_password,
                            "institution_id": st.session_state.signup_institution_id
                        }
                        
                        response = requests.post(
                            f"{API_BASE}/user/signup",
                            json=payload,
                            headers=cast(Any, headers),
                            timeout=10
                        )
                        
                        if response.status_code == 201:
                            st.session_state.signup_step = "success"   # ← persist the outcome, nothing renders here
                            st.rerun()
                        
                        else:
                            error_detail = response.json().get("detail", "Signup failed")
                            st.markdown(f'<div class="alert-error">❌ {error_detail}</div>', unsafe_allow_html=True)
                    except requests.exceptions.ConnectionError:
                        st.markdown('<div class="alert-error">❌ Cannot reach the backend server. Is FastAPI running on port 8000?</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<div class="alert-error">❌ Error: {str(e)}</div>', unsafe_allow_html=True)



    # ── STEP 3: Success Message ───────────────────────────────────────────────
    elif st.session_state.signup_step == "success":
        st.markdown('<div class="success-message">✅ Account created successfully!</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-message" style="margin-top:1rem;">
            Your account has been created. You can now sign in with your email and password.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
        col_spacer, col_login = st.columns([1, 1])
        with col_login:
            if st.button("Go to Login →", key="signup_success_login_btn", width="stretch"):
                st.switch_page("pages/login.py")





    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<p style="text-align:center;color:#334155;font-size:0.75rem;margin-top:2rem;">
    ScholarSight v1.0 &nbsp;·&nbsp; Powered by Gradient Boosting + SHAP
</p>
""", unsafe_allow_html=True)

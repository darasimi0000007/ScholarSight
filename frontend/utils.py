import streamlit as st
import requests
import json
from fastapi import HTTPException, status


API_BASE = "http://127.0.0.1:8000"

# ──────────────────────────────────────────
#  Shared CSS injected on every page
# ──────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    /* ── Root overrides ── */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0F172A !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
        border-right: 1px solid #334155 !important;
    }
    [data-testid="stSidebar"] * { font-family: 'Space Grotesk', sans-serif !important; }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }

    /* ── Typography ── */
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; font-weight: 700 !important; }
    p, li, span, label { font-family: 'Space Grotesk', sans-serif !important; }
    code, pre { font-family: 'DM Mono', monospace !important; }

    /* ── Cards ── */
    .ss-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.2s;
    }
    .ss-card:hover { border-color: #2563EB; }

    .ss-card-accent {
        background: linear-gradient(135deg, #1E3A5F 0%, #1E293B 100%);
        border: 1px solid #2563EB44;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* ── Stat tiles ── */
    .stat-tile {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }
    .stat-tile .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2563EB;
        line-height: 1;
    }
    .stat-tile .stat-label {
        font-size: 0.78rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.35rem;
    }

    /* ── Badge chips ── */
    .badge-pass {
        display: inline-block;
        background: #16a34a22;
        color: #4ade80;
        border: 1px solid #16a34a55;
        border-radius: 20px;
        padding: 3px 14px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }
    .badge-fail {
        display: inline-block;
        background: #dc262622;
        color: #f87171;
        border: 1px solid #dc262655;
        border-radius: 20px;
        padding: 3px 14px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }
    .badge-role-student {
        display: inline-block;
        background: #0ea5e922;
        color: #38bdf8;
        border: 1px solid #0ea5e955;
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .badge-role-teacher {
        display: inline-block;
        background: #7c3aed22;
        color: #a78bfa;
        border: 1px solid #7c3aed55;
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .badge-role-admin {
        display: inline-block;
        background: #ea580c22;
        color: #fb923c;
        border: 1px solid #ea580c55;
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.78rem;
        font-weight: 600;
    }

    /* ── Page header strip ── */
    .page-header {
        background: linear-gradient(90deg, #1E3A5F 0%, #1E293B 60%, #0F172A 100%);
        border-left: 4px solid #2563EB;
        border-radius: 0 10px 10px 0;
        padding: 1rem 1.5rem;
        margin-bottom: 1.8rem;
    }
    .page-header h2 {
        margin: 0 !important;
        font-size: 1.35rem !important;
        color: #F1F5F9 !important;
    }
    .page-header p {
        margin: 0.25rem 0 0 !important;
        color: #94A3B8 !important;
        font-size: 0.88rem !important;
    }

    /* ── Dividers ── */
    .ss-divider {
        height: 1px;
        background: linear-gradient(90deg, #2563EB44 0%, #33415500 100%);
        margin: 1.5rem 0;
        border: none;
    }

    /* ── Alert boxes ── */
    .alert-success {
        background: #16a34a18;
        border: 1px solid #16a34a44;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        color: #4ade80;
        font-size: 0.9rem;
    }
    .alert-error {
        background: #dc262618;
        border: 1px solid #dc262644;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        color: #f87171;
        font-size: 0.9rem;
    }
    .alert-info {
        background: #2563eb18;
        border: 1px solid #2563eb44;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        color: #93c5fd;
        font-size: 0.9rem;
    }

    /* ── Streamlit button overrides ── */
    .stButton > button {
        background: #2563EB !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.4rem !important;
        transition: all 0.15s !important;
    }
    .stButton > button:hover {
        background: #1d4ed8 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px #2563eb44 !important;
    }
    .stButton > button[kind="secondary"] {
        background: #334155 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #475569 !important;
        box-shadow: none !important;
    }

    /* ── Input fields ── */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #F1F5F9 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px #2563eb33 !important;
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* ── Sidebar nav items ── */
    .nav-item {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.55rem 0.9rem;
        border-radius: 8px;
        margin-bottom: 0.25rem;
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 500;
        color: #94A3B8;
        transition: all 0.15s;
        text-decoration: none;
    }
    .nav-item:hover { background: #334155; color: #F1F5F9; }
    .nav-item.active { background: #2563EB22; color: #60a5fa; border-left: 3px solid #2563EB; }

    /* ── Logo area ── */
    .logo-block {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1.2rem 0.5rem 1.5rem;
        border-bottom: 1px solid #334155;
        margin-bottom: 1rem;
    }
    .logo-icon {
        width: 42px; height: 42px;
        background: linear-gradient(135deg, #2563EB, #0ea5e9);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem;
        flex-shrink: 0;
        box-shadow: 0 4px 12px #2563eb55;
    }
    .logo-text { line-height: 1.15; }
    .logo-text .app-name {
        font-size: 1.1rem; font-weight: 700; color: #F1F5F9;
    }
    .logo-text .app-tagline {
        font-size: 0.72rem; color: #64748B; letter-spacing: 0.04em;
    }

    /* ── Prediction result card ── */
    .prediction-pass {
        background: linear-gradient(135deg, #14532d22 0%, #1E293B 100%);
        border: 2px solid #16a34a55;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
    }
    .prediction-fail {
        background: linear-gradient(135deg, #7f1d1d22 0%, #1E293B 100%);
        border: 2px solid #dc262655;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
    }

    /* ── Tab overrides ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #1E293B;
        border-radius: 8px;
        padding: 4px;
        gap: 4px;
        border-bottom: none !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #94A3B8 !important;
        border-radius: 6px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        background: #2563EB !important;
        color: #fff !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_logo():
    st.markdown("""
    <div class="logo-block">
        <div class="logo-icon">🎓</div>
        <div class="logo-text">
            <div class="app-name">ScholarSight</div>
            <div class="app-tagline">ACADEMIC INTELLIGENCE PLATFORM</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────
#  Auth helpers (Token-based JWT system)
# ──────────────────────────────────────────

def is_logged_in():
    """Check if user is authenticated with valid token."""
    user = st.session_state.get("user")
    return user is not None and user.get("access_token") is not None

def get_user():
    """Get the current logged-in user data."""
    return st.session_state.get("user", {})

def get_role():
    """Get the role of the current user from institution_id (student or teacher)."""
    user = get_user()
    institution_id = user.get("institution_id", "").lower()
    
    if institution_id.startswith("stu"):
        return "student"
    elif institution_id.startswith("tea"):
        return "teacher"
    return None

def get_access_token():
    """Get the JWT access token for API requests."""
    user = get_user()
    return user.get("access_token")

def require_login():
    """Redirect to login if not authenticated."""
    if not is_logged_in():
        st.switch_page("app.py")
        st.stop()

def require_teacher():
    """Require user to be a teacher. Redirect to dashboard if not."""
    require_login()
    if get_role() != "teacher":
        st.error("⛔ Access denied. Teachers only.")
        st.stop()

def require_student():
    """Require user to be a student. Redirect to dashboard if not."""
    require_login()
    if get_role() != "student":
        st.error("⛔ Access denied. Students only.")
        st.stop()


# ──────────────────────────────────────────
#  API wrappers with JWT authentication
# ──────────────────────────────────────────
def _get_auth_headers():
    """Get Authorization headers with JWT token."""
    token = get_access_token()
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def api_predict(data: dict):
    """Make a prediction request to the backend."""
    try:
        headers = _get_auth_headers()
        r = requests.post(f"{API_BASE}/predict/raw", json=data, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot reach the backend server."
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response else "Unknown"
        try:
            detail = e.response.json().get("detail", "No detail") if e.response is not  None else "No response"
        except Exception:
            detail = e.response.text if e.response else "No response"
        return None, f"Prediction failed ({e.response.status_code}): {detail}" if e.response is not None else f"Prediction failed: {str(e)}"
    except Exception as e:
        return None, str(e)

def api_get_student(student_id: str):
    """Get details of a specific student."""
    try:
        headers = _get_auth_headers()
        r = requests.get(f"{API_BASE}/students/student/{student_id}", headers=headers, timeout=10)
        if r.status_code == 404:
            return None, "Student not found."
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot reach the backend server."
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response else "Unknown"
        return None, f"Failed to fetch student: {status}"
    except Exception as e:
        return None, str(e)

def api_get_all_students():
    """Fetch all students (teacher only)."""
    try:
        headers = _get_auth_headers()
        r = requests.get(f"{API_BASE}/students", headers=headers, timeout=10)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot reach the backend server."
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response else "Unknown"
        return None, f"Failed to fetch students: {status}"
    except Exception as e:
        return None, str(e)

def api_delete_student(student_id: str):
    """Delete a student record (teacher only)."""
    try:
        headers = _get_auth_headers()
        r = requests.delete(f"{API_BASE}/students/{student_id}", headers=headers, timeout=10)
        if r.status_code == 404:
            return False, "Student not found."
        r.raise_for_status()
        return True, None
    except requests.exceptions.ConnectionError:
        return False, "Cannot reach the backend server."
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response else "Unknown"
        return False, f"Delete failed: {status}"
    except Exception as e:
        return False, str(e)

def api_update_student(student_id: str, data: dict):
    """Partially update a student record (PATCH). Backend re-runs prediction on save."""
    try:
        headers = _get_auth_headers()
        r = requests.patch(
            f"{API_BASE}/students/student/{student_id}/update",
            json=data,
            headers=headers,
            timeout=30,
        )
        if r.status_code == 404:
            return None, "Student not found."
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot reach the backend server."
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", "No detail") if e.response is not None else "No response"
        except Exception:
            detail = e.response.text if e.response else "No response"
        code = e.response.status_code if e.response is not None else "?"
        return None, f"Update failed ({code}): {detail}"
    except Exception as e:
        return None, str(e)

def api_get_shap_chart(student_id: str):
    """Get SHAP analysis chart for a student (returns image bytes)."""
    try:
        headers = _get_auth_headers()
        r = requests.get(f"{API_BASE}/students/student/{student_id}/shap", headers=headers, timeout=20)
        if r.status_code == 404:
            return None, "No SHAP analysis found for this student."
        r.raise_for_status()
        return r.content, None
    except requests.exceptions.ConnectionError:
        return None, "Cannot reach the backend server."
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response else "Unknown"
        return None, f"Failed to fetch SHAP chart: {status}"
    except Exception as e:
        return None, str(e)


# ──────────────────────────────────────────
#  Sidebar renderer (shared across pages)
# ──────────────────────────────────────────
def render_sidebar():
    """Render the main navigation sidebar."""
    with st.sidebar:
        render_logo()
        user = get_user()
        role = get_role()
        email = user.get('email', 'User')
        institution_id = user.get('institution_id', '')

        role_badge_map = {
            "teacher": "badge-role-teacher",
            "student": "badge-role-student",
        }
        badge_cls = role_badge_map.get(role or "", "badge-role-student")
        role_label = role.upper() if role else "USER"

        st.markdown(f"""
        <div style="padding: 0 0.5rem 1rem;">
            <div style="font-size:0.82rem; color:#94A3B8; margin-bottom:4px;">Logged in as</div>
            <div style="font-size:0.95rem; font-weight:600; color:#F1F5F9; margin-bottom:6px; word-break:break-word;">{email}</div>
            <span class="{badge_cls}">{role_label}</span>
        </div>
        <hr class="ss-divider" style="margin:0.5rem 0 1rem;" />
        """, unsafe_allow_html=True)

        st.page_link("pages/dashboard.py", label="📊  Dashboard")

        if role == "teacher":
            st.markdown('<div style="color:#64748B;font-size:0.72rem;letter-spacing:0.08em;padding:0.6rem 0.5rem 0.2rem;">TEACHER TOOLS</div>', unsafe_allow_html=True)
            st.page_link("pages/predict.py",        label="🔮  Make Prediction")
            st.page_link("pages/records.py",        label="🗂️  Student Records")
            st.page_link("pages/edit_student.py",   label="✏️  Edit Student")
            st.page_link("pages/delete_student.py", label="🗑️  Delete Student")
            st.page_link("pages/analysis.py",       label="🧠  SHAP Analysis")
            st.page_link("pages/charts.py",         label="📈  Analytics")

        if role == "student":
            st.markdown('<div style="color:#64748B;font-size:0.72rem;letter-spacing:0.08em;padding:0.6rem 0.5rem 0.2rem;">STUDENT PORTAL</div>', unsafe_allow_html=True)
            st.page_link("pages/my_record.py",  label="📋  My Record")
            st.page_link("pages/my_analysis.py",label="🔍  My Analysis")

        st.markdown('<hr class="ss-divider" style="margin-top:auto;">', unsafe_allow_html=True)
        if st.button("Sign Out", key="signout_btn", width="stretch"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.switch_page("app.py")

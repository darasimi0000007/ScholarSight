import streamlit as st
from utils import inject_css, is_logged_in, restore_session

st.set_page_config(
    page_title="ScholarSight – Academic Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()

# Redirect if already logged in
restore_session()
if is_logged_in():
    st.switch_page("pages/dashboard.py")

st.markdown("""
<style>

.hero-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 4rem 2rem 2.5rem;
}

.hero-logo-wrap {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2.5rem;
    justify-content: center;
}

.hero-logo-icon {
    width: 64px; height: 64px;
    border-radius: 16px;
    object-fit: cover;
    box-shadow: 0 8px 32px #2563eb55;
}

.hero-logo-fallback {
    width: 64px; height: 64px;
    border-radius: 16px;
    background: linear-gradient(135deg, #2563EB, #0ea5e9);
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem;
    box-shadow: 0 8px 32px #2563eb55;
    flex-shrink: 0;
}

.hero-brand-name {
    font-size: 2rem; font-weight: 800;
    color: #F1F5F9; letter-spacing: -0.03em; line-height: 1;
}
.hero-brand-sub {
    font-size: 0.72rem; color: #64748B;
    letter-spacing: 0.12em; margin-top: 3px; text-transform: uppercase;
}

.hero-headline {
    font-size: clamp(2rem, 4.5vw, 3.4rem);
    font-weight: 800; color: #F1F5F9;
    line-height: 1.13; letter-spacing: -0.03em;
    max-width: 780px; margin: 0 auto 1.2rem;
}
.hero-headline .accent {
    background: linear-gradient(90deg, #2563EB 0%, #0ea5e9 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}

.hero-sub {
    font-size: 1rem; color: #94A3B8;
    max-width: 580px; margin: 0 auto 2.5rem; line-height: 1.75;
}

.trust-strip {
    display: flex; align-items: center; justify-content: center;
    gap: 2rem; flex-wrap: wrap; margin-top: 1.5rem;
}
.trust-item { display: flex; align-items: center; gap: 0.45rem; font-size: 0.8rem; color: #475569; }
.trust-dot { width: 5px; height: 5px; border-radius: 50%; background: #2563EB; flex-shrink: 0; }

.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #334155 30%, #334155 70%, transparent 100%);
    margin: 3.5rem auto; max-width: 600px; border: none;
}
.section-label {
    font-size: 0.7rem; font-weight: 700; color: #2563EB;
    letter-spacing: 0.15em; text-transform: uppercase; text-align: center; margin-bottom: 0.5rem;
}
.section-title {
    font-size: 1.55rem; font-weight: 800; color: #F1F5F9;
    letter-spacing: -0.02em; text-align: center; margin-bottom: 2.5rem;
}

.features-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem; max-width: 1060px; margin: 0 auto; padding: 0 1.5rem;
}
.feature-card {
    background: #1E293B; border: 1px solid #334155;
    border-radius: 14px; padding: 1.6rem 1.4rem;
    transition: border-color 0.2s, transform 0.2s;
}
.feature-card:hover { border-color: #2563EB55; transform: translateY(-2px); }
.feature-icon { font-size: 1.8rem; margin-bottom: 0.85rem; display: block; }
.feature-title { font-size: 0.95rem; font-weight: 700; color: #F1F5F9; margin-bottom: 0.45rem; }
.feature-desc { font-size: 0.84rem; color: #64748B; line-height: 1.65; }

.hiw-steps {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem; max-width: 900px; margin: 0 auto; padding: 0 1.5rem;
}
.hiw-step { display: flex; flex-direction: column; align-items: center; gap: 0.7rem; }
.hiw-step-num {
    width: 38px; height: 38px; border-radius: 50%;
    background: linear-gradient(135deg, #1E3A5F, #1E293B);
    border: 1px solid #2563EB55;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.78rem; font-weight: 700; color: #60a5fa; letter-spacing: 0.04em;
}
.hiw-step-title { font-size: 0.87rem; font-weight: 600; color: #CBD5E1; text-align: center; }
.hiw-step-desc { font-size: 0.79rem; color: #64748B; line-height: 1.55; text-align: center; }

.roles-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 1.5rem; max-width: 900px; margin: 0 auto; padding: 0 1.5rem;
}
.role-card { border-radius: 14px; padding: 1.8rem; }
.role-card-teacher {
    background: linear-gradient(135deg, #2d1d6e18 0%, #1E293B 100%);
    border: 1px solid #7c3aed44;
}
.role-card-student {
    background: linear-gradient(135deg, #0c3d5e18 0%, #1E293B 100%);
    border: 1px solid #0ea5e944;
}
.role-icon { font-size: 1.9rem; margin-bottom: 0.7rem; display: block; }
.role-name { font-size: 1rem; font-weight: 700; color: #F1F5F9; margin-bottom: 0.4rem; }
.role-desc { font-size: 0.84rem; color: #64748B; line-height: 1.65; margin-bottom: 1rem; }
.role-pill {
    display: inline-block; font-size: 0.72rem; font-weight: 600;
    padding: 3px 9px; border-radius: 20px; letter-spacing: 0.03em;
    margin-right: 5px; margin-bottom: 4px;
}
.pill-teacher { background: #7c3aed22; color: #a78bfa; border: 1px solid #7c3aed44; }
.pill-student { background: #0ea5e922; color: #38bdf8; border: 1px solid #0ea5e944; }

.landing-footer {
    text-align: center; color: #334155; font-size: 0.76rem;
    padding: 2.5rem 1rem; border-top: 1px solid #1E293B;
    letter-spacing: 0.02em; margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)


# ── HERO ──────────────────────────────────────────────────────────────────────
# Encode logo as base64 so it renders without static file serving config
import base64 as _b64, os as _os

def _logo_b64(path):
    try:
        with open(path, "rb") as f:
            return _b64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

_logo_paths = [
    "static/scholarsight-logo-only-png.png",
    "src/scholarsight-logo-only-png.png",
    "scholarsight-logo-only-png.png",
]
_logo_data = None
for _p in _logo_paths:
    _logo_data = _logo_b64(_p)
    if _logo_data:
        break

if _logo_data:
    _logo_html = f'<img class="hero-logo-icon" src="data:image/png;base64,{_logo_data}" alt="ScholarSight logo" />'
else:
    _logo_html = '<div class="hero-logo-fallback">🎓</div>'

st.markdown(f"""
<div class="hero-section">
    <div class="hero-logo-wrap">
        {_logo_html}
        <div>
            <div class="hero-brand-name">ScholarSight</div>
            <div class="hero-brand-sub">Academic Intelligence Platform</div>
        </div>
    </div>
    <h1 class="hero-headline">
        Predict academic outcomes.<br>
        <span class="accent">Understand every factor.</span>
    </h1>
    <p class="hero-sub">
        ScholarSight uses machine learning and SHAP explainability to help teachers identify
        at-risk students early — and help students understand what drives their performance.
    </p>
</div>
""", unsafe_allow_html=True)

_, col_cta1, col_gap, col_cta2, _ = st.columns([2, 1.2, 0.3, 1.2, 2])
with col_cta1:
    if st.button("Sign In  →", width="stretch", key="hero_signin"):
        st.switch_page("pages/login.py")
with col_cta2:
    if st.button("Create Account", width="stretch", key="hero_signup"):
        st.switch_page("pages/signup.py")

st.markdown("""
<div class="trust-strip">
    <div class="trust-item"><div class="trust-dot"></div>Gradient Boosting Classifier</div>
    <div class="trust-item"><div class="trust-dot"></div>SHAP Explainability</div>
    <div class="trust-item"><div class="trust-dot"></div>Role-based Access Control</div>
    <div class="trust-item"><div class="trust-dot"></div>Real-time Predictions</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ── FEATURES ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">What you get</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Built for real academic decisions</div>', unsafe_allow_html=True)

st.markdown("""
<div class="features-grid">
    <div class="feature-card">
        <span class="feature-icon">🔮</span>
        <div class="feature-title">Pass / Fail Prediction</div>
        <div class="feature-desc">Submit a student's academic profile and receive an instant Pass or Fail prediction powered by a trained Gradient Boosting model — no spreadsheets required.</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">🧠</span>
        <div class="feature-title">SHAP Explainability</div>
        <div class="feature-desc">Every prediction comes with a SHAP chart that breaks down which factors — absences, study time, family support — pushed the outcome in each direction.</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">🗂️</span>
        <div class="feature-title">Student Record Management</div>
        <div class="feature-desc">Teachers can view, search, edit, and delete student records. Editing any field automatically re-runs the prediction so records stay accurate.</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">📈</span>
        <div class="feature-title">Analytics Dashboard</div>
        <div class="feature-desc">Visual breakdowns of pass/fail rates, gender distribution, age spread, absence patterns, and study time vs. outcome — all in one place.</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">🔐</span>
        <div class="feature-title">Role-based Access</div>
        <div class="feature-desc">Teachers run predictions and manage records. Students view their own record and SHAP analysis. Each role sees only what is relevant to them.</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">⚡</span>
        <div class="feature-title">Instant Re-prediction</div>
        <div class="feature-desc">Update any field in a student record — absences, study time, health — and the model re-runs immediately, keeping every prediction fresh.</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── HOW IT WORKS ──────────────────────────────────────────────────────────────
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">The process</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">From data to insight in four steps</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hiw-steps">
    <div class="hiw-step">
        <div class="hiw-step-num">01</div>
        <div class="hiw-step-title">Create an account</div>
        <div class="hiw-step-desc">Sign up with your institution ID. The prefix (STU or TEA) sets your role automatically.</div>
    </div>
    <div class="hiw-step">
        <div class="hiw-step-num">02</div>
        <div class="hiw-step-title">Submit student data</div>
        <div class="hiw-step-desc">Teachers fill in a student profile — attendance, study time, family factors, and more.</div>
    </div>
    <div class="hiw-step">
        <div class="hiw-step-num">03</div>
        <div class="hiw-step-title">Receive a prediction</div>
        <div class="hiw-step-desc">The model returns a Pass or Fail result and stores the record for future reference.</div>
    </div>
    <div class="hiw-step">
        <div class="hiw-step-num">04</div>
        <div class="hiw-step-title">Explore the analysis</div>
        <div class="hiw-step-desc">A SHAP chart explains exactly which factors drove the outcome — for teachers and students alike.</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── WHO IS IT FOR ──────────────────────────────────────────────────────────────
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("<div class=\"section-label\">Who it's for</div>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Two roles, one platform</div>', unsafe_allow_html=True)

st.markdown("""
<div class="roles-grid">
    <div class="role-card role-card-teacher">
        <span class="role-icon">&#128105;&#8205;&#127979;</span>
        <div class="role-name">Teachers</div>
        <div class="role-desc">Run predictions for your students, manage their records, review analytics across your class, and edit or remove entries when circumstances change.</div>
        <span class="role-pill pill-teacher">Make Predictions</span>
        <span class="role-pill pill-teacher">Manage Records</span>
        <span class="role-pill pill-teacher">View Analytics</span>
        <span class="role-pill pill-teacher">SHAP Analysis</span>
    </div>
    <div class="role-card role-card-student">
        <span class="role-icon">&#129489;&#8205;&#127891;</span>
        <div class="role-name">Students</div>
        <div class="role-desc">View your own prediction result and SHAP analysis. Understand which habits and circumstances the model found most significant — and take action.</div>
        <span class="role-pill pill-student">View My Record</span>
        <span class="role-pill pill-student">My SHAP Analysis</span>
        <span class="role-pill pill-student">Performance Insights</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── BOTTOM CTA ────────────────────────────────────────────────────────────────
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding: 0 1.5rem 2rem;">
    <div style="font-size:1.45rem;font-weight:800;color:#F1F5F9;letter-spacing:-0.02em;margin-bottom:0.5rem;">
        Ready to get started?
    </div>
    <div style="font-size:0.9rem;color:#64748B;margin-bottom:2rem;">
        Sign in if you already have an account, or create one to begin.
    </div>
</div>
""", unsafe_allow_html=True)

_, col_b1, col_bgap, col_b2, _ = st.columns([2, 1.2, 0.3, 1.2, 2])
with col_b1:
    if st.button("Sign In  →", width="stretch", key="bottom_signin"):
        st.switch_page("pages/login.py")
with col_b2:
    if st.button("Create Account", width="stretch", key="bottom_signup"):
        st.switch_page("pages/signup.py")


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="landing-footer">
    ScholarSight v1.0 &nbsp;&middot;&nbsp; Powered by Gradient Boosting + SHAP &nbsp;&middot;&nbsp;
</div>
""", unsafe_allow_html=True)

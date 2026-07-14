import streamlit as st
from utils import inject_css, render_sidebar, require_student, get_user, api_get_shap_chart

st.set_page_config(page_title="ScholarSight – My Analysis", page_icon="🔍", layout="wide")
inject_css()
require_student()
render_sidebar()

user = get_user()
institution_id = user.get("institution_id", "")

st.markdown("""
<div class="page-header">
    <h2>🔍 My SHAP Analysis</h2>
    <p>Understand which academic factors influenced your performance prediction.</p>
</div>
""", unsafe_allow_html=True)

if not institution_id:
    st.markdown("""
    <div class="alert-error">
        ⚠️ No institution ID associated with your account.
    </div>
    """, unsafe_allow_html=True)
else:
    with st.spinner("Generating your SHAP analysis..."):
        shap_chart, err = api_get_shap_chart(institution_id)

    if err:
        st.markdown(f"""
        <div class="alert-error">
            ❌ Could not generate analysis: {err}
        </div>
        """, unsafe_allow_html=True)
    elif shap_chart:
        # st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Your Feature Importance Analysis")
        st.markdown("""
        <p style="color:#94A3B8;font-size:0.85rem;line-height:1.6;margin-bottom:1rem;">
            <strong style="color:#CBD5E1;">How to read this chart:</strong><br>
            • Longer bars = stronger influence on your prediction<br>
            • The further a bar extends, the more that feature affected your outcome
        </p>
        """, unsafe_allow_html=True)

        st.image(shap_chart, caption="SHAP Summary Plot - Your Feature Impact", use_container_width = True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="ss-card" style="text-align:center;padding:3rem 1rem;">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">📭</div>
            <div style="color:#94A3B8;margin-bottom:0.5rem;font-size:0.9rem;">No analysis available</div>
            <div style="color:#64748B;font-size:0.8rem;">Your SHAP analysis will appear here once your prediction is generated.</div>
        </div>""", unsafe_allow_html=True)

# ── Recommendations ───────────────────────────────────────────────────────────
st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="ss-card">
<h4 style="margin-top:0;">💡 What This Means For You</h4>
<p style="color:#94A3B8;font-size:0.85rem;line-height:1.7;">
    By understanding which factors influenced your prediction, you can:
    <ul style="color:#94A3B8;font-size:0.85rem;line-height:1.7;">
        <li>Identify your strengths and areas of excellence</li>
        <li>Recognize areas where you could improve</li>
        <li>Make informed decisions about your study habits and routines</li>
        <li>Work with your instructor on a personalized improvement plan</li>
    </ul>
</p>
<p style="color:#64748B;font-size:0.8rem;margin-top:1rem;">
    Remember: <strong>This prediction is a tool for support, not destiny.</strong>
    Your dedication and effort can always lead to improvement and success.
</p>
</div>
""", unsafe_allow_html=True)

# ── SHAP Education ───────────────────────────────────────────────────────────
st.markdown('<hr class="ss-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="ss-card" style="background:#1e3a5f22;border-color:#2563eb44;">
<h4 style="margin-top:0;color:#93c5fd;">📚 About SHAP Explanations</h4>
<p style="color:#94A3B8;font-size:0.85rem;line-height:1.7;">
    <strong style="color:#CBD5E1;">SHAP (SHapley Additive exPlanations)</strong> is a game-theoretic approach
    from cooperative game theory that explains the output of any machine learning model.
    It connects game theory and local explanations, ensuring that each feature gets an attribution
    value for a particular prediction. This makes your model predictions fully transparent
    and auditable.
</p>
</div>
""", unsafe_allow_html=True)

import streamlit as st
from theme import apply, nav

c, theme = apply("Prediction")
nav("Prediction", c, theme)

# ---------------------------------------------------------------- Hero (two columns)
left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.markdown(
        """
        <div class="reveal" style="padding-top:.5rem;">
            <div class="page-title">🔮 Customer Churn Prediction</div>
            <div class="hero-sub" style="margin-bottom:1.6rem;">Predict customer churn with a trained Machine Learning model, understand every prediction through SHAP explainability, and turn it into clear business recommendations — all in one place.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🚀 Start Prediction", type="primary"):
        st.session_state.show_prediction_form = True

with right:
    st.markdown(
        """
        <div class="card reveal" style="height:100%;">
            <div style="display:inline-block; background:rgba(37,99,235,.15); color:#3b82f6; font-weight:700; font-size:.8rem; padding:.3rem .8rem; border-radius:999px; margin-bottom:1rem;">⚡ Results in under 2 seconds</div>
            <h3>What you'll get</h3>
            <div class="factor"><span class="chk">✔</span>Churn probability &amp; risk level</div>
            <div class="factor"><span class="chk">✔</span>SHAP explanation of the key drivers</div>
            <div class="factor"><span class="chk">✔</span>Business retention recommendations</div>
            <div class="factor"><span class="chk">✔</span>AI-generated business summary</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------- Before You Begin
st.markdown(
    """
    <div class="section reveal" style="padding-bottom:1rem;">
        <div class="section-title">Before You Begin</div>
        <div class="section-sub">Have the customer's account information ready before starting — the model needs these details to score churn risk accurately.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="card reveal" style="display:flex; gap:1.4rem; align-items:center; margin-bottom:1.1rem;">
        <div style="width:54px;height:54px;border-radius:50%;flex:0 0 auto;display:flex;align-items:center;justify-content:center;font-size:1.4rem;font-weight:800;color:#fff;background:#2563eb;">1</div>
        <div style="flex:1;">
            <h3 style="font-size:1.45rem;margin:0 0 .4rem;">👤 Customer Profile</h3>
            <p style="font-size:1.05rem;">Gender, senior-citizen status, partner and dependents — the customer's basic demographics.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="card reveal" style="display:flex; gap:1.4rem; align-items:center; margin-bottom:1.1rem;">
        <div style="width:54px;height:54px;border-radius:50%;flex:0 0 auto;display:flex;align-items:center;justify-content:center;font-size:1.4rem;font-weight:800;color:#fff;background:#2563eb;">2</div>
        <div style="flex:1;">
            <h3 style="font-size:1.45rem;margin:0 0 .4rem;">📄 Account &amp; Contract</h3>
            <p style="font-size:1.05rem;">Tenure, contract type and paperless-billing preference — how long and how they're signed up.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="card reveal" style="display:flex; gap:1.4rem; align-items:center; margin-bottom:1.1rem;">
        <div style="width:54px;height:54px;border-radius:50%;flex:0 0 auto;display:flex;align-items:center;justify-content:center;font-size:1.4rem;font-weight:800;color:#fff;background:#2563eb;">3</div>
        <div style="flex:1;">
            <h3 style="font-size:1.45rem;margin:0 0 .4rem;">🌐 Internet &amp; Services</h3>
            <p style="font-size:1.05rem;">Internet type, online security, tech support and streaming add-ons the customer uses.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="card reveal" style="display:flex; gap:1.4rem; align-items:center; margin-bottom:.5rem;">
        <div style="width:54px;height:54px;border-radius:50%;flex:0 0 auto;display:flex;align-items:center;justify-content:center;font-size:1.4rem;font-weight:800;color:#fff;background:#2563eb;">4</div>
        <div style="flex:1;">
            <h3 style="font-size:1.45rem;margin:0 0 .4rem;">💳 Billing Information</h3>
            <p style="font-size:1.05rem;">Monthly charges, total charges and payment method — the customer's billing footprint.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- Prediction form (placeholder)
if st.session_state.get("show_prediction_form"):
    st.markdown(
        """
        <div class="section reveal">
            <div class="section-title">Customer Details</div>
            <div class="section-sub">Fill in the customer's information below to generate a prediction.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # TODO: build the actual input form here (tenure, contract, services, billing, etc.)
    st.info("Prediction form goes here — wire your model inputs into this block.")
import streamlit as st
import pandas as pd
from utils.explain import explain_prediction
from theme import apply, nav

c, theme = apply("Prediction")
nav("Prediction", c, theme)

# ---------------------------------------------------------------- Hero (two columns)
left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.markdown(
        """
        <div class="reveal" style="padding-top:.5rem;">
            <div class="page-title">Customer Churn Prediction</div>
            <div class="hero-sub" style="margin-bottom:1.6rem;">Predict customer churn with a trained Machine Learning model, understand every prediction through SHAP explainability, and turn it into clear business recommendations — all in one place.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Start Prediction", type="primary"):
        st.session_state.show_prediction_form = True
        st.session_state.scroll_to_form = True

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

# ---------------------------------------------------------------- Prediction Form
if st.session_state.get("show_prediction_form"):

    st.markdown('<div id="pred-form"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section reveal">
            <div class="section-title">Customer Information</div>
            <div class="section-sub">Complete the customer details below to generate a churn prediction.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # scroll down to the form once, right after "Start Prediction" is clicked
    if st.session_state.get("scroll_to_form"):
        st.components.v1.html(
            """
            <script>
                setTimeout(function() {
                    const el = window.parent.document.getElementById('pred-form');
                    if (el) el.scrollIntoView({behavior: 'smooth', block: 'start'});
                }, 150);
            </script>
            """,
            height=0,
        )
        st.session_state.scroll_to_form = False

    with st.form("prediction_form"):

        # ------------------------------------------------ Customer Profile
        with st.expander("👤 Customer Profile", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                gender = st.selectbox("Gender", ["Female", "Male"])
                senior = st.selectbox("Senior Citizen", ["No", "Yes"])
            with c2:
                partner = st.selectbox("Partner", ["No", "Yes"])
                dependents = st.selectbox("Dependents", ["No", "Yes"])

        # ------------------------------------------------ Account & Contract
        with st.expander("📄 Account & Contract", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                tenure = st.number_input("Customer Tenure (Months)", 0, 72, 12)
                contract = st.selectbox("Contract", ["Month-to-Month", "One-Year", "Two-Year"])
            with c2:
                paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
                payment = st.selectbox(
                    "Payment Method",
                    ["Electronic Check", "Mailed Check", "Bank Transfer (Automatic)", "Credit Card (Automatic)"],
                )

        # ------------------------------------------------ Internet & Services
        with st.expander("🌐 Internet & Services", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                phone = st.selectbox("Phone Service", ["Yes", "No"])
                multiple = st.selectbox("Multiple Lines", ["Yes", "No", "No Phone Service"])
                internet = st.selectbox("Internet Service", ["Fiber Optic", "DSL", "No"])
            with c2:
                security = st.selectbox("Online Security", ["Yes", "No", "No Internet Service"])
                backup = st.selectbox("Online Backup", ["Yes", "No", "No Internet Service"])
                protection = st.selectbox("Device Protection", ["Yes", "No", "No Internet Service"])
                support = st.selectbox("Tech Support", ["Yes", "No", "No Internet Service"])

        # ------------------------------------------------ Entertainment
        with st.expander("🎬 Entertainment Services", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                tv = st.selectbox("Streaming TV", ["Yes", "No", "No Internet Service"])
            with c2:
                movies = st.selectbox("Streaming Movies", ["Yes", "No", "No Internet Service"])

        # ------------------------------------------------ Billing
        with st.expander("💳 Billing Information", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                monthly = st.number_input("Monthly Charges ($)", 0.0, 200.0, 70.0)
            with c2:
                total = st.number_input("Total Charges ($)", 0.0, 10000.0, 1000.0)

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("Predict Customer Churn", use_container_width=True)

        if submitted:
            customer = pd.DataFrame([{

                "Gender": gender,
                "Senior Citizen": senior,
                "Partner": partner,
                "Dependents": dependents,

                "Tenure Months": tenure,

                "Phone Service": phone,
                "Multiple Lines": multiple,

                "Internet Service": internet,

                "Online Security": security,
                "Online Backup": backup,
                "Device Protection": protection,
                "Tech Support": support,

                "Streaming TV": tv,
                "Streaming Movies": movies,

                "Contract": contract,
                "Paperless Billing": paperless,
                "Payment Method": payment,

                "Monthly Charges": monthly,
                "Total Charges": total

            }])

            with st.spinner("Analyzing customer..."):

                result = explain_prediction(customer)

            st.session_state.prediction_result = result

# ------------------------------------------------ Prediction Result
if "prediction_result" in st.session_state:

    result = st.session_state.prediction_result
    prediction = result["prediction_result"]

    # color + emoji driven by risk level
    risk_meta = {
        "Low":       ("#22c55e", "🟢"),
        "Medium":    ("#f59e0b", "🟡"),
        "High":      ("#f97316", "🟠"),
        "Very High": ("#ef4444", "🔴"),
    }
    rl = prediction["risk_level"]
    color, dot = risk_meta.get(rl, ("#3b82f6", "⚪"))
    prob = prediction["probability"]

    st.markdown("<div id='result'></div>", unsafe_allow_html=True)

    # ---- verdict hero ----
    st.markdown(
        f"""
        <div class="result-card reveal">
            <div class="result-eyebrow">Prediction Result</div>
            <div style="display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:1.5rem;">
                <div>
                    <div class="result-verdict" style="color:{color};">{prediction["prediction"]}</div>
                    <div class="result-sub">Risk level: <b>{dot} {rl}</b></div>
                </div>
                <div style="text-align:right;">
                    <div class="result-prob" style="color:{color};">{prob:.2f}%</div>
                    <div class="result-prob-label">Churn probability</div>
                </div>
            </div>
            <div class="result-bar"><div style="width:{prob}%; background:{color};"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- factors ----
    risk = result["risk_factors"]
    protective = result["protective_factors"]

    if rl == "Low":
        primary_title,   primary_df,   primary_cls,   primary_mk   = "🛡️ Strongest Protective Factors", protective, "f-safe", "✔"
        secondary_title, secondary_df, secondary_cls, secondary_mk = "Potential Risk Factors",          risk,       "f-risk", "▲"
    else:
        primary_title,   primary_df,   primary_cls,   primary_mk   = "⚠️ Key Churn Drivers",   risk,       "f-risk", "▲"
        secondary_title, secondary_df, secondary_cls, secondary_mk = "🛡️ Key Retention Drivers", protective, "f-safe", "✔"

    def factor_rows(df, cls, mk):
        return "".join(
            f'<div class="f-row {cls}"><span class="mk">{mk}</span><span>{exp}</span></div>'
            for exp in df["Explanation"]
        )

    left, right = st.columns(2)
    with left:
        st.markdown(
            f'<div class="f-card reveal"><h4>{primary_title}</h4>{factor_rows(primary_df, primary_cls, primary_mk)}</div>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f'<div class="f-card reveal"><h4>{secondary_title}</h4>{factor_rows(secondary_df, secondary_cls, secondary_mk)}</div>',
            unsafe_allow_html=True,
        )

    # ---- recommendations ----
    rec_rows = "".join(
        f'<div class="rec-item"><span class="arw">→</span><span>{rec}</span></div>'
        for rec in result["recommendations"]
    )
    st.markdown(
        f'<div class="rec-card reveal"><h4>💡 Recommended Actions</h4>{rec_rows}</div>',
        unsafe_allow_html=True,
    )
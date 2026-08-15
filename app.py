import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🧠",
    layout="wide"
)

THEMES = {
    "dark": {
        "bg": "#0a0a0a", "title": "#f5f5f5", "sub": "#9ca3af",
        "brand": "#ffffff", "link": "#cbd5e1", "link_hover": "#ffffff",
        "sec_border": "#3f3f46", "sec_text": "#f5f5f5",
        "card_bg": "#141414", "card_border": "#262626",
        "icon": "☀️", "switch_to": "light",
        "footer_bg": "#13151b", "footer_bar": "#1b1e26",
    },
    "light": {
        "bg": "#ffffff", "title": "#0f172a", "sub": "#475569",
        "brand": "#0f172a", "link": "#475569", "link_hover": "#0f172a",
        "sec_border": "#cbd5e1", "sec_text": "#0f172a",
        "card_bg": "#f7f7f8", "card_border": "#e5e7eb",
        "icon": "🌙", "switch_to": "dark",
        "footer_bg": "#f1f2f4",
        "footer_bg": "#f1f2f4", "footer_bar": "#e7e9ee",
    },
}

# theme state
if "theme" in st.query_params:
    theme = st.query_params["theme"]
    st.session_state["theme"] = theme
else:
    theme = st.session_state.get("theme", "dark")
if theme not in THEMES:
    theme = "light"

c = THEMES[theme]

#  styling
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}
    .stApp {{ background: {c['bg']}; }}
    [data-testid="stHeaderActionElements"] {{ display: none; }}
    header[data-testid="stHeader"] {{ background: transparent; }}
    #MainMenu, footer {{ visibility: hidden; }}
    section[data-testid="stSidebar"] {{ display: none; }}
    .block-container {{ padding-top: 1.5rem; max-width: 1240px; }}

    /* ---- motion ---- */
    @keyframes fadeUp {{ from {{ opacity:0; transform: translateY(45px); }} to {{ opacity:1; transform:none; }} }}
    @keyframes slideIn {{ from {{ opacity:0; transform: translateX(40px); }} to {{ opacity:1; transform:none; }} }}
    @keyframes floaty {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-9px); }} }}
    @keyframes gradientMove {{ 0% {{ background-position:0% 50%; }} 50% {{ background-position:100% 50%; }} 100% {{ background-position:0% 50%; }} }}
    @keyframes flowDown {{ 0% {{ background-position:0 -120%; }} 100% {{ background-position:0 120%; }} }}
    @keyframes growBar {{ from {{ width:0; }} to {{ width:73.28%; }} }}

    .reveal {{ animation: fadeUp linear both; animation-timeline: view(); animation-range: entry 0% entry 55%; }}
    .float {{ animation: floaty 4s ease-in-out infinite; display:inline-block; }}
    @supports not (animation-timeline: view()) {{
        .reveal, .node, .pred-in {{ opacity:1 !important; transform:none !important; animation:none !important; }}
        .pred-bar > div {{ width:73.28% !important; animation:none !important; }}
    }}

    /* ---- top nav ---- */
    .navbar {{ display: flex; justify-content: space-between; align-items: center; padding: 1rem 0 4.5rem 0; }}
    .brand {{ font-size: 1.7rem; font-weight: 800; color: {c['brand']}; }}
    .navlinks {{ display: flex; align-items: center; }}
    .navlinks a {{ color: {c['link']}; margin-left: 2.2rem; text-decoration: none;
        font-size: 1.05rem; font-weight: 500; transition: color .2s; }}
    .navlinks a:hover {{ color: {c['link_hover']}; }}
    .navlinks a.active {{ color: {c['link_hover']}; }}
    .theme-toggle {{ font-size: 1.4rem; line-height: 1; cursor: pointer;
        text-decoration: none !important; user-select: none; }}

    /* ---- hero ---- */
    .hero-title {{ font-size: 4.6rem; line-height: 1.05; font-weight: 800;
        color: {c['title']}; letter-spacing: -1.5px; margin: 0 0 1.8rem 0; max-width: 900px; }}
    .hero-sub {{ font-size: 1.3rem; color: {c['sub']}; line-height: 1.6;
        max-width: 780px; margin-bottom: 2.8rem; }}

    /* ---- CTA buttons ---- */
    div.stButton > button {{ padding: .8rem 2.2rem; border-radius: 8px; font-size: 1.5rem; font-weight: 800; transition: all .2s; }}
    button[kind="primary"], button[data-testid="stBaseButton-primary"] {{
        background: #2563eb; color: #fff; border: none; }}
    button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover {{ background: #1d4ed8; }}
    button[kind="secondary"], button[data-testid="stBaseButton-secondary"] {{
        background: transparent; color: {c['sec_text']}; border: 1px solid {c['sec_border']}; }}
    button[kind="secondary"]:hover, button[data-testid="stBaseButton-secondary"]:hover {{ border-color: {c['title']}; }}

    /* ---- sections ---- */
    .section {{ padding: 3rem 0; }}
    .section-title {{ font-size: 2.6rem; font-weight: 800; color: {c['title']}; margin-bottom: .5rem; }}
    .section-sub {{ font-size: 1.15rem; color: {c['sub']}; margin-bottom: 2.6rem; max-width: 640px; }}

    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(235px,1fr)); gap: 1.4rem; }}
    .card {{ background: {c['card_bg']}; border: 1px solid {c['card_border']}; border-radius: 14px;
        padding: 1.9rem; transition: transform .25s ease, border-color .25s ease; }}
    .card:hover {{ transform: translateY(-6px); border-color: #2563eb; }}
    .card .ico {{ font-size: 2.2rem; margin-bottom: .9rem; }}
    .card h3 {{ color: {c['title']}; font-size: 1.2rem; font-weight: 700; margin: .1rem 0 .5rem; }}
    .card p {{ color: {c['sub']}; font-size: .98rem; line-height: 1.55; margin: 0; }}

    /* ---- architecture pipeline ---- */
    .arch {{ display: grid; grid-template-columns: 1.05fr .95fr; gap: 3rem; align-items: center; }}
    @media (max-width: 900px) {{ .arch {{ grid-template-columns: 1fr; }} }}

    .pipe {{ display: flex; flex-direction: column; align-items: stretch; }}
    .node {{ display: flex; align-items: center; gap: 1rem; background: {c['card_bg']};
        border: 1px solid {c['card_border']}; border-radius: 14px; padding: 1rem 1.3rem;
        animation: fadeUp linear both; animation-timeline: view(); }}
    .node:hover {{ border-color: #2563eb; }}
    .node .nico {{ font-size: 1.5rem; width: 2rem; text-align: center; }}
    .node .nlbl {{ font-weight: 600; color: {c['title']}; font-size: 1.05rem; }}
    .connector {{ width: 3px; height: 30px; margin: 0 auto; border-radius: 3px;
        background: linear-gradient(180deg, #2563eb, rgba(37,99,235,.15));
        background-size: 100% 220%; animation: flowDown 1.4s linear infinite; }}

    /* ---- sample prediction card ---- */
    .pred-in {{ animation: slideIn .8s cubic-bezier(.22,1,.36,1) both; }}
    .pred-card {{ background: {c['card_bg']}; border: 1px solid {c['card_border']}; border-radius: 18px;
        padding: 2rem; position: relative; overflow: hidden; box-shadow: 0 20px 45px rgba(0,0,0,.25); }}
    .pred-card::before {{ content:''; position:absolute; top:0; left:0; right:0; height:4px;
        background: linear-gradient(90deg, #ef4444, #f59e0b); }}
    .pred-eyebrow {{ font-size:.78rem; letter-spacing:1.5px; text-transform:uppercase;
        color:{c['sub']}; font-weight:600; }}
    .pred-status {{ display:inline-flex; align-items:center; gap:.45rem; background: rgba(239,68,68,.13);
        color:#ef4444; padding:.45rem .95rem; border-radius:999px; font-weight:700; margin:.9rem 0 .4rem; }}
    .pred-pct {{ font-size:3.4rem; font-weight:800; color:{c['title']}; line-height:1; margin-top:.3rem; }}
    .pred-bar {{ background:{c['card_border']}; height:10px; border-radius:999px; margin:1rem 0 1.6rem; overflow:hidden; }}
    .pred-bar > div {{ height:100%; width:73.28%; border-radius:999px;
        background: linear-gradient(90deg, #f59e0b, #ef4444);
        animation: growBar 1.3s cubic-bezier(.22,1,.36,1) both; }}
    .pred-h {{ color:{c['title']}; font-weight:700; font-size:.95rem; margin:.4rem 0 .7rem;
        letter-spacing:.3px; }}
    .factor {{ display:flex; align-items:center; gap:.65rem; color:{c['sub']}; padding:.32rem 0; font-size:1rem; }}
    .factor .dot {{ width:7px; height:7px; border-radius:50%; background:#2563eb; flex:0 0 auto; }}
    .rec-box {{ background: rgba(37,99,235,.1); border:1px solid rgba(37,99,235,.3); border-radius:12px;
        padding:1rem 1.2rem; margin-top:1.4rem; }}
    .rec-box .rec-h {{ color:#3b82f6; font-weight:700; font-size:.85rem; text-transform:uppercase;
        letter-spacing:.5px; margin-bottom:.35rem; }}
    .rec-box .rec-t {{ color:{c['title']}; font-size:1rem; line-height:1.5; }}

    /* ---- cta band ---- */
    .cta-band {{ position: relative; overflow: hidden; margin: 4rem 0 0; padding: 3rem 3.5rem;
        border-radius: 22px; display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: center;
        background: linear-gradient(135deg, #6366f1 0%, #2563eb 52%, #1e3a8a 100%);
        background-size: 180% 180%; animation: gradientMove 10s ease infinite; }}
    .cta-band::before {{ content:''; position:absolute; top:-45%; left:-12%; width:65%; height:170%;
        background: radial-gradient(circle, rgba(255,255,255,.20), transparent 60%); pointer-events:none; }}
    @media (max-width: 800px) {{ .cta-band {{ grid-template-columns: 1fr; text-align: center; }} }}
    .cta-visual {{ display: flex; justify-content: center; align-items: center; }}
    .cta-visual svg {{ width: 100%; max-width: 380px; }}
    .cta-svg {{ animation: floaty 5s ease-in-out infinite; }}
    .chart-line {{ stroke-dasharray: 480; stroke-dashoffset: 480; animation: drawLine 2.2s ease .3s forwards; }}
    @keyframes drawLine {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes ringPulse {{ 0% {{ opacity:.85; r:7; }} 100% {{ opacity:0; r:30; }} }}
    .pulse-ring {{ animation: ringPulse 2.2s ease-out infinite; }}
    .cta-band h2 {{ position:relative; color: #fff; font-size: 2.2rem; font-weight: 800; margin-bottom: .6rem; }}
    .cta-band p {{ position:relative; color: #dbeafe; font-size: 1.1rem; margin-bottom: 1.7rem; }}
    .cta-band a {{ position:relative; display:inline-block; background: #fff; color: #1e3a8a;
        padding: .85rem 2.4rem; border-radius: 10px; font-weight: 700; text-decoration: none;
        font-size: 1.05rem; box-shadow: 0 8px 20px rgba(0,0,0,.2); transition: transform .2s; }}
    .cta-band a:hover {{ transform: translateY(-2px); }}

    /* ---- footer ---- */
    .footer-wrap {{ background: {c['footer_bg']}; border: 1px solid {c['card_border']};
        border-radius: 20px; margin-top: 4rem;  overflow: hidden; }}
    .footer-main {{ padding: 2.8rem 2rem 2.4rem; text-align: center; }}
    .footer-brand {{ display: flex; align-items: center; justify-content: center; gap: .65rem; }}
    .footer-logo {{ width: 36px; height: 36px; border-radius: 9px; display: flex; align-items: center;
        justify-content: center; font-size: 1.15rem; background: linear-gradient(135deg, #3b82f6, #2563eb); }}
    .footer-brand .name {{ font-size: 1.45rem; font-weight: 800; color: {c['title']}; }}
    .footer-tag {{ text-align: center; color: {c['sub']}; max-width: 540px; margin: 1rem auto 0;
        line-height: 1.6; font-size: .98rem; }}
    .footer-nav {{ display: flex; justify-content: center; flex-wrap: wrap; gap: 2rem; margin: 1.8rem 0 0; }}
    .footer-nav a {{ color: {c['sub']}; text-decoration: none; font-weight: 500; font-size: 1rem; transition: color .2s; }}
    .footer-nav a:hover {{ color: {c['title']}; }}
    .socials {{ display: flex; justify-content: center; gap: .7rem; margin-top: 1.6rem; }}
    .socials a {{ width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center;
        justify-content: center; color: {c['sub']}; background: rgba(127,127,127,.13);
        transition: transform .2s ease, background .2s ease, color .2s ease; }}
    .socials a:hover {{ transform: translateY(-3px); background: #2563eb; color: #fff; }}
    .footer-bottom {{ background: {c['footer_bar']}; padding: 1.1rem 2.5rem; display: flex;
        justify-content: space-between; flex-wrap: wrap; gap: .8rem; align-items: center; }}
    .footer-bottom .left a {{ color: {c['sub']}; text-decoration: none; font-size: .9rem; margin-right: 1.6rem; }}
    .footer-bottom .left a:hover {{ color: {c['title']}; }}
    .footer-bottom .right {{ color: {c['sub']}; font-size: .9rem; }}
    .footer-bottom .right a {{ color: #3b82f6; text-decoration: none; font-weight: 600; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# top nav
st.markdown(
    f"""
    <div class="navbar">
        <div class="brand">ChurnAI</div>
        <div class="navlinks">
            <a href="/?theme={theme}" class="active" target="_self">Home</a>
            <a href="/Prediction?theme={theme}" target="_self">Prediction</a>
            <a href="/Dashboard?theme={theme}" target="_self">Dashboard</a>
            <a href="/How_It_Was_Built?theme={theme}" target="_self">How It Was Built</a>
            <a href="/?theme={c['switch_to']}" class="theme-toggle" target="_self" title="Switch theme">{c['icon']}</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# hero
st.markdown('<div class="hero-title">AI-Powered Customer Churn Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Predict customer churn using Machine Learning, understand every '
    'prediction using SHAP, receive business recommendations, and generate AI-powered '
    'business summaries.</div>',
    unsafe_allow_html=True,
)

#  CTAs
col1, col2, _ = st.columns([1.1, 1.3, 4])
with col1:
    if st.button("Predict Customer", type="primary", use_container_width=True):
        st.switch_page("pages/1_Prediction.py")
with col2:
    if st.button("Business Dashboard", type="secondary", use_container_width=True):
        st.switch_page("pages/2_Dashboard.py")

#  features
st.markdown(
    f"""
    <div class="section reveal">
            <div class="section-title">Everything you need to predict and understand churn</div>
            <div class="section-sub"> From customer information to explainable predictions and business-ready insights.</div>
            <div class="cards">
                <div class="card">
                    <div class="ico float">🔮</div>
                    <h3>Customer Churn Prediction</h3>
                    <p> Predict whether a customer is likely to churn using a trained machine learning pipeline with probability and risk level.</p>
                </div>
                <div class="card">
                    <div class="ico float">🧠</div>
                    <h3>Explainable AI (SHAP)</h3>
                    <p> Understand why each prediction was made through SHAP feature contributions, highlighting both churn risks and protective factors.</p>
                </div>
                <div class="card">
                    <div class="ico float">💡</div>
                    <h3>Retention Recommendations</h3>
                    <p>Receive personalized business recommendations based on the customer's strongest churn drivers.</p>
                </div>
                <div class="card">
                    <div class="ico float">📝</div>
                    <h3>AI Business Summary</h3>
                    <p>Generate an AI-powered executive summary that converts technical model outputs into business-friendly insights.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)

# architecture + sample prediction
st.markdown(
    """
    <div class="section reveal">
        <div class="section-title">How a prediction flows</div>
        <div class="section-sub">Every customer runs through the same pipeline — data in, decision out.</div>
        <div class="arch">
            <div class="pipe">
                <div class="node" style="animation-range: entry 2% entry 22%;"><span class="nico">📥</span><span class="nlbl">Customer Data</span></div>
                <div class="connector"></div>
                <div class="node" style="animation-range: entry 8% entry 28%;"><span class="nico">🤖</span><span class="nlbl">Machine Learning Model</span></div>
                <div class="connector"></div>
                <div class="node" style="animation-range: entry 14% entry 34%;"><span class="nico">🎯</span><span class="nlbl">Prediction + Probability</span></div>
                <div class="connector"></div>
                <div class="node" style="animation-range: entry 20% entry 40%;"><span class="nico">🧠</span><span class="nlbl">SHAP Explanation</span></div>
                <div class="connector"></div>
                <div class="node" style="animation-range: entry 26% entry 46%;"><span class="nico">💡</span><span class="nlbl">Business Recommendation</span></div>
                <div class="connector"></div>
                <div class="node" style="animation-range: entry 32% entry 52%;"><span class="nico">📝</span><span class="nlbl">AI Summary</span></div>
            </div>
            <div class="pred-in">
                <div class="pred-card">
                    <div class="pred-eyebrow">Sample Prediction</div>
                    <div class="pred-status">⚠️ Likely to Churn</div>
                    <div class="pred-pct">68.72%</div>
                    <div class="pred-bar"><div></div></div>
                    <div class="pred-h">Top Risk Factors</div>
                    <div class="factor"><span class="dot"></span>Customer Tenure</div>
                    <div class="factor"><span class="dot"></span>Internet Service</div>
                    <div class="factor"><span class="dot"></span>Contract</div>
                    <div class="rec-box">
                        <div class="rec-h">Recommendation</div>
                        <div class="rec-t">Monitor this customer closely and consider a targeted retention offer.
                        Consider personalized retention offers tailored to the customer's household needs. 
                        Review service quality and pricing for the customer's Fiber Optic plan. </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# cta band
st.markdown(
    f"""
    <div class="cta-band reveal">
        <div class="cta-visual">
            <svg class="cta-svg" viewBox="0 0 300 240" xmlns="http://www.w3.org/2000/svg" fill="none">
                <rect x="24" y="60" width="252" height="150" rx="18" fill="rgba(255,255,255,.10)" stroke="rgba(255,255,255,.45)" stroke-width="1.5"/>
                <line x1="24" y1="112" x2="276" y2="112" stroke="rgba(255,255,255,.12)" stroke-width="1"/>
                <line x1="24" y1="162" x2="276" y2="162" stroke="rgba(255,255,255,.12)" stroke-width="1"/>
                <rect x="62" y="150" width="20" height="44" rx="5" fill="rgba(255,255,255,.22)"/>
                <rect x="100" y="132" width="20" height="62" rx="5" fill="rgba(255,255,255,.28)"/>
                <rect x="138" y="140" width="20" height="54" rx="5" fill="rgba(255,255,255,.24)"/>
                <rect x="176" y="112" width="20" height="82" rx="5" fill="rgba(255,255,255,.30)"/>
                <rect x="214" y="92" width="20" height="102" rx="5" fill="rgba(255,255,255,.36)"/>
                <polyline class="chart-line" points="72,150 110,128 148,134 186,102 224,80" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
                <circle class="pulse-ring" cx="224" cy="80" r="7" fill="none" stroke="#ffffff" stroke-width="2"/>
                <circle cx="224" cy="80" r="7" fill="#ffffff"/>
                <circle cx="52" cy="46" r="26" fill="rgba(255,255,255,.18)" stroke="#ffffff" stroke-width="1.5"/>
                <path d="M41 46 l7 8 l15 -17" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                <rect x="228" y="34" width="52" height="26" rx="13" fill="rgba(255,255,255,.22)"/>
                <path d="M254 54 V44 M249 49 l5 -5 l5 5" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            </svg>
        </div>
        <div class="cta-right">
            <h2>Ready to see who's about to churn?</h2>
            <p>Start with a single prediction or explore the full business dashboard.</p>
            <a href="/Prediction?theme={theme}" target="_self">Predict a Customer</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# footer
st.markdown(
    f"""
    <div class="footer-wrap reveal">
        <div class="footer-main">
            <div class="footer-brand">
                <div class="footer-logo">📈</div>
                <div class="name">ChurnAI</div>
            </div>
            <div class="footer-tag">Predict customer churn, understand every prediction, and make smarter retention decisions with explainable AI.</div>
            <div class="footer-nav">
                <a href="/?theme={theme}" target="_self">Home</a>
                <a href="/Prediction?theme={theme}" target="_self">Prediction</a>
                <a href="/Dashboard?theme={theme}" target="_self">Dashboard</a>
                <a href="/How_It_Was_Built?theme={theme}" target="_self">How It Was Built</a>
            </div>
            <div class="socials">
                <a href="https://github.com/dilnazgrewal" target="_blank" title="GitHub"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 .5A11.5 11.5 0 0 0 .5 12a11.5 11.5 0 0 0 7.86 10.92c.58.11.79-.25.79-.55 0-.28-.01-1-.02-1.97-3.2.7-3.87-1.54-3.87-1.54-.52-1.33-1.28-1.68-1.28-1.68-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.03 1.76 2.7 1.25 3.35.96.1-.74.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.68 0-1.26.45-2.28 1.18-3.08-.12-.29-.51-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.16-1.18 3.16-1.18.63 1.59.24 2.76.12 3.05.74.8 1.18 1.82 1.18 3.08 0 4.41-2.69 5.39-5.25 5.67.41.36.78 1.06.78 2.13 0 1.54-.01 2.78-.01 3.16 0 .31.21.67.8.55A11.5 11.5 0 0 0 23.5 12 11.5 11.5 0 0 0 12 .5Z"/></svg></a>
                <a href="https://www.linkedin.com/in/dilnazgrewal05/" target="_blank" title="LinkedIn"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg></a>
                <a href="#" target="_blank" title="X"><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M18.9 1.5h3.68l-8.04 9.19L24 22.5h-7.4l-5.8-7.58-6.64 7.58H.48l8.6-9.83L0 1.5h7.59l5.24 6.93L18.9 1.5zm-1.29 18.8h2.04L6.48 3.6H4.29l13.32 16.7z"/></svg></a>
            </div>
        </div>
        <div class="footer-bottom">
            <div class="left"><a href="#">Terms of Use</a><a href="#">Privacy Policy</a></div>
            <div class="right">© 2026 ChurnAI · Designed by <a href="https://www.linkedin.com/in/dilnazgrewal05/" target="_blank">Dilnaz Grewal</a></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


import streamlit as st

THEMES = {
    "dark": {
        "bg": "#0a0a0a", "title": "#f5f5f5", "sub": "#9ca3af",
        "brand": "#ffffff", "link": "#cbd5e1", "link_hover": "#ffffff",
        "sec_border": "#3f3f46", "sec_text": "#f5f5f5",
        "card_bg": "#141414", "card_border": "#262626",
        "footer_bg": "#13151b", "footer_bar": "#1b1e26",
        "icon": "☀️", "switch_to": "light",
    },
    "light": {
        "bg": "#ffffff", "title": "#0f172a", "sub": "#475569",
        "brand": "#0f172a", "link": "#475569", "link_hover": "#0f172a",
        "sec_border": "#cbd5e1", "sec_text": "#0f172a",
        "card_bg": "#f7f7f8", "card_border": "#e5e7eb",
        "footer_bg": "#f1f2f4", "footer_bar": "#e7e9ee",
        "icon": "🌙", "switch_to": "dark",
    },
}


def apply(page_title=""):
    """Call first on every page. Sets config, reads the theme, injects CSS.
    Returns (c, theme)."""
    st.set_page_config(
        page_title=page_title or "ChurnAI",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    # theme is a global preference: a ?theme= param (from the toggle) updates it,
    # otherwise we keep whatever the session already chose (survives navigation).
    if "theme" in st.query_params:
        theme = st.query_params["theme"]
        st.session_state["theme"] = theme
    else:
        theme = st.session_state.get("theme", "dark")
    if theme not in THEMES:
        theme = "dark"
    c = THEMES[theme]

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}

        .stApp {{ background: {c['bg']}; color: {c['title']}; }}
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

        .reveal {{ animation: fadeUp linear both; animation-timeline: view(); animation-range: entry 0% entry 55%; }}
        .float {{ animation: floaty 4s ease-in-out infinite; display:inline-block; }}
        @supports not (animation-timeline: view()) {{
            .reveal, .node {{ opacity:1 !important; transform:none !important; animation:none !important; }}
        }}

        /* ---- top nav ---- */
        .navbar {{ display: flex; justify-content: space-between; align-items: center; padding: 1rem 0 4rem 0; }}
        .brand {{ font-size: 1.7rem; font-weight: 800; color: {c['brand']}; }}
        .navlinks {{ display: flex; align-items: center; }}
        .navlinks a {{ color: {c['link']}; margin-left: 2.2rem; text-decoration: none;
            font-size: 1.05rem; font-weight: 500; transition: color .2s; }}
        .navlinks a:hover {{ color: {c['link_hover']}; }}
        .navlinks a.active {{ color: {c['link_hover']}; }}
        .theme-toggle {{ font-size: 1.4rem; line-height: 1; cursor: pointer;
            text-decoration: none !important; user-select: none; }}

        /* ---- hero / sections ---- */
        .hero-title {{ font-size: 4.6rem; line-height: 1.05; font-weight: 800;
            color: {c['title']}; letter-spacing: -1.5px; margin: 0 0 1.8rem 0; max-width: 900px; }}
        .page-title {{ font-size: 3.2rem; line-height: 1.08; font-weight: 800;
            color: {c['title']}; letter-spacing: -1px; margin: 0 0 1rem 0; }}
        .hero-sub {{ font-size: 1.3rem; color: {c['sub']}; line-height: 1.6;
            max-width: 780px; margin-bottom: 2.8rem; }}
        .section {{ padding: 2rem 0; }}
        .section-title {{ font-size: 2.6rem; font-weight: 800; color: {c['title']}; margin-bottom: .5rem; }}
        .section-sub {{ font-size: 1.15rem; color: {c['sub']}; margin-bottom: 2rem; max-width: 660px; }}

        /* ---- CTA buttons ---- */
        div.stButton > button {{ padding: .8rem 2.2rem; border-radius: 8px;
            font-size: .95rem; font-weight: 600; transition: all .2s; }}
        button[kind="primary"], button[data-testid="stBaseButton-primary"] {{
            background: #2563eb; color: #fff; border: none; }}
        button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover {{ background: #1d4ed8; }}
        button[kind="secondary"], button[data-testid="stBaseButton-secondary"] {{
            background: transparent; color: {c['sec_text']}; border: 1px solid {c['sec_border']}; }}
        button[kind="secondary"]:hover, button[data-testid="stBaseButton-secondary"]:hover {{ border-color: {c['title']}; }}

        /* ---- cards ---- */
        .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(235px,1fr)); gap: 1.4rem; }}
        .card {{ background: {c['card_bg']}; border: 1px solid {c['card_border']}; border-radius: 14px;
            padding: 1.8rem; transition: transform .25s ease, border-color .25s ease; height: 100%; }}
        .card:hover {{ transform: translateY(-6px); border-color: #2563eb; }}
        .card .ico {{ font-size: 2.2rem; margin-bottom: .9rem; }}
        .card h3 {{ color: {c['title']}; font-size: 1.15rem; font-weight: 700; margin: .1rem 0 .6rem; }}
        .card p {{ color: {c['sub']}; font-size: .96rem; line-height: 1.55; margin: 0; }}

        /* ---- list rows (reused for info panels) ---- */
        .factor {{ display:flex; align-items:center; gap:.65rem; color:{c['sub']};
            padding:.4rem 0; font-size:1rem; }}
        .factor .dot {{ width:7px; height:7px; border-radius:50%; background:#2563eb; flex:0 0 auto; }}
        .factor .chk {{ color:#22c55e; font-weight:700; flex:0 0 auto; }}
        .big-num {{ font-size:1.7rem; font-weight:800; color:{c['title']}; margin:.3rem 0 1rem; }}

        /* ---- requirement tiles ---- */
        .req-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:1.3rem; }}
        @media (max-width:700px) {{ .req-grid {{ grid-template-columns:1fr; }} }}
        .req-tile {{ display:flex; gap:1rem; align-items:flex-start; background:rgba(127,127,127,.06);
            border:1px solid {c['card_border']}; border-radius:12px; padding:1.15rem 1.25rem;
            transition:transform .2s ease, border-color .2s ease; }}
        .req-tile:hover {{ transform:translateY(-3px); border-color:#2563eb; }}
        .req-ico {{ width:46px; height:46px; border-radius:12px; flex:0 0 auto; display:flex;
            align-items:center; justify-content:center; font-size:1.45rem; background:rgba(37,99,235,.14); }}
        .req-tile .rt-title {{ color:{c['title']}; font-weight:700; font-size:1.08rem; margin-bottom:.2rem; }}
        .req-tile .rt-sub {{ color:{c['sub']}; font-size:.92rem; line-height:1.5; }}

        /* ---- form widgets (force widgets to follow the theme, not the dark config) ---- */
        .stApp {{ --background-color:{c['bg']}; --secondary-background-color:{c['card_bg']}; --text-color:{c['title']}; }}
        [data-testid="stForm"] {{ background:{c['card_bg']}; border:1px solid {c['card_border']};
            border-radius:16px; padding:1.6rem 1.6rem .8rem; }}
        [data-testid="stWidgetLabel"] p, [data-testid="stForm"] label p {{
            color:{c['title']} !important; font-weight:600; font-size:.92rem; }}

        /* text, number & select fields — force to theme via stable testids */
        [data-testid="stSelectbox"] div, [data-testid="stNumberInput"] div, [data-testid="stTextInput"] div {{
            background-color:{c['bg']} !important; border-color:{c['card_border']} !important; }}
        [data-testid="stSelectbox"] *, [data-testid="stNumberInput"] *, [data-testid="stTextInput"] * {{
            color:{c['title']} !important; }}
        [data-testid="stSelectbox"] input, [data-testid="stNumberInput"] input, [data-testid="stTextInput"] input {{
            background:transparent !important; color:{c['title']} !important; }}
        [data-testid="stSelectbox"] svg, [data-testid="stNumberInput"] svg {{ fill:{c['sub']} !important; }}
        [data-testid="stWidgetLabel"] p {{ color:{c['title']} !important; font-size:1.05rem !important; font-weight:600 !important; }}

        /* number-input stepper buttons (override the generic div rule above) */
        [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] {{
            background:{c['card_bg']} !important; border-color:{c['card_border']} !important; }}
        [data-testid="stNumberInputStepUp"] svg, [data-testid="stNumberInputStepDown"] svg {{
            fill:{c['title']} !important; }}
        [data-testid="stNumberInputStepUp"]:hover, [data-testid="stNumberInputStepDown"]:hover {{
            background:rgba(37,99,235,.18) !important; }}

        /* dropdown popover (rendered outside the widget) */
        [data-baseweb="popover"] [role="listbox"] {{ background:{c['card_bg']} !important; border:1px solid {c['card_border']}; }}
        [data-baseweb="popover"] li {{ color:{c['title']} !important; background:{c['card_bg']} !important; }}
        [data-baseweb="popover"] li:hover {{ background:rgba(37,99,235,.15) !important; }}

        /* expanders (fix dark header bar) */
        [data-testid="stExpander"] {{ border:1px solid {c['card_border']} !important; border-radius:12px !important;
            overflow:hidden; margin-bottom:.9rem; }}
        [data-testid="stExpander"] details {{ background:{c['card_bg']} !important; }}
        [data-testid="stExpander"] summary {{ background:{c['card_bg']} !important; color:{c['title']} !important;
            font-weight:700 !important; font-size:1.2rem !important; padding:.4rem 0 !important; }}
        [data-testid="stExpander"] summary * {{ color:{c['title']} !important; }}
        [data-testid="stExpander"] summary:hover, [data-testid="stExpander"] summary:hover * {{ color:#2563eb !important; }}

        /* submit button */
        [data-testid="stFormSubmitButton"] button {{ background:#2563eb !important; color:#fff !important;
            border:none !important; font-weight:700 !important; padding:.85rem 2rem !important;
            border-radius:8px !important; transition:background .2s; }}
        [data-testid="stFormSubmitButton"] button:hover {{ background:#1d4ed8 !important; }}

        /* ---- prediction result ---- */
        .result-eyebrow {{ font-size:.78rem; letter-spacing:1.5px; text-transform:uppercase; color:{c['sub']}; font-weight:600; }}
        .result-card {{ background:{c['card_bg']}; border:1px solid {c['card_border']}; border-radius:18px;
            padding:2rem; position:relative; overflow:hidden; box-shadow:0 18px 40px rgba(0,0,0,.22); margin-bottom:1.4rem; }}
        .result-verdict {{ font-size:2.3rem; font-weight:800; line-height:1.1; margin:.5rem 0 .35rem; }}
        .result-sub {{ color:{c['sub']}; font-size:1.02rem; }}
        .result-sub b {{ color:{c['title']}; }}
        .result-prob {{ font-size:3.1rem; font-weight:800; line-height:1; }}
        .result-prob-label {{ color:{c['sub']}; font-size:.82rem; text-transform:uppercase; letter-spacing:.6px; margin-top:.25rem; }}
        .result-bar {{ background:{c['card_border']}; height:12px; border-radius:999px; margin-top:1.7rem; overflow:hidden; }}
        .result-bar > div {{ height:100%; border-radius:999px; }}

        .f-card {{ background:{c['card_bg']}; border:1px solid {c['card_border']}; border-radius:16px; padding:1.6rem; height:100%; }}
        .f-card h4 {{ font-size:1.12rem; font-weight:700; color:{c['title']}; margin:0 0 1rem; }}
        .f-row {{ display:flex; gap:.7rem; align-items:flex-start; padding:.6rem 0; color:{c['sub']};
            font-size:.98rem; line-height:1.5; border-top:1px solid {c['card_border']}; }}
        .f-row:first-of-type {{ border-top:none; padding-top:0; }}
        .f-row .mk {{ flex:0 0 auto; font-weight:800; margin-top:.05rem; }}
        .f-risk .mk {{ color:#ef4444; }}
        .f-safe .mk {{ color:#22c55e; }}

        .rec-card {{ background:rgba(37,99,235,.08); border:1px solid rgba(37,99,235,.28); border-radius:16px;
            padding:1.6rem 1.8rem; margin-top:1.4rem; }}
        .rec-card h4 {{ font-size:1.15rem; font-weight:700; color:{c['title']}; margin:0 0 1rem; }}
        .rec-item {{ display:flex; gap:.8rem; align-items:flex-start; padding:.5rem 0;
            color:{c['title']}; font-size:1rem; line-height:1.55; }}
        .rec-item .arw {{ color:#3b82f6; font-weight:800; flex:0 0 auto; }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    return c, theme


def nav(active, c, theme):
    """Render the shared top navbar. `active` is the current page label."""
    def cls(label):
        return ' class="active"' if label == active else ""
    # toggle stays on the current page (flips theme in place, no jump to Home)
    paths = {"Home": "/", "Prediction": "/Prediction", "Dashboard": "/Dashboard", "About": "/About"}
    here = paths.get(active, "/")
    st.markdown(
        f"""
        <div class="navbar">
            <div class="brand">ChurnAI</div>
            <div class="navlinks">
                <a href="/?theme={theme}"{cls('Home')} target="_self">Home</a>
                <a href="/Prediction?theme={theme}"{cls('Prediction')} target="_self">Prediction</a>
                <a href="/Dashboard?theme={theme}"{cls('Dashboard')} target="_self">Dashboard</a>
                <a href="/About?theme={theme}"{cls('About')} target="_self">About</a>
                <a href="{here}?theme={c['switch_to']}" class="theme-toggle" target="_self" title="Switch theme">{c['icon']}</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
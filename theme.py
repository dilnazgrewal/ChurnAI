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
        page_title=page_title or "AI Churn Intelligence",
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
            <div class="brand">AI Churn Intelligence</div>
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
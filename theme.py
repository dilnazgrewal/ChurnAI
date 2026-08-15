import streamlit as st
import json

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
        layout="wide"
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
        [data-testid="stStatusWidget"] {{ display: none; }}
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

        /* ---- step cards (Before You Begin) ---- */
        @keyframes badgeFloat {{ 0%,100% {{ transform:translateY(0) rotate(0deg); }} 50% {{ transform:translateY(-5px) rotate(-4deg); }} }}
        @keyframes cascadeIn {{ from {{ opacity:0; transform:translateY(28px); }} to {{ opacity:1; transform:none; }} }}
        .step-card {{ display:flex; gap:1.3rem; align-items:center; background:{c['card_bg']};
            border:1px solid {c['card_border']}; border-radius:16px; padding:1.4rem 1.6rem; margin-bottom:1rem;
            position:relative; overflow:hidden; cursor:pointer;
            transition:transform .28s cubic-bezier(.22,1,.36,1), box-shadow .28s ease, border-color .28s ease;
            animation:cascadeIn .7s cubic-bezier(.22,1,.36,1) both, fadeUp linear both;
            animation-timeline:auto, view(); animation-range:auto, entry 0% entry 60%; }}
        .step-card::before {{ content:''; position:absolute; inset:0; opacity:0; border-radius:16px;
            background:radial-gradient(500px circle at var(--mx,50%) var(--my,50%), rgba(37,99,235,.14), transparent 55%);
            transition:opacity .3s ease; pointer-events:none; }}
        .step-card:hover {{ transform:translateY(-7px) scale(1.012); border-color:#2563eb;
            box-shadow:0 18px 34px rgba(37,99,235,.18); }}
        .step-card:hover::before {{ opacity:1; }}
        .step-card:active {{ transform:translateY(-3px) scale(.995); }}
        .step-badge {{ width:56px; height:56px; border-radius:50%; flex:0 0 auto; display:flex; align-items:center;
            justify-content:center; font-size:1.5rem; font-weight:800; color:#fff;
            background:linear-gradient(135deg,#3b82f6,#1d4ed8); box-shadow:0 8px 18px rgba(37,99,235,.35);
            animation:badgeFloat 3.4s ease-in-out infinite; }}
        .step-card .arrow {{ position:absolute; right:1.6rem; top:50%; transform:translate(8px,-50%); opacity:0;
            color:#3b82f6; font-size:1.3rem; font-weight:800; transition:all .28s ease; }}
        .step-card:hover .arrow {{ opacity:1; transform:translate(0,-50%); }}

        /* ---- pulsing primary CTA ---- */
        @keyframes pulseGlow {{ 0%,100% {{ box-shadow:0 0 0 0 rgba(37,99,235,.45); }} 50% {{ box-shadow:0 0 0 10px rgba(37,99,235,0); }} }}
        div.stButton > button[kind="primary"] {{ animation:pulseGlow 2.2s ease-in-out infinite; }}
        div.stButton > button[kind="primary"]:active {{ transform:scale(.97); }}
        div.stButton > button {{ transition:transform .15s ease, box-shadow .2s ease; }}
        div.stButton > button:active {{ transform:scale(.97); }}

        /* ---- dashboard: KPI tiles + chart panels ---- */
        .kpi-tile {{ background:{c['card_bg']}; border:1px solid {c['card_border']}; border-radius:16px;
            padding:1.5rem 1.4rem; text-align:center; transition:transform .25s ease, border-color .25s ease, box-shadow .25s ease; }}
        .kpi-tile:hover {{ transform:translateY(-5px); border-color:#2563eb; box-shadow:0 14px 28px rgba(37,99,235,.15); }}
        .kpi-label {{ color:{c['sub']}; font-size:.8rem; text-transform:uppercase; letter-spacing:.8px; font-weight:600; margin-bottom:.5rem; }}
        .kpi-value {{ font-size:2rem; font-weight:800; color:{c['title']}; line-height:1; }}
        .kpi-delta {{ font-size:.85rem; font-weight:700; margin-top:.5rem; }}
        .kpi-delta.bad {{ color:#ef4444; }}
        .kpi-delta.good {{ color:#22c55e; }}

        [data-testid="stVerticalBlockBorderWrapper"] {{ background:{c['card_bg']} !important;
            border:1px solid {c['card_border']} !important; border-radius:16px !important;
            padding:.4rem !important; transition:border-color .25s ease; }}
        [data-testid="stVerticalBlockBorderWrapper"]:hover {{ border-color:#2563eb !important; }}
        .panel-title {{ font-size:1.12rem; font-weight:700; color:{c['title']}; margin:.5rem .3rem .1rem; }}

        /* ---- insight chips ---- */
        .insight-strip {{ display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin:0 0 1.6rem; }}
        @media (max-width:900px) {{ .insight-strip {{ grid-template-columns:1fr; }} }}
        .insight-chip {{ display:flex; gap:.9rem; align-items:flex-start; background:linear-gradient(135deg, rgba(37,99,235,.08), rgba(37,99,235,.02));
            border:1px solid rgba(37,99,235,.25); border-radius:14px; padding:1.1rem 1.3rem;
            transition:transform .25s ease, border-color .25s ease; }}
        .insight-chip:hover {{ transform:translateY(-4px); border-color:#2563eb; }}
        .insight-ico {{ font-size:1.3rem; flex:0 0 auto; }}
        .insight-txt {{ color:{c['title']}; font-size:.93rem; line-height:1.5; }}
        .insight-txt b {{ color:#3b82f6; }}
        .insight-line {{ margin-top:.7rem; padding:.55rem .85rem; border-left:3px solid #2563eb;
            background:rgba(37,99,235,.06); border-radius:6px; font-size:.87rem; color:{c['sub']}; line-height:1.5; }}
        .insight-line b {{ color:{c['title']}; }}

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

        .ai-summary-card {{ background:linear-gradient(135deg, rgba(37,99,235,.10), rgba(37,99,235,.02));
        border:1px solid rgba(37,99,235,.28); border-radius:18px; padding:1.8rem; margin-top:1.4rem;
        position:relative; overflow:hidden; }}
        .ai-summary-eyebrow {{ display:inline-flex; align-items:center; gap:.4rem; font-size:.78rem; font-weight:700;
            letter-spacing:.5px; text-transform:uppercase; color:#3b82f6; margin-bottom:.7rem; }}
        .ai-summary-text {{ color:{c['title']}; font-size:1.05rem; line-height:1.7; }}

        /* ---- how it was built: filters, table, reasoning cards ---- */
        [data-testid="stMultiSelect"] > div > div {{ background-color:{c['bg']} !important; border-color:{c['card_border']} !important; }}
        [data-testid="stMultiSelect"] * {{ color:{c['title']} !important; }}
        [data-testid="stMultiSelect"] span[data-baseweb="tag"] {{ background:#2563eb !important; color:#fff !important; }}
        [data-testid="stMultiSelect"] svg {{ fill:{c['sub']} !important; }}
        [data-testid="stDataFrame"] {{ border:1px solid {c['card_border']} !important; border-radius:14px !important; overflow:hidden; }}

        .model-table-wrap {{ overflow-x:auto; border:1px solid {c['card_border']}; border-radius:16px;
            background:{c['card_bg']}; margin:1.2rem 0 .6rem; }}
        .model-table {{ width:100%; border-collapse:collapse; font-size:.93rem; min-width:720px; }}
        .model-table th {{ text-align:left; padding:.9rem 1.1rem; color:{c['sub']}; font-size:.74rem;
            text-transform:uppercase; letter-spacing:.6px; font-weight:700; border-bottom:1px solid {c['card_border']}; white-space:nowrap; }}
        .model-table td {{ padding:.8rem 1.1rem; color:{c['title']}; border-bottom:1px solid {c['card_border']}; white-space:nowrap; }}
        .model-table tr:last-child td {{ border-bottom:none; }}
        .model-table tbody tr {{ transition:background .15s ease; }}
        .model-table tbody tr:hover td {{ background:rgba(37,99,235,.07); }}
        .model-table tr.chosen td {{ background:rgba(37,99,235,.10); font-weight:600; }}
        .model-table tr.chosen td:first-child {{ border-left:3px solid #2563eb; padding-left:calc(1.1rem - 3px); }}
        .model-name {{ font-weight:700; }}
        .variant-pill {{ display:inline-block; font-size:.78rem; padding:.2rem .6rem; border-radius:999px;
            background:rgba(127,127,127,.14); color:{c['sub']}; }}
        .chosen-badge {{ display:inline-flex; align-items:center; gap:.35rem; background:#2563eb; color:#fff;
            font-size:.68rem; font-weight:700; padding:.22rem .6rem; border-radius:999px; margin-left:.55rem;
            letter-spacing:.3px; text-transform:uppercase; vertical-align:middle; }}
        .metric-best {{ color:#22c55e; font-weight:700; }}

        .reason-card {{ background:{c['card_bg']}; border:1px solid {c['card_border']}; border-radius:16px;
            padding:1.5rem; height:100%; transition:transform .25s ease, border-color .25s ease; }}
        .reason-card:hover {{ transform:translateY(-5px); border-color:#2563eb; }}
        .reason-card .ico {{ font-size:1.7rem; margin-bottom:.7rem; }}
        .reason-card h4 {{ color:{c['title']}; font-size:1.05rem; font-weight:700; margin:0 0 .5rem; }}
        .reason-card p {{ color:{c['sub']}; font-size:.93rem; line-height:1.55; margin:0; }}

        /* pipeline visual (reused from Home) */
        .pipe {{ display: flex; flex-direction: column; align-items: stretch; }}
        .node {{ display: flex; align-items: center; gap: 1rem; background: {c['card_bg']};
            border: 1px solid {c['card_border']}; border-radius: 14px; padding: 1rem 1.3rem; }}
        .node:hover {{ border-color: #2563eb; }}
        .node .nico {{ font-size: 1.5rem; width: 2rem; text-align: center; }}
        .node .nlbl {{ font-weight: 600; color: {c['title']}; font-size: 1.05rem; }}
        .connector {{ width: 3px; height: 30px; margin: 0 auto; border-radius: 3px;
            background: linear-gradient(180deg, #2563eb, rgba(37,99,235,.15));
            background-size: 100% 220%; animation: flowDown 1.4s linear infinite; }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    return c, theme


def nav(active, c, theme):
    """Render the shared top navbar. `active` is the current page label."""
    def cls(label):
        return ' class="active"' if label == active else ""
    paths = {"Home": "/", "Prediction": "/Prediction", "Dashboard": "/Dashboard", "How It Was Built": "/How_It_Was_Built"}
    here = paths.get(active, "/")
    st.markdown(
        f"""
        <div class="navbar">
            <div class="brand">ChurnAI</div>
            <div class="navlinks">
                <a href="/?theme={theme}"{cls('Home')} target="_self">Home</a>
                <a href="/Prediction?theme={theme}"{cls('Prediction')} target="_self">Prediction</a>
                <a href="/Dashboard?theme={theme}"{cls('Dashboard')} target="_self">Dashboard</a>
                <a href="/How_It_Was_Built?theme={theme}"{cls('How It Was Built')} target="_self">How It Was Built</a>
                <a href="{here}?theme={c['switch_to']}" class="theme-toggle" target="_self" title="Switch theme">{c['icon']}</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def loading_screen(c, facts, height=240):
    """Self-contained animated loader: spinning ring + rotating facts that
    fade in/out. Everything runs inside its own iframe, so it keeps
    animating even while the Python script is busy doing real work."""
    facts_json = json.dumps(facts)
    html = f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
        height:{height}px; font-family:'Poppins',sans-serif;">
        <div style="width:56px; height:56px; border-radius:50%;
            border:4px solid {c['card_border']}; border-top-color:#2563eb;
            animation:spin .85s linear infinite;"></div>
        <div id="fact-text" style="margin-top:1.5rem; max-width:460px; text-align:center;
            color:{c['sub']}; font-size:1rem; line-height:1.6; opacity:0; transition:opacity .4s ease;"></div>
    </div>
    <style>@keyframes spin {{ to {{ transform:rotate(360deg); }} }}</style>
    <script>
        const facts = {facts_json};
        let i = 0;
        const el = document.getElementById('fact-text');
        function showFact() {{
            el.style.opacity = 0;
            setTimeout(function() {{
                el.textContent = "💡 " + facts[i % facts.length];
                el.style.opacity = 1;
                i++;
            }}, 300);
        }}
        showFact();
        setInterval(showFact, 2600);
    </script>
    """
    st.components.v1.html(html, height=height + 20)
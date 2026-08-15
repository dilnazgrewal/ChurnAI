import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from theme import apply, nav, loading_screen
from pathlib import Path

c, theme = apply("Dashboard")
nav("Dashboard", c, theme)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Telco_customer_churn.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(DATA_PATH)

DASHBOARD_FACTS = [
    "A 5% increase in customer retention can raise profits by 25–95%.",
    "It typically costs 5–7x more to acquire a new customer than to keep one.",
    "Customers on month-to-month contracts churn far more than those on annual plans.",
    "SHAP values explain individual predictions by attributing each feature's contribution.",
    "The first 90 days of a customer's tenure are usually the highest-risk window.",
    "Fiber-optic customers often churn more than DSL — usually a price/reliability trade-off.",
]

if "dashboard_data_loaded" not in st.session_state:
    loader = st.empty()
    with loader:
        loading_screen(c, DASHBOARD_FACTS)
    df = load_data()
    st.session_state.dashboard_data_loaded = True
    loader.empty()
else:
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Dataset not found. Update the path in load_data() inside pages/2_Dashboard.py.")
        st.stop()

FONT = "Poppins, sans-serif"
GRID = c["card_border"]
TXT = c["title"]
SUB = c["sub"]
BLUE, RED, AMBER, GREEN = "#2563eb", "#ef4444", "#f59e0b", "#22c55e"
MAP_STYLE = "carto-darkmatter" if theme == "dark" else "carto-positron"

def style_fig(fig, height=340):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, color=TXT, size=13),
        margin=dict(l=10, r=10, t=10, b=10), height=height,
        legend=dict(font=dict(color=SUB)),
    )
    fig.update_xaxes(
        gridcolor=GRID, zerolinecolor=GRID,
        tickfont=dict(color=SUB, size=12),
        title_font=dict(color=TXT, size=13),
    )
    fig.update_yaxes(
        gridcolor=GRID, zerolinecolor=GRID,
        tickfont=dict(color=SUB, size=12),
        title_font=dict(color=TXT, size=13),
    )
    return fig

# ------------------------------------------------------------------ Header
st.markdown(
    """
    <div class="reveal" style="padding-top:.5rem;">
        <div class="page-title">Business Dashboard</div>
        <div class="hero-sub" style="margin-bottom:1.4rem;">A live view of churn risk across your customer base — who's leaving, why, and where the exposure is concentrated.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ KPI row (animated count-up)
total = len(df)
churned = int(df["Churn Value"].sum())
churn_rate = churned / total * 100
avg_cltv = df["CLTV"].mean()
avg_monthly = df["Monthly Charges"].mean()

kpis = [
    ("Total Customers", total, "", "", 0),
    ("Churned Customers", churned, "", "", 0),
    ("Avg CLTV", avg_cltv, "$", "", 0),
    ("Avg Monthly Charges", avg_monthly, "$", "", 2),
]
kcols = st.columns(4)
for col, (label, value, prefix, suffix, decimals) in zip(kcols, kpis):
    with col:
        st.markdown(
            f"""
            <div class="kpi-tile reveal">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" data-target="{value}" data-prefix="{prefix}" data-suffix="{suffix}" data-decimals="{decimals}">{prefix}0{suffix}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# count-up animation — runs once per page load, targets the parent doc
st.components.v1.html(
    """
    <script>
        setTimeout(function() {
            const doc = window.parent.document;
            const els = doc.querySelectorAll('.kpi-value[data-target]');
            els.forEach(function(el) {
                const target = parseFloat(el.dataset.target);
                const prefix = el.dataset.prefix || '';
                const suffix = el.dataset.suffix || '';
                const decimals = parseInt(el.dataset.decimals || '0');
                const duration = 900;
                const startTime = performance.now();
                function step(now) {
                    const p = Math.min((now - startTime) / duration, 1);
                    const eased = 1 - Math.pow(1 - p, 3);
                    const val = target * eased;
                    el.textContent = prefix + val.toLocaleString(undefined, {minimumFractionDigits: decimals, maximumFractionDigits: decimals}) + suffix;
                    if (p < 1) requestAnimationFrame(step);
                }
                requestAnimationFrame(step);
            });
        }, 200);
    </script>
    """,
    height=0,
)

st.markdown("<div style='height:1.6rem;'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------ Row: Contract & Tenure
r1c1, r1c2 = st.columns(2)

with r1c1:
    with st.container(border=True):
        st.markdown('<div class="panel-title">Churn Rate by Contract Type</div>', unsafe_allow_html=True)
        contract_rate = (df.groupby("Contract")["Churn Value"].mean() * 100).sort_values(ascending=False).reset_index()
        contract_rate.columns = ["Contract", "Churn Rate"]
        fig = px.bar(contract_rate, x="Contract", y="Churn Rate", text="Churn Rate")
        fig.update_traces(
            marker_color=[RED if v > churn_rate else BLUE for v in contract_rate["Churn Rate"]],
            texttemplate="%{text:.1f}%", textposition="outside",
        )
        st.plotly_chart(style_fig(fig), use_container_width=True, config={"displayModeBar": False})
        top_contract = contract_rate.iloc[0]
        st.markdown(
            f'<div class="insight-line">💡 <b>{top_contract["Contract"]}</b> customers churn at <b>{top_contract["Churn Rate"]:.1f}%</b> — the highest of any contract type. Locking customers into longer terms is the single strongest lever here.</div>',
            unsafe_allow_html=True,
        )

with r1c2:
    with st.container(border=True):
        st.markdown('<div class="panel-title">Churn Rate by Tenure Bucket</div>', unsafe_allow_html=True)
        bins = [0, 12, 24, 36, 48, 60, 72]
        labels = ["0-12", "13-24", "25-36", "37-48", "49-60", "61-72"]
        tmp = df.copy()
        tmp["Tenure Bucket"] = pd.cut(tmp["Tenure Months"], bins=bins, labels=labels, include_lowest=True)
        tenure_rate = (tmp.groupby("Tenure Bucket", observed=True)["Churn Value"].mean() * 100).reset_index()
        tenure_rate.columns = ["Tenure (Months)", "Churn Rate"]
        fig = px.bar(tenure_rate, x="Tenure (Months)", y="Churn Rate", text="Churn Rate")
        fig.update_traces(
            marker_color=[RED if v > churn_rate else BLUE for v in tenure_rate["Churn Rate"]],
            texttemplate="%{text:.1f}%", textposition="outside",
        )
        st.plotly_chart(style_fig(fig), use_container_width=True, config={"displayModeBar": False})
        newest = tenure_rate.iloc[0]
        st.markdown(
            f'<div class="insight-line">💡 New customers (<b>{newest["Tenure (Months)"]} months</b>) churn at <b>{newest["Churn Rate"]:.1f}%</b> — the first year is where most retention effort should be spent.</div>',
            unsafe_allow_html=True,
        )

st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------ Row: Gauge + Reason donut
r2c1, r2c2 = st.columns([0.85, 1.15])

with r2c1:
    with st.container(border=True):
        st.markdown('<div class="panel-title">Overall Churn Rate</div>', unsafe_allow_html=True)
        benchmark = 26.6  # industry-average telecom churn reference point
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=churn_rate,
            number={"suffix": "%", "font": {"size": 34, "color": TXT}},
            gauge={
                "axis": {"range": [0, 60], "tickcolor": SUB},
                "bar": {"color": RED if churn_rate > benchmark else GREEN},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 20], "color": "rgba(34,197,94,.18)"},
                    {"range": [20, 35], "color": "rgba(245,158,11,.18)"},
                    {"range": [35, 60], "color": "rgba(239,68,68,.18)"},
                ],
                "threshold": {"line": {"color": TXT, "width": 3}, "thickness": .8, "value": benchmark},
            },
        ))
        st.plotly_chart(style_fig(gauge, height=250), use_container_width=True, config={"displayModeBar": False})
        diff = churn_rate - benchmark
        arrow = "▲" if diff > 0 else "▼"
        cls = "bad" if diff > 0 else "good"
        st.markdown(
            f'<div class="insight-line">📊 <b class="{cls}">{arrow} {abs(diff):.1f} pts</b> vs the {benchmark}% industry benchmark (marked by the line on the dial).</div>',
            unsafe_allow_html=True,
        )

with r2c2:
    with st.container(border=True):
        st.markdown('<div class="panel-title">Churn Reason Breakdown</div>', unsafe_allow_html=True)
        reasons = df[df["Churn Value"] == 1]["Churn Reason"].value_counts().head(6).reset_index()
        reasons.columns = ["Reason", "Count"]
        fig = px.pie(
            reasons, names="Reason", values="Count", hole=0.58,
            color_discrete_sequence=[BLUE, "#3b82f6", "#60a5fa", AMBER, RED, "#93c5fd"],
        )
        fig.update_traces(
            textinfo="percent", textfont=dict(color="#ffffff", size=12),
            hovertemplate="%{label}<br>%{value} customers (%{percent})<extra></extra>",
        )
        fig.update_layout(
            legend=dict(orientation="v", x=1.02, y=0.5, font=dict(color=SUB, size=11)),
            margin=dict(l=10, r=140, t=10, b=10),
        )
        top_reason = reasons.iloc[0]
        fig.add_annotation(text=f"{top_reason['Reason']}<br><b>{top_reason['Count']/reasons['Count'].sum()*100:.0f}%</b>",
                            showarrow=False, font=dict(size=12, color=TXT))
        st.plotly_chart(style_fig(fig, height=300), use_container_width=True, config={"displayModeBar": False})
        st.markdown(
            f'<div class="insight-line">💡 <b>{top_reason["Reason"]}</b> is the single most common reason customers leave — worth a dedicated retention play.</div>',
            unsafe_allow_html=True,
        )

st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------ Row: Geographic churn map
with st.container(border=True):
    st.markdown('<div class="panel-title">Where Churn Is Happening</div>', unsafe_allow_html=True)
    map_col, list_col = st.columns([1.6, 1])

    with map_col:
        geo = df.dropna(subset=["Latitude", "Longitude"]).copy()
        geo["Status"] = geo["Churn Value"].map({1: "Churned", 0: "Retained"})
        fig = px.scatter_mapbox(
            geo, lat="Latitude", lon="Longitude", color="Status",
            color_discrete_map={"Churned": RED, "Retained": BLUE},
            hover_data={"City": True, "Monthly Charges": True, "Latitude": False, "Longitude": False},
            zoom=5, height=420, opacity=0.55,
        )
        fig.update_layout(mapbox_style=MAP_STYLE, mapbox_center={"lat": 36.7, "lon": -119.4})
        st.plotly_chart(style_fig(fig, height=420), use_container_width=True, config={"displayModeBar": False})

    with list_col:
        st.markdown('<div style="font-weight:700; color:' + TXT + '; margin-bottom:.7rem;">Top Churn Hotspots</div>', unsafe_allow_html=True)
        top_cities = df[df["Churn Value"] == 1]["City"].value_counts().head(6).reset_index()
        top_cities.columns = ["City", "Churned"]
        rows = "".join(
            f'<div class="rec-item"><span class="arw">{i+1}.</span><span>{row["City"]} — <b>{row["Churned"]}</b> churned</span></div>'
            for i, row in top_cities.iterrows()
        )
        st.markdown(f'<div>{rows}</div>', unsafe_allow_html=True)

st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------ Row: CLTV & Payment Method
r3c1, r3c2 = st.columns(2)

with r3c1:
    with st.container(border=True):
        st.markdown('<div class="panel-title">Avg CLTV — Churned vs Retained</div>', unsafe_allow_html=True)
        cltv_cmp = df.groupby("Churn Value")["CLTV"].mean().reset_index()
        cltv_cmp["Group"] = cltv_cmp["Churn Value"].map({0: "Retained", 1: "Churned"})
        fig = px.bar(cltv_cmp, x="Group", y="CLTV", text="CLTV")
        fig.update_traces(marker_color=[BLUE, RED], texttemplate="$%{text:,.0f}", textposition="outside")
        st.plotly_chart(style_fig(fig), use_container_width=True, config={"displayModeBar": False})
        gap = cltv_cmp.loc[cltv_cmp["Group"] == "Retained", "CLTV"].values[0] - cltv_cmp.loc[cltv_cmp["Group"] == "Churned", "CLTV"].values[0]
        st.markdown(
            f'<div class="insight-line">💡 Retained customers carry <b>${gap:,.0f}</b> more lifetime value on average — churn isn\'t just customer loss, it\'s value loss.</div>',
            unsafe_allow_html=True,
        )

with r3c2:
    with st.container(border=True):
        st.markdown('<div class="panel-title">Churn Rate by Payment Method</div>', unsafe_allow_html=True)
        pay_rate = (df.groupby("Payment Method")["Churn Value"].mean() * 100).sort_values(ascending=False).reset_index()
        pay_rate.columns = ["Payment Method", "Churn Rate"]
        fig = px.bar(pay_rate, x="Churn Rate", y="Payment Method", orientation="h", text="Churn Rate")
        fig.update_traces(
            marker_color=[RED if v > churn_rate else BLUE for v in pay_rate["Churn Rate"]],
            texttemplate="%{text:.1f}%", textposition="outside",
        )
        st.plotly_chart(style_fig(fig), use_container_width=True, config={"displayModeBar": False})
        top_pay = pay_rate.iloc[0]
        st.markdown(
            f'<div class="insight-line">💡 <b>{top_pay["Payment Method"]}</b> users churn most (<b>{top_pay["Churn Rate"]:.1f}%</b>) — likely a proxy for lower engagement with automatic billing.</div>',
            unsafe_allow_html=True,
        )
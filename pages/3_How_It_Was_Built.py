import streamlit as st
from theme import apply, nav
from pathlib import Path
import pandas as pd
c, theme = apply("How It Was Built")
nav("How It Was Built", c, theme)

MODEL_RESULTS = [
    {"model": "Logistic Regression", "variant": "Baseline",                  "accuracy": 0.7967, "precision": 0.6279, "recall": 0.5775, "f1": 0.6017, "roc_auc": 0.8447},
    {"model": "Logistic Regression", "variant": "Hyperparameter Tuned",      "accuracy": 0.7946, "precision": 0.6246, "recall": 0.5695, "f1": 0.5958, "roc_auc": 0.8443},
    {"model": "Logistic Regression", "variant": "SMOTE",                     "accuracy": 0.7306, "precision": 0.4958, "recall": 0.7941, "f1": 0.6105, "roc_auc": 0.8422},
    {"model": "Logistic Regression", "variant": "Threshold Optimized",       "accuracy": 0.8003, "precision": 0.6177, "recall": 0.6524, "f1": 0.6346, "roc_auc": 0.8443, "chosen": True},
    {"model": "Decision Tree",       "variant": "Baseline",                  "accuracy": 0.7875, "precision": 0.5984, "recall": 0.6096, "f1": 0.6040, "roc_auc": 0.8348},
    {"model": "Decision Tree",       "variant": "Hyperparameter Tuned",      "accuracy": 0.7868, "precision": 0.6000, "recall": 0.5936, "f1": 0.5968, "roc_auc": 0.8220},
    {"model": "Decision Tree",       "variant": "Hyperparameter + SMOTEENN", "accuracy": 0.7029, "precision": 0.4666, "recall": 0.8209, "f1": 0.5950, "roc_auc": 0.8003},
    {"model": "Random Forest",       "variant": "Baseline",                  "accuracy": 0.7918, "precision": 0.6494, "recall": 0.4706, "f1": 0.5457, "roc_auc": 0.8452},
    {"model": "Random Forest",       "variant": "Hyperparameter + SMOTEENN", "accuracy": 0.7214, "precision": 0.4857, "recall": 0.8155, "f1": 0.6088, "roc_auc": 0.8382},
    {"model": "XGBoost",             "variant": "Baseline",                  "accuracy": 0.7953, "precision": 0.6344, "recall": 0.5428, "f1": 0.5850, "roc_auc": 0.8479},
    {"model": "XGBoost",             "variant": "Threshold Optimized",       "accuracy": 0.7846, "precision": 0.5773, "recall": 0.7086, "f1": 0.6363, "roc_auc": 0.8479},
]

METRICS = ["accuracy", "precision", "recall", "f1", "roc_auc"]
METRIC_LABELS = {"accuracy": "Accuracy", "precision": "Precision", "recall": "Recall", "f1": "F1", "roc_auc": "ROC-AUC"}
best_per_metric = {m: max(r[m] for r in MODEL_RESULTS) for m in METRICS}

# ---------------------------------------------------------------- Hero
st.markdown(
    """
    <div class="reveal" style="padding-top:.5rem;">
        <div style="display:inline-block; background:rgba(37,99,235,.15); color:#3b82f6; font-weight:700; font-size:.8rem; padding:.3rem .8rem; border-radius:999px; margin-bottom:1rem;">🔬 Full Model Comparison</div>
        <div class="page-title">How It Was Built</div>
        <div class="hero-sub" style="margin-bottom:1.6rem;">
            From raw customer data to a deployed, explainable churn model — the dataset, the models
            tested, and the reasoning behind the one that made it into production.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

HERO_STATS = [
    ("Models Compared", "4"),
    ("Experiments Run", "11"),
    ("Best Accuracy", "80.03%"),
    ("Explainability", "SHAP"),
]
scols = st.columns(4)
for col, (label, value) in zip(scols, HERO_STATS):
    with col:
        st.markdown(
            f"""
            <div class="kpi-tile reveal">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------- Dataset
st.markdown(
    """
    <div class="section reveal" style="padding-bottom:.5rem;">
        <div class="section-title">Dataset</div>
        <div class="section-sub">A widely used, publicly available telecom churn dataset — no proprietary or customer data is used.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="req-grid reveal">
        <div class="req-tile">
            <div class="req-ico">📦</div>
            <div>
                <div class="rt-title">Source</div>
                <div class="rt-sub">IBM Telco Customer Churn dataset, publicly hosted on
                    <a href="https://www.kaggle.com/datasets/blastchar/telco-customer-churn" target="_blank" style="color:#3b82f6;">Kaggle</a>
                    (swap this link if you used a different mirror of the dataset).</div>
            </div>
        </div>
        <div class="req-tile">
            <div class="req-ico">🧾</div>
            <div>
                <div class="rt-title">Size &amp; Features</div>
                <div class="rt-sub">~7,000 customer records across demographic, account, billing and service-usage fields, plus the geographic and lifetime-value fields used in the Dashboard page.</div>
            </div>
        </div>
        <div class="req-tile">
            <div class="req-ico">🎯</div>
            <div>
                <div class="rt-title">Target</div>
                <div class="rt-sub">Binary churn label — whether the customer left within the observed period — with a moderately imbalanced class split, typical of real churn data.</div>
            </div>
        </div>
        <div class="req-tile">
            <div class="req-ico">🔒</div>
            <div>
                <div class="rt-title">What's Not Shared</div>
                <div class="rt-sub">The cleaned/engineered training set and exact preprocessing pipeline stay private; only the public raw source and aggregate results are shown here.</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Telco_customer_churn.xlsx"

@st.cache_data
def load_raw_preview():
    return pd.read_excel(DATA_PATH)

st.markdown('<div class="panel-title" style="margin-top:1.6rem;">Raw Dataset Preview</div>', unsafe_allow_html=True)

try:
    preview_df = load_raw_preview()
    st.caption(f"{len(preview_df):,} rows × {preview_df.shape[1]} columns — scroll to explore, exactly as sourced from Kaggle.")
    st.dataframe(preview_df, use_container_width=True, height=420)
except FileNotFoundError:
    st.info("Dataset file not found — check DATA_PATH above matches your project's data/ folder.")

# ---------------------------------------------------------------- Model comparison
st.markdown(
    """
    <div class="section reveal" style="padding-bottom:.3rem;">
        <div class="section-title">Model Comparison</div>
        <div class="section-sub">Four algorithms, multiple optimization strategies — filter to explore what was tried before landing on the final model.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

fcol1, fcol2 = st.columns(2)
with fcol1:
    model_filter = st.multiselect(
        "Filter by model",
        options=sorted({r["model"] for r in MODEL_RESULTS}),
        default=sorted({r["model"] for r in MODEL_RESULTS}),
    )
with fcol2:
    variant_filter = st.multiselect(
        "Filter by optimization",
        options=sorted({r["variant"] for r in MODEL_RESULTS}),
        default=sorted({r["variant"] for r in MODEL_RESULTS}),
    )

filtered = [r for r in MODEL_RESULTS if r["model"] in model_filter and r["variant"] in variant_filter]

def cell(r, m):
    val = r[m]
    txt = f"{val*100:.2f}%" if m != "roc_auc" else f"{val:.4f}"
    cls = "metric-best" if val == best_per_metric[m] else ""
    return f'<td><span class="{cls}">{txt}</span></td>'

rows_html = ""
for r in filtered:
    row_cls = "chosen" if r.get("chosen") else ""
    badge = '<span class="chosen-badge">✓ Selected</span>' if r.get("chosen") else ""
    rows_html += (
        f'<tr class="{row_cls}">'
        f'<td><span class="model-name">{r["model"]}</span></td>'
        f'<td><span class="variant-pill">{r["variant"]}</span>{badge}</td>'
        + "".join(cell(r, m) for m in METRICS)
        + "</tr>"
    )

if filtered:
    st.markdown(
        f"""
        <div class="model-table-wrap reveal">
            <table class="model-table">
                <thead>
                    <tr>
                        <th>Model</th>
                        <th>Variant</th>
                        {"".join(f"<th>{METRIC_LABELS[m]}</th>" for m in METRICS)}
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="insight-line">💡 Green values are the best result for that metric across every run tested. '
        'The row marked <b>✓ Selected</b> is the model actually deployed in this app.</div>',
        unsafe_allow_html=True,
    )
else:
    st.info("No runs match the current filters — adjust the selections above.")

# ---------------------------------------------------------------- Why this model
st.markdown(
    """
    <div class="section reveal" style="padding-bottom:.3rem;">
        <div class="section-title">Why Threshold-Optimized Logistic Regression</div>
        <div class="section-sub">It wasn't the top scorer on every single metric — here's why it was chosen anyway.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

REASONS = [
    ("🎯", "The Right Metric For Churn", "A missed churner (false negative) costs far more than a false alarm. Instead of the default 0.5 cutoff, the decision threshold was tuned to balance precision and recall around the real cost of losing a customer — not just raw accuracy."),
    ("🔍", "Fully Explainable", "Logistic Regression's coefficients and SHAP values map directly onto real customer attributes, so every prediction can be explained to a non-technical stakeholder in one sentence — critical for a retention tool account managers will actually use."),
    ("⚖️", "Best Overall Trade-off", "It posted the highest accuracy of every single run tested (80.03%) and the strongest F1 among all Logistic Regression variants. XGBoost's threshold-optimized run edged it out on F1 by a hair (63.6% vs 63.5%) — but at the cost of a black-box ensemble with far less transparency for a business-facing tool."),
    ("⚡", "Simple, Fast, Stable", "A linear model trains and serves in milliseconds, carries little overfitting risk on a dataset this size, and needs no ensemble of hundreds of trees kept in sync in production."),
]

rcols = st.columns(2)
for i, (ico, title, desc) in enumerate(REASONS):
    with rcols[i % 2]:
        st.markdown(
            f"""
            <div class="reason-card reveal" style="margin-bottom:1.2rem;">
                <div class="ico">{ico}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------- Methodology pipeline
st.markdown(
    """
    <div class="section reveal">
        <div class="section-title">Methodology</div>
        <div class="section-sub">The same pipeline every candidate model went through, end to end.</div>
        <div class="pipe">
            <div class="node"><span class="nico">🔎</span><span class="nlbl">Exploratory Data Analysis</span></div>
            <div class="connector"></div>
            <div class="node"><span class="nico">🛠️</span><span class="nlbl">Feature Engineering</span></div>
            <div class="connector"></div>
            <div class="node"><span class="nico">🧪</span><span class="nlbl">Baseline Models — Logistic Regression, Decision Tree, Random Forest, XGBoost</span></div>
            <div class="connector"></div>
            <div class="node"><span class="nico">🎛️</span><span class="nlbl">Hyperparameter Tuning</span></div>
            <div class="connector"></div>
            <div class="node"><span class="nico">⚖️</span><span class="nlbl">Class Imbalance Handling — SMOTE / SMOTEENN</span></div>
            <div class="connector"></div>
            <div class="node"><span class="nico">🎯</span><span class="nlbl">Decision Threshold Optimization</span></div>
            <div class="connector"></div>
            <div class="node"><span class="nico">✅</span><span class="nlbl">Final Model Selection</span></div>
            <div class="connector"></div>
            <div class="node"><span class="nico">🧠</span><span class="nlbl">SHAP Explainability Layer</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
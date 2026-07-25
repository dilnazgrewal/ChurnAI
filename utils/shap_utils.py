import shap
import pandas as pd

from loader import (
    load_pipeline,
    load_shap_background,
    load_readable_feature_names
)

pipeline = load_pipeline()
background = load_shap_background()
readable_feature_names = load_readable_feature_names()

model = pipeline.named_steps["classifier"]

preprocessor = pipeline.named_steps["preprocessor"]

# Create SHAP explainer
explainer = shap.Explainer(
    model,
    masker=shap.maskers.Independent(
        background,
        max_samples=500
    )
)

def preprocess_customer(customer_df):
    """
    Transform customer data using the trained preprocessor.
    """
    return preprocessor.transform(customer_df)

def get_shap_values(customer_processed):
    """
    Generate SHAP values for a processed customer.
    """
    return explainer(customer_processed)

def get_feature_importance(shap_values):
    """
    Convert SHAP values into a DataFrame.
    """

    importance = pd.DataFrame({
        "Feature": readable_feature_names,
        "SHAP Value": shap_values.values[0]
    })

    importance["Absolute SHAP"] = importance["SHAP Value"].abs()

    importance = importance.sort_values(
        "Absolute SHAP",
        ascending=False,
    )

    return importance

HIDDEN_FEATURES = {
    "Services per Month",
    "Security Bundle",
    "Entertainment Bundle",
    "High Value Customer",
    "Long-Term Customer"
}

def get_top_risk_factors(importance, top_n=5):

    importance = importance[
        ~importance["Feature"].isin(HIDDEN_FEATURES)
    ]

    return (
        importance[importance["SHAP Value"] > 0]
        .sort_values("SHAP Value", ascending=False)
        .head(top_n)
    )


def get_top_protective_factors(importance, top_n=5):

    importance = importance[
        ~importance["Feature"].isin(HIDDEN_FEATURES)
    ]

    return (
        importance[importance["SHAP Value"] < 0]
        .sort_values("SHAP Value")
        .head(top_n)
    )
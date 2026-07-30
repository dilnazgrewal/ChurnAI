# import shap
# import pandas as pd

# from .loader import (
#     load_pipeline,
#     load_shap_background,
#     load_readable_feature_names
# )

# pipeline = load_pipeline()
# background = load_shap_background()
# readable_feature_names = load_readable_feature_names()

# model = pipeline.named_steps["classifier"]

# preprocessor = pipeline.named_steps["preprocessor"]

# # Create SHAP explainer
# explainer = shap.Explainer(
#     model,
#     masker=shap.maskers.Independent(
#         background,
#         max_samples=500
#     )
# )

# def preprocess_customer(customer_df):
#     """
#     Transform customer data using the trained preprocessor.
#     """
#     return preprocessor.transform(customer_df)

# def get_shap_values(customer_processed):
#     """
#     Generate SHAP values for a processed customer.
#     """
#     return explainer(customer_processed)

# def get_feature_importance(shap_values):
#     """
#     Convert SHAP values into a DataFrame.
#     """

#     importance = pd.DataFrame({
#         "Feature": readable_feature_names,
#         "SHAP Value": shap_values.values[0]
#     })

#     importance["Absolute SHAP"] = importance["SHAP Value"].abs()

#     importance = importance.sort_values(
#         "Absolute SHAP",
#         ascending=False,
#     )

#     return importance

import shap
import pandas as pd
import streamlit as st

from .loader import (
    load_pipeline,
    load_shap_background,
    load_readable_feature_names,
)

@st.cache_resource
def get_pipeline():
    return load_pipeline()

@st.cache_resource
def get_explainer():
    pipeline = get_pipeline()
    model = pipeline.named_steps["classifier"]
    background = load_shap_background()
    return shap.Explainer(
        model,
        masker=shap.maskers.Independent(background, max_samples=500),
    )

@st.cache_resource
def get_readable_feature_names():
    return load_readable_feature_names()

def preprocess_customer(customer_df):
    """Transform customer data using the trained preprocessor."""
    preprocessor = get_pipeline().named_steps["preprocessor"]
    return preprocessor.transform(customer_df)

def get_shap_values(customer_processed):
    """Generate SHAP values for a processed customer."""
    return get_explainer()(customer_processed)

def get_feature_importance(shap_values):
    """Convert SHAP values into a DataFrame."""
    importance = pd.DataFrame({
        "Feature": get_readable_feature_names(),
        "SHAP Value": shap_values.values[0],
    })
    importance["Absolute SHAP"] = importance["SHAP Value"].abs()
    importance = importance.sort_values("Absolute SHAP", ascending=False)
    return importance
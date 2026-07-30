# from .loader import load_pipeline, load_threshold

# pipeline = load_pipeline()
# threshold = load_threshold()

# def get_risk_level(probability):
#     """
#     Determine customer risk level based on churn probability.
#     """

#     if probability >= 0.80:
#         return "Very High"

#     elif probability >= 0.60:
#         return "High"

#     elif probability >= 0.40:
#         return "Medium"

#     else:
#         return "Low"


# def predict_customer(customer_df):
#     """
#     Predict customer churn using the trained pipeline.

#     Parameters
#     ----------
#     customer_df : pandas.DataFrame
#         A single customer record.

#     Returns
#     -------
#     dict
#         Prediction results.
#     """

#     probability = pipeline.predict_proba(customer_df)[0, 1]

#     prediction = (
#         "Likely to Churn"
#         if probability >= threshold
#         else "Not Likely to Churn"
#     )

#     display_probability = round(float(probability) * 100, 2)

#     risk_level = get_risk_level(probability)

#     return {
#         "prediction": prediction,
#         "probability": display_probability,
#         "risk_level": risk_level
#     }

import streamlit as st
from .loader import load_threshold
from .shap_utils import get_pipeline  


@st.cache_resource
def get_threshold():
    return load_threshold()

def get_risk_level(probability):
    """Determine customer risk level based on churn probability."""
    if probability >= 0.80:
        return "Very High"
    elif probability >= 0.60:
        return "High"
    elif probability >= 0.40:
        return "Medium"
    else:
        return "Low"

def predict_customer(customer_df):
    """
    Predict customer churn using the trained pipeline.

    Parameters
    ----------
    customer_df : pandas.DataFrame
        A single customer record.

    Returns
    -------
    dict
        Prediction results.
    """
    pipeline = get_pipeline()
    threshold = get_threshold()

    probability = pipeline.predict_proba(customer_df)[0, 1]
    prediction = "Likely to Churn" if probability >= threshold else "Not Likely to Churn"
    display_probability = round(float(probability) * 100, 2)
    risk_level = get_risk_level(probability)

    return {
        "prediction": prediction,
        "probability": display_probability,
        "risk_level": risk_level,
    }
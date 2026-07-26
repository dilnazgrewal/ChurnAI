from .prediction import predict_customer
from .shap_utils import (
    preprocess_customer,
    get_shap_values,
    get_feature_importance,
)
from .feature_explanations import generate_feature_explanations
from .recommendation import generate_recommendations
from .feature_engineering import engineer_features

DISPLAY_FEATURES = [
    "Customer Tenure",
    "Contract",
    "Internet Service",
    "Monthly Charges",
    "Total Charges",
    "Online Security",
    "Online Backup",
    "Tech Support",
    "Device Protection",
    "Payment Method",
    "Paperless Billing",
    "Multiple Lines",
    "Streaming TV",
    "Streaming Movies",
    "Total Services",
    "Entertainment Bundle",
    "Security Bundle",
]

def explain_prediction(customer):

    customer = engineer_features(customer)

    prediction = predict_customer(customer)

    processed = preprocess_customer(customer)

    shap_values = get_shap_values(processed)

    importance = get_feature_importance(shap_values)

    # Compute the final risk/protective sets ONCE, using the same
    # criteria that will be shown to the user. Recommendations must
    # be generated from this exact set, or they will drift out of
    # sync with what's displayed.
    risk = (
        importance[
            (importance["SHAP Value"] > 0)
            & (importance["Feature"].isin(DISPLAY_FEATURES))
        ]
        .sort_values("SHAP Value", ascending=False)
        .head(4)
    )

    protective = (
        importance[
            (importance["SHAP Value"] < 0)
            & (importance["Feature"].isin(DISPLAY_FEATURES))
        ]
        .sort_values("SHAP Value")
        .head(4)
    )

    recommendations = generate_recommendations(
        prediction["probability"],
        risk.copy()
    )

    risk = generate_feature_explanations(
        customer.iloc[0],
        risk
    )

    protective = generate_feature_explanations(
        customer.iloc[0],
        protective
    )
    
    return {
        "prediction_result": prediction,
        "shap_values": shap_values,
        "risk_factors": risk,
        "protective_factors": protective,
        "recommendations": recommendations
    }
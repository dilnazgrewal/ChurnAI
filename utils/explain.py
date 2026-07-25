from prediction import predict_customer
from shap_utils import (
    preprocess_customer,
    get_shap_values,
    get_feature_importance,
    get_top_risk_factors,
    get_top_protective_factors
)
from feature_explanations import generate_feature_explanations
from recommendation import generate_recommendations

def explain_prediction(customer):

    # Prediction
    prediction = predict_customer(customer)

    # SHAP
    processed = preprocess_customer(customer)

    shap_values = get_shap_values(processed)

    importance = get_feature_importance(shap_values)

    risk = get_top_risk_factors(importance)

    protective = get_top_protective_factors(importance)

    risk_for_recommendation = risk.copy()

    recommendations = generate_recommendations(
        prediction["probability"],
        risk_for_recommendation
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
def generate_recommendations(churn_probability, risk_factors):
    """
    Generate personalized business recommendations based on
    churn probability and SHAP risk factors.
    """

    recommendations = []

    # Overall recommendation
    if churn_probability >= 0.70:
        recommendations.append(
            "Prioritize this customer for immediate retention outreach."
        )

    elif churn_probability >= 0.40:
        recommendations.append(
            "Monitor this customer closely and consider a targeted retention offer."
        )

    else:
        recommendations.append(
            "No immediate retention intervention is required. Continue regular engagement."
        )

    # Feature-specific recommendations
    for feature in risk_factors["Feature"]:

        if feature == "Month-to-Month Contract":
            recommendations.append(
                "Offer incentives to encourage the customer to switch to a longer-term contract."
            )

        elif feature == "Monthly Charges":
            recommendations.append(
                "Review pricing and consider personalized discounts or value-added services."
            )

        elif feature == "Average Monthly Spend":
            recommendations.append(
                "Evaluate whether the customer is receiving sufficient value for their monthly spending."
            )

        elif feature == "No Online Security":
            recommendations.append(
                "Recommend an Online Security add-on to increase service value."
            )

        elif feature == "No Tech Support":
            recommendations.append(
                "Offer a complimentary Tech Support package or promotional trial."
            )

        elif feature == "Fiber Optic Internet":
            recommendations.append(
                "Review service quality and pricing for the customer's Fiber Optic plan."
            )

        elif feature == "Electronic Check":
            recommendations.append(
                "Encourage switching to automatic payments through a small billing incentive."
            )

        elif feature == "Has Dependents":
            recommendations.append(
                "Consider personalized retention offers tailored to the customer's household needs."
            )

        elif feature == "No Partner":
            recommendations.append(
                "Provide personalized offers that focus on individual customer value."
            )

        elif feature == "Streaming TV":
            recommendations.append(
                "Bundle entertainment services to improve perceived value."
            )

        elif feature == "Streaming Movies":
            recommendations.append(
                "Promote entertainment bundles or premium content offers."
            )

        elif feature == "Entertainment Bundle":
            recommendations.append(
                "Review whether the customer's entertainment package is meeting their expectations."
            )

    # Remove duplicates while preserving order
    recommendations = list(dict.fromkeys(recommendations))

    return recommendations
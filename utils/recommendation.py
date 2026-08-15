def generate_recommendations(churn_probability, risk_factors):
    """
    Generate personalized business recommendations based on
    churn probability and SHAP risk factors.
    """

    recommendations = []

    # Overall recommendation
    if churn_probability >= 70:
        recommendations.append(
            "Prioritize this customer for immediate retention outreach."
        )

    elif churn_probability >= 40:
        recommendations.append(
            "Monitor this customer closely and consider a targeted retention offer."
        )

    else:
        recommendations.append(
            "No immediate retention intervention is required. Continue regular engagement."
        )

        return recommendations 

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

        elif feature == "Avg Monthly Spend":
            recommendations.append(
                "Evaluate whether the customer is receiving sufficient value for their monthly spending."
            )

        elif feature == "No Online Security":
            recommendations.append(
                "Recommend an Online Security add-on to increase service value."
            )

        elif feature == "No Online Backup":
            recommendations.append(
                "Recommend an Online Backup add-on to increase service value."
            )

        elif feature == "No Device Protection":
            recommendations.append(
                "Offer a Device Protection plan, especially if the customer has multiple connected devices."
            )

        elif feature == "No Tech Support":
            recommendations.append(
                "Offer a complimentary Tech Support package or promotional trial."
            )

        elif feature == "Fiber Optic Internet":
            recommendations.append(
                "Review service quality and pricing for the customer's Fiber Optic plan."
            )

        elif feature == "DSL Internet":
            recommendations.append(
                "Check whether upgrading to Fiber Optic would better meet the customer's needs."
            )

        elif feature == "No Internet Service":
            recommendations.append(
                "Explore whether an internet bundle would add value for this customer."
            )

        elif feature == "Electronic Check":
            recommendations.append(
                "Encourage switching to automatic payments through a small billing incentive."
            )


        elif feature == "Multiple Lines":
            recommendations.append(
                "Offer a multi-line discount to reinforce the value of staying on the account."
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

        elif feature == "Security Bundle":
            recommendations.append(
                "Highlight the value of the customer's security services in retention conversations."
            )

        elif feature == "Total Services":
            recommendations.append(
                "Review whether adding or optimizing services would increase perceived value."
            )

        elif feature == "Customer Tenure":
            recommendations.append(
                "Enroll the customer in an early-tenure check-in or onboarding program to build engagement."
            )


    # Remove duplicates while preserving order
    recommendations = list(dict.fromkeys(recommendations))

    return recommendations
feature_explanations = {

    # =========================
    # Numeric Features
    # =========================

    "Customer Tenure": lambda c:
        f"Customer has been with the company for {int(c['Tenure Months'])} months.",

    "Monthly Charges": lambda c:
        f"Customer pays ${c['Monthly Charges']:.2f} per month.",

    "Total Charges": lambda c:
        f"Customer has spent a total of ${c['Total Charges']:.2f}.",

    "Average Monthly Spend": lambda c:
        f"Customer spends an average of ${c['Avg Monthly Spend']:.2f} per month.",

    "Total Services": lambda c:
        f"Customer subscribes to {int(c['Total Services'])} services.",

    "Services per Month": lambda c:
        f"Customer has {c['Services_per_Month']:.2f} services per month of tenure.",

    # =========================
    # Customer Segments
    # =========================

    "New Customer": lambda c:
        "Customer is relatively new.",

    "Long-Term Customer": lambda c:
        "Customer is a long-term customer.",

    "High Value Customer": lambda c:
        "Customer belongs to the high-value customer segment.",

    # =========================
    # Bundles
    # =========================

    "Security Bundle": lambda c:
        "Customer has subscribed to multiple security-related services.",

    "Entertainment Bundle": lambda c:
        "Customer has subscribed to multiple entertainment services.",

    # =========================
    # Contract
    # =========================

    "Month-to-Month Contract": lambda c:
        "Customer is on a Month-to-Month contract.",

    "One-Year Contract": lambda c:
        "Customer is not on a One-Year contract.",

    "Two-Year Contract": lambda c:
        "Customer is not on a Two-Year contract.",

    # =========================
    # Internet
    # =========================

    "Fiber Optic Internet": lambda c:
        "Customer uses Fiber Optic Internet.",

    "DSL Internet": lambda c:
        "Customer uses DSL Internet.",

    "No Internet Service": lambda c:
        "Customer does not have an Internet service subscription.",

    # =========================
    # Additional Services
    # =========================

    "No Online Security": lambda c:
        "Customer has not subscribed to Online Security.",

    "No Online Backup": lambda c:
        "Customer has not subscribed to Online Backup.",

    "No Device Protection": lambda c:
        "Customer has not subscribed to Device Protection.",

    "No Tech Support": lambda c:
        "Customer has not subscribed to Tech Support.",

    "Streaming TV": lambda c:
        "Customer subscribes to Streaming TV.",

    "Streaming Movies": lambda c:
        "Customer subscribes to Streaming Movies.",

    # =========================
    # Billing
    # =========================

    "Electronic Check": lambda c:
        "Customer pays using Electronic Check.",

    "Paperless Billing Enabled": lambda c:
        "Customer uses Paperless Billing.",

    # =========================
    # Family
    # =========================

    "No Partner": lambda c:
        "Customer does not have a partner.",

    "Has Dependents": lambda c:
        "Customer does not have dependents."
}


def explain_feature(feature, customer, shap_value):
    """
    Convert a SHAP feature into a business-friendly explanation.
    """

    explanation = feature_explanations.get(feature)

    if explanation is None:
        return feature

    text = explanation(customer)

    if shap_value > 0:
        return f"{text} This increases the predicted churn risk."

    return f"{text} This reduces the predicted churn risk."


def generate_feature_explanations(customer, factors):
    """
    Add readable explanations to a SHAP feature DataFrame.
    """

    factors = factors.copy()

    factors["Explanation"] = factors.apply(
        lambda row: explain_feature(
            feature=row["Feature"],
            customer=customer,
            shap_value=row["SHAP Value"]
        ),
        axis=1
    )

    return factors
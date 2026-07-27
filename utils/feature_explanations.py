display_feature_names = {

    # Internet Service
    "DSL Internet": "Internet Service",
    "Fiber Optic Internet": "Internet Service",
    "No Internet Service": "Internet Service",

    # Contract
    "Month-to-Month Contract": "Contract",
    "One-Year Contract": "Contract",
    "Two-Year Contract": "Contract",

    # Payment
    "Electronic Check": "Payment Method",
    "Bank Transfer": "Payment Method",
    "Credit Card": "Payment Method",
    "Mailed Check": "Payment Method",

    # Partner
    "Has Partner": "Partner",
    "No Partner": "Partner",

    # Dependents
    "Has Dependents": "Dependents",
    "No Dependents": "Dependents",

    # Multiple Lines
    "Multiple Lines": "Multiple Lines",
    "No Multiple Lines": "Multiple Lines",

    # Online Security
    "Online Security": "Online Security",
    "No Online Security": "Online Security",

    # Tech Support
    "Tech Support": "Tech Support",
    "No Tech Support": "Tech Support",

    # Online Backup
    "Online Backup": "Online Backup",
    "No Online Backup": "Online Backup",

    # Device Protection
    "Device Protection": "Device Protection",
    "No Device Protection": "Device Protection",
}

feature_explanations = {

    "Customer Tenure": lambda c:
        f"Customer has been with the company for {int(c['Tenure Months'])} months.",

    "Monthly Charges": lambda c:
        f"Customer pays ${c['Monthly Charges']:.2f} per month, "
        f"{'above' if c['High_Value'] else 'at or below'} the typical customer's monthly spend.",

    "Total Charges": lambda c:
        f"Customer has spent a total of ${c['Total Charges']:.2f} over "
        f"{int(c['Tenure Months'])} months (avg ${c['Avg Monthly Spend']:.2f}/month).",

    "Avg Monthly Spend": lambda c:
        f"Customer spends an average of ${c['Avg Monthly Spend']:.2f} per month.",

    "Total Services": lambda c: (
    f"Customer subscribes to "
    f"{int(c['Total Services'])} "
    f"{'service' if int(c['Total Services']) == 1 else 'services'}."
    ),

    "Services per Month": lambda c:
        f"Customer has {c['Services_per_Month']:.2f} services per month of tenure.",

    "New Customer": lambda c:
        "Customer is relatively new.",

    "Long-Term Customer": lambda c:
        "Customer is a long-term customer.",

    "High Value Customer": lambda c:
        "Customer belongs to the high-value customer segment.",

    "Security Bundle": lambda c:
        "Customer has subscribed to multiple security-related services.",

    "Entertainment Bundle": lambda c:
        "Customer has subscribed to multiple entertainment services.",

    "Month-to-Month Contract": lambda c:
        "Customer is on a Month-to-Month contract.",

    "One-Year Contract": lambda c:
        "Customer is not on a One-Year contract.",

    "Two-Year Contract": lambda c:
        "Customer is not on a Two-Year contract.",

    "Fiber Optic Internet": lambda c:
    (
        "Customer uses Fiber Optic Internet service."
        if c["Internet Service"] == "fiber optic"
        else "Customer does not use Fiber Optic Internet service."
    ),

    "DSL Internet": lambda c:
    (
        "Customer uses DSL Internet service."
        if c["Internet Service"] == "dsl"
        else "Customer does not use DSL Internet service."
    ),

    "No Internet Service": lambda c:
        "Customer does not have an Internet service subscription.",

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

    "Electronic Check": lambda c:
        "Customer pays using Electronic Check.",

    "Paperless Billing Enabled": lambda c:
        "Customer uses Paperless Billing.",

    "No Partner": lambda c:
        "Customer does not have a partner.",

    "Has Dependents": lambda c:
        "Customer has dependents.",

    "Multiple Lines": lambda c:( 
    "Customer has multiple phone lines."
    if c["Multiple Lines"] == "yes"
    else "Customer does not have multiple phone lines."),

    "Online Security": lambda c:
    "Customer has subscribed to Online Security.",

    "Online Backup": lambda c:
        "Customer has subscribed to Online Backup.",

    "Device Protection": lambda c:
        "Customer has subscribed to Device Protection.",

    "Tech Support": lambda c:
        "Customer has subscribed to Tech Support.",
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

    factors["Feature"] = factors["Feature"].map(
    lambda x: display_feature_names.get(x, x)
    )

    factors = (
    factors
    .sort_values("Absolute SHAP", ascending=False)
    .drop_duplicates(subset="Feature")
    .reset_index(drop=True)
    )
    
    return factors
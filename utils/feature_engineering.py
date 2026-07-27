# import pandas as pd


# def engineer_features(customer):
#     """
#     Generate engineered features required by the trained model.

#     Parameters
#     ----------
#     customer : pd.DataFrame
#         Raw customer data collected from the prediction form.

#     Returns
#     -------
#     pd.DataFrame
#         Customer data with engineered features.
#     """

#     customer = customer.copy()

#     # New Customer
#     customer["New Customer"] = (
#         customer["Tenure Months"] <= 12
#     ).astype(int)

#     # Average Monthly Spend
#     customer["Avg Monthly Spend"] = (
#         customer["Total Charges"] /
#         customer["Tenure Months"].replace(0, 1)
#     )

#     # Total Services
#     service_cols = [
#         "Phone Service",
#         "Multiple Lines",
#         "Online Security",
#         "Online Backup",
#         "Device Protection",
#         "Tech Support",
#         "Streaming TV",
#         "Streaming Movies"
#     ]

#     customer["Total Services"] = (
#         customer[service_cols] == "Yes"
#     ).sum(axis=1)

#     # Services Per Month
#     customer["Services_per_Month"] = (
#         customer["Total Services"] /
#         customer["Tenure Months"].replace(0, 1)
#     )

#     # High Value Customer
#     HIGH_VALUE_THRESHOLD = 70.35 

#     customer["High_Value"] = (
#         customer["Monthly Charges"] > HIGH_VALUE_THRESHOLD
#     ).astype(int)

#     # Security Bundle
#     customer["Security Bundle"] = (
#         (customer["Online Security"] == "Yes").astype(int)
#         + (customer["Device Protection"] == "Yes").astype(int)
#         + (customer["Tech Support"] == "Yes").astype(int)
#     )

#     # Entertainment Bundle
#     customer["Entertainment Bundle"] = (
#         (customer["Streaming TV"] == "Yes").astype(int)
#         + (customer["Streaming Movies"] == "Yes").astype(int)
#     )

#     # Long-Term Customer
#     customer["Long-Term Customer"] = (
#         customer["Tenure Months"] > 24
#     ).astype(int)

#     return customer

def engineer_features(df):

    df = df.copy()

    text_columns = [
        "Gender",
        "Senior Citizen",
        "Partner",
        "Dependents",
        "Phone Service",
        "Multiple Lines",
        "Internet Service",
        "Online Security",
        "Online Backup",
        "Device Protection",
        "Tech Support",
        "Streaming TV",
        "Streaming Movies",
        "Contract",
        "Paperless Billing",
        "Payment Method",
    ]

    for col in text_columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
        )

    # -----------------------------
    # Feature Engineering
    # -----------------------------

    df["New Customer"] = (df["Tenure Months"] <= 12).astype(int)

    df["Avg Monthly Spend"] = (
        df["Total Charges"] /
        df["Tenure Months"].replace(0, 1)
    )

    service_cols = [
        "Phone Service",
        "Multiple Lines",
        "Online Security",
        "Online Backup",
        "Device Protection",
        "Tech Support",
        "Streaming TV",
        "Streaming Movies",
    ]

    df["Total Services"] = (
        df[service_cols] == "yes"
    ).sum(axis=1)

    df["Services_per_Month"] = (
        df["Total Services"] /
        df["Tenure Months"].replace(0, 1)
    )

    df["High_Value"] = (
        df["Monthly Charges"] >
        df["Monthly Charges"].median()
    ).astype(int)

    df["Security Bundle"] = (
        (df["Online Security"] == "yes").astype(int)
        + (df["Device Protection"] == "yes").astype(int)
        + (df["Tech Support"] == "yes").astype(int)
    )

    df["Entertainment Bundle"] = (
        (df["Streaming TV"] == "yes").astype(int)
        + (df["Streaming Movies"] == "yes").astype(int)
    )

    df["Long-Term Customer"] = (
        df["Tenure Months"] > 24
    ).astype(int)

    return df
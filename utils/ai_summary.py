import streamlit as st
from groq import Groq

MODEL = "llama-3.1-8b-instant"  

def _client():
    api_key = st.secrets.get("GROQ_API_KEY") if hasattr(st, "secrets") else None
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except Exception:
        return None


def generate_ai_summary(customer_profile, prediction, risk_factors, protective_factors, recommendations):
    """
    Generate a personalized, business-specific retention strategy for this
    exact customer — not a recap of the SHAP factors. Returns None on ANY
    failure so the caller can fall back gracefully.
    """
    client = _client()
    if client is None:
        return None

    profile_txt = "\n".join(f"- {k}: {v}" for k, v in customer_profile.items())
    risk_txt = "; ".join(risk_factors["Explanation"].tolist()[:4]) or "none identified"
    protective_txt = "; ".join(protective_factors["Explanation"].tolist()[:4]) or "none identified"
    rec_txt = "; ".join(recommendations[:4]) or "no specific action needed"

    prompt = f"""You are a senior customer retention strategist at a telecom company. An account manager is about to call this specific customer and needs a concrete plan, not a recap of the analysis they've already seen on screen.

CUSTOMER PROFILE:
{profile_txt}

MODEL PREDICTION: {prediction['prediction']} — {prediction['probability']:.1f}% churn probability, {prediction['risk_level']} risk

CHURN DRIVERS IDENTIFIED: {risk_txt}
RETENTION FACTORS IDENTIFIED: {protective_txt}
SYSTEM-GENERATED RECOMMENDATIONS: {rec_txt}

Write a detailed, personalized retention strategy for THIS customer. Do not restate or summarize the churn/retention drivers above — the account manager has already seen those. Instead:

1. Briefly interpret what this customer's specific situation (their actual contract, tenure, services, and spend) means in practice — why they're at risk in their own terms, not generic churn theory.
2. Propose ONE concrete, specific offer or intervention tailored to their exact profile — invent a realistic, plausible specific (an exact discount percentage, a named bundle combining services they already show interest in, a specific contract-term incentive, or similar). Do not stay abstract or vague.
3. Explain briefly why this particular offer should work for this particular customer, referencing their actual account details.

Write 2-3 full paragraphs, separated by a blank line between each. Plain business language, no markdown formatting, no bullet points, no headers — this will be read by a non-technical account manager."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.55,
            timeout=15,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None
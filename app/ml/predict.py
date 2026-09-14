import joblib
import pandas as pd

model = joblib.load("app/ml/underwriting_model.pkl")

FEATURE_COLUMNS = [
    "age",
    "income",
    "occupation",
    "policy_amount",
    "previous_claims",
    "credit_score",
    "medical_score",
    "smoker"
]


def predict_risk(customer_data: dict):

    df = pd.DataFrame([customer_data])

    df = df[FEATURE_COLUMNS]

    probability = model.predict_proba(df)[0][1]

    if probability >= 0.75:
        risk = "HIGH"
    elif probability >= 0.25:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "risk": round(float(probability), 4),
        "risk_level": risk
    }
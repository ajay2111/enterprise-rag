def calculate_medical_score(medical_data: dict) -> int:

    score = 0

    diagnoses = [
        diagnosis.lower()
        for diagnosis in medical_data.get("diagnoses", [])
    ]

    # Diabetes
    if any("diabetes" in d for d in diagnoses):
        score += 2

    # Hypertension
    if any(
        "hypertension" in d
        or "high blood pressure" in d
        for d in diagnoses
    ):
        score += 2

    # BMI
    bmi = medical_data.get("bmi")

    if bmi is not None:
        if bmi >= 35:
            score += 3
        elif bmi >= 30:
            score += 2
        elif bmi >= 25:
            score += 1

    # Smoking
    if medical_data.get("smoker") is True:
        score += 2

    return score

def build_ml_features(
    customer_data: dict,
    medical_data: dict
) -> dict:

    medical_score = calculate_medical_score(
        medical_data
    )

    return {
        "age": customer_data["age"],
        "income": customer_data["income"],
        "occupation": customer_data["occupation"],
        "policy_amount": customer_data["policy_amount"],
        "previous_claims": customer_data["previous_claims"],
        "credit_score": customer_data["credit_score"],
        "medical_score": medical_score,
        "smoker": int(
            medical_data.get("smoker") is True
        )
    }


features = build_ml_features(
    customer_data,
    medical_data
)

risk = predict_risk(features)
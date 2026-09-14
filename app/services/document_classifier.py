def classify_document(
    text: str
) -> str:

    text_lower = text.lower()

    medical_keywords = [
        "diagnosis",
        "blood pressure",
        "diabetes",
        "medical",
        "hospital",
        "patient"
    ]

    income_keywords = [
        "salary",
        "income",
        "employer",
        "gross pay",
        "net pay",
        "salary slip"
    ]

    policy_keywords = [
        "policy",
        "premium",
        "coverage",
        "sum assured",
        "exclusions"
    ]

    medical_score = sum(
        keyword in text_lower
        for keyword in medical_keywords
    )

    income_score = sum(
        keyword in text_lower
        for keyword in income_keywords
    )

    policy_score = sum(
        keyword in text_lower
        for keyword in policy_keywords
    )

    scores = {
        "MEDICAL": medical_score,
        "INCOME": income_score,
        "POLICY": policy_score
    }

    return max(
        scores,
        key=scores.get
    )
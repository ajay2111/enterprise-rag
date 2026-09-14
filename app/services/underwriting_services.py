from app.respositries.application_respositery import save_applicant, get_applicant_by_id

def underwrite_applicant(
    db,
    age,
    income,
    credit_score
):
    if age < 18:
        decision = "Rejected"
        message = "Applicant must be at least 18 years old."

    elif income < 0:
        decision = "Rejected"
        message = "Income cannot be negative."

    elif credit_score >= 700:
        decision = "Approved"
        message = "Applicant meets all underwriting criteria."

    else:
        decision = "Review"
        message = "Applicant does not meet underwriting criteria."

    applicant_id = save_applicant(
        db,
        age,
        income,
        credit_score,
        decision
    )

    return {
        "applicant_id": applicant_id,
        "result": decision,
        "message": message
    }

def get_applicant(db, applicant_id):
    return get_applicant_by_id(db, applicant_id)
from app.services.underwriting_services import underwriting_applicant


def test_underwriting_applicant():
    applicant_data = {
        "name": "John Doe",
        "age": 30,
        "income": 50000,
        "credit_score": 700
    }
    result = underwriting_applicant(applicant_data)
    assert result["status"] == "approved"
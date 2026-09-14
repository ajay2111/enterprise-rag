from sqlalchemy.orm import Session
from app.db.models import Applicant


def save_applicant(db: Session, age: int, income: int, credit_score: int, decision: str) -> int:
    applicant = Applicant(
        age=age,
        income=income,
        credit_score=credit_score,
        decision=decision
    )
    db.add(applicant)
    db.commit()
    db.refresh(applicant)
    return applicant.id


def get_applicant_by_id(db: Session, applicant_id: int) -> Applicant:
    return db.get(Applicant, applicant_id)







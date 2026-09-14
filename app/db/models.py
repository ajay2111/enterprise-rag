from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Applicant(Base):
    __tablename__ = "applicants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    income: Mapped[int] = mapped_column(Integer, nullable=False)
    credit_score: Mapped[int] = mapped_column(Integer, nullable=False)
    decision: Mapped[str | None] = mapped_column(String(20), nullable=True)
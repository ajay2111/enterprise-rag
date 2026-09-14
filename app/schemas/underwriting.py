from pydantic import BaseModel, Field

class underwriting_schema(BaseModel):

    age:int = Field(..., description="Age of the applicant", example=30)
    income:float = Field(..., description="Annual income of the applicant", example=50000.0)
    credit_score:int = Field(..., description="Credit score of the applicant", example=700)


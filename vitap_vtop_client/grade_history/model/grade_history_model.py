from pydantic import BaseModel

class GradeHistoryModel(BaseModel):
    credits_registered: str
    credits_earned: str
    cgpa: str

from pydantic import BaseModel
from typing import Optional

class GradeHistoryModel(BaseModel):
    credits_registered: Optional[str] = None
    credits_earned: Optional[str] = None
    cgpa: Optional[str] = None

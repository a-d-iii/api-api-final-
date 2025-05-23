from pydantic import BaseModel
from typing import Optional

from src.grade_history import GradeHistoryModel
from src.mentor import MentorModel


class StudentProfileModel(BaseModel):
    application_number: Optional[str]
    student_name: Optional[str]
    dob: Optional[str]
    gender: Optional[str]
    blood_group: Optional[str]
    email: Optional[str]
    base64_pfp: Optional[str]
    grade_history: Optional[GradeHistoryModel]
    mentor_details: Optional[MentorModel]

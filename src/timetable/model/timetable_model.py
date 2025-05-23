from typing import Dict, List
from pydantic import BaseModel


class Course(BaseModel):
    course_name: str
    slot: str
    venue: str
    faculty: str
    course_code: str
    course_type: str


# One day's schedule: key is the time slot, value is a Course
TimeSlot = Dict[str, Course]


# Weekly timetable: key is the day, value is list of time slots (lectures)
class TimetableModel(BaseModel):
    Monday: List[TimeSlot] = []
    Tuesday: List[TimeSlot] = []
    Wednesday: List[TimeSlot] = []
    Thursday: List[TimeSlot] = []
    Friday: List[TimeSlot] = []
    Saturday: List[TimeSlot] = []
    Sunday: List[TimeSlot] = []

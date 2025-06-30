import asyncio
import argparse
from getpass import getpass
 
from typing import Any

from .client import VtopClient
from .utils import get_semester_name
from .timetable.model import TimetableModel


def _shorten(value: str, max_length: int = 40) -> str:
    """Truncate long strings for friendlier terminal output."""
    if len(value) <= max_length:
        return value
    return f"{value[:20]}...{value[-10:]}"  # show start and end


def _print_timetable(tt: TimetableModel) -> None:
    """Pretty-print a TimetableModel."""
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    for day in days:
        sessions = getattr(tt, day)
        if not sessions:
            continue
        print(day + ":")
        for course in sessions:
            line = (
                f"  {course.time}: {course.course_code} {course.course_name}"
                f" ({course.slot}) @ {course.venue}"
            )
            if course.faculty:
                line += f" - {course.faculty}"
            print(line)
        print()


def _print_lines(obj: Any, indent: int = 0) -> None:
    """Recursively print dictionaries/lists with each entry on its own line."""
    prefix = " " * indent
    if hasattr(obj, "dict"):
        obj = obj.dict(exclude_none=True)

    if isinstance(obj, TimetableModel):
        _print_timetable(obj)
        return

    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                print(f"{prefix}{key}:")
                _print_lines(value, indent + 2)
            elif isinstance(value, str):
                print(f"{prefix}{key}: {_shorten(value)}")
            else:
                print(f"{prefix}{key}: {value}")
    elif isinstance(obj, list):
        for item in obj:
            _print_lines(item, indent)
    else:
        print(f"{prefix}{obj}")
 
async def main():
    parser = argparse.ArgumentParser(description="Command line interface for vitap_vtop_client")
    parser.add_argument("registration_number", help="Your VTOP registration number")
    parser.add_argument(
        "command",
        choices=[
            "profile",
            "attendance",
            "timetable",
            "biometric",
            "grade_history",
            "mentor",
            "exam_schedule",
            "marks",
            "current_semester",
        ],
        help="Which information to fetch",
    )
    parser.add_argument("--password", dest="password", help="VTOP password (will prompt if omitted)")
    parser.add_argument("--sem", dest="sem_sub_id", help="Semester subject ID for semester specific commands")
    parser.add_argument("--date", dest="date", help="Date for biometric in dd/mm/yyyy format")
    args = parser.parse_args()

    password = args.password or getpass("Password: ")

    async with VtopClient(args.registration_number, password) as client:
        if args.command == "profile":
            data = await client.get_profile()
            current_sem = await client.get_current_sem_sub_id()
            sem_name = get_semester_name(current_sem) or current_sem
            data = data.dict(exclude_none=True)
            data["current_semester"] = sem_name
            data["current_sem_sub_id"] = current_sem
        elif args.command == "attendance":
            if not args.sem_sub_id:
                parser.error("attendance command requires --sem")
            data = await client.get_attendance(args.sem_sub_id)
        elif args.command == "timetable":
            data = await client.get_timetable(args.sem_sub_id)
        elif args.command == "biometric":
            if not args.date:
                parser.error("biometric command requires --date")
            data = await client.get_biometric(args.date)
        elif args.command == "grade_history":
            data = await client.get_grade_history()
        elif args.command == "mentor":
            data = await client.get_mentor()
        elif args.command == "exam_schedule":
            data = await client.get_exam_schedule(args.sem_sub_id)
        elif args.command == "marks":
            data = await client.get_marks(args.sem_sub_id)
        elif args.command == "current_semester":
            current_sem = await client.get_current_sem_sub_id()
            sem_name = get_semester_name(current_sem) or current_sem
            data = {
                "current_semester": sem_name,
                "current_sem_sub_id": current_sem,
            }
        else:
            parser.error("Unknown command")

 
        _print_lines(data)
 

if __name__ == "__main__":
    asyncio.run(main())

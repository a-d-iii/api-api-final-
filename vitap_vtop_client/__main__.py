import asyncio
import argparse
from getpass import getpass

from typing import Any

from .client import VtopClient
from .constants import SemSubID


def _shorten(value: str, max_length: int = 40) -> str:
    """Truncate long strings for friendlier terminal output."""
    if len(value) <= max_length:
        return value
    return f"{value[:20]}...{value[-10:]}"  # show start and end


def _print_lines(obj: Any, indent: int = 0) -> None:
    """Recursively print dictionaries/lists with each entry on its own line."""
    prefix = " " * indent

    if hasattr(obj, "model_dump"):
        obj = obj.model_dump(exclude_none=True)
    elif hasattr(obj, "dict"):
        obj = obj.dict(exclude_none=True)

    if isinstance(obj, dict):
        if list(obj.keys()) == ["root"]:
            _print_lines(obj["root"], indent)
            return
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
    parser = argparse.ArgumentParser(
        description="Command line interface for vitap_vtop_client"
    )
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
        ],
        help="Which information to fetch",
    )
    parser.add_argument(
        "--password", dest="password", help="VTOP password (will prompt if omitted)"
    )
    parser.add_argument(
        "--sem",
        dest="sem_sub_id",
        help="Semester subject ID for semester specific commands",
    )
    parser.add_argument(
        "--date", dest="date", help="Date for biometric in dd/mm/yyyy format"
    )
    args = parser.parse_args()

    password = args.password or getpass("Password: ")

    async with VtopClient(args.registration_number, password) as client:
        if args.command == "profile":
            data = await client.get_profile(include_timetables=True)
            try:
                if args.sem_sub_id:
                    data.marks = {
                        args.sem_sub_id: await client.get_marks(args.sem_sub_id)
                    }
                else:
                    data.marks = await client.get_all_marks()
            except Exception as e:
                print(f"Failed to fetch marks: {e}")
        elif args.command == "attendance":
            if not args.sem_sub_id:
                parser.error("attendance command requires --sem")
            data = await client.get_attendance(args.sem_sub_id)
        elif args.command == "timetable":
            if not args.sem_sub_id:
                parser.error("timetable command requires --sem")
            data = await client.get_timetable(args.sem_sub_id)
        elif args.command == "biometric":
            if not args.date:
                parser.error("biometric command requires --date")
            data = await client.get_biometric(args.date)
        elif args.command == "grade_history":
            data = await client.get_grade_history()
        elif args.command == "mentor":
            data = await client.get_mentor()
        else:
            parser.error("Unknown command")

        _print_lines(data)

        if args.command == "profile":
            if data.marks is None:
                print("Marks: not retrieved")
            elif isinstance(data.marks, dict) and not data.marks:
                print("Marks: {}")


if __name__ == "__main__":
    asyncio.run(main())

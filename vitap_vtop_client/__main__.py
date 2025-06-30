import asyncio
import argparse
from getpass import getpass
from .client import VtopClient

async def main():
    parser = argparse.ArgumentParser(description="Command line interface for vitap_vtop_client")
    parser.add_argument("registration_number", help="Your VTOP registration number")
    parser.add_argument("command", choices=["profile", "attendance", "timetable", "biometric", "grade_history", "mentor"], help="Which information to fetch")
    parser.add_argument("--password", dest="password", help="VTOP password (will prompt if omitted)")
    parser.add_argument("--sem", dest="sem_sub_id", help="Semester subject ID for semester specific commands")
    parser.add_argument("--date", dest="date", help="Date for biometric in dd/mm/yyyy format")
    args = parser.parse_args()

    password = args.password or getpass("Password: ")

    async with VtopClient(args.registration_number, password) as client:
        if args.command == "profile":
            data = await client.get_profile()
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

        print(data)

if __name__ == "__main__":
    asyncio.run(main())

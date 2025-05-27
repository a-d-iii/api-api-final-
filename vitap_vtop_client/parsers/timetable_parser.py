from bs4 import BeautifulSoup
from vitap_vtop_client.exceptions import VtopParsingError
from vitap_vtop_client.timetable.model import TimetableModel

# TODO: Use pandas to parse the timetable
# Current implementation is very sensitive to changes


theory_timings = [
    "DAY",
    "TYPE",
    "08:00 - 08:50",
    "09:00 - 09:50",
    "09:00 - 09:50",
    "10:00 - 10:50",
    "10:00 - 10:50",
    "11:00 - 11:50",
    "11:00 - 11:50",
    "12:00 - 12:50",
    "12:00 - 12:50",
    "13:00 - 13:50",
    "Lunch",
    "14:00 - 14:50",
    "14:00 - 14:50",
    "15:00 - 15:50",
    "15:00 - 15:50",
    "16:00 - 16:50",
    "16:00 - 16:50",
    "17:00 - 17:50",
    "17:00 - 17:50",
    "18:00 - 18:50",
    "18:00 - 18:50",
    "19:00 - 19:50",
]

lab_timings = [
    "TYPE",
    "08:00 - 08:50",
    "09:00 - 09:50",
    "09:00 - 09:50",
    "09:50 - 10:40",
    "09:50 - 10:40",
    "11:00 - 11:50",
    "11:00 - 11:50",
    "11:50 - 12:40",
    "11:50 - 12:40",
    "12:50 - 13:30",
    "Lunch",
    "14:00 - 14:50",
    "14:00 - 14:50",
    "14:50 - 15:40",
    "14:50 - 15:40",
    "16:00 - 16:50",
    "16:00 - 16:50",
    "16:50 - 17:40",
    "16:50 - 17:40",
    "18:00 - 18:50",
    "18:00 - 18:50",
    "18:50 - 19:30",
]


def get_course_info(html: str) -> list:
    """
    Parses the HTML content of a timetable table and extracts timetable details
    for each day into TimetableModel.

    Args:
        html (str): The raw HTML string containing the  timetable table.

    Returns:
        TimetableModel: A list of days, each representing the course schedule for that particualr day.

    Raises:
        VtopParsingError: When failed to parse attendance data(usually due to unexpected html format).
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find_all("tr")
        courses_list = []

        for row in rows:
            cells = row.find_all("td")
            if cells and len(cells) >= 10:
                try:
                    course_p = cells[2].find("p")
                    if course_p is not None:
                        course = course_p.get_text().strip()
                        course_code, course_name = course.split(" - ", 1)

                        venue = "N/A"
                        slot = "N/A"
                        venue_p = cells[7].find_all("p")
                        if venue_p:
                            slot = (venue_p[0]).get_text().strip()
                            venue = (venue_p[1]).get_text().strip()

                        faculty = "N/A"
                        faculty_p = cells[8].find_all("p")
                        if faculty_p:
                            faculty = (faculty_p[0]).get_text().split("-")[0]

                        courses_list.append(
                            {
                                str(course_code): {
                                    "course_name": course_name,
                                    "venue": venue,
                                    "slot": slot,
                                    "faculty": faculty,
                                }
                            }
                        )
                except Exception:
                    continue
        return courses_list
    except Exception as e:
        raise VtopParsingError(f"Error parsing course information: {e}")


def update_timetable_with_course_info(
    timetable_data: dict[str, list], courses_list: list
) -> TimetableModel:
    try:
        for day, timeslots in timetable_data.items():
            for slot in range(len(timeslots)):
                for timeslot, course_info in timeslots[slot].items():
                    course_code = course_info.split("-")[1]
                    course_venue = str(
                        course_info.split("-")[3] + "-" + course_info.split("-")[4]
                    )
                    course_type = course_info.split("-")[2]

                    for course in courses_list:
                        if course_code in course:
                            course_data = course[course_code]
                            venue_match = course_data["venue"].split("-")
                            if course_venue == f"{venue_match[0]}-{venue_match[1]}":
                                timetable_data[day][slot][timeslot] = {
                                    "course_name": course_data["course_name"],
                                    "slot": course_data["slot"],
                                    "venue": course_data["venue"],
                                    "faculty": course_data["faculty"],
                                    "course_code": course_code,
                                    "course_type": course_type,
                                }
        return TimetableModel(**timetable_data)
    except Exception as e:
        raise VtopParsingError(f"Error updating timetable with course info: {e}")


def parse_time_table(html: str) -> TimetableModel:
    time_table_data = {
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": [],
        "Monday": [],
    }

    lst_table = []

    try:
        soup = BeautifulSoup(html, "html.parser")
        time_table = soup.find(id="timeTableStyle")

        if not time_table:
            print("Timetable not found for the given semester")
            return TimetableModel()

        tr_tags = time_table.find_all("tr")[4:]
        for tr_tag in tr_tags:
            tr_string = str(tr_tag.get_text(strip=False))
            lines = list(filter(None, tr_string.split("\n")))
            lst_table.append(lines)

        for day, line in zip(
            ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], lst_table[::2]
        ):
            for j in range(min(len(line), len(theory_timings))):
                if len(line[j]) > 8 and line[j] not in {"CLUBS/ECS", "ECS/CLUBS"}:
                    time_table_data[day].append({theory_timings[j]: line[j]})

        for day, line in zip(
            ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], lst_table[1::2]
        ):
            for j in range(min(len(line), len(lab_timings))):
                if line[j] not in {"-", "Lunch", ""}:
                    time_slot = lab_timings[j]
                    time_table_data[day].append({time_slot: line[j]})

        for day, sessions in time_table_data.items():
            time_table_data[day] = [
                session
                for session in sessions
                if all(len(value) >= 8 for value in session.values())
            ]

        courses_list = get_course_info(html)
        return update_timetable_with_course_info(time_table_data, courses_list)

    except Exception as e:
        raise VtopParsingError(f"Failed to parse timetable: {e}")

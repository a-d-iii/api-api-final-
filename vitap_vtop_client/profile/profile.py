import httpx
import time
import asyncio
from vitap_vtop_client.constants import PROFILE_URL, HEADERS, SemSubID
from vitap_vtop_client.mentor import fetch_mentor_info
from vitap_vtop_client.grade_history import fetch_grade_history
from vitap_vtop_client.parsers.profile_parser import parse_student_profile
from .model import StudentProfileModel
from vitap_vtop_client.timetable import fetch_timetable
from vitap_vtop_client.academic_headings import fetch_academic_headings

from vitap_vtop_client.exceptions import VtopConnectionError, VtopProfileError, VtopParsingError

async def fetch_profile(
    client: httpx.AsyncClient,
    registration_number: str,
    csrf_token: str,
    include_timetables: bool = False,
    include_academic_headings: bool = False,
) -> StudentProfileModel:
    """
    Retrieves and compiles the student profile information from the VTOP Portal.

    Parameters:
        client (httpx.AsyncClient): The async HTTP client.
        registration_number (str): The student's username.
        csrf_token (str): CSRF token for authentication.
        include_timetables (bool): When True, fetches timetable for all semesters.
        include_academic_headings (bool): When True, fetches headings from the VTOP content page.

    Returns:
        StudentProfileModel: The student's profile information. If
        include_timetables is True, the profile will include timetable
        information for all semesters available in ``SemSubID``. If
        ``include_academic_headings`` is True, ``academic_headings`` will
        contain the list of headings from the content page.

    Raises:
        VtopConnectionError: If an HTTP request fails.
        VtopProfileError: If initialization or data fetch fails.
        VtopParsingError: If parsing fails.
    """
    try:
        data = {
            'verifyMenu': 'true',
            'authorizedID': registration_number,
            '_csrf': csrf_token,
            'nocache': int(round(time.time() * 1000))
        }

        response = await client.post(PROFILE_URL, data=data, headers=HEADERS)
        response.raise_for_status()

        # Now add nested fields
        profile = parse_student_profile(response.text)
        profile.grade_history = await fetch_grade_history(client, registration_number, csrf_token)
        profile.mentor_details = await fetch_mentor_info(client, registration_number, csrf_token)

        if include_timetables:
            profile.timetables = {}
            tasks = {
                name: asyncio.create_task(
                    fetch_timetable(
                        client=client,
                        username=registration_number,
                        semSubID=sem_id,
                        csrf_token=csrf_token,
                    )
                )
                for name, sem_id in SemSubID.items()
            }
            for name, task in tasks.items():
                try:
                    profile.timetables[name] = await task
                except Exception:
                    profile.timetables[name] = None

        if include_timetables or include_academic_headings:
            profile.academic_headings = await fetch_academic_headings(client)

        return profile

    except VtopParsingError as e:
        raise e

    except httpx.RequestError as e:
        print(f"Student profile fetch failed: {e}")
        raise VtopConnectionError(
            f"Failed to fetch student profile: {e}",
            original_exception=e,
            status_code=502
        )
    except Exception as e:
        print(f"An unexpected error occurred while fetching student profile: {e}")
        raise VtopProfileError(f"Unexpected error while fetching student profile: {e}") from e

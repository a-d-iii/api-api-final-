import httpx
import time
from datetime import datetime, timezone
from src.parsers import attendance_parser
from src.constants import VIEW_ATTENDANCE_URL, ATTENDANCE_URL, HEADERS

async def get_attendance(
    client: httpx.AsyncClient,
    username: str,
    semSubID: str,
    csrf_token: str
) -> dict:
    """
    Retrieves the attendance details for a specific user and semester subject.

    Parameters:
        client (httpx.AsyncClient): The active httpx async client.
        username (str): The username of the student.
        semSubID (str): The identifier for the semester subject.
        csrf_token (str): The CSRF token.

    Returns:
        dict: A dictionary containing the parsed attendance data.

    Raises:
        httpx.RequestError: If an HTTP request fails.
        ValueError: If the initial POST or the attendance data request fails or returns unexpected content.
        Exception: For parsing errors.
    """
    try:
        # First POST to verify menu/session
        data_initial = {
            "verifyMenu": "true",
            "authorizedID": username,
            "_csrf": csrf_token,
            "nocache": int(round(time.time() * 1000)),
        }
        # Use await client.post
        initial_response = await client.post(ATTENDANCE_URL, data=data_initial, headers=HEADERS)
        initial_response.raise_for_status() # Raise exception for bad status codes

        # Check if the initial POST was successful in setting up the page context
        # This might involve checking the response content or status,
        # but raise_for_status is a good start for HTTP errors.
        # More specific checks might be needed based on VTOP's responses.

    except httpx.RequestError as e:
        print(f"Attendance initial POST failed: {e}")
        raise ValueError(f"Failed to initialize attendance page: {e}") from e
    except Exception as e:
         print(f"An unexpected error occurred during attendance initial POST: {e}")
         raise ValueError(f"Failed to initialize attendance page: {e}") from e

    try:
        # Second POST to fetch attendance data
        data_fetch = {
            "_csrf": csrf_token,
            "semesterSubId": semSubID,
            "authorizedID": username,
            "x": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT"),
        }
        # Use await client.post
        attendance_response = await client.post(VIEW_ATTENDANCE_URL, data=data_fetch, headers=HEADERS)
        attendance_response.raise_for_status() # Raise exception for bad status codes

        # Check response content for VTOP-specific errors before parsing
        # Example: check if the response contains a known error message div/span
        if "Invalid semester subject ID" in attendance_response.text: # Example error check
             raise ValueError(f"Invalid semester subject ID: {semSubID}")
        # Add other specific VTOP error checks here

        # Parse the HTML content
        parsed_data = attendance_parser.parse_attendance(attendance_response.text)

        # Check if parser returned an error (if parser handles errors by returning dict with "error")
        if isinstance(parsed_data, dict) and "error" in parsed_data:
             # If parser returns error dict, raise an exception
             raise ValueError(f"Failed to parse attendance data: {parsed_data['error']}")

        return parsed_data

    except httpx.RequestError as e:
        print(f"Attendance data fetch failed: {e}")
        raise ValueError(f"Failed to fetch attendance data: {e}") from e
    except ValueError as e:
         # Re-raise ValueErrors from content checks or parser errors
         raise e
    except Exception as e:
        print(f"An unexpected error occurred while fetching or parsing attendance: {e}")
        raise Exception(f"An unexpected error occurred: {e}") from e # Wrap unexpected errors
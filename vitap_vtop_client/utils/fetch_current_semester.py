import time
import httpx
from vitap_vtop_client.constants import MARKS_URL, HEADERS
from vitap_vtop_client.utils.find_current_semester import find_current_sem_sub_id
from vitap_vtop_client.exceptions.exception import VtopConnectionError, VtopSessionError


async def fetch_current_sem_sub_id(
    client: httpx.AsyncClient,
    registration_number: str,
    csrf_token: str,
) -> str:
    """Retrieve the current semesterSubId using the marks page."""
    try:
        init_data = {
            "verifyMenu": "true",
            "authorizedID": registration_number,
            "_csrf": csrf_token,
            "nocache": int(round(time.time() * 1000)),
        }
        response = await client.post(MARKS_URL, data=init_data, headers=HEADERS)
        response.raise_for_status()
        sem = find_current_sem_sub_id(response.text)
        if not sem:
            raise VtopSessionError("Unable to determine current semester")
        return sem
    except httpx.RequestError as e:
        raise VtopConnectionError(
            f"Failed to determine current semester: {e}", original_exception=e, status_code=502
        )

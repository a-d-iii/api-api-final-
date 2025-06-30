import httpx
from bs4 import BeautifulSoup

from vitap_vtop_client.constants import VTOP_CONTENT_URL, HEADERS
from vitap_vtop_client.exceptions import VtopConnectionError, VtopParsingError


async def fetch_academic_headings(client: httpx.AsyncClient) -> list[str]:
    """Fetch sub-headings listed under the ``ACADEMICS`` menu on the VTOP content page."""
    try:
        response = await client.get(VTOP_CONTENT_URL, headers=HEADERS)
        response.raise_for_status()
    except httpx.RequestError as e:
        raise VtopConnectionError(
            f"Failed to load VTOP content page: {e}",
            original_exception=e,
            status_code=502,
        )

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        academics_tag = soup.find(lambda tag: tag.get_text(strip=True).upper() == "ACADEMICS")
        if not academics_tag:
            return []
        menu = academics_tag.find_next("ul")
        if not menu:
            return []
        return [li.get_text(strip=True) for li in menu.find_all("li")]
    except Exception as e:
        raise VtopParsingError(f"Failed to parse academic headings: {e}") from e

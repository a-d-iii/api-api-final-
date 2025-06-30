import httpx
from bs4 import BeautifulSoup

from vitap_vtop_client.constants import VTOP_CONTENT_URL, HEADERS
from vitap_vtop_client.exceptions import VtopConnectionError, VtopParsingError


async def fetch_academic_headings(client: httpx.AsyncClient) -> list[str]:
    """Fetch all heading text present on the VTOP content page."""
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
        return [tag.get_text(strip=True) for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
    except Exception as e:
        raise VtopParsingError(f"Failed to parse academic headings: {e}") from e

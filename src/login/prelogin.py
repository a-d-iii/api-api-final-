import httpx
from src.constants import VTOP_PRELOGIN_INIT_URL, VTOP_URL, HEADERS, VTOP_PRELOGIN_URL 
from src.utils import find_csrf
import asyncio

async def fetch_csrf_token(client: httpx.AsyncClient, max_retries: int = 3) -> str | None:
    """
    Fetches CSRF token from the VTOP website using an async client.

    Args:
        client (httpx.AsyncClient): Async client object for making HTTP requests.
        max_retries (int): Maximum attempts to fetch the token.

    Returns:
        str or None: CSRF token if found, otherwise None after retries.

    Raises:
        httpx.RequestError: If the HTTP request fails after all retries.
        ValueError: If CSRF token is not found in the response after all retries.
        Exception: For unexpected errors.
    """
    for attempt in range(max_retries):
        print(f"Fetching initial CSRF token, attempt {attempt + 1}/{max_retries}...")
        try:
            # Use await client.get
            response = await client.get(VTOP_URL, headers=HEADERS)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

            csrf_token = find_csrf.find_csrf(response.text) # Use the refactored utility

            if csrf_token: # Check if utility returned a value (not None)
                print("Initial CSRF token found.")
                return csrf_token
            else:
                print("Initial CSRF token not found in response.")
                if attempt < max_retries - 1:
                    print("Retrying fetch_csrf_token...")
                    await asyncio.sleep(1) # Small delay before retry
                else:
                     # Raise error if token not found after retries
                     raise ValueError(f"Initial CSRF token not found in response after {max_retries} attempts.")

        except httpx.RequestError as e:
            print(f"Failed to fetch initial CSRF token page: {e}")
            if attempt < max_retries - 1:
                 print("Retrying fetch_csrf_token...")
                 await asyncio.sleep(1)
            else:
                raise httpx.RequestError(f"Failed to fetch initial CSRF token page after {max_retries} attempts: {e}") from e
        except ValueError as e:
            # Re-raise ValueError if token not found
            raise e
        except Exception as e:
            print(f"An unexpected error occurred during fetch_csrf_token attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                 print("Retrying fetch_csrf_token...")
                 await asyncio.sleep(1)
            else:
                raise Exception(f"An unexpected error occurred during fetch_csrf_token after {max_retries} attempts: {e}") from e

    # Should not be reached if exceptions are raised correctly
    return None


async def pre_login(client: httpx.AsyncClient, csrf_token: str) -> None:
    """
    Sends async pre-login request to VTOP website using an async client.
    This request seems to be necessary to set session state before actual login.

    Args:
        client (httpx.AsyncClient): Async client object for making HTTP requests.
        csrf_token (str): CSRF token fetched from the initial page.

    Returns:
        None

    Raises:
        httpx.RequestError: If the HTTP request fails.
        ValueError: If the pre-login request does not succeed based on response status.
        Exception: For unexpected errors.
    """
    try:
        data = {'_csrf': csrf_token, 'flag': 'VTOP'}
        # Use await client.post
        response = await client.post(VTOP_PRELOGIN_URL, data=data, headers=HEADERS)

        if(response.status_code < 400):
            print("Pre-login successful.")

    except httpx.RequestError as e:
        print(f"Pre-login request failed unexpectedly: {e}")
        raise httpx.RequestError(f"Pre-login request failed: {e}") from e
    except Exception as e:
        print(f"Pre-login failed unexpectedly: {e}")
        raise Exception(f"Pre-login failed: {e}") from e
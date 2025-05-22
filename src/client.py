import string
import httpx
import asyncio

from src.exceptions.exception import (
    VtopLoginError,
    VtopCaptchaError,
    VtopConnectionError,
    VtopSessionError,
    VitapVtopClientError
)

from src.login.fetch_csrf_token import fetch_csrf_token
from src.login.model.logged_in_student_model import LoggedInStudent
from src.login.prelogin import pre_login
from src.login.fetch_captcha import fetch_captcha
from src.utils.solve_captcha import solve_captcha
from src.login.student_login import student_login


async def login(
    client: httpx.AsyncClient,
    username: str,
    password: str,
    max_retries: int = 3,
    captcha_retries: int = 5
) -> LoggedInStudent:
    """
    Performs the full VTOP login sequence asynchronously.
    Raises descriptive exceptions on failure.
    """
    if not username or not password:
        raise VtopLoginError("Username and password are required.", status_code=400)
    if len(username) < 5 or any(c in string.punctuation for c in username):
        raise VtopLoginError("Invalid username format.", status_code=400)

    for attempt in range(max_retries):
        print(f"Overall login attempt {attempt + 1}/{max_retries} for user {username}")
        try:
            # Step 1: Fetch initial CSRF token
            csrf_token = await fetch_csrf_token(client)
            print(f"CSRF TOKEN: {csrf_token}")

            # Step 2: Pre-login setup
            await pre_login(client, csrf_token)

            # Step 3: Fetch and solve CAPTCHA
            captcha_base64 = await fetch_captcha(client, retries=captcha_retries)
            captcha_value = await asyncio.to_thread(solve_captcha, captcha_base64)

            if not captcha_value:
                raise VtopCaptchaError("Failed to solve captcha.", status_code=422)

            print(f"Solved captcha: {captcha_value}")

            # Step 4: Attempt login
            login_result = await student_login(
                client, csrf_token, username, password, captcha_value
            )

            return login_result

        except VtopCaptchaError as e:
            print(f"Captcha error: {e}")
            if attempt < max_retries - 1:
                print("Retrying entire login due to captcha error...")
                await asyncio.sleep(2 ** attempt)
                continue
            raise

        except VtopLoginError as e:
            print(f"Login failed due to credentials or format: {e}")
            raise  # No point retrying invalid inputs

        except VtopConnectionError as e:
            print(f"Connection error during login: {e}")
            if attempt < max_retries - 1:
                print("Retrying login sequence due to connection error...")
                await asyncio.sleep(2 ** attempt)
                continue
            raise

        except VtopSessionError as e:
            print(f"Session error (e.g., CSRF/session expired): {e}")
            if attempt < max_retries - 1:
                print("Retrying login sequence due to session error...")
                await asyncio.sleep(2 ** attempt)
                continue
            raise

        except VitapVtopClientError as e:
            print(f"Other known VTOP client error: {e}")
            if attempt < max_retries - 1:
                print("Retrying login sequence due to client error...")
                await asyncio.sleep(2 ** attempt)
                continue
            raise

        except Exception as e:
            print(f"Unexpected error during login: {e}")
            if attempt < max_retries - 1:
                print("Retrying login sequence due to unexpected error...")
                await asyncio.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Login failed after {max_retries} attempts due to unexpected error: {e}") from e

    raise RuntimeError(f"Login failed for user {username} after {max_retries} attempts.")
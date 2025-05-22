import httpx
from src.constants import VTOP_LOGIN_ERROR_ROUTE, VTOP_LOGIN_INIT_ROUTE, VTOP_LOGIN_URL, VTOP_CONTENT_URL, VTOP_LOGIN_ERROR_URL, HEADERS
from src.utils import find_login_response
from src.utils import find_csrf 


async def login(
    client: httpx.AsyncClient,
    csrf_token: str,
    username: str,
    password: str,
    captcha_value: str,
) -> dict | None: # Changed return type to dict on success, raise on failure
    """
    Attempts to log in to the VTOP system using provided credentials and captcha.

    Args:
        client (httpx.AsyncClient): Async client object for making HTTP requests.
        csrf_token (str): Cross-Site Request Forgery token required for the login request (from pre-login).
        username (str): Username for logging in.
        password (str): Password for logging in.
        captcha_value (str): Value of the CAPTCHA image solved by the solver.

    Returns:
        dict: A dictionary containing login success status and potentially the
              post-login CSRF token. Example: {"success": True, "message": "Logged in", "post_login_csrf": "..."}

    Raises:
        httpx.RequestError: If a network-related issue occurs during the POST request.
        ValueError: If login fails due to invalid credentials or captcha.
        RuntimeError: If the login succeeds but the expected post-login page or CSRF is not found.
        Exception: For other unexpected issues.
    """
    try:
        data = {
            "_csrf": csrf_token,
            "username": username,
            "password": password,
            "captchaStr": captcha_value,
        }
        response = await client.post(VTOP_LOGIN_URL, data=data, headers=HEADERS)
        print(response.text)
        print(response.url)
        print(response.cookies)
        print(response.headers.get("Location"))
        # Don't raise_for_status immediately
        final_url = response.url

        if (response.has_redirect_location):
            print(response.headers.get("Location"))
            if(response.headers.get("Location") == VTOP_LOGIN_INIT_ROUTE):
                print(f"Login successful for user {username}. Redirected to content page.")
                # After successful login, we need to get the CSRF token from the content page
                # for subsequent requests.
                content_resp = await client.get(VTOP_CONTENT_URL, headers=HEADERS)
                print(content_resp.text)
                print(content_resp.url)

                post_login_csrf = find_csrf.find_csrf(content_resp.text)

                if post_login_csrf is None:
                    # This is a critical failure: login succeeded but couldn't get the necessary token for later
                    raise RuntimeError("Login successful, but failed to find post-login CSRF token.")

                return {"success": True, "message": f"Logged in Successfully as {username}", "post_login_csrf": post_login_csrf}
            elif(response.status_code == 302 and (response.headers.get("Location") == VTOP_LOGIN_ERROR_ROUTE)):
                response = await client.get(VTOP_LOGIN_ERROR_URL, headers=HEADERS)
                error_message = find_login_response.login_error_identifier(response.text)
                print(f"Err: ${error_message}")
                ValueError(f"Login Credential Error: ${error_message}")

        elif  (response.status_code == 404): #final_url.startswith(VTOP_LOGIN_ERROR_URL) or
            # Check for the specific error page or a 404 on the login URL itself
            error_message = find_login_response.login_error_identifier(response.text) # Use the refactored utility

            if error_message:
                 print(f"Login failed for user {username}: {error_message}")
                 # Use ValueError for input/credential errors
                 raise ValueError(f"Login failed: {error_message}")
            else:
                 # If we landed on the error page but couldn't find the specific message
                 print(f"Login failed for user {username}. Generic error page or 404 received. Status: {response.status_code}")
                 # Raise a general error indicating failure
                 raise RuntimeError(f"Login failed: Could not identify specific error message (Status: {response.status_code})")

        else:
            # Landed on an unexpected page after login POST
            print(f"Login failed for user {username}. Unexpected redirection to {final_url}. Status: {response.status_code}")
            raise RuntimeError(f"Login failed: Unexpected redirection after POST to {final_url} (Status: {response.status_code})")

    except httpx.RequestError as e:
        print(f"Login POST request failed: Network Error {e}")
        raise httpx.RequestError(f"Login request failed: {e}") from e # Re-raise with context
    except (ValueError, RuntimeError) as e:
         # Re-raise known login failure types
         raise e
    except Exception as e:
        print(f"An unexpected error occurred during login process: {e}")
        raise Exception(f"An unexpected error occurred during login: {e}") from e # Wrap unexpected errors
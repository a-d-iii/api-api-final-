import httpx
import asyncio
from src.login.prelogin import fetch_csrf_token, pre_login
from src.login.captcha_solver import fetch_captcha, solve_captcha
from src.login import login

async def login_main(
    client: httpx.AsyncClient,
    username: str,
    password: str,
    max_retries: int = 3,
    captcha_retries: int = 2 # Retries specifically for captcha solving within one login attempt
) -> dict: # Return dict containing auth details and maybe user info later
    """
    Performs the full VTOP login sequence asynchronously.

    Args:
        client: The httpx.AsyncClient instance to use.
        username: VTOP username (registration number).
        password: VTOP password.
        max_retries: Maximum attempts for the overall login process (including captcha issues).
        captcha_retries: Maximum attempts to solve the captcha within a single login attempt.

    Returns:
        dict: A dictionary containing authentication details (e.g., username, csrf_token)
              and potentially other initial user info fetched after login.
              Example: {"username": "...", "csrf_token": "...", "message": "..."}

    Raises:
        ValueError: If input credentials are invalid or format is wrong.
        httpx.RequestError: If a network error prevents communication with VTOP.
        RuntimeError: If VTOP returns a persistent error or internal logic fails.
        Exception: For any other unexpected errors.
    """
    if not username or not password:
         raise ValueError("Username and password are required.")
    if len(username) < 5:
         # Basic validation based on original handle_login, refine as needed
         raise ValueError("Invalid username format.")


    for attempt in range(max_retries):
        print(f"Overall login attempt {attempt + 1}/{max_retries} for user {username}")
        try:
            # 1. Fetch initial CSRF token
            # fetch_csrf_token already has retries internally now
            csrf_token = await fetch_csrf_token(client)
            print(f"CSRF TOKEN: {csrf_token}")
            # fetch_csrf_token raises ValueError if not found after retries

            # 2. Perform pre-login (might require the fetched CSRF token)
            await pre_login(client, csrf_token)
            # pre_login raises exceptions on failure

            # 3. Fetch and Solve CAPTCHA
            # fetch_and_display_captcha already has retries internally now
            captcha_base64 = await fetch_captcha(client)
            # fetch_and_display_captcha raises ValueError if not found after retries

            # Solve captcha (synchronous CPU-bound task)
            # Run in a thread pool to avoid blocking the event loop
            captcha_value = await asyncio.to_thread(solve_captcha, captcha_base64)

            if not captcha_value: # Check if solver failed or returned None
                 print("Captcha solver failed to produce a valid value.")
                 # This is a critical step, if solving fails, retry the whole login sequence (get new captcha)
                 raise ValueError("Failed to solve captcha.")


            print(f"Solved captcha: {captcha_value}")

            # 4. Attempt actual login
            # perform_login handles VTOP's responses and raises specific exceptions
            login_result = await login.login(
                client, csrf_token, username, password, captcha_value
            )

            # If perform_login returns successfully, it means login worked
            # It also already fetches the post-login CSRF token
            # Return the necessary details from the result dictionary
            return {
                "username": username, # Keep track of the logged-in username
                "csrf_token": login_result["post_login_csrf"], # This is the CSRF needed for subsequent calls
                "message": login_result["message"] # Success message
                # Add any other crucial info returned by perform_login or fetched immediately after login
            }


        except (httpx.RequestError, ValueError, RuntimeError) as e:
            # Catch specific exceptions raised by the steps
            print(f"Error during overall login attempt {attempt + 1}: {e}")

            # Decide based on error type if retrying is appropriate
            # Network errors or VTOP internal errors (RuntimeError) are good candidates for retry
            # Invalid credentials or persistent "captcha not found" (ValueErrors) usually mean no point retrying the same inputs
            if isinstance(e, ValueError) and ("credentials" in str(e).lower() or "captcha" in str(e).lower()):
                 # Specific input errors - do not retry with same input
                 raise e # Re-raise the specific error immediately
            elif attempt < max_retries - 1:
                print("Retrying login sequence...")
                await asyncio.sleep(2**attempt) # Exponential backoff delay
                continue # Go to the next overall attempt
            else:
                print(f"Max overall retries reached. Login failed for user {username}.")
                raise e # Re-raise the last error


        except Exception as e:
             # Catch any other unexpected errors
             print(f"An unexpected error occurred during overall login attempt {attempt + 1}: {e}")
             if attempt < max_retries - 1:
                print("Retrying login sequence due to unexpected error...")
                await asyncio.sleep(2**attempt) # Exponential backoff delay
                continue # Go to the next overall attempt
             else:
                print(f"Max overall retries reached. Login failed for user {username}.")
                raise Exception(f"Login failed after {max_retries} attempts due to unexpected error: {e}") from e


    # This point should ideally not be reached if all attempts raise exceptions
    raise RuntimeError(f"Login process completed without success or clear failure reason for user {username}.")


# You might add other top-level functions here later
# e.g., async def get_profile(client: httpx.AsyncClient, username: str, csrf_token: str) -> dict: ...
# These would call the corresponding functions from other files (profile.py etc.)

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:
        result = await login_main(
            client=client,
            username="23BCE7625",
            password="g4st=sTevi"
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
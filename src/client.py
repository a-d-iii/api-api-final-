import string
import httpx
import asyncio

from src.attendance.model.attendance_model import AttendanceModel

from .exceptions.exception import (
    VtopLoginError,
    VtopCaptchaError,
    VtopConnectionError,
    VtopSessionError,
    VitapVtopClientError
)
from .login import (
    fetch_csrf_token,
    pre_login,
    fetch_captcha,
    student_login
)
from .login.model import LoggedInStudent # Ensure this import path is correct
from .utils.solve_captcha import solve_captcha # Assuming this utility exists

# Import your specific data fetching functions
from .attendance.attendance import get_attendance as fetch_attendance_data
# from .timetable.timetable import get_timetable as fetch_timetable_data # Example
# from .marks.marks import get_marks as fetch_marks_data # Example
# ... and so on for other features

class VtopClient:
    """
    An asynchronous client for interacting with the VIT-AP VTOP portal.
    """
    def __init__(self, username: str, password: str, max_login_retries: int = 3, captcha_retries: int = 5):
        """
        Initializes the VtopClient.

        Args:
            username: The VTOP registration number.
            password: The VTOP password.
            max_login_retries: Maximum number of overall login attempts.
            captcha_retries: Maximum number of captcha fetch/solve attempts per login.
        """
        if not username or not password:
            raise VtopLoginError("Username and password are required for VtopClient.", status_code=400)
        # TODO: Basic validation, improve this
        if len(username) < 5 or any(c in string.punctuation for c in username):
            raise VtopLoginError("Invalid username format for VtopClient.", status_code=400)

        self.username = username.upper()
        self.password = password
        self._client = httpx.AsyncClient(timeout=30.0, follow_redirects=True, )
        self._logged_in_student: LoggedInStudent | None = None
        self.max_login_retries = max_login_retries
        self.captcha_retries = captcha_retries
        self._login_lock = asyncio.Lock() # Prevents concurrent login attempts

    async def _perform_login_sequence(self) -> LoggedInStudent:
        """
        Handles the complete login sequence.
        This sequence must be performed everytime when a user needs something. 
        """
        for attempt in range(self.max_login_retries):
            print(f"VtopClient: Login attempt {attempt + 1}/{self.max_login_retries} for user {self.username}")
            try:
                # Step 1: Fetch initial CSRF token
                csrf_token = await fetch_csrf_token(self._client)
                print(f"VtopClient: CSRF TOKEN: {csrf_token}")

                # Step 2: Pre-login setup
                await pre_login(self._client, csrf_token)

                # Step 3: Fetch and solve CAPTCHA
                captcha_base64 = await fetch_captcha(self._client, retries=self.captcha_retries)
                captcha_value = await asyncio.to_thread(solve_captcha, captcha_base64)
                print(f"VtopClient: Solved captcha: {captcha_value}")

                # Step 4: Attempt login
                logged_in_student = await student_login(
                    self._client, csrf_token, self.username, self.password, captcha_value
                )
                self._logged_in_student = logged_in_student
                print(f"VtopClient: Login successful for {self.username}")
                return logged_in_student

            except VtopCaptchaError as e:
                print(f"VtopClient: Captcha error during login: {e}")
                if attempt == self.max_login_retries - 1: raise
                await asyncio.sleep(1) # Wait a bit before retrying captcha
            except VtopLoginError as e: # Typically for bad credentials
                print(f"VtopClient: Login failed due to invalid credentials or format: {e}")
                raise # No point retrying if credentials are bad
            except VtopConnectionError as e:
                raise

            except VtopSessionError as e:
                print(f"Session error (e.g., CSRF/session expired): {e}")
                raise
            except Exception as e:
                print(f"VtopClient: Unexpected error during login: {e}")
                if attempt == self.max_login_retries - 1:
                    raise VitapVtopClientError(f"Login failed after {self.max_login_retries} attempts due to unexpected error: {e}")
                await asyncio.sleep(attempt + 1)
        
        # Should not be reached if loop completes without returning/raising
        raise VitapVtopClientError(f"Login failed for user {self.username} after {self.max_login_retries} attempts.")

    async def _ensure_logged_in(self) -> LoggedInStudent:
        """
        Ensures the client is logged in. If not, performs login.
        This method is idempotent.
        """
        # Check if already logged in and session is potentially valid
        if self._logged_in_student is not None:
            return self._logged_in_student

        async with self._login_lock:
            # Double-check after acquiring the lock, in case another coroutine logged in
            if self._logged_in_student is None:
                print(f"VtopClient: Not logged in or session expired for {self.username}. Initiating login.")
                await self._perform_login_sequence()
            
            if self._logged_in_student is None: # Should be set by _perform_login_sequence on success
                raise VitapVtopClientError("VtopClient: Failed to establish a login session.")
            return self._logged_in_student

    async def get_attendance(self, sem_sub_id: str) -> list[AttendanceModel]:
        """
        Fetches attendance data for the given semester subject ID.

        Args:
            sem_sub_id: The semester subject ID (e.g., "AP2023242").

        Returns:
            A list containing the parsed attendance data(AttendanceModel).
        """
        logged_in_info = await self._ensure_logged_in()
        return await fetch_attendance_data(
            client=self._client,
            username=logged_in_info.registration_number,
            semSubID=sem_sub_id,
            csrf_token=logged_in_info.post_login_csrf_token
        )

    # --- Other VTOP feature methods here ---
    # Example:
    # async def get_timetable(self, sem_sub_id: str) -> dict:
    #     logged_in_info = await self._ensure_logged_in()
    #     return await fetch_timetable_data(
    #         client=self._client,
    #         username=logged_in_info.registration_number,
    #         semSubID=sem_sub_id,
    #         csrf_token=logged_in_info.post_login_csrf_token
    #     )

    # async def get_marks(self, some_identifier: str) -> dict:
    #    logged_in_info = await self._ensure_logged_in()
    #    return await fetch_marks_data(
    #        client=self._client,
    #        username=logged_in_info.registration_number,
    #        csrf_token=logged_in_info.post_login_csrf_token,
    #        # ...other params for marks...
    #        identifier=some_identifier
    #    )

    async def close(self):
        """
        Closes the underlying HTTP client. Should be called when done with the VtopClient.
        """
        await self._client.aclose()

    async def __aenter__(self):
        """Allows using the client with 'async with'."""
        # You could optionally call await self._ensure_logged_in() here
        # if you want to ensure login upon entering the context.
        # However, lazy login (on first actual data request) is often preferred.
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Closes the client when exiting 'async with' block."""
        await self.close()

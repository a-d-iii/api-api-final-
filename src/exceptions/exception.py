import httpx

class VitapVtopClientError(Exception):
    """Base exception for all VITAP VTOP client errors."""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code

class VtopConnectionError(VitapVtopClientError):
    """Raised for network-related errors during VTOP communication."""
    def __init__(
        self,
        message: str,
        original_exception: httpx.RequestError | None = None,
        status_code: int | None = None
    ):
        super().__init__(message, status_code)
        self.original_exception = original_exception

class VtopLoginError(VitapVtopClientError):
    """Raised when login fails due to invalid credentials, server-side validation, etc."""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)

class VtopCaptchaError(VtopLoginError):
    """Raised for errors specifically related to CAPTCHA fetching or solving."""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)

class VtopCsrfError(VtopLoginError):
    """Raised for errors specifically related to CSRF scraping and fetching."""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)

class VtopParsingError(VitapVtopClientError):
    """Raised when data parsing fails unexpectedly (e.g., new HTML format)."""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)

class VtopSessionError(VitapVtopClientError):
    """Raised when an operation requires an active session but one is not available or valid."""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)

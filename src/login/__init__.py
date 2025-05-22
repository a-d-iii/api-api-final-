# Expose the main login function and potentially others later
from src.client import login

# You might define __all__ to be explicit about the public API
__all__ = ["login"]

# Optional: Define a custom exception base class for the library
class VITAPVTOPClientError(Exception):
    """Base exception for VITAP VTOP client errors."""
    pass

class VTOPLoginError(VITAPVTOPClientError, ValueError):
    """Raised when login fails due to invalid credentials, captcha, etc."""
    pass

class VTOPScrapingError(VITAPVTOPClientError, RuntimeError):
    """Raised when data scraping or parsing fails unexpectedly."""
    pass

class VTOPSessionError(VITAPVTOPClientError, PermissionError):
    """Raised when an operation requires an active session but one is not available or valid."""
    pass

# You could then update the functions in login.py, prelogin.py etc.
# to raise these specific exceptions instead of generic ValueError/RuntimeError.
# Example in login.py: change `raise ValueError(f"Login failed: {error_message}")`
# to `raise VTOPLoginError(f"Login failed: {error_message}")`.
# Update client.py and api/main.py to catch these new specific exceptions.
"""Convenience exports for the vitap_vtop_client package."""

from .client import VtopClient
from .exceptions import (
    VitapVtopClientError,
    VtopConnectionError,
    VtopCaptchaError,
    VtopCaptchaSolvingError,
    VtopCsrfError,
    VtopLoginError,
    VtopSessionError,
    VtopParsingError,
    VtopAttendanceError,
    VtopTimetableError,
    VtopMentorError,
    VtopBiometricError,
    VtopGradeHistoryError,
    VtopProfileError,
    VtopExamScheduleError,
    VtopMarksError,
    VtopGeneralOutingError,
    VtopWeekendOutingError,
)

__all__ = [
    "VtopClient",
    "VitapVtopClientError",
    "VtopConnectionError",
    "VtopCaptchaError",
    "VtopCaptchaSolvingError",
    "VtopCsrfError",
    "VtopLoginError",
    "VtopSessionError",
    "VtopParsingError",
    "VtopAttendanceError",
    "VtopTimetableError",
    "VtopMentorError",
    "VtopBiometricError",
    "VtopGradeHistoryError",
    "VtopProfileError",
    "VtopExamScheduleError",
    "VtopMarksError",
    "VtopGeneralOutingError",
    "VtopWeekendOutingError",
]


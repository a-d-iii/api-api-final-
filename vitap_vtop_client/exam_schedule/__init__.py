"""Exports for the exam_schedule submodule."""

from .exam_schedule import fetch_exam_schedule
from .model.exam_schedule_model import ExamScheduleModel

__all__ = ["fetch_exam_schedule", "ExamScheduleModel"]

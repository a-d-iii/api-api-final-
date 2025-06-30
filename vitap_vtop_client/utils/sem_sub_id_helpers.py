from vitap_vtop_client.constants import SemSubID


def get_semester_name(sem_sub_id: str) -> str | None:
    """Return the human readable name for a semesterSubId if known."""
    for name, value in SemSubID.items():
        if value == sem_sub_id:
            return name
    return None

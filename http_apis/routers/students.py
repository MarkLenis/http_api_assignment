import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from http_apis.models.student import Student

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_json_data(filename: str) -> list[dict[str, Any]]:
    """Load list-based JSON data from the data directory."""
    file_path = DATA_DIR / filename
    with file_path.open("r", encoding="utf-8") as json_file:
        return json.load(json_file)


STUDENTS = load_json_data("students.json")


@router.get(
    "/mct/students",
    response_model=list[Student],
    summary="Get all students",
    description="Return all students in the MCT programme.",
    tags=["Students"],
)
def get_students() -> list[Student]:
    """Return all students."""
    return list(map(lambda student: Student(**student), STUDENTS))


@router.get(
    "/mct/students/name/{name}",
    response_model=list[Student],
    summary="Get students by name",
    description="Return students where the name matches the provided value.",
    tags=["Students"],
)
def get_students_by_name(name: str) -> list[Student]:
    """Return students that match the provided name."""
    filtered_students = list(
        filter(
            lambda student: str(student.get("name", "")).lower() == name.lower(),
            STUDENTS,
        )
    )
    return list(map(lambda student: Student(**student), filtered_students))


@router.get(
    "/mct/students/track/{track}",
    response_model=list[Student],
    summary="Get students by track",
    description="Return students where the track matches the provided value.",
    tags=["Students"],
)
def get_students_by_track(track: str) -> list[Student]:
    """Return students that match the provided track."""
    filtered_students = list(
        filter(
            lambda student: str(student.get("track", "")).lower() == track.lower(),
            STUDENTS,
        )
    )
    return list(map(lambda student: Student(**student), filtered_students))

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Response, status
from http_apis.models.student import Student

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
STUDENTS_FILE = DATA_DIR / "students.json"


def load_json_data() -> list[dict[str, Any]]:
    """Load list-based JSON data from the data directory."""
    with STUDENTS_FILE.open("r", encoding="utf-8") as json_file:
        return json.load(json_file)


def save_json_data(students: list[dict[str, Any]]) -> None:
    """Persist student data to the students JSON file."""
    with STUDENTS_FILE.open("w", encoding="utf-8") as json_file:
        json.dump(students, json_file, indent=2)


def find_student_index_by_name(name: str) -> int | None:
    """Find the index of a student by name (case-insensitive)."""
    for index, student in enumerate(STUDENTS):
        if str(student.get("name", "")).lower() == name.lower():
            return index
    return None


STUDENTS = load_json_data()


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


@router.post(
    "/mct/students",
    response_model=Student,
    status_code=status.HTTP_201_CREATED,
    summary="Create a student",
    description="Create a new student and store it in students.json.",
    tags=["Students"],
)
def create_student(student: Student) -> Student:
    """Create and persist a new student."""
    if find_student_index_by_name(student.name) is not None:
        raise HTTPException(status_code=400, detail="Student already exists.")

    STUDENTS.append(student.model_dump())
    save_json_data(STUDENTS)
    return student


@router.put(
    "/mct/students/name/{name}",
    response_model=Student,
    summary="Update a student",
    description="Update an existing student by name.",
    tags=["Students"],
)
def update_student(name: str, student: Student) -> Student:
    """Update and persist an existing student."""
    student_index = find_student_index_by_name(name)
    if student_index is None:
        raise HTTPException(status_code=404, detail="Student not found.")

    STUDENTS[student_index] = student.model_dump()
    save_json_data(STUDENTS)
    return Student(**STUDENTS[student_index])


@router.delete(
    "/mct/students/name/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a student",
    description="Delete an existing student by name.",
    tags=["Students"],
)
def delete_student(name: str) -> Response:
    """Delete a student and persist the remaining list."""
    student_index = find_student_index_by_name(name)
    if student_index is None:
        raise HTTPException(status_code=404, detail="Student not found.")

    STUDENTS.pop(student_index)
    save_json_data(STUDENTS)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

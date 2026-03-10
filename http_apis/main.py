import json
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI
from http_apis.models.course import Course
from http_apis.models.lecturer import Lecturer
from http_apis.models.student import Student

app = FastAPI()

DATA_DIR = Path(__file__).resolve().parent / "data"


def load_json_data(filename: str) -> list[dict[str, Any]]:
    """Load list-based JSON data from the data directory."""
    file_path = DATA_DIR / filename
    with file_path.open("r", encoding="utf-8") as json_file:
        return json.load(json_file)


COURSES = load_json_data("courses.json")
LECTURERS = load_json_data("lecturers.json")
STUDENTS = load_json_data("students.json")


@app.get(
    "/",
    response_model=dict[str, str],
    summary="API health check",
    description="Simple endpoint to verify the API is running.",
    tags=["General"],
)
def read_root() -> dict[str, str]:
    """Return a simple welcome payload."""
    return {"Hello": "World"}


@app.get(
    "/items/{item_id}",
    response_model=dict[str, int | str | None],
    summary="Get item by id",
    description="Return an item id and optional query value.",
    tags=["General"],
)
def read_item(item_id: int, q: Optional[str] = None) -> dict[str, int | str | None]:
    """Return an item id and optional query string."""
    # `q` is an optional query parameter (example: /items/5?q=search_text).
    return {"item_id": item_id, "q": q}


@app.get(
    "/mct/courses",
    response_model=list[Course],
    summary="Get all courses",
    description="Return all available MCT courses.",
    tags=["Courses"],
)
def get_courses() -> list[Course]:
    """Return all courses."""
    return list(map(lambda course: Course(**course), COURSES))


@app.get(
    "/mct/courses/name/{name}",
    response_model=list[Course],
    summary="Get courses by name",
    description="Return courses where the title matches the provided name.",
    tags=["Courses"],
)
def get_courses_by_name(name: str) -> list[Course]:
    """Return courses that match the provided course title."""
    filtered_courses = list(
        filter(
            lambda course: str(course.get("title", "")).lower() == name.lower(),
            COURSES,
        )
    )
    return list(map(lambda course: Course(**course), filtered_courses))


@app.get(
    "/mct/courses/track/{track}",
    response_model=list[Course],
    summary="Get courses by track",
    description="Return courses where the track list contains the provided track.",
    tags=["Courses"],
)
def get_courses_by_track(track: str) -> list[Course]:
    """Return courses that include the given track."""
    filtered_courses = list(
        filter(
            lambda course: track.lower()
            in list(map(lambda value: str(value).lower(), course.get("tracks", []))),
            COURSES,
        )
    )
    return list(map(lambda course: Course(**course), filtered_courses))


@app.get(
    "/mct/lecturers",
    response_model=list[Lecturer],
    summary="Get all lecturers",
    description="Return all lecturers in the MCT programme.",
    tags=["Lecturers"],
)
def get_lecturers() -> list[Lecturer]:
    """Return all lecturers."""
    return list(map(lambda lecturer: Lecturer(**lecturer), LECTURERS))


@app.get(
    "/mct/lecturers/name/{name}",
    response_model=list[Lecturer],
    summary="Get lecturers by name",
    description="Return lecturers where the name matches the provided value.",
    tags=["Lecturers"],
)
def get_lecturers_by_name(name: str) -> list[Lecturer]:
    """Return lecturers that match the provided name."""
    filtered_lecturers = list(
        filter(
            lambda lecturer: str(lecturer.get("name", "")).lower() == name.lower(),
            LECTURERS,
        )
    )
    return list(map(lambda lecturer: Lecturer(**lecturer), filtered_lecturers))


@app.get(
    "/mct/lecturers/track/{track}",
    response_model=list[Lecturer],
    summary="Get lecturers by track",
    description="Return lecturers where the track matches the provided value.",
    tags=["Lecturers"],
)
def get_lecturers_by_track(track: str) -> list[Lecturer]:
    """Return lecturers that match the provided track."""
    filtered_lecturers = list(
        filter(
            lambda lecturer: str(lecturer.get("track", "")).lower() == track.lower(),
            LECTURERS,
        )
    )
    return list(map(lambda lecturer: Lecturer(**lecturer), filtered_lecturers))


@app.get(
    "/mct/students",
    response_model=list[Student],
    summary="Get all students",
    description="Return all students in the MCT programme.",
    tags=["Students"],
)
def get_students() -> list[Student]:
    """Return all students."""
    return list(map(lambda student: Student(**student), STUDENTS))


@app.get(
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


@app.get(
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

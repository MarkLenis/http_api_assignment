import json
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI

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


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a simple welcome payload."""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None) -> dict[str, int | str | None]:
    """Return an item id and optional query string."""
    # `q` is an optional query parameter (example: /items/5?q=search_text).
    return {"item_id": item_id, "q": q}


@app.get("/mct/courses")
def get_courses() -> list[dict[str, Any]]:
    """Return all courses."""
    return COURSES


@app.get("/mct/courses/name/{name}")
def get_courses_by_name(name: str) -> list[dict[str, Any]]:
    """Return courses that match the provided course title."""
    return list(
        filter(
            lambda course: str(course.get("title", "")).lower() == name.lower(),
            COURSES,
        )
    )


@app.get("/mct/courses/track/{track}")
def get_courses_by_track(track: str) -> list[dict[str, Any]]:
    """Return courses that include the given track."""
    return list(
        filter(
            lambda course: track.lower()
            in list(map(lambda value: str(value).lower(), course.get("tracks", []))),
            COURSES,
        )
    )


@app.get("/mct/lecturers")
def get_lecturers() -> list[dict[str, Any]]:
    """Return all lecturers."""
    return LECTURERS


@app.get("/mct/lecturers/name/{name}")
def get_lecturers_by_name(name: str) -> list[dict[str, Any]]:
    """Return lecturers that match the provided name."""
    return list(
        filter(
            lambda lecturer: str(lecturer.get("name", "")).lower() == name.lower(),
            LECTURERS,
        )
    )


@app.get("/mct/lecturers/track/{track}")
def get_lecturers_by_track(track: str) -> list[dict[str, Any]]:
    """Return lecturers that match the provided track."""
    return list(
        filter(
            lambda lecturer: str(lecturer.get("track", "")).lower() == track.lower(),
            LECTURERS,
        )
    )


@app.get("/mct/students")
def get_students() -> list[dict[str, Any]]:
    """Return all students."""
    return STUDENTS


@app.get("/mct/students/name/{name}")
def get_students_by_name(name: str) -> list[dict[str, Any]]:
    """Return students that match the provided name."""
    return list(
        filter(
            lambda student: str(student.get("name", "")).lower() == name.lower(),
            STUDENTS,
        )
    )


@app.get("/mct/students/track/{track}")
def get_students_by_track(track: str) -> list[dict[str, Any]]:
    """Return students that match the provided track."""
    return list(
        filter(
            lambda student: str(student.get("track", "")).lower() == track.lower(),
            STUDENTS,
        )
    )

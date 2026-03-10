import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from http_apis.models.course import Course

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_json_data(filename: str) -> list[dict[str, Any]]:
    """Load list-based JSON data from the data directory."""
    file_path = DATA_DIR / filename
    with file_path.open("r", encoding="utf-8") as json_file:
        return json.load(json_file)


COURSES = load_json_data("courses.json")


@router.get(
    "/mct/courses",
    response_model=list[Course],
    summary="Get all courses",
    description="Return all available MCT courses.",
    tags=["Courses"],
)
def get_courses() -> list[Course]:
    """Return all courses."""
    return list(map(lambda course: Course(**course), COURSES))


@router.get(
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


@router.get(
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

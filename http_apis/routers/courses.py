import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Response, status
from http_apis.models.course import Course

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
COURSES_FILE = DATA_DIR / "courses.json"


def load_json_data() -> list[dict[str, Any]]:
    """Load list-based JSON data from the data directory."""
    with COURSES_FILE.open("r", encoding="utf-8") as json_file:
        return json.load(json_file)


def save_json_data(courses: list[dict[str, Any]]) -> None:
    """Persist course data to the courses JSON file."""
    with COURSES_FILE.open("w", encoding="utf-8") as json_file:
        json.dump(courses, json_file, indent=2)


def find_course_index_by_title(title: str) -> int | None:
    """Find the index of a course by title (case-insensitive)."""
    for index, course in enumerate(COURSES):
        if str(course.get("title", "")).lower() == title.lower():
            return index
    return None


COURSES = load_json_data()


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


@router.post(
    "/mct/courses",
    response_model=Course,
    status_code=status.HTTP_201_CREATED,
    summary="Create a course",
    description="Create a new course and store it in courses.json.",
    tags=["Courses"],
)
def create_course(course: Course) -> Course:
    """Create and persist a new course."""
    if find_course_index_by_title(course.title) is not None:
        raise HTTPException(status_code=400, detail="Course already exists.")

    COURSES.append(course.model_dump())
    save_json_data(COURSES)
    return course


@router.put(
    "/mct/courses/name/{name}",
    response_model=Course,
    summary="Update a course",
    description="Update an existing course by title.",
    tags=["Courses"],
)
def update_course(name: str, course: Course) -> Course:
    """Update and persist an existing course."""
    course_index = find_course_index_by_title(name)
    if course_index is None:
        raise HTTPException(status_code=404, detail="Course not found.")

    COURSES[course_index] = course.model_dump()
    save_json_data(COURSES)
    return Course(**COURSES[course_index])


@router.delete(
    "/mct/courses/name/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a course",
    description="Delete an existing course by title.",
    tags=["Courses"],
)
def delete_course(name: str) -> Response:
    """Delete a course and persist the remaining list."""
    course_index = find_course_index_by_title(name)
    if course_index is None:
        raise HTTPException(status_code=404, detail="Course not found.")

    COURSES.pop(course_index)
    save_json_data(COURSES)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

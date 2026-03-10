import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Response, status
from http_apis.models.lecturer import Lecturer

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
LECTURERS_FILE = DATA_DIR / "lecturers.json"


def load_json_data() -> list[dict[str, Any]]:
    """Load list-based JSON data from the data directory."""
    with LECTURERS_FILE.open("r", encoding="utf-8") as json_file:
        return json.load(json_file)


def save_json_data(lecturers: list[dict[str, Any]]) -> None:
    """Persist lecturer data to the lecturers JSON file."""
    with LECTURERS_FILE.open("w", encoding="utf-8") as json_file:
        json.dump(lecturers, json_file, indent=2)


def find_lecturer_index_by_name(name: str) -> int | None:
    """Find the index of a lecturer by name (case-insensitive)."""
    for index, lecturer in enumerate(LECTURERS):
        if str(lecturer.get("name", "")).lower() == name.lower():
            return index
    return None


LECTURERS = load_json_data()


@router.get(
    "/mct/lecturers",
    response_model=list[Lecturer],
    summary="Get all lecturers",
    description="Return all lecturers in the MCT programme.",
    tags=["Lecturers"],
)
def get_lecturers() -> list[Lecturer]:
    """Return all lecturers."""
    return list(map(lambda lecturer: Lecturer(**lecturer), LECTURERS))


@router.get(
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


@router.get(
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


@router.post(
    "/mct/lecturers",
    response_model=Lecturer,
    status_code=status.HTTP_201_CREATED,
    summary="Create a lecturer",
    description="Create a new lecturer and store it in lecturers.json.",
    tags=["Lecturers"],
)
def create_lecturer(lecturer: Lecturer) -> Lecturer:
    """Create and persist a new lecturer."""
    if find_lecturer_index_by_name(lecturer.name) is not None:
        raise HTTPException(status_code=400, detail="Lecturer already exists.")

    LECTURERS.append(lecturer.model_dump())
    save_json_data(LECTURERS)
    return lecturer


@router.put(
    "/mct/lecturers/name/{name}",
    response_model=Lecturer,
    summary="Update a lecturer",
    description="Update an existing lecturer by name.",
    tags=["Lecturers"],
)
def update_lecturer(name: str, lecturer: Lecturer) -> Lecturer:
    """Update and persist an existing lecturer."""
    lecturer_index = find_lecturer_index_by_name(name)
    if lecturer_index is None:
        raise HTTPException(status_code=404, detail="Lecturer not found.")

    LECTURERS[lecturer_index] = lecturer.model_dump()
    save_json_data(LECTURERS)
    return Lecturer(**LECTURERS[lecturer_index])


@router.delete(
    "/mct/lecturers/name/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a lecturer",
    description="Delete an existing lecturer by name.",
    tags=["Lecturers"],
)
def delete_lecturer(name: str) -> Response:
    """Delete a lecturer and persist the remaining list."""
    lecturer_index = find_lecturer_index_by_name(name)
    if lecturer_index is None:
        raise HTTPException(status_code=404, detail="Lecturer not found.")

    LECTURERS.pop(lecturer_index)
    save_json_data(LECTURERS)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

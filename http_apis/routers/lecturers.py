import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from http_apis.models.lecturer import Lecturer

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_json_data(filename: str) -> list[dict[str, Any]]:
    """Load list-based JSON data from the data directory."""
    file_path = DATA_DIR / filename
    with file_path.open("r", encoding="utf-8") as json_file:
        return json.load(json_file)


LECTURERS = load_json_data("lecturers.json")


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

from pydantic import BaseModel, Field


class Course(BaseModel):
    title: str
    content: str
    semester: int
    pillar: str
    tags: list[str] = Field(default_factory=list)
    tracks: list[str] = Field(default_factory=list)
    lecturers: list[str] = Field(default_factory=list)
    students: list[str] = Field(default_factory=list)

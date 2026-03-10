from pydantic import BaseModel


class Lecturer(BaseModel):
    name: str
    language: str
    track: str
    programmingLanguage: str
    favouriteCourse: str

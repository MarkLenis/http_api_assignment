from pydantic import BaseModel


class Student(BaseModel):
    name: str
    language: str
    track: str
    programmingLanguage: str
    favouriteCourse: str

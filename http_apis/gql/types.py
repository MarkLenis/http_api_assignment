import strawberry

from http_apis.models.course import Course
from http_apis.models.lecturer import Lecturer
from http_apis.models.student import Student


@strawberry.experimental.pydantic.type(model=Course, all_fields=True)
class CourseType:
    pass


@strawberry.experimental.pydantic.input(model=Course, all_fields=True)
class CourseInput:
    pass


@strawberry.experimental.pydantic.type(model=Lecturer, all_fields=True)
class LecturerType:
    pass


@strawberry.experimental.pydantic.input(model=Lecturer, all_fields=True)
class LecturerInput:
    pass


@strawberry.experimental.pydantic.type(model=Student, all_fields=True)
class StudentType:
    pass

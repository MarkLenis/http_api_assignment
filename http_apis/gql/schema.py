import strawberry
from strawberry.fastapi import GraphQLRouter

from http_apis.gql.data_store import load_json_data, save_json_data
from http_apis.gql.types import (
    CourseInput,
    CourseType,
    LecturerInput,
    LecturerType,
)
from http_apis.models.course import Course
from http_apis.models.lecturer import Lecturer

COURSES_FILE = "courses.json"
LECTURERS_FILE = "lecturers.json"


@strawberry.type
class Query:
    @strawberry.field(description="Return all courses from the data store.")
    def courses(self) -> list[CourseType]:
        """Return all courses."""
        courses = load_json_data(COURSES_FILE)
        return list(
            map(
                lambda course: CourseType.from_pydantic(Course(**course)),
                courses,
            )
        )

    @strawberry.field(description="Return all lecturers from the data store.")
    def lecturers(self) -> list[LecturerType]:
        """Return all lecturers."""
        lecturers = load_json_data(LECTURERS_FILE)
        return list(
            map(
                lambda lecturer: LecturerType.from_pydantic(Lecturer(**lecturer)),
                lecturers,
            )
        )


@strawberry.type
class Mutation:
    @strawberry.mutation(description="Create and persist a new course.")
    def create_course(self, course: CourseInput) -> CourseType:
        """Create a course in courses.json."""
        courses = load_json_data(COURSES_FILE)
        course_model = course.to_pydantic()

        existing = next(
            filter(
                lambda current: str(current.get("title", "")).lower()
                == course_model.title.lower(),
                courses,
            ),
            None,
        )
        if existing is not None:
            raise ValueError("Course already exists.")

        courses.append(course_model.model_dump())
        save_json_data(COURSES_FILE, courses)
        return CourseType.from_pydantic(course_model)

    @strawberry.mutation(description="Create and persist a new lecturer.")
    def create_lecturer(self, lecturer: LecturerInput) -> LecturerType:
        """Create a lecturer in lecturers.json."""
        lecturers = load_json_data(LECTURERS_FILE)
        lecturer_model = lecturer.to_pydantic()

        existing = next(
            filter(
                lambda current: str(current.get("name", "")).lower()
                == lecturer_model.name.lower(),
                lecturers,
            ),
            None,
        )
        if existing is not None:
            raise ValueError("Lecturer already exists.")

        lecturers.append(lecturer_model.model_dump())
        save_json_data(LECTURERS_FILE, lecturers)
        return LecturerType.from_pydantic(lecturer_model)


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_router = GraphQLRouter(schema)

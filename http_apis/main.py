from typing import Optional

from fastapi import FastAPI
from http_apis.gql.schema import graphql_router
from http_apis.routers import courses, lecturers, students

app = FastAPI()


@app.get(
    "/",
    response_model=dict[str, str],
    summary="API health check",
    description="Simple endpoint to verify the API is running.",
    tags=["General"],
)
def read_root() -> dict[str, str]:
    """Return a simple welcome payload."""
    return {"Hello": "World"}


@app.get(
    "/items/{item_id}",
    response_model=dict[str, int | str | None],
    summary="Get item by id",
    description="Return an item id and optional query value.",
    tags=["General"],
)
def read_item(item_id: int, q: Optional[str] = None) -> dict[str, int | str | None]:
    """Return an item id and optional query string."""
    # `q` is an optional query parameter (example: /items/5?q=search_text).
    return {"item_id": item_id, "q": q}


app.include_router(courses.router)
app.include_router(lecturers.router)
app.include_router(students.router)
app.include_router(graphql_router, prefix="/graphql")

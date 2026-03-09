from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None) -> dict[str, int | str | None]:
    # `q` is an optional query parameter
    return {"item_id": item_id, "q": q}

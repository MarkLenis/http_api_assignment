## Virtual environment setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install fastapi "uvicorn[standard]" strawberry-graphql
```

## Run the API

```powershell
uvicorn http_apis.main:app --reload
```

Then open:

- API root: `http://127.0.0.1:8000/`
- Swagger docs: `http://127.0.0.1:8000/docs`
- GraphQL endpoint: `http://127.0.0.1:8000/graphql`

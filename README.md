# web2-2026-isit

## Backend starter

A minimal learning-oriented Python backend lives in `backend/` and uses FastAPI.

### Structure

```text
backend/
├── alembic/
├── app/
│   ├── api/v1/routes/
│   ├── core/
│   ├── db/models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── tests/
│   └── main.py
├── .env.example
└── pyproject.toml
```

### Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for Swagger UI.

### HTTP QUERY method

Students can be filtered with the HTTP `QUERY` method (safe and idempotent like
`GET`, but the filters travel in a JSON body instead of the query string):

```bash
curl -X QUERY http://127.0.0.1:8000/api/v1/students \
  -H 'Content-Type: application/json' \
  -d '{"first_name": "Ana", "max_age": 21}'
```

Send `{}` to get every student. Invalid filters return `422`.

`QUERY` is only a valid path item method from OpenAPI 3.2 onwards, so `app/main.py`
generates the schema with `openapi_version="3.2.0"` and registers `QUERY` in
FastAPI's `METHODS_WITH_BODY` so the request body is documented. Swagger UI shows
the operation with its schema, but its "Try it out" button does not support `QUERY`
yet - use curl for live calls. The query-string variant `GET /api/v1/students/query`
is still available.

# Travel Planner API

A RESTful travel management API built with FastAPI and SQLModel.

The application allows travelers to create travel projects, add places retrieved from the Art Institute of Chicago API, attach notes, and track visited locations.

---

## Features

### Travel Projects
- Create project (optionally with initial places)
- List projects (pagination supported)
- Get project by ID
- Update project
- Delete project (blocked if any place is visited)

### Places
- Add place to project (validated via external API)
- Prevent duplicate places per project
- Maximum 10 places per project
- Update place (notes, visited)
- Auto-complete project when all places are visited
- List places in project
- Get single place

---

## Additional Features

- Pagination on project listing
- HTTP Basic Authentication
- Docker support
- Environment-based configuration
- Postman collection
- Clean project structure

---

## Tech Stack

- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- SQLite
- HTTPX
- Docker

---

## Authentication

All endpoints require HTTP Basic authentication.

Credentials are configured via environment variables.

Create a `.env` file based on `.env.example`:
```
BASIC_AUTH_USERNAME=admin
BASIC_AUTH_PASSWORD=secret
```

---

## Running Locally

1. Create virtual environment
2. Install dependencies:

pip install -r requirements.txt

3. Create `.env` file (see `.env.example`)
4. Run:
```
uvicorn app.main:app --reload
```
5. Open Swagger UI:

http://localhost:8000/docs

---

## Running with Docker

Build image:
```
docker build -t travel-planner .
```
Run container:
```
docker run -p 8000:8000 --env-file .env travel-planner
```
---

## Example Request

{
  "name": "NYC Art Trip",
  "places": [27992, 129884]
}

---

## Business Rules

- Maximum 10 places per project
- Duplicate places are not allowed
- Cannot delete project if any place is visited
- Project automatically marked completed when all places are visited
- Places validated via Art Institute API

---

## API Documentation

/docs
/openapi.json
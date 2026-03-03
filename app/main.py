from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db import create_db_and_tables
from app.api.projects import router as projects_router
from app.api.places import router as places_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Travel Planner API",
    lifespan=lifespan
)

app.include_router(projects_router)
app.include_router(places_router)

@app.get("/")
def read_root():
    return {"message": "Travel Planner API is running"}

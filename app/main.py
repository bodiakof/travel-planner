from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Travel Planner API",
    lifespan=lifespan
)


@app.get("/")
def read_root():
    return {"message": "Travel Planner API is running"}

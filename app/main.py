from fastapi.security import HTTPBasic, HTTPBasicCredentials
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
import secrets

from app.db import create_db_and_tables
from app.api.projects import router as projects_router
from app.api.places import router as places_router


security = HTTPBasic()

USERNAME = "admin"
PASSWORD = "secret"

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Travel Planner API",
    lifespan=lifespan
)

def verify_credentials(
    credentials: HTTPBasicCredentials = Depends(security),
):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

app.include_router(projects_router, dependencies=[Depends(verify_credentials)])
app.include_router(places_router, dependencies=[Depends(verify_credentials)])

@app.get("/")
def read_root():
    return {"message": "Travel Planner API is running"}



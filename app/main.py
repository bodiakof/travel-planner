import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import secrets

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Depends, HTTPException, status

from app.db import create_db_and_tables
from app.api.projects import router as projects_router
from app.api.places import router as places_router

load_dotenv()

security = HTTPBasic()

USERNAME = os.getenv("BASIC_AUTH_USERNAME")
PASSWORD = os.getenv("BASIC_AUTH_PASSWORD")

if not USERNAME or not PASSWORD:
    raise RuntimeError("Basic auth credentials not configured")

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
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Travel Planner API",
    lifespan=lifespan
)    

app.include_router(projects_router, dependencies=[Depends(verify_credentials)])
app.include_router(places_router, dependencies=[Depends(verify_credentials)])

@app.get("/")
def read_root():
    return {"message": "Travel Planner API is running"}

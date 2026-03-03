from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db import get_session
from app.models import TravelProject, TravelProjectCreate, TravelProjectRead

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=TravelProjectRead, status_code=201)
def create_project(
    project_data: TravelProjectCreate,
    session: Session = Depends(get_session),
):
    project = TravelProject(**project_data.model_dump())

    session.add(project)
    session.commit()
    session.refresh(project)

    return project

@router.get("/", response_model=list[TravelProjectRead])
def list_projects(
    session: Session = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
):
    statement = select(TravelProject).offset(offset).limit(limit)
    projects = session.exec(statement).all()
    return projects

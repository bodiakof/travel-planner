from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db import get_session
from app.models import TravelProject, TravelProjectCreate, TravelProjectRead, TravelProjectUpdate

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

@router.get("/{project_id}", response_model=TravelProjectRead)
def get_project(
    project_id: int,
    session: Session = Depends(get_session),
):
    project = session.get(TravelProject, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

@router.patch("/{project_id}", response_model=TravelProjectRead)
def update_project(
    project_id: int,
    project_data: TravelProjectUpdate,
    session: Session = Depends(get_session),
):
    project = session.get(TravelProject, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(project, key, value)

    session.add(project)
    session.commit()
    session.refresh(project)

    return project

@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    session: Session = Depends(get_session),
):
    project = session.get(TravelProject, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if any(place.visited for place in project.places):
        raise HTTPException(
            status_code=400,
            detail="Cannot delete project with visited places"
        )

    session.delete(project)
    session.commit()

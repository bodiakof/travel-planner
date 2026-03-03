from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.services.artic_client import fetch_artwork
from app.db import get_session
from app.models import (
    TravelProject, 
    TravelProjectCreate, 
    TravelProjectRead, 
    TravelProjectUpdate, 
    ProjectPlace
)


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=TravelProjectRead, status_code=201)
async def create_project(
    project_data: TravelProjectCreate,
    session: Session = Depends(get_session),
):
    unique_ids: list[int] = []

    if project_data.places:
        unique_ids = list(dict.fromkeys(project_data.places))

        if len(unique_ids) != len(project_data.places):
            raise HTTPException(
                status_code=400,
                detail="Duplicate place IDs provided",
            )

        if len(unique_ids) > 10:
            raise HTTPException(
                status_code=400,
                detail="Project cannot contain more than 10 places",
            )

        artworks = []
        for external_id in unique_ids:
            artwork = await fetch_artwork(external_id)
            artworks.append(artwork)
    else:
        artworks = []

    project = TravelProject(
        name=project_data.name,
        description=project_data.description,
        start_date=project_data.start_date,
    )

    session.add(project)
    session.commit()
    session.refresh(project)

    for artwork in artworks:
        place = ProjectPlace(
            project_id=project.id,
            external_id=artwork["external_id"],
            title=artwork["title"],
        )
        session.add(place)

    if artworks:
        session.commit()

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

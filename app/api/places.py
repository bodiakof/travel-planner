from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models import (
    TravelProject,
    ProjectPlace,
    ProjectPlaceCreate,
    ProjectPlaceRead,
    ProjectPlaceUpdate,
)
from app.services.artic_client import fetch_artwork


router = APIRouter(
    prefix="/projects/{project_id}/places",
    tags=["Places"],
)

@router.post("/", response_model=ProjectPlaceRead, status_code=201)
async def add_place(
    project_id: int,
    place_data: ProjectPlaceCreate,
    session: Session = Depends(get_session),
):
    project = session.get(TravelProject, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if len(project.places) >= 10:
        raise HTTPException(
            status_code=400,
            detail="Project cannot contain more than 10 places"
        )

    statement = select(ProjectPlace).where(
        ProjectPlace.project_id == project_id,
        ProjectPlace.external_id == place_data.external_id,
    )
    existing = session.exec(statement).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Place already added to this project"
        )

    artwork = await fetch_artwork(place_data.external_id)

    new_place = ProjectPlace(
        project_id=project_id,
        external_id=artwork["external_id"],
        title=artwork["title"],
    )

    session.add(new_place)
    session.commit()
    session.refresh(new_place)

    return new_place

@router.get("/", response_model=list[ProjectPlaceRead])
def list_places(
    project_id: int,
    session: Session = Depends(get_session),
):
    project = session.get(TravelProject, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project.places

@router.get("/{place_id}", response_model=ProjectPlaceRead)
def get_place(
    project_id: int,
    place_id: int,
    session: Session = Depends(get_session),
):
    statement = select(ProjectPlace).where(
        ProjectPlace.id == place_id,
        ProjectPlace.project_id == project_id,
    )
    place = session.exec(statement).first()

    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    return place


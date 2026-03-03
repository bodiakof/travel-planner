from datetime import date
from sqlmodel import SQLModel, Field, Relationship


class ProjectPlaceBase(SQLModel):
    external_id: int
    title: str
    notes: str | None = None
    visited: bool = False


class ProjectPlace(ProjectPlaceBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="travelproject.id")

    project: "TravelProject" | None = Relationship(back_populates="places")


class TravelProjectBase(SQLModel):
    name: str
    description: str | None = None
    start_date: date | None = None


class TravelProject(TravelProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    is_completed: bool = False

    places: list[ProjectPlace] = Relationship(back_populates="project")

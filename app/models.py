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

    project: "TravelProject" = Relationship(back_populates="places")


class TravelProjectBase(SQLModel):
    name: str
    description: str | None = None
    start_date: date | None = None


class TravelProject(TravelProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    is_completed: bool = False

    places: list["ProjectPlace"] = Relationship(back_populates="project")


class TravelProjectCreate(SQLModel):
    name: str
    description: str | None = None
    start_date: date | None = None
    places: list[int] | None = None


class TravelProjectRead(SQLModel):
    id: int
    name: str
    description: str | None
    start_date: date | None
    is_completed: bool


class TravelProjectUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    start_date: date | None = None


class ProjectPlaceCreate(SQLModel):
    external_id: int


class ProjectPlaceRead(SQLModel):
    id: int
    external_id: int
    title: str
    notes: str | None
    visited: bool


class ProjectPlaceUpdate(SQLModel):
    notes: str | None = None
    visited: bool | None = None

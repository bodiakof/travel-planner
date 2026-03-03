from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import event
from sqlalchemy.engine import Engine
from typing import Generator


DATABASE_URL = "sqlite:///./travel.db"

engine = create_engine(DATABASE_URL, echo=False)

@event.listens_for(Engine, "connect")
def enable_sqlite_fk(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

from os import getcwd
from typing import Any, Optional

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import JSON, Column, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from starlette.responses import Response

SQLALCHEMY_DATABASE_URI = f"postgresql://:@/fohispital?host={getcwd()}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Item(BaseModel):
    id: int
    value: Any = None


class CustomBase:
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)


class DBItem(Base):
    id = Column(Integer, primary_key=True)
    value = Column(JSON)


Base.metadata.create_all(bind=engine)

db_session = SessionLocal()

item = db_session.query(DBItem).first()
if not item:
    item = DBItem(value={"foo": "Fighters", "bar": 3})
    db_session.add(item)
    db_session.commit()

db_session.close()


def get(db_session: Session, *, item_id: int) -> Optional[Item]:
    return db_session.query(DBItem).filter(DBItem.id == item_id).first()


def get_db(request: Request):
    return request.state.db


app = FastAPI()


@app.get("/{item_id}", response_model=Item)
def get_rule(*, db: Session = Depends(get_db), item_id: int):
    return get(db, item_id=item_id)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

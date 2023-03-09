from sqlalchemy import Column, Integer
from sqlalchemy_json import mutable_json_type
from sqlalchemy.dialects.postgresql import JSONB

from .database import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(mutable_json_type(dbtype=JSONB, nested=True))

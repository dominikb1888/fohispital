from pydantic import BaseModel
from typing import Any

class Resource(BaseModel):
    id: int
    data: dict = {}

class ResourceCreate(BaseModel):
    data: dict

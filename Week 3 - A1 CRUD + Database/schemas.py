from typing import Optional
from pydantic import BaseModel


# Schema for task creation request body
class TaskCreate(BaseModel):
    title: Optional[str] = None

    class Config:
        json_schema_extra = {"example": {"title": "Buy milk"}}


# Schema for task update request body
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

    class Config:
        json_schema_extra = {"example": {"title": "Buy organic milk", "done": True}}


# Schema for task response output representation
class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {"id": 1, "title": "Setup FastAPI project", "done": True}
        }

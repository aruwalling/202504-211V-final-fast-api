from datetime import datetime
from pydantic import BaseModel, Field


class StudentBase(BaseModel):
    dni: str = Field(..., min_length=8, max_length=8)
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0)
    grade: float = Field(..., ge=0, le=20)
    is_approved: bool


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    dni: str | None = Field(default=None, min_length=8, max_length=8)
    name: str | None = Field(default=None, min_length=1)
    age: int | None = Field(default=None, ge=0)
    grade: float | None = Field(default=None, ge=0, le=20)
    is_approved: bool | None = None


class StudentResponse(StudentBase):
    id: str
    created_at: datetime
    updated_at: datetime
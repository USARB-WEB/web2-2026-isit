from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=16, le=120)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int


class StudentQuery(BaseModel):
    """Filters carried in the body of an HTTP QUERY request."""

    first_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[str] = Field(default=None, min_length=1)
    min_age: Optional[int] = Field(default=None, ge=16, le=120)
    max_age: Optional[int] = Field(default=None, ge=16, le=120)

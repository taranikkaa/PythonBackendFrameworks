from pydantic import BaseModel
from typing import Optional, List

# Schema used when creating a course (Request Body)
class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int

# Schema used when updating a course (All fields optional)
class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[str] = None
    department_id: Optional[int] = None

# Base response schema for a course
class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int

    class Config:
        from_attributes = True

# Nested schema to demonstrate nested relationships
class DepartmentResponse(BaseModel):
    id: int
    name: str
    code: str
    courses: List[CourseResponse] = []

    class Config:
        from_attributes = True
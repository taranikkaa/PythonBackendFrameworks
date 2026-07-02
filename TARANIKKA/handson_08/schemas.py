from pydantic import BaseModel
from typing import Optional, List

class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None

class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int

    class Config:
        from_attributes = True

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
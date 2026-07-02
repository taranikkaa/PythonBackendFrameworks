from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from database import Base

class Department(Base):
    __tablename__ = "departments"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    code: Mapped[str] = mapped_column(unique=True, index=True)
    
    courses: Mapped[List["Course"]] = relationship(back_populates="department")

class Course(Base):
    __tablename__ = "courses"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    code: Mapped[str] = mapped_column(unique=True, index=True)
    credits: Mapped[int] = mapped_column()
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    
    department: Mapped["Department"] = relationship(back_populates="courses")
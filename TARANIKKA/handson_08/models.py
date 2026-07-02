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
    enrollments: Mapped[List["Enrollment"]] = relationship(back_populates="course")

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    enrollments: Mapped[List["Enrollment"]] = relationship(back_populates="student")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    
    course: Mapped["Course"] = relationship(back_populates="enrollments")
    student: Mapped["Student"] = relationship(back_populates="enrollments")
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from database import engine, Base, get_db
from models import Course, Student, Enrollment
from schemas import CourseCreate, CourseUpdate, CourseResponse, StudentResponse, EnrollmentCreate

# Step 75: Customizing OpenAPI Metadata
app = FastAPI(
    title='Course Management System API', 
    version='2.0',
    description='Advanced API tracking courses, departments, and dynamic background notifications.'
)

# Initialize database tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Background Task Function - Step 73
def send_confirmation_email(student_email: str):
    print(f"Sending confirmation email to {student_email}")

# --- COURSES ENDPOINTS ---

@app.get('/api/courses/', response_model=List[CourseResponse], tags=['Courses'])
async def get_courses(skip: int = 0, limit: int = 10, department_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(Course).offset(skip).limit(limit)
    if department_id is not None:
        query = query.where(Course.department_id == department_id)
    result = await db.execute(query)
    return result.scalars().all()

@app.get('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    return course

@app.post('/api/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED, tags=['Courses'], summary="Create a brand new Course configuration record")
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course

@app.put('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def update_course(course_id: int, course_data: CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    
    update_data = course_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)
    await db.commit()
    await db.refresh(course)
    return course

@app.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    await db.delete(course)
    await db.commit()
    return None

# Step 71: GET students enrolled in a specific course
@app.get('/api/courses/{course_id}/students/', response_model=List[StudentResponse], tags=['Courses'])
async def get_enrolled_students(course_id: int, db: AsyncSession = Depends(get_db)):
    course_check = await db.execute(select(Course).where(Course.id == course_id))
    if not course_check.scalar_one_or_none():
        raise HTTPException(status_code=404, detail='Course not found')
        
    query = select(Student).join(Enrollment).where(Enrollment.course_id == course_id)
    result = await db.execute(query)
    return result.scalars().all()

# --- ENROLLMENTS & BACKGROUND TASK ENDPOINTS ---

# Step 73 & 74: POST handling background workers
@app.post('/api/enrollments/', status_code=status.HTTP_201_CREATED, tags=['Enrollments'])
async def create_enrollment(enrollment: EnrollmentCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    new_enrollment = Enrollment(**enrollment.model_dump())
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)
    
    student_email = f"student_{enrollment.student_id}@university.edu"
    background_tasks.add_task(send_confirmation_email, student_email)
    
    return {"status": "success", "message": "Enrollment processed successfully"}
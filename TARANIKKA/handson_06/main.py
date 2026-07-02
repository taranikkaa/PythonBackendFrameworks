from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

# Import database configs, models, and schemas
from database import engine, Base, get_db
from models import Course, Department
from schemas import CourseCreate, CourseUpdate, CourseResponse

app = FastAPI(title='Course Management API', version='1.0')

# Automatically create all database tables when the app launches
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get('/')
def root():
    return {'message': 'API running and tables initialized'}

# 1. GET ALL COURSES (With pagination & filtering) - Step 63 & 67
@app.get('/api/courses/', response_model=List[CourseResponse])
async def get_courses(
    skip: int = 0, 
    limit: int = 10, 
    department_id: Optional[int] = None, 
    db: AsyncSession = Depends(get_db)
):
    query = select(Course).offset(skip).limit(limit)
    if department_id is not None:
        query = query.where(Course.department_id == department_id)
        
    result = await db.execute(query)
    return result.scalars().all()

# 2. GET SINGLE COURSE BY ID - Step 62
@app.get('/api/courses/{course_id}', response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# 3. POST CREATE NEW COURSE - Step 60
@app.post('/api/courses/', response_model=CourseResponse, status_code=201)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = Course(
        name=course.name,
        code=course.code,
        credits=course.credits,
        department_id=course.department_id
    )
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course

# 4. PUT UPDATE COURSE BY ID - Step 66
@app.put('/api/courses/{course_id}', response_model=CourseResponse)
async def update_course(course_id: int, course_data: CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Only update fields that were provided in request body
    update_dict = course_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(course, key, value)
        
    await db.commit()
    await db.refresh(course)
    return course

# 5. DELETE COURSE BY ID - Step 66
@app.delete('/api/courses/{course_id}', status_code=200)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    await db.delete(course)
    await db.commit()
    return {"message": f"Course {course_id} successfully deleted"}
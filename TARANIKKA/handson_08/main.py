from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Optional

from database import engine, Base, get_db
from models import Course
from schemas import CourseCreate, CourseUpdate, CourseResponse

# Step 75 & 82: API Versioning Configuration with OpenAPI Customization
app = FastAPI(
    title='RESTful Course Management System API', 
    version='1.0',
    description='Refactored API enforcing strict REST constraints, uniform pagination structures, and /api/v1/ prefix paths.'
)

# Initialize database schema arrays automatically on launch
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# --- REFACTORED COURSES ENDPOINTS ---

# Step 83 & 84: GET list with Offset Pagination envelope & Case-Insensitive Search Filter
@app.get('/api/v1/courses/', tags=['Courses'])
async def get_courses(
    page: int = 1, 
    page_size: int = 10, 
    search: Optional[str] = None, 
    db: AsyncSession = Depends(get_db)
):
    # Core Select Query
    query = select(Course)
    
    # Step 84: Case-insensitive dynamic search mapping logic
    if search:
        query = query.where(
            func.lower(Course.name).like(f"%{search.lower()}%") | 
            func.lower(Course.code).like(f"%{search.lower()}%")
        )
    
    # Track the exact total elements matching our filter condition
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total_count = total_result.scalar() or 0
    
    # Calculate offset locations matching selected limits
    offset_value = (page - 1) * page_size
    query = query.offset(offset_value).limit(page_size)
    
    result = await db.execute(query)
    courses = result.scalars().all()
    
    # Build relative pagination navigation string endpoints
    next_url = f"/api/v1/courses/?page={page + 1}&page_size={page_size}" if offset_value + page_size < total_count else None
    prev_url = f"/api/v1/courses/?page={page - 1}&page_size={page_size}" if page > 1 else None
    
    # Step 83: Return standard envelope matching assignment specifications
    return {
        "count": total_count,
        "next": next_url,
        "previous": prev_url,
        "results": [CourseResponse.model_validate(c) for c in courses]
    }

# Step 85: GET Course record tracking a Standardized Error format fallback structure
@app.get('/api/v1/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    
    if not course:
        # Step 85: Standardized custom error response format mapping
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "NOT_FOUND", 
                    "message": f"Course with id {course_id} does not exist", 
                    "field": None
                }
            }
        )
    return course

# Step 80 & 81: POST endpoint injecting explicit Location header map properties
@app.post('/api/v1/courses/', status_code=status.HTTP_201_CREATED, response_model=CourseResponse, tags=['Courses'])
async def create_course(course: CourseCreate, response: Response, db: AsyncSession = Depends(get_db)):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    
    # Step 81: Appending explicit REST location parameter values pointing to our structural record 
    response.headers["Location"] = f"/api/v1/courses/{new_course.id}/"
    return new_course

# Step 79: PATCH handler supporting dynamic partial model dictionary state changes
@app.patch('/api/v1/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def patch_course(course_id: int, course_data: CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    
    if not course:
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "NOT_FOUND", 
                    "message": f"Course with id {course_id} does not exist", 
                    "field": None
                }
            }
        )
    
    # Unpack properties provided by user to avoid blowing away existing fields
    update_dict = course_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(course, key, value)
        
    await db.commit()
    await db.refresh(course)
    return course

# Step 80: DELETE course yielding a standard 204 No Content success flag
@app.delete('/api/v1/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    
    if not course:
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "NOT_FOUND", 
                    "message": f"Course with id {course_id} does not exist", 
                    "field": None
                }
            }
        )
        
    await db.delete(course)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
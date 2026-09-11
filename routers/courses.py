from schemas import CourseResponse, CreateCourse
from models import Course
from database import get_db

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter

router = APIRouter(prefix="/courses")

@router.post("", response_model=CourseResponse, status_code=201)
def post_course(course: CreateCourse, db: Session = Depends(get_db)):
    db_course = Course(name = course.name)

    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course

@router.get("", response_model= list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()

    return courses

# courses.py
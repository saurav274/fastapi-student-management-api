from schemas import StudentCreate, StudentResponse, StudentUpdate
from models import Student, Course
from database import get_db
from auth import verify_api_key
from auth import authenticate_user

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Literal

router = APIRouter(prefix= "/students")

@router.post("", status_code = 201)
def create_students(
    student: StudentCreate,
    current_user = Depends(authenticate_user),
    db: Session = Depends(get_db)
):
    db_student = Student(
        name = student.name,
        age = student.age,
        course_id = student.course_id
    )

    course = db.query(Course).filter(Course.id == student.course_id).first()
    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Invalid Course id"
        )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student

@router.get("/{student_id}",response_model = StudentResponse)
def get_student(
    student_id: int,
    current_user = Depends(authenticate_user),
    db: Session = Depends(get_db)):

    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code = 404,
            detail= "Student not found"
        )
    
    return student

@router.get("", response_model= list[StudentResponse])
def get_students(
    current_user = Depends(authenticate_user),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    course_id: int | None = None ,
    sort_by: str | None = None,
    sort_order: Literal["asc", "desc"] = "desc",
    db: Session = Depends(get_db)
):

    sorting = {
        "age": Student.age,
        "id": Student.id,
        "name": Student.name
    }

    value = sorting.get(sort_by, Student.id)

    if sort_order == "desc":
        order = value.desc()

    elif sort_order == "asc":
        order = value.asc()
    
    offset = (page - 1)*limit

    student_query = db.query(Student)

    if course_id is not None:
        course = db.query(Course).filter(Course.id == course_id).first()
        if course is None:
            raise HTTPException(
                status_code = 404,
                detail = "Invalid course id"
            )
        student_query = student_query.filter(Student.course_id == course_id)

    student = student_query.order_by(order).offset(offset).limit(limit).all()

    return student

@router.put("/{student_id}",response_model = StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentCreate,
    current_user = Depends(authenticate_user),
    db: Session = Depends(get_db)
):
        
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code= 404,
            detail = "Student not found"
        )

    course = db.query(Course).filter(Course.id == student_data.course_id).first()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Invalid course id"
        )

    student.name = student_data.name
    student.age = student_data.age
    student.course_id = student_data.course_id

    
    db.commit()
    db.refresh(student)
    return student

@router.patch("/{student_id}",response_model = StudentResponse)
def partially_update_student(
    student_id: int,
    partially_update_data: StudentUpdate,
    current_user = Depends(authenticate_user),
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code= 404,
            detail="Student not found"
        )
    
    update_data = partially_update_data.model_dump(exclude_unset=True)

    if "course_id" in update_data:
        check_course = db.query(Course).filter(Course.id == partially_update_data.course_id).first()
        if check_course is None:
            raise HTTPException(
                status_code=404,
                detail="Invalid course id"
            )
    
    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(authenticate_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code= 404,
            detail = "Student not found"
        )
    
    db.delete(student)
    db.commit()
    return {"message": "Student removed successfully !"}
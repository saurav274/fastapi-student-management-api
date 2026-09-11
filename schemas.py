from pydantic import BaseModel, Field

class StudentCreate(BaseModel):
    name: str= Field(min_length=3, max_length=25)
    age: int= Field(ge=18, le=60)
    course_id: int

class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    course_id: int | None = None

class CreateCourse(BaseModel):
    name: str = Field(min_length=2, max_length=45)

class CourseResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    course_id: int
    course: CourseResponse

    model_config = {"from_attributes": True}

# schemas.py
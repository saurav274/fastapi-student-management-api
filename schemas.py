from pydantic import BaseModel, Field

class StudentCreate(BaseModel):
    name: str= Field(min_length=3, max_length=25)
    age: int= Field(ge=18, le=60)
    course_id: int

class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    course_id: int | None = None

class CreateUser(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=128)

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

class UserResponse(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}

# schemas.py
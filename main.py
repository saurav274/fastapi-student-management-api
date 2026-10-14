from database import Base, engine
from routers.students import router as students_router
from routers.courses import router as courses_router
from routers.users import router as users_router

from fastapi import FastAPI

app = FastAPI()

app.include_router(users_router)
app.include_router(students_router)
app.include_router(courses_router)

Base.metadata.create_all(engine)
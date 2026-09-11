# FastAPI Student Management API

A REST API built with FastAPI for managing students and courses. This project was built as a learning project to practice backend development with FastAPI, Pydantic, SQLAlchemy, and SQLite.

## Features

- Create and retrieve courses
- Create, retrieve, update, partially update, and delete students
- Validate request data using Pydantic
- Manage student-course relationships using SQLAlchemy
- Validate course IDs before assigning them to students
- Pagination for student records
- Filter students by course
- Sort students by ID, name, or age
- Support ascending and descending sorting
- HTTP error handling for missing students and courses
- Separate routers for students and courses

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Uvicorn

## Project Structure

```text
.
├── routers/
│   ├── __init__.py
│   ├── courses.py
│   └── students.py
├── database.py
├── main.py
├── models.py
├── schemas.py
├── requirements.txt
├── .gitignore
└── README.md
```

## API Endpoints

### Students

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /students | Create a student |
| GET | /students | Get students with pagination, filtering, and sorting |
| GET | /students/{student_id} | Get a student by ID |
| PUT | /students/{student_id} | Update a student |
| PATCH | /students/{student_id} | Partially update a student |
| DELETE | /students/{student_id} | Delete a student |

### Courses

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /courses | Create a course |
| GET | /courses | Get all courses |

## Query Parameters

The student listing endpoint supports the following query parameters:

- `page` — page number
- `limit` — number of students per page
- `course_id` — filter students by course
- `sort_by` — sort by `id`, `name`, or `age`
- `sort_order` — sort ascending (`asc`) or descending (`desc`)

Example:

```
GET /students?page=1&limit=10&sort_by=age&sort_order=asc
```

## Setup

Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment (Windows PowerShell):

```bash
venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

FastAPI automatically provides interactive API documentation:

- Swagger UI — `http://127.0.0.1:8000/docs`
- ReDoc — `http://127.0.0.1:8000/redoc`

## Database

The project currently uses SQLite for simplicity. Database tables are created from the SQLAlchemy models when the application starts.

## Purpose

This project was built to practice:

- FastAPI routing and dependency injection
- Pydantic validation and response models
- SQLAlchemy ORM
- Database relationships and foreign keys
- CRUD operations
- Pagination and query parameters
- API error handling

## Future Improvements

Planned improvements include:

- Authentication and authorization
- Password hashing
- Improved validation for partial updates
- Database migrations with Alembic
- Deployment
- Additional API functionality

## Status

This is an ongoing learning project. The API will be extended as new backend concepts are learned.
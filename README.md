# FastAPI Student Management API

A REST API built with FastAPI for managing students and courses, secured with JWT authentication and password hashing. This project was built as a learning project to practice backend development with FastAPI, Pydantic, SQLAlchemy, and SQLite.

## Features

- User registration and login with JWT access tokens (30-minute expiry)
- Password hashing with Argon2 (via `pwdlib`); plain passwords are never stored
- All student and course endpoints require authentication
- Alternative API key authentication through the `X-API-KEY` header
- Create and retrieve courses
- Create, retrieve, update, partially update, and delete students
- Validate request data using Pydantic
- Manage student-course relationships using SQLAlchemy
- Validate course IDs before assigning them to students
- Pagination for student records
- Filter students by course
- Sort students by ID, name, or age in ascending or descending order
- HTTP error handling for missing students and courses
- Separate routers for students, courses, and users

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- PyJWT
- pwdlib (Argon2)
- python-dotenv
- Uvicorn

## Project Structure

```text
.
├── routers/
│   ├── __init__.py
│   ├── courses.py
│   ├── students.py
│   └── users.py
├── auth.py
├── database.py
├── main.py
├── models.py
├── schemas.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Authentication

The API supports two ways to authenticate. Send either one with each request to a protected endpoint.

**1. JWT (for users)**

1. Register an account with `POST /user/register`.
2. Log in with `POST /user/login` (form fields: `username` and `password`). The response contains an access token.
3. Send the token in the `Authorization` header: `Authorization: Bearer <token>`.

Tokens expire after 30 minutes, after which you need to log in again.

**2. API key**

Send the key from your `.env` file in the `X-API-KEY` header.

**Using Swagger UI:** open `/docs`, click **Authorize**, enter your username and password, and all requests from the page will include your token.

Example with curl:

```bash
# Register
curl -X POST http://127.0.0.1:8000/user/register \
  -H "Content-Type: application/json" \
  -d '{"username": "saurav", "password": "strongpassword123"}'

# Log in
curl -X POST http://127.0.0.1:8000/user/login \
  -d "username=saurav&password=strongpassword123"

# Call a protected endpoint
curl http://127.0.0.1:8000/students \
  -H "Authorization: Bearer <your_token>"
```

> **Note:** Authentication is implemented, but role-based authorization is not. Any authenticated user can modify any record.

## API Endpoints

### Users

| Method | Endpoint | Auth required | Description |
|--------|----------|---------------|-------------|
| POST | /user/register | No | Register a new user |
| POST | /user/login | No | Log in and receive a JWT access token |
| GET | /user/me | JWT | Get the current logged-in user |

### Students

All student endpoints require authentication (JWT or API key).

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /students | Create a student |
| GET | /students | Get students with pagination, filtering, and sorting |
| GET | /students/{student_id} | Get a student by ID |
| PUT | /students/{student_id} | Update a student |
| PATCH | /students/{student_id} | Partially update a student |
| DELETE | /students/{student_id} | Delete a student |

### Courses

All course endpoints require authentication (JWT or API key).

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
git clone https://github.com/saurav274/fastapi-student-management-api.git
cd fastapi-student-management-api
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

Create your environment file by copying the example:

```bash
copy .env.example .env
```

Then open `.env` and set your own values:

```env
SECRET_KEY=your-generated-secret
API_KEY=your-api-key
```

Generate a secure secret key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
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

The project currently uses SQLite for simplicity. Tables for students, courses, and users are created from the SQLAlchemy models when the application starts. The users table stores only hashed passwords.

## Purpose

This project was built to practice:

- FastAPI routing and dependency injection
- Pydantic validation and response models
- SQLAlchemy ORM
- Database relationships and foreign keys
- CRUD operations
- Pagination and query parameters
- API error handling
- JWT authentication and password hashing
- Protecting routes with dependencies
- Managing secrets with environment variables

## Future Improvements

Planned improvements include:

- Role-based authorization
- Automated tests with pytest
- Database migrations with Alembic
- Deployment
- Additional API functionality

## Status

This is an ongoing learning project. The API will be extended as new backend concepts are learned.
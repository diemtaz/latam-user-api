# LATAM User Management API

REST API for user management built with FastAPI and SQLAlchemy.

This project was developed as part of a technical challenge and demonstrates clean architecture principles, repository pattern usage, and proper API design.

---

# 🚀 Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy (ORM)
- PosgrestSQl
- Uvicorn
- Pydantic

---

# 📂 Project Structure

latam-user-api/
│
├── app/
│ ├── api/ # Route definitions
│ ├── db/ # Database configuration and models
│ ├── repositories/ # Data access layer
│ ├── services/ # Business logic layer
│ ├── schemas/ # Pydantic schemas
│ └── main.py # Application entry point
│
├── requirements.txt
└── README.md

yaml
Copiar código

---

#  Architecture

The project follows a layered architecture:

### 1️⃣ API Layer (Routes)
Handles HTTP requests and responses.

### 2️⃣ Service Layer
Contains business logic and validations.

### 3️⃣ Repository Layer
Handles direct interaction with the database.

### 4️⃣ Schemas
Data validation and serialization using Pydantic.

### 5️⃣ Models
SQLAlchemy ORM models that map to database tables.

---

# Installation

## Clone the repository

```bash
git clone <your-repository-url>
cd latam-user-api
```
2️⃣ Create a virtual environment
```bash
python -m venv venv
```
## Activate the environment:
### Mac / Linux

```bash

source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### ▶️ Run the Application
```bash
uvicorn app.main:app --reload

```
The server will start at:

```bash
http://127.0.0.1:8000
```

### 📘 API Documentation
Once the application is running, you can access:

#### Swagger UI

```bash
http://127.0.0.1:8000/docs
```

#### ReDoc

```bash
http://127.0.0.1:8000/redoc
```

#### 📌 Available Endpoints

##### Users

| Method | Endpoint        | Description               |
|--------|----------------|--------------------------|
| POST   | /users/        | Create a new user        |
| GET    | /users/        | Get all users            |
| GET    | /users/{id}    | Get user by ID           |
| PATCH  | /users/{id}    | Partially update user    |
| PUT    | /users/{id}    | Replace user             |
| DELETE | /users/{id}    | Soft delete user         |


#### 🗄 Database
Default database: PostgrestSQL

Tables are created automatically on application startup:

```bash
Base.metadata.create_all(bind=engine)
```


#### 🔄 Soft Delete
Users are not physically removed from the database.
Instead, the active field is set to False.

This preserves historical data while preventing access to inactive users.
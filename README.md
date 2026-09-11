<div align="center">

# 🔐 FastAPI JWT Auth & Logging Application

### Secure Authentication • Structured Logging • Request Tracing • Async Database

<p>
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/JWT-RS256-black?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Structlog-Structured%20Logging-orange?style=for-the-badge" />
</p>

<p>
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white" />
  <img src="https://img.shields.io/badge/PyJWT-000000?style=for-the-badge" />
  <img src="https://img.shields.io/badge/bcrypt-Password%20Hashing-4B5563?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Uvicorn-Production%20Server-2F855A?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
</p>

<br>

> **A production-oriented FastAPI backend demonstrating secure JWT authentication, RS256 cryptography, PostgreSQL integration, CRUD APIs, structured logging, request tracing, middleware, exception handling, and log rotation.**

</div>

---

## 🚀 Project Overview

This project is a complete **FastAPI user management application** built around modern backend development practices.

It combines:

* 🔐 JWT (JSON Web Token) authentication
* 🔑 RS256 (RSA Signature with SHA-256)
* 🧂 bcrypt password hashing
* 🗄️ PostgreSQL database
* ⚡ Asynchronous SQLAlchemy ORM (Object Relational Mapper)
* 🔄 CRUD (Create, Read, Update, Delete) operations
* 🔎 Search and pagination
* 📝 Python structured logging
* 📊 JSON log formatting
* 🧩 Structlog structured logging
* 🌐 FastAPI middleware
* 🆔 Request ID tracing
* 🚨 Exception logging
* 📁 Rotating log files
* 📖 Swagger API documentation
* 🖥️ Streamlit client interface

---

# ✨ Features

<table>
<tr>
<td width="50%">

### 🔐 Authentication

* JWT authentication
* RS256 signing
* RSA private/public keys
* Token expiration
* Protected endpoints
* bcrypt password hashing
* Authentication & authorization

</td>

<td width="50%">

### 📊 Observability

* Structured logs
* JSON formatting
* Structlog processors
* Request middleware
* Request IDs
* Request duration
* Exception logging
* Rotating log files

</td>
</tr>

<tr>
<td>

### 🗄️ Database

* PostgreSQL
* SQLAlchemy ORM
* Async database operations
* User model
* Unique email validation
* Transaction rollback

</td>

<td>

### ⚡ API

* REST APIs
* CRUD operations
* Search
* Pagination
* Request validation
* HTTP status codes
* Swagger UI

</td>
</tr>
</table>

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │       Client         │
                         │  Streamlit / HTTP    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ FastAPI Middleware   │
                         │                      │
                         │ • Request ID         │
                         │ • Request Logging    │
                         │ • Error Handling     │
                         │ • Request Duration   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Authentication Layer │
                         │                      │
                         │ • JWT                │
                         │ • RS256              │
                         │ • bcrypt             │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     API Routes       │
                         │                      │
                         │ • Create User        │
                         │ • Get Users          │
                         │ • Update User        │
                         │ • Delete User        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   SQLAlchemy ORM     │
                         │   AsyncSession       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     PostgreSQL       │
                         │       Database       │
                         └──────────────────────┘
```

---

# 🔐 JWT Authentication

The application uses **JWT (JSON Web Token)** authentication with the **RS256** algorithm.

## Authentication Flow

```text
┌──────────┐
│   User   │
└────┬─────┘
     │
     │ Email + Password
     ▼
┌──────────────────┐
│     FastAPI      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ bcrypt Password  │
│    Verification  │
└────────┬─────────┘
         │
      Valid?
      /     \
    No       Yes
    │         │
    ▼         ▼
  401     JWT Creation
              │
              ▼
       RSA Private Key
              │
              │ Sign
              ▼
         Access Token
              │
              ▼
        Protected API
              │
              │ Verify
              ▼
       RSA Public Key
              │
              ▼
        API Response
```

---

# 🔑 Why RS256?

**RS256** uses asymmetric cryptography.

```text
             RSA PRIVATE KEY
                    │
                    │ Sign
                    ▼
                ┌───────┐
                │  JWT  │
                └───┬───┘
                    │
                    │ Verify
                    ▼
             RSA PUBLIC KEY
```

### Private Key

Used to **sign** tokens.

### Public Key

Used to **verify** tokens.

The private key is never committed to the repository.

---

# 📝 Structured Logging

The project implements structured logging using:

### Python `logging`

The application uses:

* Log levels
* Handlers
* Formatters
* JSON formatting
* Error logging
* Exception logging
* `RotatingFileHandler`

### Structlog

Structured application logging is implemented using:

* Structlog processors
* JSON rendering
* Structured event fields
* Context variables
* Request IDs

---

# 📊 Request Logging

FastAPI middleware captures information about every request.

```text
HTTP Request
     │
     ▼
┌─────────────────────┐
│ FastAPI Middleware  │
├─────────────────────┤
│ Request ID          │
│ HTTP Method         │
│ Request Path        │
│ Status Code         │
│ Request Duration    │
│ Exception Details   │
└──────────┬──────────┘
           │
           ▼
      Structured Log
           │
           ▼
        JSON Log
```

Example:

```json
{
  "event": "request_completed",
  "method": "POST",
  "path": "/users",
  "status_code": 409,
  "duration_ms": 232.46,
  "request_id": "9e7a57b8-79a2-47fa-95ae-226e7b6477a3"
}
```

---

# 🆔 Request ID Tracing

Every incoming request receives a unique **UUID (Universally Unique Identifier)**.

Example:

```text
request_id = 9e7a57b8-79a2-47fa-95ae-226e7b6477a3
```

All logs generated during that request can share the same ID.

```text
POST /users
      │
      ├── request_id = abc-123
      │
      ├── user_creation_failed
      │
      └── request_completed
```

This makes debugging and tracing individual requests much easier.

---

# 📁 Log Rotation

The application uses `RotatingFileHandler` to prevent log files from growing indefinitely.

Example:

```text
logs/
│
├── app.log
├── app.log.1
├── app.log.2
├── app.log.3
├── app.log.4
└── app.log.5
```

When the active log file reaches the configured size, older logs are rotated automatically.

---

# 👤 User API

| Method   | Endpoint      | Description         |
| -------- | ------------- | ------------------- |
| `POST`   | `/users`      | Create a user       |
| `GET`    | `/users`      | Get users           |
| `GET`    | `/users/{id}` | Get a specific user |
| `PUT`    | `/users/{id}` | Update a user       |
| `DELETE` | `/users/{id}` | Delete a user       |
| `POST`   | `/login`      | Authenticate user   |

---

# 🔎 Search & Pagination

The user listing API supports search and pagination.

Example:

```text
GET /users?search=gmail&page=1&page_size=10
```

Supported parameters:

```text
search
page
page_size
```

This allows large datasets to be retrieved efficiently instead of loading every record at once.

---

# 🛡️ Security

The application follows several security practices:

* 🔑 Passwords are hashed using bcrypt.
* 🚫 Password hashes are never returned in API responses.
* 🔐 JWT tokens are signed using RS256.
* 🔒 RSA private keys remain outside source control.
* ⏱️ JWT tokens have an expiration time.
* 🛡️ Protected endpoints require authentication.
* 🔐 Sensitive configuration is stored in environment variables.
* 🚨 Authentication failures are logged.
* 🧹 Database transactions are rolled back after failed operations.

---

# 🧰 Tech Stack

<div align="center">

| Technology     | Purpose             |
| -------------- | ------------------- |
| 🐍 Python      | Backend language    |
| ⚡ FastAPI      | API framework       |
| 🗄️ PostgreSQL | Database            |
| 🔄 SQLAlchemy  | ORM                 |
| 🧩 Psycopg     | PostgreSQL driver   |
| 📋 Pydantic    | Data validation     |
| 🔐 PyJWT       | JWT implementation  |
| 🔑 bcrypt      | Password hashing    |
| 📊 Structlog   | Structured logging  |
| 📝 Logging     | Application logging |
| 🚀 Uvicorn     | ASGI server         |
| 🖥️ Streamlit  | UI/client           |

</div>

---

# 📂 Project Structure

```text
fastapi-jwt-auth-logging-app/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── auth.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── loggers.py
│
├── ui/
│   └── streamlit_app.py
│
├── logs/
│   └── app.log
│
├── .env
├── .gitignore
├── pyproject.toml
└── README.md
```

> ⚠️ `.env`, RSA private keys, virtual environments, cache files, and sensitive log files should not be committed to Git.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/fastapi-jwt-auth-logging-app.git
```

```bash
cd fastapi-jwt-auth-logging-app
```

---

## 2. Install dependencies

If using `uv`:

```bash
uv sync
```

---

## 3. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=your_database_url
```

Keep secrets and credentials outside version control.

---

# 🗄️ Database Configuration

Create a PostgreSQL database and configure the connection string.

Example:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/database_name
```

---

# ▶️ Run the Backend

Start the FastAPI application:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# 📖 API Documentation

FastAPI automatically provides interactive Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can use Swagger UI to:

* Register users
* Login
* Authorize using JWT
* Test protected endpoints
* Test CRUD operations
* Test search and pagination

---

# 🖥️ Run the Streamlit UI

Start the UI:

```bash
streamlit run ui/streamlit_app.py
```

The Streamlit client provides a simple interface for interacting with the backend APIs.

---

# 🧪 Authentication Testing

Recommended testing flow:

```text
1. Register User
       ↓
2. Login
       ↓
3. Receive JWT
       ↓
4. Authorize in Swagger
       ↓
5. Call Protected API
       ↓
6. JWT Verified
       ↓
7. API Response
```

---

# 📌 HTTP Status Codes

The API uses meaningful HTTP status codes.

| Status | Meaning                        |
| ------ | ------------------------------ |
| `200`  | Successful request             |
| `201`  | Resource created               |
| `400`  | Bad request                    |
| `401`  | Authentication required/failed |
| `403`  | Access forbidden               |
| `404`  | Resource not found             |
| `409`  | Resource conflict              |
| `422`  | Validation error               |
| `500`  | Internal server error          |

Example:

```text
409 Conflict
    ↓
Email already exists
```

---

# 🧠 Concepts Demonstrated

This project demonstrates practical understanding of:

```text
FastAPI
   ↓
REST APIs
   ↓
SQLAlchemy ORM
   ↓
PostgreSQL
   ↓
Async Database Operations
   ↓
CRUD
   ↓
Authentication
   ↓
Authorization
   ↓
JWT
   ↓
RS256
   ↓
bcrypt
   ↓
Structured Logging
   ↓
Structlog
   ↓
Middleware
   ↓
Request Tracing
   ↓
Exception Handling
   ↓
Log Rotation
```

---

# 🔮 Future Improvements

Planned improvements can include:

* 🔄 Refresh token implementation
* 🚫 JWT token revocation
* 🆔 JWT `jti` tracking
* 👥 Role-Based Access Control (RBAC)
* 🔑 RSA key rotation
* 🏷️ JWT `kid` support
* 🌐 JSON Web Key Set (JWKS)
* 🧪 Automated testing
* 🐳 Docker support
* 📊 Centralized log monitoring
* 🚀 Production deployment

---

# 📸 Demo

Add screenshots or a short GIF here to showcase:

```text
Swagger UI
   ↓
Login
   ↓
JWT Authorization
   ↓
User Management
   ↓
Structured Logs
```

Example:

```html
<p align="center">
  <img src="assets/demo.gif" width="900">
</p>
```

---

# 📚 Learning Focus

This project was developed as a hands-on backend engineering project focused on understanding how authentication, databases, APIs, and observability work together in a real application.

The goal is not only to implement the features, but also to understand the underlying architecture and security principles.

---

<div align="center">

## ⭐ Built with FastAPI, PostgreSQL, JWT & Structlog

**Secure APIs • Clean Architecture • Structured Observability**

<br>

### 🔐 Authenticate → 🛡️ Authorize → 📊 Observe → 🚀 Improve

</div>

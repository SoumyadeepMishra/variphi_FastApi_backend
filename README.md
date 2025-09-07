# FastAPI MVC Template

A complete FastAPI server template with MVC architecture, authentication, and database integration.

## Features

- **FastAPI** with automatic API documentation
- **SQLAlchemy** ORM with database models
- **Pydantic** for data validation and serialization
- **JWT Authentication** with OAuth2
- **Password hashing** with bcrypt
- **CORS middleware** for cross-origin requests
- **MVC Architecture** with proper separation of concerns
- **Environment configuration** with pydantic-settings

## Project Structure

```
app/
├── __init__.py
├── main.py                 # FastAPI application entry point
├── config.py              # Application configuration
├── database.py            # Database connection and session
├── models/                # SQLAlchemy database models
│   ├── __init__.py
│   └── user.py
├── schemas/               # Pydantic schemas for request/response
│   ├── __init__.py
│   └── user.py
├── views/                 # API route handlers
│   ├── __init__.py
│   ├── user_view.py
│   └── auth_view.py
├── services/              # Business logic layer
│   ├── __init__.py
│   ├── user_service.py
│   └── auth_service.py
└── middleware/            # Custom middleware
    ├── __init__.py
    └── cors.py
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.py
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the development server:**
   ```bash
   python run.py
   # or
   uvicorn app.main:app --reload
   ```

4. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Users
- `GET /users/` - Get all users
- `GET /users/{user_id}` - Get user by ID
- `POST /users/` - Create new user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### General
- `GET /` - Root endpoint
- `GET /health` - Health check

## Database

The template uses SQLite by default. To use PostgreSQL or MySQL:

1. Update `DATABASE_URL` in your `.env` file
2. Install the appropriate database driver:
   - PostgreSQL: `pip install psycopg2-binary`
   - MySQL: `pip install PyMySQL`

## Authentication

The template includes JWT-based authentication:

1. Create a user via `POST /users/`
2. Login via `POST /auth/login` to get an access token
3. Use the token in the `Authorization: Bearer <token>` header for protected endpoints

## Configuration

All configuration is managed through environment variables and the `app/config.py` file. Key settings:

- `APP_NAME`: Application name
- `DEBUG`: Enable debug mode
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Development

The template follows FastAPI best practices:

- **Type hints** throughout the codebase
- **Automatic validation** with Pydantic
- **Dependency injection** for database sessions
- **Proper error handling** with HTTP exceptions
- **Service layer** for business logic
- **Separation of concerns** with MVC architecture

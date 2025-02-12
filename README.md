# Users and Tasks API

## Prerequisites

- Python 3.12
- SQlite database
- Poetry

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
DATABASE_URL="sqlite+aiosqlite:///database.db"
JWT_SECRET_KEY="your-secret-key"
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd users_and_tasks
```

2. Set up a virtual environment (optional but recommended):
```bash
poetry env use python
```
or
```bash
poetry env use /path/to/python/of/specific/version
```

3. Install dependencies:
```bash
poetry install
```

## Database Setup

1. Update the `DATABASE_URL` in your `.env` file
2. Run database migrations:
```bash
alembic upgrade head
```

## Running the Application

1. Start the application:
```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Available Endpoints

- Authentication: `/auth/jwt/*`
- Users: `/users/*`
- Tasks: `/tasks/*`

## Development

For development with hot reload:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

For testing:
```bash
poetry run pytest
```

## Docker
To make image:
```bash
docker build -t users_and_tasks
```
To start container:
```bash
docker run -p 80:80 users_and_tasks
```
The site will be available at the url: http://0.0.0.0:80
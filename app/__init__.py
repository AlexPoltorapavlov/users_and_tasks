"""
FastAPI-based Task Management System with JWT Authentication

Project Structure:
├── alembic           - Database migrations (version control for DB schema)
├── app               - Core application components
│   ├── auth          - JWT authentication system (Bearer token transport)
│   ├── errors        - Custom exceptions
│   ├── managers      - Business logic layer (data processing/validation)
│   ├── models        - Database models/SQLAlchemy ORM entities
│   ├── repositories  - Database interaction layer (CRUD operations)
│   ├── routes        - API endpoints definition (FastAPI routers)
│   └── schemas       - Pydantic validation schemas (request/response models)
├── tests             - Test suite (unit/integration tests)

Key Architecture Principles:
- Clear separation of concerns (business logic ↔ data access ↔ presentation)
- Asynchronous database sessions throughout the stack
- Environment-based configuration management
- Type hinting and schema validation at all layers

Main Components:
• auth/              - Handles user registration/login/JWT token management
• managers/          - Task/User business logic (pre/post DB processing)
• repositories/      - DB operations (TaskRepository, UserRepository)
• routes/            - Organized API endpoints following REST conventions
• schemas/           - Strong typing with Pydantic (input/output validation)

Supporting Files:
• config.py          - Centralized environment configuration (.env loader)
• db.py              - Database engine/session factory setup
• main.py            - Application entry point (FastAPI instance initialization)
"""

__version__ = "0.1.0"
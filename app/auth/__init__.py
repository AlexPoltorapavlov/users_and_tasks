"""
User authentication and registration service.

Core components:
- Built using the FastAPI Users library.
- JWT tokens for authentication.
- Token transport mechanism: Bearer (via HTTP headers).

Architecture:
* UserManager: handles user-related business logic (registration, 
  validation, request processing).
* UserRepository: manages database interactions 
  (located in app/repositories).

Supported features:
- User registration
- Login/password authentication
- JWT token refresh
- Logout functionality
"""
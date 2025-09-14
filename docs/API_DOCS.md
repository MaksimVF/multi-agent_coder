
# API Documentation

## Table of Contents
1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Request/Response Format](#requestresponse-format)
4. [Error Handling](#error-handling)

## Authentication

The API uses JWT for authentication. Include the token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Authentication
- **POST /api/auth/login** - User login
- **POST /api/auth/register** - User registration
- **POST /api/auth/refresh** - Refresh token

### Users
- **GET /api/users** - Get user list
- **GET /api/users/{id}** - Get user details
- **POST /api/users** - Create user
- **PUT /api/users/{id}** - Update user
- **DELETE /api/users/{id}** - Delete user

## Request/Response Format

All requests and responses use JSON format.

### Example Request
```json
{
    "username": "testuser",
    "password": "securepassword"
}
```

### Example Response
```json
{
    "id": 1,
    "username": "testuser",
    "token": "jwt.token.here"
}
```

## Error Handling

Errors are returned with appropriate HTTP status codes and JSON body:
```json
{
    "error": "error_code",
    "message": "Error description"
}
```

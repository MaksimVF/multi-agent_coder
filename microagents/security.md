

---
name: security
type: knowledge
version: 1.0.0
agent: DeveloperAgent
triggers:
- security
- vulnerability
- authentication
- authorization
- permissions
- secure
- encryption
- oauth
- jwt
---

This document provides guidance on security best practices for development.

## Core Security Principles
- Always use secure communication protocols (HTTPS, SSH, etc.)
- Never store sensitive data (passwords, tokens, keys) in code or version control
- Apply the principle of least privilege
- Validate and sanitize all user inputs
- Use parameterized queries to prevent SQL injection
- Implement proper error handling to avoid information leakage

## Common Security Checks
- Ensure proper authentication and authorization mechanisms
- Verify secure session management
- Confirm secure storage of sensitive data (use encryption)
- Validate secure configuration of services and APIs
- Implement rate limiting to prevent abuse

## Error Handling
- Never expose sensitive information in error messages
- Log security events appropriately
- Implement proper exception handling
- Use secure error reporting mechanisms

## Authentication Best Practices
- Use multi-factor authentication when possible
- Implement proper password hashing (bcrypt, Argon2)
- Use secure token storage and transmission
- Validate JWT tokens properly

## API Security
- Use API gateways for rate limiting and authentication
- Validate all input parameters
- Implement proper CORS configuration
- Use OAuth2 or similar standards for API authentication


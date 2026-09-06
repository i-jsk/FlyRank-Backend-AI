from typing import Optional

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from supabase_client import supabase


class AuthException(Exception):
    """Custom authentication exception with status code and error message."""

    def __init__(self, status_code: int, error: str):
        self.status_code = status_code
        self.error = error
        super().__init__(error)


# Reusable OpenAPI Bearer security scheme for Swagger UI & route protection
security = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
):
    """Reusable FastAPI dependency / middleware guard that verifies Supabase JWT.

    Extracts Bearer token, validates it against Supabase, and returns the User object.
    Raises AuthException(401) on missing, malformed, invalid, or expired tokens.
    """
    token: Optional[str] = None

    if credentials and credentials.credentials:
        token = credentials.credentials.strip()
    else:
        # Fallback check on raw Authorization header for non-standard clients
        auth_header = request.headers.get("authorization")
        if not auth_header:
            raise AuthException(status_code=401, error="Access token required")

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1].strip():
            raise AuthException(status_code=401, error="Access token required")

        token = parts[1].strip()

    if not token:
        raise AuthException(status_code=401, error="Access token required")

    try:
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise AuthException(status_code=401, error="Invalid or expired token")

        # Store token and verified user on request.state for downstream handlers
        request.state.user = user_response.user
        request.state.token = token
        return user_response.user

    except AuthException:
        raise
    except Exception:
        # If Supabase rejects the token as invalid, tampered, or expired
        raise AuthException(status_code=401, error="Invalid or expired token")

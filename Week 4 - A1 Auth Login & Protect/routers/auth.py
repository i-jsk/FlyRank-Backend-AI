from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from schemas import UserAuth
from supabase_client import supabase

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", status_code=201, summary="User Sign Up")
def sign_up(payload: UserAuth):
    """Register a new user account with Supabase Auth.

    Validates required credentials, returning 400 on missing or empty fields.
    Returns 201 Created with the user object on success.
    """
    if (
        not payload.email
        or not payload.password
        or not str(payload.email).strip()
        or not str(payload.password).strip()
    ):
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required"},
        )

    clean_email = str(payload.email).strip()
    clean_password = str(payload.password).strip()

    try:
        res = supabase.auth.sign_up(
            {"email": clean_email, "password": clean_password}
        )

        if not res.user:
            return JSONResponse(
                status_code=400,
                content={"error": "Failed to create user account"},
            )

        user_dict = jsonable_encoder(res.user)
        return JSONResponse(status_code=201, content=user_dict)

    except Exception as e:
        error_msg = str(e)
        if hasattr(e, "message") and e.message:
            error_msg = e.message
        return JSONResponse(
            status_code=400,
            content={"error": error_msg},
        )


@router.post("/login", status_code=200, summary="User Log In")
def login(payload: UserAuth):
    """Authenticate an existing user with Supabase Auth.

    Validates required credentials (400 if empty/missing).
    Returns 401 if credentials are rejected.
    Returns 200 with access_token and refresh_token on success.
    """
    if (
        not payload.email
        or not payload.password
        or not str(payload.email).strip()
        or not str(payload.password).strip()
    ):
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required"},
        )

    clean_email = str(payload.email).strip()
    clean_password = str(payload.password).strip()

    try:
        res = supabase.auth.sign_in_with_password(
            {"email": clean_email, "password": clean_password}
        )

        if not res.session or not res.session.access_token:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid login credentials"},
            )

        user_dict = jsonable_encoder(res.user) if res.user else None

        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "token_type": res.session.token_type or "bearer",
            "user": user_dict,
        }

    except Exception:
        # Per specification: If Supabase rejects credentials, return 401 with {"error": "Invalid login credentials"}
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid login credentials"},
        )

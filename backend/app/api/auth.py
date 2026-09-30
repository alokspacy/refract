from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new teacher or user"
)
def register(req: UserRegisterRequest, db: Session = Depends(get_db)):
    """Register a new user account and return JWT access token."""
    user = AuthService.register_user(db, req)
    return AuthService.create_token_response(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate and receive JWT token"
)
def login(req: UserLoginRequest, db: Session = Depends(get_db)):
    """Log in with email and password to receive JWT access token."""
    user = AuthService.authenticate_user(db, req)
    return AuthService.create_token_response(user)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user profile"
)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Return the profile details of the currently authenticated user."""
    return current_user

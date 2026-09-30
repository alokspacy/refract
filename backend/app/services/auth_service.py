import logging
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse

logger = logging.getLogger("accesslearn.auth")


class AuthService:
    @staticmethod
    def register_user(db: Session, req: UserRegisterRequest) -> User:
        email = req.email.strip().lower()
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            logger.warning(f"Registration failed: duplicate email {email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "EMAIL_ALREADY_EXISTS", "message": "A user with this email already exists."}
            )

        hashed = hash_password(req.password)
        user = User(
            email=email,
            password_hash=hashed,
            name=req.name.strip(),
            role=req.role or "teacher",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User registered successfully: id={user.id}, email={user.email}")
        return user

    @staticmethod
    def authenticate_user(db: Session, req: UserLoginRequest) -> User:
        email = req.email.strip().lower()
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(req.password, user.password_hash):
            logger.warning(f"Login failed for email={email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "INVALID_CREDENTIALS", "message": "Invalid email or password."}
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "USER_INACTIVE", "message": "User account is disabled."}
            )

        logger.info(f"User authenticated successfully: id={user.id}, email={user.email}")
        return user

    @staticmethod
    def create_token_response(user: User) -> TokenResponse:
        token = create_access_token(
            subject=user.id,
            extra_claims={"email": user.email, "role": user.role}
        )
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )

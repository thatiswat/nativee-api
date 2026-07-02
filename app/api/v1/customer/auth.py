from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import (
    LoginResponse,
    UserCreateRequest,
    UserLoginRequest,
    UserMessageResponse,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ==========================================================
# Register
# ==========================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: UserCreateRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        user = service.register(request)
        return UserResponse.model_validate(user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ==========================================================
# Login
# ==========================================================

@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        token = service.login(request)

        return LoginResponse(
            access_token=token,
            token_type="bearer",
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


# ==========================================================
# Current User
# ==========================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):
    return UserResponse.model_validate(current_user)
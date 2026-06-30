from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


# ==========================================================
# Register
# ==========================================================

class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "password123",
            }
        }
    )


# ==========================================================
# Login
# ==========================================================

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "password": "password123",
            }
        }
    )


# ==========================================================
# Response
# ==========================================================

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "role": "customer",
                "is_active": True,
                "created_at": "2026-06-30T18:30:00Z",
                "updated_at": "2026-06-30T18:30:00Z",
            }
        },
    )


# ==========================================================
# Message
# ==========================================================

class UserMessageResponse(BaseModel):
    success: bool
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "User created successfully",
            }
        }
    )
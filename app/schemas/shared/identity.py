from pydantic import BaseModel, EmailStr


class IdentityClaims(BaseModel):
    id: int
    public_id: str
    email: EmailStr
    name: str
    role: str
    session_id: str
    is_active: bool
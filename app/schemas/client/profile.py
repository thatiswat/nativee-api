from pydantic import BaseModel


class ClientProfileResponse(BaseModel):
    id: str
    email: str
    name: str | None = None
    avatar: str | None = None
    primary_language: str | None = None
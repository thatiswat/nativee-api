from pydantic import BaseModel


class CreateAPIKeyRequest(BaseModel):
    name: str
    live: bool = True


class CreateAPIKeyResponse(BaseModel):
    id: int
    name: str
    api_key: str
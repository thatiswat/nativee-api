from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    translation_provider: str
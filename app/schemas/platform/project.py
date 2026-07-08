from pydantic import BaseModel, ConfigDict


# ==========================================================
# Create
# ==========================================================

class CreateProjectRequest(BaseModel):
    name: str
    description: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Nativee Production",
                "description": "Production APIs",
            }
        }
    )


# ==========================================================
# Update
# ==========================================================

class UpdateProjectRequest(BaseModel):
    name: str
    description: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Nativee Development",
                "description": "Development Environment",
            }
        }
    )


# ==========================================================
# Response
# ==========================================================

class ProjectResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Nativee Production",
                "slug": "nativee-production",
                "description": "Production APIs",
            }
        },
    )


# ==========================================================
# List Response
# ==========================================================

class ProjectsResponse(BaseModel):
    projects: list[ProjectResponse]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "projects": [
                    {
                        "id": 1,
                        "name": "Nativee Production",
                        "slug": "nativee-production",
                        "description": "Production APIs",
                    }
                ]
            }
        }
    )


# ==========================================================
# Message
# ==========================================================

class ProjectMessageResponse(BaseModel):
    success: bool
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Project deleted",
            }
        }
    )
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.platform.project import (
    CreateProjectRequest,
    ProjectMessageResponse,
    ProjectResponse,
    ProjectsResponse,
    UpdateProjectRequest,
)
from app.services.platform.projects import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


# ==========================================================
# Create Project
# ==========================================================

@router.post(
    "",
    response_model=ProjectResponse,
    summary="Create Project",
)
def create_project(
    request: CreateProjectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ProjectService(db)

    return service.create(
        user_id=current_user.id,
        name=request.name,
        description=request.description,
    )


# ==========================================================
# List Projects
# ==========================================================

@router.get(
    "",
    response_model=ProjectsResponse,
    summary="List Projects",
)
def get_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ProjectService(db)

    return {
        "projects": service.get_all(
            user_id=current_user.id,
        )
    }


# ==========================================================
# Get Project (SECURED)
# ==========================================================

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get Project",
)
def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ProjectService(db)

    return service.get(
        user_id=current_user.id,
        project_id=project_id,
    )


# ==========================================================
# Update Project (SECURED)
# ==========================================================

@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update Project",
)
def update_project(
    project_id: int,
    request: UpdateProjectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ProjectService(db)

    return service.update(
        user_id=current_user.id,
        project_id=project_id,
        name=request.name,
        description=request.description,
    )


# ==========================================================
# Delete Project (SECURED)
# ==========================================================

@router.delete(
    "/{project_id}",
    response_model=ProjectMessageResponse,
    summary="Delete Project",
)
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ProjectService(db)

    return service.delete(
        user_id=current_user.id,
        project_id=project_id,
    )
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.project import (
    CreateProjectRequest,
    ProjectMessageResponse,
    ProjectResponse,
    ProjectsResponse,
    UpdateProjectRequest,
)
from app.services.project_service import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)

service = ProjectService


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
    return service(db).create(
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
    return {
        "projects": service(db).get_all(
            current_user.id,
        )
    }


# ==========================================================
# Get Project
# ==========================================================

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get Project",
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    return service(db).get(project_id)


# ==========================================================
# Update Project
# ==========================================================

@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update Project",
)
def update_project(
    project_id: int,
    request: UpdateProjectRequest,
    db: Session = Depends(get_db),
):
    return service(db).update(
        project_id=project_id,
        name=request.name,
        description=request.description,
    )


# ==========================================================
# Delete Project
# ==========================================================

@router.delete(
    "/{project_id}",
    response_model=ProjectMessageResponse,
    summary="Delete Project",
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    return service(db).delete(project_id)
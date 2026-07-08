from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.project import Project
from app.models.user import User
from app.services.platform.analytics import AnalyticsService

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/overview")
async def overview(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project or project.owner_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return AnalyticsService(db).overview(
        project_id,
    )
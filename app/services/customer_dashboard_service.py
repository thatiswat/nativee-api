from sqlalchemy.orm import Session

from app.models.api_key import APIKey
from app.models.project import Project
from app.repositories.api_key_repository import APIKeyRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.usage_repository import UsageRepository

from app.schemas.customer_dashboard import (
    DashboardActivity,
    DashboardProject,
    DashboardResponse,
    DashboardStats,
    DashboardUser,
)


class CustomerDashboardService:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.project_repository = ProjectRepository(db)
        self.api_key_repository = APIKeyRepository(db)
        self.usage_repository = UsageRepository(db)

    def overview(
        self,
        user,
    ) -> DashboardResponse:

        project_count = self.project_repository.count_by_user(
            user.id,
        )

        api_key_count = self.api_key_repository.count_by_user(
            user.id,
        )

        latest_key = (
            self.db.query(APIKey)
            .join(APIKey.plan)
            .join(APIKey.project)
            .filter(
                APIKey.project.has(owner_id=user.id)
            )
            .order_by(APIKey.created_at.desc())
            .first()
        )

        current_plan = (
            latest_key.plan.name
            if latest_key
            else "Free"
        )

        projects = self.project_repository.get_by_user(
            user.id,
        )

        dashboard_projects = []

        for project in projects:

            project_api_key_count = len(project.api_keys)

            requests = self.usage_repository.count_by_project(
                project.id,
            )

            plan = (
                project.api_keys[0].plan.name
                if project.api_keys
                else "Free"
            )

            dashboard_projects.append(
                DashboardProject(
                    id=project.id,
                    name=project.name,
                    plan=plan,
                    api_keys=project_api_key_count,
                    requests=requests,
                )
            )

        total_requests = self.usage_repository.count_by_user(
            user.id,
        )

        projects = (
            self.db.query(Project)
            .filter(
                Project.owner_id == user.id,
            )
            .all()
        )

        api_keys = (
            self.db.query(APIKey)
            .join(Project)
            .filter(
                Project.owner_id == user.id,
            )
            .all()
        )

        activities = []

        for project in projects:
            activities.append(
                DashboardActivity(
                    id=project.id,
                    message=f"Created project '{project.name}'",
                    created_at=project.created_at.isoformat(),
                )
            )

        for key in api_keys:
            activities.append(
                DashboardActivity(
                    id=100000 + key.id,
                    message=f"Created API key '{key.name}'",
                    created_at=key.created_at.isoformat(),
                )
            )

        activities.sort(
            key=lambda x: x.created_at,
            reverse=True,
        )

        return DashboardResponse(
            user=DashboardUser(
                id=user.id,
                name=user.name,
            ),
            stats=DashboardStats(
                projects=project_count,
                api_keys=api_key_count,
                requests=total_requests,
                current_plan=current_plan,
            ),
            projects=dashboard_projects,
            activities=activities,
        )
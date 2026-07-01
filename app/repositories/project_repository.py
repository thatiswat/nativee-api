from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    # ----------------------------------
    # Create
    # ----------------------------------

    def create(
        self,
        project: Project,
    ) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project

    # ----------------------------------
    # Read
    # ----------------------------------

    def get(
        self,
        project_id: int,
    ) -> Project | None:
        return (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

    def get_owned(
        self,
        user_id: int,
        project_id: int,
    ) -> Project | None:
        return (
            self.db.query(Project)
            .filter(
                Project.id == project_id,
                Project.user_id == user_id,
            )
            .first()
        )

    def get_by_slug(
        self,
        slug: str,
    ) -> Project | None:
        return (
            self.db.query(Project)
            .filter(Project.slug == slug)
            .first()
        )

    def get_all(
        self,
    ) -> list[Project]:
        return (
            self.db.query(Project)
            .order_by(Project.created_at.desc())
            .all()
        )

    # ----------------------------------
    # User
    # ----------------------------------

    def get_by_user(
        self,
        user_id: int,
    ) -> list[Project]:
        return (
            self.db.query(Project)
            .filter(
                Project.user_id == user_id,
            )
            .order_by(
                Project.created_at.desc(),
            )
            .all()
        )

    def count_by_user(
        self,
        user_id: int,
    ) -> int:
        return (
            self.db.query(Project)
            .filter(
                Project.user_id == user_id,
            )
            .count()
        )

    # ----------------------------------
    # Update
    # ----------------------------------

    def update(
        self,
        project: Project,
    ) -> Project:
        self.db.commit()
        self.db.refresh(project)

        return project

    # ----------------------------------
    # Delete
    # ----------------------------------

    def delete(
        self,
        project: Project,
    ) -> None:
        self.db.delete(project)
        self.db.commit()
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
        print("PROJECT:", project.__dict__)

        self.db.add(project)

        print("BEFORE COMMIT:", project.__dict__)

        self.db.commit()

        print("AFTER COMMIT:", project.__dict__)

        self.db.refresh(project)

        print("AFTER REFRESH:", project.__dict__)

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
        owner_id: int,
        project_id: int,
    ) -> Project | None:
        return (
            self.db.query(Project)
            .filter(
                Project.id == project_id,
                Project.owner_id == owner_id,
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
    # Owner scoped queries
    # ----------------------------------

    def get_by_user(
        self,
        owner_id: int,
    ) -> list[Project]:
        return (
            self.db.query(Project)
            .filter(
                Project.owner_id == owner_id,
            )
            .order_by(
                Project.created_at.desc(),
            )
            .all()
        )

    def count_by_user(
        self,
        owner_id: int,
    ) -> int:
        return (
            self.db.query(Project)
            .filter(
                Project.owner_id == owner_id,
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
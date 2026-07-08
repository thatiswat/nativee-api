from re import sub

from fastapi import HTTPException

from app.models.project import Project
from app.repositories.project_repository import ProjectRepository


class ProjectService:

    def __init__(self, db):
        self.db = db
        self.repository = ProjectRepository(db)

    # ----------------------------------
    # Helpers
    # ----------------------------------

    def _generate_slug(self, name: str) -> str:
        """
        Convert project name into a URL-friendly slug.

        Example:
            "Nativee Production"
                ↓
            "nativee-production"
        """
        return sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

    # ----------------------------------
    # Create
    # ----------------------------------

    def create(
        self,
        user_id: int,
        name: str,
        description: str | None = None,
    ) -> Project:

        slug = self._generate_slug(name)

        existing = self.repository.get_by_slug(slug)

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Project already exists",
            )

        project = Project(
            owner_id=user_id,
            name=name,
            slug=slug,
            description=description,
        )

        return self.repository.create(project)

    # ----------------------------------
    # Read
    # ----------------------------------

    def get(
        self,
        user_id: int,
        project_id: int,
    ) -> Project:

        project = self.repository.get_owned(
            user_id=user_id,
            project_id=project_id,
        )

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )

        return project

    def get_all(
        self,
        user_id: int,
    ) -> list[Project]:
        return self.repository.get_by_user(user_id)

    # ----------------------------------
    # Update
    # ----------------------------------

    def update(
        self,
        user_id: int,
        project_id: int,
        name: str,
        description: str | None = None,
    ) -> Project:

        project = self.get(
            user_id=user_id,
            project_id=project_id,
        )

        new_slug = self._generate_slug(name)

        existing = self.repository.get_by_slug(new_slug)

        if existing and existing.id != project.id:
            raise HTTPException(
                status_code=409,
                detail="Project already exists",
            )

        project.name = name
        project.slug = new_slug
        project.description = description

        return self.repository.update(project)

    # ----------------------------------
    # Delete
    # ----------------------------------

    def delete(
        self,
        user_id: int,
        project_id: int,
    ):

        project = self.get(
            user_id=user_id,
            project_id=project_id,
        )

        self.repository.delete(project)

        return {
            "success": True,
            "message": "Project deleted",
        }
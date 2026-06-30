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

    def _generate_slug(
        self,
        name: str,
    ) -> str:
        """
        Convert project name into URL-friendly slug.

        Example:
            "Nativee Production"
                ↓
            "nativee-production"
        """

        slug = (
            sub(r"[^a-z0-9]+", "-", name.lower())
            .strip("-")
        )

        return slug

    # ----------------------------------
    # Create
    # ----------------------------------

    def create(
        self,
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
        project_id: int,
    ) -> Project:

        project = self.repository.get(project_id)

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )

        return project

    def get_all(self):
        return self.repository.get_all()

    # ----------------------------------
    # Update
    # ----------------------------------

    def update(
        self,
        project_id: int,
        name: str,
        description: str | None = None,
    ) -> Project:

        project = self.get(project_id)

        project.name = name
        project.slug = self._generate_slug(name)
        project.description = description

        return self.repository.update(project)

    # ----------------------------------
    # Delete
    # ----------------------------------

    def delete(
        self,
        project_id: int,
    ):

        project = self.get(project_id)

        self.repository.delete(project)

        return {
            "success": True,
            "message": "Project deleted",
        }
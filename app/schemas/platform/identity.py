from pydantic import BaseModel


# ==========================================================
# Project
# ==========================================================

class ProjectInfo(BaseModel):
    id: int
    name: str


# ==========================================================
# API Key
# ==========================================================

class APIKeyInfo(BaseModel):
    id: int
    name: str


# ==========================================================
# Plan
# ==========================================================

class PlanInfo(BaseModel):
    id: int
    name: str
    requests_per_minute: int
    requests_per_month: int


# ==========================================================
# Authenticated Identity (/me)
# ==========================================================

class MeResponse(BaseModel):
    project: ProjectInfo
    api_key: APIKeyInfo
    plan: PlanInfo
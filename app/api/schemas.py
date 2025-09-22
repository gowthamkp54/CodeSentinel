from pydantic import BaseModel, HttpUrl


class RepositoryRequest(BaseModel):
    repository_url: HttpUrl


class AnalysisResponse(BaseModel):
    repository_url: str
    total_files: int
    python_files: int
    findings: list[dict]
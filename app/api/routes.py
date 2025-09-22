from fastapi import APIRouter, HTTPException

from app.api.schemas import RepositoryRequest
from app.github.repository import (
    cleanup_repository,
    clone_repository,
)
from app.analyzers.repository_analyzer import (
    RepositoryAnalyzer,
)


router = APIRouter()

analyzer = RepositoryAnalyzer()


@router.post("/analyze")
def analyze_repository(
    request: RepositoryRequest,
):

    repository_path = None

    try:

        repository_url = str(
            request.repository_url
        )

        repository_path = clone_repository(
            repository_url
        )

        result = analyzer.analyze(
            repository_path
        )

        return {
            "repository_url": repository_url,
            **result,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    finally:

        if repository_path:
            cleanup_repository(
                repository_path
            )
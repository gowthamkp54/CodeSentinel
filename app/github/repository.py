import shutil
import tempfile
from pathlib import Path

from git import Repo


def clone_repository(repository_url: str) -> Path:
    temp_dir = Path(
        tempfile.mkdtemp(prefix="codesentinel_")
    )

    try:
        Repo.clone_from(repository_url, temp_dir)
        return temp_dir

    except Exception as exc:
        shutil.rmtree(temp_dir, ignore_errors=True)

        raise RuntimeError(
            f"Failed to clone repository: {exc}"
        ) from exc


def cleanup_repository(repository_path: Path) -> None:
    shutil.rmtree(
        repository_path,
        ignore_errors=True,
    )
from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "build",
    "dist",
}


def should_ignore(path: Path) -> bool:
    return any(
        part in IGNORED_DIRECTORIES
        for part in path.parts
    )


def find_source_files(
    repository_path: Path,
) -> list[Path]:

    source_files = []

    for path in repository_path.rglob("*"):

        if not path.is_file():
            continue

        if should_ignore(path):
            continue

        source_files.append(path)

    return source_files


def find_python_files(
    repository_path: Path,
) -> list[Path]:

    return [
        path
        for path in repository_path.rglob("*.py")
        if path.is_file()
        and not should_ignore(path)
    ]
from pathlib import Path

from app.analyzers.ast_analyzer import ASTAnalyzer
from app.utils.file_utils import (
    find_python_files,
    find_source_files,
)


class RepositoryAnalyzer:

    def __init__(self):
        self.ast_analyzer = ASTAnalyzer()

    def analyze(
        self,
        repository_path: Path,
    ) -> dict:

        all_files = find_source_files(
            repository_path
        )

        python_files = find_python_files(
            repository_path
        )

        findings = []

        for file_path in python_files:

            file_findings = (
                self.ast_analyzer.analyze_file(
                    file_path
                )
            )

            findings.extend(file_findings)

        return {
            "total_files": len(all_files),
            "python_files": len(python_files),
            "findings": findings,
        }
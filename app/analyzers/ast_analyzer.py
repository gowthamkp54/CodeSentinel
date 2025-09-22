import ast
from pathlib import Path


class ASTAnalyzer:

    def analyze_file(
        self,
        file_path: Path,
    ) -> list[dict]:

        findings = []

        try:
            source_code = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            tree = ast.parse(source_code)

        except SyntaxError as exc:
            return [
                {
                    "type": "syntax_error",
                    "severity": "high",
                    "file": str(file_path),
                    "line": exc.lineno,
                    "message": str(exc),
                }
            ]

        # Analyze all AST nodes
        for node in ast.walk(tree):

            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):
                findings.extend(
                    self._analyze_function(
                        node,
                        file_path,
                    )
                )

            # Detect bare except
            if isinstance(node, ast.ExceptHandler):

                if node.type is None:
                    findings.append(
                        {
                            "type": "bare_except",
                            "severity": "medium",
                            "file": str(file_path),
                            "line": node.lineno,
                            "message": (
                                "Bare except detected. "
                                "Catch specific exceptions instead."
                            ),
                        }
                    )

            # Detect eval() and exec()
            if isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):

                    if node.func.id in {
                        "eval",
                        "exec",
                    }:
                        findings.append(
                            {
                                "type": "dangerous_function",
                                "severity": "high",
                                "file": str(file_path),
                                "line": node.lineno,
                                "function": node.func.id,
                                "message": (
                                    f"Use of '{node.func.id}()' "
                                    "may introduce security risks."
                                ),
                            }
                        )

        return findings

    def _analyze_function(
        self,
        node,
        file_path: Path,
    ) -> list[dict]:

        findings = []

        # -----------------------------------
        # Large function
        # -----------------------------------

        end_line = getattr(
            node,
            "end_lineno",
            node.lineno,
        )

        function_length = (
            end_line - node.lineno + 1
        )

        if function_length > 50:

            findings.append(
                {
                    "type": "large_function",
                    "severity": "medium",
                    "file": str(file_path),
                    "line": node.lineno,
                    "function": node.name,
                    "message": (
                        f"Function '{node.name}' "
                        f"is {function_length} lines long."
                    ),
                }
            )

        # -----------------------------------
        # Too many arguments
        # -----------------------------------

        argument_count = (
            len(node.args.args)
            + len(node.args.kwonlyargs)
        )

        if argument_count > 6:

            findings.append(
                {
                    "type": "too_many_arguments",
                    "severity": "low",
                    "file": str(file_path),
                    "line": node.lineno,
                    "function": node.name,
                    "message": (
                        f"Function '{node.name}' has "
                        f"{argument_count} arguments."
                    ),
                }
            )

        # -----------------------------------
        # Mutable default arguments
        # -----------------------------------

        for default in (
            list(node.args.defaults)
            + list(node.args.kw_defaults)
        ):

            if isinstance(
                default,
                (ast.List, ast.Dict, ast.Set),
            ):

                findings.append(
                    {
                        "type": "mutable_default_argument",
                        "severity": "medium",
                        "file": str(file_path),
                        "line": node.lineno,
                        "function": node.name,
                        "message": (
                            f"Function '{node.name}' uses "
                            "a mutable default argument."
                        ),
                    }
                )

        # -----------------------------------
        # Branch complexity
        # -----------------------------------

        branch_count = 0

        for child in ast.walk(node):

            if isinstance(
                child,
                (
                    ast.If,
                    ast.For,
                    ast.While,
                    ast.Try,
                    ast.Match,
                ),
            ):
                branch_count += 1

        if branch_count > 10:

            findings.append(
                {
                    "type": "high_branch_complexity",
                    "severity": "medium",
                    "file": str(file_path),
                    "line": node.lineno,
                    "function": node.name,
                    "message": (
                        f"Function '{node.name}' contains "
                        f"{branch_count} control-flow branches."
                    ),
                }
            )

        # -----------------------------------
        # Deep nesting
        # -----------------------------------

        nesting_depth = self._calculate_nesting(
            node,
        )

        if nesting_depth > 4:

            findings.append(
                {
                    "type": "deep_nesting",
                    "severity": "medium",
                    "file": str(file_path),
                    "line": node.lineno,
                    "function": node.name,
                    "message": (
                        f"Function '{node.name}' has "
                        f"nesting depth {nesting_depth}."
                    ),
                }
            )

        return findings

    def _calculate_nesting(
        self,
        node,
        current_depth=0,
    ) -> int:

        max_depth = current_depth

        nesting_nodes = (
            ast.If,
            ast.For,
            ast.While,
            ast.Try,
            ast.With,
        )

        for child in ast.iter_child_nodes(node):

            if isinstance(
                child,
                nesting_nodes,
            ):

                depth = self._calculate_nesting(
                    child,
                    current_depth + 1,
                )

            else:

                depth = self._calculate_nesting(
                    child,
                    current_depth,
                )

            max_depth = max(
                max_depth,
                depth,
            )

        return max_depth
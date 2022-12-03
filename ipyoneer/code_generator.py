import ast


def generate_code(statements: ast.Module) -> ast.Module:
    """Code generation for time profiling

    Parameters
    ----------
    statements : ast.Module


    Returns
    -------
    ast.Module
        _description_
    """
    new_body = [
        ast.parse(
            "import ipyoneer\n" + "__ipyoneer_timer_manager = ipyoneer.TimerManager()",
            mode="exec",
        ).body[0],
    ]
    for line in statements.body:
        new_body.append(_parse_code(line))


_measuring_statements = [
    ast.Return,
    ast.Delete,
    ast.Assign,
    ast.AnnAssign,
    ast.AugAssign,
    ast.Expr,
]

_digging_statements = [
    # ast.FunctionDef,
    # ast.AsyncFunctionDef,
    # ast.ClassDef,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.If,
    ast.With,
    ast.AsyncWith,
    ast.Match,
    ast.Raise,
    ast.Try,
    ast.TryStar,
    ast.Assert,
    ast.Import,
    ast.ImportFrom,
    # ast.Global,
    # ast.Nonlocal,
    # ast.Pass,
    # ast.Break,
    # ast.Continue,
]


def _parse_code(line: ast.stmt, indent: int = 0) -> ast.stmt:
    """Parse a single statement

    Parameters
    ----------
    statement : ast.stmt
        Statement
    indent : int
        indentation level

    Returns
    -------
    ast.stmt
        parsed result"""
    if issubclass(type(line), _measuring_statements):
        return ast.With(
            items=[
                ast.parse(
                    f"ipyoneer.Timer(__ipyoneer_timer_manager, {0}, {1}, '{2}')".format(
                        line.lineno, indent, ast.dump(line)
                    ),
                    mode="exec",
                ).body[0]
            ],
            body=[line],
        )
    elif not isinstance(line, _digging_statements):
        return ast.With(
            items=[
                ast.parse(
                    f"ipyoneer.Timer(__ipyoneer_timer_manager, {0}, {1}, '{2}')".format(
                        line.lineno, indent, ast.dump(line)
                    ),
                    mode="exec",
                ).body[0]
            ],
            body=[line],
        )
    else:
        return line

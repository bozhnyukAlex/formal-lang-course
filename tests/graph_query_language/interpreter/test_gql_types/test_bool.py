import sys

import pytest

from project.graph_query_language.interpreter.gql_exceptions import (
    NotImplementedException,
)
from project.graph_query_language.interpreter.gql_types.bool import Bool

if sys.platform.startswith("win"):
    pytest.skip("Skip bool tests", allow_module_level=True)
else:
    from tests.graph_query_language.interpreter.interpreter import (
        interpreter_with_value,
    )


@pytest.mark.parametrize(
    "bool_expr, expected",
    [
        ("TRUE & FALSE", False),
        ("TRUE & TRUE", True),
        ("FALSE & TRUE", False),
        ("FALSE & FALSE", False),
    ],
)
def test_bool_intersect(bool_expr, expected):
    assert interpreter_with_value(bool_expr, "expr") == Bool(expected)


@pytest.mark.parametrize(
    "bool_expr, expected",
    [
        ("TRUE | FALSE", True),
        ("TRUE | TRUE", True),
        ("FALSE | TRUE", True),
        ("FALSE | FALSE", False),
    ],
)
def test_bool_union(bool_expr, expected):
    assert interpreter_with_value(bool_expr, "expr") == Bool(expected)


@pytest.mark.parametrize(
    "bool_expr, expected",
    [
        ("NOT TRUE", False),
        ("NOT FALSE", True),
    ],
)
def test_bool_inverse(bool_expr, expected):
    assert interpreter_with_value(bool_expr, "expr") == Bool(expected)


@pytest.mark.parametrize(
    "bool_expr",
    [
        "TRUE . TRUE",
        "TRUE . FALSE",
        "FALSE . TRUE",
        "FALSE . FALSE",
        "TRUE *",
    ],
)
def test_bool_unsupported(bool_expr):
    with pytest.raises(NotImplementedException):
        interpreter_with_value(bool_expr, "expr")

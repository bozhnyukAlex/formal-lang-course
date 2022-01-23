import pytest

from interpreter import interpreter_with_value
from project.graph_query_language.interpreter.gql_types.bool import Bool


@pytest.mark.parametrize(
    "initial_set, fun, expected_set",
    [
        ("{1, 2, 3, 4, 5}", "LAMBDA x: x IN {2..4}", "{2, 3, 4}"),
        ("{1, 2, 3, 4, 5}", "LAMBDA _: TRUE", "{1, 2, 3, 4, 5}"),
        ("{1, 2, 3, 4, 5}", "LAMBDA _: FALSE", "{}"),
    ],
)
def test_filter(initial_set, fun, expected_set):
    expression = f"FILTER ({fun}) {initial_set}"
    actual = interpreter_with_value(expression, "filtering")
    expected = interpreter_with_value(expected_set, "vertices")
    assert actual.data == expected.data


@pytest.mark.parametrize(
    "initial_set, fun, expected_set",
    [
        ("{1, 2}", "LAMBDA x: x IN {2}", {Bool(True), Bool(False)}),
        ("{1, 2, 3}", "LAMBDA x: 5", {5}),
        ("{1, 2, 3}", "LAMBDA _: 1", {1}),
    ],
)
def test_map(initial_set, fun, expected_set):
    expression = f"MAP ({fun}) {initial_set}"
    actual = interpreter_with_value(expression, "mapping")
    assert actual.data == expected_set

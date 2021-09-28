from itertools import product

import pytest
from pyformlang.regular_expression import PythonRegex

from project import generate_two_cycles_graph, rpq


@pytest.fixture
def default_graph():
    return generate_two_cycles_graph(3, 2, ("a", "b"))


@pytest.fixture
def nodes_rpq():
    res = set(product(range(4), range(4)))
    return res.union({(0, 4), (4, 5), (5, 0)})


def test_all_nodes_start_and_final(default_graph, nodes_rpq):
    actual_rpq = rpq(default_graph, PythonRegex("a*|b"))

    assert actual_rpq == nodes_rpq


@pytest.mark.parametrize(
    "pattern,start_nodes,final_nodes,expected_rpq",
    [
        ("a*|b", {0}, {1, 2, 3, 4}, {(0, 1), (0, 2), (0, 3), (0, 4)}),
        ("a*|b", {4}, {4, 5}, {(4, 5)}),
        ("aa", {0, 1, 2, 3}, {0, 1, 2, 3}, {(0, 2), (1, 3), (2, 0), (3, 1)}),
        ("b", {0}, {0, 1, 2, 3}, set()),
        ("b*", {0}, {5, 4}, {(0, 5), (0, 4)}),
    ],
)
def test_query(default_graph, pattern, start_nodes, final_nodes, expected_rpq):
    regex = PythonRegex(pattern)
    actual_rpq = rpq(default_graph, regex, start_nodes, final_nodes)

    assert actual_rpq == expected_rpq

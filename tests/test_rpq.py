import networkx as nx
import pytest
from itertools import product
from pyformlang.regular_expression import PythonRegex, Regex

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


@pytest.fixture
def empty_graph():
    return nx.empty_graph(create_using=nx.MultiDiGraph)


@pytest.fixture
def acyclic_graph():
    graph = nx.MultiDiGraph()
    graph.add_edges_from(
        [(0, 1, {"label": "x"}), (1, 2, {"label": "y"}), (2, 3, {"label": "y"})]
    )
    return graph


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


def test_empty_graph_rpq(empty_graph):
    actual_rpq = rpq(empty_graph, PythonRegex("x*|y"))
    assert actual_rpq == set()


def test_all_different_labels_query(default_graph):
    actual_rpq = rpq(default_graph, PythonRegex("z*|g"))
    assert actual_rpq == set()


def test_acyclic_graph_rpq(acyclic_graph):
    actual_rpq = rpq(acyclic_graph, Regex("x y y"))
    assert actual_rpq == {(0, 3)}


def test_some_different_labels_query(default_graph):
    actual_rpq = rpq(default_graph, Regex("a*|z"))
    expected_rpq = set((i, j) for i in range(4) for j in range(4))
    assert actual_rpq == expected_rpq


def test_empty_graph_empty_query(empty_graph):
    actual_rpq = rpq(empty_graph, PythonRegex(""))
    assert actual_rpq == set()

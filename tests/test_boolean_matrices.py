import pytest
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    State,
)

from project import BooleanMatrices


@pytest.fixture
def default_fa():
    fa = NondeterministicFiniteAutomaton()
    fa.add_transitions(
        [
            (0, "a", 1),
            (0, "a", 2),
            (2, "d", 3),
            (1, "c", 1),
            (1, "b", 2),
            (3, "d", 0),
        ]
    )

    return fa


def test_labels(default_fa):
    bm = BooleanMatrices.from_automaton(default_fa)
    actual_labels = bm.bool_matrices.keys()
    expected_labels = default_fa.symbols

    assert actual_labels == expected_labels


@pytest.mark.parametrize(
    "label, expected_nnz", [("a", 2), ("b", 1), ("c", 1), ("d", 2)]
)
def test_nonzero(default_fa, label, expected_nnz):
    bm = BooleanMatrices.from_automaton(default_fa)
    actual_nnz = bm.bool_matrices[label].nnz

    assert actual_nnz == expected_nnz


@pytest.mark.parametrize(
    "label,edges",
    [
        ("a", [(0, 1), (0, 2)]),
        ("b", [(1, 2)]),
        ("c", [(1, 1)]),
        ("d", [(2, 3), (3, 0)]),
    ],
)
def test_adjacency(default_fa, label, edges):
    bm = BooleanMatrices.from_automaton(default_fa)
    assert all(bm.bool_matrices[label][edge] for edge in edges)


def test_transitive_closure(default_fa):
    bm = BooleanMatrices.from_automaton(default_fa)
    tc = bm.transitive_closure()
    assert tc.sum() == tc.size


def test_intersection():
    fa1 = NondeterministicFiniteAutomaton()
    fa1.add_transitions(
        [(0, "a", 1), (0, "c", 1), (0, "c", 0), (1, "b", 1), (1, "c", 2), (2, "d", 0)]
    )
    fa1.add_start_state(State(0))
    fa1.add_final_state(State(0))
    fa1.add_final_state(State(1))
    fa1.add_final_state(State(2))

    bm1 = BooleanMatrices.from_automaton(fa1)

    fa2 = NondeterministicFiniteAutomaton()
    fa2.add_transitions([(0, "a", 1), (0, "a", 0), (1, "b", 1), (1, "e", 2)])
    fa2.add_start_state(State(0))
    fa2.add_final_state(State(1))

    bm2 = BooleanMatrices.from_automaton(fa2)

    expected_fa = DeterministicFiniteAutomaton()
    expected_fa.add_transitions([(0, "a", 1), (1, "b", 1)])
    expected_fa.add_start_state(State(0))
    expected_fa.add_final_state(State(1))

    actual_fa = bm1.intersect(bm2).to_automaton()

    assert actual_fa.is_equivalent_to(expected_fa)

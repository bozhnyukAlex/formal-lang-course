from typing import Iterable, List

import pytest
from pyformlang.regular_expression import MisformedRegexError

from project.regex import regex_to_min_dfa
from pyformlang.finite_automaton import Symbol, DeterministicFiniteAutomaton, State


def test_regex_to_dfa_deterministic():
    regex1 = "11(10)*"
    dfa = regex_to_min_dfa(regex1)
    assert dfa.is_deterministic()


@pytest.mark.parametrize(
    "regex, expected_words, unexpected_words",
    [
        ("", [], [[Symbol("*")], [Symbol("a"), Symbol("a")]]),
        (
            "1 0 (1 0)*",
            [
                [Symbol("1"), Symbol("0")],
                [Symbol("1"), Symbol("0"), Symbol("1"), Symbol("0")],
                [
                    Symbol("1"),
                    Symbol("0"),
                    Symbol("1"),
                    Symbol("0"),
                    Symbol("1"),
                    Symbol("0"),
                ],
            ],
            [[], [Symbol("1")], [Symbol("0")], [Symbol("1"), Symbol("0"), Symbol("1")]],
        ),
        (
            "a* b c | d*",
            [
                [],
                [Symbol("d")],
                [Symbol("d"), Symbol("d"), Symbol("d"), Symbol("d")],
                [Symbol("b"), Symbol("c")],
                [Symbol("a"), Symbol("a"), Symbol("b"), Symbol("c")],
                [Symbol("a"), Symbol("b"), Symbol("c")],
            ],
            [[Symbol("g")], [Symbol("b"), Symbol("c"), Symbol("d")], [Symbol("a")]],
        ),
    ],
)
def test_regex_to_dfa_accept(
    regex: str,
    expected_words: List[Iterable[Symbol]],
    unexpected_words: List[Iterable[Symbol]],
):
    dfa = regex_to_min_dfa(regex)
    assert all(dfa.accepts(expected_word) for expected_word in expected_words) and all(
        (not dfa.accepts(unexpected_word)) for unexpected_word in unexpected_words
    )


def test_wrong_regex():
    with pytest.raises(MisformedRegexError):
        regex_to_min_dfa("*|wrong|*")


def test_get_min_dfa() -> None:
    expected_dfa = DeterministicFiniteAutomaton()

    state_0 = State(0)
    state_1 = State(1)
    state_2 = State(2)

    symbol_a = Symbol("a")
    symbol_l = Symbol("l")
    symbol_e = Symbol("e")

    expected_dfa.add_start_state(state_0)

    expected_dfa.add_final_state(state_0)
    expected_dfa.add_final_state(state_1)
    expected_dfa.add_final_state(state_2)

    expected_dfa.add_transition(state_0, symbol_a, state_0)
    expected_dfa.add_transition(state_0, symbol_l, state_1)
    expected_dfa.add_transition(state_0, symbol_e, state_2)

    expected_dfa.add_transition(state_1, symbol_l, state_1)
    expected_dfa.add_transition(state_1, symbol_e, state_2)

    expected_dfa.add_transition(state_2, symbol_e, state_2)

    actual_dfa = regex_to_min_dfa("a* l* e*")

    assert expected_dfa.is_equivalent_to(actual_dfa) and len(actual_dfa.states) == len(
        expected_dfa.states
    )

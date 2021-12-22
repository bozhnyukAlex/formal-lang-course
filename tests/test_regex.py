from typing import Iterable, List

import pytest
from pyformlang.regular_expression import MisformedRegexError

from project.regex_utils import regex_str_to_min_dfa
from pyformlang.finite_automaton import Symbol, DeterministicFiniteAutomaton, State


def test_regex_to_dfa_deterministic():
    regex1 = "11(10)*"
    dfa = regex_str_to_min_dfa(regex1)
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
    dfa = regex_str_to_min_dfa(regex)
    assert all(dfa.accepts(expected_word) for expected_word in expected_words) and all(
        (not dfa.accepts(unexpected_word)) for unexpected_word in unexpected_words
    )


def test_wrong_regex():
    with pytest.raises(MisformedRegexError):
        regex_str_to_min_dfa("*|wrong|*")


# def test_is_minimal():
#    dfa = regex_str_to_min_dfa("1* 0 0")
#    dfa_minimal = dfa.minimize()
#
#    assert dfa.is_equivalent_to(dfa_minimal)

from project.regex import regex_to_dfa
from pyformlang.finite_automaton import Symbol


def test_regex_to_dfa_deterministic():
    regex1 = "11(10)*"
    dfa = regex_to_dfa(regex1)
    assert dfa.is_deterministic()


def test_regex_to_dfa_accept():
    regex1 = "a* b c | d*"
    test_words = [
        [],
        [Symbol("d")],
        [Symbol("d"), Symbol("d"), Symbol("d"), Symbol("d")],
        [Symbol("b"), Symbol("c")],
        [Symbol("a"), Symbol("a"), Symbol("b"), Symbol("c")],
        [Symbol("a"), Symbol("b"), Symbol("c")],
    ]
    dfa = regex_to_dfa(regex1)
    assert all(dfa.accepts(word) for word in test_words)

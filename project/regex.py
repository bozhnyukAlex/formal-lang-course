from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex


def regex_to_dfa(regex_str: str) -> DeterministicFiniteAutomaton:
    """
    Gets a string representation of regular expression and builds equivalent Deterministic Finite Automaton

    Parameters
    ----------
    regex_str: str
        String representation of regular expression

    Returns
    -------
    DeterministicFiniteAutomaton
        Deterministic Finite Automaton, which is equivalent to given regular expression
    """
    regex = Regex(regex_str)
    enfa = regex.to_epsilon_nfa()
    dfa = enfa.to_deterministic()
    return dfa

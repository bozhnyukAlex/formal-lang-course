from typing import Iterable

from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

__all__ = ["RSM", "minimize_rsm", "Box"]


class Box:
    """
    This class represents a box for recursive state machine

    Parameters
    ----------
    variable : Variable
       variable of RSM
    dfa : DeterministicFiniteAutomaton
        Deterministic Finite Automaton for variable
    """

    def __init__(
        self, variable: Variable = None, dfa: DeterministicFiniteAutomaton = None
    ):
        self._dfa = dfa
        self._variable = variable

    def __eq__(self, other: "Box"):
        return self._variable == other._variable and self._dfa.is_equivalent_to(
            other._dfa
        )

    def minimize(self):
        """
        Minimize dfa in Box

        Returns
        -------
            None
        """
        self._dfa = self._dfa.minimize()

    @property
    def dfa(self):
        return self._dfa

    @property
    def variable(self):
        return self._variable


class RSM:
    """
    This class represents a recursive state machine (RSM).

    Parameters
    ----------
    start_symbol : Variable
        A start symbol for automaton
    boxes : Iterable[Box]
        A finite collection of boxes
    """

    def __init__(
        self,
        start_symbol: Variable,
        boxes: Iterable[Box],
    ):
        self._start_symbol = start_symbol
        self._boxes = boxes

    @property
    def boxes(self):
        return self._boxes

    @property
    def start_symbol(self):
        return self._start_symbol

    def set_start_symbol(self, start_symbol: Variable):
        self._start_symbol = start_symbol

    def minimize(self):
        for box in self._boxes:
            box.minimize()
        return self


def minimize_rsm(rsm: RSM) -> RSM:
    """
    Function to minimize given RSM

    Parameters
    ----------
        rsm: RSM
            RSM to minimize

    Returns
    -------
        RSM:
            Minimized RSM
    """
    return rsm.minimize()

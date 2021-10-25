from typing import AbstractSet, Iterable

from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

__all__ = ["ECFG", "InvalidECFGFormatException", "ECFGProduction"]

from project import RSM, Box, regex_to_min_dfa


class ECFGProduction:
    """
    This class represents a production of a ECFG

    Attributes
    ----------
    head: Variable
        head of production
    body: Regex
        body of production represented by regex
    """

    def __init__(self, head: Variable, body: Regex):
        self._head = head
        self._body = body

    def __str__(self):
        return str(self.head) + " -> " + str(self.body)

    @property
    def head(self) -> Variable:
        return self._head

    @property
    def body(self) -> Regex:
        return self._body


class InvalidECFGFormatException(Exception):
    pass


class ECFG:
    """
    This class represents a Extended CFG.
    Extended CFG:
        - There is exactly one rule for each non-terminal.
        - One line contains exactly one rule.
        - Rule is non-terminal and regex over terminals and non-terminals accepted by pyformlang, separated by '->'.
          For example: S -> a | b * S

    Attributes
    ----------
    variables: AbstractSet[Variable]
        Set of variables of ECFG
    start_symbol: Variable
        Start symbol of ECFG
    productions: Iterable[ECFGProduction]
        Collection containing productions of ECFG
    """

    def __init__(
        self,
        variables: AbstractSet[Variable] = None,
        start_symbol: Variable = None,
        productions: Iterable[ECFGProduction] = None,
    ):
        self._variables = variables or set()
        self._start_symbol = start_symbol
        self._productions = productions or set()

    @property
    def variables(self) -> AbstractSet[Variable]:
        return self._variables

    @property
    def productions(self) -> AbstractSet[ECFGProduction]:
        return self._productions

    @property
    def start_symbol(self) -> Variable:
        return self._start_symbol

    def to_text(self) -> str:
        """
        Get a string representation of CFG

        Returns
        -------
        str:
            String representation
        """
        return "\n".join(str(p) for p in self.productions)

    @classmethod
    def from_text(cls, text, start_symbol=Variable("S")) -> "ECFG":
        """
        Read an ECFG from text

        Parameters
        ----------
        text: str
            Input text
        start_symbol: Variable
            Start symbol of ECFG

        Raises
        ------
        InvalidECFGFormatException:
            If there is a problem with ECFG format in text
        """
        variables = set()
        productions = set()
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            production_objects = line.split("->")
            if len(production_objects) != 2:
                raise InvalidECFGFormatException(
                    "There should only be one production per line."
                )

            head_text, body_text = production_objects
            head = Variable(head_text.strip())

            if head in variables:
                raise InvalidECFGFormatException(
                    "There should only be one production for each variable."
                )

            variables.add(head)
            body = Regex(body_text.strip())
            productions.add(ECFGProduction(head, body))

        return ECFG(
            variables=variables, start_symbol=start_symbol, productions=productions
        )

    @classmethod
    def from_file(cls, path: str, start_symbol: str = "S") -> "ECFG":
        """
        Read an ECFG from file

        Parameters
        ----------
        path: str
            Path to file containing ECFG
        start_symbol: Variable
            Start symbol of ECFG

        Raises
        ------
        InvalidECFGFormatException:
            If there is a problem with ECFG format in file text
        """

        with open(path) as f:
            return ECFG.from_text(f.read(), start_symbol=Variable(start_symbol))


def ecfg_to_rsm(ecfg: ECFG) -> RSM:
    """
    Converts an ECFG to a Recursive State Machine

    Parameters
    ----------
    ecfg: ECFG
        Input Extended CFG to convert

    Returns
    -------
    RSM:
        Recursive state machine from ECFG.
    """
    boxes = [Box(p.head, regex_to_min_dfa(p.body)) for p in ecfg.productions]
    return RSM(start_symbol=ecfg.start_symbol, boxes=boxes)

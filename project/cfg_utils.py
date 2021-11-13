import os
from typing import AbstractSet

from pyformlang.cfg import CFG, Variable, Production, Epsilon

__all__ = [
    "get_cnf_from_file",
    "get_cnf_from_text",
    "get_wcnf_from_file",
    "get_wcnf_from_text",
    "is_wcnf",
    "get_original_cfg_from_file",
    "cfg_to_ecfg",
    "cfg_to_wcnf",
]

from pyformlang.regular_expression import Regex

from project.ecfg_utils import ECFGProduction, ECFG


def get_cnf_from_file(path: str, start_symbol: str = None) -> CFG:
    """
    Gets Context Free Grammar in Chomsky Normal Form (a more strict case of
    the Weak Chomsky Normal Form, which can be weakened to it through product changes)
    equivalent to file text representation of CFG.

    Parameters
    ----------
    path: str
        A path to file containing text representation of CFG with rules:
        The structure of a production is: head -> body_1 | body_2 | … | body_n
        A variable (or non terminal) begins by a capital letter
        A terminal begins by a non-capital character
        Terminals and Variables are separated by spaces
        An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є
    start_symbol: str, default = None
        An axiom for CFG
        If not specified, 'S' will be used

    Returns
    -------
    CNF:
        Context Free Grammar in Chomsky Normal Form equivalent to
        file text representation of CFG
    Raises
    ------
    OSError:
        If there was an error while working with file
    ValueError:
        If file text is not satisfied to the rules
    """

    __check_path(path)

    with open(path, "r") as file:
        cfg_str = file.read()

    return get_cnf_from_text(cfg_str, start_symbol)


def get_wcnf_from_file(path: str, start_symbol: str = None) -> CFG:
    """
    Gets Context Free Grammar in Weak Chomsky Normal Form
    equivalent to file text representation of CFG.

    Parameters
    ----------
    path: str
        A path to file containing text representation of CFG with rules:
        The structure of a production is: head -> body_1 | body_2 | … | body_n
        A variable (or non terminal) begins by a capital letter
        A terminal begins by a non-capital character
        Terminals and Variables are separated by spaces
        An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є
    start_symbol: str, default = None
        An axiom for CFG
        If not specified, 'S' will be used

    Returns
    -------
    CNF:
        Context Free Grammar in Chomsky Normal Form equivalent to
        file text representation of CFG
    Raises
    ------
    OSError:
        If there was an error while working with file
    ValueError:
        If file text is not satisfied to the rules
    """

    __check_path(path)

    with open(path, "r") as file:
        cfg_str = file.read()

    return get_wcnf_from_text(cfg_str, start_symbol)


def get_original_cfg_from_file(path: str, start_symbol: str = None) -> CFG:
    """
    Gets Context Free Grammar equivalent to file text representation of CFG.

    Parameters
    ----------
    path: str
        A path to file containing text representation of CFG with rules:
        The structure of a production is: head -> body_1 | body_2 | … | body_n
        A variable (or non terminal) begins by a capital letter
        A terminal begins by a non-capital character
        Terminals and Variables are separated by spaces
        An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є
    start_symbol: str, default = None
        An axiom for CFG
        If not specified, 'S' will be used

    Returns
    -------
    CNF:
        Context Free Grammar in Chomsky Normal Form equivalent to
        file text representation of CFG
    Raises
    ------
    OSError:
        If there was an error while working with file
    ValueError:
        If file text is not satisfied to the rules
    """

    if start_symbol is None:
        start_symbol = "S"

    __check_path(path)

    with open(path, "r") as file:
        cfg_str = file.read()
    cfg = CFG.from_text(cfg_str, Variable(start_symbol))
    return cfg


def __check_path(path: str) -> None:
    """
    Checks whether path is representing a non-empty file with txt extension.

    Parameters
    ----------
    path: str
        A path to file containing text representation of CFG

    Raises
    ------
    OSError:
        If file does not exist or its extension is not txt or it is empty.
    """
    if not os.path.exists(path):
        raise OSError("Wrong file path specified: file is not exists")
    if not path.endswith(".txt"):
        raise OSError("Wrong file path specified: *.txt is required")
    if os.path.getsize(path) == 0:
        raise OSError("Wrong file path specified: file is empty")


def get_cnf_from_text(cfg_text: str, start_symbol: str = None) -> CFG:
    """
    Get context Free Grammar in Chomsky Normal Form (more strict case of
    the Weak Chomsky Normal Form, which can be weakened to it through product changes)
    equivalent to file text representation of CFG.

    Parameters
    ----------
    cfg_text: str
        Text representation of CFG with rules:
        The structure of a production is: head -> body1 | body2 | … | bodyn
        A variable (or non terminal) begins by a capital letter
        A terminal begins by a non-capital character
        Terminals and Variables are separated by spaces
        An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є
    start_symbol: str, default = None
        An axiom for CFG
        If not specified, 'S' will be used
    Returns
    -------
    CNF:
        Context Free Grammar in Chomsky Normal Form equivalent to
        file text representation of CFG
    Raises
    ------
    ValueError:
        If file text is not satisfied to the rules
    """

    if start_symbol is None:
        start_symbol = "S"

    cfg = CFG.from_text(cfg_text, Variable(start_symbol))
    cnf = cfg.to_normal_form()

    return cnf


def get_wcnf_from_text(cfg_text: str, start_symbol: str = None) -> CFG:
    """
    Get context Free Grammar in Weak Chomsky Normal Form
    equivalent to file text representation of CFG.

    Parameters
    ----------
    cfg_text: str
        Text representation of CFG with rules:
        The structure of a production is: head -> body1 | body2 | … | bodyn
        A variable (or non terminal) begins by a capital letter
        A terminal begins by a non-capital character
        Terminals and Variables are separated by spaces
        An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є
    start_symbol: str, default = None
        An axiom for CFG
        If not specified, 'S' will be used
    Returns
    -------
    CNF:
        Context Free Grammar in Chomsky Normal Form equivalent to
        file text representation of CFG
    Raises
    ------
    ValueError:
        If file text is not satisfied to the rules
    """

    if start_symbol is None:
        start_symbol = "S"

    cfg = CFG.from_text(cfg_text, Variable(start_symbol))

    wcnf = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )

    new_productions = wcnf._get_productions_with_only_single_terminals()
    new_productions = wcnf._decompose_productions(new_productions)

    return CFG(start_symbol=wcnf.start_symbol, productions=set(new_productions))


def __check_epsilons(
    reachable_symbols: AbstractSet[Variable],
    productions_old: AbstractSet[Production],
    productions_nf: AbstractSet[Production],
):
    """
    Test whether all epsilons in reachable variables from initial grammar are present in given normal form

    Parameters
    ----------
    reachable_symbols: AbstractSet[Variable]
        Set of variables in cfg_nf
    productions_old: AbstractSet[Production]
        Old set of productions
    productions_nf: AbstractSet[Production]

    Returns
    -------
    bool:
        true if all epsilons in reachable variables from initial grammar are present in given normal form
        false otherwise
    """
    productions_old_with_epsilon = set(
        filter(
            lambda prod: prod.head in reachable_symbols and not prod.body,
            productions_old,
        )
    )
    productions_nf_with_epsilon = set(
        filter(lambda prod: not prod.body, productions_nf)
    )
    for production in productions_old_with_epsilon:
        if production not in productions_nf_with_epsilon:
            return False
    return True


def is_wcnf(cfg: CFG) -> bool:
    """
    Test whether given cfg is in Minimal Weakened Chomsky Normal Form
    The rules are:
    (1) A -> BC, where A, B, C in Variables
    (2) A -> a, where A in Variables, a in Terminals
    (3) A -> epsilon, where A in Variables
    It is also checked whether every reachable epsilon production from original grammar is present in WNCF

    Parameters
    ----------
    cfg:
        CFG to be checked

    Returns
    -------
    bool:
        true if cfg is in Minimal Weakened Chomsky Normal Form
        false otherwise
    """
    return all(p.is_normal_form() if p.body else True for p in cfg.productions)


def cfg_to_ecfg(cfg: CFG) -> ECFG:
    """
    This function converts a CFG to an Extended CFG

    Parameters
    ---------
    cfg: CFG
        CFG to convert

    Returns
    -------
    ECFG:
        Extended CFG from CFG
    """
    productions = dict()

    for p in cfg.productions:
        body = Regex(" ".join(cfg_obj.value for cfg_obj in p.body) if p.body else "$")
        if p.head not in productions:
            productions[p.head] = body
        else:
            productions[p.head] = productions.get(p.head).union(body)

    ecfg_productions = [
        ECFGProduction(head, body) for head, body in productions.items()
    ]

    return ECFG(
        variables=cfg.variables,
        start_symbol=cfg.start_symbol,
        productions=ecfg_productions,
    )


def cfg_to_wcnf(cfg: CFG) -> CFG:
    """
    Converts a CFG to the Weak Chomsky Normal Form
    The rules are:
    (1) A -> BC, where A, B, C in Variables
    (2) A -> a, where A in Variables, a in Terminals
    (3) A -> epsilon, where A in Variables
    It is also checked whether every reachable epsilon production from original grammar is present in WNCF
    Parameters
    ----------
    cfg:
        CFG to сonvert

    Returns
    -------
    CFG:
        cfg in Weak Chomsky Normal Form
    """
    cleared_cfg = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    cleared_productions = cleared_cfg._get_productions_with_only_single_terminals()
    cleared_productions = cleared_cfg._decompose_productions(cleared_productions)
    return CFG(start_symbol=cleared_cfg.start_symbol, productions=cleared_productions)

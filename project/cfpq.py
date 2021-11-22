from typing import Set, Tuple
import networkx as nx
from pyformlang.cfg import CFG, Variable
from scipy import sparse

from project import hellings, cfg_to_wcnf

__all__ = ["hellings_cfpq", "matrix_cfpq"]


def hellings_cfpq(
    graph: nx.MultiDiGraph,
    cfg: CFG,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
    start_var: Variable = Variable("S"),
) -> Set[Tuple[int, int]]:
    """
    Context-Free Path Querying based on Hellings Algorithm
    for given graph, cfg, start nodes (optional), final nodes (optional), start variable

    Parameters
    ----------
    graph: nx.MultiDiGraph
        input graph
    cfg: CFG
        input CFG
    start_nodes: Set[int]
        set of start nodes in given graph
    final_nodes: Set[int]
        set of final nodes in given graph
    start_var: Variable
        start variable in CFG

    Returns
    -------
    Set[Tuple[int, int]]:
        set of tuples (node, node) - answer to the CFPQ-problem
    """
    cfg._start_symbol = start_var
    wcnf = cfg_to_wcnf(cfg)
    reach_pairs = {
        (u, v) for u, h, v in hellings(graph, wcnf) if h == wcnf.start_symbol.value
    }
    if start_nodes:
        reach_pairs = {(u, v) for u, v in reach_pairs if u in start_nodes}
    if final_nodes:
        reach_pairs = {(u, v) for u, v in reach_pairs if v in final_nodes}

    return reach_pairs


def matrix_cfpq(
    graph: nx.MultiDiGraph,
    cfg: CFG,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
    start_var: Variable = Variable("S"),
) -> Set[Tuple[int, int]]:
    """
    Context-Free Path Querying based on matrix multiplication
    for given graph, cfg, start nodes (optional), final nodes (optional), start variable

    Parameters
    ----------
    graph: nx.MultiDiGraph
        input graph
    cfg: CFG
        input CFG
    start_nodes: Set[int]
        set of start nodes in given graph
    final_nodes: Set[int]
        set of final nodes in given graph
    start_var: Variable
        start variable in CFG

    Returns
    -------
    Set[Tuple[int, int]]:
        set of tuples (node, node) - answer to the CFPQ-problem
    """
    cfg._start_symbol = start_var
    wcnf = cfg_to_wcnf(cfg)

    eps_prod_heads = [p.head.value for p in wcnf.productions if not p.body]
    term_productions = {p for p in wcnf.productions if len(p.body) == 1}
    var_productions = {p for p in wcnf.productions if len(p.body) == 2}
    nodes_num = graph.number_of_nodes()
    matrices = {
        v.value: sparse.dok_matrix((nodes_num, nodes_num), dtype=bool)
        for v in wcnf.variables
    }

    for i, j, data in graph.edges(data=True):
        l = data["label"]
        for v in {p.head.value for p in term_productions if p.body[0].value == l}:
            matrices[v][i, j] = True

    for i in range(nodes_num):
        for v in eps_prod_heads:
            matrices[v][i, i] = True

    any_changing = True
    while any_changing:
        any_changing = False
        for p in var_productions:
            old_nnz = matrices[p.head.value].nnz
            matrices[p.head.value] += (
                matrices[p.body[0].value] @ matrices[p.body[1].value]
            )
            new_nnz = matrices[p.head.value].nnz
            any_changing = old_nnz != new_nnz

    reach_pairs = {(u, v) for u, v in zip(*matrices[wcnf.start_symbol.value].nonzero())}
    if start_nodes:
        reach_pairs = {(u, v) for u, v in reach_pairs if u in start_nodes}
    if final_nodes:
        reach_pairs = {(u, v) for u, v in reach_pairs if v in final_nodes}

    return reach_pairs

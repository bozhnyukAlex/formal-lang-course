from typing import Tuple, Set

import networkx as nx
from pyformlang.regular_expression import Regex

from project import regex_to_min_dfa, graph_to_nfa, BooleanMatrices

__all__ = ["rpq", "get_reachable"]


def get_reachable(
    bmatrix: BooleanMatrices, query_bm: BooleanMatrices = None
) -> Set[Tuple[int, int]]:
    """
    Parameters
    ----------
    bmatrix: BooleanMatrices
        Boolean matrix object
    query_bm: BooleanMatrices
        Query boolean matrix object
    Returns
    -------
        reachable: Set[Tuple[int, int]]
            All reachable nodes, according to start and final states
    """
    transitive_closure = bmatrix.transitive_closure()

    start_states = bmatrix.get_start_states()
    final_states = bmatrix.get_final_states()

    result_set = set()

    for state_from, state_to in zip(*transitive_closure.nonzero()):
        if state_from in start_states and state_to in final_states:
            result_set.add(
                (
                    state_from // query_bm.states_count
                    if query_bm is not None
                    else bmatrix.states_count,
                    state_to // query_bm.states_count
                    if query_bm is not None
                    else bmatrix.states_count,
                )
            )

    return result_set


def rpq(
    graph: nx.MultiDiGraph,
    query: Regex,
    start_nodes: set = None,
    final_nodes: set = None,
):
    """
    This function solves Regular Path Querying problem for
    giving graph, regex query with possibility of input start and final nodes

    Parameters
    ----------
    graph: nx.MultiDiGraph
        Graph for working with queries
    query: Regex
        Query represented by regex
    start_nodes:
        Set of start nodes in graph
    final_nodes:
        Set of final nodes in graph

    Returns
    -------
    set:
        Set of pairs with answer to RPG problem

    """
    graph_bm = BooleanMatrices.from_automaton(
        graph_to_nfa(graph, start_nodes, final_nodes)
    )
    query_bm = BooleanMatrices.from_automaton(regex_to_min_dfa(query))

    intersected_bm = graph_bm.intersect(query_bm)
    return get_reachable(intersected_bm, query_bm)

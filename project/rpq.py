import networkx as nx
from pyformlang.regular_expression import Regex

from project import regex_to_min_dfa, graph_to_nfa, BooleanMatrices


def rpq(
    graph: nx.MultiDiGraph,
    query: Regex,
    start_nodes: set = None,
    final_nodes: set = None,
) -> set:
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
    intersected_start_states = intersected_bm.get_start_states()
    intersected_final_states = intersected_bm.get_final_states()
    transitive_closure = intersected_bm.transitive_closure()
    res = set()

    for s_from, s_to in zip(*transitive_closure.nonzero()):
        if s_from in intersected_start_states and s_to in intersected_final_states:
            res.add((s_from // query_bm.num_states, s_to // query_bm.num_states))

    return res

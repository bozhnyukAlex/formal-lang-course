from typing import Tuple, Set

import cfpq_data
import networkx as nx

__all__ = [
    "GraphInfo",
    "graph_info",
    "generate_two_cycles_graph",
    "graph_to_nfa",
    "GraphException",
    "add_states_to_nfa",
    "replace_nfa_states",
    "get_graph",
]

from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State


class GraphException(Exception):
    """
    Exception raised for errors in working with graph.

    Attributes
    ----------
        message: str
            Explanation of the error
    """

    def __init__(self, message):
        self.message = message


class GraphInfo:
    """
    Encapsulates information about graph: number of nodes, number of edges, set of labels on edges.
    It has not any binding to defined graph, it simply holds a info.

    Attributes
    ----------
    nodes_count: int
        Number of nodes in graph
    edges_count: int
        Number of edges in graph
    labels: Set[str]
        Set of labels on edges
    """

    def __init__(self, nodes_count: int, edges_count: int, labels: Set[str]):
        self.edges_count = edges_count
        self.nodes_count = nodes_count
        self.labels = labels

    def __str__(self):
        return f"""
        Edges count: {str(self.edges_count)}
        Nodes count: {str(self.nodes_count)}
        Labels: {str(self.labels)}
    """


def get_graph(graph_name) -> MultiDiGraph:
    """
    Get graph by name

    Parameters
    ----------
    graph_name: str
        Name of graph
    Returns
    -------
    MultiDiGraph
        Result graph

    """
    if all(
        graph_name not in cfpq_data.DATASET[graph_from_ds].keys()
        for graph_from_ds in cfpq_data.DATASET.keys()
    ):
        raise Exception("Graph with this name does not found in dataset.")

    graph = cfpq_data.graph_from_dataset(graph_name, verbose=False)
    return graph


def graph_info(graph: nx.MultiDiGraph) -> GraphInfo:
    """
    Gets a info about graph encapsulated in GraphInfo object
    Parameters
    ----------
    graph: nx.MultiDiGraph
        Graph from which information is gained
    Returns
    -------
    GraphInfo
        Info about graph
    """
    return GraphInfo(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        cfpq_data.get_labels(graph, verbose=False),
    )


def generate_two_cycles_graph(
    first_cycle_nodes_num: int, second_cycle_nodes_num: int, labels: Tuple[str, str]
) -> nx.MultiDiGraph:
    """
    Generates graph with two cycles

    Parameters
    ----------
    first_cycle_nodes_num: int
        Number of nodes in the first cycle
    second_cycle_nodes_num: int
        Number of nodes in the second cycle
    labels: Tuple[str, str]
        Labels for the edges on the first and second cycle

    Returns
    -------
    nx.MultiDiGraph
        Generated graph with two cycles
    """
    graph_generated = cfpq_data.labeled_two_cycles_graph(
        first_cycle_nodes_num, second_cycle_nodes_num, edge_labels=labels, verbose=False
    )
    return graph_generated


def graph_to_nfa(
    graph: MultiDiGraph, start_states: set = None, final_states: set = None
) -> NondeterministicFiniteAutomaton:
    """
    Converts graph by name to the finite state automaton

    Parameters
    ----------
    graph: MultiDiGraph
        Graph to convert
    start_states: set
        Set of containing start nodes
    final_states: set
        Set of containing end nodes

    Returns
    -------
    EpsilonNFA:
        A epsilon nondeterministic finite automaton read from the graph

    Raises
    ------
    GraphException:
        If automata states do not match to the nodes of input graph
    """

    nfa = NondeterministicFiniteAutomaton()

    graph_nodes = graph.nodes

    for n_from, n_to in graph.edges():
        e_data = graph.get_edge_data(n_from, n_to)[0]["label"]
        nfa.add_transition(n_from, e_data, n_to)

    if start_states is None:
        start_states = set(graph_nodes)
    if final_states is None:
        final_states = set(graph_nodes)

    if not start_states.issubset(graph_nodes):
        raise GraphException(
            f"Invalid start states: {start_states.difference(set(graph_nodes))}"
        )

    if not final_states.issubset(graph_nodes):
        raise GraphException(
            f"Invalid final states: {final_states.difference(set(graph_nodes))}"
        )

    for state in start_states:
        nfa.add_start_state(State(state))
    for state in final_states:
        nfa.add_final_state(State(state))

    return nfa


def get_graph_info_util(graph_name) -> GraphInfo:
    """
    Provides and prints information about graph
    Parameters
    ----------
    graph_name: str
        Name of the graph
    Returns
    -------
    GraphInfo
        Object with information about graph
    Raises
    ------
    Exception
        If graph does not found in dataset
    """

    graph = get_graph(graph_name)

    gr_info = graph_info(graph)

    return gr_info


def replace_nfa_states(
    nfa: NondeterministicFiniteAutomaton,
    start_states: set = None,
    final_states: set = None,
) -> NondeterministicFiniteAutomaton:
    new_nfa = nfa.copy()
    new_nfa._start_states = set()
    new_nfa._final_states = set()

    if start_states:
        for state in start_states:
            new_nfa.add_start_state(state)

    if final_states:
        for state in final_states:
            new_nfa.add_final_state(state)

    return new_nfa


def add_states_to_nfa(
    nfa: NondeterministicFiniteAutomaton,
    start_states: set = None,
    final_states: set = None,
) -> NondeterministicFiniteAutomaton:
    new_nfa = nfa.copy()

    if start_states:
        for state in start_states:
            new_nfa.add_start_state(state)

    if final_states:
        for state in final_states:
            new_nfa.add_final_state(state)

    return new_nfa

from typing import Tuple, Set

import cfpq_data
import networkx as nx

__all__ = ["GraphInfo", "graph_info", "generate_two_cycles_graph"]


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

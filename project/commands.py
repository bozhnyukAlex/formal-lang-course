import sys
from pathlib import Path

import cfpq_data
import networkx as nx

from project.graphs import *

__all__ = ["ExecutionException"]

graph_pool = {}


class ExecutionException(Exception):
    """
    Exception raised for errors in the execution.

    Attributes
    ----------
        message: str
            Explanation of the error
    """

    def __init__(self, message: str):
        self.message = message


def get_graph_info(graph_name: str) -> None:
    """
    Implementation of get_graph_info command in application.
    Prints information about graph by its name.

    Parameters
    ----------
    graph_name: str
        Name of the graph

    Returns
    -------
    None

    Raises
    ------
    ExecutionException
        If there is a problem in graph's name
    """
    if all(
        graph_name not in cfpq_data.DATASET[graph_class].keys()
        for graph_class in cfpq_data.DATASET.keys()
    ):
        raise ExecutionException("No such graph with this name!")

    graph = cfpq_data.graph_from_dataset(graph_name, verbose=False)

    info = graph_info(graph)

    print("Information about graph:")
    print(info)


def create_two_cycles(
    graph_name: str,
    nodes_first_num: str,
    nodes_second_num: str,
    label_first: str,
    label_second: str,
) -> None:
    """
    Implementation of create_two_cycles command in application.
    Create named and labeled graph with two cycles.

    Parameters
    ----------
    graph_name: str
        Name of the created graph
    nodes_first_num: str
        String representation of number of nodes on the first cycle
    nodes_second_num: str
        String representation of number of nodes on the second cycle
    label_first: str
        Label for edges in the first cycle
    label_second: str
        Label for edges in the second cycle

    Returns
    -------
    None
    """
    graph = generate_two_cycles_graph(
        int(nodes_first_num), int(nodes_second_num), (label_first, label_second)
    )

    graph_pool[graph_name] = graph

    print(f"Graph {graph_name} has been created")


def save_to_dot(graph_name: str, folder_path: str):
    """
    Implementation of save_to_dot command in application.
    Saves given graph to the dot file in folder_path.

    Parameters
    ----------
    graph_name: str
        Name of saved graph
    folder_path: str
        Path to the folder where to save graph
    Returns
    -------
    None

    Raises
    ------
    ExecutionException
        If there is no graph with this name
    """
    if graph_name not in graph_pool:
        raise ExecutionException("No graph with this name!")

    graph = graph_pool[graph_name]

    graph_dot = nx.drawing.nx_pydot.to_pydot(graph)
    dot_path = f"{folder_path}/{graph_name}.dot"
    dot_file = Path(dot_path)

    if not dot_file.is_file():
        open(dot_path, "w")

    graph_dot.write_raw(dot_path)

    print(f"Graph was saved in {dot_path}")


def quit_app() -> None:
    """
    Implementation of quit command in application.
    Quits an application.

    Returns
    -------
    None
    """
    print("Quit...")
    sys.exit(0)

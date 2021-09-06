import os
import sys
from pathlib import Path

import networkx
import pydot

from project.graphs import *

__all__ = ["ExecutionException"]


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


def graph_info(graph_filename: str) -> None:
    """
    Implementation of graph_info command in application.
    Prints information about graph by its name.

    Parameters
    ----------
    graph_filename: str
        name of the graph file

    Returns
    -------
    None

    Raises
    ------
    ExecutionException
        If there is a problem file extension of file existence
    """
    file = Path(graph_filename)
    _, extension = os.path.splitext(graph_filename)
    if not file.is_file():
        raise ExecutionException("No such file exists!")
    if extension != ".dot":
        raise ExecutionException("Wrong extension of file!")
    pydot_graph = pydot.graph_from_dot_file(graph_filename)[0]
    graph = networkx.drawing.nx_pydot.from_pydot(pydot_graph)
    info = get_graph_info(graph)
    print("Information about graph")
    print(info)


def create_and_save(
    filename: str,
    nodes_first_num: str,
    nodes_second_num: str,
    label_first: str,
    label_second: str,
) -> None:
    """
    Implementation of create_and_save command in application.
    Generates labeled graph with two cycles and saves it in file.

    Parameters
    ----------
    filename: str
        Name of the file for saving graph
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
    file = Path(filename)
    if not file.is_file():
        open(filename, "w")
    generate_and_save_two_cycles(
        int(nodes_first_num),
        int(nodes_second_num),
        (label_first, label_second),
        filename,
    )
    print("Graph has been created and saved.")


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

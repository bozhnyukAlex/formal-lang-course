import networkx
import pydot

from project import commands
from project import graphs


def test_saving_to_dot_path():
    commands.create_two_cycles("test_path", "3", "4", "a", "b")
    path = commands.save_to_dot("test_path", "data")
    assert path == "data/test.dot"


def test_saving_to_dot_nodes():
    commands.create_two_cycles("test_nodes", "4", "3", "c", "d")
    commands.save_to_dot("test_nodes", "data")
    pydot_graph = pydot.graph_from_dot_file("data/test_nodes.dot")[0]
    graph = networkx.drawing.nx_pydot.from_pydot(pydot_graph)
    info = graphs.graph_info(graph)
    assert info.nodes_count == 8


def test_saving_to_dot_labels():
    commands.create_two_cycles("test_labels", "1", "2", "foo", "bar")
    commands.save_to_dot("test_labels", "data")
    pydot_graph = pydot.graph_from_dot_file("data/test_labels.dot")[0]
    graph = networkx.drawing.nx_pydot.from_pydot(pydot_graph)
    info = graphs.graph_info(graph)
    assert info.labels == {"foo", "bar"}


def test_saving_to_dot_edges():
    commands.create_two_cycles("test_edges", "1", "2", "vvv", "ggg")
    commands.save_to_dot("test_edges", "data")
    pydot_graph = pydot.graph_from_dot_file("data/test_edges.dot")[0]
    graph = networkx.drawing.nx_pydot.from_pydot(pydot_graph)
    info = graphs.graph_info(graph)
    assert info.edges_count == 5

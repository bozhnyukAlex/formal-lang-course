import networkx as nx
import pytest
import rdflib
from pyformlang.finite_automaton import State, NondeterministicFiniteAutomaton, Symbol

from project import commands, generate_two_cycles_graph, graph_to_nfa, GraphException

graph_info = commands.get_graph_info("travel")


def test_graph_info_nodes():
    assert graph_info.nodes_count == 131


def test_graph_info_edges():
    assert graph_info.edges_count == 277


def test_graph_info_labels():
    assert graph_info.labels == {
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#unionOf"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#disjointWith"),
        rdflib.term.URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"),
        rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#onProperty"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#someValuesFrom"),
        rdflib.term.URIRef("http://www.owl-ontologies.com/travel.owl#hasPart"),
        rdflib.term.URIRef("http://www.w3.org/2000/01/rdf-schema#domain"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#inverseOf"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#oneOf"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#hasValue"),
        rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#rest"),
        rdflib.term.URIRef("http://www.owl-ontologies.com/travel.owl#hasAccommodation"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#complementOf"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#differentFrom"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#minCardinality"),
        rdflib.term.URIRef("http://www.w3.org/2000/01/rdf-schema#comment"),
        rdflib.term.URIRef("http://www.w3.org/2000/01/rdf-schema#range"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#equivalentClass"),
        rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#intersectionOf"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#versionInfo"),
    }


def test_convert_to_nfa_deterministic_check():
    graph = generate_two_cycles_graph(2, 2, ("a", "b"))
    nfa = graph_to_nfa(graph)
    assert not nfa.is_deterministic()


@pytest.mark.parametrize(
    "start_states, final_states",
    [
        (None, None),
        ({1}, {2}),
        ({0, 2, 3}, {0, 2, 3}),
    ],
)
def test_convert_to_nfa_is_equivalent(start_states, final_states):

    graph = generate_two_cycles_graph(2, 2, ("a", "b"))
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transitions(
        [(1, "a", 2), (2, "a", 0), (0, "a", 1), (0, "b", 3), (3, "b", 4), (4, "b", 0)]
    )

    if not start_states:
        start_states = {0, 1, 2, 3, 4}
    if not final_states:
        final_states = {0, 1, 2, 3, 4}

    for state in start_states:
        nfa.add_start_state(State(state))
    for state in final_states:
        nfa.add_final_state(State(state))

    nfa_from_graph = graph_to_nfa(graph, start_states, final_states)

    assert nfa_from_graph.is_equivalent_to(nfa)


@pytest.mark.parametrize(
    "word, accept",
    [
        ("a", True),
        ("aa", False),
        ("aaaa", True),
        ("ab", False),
        ("aab", True),
        ("", True),
        ("bbb", True),
        ("b", False),
    ],
)
def test_convert_to_nfa_acceptance(word, accept):
    graph = generate_two_cycles_graph(2, 2, ("a", "b"))
    nfa = graph_to_nfa(graph, {1, 3}, {2, 3})
    assert nfa.accepts(word) == accept


def test_mismatch_states():
    graph = generate_two_cycles_graph(2, 2, ("a", "b"))
    with pytest.raises(GraphException):
        graph_to_nfa(graph, {0, 1, 2, 33}, {0, 1, 2, 3})


def test_null_graph_to_nfa():
    null_graph = nx.null_graph(create_using=nx.MultiDiGraph)
    nfa = graph_to_nfa(null_graph)

    assert nfa.is_empty()


def test_empty_graph_to_nfa():
    empty_graph = nx.empty_graph(3, create_using=nx.MultiDiGraph)
    nfa_from_graph = graph_to_nfa(empty_graph)

    nfa = NondeterministicFiniteAutomaton()
    nfa.add_start_state(State(0))
    nfa.add_start_state(State(1))
    nfa.add_start_state(State(2))
    nfa.add_final_state(State(0))
    nfa.add_final_state(State(1))
    nfa.add_final_state(State(2))

    assert nfa_from_graph.is_equivalent_to(nfa)


def test_one_node_loop_graph_to_nfa():
    one_node_loop = nx.empty_graph(1, create_using=nx.MultiDiGraph)
    one_node_loop.add_edge(0, 0, label="a")
    nfa_from_loop = graph_to_nfa(one_node_loop)

    nfa = NondeterministicFiniteAutomaton()
    nfa.add_start_state(State(0))
    nfa.add_final_state(State(0))
    nfa.add_transition(State(0), Symbol("a"), State(0))

    assert nfa_from_loop.is_equivalent_to(nfa)

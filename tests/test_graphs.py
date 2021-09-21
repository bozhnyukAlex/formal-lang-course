import pytest
import rdflib
from pyformlang.finite_automaton import State, NondeterministicFiniteAutomaton

from project import commands, generate_two_cycles_graph, graph_to_nfa

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

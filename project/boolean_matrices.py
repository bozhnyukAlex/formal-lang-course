from scipy import sparse
from pyformlang.finite_automaton import State, NondeterministicFiniteAutomaton

__all__ = ["BooleanMatrices"]

from scipy.sparse import dok_matrix


class BooleanMatrices:
    """Class representing boolean adjacency matrices
    for each label of finite automaton

    Attributes
    ----------
    num_states: int
        Number of states in automaton
    start_states: Set[State]
        Set of start states of automaton
    final_states: Set[State]
        Set of final states of automaton
    bool_matrices: Dict[Symbol, dok_matrix]
        Mapping of labels to boolean matrices
    state_indexes: Dict[State, int]
        Mapping of states to their indices
    """

    def __init__(self, n_automaton: NondeterministicFiniteAutomaton = None):
        if n_automaton is None:
            self.num_states = 0
            self.start_states = set()
            self.final_states = set()
            self.bool_matrices = {}
            self.state_indexes = {}
        else:
            self.states_count = len(n_automaton.states)
            self.state_indices = {
                state: index for index, state in enumerate(n_automaton.states)
            }
            self.start_states = n_automaton.start_states
            self.final_states = n_automaton.final_states
            self.bool_matrices = self._create_boolean_matrices(n_automaton)

    def to_automaton(self):
        """
        Transforms BooleanMatrices into NFA
        Returns
        -------
        nfa: NondeterministicFiniteAutomaton
            Representation of BooleanMatrices as NFA
        """
        automaton = NondeterministicFiniteAutomaton()
        for label, bool_matrix in self.bool_matrices.items():
            for s_from, s_to in zip(*bool_matrix.nonzero()):
                automaton.add_transition(s_from, label, s_to)

        for state in self.start_states:
            automaton.add_start_state(State(state))

        for state in self.final_states:
            automaton.add_final_state(State(state))

        return automaton

    def get_states(self):
        return self.state_indexes.keys()

    def get_start_states(self):
        return self.start_states.copy()

    def get_final_states(self):
        return self.final_states.copy()

    def transitive_closure(self):
        """
        Computes transitive closure of boolean matrices
        Returns
        -------
        tc: dok_matrix
            Transitive closure of boolean matrices
        """
        if not self.bool_matrices.values():
            return dok_matrix((1, 1))
        tc = sum(bm for bm in self.bool_matrices.values())
        prev_nnz = tc.nnz
        new_nnz = 0

        while prev_nnz != new_nnz:
            tc += tc @ tc
            prev_nnz, new_nnz = new_nnz, tc.nnz

        return tc

    @classmethod
    def from_automaton(cls, automaton):
        """
        Transforms NFA into BooleanMatrices
        Parameters
        ----------
        automaton: NondeterministicFiniteAutomaton
            NFA to transform
        Returns
        -------
        obj: BooleanMatrices
            BooleanMatrices object from NFA
        """
        bm = cls()
        bm.num_states = len(automaton.states)
        bm.start_states = automaton.start_states
        bm.final_states = automaton.final_states
        bm.state_indexes = {state: idx for idx, state in enumerate(automaton.states)}
        bm.bool_matrices = bm._create_boolean_matrices(automaton)
        return bm

    def intersect(self, other):
        """
        Returns a new class object containing
        the Kronecker products for given matrices

        Parameters
        ----------
        other: BooleanMatrices
            Right-hand side boolean matrix
        Returns
        -------
        intersection: BooleanMatrices
            Intersection of two boolean matrices
        """
        bm_res = BooleanMatrices()
        bm_res.num_states = self.num_states * other.num_states
        common_labels = self.bool_matrices.keys() & other.bool_matrices.keys()

        for label in common_labels:
            bm_res.bool_matrices[label] = sparse.kron(
                self.bool_matrices[label], other.bool_matrices[label], format="dok"
            )

        for s_first, s_first_index in self.state_indexes.items():
            for s_second, s_second_index in other.state_indexes.items():
                new_state = new_state_index = (
                    s_first_index * other.num_states + s_second_index
                )
                bm_res.state_indexes[new_state] = new_state_index

                if s_first in self.start_states and s_second in other.start_states:
                    bm_res.start_states.add(new_state)

                if s_first in self.final_states and s_second in other.final_states:
                    bm_res.final_states.add(new_state)

        return bm_res

    def _create_boolean_matrices(self, automaton: NondeterministicFiniteAutomaton):
        """
        Build dict of boolean matrix for every automata label-key from nfa

        Parameters
        ----------
        automaton: NondeterministicFiniteAutomaton
            NFA to transform to matrix
        Returns
        -------
        boolean_matrices: dict
            Dict of boolean matrix for every automata label-key
        """
        bool_matrices = {}
        for s_from, trans in automaton.to_dict().items():
            for label, states_to in trans.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for s_to in states_to:
                    index_from = self.state_indexes[s_from]
                    index_to = self.state_indexes[s_to]
                    if label not in bool_matrices:
                        bool_matrices[label] = sparse.dok_matrix(
                            (self.num_states, self.num_states), dtype=bool
                        )
                    bool_matrices[label][index_from, index_to] = True

        return bool_matrices

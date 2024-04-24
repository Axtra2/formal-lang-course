from pyformlang.finite_automaton import *
from scipy.sparse import *
from networkx import *
from typing import *

from project.task02 import regex_to_dfa, graph_to_nfa

from itertools import product


class FiniteAutomaton:
    def __init__(self, fa=None):
        if fa is None:
            return

        state_to_i = {s: i for i, s in enumerate(fa.states)}

        self.i_to_state = list(fa.states)

        self.start_states = {state_to_i[st] for st in fa.start_states}
        self.final_states = {state_to_i[fi] for fi in fa.final_states}

        self.matrix = {}

        states = fa.to_dict()
        n = len(fa.states)

        for l in fa.symbols:
            self.matrix[l] = dok_matrix((n, n), dtype=bool)
            for st, ls in states.items():
                if l in ls:
                    for fi in ls[l] if isinstance(ls[l], set) else {ls[l]}:
                        self.matrix[l][state_to_i[st], state_to_i[fi]] = True

    def accepts(self, word: Iterable[Symbol]) -> bool:
        nfa = NondeterministicFiniteAutomaton()

        for l, m in self.matrix.items():
            nfa.add_transitions(
                [
                    (st, l, fi)
                    for (st, fi) in product(range(m.shape[0]), repeat=2)
                    if self.matrix[l][st, fi]
                ]
            )

        for st in self.start_states:
            nfa.add_start_state(st)
        for fi in self.final_states:
            nfa.add_final_state(fi)

        return nfa.accepts(word)

    def is_empty(self) -> bool:
        if len(self.matrix) == 0:
            return True
        m = sum(self.matrix.values())
        for _ in range(m.shape[0]):
            m += m @ m
        for st, fi in product(self.start_states, self.final_states):
            if m[st, fi] != 0:
                return False
        return True


def intersect_automata(
    automaton1: FiniteAutomaton, automaton2: FiniteAutomaton
) -> FiniteAutomaton:

    ls = automaton1.matrix.keys() & automaton2.matrix.keys()
    fa = FiniteAutomaton()
    fa.matrix = {}

    for l in ls:
        fa.matrix[l] = kron(automaton1.matrix[l], automaton2.matrix[l], "csr")

    fa.start_states = set()
    fa.final_states = set()

    n_states2 = automaton2.matrix.values().__iter__().__next__().shape[0]

    for i, j in product(automaton1.start_states, automaton2.start_states):
        fa.start_states.add(i * (n_states2) + j)
    for i, j in product(automaton1.final_states, automaton2.final_states):
        fa.final_states.add(i * (n_states2) + j)

    return fa


def paths_ends(
    graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int], regex: str
) -> list[tuple[int, int]]:
    fa1 = FiniteAutomaton(graph_to_nfa(graph, start_nodes, final_nodes))
    fa2 = FiniteAutomaton(regex_to_dfa(regex))
    fa = intersect_automata(fa1, fa2)

    if len(fa.matrix) == 0:
        return []

    m = sum(fa.matrix.values())
    for _ in range(m.shape[0]):
        m += m @ m

    n_states2 = fa2.matrix.values().__iter__().__next__().shape[0]

    def extract_fa1_node_idx(i):
        return fa1.i_to_state[i // n_states2].value

    res = []
    for st, fi in product(fa.start_states, fa.final_states):
        if m[st, fi] != 0:
            res.append((extract_fa1_node_idx(st), extract_fa1_node_idx(fi)))

    return res

from pyformlang.finite_automaton import *

from scipy.sparse import bsr_matrix

from typing import *


class FiniteAutomaton:
    def __init__(self, fa):
        if isinstance(fa, DeterministicFiniteAutomaton):
            pass
        elif isinstance(fa, NondeterministicFiniteAutomaton):
            fa = fa.to_deterministic()
        else:
            return

        n = fa.states()
        # self.states = list(product(fa.states, fa.symbols))

        self.start_states = fa.start_states()
        self.final_states = fa.final_states()
        self.matrix = bsr_matrix((n, n), dtype=str)

        for st, d in fa.to_dict.items():
            for sy, fi in d.items():
                self.matrix[st, fi] += sy

    def accepts(self, word: Iterable[Symbol]) -> bool:
        pass

    def is_empty(self) -> bool:
        pass


def intersect_automata(
    automaton1: FiniteAutomaton, automaton2: FiniteAutomaton
) -> FiniteAutomaton:
    pass

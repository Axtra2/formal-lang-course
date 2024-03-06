from pyformlang.finite_automaton import *
from scipy.sparse import *
from typing import *


class FiniteAutomaton:
    def __init__(self, fa):
        self.start_states = fa.start_states
        self.final_states = fa.final_states
        self.matrix = {}
        self.state_to_i = {s: i for i, s in enumerate(fa.states)}

        states = fa.to_dict()
        n = len(fa.states)

        for l in fa.symbols:
            self.matrix[l] = dok_matrix((n, n), dtype=bool)
            for st, ls in states.items():
                if l in ls:
                    for fi in ls[l]:
                        self.matrix[l][self.state_to_i[st], self.state_to_i[fi]] = True

    def accepts(self, word: Iterable[Symbol]) -> bool:
        pass

    def is_empty(self) -> bool:
        pass


def intersect_automata(
    automaton1: FiniteAutomaton, automaton2: FiniteAutomaton
) -> FiniteAutomaton:
    pass

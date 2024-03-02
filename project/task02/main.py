from networkx import MultiDiGraph

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol
from pyformlang.finite_automaton import Epsilon

from pyformlang.regular_expression import Regex

import project.task01

from typing import Set


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    return Regex(regex).to_epsilon_nfa().to_deterministic().minimize()


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:

    if len(start_states) == 0:
        start_states = graph.nodes

    if len(final_states) == 0:
        final_states = graph.nodes

    e_nfa = EpsilonNFA()
    for s in start_states:
        e_nfa.add_start_state(s)
    for s in final_states:
        e_nfa.add_final_state(s)
    for s, t, l in graph.edges(data="label"):
        e_nfa.add_transition(s, l, t)

    return e_nfa.remove_epsilon_transitions().minimize()

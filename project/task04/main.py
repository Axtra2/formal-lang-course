from project.task03 import FiniteAutomaton
from scipy.sparse import *


def diagonalise(m):
    h = m.shape[0]

    res = dok_matrix(m.shape, dtype=bool)

    for i in range(h):
        for j in range(h):
            if m[j, i]:
                res[i] += m[j]

    return res


def reachability_with_constraints(
    fa: FiniteAutomaton, constraints_fa: FiniteAutomaton
) -> dict[int, set[int]]:

    ms = {}

    ls = fa.matrix.keys() & constraints_fa.matrix.keys()
    m, n = len(constraints_fa.i_to_state), len(fa.i_to_state)

    for l in ls:
        A = constraints_fa.matrix[l]
        B = fa.matrix[l]
        ms[l] = block_diag((A, B))

    h = m
    w = m + n

    res = {s.value: set() for s in fa.i_to_state}

    for st in fa.start_states:
        front = dok_matrix((h, w), dtype=bool)
        for cst in constraints_fa.start_states:
            front[cst, cst] = True

        for i in range(h):
            front[i, st + m] = True

        for _ in range(m * n):
            new_front = dok_matrix((h, w), dtype=bool)
            for l in ls:
                new_front += diagonalise(front @ ms[l])
            front = new_front
            for i in range(h):
                if i in constraints_fa.final_states and front[i, i]:
                    for j in range(n):
                        if j in fa.final_states and front[i, j + m]:
                            res[fa.i_to_state[st]].add(fa.i_to_state[j])
    return res

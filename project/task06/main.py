from pyformlang.cfg import *

from typing import *
import networkx as nx
from copy import deepcopy


def cfg_to_weak_normal_form(cfg: CFG) -> CFG:
    cfg = cfg.eliminate_unit_productions().remove_useless_symbols()
    return CFG(
        start_symbol=cfg.start_symbol,
        productions=cfg._decompose_productions(
            cfg._get_productions_with_only_single_terminals()
        ),
    )


def cfpq_with_hellings(
    cfg: CFG,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:

    start_nodes = graph.nodes if start_nodes is None else start_nodes
    final_nodes = graph.nodes if final_nodes is None else final_nodes
    cfg = cfg_to_weak_normal_form(cfg)

    N_to_eps = {p.head for p in cfg.productions if len(p.body) == 0}

    N_to_t = {}
    for p in cfg.productions:
        if len(p.body) == 1 and isinstance(p.body[0], Terminal):
            N_to_t.setdefault(p.head, set()).add(p.body[0])

    N_to_NN = {}
    for p in cfg.productions:
        if len(p.body) == 2:
            N_to_NN.setdefault(p.head, set()).add((p.body[0], p.body[1]))

    r = {(N, n, n) for N in N_to_eps for n in graph.nodes} | {
        (N, n, m)
        for N, ls in N_to_t.items()
        for n, m, l in graph.edges(data="label")
        if Terminal(l) in ls
    }

    new = r.copy()

    while len(new) != 0:
        N, n, m = new.pop()
        to_add = set()
        for M, n_, m_ in r:
            if m_ == n:
                for N_, NNs in N_to_NN.items():
                    if (M, N) in NNs and (N_, n_, m) not in r:
                        new.add((N_, n_, m))
                        to_add.add((N_, n_, m))
            if n_ == m:
                for M_, NNs in N_to_NN.items():
                    if (N, M) in NNs and (M_, n, m_) not in r:
                        new.add((M_, n, m_))
                        to_add.add((M_, n, m_))
        r |= to_add

    return {
        (n, m)
        for N, n, m in r
        if n in start_nodes and m in final_nodes and N == cfg.start_symbol
    }

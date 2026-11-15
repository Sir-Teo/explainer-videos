"""Monochord's research methods (Part 67 of *Music, Built*): how the kinds of music research know what they claim, each
with something to compute.

    copy_tradition                a manuscript tradition: a tune copied by scribes, each copy keeping its exemplar's
                                  errors and adding its own; some copies lost
    hamming, neighbor_joining     distances between surviving witnesses by shared readings, and a tree joined from them
                                  (Saitou and Nei, 1987)
    splits, rf_distance           a tree as the bipartitions of its leaves, and the Robinson-Foulds distance between two
    reconstruct                   the lost original, by majority of the witnesses and by majority within each branch
    abx_power                     the exact power of a listening test of n ABX trials at a true hit rate
    abx_trials_needed             the fewest trials for a given power
    star_problems                 every part's research problem, read from the series' READMEs

No manim.  Checked in ``tests/music/test_research.py``.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from scipy import stats


# --------------------------------------------------------------------------------------------- manuscripts
def copy_tradition(notes, rng, generations: int = 4, children=(1, 3), error_rate: float = 0.04, lost: float = 0.4) -> dict:
    """Copy ``notes`` (a list of key numbers) down ``generations`` of scribes.  Each copy has 1 to 3 children; each note
    of a copy is miscopied with probability ``error_rate`` (a step up or down, or a third), on top of its exemplar's
    errors.  The original and a share ``lost`` of the copies are lost; the rest survive.  Returns every manuscript with
    its parent, and which survive."""
    mss = [{"id": 0, "parent": None, "notes": list(notes), "gen": 0}]
    frontier = [0]
    for g in range(1, generations + 1):
        nxt = []
        for p in frontier:
            for _ in range(int(rng.integers(children[0], children[1] + 1))):
                x = list(mss[p]["notes"])
                for i in range(len(x)):
                    if rng.random() < error_rate:
                        x[i] += int(rng.choice([-2, -1, 1, 2, -4, 4]))
                mss.append({"id": len(mss), "parent": p, "notes": x, "gen": g})
                nxt.append(len(mss) - 1)
        frontier = nxt
    survive = [m["id"] for m in mss if m["id"] != 0 and rng.random() > lost]
    return {"mss": mss, "survive": survive}


def hamming(a, b) -> int:
    return int(sum(x != y for x, y in zip(a, b)))


def neighbor_joining(D, names) -> dict:
    """Neighbour joining on a distance matrix: repeatedly join the pair that minimizes the Q criterion.  Returns an
    unrooted tree as an adjacency dict {node: {neighbour: length}}, leaves named by ``names``."""
    D = np.asarray(D, float).copy()
    nodes = list(names)
    adj = {n: {} for n in nodes}
    k = 0
    while len(nodes) > 2:
        n = len(nodes)
        r = D.sum(1)
        Q = (n - 2) * D - r[:, None] - r[None, :]
        np.fill_diagonal(Q, np.inf)
        i, j = np.unravel_index(int(np.argmin(Q)), Q.shape)
        u = f"x{k}"
        k += 1
        di = 0.5 * D[i, j] + (r[i] - r[j]) / (2 * (n - 2))
        dj = D[i, j] - di
        adj[u] = {nodes[i]: max(di, 0.0), nodes[j]: max(dj, 0.0)}
        adj[nodes[i]][u] = max(di, 0.0)
        adj[nodes[j]][u] = max(dj, 0.0)
        du = 0.5 * (D[i] + D[j] - D[i, j])
        keep = [m for m in range(n) if m not in (i, j)]
        D2 = np.zeros((len(keep) + 1, len(keep) + 1))
        D2[:-1, :-1] = D[np.ix_(keep, keep)]
        D2[-1, :-1] = D2[:-1, -1] = du[keep]
        D = D2
        nodes = [nodes[m] for m in keep] + [u]
    a, b = nodes
    adj[a][b] = adj[b][a] = max(D[0, 1], 0.0)
    return adj


def splits(adj, leaves) -> set:
    """The non-trivial bipartitions of the leaves made by cutting each internal edge (as frozensets of the side
    without the first leaf)."""
    leaves = set(leaves)
    ref = min(leaves)
    out = set()
    for u in adj:
        for v in adj[u]:
            if u < v or True:
                side = _side(adj, v, u) & leaves
                if 1 < len(side) < len(leaves) - 1:
                    s = frozenset(side) if ref not in side else frozenset(leaves - side)
                    out.add(s)
    return out


def _side(adj, start, block):
    seen, stack = {start}, [start]
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y != block and y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


def true_adjacency(mss, survive) -> dict:
    """The real copying tree, reduced to the surviving manuscripts (lost ones kept as internal nodes, chains of lost
    single-child copies contracted implicitly by the split comparison)."""
    adj = {m["id"]: {} for m in mss}
    for m in mss:
        if m["parent"] is not None:
            adj[m["id"]][m["parent"]] = 1.0
            adj[m["parent"]][m["id"]] = 1.0
    keep = set(survive)
    # prune lost leaves repeatedly, so every leaf of the tree survives
    changed = True
    while changed:
        changed = False
        for n in list(adj):
            if n not in keep and len(adj[n]) <= 1:
                for v in adj[n]:
                    del adj[v][n]
                del adj[n]
                changed = True
    return {str(k): {str(v): w for v, w in nb.items()} for k, nb in adj.items()}


def rf_distance(adj1, adj2, leaves) -> dict:
    """The Robinson-Foulds distance: bipartitions in one tree and not the other, and the share recovered."""
    leaves = [str(x) for x in leaves]
    s1, s2 = splits(adj1, leaves), splits(adj2, leaves)
    return {"rf": len(s1 ^ s2), "true_splits": len(s1), "recovered": len(s1 & s2), "share": len(s1 & s2) / max(len(s1), 1)}


def reconstruct(witnesses) -> list:
    """The reading of the majority of the witnesses at each position (ties to the lower note)."""
    W = np.array(witnesses)
    out = []
    for col in W.T:
        vals, counts = np.unique(col, return_counts=True)
        out.append(int(vals[np.argmax(counts)]))
    return out


def reconstruct_by_branch(witnesses, groups) -> list:
    """Lachmann's idea, crudely: let each branch of the tradition (a group of witnesses descended from one lost copy)
    cast one vote, its own majority, so a prolific branch cannot outvote the others."""
    votes = [reconstruct([witnesses[i] for i in g]) for g in groups if g]
    return reconstruct(votes)


# --------------------------------------------------------------------------------------------- listening tests
def abx_power(p_true: float, n: int, alpha: float = 0.05) -> dict:
    """An ABX test of n trials: the listener passes if the hits reach the binomial critical value at ``alpha``
    (one-sided, chance 1/2).  Returns the critical number of hits, the exact size and the power at ``p_true``."""
    c = int(stats.binom.ppf(1 - alpha, n, 0.5)) + 1
    size = float(stats.binom.sf(c - 1, n, 0.5))
    power = float(stats.binom.sf(c - 1, n, p_true))
    return {"n": n, "critical": c, "size": size, "power": power}


def abx_trials_needed(p_true: float, power: float = 0.8, alpha: float = 0.05, nmax: int = 2000) -> int:
    for n in range(4, nmax):
        if abx_power(p_true, n, alpha)["power"] >= power:
            return n
    return nmax


# --------------------------------------------------------------------------------------------- the series' open problems
def star_problems(root, series: str = "music") -> list:
    """Every part's starred research problem, from ``videos/<series>/<part>/README.md``: (part, question)."""
    out = []
    for d in sorted(Path(root, "videos", series).glob(f"{series}[0-9]*"), key=lambda p: int(re.sub(r"\D", "", p.name) or 0)):
        f = d / "README.md"
        if not f.exists():
            continue
        for line in f.read_text().splitlines():
            m = re.match(r"^\s*\d+\.\s*★\s*\*\*(.+?)\*\*", line)
            if m:
                out.append((int(re.sub(r"\D", "", d.name)), m.group(1).strip()))
                break
    return out

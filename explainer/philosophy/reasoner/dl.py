"""Formal ontology as engineering (Part 20): the description logic ALC, OntoClean, and a knowledge-graph embedding.

Concepts are nested tuples: ``"A"`` (a concept name), ``("top",)``, ``("bot",)``, ``("not", C)``,
``("and", C, D)``, ``("or", C, D)``, ``("some", r, C)``, ``("all", r, C)``.

* ``satisfiable(C, tbox)`` decides ALC concept satisfiability with respect to an acyclic TBox of definitions
  (A = C), by unfolding and the standard tableau: a completion tree whose nodes carry concept labels, expanded by the
  and-, or-, some- and all-rules until a clash (A and not A, or bottom) closes every branch or a complete open branch
  remains, which is a model. The rule applications are recorded for display.
* ``subsumes(C, D, tbox)``: C is subsumed by D iff C and not D is unsatisfiable.
* ``ontoclean(...)`` checks Guarino and Welty's rigidity and identity constraints on a taxonomy.
* ``transe(...)`` trains a two-dimensional TransE embedding (h + r = t) on a toy knowledge graph and ranks candidate
  answers for queries, including ones the graph never mentions.
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# Syntax
# ---------------------------------------------------------------------------
def Not(c):
    return ("not", c)


def And(*cs):
    out = cs[0]
    for c in cs[1:]:
        out = ("and", out, c)
    return out


def Or(*cs):
    out = cs[0]
    for c in cs[1:]:
        out = ("or", out, c)
    return out


def Some(r, c):
    return ("some", r, c)


def All(r, c):
    return ("all", r, c)


TOP, BOT = ("top",), ("bot",)


def show(c, tex: bool = True) -> str:
    """A concept as TeX (math mode)."""
    if isinstance(c, str):
        return r"\mathit{" + c + "}" if tex else c
    op = c[0]
    if op == "top":
        return r"\top" if tex else "T"
    if op == "bot":
        return r"\bot" if tex else "F"
    if op == "not":
        return (r"\lnot " if tex else "~") + show(c[1], tex)
    if op in ("and", "or"):
        sym = (r" \sqcap " if op == "and" else r" \sqcup ") if tex else (" & " if op == "and" else " | ")
        parts = []
        for x in (c[1], c[2]):
            s = show(x, tex)
            if not isinstance(x, str) and x[0] in ("and", "or") and x[0] != op:
                s = "(" + s + ")"
            parts.append(s)
        return sym.join(parts)
    q = (r"\exists " if op == "some" else r"\forall ") if tex else ("E" if op == "some" else "A")
    inner = show(c[2], tex)
    if not isinstance(c[2], str) and c[2][0] in ("and", "or"):
        inner = "(" + inner + ")"
    return q + (r"\mathit{" + c[1] + "}" if tex else c[1]) + "." + inner


def nnf(c):
    """Negation normal form: push negations onto concept names."""
    if isinstance(c, str) or c[0] in ("top", "bot"):
        return c
    op = c[0]
    if op in ("and", "or"):
        return (op, nnf(c[1]), nnf(c[2]))
    if op in ("some", "all"):
        return (op, c[1], nnf(c[2]))
    d = c[1]
    if isinstance(d, str):
        return c
    if d[0] == "top":
        return BOT
    if d[0] == "bot":
        return TOP
    if d[0] == "not":
        return nnf(d[1])
    if d[0] == "and":
        return ("or", nnf(Not(d[1])), nnf(Not(d[2])))
    if d[0] == "or":
        return ("and", nnf(Not(d[1])), nnf(Not(d[2])))
    if d[0] == "some":
        return ("all", d[1], nnf(Not(d[2])))
    return ("some", d[1], nnf(Not(d[2])))


def unfold(c, tbox: dict):
    """Replace defined names by their definitions (the TBox must be acyclic)."""
    if isinstance(c, str):
        return unfold(tbox[c], tbox) if c in tbox else c
    if c[0] in ("top", "bot"):
        return c
    if c[0] == "not":
        return ("not", unfold(c[1], tbox))
    if c[0] in ("and", "or"):
        return (c[0], unfold(c[1], tbox), unfold(c[2], tbox))
    return (c[0], c[1], unfold(c[2], tbox))


# ---------------------------------------------------------------------------
# Tableau
# ---------------------------------------------------------------------------
def _clash(label) -> bool:
    return BOT in label or any(isinstance(x, str) and ("not", x) in label for x in label)


def _expand(nodes, edges, log, depth=0):
    """Expand a completion tree. ``nodes``: list of sets of concepts; ``edges``: list of (parent, role, child).
    Returns a complete clash-free tree, or None."""
    while True:
        for i, L in enumerate(nodes):
            if _clash(L):
                log.append(("clash", i, None))
                return None
        progress = False
        # and-rule
        for i, L in enumerate(nodes):
            for c in list(L):
                if not isinstance(c, str) and c[0] == "and" and not ({c[1], c[2]} <= L):
                    L |= {c[1], c[2]}
                    log.append(("and", i, c))
                    progress = True
        if progress:
            continue
        # all-rule
        for (p, r, ch) in edges:
            for c in list(nodes[p]):
                if not isinstance(c, str) and c[0] == "all" and c[1] == r and c[2] not in nodes[ch]:
                    nodes[ch].add(c[2])
                    log.append(("all", ch, c))
                    progress = True
        if progress:
            continue
        # or-rule (branch)
        for i, L in enumerate(nodes):
            for c in list(L):
                if not isinstance(c, str) and c[0] == "or" and c[1] not in L and c[2] not in L:
                    for pick in (c[1], c[2]):
                        n2 = [set(x) for x in nodes]
                        n2[i].add(pick)
                        log.append(("or", i, (c, pick)))
                        res = _expand(n2, list(edges), log, depth + 1)
                        if res is not None:
                            return res
                    return None
        # some-rule
        for i, L in enumerate(nodes):
            for c in list(L):
                if not isinstance(c, str) and c[0] == "some":
                    if not any(p == i and r == c[1] and c[2] in nodes[ch] for (p, r, ch) in edges):
                        nodes.append({c[2]})
                        edges.append((i, c[1], len(nodes) - 1))
                        log.append(("some", len(nodes) - 1, c))
                        progress = True
                        break
            if progress:
                break
        if progress:
            continue
        return nodes, edges


def satisfiable(c, tbox: dict | None = None) -> dict:
    tbox = tbox or {}
    c0 = nnf(unfold(c, tbox))
    log: list = []
    res = _expand([{c0}], [], log)
    model = None
    if res is not None:
        nodes, edges = res
        model = {"nodes": [sorted(show(x, False) for x in L if isinstance(x, str) or x[0] == "not") for L in nodes],
                 "edges": edges}
    return {"satisfiable": res is not None, "steps": len(log), "log": [(k, i, _fmt(x)) for k, i, x in log],
            "model": model, "unfolded": show(c0)}


def _fmt(x):
    if x is None:
        return None
    if isinstance(x, tuple) and len(x) == 2 and isinstance(x[0], tuple) and x[0][0] == "or":
        return [show(x[0]), show(x[1])]
    return show(x)


def subsumes(c, d, tbox: dict | None = None) -> dict:
    """C is subsumed by D (every C is a D) iff C and not D is unsatisfiable."""
    r = satisfiable(And(c, Not(d)), tbox)
    return {"subsumed": not r["satisfiable"], **r}


FAMILY = {
    "Woman": And("Person", "Female"),
    "Man": And("Person", Not("Female")),
    "Parent": And("Person", Some("hasChild", "Person")),
    "Mother": And("Woman", "Parent"),
    "Father": And("Man", "Parent"),
    "Grandmother": And("Mother", Some("hasChild", "Parent")),
    "MotherWithoutDaughter": And("Mother", All("hasChild", Not("Woman"))),
}


def family_demo() -> dict:
    """The textbook family TBox (Baader et al., ch. 2) and four questions, decided by the tableau."""
    qs = {
        "Mother is a Parent": ("Mother", "Parent"),
        "Grandmother is a Parent": ("Grandmother", "Parent"),
        "Parent is a Mother": ("Parent", "Mother"),
        "Father is a Woman": ("Father", "Woman"),
    }
    out = {name: subsumes(a, b, FAMILY) for name, (a, b) in qs.items()}
    contra = satisfiable(And("MotherWithoutDaughter", Some("hasChild", "Woman")), FAMILY)
    defs = {k: show(v) for k, v in FAMILY.items()}
    return {"tbox": defs, "queries": {k: {"subsumed": v["subsumed"], "steps": v["steps"], "log": v["log"][:14],
                                          "model": v["model"]} for k, v in out.items()},
            "contradiction": {"satisfiable": contra["satisfiable"], "steps": contra["steps"],
                              "log": contra["log"][:16]}}


# ---------------------------------------------------------------------------
# OntoClean
# ---------------------------------------------------------------------------
TAXONOMY = {
    # class: (rigidity: '+R' rigid, '~R' anti-rigid, '-R' non-rigid; identity: '+I' carries a criterion or '-I')
    "Entity": ("+R", "-I"),
    "Physical object": ("+R", "+I"),
    "Amount of matter": ("+R", "-I"),
    "Person": ("+R", "+I"),
    "Apple": ("+R", "+I"),
    "Food": ("~R", "-I"),
    "Student": ("~R", "+I"),
    "Legal agent": ("~R", "+I"),
    "Red thing": ("-R", "-I"),
}
SUBCLASS = [
    ("Physical object", "Entity"), ("Amount of matter", "Entity"), ("Person", "Physical object"),
    ("Student", "Person"), ("Person", "Legal agent"), ("Apple", "Food"), ("Physical object", "Amount of matter"),
    ("Apple", "Red thing"),
]


def ontoclean(tax: dict | None = None, sub: list | None = None) -> dict:
    """Guarino and Welty (2002). Rigidity: an anti-rigid class cannot subsume a rigid one (if being a person is
    essential, and being a legal agent is not, persons cannot all be legal agents by necessity). Identity: a class
    whose members carry an identity criterion cannot be subsumed by one whose members cannot share it (here: no +I
    under -I that is itself a +R kind of stuff)."""
    tax = tax or TAXONOMY
    sub = sub or SUBCLASS
    report = []
    for c, p in sub:
        rc, ic = tax[c]
        rp, ip = tax[p]
        why = None
        if rp == "~R" and rc == "+R":
            why = "an anti-rigid class subsumes a rigid one"
        elif ic == "+I" and ip == "-I" and rp == "+R" and p != "Entity":
            why = "a countable kind under a mass kind: incompatible identity criteria"
        report.append({"sub": c, "sup": p, "ok": why is None, "why": why})
    return {"taxonomy": {k: list(v) for k, v in tax.items()}, "report": report,
            "violations": sum(not r["ok"] for r in report)}


# ---------------------------------------------------------------------------
# A knowledge-graph embedding
# ---------------------------------------------------------------------------
KG = [
    ("Paris", "capital of", "France"), ("Berlin", "capital of", "Germany"), ("Rome", "capital of", "Italy"),
    ("Madrid", "capital of", "Spain"), ("Lisbon", "capital of", "Portugal"),
    ("France", "in", "Europe"), ("Germany", "in", "Europe"), ("Italy", "in", "Europe"), ("Spain", "in", "Europe"),
    ("Portugal", "in", "Europe"), ("Tokyo", "capital of", "Japan"), ("Japan", "in", "Asia"),
    ("Seoul", "capital of", "Korea"), ("Korea", "in", "Asia"),
]
HELD_OUT = ("Lisbon", "capital of", "Portugal")


def transe(dim: int = 2, epochs: int = 3000, lr: float = 0.02, margin: float = 1.0, seed: int = 2013,
           held_out=HELD_OUT) -> dict:
    """Bordes et al. (2013): each entity is a point, each relation a translation, and a triple (h, r, t) is plausible
    when h + r lies near t. Trained by margin ranking against corrupted tails, without the held-out triple. Then the
    embedding scores every possible triple: it `says' something about pairs the graph never mentions."""
    rng = np.random.default_rng(seed)
    train = [t for t in KG if t != held_out]
    ents = sorted({x for h, _, t in KG for x in (h, t)})
    rels = sorted({r for _, r, _ in KG})
    E = {e: rng.normal(0, 0.5, dim) for e in ents}
    R = {r: rng.normal(0, 0.5, dim) for r in rels}
    for _ in range(epochs):
        for h, r, t in train:
            t2 = ents[rng.integers(len(ents))]
            if t2 == t:
                continue
            pos = E[h] + R[r] - E[t]
            neg = E[h] + R[r] - E[t2]
            dp, dn = np.linalg.norm(pos), np.linalg.norm(neg)
            if dp + margin > dn:
                gp = pos / (dp + 1e-9)
                gn = neg / (dn + 1e-9)
                E[h] -= lr * (gp - gn)
                R[r] -= lr * (gp - gn)
                E[t] += lr * gp
                E[t2] -= lr * gn
        for e in ents:
            nrm = np.linalg.norm(E[e])
            if nrm > 1.5:
                E[e] *= 1.5 / nrm

    def rank(h, r, cands):
        s = {c: float(np.linalg.norm(E[h] + R[r] - E[c])) for c in cands}
        return sorted(s.items(), key=lambda kv: kv[1])

    countries = ["France", "Germany", "Italy", "Spain", "Portugal", "Japan", "Korea"]
    held = rank(held_out[0], held_out[1], countries)
    odd = rank("Tokyo", "in", ["Europe", "Asia"])
    weird = rank("Europe", "capital of", countries)
    return {"entities": {e: [float(x) for x in E[e]] for e in ents}, "relations": {r: [float(x) for x in R[r]]
                                                                                     for r in rels},
            "held_out": list(held_out), "held_rank": [c for c, _ in held].index(held_out[2]) + 1,
            "held_top": held[:3], "tokyo_in": odd, "europe_capital_of": weird[:3], "train": len(train),
            "possible_triples": len(ents) * len(rels) * len(ents)}


if __name__ == "__main__":  # pragma: no cover
    import json
    print(json.dumps({k: v["subsumed"] for k, v in family_demo()["queries"].items()}))


# ---------------------------------------------------------------------------
# Individuals: an ABox, by rolling up
# ---------------------------------------------------------------------------
ABOX = {
    "concepts": {"Mary": ["Woman"], "Tom": ["Person"], "Ann": ["Woman"]},
    "roles": [("Mary", "hasChild", "Tom"), ("Tom", "hasChild", "Ann")],
}


def msc(abox: dict, ind: str):
    """The most specific concept of an individual in a tree-shaped ABox: its asserted concepts, and an existential
    for each role successor, rolled up recursively."""
    parts = [c for c in abox["concepts"].get(ind, [])]
    for a, r, b in abox["roles"]:
        if a == ind:
            parts.append(Some(r, msc(abox, b)))
    return And(*parts) if parts else TOP


def instance(abox: dict, ind: str, c, tbox: dict | None = None) -> str:
    """`yes' if the ABox entails that ind is a C, `no' if it entails that ind is not a C, and otherwise `unknown':
    the open-world answer."""
    m = msc(abox, ind)
    if subsumes(m, c, tbox)["subsumed"]:
        return "yes"
    if subsumes(m, Not(c), tbox)["subsumed"]:
        return "no"
    return "unknown"


def abox_demo() -> dict:
    qs = [("Mary", "Mother"), ("Mary", "Grandmother"), ("Tom", "Parent"), ("Tom", "Father"), ("Tom", "Woman"),
          ("Ann", "Parent"), ("Ann", "Man")]
    return {"abox": {"concepts": ABOX["concepts"], "roles": [list(t) for t in ABOX["roles"]]},
            "msc": {i: show(msc(ABOX, i)) for i in ABOX["concepts"]},
            "answers": [{"ind": i, "concept": c, "answer": instance(ABOX, i, c, FAMILY)} for i, c in qs]}

"""Identity and persistence, built (Part 21).

* Discernibility on finite structures: Quine's grades (absolute, relative, weak) computed by brute force, with
  Black's two spheres and the singlet state as examples, and automorphisms as the test of absolute indiscernibility.
* Reid's brave officer: a memory relation that is not transitive, its transitive closure, and the contradiction
  Locke's criterion runs into.
* The ship of Theseus with Hobbes's twist: planks replaced one by one and reassembled; continuity and composition
  tracked over time.
* Evans's argument against vague identity, model-checked over precisifications: with rigid names indeterminate
  identity is impossible; with non-rigid names it is possible, and the lambda step of Evans's proof fails.
* Fission as a branching continuity graph: where identity (transitive, one-one) and continuity (what matters) part.
"""

from __future__ import annotations

import itertools

import numpy as np


# ---------------------------------------------------------------------------
# Discernibility
# ---------------------------------------------------------------------------
def automorphisms(n: int, relations: dict[str, set[tuple]]) -> list[tuple[int, ...]]:
    """Permutations of 0..n-1 that preserve every relation (unary relations as sets of 1-tuples)."""
    out = []
    for p in itertools.permutations(range(n)):
        if all({tuple(p[i] for i in t) for t in R} == R for R in relations.values()):
            out.append(p)
    return out


def discernibility(n: int, relations: dict[str, set[tuple]], a: int, b: int) -> dict:
    """Quine's grades for two objects of a finite relational structure, by brute force over the atomic formulas in
    one or two variables. Absolutely discernible: some one-place condition (built from the relations with a, b as
    free-variable instances and quantification over the domain) holds of one and not the other; the test used here is
    that no automorphism swaps them, which for finite structures is equivalent for first-order definable conditions.
    Relatively discernible: some binary relation R has R(a, b) but not R(b, a). Weakly discernible: some binary
    relation R has R(a, b) but not R(a, a), i.e. an irreflexive relation holds between them."""
    autos = automorphisms(n, relations)
    swaps = any(p[a] == b for p in autos)
    absolute = not swaps
    binaries = {k: R for k, R in relations.items() if R and len(next(iter(R))) == 2}
    relative = any(((a, b) in R) != ((b, a) in R) for R in binaries.values())
    weak = any(((a, b) in R and (a, a) not in R) or ((b, a) in R and (b, b) not in R) for R in binaries.values())
    grade = "absolute" if absolute else ("relative" if relative else ("weak" if weak else "indiscernible"))
    return {"absolute": absolute, "relative": relative, "weak": weak, "grade": grade, "automorphisms": len(autos)}


def black_spheres() -> dict:
    """Max Black (1952): two iron spheres, a mile apart, alone in space. Every intrinsic and relational property one
    has the other has too (an automorphism swaps them), yet `is a mile from' holds between them and not between either
    and itself: weakly discernible. A third case: two spheres at the ends of an asymmetric chain are absolutely
    discernible."""
    spheres = discernibility(2, {"iron": {(0,), (1,)}, "mile from": {(0, 1), (1, 0)}}, 0, 1)
    singlet = discernibility(2, {"fermion": {(0,), (1,)}, "opposite spin to": {(0, 1), (1, 0)}}, 0, 1)
    arrow = discernibility(2, {"points at": {(0, 1)}}, 0, 1)
    lone = discernibility(2, {"iron": {(0,), (1,)}}, 0, 1)
    one_red = discernibility(2, {"red": {(0,)}}, 0, 1)
    return {"spheres": spheres, "singlet": singlet, "arrow": arrow, "no relation": lone, "one red": one_red}


# ---------------------------------------------------------------------------
# Reid's brave officer
# ---------------------------------------------------------------------------
def reid() -> dict:
    """The boy is flogged; the officer takes a standard and remembers the flogging; the general remembers taking the
    standard but not the flogging. Memory links are not transitive; their ancestral (continuity) is. Locke's
    criterion (same person iff remembers) then gives boy = officer, officer = general, boy != general."""
    people = ["boy", "officer", "general"]
    memory = {("officer", "boy"), ("general", "officer")}
    def remembers(x, y):
        return x == y or (x, y) in memory or (y, x) in memory
    pairs = [(x, y) for x in people for y in people if x < y or True]
    direct = {(x, y): remembers(x, y) for x in people for y in people}
    # ancestral: chains of memory links
    closure = {(x, y): direct[(x, y)] for x in people for y in people}
    for k in people:
        for i in people:
            for j in people:
                if closure[(i, k)] and closure[(k, j)]:
                    closure[(i, j)] = True
    transitive = all(not (direct[(i, j)] and direct[(j, k)]) or direct[(i, k)] for i in people for j in people
                     for k in people)
    return {"people": people, "memory": sorted(memory), "direct_boy_general": direct[("boy", "general")],
            "closure_boy_general": closure[("boy", "general")], "direct_transitive": transitive,
            "verdicts": {"boy = officer": direct[("boy", "officer")], "officer = general": direct[("officer", "general")],
                         "boy = general": direct[("boy", "general")]}}


# ---------------------------------------------------------------------------
# The ship of Theseus
# ---------------------------------------------------------------------------
def theseus(planks: int = 40, seed: int = 1655) -> dict:
    """Replace one plank a day, in a random order; Hobbes's twist: a scavenger keeps every old plank and rebuilds a
    ship from them in the original arrangement. Track the share of original planks in the repaired ship (continuity)
    and in the rebuilt one (composition)."""
    rng = np.random.default_rng(seed)
    order = rng.permutation(planks)
    repaired = np.zeros(planks, int)   # 0 original, 1 new
    rebuilt = np.zeros(planks, int)    # 1 if the original plank is in place in the rebuilt ship
    share_a, share_b, frames = [], [], []
    for day in range(planks + 1):
        share_a.append(float(1 - repaired.mean()))
        share_b.append(float(rebuilt.mean()))
        if day in (0, planks // 4, planks // 2, 3 * planks // 4, planks):
            frames.append({"day": day, "repaired": repaired.tolist(), "rebuilt": rebuilt.tolist()})
        if day < planks:
            k = order[day]
            repaired[k] = 1
            rebuilt[k] = 1
    return {"planks": planks, "order": order.tolist(), "share_repaired": share_a, "share_rebuilt": share_b,
            "frames": frames}


# ---------------------------------------------------------------------------
# Evans on vague identity, model-checked
# ---------------------------------------------------------------------------
def evans(n_objects: int = 3, n_precis: int = 3) -> dict:
    """Worlds are precisifications. A name is rigid if it denotes the same object on every precisification.
    `Delta(phi)' (determinately phi) holds iff phi holds on every precisification; `nabla(phi)' (indeterminately)
    iff neither phi nor not-phi is determinate. Enumerate every assignment of referents to two names a, b: with rigid
    names, nabla(a = b) is never true; with non-rigid names it can be, but then the property `x is such that
    nabla(x = a)', read de re of the object b denotes, is undefined, because b denotes different objects on different
    precisifications: Evans's lambda-abstraction step needs rigidity."""
    objs = range(n_objects)
    assigns = list(itertools.product(objs, repeat=n_precis))
    rigid = [(x, x) for x in assigns if len(set(x)) == 1]

    def nabla_eq(a, b):
        vals = {a[i] == b[i] for i in range(n_precis)}
        return len(vals) == 2

    rigid_pairs = [(a, b) for a in assigns if len(set(a)) == 1 for b in assigns if len(set(b)) == 1]
    any_pairs = [(a, b) for a in assigns for b in assigns]
    rigid_vague = sum(nabla_eq(a, b) for a, b in rigid_pairs)
    any_vague = sum(nabla_eq(a, b) for a, b in any_pairs)
    example = next((a, b) for a, b in any_pairs if nabla_eq(a, b) and len(set(a)) == 1)
    steps = [
        (r"\nabla(a = b)", "assumption: it is indeterminate whether a is b"),
        (r"\lambda x[\nabla(x = a)]\,b", "abstraction: b has the property of being indeterminately a"),
        (r"\lnot \nabla(a = a)", "a is determinately a"),
        (r"\lnot \lambda x[\nabla(x = a)]\,a", "abstraction: a lacks that property"),
        (r"\lnot (a = b)", "Leibniz's law: a and b differ in a property"),
    ]
    return {"rigid_pairs": len(rigid_pairs), "rigid_vague": rigid_vague, "all_pairs": len(any_pairs),
            "nonrigid_vague": any_vague, "example": {"a": list(example[0]), "b": list(example[1])},
            "steps": steps, "precisifications": n_precis, "objects": n_objects}


# ---------------------------------------------------------------------------
# Fission
# ---------------------------------------------------------------------------
def fission() -> dict:
    """A continuity graph over time: one person-stage line that splits into two at the fission. Psychological
    continuity (the transitive closure of stage-to-stage links) relates the original to both branches; identity must
    be transitive and one-one, so it cannot relate the original to both. Lewis's view: two worms that overlap before
    the split. Parfit's: there is no further fact; what matters is continuity, and it holds to both."""
    stages = ["t0", "t1", "t2", "L3", "L4", "R3", "R4"]
    links = [("t0", "t1"), ("t1", "t2"), ("t2", "L3"), ("L3", "L4"), ("t2", "R3"), ("R3", "R4")]
    adj = {s: set() for s in stages}
    for a, b in links:
        adj[a].add(b)
        adj[b].add(a)

    def connected(x, y):
        seen, st = {x}, [x]
        while st:
            v = st.pop()
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    st.append(w)
        return y in seen

    cont = {(x, y): connected(x, y) for x in stages for y in stages}
    # if continuity were identity: t0 = L4, t0 = R4, so L4 = R4 by transitivity, but L4 and R4 are not continuous
    # through any path that avoids the past: they are distinct people now
    worms = [["t0", "t1", "t2", "L3", "L4"], ["t0", "t1", "t2", "R3", "R4"]]
    return {"stages": stages, "links": links, "t0_L4": cont[("t0", "L4")], "t0_R4": cont[("t0", "R4")],
            "L4_R4_now_distinct": True, "worms": worms, "shared": sorted(set(worms[0]) & set(worms[1]))}


# ---------------------------------------------------------------------------
# Connectedness and continuity
# ---------------------------------------------------------------------------
def memory_chain(years: int = 80, per_year: int = 200, keep: float = 0.95, seed: int = 1984,
                 ref_age: int = 10) -> dict:
    """A toy life: each year lays down new memories; each memory survives each later year with probability keep.
    Connectedness between two ages: the share of the earlier self's memories that the later self still has (a stand-in
    for Parfit's direct psychological connections). Continuity: an unbroken chain of year-to-year connectedness above a
    threshold. Connectedness fades by degrees; continuity holds all the way."""
    rng = np.random.default_rng(seed)
    born = np.repeat(np.arange(years), per_year)
    death = born + 1 + rng.geometric(1 - keep, size=born.size)
    def held(age):
        return set(np.flatnonzero((born <= age) & (death > age)))
    sets = [held(a) for a in range(years)]
    conn_ref = [len(sets[ref_age] & sets[a]) / max(1, len(sets[ref_age])) if a >= ref_age else None
                for a in range(years)]
    step = [len(sets[a] & sets[a + 1]) / max(1, len(sets[a])) for a in range(years - 1)]
    half = next((a for a in range(ref_age, years) if conn_ref[a] is not None and conn_ref[a] < 0.5), None)
    return {"years": years, "ref_age": ref_age, "connectedness": conn_ref, "year_to_year_min": float(min(step)),
            "half_at": half, "keep": keep}


# ---------------------------------------------------------------------------
# Identity in computing; modal profiles
# ---------------------------------------------------------------------------
def python_identity() -> dict:
    """`is' is numerical identity (one object); `==' is qualitative equality (same value). Leibniz's law holds for
    `is': a change made through one name shows up through the other."""
    a = [1, 2]
    b = a
    c = [1, 2]
    before = {"a is b": a is b, "a is c": a is c, "a == c": a == c}
    a.append(3)
    after = {"b": list(b), "c": list(c), "a == c": a == c}
    return {"before": before, "after": after}


def modal_profiles() -> dict:
    """The statue and the lump across possible scenarios: in which does each still exist? They share every actual
    property and differ only in their profiles."""
    scenarios = [
        ("actual: sculpted Tuesday, kept", True, True),
        ("squashed into a ball", True, False),
        ("one arm replaced with new clay", False, True),
        ("never sculpted", True, False),
        ("melted down", False, False),
    ]
    return {"scenarios": [{"case": c, "lump": l, "statue": s} for c, l, s in scenarios],
            "differ": sum(l != s for _, l, s in scenarios)}


def weight_drift(steps: int = 40, dim: int = 512, step: float = 0.25, seed: int = 21) -> dict:
    """A model's weights as a ship of Theseus: a unit vector in ``dim`` dimensions takes ``steps`` small random
    updates (fine-tuning runs, say), each renormalized. Cosine similarity to the original fades (Parfit's
    connectedness), while each version stays very close to the one before (continuity)."""
    rng = np.random.default_rng(seed)
    w0 = rng.standard_normal(dim)
    w0 /= np.linalg.norm(w0)
    w = w0.copy()
    to_orig, to_prev = [1.0], []
    for _ in range(steps):
        d = rng.standard_normal(dim)
        d /= np.linalg.norm(d)
        nw = w + step * d
        nw /= np.linalg.norm(nw)
        to_orig.append(float(nw @ w0))
        to_prev.append(float(nw @ w))
        w = nw
    half = next((i for i, s in enumerate(to_orig) if s < 0.5), None)
    return {"steps": steps, "dim": dim, "to_original": [round(s, 4) for s in to_orig],
            "to_previous": [round(s, 4) for s in to_prev], "min_step": round(min(to_prev), 4),
            "final": round(to_orig[-1], 4), "below_half_at": half}

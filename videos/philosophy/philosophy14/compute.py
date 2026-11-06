"""Precompute everything in Part 14 of *Philosophy, Built* ("Changing Your Mind").

    python -m videos.philosophy.philosophy14.compute            # everything missing (a few seconds)

Items:
    moves       expansion, revision and contraction on the detective's ranking; the book and the magazine
    agm         the AGM revision postulates checked for four operators; Satoh's failure of subexpansion
    spheres     Grove's spheres for a three-atom ranking; revisions; partial meet contraction; Levi and Harper;
                entrenchment
    iterated    Darwiche--Pearl postulates for four operators; the red bird that is forgotten
    gardenfors  the impossibility theorem on three worlds
    counter     five counterfactual countermodels; Stalnaker's conditional excluded middle
    trivial     Lewis's triviality on three worlds; the exhaustive search; imaging; the triviality Price List
    mcgee       McGee's 1980 election
    defaults    Reiter's extensions: Tweety and the Nixon diamond
    systemz     System Z on the penguins; the world ranking; KLM rules on two models
    argue       Dung's semantics on five frameworks
    editing     a toy knowledge base with background rules: AGM revision versus a local edit
    explain     a loan classifier's counterfactual explanations under two distances
    yale        the Yale shooting problem: the intended and the anomalous minimal models
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import argue as G
from explainer.philosophy.reasoner import cond as C
from explainer.philosophy.reasoner import prop
from explainer.philosophy.reasoner import revision as R

CACHE = Cache("philosophy14")
load = CACHE.load

# the triviality cluster: each claim an atom; together they are inconsistent
TRIVIAL = [("T1", r"$P(A \to C) = P(C \mid A)$ \ for every credence", "a"),
           ("T2", r"rational credences stay rational when conditioned", "b"),
           ("T3", r"`if $A$, $C$' is true or false at each world", "c"),
           ("T4", r"some credence has $P(C \mid A) \neq P(C)$ \ (non-trivial)", "d")]

DETECTIVE = ("b", "m")                     # b: the butler did it; m: the maid did it
DETECTIVE_RANK = {"b~m": 0, "bm": 0, "~bm": 1, "~b~m": 2}


def compute_moves() -> dict:
    atoms = DETECTIVE
    rank = DETECTIVE_RANK
    notb = R.P("~b", atoms)
    b = R.P("b", atoms)
    return {"rank": rank, "beliefs": sorted(R.beliefs(rank)),
            "expand ~m": sorted(R.expand(R.beliefs(rank), R.P("~m", atoms))),
            "revise ~b": sorted(R.revise(rank, notb)), "contract b": sorted(R.contract(rank, b)),
            "book": R.book_and_magazine()}


def compute_agm() -> dict:
    t = R.postulate_table()
    return {"table": {k: {p: v["holds"] for p, v in row.items()} for k, row in t.items()},
            "satoh": R.satoh_example(), "postulates": [list(p) for p in R.POSTULATES]}


def compute_spheres() -> dict:
    atoms = ("p", "q", "r")
    K = R.P("p & q & r", atoms)
    rank = {w: (0 if w in K else min(R.hamming(w, k, atoms) for k in K)) for w in R.worlds(atoms)}
    revs = {f: sorted(R.revise(rank, R.P(f, atoms))) for f in ("~p", "~p | ~q", "~p & ~q", "~r")}
    W = R.worlds(atoms)
    A = R.P("p", atoms)
    rem = R.remainders(K, A, W)
    return {"rank": rank, "spheres": [sorted(s) for s in R.spheres(rank)], "revisions": revs,
            "contract p": sorted(R.contract(rank, A)), "remainders": [sorted(x) for x in rem],
            "maxichoice": sorted(R.partial_meet(K, A, W, lambda xs: xs[:1])),
            "full meet": sorted(R.partial_meet(K, A, W, lambda xs: xs)),
            "identities": R.identities_hold(rank),
            "entrenchment": {f: R.entrenchment(rank, R.P(f, atoms)) for f in ("p", "p | q", "p | q | r", "p & q")}}


def compute_iterated() -> dict:
    t = R.dp_table()
    return {"table": {k: {p: v["holds"] for p, v in row.items()} for k, row in t.items()},
            "demo": {k: {kk: vv for kk, vv in v.items() if kk != "rank"} | {"rank": v["rank"]}
                     for k, v in R.iterate_demo().items()},
            "dp": [list(x) for x in R.DP]}


def compute_gardenfors() -> dict:
    return R.gardenfors()


def compute_counter() -> dict:
    out = {}
    for k, v in C.classic_models().items():
        M = v["model"]
        rows = []
        for w in M.facts:
            if w == M.actual:
                continue
            rows.append({"world": w, "dist": M.near[M.actual][w], "facts": M.facts[w]})
        out[k] = {"premises": v["premises"], "conclusion": v["conclusion"], "gloss": list(v["gloss"]),
                  "premises_hold": v["premises_hold"], "conclusion_holds": v["conclusion_holds"],
                  "material_valid": v["material_valid"], "worlds": sorted(rows, key=lambda r: r["dist"]),
                  "stalnaker": v["stalnaker_model"]}
    return {"models": out, "cem_stalnaker": C.cem_stalnaker()}


def compute_trivial() -> dict:
    claims = {k: prop.parse(f) for k, _, f in TRIVIAL}
    res = prop.mus_mcs(claims, [prop.parse("(a & b & c & d) -> F"), prop.parse("~F")])
    return {"proof": C.lewis_proof(), "search4": C.triviality_search(),
            "search3": C.triviality_search(("AC", "A~C", "~A~C")),
            "trivial": C.triviality_search(("AC", "~AC", "~A~C")), "imaging": C.imaging_demo(),
            "claims": [{"key": k, "text": t} for k, t, _ in TRIVIAL],
            "mus": [sorted(x) for x in res["mus"]], "mcs": [sorted(x) for x in res["mcs"]]}


def compute_mcgee() -> dict:
    return C.mcgee()


def compute_defaults() -> dict:
    return {"tweety": G.tweety(), "nixon": G.nixon()}


def compute_systemz() -> dict:
    atoms = ("b", "f", "p", "w", "r")
    pen = G.penguins()
    rank = G.z_rank([tuple(d) for d in pen["defaults"]], atoms)
    # the worlds that matter for the picture: r false
    shown = {w: k for w, k in rank.items() if w.endswith("~r")}
    return {"penguins": pen, "rank": shown, "klm": {k: {r: v["holds"] for r, v in row.items()}
                                                   for k, row in G.klm_table().items()},
            "klm_cex": {k: {r: v["counterexample"] for r, v in row.items() if not v["holds"]}
                        for k, row in G.klm_table().items()}}


def compute_argue() -> dict:
    out = {}
    for k, af in G.EXAMPLES.items():
        out[k] = {"args": af.args, "attacks": sorted(af.att), **af.summary()}
    return out


def compute_editing() -> dict:
    """b: plays for Barcelona; p: plays for Paris; s: lives in Spain; f: lives in France. Rules: b -> s, p -> f,
    not both clubs, not both countries. Believed: b and s. Learn p."""
    atoms = ("b", "p", "s", "f")
    rules = R.P("(b -> s) & (p -> f) & ~(b & p) & ~(s & f)", atoms)
    W = R.worlds(atoms)
    start = next(w for w in rules if R.valuation(w, atoms) == {"b": True, "p": False, "s": True, "f": False})
    rank = {w: (R.hamming(w, start, atoms) if w in rules else 10 ** 9) for w in W}
    agm = sorted(R.revise(rank, R.P("p", atoms)))
    local = "~bp" + "s~f"                                  # flip the clubs, leave the rest
    return {"rules": sorted(rules), "start": start, "agm": agm, "agm_facts": [R.valuation(w, atoms) for w in agm],
            "local": local, "local_consistent": local in rules}


def compute_explain() -> dict:
    """Approve when 0.6 * income (in $k) + 3 * years employed - 45 >= 0. An applicant with $50k and 2 years is
    refused. The closest approvals, measuring income in steps of $10k and employment in years."""
    w = (6.0, 3.0)                                  # per $10k of income, per year of employment
    x = (5.0, 2.0)                                  # $50k, 2 years
    gap = 45 - (w[0] * x[0] + w[1] * x[1])          # how far below the line
    l2 = tuple(gap * wi / (w[0] ** 2 + w[1] ** 2) for wi in w)
    l1 = min(((gap / w[0], 0.0), (0.0, gap / w[1])), key=lambda d: abs(d[0]) + abs(d[1]))
    return {"weights": [0.6, 3.0, -45], "applicant": {"income_k": 50, "years": 2},
            "score": 0.6 * 50 + 3 * 2 - 45, "l2": {"income_k": 10 * l2[0], "years": l2[1]},
            "l1": {"income_k": 10 * l1[0], "years": l1[1]}}


def compute_yale() -> dict:
    """Hanks and McDermott (1986). Load at time 0, wait at 1, shoot at 2. A change of a fluent while waiting counts
    as an abnormality, and the shooting axiom makes a loaded shot abnormal for 'alive'; circumscription keeps the models whose set of abnormalities is minimal. Two
    survive: the intended one (the gun stays loaded and the shot kills) and the anomalous one (the gun mysteriously
    unloads while we wait, and Fred lives)."""
    import itertools as it
    models = []
    for loaded2, alive1, alive2 in it.product([True, False], repeat=3):
        alive0, loaded1 = True, True                   # Fred is alive; loading works
        alive3 = alive2 and not loaded2                # shooting a loaded gun kills
        changes = set()
        if alive1 != alive0:
            changes.add("alive during load")
        if loaded2 != loaded1:
            changes.add("loaded during wait")
        if alive2 != alive1:
            changes.add("alive during wait")
        if loaded2:                                    # the shooting axiom: a loaded shot is abnormal for 'alive'
            changes.add("alive at the shot")
        models.append({"loaded2": loaded2, "alive1": alive1, "alive2": alive2, "alive3": alive3,
                       "changes": sorted(changes)})
    minimal = [m for m in models if not any(set(o["changes"]) < set(m["changes"]) for o in models)]
    return {"minimal": minimal, "count": len(models)}


ITEMS = {"moves": compute_moves, "agm": compute_agm, "spheres": compute_spheres, "iterated": compute_iterated,
         "gardenfors": compute_gardenfors, "counter": compute_counter, "trivial": compute_trivial,
         "mcgee": compute_mcgee, "defaults": compute_defaults, "systemz": compute_systemz, "argue": compute_argue,
         "editing": compute_editing, "explain": compute_explain, "yale": compute_yale}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

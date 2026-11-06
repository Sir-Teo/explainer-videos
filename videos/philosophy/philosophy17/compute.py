"""Precompute everything in Part 17 of *Philosophy, Built* ("Cause").

    python -m videos.philosophy.philosophy17.compute            # everything missing (a few seconds)

Items:
    mill        the methods of agreement and difference on a table of cases; INUS conditions for a house fire
    preempt     Suzy and Billy, overdetermination: counterfactual dependence against the HP definition
    prob        Hesslow's pills (faithfulness fails); Simpson again
    berkson     collider bias among actors
    dsep        d-separation queries on the sprinkler graph
    adjust      back-door and front-door, exact and from a sample
    nonid       two models, one observational distribution, two causal effects
    calculus    the front-door formula derived rule by rule; the bow arc; M-bias
    ladder      the firing squad on three rungs; necessity and sufficiency
    actual      the modified Halpern--Pearl definition on six classic cases; the preemption Price List;
                degrees of responsibility in a vote
    markov      factorization; Yule's nonsense correlations; the CHSH bound
    pc          PC with an oracle and with 20,000 samples; the Markov equivalence class; LiNGAM's direction
    outcomes    the perfect doctor and every randomization; instrumental variables; difference in differences
    mind        Kim's exclusion argument as a Price List; Yablo's pigeon and proportionality
    industry    CUPED's variance cut; uplift targeting against response targeting; invariant prediction
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import causal as C
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy17")
load = CACHE.load


def compute_mill() -> dict:
    cases = [dict(spark=1, oxygen=1, fuel=1, wet=0, fire=1), dict(spark=0, oxygen=1, fuel=1, wet=0, fire=0),
             dict(spark=1, oxygen=1, fuel=1, wet=1, fire=0), dict(spark=1, oxygen=1, fuel=0, wet=0, fire=0),
             dict(spark=1, oxygen=1, fuel=1, wet=0, fire=1)]

    def fire(sc, fl, sp, ar):
        return int((sc and fl and not sp) or (ar and fl))
    names = ["short circuit", "flammable", "sprinkler", "arson"]
    pis = C.prime_implicants(fire, names)
    inus = {n: C.inus(fire, names, n, 0 if n == "sprinkler" else 1)["inus"] for n in names}
    return {"cases": cases, "methods": C.mill_difference(cases, "fire"), "prime_implicants": pis, "inus": inus}


def compute_preempt() -> dict:
    return {"cases": C.classic_cases()}


def compute_prob() -> dict:
    return C.hesslow()


def compute_berkson() -> dict:
    return C.berkson()


def compute_dsep() -> dict:
    g = C.DAG([("C", "S"), ("C", "R"), ("S", "W"), ("R", "W"), ("W", "L")])
    qs = [("S", "R", []), ("S", "R", ["C"]), ("S", "R", ["C", "W"]), ("S", "R", ["C", "L"]), ("C", "L", ["W"]),
          ("C", "W", ["S", "R"]), ("S", "L", ["W"])]
    return {"queries": [{"x": x, "y": y, "z": z, "dsep": g.dsep({x}, {y}, set(z))} for x, y, z in qs]}


def compute_adjust() -> dict:
    return {**C.adjustment_demo(), "sample": C.simulate_adjustment()}


def compute_nonid() -> dict:
    return C.nonidentifiable()


def compute_calculus() -> dict:
    return {"derivation": C.frontdoor_derivation(), "mbias": C.m_bias()}


def compute_ladder() -> dict:
    return {"squad": C.firing_squad(), "pnps": C.pn_ps_demo()}


PREEMPT = [("P1", r"causation requires counterfactual dependence, \ or a chain of it", "a"),
           ("P2", r"Suzy's throw caused the shattering", "b"),
           ("P3", r"no chain of dependence links Suzy's throw to the shattering: \ Billy's rock would have done it",
            "c")]


def compute_actual() -> dict:
    claims = {k: prop.parse(f) for k, _, f in PREEMPT}
    res = prop.mus_mcs(claims, [prop.parse("(a & b) -> ~c")])
    return {"cases": C.classic_cases(), "claims": [{"key": k, "text": t} for k, t, _ in PREEMPT],
            "mus": [sorted(x) for x in res["mus"]], "mcs": [sorted(x) for x in res["mcs"]],
            "votes": [C.responsibility(a, b) for a, b in ((6, 5), (7, 4), (8, 3), (11, 0))]}


def compute_markov() -> dict:
    g = C.DAG([("C", "S"), ("C", "R"), ("S", "W"), ("R", "W"), ("W", "L")])
    params = sum(2 ** len(g.pa[v]) for v in g.nodes)
    return {"yule": C.yule_walks(), "chsh": C.chsh(), "params_factored": params,
            "params_full": 2 ** len(g.nodes) - 1}


def compute_pc() -> dict:
    return {**C.pc_demo(), "lingam": C.lingam_demo()}


def compute_outcomes() -> dict:
    return {"iv": C.instrumental(), "did": C.diff_in_diff(), "doctor": C.perfect_doctor()}


def compute_industry() -> dict:
    return {"cuped": C.cuped(), "uplift": C.uplift_demo(), "icp": C.icp_demo()}


KIM = [("K1", r"mental causation: \ some mental events cause physical events", "a"),
       ("K2", r"irreducibility: \ mental events are not physical events", "b"),
       ("K3", r"closure: \ every physical event that has a cause has a sufficient physical cause", "c"),
       ("K4", r"exclusion: \ no event has two distinct sufficient causes, \ unless it is overdetermined", "d"),
       ("K5", r"no systematic overdetermination: \ the mind does not double every cause", "e")]


def compute_mind() -> dict:
    claims = {k: prop.parse(f) for k, _, f in KIM}
    res = prop.mus_mcs(claims, [prop.parse("~(a & b & c & d & e)")])
    # Yablo's pigeon: trained to peck at red; shown scarlet. Which description is the proportional cause?
    shades = {"scarlet": "red", "crimson": "red", "maroon": "red", "navy": "blue", "sky": "blue"}
    peck = {s: int(c == "red") for s, c in shades.items()}
    shade_alts = [s for s in shades if s != "scarlet"]
    shade_diff = sum(peck[s] != peck["scarlet"] for s in shade_alts)
    color_alts = sorted({c for c in shades.values() if c != "red"})
    color_diff = sum(int(c == "red") != 1 for c in color_alts)
    return {"claims": [{"key": k, "text": t} for k, t, _ in KIM], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]],
            "pigeon": {"shade_alts": len(shade_alts), "shade_diff": shade_diff, "color_alts": len(color_alts),
                       "color_diff": color_diff}}


ITEMS = {"mill": compute_mill, "preempt": compute_preempt, "prob": compute_prob, "berkson": compute_berkson, "dsep": compute_dsep,
         "adjust": compute_adjust, "nonid": compute_nonid, "calculus": compute_calculus,
         "ladder": compute_ladder, "actual": compute_actual, "markov": compute_markov,
         "pc": compute_pc, "outcomes": compute_outcomes,
         "industry": compute_industry, "mind": compute_mind}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

"""Precompute everything in Part 27 of *Philosophy, Built* ("Sense and Reference").

    python -m videos.philosophy.philosophy27.compute            # everything missing (seconds)

Items:
    horse       Gongsun Long's white horse: identity against inclusion
    medians     Frege's medians: three descriptions, one point
    russell     Russell's descriptions, both scopes of negation, in four models
    strawson    Strawson's truth-value gaps against Russell's values
    incomplete  an incomplete description, with and without domain restriction
    donnellan   referential and attributive uses at a party
    rigid       Kripke: rigid names and non-rigid descriptions across worlds
    twin        Twin Earth: same inner state, different extension
    burge       Burge's arthritis: the same patient in two communities
    twod        two-dimensional matrices for three sentences
    kaplan      Kaplan's character and content for 'I am here now'
    tarski      a T-sentence derived step by step
    foster      Foster's problem: two truth theories that agree in the actual world
    beta        beta reduction of 'every student smokes'
    fragment    the Heim--Kratzer fragment: every node of every tree
    gq          conservativity and monotonicity of seven quantifiers
    conscount   the 512 conservative determiners among 65 536
    ef          Ehrenfeucht--Fraisse games: 'most' is not first-order
    omni        propositions as sets of worlds: logical omniscience
    donkey      dynamic predicate logic against first-order translations
    sql         the fragment compiled to SQL and run in sqlite
    nli         an inference suite with computed gold labels
    frege       the Price List for Frege's puzzle
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import prop
from explainer.philosophy.reasoner import semantics as M

CACHE = Cache("philosophy27")
load = CACHE.load

FREGE = [
    ("N", r"a name's meaning is just its referent"),
    ("S", r"co-referring names can be swapped without changing a sentence's truth"),
    ("L", r"Lois believes that Superman flies, \ and does not believe that Clark Kent flies"),
]


def compute_frege():
    claims = {k: prop.Var(k) for k, _ in FREGE}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in FREGE]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in FREGE], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_fragment():
    out = M.fragment()
    for v in out.values():
        for n in v["nodes"]:
            if isinstance(n["value"], set):
                n["value"] = sorted(n["value"])
    return out


ITEMS = {"horse": M.white_horse, "medians": M.medians, "russell": M.descriptions, "strawson": M.strawson,
         "donnellan": M.donnellan, "incomplete": M.incomplete, "rigid": M.rigidity, "twin": M.twin, "burge": M.burge, "twod": M.two_d, "kaplan": M.kaplan,
         "tarski": M.t_theory, "foster": M.foster, "beta": M.beta_demo, "fragment": compute_fragment,
         "gq": M.quantifiers, "conscount": M.count_conservative, "ef": M.ef_most, "omni": M.omniscience,
         "donkey": M.donkeys, "sql": M.sql_check, "nli": M.nli_suite, "frege": compute_frege}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

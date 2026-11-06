"""Precompute everything in Part 34 of *Philosophy, Built* ("Games and the Social Contract").

    python -m videos.philosophy.philosophy34.compute            # everything missing (seconds)

Items:
    equilibria    Nash equilibria of five 2x2 games, by support enumeration
    br            best-response correspondences of the battle of the sexes
    commons       the commons as a Cournot game, for 1 to 100 herders
    public        a public goods game with and without graduated sanctions
    stag          the stag hunt: basins and stochastic stability
    centipede     the centipede: backward induction and noisy best response
    correlated    correlated equilibrium of chicken, by linear programming
    shadow        every deterministic memory-one strategy against grim and tit for tat, by discount factor
    folk          the folk theorem: the patience each cyclic plan needs under grim trigger
    tournament    Axelrod's tournament, with and without noise; the ecological simulation
    zd            Press and Dyson's zero-determinant strategies, checked
    evolution     evolution with rare mutations among six memory-one strategies
    demand        Skyrms's Nash demand game: basins on the simplex
    assort        the fair basin as encounters become correlated
    bargaining    Nash, Kalai-Smorodinsky and Rubinstein
    shapley       the glove game, Harsanyi dividends, SHAP on a tiny model
    auctions      second price, first price, revenue equivalence, Myerson's reserve
    gsp           sponsored search: GSP against VCG
    matching      deferred acceptance on five students and five schools
    tetrad        the Price List for the prisoner's dilemma
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import games as G
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy34")
load = CACHE.load

TETRAD = [
    ("SELF", r"each player chooses what is best for herself"),
    ("DOM", r"in a one-shot dilemma, \ defecting is best whatever the other does"),
    ("PARETO", r"mutual cooperation is better for both than mutual defection"),
    ("COLL", r"if all choose rationally, \ they cannot all do worse than they could"),
]


def compute_tetrad():
    # SELF and DOM say both defect; PARETO says that leaves both worse off; COLL says rational choice cannot do that
    claims = {k: prop.Var(k) for k, _ in TETRAD}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in TETRAD]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in TETRAD], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_tournament():
    t = G.tournament()
    t["ecology"] = {k: G.ecological(v["matrix"]) for k, v in t["by_noise"].items()}
    return t


ITEMS = {"equilibria": G.equilibria_table, "br": G.best_responses, "commons": G.commons, "public": G.public_goods,
         "stag": G.stag_hunt, "centipede": G.centipede, "correlated": G.correlated_chicken,
         "shadow": G.shadow, "folk": G.folk_theorem,
         "tournament": compute_tournament, "zd": G.zero_determinant, "evolution": G.evolution_rare_mutation,
         "demand": G.nash_demand, "assort": G.nash_demand_assort, "bargaining": G.bargaining,
         "shapley": G.shapley_examples, "auctions": G.auctions, "gsp": G.gsp_vcg, "matching": G.gale_shapley,
         "tetrad": compute_tetrad}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

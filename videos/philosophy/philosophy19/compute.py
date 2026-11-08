"""Precompute everything in Part 19 of *Philosophy, Built* ("Life").

    python -m videos.philosophy.philosophy19.compute            # everything missing (under a minute)

Items:
    paley       design against selection as likelihoods (illustrative probabilities)
    breeder     selection with and without heredity; the breeder's equation
    price       Price's identity on a simulated population of birds
    hawkdove    the hawk-dove game: the mixed ESS and replicator flows
    rps         rock-paper-scissors cycles on the simplex
    kin         Hamilton's rule from Price, and simulated altruism above and below rb = c
    levels      the multilevel Price decomposition: Simpson's paradox in two groups
    function    the swampman Price List for etiological functions
    code        the genetic code's redundancy in bits; silent mutations
    tree        Fitch parsimony on a vertebrate character matrix
    axelrod     a small iterated prisoner's dilemma tournament
    lenia       a Lenia glider condensing from noise, with a 300-frame film
    entropy     entropy budgets for a resting body and for the Earth
    lifedef     five definitions of life against seven cases
    conway      Conway's glider: period 4, shift (1, 1)
    eye         Nilsson and Pelger's clock for the camera eye
    drift       Wright-Fisher drift; fixation probabilities against Kimura's formula
    fisher      Fisher's fundamental theorem as the Price equation with z = w
    signals     Lewis-Skyrms signalling games learned by urn reinforcement
    relatedness exact relatedness, diploid and haplodiploid
    parity      mutual information of gene and diet under three backgrounds
    shadow      tit for tat against always defect in a game that continues with probability w
"""

from __future__ import annotations

import json

from explainer.ai.cache import Cache
from explainer.cache_lock import locked_item
from explainer.philosophy.reasoner import evo as Ev
from explainer.philosophy.reasoner import prop

def _rps_current(path) -> bool:
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError):
        return False
    return (isinstance(data, dict) and data.get("schema") == 2 and
            all(isinstance(data.get(key), dict) and data[key].get("eps") == eps
                for key, eps in (("neutral", 0.0), ("in", -0.3), ("out", 0.3))))


class _EvolutionCache(Cache):
    """Upgrade legacy RPS caches whose inward and outward branches were reversed."""

    @locked_item(lambda self, name: self.path(name))
    def load(self, name):
        if name == "rps" and not _rps_current(self.path(name)):
            self.save(name, compute_rps())
        return super().load(name)


CACHE = _EvolutionCache("philosophy19")


def load(name):
    return CACHE.load(name)


def cache_current(name):
    return name != "rps" or _rps_current(CACHE.path(name))


def compute_paley() -> dict:
    return Ev.paley_likelihoods()


def compute_breeder() -> dict:
    return Ev.breeder()


def compute_price() -> dict:
    return Ev.price_check()


def compute_hawkdove() -> dict:
    return Ev.hawk_dove()


def compute_rps() -> dict:
    return {"schema": 2, "neutral": Ev.rps(eps=0.0), "in": Ev.rps(eps=-0.3), "out": Ev.rps(eps=0.3)}


def compute_kin() -> dict:
    sims = [Ev.hamilton_sim(r, b, c) for r, b, c in ((0.5, 3, 1), (0.25, 3, 1), (0.125, 10, 1), (0.125, 6, 1))]
    return {"sims": sims, "price": Ev.hamilton_from_price(0.5, 3, 1)}


def compute_levels() -> dict:
    return Ev.multilevel()


SWAMP = [("F1", r"a trait's function is the effect that explains why it is there \ (selection history)", "a"),
         ("F2", r"Swampman's heart, \ made by lightning, \ has the function of pumping blood", "b"),
         ("F3", r"Swampman's heart has no selection history", "c")]


def compute_function() -> dict:
    claims = {k: prop.parse(f) for k, _, f in SWAMP}
    res = prop.mus_mcs(claims, [prop.parse("(a & c) -> ~b")])
    return {"claims": [{"key": k, "text": t} for k, t, _ in SWAMP], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_code() -> dict:
    return Ev.code_information()


def compute_tree() -> dict:
    return Ev.parsimony_demo()


def compute_axelrod() -> dict:
    return Ev.axelrod_mini()


def compute_lenia() -> dict:
    return Ev.lenia_glider(steps=1500, frames=7, movie=(0, 5, 300))


def compute_entropy() -> dict:
    return Ev.entropy_budget()


def compute_lifedef() -> dict:
    return Ev.life_definitions()


def compute_conway() -> dict:
    return Ev.conway_glider()


def compute_eye() -> dict:
    return Ev.eye_generations()


def compute_drift() -> dict:
    return Ev.wright_fisher()


def compute_fisher() -> dict:
    return Ev.fisher_theorem()


def compute_signals() -> dict:
    return {"two": Ev.lewis_signalling(n=2, runs=200), "three": Ev.lewis_signalling(n=3, runs=200)}


def compute_relatedness() -> dict:
    return Ev.relatedness_table()


def compute_parity() -> dict:
    return Ev.parity_demo()


def compute_shadow() -> dict:
    return Ev.shadow()


ITEMS = {"paley": compute_paley, "breeder": compute_breeder, "price": compute_price, "hawkdove": compute_hawkdove,
         "rps": compute_rps, "kin": compute_kin, "levels": compute_levels, "function": compute_function, "code": compute_code, "tree": compute_tree,
         "axelrod": compute_axelrod, "lenia": compute_lenia,
         "entropy": compute_entropy, "lifedef": compute_lifedef, "conway": compute_conway,
         "eye": compute_eye, "drift": compute_drift, "fisher": compute_fisher, "signals": compute_signals,
         "relatedness": compute_relatedness, "parity": compute_parity, "shadow": compute_shadow}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

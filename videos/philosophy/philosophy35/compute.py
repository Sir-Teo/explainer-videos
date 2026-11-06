"""Precompute everything in Part 35 of *Philosophy, Built* ("The Right and the Good").

    python -m videos.philosophy.philosophy35.compute            # everything missing (seconds)

Items:
    felicific     Bentham's ledger for two acts
    harsanyi      nonlinear welfare functions against vNM and Pareto; the possibility frontier
    distribution  five distributions under five views; Gini and Atkinson; levelling down
    promises      a world of promises with a share of lying promisers
    maxims        universalizability: hits, false positives, a false negative
    paradox       the paradox of deontology, and consequentializing it
    trolley       trolley cases, utilitarianism and double effect
    transmitter   Scanlon's Transmitter Room: full, individualist and partial aggregation
    uncertainty   moral uncertainty: expected choiceworthiness and a parliament
    tetrad        the Price List for the trolley cases
    levels        rules against acts: a noisy act utilitarian, a rule follower, a two-level thinker
    monster       Nozick's utility monster under three views
    pond          Singer's pond with logarithmic welfare; full and partial compliance
    taurek        Taurek's numbers: three policies, each person's chance
    particularism the best fixed-weight rule of reasons against principles with defeaters
    adaptive      sour grapes: desire satisfaction recovers as options close; capability does not
    humanity      the formula of humanity as a consent test, on seven acts
    moralinfo     the value of learning which moral theory is true, by credence
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import ethics as E
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy35")
load = CACHE.load

TETRAD = [
    ("SWITCH", r"turning the trolley onto the one is permissible"),
    ("PUSH", r"pushing the man off the footbridge is impermissible"),
    ("ONLY", r"the cases differ only in that the one is used as a means"),
    ("NODIFF", r"harming as a means rather than as a side effect makes no moral difference"),
]


def compute_tetrad():
    claims = {k: prop.Var(k) for k, _ in TETRAD}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in TETRAD]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in TETRAD], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]],
            # PhilPapers Survey 2020 (Bourget and Chalmers 2023), target faculty, accept or lean towards
            "survey": {"switch": 0.634, "don't switch": 0.133, "push": 0.220, "don't push": 0.562,
                       "virtue ethics": 0.370, "deontology": 0.321, "consequentialism": 0.306,
                       "experience machine: no": 0.769, "experience machine: yes": 0.130}}


ITEMS = {"felicific": E.felicific, "harsanyi": E.harsanyi, "distribution": E.distributions,
         "promises": E.promise_world, "maxims": E.maxims, "paradox": E.deontology_paradox, "trolley": E.trolley,
         "transmitter": E.transmitter, "uncertainty": E.moral_uncertainty, "tetrad": compute_tetrad,
         "levels": E.two_level, "monster": E.utility_monster, "pond": E.pond, "taurek": E.taurek,
         "particularism": E.particularism, "adaptive": E.adaptive_preferences,
         "humanity": E.humanity_test, "moralinfo": E.moral_information}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

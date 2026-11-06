"""Precompute everything in Part 33 of *Philosophy, Built* ("Rational Choice").

    python -m videos.philosophy.philosophy33.compute            # everything missing (seconds)

Items:
    pump          a money pump for cyclic preferences
    revealed      revealed preference: GARP and Afriat's efficiency index for two shoppers
    stpete        St Petersburg: simulated averages, Bernoulli's log utility
    triangle      the Marschak-Machina triangle: parallel expected-utility lines
    allais        Allais: no utility fits the common choices; risk-weighted utility does
    ellsberg      Ellsberg: no probability fits; maxmin expected utility does
    prospect      prospect theory: value, weights, the fourfold pattern
    framing       the Asian disease problem, valued by prospect theory
    kelly         the Kelly criterion: growth rates and 1000 simulated paths
    pasadena      the Pasadena game's rearrangements
    newcomb       Newcomb's problem with a predictor of any accuracy
    twins         the prisoner's dilemma against a near-copy (Lewis 1979)
    lesion        the smoking lesion: evidential against causal expected utility
    damascus      death in Damascus: no ratifiable choice
    button        the psychopath button: causal decision theory's counterexample
    hitchhiker    Parfit's hitchhiker: acts against policies
    ulysses       Ulysses and the sirens: naive, sophisticated, resolute
    discount      exponential against hyperbolic discounting: a preference reversal
    good          Good's theorem on 2000 random problems; a risk-weighted counterexample
    voi           Good's theorem drawn: the convex envelope and one test
    envelopes     the two envelopes under proper and Broome priors
    tetrad        the Price List for Newcomb's problem
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import decision as D
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy33")
load = CACHE.load

TETRAD = [
    ("DOM", r"if an act is better whatever the state, \ choose it"),
    ("EV", r"choose the act with the greatest expected value, \ given the act"),
    ("REL", r"the predictor is reliable: \ one-boxers almost always get the million"),
    ("FIX", r"the boxes' contents are fixed before you choose"),
]


def compute_tetrad():
    # DOM with FIX says take both; EV with REL says take one: the four together recommend incompatible acts
    claims = {k: prop.Var(k) for k, _ in TETRAD}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in TETRAD]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in TETRAD], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]],
            # PhilPapers Survey 2020 (Bourget and Chalmers 2023), target faculty, accept or lean towards
            "survey": {"two boxes": 0.390, "one box": 0.312}}


ITEMS = {"pump": D.money_pump, "revealed": D.revealed_preference, "framing": D.asian_disease, "twins": D.twin_pd,
         "stpete": D.st_petersburg, "triangle": D.triangle_lines, "allais": D.allais,
         "ellsberg": D.ellsberg, "prospect": D.prospect, "kelly": D.kelly, "pasadena": D.pasadena,
         "newcomb": D.newcomb, "lesion": D.smoking_lesion, "damascus": D.damascus,
         "button": D.psychopath_button, "hitchhiker": D.hitchhiker,
         "ulysses": D.ulysses, "discount": D.discounting, "good": D.good_theorem, "voi": D.voi_example, "envelopes": D.two_envelopes, "tetrad": compute_tetrad}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

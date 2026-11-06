"""Precompute everything in Part 13 of *Philosophy, Built* ("Degrees of Belief").

    python -m videos.philosophy.philosophy13.compute            # everything missing (a few seconds)

Items:
    dutch       Dutch books found by linear programming: A and not-A at 0.6 each; A, B, A-and-B, A-or-B
    accuracy    incoherent credences and their projections onto the simplex, in two and three dimensions
    scoring     expected penalty curves for four rules at credence 0.7; which report each rule rewards
    forecast    four synthetic forecasters on 2,000 events: Brier and log scores, calibration
    update      Bayes on a medical test; Lewis's diachronic book; Jeffrey's cloth by candlelight
    maxent      Jaynes's Brandeis dice: the maximum-entropy die with mean 4.5
    bertrand    three random-chord ensembles, simulated; van Fraassen's cube factory
    dilation    a sharp coin, a vague proposition, and a credence that dilates from 1/2 to [0, 1]
    lottery     the lottery and the preface; the lottery triad as a Price List; Leitgeb's stable sets
    beauty      Sleeping Beauty, simulated 100,000 times
    doomsday    the Doomsday argument under SSA and SIA; the presumptuous philosopher
    bayesnet    rain, sprinkler, wet grass: exact inference by enumeration, and the size of the joint table
"""

from __future__ import annotations

import itertools

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import credence as Cr
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy13")
load = CACHE.load

LOTTERY = [("L1", r"a credence of 0.99 or more suffices for belief", "a"),
           ("L2", r"rational belief is closed under conjunction", "b"),
           ("L3", r"never believe what you know to be false", "c")]


def compute_dutch() -> dict:
    W = ["w1", "w2"]
    two = Cr.dutch_book(W, {"A": {"w1"}, "notA": {"w2"}}, {"A": 0.6, "notA": 0.6})
    W3 = ["AB", "A~B", "~AB", "~A~B"]
    props = {"A": {"AB", "A~B"}, "B": {"AB", "~AB"}, "A&B": {"AB"}, "AvB": {"AB", "A~B", "~AB"}}
    cred = {"A": 0.5, "B": 0.5, "A&B": 0.4, "AvB": 0.5}
    four = Cr.dutch_book(W3, props, cred)
    fixed = Cr.dutch_book(W3, props, {"A": 0.5, "B": 0.5, "A&B": 0.25, "AvB": 0.75})
    return {"two": two, "four": four, "four_cred": cred, "fixed_coherent": fixed is None}


def compute_accuracy() -> dict:
    return {"two": Cr.dominance([0.6, 0.6]), "two_b": Cr.dominance([0.8, 0.5]),
            "three": Cr.dominance([0.5, 0.4, 0.3]), "three_b": Cr.dominance([0.2, 0.2, 0.3])}


def compute_scoring() -> dict:
    p = 0.7
    qs = [i / 100 for i in range(1, 100)]
    curves = {r: [[q, Cr.expected_score(r, q, p)] for q in qs] for r in ("brier", "log", "spherical", "linear")}
    return {"p": p, "curves": curves, "best": {r: Cr.best_report(r, p) for r in curves}}


def compute_forecast() -> dict:
    return Cr.forecasters()


def compute_update() -> dict:
    prev, sens, fpr = 0.01, 0.9, 0.09
    post = prev * sens / (prev * sens + (1 - prev) * fpr)
    j = Cr.jeffrey(Cr.JEFFREY_CLOTH["prior"], Cr.JEFFREY_CLOTH["post"], Cr.JEFFREY_CLOTH["sold"])
    return {"test": {"prevalence": prev, "sensitivity": sens, "false_positive": fpr, "posterior": post,
                     "per_1000": {"sick_pos": prev * sens * 1000, "well_pos": (1 - prev) * fpr * 1000}},
            "diachronic": Cr.diachronic_book(0.5, 0.6, 0.4), "jeffrey": {**Cr.JEFFREY_CLOTH, **j}}


def compute_maxent() -> dict:
    return {"mean": 4.5, "p": Cr.maxent_die(4.5), "uniform_mean": 3.5}


def compute_bertrand() -> dict:
    return {"chords": Cr.bertrand(100000, keep=250), "cubes": Cr.cube_factory()}


def compute_dilation() -> dict:
    return Cr.dilation(11)


def compute_lottery() -> dict:
    claims = {k: prop.parse(f) for k, _, f in LOTTERY}
    res = prop.mus_mcs(claims, [prop.parse("(a & b & c) -> F"), prop.parse("~F")])
    probs = {"w1": 0.54, "w2": 0.34, "w3": 0.10, "w4": 0.02}
    return {"lottery": Cr.lottery(), "preface": Cr.preface(), "claims": [{"key": k, "text": t} for k, t, _ in LOTTERY],
            "mus": [sorted(x) for x in res["mus"]], "mcs": [sorted(x) for x in res["mcs"]],
            "stable": {"probs": probs, "sets": Cr.stable_sets(probs)}}


def compute_beauty() -> dict:
    return Cr.sleeping_beauty(100000)


def compute_doomsday() -> dict:
    return Cr.doomsday()


def compute_bayesnet() -> dict:
    """P(rain) = 0.2; P(sprinkler | rain) = 0.01, P(sprinkler | no rain) = 0.4; P(wet | s, r): 0.99, 0.9, 0.8, 0."""
    pr = 0.2
    ps = {True: 0.01, False: 0.4}
    pw = {(True, True): 0.99, (True, False): 0.9, (False, True): 0.8, (False, False): 0.0}
    joint = {}
    for r, s_, w in itertools.product([True, False], repeat=3):
        p = (pr if r else 1 - pr) * (ps[r] if s_ else 1 - ps[r]) * (pw[(s_, r)] if w else 1 - pw[(s_, r)])
        joint[(r, s_, w)] = p
    pw_ = sum(p for (r, s_, w), p in joint.items() if w)
    prw = sum(p for (r, s_, w), p in joint.items() if w and r) / pw_
    return {"p_rain_given_wet": prw, "p_wet": pw_, "table_sizes": [[n, 2 ** n] for n in (3, 10, 20, 30, 50)]}


ITEMS = {"dutch": compute_dutch, "accuracy": compute_accuracy, "scoring": compute_scoring,
         "forecast": compute_forecast, "update": compute_update, "maxent": compute_maxent,
         "bertrand": compute_bertrand, "dilation": compute_dilation, "lottery": compute_lottery,
         "beauty": compute_beauty, "doomsday": compute_doomsday, "bayesnet": compute_bayesnet}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

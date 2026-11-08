"""Precompute everything in Part 36 of *Philosophy, Built* ("Weighing Lives").

    python -m videos.philosophy.philosophy36.compute            # everything missing (seconds)

Items:
    sequence      Parfit's sequence A, B, ..., Z under five axiologies
    addition      the mere addition paradox, step by step
    vrc           the very repugnant conclusion on the total view
    tetrad        the Price List for the repugnant conclusion
    arrhenius     five axiologies against six conditions, counterexamples found by search
    nonidentity   Parfit's depletion case
    ramsey        the Ramsey rule with Stern's and Nordhaus's parameters; Weitzman's declining rate
    xrisk         the value of reducing extinction risk, constant risk against a time of perils
    fanatic       a chain of ever longer shots under three decision rules
    infinite      infinite streams: catching up, and the Basu-Mitra construction
    cea           cost-effectiveness over 200 toy interventions
    vsl           the value of a statistical life from a wage-risk trade-off
    neutrality    Broome's argument against the intuition of neutrality
    policy        one climate policy under Stern's and Nordhaus's discount rates
    three         Parfit's three outcomes: peace, 99%, 100%
    qaly          one course of treatment, three patients, three weightings
    sadism        the sadistic conclusion on a critical-level view
    scope         scope insensitivity: the birds (cited)
    hazard        Stern's pure time preference read as a chance of extinction
    benign        the benign addition, under five views
    weights       a toy of expected moral weights across kinds of being
    hmv           Meacham's harm-minimizing view on depletion and on A against Z
    transfer      the value of a statistical life transferred across incomes
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import population as Pop
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy36")
load = CACHE.load

# Desvousges et al. (1993), as reported by Kahneman, Ritov and Schkade (1999): mean willingness to pay to save
# migrating birds from oil ponds, by the number of birds
SCOPE = {"birds": [2000, 20000, 200000], "dollars": [80, 78, 88]}

TETRAD = [
    ("MA", r"adding lives worth living, \ affecting no one else, \ does not make an outcome worse"),
    ("NAE", r"a larger total, \ shared more equally, \ among the same people, \ is better"),
    ("TRANS", r"`better than' is transitive"),
    ("AZ", r"A, \ ten billion flourishing lives, \ is better than Z"),
]


def compute_tetrad():
    # MA: A+ is no worse than A; NAE: B is better than A+; iterate with TRANS down to Z: Z is better than A
    claims = {k: prop.Var(k) for k, _ in TETRAD}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in TETRAD]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in TETRAD], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


ITEMS = {"sequence": Pop.parfit_sequence, "addition": Pop.mere_addition, "vrc": Pop.very_repugnant, "tetrad": compute_tetrad,
         "arrhenius": Pop.arrhenius_table, "nonidentity": Pop.non_identity, "ramsey": Pop.ramsey,
         "xrisk": Pop.existential, "fanatic": Pop.fanaticism, "infinite": Pop.infinite,
         "cea": Pop.cost_effectiveness, "vsl": Pop.vsl, "neutrality": Pop.neutrality, "policy": Pop.climate_policy,
         "three": Pop.three_outcomes, "qaly": Pop.qaly_allocation, "sadism": Pop.sadistic_example,
         "scope": lambda: SCOPE, "hazard": Pop.stern_hazard, "benign": Pop.benign_addition,
         "weights": Pop.moral_weights, "hmv": Pop.harm_minimizing, "transfer": Pop.vsl_transfer}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

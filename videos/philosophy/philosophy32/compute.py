"""Precompute everything in Part 32 of *Philosophy, Built* ("Free Will").

    python -m videos.philosophy.philosophy32.compute            # everything missing (seconds)

Items:
    rules         the consequence argument's rules on McKay and Johnson's coin: alpha, beta, beta-box, agglomeration
    frankfurt     a Frankfurt case on the same model: no choice about the act, a flicker of freedom
    tetrad        the Price List for free will
    rollback      van Inwagen's rollback: 1000 replays of one undetermined moment
    accumulator   Schurger, Sitt and Dehaene's leaky stochastic accumulator: a readiness potential from noise
    prediction    self-prediction: a contrarian agent, and a diagonal over predictors
    luck          moral luck: ten thousand drivers, equally careless
    miracles      Lewis's local miracles on a reversible deterministic world
    interruptus   the accumulator, interrupted: response times by where the noise had carried it
    responsibility  Chockler and Halpern's degrees of responsibility: votes, and many hands
    responsive    Fischer and Ravizza's reasons-responsiveness, on three mechanisms
    chsh          answers fixed in advance: the CHSH bound over all 16 local strategies
    levels        List's levels: a deterministic micro-world, an indeterministic agent-level one
    torn          a torn decision: a double well that amplifies any difference
    ledgers       the careless drivers blamed by outcome and by risk
    avoider       Dennett's evitability: a deterministic agent that dodges falling rocks
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import freewill as F
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy32")
load = CACHE.load

TETRAD = [
    ("F", r"some of our acts are free"),
    ("A", r"an act is free only if the agent could have done otherwise"),
    ("C", r"if determinism is true, no one could ever have done otherwise"),
    ("D", r"determinism is true"),
]


def compute_tetrad():
    claims = {k: prop.Var(k) for k, _ in TETRAD}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in TETRAD]))]
    res = prop.mus_mcs(claims, bg)
    # PhilPapers Survey 2020 (Bourget and Chalmers 2023), target faculty, accept or lean towards
    return {"claims": [{"key": k, "text": t} for k, t in TETRAD], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]],
            "survey": {"compatibilism": 0.592, "libertarianism": 0.188, "no free will": 0.112}}


ITEMS = {"rules": F.rule_check, "frankfurt": F.frankfurt, "tetrad": compute_tetrad, "rollback": F.rollback,
         "accumulator": F.accumulator, "prediction": F.self_prediction, "luck": F.moral_luck,
         "miracles": F.miracles, "interruptus": F.interruptus, "responsibility": F.responsibility,
         "responsive": F.reasons_responsive, "chsh": F.chsh_local, "levels": F.levels,
         "torn": F.torn_decision, "ledgers": F.blame_ledgers,
         "avoider": F.avoider}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

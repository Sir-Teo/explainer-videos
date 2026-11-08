"""Precompute everything in Part 16 of *Philosophy, Built* ("Evidence by Numbers").

    python -m videos.philosophy.philosophy16.compute            # everything missing (under a minute)

Items:
    schools     60 heads in 100: Fisher's p, Neyman--Pearson's decision and power, Jeffreys's Bayes factor
    pdist       p-values under the null and an alternative
    misread     six misreadings of p, each refuted by simulation
    baserate    a screening test on 1,000 people
    collins     People v. Collins: one in twelve million, and the chance of a second matching couple
    ppv         Ioannidis's table, recomputed; PPV as a function of prior odds and power
    garden      a garden of forking paths over pure noise
    stopping    optional stopping under the null; a likelihood-ratio stopper
    birnbaum    binomial and negative binomial data with proportional likelihoods; the Birnbaum Price List
    lindley     Lindley's paradox; prior sensitivity of the Bayes factor; the Sellke--Bayarri--Berger bound
    severity    Mayo's severity curves
    simpson     Berkeley 1973, six departments
    betting     a test martingale, Ville's inequality, wealth under the alternative
    ab          A/B peeking against an e-process
    aic         AIC, BIC and predictive accuracy for polynomial degree
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import prop
from explainer.philosophy.reasoner import stats as S

CACHE = Cache("philosophy16")
load = CACHE.load

BIRNBAUM = [("B1", r"sufficiency: \ outcomes with the same sufficient statistic carry the same evidence", "a"),
            ("B2", r"conditionality: \ a coin flip choosing the experiment adds no evidence", "b"),
            ("B3", r"the sampling plan matters: \ binomial and negative binomial data differ as evidence", "c")]


def compute_schools() -> dict:
    return S.three_schools()


def compute_pdist() -> dict:
    return {**S.p_distribution(), "ci": S.ci_coverage()}


def compute_misread() -> dict:
    return S.misreadings()


def compute_baserate() -> dict:
    return S.base_rate()


def compute_collins() -> dict:
    return S.collins()


def compute_ppv() -> dict:
    curve = {str(pw): [[r, S.ppv(pw, 0.05, r)] for r in [10 ** (k / 10) for k in range(-30, 11)]]
             for pw in (0.2, 0.5, 0.8)}
    return {"table": S.ioannidis_table(), "curve": curve}


def compute_garden() -> dict:
    return {**S.garden(), "one": S.garden_paths(10), "curse": S.winners_curse()}


def compute_stopping() -> dict:
    return S.optional_stopping()


def compute_birnbaum() -> dict:
    claims = {k: prop.parse(f) for k, _, f in BIRNBAUM}
    res = prop.mus_mcs(claims, [prop.parse("(a & b) -> ~c")])
    return {**S.birnbaum(), "claims": [{"key": k, "text": t} for k, t, _ in BIRNBAUM],
            "mus": [sorted(x) for x in res["mus"]], "mcs": [sorted(x) for x in res["mcs"]]}


def compute_lindley() -> dict:
    return {"lindley": S.lindley(), "prior": S.prior_sensitivity(),
            "sellke": [{"p": p, "bf01_min": S.sellke_bound(p)} for p in (0.05, 0.01, 0.005, 0.001)]}


def compute_severity() -> dict:
    return S.severity()


def compute_simpson() -> dict:
    return S.simpson()


def compute_betting() -> dict:
    return S.betting()


def compute_ab() -> dict:
    return S.ab_peeking()


def compute_aic() -> dict:
    return S.aic_bic()


ITEMS = {"schools": compute_schools, "pdist": compute_pdist, "misread": compute_misread,
         "baserate": compute_baserate, "collins": compute_collins, "ppv": compute_ppv, "garden": compute_garden, "stopping": compute_stopping,
         "birnbaum": compute_birnbaum, "lindley": compute_lindley, "severity": compute_severity,
         "simpson": compute_simpson, "betting": compute_betting, "ab": compute_ab, "aic": compute_aic}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

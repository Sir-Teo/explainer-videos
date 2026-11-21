"""Precompute every number in Part 60 of *Economics, Built* ("The Price").

    python -m videos.economics.econ60.compute            # everything missing (about two minutes)
    python -m videos.economics.econ60.compute --force dynamic

Results are cached in ``.cache/econ60/<name>.json``; scenes call ``load(name)``.  Models: Agora's ``revenue`` module
(the Island's airline, its survey respondents, its hotels and shops).  Data: FRED's producer price index for processed
foods and the consumer price index for food at home (the pass-through chapter and the intermission).

Items:
    costplus    the markup rule against a fixed markup when the elasticity is only estimated
    conjoint    a choice-based conjoint survey of 400 travellers, fitted by a multinomial logit
    experiment  an A/B test of a discount with scarce rooms, against the global effect and a test by city
    dynamic     the Island's flight: the optimal policy by dynamic programming, the best fixed price
    playit      the Play-it's four weekly rules, simulated
    rm          Littlewood's two fares, EMSR-b's protection levels, overbooking
    menu        good, better, best; a most-favoured-customer clause
    bundle      large bundles of goods with independent values
    hilo        high-low promotions against everyday low prices, with shoppers who value a deal
    chain       store-by-store against uniform prices in a chain
    passthrough factory-gate food prices to the grocer's: the 2000-19 relation and 2021-23
    bandit      Thompson sampling against test-then-commit
    film        the intermission's data film: producer and consumer food prices, 1990-2026
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data
from explainer.economics import score as SC
from explainer.economics.agora import revenue as R

CACHE = Cache("econ60")
load = CACHE.load
TRUTH = {"flight": "buyers' arrival rates and willingness to pay by day are planted (FLIGHT in agora.revenue)"}
FILM_SECONDS = 44.0
MELODY_SECONDS = FILM_SECONDS + 10.0
FILM_YEARS = (1990.0, 2027.0)


def film_time(year: float) -> float:
    a, b = FILM_YEARS
    return 2.0 + (year - a) / (b - a) * (FILM_SECONDS - 4.0)


def _jsonable(x):
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return [_jsonable(v) for v in x.tolist()]
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, float) and not np.isfinite(x):
        return None
    return x


def compute_costplus() -> dict:
    return _jsonable(R.cost_plus_robustness())


def compute_conjoint() -> dict:
    return _jsonable(R.conjoint())


def compute_experiment() -> dict:
    return _jsonable(R.interference())


def compute_dynamic() -> dict:
    F = R.flight()
    D = R.dp_prices(F)
    pol = np.array(D["policy"])
    # one simulated flight under the optimal policy, day by day
    rng = np.random.default_rng(601)
    x, path_p, path_x = F["seats"], [], []
    for t in range(F["days"]):
        p = float(pol[t, x]) if x > 0 else float("nan")
        path_p.append(p)
        path_x.append(x)
        if x > 0:
            s = min(int(rng.poisson(F["lam"][t] * np.exp(-p / F["mu"][t]))), x)
            x -= s
    return _jsonable({"V0": D["V0"], "policy": pol[:, ::5], "seats_axis": list(range(0, F["seats"] + 1, 5)),
                      "fixed": D["fixed"], "path_p": path_p, "path_x": path_x, "flight": {
                          k: v for k, v in F.items() if k not in ("dleft", "lam", "mu")},
                      "lam": F["lam"], "mu": F["mu"], "days": F["days"]})


def compute_playit() -> dict:
    F = R.flight()
    D = R.dp_prices(F)
    P = R.playit_rules(F, D)
    return _jsonable(P)


def compute_rm() -> dict:
    L = R.littlewood()
    E = R.emsr_b()
    O = R.overbooking()
    return _jsonable({"littlewood": L, "emsr": E, "overbooking": O})


def compute_menu() -> dict:
    return _jsonable({"menu": R.menu(), "mfn": R.mfn()})


def compute_bundle() -> dict:
    return _jsonable(R.big_bundle())


def compute_hilo() -> dict:
    return _jsonable(R.hilo())


def compute_chain() -> dict:
    return _jsonable(R.chain())


def _food():
    a, b = data.fred("CUSR0000SAF11"), data.fred("WPU02")
    A = dict(zip(a["date"], a["value"]))
    B = dict(zip(b["date"], b["value"]))
    dates = [d for d in a["date"] if d in B and d >= "1990-01-01" and A[d] == A[d] and B[d] == B[d]]
    return dates, np.array([A[d] for d in dates]), np.array([B[d] for d in dates]), a["retrieved"]


def compute_passthrough() -> dict:
    dates, r, q, retrieved = _food()
    i0, i1 = dates.index("2000-01-01"), dates.index("2019-12-01")
    fit = R.passthrough_lags(r[i0:i1 + 1], q[i0:i1 + 1], lags=12)
    dq, dr = np.diff(np.log(q)), np.diff(np.log(r))
    coef, c = np.array(fit["coef"]), fit["const"]
    j0, j1 = dates.index("2021-01-01"), dates.index("2023-12-01")
    pred = [c + sum(coef[k] * dq[t - 1 - k] for k in range(13)) for t in range(j0, j1 + 1)]
    act = dr[j0 - 1:j1]
    months = dates[j0 - 1:j1 + 1]
    cum_pred = np.r_[0.0, np.cumsum(pred)]
    cum_act = np.r_[0.0, np.cumsum(act)]
    cum_ppi = np.r_[0.0, np.cumsum(dq[j0 - 1:j1])]
    return _jsonable({"cum": fit["cum"], "cum_se": fit["cum_se"], "coef": fit["coef"], "months": months,
                      "pred": 100 * (np.exp(cum_pred) - 1), "actual": 100 * (np.exp(cum_act) - 1),
                      "ppi": 100 * (np.exp(cum_ppi) - 1), "cpi_change": 100 * (r[j1] / r[j0 - 1] - 1),
                      "ppi_change": 100 * (q[j1] / q[j0 - 1] - 1), "pred_change": 100 * (np.exp(cum_pred[-1]) - 1),
                      "retrieved": retrieved})


def compute_bandit() -> dict:
    B = R.bandit_pricing()
    idx = np.unique(np.r_[np.linspace(0, len(B["ts_regret"]) - 1, 81).astype(int)])
    return _jsonable({**{k: v for k, v in B.items() if k not in ("ts_regret", "tc_regret")}, "t": idx + 1,
                      "ts": np.array(B["ts_regret"])[idx], "tc": np.array(B["tc_regret"])[idx],
                      "test": 1200, "horizon": len(B["ts_regret"])})


def compute_film() -> dict:
    dates, r, q, retrieved = _food()
    yrs = np.array([int(d[:4]) + (int(d[5:7]) - 0.5) / 12 for d in dates])
    base_r, base_q = r[0], q[0]
    annual = {}
    for d, v in zip(dates, r):
        annual.setdefault(int(d[:4]), []).append(v)
    ys = sorted(y for y in annual if len(annual[y]) == 12)
    inf = [100 * (np.mean(annual[y]) / np.mean(annual[y - 1]) - 1) for y in ys if y - 1 in annual]
    ys_inf = [y for y in ys if y - 1 in annual]
    return _jsonable({"t": [film_time(y) for y in yrs], "years": yrs, "cpi": 100 * r / base_r, "ppi": 100 * q / base_q,
                      "inf_years": ys_inf, "inflation": inf, "inf_t": [film_time(y + 0.5) for y in ys_inf],
                      "last": dates[-1], "retrieved": retrieved,
                      "events": [{"year": 2008.0, "what": "the 2008 food spike", "t": film_time(2008.0)},
                                 {"year": 2020.2, "what": "the pandemic", "t": film_time(2020.2)},
                                 {"year": 2022.2, "what": "war in Ukraine", "t": film_time(2022.2)}]})


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["inflation"])
    times = f["inf_t"]
    mel = SC.data_melody(vals, MELODY_SECONDS, times=times, act=11, log=False, low=45, high=84)
    events = {"film_end": film_time(FILM_YEARS[1]) + 4.0, "first": times[0]}
    clip = Clip(mel["y"], SC.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": SC.hz(nn), "name": f"{x:+.1f}%"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "food-at-home inflation, the CPI's yearly change, 1991-2025 (BLS via FRED), as a tune "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ60").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "costplus": compute_costplus,
    "conjoint": compute_conjoint,
    "experiment": compute_experiment,
    "dynamic": compute_dynamic,
    "playit": compute_playit,
    "rm": compute_rm,
    "menu": compute_menu,
    "bundle": compute_bundle,
    "hilo": compute_hilo,
    "chain": compute_chain,
    "passthrough": compute_passthrough,
    "bandit": compute_bandit,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

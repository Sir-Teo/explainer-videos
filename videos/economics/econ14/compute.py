"""Precompute every number in Part 14 of *Economics, Built* ("Incentives").

    python -m videos.economics.econ14.compute            # everything missing (seconds)
    python -m videos.economics.econ14.compute --force playit

Results are cached in ``.cache/econ14/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the Maddison Project's GDP per head for China and India; Gneezy and Rustichini's
day-care counts; transcribed passages from Lazear 2000, Shearer 2004, Bandiera, Barankay and Rasul 2005, Raff and
Summers 1987, Lin 1992 and Jacob and Levitt 2003).  Models: Agora's contracts (``agora.contracts``), with the
Island's Part 14 truths.

Items:
    playit      Crusoe's offers to Friday: the share, the fixed pay that keeps Friday on, effort, and Crusoe's profit
    team        Holmström's team: effort and surplus as the team grows
    discrete    the two-outcome model: the wages that buy hard work, and what risk costs
    tradeoff    the optimal share against noise and risk aversion
    rpe         relative performance evaluation: removing the common shock
    multitask   efforts on a measured and an unmeasured task against the share paid on the measured one
    tournament  effort against the prize spread, for two levels of noise
    ratchet     effort with a fixed target and with a ratchet
    shirking    Shapiro and Stiglitz's no-shirking curve, labour demand and the equilibrium
    sharecrop   effort and surplus against the tenant's share
    daycare     Gneezy and Rustichini's late pickups, fined centres against the others
    dial        the piece-rate dial's rows
    film        the intermission's data film: GDP per head in China and India, 1950-2022
    melody      its data melody: China's GDP per head, year by year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import contracts as ct
from explainer.economics.data import tables

CACHE = Cache("econ14")
load = CACHE.load
TRUTH = island.truths(14)


def compute_playit() -> dict:
    t = TRUTH["playit"]
    r, c, sig = t["r"], t["c"], t["sigma"]
    rows = []
    for b in t["shares"]:
        e = b / c
        risk = r * b ** 2 * sig ** 2 / 2
        alpha = -b * e + c * e ** 2 / 2 + risk          # the fixed pay that leaves Friday's certainty equivalent at 0
        profit = e - alpha - b * e
        rows.append({"share": float(b), "fixed": float(alpha), "effort": float(e), "risk": float(risk),
                     "profit": float(profit)})
    la = ct.linear_agency(r, c, sig)
    bs = np.linspace(0, 1, 101)
    prof = [ct.linear_agency(r, c, sig, beta=b)["surplus"] for b in bs]
    return {"rows": rows, "beta_star": la["beta_star"], "best_profit": la["surplus"], "fb_effort": la["first_best_effort"],
            "fb_profit": la["first_best_surplus"], "betas": bs, "profit_curve": prof, **t}


def compute_team() -> dict:
    t = TRUTH["team"]
    rows = [ct.team(n, t["a"], t["c"]) for n in t["ns"]]
    ns = np.arange(1, 21)
    return {"rows": rows, "ns": ns, "effort": [ct.team(int(n), t["a"], t["c"])["e_eq"] for n in ns],
            "lost": [ct.team(int(n), t["a"], t["c"])["lost"] for n in ns], "n18": ct.team(18, t["a"], t["c"])}


def compute_discrete() -> dict:
    t = TRUTH["discrete"]
    d = ct.two_outcome(t["p_high"], t["p_low"], t["y_high"], t["y_low"], t["cost"], t["reservation"])
    return {**d, **t}


def compute_tradeoff() -> dict:
    t = TRUTH["tradeoff"]
    sig = np.linspace(t["sigmas"][0], t["sigmas"][1], 101)
    cur = ct.share_curve(sig, t["rs"], t["c"])
    return {"sigma": sig, "rs": list(t["rs"]), "curves": [cur["curves"][r] for r in t["rs"]], "c": t["c"],
            "here": ct.linear_agency(TRUTH["playit"]["r"], TRUTH["playit"]["c"], TRUTH["playit"]["sigma"])}


def compute_rpe() -> dict:
    t = TRUTH["rpe"]
    return {**ct.relative_performance(t["r"], t["c"], t["common"], t["own"]), **t}


def compute_multitask() -> dict:
    t = TRUTH["multitask"]
    m = ct.multitask(t["s"], t["c"], t["base"])
    k = int(np.argmax(m["e2"] <= 1e-12)) if (m["e2"] <= 1e-12).any() else len(m["e2"]) - 1
    return {**m, "drop_at": float(m["beta"][k]), "base": t["base"]}


def compute_tournament() -> dict:
    t = TRUTH["tournament"]
    sp = np.linspace(t["spreads"][0], t["spreads"][1], 81)
    a = ct.tournament(sp, t["sigma"], t["c"])
    b = ct.tournament(sp, 2 * t["sigma"], t["c"])
    return {"spread": sp, "effort": a["effort"], "effort_noisy": b["effort"], "g0": a["g0"], "sigma": t["sigma"]}


def compute_ratchet() -> dict:
    t = TRUTH["ratchet"]
    return {**ct.ratchet(1.0, t["c"], t["delta"], t["bonus"]), **t}


def compute_shirking() -> dict:
    return ct.shapiro_stiglitz(**TRUTH["shirking"])


def compute_sharecrop() -> dict:
    return {**ct.sharecrop(**TRUTH["sharecrop"]), **TRUTH["sharecrop"]}


def compute_daycare() -> dict:
    g = tables.GNEEZY_RUSTICHINI_2000.data
    test = np.array([g["centres"][k][1] for k in g["test"]], float)
    ctrl = np.array([g["centres"][k][1] for k in g["control"]], float)
    return {"weeks": np.arange(1, g["weeks"] + 1), "test": test.mean(axis=0), "control": ctrl.mean(axis=0),
            "fine_from": g["fine_from_week"], "fine_until": g["fine_until_week"], "fine_nis": g["fine_nis"],
            "city": g["city"], "before": float(test[:, :4].mean()), "during": float(test[:, 4:16].mean()),
            "after": float(test[:, 16:].mean()), "control_mean": float(ctrl.mean())}


def compute_dial() -> dict:
    rows = [(e.who, e.year, e.design, e.sample, e.value, e.lo, e.hi)
            for e in dials.DIALS["piece_rate_response"].estimates]
    return {"rows": rows, "lazear": tables.LAZEAR_2000.data, "cases": tables.INCENTIVE_CASES.data}


# ---------------------------------------------------------------------------------------------------------------
# the intermission: China and India

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0


def film_time(k: int, n: int) -> float:
    return 1.5 + FILM_SECONDS * k / (n - 1)


def compute_film() -> dict:
    c, i = data.maddison_country("CHN"), data.maddison_country("IND")
    cm, im = dict(zip(c["year"], c["gdppc"])), dict(zip(i["year"], i["gdppc"]))
    years = [y for y in range(1950, 2023) if y in cm and y in im and cm[y] == cm[y] and im[y] == im[y]]
    n = len(years)
    ch, ind = [float(cm[y]) for y in years], [float(im[y]) for y in years]
    return {"years": years, "china": ch, "india": ind, "times": [film_time(k, n) for k in range(n)],
            "c1978": cm[1978], "c2022": cm[2022], "i1978": im[1978], "i2022": im[2022],
            "ratio_china": float(cm[2022] / cm[1978]), "ratio_india": float(im[2022] / im[1978])}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    times = f["times"]
    mel = score.data_melody(np.array(f["china"]), MELODY_SECONDS, times=times, act=4, log=True, low=45, high=84)
    events = {"film_end": times[-1] + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.3, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], f["years"])],
                meta={"label": "China's GDP per head, year by year, 1950-2022 (the Maddison Project), as a tune "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ14").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "years": f["years"], "seconds": MELODY_SECONDS}


ITEMS = {
    "playit": compute_playit,
    "team": compute_team,
    "discrete": compute_discrete,
    "tradeoff": compute_tradeoff,
    "rpe": compute_rpe,
    "multitask": compute_multitask,
    "tournament": compute_tournament,
    "ratchet": compute_ratchet,
    "shirking": compute_shirking,
    "sharecrop": compute_sharecrop,
    "daycare": compute_daycare,
    "dial": compute_dial,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

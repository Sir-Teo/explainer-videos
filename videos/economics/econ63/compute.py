"""Precompute every number in Part 63 of *Economics, Built* ("The Economy as a Network").

    python -m videos.economics.econ63.compute            # everything missing (under a minute)
    python -m videos.economics.econ63.compute --force quake

Results are cached in ``.cache/econ63/<name>.json``; scenes call ``load(name)``.  Models: Agora's ``network`` module
(the Island's input-output table, its firms' supply web, banks, villages and players).  Data: Japan's industrial
production, monthly, from the OECD via FRED (the intermission).

Items:
    table       the Island's input-output table, Domar weights, the Leontief inverse path by path, upstreamness
    hulten      each sector's shock under Cobb-Douglas technologies: GDP's loss equals the Domar weight times it
    playit      the Play-it: which sector's failure costs the Island most, with inputs hard to substitute
    response    GDP's response to energy shocks of every size, by the elasticity of substitution
    granular    aggregate volatility with equal against Zipf-sized firms, and a star against a ring of sectors
    quake       the earthquake on the Island's supply web: losses by distance, downstream and upstream
    oring       Kremer's O-ring teams, sorted and mixed
    banks       a four-bank clearing example, and contagion in a ring against a complete network
    ties        Granovetter's weak ties as two curves
    diffusion   seeding a village network: share informed by round, and one run of each rule
    keyplayer   the key player in a hub-and-clique network
    formation   Jackson and Wolinsky's connections model: efficient and stable networks by link cost
    fragility   Elliott, Golub and Leduc's supply networks: the share able to produce by relationship strength
    dials       the Island's estimates for the Dials: the granular residual and the elasticity of substitution
    film        the intermission's data film: Japan's industrial production, 2000-2024
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data
from explainer.economics import score as SC
from explainer.economics.agora import network as N

CACHE = Cache("econ63")
load = CACHE.load
TRUTH = {"quake": "the Island's supply web, the disaster and the share of inputs that are specific are planted "
                  "(agora.network.quake)",
         "dials": "the share of variance from firms' own shocks and the elasticity of substitution are planted "
                  "(agora.network.granular_residual, substitution_estimate)"}
FILM_SECONDS = 46.0
MELODY_SECONDS = FILM_SECONDS + 12.0
FILM_YEARS = (2000.0, 2024.5)
SERIES = "JPNPROINDMISMEI"


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


def compute_table() -> dict:
    return _jsonable({**N.island_table(), **N.leontief()})


def compute_hulten() -> dict:
    W = N.which_failure(shock=-0.10, theta=1.0)
    return _jsonable({**W, "domar": N.leontief()["domar"]})


def compute_playit() -> dict:
    return _jsonable({**N.which_failure(shock=-0.5, theta=0.15), "links": (N.SHARES > 0).sum(0)})


def compute_response() -> dict:
    return _jsonable(N.gdp_response("energy", shocks=np.linspace(-0.7, 0.3, 41), thetas=(0.15, 0.5, 1.0, 1.5)))


def compute_granular() -> dict:
    return _jsonable(N.granular())


def compute_quake() -> dict:
    Q = N.quake()
    Qd = N.quake(theta=1.0)
    Qg = N.quake(replace_specific=0.95)
    keep = ("rows", "far_loss", "direct_specific", "direct_generic", "hit_loss", "final_loss", "direct_only",
            "total_loss", "hit_share", "capacity", "theta")
    # a small drawing of the web: 5 tiers of 14 firms, links to the tier below
    rng = np.random.default_rng(63)
    small = []
    for t in range(1, 5):
        for i in range(14):
            for j in rng.choice(14, 2, replace=False):
                small.append((t - 1, int(j), t, i))
    return _jsonable({**{k: Q[k] for k in keep}, "cobb_douglas": {k: Qd[k] for k in keep},
                      "all_replaceable": {k: Qg[k] for k in keep}, "small_links": small})


def compute_oring() -> dict:
    O = N.oring()
    return _jsonable({k: v for k, v in O.items() if k != "q"} | {"q_hist": np.histogram(O["q"], bins=12,
                                                                                       range=(0.4, 1.0))[0]})


def compute_banks() -> dict:
    return _jsonable({"example": N.bank_example(), "contagion": N.contagion(shocks=np.linspace(0, 20, 41))})


def compute_ties() -> dict:
    return _jsonable(N.weak_ties())


def compute_diffusion() -> dict:
    D = N.diffusion()
    A = N.village()
    n = len(A)
    deg = A.sum(1)
    hubs = np.flatnonzero(deg >= 15)
    ang = 2 * np.pi * np.arange(n) / n
    rad = np.where(np.isin(np.arange(n), hubs), 0.45, 1.0)
    xy = np.c_[rad * np.cos(ang), rad * np.sin(ang)]
    w, v = np.linalg.eigh(A.astype(float))
    cent = np.abs(v[:, -1])
    rng = np.random.default_rng(630)
    runs = {}
    for name, pick in (("most central", np.argsort(-cent)[:5]), ("at random", rng.choice(n, 5, replace=False)),
                       ("least central", np.argsort(cent)[:5])):
        informed = np.zeros(n, bool)
        informed[pick] = True
        seq = [np.flatnonzero(informed).tolist()]
        for _ in range(8):
            tries = A[informed].sum(0)
            informed = informed | (rng.random(n) < 1 - (1 - 0.12) ** tries)
            seq.append(np.flatnonzero(informed).tolist())
        runs[name] = seq
    edges = [(int(i), int(j)) for i, j in zip(*np.nonzero(np.triu(A)))]
    return _jsonable({**D, "xy": xy, "edges": edges, "runs": runs, "hubs": hubs})


def compute_keyplayer() -> dict:
    return _jsonable(N.key_player())


def compute_formation() -> dict:
    return _jsonable(N.formation(costs=np.round(np.linspace(0.05, 1.2, 47), 4)))


def compute_fragility() -> dict:
    return _jsonable(N.fragility())


def compute_dials() -> dict:
    G = N.granular_residual()
    S = N.substitution_estimate()
    return _jsonable({"granular": {k: v for k, v in G.items() if k != "r2"}, "substitution": S})


def _japan():
    s = data.fred(SERIES)
    yrs = np.array([int(d[:4]) + (int(d[5:7]) - 1) / 12 + 1 / 24 for d in s["date"]])
    v = np.array([np.nan if x in ("", None) else float(x) for x in s["value"]])
    return yrs, v, s["date"], data.FRED_RETRIEVED[SERIES]


def compute_film() -> dict:
    yrs, v, dates, retrieved = _japan()
    keep = (yrs >= FILM_YEARS[0]) & np.isfinite(v)
    y, x = yrs[keep], v[keep]
    dts = [d for d, k in zip(dates, keep) if k]
    mom = 100 * (x[1:] / x[:-1] - 1)
    worst = np.argsort(mom)[:3]
    quarters = {}
    for yy, xx in zip(y, x):
        quarters.setdefault((int(yy), int((yy % 1) * 12) // 3), []).append(xx)
    qs = sorted(k for k in quarters if len(quarters[k]) == 3)
    qv = np.array([np.mean(quarters[k]) for k in qs])
    qg = 100 * (qv[1:] / qv[:-1] - 1)
    qt = [film_time(k[0] + (k[1] + 1) / 4) for k in qs[1:]]
    march = dts.index("2011-03-01")
    return _jsonable({"years": y, "index": x, "t": [film_time(t) for t in y], "first": dts[0], "last": dts[-1],
                      "retrieved": retrieved, "worst": [{"date": dts[i + 1], "change": mom[i]} for i in worst],
                      "march_2011": float(mom[march - 1]), "feb_2011": float(x[march - 1]),
                      "mar_2011": float(x[march]),
                      "recovered": dts[march + int(np.argmax(x[march:] >= 0.97 * x[march - 1]))],
                      "q_growth": qg, "q_t": qt, "peak_2008": float(x[(y > 2007) & (y < 2009)].max()),
                      "trough_2009": float(x[(y > 2008.5) & (y < 2010)].min())})


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["q_growth"])
    times = f["q_t"]
    mel = SC.data_melody(vals, MELODY_SECONDS, times=times, act=12, log=False, low=45, high=84)
    events = {"film_end": film_time(FILM_YEARS[1]) + 4.0, "first": times[0], "quake": film_time(2011 + 2.5 / 12)}
    clip = Clip(mel["y"], SC.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": SC.hz(nn), "name": f"{x:+.1f}%"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "Japan's industrial production, its growth quarter by quarter since 2000 (OECD via "
                               "FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ63").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "table": compute_table,
    "hulten": compute_hulten,
    "playit": compute_playit,
    "response": compute_response,
    "granular": compute_granular,
    "quake": compute_quake,
    "oring": compute_oring,
    "banks": compute_banks,
    "ties": compute_ties,
    "diffusion": compute_diffusion,
    "keyplayer": compute_keyplayer,
    "formation": compute_formation,
    "fragility": compute_fragility,
    "dials": compute_dials,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

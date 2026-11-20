"""Precompute every number in Part 44 of *Economics, Built* ("Dynamics, Platforms and Antitrust").

    python -m videos.economics.econ44.compute            # everything missing (about five minutes)
    python -m videos.economics.econ44.compute --force qlearn

Results are cached in ``.cache/econ44/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: Rust's Madison bus panel; the tables of Rust and Hotz and Miller, Ericson and Pakes,
Bajari, Benkard and Levin and Ryan, the vertical cases, Rochet and Tirole, Armstrong and Rysman, David and Liebowitz
and Margolis, Arrow, Aghion et al. and Cunningham, Ederer and Ma, Calvano et al. and Assad et al., the antitrust
cases, Baron and Myerson, Kwoka's retrospectives and IDC).  Models: Agora's industrial organization (``agora.io``,
part II) with the Island's Part 44 truths.

Items:
    ledger       ten of Rust's 1975 GMC buses: miles since the last rebuild, month by month
    playit       the Island's rebuild game: average monthly cost of four rules and the best one
    rust         Rust's data and model: transitions, NFXP at beta 0.9999 and at 0, the likelihood across betas
    ccp          conditional choice probabilities: on Zurcher's buses and on simulated fleets, against NFXP
    duopoly      a Markov-perfect duopoly: investment policy, a simulated history, the distribution of the gap
    vertical     double marginalization
    platform     a two-sided platform's prices as one side's value to the other rises
    lockin       how often an inferior first mover wins, by the strength of network effects
    innovation   Arrow's replacement effect; the step-by-step model's inverted U
    killer       a killer acquisition in numbers
    qlearn       twelve sessions of Q-learning price setters; a deviation and its punishment
    regulation   Baron and Myerson: the distortion and the rent, by the weight on profits
    film         the intermission's data film: the fleet's mileage since rebuild, month by month, 1974-1985
    melody       its data melody
"""

from __future__ import annotations

import time

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import io
from explainer.economics.data import tables

CACHE = Cache("econ44")
load = CACHE.load
TRUTH = island.truths(44)
FILM_SECONDS = 52.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def _panel():
    T = TRUTH["rust"]
    return io.rust_panel(data.rust_buses(), groups=T["groups"], bin_miles=T["bin"], n_states=T["n"])


def compute_playit() -> dict:
    P = TRUTH["playit"]
    R = _panel()
    p = io.rust_transitions(R["dx"])
    m = io.Rust(P["RC"], 1000 * P["per_bin"], p, beta=0.9999, n=TRUTH["rust"]["n"])
    th = np.arange(4, 89)
    cost = np.array([m.average_cost(int(t)) for t in th])
    k = int(np.argmin(cost))
    opts = {str(o): m.average_cost(int(o // 5000)) for o in P["options"]}
    best_opt = min(opts, key=opts.get)
    miles_month = float((p * np.arange(len(p))).sum() * 5000)
    return {"thresholds": (th * 5000).tolist(), "cost": cost.tolist(), "best": int(th[k] * 5000),
            "best_cost": float(cost[k]), "options": opts, "best_option": int(best_opt), "p": p.tolist(),
            "miles_month": miles_month, "RC": P["RC"], "per_bin": P["per_bin"],
            "upkeep_150k": P["per_bin"] * 30}


def compute_rust() -> dict:
    T = TRUTH["rust"]
    d = data.rust_buses()
    R = _panel()
    p = io.rust_transitions(R["dx"])
    t0 = time.time()
    nf = io.rust_nfxp(R["x"], R["d"], p, beta=T["beta"], n=T["n"])
    secs = time.time() - t0
    my = io.rust_nfxp(R["x"], R["d"], p, beta=0.0, start=(5.0, 50.0), n=T["n"])
    prof = []
    for b in T["betas"]:
        r = io.rust_nfxp(R["x"], R["d"], p, beta=b, start=(nf["RC"], nf["theta1"]) if b > 0.5 else (5.0, 50.0),
                         n=T["n"])
        prof.append({"beta": b, "loglik": r["loglik"], "RC": r["RC"], "theta1": r["theta1"]})
    m = io.Rust(nf["RC"], nf["theta1"], p, beta=T["beta"], n=T["n"])
    ev = m.ev()
    p1 = m.prob_replace(ev)
    # observed replacement frequency by 25,000-mile band
    bands = np.arange(0, 450001, 25000)
    xm = R["x"] * T["bin"]
    freq, mids, counts = [], [], []
    for lo, hi in zip(bands[:-1], bands[1:]):
        sel = (xm >= lo) & (xm < hi)
        if sel.sum() >= 30:
            freq.append(float(R["d"][sel].mean()))
            mids.append(float((lo + hi) / 2))
            counts.append(int(sel.sum()))
    g = np.asarray(d["group"])
    buses = len({(a, b) for a, b in zip(d["group"], d["bus"])})
    return {"p": p.tolist(), "nfxp": nf, "myopic": my, "profile": prof, "lr": 2 * (nf["loglik"] - my["loglik"]),
            "seconds": secs, "p1": p1.tolist(), "ev": ev.tolist(), "freq": freq, "mids": mids, "counts": counts,
            "at": R["at"].tolist(), "mean_at": float(R["at"].mean()), "n_obs": int(len(R["x"])),
            "n_repl": int(R["d"].sum()), "buses_all": buses, "buses_used": int(np.sum([len({b for gg, b in
                                                                                         zip(g, d["bus"]) if gg == k})
                                                                                         for k in T["groups"]])),
            "cost_150k": 0.001 * nf["theta1"] * 30, "months_of_upkeep": nf["RC"] / (0.001 * nf["theta1"] * 30)}


def _simulate_fleet(m: io.Rust, nb: int, months: int, rng) -> tuple:
    P1 = m.prob_replace()
    xs, ds = [], []
    for _ in range(nb):
        x = 0
        for _t in range(months):
            dd = rng.random() < P1[x]
            xs.append(x)
            ds.append(int(dd))
            x = min((0 if dd else x) + int(rng.choice(len(m.p), p=m.p)), m.n - 1)
    return np.array(xs), np.array(ds)


def compute_ccp() -> dict:
    R = _panel()
    p = io.rust_transitions(R["dx"])
    Rr = load("rust")
    real = {}
    for deg in (1, 2, 3):
        t0 = time.time()
        c = io.rust_ccp(R["x"], R["d"], p, degree=deg)
        real[str(deg)] = {"RC": c["RC"], "theta1": c["theta1"], "seconds": time.time() - t0, "p1": c["p1_hat"]}
    F = TRUTH["fleets"]
    rng = np.random.default_rng(F["seed"])
    m = io.Rust(Rr["nfxp"]["RC"], Rr["nfxp"]["theta1"], p)
    sims = {}
    for nb in F["sizes"]:
        xs, ds = _simulate_fleet(m, nb, F["months"], rng)
        t0 = time.time()
        nf = io.rust_nfxp(xs, ds, p)
        t1 = time.time() - t0
        t0 = time.time()
        cc = io.rust_ccp(xs, ds, p, degree=3)
        t2 = time.time() - t0
        sims[str(nb)] = {"replacements": int(ds.sum()), "nfxp": [nf["RC"], nf["theta1"]], "ccp": [cc["RC"],
                                                                                                 cc["theta1"]],
                         "t_nfxp": t1, "t_ccp": t2}
    return {"real": real, "sims": sims, "truth": [Rr["nfxp"]["RC"], Rr["nfxp"]["theta1"]]}


def compute_duopoly() -> dict:
    D = TRUTH["duopoly"]
    eq = io.pm_duopoly(K=D["K"], M=D["M"], a=D["a"], delta=D["delta"], beta=D["beta"])
    path = io.pm_simulate(eq, T=D["T"], seed=D["seed"])
    gap = path[:, 0] - path[:, 1]
    lead = np.sign(gap)
    changes = int(np.sum((lead[1:] != lead[:-1]) & (lead[1:] != 0) & (lead[:-1] != 0)))
    hist = np.bincount(np.abs(gap), minlength=D["K"]) / len(gap)
    return {"X": eq["X"].tolist(), "V": eq["V"].tolist(), "pi": eq["pi"].tolist(), "iterations": eq["iterations"],
            "path": path[:300].tolist(), "gap_hist": hist.tolist(), "mean_gap": float(np.abs(gap).mean()),
            "lead_changes": changes, "T": D["T"], "x_even": float(np.mean(np.diag(eq["X"]))),
            "x_lead2": float(np.mean([eq["X"][i + 2, i] for i in range(D["K"] - 2)])),
            "x_lag2": float(np.mean([eq["X"][i, i + 2] for i in range(D["K"] - 2)]))}


def compute_vertical() -> dict:
    return io.double_marginalization(**TRUTH["vertical"])


def compute_platform() -> dict:
    P = TRUTH["platform"]
    al = np.round(np.linspace(0.0, 1.2, 25), 3)
    rows = [io.platform(P["a1"], P["a2"], P["alpha1"], float(a)) for a in al]
    return {"alpha2": al.tolist(), "p1": [r["p"][0] for r in rows], "p2": [r["p"][1] for r in rows],
            "n1": [r["n"][0] for r in rows], "n2": [r["n"][1] for r in rows], "alpha1": P["alpha1"],
            "at": {str(a): io.platform(P["a1"], P["a2"], P["alpha1"], a) for a in (0.2, 0.8, 1.2)}}


def compute_lockin() -> dict:
    L = TRUTH["lockin"]
    nets = np.round(np.linspace(0.0, 0.04, 17), 4)
    share = [io.inferior_lockin(L["quality"], float(n), L["adopters"], L["runs"], L["seed"])["share_a_wins"]
             for n in nets]
    ex = io.inferior_lockin(L["quality"], 0.02, L["adopters"], 40, L["seed"] + 1)
    return {"network": nets.tolist(), "share": share, "paths": ex["paths"], "quality": L["quality"],
            "at02": ex["share_a_wins"], "qwerty": tables.QWERTY.where}


def compute_innovation() -> dict:
    N = TRUTH["innovation"]
    ds = np.round(np.linspace(0.02, 1.0, 50), 3)
    rows = [io.step_by_step(float(x), N["pi1"], N["r"], N["h"]) for x in ds]
    inn = np.array([r["innovation"] for r in rows])
    k = int(np.argmax(inn))
    arrow = io.arrow_replacement(N["a"], N["c"], N["c_new"])
    return {"delta": ds.tolist(), "innovation": inn.tolist(), "n0": [r["n0"] for r in rows],
            "nm": [r["nm"] for r in rows], "mu0": [r["mu0"] for r in rows], "peak": float(ds[k]),
            "peak_value": float(inn[k]), "low": float(inn[0]), "high": float(inn[-1]), "arrow": arrow}


def compute_killer() -> dict:
    return {**io.killer(**TRUTH["killer"]), **TRUTH["killer"]}


def compute_qlearn() -> dict:
    Q = TRUTH["qlearn"]
    res = []
    for s in range(Q["sessions"]):
        r = io.q_learning(max_iter=Q["max_iter"], stable=Q["stable"], seed=Q["seed"] + s)
        dv = io.q_deviation(r)
        res.append({"prices": r["prices"], "gain": r["gain"], "iterations": r["iterations"], "dev": dv,
                    "cycle": len(r["cycle"])})
        nash, mono, grid = r["nash"], r["monopoly"], r["grid"]
    gains = np.array([r["gain"] for r in res])
    order = np.argsort(gains)
    med = res[int(order[len(order) // 2])]
    punished = [bool(min(r["dev"]["p2"][2:6]) < r["dev"]["p2"][0] - 1e-9) for r in res]
    return {"sessions": res, "gains": gains.tolist(), "mean_gain": float(gains.mean()), "nash": nash,
            "monopoly": mono, "grid": grid, "median": med, "punished": punished,
            "share_punished": float(np.mean(punished)),
            "mean_price": float(np.mean([np.mean(r["prices"]) for r in res])),
            "iterations": float(np.mean([r["iterations"] for r in res]))}


def compute_regulation() -> dict:
    R = TRUTH["regulation"]
    base = io.baron_myerson(**R)
    ws = np.round(np.linspace(0.0, 1.0, 21), 3)
    rows = [io.baron_myerson(R["a"], R["c_lo"], R["c_hi"], R["nu"], float(w)) for w in ws]
    return {**base, "weights": ws.tolist(), "q_hi_w": [r["q_hi"] for r in rows], "rent_w": [r["rent"] for r in rows]}


def compute_ledger() -> dict:
    """Ten buses of Rust's group 4 (GMC 1975): miles since the last rebuild, month by month."""
    d = {k: np.asarray(v) for k, v in data.rust_buses().items()}
    g4 = d["group"] == 4
    buses = sorted(set(d["bus"][g4]))
    rows = []
    for b in buses:
        idx = np.where(g4 & (d["bus"] == b))[0]
        t = (d["year"][idx] + (d["month"][idx] - 1) / 12).tolist()
        base, since, marks = 0.0, [], []
        for k, i in enumerate(idx):
            since.append((d["odometer"][i] - base) / 1000)
            if d["replace"][i] and k + 1 < len(idx):
                base = (d["odometer"][i] + d["odometer"][idx[k + 1]]) / 2
                marks.append(float(t[k]))
        rows.append({"bus": int(b), "t": t, "since": since, "rebuilds": marks})
    with_r = [r for r in rows if r["rebuilds"]]
    pick = with_r[:8] + [r for r in rows if not r["rebuilds"]][:2]
    return {"buses": pick, "n_group": len(buses), "n_rebuilt": len(with_r)}


def film_time(t: float, first: float = 1974.9, last: float = 1985.4) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    d = {k: np.asarray(v) for k, v in data.rust_buses().items()}
    t = d["year"] + (d["month"] - 1) / 12
    keys = sorted({(g, b) for g, b in zip(d["group"], d["bus"])})
    # miles since the last rebuild, bus by bus
    since = np.zeros(len(t))
    for g, b in keys:
        idx = np.where((d["group"] == g) & (d["bus"] == b))[0]
        base = 0.0
        for k, i in enumerate(idx):
            since[i] = d["odometer"][i] - base
            if d["replace"][i] and k + 1 < len(idx):
                base = (d["odometer"][i] + d["odometer"][idx[k + 1]]) / 2
    months = np.unique(np.round(t, 4))
    avg, n, reb = [], [], []
    for mth in months:
        sel = np.isclose(t, mth)
        avg.append(float(since[sel].mean()))
        n.append(int(sel.sum()))
        reb.append(int(d["replace"][sel].sum()))
    months = months.tolist()
    keep = [i for i, c in enumerate(n) if c >= 20]
    ts = [months[i] for i in keep]
    return {"t": ts, "v": [avg[i] / 1000 for i in keep], "n": [n[i] for i in keep], "rebuilds": [reb[i] for i in keep],
            "times": [film_time(x) for x in ts], "total_rebuilds": int(d["replace"].sum()),
            "peak": float(max(avg[i] for i in keep) / 1000), "first": ts[0], "last": ts[-1]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=9, log=False, low=40, high=84)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.3, "hz": score.hz(nn), "name": f"{x:.0f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the average mileage since the last engine rebuild across the Madison buses in "
                               "service, month by month, 1974-1985 (Rust's data), as a tune (computed)",
                      "kind": "synthesized"})
    ClipStore("econ44").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "ledger": compute_ledger,
    "playit": compute_playit,
    "rust": compute_rust,
    "ccp": compute_ccp,
    "duopoly": compute_duopoly,
    "vertical": compute_vertical,
    "platform": compute_platform,
    "lockin": compute_lockin,
    "innovation": compute_innovation,
    "killer": compute_killer,
    "qlearn": compute_qlearn,
    "regulation": compute_regulation,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

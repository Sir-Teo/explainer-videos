"""Precompute every number in Part 29 of *Economics, Built* ("The Cycle as Equilibrium").

    python -m videos.economics.econ29.compute            # everything missing (a minute)
    python -m videos.economics.econ29.compute --force rbc

Results are cached in ``.cache/econ29/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: FRED's real GDP, consumption, investment (with its residential and business parts),
hours and output per hour in the nonfarm business sector, the NBER's recession dates, and the Penn World Table for
the United States).  Models: Agora's dynamic programming (``agora.dp``) and real business cycle (``agora.rbc``) with the
Island's Part 29 truths.

Items:
    cycle        log real GDP, 1947-2026: its Hodrick-Prescott trend and cycle, and Hamilton's cycle
    play         Play it: six series on average around the NBER's business-cycle peaks, 1953-2007
    cake         the cake: value function iteration, the iterates, the contraction, the policy
    chains       Tauchen's and Rouwenhorst's chains for an AR(1), at two persistences
    bm           Brock and Mirman's closed form, and the growth model on a grid
    calibrate    the growth facts behind the parameters, from the Penn World Table
    rbc          the Island's RBC: steady state, the linear system's roots, the policy, impulse responses, moments
    frisch       hours' volatility in the model as the Frisch elasticity varies
    facts        the US business cycle's volatilities and comovements, 1948-2019, beside the model's
    solow        the Solow residual for the United States, 1950-2019, and its cycle
    gali         what a technology shock does to hours: Gali's VAR, with hours in growth rates and in levels
    wedges       the labour wedge and the efficiency wedge over the cycle
    film         the intermission's data film: the cycle in American real GDP, quarter by quarter
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import dp, rbc

CACHE = Cache("econ29")
load = CACHE.load
TRUTH = island.truths(29)

FIRST, LAST = "1948-01-01", "2019-10-01"        # the sample: postwar, before the pandemic


def _q(key: str) -> dict:
    d = data.fred(key)
    return {x: v for x, v in zip(d["date"], d["value"]) if np.isfinite(v)}


def _t(d: str) -> float:
    return int(d[:4]) + (int(d[5:7]) - 1) / 12


def _cyc(v, lam: float = 1600.0) -> np.ndarray:
    return np.asarray(dp.hp_filter(np.asarray(v, float), lam)["cycle"])


def _recessions(first: str = "1947-01-01") -> list:
    """NBER peaks and troughs (months) from the USREC indicator, as (peak, trough) dates."""
    d = data.fred("USREC")
    v, ds = np.array(d["value"]), d["date"]
    out, start = [], None
    for i in range(1, len(v)):
        if v[i] == 1 and v[i - 1] == 0:
            start = ds[i - 1]
        if v[i] == 0 and v[i - 1] == 1 and start is not None:
            if start >= first:
                out.append((start, ds[i - 1]))
            start = None
    return out


def _quarter(d: str) -> str:
    """The first month of the quarter containing month ``d``."""
    m = int(d[5:7])
    return f"{d[:4]}-{3 * ((m - 1) // 3) + 1:02d}-01"


def compute_cycle() -> dict:
    y = _q("GDPC1")
    ds = sorted(y)
    ly = np.log([y[d] for d in ds])
    hp = dp.hp_filter(ly)
    ham = dp.hamilton_filter(ly, h=8, p=4)
    t = np.array([_t(d) for d in ds])
    k = ham["start"]
    hc = np.array(ham["cycle"])
    hpc = np.array(hp["cycle"])
    lin = np.polyfit(t, ly, 1)
    rec = [(_t(a), _t(b)) for a, b in _recessions()]
    # how the HP trend at a date moves when later data arrive: the end-point problem
    cut = ds.index("2008-07-01")
    early = dp.hp_filter(ly[:cut + 1])
    return {"t": t.tolist(), "ly": ly.tolist(), "trend": hp["trend"], "hp": (100 * hpc).tolist(),
            "ham_t": t[k:].tolist(), "ham": (100 * hc).tolist(), "lin": (100 * (ly - np.polyval(lin, t))).tolist(),
            "corr_hp_ham": float(np.corrcoef(hpc[k:], hc)[0, 1]), "sd_hp": float(100 * hpc.std()),
            "sd_ham": float(100 * hc.std()), "recessions": rec, "growth": float(100 * 4 * lin[0] / 4),
            "endpoint": {"t": t[:cut + 1].tolist(), "early": (100 * np.array(early["cycle"])).tolist(),
                         "late": (100 * hpc[:cut + 1]).tolist()},
            "last": ds[-1]}


PLAY = (("GDPC1", r"real GDP"), ("PCECC96", r"consumer spending"), ("A008RA3Q086SBEA", r"business investment"),
        ("A011RA3Q086SBEA", r"housing investment"), ("HOANBS", r"hours worked"), ("OPHNFB", r"output per hour"))


def compute_play() -> dict:
    """Each series' log level around each NBER peak from 1953 to 2007, relative to its level at the peak quarter,
    with the series' own average growth over the window taken out; then averaged over the ten recessions."""
    peaks = [_quarter(a) for a, _ in _recessions() if "1953-01-01" <= a <= "2008-01-01"]
    out = {}
    W = 8
    for key, name in PLAY:
        s = _q(key)
        ds = sorted(s)
        ls = np.log([s[d] for d in ds])
        g = np.mean(np.diff(ls[ds.index("1950-01-01"):ds.index("2019-10-01") + 1]))
        paths = []
        for p in peaks:
            i = ds.index(p)
            seg = ls[i - W:i + W + 1] - ls[i] - g * np.arange(-W, W + 1)
            paths.append(100 * seg)
        P = np.array(paths)
        avg = P.mean(axis=0)
        own = [int(np.argmax(row[:W + 3])) - W for row in P]           # each recession's own peak, up to 2 after
        out[key] = {"name": name, "avg": avg.tolist(), "peak_q": int(np.argmax(avg[:W + 3])) - W,
                    "median_peak": float(np.median(own)), "drop": float(avg[W + 4] - avg.max()),
                    "paths": P.tolist()}
    order = sorted(out, key=lambda k: out[k]["peak_q"])
    return {"q": list(range(-W, W + 1)), "series": out, "peaks": peaks, "order": order, "leader": order[0]}


def compute_cake() -> dict:
    c = TRUTH["cake"]
    r = dp.cake(beta=c["beta"], w_max=c["w_max"], n=c["n"], iters=c["iters"], keep=c["keep"])
    w = np.array(r["w"])
    sub = np.arange(0, len(w), 10)
    gaps = np.array(r["gaps"])
    V, Vx = np.array(r["V"]), np.array(r["V_exact"])
    cc = np.array(r["c"])
    mid = slice(len(w) // 5, len(w))
    return {"w": w[sub].tolist(), "kept": {k: np.array(v)[sub].tolist() for k, v in r["kept"].items()},
            "V": V[sub].tolist(), "V_exact": Vx[sub].tolist(), "c": cc[sub].tolist(),
            "c_exact": np.array(r["c_exact"])[sub].tolist(), "gaps": gaps.tolist(), "iterations": r["iterations"],
            "ratio": float(np.median(gaps[5:60] / gaps[4:59])), "beta": c["beta"],
            "share": float(np.median(cc[mid] / w[mid])), "v_err": float(np.max(np.abs(V - Vx)[mid])),
            "gap1": float(gaps[0]), "n": c["n"]}


def compute_chains() -> dict:
    c = TRUTH["chains"]
    out = {}
    for rho in (c["rho"], c["rho_high"]):
        sd_true = c["sigma"] / np.sqrt(1 - rho ** 2)
        row = {"sd_true": float(sd_true)}
        for name, f in (("tauchen", dp.tauchen), ("rouwenhorst", dp.rouwenhorst)):
            ch = f(c["n"], rho, c["sigma"])
            m = dp.chain_moments(ch["z"], ch["P"])
            row[name] = {"z": ch["z"], "P": ch["P"], "sd": m["sd"], "rho": m["rho"], "pi": m["pi"]}
        out[f"{rho:g}"] = row
    return {"n": c["n"], "sigma": c["sigma"], "rhos": [c["rho"], c["rho_high"]], "chains": out}


def compute_bm() -> dict:
    b = TRUTH["bm"]
    g = TRUTH["growth"]
    path = rbc.brock_mirman(b["alpha"], b["beta"], b["rho"], b["sigma"], b["T"], b["seed"])
    full = rbc.growth_vfi(alpha=g["alpha"], beta=g["beta"], delta=1.0, rho=g["rho"], sigma=g["sigma"], nk=g["nk"],
                          nz=g["nz"])
    k = np.array(full["k"])
    z = np.array(full["z"])
    exact = g["alpha"] * g["beta"] * z[:, None] * k[None, :] ** g["alpha"]
    err = float(np.max(np.abs(np.array(full["kprime"]) - exact) / exact))
    step = float(k[1] - k[0])
    part = rbc.growth_vfi(**g)
    return {"path": path, "full": {"k": full["k"], "z": full["z"], "kprime": full["kprime"], "exact": exact.tolist(),
                                   "max_rel_err": err, "step_rel": step / float(np.mean(k)),
                                   "iterations": full["iterations"]},
            "part": {"k": part["k"], "z": part["z"], "kprime": part["kprime"], "kss": part["kss"],
                     "iterations": part["iterations"]}, "saving_rate": path["saving_rate"]}


def compute_calibrate() -> dict:
    rows = [r for r in data.pwt("USA") if 1950 <= r["year"] <= 2019]
    yr = np.array([r["year"] for r in rows])
    labsh = np.array([r["labsh"] for r in rows])
    ky = np.array([r["rnna"] / r["rgdpna"] for r in rows])
    iy = np.array([r["csh_i"] for r in rows])
    delta = np.array([r["delta"] for r in rows])
    hours = np.array([r["avh"] for r in rows])
    y = np.array([r["rgdpna"] / r["pop"] for r in rows])
    g = float(np.polyfit(yr, np.log(y), 1)[0])
    rb = TRUTH["rbc"]
    alpha, beta, dlt = rb["alpha"], rb["beta"], rb["delta"]
    ky_model = alpha / (1 / beta - 1 + dlt) / 4                                # annual K/Y in the model
    return {"labsh": float(labsh.mean()), "alpha_data": float(1 - labsh.mean()), "ky": float(ky.mean()),
            "iy": float(iy.mean()), "delta": float(delta.mean()), "hours": float(hours.mean()), "g": g,
            "hours_share": float(hours.mean() / (52 * 14 * 7)), "years": [int(yr[0]), int(yr[-1])],
            "model": {"alpha": alpha, "beta": beta, "delta": dlt, "r_annual": float(beta ** -4 - 1),
                      "ky": float(ky_model), "iy": float(dlt * 4 * ky_model), "rho": rb["rho"], "sigma": rb["sigma"],
                      "n_ss": rb["n_ss"]},
            "labsh_series": labsh.tolist(), "years_all": yr.tolist()}


def _model(frisch=None) -> rbc.RBC:
    r = TRUTH["rbc"]
    m = rbc.RBC(alpha=r["alpha"], beta=r["beta"], delta=r["delta"], rho=r["rho"], sigma=r["sigma"], n_ss=r["n_ss"],
                frisch=frisch)
    m.solve()
    return m


def _sim_moments(m: rbc.RBC) -> dict:
    r = TRUTH["rbc"]
    sim = m.simulate(r["T"], r["seed"])
    mo = rbc.moments(sim)
    c = {k: _cyc(v) for k, v in sim.items()}
    mo["corr_nw"] = float(np.corrcoef(c["n"], c["w"])[0, 1])
    mo["ac_y"] = float(np.corrcoef(c["y"][1:], c["y"][:-1])[0, 1])
    return mo


def compute_rbc() -> dict:
    m = _model()
    sol = m.solve()
    irf = m.irf(40, 0.01)
    mo = _sim_moments(m)
    sim = m.simulate(400, 5)
    sim_hp = {k: (100 * _cyc(v)).tolist() for k, v in sim.items()}         # filtered as the data are
    return {"ss": {"k": m.k_ss, "y": m.y_ss, "c": m.c_ss, "i": m.i_ss, "n": m.n_ss, "A": m.A,
                   "ky": m.k_ss / m.y_ss, "cy": m.c_ss / m.y_ss, "iy": m.i_ss / m.y_ss},
            "F": sol["F"], "P": sol["P"], "moduli": sol["moduli"], "n_stable": sol["n_stable"], "bk_ok": sol["bk_ok"],
            "eig": [float(abs(v)) for v in sol["eigenvalues"]], "irf": irf, "moments": mo,
            "AB": [x.tolist() for x in m.linear_system()], "phase": m.phase(),
            "sim": {k: (100 * np.array(v)).tolist() for k, v in sim.items()}, "sim_hp": sim_hp}


def compute_frisch() -> dict:
    out = []
    for f in TRUTH["rbc"]["frisch_grid"]:
        m = _model(f)
        mo = _sim_moments(m)
        irf = m.irf(12, 0.01)
        out.append({"frisch": f, "y": mo["y"]["sd"], "n_rel": mo["n"]["rel"], "w_rel": mo["w"]["rel"],
                    "n_impact": irf["n"][0]})
    m = _model()
    mo = _sim_moments(m)
    hansen = {"frisch": None, "y": mo["y"]["sd"], "n_rel": mo["n"]["rel"], "w_rel": mo["w"]["rel"],
              "n_impact": m.irf(12, 0.01)["n"][0]}
    from scipy.optimize import brentq

    half = brentq(lambda f: _sim_moments(_model(f))["n"]["rel"] - 0.5, 0.5, 4.0, xtol=1e-3)
    return {"rows": out, "hansen": hansen, "half": float(half)}


def compute_facts() -> dict:
    keys = {"y": "GDPC1", "c": "PCECC96", "i": "GPDIC1", "n": "HOANBS", "w": "OPHNFB"}
    S = {k: _q(v) for k, v in keys.items()}
    ds = sorted(d for d in S["y"] if all(d in S[k] for k in S) and FIRST <= d <= LAST)
    L = {k: np.log([S[k][d] for d in ds]) for k in S}
    C = {k: _cyc(v) for k, v in L.items()}
    ybus = _cyc(L["w"] + L["n"])                                              # nonfarm business output
    sy = C["y"].std()
    data_ = {"y": {"sd": float(100 * sy), "rel": 1.0, "corr": 1.0},
             "c": {"sd": float(100 * C["c"].std()), "rel": float(C["c"].std() / sy),
                   "corr": float(np.corrcoef(C["c"], C["y"])[0, 1])},
             "i": {"sd": float(100 * C["i"].std()), "rel": float(C["i"].std() / sy),
                   "corr": float(np.corrcoef(C["i"], C["y"])[0, 1])},
             "n": {"sd": float(100 * C["n"].std()), "rel": float(C["n"].std() / ybus.std()),
                   "corr": float(np.corrcoef(C["n"], ybus)[0, 1])},
             "w": {"sd": float(100 * C["w"].std()), "rel": float(C["w"].std() / ybus.std()),
                   "corr": float(np.corrcoef(C["w"], ybus)[0, 1])},
             "corr_nw": float(np.corrcoef(C["n"], C["w"])[0, 1]),
             "ac_y": float(np.corrcoef(C["y"][1:], C["y"][:-1])[0, 1])}
    split = {}
    for a, b in (("1948", "1984"), ("1985", "2019")):
        idx = [i for i, d in enumerate(ds) if a <= d[:4] <= b]
        split[f"{a}-{b}"] = {"corr_wy": float(np.corrcoef(C["w"][idx], ybus[idx])[0, 1]),
                            "corr_nw": float(np.corrcoef(C["n"][idx], C["w"][idx])[0, 1]),
                            "sd_y": float(100 * C["y"][idx].std())}
    t = [_t(d) for d in ds]
    return {"data": data_, "model": _sim_moments(_model()), "split": split, "first": ds[0], "last": ds[-1],
            "t": t, "cyc": {k: (100 * v).tolist() for k, v in C.items()}, "ybus": (100 * ybus).tolist()}


def compute_solow() -> dict:
    rows = [r for r in data.pwt("USA") if 1950 <= r["year"] <= 2019]
    yr = np.array([r["year"] for r in rows])
    Y = np.log([r["rgdpna"] for r in rows])
    K = np.log([r["rnna"] for r in rows])
    L = np.log([r["emp"] * r["avh"] for r in rows])
    s = np.array([r["labsh"] for r in rows])
    sb = (s[1:] + s[:-1]) / 2
    dA = np.diff(Y) - (1 - sb) * np.diff(K) - sb * np.diff(L)
    A = np.concatenate([[0.0], np.cumsum(dA)])
    ca, cy = _cyc(A, 100.0), _cyc(Y, 100.0)
    cl = _cyc(L, 100.0)
    worst = [int(yr[1:][i]) for i in np.argsort(dA)[:5]]
    return {"years": yr.tolist(), "dA": (100 * dA).tolist(), "dY": (100 * np.diff(Y)).tolist(),
            "cycA": (100 * ca).tolist(), "cycY": (100 * cy).tolist(), "cycL": (100 * cl).tolist(),
            "corr": float(np.corrcoef(ca, cy)[0, 1]), "corr_l": float(np.corrcoef(cl, cy)[0, 1]),
            "mean": float(100 * dA.mean()), "sd": float(100 * dA.std()),
            "negative_years": int(np.sum(dA < 0)), "worst": worst,
            "y2009": float(100 * dA[list(yr[1:]).index(2009)]), "y1982": float(100 * dA[list(yr[1:]).index(1982)])}


def compute_gali() -> dict:
    P, H = _q("OPHNFB"), _q("HOANBS")
    ds = sorted(d for d in P if d in H and FIRST <= d <= LAST)
    lp = np.log([P[d] for d in ds])
    lh = np.log([H[d] for d in ds])
    t = np.arange(len(lh))
    lhd = lh - np.polyval(np.polyfit(t, lh, 1), t)
    diff = rbc.gali(np.diff(lp), np.diff(lh), p=4, h=12, differenced=True, reps=500, seed=1)
    lev = rbc.gali(np.diff(lp), lhd[1:], p=4, h=12, differenced=False, reps=500, seed=2)
    k = ds.index("1994-10-01")
    old = rbc.gali(np.diff(lp[:k + 1]), np.diff(lh[:k + 1]), p=4, h=12, differenced=True, reps=300, seed=3)
    model = _model().irf(13, 0.01)
    return {"diff": diff, "levels": lev, "gali_sample": old, "model_n": model["n"], "model_w": model["w"],
            "first": ds[0], "last": ds[-1]}


def compute_wedges() -> dict:
    """With utility log c - A n and Cobb-Douglas output, the labour wedge is 1 - tau = A c n / ((1 - alpha) y) and
    the efficiency wedge is the Solow residual; their cycles, quarterly, from consumption, output and hours."""
    Y, C, H, P = _q("GDPC1"), _q("PCECC96"), _q("HOANBS"), _q("OPHNFB")
    ds = sorted(d for d in Y if d in C and d in H and d in P and FIRST <= d <= LAST)
    lw = np.log([C[d] / Y[d] * H[d] for d in ds])
    cw = -_cyc(lw)                                                         # tau's cycle (approximately)
    cy = _cyc(np.log([Y[d] for d in ds]))
    t = np.array([_t(d) for d in ds])
    rec = [(_t(a), _t(b)) for a, b in _recessions("1948-01-01") if a <= LAST]
    return {"t": t.tolist(), "labour": (100 * cw).tolist(), "y": (100 * cy).tolist(),
            "corr": float(np.corrcoef(cw, cy)[0, 1]), "sd": float(100 * cw.std()), "recessions": rec}


FILM_SECONDS = 40.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def film_time(t: float, first: float = 1947.0, last: float = 2026.75) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    c = compute_cycle()
    return {"t": c["t"], "cycle": c["hp"], "times": [film_time(x) for x in c["t"]], "recessions": c["recessions"],
            "last": c["last"]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    t = np.array(f["t"])
    vals = np.array(f["cycle"])
    times = [film_time(x) for x in t]
    mel = score.data_melody(vals - vals.min() + 1.0, MELODY_SECONDS, times=times, act=6, log=False, low=40,
                            high=84)
    events = {"film_end": film_time(t[-1]) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.1f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the cycle in American real GDP (its deviation from a Hodrick-Prescott trend), quarter "
                               "by quarter, 1947-2026 (BEA via FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ29").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "cycle": compute_cycle,
    "play": compute_play,
    "cake": compute_cake,
    "chains": compute_chains,
    "bm": compute_bm,
    "calibrate": compute_calibrate,
    "rbc": compute_rbc,
    "frisch": compute_frisch,
    "facts": compute_facts,
    "solow": compute_solow,
    "gali": compute_gali,
    "wedges": compute_wedges,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

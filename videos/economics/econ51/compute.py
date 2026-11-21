"""Precompute every number in Part 51 of *Economics, Built* ("Computing Economies").

    python -m videos.economics.econ51.compute            # everything missing (about a minute)
    python -m videos.economics.econ51.compute --force growth

Results are cached in ``.cache/econ51/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models: Agora's
solver harness (``agora.solve``) with the Island's Part 51 truths; Tauchen's and Rouwenhorst's chains from Agora's
``dp``.  Data: transistors per microprocessor (Rupp, via Our World in Data) for the intermission.  Times are wall
clock on the machine that builds the cache, so they differ from machine to machine; the ratios are what matter.

Items:
    growth      the growth model: value function iteration (iterates, distances, time), Howard's policy iteration,
                the contraction ratios, Blackwell's conditions
    grids       three grids of 30, 100 and 1,000 points: policies, steady states, Euler errors
    interp      value iteration between grid points with linear, cubic and Chebyshev interpolation; Runge's example
    household   the household by the endogenous grid method and by value iteration on four grids
    projection  Chebyshev collocation of degrees 1 to 10 and Galerkin; the residual at degree 3
    perturb     first- and second-order perturbation against the accurate rule; precautionary saving
    accuracy    the table of methods; the stopping tolerance against accuracy
    expect      Tauchen against Rouwenhorst at high persistence; Gauss-Hermite against Monte Carlo
    hjb         the household in continuous time: policies, the stationary distribution, the sparse matrix
    zlb         the zero bound by guess and verify, against the linear solution
    dimension   tensor against Smolyak grids: counts, and interpolation errors in four dimensions (of
                exp(-|x|^2/2) on [-1, 1]^4)
    reproduce   seeded draws, and a test with a known answer (Brock and Mirman's closed form)
    dials       how much the consumption rule moves with the elasticity of substitution, against method error
    frontier    the derivative of the solution with respect to beta: implicit function theorem against finite
                differences
    film        the intermission's data film: transistors per microprocessor, 1971-2021
    melody      its data melody
"""

from __future__ import annotations

import time

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import dp
from explainer.economics.agora import solve as S

CACHE = Cache("econ51")
load = CACHE.load
TRUTH = island.truths(51)
FILM_SECONDS = 46.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def _m():
    return S.growth(**TRUTH["growth"])


def _accurate(m):
    return S.collocation(m, 11)


def _ee(m, c, n=241):
    k = np.linspace(0.6 * m["kss"], 1.4 * m["kss"], n)
    e = S.euler_errors(m, c, k)
    return {"k": (k / m["kss"]).tolist(), "log10": e["log10"], "max": e["max"], "mean": e["mean"]}


def compute_growth() -> dict:
    m = _m()
    g = S.kgrid(m, 300)
    r = S.vfi(m, g, tol=1e-6, keep=(1, 2, 5, 10, 30, 100))
    h = S.howard(m, g)
    cp = S.contraction_path(m, g, 80)
    bw = S.blackwell(m, g)
    kept = {str(k): (v / 1.0).tolist() for k, v in r["kept"].items()}
    # when value iteration's policy stops changing, long before its values stop
    V = np.zeros(len(g))
    U = S._payoff(m, g)
    last_change, j_old = 0, None
    for it in range(1, r["iters"] + 1):
        V, j = S.bellman(V, g, m, U)
        if j_old is not None and np.any(j != j_old):
            last_change = it
        j_old = j
    return {"kss": m["kss"], "css": m["css"], "beta": m["beta"], "grid": (g / m["kss"]).tolist(),
            "V": r["V"].tolist(), "kept": kept, "vfi_iters": r["iters"], "vfi_seconds": r["seconds"],
            "dist": r["dist"], "howard_iters": h["iters"], "howard_changes": h["changes"],
            "howard_seconds": h["seconds"], "same_policy": bool(np.array_equal(h["j"], r["j"])),
            "ratio": cp["ratio"], "monotone": bw["monotone"], "discount_error": bw["discount_error"],
            "kprime": (r["kprime"] / m["kss"]).tolist(), "policy_settled": last_change}


def compute_grids() -> dict:
    m = _m()
    acc = _accurate(m)
    out = {"n": list(TRUTH["grids"]), "rows": []}
    kk = np.linspace(0.5, 1.5, 201) * m["kss"]
    out["k"] = (kk / m["kss"]).tolist()
    out["accurate"] = ((S.resources(kk, m) - acc["c"](kk)) / m["kss"]).tolist()
    for n in TRUTH["grids"]:
        g = S.kgrid(m, n)
        r = S.vfi(m, g, tol=1e-8)
        kp = r["kprime"]
        # the steady state of the grid's policy: the grid point it maps to itself (or the nearest)
        fixed = g[np.argmin(np.abs(kp - g))]
        pol = lambda k, g=g, kp=kp: S.resources(k, m) - np.interp(k, g, kp)  # noqa: E731
        e = _ee(m, pol)
        out["rows"].append({"n": n, "grid": (g / m["kss"]).tolist() if n <= 100 else [],
                            "kprime": (kp / m["kss"]).tolist() if n <= 100 else [],
                            "steady": float(fixed / m["kss"]), "iters": r["iters"], "seconds": r["seconds"],
                            "ee": e})
    return out


def compute_interp() -> dict:
    m = _m()
    out = {}
    for kind, g in (("linear", S.kgrid(m, 40)), ("cubic", S.kgrid(m, 40)),
                    ("chebyshev", S.chebyshev_nodes(12, 0.5 * m["kss"], 1.5 * m["kss"]))):
        r = S.vfi_continuous(m, g, kind)
        out[kind] = {"points": len(g), "iters": r["iters"], "seconds": r["seconds"], "ee": _ee(m, r["c"])}
    # Runge's example: 1/(1 + 25 x^2) through 11 points, evenly spaced or at Chebyshev nodes
    f = lambda x: 1 / (1 + 25 * x ** 2)  # noqa: E731
    x = np.linspace(-1, 1, 401)
    n = 11
    xe = np.linspace(-1, 1, n)
    xc = S.chebyshev_nodes(n, -1, 1)
    pe = np.polyfit(xe, f(xe), n - 1)
    pc = np.polyfit(xc, f(xc), n - 1)
    out["runge"] = {"x": x.tolist(), "f": f(x).tolist(), "even": np.polyval(pe, x).tolist(),
                    "cheb": np.polyval(pc, x).tolist(), "xe": xe.tolist(), "xc": xc.tolist(),
                    "err_even": float(np.max(np.abs(np.polyval(pe, x) - f(x)))),
                    "err_cheb": float(np.max(np.abs(np.polyval(pc, x) - f(x)))), "n": n}
    return out


def compute_household() -> dict:
    H = TRUTH["household"]
    h = S.household(**H)
    e = S.egm(h)
    ee = S.household_euler_errors(h, e["c"])
    a = h["a"]
    keep = a <= 10
    out = {"a": a[keep].tolist(), "y": h["y"].tolist(), "egm_c": e["c"][keep].tolist(), "egm_iters": e["iters"],
           "egm_seconds": e["seconds"], "egm_ee": ee["max"], "vfi": []}
    for n in (100, 200, 400, 800):
        hh = S.household(**{**H, "n_a": n})
        v = S.household_vfi(hh)
        out["vfi"].append({"n": n, "seconds": v["seconds"], "iters": v["iters"],
                           "ee": S.household_euler_errors(hh, v["c"])["max"]})
        if n == 200:
            out["vfi_c"] = v["c"][keep].tolist()
    return out


def compute_projection() -> dict:
    m = _m()
    rows = []
    for n in range(2, 12):
        c = S.collocation(m, n)
        rows.append({"degree": n - 1, "nodes": n, "ee": _ee(m, c["c"])["max"], "seconds": c["seconds"],
                     "ok": c["ok"]})
    g5 = S.galerkin(m, 5)
    c4 = S.collocation(m, 4)
    k = np.linspace(0.5, 1.5, 301) * m["kss"]
    th = c4["theta"]
    resid = S._residual(th, k, m, c4["lo"], c4["hi"])
    nodes = S.chebyshev_nodes(4, c4["lo"], c4["hi"])
    return {"rows": rows, "galerkin5": _ee(m, g5["c"])["max"], "colloc5": rows[3]["ee"],
            "resid_k": (k / m["kss"]).tolist(), "resid": resid.tolist(), "nodes": (nodes / m["kss"]).tolist()}


def compute_perturb() -> dict:
    m = _m()
    acc = _accurate(m)
    p1, p2 = S.perturbation(m, 1), S.perturbation(m, 2)
    k = np.linspace(0.3, 1.7, 141) * m["kss"]
    true_kp = S.resources(k, m) - acc["c"](k)
    out = {"g1": p1["g1"], "g2": p2["g2"], "k": (k / m["kss"]).tolist(), "accurate": (true_kp / m["kss"]).tolist(),
           "first": (p1["kprime"](k) / m["kss"]).tolist(), "second": (p2["kprime"](k) / m["kss"]).tolist(),
           "ee_first": _ee(m, p1["c"]), "ee_second": _ee(m, p2["c"])}
    # certainty equivalence: the household with income risk against the same household without it
    H = TRUTH["household"]
    risky = S.household(**H)
    safe = S.household(**{**H, "sigma": 1e-4})
    cr = S.egm(risky)["c"]
    cs = S.egm(safe)["c"]
    a = risky["a"]
    keep = a <= 10
    mid = len(risky["y"]) // 2
    out["precaution"] = {"a": a[keep].tolist(), "risky": cr[keep, mid].tolist(), "safe": cs[keep, mid].tolist(),
                         "gap_at_2": float(np.interp(2.0, a, cs[:, mid]) - np.interp(2.0, a, cr[:, mid]))}
    return out


def compute_accuracy() -> dict:
    m = _m()
    rows = []
    g = S.kgrid(m, 1000)
    r = S.vfi(m, g, tol=1e-8)
    pol = lambda k: S.resources(k, m) - np.interp(k, g, r["kprime"])  # noqa: E731
    rows.append(("value iteration, 1,000 grid points", _ee(m, pol), r["seconds"]))
    for kind, gg, name in (("linear", S.kgrid(m, 40), "between points, linear, 40 points"),
                           ("cubic", S.kgrid(m, 40), "between points, cubic spline, 40 points"),
                           ("chebyshev", S.chebyshev_nodes(12, 0.5 * m["kss"], 1.5 * m["kss"]),
                            "between points, Chebyshev, 12 points")):
        rr = S.vfi_continuous(m, gg, kind)
        rows.append((name, _ee(m, rr["c"]), rr["seconds"]))
    for n in (5, 9):
        c = S.collocation(m, n)
        rows.append((f"collocation, degree {n - 1}", _ee(m, c["c"]), c["seconds"]))
    for o in (1, 2):
        t0 = time.perf_counter()
        p = S.perturbation(m, o)
        rows.append((f"perturbation, order {o}", _ee(m, p["c"]), time.perf_counter() - t0))
    table = [{"method": n_, "max": e["max"], "mean": e["mean"], "seconds": s_, "curve": e["log10"]}
             for n_, e, s_ in rows]
    tols = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-8]
    tol_rows = []
    for t in tols:
        rr = S.vfi(m, g, tol=t)
        tol_rows.append({"tol": t, "iters": rr["iters"],
                         "ee": _ee(m, lambda k, rr=rr: S.resources(k, m) - np.interp(k, g, rr["kprime"]))["max"]})
    return {"table": table, "k": _ee(m, lambda k: S.resources(k, m) - np.interp(k, g, r["kprime"]))["k"],
            "tolerance": tol_rows}


def compute_expect() -> dict:
    out = {}
    for rho in (0.9, 0.99):
        sig = 0.01
        true_sd = sig / np.sqrt(1 - rho ** 2)
        rows = {}
        for name, fn in (("tauchen", dp.tauchen), ("rouwenhorst", dp.rouwenhorst)):
            ch = fn(5, rho, sig)
            mo = dp.chain_moments(ch["z"], ch["P"])
            rows[name] = {"rho": mo["rho"], "sd": mo["sd"], "P": np.asarray(ch["P"]).tolist(),
                          "z": np.asarray(ch["z"]).tolist()}
        out[str(rho)] = {"true_sd": true_sd, **rows}
    q = S.quadrature_error(lambda x: np.exp(0.5 * x), float(np.exp(0.125)))
    out["quadrature"] = q
    return out


def compute_hjb() -> dict:
    r = S.hjb_household(**TRUTH["hjb"])
    a = np.array(r["a"])
    g = np.array(r["g"])
    da = a[1] - a[0]
    return {"a": r["a"], "c": r["c"], "s": r["s"], "g": r["g"], "iters": r["iters"], "seconds": r["seconds"],
            "nnz": r["nnz"], "size": r["size"], "dist": r["dist"], "at_limit": float(g[0].sum() * da),
            "low_share": float(g[:, 0].sum() * da), "mean_a": float((a[:, None] * g).sum() * da)}


def compute_zlb() -> dict:
    return S.zlb_occbin(**TRUTH["zlb"])


def compute_dimension() -> dict:
    ds = list(range(1, 21))
    counts = {"d": ds, "tensor5": [S.tensor_count(d, 2) for d in ds], "smolyak2": [S.smolyak_count(d, 2) for d in ds],
              "tensor9": [S.tensor_count(d, 3) for d in ds], "smolyak3": [S.smolyak_count(d, 3) for d in ds]}
    d = 4
    rng = np.random.default_rng(51)
    X = rng.uniform(-1, 1, (300, d))
    f = lambda Z: np.exp(-0.5 * np.sum(np.atleast_2d(Z) ** 2, axis=1))  # noqa: E731
    fx = f(X)
    rows = []
    for mu in (1, 2, 3, 4):
        r = S.smolyak_interpolate(f, d, mu, X)
        rows.append({"kind": "smolyak", "level": mu, "points": r["points"],
                     "err": float(np.max(np.abs(r["values"] - fx))),
                     "rms": float(np.sqrt(np.mean((r["values"] - fx) ** 2)))})
    for lev in (2, 3, 4):
        r = S.tensor_interpolate(f, d, lev, X)
        rows.append({"kind": "tensor", "level": lev, "points": r["points"],
                     "err": float(np.max(np.abs(r["values"] - fx))),
                     "rms": float(np.sqrt(np.mean((r["values"] - fx) ** 2)))})
    return {"counts": counts, "interp": rows, "d": d}


def compute_reproduce() -> dict:
    f = lambda x: np.exp(0.5 * x)  # noqa: E731
    est = {}
    for name, seed in (("seed 0", 0), ("seed 0, again", 0), ("seed 1", 1)):
        rng = np.random.default_rng(seed)
        est[name] = float(f(rng.standard_normal(10000)).mean())
    # a test with a known answer: Brock and Mirman's economy (log utility, full depreciation) has k' = alpha beta k^a
    bm = S.growth(alpha=0.36, beta=0.96, delta=1.0, gamma=1.0)
    c = S.collocation(bm, 9)
    k = np.linspace(0.6, 1.4, 201) * bm["kss"]
    exact = (1 - bm["alpha"] * bm["beta"]) * k ** bm["alpha"]
    g = S.kgrid(bm, 500)
    v = S.vfi(bm, g, tol=1e-9)
    vf = S.resources(k, bm) - np.interp(k, g, v["kprime"])
    return {"exact": float(np.exp(0.125)), "estimates": est,
            "bm_colloc_err": float(np.max(np.abs(c["c"](k) / exact - 1))),
            "bm_vfi_err": float(np.max(np.abs(vf / exact - 1))), "bm_share": 1 - bm["alpha"] * bm["beta"]}


def compute_dials() -> dict:
    out = []
    for gam in TRUTH["gammas"]:
        m = S.growth(**{**TRUTH["growth"], "gamma": gam})
        c = S.collocation(m, 9)
        k0 = 0.8 * m["kss"]
        out.append({"gamma": gam, "eis": 1 / gam, "c_at": float(c["c"](k0)), "kss": m["kss"],
                    "ee": _ee(m, c["c"])["max"],
                    "speed": float(1 - S.perturbation(m, 1)["g1"])})
    base = out[1]["c_at"]
    for r in out:
        r["diff_pct"] = 100 * (r["c_at"] / base - 1)
    return {"rows": out}


def compute_frontier() -> dict:
    m = _m()
    r = S.collocation_derivative(m, 8, "beta")
    return {**r, "beta": m["beta"]}


def film_time(t: float, first: float = 1971.0, last: float = 2021.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    T = data.transistors()
    y = T["year"]
    v = T["transistors"]
    lv = np.log10(v)
    slope = np.polyfit(y, lv, 1)[0]
    return {"t": y, "v": v, "log10": lv.tolist(), "times": [film_time(t) for t in y], "first": v[0], "last": v[-1],
            "doubling_years": float(np.log10(2) / slope), "ratio": float(v[-1] / v[0])}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["log10"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=10, log=False, low=40, high=88)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.3, "hz": score.hz(nn), "name": f"{10 ** x:.3g}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "transistors per microprocessor, 1971-2021 (Rupp, via Our World in Data), log scale, as "
                               "a tune (computed)", "kind": "synthesized"})
    ClipStore("econ51").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "growth": compute_growth,
    "grids": compute_grids,
    "interp": compute_interp,
    "household": compute_household,
    "projection": compute_projection,
    "perturb": compute_perturb,
    "accuracy": compute_accuracy,
    "expect": compute_expect,
    "hjb": compute_hjb,
    "zlb": compute_zlb,
    "dimension": compute_dimension,
    "reproduce": compute_reproduce,
    "dials": compute_dials,
    "frontier": compute_frontier,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

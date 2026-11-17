"""Precompute every number in Part 25 of *Psychology, Built* ("Deciding in Time").

    python -m videos.psychology.psych25.compute            # everything missing (a few minutes; fetches data once)
    python -m videos.psychology.psych25.compute --force selective

Results are cached in ``.cache/psych25/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.decide``, with Part 1's ex-Gaussian from ``chronometry``).  The data are
Wagenmakers, Ratcliff, Gomez and McKoon's (2008) speed-accuracy lexical decisions and Ratcliff and Rouder's (1998)
brightness judgements, both as packaged in the R package rtdists and fetched by ``explainer.psychology.opendata``.
Simulations use fixed seeds; where a part shows one run of many, it is the run of median length, chosen by rule.
Times are in seconds.

Items:
    sprt         Wald's test on a coin: one run (the median-length one of 101), Wald's bounds, the operating
                 characteristic and average sample number against the fixed-sample test, checked by simulation
    hick         a race of n accumulators held to 90% accuracy: the bound and the mean time against log2 n
    fitts        iterative corrections: submovements needed against Fitts's index of difficulty
    ddm          sample paths; first-passage densities against a simulation; the closed forms; the speed-accuracy
                 curve as the bound moves
    shape        one person's response times (the median person of 17, by mean time): histogram, quantiles,
                 ex-Gaussian fit; two distributions with the same mean
    selective    17 people, speed against accuracy: per-person fits under four models and their AICs
    rr98         3 people, 33 brightness levels: psychometric and chronometric functions with a diffusion fit
    variability  correct and error times with no variability, drift variability, start variability; the data's
                 fast and slow errors
    brain        accumulators averaged by strength, aligned to the stimulus and the response; a stepping model
    lba          the linear ballistic accumulator: densities against a simulation
    stop         the stop-signal race: inhibition function, signal-respond times, the integration method
    confidence   the balance of evidence in a two-accumulator race, for correct and error trials
    urgency      fixed against collapsing bounds: the distributions they produce
    addm         value-based choice with attention: gaze advantage against choice, one trial's path
    traits       test-retest reliability of a fitted drift against the number of trials
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import opendata
from explainer.psychology.psyche import chronometry as C
from explainer.psychology.psyche import decide as D

CACHE = Cache("psych25")
load = CACHE.load


def compute_sprt() -> dict:
    p0, p1, alpha, beta = 0.5, 0.7, 0.05, 0.05
    A, B = D.wald_bounds(alpha, beta)
    rng = np.random.default_rng(25)
    runs = [D.sprt_bernoulli(rng.random(400) < 0.7, p0, p1, alpha, beta) for _ in range(101)]
    order = np.argsort([r["n"] for r in runs], kind="stable")
    ex = runs[order[50]]  # the median-length run, chosen by rule
    ps = np.linspace(0.4, 0.8, 41)
    oc, asn = np.array([D.sprt_oc_asn(p, p0, p1, alpha, beta) for p in ps]).T
    sims = {p: D.sprt_simulate(p, p0, p1, alpha, beta, reps=20000, seed=7) for p in (0.5, 0.6, 0.7)}
    nf = D.fixed_n(p0, p1, alpha, beta)
    return {"p0": p0, "p1": p1, "A": A, "B": B, "path": ex["path"], "n": ex["n"], "decision": ex["decision"],
            "ps": ps, "oc": oc, "asn": asn, "fixed_n": nf,
            "sim_p": np.array(list(sims)), "sim_accept": np.array([s["accept_h1"] for s in sims.values()]),
            "sim_mean_n": np.array([s["mean_n"] for s in sims.values()]),
            "asn_h0": float(D.sprt_oc_asn(p0, p0, p1, alpha, beta)[1]),
            "asn_h1": float(D.sprt_oc_asn(p1, p0, p1, alpha, beta)[1])}


def compute_hick() -> dict:
    r = D.race_hick(ns=(2, 4, 8, 16), target=0.9, v_correct=2.0, seed=1, n=3000)
    bits = np.log2(r["n"])
    slope, icpt = np.polyfit(bits, r["mean_dt"], 1)
    resid = r["mean_dt"] - (icpt + slope * bits)
    return {**r, "bits": bits, "slope": slope, "intercept": icpt, "max_resid": float(np.abs(resid).max())}


def compute_fitts() -> dict:
    """Crossman and Goodeve's (1963) iterative corrections: each submovement leaves a fixed share r of the
    remaining distance, so the number needed to land within W/2 of a target D away is log(2D/W) / log(1/r)."""
    r = 0.25
    ID = np.linspace(1.0, 7.0, 121)  # log2(2D/W), bits
    k_exact = ID / np.log2(1 / r)
    k_steps = np.ceil(k_exact - 1e-9)
    path_D, path_W = 8.0, 0.5
    pts = [path_D]
    while pts[-1] > path_W / 2:
        pts.append(pts[-1] * r)
    return {"r": r, "ID": ID, "k_exact": k_exact, "k_steps": k_steps, "path_D": path_D, "path_W": path_W,
            "remaining": np.array(pts), "path_ID": float(np.log2(2 * path_D / path_W))}


def compute_ddm() -> dict:
    v, a, w, t0 = 1.5, 1.2, 0.5, 0.3
    rng = np.random.default_rng(3)
    dt = 0.002
    paths = []
    for _ in range(12):
        x, xs = a * w, [a * w]
        while 0 < x < a and len(xs) < 3000:
            x += v * dt + np.sqrt(dt) * rng.standard_normal()
            xs.append(min(max(x, 0.0), a))
        paths.append(np.array(xs))
    t = np.linspace(0.001, 2.0, 400)
    up = D.fpt_density(t, v, a, w, "upper")
    lo = D.fpt_density(t, v, a, w, "lower")
    rt, hit = D.simulate(v, a, w, 0.0, n=40000, seed=4, dt=0.0005)
    edges = np.linspace(0, 2.0, 41)
    h_up = np.histogram(rt[hit], edges)[0] / (len(rt) * np.diff(edges))
    h_lo = np.histogram(rt[~hit], edges)[0] / (len(rt) * np.diff(edges))
    a_grid = np.linspace(0.3, 2.6, 60)
    sat_acc = D.p_upper(v, a_grid, 0.5)
    sat_rt = D.mean_dt(v, a_grid, 0.5) + t0
    return {"v": v, "a": a, "w": w, "t0": t0, "dt": dt, "paths": np.array([np.pad(p, (0, 3001 - len(p)),
                                                                                 constant_values=np.nan)
                                                                          for p in paths]),
            "path_len": np.array([len(p) for p in paths]), "t": t, "up": up, "lo": lo, "edges": edges,
            "h_up": h_up, "h_lo": h_lo, "p_upper": float(D.p_upper(v, a, w)), "mean_dt": float(D.mean_dt(v, a, w)),
            "sim_p_upper": float(hit.mean()), "sim_mean_dt": float(np.mean(rt)),
            "cond_up": D.cond_mean_dt(v, a, w, "upper"), "cond_lo": D.cond_mean_dt(v, a, w, "lower"),
            "a_grid": a_grid, "sat_acc": sat_acc, "sat_rt": sat_rt}


def _people():
    d = opendata.speed_acc()
    ids = sorted(set(d["id"]), key=int)
    return d, ids


def compute_shape() -> dict:
    d, ids = _people()
    acc = ~d["speed"]
    means = np.array([d["rt"][acc & d["correct"] & (d["id"] == i)].mean() for i in ids])
    k = int(np.argsort(means, kind="stable")[len(ids) // 2])  # the median person, by mean time, chosen by rule
    who = ids[k]
    rt = d["rt"][acc & d["correct"] & (d["id"] == who)]
    fit = C.fit_exgauss(1000 * rt)
    edges = np.linspace(0.2, 2.0, 46)
    hist = np.histogram(rt, edges)[0] / (len(rt) * np.diff(edges))
    t = np.linspace(0.2, 2.0, 300)
    pdf = C.exgauss_pdf(1000 * t, fit["mu"], fit["sigma"], fit["tau"]) * 1000
    q = np.quantile(rt, [0.1, 0.3, 0.5, 0.7, 0.9])
    # two distributions with the same mean: a normal, and an ex-Gaussian with most of its spread in the tail
    m = float(rt.mean())
    same_t = np.linspace(0.2, 2.0, 300)
    norm = np.exp(-0.5 * ((same_t - m) / 0.12) ** 2) / (0.12 * np.sqrt(2 * np.pi))
    tau2 = 0.25
    skew = C.exgauss_pdf(1000 * same_t, 1000 * (m - tau2), 40.0, 1000 * tau2) * 1000
    return {"who": who, "n_people": len(ids), "n": len(rt), "rt": rt, "edges": edges, "hist": hist, "t": t,
            "pdf": pdf, "mu": fit["mu"] / 1000, "sigma": fit["sigma"] / 1000, "tau": fit["tau"] / 1000,
            "mean": m, "median": float(np.median(rt)), "q": q, "same_t": same_t, "norm": norm, "skew": skew}


MODELS = {"bound": ("a",), "drift": ("v",), "bound and t0": ("a", "t0"), "all three": ("v", "a", "t0")}


def compute_selective() -> dict:
    d, ids = _people()
    out = {"ids": np.array(ids), "models": np.array(list(MODELS))}
    aic = np.zeros((len(ids), len(MODELS)))
    par = np.zeros((len(ids), 2, 3))  # person, (speed, accuracy), (v, a, t0) from the all-free model
    pc = np.zeros((len(ids), 2))
    mrt = np.zeros((len(ids), 2))
    fast_err = np.zeros((len(ids), 2))
    for k, i in enumerate(ids):
        data = {}
        for j, sp in enumerate((True, False)):
            m = (d["id"] == i) & (d["speed"] == sp)
            data["speed" if sp else "accuracy"] = (d["rt"][m], d["correct"][m])
            pc[k, j] = d["correct"][m].mean()
            mrt[k, j] = d["rt"][m].mean()
            fast_err[k, j] = np.median(d["rt"][m & ~d["correct"]]) - np.median(d["rt"][m & d["correct"]])
        for jm, free in enumerate(MODELS.values()):
            f = D.fit_conditions(data, free, fix={"w": 0.5})
            aic[k, jm] = f["aic"]
            if free == ("v", "a", "t0"):
                for j, c in enumerate(("speed", "accuracy")):
                    par[k, j] = [f["params"][c][p] for p in ("v", "a", "t0")]
    best = aic.argmin(1)
    out.update(aic=aic, best=best, params=par, pc=pc, mrt=mrt, err_minus_correct=fast_err,
               bound_beats_drift=int((aic[:, 0] < aic[:, 1]).sum()),
               a_lower_speed=int((par[:, 0, 1] < par[:, 1, 1]).sum()),
               a_ratio=float(np.median(par[:, 0, 1] / par[:, 1, 1])),
               v_ratio=float(np.median(par[:, 0, 0] / par[:, 1, 0])),
               t0_lower_speed=int((par[:, 0, 2] < par[:, 1, 2]).sum()),
               wins=np.bincount(best, minlength=len(MODELS)),
               fast_errors_speed=int((fast_err[:, 0] < 0).sum()), slow_errors_accuracy=int((fast_err[:, 1] > 0).sum()))
    return out


BINS = [np.arange(k * 4, k * 4 + 4) for k in range(8)]  # strength 0-31 in eight bins of four (32 joins the last)
BINS[-1] = np.arange(28, 33)


def compute_rr98() -> dict:
    d = opendata.rr98()
    ids = sorted(set(d["id"]))
    nb = len(BINS)
    obs_p = np.zeros((len(ids), 2, nb))
    obs_rt = np.zeros((len(ids), 2, nb))
    mod_p = np.zeros_like(obs_p)
    mod_rt = np.zeros_like(obs_rt)
    pars = []
    for k, i in enumerate(ids):
        data = {}
        for j, sp in enumerate((True, False)):
            for b, bin_ in enumerate(BINS):
                m = (d["id"] == i) & (d["speed"] == sp) & np.isin(d["strength"], bin_)
                obs_p[k, j, b] = d["said_light"][m].mean()
                obs_rt[k, j, b] = d["rt"][m].mean()
                data[(j, b)] = (d["rt"][m], d["said_light"][m])
        f = _fit_rr98(data, nb)
        pars.append(f)
        for j in range(2):
            for b in range(nb):
                v, a, w, t0 = f["v"][b], f["a"][j], f["w"][j], f["t0"][j]
                mod_p[k, j, b] = D.p_upper(v, a, w)
                mod_rt[k, j, b] = D.mean_dt(v, a, w) + t0
    return {"ids": np.array(ids), "bin_mid": np.array([b.mean() for b in BINS]), "obs_p": obs_p, "obs_rt": obs_rt,
            "mod_p": mod_p, "mod_rt": mod_rt, "v": np.array([p["v"] for p in pars]),
            "a": np.array([p["a"] for p in pars]), "w": np.array([p["w"] for p in pars]),
            "t0": np.array([p["t0"] for p in pars]), "n": len(d["rt"])}


def _fit_rr98(data, nb):
    """Stimulus-coded fit (upper = 'light'): a drift per brightness bin shared by both instructions; a bound, a
    start and a non-decision time per instruction (speed, accuracy)."""
    from scipy import optimize

    mins = [min(np.min(data[(j, b)][0]) for b in range(nb)) for j in range(2)]
    x0 = list(np.linspace(-2.5, 2.5, nb)) + [0.8, 1.6, 0.5, 0.5, 0.8 * mins[0], 0.8 * mins[1]]

    def nll(x):
        v, a, w, t0 = x[:nb], x[nb:nb + 2], x[nb + 2:nb + 4], x[nb + 4:]
        return sum(D.neg_loglik([v[b], a[j], w[j], t0[j]], *data[(j, b)]) for j in range(2) for b in range(nb))

    res = optimize.minimize(nll, x0, method="Powell", options={"maxiter": 40000, "xtol": 1e-4, "ftol": 1e-6})
    x = res.x
    return {"v": x[:nb], "a": x[nb:nb + 2], "w": x[nb + 2:nb + 4], "t0": x[nb + 4:], "nll": float(res.fun)}


def compute_variability() -> dict:
    v, a, w = 1.0, 1.2, 0.5
    cases = {"none": {}, "drift varies": {"sv": 1.2}, "start varies": {"sw": 0.6}}
    out = {"cases": np.array(list(cases))}
    mc, me, acc = [], [], []
    for name, kw in cases.items():
        rt, up = D.simulate(v, a, w, 0.0, n=60000, seed=11, dt=0.0005, **kw)
        ok = np.isfinite(rt)
        mc.append(rt[ok & up].mean())
        me.append(rt[ok & ~up].mean())
        acc.append(up[ok].mean())
    out.update(mean_correct=np.array(mc), mean_error=np.array(me), acc=np.array(acc))
    return out


def compute_brain() -> dict:
    r = D.aligned_means([0.0, 0.8, 1.6, 3.2], a=2.0, n=1500, seed=2)
    s = D.stepping(n=600, seed=3)
    return {**r, "vs": np.array([0.0, 0.8, 1.6, 3.2]), "step_t": s["t"], "step_trials": s["trials"][:6],
            "step_mean": s["mean"]}


def compute_lba() -> dict:
    vs, A, b, s, t0 = [1.2, 0.8], 0.5, 1.0, 0.3, 0.2
    t = np.linspace(0.2, 2.5, 300)
    f0 = D.lba_defective(t, 0, vs, A, b, s, t0)
    f1 = D.lba_defective(t, 1, vs, A, b, s, t0)
    rt, win = D.lba_simulate(vs, A, b, s, t0, n=50000, seed=5)
    edges = np.linspace(0.2, 2.5, 47)
    h0 = np.histogram(rt[win == 0], edges)[0] / (50000 * np.diff(edges))
    h1 = np.histogram(rt[win == 1], edges)[0] / (50000 * np.diff(edges))
    return {"vs": np.array(vs), "A": A, "b": b, "s": s, "t0": t0, "t": t, "f0": f0, "f1": f1, "edges": edges,
            "h0": h0, "h1": h1, "p0": float((win == 0).mean())}


def compute_stop() -> dict:
    rng = np.random.default_rng(13)
    go = 0.25 + rng.gamma(4.0, 0.06, 100000)  # a go distribution, mean 0.49 s
    ssrt = 0.22
    ssds = np.linspace(0.0, 0.5, 26)
    r = D.stop_race(go, ssds, ssrt, ssrt_sd=0.03, seed=14)
    est = np.array([D.ssrt_integration(go, s_, p) if 0.1 < p < 0.9 else np.nan
                    for s_, p in zip(r["ssd"], r["p_respond"])])
    edges = np.linspace(0.2, 1.4, 49)
    go_h = np.histogram(go, edges)[0] / (len(go) * np.diff(edges))
    return {**r, "ssrt": ssrt, "estimates": est, "go_mean": float(go.mean()), "edges": edges, "go_hist": go_h}


def compute_confidence() -> dict:
    v = np.linspace(0.2, 3.2, 13)
    out = D.race_confidence(v, b=2.0, n=3000, seed=17)
    return {**out, "b": 2.0, "conf_correct": out["conf_correct"] / 2.0, "conf_error": out["conf_error"] / 2.0}


def compute_urgency() -> dict:
    fixed = lambda t: 1.0  # noqa: E731
    collapse = lambda t: 1.0 * (1 - 0.8 * t / (t + 0.5))  # noqa: E731
    out = {}
    edges = np.linspace(0.2, 3.0, 57)
    for name, fn in (("fixed", fixed), ("collapsing", collapse)):
        rt, up = D.simulate_bound(0.8, fn, t0=0.3, n=30000, seed=19, dt=0.001)
        ok = np.isfinite(rt)
        out[name + "_hist"] = np.histogram(rt[ok], edges)[0] / (ok.sum() * np.diff(edges))
        out[name + "_acc"] = float(up[ok].mean())
        out[name + "_mean"] = float(rt[ok].mean())
        out[name + "_skew"] = float(((rt[ok] - rt[ok].mean()) ** 3).mean() / rt[ok].std() ** 3)
    tb = np.linspace(0, 2.5, 100)
    out.update(edges=edges, tb=tb, bound_fixed=np.ones_like(tb), bound_collapse=collapse(tb))
    return out


def compute_addm() -> dict:
    r = D.addm(3.0, 3.0, n=3000, seed=21)
    adv = r["left_advantage"]
    edges = np.array([-1.2, -0.6, -0.3, -0.1, 0.1, 0.3, 0.6, 1.2])
    mids, p, cnt = [], [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (adv >= lo) & (adv < hi)
        if m.sum() >= 30:
            mids.append((lo + hi) / 2)
            p.append(r["choice_left"][m].mean())
            cnt.append(int(m.sum()))
    last = float(np.mean(r["choice_left"] == r["last_left"]))
    rng = np.random.default_rng(5)
    # one trial's path, for the picture: alternating looks, drift by which item is looked at
    dt, x, t, left, path, looks = 0.005, 0.0, 0.0, True, [(0.0, 0.0)], []
    v_l, v_r, dd, th = 4.0, 2.0, 0.4, 0.3
    while abs(x) < 1.0 and t < 4:
        dur = max(0.15, rng.exponential(0.45))
        t_start = t
        mu = dd * (v_l - th * v_r) if left else dd * (th * v_l - v_r)
        for _ in range(int(dur / dt)):
            x += mu * dt + np.sqrt(dt) * rng.standard_normal()
            t += dt
            path.append((t, x))
            if abs(x) >= 1.0:
                break
        looks.append((t_start, t, left))
        left = not left
    return {"adv_mid": np.array(mids), "p_left": np.array(p), "count": np.array(cnt), "p_last": last,
            "path": np.array(path), "looks": np.array([[a, b, float(c)] for a, b, c in looks])}


def compute_traits() -> dict:
    return D.retest(n_people=100, trials=(20, 50, 100, 200, 500), seed=23)


ITEMS = {
    "sprt": compute_sprt,
    "hick": compute_hick,
    "fitts": compute_fitts,
    "ddm": compute_ddm,
    "shape": compute_shape,
    "selective": compute_selective,
    "rr98": compute_rr98,
    "variability": compute_variability,
    "brain": compute_brain,
    "lba": compute_lba,
    "stop": compute_stop,
    "confidence": compute_confidence,
    "urgency": compute_urgency,
    "addm": compute_addm,
    "traits": compute_traits,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

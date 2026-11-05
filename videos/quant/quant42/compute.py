"""Every number in Part 42 (Machines in the Market), computed and cached in .cache/quant42/.

    python -m videos.quant.quant42.compute [items] [--force]

Data: Kenneth French's daily US market return, 1926-2020 (the research window), for the stylised facts. Everything
else is simulation, with fixed seeds: an artificial market of fundamentalists and chartists, Kirman's ant model, a
dealer market with a learning market maker, Calvano et al.'s pricing game with Q-learners, and a crowd sharing one
model.

* ``facts``      a Franke-Westerhoff-type market against the US market and a Gaussian: kurtosis, tail exponent,
                 autocorrelations of returns and of their size; a sample path with the chartists' share;
* ``kirman``     the ant model: paths for herding and for independent agents, and the exact stationary law against
                 its Beta limit and a long simulation;
* ``maker``      the dealer market: every fixed quote rule, a Q-learning market maker, policies trained at one level of
                 informed trading and tested at others, and the bias of evaluating a quote rule on another rule's tape;
* ``collusion``  two Q-learners in Calvano et al.'s logit game: the collusion index by discount factor and by profit
                 noise, the prices after a forced deviation, the one-shot points;
* ``sessions``   session by session at delta = 0.95: the price pair each settles on, and whether it punishes;
* ``crowd``      a crowd mixing a shared model with its own signals: flow variance against its formula, volatility,
                 and the day the shared model errs;
* ``research``   the repeated-game threshold for grim trigger and for T-period punishments, against what the learners
                 do: below and above the threshold, and how long they punish.
"""

from __future__ import annotations

import json
import math
import warnings

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import agents as A, pit

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant42")
load = pit.counted(CACHE.load, 42)


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def compute_facts() -> dict:
    km = data.ken_french_daily(through="2020-12-31")
    real = A.stylized(km["mkt"])
    m = A.fw_model(T=24000, seed=7)
    sim = A.stylized(m["r"])
    g = np.random.default_rng(7).standard_normal(24000)
    gau = A.stylized(g)
    w = slice(4000, 6000)
    # the method of simulated moments, on a grid of the chartists' extrapolation and noise: match the market's excess
    # kurtosis and its lag-20 autocorrelation of |r|, each scaled by its value
    target = np.array([real["kurt"], real["acf_abs"][4]])
    chis = np.round(np.linspace(1.5, 3.1, 9), 2)
    sigs = np.round(np.linspace(1.6, 3.6, 9), 2)
    L = np.zeros((len(chis), len(sigs)))
    for i, ch in enumerate(chis):
        for j, sg in enumerate(sigs):
            st = A.stylized(A.fw_model(T=24000, chi=float(ch), sig_c=float(sg), seed=11)["r"])
            m_ = np.array([st["kurt"], st["acf_abs"][4]])
            L[i, j] = float(np.sum(((m_ - target) / target) ** 2))
    i, j = np.unravel_index(int(np.argmin(L)), L.shape)
    best = A.stylized(A.fw_model(T=24000, chi=float(chis[i]), sig_c=float(sigs[j]), seed=11)["r"])
    near = int(np.sum(L <= 2 * L.min() + 0.02))
    return _json({"real": real, "sim": sim, "gauss": gau, "n_real": len(km["mkt"]),
                  "path": {"r": m["r"][w], "nf": m["nf"][w]}, "real_path": km["mkt"][-2000:],
                  "msm": {"chis": chis, "sigs": sigs, "L": L, "best": {"chi": float(chis[i]), "sig_c": float(sigs[j]),
                          "kurt": best["kurt"], "acf20": best["acf_abs"][4], "loss": float(L.min())}, "near": near,
                          "target": target}})


def compute_kirman() -> dict:
    N = 100
    herd = A.kirman(N, 0.002, 0.01, 400_000, seed=1)[::200]
    indep = A.kirman(N, 0.02, 0.01, 400_000, seed=1)[::200]
    out = {"N": N, "herd": herd / N, "indep": indep / N}
    for name, eps in (("bi", 0.002), ("uni", 0.02)):
        pi = A.kirman_stationary(N, eps, 0.01)
        a = A.kirman_alpha(N, eps, 0.01)
        from scipy.stats import beta as B
        x = (np.arange(N + 1) + 0.5) / (N + 1)
        bl = B.pdf(np.clip(x, 1e-3, 1 - 1e-3), a, a)
        bl = bl / bl.sum()
        sim = A.kirman(N, eps, 0.01, 40_000_000, seed=2)[100_000:]
        h = np.bincount(sim, minlength=N + 1) / len(sim)
        bb = A.betabinom_pmf(N, a)
        out[name] = {"eps": eps, "alpha": a, "exact": pi, "beta": bl, "sim": h, "bb": bb,
                     "tv_exact_sim": float(0.5 * np.abs(pi - h).sum()),
                     "tv_exact_beta": float(0.5 * np.abs(pi - bl).sum()),
                     "max_exact_bb": float(np.abs(pi - bb).max()), "p_edges": float(pi[0] + pi[-1])}
    # a market driven by the herd: price = fundamental noise + sentiment (2x - 1), sampled every N steps
    x = A.kirman(N, 0.002, 0.01, 4_000_000, seed=5)[::N] / N
    rng = np.random.default_rng(5)
    r_h = 0.02 * np.diff(2 * x - 1) + 0.002 * rng.standard_normal(len(x) - 1)
    x2 = A.kirman(N, 0.02, 0.01, 4_000_000, seed=5)[::N] / N
    r_i = 0.02 * np.diff(2 * x2 - 1) + 0.002 * rng.standard_normal(len(x2) - 1)
    out["market"] = {"herd": A.stylized(r_h), "indep": A.stylized(r_i), "r_herd": r_h[:3000], "r_indep": r_i[:3000]}
    # how long the crowd stays: the exact mean time to swing from 90% to 10% holding A, against simulation
    sw = {}
    for name, eps in (("bi", 0.002), ("uni", 0.02)):
        th = A.kirman_passage(N, eps, 0.01, 90, 10)
        path = A.kirman(N, eps, 0.01, 60_000_000, seed=8)[::10]     # sampled every 10 steps
        times, start = [], None
        for t_, kk in enumerate(path.tolist()):    # each passage: from the first visit at 90 or more to 10 or fewer
            if start is None and kk >= 90:
                start = t_
            elif start is not None and kk <= 10:
                times.append(10 * (t_ - start))
                start = None
        sw[name] = {"theory": th, "sim": float(np.mean(times)) if times else float("nan"), "n": len(times)}
    out["swing"] = sw
    out["cascade"] = [{"p": p_, **A.cascade_theory(p_), "sim": A.cascade_sim(p_, seed=4)} for p_ in (0.6, 0.7, 0.8, 0.9)]
    # the edges converge slowly: P(k in {0, N}) under beta-binomial for growing N at alpha = 0.2
    out["edges"] = [{"N": n_, "p": float(A.betabinom_pmf(n_, 0.2)[[0, -1]].sum())} for n_ in (100, 1000, 10000)]
    return _json(out)


def compute_maker() -> dict:
    pis = (0.05, 0.15, 0.3)
    fixed = {}
    for pi in pis:
        row = []
        for h, k in A.MAKER_ACTIONS:
            a = A.MAKER_ACTIONS.index((h, k))
            r = A.run_maker(A.DealerEnv(pi_inf=pi, seed=11), lambda s, a=a: a, 400)
            row.append({"half": h, "skew": k, "mean": r["mean"], "se": r["se"]})
        fixed[str(pi)] = row
    pols = {}
    curve = []
    snaps = (500, 1000, 2000, 4000, 8000, 12000, 16000, 20000)
    for pi in (0.05, 0.3):
        Q = A.q_maker(A.DealerEnv(pi_inf=pi, seed=21), episodes=24000, alpha=0.02, seed=3,
                      snapshots=snaps if pi == 0.05 else ())
        pols[str(pi)] = Q
        if pi == 0.05:
            for ep, Qs in sorted(A.q_maker.snaps.items()):
                r = A.run_maker(A.DealerEnv(pi_inf=0.05, seed=51), lambda s, Qs=Qs: int(np.argmax(Qs[s])), 200)
                curve.append({"episodes": ep, "mean": r["mean"], "se": r["se"]})
            r = A.run_maker(A.DealerEnv(pi_inf=0.05, seed=51), lambda s, Q=Q: int(np.argmax(Q[s])), 200)
            curve.append({"episodes": 24000, "mean": r["mean"], "se": r["se"]})
    a_best = A.MAKER_ACTIONS.index((3, 1))
    path = A.maker_path(A.DealerEnv(pi_inf=0.15, seed=61), lambda s: a_best)
    cross = {}
    for tr, Q in pols.items():
        pol = lambda s, Q=Q: int(np.argmax(Q[s]))
        cross[tr] = {str(te): A.run_maker(A.DealerEnv(pi_inf=te, seed=31), pol, 400) for te in pis}
    Q = pols["0.05"]
    env = A.DealerEnv()
    mi = env.max_inv
    grid = []
    for inv in range(-mi, mi + 1):
        s = (inv + mi) * 3 + 1
        h, k = A.MAKER_ACTIONS[int(np.argmax(Q[s]))]
        grid.append({"inv": inv, "half": h, "skew": k})
    # a backtest is not an environment: record the tape of half-spread 2, evaluate half-spread 4 on it naively
    a2, a4 = A.MAKER_ACTIONS.index((2, 1)), A.MAKER_ACTIONS.index((4, 1))
    env = A.DealerEnv(pi_inf=0.15, seed=41)
    naive, live2 = [], []
    for _ in range(400):
        env.reset(record=True)
        done, R = False, 0.0
        while not done:
            _, r, done = env.step(*A.MAKER_ACTIONS[a2])
            R += r
        live2.append(R)
        naive.append(R + 2 * len(env.tape))      # the same fills, two ticks better each
    live4 = A.run_maker(A.DealerEnv(pi_inf=0.15, seed=41), lambda s: a4, 400)
    return _json({"fixed": fixed, "cross": cross, "grid": grid, "pis": pis, "curve": curve, "path": path,
                  "replay": {"live2": float(np.mean(live2)), "naive4": float(np.mean(naive)), "live4": live4["mean"]}})


def compute_collusion() -> dict:
    pts = A.bertrand_points()
    out = {"p_nash": pts["p_nash"], "p_mon": pts["p_mon"], "pi_nash": pts["pi_nash"], "pi_mon": pts["pi_mon"]}

    def summarise(c, S):
        ds, ps, lens = [], [], []
        for s in range(S):
            g = A.greedy_cycle(c["Q"][s], int(c["state"][s]), c["k"], c["R"])
            ds.append(A.delta_index(float(g["profit"].mean()), pts["pi_nash"], pts["pi_mon"]))
            ps.append(float(np.mean([c["grid"][i] for pr in g["prices"] for i in pr])))
            lens.append(g["len"])
        return {"delta": float(np.mean(ds)), "delta_q": np.quantile(ds, [0.1, 0.5, 0.9]), "price": float(np.mean(ps)),
                "cycle1": float(np.mean(np.array(lens) == 1)), "all": ds}
    S = 96
    by_delta = []
    keep = None
    for d in (0.0, 0.25, 0.5, 0.75, 0.9, 0.95):
        c = A.calvano(sessions=S, iters=1_500_000, beta=4e-6, delta=d, seed=5)
        by_delta.append({"delta_disc": d, **summarise(c, S)})
        if d == 0.95:
            keep = c
    by_noise = []
    for nz in (0.0, 0.05, 0.1, 0.2):
        c = keep if nz == 0.0 else A.calvano(sessions=S, iters=1_500_000, beta=4e-6, delta=0.95, noise=nz, seed=6)
        by_noise.append({"noise": nz, **summarise(c, S)})
    # the average response to a forced one-period deviation, over sessions whose greedy play is a fixed point
    irs = []
    for s in range(S):
        g = A.greedy_cycle(keep["Q"][s], int(keep["state"][s]), keep["k"], keep["R"])
        if g["len"] == 1:
            irs.append(A.impulse(keep["Q"][s], int(keep["state"][s]), keep["k"], keep["R"], keep["grid"]))
    ir1 = np.mean([x["p1"] for x in irs], 0)
    ir2 = np.mean([x["p2"] for x in irs], 0)
    out.update({"by_delta": by_delta, "by_noise": by_noise, "ir1": ir1, "ir2": ir2, "n_ir": len(irs),
                "grid": keep["grid"], "sessions": S})
    return _json(out)


def compute_sessions() -> dict:
    """Session by session at delta = 0.95: where each pair of learners settles, and whether it punishes."""
    pts = A.bertrand_points()
    S = 96
    c = A.calvano(sessions=S, iters=1_500_000, beta=4e-6, delta=0.95, seed=5)
    out = []
    for s in range(S):
        g = A.greedy_cycle(c["Q"][s], int(c["state"][s]), c["k"], c["R"])
        p1 = float(np.mean([c["grid"][a] for a, _ in g["prices"]]))
        p2 = float(np.mean([c["grid"][b] for _, b in g["prices"]]))
        row = {"p1": p1, "p2": p2, "len": g["len"],
               "delta": A.delta_index(float(g["profit"].mean()), pts["pi_nash"], pts["pi_mon"])}
        if g["len"] == 1:
            ir = A.impulse(c["Q"][s], int(c["state"][s]), c["k"], c["R"], c["grid"])
            row["punish"] = bool(ir["p2"][2] < ir["p2"][0] - 1e-9)
            row["returns"] = bool(abs(ir["p2"][-1] - ir["p2"][0]) < 1e-9 and abs(ir["p1"][-1] - ir["p1"][0]) < 1e-9)
        out.append(row)
    fixed_pts = [x for x in out if x["len"] == 1]
    return _json({"rows": out, "p_nash": pts["p_nash"], "p_mon": pts["p_mon"], "S": S,
                  "n_fixed": len(fixed_pts), "punish": float(np.mean([x["punish"] for x in fixed_pts])),
                  "returns": float(np.mean([x["returns"] for x in fixed_pts])),
                  "symmetric": float(np.mean([abs(x["p1"] - x["p2"]) < 1e-9 for x in out]))})


def compute_crowd() -> dict:
    rows = []
    for sh in (0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0):
        c = A.crowd(N=100, share=sh, T=5000, model_err=4.0, seed=9)
        base = A.crowd(N=100, share=0.0, T=5000, seed=9)["vol"]
        rows.append({"share": sh, "flow_var": c["flow_var"], "flow_var_th": c["flow_var_th"], "vol": c["vol"],
                     "vol_ratio": c["vol"] / base, "common": c["common_share"], "shock": c["shock_day"],
                     "shock_sd": c["shock_day"] / base})
    return _json({"rows": rows, "N": 100})


def compute_research() -> dict:
    pts = A.bertrand_points()
    k = 15
    grid = A.price_grid(pts["p_nash"], pts["p_mon"], k)
    P1, P2 = np.meshgrid(grid, grid, indexing="ij")
    R = A.profits(np.stack([P1, P2], -1))
    rows = []
    for j in (k - 3, k - 5, k - 7):         # collusive prices on the grid, from near monopoly down
        pc = float(grid[j])
        pi_c = float(R[j, j, 0])
        dev = int(np.argmax(R[:, j, 0]))
        pi_d = float(R[dev, j, 0])
        pi_n = float(A.profits([pts["p_nash"], pts["p_nash"]])[0])
        rows.append({"price": pc, "pi_c": pi_c, "pi_d": pi_d, "pi_n": pi_n, "dev_price": float(grid[dev]),
                     "grim": A.grim_threshold(pi_c, pi_n, pi_d),
                     "T": {str(T): A.punish_threshold(pi_c, pi_n, pi_d, T) for T in (1, 2, 3, 5, 10)}})
    # monopoly price, continuous
    pm = pts["p_mon"]
    br = pts["br"](pm)
    pi_d = float(A.profits([br, pm])[0])
    mono = {"pi_c": pts["pi_mon"], "pi_d": pi_d, "pi_n": pts["pi_nash"], "dev_price": br,
            "grim": A.grim_threshold(pts["pi_mon"], pts["pi_nash"], pi_d),
            "T": {str(T): A.punish_threshold(pts["pi_mon"], pts["pi_nash"], pi_d, T) for T in (1, 2, 3, 5, 10)}}
    # how long the learners punish: periods until both prices are back within one grid step of the pre-deviation level
    c = load("collusion")
    ir1, ir2 = np.asarray(c["ir1"]), np.asarray(c["ir2"])
    step = float(grid[1] - grid[0])
    back = next((t for t in range(2, len(ir1)) if abs(ir1[t] - ir1[0]) < step and abs(ir2[t] - ir2[0]) < step), -1)
    # Abreu's harshest punishment: the minmax profit, the most a firm can guarantee whatever its rival charges; as a
    # stick it lowers the threshold to (pi_d - pi_c) / (pi_d - pi_minmax), a bound for any punishment
    mm = float(min(R[:, j, 0].max() for j in range(k)))
    mono["minmax"] = mm
    mono["abreu"] = (mono["pi_d"] - mono["pi_c"]) / (mono["pi_d"] - mm)
    # the one-shot game on the grid has its own equilibria, at or just above Nash
    pi_N, pi_M = pts["pi_nash"], pts["pi_mon"]
    grid_ne = [{"price": float(grid[i]), "delta": A.delta_index(float(R[i, i, 0]), pi_N, pi_M)}
               for i in range(k) if int(np.argmax(R[:, i, 0])) == i]
    d0 = [x for x in c["by_delta"] if x["delta_disc"] == 0.0][0]
    return _json({"rows": rows, "mono": mono, "back": back - 1, "grid_step": step, "grid_ne": grid_ne,
                  "myopic": {"median": float(np.median(d0["all"])), "max": float(np.max(d0["all"])),
                             "above_grid_ne": float(np.mean(np.array(d0["all"]) > max(x["delta"] for x in grid_ne) + 1e-9))},
                  "below": [x for x in c["by_delta"] if x["delta_disc"] < mono["grim"]],
                  "above": [x for x in c["by_delta"] if x["delta_disc"] >= mono["grim"]]})


ITEMS = {"facts": compute_facts, "kirman": compute_kirman, "maker": compute_maker, "collusion": compute_collusion,
         "sessions": compute_sessions, "crowd": compute_crowd, "research": compute_research}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

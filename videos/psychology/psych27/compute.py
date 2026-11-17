"""Precompute every number in Part 27 of *Psychology, Built* ("Consciousness").

    python -m videos.psychology.psych27.compute            # everything missing (about a minute)
    python -m videos.psychology.psych27.compute --force ignition

Results are cached in ``.cache/psych27/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Every model is
Psyche's (``explainer.psychology.psyche.workspace``); published numbers are quoted in the scenes with their sources.
Simulations use fixed seeds; where a part shows one run of many, it is chosen by rule.

Items:
    masking      one representation, two readings: P(seen), accuracy on seen and unseen trials across target-mask
                 asynchronies, for three criteria for "seen"
    rivalry      the rivalry oscillator: a 40-second stretch, dominance durations and their gamma fit, and Levelt's
                 manipulation (one eye's contrast raised)
    ignition     a sensory stage and a workspace: graded early activity, all-or-none late activity, P(ignite)
                 against strength, the late activity's distribution at the threshold, mean traces
    phi          integrated information (Tononi 2004) for six small Boolean networks, with the minimum information
                 bipartition
    libet        Schurger's accumulator: a stretch of activity with its crossings, the back-average, the waits
    pci          four binary response patterns and their perturbational complexity
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import workspace as W

CACHE = Cache("psych27")
load = CACHE.load


def compute_masking() -> dict:
    soas = np.array([0, 8, 17, 25, 33, 42, 50, 67, 83, 100, 125, 150], float)
    out = {"soa": soas}
    for name, c in (("strict", 2.0), ("middle", 1.5), ("lax", 1.0)):
        v = W.visibility_curve(soas, c_seen=c)
        out[f"{name}_c"] = c
        for k in ("p_seen", "acc_unseen", "acc_seen", "acc"):
            out[f"{name}_{k}"] = v[k]
        out["d"] = v["d"]
    # the example the film dwells on: 33 ms, the middle criterion
    k = int(np.argmin(np.abs(soas - 33)))
    out["ex_soa"] = float(soas[k])
    out["ex_p_seen"] = float(out["middle_p_seen"][k])
    out["ex_acc_unseen"] = float(out["middle_acc_unseen"][k])
    out["ex_d"] = float(out["d"][k])
    # a criterion so strict that almost nothing is "seen": unseen accuracy approaches the overall accuracy
    out["ex_strict_unseen"] = float(out["strict_acc_unseen"][k])
    out["ex_lax_unseen"] = float(out["lax_acc_unseen"][k])
    return out


def compute_rivalry() -> dict:
    r = W.rivalry(T=600.0, seed=27)
    d = W.dominance_durations(r["u"], r["dt"])
    t0, t1 = int(60 / r["dt"]), int(100 / r["dt"])
    step = 10
    r2 = W.rivalry(T=600.0, I=(0.65, 0.6), seed=27)
    d2 = W.dominance_durations(r2["u"], r2["dt"])
    edges = np.linspace(0, 12, 25)
    hist = np.histogram(d["all"], bins=edges, density=True)[0]
    from scipy.stats import gamma
    x = np.linspace(0.05, 12, 200)
    return {"t": r["t"][t0:t1:step] - r["t"][t0], "u1": r["u"][t0:t1:step, 0], "u2": r["u"][t0:t1:step, 1],
            "n": int(len(d["all"])), "mean": float(d["all"].mean()), "shape": d["shape"], "scale": d["scale"],
            "cv": float(d["all"].std() / d["all"].mean()), "edges": edges, "hist": hist, "x": x,
            "gamma_pdf": gamma.pdf(x, d["shape"], scale=d["scale"]),
            "equal_means": [d["mean1"], d["mean2"]], "raised_means": [d2["mean1"], d2["mean2"]]}


def compute_ignition() -> dict:
    strengths = np.round(np.arange(0.0, 1.55, 0.05), 2)
    g = W.ignition(strengths, n_trials=400, seed=27)
    k_half = int(np.argmin(np.abs(g["p_ignite"] - 0.5)))
    edges = np.linspace(0, 1.1, 23)
    late_hist = np.histogram(g["late"][k_half], bins=edges)[0]
    pick = [int(np.argmin(np.abs(strengths - s))) for s in (0.5, strengths[k_half], 1.25)]
    return {"strength": strengths, "p_ignite": g["p_ignite"], "early_mean": g["early"].mean(1),
            "late_mean": g["late"].mean(1), "late_sd": g["late"].std(1), "early_sd": g["early"].std(1),
            "threshold": float(strengths[k_half]), "p_at_threshold": float(g["p_ignite"][k_half]),
            "edges": edges, "late_hist": late_hist, "t": g["t"][::5],
            "traces_s": g["mean_s"][pick][:, ::5], "traces_r": g["mean_r"][pick][:, ::5],
            "trace_strengths": strengths[pick]}


NETS = [("pairs", 6, "two-node loops, unconnected"), ("chain", 6, "a feed-forward chain"),
        ("ring_copy", 4, "a ring of four"), ("ring_copy", 6, "a ring of six"),
        ("all_or", 5, "five nodes, each the OR of the rest"), ("ring_xor", 6, "a ring of XOR gates")]


def compute_phi() -> dict:
    rows = []
    for kind, n, label in NETS:
        r = W.phi(W.network(kind, n))
        rows.append({"kind": kind, "n": n, "label": label, "phi": r["phi"], "mib_a": list(r["mib"][0]),
                     "mib_b": list(r["mib"][1])})
    # effective information across the halves of the ring of six, each way
    net = W.network("ring_copy", 6)
    A, B = (0, 1, 2), (3, 4, 5)
    return {"rows": rows, "ring_ei_ab": W.ei(net, A, B), "ring_ei_ba": W.ei(net, B, A),
            "n_bipartitions_6": sum(1 for _ in W.bipartitions(6))}


def compute_libet() -> dict:
    s = W.schurger(T=1200.0, seed=27)
    b = W.back_average(s["x"], s["hits"], s["dt"], window=3.0)
    k0 = 20.0
    i0, i1 = int(k0 / s["dt"]), int((k0 + 30.0) / s["dt"])
    hits = s["hits"][(s["hits"] >= i0) & (s["hits"] < i1)]
    # where the average starts to rise: first time it exceeds its value 3 s before plus 10% of its rise
    m = b["mean"]
    onset = float(b["t"][int(np.argmax(m > m[0] + 0.1 * (m[-1] - m[0])))])
    return {"t": (np.arange(i0, i1, 10) - i0) * s["dt"], "x": s["x"][i0:i1:10], "hits": (hits - i0) * s["dt"],
            "threshold": 0.298, "bt": b["t"][::10], "bmean": m[::10], "n_epochs": int(b["n"]),
            "waits": s["waits"], "median_wait": float(np.median(s["waits"])), "onset": onset,
            "sample_epochs": b["epochs"][:12, ::10]}


def compute_pci() -> dict:
    out = {}
    for k in ("wake", "sleep", "local", "noise"):
        M = W.responses(k, seed=27)
        out[f"{k}_M"] = M
        out[f"{k}_pci"] = W.pci(M)
    out["threshold"] = 0.31  # Casarotto et al. (2016)
    return out


ITEMS = {"masking": compute_masking, "rivalry": compute_rivalry, "ignition": compute_ignition, "phi": compute_phi,
         "libet": compute_libet, "pci": compute_pci}


if __name__ == "__main__":
    CACHE.main(ITEMS)

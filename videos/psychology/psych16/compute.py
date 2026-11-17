"""Precompute every number in Part 16 of *Psychology, Built* ("Conditioning").

    python -m videos.psychology.psych16.compute            # everything missing (about a minute)
    python -m videos.psychology.psych16.compute --force choice

Results are cached in ``.cache/psych16/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.conditioning``); every simulated study is picked by rule (a fixed seed, or the
median of many runs), never by its result.

Items:
    pavlov      acquisition, extinction and spontaneous recovery of a salivary response; a generalization gradient
    thorndike   escape times of a law-of-effect learner in a puzzle box (one cat, and the median of 200)
    shaping     the form of a response under successive approximation, and when waiting for the target
    schedules   cumulative records under FR, VR, FI and VI schedules
    contingency the film's contingency game; learning curves for three contingencies; the solved asymptotes
    rescorla68  Rescorla's (1968) ten groups under Rescorla-Wagner with the context as a cue
    rw          Rescorla-Wagner on the classic designs, and the error surface for blocking
    extinction  latent inhibition, spontaneous recovery and renewal
    attention   Mackintosh and Pearce-Hall associabilities on one history
    timing      peak-procedure curves and the I/T law against Rescorla-Wagner
    choice      concurrent schedules chosen by melioration; the generalized matching fit; a melioration trap
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import conditioning as K

CACHE = Cache("psych16")
load = CACHE.load


def compute_pavlov() -> dict:
    rng = np.random.default_rng(16)
    phases = [("lab", 1.0, 30), ("lab", 0.0, 25)]
    _, curve = K.extinction_in_context(phases, alpha=0.18, tau=48.0)
    # the next day: a probe after a 24-hour gap, then extinction again
    probes, _ = K.extinction_in_context(phases + [("test", "lab", 24.0)], alpha=0.18, tau=48.0)
    drops = 12 * curve + rng.normal(0, 0.6, curve.size)
    f = np.geomspace(250, 4000, 81)
    return {"trial": np.arange(1, curve.size + 1), "R": curve, "drops": np.clip(drops, 0, None),
            "recovered": float(probes[0]), "drops_recovered": float(12 * probes[0]),
            "f": f, "gen": K.generalization(f), "probe_f": np.array([500.0, 700.0, 1000.0, 1400.0, 2000.0]),
            "probe_gen": K.generalization(np.array([500.0, 700.0, 1000.0, 1400.0, 2000.0]))}


def compute_thorndike() -> dict:
    one = K.puzzle_box(rng=np.random.default_rng(12))
    many = np.array([K.puzzle_box(rng=np.random.default_rng(s)) for s in range(200)])
    return {"one": one, "median": np.median(many, 0), "q25": np.quantile(many, 0.25, 0), "q75": np.quantile(many, 0.75, 0)}


def compute_shaping() -> dict:
    mu, hit = K.shaping(rng=np.random.default_rng(1))
    mu0, hit0 = K.shaping(rng=np.random.default_rng(1), successive=False)
    return {"mu": mu, "hit": hit, "mu0": mu0, "hit0": hit0, "target": 3.0}


def compute_schedules() -> dict:
    out = {}
    for kind, v in (("FR", 20), ("VR", 20), ("FI", 60), ("VI", 60)):
        r, f = K.schedule(kind, v, duration=900.0, rng=np.random.default_rng(7))
        t, c = K.cumulative(r, 900.0)
        out[f"t_{kind}"], out[f"c_{kind}"], out[f"rf_{kind}"] = t, c, f
        out[f"rf_c_{kind}"] = np.searchsorted(np.sort(r), f, side="right")
        out[f"rate_{kind}"] = float(len(r) / 900.0 * 60)
    return out


GAME = ((0.75, 0.75), (0.75, 0.25), (0.25, 0.25), (0.25, 0.75))


def compute_contingency() -> dict:
    rng = np.random.default_rng(3)
    # the film's game: 24 plants, fertilizer on half; nine of each twelve bloom, so the contingency is exactly zero
    order = rng.permutation(24)
    given = np.array([1] * 12 + [0] * 12)[order]
    bloom = np.array([1] * 9 + [0] * 3 + [1] * 9 + [0] * 3)[order]
    out = {"given": given, "bloom": bloom}
    for k, (p1, p0) in enumerate(GAME):
        curves = np.array([K.contingency_learning(p1, p0, n=60, rng=np.random.default_rng(s)) for s in range(500)])
        out[f"curve_{k}"] = curves.mean(0)
        out[f"asym_{k}"] = float(K.rw_asymptote([("CX", 0.5, p1), ("C", 0.5, p0)])[1][1])
    out["cells"] = np.array([[int(((given == 1) & (bloom == 1)).sum()), int(((given == 1) & (bloom == 0)).sum())],
                             [int(((given == 0) & (bloom == 1)).sum()), int(((given == 0) & (bloom == 0)).sum())]])
    return out


def compute_rescorla68() -> dict:
    groups = K.RESCORLA_1968_GROUPS
    med = np.array([np.median([K.rescorla_1968(p1, p0, rng=np.random.default_rng(s)) for s in range(8)])
                    for p1, p0 in groups])
    asym = np.array([K.rw_asymptote([("CX", 0.2, p1), ("C", 0.8, p0)])[1][1] for p1, p0 in groups])
    return {"groups": np.array(groups), "V": med, "SR": K.suppression_ratio(med), "asym": asym}


def compute_rw() -> dict:
    out = {}
    _, V = K.rescorla_wagner(K.sequence([("A+", 30), ("A-", 30)]), alpha=0.3, beta=(0.5, 0.5))
    out["acq_ext"] = V[:, 0]
    _, Vb = K.rescorla_wagner(K.sequence([("A+", 30), ("AX+", 30)]), alpha=0.3)
    _, Vc = K.rescorla_wagner(K.sequence([("B+", 30), ("AX+", 30)]), alpha=0.3, cues="ABX")
    out["block_A"], out["block_X"], out["ctrl_X"] = Vb[:, 0], Vb[:, 1], Vc[:, 2]
    _, Vo = K.rescorla_wagner(K.sequence([("AX+", 40)]), alpha={"A": 0.45, "X": 0.1})
    _, Vs = K.rescorla_wagner(K.sequence([("X+", 40)]), alpha={"X": 0.1})
    out["over_A"], out["over_X"], out["solo_X"] = Vo[:, 0], Vo[:, 1], Vs[:, 0]
    _, Vi = K.rescorla_wagner(K.sequence([("A+ AX-", 120)]), alpha=0.3)
    out["inh_A"], out["inh_X"] = Vi[:, 0], Vi[:, 1]
    _, Ve = K.rescorla_wagner(K.sequence([("A+ B+", 80), ("AB+", 40)]), alpha=0.3)
    out["oe_A"], out["oe_B"] = Ve[:, 0], Ve[:, 1]
    # the error surface over (V_A, V_X) on a compound trial, and the blocking path through it
    g = np.linspace(-0.2, 1.2, 57)
    out["grid"] = g
    out["surface"] = 0.5 * (1.0 - g[None, :] - g[:, None]) ** 2  # rows V_X, columns V_A
    out["path_block"] = np.c_[Vb[30:, 0], Vb[30:, 1]]
    out["path_ctrl"] = np.c_[Vc[30:, 0], Vc[30:, 2]]
    return out


def compute_extinction() -> dict:
    out = {d: K.renewal(d, alpha=0.25) for d in ("AAA", "ABA", "ABC", "AAB")}
    delays = np.linspace(0, 96, 49)
    rec = [K.extinction_in_context([("A", 1.0, 20), ("A", 0.0, 40), ("test", "A", float(d))], tau=48.0)[0][0]
           for d in delays]
    _, Vrw_pre = K.rescorla_wagner(K.sequence([("X-", 40), ("X+", 12)]))
    _, Vrw_new = K.rescorla_wagner(K.sequence([("X+", 12)]))
    _, Vph_pre, Aph = K.pearce_hall(K.sequence([("X-", 40), ("X+", 12)]))
    _, Vph_new, _ = K.pearce_hall(K.sequence([("X+", 12)]))
    return {"renewal": out, "delays": delays, "recovery": np.array(rec),
            "rw_pre": Vrw_pre[40:, 0], "rw_new": Vrw_new[:, 0], "ph_pre": Vph_pre[40:, 0], "ph_new": Vph_new[:, 0],
            "ph_alpha_pre": Aph[:41, 0]}


def compute_attention() -> dict:
    seq = K.sequence([("A+ B+ A+ B-", 160)])
    _, Vm, Am = K.mackintosh(seq)
    _, Vp, Ap = K.pearce_hall(seq)
    return {"mack_A": Am[:, 0], "mack_B": Am[:, 1], "ph_A": Ap[:, 0], "ph_B": Ap[:, 1],
            "mack_VA": Vm[:, 0], "mack_VB": Vm[:, 1], "ph_VA": Vp[:, 0], "ph_VB": Vp[:, 1]}


def compute_timing() -> dict:
    t = np.linspace(0, 120, 481)
    r = np.geomspace(1, 30, 30)
    return {"t": t, "p20": K.peak_curve(t, 20), "p40": K.peak_curve(t, 40), "p60": K.peak_curve(t, 60),
            "ratio": r, "gg": K.reinforcements_to_acquisition(r), "rw": K.rw_trials_to_criterion(r)}


PAIRS = ((15, 135), (30, 90), (45, 45), (90, 30), (135, 15), (20, 180), (180, 20))


def compute_choice() -> dict:
    Bs, Rs = [], []
    for k, (a, b) in enumerate(PAIRS):
        B, R = K.concurrent(means=(float(a), float(b)), minutes=400, rng=np.random.default_rng(100 + k))
        Bs.append(B)
        Rs.append(R)
    Bs, Rs = np.array(Bs), np.array(Rs)
    a, c = K.generalized_matching(Bs, Rs)
    Bv, Rv = K.concurrent(kind=("VR", "VR"), means=(20.0, 40.0), minutes=400, rng=np.random.default_rng(9))
    mel = np.array([K.melioration_trap(rng=np.random.default_rng(s)) for s in range(50)])
    mx = K.melioration_trap(policy="maximize")
    return {"B": Bs, "R": Rs, "a": a, "logb": c, "B_vr": Bv, "R_vr": Rv,
            "trap_mel": mel.mean(0), "trap_max": mx, "trap_mel_mean": float(mel.mean()), "trap_max_mean": float(mx.mean())}


ITEMS = {
    "pavlov": compute_pavlov,
    "thorndike": compute_thorndike,
    "shaping": compute_shaping,
    "schedules": compute_schedules,
    "contingency": compute_contingency,
    "rescorla68": compute_rescorla68,
    "rw": compute_rw,
    "extinction": compute_extinction,
    "attention": compute_attention,
    "timing": compute_timing,
    "choice": compute_choice,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

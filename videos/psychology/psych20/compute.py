"""Precompute every number in Part 20 of *Psychology, Built* ("Memory I: Storing and Finding").

    python -m videos.psychology.psych20.compute            # everything missing (a few minutes)
    python -m videos.psychology.psych20.compute --force cmr

Results are cached in ``.cache/psych20/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.memory``); the free-recall data are PEERS (Kahana lab), fetched by
``explainer.psychology.opendata``.  Simulated studies are picked by rule (a fixed seed, or the mean of many runs),
never by their result.

Items:
    forgetting  Ebbinghaus's savings with three fitted laws; ACT-R's activation and its power-law forgetting
    peers       the open data: serial position, first recall, lag-CRP, recall counts
    cmr         the context model fitted by maximum likelihood to half the lists, checked on the other half;
                its curves after a filled delay and with a distractor after every item
    sam         SAM's serial position and lag-CRP: symmetric contiguity
    drift       context similarity against lag in the fitted model, forward and backward
    hopfield    capacity against load; one stored pattern recalled from a corrupted cue, step by step
    recognition dual-process and unequal-variance ROCs and their z-ROCs
    separation  output overlap against input overlap for a sparse expansion
    divers      Godden and Baddeley's four means (1975) and Murre's sixteen divers (2021), with the paired context
                effect and an exact sign-flip test
    persons     every PEERS participant's own serial-position and lag-CRP curves: how many show recency, primacy and
                a forward-leaning contiguity
    reinstate   what recalling one item does in the fitted context model: activation by lag, with the episodic and
                the pre-experimental part of context separately
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import archive, opendata
from explainer.psychology.psyche import memory as M

CACHE = Cache("psych20")
load = CACHE.load

N = 16


def compute_forgetting() -> dict:
    e = archive.EBBINGHAUS_1885.data
    t, y = np.array(e["minutes"]), np.array(e["saving"])
    fits = M.fit_forgetting(t, y)
    tt = np.geomspace(15, 50000, 200)
    k, c = fits["ebbinghaus"]["params"]
    a, b = fits["power"]["params"]
    a2, tau = fits["exponential"]["params"]
    days = np.linspace(0.25, 60, 160)
    act = {}
    for n in (1, 3, 10):
        practice = -np.linspace(0, 48, n)[::-1]  # n uses over two days, in hours, the last at time 0
        act[n] = np.array([M.actr_recall(M.actr_activation(practice, d * 24.0), threshold=-2.0, s=0.5)
                           for d in days])
    return {"t": t, "y": y, "tt": tt, "ebb": M.ebbinghaus_formula(tt, k, c), "pow": a * tt ** (-b),
            "exp": a2 * np.exp(-tt / tau), "sse": np.array([fits[m]["sse"] for m in ("ebbinghaus", "power", "exponential")]),
            "params_ebb": np.array([k, c]), "params_pow": np.array([a, b]), "params_exp": np.array([a2, tau]),
            "days": days, "act1": act[1], "act3": act[3], "act10": act[10]}


def _peers():
    d = opendata.peers_free_recall()
    return d["recalls"], d["subject"]


def compute_peers() -> dict:
    R, subj = _peers()
    s = M.recall_summary(R, N, max_lag=5)
    counts = (R > 0).sum(1)
    return {"spc": s["spc"], "pfr": s["pfr"], "lags": s["lags"], "crp": s["crp"], "n_lists": len(R),
            "n_subjects": len(np.unique(subj)), "mean_recalled": float(counts.mean()),
            "intrusion_rate": float((R == 0).sum() / max(1, R.size))}


def compute_cmr() -> dict:
    R, subj = _peers()
    fit_half, test_half = R[::2], R[1::2]
    # start from a previous fit's values (the optimum does not depend on them; the run time does)
    x0 = {"B_enc": 0.95, "B_rec": 0.92, "B_start": 0.044, "gamma_fc": 0.11, "phi_s": 8.5, "phi_d": 1.55, "tau": 1.19,
          "stop_s": 0.007, "stop_r": 0.30}
    f = M.fit_cmr_ml(fit_half, N, x0=x0, maxiter=3000)
    p = f["params"]
    rng = np.random.default_rng(2002)
    sims = {name: M.recall_summary(M.cmr_simulate(N, 4000, p, rng, **kw), N)
            for name, kw in (("immediate", {}), ("delayed", {"end_distractor": 0.99}),
                             ("continual", {"between": 0.99, "end_distractor": 0.99}))}
    test = M.recall_summary(test_half, N)
    # the choice of each held-out recall: CMR against a serial-position baseline and against chance
    cm = M.cmr_loglik(p, test_half, N, parts=True)
    base = M.position_choice_loglik(M.spc(fit_half, N), test_half, N)
    unif = M.position_choice_loglik(np.ones(N), test_half, N)
    out = {"params": np.array([p[k] for k in ("B_enc", "B_rec", "B_start", "gamma_fc", "phi_s", "phi_d", "tau",
                                              "stop_s", "stop_r")]),
           "loglik": f["loglik"], "loglik_test": M.cmr_loglik(p, test_half, N), "n_fit": len(fit_half),
           "n_test": len(test_half), "evals": f.get("evals", 0),
           "test_spc": test["spc"], "test_crp": test["crp"], "test_pfr": test["pfr"],
           "bits_cmr": -cm["choice"] / cm["recalls"] / np.log(2), "bits_position": -base["choice"] /
           base["recalls"] / np.log(2), "bits_chance": -unif["choice"] / unif["recalls"] / np.log(2),
           "test_recalls": cm["recalls"]}
    for name, s in sims.items():
        out[f"{name}_spc"] = s["spc"]
        out[f"{name}_crp"] = s["crp"]
        out[f"{name}_pfr"] = s["pfr"]
    out["lags"] = sims["immediate"]["lags"]
    return out


def compute_sam() -> dict:
    s = M.recall_summary(M.sam_simulate(N, 4000, rng=np.random.default_rng(1981)), N)
    return {"spc": s["spc"], "crp": s["crp"], "lags": s["lags"], "pfr": s["pfr"]}


def compute_hopfield() -> dict:
    h = M.hopfield_capacity(200, np.linspace(0.02, 0.3, 29), trials=40, rng=np.random.default_rng(1982))
    rng = np.random.default_rng(7)
    n = 100
    pats = rng.choice([-1.0, 1.0], size=(8, n))
    # a recognisable pattern first: a ring on a 10 x 10 grid
    yy, xx = np.mgrid[0:10, 0:10]
    ring = np.where(np.abs(np.hypot(xx - 4.5, yy - 4.5) - 3.2) < 1.1, 1.0, -1.0).ravel()
    pats[0] = ring
    W = pats.T @ pats / n
    np.fill_diagonal(W, 0.0)
    s = ring.copy()
    flip = rng.random(n) < 0.3
    s[flip] *= -1
    steps = [s.copy()]
    order = rng.permutation(n)
    for k in range(4):  # asynchronous sweeps, recorded after each quarter sweep
        for j, i in enumerate(order):
            s[i] = 1.0 if W[i] @ s >= 0 else -1.0
            if (j + 1) % 25 == 0:
                steps.append(s.copy())
    energy = [-0.5 * x @ W @ x for x in steps]
    return {"loads": h["loads"], "overlap": h["overlap"], "recalled": h["recalled"], "steps": np.array(steps),
            "energy": np.array(energy), "target": ring}


def compute_recognition() -> dict:
    F1, H1 = M.dual_process_roc(0.3, 1.0)
    F2, H2 = M.uvsd_roc(1.2, 1.25)
    from scipy.stats import norm

    def z(p):
        return norm.ppf(np.clip(p, 1e-4, 1 - 1e-4))

    return {"F_dp": F1, "H_dp": H1, "F_uv": F2, "H_uv": H2, "zF_dp": z(F1), "zH_dp": z(H1), "zF_uv": z(F2),
            "zH_uv": z(H2)}


def compute_separation() -> dict:
    ov = np.linspace(0, 1, 11)
    return {"input": ov, "output": M.pattern_separation(ov, pairs=60, rng=np.random.default_rng(1971))}


def compute_drift() -> dict:
    p = dict(zip(("B_enc", "B_rec", "B_start", "gamma_fc", "phi_s", "phi_d", "tau", "stop_s", "stop_r"),
                 load("cmr")["params"]))
    M_fc, M_cf, c = M._cmr_study(N, {**M.CMR_DEFAULT, **p})
    # context at study of each item = rows of M_cf (up to the primacy gain), normalised
    ctx = M_cf - M.CMR_DEFAULT["alpha"]
    ctx = ctx / np.linalg.norm(ctx, axis=1, keepdims=True)
    sim = ctx @ ctx.T
    lags = np.arange(-6, 7)
    mean = np.array([np.mean([sim[i, i + l] for i in range(N) if 0 <= i + l < N]) for l in lags])
    return {"sim": sim, "lags": lags, "mean": mean}


def compute_divers() -> dict:
    d = opendata.murre_2021()
    S = d["scores"]  # divers x (DD, DW, WD, WW): learn, then recall environment
    same = (S[:, 0] + S[:, 3]) / 2
    diff = (S[:, 1] + S[:, 2]) / 2
    eff = same - diff
    # exact sign-flip test of the mean paired effect: all 2^16 sign patterns
    n = len(eff)
    signs = ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1) * 2 - 1
    null = (signs * eff).mean(1)
    p = float(np.mean(np.abs(null) >= abs(eff.mean()) - 1e-12))
    gb = archive.GODDEN_BADDELEY_1975.data
    return {"scores": S, "means": S.mean(0), "se": S.std(0, ddof=1) / np.sqrt(n), "effect": eff,
            "effect_mean": float(eff.mean()), "effect_se": float(eff.std(ddof=1) / np.sqrt(n)), "p_signflip": p,
            "gb_means": np.array(gb["means"]), "n": n}


def compute_persons() -> dict:
    R, subj = _peers()
    ids = np.unique(subj)
    rec, prim, fwd, bwd, first_last = [], [], [], [], []
    for s_ in ids:
        Rs = R[subj == s_]
        sm = M.recall_summary(Rs, N, max_lag=1)
        spc_, crp_ = sm["spc"], sm["crp"]
        rec.append(spc_[-1] - spc_[6:10].mean())
        prim.append(spc_[0] - spc_[6:10].mean())
        bwd.append(crp_[0])
        fwd.append(crp_[2])
        first_last.append(sm["pfr"][-1])
    rec, prim, fwd, bwd = map(np.array, (rec, prim, fwd, bwd))
    return {"recency": rec, "primacy": prim, "fwd": fwd, "bwd": bwd, "pfr_last": np.array(first_last),
            "n": len(ids), "share_recency": float((rec > 0).mean()), "share_primacy": float((prim > 0).mean()),
            "share_forward": float((fwd > bwd).mean()), "share_contig": float((np.minimum(fwd, bwd) > 0).mean())}


def compute_reinstate() -> dict:
    keys = ("B_enc", "B_rec", "B_start", "gamma_fc", "phi_s", "phi_d", "tau", "stop_s", "stop_r")
    p = {**M.CMR_DEFAULT, **dict(zip(keys, load("cmr")["params"]))}
    k = 7  # the eighth item is recalled first
    lags = np.arange(-7, 9)
    out = {"lags": lags}
    for name, g in (("fitted", p["gamma_fc"]), ("pre", 0.0), ("episodic", 0.95)):
        q = {**p, "gamma_fc": g, "phi_s": 0.0}  # no primacy gain, so only the lag shapes the profile
        M_fc, M_cf, _ = M._cmr_study(N, q)
        c_in = M_fc[:, k] / np.linalg.norm(M_fc[:, k])  # the context the recalled item brings back
        a = M_cf @ c_in - q["alpha"] * c_in.sum()  # the support it gives each item, above the uniform baseline
        a = a / np.max(np.delete(a, k))
        a[k] = np.nan
        out[name] = np.array([a[k + l] if 0 <= k + l < N else np.nan for l in lags])
    return out


ITEMS = {
    "forgetting": compute_forgetting,
    "peers": compute_peers,
    "cmr": compute_cmr,
    "sam": compute_sam,
    "drift": compute_drift,
    "hopfield": compute_hopfield,
    "recognition": compute_recognition,
    "separation": compute_separation,
    "divers": compute_divers,
    "persons": compute_persons,
    "reinstate": compute_reinstate,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

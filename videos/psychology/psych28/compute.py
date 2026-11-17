"""Precompute every number in Part 28 of *Psychology, Built* ("Motivation").

    python -m videos.psychology.psych28.compute            # everything missing (under a minute)
    python -m videos.psychology.psych28.compute --force rrr

Results are cached in ``.cache/psych28/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Every model is
Psyche's (``explainer.psychology.psyche.drive``); the one dataset is the ego-depletion Registered Replication
Report's table of laboratories (Hagger et al. 2016), fetched and checked by ``explainer.psychology.opendata``.
Published numbers are quoted in the scenes with their sources.  Simulations use fixed seeds; where a part shows one
run of many, it is chosen by rule.

Items:
    stim         the self-stimulation learner: the share of presses on the current and the energy store against
                 the current's worth (five seeds each), and two runs drawn over time
    thermostat   proportional and proportional-plus-integral control after a step disturbance
    weight       a 500-kcal diet for 300 days: the static rule, a settling point, a defended set point
    arousal      performance against arousal for an easy and a hard task, with the optima
    salt         a cue's cached value and its incentive value, through training and a change of state
    perception   self-perception as Bayes: inferred interest with and without a promised reward, and across the
                 reward's pull
    atkinson     Atkinson's tendency against the chance of success for the success-oriented and the anxious
    titration    the adjusting-amount procedure on three hyperbolic choosers
    literature   a simulated literature of a null effect, small samples and a file drawer: what a meta-analysis of
                 the published studies finds, and what the precision-effect test finds
    rrr          the Registered Replication Report: 23 laboratories, Hedges's g each, the random-effects estimate
    waiting      the expected remaining wait and the best give-up time, for a reliable and an unreliable return
    confound     delay of gratification and a later outcome, with and without background controlled
    grit         grit's increment over conscientiousness, from Crede, Tynan and Harms's correlations
    effort       the expected value of control over reward and over difficulty
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import archive, evidence, opendata
from explainer.psychology.psyche import drive as D

CACHE = Cache("psych28")
load = CACHE.load


def compute_stim() -> dict:
    values = np.round(np.arange(0.2, 2.01, 0.1), 2)
    share, energy = [], []
    for v in values:
        runs = [D.self_stimulation(stim=1, stim_value=float(v), seed=s) for s in range(5)]
        share.append(np.mean([r["choice"][-1000:].mean() for r in runs]))
        energy.append(np.mean([r["energy"][-1000:].mean() for r in runs]))
    share, energy = np.array(share), np.array(energy)
    food = D.self_stimulation(stim=0, seed=0)
    hi = D.self_stimulation(stim=1, stim_value=1.5, seed=0)
    w = 50  # presses per bin for the traces
    def binned(x):
        return x[: len(x) // w * w].reshape(-1, w).mean(1)
    k_starve = int(np.argmax(energy < 0.1))
    return {"value": values, "share": share, "energy": energy, "starve_at": float(values[k_starve]),
            "food_energy": float(food["energy"][-1000:].mean()),
            "t": np.arange(len(binned(hi["energy"]))) * w, "hi_energy": binned(hi["energy"]),
            "hi_share": binned(hi["choice"].astype(float)), "food_trace": binned(food["energy"]),
            "hi_share_end": float(hi["choice"][-1000:].mean())}


def compute_thermostat() -> dict:
    dist = lambda t: -1.0 if t >= 20 else 0.0  # noqa: E731  a window opened at minute 20
    p = D.thermostat(T=80.0, k=0.2, x0=14.0, disturbance=dist)
    pi = D.thermostat(T=80.0, k=0.2, ki=0.05, x0=14.0, disturbance=dist)
    p20 = D.thermostat(T=80.0, k=0.2, x0=20.0, disturbance=dist)
    pi20 = D.thermostat(T=80.0, k=0.2, ki=0.05, x0=20.0, disturbance=dist)
    step = 8
    return {"t": p["t"][::step], "p": p["x"][::step], "pi": pi["x"][::step], "p20": p20["x"][::step],
            "pi20": pi20["x"][::step], "pi_low": float(pi20["x"].min()), "set": 20.0, "k": 0.2, "ki": 0.05,
            "D": -1.0, "p_end": float(p["x"][-1]), "pi_end": float(pi["x"][-1]), "start": 14.0,
            "half_time": float(np.log(2) / 0.2)}


def compute_weight() -> dict:
    days, diet, cut = 1100, (100, 400), 500.0
    static = D.static_rule(days, diet, cut)
    settle = D.body_weight(days, diet, cut)
    defend = D.body_weight(days, diet, cut, hunger=60.0, thrift=25.0)
    step = 5
    return {"day": settle["day"][::step], "static": static[::step], "settle": settle["W"][::step],
            "defend": defend["W"][::step], "diet": diet, "cut": cut,
            "static_loss": float(80 - static[diet[1] - 1]), "settle_loss": float(80 - settle["W"][diet[1] - 1]),
            "defend_loss": float(80 - defend["W"][diet[1] - 1]),
            "settle_steady": settle["steady_loss"], "settle_tau": settle["tau_days"],
            "defend_steady": defend["steady_loss"], "defend_tau": defend["tau_days"],
            "settle_end": float(settle["W"][-1]), "defend_end": float(defend["W"][-1]),
            "defend_intake_gap": float(defend["intake"][diet[1] - 1] - (2400 - cut)),
            "defend_out_gap": float(2400 - defend["out"][diet[1] - 1]),
            "settle_out_gap": float(2400 - settle["out"][diet[1] - 1]),
            "per_kg": 24.0, "hunger": 60.0, "thrift": 25.0}


def compute_arousal() -> dict:
    a = np.linspace(0, 1, 101)
    easy, hard = D.arousal_performance(a, 0.85), D.arousal_performance(a, 0.45)
    return {"a": a, "easy": easy / easy.max(), "hard": hard / hard.max(), "easy_best": float(a[easy.argmax()]),
            "hard_best": float(a[hard.argmax()])}


def compute_salt() -> dict:
    s = D.salt_cue()
    return {**s, "train_end": float(s["cached"][s["switch"] - 1]), "test_cached": float(s["cached"][s["switch"]]),
            "test_incentive": float(s["incentive"][s["switch"]]), "end_cached": float(s["cached"][-1])}


def compute_perception() -> dict:
    s = D.self_perception()
    pulls = np.linspace(0, 4, 41)
    curve = np.array([D.self_perception(reward=float(r))["reward"] for r in pulls])
    return {"no_reward": s["no_reward"], "reward": s["reward"], "prior": 0.5, "p_draw_none": s["no_reward_p_draw"],
            "p_draw_reward": s["reward_p_draw"], "pull": pulls, "curve": curve}


def compute_atkinson() -> dict:
    P = np.linspace(0, 1, 101)
    return {"P": P, "success": D.atkinson(P, 1.0, 0.3), "anxious": D.atkinson(P, 0.3, 1.0)}


def compute_titration() -> dict:
    out = {}
    for name, k in (("patient", 0.002), ("middle", 0.02), ("impulsive", 0.1)):
        r = D.discount_titration(k)
        out[f"{name}_k"] = k
        out[f"{name}_ind"] = r["indifference"]
        out[f"{name}_fit"] = r["k_fit"]
        out[f"{name}_auc"] = r["auc"]
        if name == "middle":
            out["offers"] = r["offers"]
    out["delay"] = np.array([1, 7, 30, 90, 180, 365], float)
    out["grid"] = np.linspace(0, 365, 200)
    return out


def compute_literature() -> dict:
    """A null effect studied by 1,500 small two-group studies (10 to 40 people a group), a file drawer that
    publishes 5% of the rest, and a 30% chance that a non-significant study is pushed over the line."""
    rng = np.random.default_rng(28)
    n = rng.integers(10, 41, 1500)
    lit = evidence.literature(1500, 0.0, n, rng=rng, publish_null=0.05, hack=0.3)
    pub = lit["published"]
    J = 1 - 3 / (4 * 2 * n - 9)
    g = lit["est"] * J
    se = lit["se"]
    re = D.random_effects(g[pub], se[pub] ** 2)
    pe = D.pet(g[pub], se[pub])
    return {"g": g[pub], "se": se[pub], "g_all": g, "se_all": se, "k_run": 1500, "k_pub": int(pub.sum()),
            "share_sig": float(lit["significant"][pub].mean()), "re": re["estimate"], "re_lo": re["lo"],
            "re_hi": re["hi"], "pet": pe["intercept"], "pet_se": pe["se_intercept"], "pet_slope": pe["slope"],
            "all_re": D.random_effects(g, se ** 2)["estimate"]}


def compute_rrr() -> dict:
    d = opendata.ego_depletion_rrr()
    orig = d["original"]
    g, v = [], []
    for i in range(len(d["lab"])):
        gi, vi = D.hedges_g(d["m_dep"][i], d["sd_dep"][i], d["n_dep"][i], d["m_ctl"][i], d["sd_ctl"][i],
                            d["n_ctl"][i])
        g.append(gi)
        v.append(vi)
    g, v = np.array(g), np.array(v)
    rep = ~orig
    re = D.random_effects(g[rep], v[rep])
    pe = D.pet(g[rep], np.sqrt(v[rep]))
    order = np.argsort(g[rep])
    return {"lab": [str(x) for x in np.array(d["lab"])[rep][order]], "g": g[rep][order],
            "lo": (g[rep] - 1.96 * np.sqrt(v[rep]))[order], "hi": (g[rep] + 1.96 * np.sqrt(v[rep]))[order],
            "n": (d["n_dep"] + d["n_ctl"])[rep][order], "english": (d["language"][rep] == "English")[order],
            "k": int(rep.sum()), "N": int((d["n_dep"] + d["n_ctl"])[rep].sum()),
            "orig_g": float(g[orig][0]), "orig_lo": float(g[orig][0] - 1.96 * np.sqrt(v[orig][0])),
            "orig_hi": float(g[orig][0] + 1.96 * np.sqrt(v[orig][0])), "orig_n": int((d["n_dep"] + d["n_ctl"])[orig][0]),
            "re": re["estimate"], "re_lo": re["lo"], "re_hi": re["hi"], "tau2": re["tau2"], "I2": re["I2"],
            "Q": re["Q"], "pet": pe["intercept"], "n_positive": int((g[rep] > 0).sum()),
            "n_sig": int(((g[rep] - 1.96 * np.sqrt(v[rep])) > 0).sum())}


def compute_waiting() -> dict:
    t = np.linspace(0, 20, 201)
    out = {"t": t}
    for kind in ("normal", "pareto"):
        out[f"{kind}_wait"] = D.remaining_wait(t, kind)
        g = D.give_up_time(kind)
        out[f"{kind}_tau"] = g["tau"][::4]
        out[f"{kind}_rate"] = g["rate"][::4]
        out[f"{kind}_best"] = g["best"]
        out[f"{kind}_now"] = float(D.remaining_wait([0.0], kind)[0])
        out[f"{kind}_at5"] = float(D.remaining_wait([5.0], kind)[0])
        out[f"{kind}_at10"] = float(D.remaining_wait([10.0], kind)[0])
    return out


def compute_confound() -> dict:
    c = D.confounded_delay()
    return c


def compute_grit() -> dict:
    a = archive.CREDE_2017.data
    r_gc = a["grit_conscientiousness"]["rho"]
    r_gy = a["grit_academic_performance"]["rho"]
    r_cy = np.linspace(0.0, 0.3, 61)
    inc = (r_gy - r_cy * r_gc) ** 2 / (1 - r_gc ** 2)
    beta = (r_gy - r_cy * r_gc) / (1 - r_gc ** 2)
    k = int(np.argmin(np.abs(r_cy - r_gy)))
    return {"r_gc": r_gc, "r_gy": r_gy, "r_cy": r_cy, "inc": inc, "beta": beta, "at_equal": float(inc[k]),
            "beta_equal": float(beta[k]), "alone": r_gy ** 2}


def compute_effort() -> dict:
    rewards = np.round(np.linspace(0.25, 8, 63), 3)
    e = D.evc_curve(rewards)
    diffs = np.round(np.linspace(0.0, 2.6, 53), 3)
    lo, hi = D.intensity(diffs, reward=4.0), D.intensity(diffs, reward=8.0)
    k = int(np.argmax(e["u"] > 0.5))
    return {"reward": rewards, "u": e["u"], "p": e["p"], "jump": float(rewards[k]), "difficulty": diffs,
            "u_lo": lo["u"], "u_hi": hi["u"], "p_lo": lo["p"], "p_hi": hi["p"],
            "quit_lo": float(diffs[int(np.argmax((diffs > 0.5) & (lo["u"] == 0)))]),
            "quit_hi": float(diffs[int(np.argmax((diffs > 0.5) & (hi["u"] == 0)))])}


ITEMS = {"stim": compute_stim, "thermostat": compute_thermostat, "weight": compute_weight,
         "arousal": compute_arousal, "salt": compute_salt, "perception": compute_perception,
         "atkinson": compute_atkinson, "titration": compute_titration, "literature": compute_literature,
         "rrr": compute_rrr, "waiting": compute_waiting, "confound": compute_confound, "grit": compute_grit,
         "effort": compute_effort}


if __name__ == "__main__":
    CACHE.main(ITEMS)

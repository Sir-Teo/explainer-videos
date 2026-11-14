"""Precompute every number in Part 11 of *Psychology, Built* ("The Threshold").

    python -m videos.psychology.psych11.compute            # everything missing (a few minutes), into .cache/psych11/
    python -m videos.psychology.psych11.compute --force fit

Results are cached in ``.cache/psych11/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The observer is
Psyche's (``explainer.psychology.psyche.psychophysics``): noise with a floor and a part that grows in proportion to
the stimulus, a 2% lapse rate.  Every simulated study that the film shows alone is picked by rule (the median of
101), never by its result.

Items:
    onyou      the eight trials of the hook, and what a lapse-free observer gets right on each
    weber      JNDs and Weber fractions across six decades; the floor; a near miss
    fechner    Fechner's staircase of JNDs and the logarithm it approaches; Ekman's alternative gives a power
    methods    the three classical methods on the observer: limits (and its criterion), adjustment, constant stimuli
    shapes     the psychometric function: three forms matched at threshold and slope; the four parameters
    fit        one study of 8 x 40 trials fitted by maximum likelihood; the likelihood surface; the bootstrap; a
               lapse that biases a fit with no lapse parameter
    stairs     two-down one-up and three-down one-up tracks; where they converge; small and large steps
    quest      a Bayesian staircase's placements and posterior; efficiency of three methods against trials
    stevens    magnitude estimation for three continua; the exponent table; cross-modality matching; range
    origin     two mechanisms with one JND curve: noise that grows, or a logarithmic code with fixed noise
    elsewhere  Weber's law for number and for time
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats

from explainer.ai.cache import Cache
from explainer.psychology import archive
from explainer.psychology.psyche import psychophysics as P

CACHE = Cache("psych11")
load = CACHE.load

OBS = P.Observer(k=0.08, sigma0=0.5, lapse=0.02)
CLEAN = P.Observer(k=0.08, sigma0=0.5, lapse=0.0)
STANDARD = 100.0
DELTAS = np.array([1.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0, 24.0])


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def _median_pick(values) -> int:
    v = np.asarray(values, float)
    return int(np.argsort(v)[len(v) // 2])


def _level(observer, p) -> float:
    return float(optimize.brentq(lambda d: float(observer.p_correct(STANDARD, d)) - p, 1e-3, 200))


# ---------------------------------------------------------------------------
def compute_onyou() -> dict:
    # eight trials, from easy to hard and back, on a standard grey of 100: increments in percent
    inc = np.array([24.0, 12.0, 6.0, 3.0, 1.5, 8.0, 2.0, 16.0])
    brighter = np.array([0, 1, 1, 0, 1, 0, 0, 1])  # which patch is brighter: 0 left, 1 right
    return {"increments": inc, "brighter": brighter, "p_clean": CLEAN.p_correct(STANDARD, inc),
            "jnd": float(P.jnd(CLEAN, STANDARD))}


def compute_weber() -> dict:
    s = np.logspace(-1, 5, 61)
    near = P.Observer(k=0.08, sigma0=0.5, lapse=0.0, near_miss=0.05)
    return {"standards": s, "jnd": P.jnd(CLEAN, s), "fraction": P.weber_fractions(CLEAN, s),
            "fraction_near": P.weber_fractions(near, s), "w": float(P.weber_fractions(CLEAN, 1e4)),
            "floor_at": float(CLEAN.sigma0 / CLEAN.k), "at_1": float(P.weber_fractions(CLEAN, 1.0)),
            "at_100": float(P.weber_fractions(CLEAN, 100.0)), "mcgill": archive.MCGILL_GOLDBERG_1968.data["slope"]}


def compute_fechner() -> dict:
    w, i0 = 0.08, 1.0
    steps = [i0]
    while steps[-1] < 1000:
        steps.append(steps[-1] * (1 + w))
    steps = np.array(steps)
    i = np.logspace(0, 3, 200)
    # Ekman's alternative: the sensation JND is a fixed fraction c of the sensation, so S grows as I^(c/w)
    c = 0.033
    return {"w": w, "steps": steps, "n_steps": len(steps) - 1, "i": i, "log_law": P.fechner(i, i0, w),
            "jnds_to_1000": float(P.fechner(1000.0, i0, w)), "c": c, "power_exponent": c / w,
            "log_norm": np.log(i) / math.log(1000.0), "power_norm": (i ** (c / w) - 1) / (1000.0 ** (c / w) - 1)}


def compute_methods() -> dict:
    g = rng(11)
    lim = P.method_of_limits(CLEAN, STANDARD, 40.0, 2.5, 8, g, criterion=1.0)
    series = [(np.asarray(lv), np.asarray(ans).astype(int)) for lv, ans in lim["series"]]
    crit = {}
    for c in (0.5, 1.0, 1.5):
        crit[f"crit_{c}"] = np.array([P.method_of_limits(CLEAN, STANDARD, 40.0, 2.5, 10, rng(100 + j), criterion=c)["threshold"]
                                      for j in range(200)])
    adj = P.method_of_adjustment(CLEAN, STANDARD, 20, rng(12))
    cs = P.constant_stimuli(OBS, STANDARD, DELTAS, 40, rng(13))
    out = {"limits_threshold": lim["threshold"], "limits_down": lim["descending"], "limits_up": lim["ascending"],
           "limits_points": lim["points"], "adj_settings": adj["settings"], "adj_pse": adj["pse"], "adj_sd": adj["sd"],
           "adj_jnd": adj["jnd_from_sd"], "cs_delta": cs["delta"], "cs_k": cs["k"], "cs_n": cs["n"],
           "jnd": float(P.jnd(CLEAN, STANDARD)), "yes50": float(math.sqrt(2) * CLEAN.sigma(STANDARD))}
    for c in (0.5, 1.0, 1.5):
        out[f"crit_{c}"] = float(np.median(crit[f"crit_{c}"]))
    for j, (lv, ans) in enumerate(series[:4]):
        out[f"series_{j}_levels"], out[f"series_{j}_answers"] = lv, ans
    return out


def compute_shapes() -> dict:
    x = np.linspace(0, 24, 241)
    # match the three forms at the 75% point and the slope there (Weibull alpha, beta solved numerically)
    a, b = 8.0, 3.5

    def slope(f, xx, h=1e-4):
        return (f(xx + h) - f(xx - h)) / (2 * h)

    gauss = lambda z: P.psychometric(z, a, b, 0.5, 0.0, "gauss")  # noqa: E731
    th = a + b * stats.norm.ppf(0.5)
    s_g = slope(gauss, th)
    beta_l = optimize.brentq(lambda bl: slope(lambda z: P.psychometric(z, th, bl, 0.5, 0.0, "logistic"), th) - s_g, 0.1, 20)

    def wb(params):
        al, be = params
        f = lambda z: P.psychometric(z, al, be, 0.5, 0.0, "weibull")  # noqa: E731
        return [float(f(th)) - 0.75, slope(f, th) - s_g]

    al, be = optimize.fsolve(wb, [th * 1.2, 2.5])
    return {"x": x, "gauss": gauss(x), "logistic": P.psychometric(x, th, beta_l, 0.5, 0.0, "logistic"),
            "weibull": P.psychometric(x, al, be, 0.5, 0.0, "weibull"), "threshold": float(th),
            "four": P.psychometric(x, 9.0, 3.0, 0.5, 0.06, "gauss"), "four_alpha": 9.0, "four_beta": 3.0,
            "four_gamma": 0.5, "four_lam": 0.06}


def compute_fit() -> dict:
    studies = [P.constant_stimuli(OBS, STANDARD, DELTAS, 40, rng(1000 + j)) for j in range(101)]
    fits = [P.fit(s["delta"], s["k"], s["n"], form="gauss") for s in studies]
    th = [P.threshold_at(f, 0.75) for f in fits]
    j = _median_pick(th)
    s, f = studies[j], fits[j]
    boot = P.bootstrap(s["delta"], s["k"], s["n"], f, n_boot=1000, rng=rng(2000))
    al = np.linspace(2, 16, 71)
    be = np.linspace(1, 12, 56)
    ll = np.zeros((len(be), len(al)))
    for r, b in enumerate(be):
        for c, a in enumerate(al):
            p = np.clip(P.psychometric(s["delta"], a, b, 0.5, f["lam"], "gauss"), 1e-9, 1 - 1e-9)
            ll[r, c] = float(np.sum(s["k"] * np.log(p) + (s["n"] - s["k"]) * np.log(1 - p)))
    true75 = _level(OBS, 0.75)
    # a lapse: the same study with one wrong answer more at the easiest level, fitted with and without a lapse rate
    k2 = s["k"].copy()
    k2[-1] = s["n"][-1] - 3
    no_lapse = P.fit(s["delta"], k2, s["n"], form="gauss", lam=0.0)
    with_lapse = P.fit(s["delta"], k2, s["n"], form="gauss")
    return {"delta": s["delta"], "k": s["k"], "n": s["n"], "alpha": f["alpha"], "beta": f["beta"], "lam": f["lam"],
            "threshold": th[j], "all_thresholds": np.array(th), "ci": boot["threshold_ci"], "boot": boot["threshold"],
            "true75": true75, "grid_alpha": al, "grid_beta": be, "loglik": ll, "deviance": f["deviance"],
            "k_lapse": k2, "beta_no_lapse": no_lapse["beta"], "beta_with_lapse": with_lapse["beta"],
            "th_no_lapse": P.threshold_at(no_lapse, 0.75), "th_with_lapse": P.threshold_at(with_lapse, 0.75),
            "lam_with_lapse": with_lapse["lam"], "boot_dev": boot["deviance"], "p_fit": boot["p_fit"]}


def compute_stairs() -> dict:
    out = {}
    for k_down in (2, 3):
        long = k_down == 3  # a 3-down staircase descends slowly from an easy start, so it gets 200 trials
        runs = [P.staircase(OBS, STANDARD, 30.0, factor=1.12, k_down=k_down, n_trials=200 if long else 80,
                            rng=rng(3000 + 100 * k_down + j), n_reversals_used=12 if long else 8) for j in range(101)]
        est = [r["estimate"] for r in runs]
        j = _median_pick(est)
        out[f"k{k_down}_levels"] = runs[j]["levels"]
        out[f"k{k_down}_correct"] = runs[j]["correct"].astype(int)
        out[f"k{k_down}_reversals"] = runs[j]["reversals"]
        out[f"k{k_down}_estimate"] = runs[j]["estimate"]
        out[f"k{k_down}_estimates"] = np.array(est)
        out[f"k{k_down}_median"] = float(np.median(est))
        out[f"k{k_down}_target"] = P.updown_target(k_down)
        out[f"k{k_down}_level"] = _level(OBS, P.updown_target(k_down))
    coarse = [P.staircase(OBS, STANDARD, 30.0, factor=1.5, k_down=2, n_trials=80, rng=rng(3500 + j))["estimate"] for j in range(301)]
    fine = [P.staircase(OBS, STANDARD, 30.0, factor=1.12, k_down=2, n_trials=200, rng=rng(3900 + j), n_reversals_used=12)["estimate"]
            for j in range(301)]
    out.update({"coarse_median": float(np.median(coarse)), "fine_median": float(np.median(fine))})
    return out


def compute_quest() -> dict:
    target = 0.82
    runs = [P.quest(OBS, STANDARD, 40, rng=rng(4000 + j), p_target=target) for j in range(101)]
    j = _median_pick([r["estimate"] for r in runs])
    q = runs[j]
    level = _level(OBS, target)
    # efficiency: the spread of threshold estimates against trials, for three methods aimed at their own targets
    ns = np.array([16, 24, 32, 48, 64, 96, 128])
    reps = 120
    sd = {"constant": [], "staircase": [], "quest": []}
    aims = {"constant": math.log(_level(OBS, 0.75)), "staircase": math.log(_level(OBS, P.updown_target(2))),
            "quest": math.log(level)}
    for n in ns:
        per = max(1, n // len(DELTAS))
        c_est, s_est, q_est = [], [], []
        for r in range(reps):
            cs = P.constant_stimuli(OBS, STANDARD, DELTAS, per, rng(5000 + 1000 * int(n) + r))
            f = P.fit(cs["delta"], cs["k"], cs["n"], form="gauss", lam=0.02)
            c_est.append(np.log(max(min(P.threshold_at(f, 0.75), 200.0), 0.5)))
            st = P.staircase(OBS, STANDARD, 30.0, factor=1.12, k_down=2, n_trials=int(n), rng=rng(6000 + 1000 * int(n) + r),
                             n_reversals_used=6)
            s_est.append(np.log(st["estimate"]))
            qq = P.quest(OBS, STANDARD, int(n), rng=rng(7000 + 1000 * int(n) + r), p_target=target)
            q_est.append(np.log(qq["estimate"]))
        # root mean square error in log units, against each method's own target level
        for name, est in (("constant", c_est), ("staircase", s_est), ("quest", q_est)):
            sd[name].append(float(np.sqrt(np.mean((np.array(est) - aims[name]) ** 2))))
    return {"placed": q["placed"], "correct": q["correct"].astype(int), "estimates": q["estimates"],
            "log_sd": q["log_sd"], "estimate": q["estimate"], "level": level, "target": target, "grid": q["grid"],
            "posterior": q["posterior"], "ns": ns, "sd_constant": np.array(sd["constant"]),
            "sd_staircase": np.array(sd["staircase"]), "sd_quest": np.array(sd["quest"])}


def compute_stevens() -> dict:
    table = archive.STEVENS_1957.data["exponents"]
    out = {"names": [t[0] for t in table], "exponents": np.array([t[1] for t in table])}
    i = np.logspace(0, 1, 7)
    for name, a, seed in (("brightness", 0.33, 1), ("heaviness", 1.45, 2), ("shock", 3.5, 3)):
        me = P.magnitude_estimation(i, a, 20, rng(8000 + seed), c=10.0)
        f = P.fit_power(me["intensity"], me["geometric_mean"])
        out[f"{name}_i"], out[f"{name}_geo"], out[f"{name}_fit"] = me["intensity"], me["geometric_mean"], f["exponent"]
    out["match_brightness_loudness"] = P.cross_modality(0.33, 0.67)
    # range: a person who maps any stimulus range onto the same span of numbers (1 to 100) half of the way
    a_true, ranges = 0.67, np.array([10.0, 100.0, 1000.0])
    fixed = 2.0 / np.log10(ranges)
    out["range_ratios"], out["range_exponents"] = ranges, 0.5 * a_true + 0.5 * fixed
    return out


def compute_origin() -> dict:
    s = np.logspace(0, 4, 41)
    # mechanism A: a linear code whose noise grows, sd = sqrt(sigma0^2 + (k I)^2)
    # mechanism B: a compressive code f(I) = asinh(k I / sigma0) / k (logarithmic above the floor) with noise of 1
    k, sigma0 = 0.08, 0.5
    z = math.sqrt(2) * stats.norm.ppf(0.75)
    jnd_a = z * np.sqrt(sigma0 ** 2 + (k * s) ** 2)
    jnd_b = sigma0 / k * np.sinh(np.arcsinh(k * s / sigma0) + z * k) - s
    code = np.arcsinh(k * s / sigma0) / k
    return {"standards": s, "jnd_a": jnd_a, "jnd_b": jnd_b, "code": code, "max_ratio": float(np.max(jnd_a / jnd_b)),
            "min_ratio": float(np.min(jnd_a / jnd_b))}


def compute_elsewhere() -> dict:
    h = archive.HALBERDA_2008.data
    w = h["adult_w"]
    ratios = np.linspace(1.0, 2.0, 101)
    out = {"ratios": ratios, "w_adult": w}
    for n_small, name in ((8, "small"), (16, "large")):
        big = n_small * ratios
        out[f"p_{name}"] = stats.norm.cdf((big - n_small) / (w * np.sqrt(big ** 2 + n_small ** 2)))
    z = stats.norm.ppf(0.75)
    for key, name in (("age3_ratio", "age3"), ("age6_ratio", "age6")):
        lo, hi = (float(v) for v in h[key].split(":"))
        r = hi / lo
        wv = (r - 1) / (z * math.sqrt(r ** 2 + 1))  # the Weber fraction that puts 75% correct at that ratio
        out[f"p_{name}"] = stats.norm.cdf((ratios - 1) / (wv * np.sqrt(ratios ** 2 + 1)))
        out[f"w_{name}"], out[f"r_{name}"] = wv, r
    # timing: produced intervals with a constant coefficient of variation
    cv = 0.15
    targets = np.array([2.0, 4.0, 8.0, 16.0])
    g = rng(9000)
    out["time_targets"], out["time_cv"] = targets, cv
    for t in targets:
        out[f"time_{int(t)}"] = t * (1 + cv * g.standard_normal(400))
    return out


def compute_goodfit() -> dict:
    """Goodness of fit.  The same design run on an observer whose attention wanders between blocks of ten trials
    (its threshold moves by a factor drawn each block), so its counts vary more than a binomial allows.  A curve
    still fits; the deviance says it fits worse than its own repeats would.  The study shown is the median of 41 by
    its p-value."""
    studies, fits, boots = [], [], []
    for j in range(41):
        g = rng(5000 + j)
        k = np.zeros(len(DELTAS), dtype=int)
        for _ in range(4):  # four blocks of ten trials at every level
            shift = math.exp(0.6 * g.standard_normal())
            o = P.Observer(k=OBS.k * shift, sigma0=OBS.sigma0, lapse=OBS.lapse)
            k += np.array([sum(o.respond(STANDARD, d, g) for _ in range(10)) for d in DELTAS])
        n = np.full(len(DELTAS), 40)
        f = P.fit(DELTAS, k, n, form="gauss")
        studies.append(k)
        fits.append(f)
        boots.append(P.bootstrap(DELTAS, k, n, f, n_boot=300, rng=rng(6000 + j)))
    ps = np.array([b["p_fit"] for b in boots])
    j = _median_pick(ps)
    return {"k": studies[j], "n": np.full(len(DELTAS), 40), "delta": np.asarray(DELTAS, dtype=float),
            "alpha": fits[j]["alpha"], "beta": fits[j]["beta"], "lam": fits[j]["lam"], "deviance": fits[j]["deviance"],
            "boot_dev": boots[j]["deviance"], "p_fit": float(ps[j]), "p_all": ps,
            "share_rejected": float(np.mean(ps < 0.05))}


def compute_wander() -> dict:
    """What wandering attention does to the curve: 101 studies of a steady observer and 101 of one whose threshold
    moves between blocks of ten trials (as in ``goodfit``); the fitted slopes and 75% thresholds."""
    out = {}
    for name, sd in (("steady", 0.0), ("wander", 0.6)):
        betas, ths = [], []
        for j in range(101):
            g = rng(7000 + j)
            k = np.zeros(len(DELTAS), dtype=int)
            for _ in range(4):
                o = P.Observer(k=OBS.k * math.exp(sd * g.standard_normal()), sigma0=OBS.sigma0, lapse=OBS.lapse)
                k += np.array([sum(o.respond(STANDARD, d, g) for _ in range(10)) for d in DELTAS])
            f = P.fit(DELTAS, k, np.full(len(DELTAS), 40), form="gauss")
            betas.append(f["beta"])
            ths.append(P.threshold_at(f, 0.75))
        out[f"{name}_beta"], out[f"{name}_th"] = float(np.median(betas)), float(np.median(ths))
    out["true75"] = _level(OBS, 0.75)
    return out


def compute_bisection() -> dict:
    """A grey midway between a black (4% reflectance) and a white (85%): the physical mean, Fechner's (the
    geometric mean), a power law with brightness's exponent, and CIE lightness (a cube root with an offset)."""
    b, w = 0.04, 0.85
    cie = lambda y: 116 * y ** (1 / 3) - 16  # noqa: E731
    cie_inv = lambda l: ((l + 16) / 116) ** 3  # noqa: E731
    return {"black": b, "white": w, "mean": (b + w) / 2, "fechner": math.sqrt(b * w),
            "power": ((b ** (1 / 3) + w ** (1 / 3)) / 2) ** 3, "cie": cie_inv((cie(b) + cie(w)) / 2),
            "cie_50": cie_inv(50.0)}


def compute_thurstone() -> dict:
    """Thurstone's Case V on 200 simulated judges comparing six offences whose seriousness is planted."""
    names = ["fare dodging", "shoplifting", "vandalism", "burglary", "assault", "arson"]
    planted = np.array([0.0, 0.35, 0.6, 1.45, 1.8, 2.3])
    p = P.paired_comparisons(planted, 200, rng(8000))
    scale = P.thurstone_case_v(p)
    unit = (planted - planted.mean()) / math.sqrt(2)
    return {"names": names, "planted": planted, "p": p, "scale": scale, "planted_scaled": unit,
            "max_error": float(np.max(np.abs(scale - unit))), "judges": 200}


def compute_tvi() -> dict:
    """Threshold against intensity for an eye-like observer: a dark-light floor, photon noise (variance in
    proportion to intensity) and Weber noise.  Slopes 0, 1/2 and 1 on log-log axes."""
    o = P.Observer(k=0.02, sigma0=0.05, lapse=0.0, poisson=1.0)
    i = np.logspace(-4, 7, 221)
    j = P.jnd(o, i)
    slope = np.gradient(np.log10(j), np.log10(i))
    return {"intensity": i, "jnd": j, "slope": slope, "k": o.k, "sigma0": o.sigma0, "poisson": o.poisson,
            "to_root": o.sigma0 ** 2 / o.poisson, "to_weber": o.poisson / o.k ** 2,
            "slope_low": float(slope[0]), "slope_mid": float(np.interp(0.0, np.log10(i), slope)),
            "slope_high": float(slope[-1])}


def compute_money() -> dict:
    """Bernoulli's rule: the value of a small gain is inversely proportional to wealth, so value is a logarithm."""
    w = np.linspace(1, 1000, 400)
    gains = {f"gain_at_{v}": float(math.log((v + 10) / v)) for v in (10, 100, 1000)}
    return {"wealth": w, "value": np.log(w), "ratio_10_1000": float(math.log(20 / 10) / math.log(1010 / 1000)), **gains}


def compute_triangle() -> dict:
    """The triangle test: three samples, two the same; pick the odd one.  Guessing is right a third of the time."""
    ns = np.array([12, 18, 24, 30, 36, 48, 60, 72, 90, 120])
    crit = np.array([P.triangle_critical(int(n)) for n in ns])
    ds = np.linspace(0, 0.6, 61)
    power = {int(n): np.array([P.triangle_power(int(n), d) for d in ds]) for n in (12, 30, 60, 120)}
    need = next(int(n) for n in range(6, 400) if P.triangle_power(n, 0.3) >= 0.8)
    need_small = next(int(n) for n in range(6, 2000) if P.triangle_power(n, 0.1) >= 0.8)
    return {"ns": ns, "crit": crit, "d": ds, **{f"power_{n}": v for n, v in power.items()},
            "crit_30": P.triangle_critical(30), "need_30pct": need, "need_10pct": need_small,
            "power_30_at_30": P.triangle_power(30, 0.3), "chance_30": float(stats.binom.sf(P.triangle_critical(30) - 1,
                                                                                           30, 1 / 3))}


def compute_audio() -> dict:
    """A pure-tone threshold by the Hughson-Westlake rule on a yes-no listener: down 10 dB after a response, up 5 dB
    after none; the threshold is the lowest level heard on 2 of 3 ascending presentations.  The listener hears a
    tone at level L (dB) with probability Phi((L - T) / 3), with T = 25 dB, and answers with no false alarms."""
    g = rng(9500)
    true_t, sd = 25.0, 3.0
    level, heard_prev = 40.0, None
    levels, heard = [], []
    ascending_hits: dict = {}
    ascending_tries: dict = {}
    answer = None
    for _ in range(40):
        h = bool(g.random() < stats.norm.cdf((level - true_t) / sd))
        ascending = heard_prev is False
        levels.append(level)
        heard.append(h)
        if ascending:
            ascending_tries[level] = ascending_tries.get(level, 0) + 1
            if h:
                ascending_hits[level] = ascending_hits.get(level, 0) + 1
                if ascending_hits[level] >= 2 and ascending_tries[level] <= 3:
                    answer = level
                    break
        heard_prev = h
        level = level - 10 if h else level + 5
    return {"levels": np.array(levels), "heard": np.array(heard).astype(int), "threshold": answer, "true": true_t,
            "fifty": true_t}


ITEMS = {
    "onyou": compute_onyou,
    "weber": compute_weber,
    "fechner": compute_fechner,
    "methods": compute_methods,
    "shapes": compute_shapes,
    "fit": compute_fit,
    "stairs": compute_stairs,
    "quest": compute_quest,
    "stevens": compute_stevens,
    "origin": compute_origin,
    "elsewhere": compute_elsewhere,
    "audio": compute_audio,
    "goodfit": compute_goodfit,
    "wander": compute_wander,
    "tvi": compute_tvi,
    "bisection": compute_bisection,
    "thurstone": compute_thurstone,
    "money": compute_money,
    "triangle": compute_triangle,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

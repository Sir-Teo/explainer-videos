"""Psyche at work (Part 51): an operator model for human factors.

Fitts's law and the Hick-Hyman law for controls and choices; a compatibility cost; a vigilance watch analysed by
signal detection block by block (Part 12); the prevalence effect as a criterion set for rare targets; workload by
NASA-TLX weighting; takeover after automation (the ironies of automation); alarm thresholds, their positive
predictive value and the operators who learn to ignore them; the Swiss cheese model with independent and
correlated holes; and fatigue as hours awake against blood-alcohol equivalents.

Part 52 (designing for minds) adds the Model Human Processor's cycle times; the keystroke-level model; pointing
throughput with the effective width and the steering law; a menu model of depth against breadth; an information
forager and the marginal value theorem; the problem-discovery curve with users who differ in what they find;
graphical perception as Stevens's power law plus noise; WCAG contrast; and habit formation curves.

Part 53 (people at work) adds a selection simulator: observed validity under unreliability and range restriction and
their corrections, Taylor-Russell success rates, the Brogden-Cronbach-Gleser utility, adverse impact and the
validity-diversity frontier; an interview-noise model and holistic against mechanical combination.

Part 54 (the science of learning) adds a review scheduler on Part 21's memory model (Pavlik and Anderson's
activation): massed, fixed, expanding and model-based policies compared at an equal number of reviews; and the
simple view of reading.

Part 55 (behaviour change at scale) adds the inertia algebra of defaults, a megastudy simulator (many arms with
small true effects, the winner's curse and empirical-Bayes shrinkage), and a publication filter that reproduces the
gap between published nudges and nudge-unit trials.

Part 56 (psychology and law) adds line-ups by signal detection (simultaneous with the max rule, sequential with a
first-past-the-criterion stop rule) with their ROC curves, diagnosticity ratios and partial areas, confidence and
the inflation feedback causes, a risk score's error rates across groups with different base rates (the
impossibility result), and the interval around an IQ score.

Part 57 (health and care) adds an expectation model of placebo analgesia (Part 14's observer combining a sensory
signal with an expected level) and a stepped-care simulator (weekly referrals, low- and high-intensity capacity,
waiting lists, stepping up non-responders).  numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


# ----------------------------------------------------------------------------------------------------------------
# Controls and choices
# ----------------------------------------------------------------------------------------------------------------
def fitts_mt(distance, width, a: float = 0.05, b: float = 0.15):
    """Fitts's law, Shannon form: movement time = a + b log2(D/W + 1), in seconds."""
    return a + b * np.log2(np.asarray(distance, float) / np.asarray(width, float) + 1)


def fitts_trials(n: int = 400, seed: int = 0) -> dict:
    """Simulated pointing: targets at several distances and widths; times with lognormal noise around the law;
    the fitted intercept and slope."""
    rng = np.random.default_rng(seed)
    D = rng.choice([64, 128, 256, 512], n)
    W = rng.choice([8, 16, 32, 64], n)
    ID = np.log2(D / W + 1)
    t = fitts_mt(D, W) * np.exp(rng.normal(0, 0.12, n))
    b, a = np.polyfit(ID, t, 1)
    return {"ID": ID, "t": t, "a": float(a), "b": float(b), "r": float(np.corrcoef(ID, t)[0, 1])}


def hick_rt(n_choices, a: float = 0.2, b: float = 0.15, compatible: bool = True, cost: float = 0.12):
    """The Hick-Hyman law, RT = a + b log2(N + 1), plus a translation cost when the stimulus-response mapping is
    incompatible."""
    n = np.asarray(n_choices, float)
    return a + b * np.log2(n + 1) + (0.0 if compatible else cost * np.log2(n + 1))


# ----------------------------------------------------------------------------------------------------------------
# Vigilance and rare targets
# ----------------------------------------------------------------------------------------------------------------
def vigilance(minutes: int = 120, block: int = 30, events_per_min: float = 20, p_signal: float = 0.012,
              d0: float = 2.6, d_loss: float = 0.5, c0: float = 0.6, c_gain: float = 0.6, watchers: int = 1,
              seed: int = 0) -> dict:
    """Mackworth's clock: a pointer jumps every few seconds, and occasionally jumps double.  The watcher's
    sensitivity falls and criterion rises over the watch (both linear in time).  Hits and false alarms are
    simulated per block and d' and c are re-estimated from them, as an experimenter would."""
    rng = np.random.default_rng(seed)
    nb = minutes // block
    out = {"block_end": [], "hit": [], "fa": [], "d": [], "c": [], "d_true": [], "c_true": []}
    for k in range(nb):
        mid = (k + 0.5) / nb
        d = d0 - d_loss * mid
        c = c0 + c_gain * mid
        n = int(events_per_min * block) * watchers
        sig = rng.random(n) < p_signal
        x = rng.normal(0, 1, n) + d * sig
        say = x > d / 2 + c
        H = (say & sig).sum() + 0.5
        F = (say & ~sig).sum() + 0.5
        h, f = H / (sig.sum() + 1), F / ((~sig).sum() + 1)
        out["block_end"].append((k + 1) * block)
        out["hit"].append(h); out["fa"].append(f)
        out["d"].append(stats.norm.ppf(h) - stats.norm.ppf(f)); out["c"].append(-(stats.norm.ppf(h) + stats.norm.ppf(f)) / 2)
        out["d_true"].append(d); out["c_true"].append(c)
    return {k: np.array(v) for k, v in out.items()}


def prevalence(prevs=(0.5, 0.1, 0.02, 0.01, 0.001), d: float = 2.0) -> dict:
    """An observer who sets the criterion that maximizes accuracy for the prevalence p (beta = (1 - p)/p): the
    miss rate and false-alarm rate at each prevalence."""
    prevs = np.asarray(prevs, float)
    beta = (1 - prevs) / prevs
    c = np.log(beta) / d
    miss = stats.norm.cdf(c - d / 2)
    fa = stats.norm.sf(c + d / 2)
    return {"prev": prevs, "c": c, "miss": miss, "fa": fa}


def prevalence_partial(prevs=(0.5, 0.1, 0.02, 0.01), d: float = 2.0, shift: float = 0.5) -> dict:
    """People shift their criterion only part of the way toward the optimum (the share ``shift`` of the way, on the log-beta scale):
    misses still rise sharply as targets get rare."""
    prevs = np.asarray(prevs, float)
    c = shift * np.log((1 - prevs) / prevs) / d
    return {"prev": prevs, "miss": stats.norm.cdf(c - d / 2), "fa": stats.norm.sf(c + d / 2)}


# ----------------------------------------------------------------------------------------------------------------
# Workload
# ----------------------------------------------------------------------------------------------------------------
TLX = ("mental", "physical", "temporal", "performance", "effort", "frustration")


def nasa_tlx(ratings, weights) -> float:
    """NASA-TLX: six ratings (0-100) weighted by how often each scale was chosen in the 15 pairwise comparisons."""
    r, w = np.asarray(ratings, float), np.asarray(weights, float)
    assert w.sum() == 15
    return float(np.sum(r * w) / 15)


# ----------------------------------------------------------------------------------------------------------------
# Automation
# ----------------------------------------------------------------------------------------------------------------
def takeover(reliabilities=(0.9, 0.99, 0.999, 0.9999), budget: float = 7.0, base: float = 2.5, seed: int = 0,
             n: int = 20000) -> dict:
    """Bainbridge's irony, as a model: the more reliable the automation, the rarer the operator's practice and the
    lower their expectation of a failure, so the slower and less skilled the takeover.  Takeover time is lognormal
    with a median that grows with log10 of the mean time between failures; the share of takeovers completed within
    the time ``budget``, and the overall failure rate per demand (automation failure times failed takeover)."""
    rng = np.random.default_rng(seed)
    rel = np.asarray(reliabilities, float)
    mtbf = 1 / (1 - rel)
    med = base * (1 + 0.35 * np.log10(mtbf))
    within, system = [], []
    for m, r in zip(med, rel):
        t = rng.lognormal(np.log(m), 0.45, n)
        w = float(np.mean(t < budget))
        within.append(w)
        system.append((1 - r) * (1 - w))
    return {"reliability": rel, "median_s": med, "within": np.array(within), "system_fail": np.array(system)}


def alarm(base_rate: float = 0.01, d: float = 2.5, thresholds=None) -> dict:
    """An alarm on a noisy sensor: for each threshold, the hit rate, the false-alarm rate, the positive predictive
    value, and, if operators come to respond to an alarm with probability equal to its PPV (Bliss's probability
    matching), the share of real events that get a response."""
    th = np.linspace(-0.5, 3.5, 41) if thresholds is None else np.asarray(thresholds, float)
    hit = stats.norm.sf(th - d)
    fa = stats.norm.sf(th)
    ppv = base_rate * hit / (base_rate * hit + (1 - base_rate) * fa)
    caught = hit * ppv
    return {"threshold": th, "hit": hit, "fa": fa, "ppv": ppv, "caught": caught,
            "best": float(th[int(np.argmax(caught))]), "best_caught": float(caught.max())}


# ----------------------------------------------------------------------------------------------------------------
# Systems
# ----------------------------------------------------------------------------------------------------------------
def swiss_cheese(layers: int = 4, hole: float = 0.1, rho: float = 0.0, n: int = 400000, seed: int = 0) -> float:
    """Reason's model: an accident needs a hole in every layer.  Holes are open with probability ``hole``; with
    correlation ``rho`` between layers (shared fatigue, a shared culture), via a Gaussian copula."""
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((n, layers)) * np.sqrt(1 - rho) + np.sqrt(rho) * rng.standard_normal((n, 1))
    return float(np.mean(np.all(z < stats.norm.ppf(hole), axis=1)))


# ----------------------------------------------------------------------------------------------------------------
# Fatigue
# ----------------------------------------------------------------------------------------------------------------
def awake_bac(hours) -> np.ndarray:
    """Dawson and Reid's (1997) equivalence, as reported: after about 17 hours awake, performance like a
    blood-alcohol concentration of 0.05%; after about 24 hours, like 0.10%.  Linear between 10 and 26 hours, zero
    before 10."""
    h = np.asarray(hours, float)
    return np.clip(0.05 + (h - 17) * (0.05 / 7), 0, None) * (h >= 10)


# ----------------------------------------------------------------------------------------------------------------
# Part 52: designing for minds
# ----------------------------------------------------------------------------------------------------------------
MHP = {"perceptual": (100, 50, 200), "cognitive": (70, 25, 170), "motor": (70, 30, 100)}
"""Card, Moran and Newell's (1983) processor cycle times in ms: (typical, fastest, slowest)."""

KLM = {"K": 0.28, "P": 1.10, "B": 0.10, "H": 0.40, "M": 1.35}
"""Keystroke-level operators in seconds (Card, Moran and Newell 1980): K a keystroke (an average non-secretarial
typist), P point with a mouse, B a button press or release, H home the hand between keyboard and mouse, M mental
preparation.  R, the system's response time, is given per task."""


def mhp_reaction(kind: str = "simple") -> dict:
    """The Model Human Processor's predictions: a simple reaction is one perceptual, one cognitive and one motor
    cycle; a physical match adds a cognitive cycle, a name match two (Posner's tasks, Part 1).  Typical, fastest and
    slowest totals in ms."""
    extra = {"simple": 0, "physical": 1, "name": 2}[kind]
    p, c, m = MHP["perceptual"], MHP["cognitive"], MHP["motor"]
    return {k: p[i] + (1 + extra) * c[i] + m[i] for i, k in enumerate(("typical", "fast", "slow"))}


def klm_time(ops: str, response: float = 0.0, k: float | None = None) -> float:
    """The keystroke-level model: the time of a method written as a string of operators (``"MHPBB"``), plus the
    system's response time.  ``k`` overrides the keystroke time (0.12 s for a skilled typist, 1.2 s for a novice)."""
    t = 0.0
    for o in ops.replace(" ", ""):
        t += (k if (o == "K" and k is not None) else KLM[o])
    return t + response


def klm_place_m(ops: str) -> str:
    """A simplified form of Card, Moran and Newell's heuristics for mental operators: an M before each P that
    starts a new step and before each run of keystrokes that forms one unit (a word, a number), none inside a run or
    between a point and its click."""
    out, prev = [], ""
    for o in ops:
        if o == "P" and prev not in ("P",):
            out.append("M")
        if o == "K" and prev != "K":
            out.append("M")
        out.append(o)
        prev = o
    return "".join(out)


def fitts_effective(n: int = 30, distance: float = 256, width: float = 32, sd_scale: float = 0.25,
                    a: float = 0.1, b: float = 0.12, seed: int = 0) -> dict:
    """One pointing condition with the endpoints recorded: the effective width (4.133 times the SD of the endpoints,
    which covers 96% of a normal spread), the effective index of difficulty and the throughput in bits per second
    (MacKenzie; ISO 9241-9).  Endpoint SD is ``sd_scale`` times the nominal width."""
    rng = np.random.default_rng(seed)
    ends = rng.normal(0, sd_scale * width, n)
    t = (a + b * np.log2(distance / width + 1)) * np.exp(rng.normal(0, 0.1, n))
    we = 4.133 * ends.std(ddof=1)
    ide = np.log2(distance / we + 1)
    return {"ends": ends, "t": t, "We": float(we), "IDe": float(ide), "ID": float(np.log2(distance / width + 1)),
            "throughput": float(ide / t.mean()), "errors": float(np.mean(np.abs(ends) > width / 2))}


def steering_time(length, width, a: float = 0.2, b: float = 0.08):
    """The steering law (Accot and Zhai 1997): moving through a tunnel of length A and width W takes a + b A/W."""
    return a + b * np.asarray(length, float) / np.asarray(width, float)


def menu_time(items: int = 64, breadth=(2, 4, 8, 16, 32, 64), a: float = 0.2, b: float = 0.15,
              read: float = 0.0, point: float = 0.6, practised: bool = True) -> dict:
    """Selecting one of ``items`` from a hierarchy of menus of a given breadth: depth = log_b(items) levels, each
    costing a choice (Hick-Hyman, if the user knows the menu, or a linear scan of ``read`` seconds per item if not)
    and a pointing movement.  Returns time by breadth."""
    out = []
    for br in breadth:
        depth = np.log(items) / np.log(br)
        choose = a + b * np.log2(br + 1) if practised else a + read * (br + 1) / 2
        out.append(depth * (choose + point))
    return {"breadth": np.array(breadth), "time": np.array(out), "depth": np.log(items) / np.log(np.array(breadth))}


def patch_gain(t, total: float = 10.0, tau: float = 30.0):
    """Information found in a patch (a page, a search result list) after ``t`` seconds: diminishing returns."""
    return total * (1 - np.exp(-np.asarray(t, float) / tau))


def mvt_leave(travel: float, total: float = 10.0, tau: float = 30.0) -> dict:
    """Charnov's marginal value theorem for an information forager (Pirolli and Card 1999): leave a patch when its
    instantaneous rate of gain falls to the best overall rate, g'(t) = g(t)/(t + travel).  Solved numerically."""
    from scipy.optimize import brentq

    f = lambda t: (total / tau) * np.exp(-t / tau) * (t + travel) - patch_gain(t, total, tau)
    t_star = brentq(f, 1e-6, 50 * tau)
    return {"t": float(t_star), "rate": float(patch_gain(t_star, total, tau) / (t_star + travel))}


def discovery(n_users, p=None, n_problems: int = 100, a: float = None, b: float = None, seed: int = 0,
              reps: int = 400) -> dict:
    """The share of usability problems found by n users.  With one detection probability p for every problem the
    curve is 1 - (1 - p)^n (Nielsen and Landauer 1993).  With problems that differ (p ~ Beta(a, b) with the same
    mean), the curve rises more slowly: rare problems need many users.  Returns both curves, the second simulated."""
    n = np.asarray(n_users)
    p = p if p is not None else a / (a + b)
    homog = 1 - (1 - p) ** n
    rng = np.random.default_rng(seed)
    if a is None:
        return {"n": n, "homog": homog}
    found = np.zeros(len(n))
    for _ in range(reps):
        ps = rng.beta(a, b, n_problems)
        found += 1 - np.mean((1 - ps)[None, :] ** n[:, None], axis=1)
    return {"n": n, "homog": homog, "hetero": found / reps, "mean_p": p}


STEVENS_EXP = {"position": 1.0, "length": 1.0, "angle": 0.85, "area": 0.7, "volume": 0.6, "colour": 0.5}
"""Exponents of perceived magnitude used for the encodings (length about 1, area about 0.7, volume about 0.6 in
Stevens's tables; angle and colour saturation illustrative)."""

ENC_NOISE = {"position": 0.09, "length": 0.11, "angle": 0.13, "area": 0.16, "volume": 0.2, "colour": 0.25}
"""Relative judgement noise for each encoding (illustrative, ordered as in Cleveland and McGill's ranking)."""


def graphical_error(encoding: str, n: int = 2000, seed: int = 0, calibrate: bool = False) -> dict:
    """Judging what percentage a smaller mark is of a larger one, as in Cleveland and McGill (1984): the perceived
    ratio is the true ratio to the encoding's Stevens exponent, with multiplicative noise.  The error measure is
    theirs: log2(|judged - true| + 1/8), in percentage points."""
    rng = np.random.default_rng(seed)
    true = rng.uniform(10, 90, n)
    e = STEVENS_EXP[encoding] if not calibrate else 1.0
    judged = 100 * (true / 100) ** e * np.exp(rng.normal(0, ENC_NOISE[encoding], n))
    judged = np.clip(judged, 0, 100)
    err = np.log2(np.abs(judged - true) + 0.125)
    return {"true": true, "judged": judged, "log_err": float(err.mean()), "mae": float(np.mean(np.abs(judged - true)))}


def relative_luminance(rgb) -> float:
    """WCAG 2 relative luminance of an sRGB colour given as 0-255 integers."""
    c = np.asarray(rgb, float) / 255
    lin = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return float(0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2])


def contrast_ratio(fg, bg) -> float:
    """WCAG 2 contrast ratio (L1 + 0.05)/(L2 + 0.05), from 1 to 21.  Normal text needs 4.5 for level AA."""
    l1, l2 = sorted((relative_luminance(fg), relative_luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def habit_curve(days, asymptote: float = 100.0, t95: float = 66.0):
    """Automaticity rising to an asymptote, as Lally and colleagues (2010) modelled it: 95% of the asymptote is
    reached at ``t95`` days."""
    k = np.log(20) / t95
    return asymptote * (1 - np.exp(-k * np.asarray(days, float)))


def habit_people(n: int = 96, median: float = 66.0, sigma: float = 0.65, seed: int = 0) -> np.ndarray:
    """Days to reach 95% of each person's plateau, lognormal around a median of 66 days (illustrative spread; Lally
    and colleagues reported a range of about 18 to 254 days)."""
    rng = np.random.default_rng(seed)
    return np.exp(np.log(median) + sigma * rng.standard_normal(n))


# ----------------------------------------------------------------------------------------------------------------
# Part 53: people at work
# ----------------------------------------------------------------------------------------------------------------
def selection(n: int = 200000, validity: float = 0.5, crit_rel: float = 0.6, ratio: float = 0.2,
              seed: int = 0) -> dict:
    """Applicants with a predictor score X and true performance T correlated ``validity``; the criterion that is
    actually observed (a supervisor's rating) has reliability ``crit_rel`` among applicants.  Hire the top ``ratio``
    on X.  Returns the observed validity among the hired; that validity corrected for range restriction alone
    (Thorndike's Case II); corrected for criterion unreliability alone (with the incumbents' reliability, which is
    lower than the applicants'); corrected for both, in that order; and the applicant-population truth."""
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(n)
    t = validity * x + np.sqrt(1 - validity ** 2) * rng.standard_normal(n)
    true_part = np.sqrt(crit_rel) * t
    y = true_part + np.sqrt(1 - crit_rel) * rng.standard_normal(n)
    hired = x >= np.quantile(x, 1 - ratio)
    r_obs = float(np.corrcoef(x[hired], y[hired])[0, 1])
    rel_inc = float(true_part[hired].var() / y[hired].var())
    u = float(x.std() / x[hired].std())
    r_rel = r_obs / np.sqrt(rel_inc)
    return {"r_obs": r_obs, "rel_incumbents": rel_inc, "u": u, "r_rr_only": float(case2(r_obs, u)),
            "r_rel_only": float(r_rel), "r_both": float(case2(r_rel, u)),
            "r_all_true": float(np.corrcoef(x, t)[0, 1]), "r_all_obs": float(np.corrcoef(x, y)[0, 1]),
            "x": x[:3000], "y": y[:3000], "hired": hired[:3000]}


def case2(r: float, u: float) -> float:
    """Thorndike's Case II correction for direct range restriction: u = SD(applicants)/SD(hired) on the predictor."""
    return r * u / np.sqrt(1 + r ** 2 * (u ** 2 - 1))


def taylor_russell(validity: float, base_rate: float, ratio: float) -> float:
    """The share of those selected who succeed (Taylor and Russell 1939): bivariate normal with correlation
    ``validity``; success is the top ``base_rate`` of performance, selection the top ``ratio`` of the predictor."""
    xc, yc = stats.norm.ppf(1 - ratio), stats.norm.ppf(1 - base_rate)
    cov = [[1, validity], [validity, 1]]
    both = 1 - stats.norm.cdf(xc) - stats.norm.cdf(yc) + stats.multivariate_normal(mean=[0, 0], cov=cov).cdf([xc, yc])
    return float(both / ratio)


def bcg_utility(validity: float, ratio: float, sd_y: float, n_hired: int = 100, years: float = 5.0,
                cost_per_applicant: float = 0.0) -> dict:
    """The Brogden-Cronbach-Gleser utility of a selection procedure against random hiring: n_hired x years x
    validity x SD_y x (mean standardized predictor score of those hired), minus testing costs.  The mean score of
    the top ``ratio`` is phi(z)/ratio."""
    z = stats.norm.ppf(1 - ratio)
    zbar = stats.norm.pdf(z) / ratio
    gain = n_hired * years * validity * sd_y * zbar
    cost = cost_per_applicant * n_hired / ratio
    return {"zbar": float(zbar), "gain": float(gain), "cost": float(cost), "net": float(gain - cost)}


def adverse_impact(d: float, ratio: float, minority_share: float = 0.3) -> dict:
    """Two applicant groups whose predictor means differ by ``d`` SD; one cut gives the overall selection ratio.
    Returns each group's selection rate and the impact ratio (the four-fifths rule flags < 0.8)."""
    from scipy.optimize import brentq

    f = lambda c: (1 - minority_share) * stats.norm.sf(c) + minority_share * stats.norm.sf(c + d) - ratio
    c = brentq(f, -6, 6)
    maj, mino = stats.norm.sf(c), stats.norm.sf(c + d)
    return {"cut": float(c), "majority": float(maj), "minority": float(mino), "impact_ratio": float(mino / maj)}


def frontier(r1: float = 0.31, d1: float = 0.8, r2: float = 0.42, d2: float = 0.3, r12: float = 0.3,
             ratio: float = 0.2, weights=None) -> dict:
    """The validity-diversity trade-off (De Corte, Lievens and Sackett): a composite w X1 + (1 - w) X2 of a predictor
    with validity r1 and group difference d1 and one with r2, d2, intercorrelated r12.  For each weight, the
    composite's validity and group difference, and the impact ratio at the given selection ratio."""
    ws = np.linspace(0, 1, 21) if weights is None else np.asarray(weights, float)
    val, dd, ir = [], [], []
    for w in ws:
        a, b = w, 1 - w
        sd = np.sqrt(a ** 2 + b ** 2 + 2 * a * b * r12)
        val.append((a * r1 + b * r2) / sd)
        dd.append((a * d1 + b * d2) / sd)
        ir.append(adverse_impact(dd[-1], ratio)["impact_ratio"])
    return {"w": ws, "validity": np.array(val), "d": np.array(dd), "impact": np.array(ir)}


def interviews(n: int = 4000, seed: int = 0, test_validity: float = 0.31, unstructured_noise: float = 2.2,
               structured_noise: float = 0.6, holistic_weight: float = 0.7) -> dict:
    """An interview-noise model.  Performance depends on a trait the interview partly sees; an unstructured
    interview's rating adds a large impression error (rapport, first impressions, rater idiosyncrasy), a structured
    one a smaller error.  A recruiter combining the test and an unstructured impression holistically, weighting the
    impression ``holistic_weight``, can do worse than the test alone (Dana, Dawes and Peterson 2013)."""
    rng = np.random.default_rng(seed)
    g = rng.standard_normal(n)  # what the test measures
    s = rng.standard_normal(n)  # what a good interview can see (job-relevant skills)
    perf = test_validity * g + 0.45 * s + np.sqrt(max(1 - test_validity ** 2 - 0.45 ** 2, 0.05)) * rng.standard_normal(n)
    test = g + 0.4 * rng.standard_normal(n)
    uns = s + unstructured_noise * rng.standard_normal(n)
    struct = s + structured_noise * rng.standard_normal(n)
    z = lambda v: (v - v.mean()) / v.std()
    holistic = holistic_weight * z(uns) + (1 - holistic_weight) * z(test)
    beta = np.linalg.lstsq(np.column_stack([np.ones(n), z(test), z(struct)]), perf, rcond=None)[0]
    mech = beta[1] * z(test) + beta[2] * z(struct)
    r = lambda v: float(np.corrcoef(v, perf)[0, 1])
    return {"test": r(test), "unstructured": r(uns), "structured": r(struct), "holistic": r(holistic),
            "mechanical": r(mech), "test_plus_unstructured_equal": r(z(test) + z(uns))}


# ----------------------------------------------------------------------------------------------------------------
# Part 54: the science of learning
# ----------------------------------------------------------------------------------------------------------------
def pa_activation_capped(times, now, c: float = 0.25, a: float = 0.18, d_max: float = 1.0) -> float:
    """Part 21's Pavlik-Anderson activation with each trace's decay capped at ``d_max``.  Uncapped, presentations a
    few minutes apart feed each other's decay rates until they overflow; the cap keeps massed study well defined
    (its traces simply decay at the fastest allowed rate).  Times in days."""
    times = np.sort(np.asarray(times, float))
    ds = []
    for j, tj in enumerate(times):
        if j == 0:
            ds.append(a)
            continue
        ages = np.maximum(tj - times[:j], 1e-6)
        m = np.log(np.sum(ages ** (-np.array(ds))))
        ds.append(min(c * np.exp(m) + a, d_max))
    ages = np.maximum(now - times, 1e-6)
    return float(np.log(np.sum(ages ** (-np.array(ds)))))


def _recall_at(times, now, offset: float = 0.0) -> float:
    from explainer.psychology.psyche import memory as Mem

    return float(Mem.pa_recall(pa_activation_capped(times, now) - offset))


def schedule(policy: str, reviews: int = 4, horizon: float = 28.0, test_day: float = 60.0, n_items: int = 60,
             seed: int = 0, estimate_noise: float = 0.3, base: float = 0.0) -> dict:
    """Study each of ``n_items`` once at day 0 and review it ``reviews`` more times before ``horizon``; test at
    ``test_day``.  Items differ in difficulty (an offset on activation).  Policies: "massed" (all reviews within the
    first session), "fixed" (equal gaps), "expanding" (gaps doubling), "model" (choose, among schedules whose gaps grow,
    stay equal or shrink and whose last review falls at a half, three quarters or all of the horizon, the one with
    the highest predicted recall at the test under the memory model).  Returns the mean recall at the test and the review times of the first item."""
    rng = np.random.default_rng(seed)
    diff = base + rng.normal(0, 0.25, n_items)
    est = diff + rng.normal(0, estimate_noise * 0.25, n_items)
    finals, first, best = [], None, None
    for i in range(n_items):
        if policy == "massed":
            times = [0.0] + [0.01 * (k + 1) for k in range(reviews)]
        elif policy == "fixed":
            g = horizon / reviews
            times = [0.0] + [g * (k + 1) for k in range(reviews)]
        elif policy == "expanding":
            unit = horizon / (2 ** reviews - 1)
            times = [0.0] + [unit * (2 ** (k + 1) - 1) for k in range(reviews)]
        elif policy == "model":
            if best is None:
                cands = []
                for q in (0.5, 0.75, 1.0, 1.5, 2.0):
                    for f in (0.5, 0.75, 1.0):
                        g = q ** np.arange(reviews)
                        cands.append([0.0] + list(f * horizon * np.cumsum(g) / g.sum()))
                best = max(cands, key=lambda c: _recall_at(c, test_day, float(np.mean(est))))
            times = list(best)
        else:
            raise ValueError(policy)
        if first is None:
            first = list(times)
        finals.append(_recall_at(times, test_day, diff[i]))
    return {"recall": float(np.mean(finals)), "first_item_times": np.array(first)}


def simple_view(decoding, comprehension):
    """Gough and Tunmer's simple view of reading: reading comprehension = decoding x language comprehension, each
    on 0 to 1."""
    return np.asarray(decoding, float) * np.asarray(comprehension, float)


# ----------------------------------------------------------------------------------------------------------------
# Part 55: behaviour change at scale
# ----------------------------------------------------------------------------------------------------------------
def default_inertia(opt_in: float, opt_out: float) -> dict:
    """A two-type reading of a default effect: a share q of people stay with whatever is set, the rest choose, and a
    share p of choosers want in.  Opt-in rate = (1 - q) p; opt-out rate = q + (1 - q) p.  Solved for q and p."""
    q = opt_out - opt_in
    p = opt_in / (1 - q)
    return {"inertia": float(q), "prefer": float(p)}


def megastudy(arms: int = 53, n_per_arm: int = 1200, base: float = 0.30, mean_effect: float = 0.01,
              sd_effect: float = 0.012, seed: int = 0) -> dict:
    """Many interventions tested in one population against one control (as in Milkman et al. 2021).  True effects
    (in proportion units) ~ N(mean, sd); each arm's estimate has binomial noise.  Returns true and estimated effects,
    the winner's estimate against its truth, and normal empirical-Bayes shrinkage of every estimate."""
    rng = np.random.default_rng(seed)
    true = rng.normal(mean_effect, sd_effect, arms)
    ctrl = rng.binomial(n_per_arm * 4, base) / (n_per_arm * 4)
    est = rng.binomial(n_per_arm, np.clip(base + true, 0, 1)) / n_per_arm - ctrl
    se2 = base * (1 - base) / n_per_arm + base * (1 - base) / (n_per_arm * 4)
    tau2 = max(est.var(ddof=1) - se2, 1e-8)
    w = tau2 / (tau2 + se2)
    shrunk = est.mean() + w * (est - est.mean())
    k = int(np.argmax(est))
    return {"true": true, "est": est, "shrunk": shrunk, "se": float(np.sqrt(se2)), "tau": float(np.sqrt(tau2)),
            "winner": k, "winner_est": float(est[k]), "winner_true": float(true[k]), "winner_shrunk": float(shrunk[k]),
            "weight": float(w)}


def publication_gap(n_trials: int = 4000, mean_effect: float = 0.014, sd_effect: float = 0.015, seed: int = 0,
                    academic_n=(60, 300), unit_n=(2000, 20000), base: float = 0.3) -> dict:
    """Two literatures from one distribution of true nudge effects (percentage-point changes).  Academic trials are
    small and published only if significant (plus 10% of the rest); nudge-unit trials are large and all reported.
    Returns the average reported effect in each (DellaVigna and Linos's comparison)."""
    rng = np.random.default_rng(seed)
    true = rng.normal(mean_effect, sd_effect, n_trials)
    out = {}
    for name, (lo, hi), filt in (("academic", academic_n, True), ("units", unit_n, False)):
        n = rng.integers(lo, hi, n_trials)
        se = np.sqrt(2 * base * (1 - base) / n)
        est = true + rng.normal(0, se)
        keep = (est / se > 1.96) | (rng.random(n_trials) < 0.1) if filt else np.ones(n_trials, bool)
        out[name] = {"mean_reported": float(est[keep].mean()), "share_reported": float(keep.mean()),
                     "mean_true_reported": float(true[keep].mean())}
    out["truth"] = float(true.mean())
    return out


# ----------------------------------------------------------------------------------------------------------------
# Part 56: psychology and law
# ----------------------------------------------------------------------------------------------------------------
def lineup_roc(procedure: str = "simultaneous", d_prime: float = 1.5, size: int = 6, criteria=None,
               n: int = 100_000, seed: int = 0) -> dict:
    """Line-ups by signal detection (Part 12; Wixted and Mickes 2014).  The culprit's face gives memory strength
    N(d', 1), every other face N(0, 1); in culprit-absent line-ups an innocent suspect stands in.  Simultaneous: the
    witness picks the strongest face if it passes the criterion.  Sequential: faces are shown one at a time in random
    order (the suspect's position random) and the witness picks the first that passes the criterion, and stops.
    For each criterion: the correct-identification rate (culprit picked, culprit-present) and the false-ID rate
    (innocent suspect picked, culprit-absent), the diagnosticity ratio, and the partial area under the ROC up to
    the largest common false-ID rate."""
    rng = np.random.default_rng(seed)
    cs = np.linspace(-0.5, 3.5, 33) if criteria is None else np.asarray(criteria, float)
    present = rng.standard_normal((n, size))
    present[:, 0] += d_prime
    absent = rng.standard_normal((n, size))
    if procedure == "sequential":
        order = np.argsort(rng.random((n, size)), axis=1)
        present = np.take_along_axis(present, order, 1)
        absent = np.take_along_axis(absent, order, 1)
        sus_p = np.argmax(order == 0, axis=1)
        sus_a = np.argmax(order == 0, axis=1)
    hit, fa = [], []
    for c in cs:
        if procedure == "simultaneous":
            hp = np.mean((present.argmax(1) == 0) & (present.max(1) > c))
            fp = np.mean((absent.argmax(1) == 0) & (absent.max(1) > c))
        else:
            first_p = np.where((present > c).any(1), (present > c).argmax(1), -1)
            first_a = np.where((absent > c).any(1), (absent > c).argmax(1), -1)
            hp = np.mean(first_p == sus_p)
            fp = np.mean(first_a == sus_a)
        hit.append(hp)
        fa.append(fp)
    hit, fa = np.array(hit), np.array(fa)
    return {"criteria": cs, "hit": hit, "fa": fa, "dr": hit / np.maximum(fa, 1e-9)}


def partial_auc(fa, hit, upto: float) -> float:
    """Area under an ROC (false-ID rate on x) from 0 to ``upto``, by the trapezoid rule."""
    o = np.argsort(fa)
    x, y = np.concatenate([[0.0], np.asarray(fa)[o]]), np.concatenate([[0.0], np.asarray(hit)[o]])
    keep = x <= upto
    xs, ys = x[keep], y[keep]
    yu = np.interp(upto, x, y)
    xs, ys = np.append(xs, upto), np.append(ys, yu)
    return float(np.sum(np.diff(xs) * (ys[1:] + ys[:-1]) / 2))


def confidence_feedback(d_prime: float = 1.5, size: int = 6, criteria=(0.5, 1.0, 1.5, 2.0, 2.5), boost: float = 0.8,
                        n: int = 200_000, seed: int = 0) -> dict:
    """Confidence-accuracy at the initial identification, and after confirming feedback ("good, you picked the
    suspect") that raises every suspect-picker's confidence by ``boost`` criteria steps (Wells and Bradfield 1998,
    as a model).  Returns the share of suspect identifications that are correct at each confidence level, before
    and after."""
    rng = np.random.default_rng(seed)
    c = np.asarray(criteria, float)
    present = rng.standard_normal((n, size))
    present[:, 0] += d_prime
    absent = rng.standard_normal((n, size))
    out = {"levels": np.arange(1, len(c) + 1)}
    for tag, shift in (("initial", 0.0), ("after", boost)):
        res = []
        for L in (present, absent):
            pick = L.argmax(1) == 0
            conf = np.searchsorted(c, L.max(1), side="right")
            conf = np.where(pick & (conf > 0), np.minimum(conf + int(round(shift)), len(c)), conf)
            res.append(np.array([np.sum(pick & (conf == k)) for k in out["levels"]]))
        tp, ti = res
        out[tag] = tp / np.maximum(tp + ti, 1)
        out[tag + "_n"] = tp + ti
    return out


def risk_groups(base_rates=(0.3, 0.5), d: float = 1.2, threshold: float = 0.5, n: int = 400_000, seed: int = 0) -> dict:
    """One risk score, calibrated in both groups (the same score means the same probability of reoffending), used
    at one threshold in two groups with different base rates.  Returns each group's false-positive and
    false-negative rates and positive predictive value: Chouldechova's and Kleinberg's impossibility result in
    numbers (with unequal base rates, calibration and equal error rates cannot all hold)."""
    rng = np.random.default_rng(seed)
    out = {}
    for b in base_rates:
        y = rng.random(n) < b
        x = rng.normal(0, 1, n) + d * y
        logit_b = np.log(b / (1 - b))
        # the calibrated probability given x within this group
        lp = logit_b + d * x - d * d / 2
        prob = 1 / (1 + np.exp(-lp))
        flag = prob >= threshold
        out[b] = {"fpr": float(np.mean(flag[~y])), "fnr": float(np.mean(~flag[y])), "ppv": float(np.mean(y[flag])),
                  "flagged": float(np.mean(flag))}
    return out


def score_interval(score: float, reliability: float = 0.95, sd: float = 15.0, level: float = 0.95) -> dict:
    """The standard error of measurement SD sqrt(1 - r) and an interval around an observed score (Part 3)."""
    sem = sd * np.sqrt(1 - reliability)
    z = stats.norm.ppf(0.5 + level / 2)
    return {"sem": float(sem), "lo": float(score - z * sem), "hi": float(score + z * sem)}


# ----------------------------------------------------------------------------------------------------------------
# Part 57: health and care
# ----------------------------------------------------------------------------------------------------------------
def placebo_pain(stimulus: float = 6.0, expected=(6.0, 4.0), sensory_sd: float = 1.0, prior_sd: float = 1.5) -> dict:
    """Pain as inference (Part 14): the reported intensity is the posterior mean combining a noisy sensory signal
    (the stimulus, with SD ``sensory_sd``) and an expectation (a prior centred on the expected intensity, SD
    ``prior_sd``).  A placebo lowers the expectation.  Returns reported pain with and without the placebo, and the
    weight on expectation."""
    w = (1 / prior_sd ** 2) / (1 / prior_sd ** 2 + 1 / sensory_sd ** 2)
    rep = [float(w * e + (1 - w) * stimulus) for e in expected]
    return {"no_placebo": rep[0], "placebo": rep[1], "effect": rep[0] - rep[1], "weight": float(w)}


def placebo_by_noise(sensory_sds=(0.5, 1.0, 1.5, 2.0, 3.0), **kw) -> dict:
    """The placebo effect grows as the bodily signal becomes less precise: the prior carries more weight."""
    sds = np.asarray(sensory_sds, float)
    eff = np.array([placebo_pain(sensory_sd=float(s), **kw)["effect"] for s in sds])
    return {"sensory_sd": sds, "effect": eff}


def stepped_care(policy: str = "stepped", weeks: int = 104, referrals: int = 100, low_slots: int = 70,
                 high_slots: int = 30, low_course: int = 6, high_course: int = 12, p_low: float = 0.45,
                 p_high: float = 0.55, severe_share: float = 0.3, p_natural: float = 0.01, seed: int = 0) -> dict:
    """A service over ``weeks``: ``referrals`` people a week; ``severe_share`` are severe.  Low-intensity courses
    (guided self-help) take ``low_course`` weeks and start up to ``low_slots`` people a week; high-intensity
    (therapy) ``high_course`` weeks and ``high_slots`` a week.  Recovery after a course with probability p_low or
    p_high (halved for severe cases at low intensity); waiting people recover naturally at ``p_natural`` a week.
    Policies: "high_only" (everyone waits for therapy), "matched" (severe to therapy, others to self-help),
    "stepped" (everyone starts low; non-responders step up).  Returns the share recovered by the end and within 26
    weeks of referral, the mean wait to a first treatment, and the share never started, over the people referred in
    the first year."""
    rng = np.random.default_rng(seed)
    q_low, q_high = [], []  # waiting lists: (id)
    people = []
    in_low, in_high = [], []  # (finish week, id)
    for t in range(weeks):
        for _ in range(referrals):
            pid = len(people)
            sev = rng.random() < severe_share
            people.append({"t0": t, "sev": sev, "start": None, "rec": None, "stepped": False})
            if policy == "high_only" or (policy == "matched" and sev):
                q_high.append(pid)
            else:
                q_low.append(pid)
        for q in (q_low, q_high):  # natural recovery while waiting
            keep = []
            for pid in q:
                if rng.random() < p_natural:
                    people[pid]["rec"] = t
                else:
                    keep.append(pid)
            q[:] = keep
        done_low = [x for x in in_low if x[0] == t]
        in_low = [x for x in in_low if x[0] != t]
        for _, pid in done_low:
            p = p_low * (0.5 if people[pid]["sev"] else 1.0)
            if rng.random() < p:
                people[pid]["rec"] = t
            elif policy == "stepped":
                people[pid]["stepped"] = True
                q_high.append(pid)
        done_high = [x for x in in_high if x[0] == t]
        in_high = [x for x in in_high if x[0] != t]
        for _, pid in done_high:
            if rng.random() < p_high:
                people[pid]["rec"] = t
        for _ in range(low_slots):
            if not q_low:
                break
            pid = q_low.pop(0)
            if people[pid]["start"] is None:
                people[pid]["start"] = t
            in_low.append((t + low_course, pid))
        for _ in range(high_slots):
            if not q_high:
                break
            pid = q_high.pop(0)
            if people[pid]["start"] is None:
                people[pid]["start"] = t
            in_high.append((t + high_course, pid))
    first = [p for p in people if p["t0"] < 52]
    rec = np.mean([p["rec"] is not None for p in first])
    rec26 = np.mean([p["rec"] is not None and p["rec"] - p["t0"] <= 26 for p in first])
    waits = [(p["start"] if p["start"] is not None else weeks) - p["t0"] for p in first]
    waiting = np.mean([p["start"] is None and p["rec"] is None for p in first])
    return {"recovered": float(rec), "recovered_26": float(rec26), "mean_wait": float(np.mean(waits)), "never_started": float(waiting),
            "stepped_up": float(np.mean([p["stepped"] for p in first]))}

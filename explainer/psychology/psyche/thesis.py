"""The series' dissertation (Part 62): a registered report run end to end, and the accounts closed.

The question joins two earlier parts.  Part 24 fitted mental-rotation slopes to Ganis and Kievit's (2015) open data:
the effect is robust (it rose for 53 of 54 people).  Part 59's reliability paradox says a robust group effect is
often a poor measure of individuals.  Is a person's rotation slope a reliable measure of that person?

``PLAN`` is the Stage 1 registration: written, and its SHA-256 recorded, before the analysis below was run on the
data.  ``power`` is the design check on simulated people (the Pool); ``analyse`` is the registered analysis;
``verdict`` applies the registered decision rule.  The exploratory analyses are separate and labelled as such.
numpy only.
"""

from __future__ import annotations

import hashlib
import json

import numpy as np

PLAN = {
    "title": "Is a robust effect a reliable measure? Mental rotation slopes, split in half",
    "theory": "Part 59's reliability paradox: an effect almost everyone shows has little between-person variance "
              "left to measure, and a slope is a difference-like score that doubles trial noise.",
    "H1": "The Spearman-Brown corrected split-half reliability of the rotation slope (ms per degree) is below 0.70.",
    "H2": "The person's mean response time (on the same trials) is more reliable than the slope.",
    "alternative": "Rotation speed is a stable spatial ability (Part 32): slope reliability is 0.70 or more.",
    "data": "Ganis and Kievit (2015), 54 people, 96 trials each, as read by explainer.psychology.opendata.",
    "trials": "'same' trials answered correctly, with a response time from 200 to 10,000 ms.",
    "people": "everyone with at least 4 usable trials at each angle in each half; no other exclusions.",
    "split": "odd against even trial numbers (the published trial index).",
    "slope": "least-squares slope of response time on angle (0, 50, 100, 150 degrees), per person and half.",
    "reliability": "Pearson correlation of the halves across people, then Spearman-Brown: 2r / (1 + r).",
    "interval": "95% percentile bootstrap over people, 4,000 resamples, seed 62.",
    "decision": "H1 supported if the interval's upper end is below 0.70; refuted if its lower end is above 0.70; "
                "otherwise inconclusive.  H2 supported if the paired bootstrap difference (mean minus slope "
                "reliability) has a lower end above 0.",
    "exploratory": "anything else, labelled as exploratory.",
}


# The one deviation, made after the counts of usable trials were seen and before any reliability was computed: the
# registered minimum of 4 usable trials per angle in each half excluded all 54 people (the data have fewer 'same'
# trials per cell than the plan assumed), so the minimum was lowered to 2.  Reported as a deviation in the film and
# the README.
DEVIATION = {"rule": "people", "registered_min_per_cell": 4, "used_min_per_cell": 2,
             "why": "the registered minimum excluded every participant; decided on trial counts alone"}


def plan_hash() -> str:
    """SHA-256 of the registered plan, as canonical JSON."""
    return hashlib.sha256(json.dumps(PLAN, sort_keys=True).encode("utf-8")).hexdigest()


# ----------------------------------------------------------------------------------------------------------------
# Reliability of a slope
# ----------------------------------------------------------------------------------------------------------------
def spearman_brown(r: float, k: float = 2.0) -> float:
    return float(k * r / (1 + (k - 1) * r))


def _slope_and_mean(angle, rt):
    a = np.asarray(angle, float)
    y = np.asarray(rt, float)
    X = np.column_stack([np.ones(len(a)), a])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return float(b[1]), float(y.mean())


def person_halves(data: dict, min_per_cell: int = 4) -> dict:
    """The registered data rules applied: usable trials, the odd/even split, each person's slope and mean in each
    half.  Returns arrays over the people kept, and the count excluded."""
    sid = np.asarray(data["subject"])
    keep = (np.asarray(data["same"], bool) & np.asarray(data["correct"], bool) & np.isfinite(data["rt"])
            & (np.asarray(data["rt"]) >= 200) & (np.asarray(data["rt"]) <= 10000))
    odd = (np.asarray(data["trial"]) % 2) == 1
    angles = np.unique(np.asarray(data["angle"]))
    out = {"subject": [], "slope_odd": [], "slope_even": [], "mean_odd": [], "mean_even": []}
    excluded = 0
    for s in np.unique(sid):
        rows = {}
        ok = True
        for half, m in (("odd", odd), ("even", ~odd)):
            sel = (sid == s) & keep & m
            counts = [np.sum(sel & (np.asarray(data["angle"]) == a)) for a in angles]
            if min(counts) < min_per_cell:
                ok = False
                break
            rows[half] = _slope_and_mean(np.asarray(data["angle"])[sel], np.asarray(data["rt"])[sel])
        if not ok:
            excluded += 1
            continue
        out["subject"].append(int(s))
        out["slope_odd"].append(rows["odd"][0])
        out["slope_even"].append(rows["even"][0])
        out["mean_odd"].append(rows["odd"][1])
        out["mean_even"].append(rows["even"][1])
    res = {k: np.array(v) for k, v in out.items()}
    res["excluded"] = excluded
    return res


def reliability(x_odd, x_even) -> float:
    return spearman_brown(float(np.corrcoef(x_odd, x_even)[0, 1]))


def analyse(halves: dict, boots: int = 4000, seed: int = 62) -> dict:
    """The registered analysis: corrected split-half reliabilities of the slope and of the mean, with percentile
    bootstrap intervals over people, and the paired difference."""
    rng = np.random.default_rng(seed)
    so, se = halves["slope_odd"], halves["slope_even"]
    mo, me = halves["mean_odd"], halves["mean_even"]
    n = len(so)
    rs, rm = reliability(so, se), reliability(mo, me)
    bs, bm = np.empty(boots), np.empty(boots)
    for b in range(boots):
        i = rng.integers(0, n, n)
        bs[b] = reliability(so[i], se[i])
        bm[b] = reliability(mo[i], me[i])
    diff = bm - bs
    return {"n": n, "slope_rel": rs, "slope_ci": [float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))],
            "mean_rel": rm, "mean_ci": [float(np.quantile(bm, 0.025)), float(np.quantile(bm, 0.975))],
            "diff_ci": [float(np.quantile(diff, 0.025)), float(np.quantile(diff, 0.975))],
            "median_slope": float(np.median((so + se) / 2))}


def verdict(res: dict, threshold: float = 0.70) -> dict:
    lo, hi = res["slope_ci"]
    h1 = "supported" if hi < threshold else ("refuted" if lo > threshold else "inconclusive")
    h2 = "supported" if res["diff_ci"][0] > 0 else "not supported"
    return {"H1": h1, "H2": h2}


# ----------------------------------------------------------------------------------------------------------------
# The design check on simulated people
# ----------------------------------------------------------------------------------------------------------------
def simulate_halves(n_people: int = 54, true_rel: float = 0.5, mean_slope: float = 10.0, slope_sd: float = 4.0,
                    trials_per_angle: int = 6, seed: int = 0) -> dict:
    """Simulated people whose true slopes vary with SD ``slope_sd``; trial noise is set so that the full-test
    (both halves) reliability is ``true_rel``.  Returns odd and even halves in ``person_halves``' format."""
    rng = np.random.default_rng(seed)
    angles = np.array([0, 50, 100, 150], float)
    half_rel = true_rel / (2 - true_rel)  # Spearman-Brown in reverse
    err_var_slope = slope_sd ** 2 * (1 - half_rel) / half_rel
    sxx = trials_per_angle * np.sum((angles - angles.mean()) ** 2)
    sigma = np.sqrt(err_var_slope * sxx)
    true = rng.normal(mean_slope, slope_sd, n_people)
    base = rng.normal(1600, 300, n_people)
    out = {"slope_odd": [], "slope_even": [], "mean_odd": [], "mean_even": []}
    a = np.repeat(angles, trials_per_angle)
    for p in range(n_people):
        for half in ("odd", "even"):
            y = base[p] + true[p] * a + rng.normal(0, sigma, len(a))
            s, m = _slope_and_mean(a, y)
            out["slope_" + half].append(s)
            out["mean_" + half].append(m)
    return {k: np.array(v) for k, v in out.items()}


def power(true_rels=(0.4, 0.55, 0.7, 0.85), n_people: int = 54, reps: int = 300, seed: int = 0) -> dict:
    """How often the registered rule, applied to 54 simulated people, says supported, inconclusive or refuted,
    for each true reliability.  Uses a smaller bootstrap (500) for speed."""
    rng = np.random.default_rng(seed)
    table = []
    for tr in true_rels:
        counts = {"supported": 0, "inconclusive": 0, "refuted": 0}
        for _ in range(reps):
            h = simulate_halves(n_people=n_people, true_rel=tr, seed=int(rng.integers(1 << 30)))
            v = verdict(analyse(h, boots=500, seed=int(rng.integers(1 << 30))))
            counts[v["H1"]] += 1
        table.append([counts["supported"] / reps, counts["inconclusive"] / reps, counts["refuted"] / reps])
    return {"true_rel": np.array(true_rels), "table": np.array(table)}


# ----------------------------------------------------------------------------------------------------------------
# Psyche's scorecard on the Battery
# ----------------------------------------------------------------------------------------------------------------
def _slope(x, y):
    return float(np.polyfit(np.asarray(x, float), np.asarray(y, float), 1)[0])


def scorecard(seed: int = 62) -> list:
    """Every Battery task Psyche sits through the shared interface (``battery.run``), with Psyche's default
    parameters, checked against the task's published signature.  Returns rows of (task number, name, the signature,
    Psyche's number, pass).  Tasks modelled only inside their own parts are listed as such."""
    from explainer.psychology import battery
    from explainer.psychology.psyche import chronometry as ch
    from explainer.psychology.psyche import memory as M
    from explainer.psychology.psyche import psychophysics as P
    from explainer.psychology.psyche import wm

    rows = []
    m = ch.donders_models()
    a = battery.run("rt_simple", m["a"], 2000, seed=seed)
    b = battery.run("rt_choice", m["b"], 2000, seed=seed + 1)
    rt = b.rts()
    skew = float(np.mean(((rt - rt.mean()) / rt.std()) ** 3))
    rows.append((1, "reaction time", "right-skewed; choice slower than simple",
                 f"skew {skew:.2f}; {b.mean_rt() - a.mean_rt():.0f} ms slower", skew > 0 and b.mean_rt() > a.mean_rt()))

    t = battery.run("threshold", P.Observer(), 1600, seed=seed + 2)
    acc = [t.correct[t.extra["delta"] == d].mean() for d in battery.THRESHOLD_DELTAS]
    rows.append((2, "two-alternative threshold", "a rising psychometric function",
                 f"{100 * acc[0]:.0f}% at the smallest step, {100 * acc[-1]:.0f}% at the largest",
                 acc[-1] > 0.9 and acc[0] < 0.75))

    s = battery.run("stroop", {}, 1500, seed=seed + 3)
    inter = s.mean_rt("incongruent") - s.mean_rt("neutral")
    facil = s.mean_rt("neutral") - s.mean_rt("congruent")
    rows.append((3, "Stroop", "interference larger than facilitation",
                 f"{inter:.0f} ms against {facil:.0f} ms", inter > facil > -5))

    v = battery.run("search", {}, 3200, seed=seed + 4)
    ss = v.extra["set_size"]

    def sl(kind, present):
        mm = v.where(kind) & (v.extra["present"] == present) & v.correct
        sizes = np.unique(ss[mm])
        return _slope(sizes, [v.rt[mm & (ss == k)].mean() for k in sizes])
    fp, cp, ca = sl("feature", True), sl("conjunction", True), sl("conjunction", False)
    rows.append((4, "visual search", "feature flat; conjunction absent about twice present",
                 f"{fp:.1f}, {cp:.1f} and {ca:.1f} ms per item", fp < 5 and 1.4 < ca / cp < 2.8))

    c = battery.run("change", {}, 2000, seed=seed + 5)
    k8 = c.extra["set_size"] == 8
    H = c.correct[k8 & c.extra["changed"]].mean()
    FA = 1 - c.correct[k8 & ~c.extra["changed"]].mean()
    K = wm.k_cowan(H, FA, 8)
    rows.append((5, "change detection", "capacity three to four items", f"K = {K:.1f}", 2.5 <= K <= 4.5))

    r = battery.run("recall", {}, 400, seed=seed + 6)
    summ = M.recall_summary(r.extra["recalls"], 16, max_lag=1)
    spc, crp = np.asarray(summ["spc"]), np.asarray(summ["crp"])
    rows.append((6, "free recall", "primacy, recency and forward contiguity",
                 f"first {spc[0]:.2f}, middle {spc[7]:.2f}, last {spc[-1]:.2f}; lag +1 {crp[2]:.2f} against -1 "
                 f"{crp[0]:.2f}", spc[0] > spc[7] and spc[-1] > spc[7] and crp[2] > crp[0]))

    g = battery.run("gambles", {}, 8000, seed=seed + 7)

    def ce(cond, p):
        """Certainty equivalent: the sure amount (in absolute value) at which the gamble is chosen half the time (for
        losses, the sure loss accepted half the time: above the expected loss is risk aversion),
        by linear interpolation of the choice share across the sure amounts offered."""
        mm = (g.condition == cond) & (g.extra["p"] == p)
        sures = np.unique(np.abs(g.extra["sure"][mm]))
        share = np.array([g.correct[mm & (np.abs(g.extra["sure"]) == x)].mean() for x in sures])
        if cond == "loss":
            share = 1 - share  # for losses, choosing the sure loss is the analogue of taking the gamble
        for i in range(len(sures) - 1):
            if (share[i] - 0.5) * (share[i + 1] - 0.5) <= 0 and share[i] != share[i + 1]:
                return float(sures[i] + (0.5 - share[i]) * (sures[i + 1] - sures[i]) / (share[i + 1] - share[i]))
        return float(sures[0] if share[0] < 0.5 else sures[-1])
    lo, hi = min(np.unique(g.extra["p"][g.condition == "gain"])), max(np.unique(g.extra["p"][g.condition == "gain"]))
    cg_lo, cg_hi, cl_lo, cl_hi = ce("gain", lo), ce("gain", hi), ce("loss", lo), ce("loss", hi)
    ev_lo, ev_hi = 100 * lo, 100 * hi
    rows.append((9, "risky choice", "the fourfold pattern (certainty equivalents against expected values)",
                 f"gains: {cg_lo:.0f} for EV {ev_lo:.0f}, {cg_hi:.0f} for EV {ev_hi:.0f}; losses: {cl_lo:.0f} and "
                 f"{cl_hi:.0f}", cg_lo > ev_lo and cg_hi < ev_hi and cl_lo > ev_lo and cl_hi < ev_hi))

    for num, name, part in ((7, "random-dot motion", 25), (8, "bandits and the two-step task", 17),
                            (10, "mental rotation", 24), (11, "lexical decision and reading", 23),
                            (12, "matrix reasoning", 32), ("Q", "Big Five inventory", 33)):
        rows.append((num, name, f"modelled in Part {part} with its own parameters", "not run on one Psyche", None))
    return rows


# ----------------------------------------------------------------------------------------------------------------
# The Ledger, complete
# ----------------------------------------------------------------------------------------------------------------
ACTS = (("I", "Asking a Mind a Question", 1, 4), ("II", "The Wet Machine", 5, 10), ("III", "Sensing", 11, 15),
        ("IV", "Learning", 16, 17), ("V", "Thinking", 18, 27), ("VI", "Feeling and Wanting", 28, 29),
        ("VII", "Growing", 30, 31), ("VIII", "Differing", 32, 33), ("IX", "Other People", 34, 38),
        ("X", "When Minds Suffer", 39, 43), ("XI", "The Graduate Toolkit", 44, 50),
        ("XII", "Psychology at Work", 51, 57), ("XIII", "The Frontier", 58, 62))
GROUPS = {"held": ("replicated", "replicated, smaller", "story and record"), "contested": ("contested",),
          "failed": ("failed", "retracted"), "untested": ("not directly tested",)}


def ledger_by_act(rows) -> dict:
    """Counts of the Ledger's rows by act and by group of status (held, contested, failed, untested)."""
    table = np.zeros((len(ACTS), len(GROUPS)), int)
    for f in rows:
        for i, (_, _, lo, hi) in enumerate(ACTS):
            if lo <= f.part <= hi:
                for j, statuses in enumerate(GROUPS.values()):
                    if f.status in statuses:
                        table[i, j] += 1
    return {"acts": [a[0] for a in ACTS], "names": [a[1] for a in ACTS], "groups": list(GROUPS), "table": table}


DECADES = ((0, 1950, "before 1950"), (1950, 1970, "1950s-60s"), (1970, 1990, "1970s-80s"), (1990, 2000, "1990s"),
           (2000, 2010, "2000s"), (2010, 2100, "since 2010"))


def ledger_by_decade(rows) -> dict:
    """Counts of the Ledger's rows by when the original study appeared, and by group of status.  Older findings
    have had longer to be tested (and, if they failed, to be forgotten before a course would teach them), so the
    gradient mixes survivorship with any change in how research was done."""
    table = np.zeros((len(DECADES), len(GROUPS)), int)
    for f in rows:
        for i, (lo, hi, _) in enumerate(DECADES):
            if lo <= f.original.year < hi:
                for j, statuses in enumerate(GROUPS.values()):
                    if f.status in statuses:
                        table[i, j] += 1
    return {"labels": [d[2] for d in DECADES], "groups": list(GROUPS), "table": table}


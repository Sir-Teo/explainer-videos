"""Precompute every number in Part 2 of *Psychology, Built* ("The Experiment").

    python -m videos.psychology.psych2.compute            # everything missing (well under a minute)
    python -m videos.psychology.psych2.compute --force threats

Results are cached in ``.cache/psych2/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Historical numbers
come from the Archive (``explainer.psychology.archive``, each with its source), the model of Clever Hans from
Psyche (``explainer.psychology.psyche.cueing``), the designs from the laboratory (``explainer.psychology.lab``)
run on the Pool (seed 1850); every random choice here is seeded.

Items:
    hans         Pfungst's conditions (who knew the answer, who could be seen, how far away) with their counts and
                 binomial intervals; the four-parameter cue-reading model fitted to them; its detection curve
                 over distance; two simulated sittings, tap by tap
    one_group    a training that does nothing, studied with one group before and after, and then with a
                 randomized control group measured the same way
    threats      the six unsound designs of Campbell and Stanley on the Pool with the true effect zero: the
                 effect each reports in one study and over 200 studies, beside the randomized experiment
    balance      what shuffling a deck does: the standardized difference between the groups in age and in
                 eagerness over 5,000 shuffles, against the same difference when people choose for themselves;
                 one randomized study of a real effect with its randomization test
    within       the correlation of a person's two sessions; the spread of the estimate between and within
                 people; people needed for 80% power either way, checked by simulation; the cross-over with
                 and without counterbalancing; a Williams square for four conditions
    expectancy   Rosenthal and Fode's rats day by day; Raudenbush's eighteen experiments by weeks of contact;
                 the demand effects measured by de Quidt, Haushofer and Roth
    factorial    a treatment that takes a tenth off everyone's reaction time, in slow and in quick people: an
                 interaction in milliseconds that vanishes on a logarithmic scale
    be_random    a generator that switches keys too often, as people do, against a fair coin: alternation
                 rates, longest runs, and how often a simple predictor guesses the next press
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.psychology import archive, lab
from explainer.psychology.pool import Pool
from explainer.psychology.psyche import cueing

CACHE = Cache("psych2")
load = CACHE.load

N = 200  # people in each study of the film, unless the chapter says otherwise
EFFECT = -8.0  # ms: the real effect planted when the film needs one (a treatment that speeds reactions by 8 ms)


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def wilson(k: float, n: int, z: float = 1.96) -> tuple:
    """Wilson's interval for a binomial proportion."""
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(centre - half, 0.0), min(centre + half, 1.0)


# ---------------------------------------------------------------------------
def compute_hans() -> dict:
    d = archive.PFUNGST_1907.data
    reader = cueing.fit_hans()
    rows = []
    for name, knows, sees, dist, n, share in cueing.PFUNGST_CONDITIONS:
        lo, hi = wilson(share * n, n)
        rows.append({"name": name, "knows": knows, "sees": sees, "distance": dist, "n": n, "share": share,
                     "lo": lo, "hi": hi, "model": reader.p_correct(knows, sees, dist)})
    # the two contrasts the film opens with, straight from the book
    num, blind = d["numerals"], d["blinders"]
    assert rows[0]["share"] == num["with_knowledge"]["correct"] and rows[1]["n"] == num["without_knowledge"]["n"]
    grid = np.linspace(0.25, 6.0, 231)
    targets = [3, 7, 5, 8, 4, 10, 6, 9, 2, 12]
    knows = cueing.simulate_session(reader, targets, knows=True, seed=4)
    blindfold = cueing.simulate_session(reader, targets, knows=False, seed=4)
    far = cueing.simulate_session(reader, targets * 4, knows=True, distance=4.25, seed=5)
    return {
        "rows": rows, "numerals": num, "blinders": blind, "placards": d["placards"],
        "distance": d["distance_m"], "laboratory": d["laboratory"],
        "commission_members": d["commission_members"],
        "reader": {"d0": reader.d0, "sigma": reader.sigma, "lapse": reader.lapse, "guess": reader.guess},
        "grid": grid, "p_detect": reader.p_detect(grid),
        "p_correct_grid": reader.p_detect(grid) + (1 - reader.p_detect(grid)) * reader.guess,
        "targets": targets, "tapped_knows": knows["tapped"], "tapped_blind": blindfold["tapped"],
        "share_knows": knows["share"], "share_blind": blindfold["share"], "share_far": far["share"],
        "max_abs_miss": max(abs(r["model"] - r["share"]) for r in rows),
    }


def compute_one_group() -> dict:
    """A training that does nothing (true effect 0).  First the study as it is usually run: one group, a test
    before and a test after.  Then the same people's design done properly: a randomized control group that takes
    the same two tests."""
    pool = Pool()

    def study(k):
        ids = pool.sample(N, seed=1000 + k)
        pre = pool.session_rt(ids, 0, 20, seed=1000 + k)
        post = pool.session_rt(ids, 1, 20, seed=1000 + k)
        g = lab.randomize(N, 2, rng(2000 + k))
        return ids, pre, post, g, lab.difference(post - pre, g)

    # the film shows one study: the median one of 101, so that it is typical and not picked for its result
    effects = [study(k)[4].effect for k in range(101)]
    k = int(np.argsort(effects)[50])
    ids, pre, post, g, both = study(k)
    alone = lab.paired(post, pre)
    means = {"treated": {"pre": float(pre[g == 1].mean()), "post": float(post[g == 1].mean())},
             "control": {"pre": float(pre[g == 0].mean()), "post": float(post[g == 0].mean())}}
    assert abs(alone.effect + pool.practice_gain(ids, 1).mean()) < 2.0  # what the single group reports is practice
    assert both.ci()[0] < 0 < both.ci()[1]
    return {"n": N, "pre_mean": float(pre.mean()), "post_mean": float(post.mean()), "alone": alone.as_dict(),
            "means": means, "with_control": both.as_dict(), "true_effect": 0.0,
            "practice": float(pool.practice_gain(ids, 1).mean()),
            "pre_sample": pre[:60], "post_sample": post[:60], "study_index": k,
            "control_effects_sd": float(np.std(effects))}


def compute_threats() -> dict:
    pool = Pool()
    L = lab.Lab(pool)
    quick = lab.Lab(pool, n_trials=5)  # a five-trial screening test: noisier, so it regresses more
    out = {}
    designs = [("selection", L, {}), ("testing", L, {}), ("history", L, {}), ("maturation", L, {}),
               ("regression", quick, {}), ("attrition", L, {})]
    for name, where, kw in designs:
        one = where.threat(name, n=N, **kw)
        many = where.replicate(name, studies=200, n=N, **kw)
        assert one.ci()[1] < 0, name
        out[name] = dict(one.as_dict(), mean=float(many.mean()), sd=float(many.std()),
                         share_significant=float(np.mean([where.threat(name, n=N, study=s, **kw).p < 0.05
                                                          for s in range(100)])))
    sound = L.randomized(n=N)
    many = L.replicate("randomized", studies=500, n=N)
    edges = np.linspace(-12, 12, 25)
    out["randomized"] = dict(sound.as_dict(), mean=float(many.mean()), sd=float(many.std()),
                             share_significant=float(np.mean([L.randomized(n=N, study=s).p < 0.05
                                                              for s in range(500)])))
    assert abs(many.mean()) < 0.5 and 0.02 < out["randomized"]["share_significant"] < 0.09
    return {"n": N, "designs": out, "order": list(lab.THREATS), "edges": edges,
            "hist_randomized": np.histogram(many, edges)[0], "keyboard_shock": -6.0,
            "children_ms_per_year": -22.0, "dropout": 0.35, "screened": 2000, "screen_trials": 5}


def compute_balance() -> dict:
    pool = Pool()
    L = lab.Lab(pool)
    ids = pool.sample(N, seed=201)
    age, keen, speed = pool.age[ids].astype(float), pool.keen[ids], pool.simple_mean(ids)
    g = rng(202)
    shuffles = [lab.randomize(N, 2, g) for _ in range(5000)]
    z_age = np.array([lab.balance(age, s) for s in shuffles])
    z_keen = np.array([lab.balance(keen, s) for s in shuffles])
    z_speed = np.array([lab.balance(speed, s) for s in shuffles])
    # people choosing for themselves: the keener half takes the treatment
    chosen = (keen > np.median(keen)).astype(int)
    self_sel = {"age": lab.balance(age, chosen), "keen": lab.balance(keen, chosen),
                "speed": lab.balance(speed, chosen)}
    # an experimenter assigning "at random" by eye, who tends to put the alert-looking (quick) people in the
    # treatment: a mild preference is enough
    by_eye = (speed + 75.0 * g.standard_normal(N) < np.median(speed)).astype(int)
    eye = {"age": lab.balance(age, by_eye), "speed": lab.balance(speed, by_eye)}
    edges = np.linspace(-0.6, 0.6, 41)
    theory_sd = math.sqrt(4 / N)
    assert abs(z_keen.std() - theory_sd) < 0.01 and abs(z_keen.mean()) < 0.01
    # one randomized study of a real effect, analysed by reshuffling the deck
    ests = [L.randomized(n=N, effect=EFFECT, study=k).effect for k in range(101)]
    study = int(np.argsort(ests)[50])  # the median study of 101: typical, not picked for its result
    ids2 = pool.sample(N, seed=L.seed * 7919 + study)
    assign = lab.randomize(N, 2, L._rng(1, study))
    y = pool.session_rt(ids2, 0, 20, seed=L.seed * 1000 + 100 + study, shift=EFFECT * assign)
    est = lab.difference(y, assign)
    assert abs(est.effect - L.randomized(n=N, effect=EFFECT, study=study).effect) < 1e-9
    rt = lab.randomization_test(y, assign, 20_000, rng(203))
    null_edges = np.linspace(-14, 14, 41)
    cover = [lo <= EFFECT <= hi for lo, hi in (L.randomized(n=N, effect=EFFECT, study=s).ci() for s in range(400))]
    return {"n": N, "edges": edges, "hist_age": np.histogram(z_age, edges)[0],
            "hist_keen": np.histogram(z_keen, edges)[0], "hist_speed": np.histogram(z_speed, edges)[0],
            "sd_age": float(z_age.std()), "sd_keen": float(z_keen.std()), "theory_sd": theory_sd,
            "share_beyond_0p3": float(np.mean(np.abs(z_keen) > 0.3)),
            "self_selected": self_sel, "by_eye": eye, "shuffles": 5000,
            "study": dict(est.as_dict(), true=EFFECT, p_randomization=rt["p"]),
            "null_edges": null_edges, "null_hist": np.histogram(rt["null"], null_edges)[0],
            "coverage": float(np.mean(cover))}


def compute_within() -> dict:
    pool = Pool()
    L = lab.Lab(pool)
    rho = L.session_correlation()
    ids = pool.sample(5000, seed=301)
    sd = float(pool.session_rt(ids, 0, 20, seed=301).std())
    d = abs(EFFECT) / sd
    n_between, n_within = lab.n_two_group(d), lab.n_paired(d, rho)
    ns = np.arange(4, 401, 2)
    # checks by simulation, on the Pool
    sims = 400
    hit_between = np.mean([L.randomized(n=2 * n_between, effect=EFFECT, study=s).p < 0.05 for s in range(sims)])
    hit_within = np.mean([L.crossover(n=n_within, effect=EFFECT, study=s).p < 0.05 for s in range(sims)])
    # the normal approximation is optimistic for so few people (a t test on 14 degrees of freedom): find the
    # number that reaches 80% in simulation
    grid = list(range(n_within, 41, 2))
    sim_grid = [float(np.mean([L.crossover(n=n, effect=EFFECT, study=s).p < 0.05 for s in range(sims)]))
                for n in grid]
    n_within_sim = next(n for n, pw in zip(grid, sim_grid) if pw >= 0.8)
    spread_between = L.replicate("randomized", 300, n=40, effect=EFFECT)
    spread_within = L.replicate("crossover", 300, n=40, effect=EFFECT)
    spread_unbalanced = L.replicate("crossover", 300, n=40, effect=EFFECT, counterbalanced=False)
    edges = np.linspace(-40, 24, 33)
    w = lab.williams(4)
    counts = lab.position_counts(w)
    cyc = lab.position_counts(lab.latin_square(4))
    assert 0.7 < hit_between < 0.9 and 0.55 < hit_within < 0.9 and n_within_sim < n_between / 4
    assert abs(spread_within.mean() - EFFECT) < 1.0 and spread_unbalanced.mean() < EFFECT - 4
    return {"rho": rho, "sd": sd, "d": d, "effect": EFFECT, "n_between_per_group": n_between,
            "n_between_total": 2 * n_between, "n_within": n_within, "ns": ns,
            "power_between": np.array([lab.power_two_group(d, int(n) // 2) for n in ns]),
            "power_within": np.array([lab.power_paired(d, int(n), rho) for n in ns]),
            "sim_power_between": float(hit_between), "sim_power_within": float(hit_within),
            "n_within_sim": n_within_sim, "sim_grid_n": grid, "sim_grid_power": sim_grid,
            "edges": edges, "hist_between": np.histogram(spread_between, edges)[0],
            "hist_within": np.histogram(spread_within, edges)[0],
            "hist_unbalanced": np.histogram(spread_unbalanced, edges)[0],
            "mean_between": float(spread_between.mean()), "sd_between": float(spread_between.std()),
            "mean_within": float(spread_within.mean()), "sd_within": float(spread_within.std()),
            "mean_unbalanced": float(spread_unbalanced.mean()), "sd_unbalanced": float(spread_unbalanced.std()),
            "practice_first_retest": float(pool.practice_gain(ids, 1).mean()),
            "williams": w, "williams_follows": counts["follows"], "cyclic": lab.latin_square(4),
            "cyclic_follows": cyc["follows"], "orders_complete": math.factorial(4)}


def compute_expectancy() -> dict:
    rf, ra, dq = (archive.ROSENTHAL_FODE_1963.data, archive.RAUDENBUSH_1984.data, archive.DE_QUIDT_2018.data)
    bright, dull = np.array(rf["bright"]), np.array(rf["dull"])
    assert abs(bright.mean() - rf["mean_bright"]) < 0.01 and abs(dull.mean() - rf["mean_dull"]) < 0.01
    lit = archive.LIT_2011.data
    return {"days": np.arange(1, 6), "bright": bright, "dull": dull, "mean_bright": rf["mean_bright"],
            "mean_dull": rf["mean_dull"], "ratio": rf["mean_bright"] / rf["mean_dull"],
            "experimenters": rf["experimenters"], "rats": rf["experimenters"] * rf["rats_per_experimenter"],
            "runs_per_day": rf["trials_per_rat_per_day"], "t": rf["t"], "p_one_tailed": rf["p_one_tailed"],
            "raudenbush": {"labels": ["none", "one week", "more than two weeks"],
                           "effect": [ra["effect_no_prior_contact"], ra["effect_one_week"],
                                      ra["effect_more_than_two_weeks"]],
                           "k": [ra["n_no_prior_contact"], ra["n_one_week"], ra["n_more_than_two_weeks"]],
                           "experiments": ra["experiments"]},
            "demand": {"strong": list(dq["strong_demand_sd"]), "weak": list(dq["weak_demand_sd"]),
                       "weak_mean": dq["weak_demand_mean_sd"], "participants": dq["participants"],
                       "tasks": dq["tasks"], "experiments": dq["experiments"]},
            "dogs": {"teams": lit["teams"], "alerts": lit["incorrect_alerts"]}}


def compute_factorial() -> dict:
    """A treatment that takes a tenth off a reaction time.  Factor A: the person is quick or slow (a median split
    of the Pool's sample).  Factor B: treated or not.  In milliseconds the slow gain more, so the lines are not
    parallel; on a logarithmic scale the gain is the same for both, and they are."""
    pool = Pool()
    ids = pool.sample(4000, seed=401)
    base = pool.simple_mean(ids)
    slow = base > np.median(base)
    g = lab.randomize(len(ids), 2, rng(402))
    y = pool.session_rt(ids, 0, 20, seed=401, shift=-0.10 * base * g)
    ms = np.array([[y[(~slow) & (g == 0)].mean(), y[(~slow) & (g == 1)].mean()],
                   [y[slow & (g == 0)].mean(), y[slow & (g == 1)].mean()]])
    logs = np.array([[np.log(y[(~slow) & (g == 0)]).mean(), np.log(y[(~slow) & (g == 1)]).mean()],
                     [np.log(y[slow & (g == 0)]).mean(), np.log(y[slow & (g == 1)]).mean()]])
    # standard errors of the two interaction contrasts, by the delta of four independent cells
    def se(values_fn):
        cells = [values_fn(y[m]) for m in ((~slow) & (g == 0), (~slow) & (g == 1), slow & (g == 0), slow & (g == 1))]
        return math.sqrt(sum(c.var(ddof=1) / len(c) for c in cells))

    inter_ms, inter_log = lab.interaction_2x2(ms), lab.interaction_2x2(logs)
    se_ms, se_log = se(lambda v: v), se(np.log)
    assert inter_ms < -2 * se_ms and abs(inter_log) < 2.5 * se_log
    return {"n": len(ids), "ms": ms, "log": logs, "percent": 100 * (np.exp(logs[:, 1] - logs[:, 0]) - 1),
            "gain_ms": ms[:, 1] - ms[:, 0], "interaction_ms": inter_ms, "se_ms": se_ms,
            "interaction_log": inter_log, "se_log": se_log, "cut": 0.10}


def compute_be_random() -> dict:
    g = rng(501)
    n_press, reps = 100, 4000
    out, hists = {}, {}
    for name, p in (("person", 0.6), ("coin", 0.5)):
        seqs = [lab.human_like_sequence(n_press, p, g) for _ in range(reps)]
        alt = np.array([lab.alternation_rate(s) for s in seqs])
        runs = np.array([lab.longest_run(s) for s in seqs])
        acc = np.array([lab.predict_presses(s)["accuracy"] for s in seqs[:1500]])
        out[name] = {"alternation": float(alt.mean()), "alternation_sd": float(alt.std()),
                     "longest_run": float(runs.mean()), "accuracy": float(acc.mean()),
                     "accuracy_sd": float(acc.std())}
        hists[name] = np.bincount(np.minimum(runs, 12), minlength=13)[1:] / reps
    # the chance that 20 tosses of a fair coin contain a run of four or more: count the sequences that do not
    # free[r]: the number of sequences so far with no run of four that end in a run of length r
    free = {r: (2.0 if r == 1 else 0.0) for r in (1, 2, 3)}
    for _ in range(19):
        free = {1: free[1] + free[2] + free[3], 2: free[1], 3: free[2]}
    p_run4 = 1 - sum(free.values()) / 2 ** 20
    example_person = lab.human_like_sequence(40, 0.6, rng(502))
    example_coin = lab.human_like_sequence(40, 0.5, rng(503))
    assert out["person"]["accuracy"] > out["coin"]["accuracy"] + 0.03 and abs(out["coin"]["accuracy"] - 0.5) < 0.01
    assert out["person"]["longest_run"] < out["coin"]["longest_run"]
    return {"n_press": n_press, "p_person": 0.6, "person": out["person"], "coin": out["coin"],
            "example_person": example_person, "example_coin": example_coin,
            "p_run4_in_20": p_run4, "run_lengths": np.arange(1, 13), "hist_runs_person": hists["person"], "hist_runs_coin": hists["coin"],
            "expected_longest_run_coin": float(math.log2(n_press))}


ITEMS = {
    "hans": compute_hans,
    "one_group": compute_one_group,
    "threats": compute_threats,
    "balance": compute_balance,
    "within": compute_within,
    "expectancy": compute_expectancy,
    "factorial": compute_factorial,
    "be_random": compute_be_random,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

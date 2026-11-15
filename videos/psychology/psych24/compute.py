"""Precompute every number in Part 24 of *Psychology, Built* ("Reasoning and Problem Solving").

    python -m videos.psychology.psych24.compute            # everything missing (under a minute; fetches data once)
    python -m videos.psychology.psych24.compute --force rotation

Results are cached in ``.cache/psych24/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.reason``).  The syllogism answers are Ragni's 2016 data as packaged in the
CCOBRA benchmark, and the mental rotation times Ganis and Kievit's 2015 validation data, both fetched by
``explainer.psychology.opendata``.  Simulations use fixed seeds; where a part shows one run of many, it is the run
of median length, chosen by rule.

Items:
    syllogisms   the 64 syllogisms: valid conclusions, people's answers, accuracy, and four accounts scored
    selection    the expected information gain of each card, and where the card order changes with P(p), P(q)
    hanoi        the 3-disc state space and its layout, the shortest path, a hill-climber's path, the goal stack's
                 move latencies for 4 discs
    ninedots     every drawing of four lines through the nine dots, turning inside the box and outside it
    analogy      a structure-mapping of the fortress story onto the radiation problem
    rotation     open data: time and errors by angle; each person's rotation rate; Psyche's rotation model
    causes       delta P and causal power for a cause that adds the same strength on different backgrounds
    everyday     posterior-median predictions under power-law, Erlang and Gaussian priors
    usability    the share of usability problems found by n test users
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import opendata
from explainer.psychology.psyche import reason as R

CACHE = Cache("psych24")
load = CACHE.load


def compute_syllogisms() -> dict:
    d = opendata.syllogisms_ragni2016()
    parsed = [R.parse_ccobra(t, r) for t, r in zip(d["task"], d["response"])]
    T = R.response_table([a for a, _ in parsed], [b for _, b in parsed])
    ri = {r: k for k, r in enumerate(R.RESPONSES)}
    valid = [R.valid_conclusions(t) for t in R.TASKS]
    acc = np.array([T[k, [ri[r] for r in v]].sum() for k, v in enumerate(valid)])
    has_valid = np.array([v != ["NVC"] for v in valid])
    out = {"table": T, "tasks": np.array(R.TASKS), "responses": np.array(R.RESPONSES), "accuracy": acc,
           "has_valid": has_valid, "n_people": int(len(np.unique(d["id"]))), "n_answers": int(len(d["id"])),
           "n_valid": int(has_valid.sum()), "mean_acc": float(acc.mean()),
           "acc_valid": float(acc[has_valid].mean()), "acc_nvc": float(acc[~has_valid].mean()),
           "nvc_share": float(T[:, -1].mean()), "median_age": float(np.median(d["age"][d["age"] > 0])),
           "valid_str": np.array(["/".join(v) for v in valid])}
    for acct in ("logic", "atmosphere", "matching", "phm"):
        hits_v = sum(int(np.argmax(T[k])) in [ri[r] for r in R.predict(t, acct)]
                     for k, t in enumerate(R.TASKS) if has_valid[k])
        hits_n = sum(int(np.argmax(T[k])) in [ri[r] for r in R.predict(t, acct)]
                     for k, t in enumerate(R.TASKS) if not has_valid[k])
        sc = R.score(T, acct)
        out[f"{acct}_hits_valid"], out[f"{acct}_hits_nvc"] = hits_v, hits_n
        out[f"{acct}_coverage"] = sc["coverage"]
    order = np.argsort(acc)
    out["hardest"], out["easiest"] = np.array(R.TASKS)[order[:3]], np.array(R.TASKS)[order[-3:]]
    # two worked examples: All-All (figure 1), and No-All (figure 1), the hardest
    for name in ("AA1", "EA1"):
        out[f"ex_{name}"] = T[R.TASKS.index(name)]
    return out


def compute_selection() -> dict:
    g = R.selection_information(0.1, 0.2)
    cards = ["p", "q", "not-q", "not-p"]
    a_grid = np.linspace(0.02, 0.5, 49)
    b_grid = np.linspace(0.02, 0.98, 97)
    first = np.full((len(b_grid), len(a_grid)), -1)
    for j, a in enumerate(a_grid):
        for i, b in enumerate(b_grid):
            if b < a:
                continue
            e = R.selection_information(a, b)
            first[i, j] = ["p", "q", "not-q", "not-p"].index(max(e, key=e.get))
    # where does not-q beat q?  the line P(q) = 1 - P(p) and beyond, for a rare p
    q_vs_notq = np.array([[R.selection_information(a, b)["q"] - R.selection_information(a, b)["not-q"]
                           if b >= a else np.nan for a in a_grid] for b in b_grid])
    return {"cards": np.array(cards), "eig": np.array([g[c] for c in cards]),
            "people": np.array([0.89, 0.62, 0.25, 0.16]), "people_n": 845, "people_studies": 13,
            "a_grid": a_grid, "b_grid": b_grid, "q_minus_notq": q_vs_notq}


def compute_hanoi() -> dict:
    S, E = R.hanoi_graph(3)
    pos = R.hanoi_layout(3)
    xy = np.array([pos[s] for s in S])
    start, goal = (0, 0, 0), (2, 2, 2)
    opt = R.hanoi_shortest(start, goal)
    idx = {s: k for k, s in enumerate(S)}
    runs = [R.hill_climb(3, rng=seed) for seed in range(101)]
    lens = np.array([len(p) - 1 for p in runs])
    med = int(np.argsort(lens)[len(lens) // 2])  # the run of median length, by rule
    g = R.goal_stack_solver(4)
    runs4 = np.array([len(R.hill_climb(4, rng=seed)) - 1 for seed in range(101)])
    return {"xy": xy, "edges": np.array(E), "states": np.array(S), "opt": np.array([idx[s] for s in opt]),
            "hill": np.array([idx[s] for s in runs[med]]), "hill_lengths": lens, "hill_median": int(lens[med]),
            "hill_optimal_share": float((lens == 7).mean()), "hill4_median": float(np.median(runs4)),
            "latency4": g["latency"], "moves4": np.array(g["moves"]), "n_states": len(S)}


def compute_ninedots() -> dict:
    inside = R.nine_dots(0, 2)
    outside = R.nine_dots(-1, 3)
    wider = R.nine_dots(-2, 4)
    classic = next(p for p in outside if p[0] == (0, 0) and p[1] == (0, 3)) if outside else []
    return {"n_inside": len(inside), "n_outside": len(outside), "n_wider": len(wider),
            "classic": np.array(classic, float), "outside": np.array([np.array(p, float) for p in outside])}


FORTRESS = [
    ("cause", ("divide", "army"), ("converge", "army", "fortress")),
    ("cause", ("converge", "army", "fortress"), ("capture", "army", "fortress")),
    ("block", "mines", ("converge", "army", "fortress")),
    ("surround", "roads", "fortress"),
    ("command", "general", "army"),
]
RADIATION = [
    ("cause", ("divide", "rays"), ("converge", "rays", "tumour")),
    ("cause", ("converge", "rays", "tumour"), ("capture", "rays", "tumour")),
    ("block", "tissue", ("converge", "rays", "tumour")),
    ("surround", "tissue", "tumour"),
    ("command", "doctor", "rays"),
]


def compute_analogy() -> dict:
    m = R.structure_map(FORTRESS, RADIATION)
    return {"score": m["score"], "pairs": np.array(sorted(m["mapping"].items())), "n_matched": len(m["matched"]),
            "n_base": len(FORTRESS)}


def compute_rotation() -> dict:
    d = opendata.mental_rotation()
    subj = np.unique(d["subject"])
    angles = np.array([0.0, 50.0, 100.0, 150.0])
    ok_same = d["same"] & d["correct"]
    per = np.array([[np.mean(d["rt"][ok_same & (d["subject"] == s) & (d["angle"] == a)]) for a in angles]
                    for s in subj])
    err_same = np.array([1 - d["correct"][d["same"] & (d["angle"] == a)].mean() for a in angles])
    err_diff = np.array([1 - d["correct"][~d["same"] & (d["angle"] == a)].mean() for a in angles])
    fits = [R.rotation_fit(d["angle"][ok_same & (d["subject"] == s)], d["rt"][ok_same & (d["subject"] == s)])
            for s in subj]
    slope = np.array([f["slope"] for f in fits])
    icpt = np.array([f["intercept"] for f in fits])
    group = R.rotation_fit(np.repeat(angles[None], len(subj), 0).ravel(), per.ravel())
    model = R.rotation_model(angles, rate=float(1000 / np.median(slope)), t0=float(np.median(icpt)), n=2000,
                             rng=np.random.default_rng(1971))
    return {"angles": angles, "mean": per.mean(0), "se": per.std(0, ddof=1) / np.sqrt(len(subj)),
            "err_same": err_same, "err_diff": err_diff, "slope": slope, "intercept": icpt,
            "median_rate": float(1000 / np.median(slope)), "median_slope": float(np.median(slope)),
            "positive": int((slope > 0).sum()), "n": len(subj), "n_trials": int(len(d["rt"])),
            "group_slope": group["slope"], "group_intercept": group["intercept"],
            "model_mean": model.mean(0), "model_sd": model.std(0), "accuracy": float(d["correct"].mean())}


def compute_causes() -> dict:
    base = np.linspace(0, 0.9, 10)  # P(e | not c)
    q = 0.5  # the cause's power, the same throughout
    pe_c = base + q * (1 - base)
    dp = pe_c - base
    power = dp / (1 - base)
    return {"base": base, "pe_c": pe_c, "delta_p": dp, "power": power, "q": q}


def compute_everyday() -> dict:
    t = np.linspace(1, 100, 100)
    out = {"t": t}
    for g in (0.5, 1.0, 2.0):
        out[f"power_{g}"] = np.array([R.predict_total(x, "power", gamma=g) for x in t])
    out["erlang"] = np.array([R.predict_total(x, "erlang", scale=20.0) for x in t])
    out["gauss"] = np.array([R.predict_total(x, "gauss", mu=75.0, sigma=16.0) for x in t])
    out["ex_life_18"] = R.predict_total(18.0, "gauss", mu=75.0, sigma=16.0)
    out["ex_life_39"] = R.predict_total(39.0, "gauss", mu=75.0, sigma=16.0)
    out["ex_life_90"] = R.predict_total(90.0, "gauss", mu=75.0, sigma=16.0)
    # the film example: $40 million so far, a power-law prior p(T) ~ 1/T (gamma = 1), each curve scaled to peak 1
    T = np.linspace(5.0, 300.0, 600)
    seen = 40.0
    like = np.where(T >= seen, seen / T, 0.0)
    out.update(film_T=T, film_prior=5.0 / T, film_like=like, film_post=like ** 2, film_seen=seen,
               film_guess=R.predict_total(seen, "power", gamma=1.0))
    return out


def compute_usability() -> dict:
    n = np.arange(0, 16)
    L = 0.31
    return {"n": n, "found": 1 - (1 - L) ** n, "L": L, "five": float(1 - (1 - L) ** 5)}


ITEMS = {
    "syllogisms": compute_syllogisms,
    "selection": compute_selection,
    "hanoi": compute_hanoi,
    "ninedots": compute_ninedots,
    "analogy": compute_analogy,
    "rotation": compute_rotation,
    "causes": compute_causes,
    "everyday": compute_everyday,
    "usability": compute_usability,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

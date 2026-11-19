"""Precompute every number in Part 5 of *Economics, Built* ("What People Want").

    python -m videos.economics.econ5.compute            # everything missing (a minute or so)
    python -m videos.economics.econ5.compute --force america

Results are cached in ``.cache/econ5/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: personal consumption expenditures by type of product, 1929-2025; the transcribed
tables of Harbaugh et al., Choi et al., Andreoni and Miller, Chen et al., Saez and McFadden).  Models: Agora's consumer
(``agora.consumer``), with the Island's Part 5 truths.  Every random draw is seeded.

Items:
    budgets       the eleven budget lines of Play it, as prices and incomes
    choosers      four islanders' choices on the eleven lines; GARP, CCEI, Houtman-Maks; Afriat's solution for Bo
                  and three of its indifference curves
    receipts      Bo's three receipts from the hook, and their contradiction
    bronars       random choosers on the same lines: how often they violate GARP, and their CCEIs
    shapes        indifference maps of the standard preferences, and the CES family
    tangency      Bo's best bundle on one budget, the multiplier as the value of a dollar
    pump          the money pump: a trader with circular tastes, swap by swap
    bulk          Bo's budget with a bulk price for coconuts: a non-convex budget and a jump in demand
    credit        4,000 earners facing the EITC's first kink at three elasticities
    becker        Becker's random islanders: demand slopes down anyway
    ferry         the ferry survey: a logit fitted to 2,000 choices recovers the planted value of time
    varian        bounds on Bo's indifference curve from his eleven choices alone, against the planted curve
    america       America as one consumer, 1929-2025: fifteen goods, GARP, and the test's power
    repeat        Bo on the same line forty times: the spread that random utility models
    studies       the published consistency scores (children, students, Dutch adults, altruists, GPT)
    dial          the consistency dial's rows
    film          the intermission's data film: a century of the American basket
    melody        its data melody: the share of spending on food at home, year by year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import consumer as cs
from explainer.economics.data import tables

CACHE = Cache("econ5")
load = CACHE.load
TRUTH = island.truths(5)
INCOME = 60.0     # every Play-it line is $60 of island money: fish at 60/A, coconuts at 60/B


def _lines():
    L = np.array(TRUTH["budgets"]["lines"], float)
    P = np.column_stack([INCOME / L[:, 0], INCOME / L[:, 1]])
    return L, P, np.full(len(L), INCOME)


def compute_budgets() -> dict:
    L, P, m = _lines()
    return {"lines": L, "prices": P, "income": m}


def _choose(spec: dict, P, m, rng) -> np.ndarray:
    if spec["kind"] == "random":
        return cs.random_on_budgets(P, m, rng)
    pref = cs.Preference(spec["kind"], a=spec.get("a", 0.5), b=spec.get("b", 1.0))
    X = np.array([pref.demand(px, py, mm) for (px, py), mm in zip(P, m)])
    tr = spec.get("tremble", 0.0)
    if tr:
        # slide along the budget line by a small random share of the line's length
        share = np.clip(X[:, 0] * P[:, 0] / m + rng.normal(0, tr / 2, len(m)), 0, 1)
        X = np.column_stack([share * m / P[:, 0], (1 - share) * m / P[:, 1]])
    return X


def compute_choosers() -> dict:
    L, P, m = _lines()
    spec = TRUTH["choosers"]
    rng = np.random.default_rng(spec["seed"])
    out = {}
    for who in ("bo", "ana", "chidi", "dara"):
        X = _choose(spec[who], P, m, rng)
        v = cs.garp_violations(P, X)
        out[who] = {"X": X, "violations": v, "n_violations": len({i for i, _ in v}), "ccei": cs.ccei(P, X),
                    "warp": cs.warp_violations(P, X), "hm": len(cs.houtman_maks(P, X)),
                    "left_on_table": 1 - cs.ccei(P, X)}
    # Afriat's construction for Ana and Chidi (who pass exactly), and Bo at his own efficiency
    for who in ("ana", "chidi"):
        sol = cs.afriat(P, out[who]["X"])
        out[who]["afriat"] = None if sol is None else {"U": sol["U"], "lam": sol["lam"]}
    Xb = out["bo"]["X"]
    keep = cs.houtman_maks(P, Xb)
    sol = cs.afriat(P[keep], Xb[keep])
    gx = np.linspace(0.2, 13, 140)
    gy = np.linspace(0.2, 13, 140)
    GX, GY = np.meshgrid(gx, gy)
    u = cs.afriat_utility(P[keep], Xb[keep], sol)(np.column_stack([GX.ravel(), GY.ravel()])).reshape(GX.shape)
    out["bo"]["keep"] = keep
    ufun = cs.afriat_utility(P[keep], Xb[keep], sol)
    xs = np.linspace(0.15, 13, 260)
    curves = {}
    for i in (int(np.argmin(sol["U"])), int(np.argsort(sol["U"])[len(keep) // 2]), int(np.argmax(sol["U"]))):
        level = float(sol["U"][i])
        lo, hi = np.zeros_like(xs), np.full_like(xs, 40.0)
        for _ in range(60):                      # u rises with coconuts: bisect for the curve's height at each x
            mid = 0.5 * (lo + hi)
            up = ufun(np.column_stack([xs, mid])) >= level
            hi, lo = np.where(up, mid, hi), np.where(up, lo, mid)
        ys = np.where(hi < 39.9, hi, np.nan)
        curves[str(keep[i])] = ys
    out["bo"]["afriat"] = {"U": sol["U"], "lam": sol["lam"], "grid_x": gx, "grid_y": gy, "u": u,
                           "levels": np.sort(sol["U"]), "xs": xs, "curves": curves}
    return out


def compute_receipts() -> dict:
    """Bo's three receipts from the hook: week 1 and week 3 contradict each other."""
    P = np.array([[4.0, 3.0], [2.0, 4.0], [6.0, 2.0]])
    X = np.array([[3.0, 8.0], [6.0, 6.0], [4.0, 6.0]])
    C = P @ X.T
    return {"P": P, "X": X, "spend": np.diag(C), "cost": C, "warp": cs.warp_violations(P, X),
            "garp": cs.garp_violations(P, X), "ccei": cs.ccei(P, X)}


def compute_bronars() -> dict:
    L, P, m = _lines()
    b = cs.bronars(P, m, reps=5000, seed=1987)
    edges = np.linspace(0.4, 1.0, 25)
    h, _ = np.histogram(np.clip(b["ccei"], 0.4, 1.0), bins=edges)
    return {"power": b["power"], "ccei_mean": b["ccei_mean"], "above_95": b["share_above_95"],
            "above_90": b["share_above_90"], "edges": edges, "hist": h / len(b["ccei"]), "reps": 5000}


def _symmetric_curve(pref, level: float, top: float = 12.0, n: int = 300) -> np.ndarray:
    """Points of an indifference curve of a symmetric preference (equal weights), as an (m x 2) array from the top
    left to the bottom right: the branch below the diagonal is computed, the other is its mirror image, so the steep
    part is drawn as well as the flat part however sharp the corner."""
    lo = level * 1.0000001
    xs = np.unique(np.concatenate([lo + (top - lo) * np.linspace(0, 1, n) ** 2]))
    ys = pref.indifference(level, xs)
    ok = np.isfinite(ys) & (ys >= 0) & (ys <= xs + 1e-9)
    branch = np.column_stack([xs[ok], ys[ok]])
    mirror = branch[::-1][:, ::-1]
    return np.vstack([mirror, branch])


def compute_shapes() -> dict:
    xs = np.linspace(0.05, 12, 400)
    maps = {}
    for key, pref in (("cobb-douglas", cs.Preference("cobb-douglas", a=0.5)),
                      ("substitutes", cs.Preference("substitutes", a=1.0, b=1.0)),
                      ("quasilinear", cs.Preference("quasilinear", a=2.0))):
        levels = {"cobb-douglas": (2, 4, 6, 8), "substitutes": (3, 6, 9, 12), "quasilinear": (2, 4, 6, 8)}[key]
        maps[key] = {"levels": levels,
                     "curves": [np.column_stack([xs, pref.indifference(lv, xs)]) for lv in levels]}
    maps["complements"] = {"levels": (2, 4, 6, 8),
                           "curves": [np.array([[lv, 12.0], [lv, lv], [12.0, lv]]) for lv in (2, 4, 6, 8)]}
    sigmas = (0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 20.0)
    ces = {f"{s:g}": _symmetric_curve(cs.Preference("ces", a=0.5, sigma=s), 5.0) for s in sigmas}
    return {"xs": xs, "maps": maps, "ces": ces, "sigmas": sigmas}


def compute_tangency() -> dict:
    pref = cs.Preference("cobb-douglas", a=0.6)
    px, py, m = 4.0, 3.0, 60.0
    x, y = pref.demand(px, py, m)
    u0 = float(pref.u(x, y))
    x1, y1 = pref.demand(px, py, m + 1)
    lam = pref.a * float(pref.u(x, y)) / (px * x)       # MU_x / p_x at the optimum
    xs = np.linspace(0.2, 15, 300)
    return {"px": px, "py": py, "m": m, "x": x, "y": y, "u": u0, "mrs": pref.mrs(x, y), "ratio": px / py,
            "lam": lam, "du_one_dollar": float(pref.u(x1, y1)) - u0, "xs": xs, "ic": pref.indifference(u0, xs),
            "ic_low": pref.indifference(u0 * 0.75, xs), "ic_high": pref.indifference(u0 * 1.25, xs)}


def compute_pump() -> dict:
    p = TRUTH["pump"]
    goods = list(p["goods"])
    holding, coins, steps = "fish", 30, []
    # the trader prefers the next good in the circle to the one he holds: cloth over fish, coconut over cloth...
    better = {"fish": "cloth", "cloth": "coconut", "coconut": "fish"}
    for k in range(p["rounds"]):
        nxt = better[holding]
        coins -= p["fee"]
        steps.append({"from": holding, "to": nxt, "coins": coins})
        holding = nxt
    return {"goods": goods, "better": better, "steps": steps, "start_coins": 30, "fee": p["fee"]}


def compute_bulk() -> dict:
    """Coconuts cost price_first each for the first ``first``, then price_after: the budget frontier bends outward
    (a non-convex budget set).  Bo (Cobb-Douglas, half and half) stays below the threshold when he is poor and jumps
    past it, skipping a whole range of quantities, once his income is high enough."""
    b = TRUTH["bulk"]
    pref = cs.Preference("cobb-douglas", a=0.5)
    cap = b["first"] * b["price_first"]

    def frontier(m):
        s = np.linspace(0, m, 6001)               # money spent on coconuts
        coconuts = np.where(s <= cap, s / b["price_first"], b["first"] + (s - cap) / b["price_after"])
        return (m - s) / b["fish"], coconuts

    incomes = np.linspace(8.0, 40.0, 161)
    best = np.array([[cs.best_on_frontier(pref, *frontier(m))[k] for k in ("x", "y")] for m in incomes])
    jump = int(np.argmax(np.diff(best[:, 1])))
    # where the two local optima tie: (m - first)^2 / 4 = m^2 / 8 for Cobb-Douglas halves (price_after = 1)
    tie = b["first"] / (1 - 1 / np.sqrt(2)) if b["price_after"] == 1.0 else float(incomes[jump])
    shown = {}
    for m in (16.0, 28.0):
        f, c = frontier(m)
        r = cs.best_on_frontier(pref, f, c)
        shown[f"{m:g}"] = {"frontier": np.column_stack([f, c]), "choice": (r["x"], r["y"]), "u": r["u"]}
    return {"incomes": incomes, "best": best, "jump": (best[jump].tolist(), best[jump + 1].tolist()),
            "jump_income": float(incomes[jump + 1]), "tie": float(tie), "shown": shown, "first": b["first"],
            "price_first": b["price_first"], "price_after": b["price_after"], "fish": b["fish"]}


def compute_credit() -> dict:
    c = TRUTH["credit"]
    rng = np.random.default_rng(c["seed"])
    n = c["median"] * np.exp(rng.normal(0, c["sigma"], c["people"]))
    t = tables.SAEZ_2010.data["one_child_2008"]
    edges = np.arange(0, 20001, 500)
    out = {"edges": edges, "kink": t["phase_in"][1], "plateau_end": t["plateau"][1], "rate_in": t["phase_in"][2],
           "rate_out": t["phase_out"][2], "top": t["phase_in"][2] * t["phase_in"][1], "by_e": {}}
    for e in c["elasticities"]:
        z = cs.earnings_choice(n, e)
        h, _ = np.histogram(z, bins=edges)
        out["by_e"][f"{e:g}"] = {"hist": h, "at_kink": float(np.mean(np.abs(z - out["kink"]) < 5))}
    zz = np.linspace(0, 36000, 721)
    out["schedule"] = {"z": zz, "credit": cs.eitc(zz)}
    return out


def compute_becker() -> dict:
    b = TRUTH["becker"]
    d = cs.becker_demand(b["prices"], b["income"], b["people"], seed=b["seed"])
    pick = [0, 1, 2]
    return {"prices": d["prices"], "mean": d["mean"], "theory": d["theory"], "few": d["each"][:, pick].T,
            "people": b["people"], "income": b["income"]}


def compute_ferry() -> dict:
    f = TRUTH["ferry"]
    rng = np.random.default_rng(f["seed"])
    n = f["trips"]
    saves = rng.choice(np.array(f["saves"], float), n)
    extra = rng.uniform(0, f["max_extra"], n)
    vot_min = f["value_of_time"] / 60
    v = f["scale"] * (vot_min * saves - extra)
    fast = (rng.random(n) < 1 / (1 + np.exp(-v))).astype(float)
    fit = cs.logit_fit(np.column_stack([saves, extra]), fast)
    a, b = fit["b"]
    vot = -a / b * 60
    # the delta method for the ratio
    cov = np.linalg.inv((np.column_stack([saves, extra]) * (lambda p: p * (1 - p))(
        1 / (1 + np.exp(-np.column_stack([saves, extra]) @ fit["b"])))[:, None]).T @ np.column_stack([saves, extra]))
    g = np.array([-1 / b, a / b ** 2]) * 60
    vot_se = float(np.sqrt(g @ cov @ g))
    bins = np.linspace(0, f["max_extra"], 11)
    shares = {}
    for s_ in f["saves"]:
        m = saves == s_
        idx = np.digitize(extra[m], bins) - 1
        shares[str(s_)] = [float(fast[m][idx == k].mean()) if np.any(idx == k) else None for k in range(10)]
    return {"bins": bins, "shares": shares, "a": float(a), "b": float(b), "se": fit["se"], "vot": float(vot),
            "vot_se": vot_se, "truth": f["value_of_time"], "trips": n, "saves": list(f["saves"]),
            "max_extra": f["max_extra"]}


def compute_varian() -> dict:
    L, P, m = _lines()
    ch = compute_choosers()
    X = ch["bo"]["X"][ch["bo"]["keep"]]
    PP = P[ch["bo"]["keep"]]
    k = int(np.argmin(np.abs(X[:, 0] - X[:, 1] * 1.0) + np.abs(PP[:, 0] - PP[:, 1])))
    worse = cs.revealed_worse(PP, X, k)
    better = cs.revealed_better(PP, X, k)
    pref = cs.Preference("cobb-douglas", a=TRUTH["choosers"]["bo"]["a"])
    xs = np.linspace(0.3, 13, 300)
    # a forecast from revealed preference alone: on a new budget (10 fish or 5 coconuts), which choices would keep
    # all twelve consistent?
    A, B = 10.0, 5.0
    pn = np.array([INCOME / A, INCOME / B])
    grid = np.linspace(0, A, 801)
    ok = [float(x) for x in grid if not cs.garp_violations(np.vstack([PP, pn]),
                                                           np.vstack([X, [x, (INCOME - pn[0] * x) / pn[1]]]))]
    truth = pref.demand(pn[0], pn[1], INCOME)
    return {"P": PP, "X": X, "k": k, "worse": worse, "better": better, "xs": xs,
            "true_ic": pref.indifference(float(pref.u(*X[k])), xs),
            "predict": {"line": (A, B), "lo": min(ok), "hi": max(ok), "truth": truth}}


def compute_america() -> dict:
    d = data.pce_by_type()
    P, X = d["prices"], d["quantities"]
    years = d["years"]
    v = cs.garp_violations(P, X)
    rng = np.random.default_rng(1929)
    budget = (P * X).sum(1)
    shares = (P * X) / budget[:, None]

    def power_random(idx, reps):
        return float(np.mean([bool(cs.garp_violations(P[idx], cs.random_on_budgets(P[idx], budget[idx], rng)))
                              for _ in range(reps)]))

    def power_shuffle(idx, reps):
        hits = 0
        for _ in range(reps):
            perm = rng.permutation(len(idx))
            Xr = shares[idx][perm] * budget[idx][:, None] / P[idx]
            hits += bool(cs.garp_violations(P[idx], Xr))
        return hits / reps

    allidx = np.arange(len(years))
    windows = {}
    for a, b in ((1929, 1940), (1970, 1985), (2000, 2025)):
        idx = np.array([years.index(y) for y in range(a, b + 1)])
        windows[f"{a}-{b}"] = {"random": power_random(idx, 300), "shuffle": power_shuffle(idx, 300),
                               "violations": len(cs.garp_violations(P[idx], X[idx]))}
    C = P @ X.T
    own = np.diag(C)
    afford = int(((C <= own[:, None] + 1e-9) & ~np.eye(len(years), dtype=bool)).sum())
    return {"years": years, "names": d["names"], "codes": d["codes"], "shares": shares, "real_total": X.sum(1),
            "spending": budget, "violations": len(v), "ccei": cs.ccei(P, X),
            "power_random": power_random(allidx, 200), "power_shuffle": power_shuffle(allidx, 200),
            "windows": windows, "affordable_pairs": afford, "pairs": len(years) * (len(years) - 1)}


def compute_repeat() -> dict:
    L, P, m = _lines()
    spec = TRUTH["choosers"]["bo"]
    rng = np.random.default_rng(4040)
    Pk = np.repeat(P[:1], 40, axis=0)
    mk = np.repeat(m[:1], 40)
    X = _choose(spec, Pk, mk, rng)
    share = X[:, 0] * Pk[:, 0] / mk
    return {"line": L[0], "X": X, "share": share, "mean_share": float(share.mean()), "sd": float(share.std(ddof=1)),
            "planted": spec["a"]}


def compute_studies() -> dict:
    h = tables.HARBAUGH_2001.data
    c7 = tables.CHOI_2007.data
    c14 = tables.CKMS_2014.data
    am = tables.ANDREONI_MILLER_2002.data
    gpt = tables.CHEN_2023.data
    return {"harbaugh": h, "choi2007": c7, "ckms2014": c14, "andreoni_miller": am, "chen2023": gpt}


def compute_dial() -> dict:
    h = tables.HARBAUGH_2001.data["groups"]
    rows = [("Harbaugh et al. (2001)", "7-year-olds, 11 sets", h["second graders"]["afriat"], "lab"),
            ("Harbaugh et al. (2001)", "11-year-olds, 11 sets", h["sixth graders"]["afriat"], "lab"),
            ("Harbaugh et al. (2001)", "undergraduates, 11 sets", h["undergraduates"]["afriat"], "lab"),
            ("Choi et al. (2007)", "Berkeley students, 50 budgets", tables.CHOI_2007.data["mean_ccei"], "lab"),
            ("Choi et al. (2014)", "1,182 Dutch adults, 25 budgets", tables.CKMS_2014.data["mean_ccei"], "online panel"),
            ("Chen et al. (2023)", "their human subjects, food", tables.CHEN_2023.data["humans"]["food"], "online"),
            ("Chen et al. (2023)", "GPT, food", tables.CHEN_2023.data["gpt"]["food"], "a language model")]
    rand = [("random choice, Harbaugh's 11 sets", tables.HARBAUGH_2001.data["groups"]["random (uniform)"]["afriat"]),
            ("random choice, 50 budgets", tables.CHOI_2007.data["random"]["budgets_50"]["mean_ccei"])]
    return {"rows": rows, "random": rand}


FILM_SECONDS = 38.0
MELODY_SECONDS = 46.0


def film_time(k: int, n: int) -> float:
    """When the data film reaches the k-th year (0-based) of n."""
    return 1.5 + FILM_SECONDS * k / (n - 1)


def compute_film() -> dict:
    a = compute_america()
    n = len(a["years"])
    return {"years": a["years"], "shares": a["shares"], "names": a["names"], "codes": a["codes"],
            "times": [film_time(k, n) for k in range(n)], "real_total": a["real_total"]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    food = np.array(f["shares"])[:, f["codes"].index("DFXA")] * 100
    times = f["times"]
    mel = score.data_melody(food, MELODY_SECONDS, times=times, act=2, log=False, low=50, high=84)
    events = {"film_end": times[-1] + 1.5, "war": times[f["years"].index(1944)], "first": times[0]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.3, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], f["years"])],
                meta={"label": "a century of the American basket: the share spent on food at home, 1929-2025, as a "
                               "tune (computed)", "kind": "synthesized"})
    ClipStore("econ5").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "food": food, "seconds": MELODY_SECONDS}


ITEMS = {
    "budgets": compute_budgets,
    "choosers": compute_choosers,
    "receipts": compute_receipts,
    "bronars": compute_bronars,
    "shapes": compute_shapes,
    "tangency": compute_tangency,
    "pump": compute_pump,
    "bulk": compute_bulk,
    "credit": compute_credit,
    "becker": compute_becker,
    "ferry": compute_ferry,
    "varian": compute_varian,
    "america": compute_america,
    "repeat": compute_repeat,
    "studies": compute_studies,
    "dial": compute_dial,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

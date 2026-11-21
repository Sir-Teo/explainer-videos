"""Precompute every number in Part 49 of *Economics, Built* ("The Economic Approach").

    python -m videos.economics.econ49.compute            # everything missing (under a minute)
    python -m videos.economics.econ49.compute --force star

Results are cached in ``.cache/econ49/<name>.json`` (+ ``.npz``); scenes call ``load(name)``. Data: the Data Room
(``explainer.economics.data``: Tennessee's Project STAR, California's school districts, Angrist and Evans's census
mothers, cigarettes by state, the Australian Health Survey and murder rates in 1950, all as distributed in the R
package AER; FRED's labour force participation by sex; Our World in Data's children per woman; the tables of Part 49).
Models: Agora's economic approach (``agora.family``) with the Island's Part 49 truths.

Items:
    offenders   potential offenders: who offends at the start, and with the chance or the sentence doubled, by kind
    deterrence  the offence rate over the chance of being caught and the sentence (risk-neutral offenders)
    planner     Becker's planner: the loss over the chance and the fine, with fines and with prison
    police      the Island's blocks: the naive, noisy and experimental estimates against the planted elasticity
    murder      murder rates in 44 states in 1950 against convictions and executions
    participation  women's and men's labour force participation, 1948-2025 (BLS via FRED)
    household   who works where as the second earner's wage rises
    marriage    a marriage market by education: equilibrium, estimated surplus, sorting; more men; more educated women
    fertility   children per woman, 1950-2023, for the world, China, South Korea, India, the US and Japan (OWID)
    qq          quantity and quality as the mother's wage rises
    angrist     Angrist and Evans on AER's 30,000 mothers: same-sex siblings, a third child, weeks worked
    bargain     child spending in a unitary and a collective household as the mother's share of income rises
    star        Project STAR: kindergarten and grade-3 percentiles by class type, within schools
    caschools   California districts: scores against pupils per teacher, with and without controls
    maimonides  the Island's schools under a cap of 40: class size, scores, naive and discontinuity estimates
    teachers    teachers' value added: raw, shrunk, the move test, with and without sorting
    grossman    the demand for health over a life
    doctors     the Australian Health Survey: doctor visits by insurance, Poisson regression
    drug        a patented drug: the monopoly price, the profit that pays for discovery, the lost triangle
    cigarettes  cigarette demand by state: OLS and 2SLS in 1995 and in ten-year differences
    addiction   a rational and a myopic addict facing an announced price rise
    film        the intermission's data film: the world's children per woman, 1950-2023
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import family as fm

CACHE = Cache("econ49")
load = CACHE.load
TRUTH = island.truths(49)
FILM_SECONDS = 52.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def _gains() -> np.ndarray:
    O = TRUTH["offenders"]
    rng = np.random.default_rng(O["seed"])
    return O["median"] * np.exp(O["sigma"] * rng.standard_normal(O["n"]))


def compute_offenders() -> dict:
    O = TRUTH["offenders"]
    g = _gains()
    play = fm.play_doubling(O["p"], O["sentence"], g, TRUTH["kinds"])
    el = {k: fm.elasticities(O["p"], O["sentence"], g, a, b) for k, (a, b) in TRUTH["kinds"].items()}
    edges = np.linspace(0.0, 6.0, 31)
    hist, _ = np.histogram(g, bins=edges)
    return {"p": O["p"], "sentence": O["sentence"], "play": play, "elasticities": el, "kinds": list(TRUTH["kinds"]),
            "hist": (hist / len(g)).tolist(), "edges": edges.tolist(), "above6": float(np.mean(g > 6)),
            "median": float(np.median(g)),
            "expected": O["p"] * O["sentence"]}


def compute_deterrence() -> dict:
    g = _gains()
    ps = np.linspace(0.02, 0.6, 30)
    ss = np.linspace(0.5, 12, 30)
    grid = [[fm.offend_share(p, s, g) for s in ss] for p in ps]
    return {"p": ps.tolist(), "s": ss.tolist(), "rate": grid}


def compute_planner() -> dict:
    P = TRUTH["planner"]
    O = TRUTH["offenders"]
    g = _gains()
    fine = fm.optimal_enforcement(g, P["harm"], P["cost_p"], P["f_max"], 0.0, n_p=80, n_f=80)
    keep = ("p_star", "f_star", "loss_star", "offences_star")
    # along the curve of equal deterrence through the start (p F = 0.6), the cost of catching falls as F rises
    k = O["p"] * O["sentence"]
    fs = np.linspace(k / 0.42, P["f_max"], 60)
    start_rate = fm.offend_share(O["p"], O["sentence"], g)
    start_loss = P["harm"] * start_rate + P["cost_p"] * O["p"]
    return {**{x: fine[x] for x in keep}, "curve_f": fs.tolist(), "curve_p": (k / fs).tolist(), "k": k,
            "start_rate": start_rate, "start_loss": start_loss, **P}


def compute_police() -> dict:
    return fm.police_blocks(**TRUTH["police"])


def _ols(X, y, cluster=None):
    X, y = np.asarray(X, float), np.asarray(y, float)
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    XtX = np.linalg.inv(X.T @ X)
    if cluster is None:
        meat = (X * e[:, None] ** 2).T @ X                    # HC0
        n, k = X.shape
        V = XtX @ meat @ XtX * n / (n - k)
    else:
        meat = np.zeros((X.shape[1], X.shape[1]))
        for c in np.unique(cluster):
            s = X[cluster == c].T @ e[cluster == c]
            meat += np.outer(s, s)
        V = XtX @ meat @ XtX
    return b, np.sqrt(np.diag(V))


def compute_murder() -> dict:
    M = data.murder_rates()
    rate, conv, exe = (np.array(M[k]) for k in ("rate", "convictions", "executions"))
    south = np.array(M["southern"])
    one = np.ones_like(rate)
    b1, s1 = _ols(np.column_stack([one, conv, exe]), rate)
    b2, s2 = _ols(np.column_stack([one, conv, exe, south, np.array(M["income"]), np.array(M["noncauc"])]), rate)
    return {"rate": rate.tolist(), "convictions": conv.tolist(), "executions": exe.tolist(), "south": south.tolist(),
            "simple": {"conv": float(b1[1]), "conv_se": float(s1[1]), "exe": float(b1[2]), "exe_se": float(s1[2])},
            "controls": {"conv": float(b2[1]), "conv_se": float(s2[1]), "exe": float(b2[2]), "exe_se": float(s2[2])},
            "mean_south": float(rate[south == 1].mean()), "mean_north": float(rate[south == 0].mean()),
            "n": int(len(rate))}


def _annual(series):
    d = data.fred(series)
    out = {}
    for t, v in zip(d["date"], d["value"]):
        if v == v:
            out.setdefault(int(t[:4]), []).append(v)
    ys = sorted(y for y, v in out.items() if len(v) == 12)
    return ys, [float(np.mean(out[y])) for y in ys]


def compute_participation() -> dict:
    yw, w = _annual("LNS11300002")
    ym, m = _annual("LNS11300001")
    return {"year": yw, "women": w, "men": m, "w_first": w[0], "w_last": w[-1], "m_first": m[0], "m_last": m[-1],
            "w_peak": max(w), "w_peak_year": yw[int(np.argmax(w))], "first_year": yw[0], "last_year": yw[-1]}


def compute_household() -> dict:
    H = TRUTH["household"]
    w2 = np.round(np.linspace(0.3, 1.6, 27), 3)
    rows = [fm.household_time(H["w1"], float(w), H["h1"], H["h2"], H["alpha"]) for w in w2]
    return {"w2": w2.tolist(), "market1": [r["market1"] for r in rows], "market2": [r["market2"] for r in rows],
            "home1": [r["t1"] for r in rows], "home2": [r["t2"] for r in rows], **H,
            "ratio_switch": H["h2"] / H["h1"]}


def compute_marriage() -> dict:
    M = TRUTH["marriage"]
    phi = np.array(M["phi"])
    eq = fm.choo_siow(M["men"], M["women"], phi)
    smp = fm.draw_market(M["men"], M["women"], phi, seed=M["seed"])
    rand = np.outer(np.array(M["men"]) / sum(M["men"]), np.array(M["women"]) / sum(M["women"]))
    more_men = fm.choo_siow([int(1.2 * x) for x in M["men"]], M["women"], phi)
    ed_women = fm.choo_siow(M["men"], (1800, 2600, 3400), phi)
    def degree(e, women):
        mu = np.array(e["mu"])
        return {"deg_women_single": e["single_women"][2] / women[2], "deg_women_with_deg": mu[2, 2] / women[2],
                "deg_women_down": (mu[0, 2] + mu[1, 2]) / women[2]}

    return {"men": list(M["men"]), "women": list(M["women"]), "phi": phi.tolist(), "eq": eq, "sample": smp,
            "deg_base": degree(eq, M["women"]), "deg_ed": degree(ed_women, (1800, 2600, 3400)),
            "sorting": fm.sorting_index(eq["mu"]), "random_diag": float(np.trace(rand)),
            "more_men": more_men, "ed_women": ed_women, "ed_women_counts": [1800, 2600, 3400]}


def compute_fertility() -> dict:
    out = {}
    for e in ("World", "China", "South Korea", "India", "United States", "Japan"):
        d = data.longrun("children-born-per-woman", e)
        keep = [i for i, y in enumerate(d["year"]) if y >= 1950]
        out[e] = {"year": [d["year"][i] for i in keep], "value": [d["value"][i] for i in keep]}
    ch = out["China"]
    yy, vv = np.array(ch["year"]), np.array(ch["value"])
    return {"series": out, "china_1970": float(vv[yy == 1970][0]), "china_1979": float(vv[yy == 1979][0]),
            "china_last": float(vv[-1]), "korea_last": float(out["South Korea"]["value"][-1]),
            "world_first": float(out["World"]["value"][0]), "world_last": float(out["World"]["value"][-1]),
            "last_year": int(yy[-1])}


def compute_qq() -> dict:
    C = TRUTH["children"]
    ws = np.linspace(0.1, 3.0, 30)
    rows = [fm.quantity_quality(C["income"], float(w), C["time"], C["goods"], C["a"], C["b"]) for w in ws]
    return {"wage": ws.tolist(), "n": [r["n"] for r in rows], "q": [r["q"] for r in rows],
            "price": [r["price_child"] for r in rows], **C}


def compute_angrist() -> dict:
    F = data.fertility()
    b1, b2, more, work = (np.array(F[k]) for k in ("boy1", "boy2", "morekids", "work"))
    same = (b1 == b2).astype(float)
    w = fm.wald(same, more, work)
    worked = (work > 0).astype(float)
    w2 = fm.wald(same, more, worked)
    X = np.column_stack([np.ones_like(work), more])
    ols, ols_se = _ols(X, work)
    by = {}
    for name, k in (("two boys", (b1 == 1) & (b2 == 1)), ("two girls", (b1 == 0) & (b2 == 0)),
                    ("a boy and a girl", b1 != b2)):
        by[name] = {"n": int(k.sum()), "third": float(more[k].mean())}
    return {"wald": w, "wald_any": w2, "ols": float(ols[1]), "ols_se": float(ols_se[1]), "by": by,
            "mean_work": float(work.mean()), "share_third": float(more.mean()), "n": int(len(work))}


def compute_bargain() -> dict:
    B = TRUTH["bargain"]
    share = np.linspace(0.0, 1.0, 41)
    col = [fm.collective(1 - s, s, B["child_taste"], B["slope"]) for s in share]
    uni = [fm.collective(1 - s, s, B["child_taste"], B["slope"], unitary=True) for s in share]
    # the reform: a benefit of 0.1 of income moves from the father's pay to the mother's purse at a share of 0.3
    before = fm.collective(0.7 + 0.1, 0.3, B["child_taste"], B["slope"])
    after = fm.collective(0.7, 0.3 + 0.1, B["child_taste"], B["slope"])
    return {"share": share.tolist(), "child_col": [c["child"] for c in col], "child_uni": [c["child"] for c in uni],
            "lambda": [c["lambda"] for c in col], "before": before, "after": after,
            "rise": after["child"] / before["child"] - 1, **B}


def _pct(x, ref):
    ref = np.sort(ref)
    return 100.0 * np.searchsorted(ref, x, side="right") / len(ref)


def _within(y, X, g):
    """OLS of y on X after removing group means, errors clustered by group."""
    Xd, yd = X.copy(), y.copy()
    for c in np.unique(g):
        k = g == c
        Xd[k] -= X[k].mean(0)
        yd[k] -= y[k].mean()
    return _ols(Xd, yd, cluster=g)


def compute_star() -> dict:
    S = data.star()
    st, r, m, sch = (np.array(S[k]) for k in ("stark", "readk", "mathk", "schoolidk"))
    ok = (st != "") & np.isfinite(r) & np.isfinite(m)
    reg = ok & (st != "small")
    pr, pm = _pct(r, r[reg]), _pct(m, m[reg])
    p = (pr + pm) / 2
    idx = np.where(ok)[0]
    X = np.column_stack([(st[idx] == "small"), (st[idx] == "regular+aide")]).astype(float)
    b, se = _within(p[idx], X, sch[idx])
    means = {t: float(p[ok & (st == t)].mean()) for t in ("small", "regular", "regular+aide")}
    # by free-lunch status and by race
    lunch, eth = np.array(S["lunchk"]), np.array(S["ethnicity"])
    sub = {}
    for name, k in (("free lunch", lunch == "free"), ("no free lunch", lunch == "non-free"),
                    ("black pupils", eth == "afam"), ("white pupils", eth == "cauc")):
        kk = ok & k
        ii = np.where(kk)[0]
        Xs = np.column_stack([(st[ii] == "small"), (st[ii] == "regular+aide")]).astype(float)
        bb, ss = _within(p[ii], Xs, sch[ii])
        sub[name] = {"small": float(bb[0]), "se": float(ss[0]), "n": int(kk.sum())}
    # grade 3, by the class type in grade 3 (no school identifier kept for grade 3: raw differences)
    s3, r3, m3 = (np.array(S[k]) for k in ("star3", "read3", "math3"))
    ok3 = (s3 != "") & np.isfinite(r3) & np.isfinite(m3)
    reg3 = ok3 & (s3 != "small")
    p3 = (_pct(r3, r3[reg3]) + _pct(m3, m3[reg3])) / 2
    g3 = {t: float(p3[ok3 & (s3 == t)].mean()) for t in ("small", "regular", "regular+aide")}
    # the distributions, for drawing: percentiles of small and regular kindergarten classes
    qs = np.linspace(0.02, 0.98, 49)
    return {"n": int(ok.sum()), "schools": int(len(np.unique(sch[idx]))), "small": float(b[0]),
            "small_se": float(se[0]), "aide": float(b[1]), "aide_se": float(se[1]), "means": means, "sub": sub,
            "g3": g3,
            "g3_diff": g3["small"] - g3["regular"], "n3": int(ok3.sum()),
            "q_small": np.quantile(p[ok & (st == "small")], qs).tolist(),
            "q_regular": np.quantile(p[ok & (st == "regular")], qs).tolist(), "qs": qs.tolist()}


def compute_caschools() -> dict:
    C = data.caschools()
    str_ = np.array(C["students"]) / np.array(C["teachers"])
    sc = (np.array(C["read"]) + np.array(C["math"])) / 2
    one = np.ones_like(sc)
    b1, s1 = _ols(np.column_stack([one, str_]), sc)
    b2, s2 = _ols(np.column_stack([one, str_, np.array(C["english"]), np.array(C["lunch"])]), sc)
    return {"str": str_.tolist(), "score": sc.tolist(), "english": C["english"], "lunch": C["lunch"],
            "naive": float(b1[1]), "naive_se": float(s1[1]), "naive_a": float(b1[0]), "controls": float(b2[1]),
            "controls_se": float(s2[1]), "sd": float(sc.std()), "n": int(len(sc))}


def compute_maimonides() -> dict:
    M = TRUTH["maimonides"]
    base = fm.maimonides_study(**M)
    sort = fm.maimonides_study(**M, sorting=0.6)
    e = np.arange(1, 161)
    return {"rule_e": e.tolist(), "rule": fm.maimonides(e, M["cap"]).tolist(), "effect": M["effect"],
            "naive": base["naive"], "iv": base["iv"], "iv_se": base["iv_se"], "sorted_iv": sort["iv"],
            "sorted_iv_se": sort["iv_se"], "enrolment": base["enrolment"], "class_size": base["class_size"],
            "score": base["score"], "enrolment_sorted": sort["enrolment"]}


def compute_teachers() -> dict:
    T = TRUTH["teachers"]
    a = fm.teacher_va(**T)
    b = fm.teacher_va(**T, sorting=1.0)
    keep = ("sd_true", "sd_raw", "sd_shrunk", "reliability", "forecast_coef", "forecast_se", "corr_raw")
    return {"clean": {**{k: a[k] for k in keep}, "true": a["true"][:300], "raw": a["raw"][:300],
                      "shrunk": a["shrunk"][:300], "d_va": a["d_va"], "d_score": a["d_score"]},
            "sorted": {**{k: b[k] for k in keep}, "d_va": b["d_va"], "d_score": b["d_score"]}, **T}


def compute_grossman() -> dict:
    G = TRUTH["grossman"]
    ages = np.arange(20, 111)
    base = fm.grossman(ages, **G)
    richer = fm.grossman(ages, **{**G, "a": G["a"] * 1.25})      # more productive at making health (education)
    return {"base": base, "educated": richer, **G}


def _poisson(X, y, iters=50):
    b = np.zeros(X.shape[1])
    b[0] = np.log(y.mean())
    for _ in range(iters):
        mu = np.exp(X @ b)
        step = np.linalg.solve(X.T @ (X * mu[:, None]), X.T @ (y - mu))
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    mu = np.exp(X @ b)
    A = np.linalg.inv(X.T @ (X * mu[:, None]))
    meat = (X * ((y - mu) ** 2)[:, None]).T @ X
    V = A @ meat @ A                                            # robust (sandwich)
    return b, np.sqrt(np.diag(V))


def compute_doctors() -> dict:
    D = data.doctor_visits()
    y = np.array(D["visits"])
    names = ("private", "freepoor", "freerepat", "illness", "reduced", "health", "female", "age", "income", "nchronic",
             "lchronic")
    X = np.column_stack([np.ones_like(y)] + [np.array(D[k]) for k in names] + [np.array(D["age"]) ** 2])
    b, se = _poisson(X, y)
    rr = {k: float(np.exp(b[i + 1])) for i, k in enumerate(names)}
    lo = {k: float(np.exp(b[i + 1] - 1.96 * se[i + 1])) for i, k in enumerate(names)}
    hi = {k: float(np.exp(b[i + 1] + 1.96 * se[i + 1])) for i, k in enumerate(names)}
    ins = {}
    priv, poor, rep = (np.array(D[k]) for k in ("private", "freepoor", "freerepat"))
    groups = {"private insurance": priv == 1, "free (low income)": poor == 1, "free (age or service)": rep == 1,
              "basic public cover only": (priv == 0) & (poor == 0) & (rep == 0)}
    for k, m in groups.items():
        ins[k] = {"n": int(m.sum()), "visits": float(y[m].mean()), "illness": float(np.array(D["illness"])[m].mean()),
                  "age": float(100 * np.array(D["age"])[m].mean())}
    return {"rr": rr, "lo": lo, "hi": hi, "groups": ins, "n": int(len(y)), "mean": float(y.mean()),
            "zero": float(np.mean(y == 0))}


def compute_drug() -> dict:
    """A patented drug on the Island: linear demand q = A - p, marginal cost c; the monopoly price under the patent
    against the price once generics enter, and what each side of the trade is worth."""
    D = TRUTH["drug"]
    A, c = D["A"], D["cost"]
    pm = (A + c) / 2
    qm, qc = A - pm, A - c
    return {**D, "p_mono": pm, "q_mono": qm, "q_comp": qc, "profit": (pm - c) * qm, "dwl": 0.5 * (pm - c) * (qc - qm),
            "cs_mono": 0.5 * (A - pm) * qm, "cs_comp": 0.5 * (A - c) * qc,
            "years_profit": D["patent_years"] * (pm - c) * qm}


def compute_cigarettes() -> dict:
    C = data.cigarettes()
    yr = np.array(C["year"])
    cpi = np.array(C["cpi"])
    packs = np.array(C["packs"])
    price = np.array(C["price"]) / cpi
    inc = np.array(C["income"]) / np.array(C["population"]) / cpi
    salestax = (np.array(C["taxs"]) - np.array(C["tax"])) / cpi
    cigtax = np.array(C["tax"]) / cpi
    k95, k85 = yr == 1995, yr == 1985
    one = np.ones(k95.sum())

    def tsls(y, x, z, w):
        Z = np.column_stack([one, *w, *z])
        xh = Z @ np.linalg.lstsq(Z, x, rcond=None)[0]
        X = np.column_stack([one, xh, *w])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - np.column_stack([one, x, *w]) @ b
        XtX = np.linalg.inv(X.T @ X)
        V = XtX @ ((X * e[:, None] ** 2).T @ X) @ XtX * len(y) / (len(y) - X.shape[1])
        # first-stage F for the excluded instruments
        Zr = np.column_stack([one, *w])
        rss_r = np.sum((x - Zr @ np.linalg.lstsq(Zr, x, rcond=None)[0]) ** 2)
        rss_u = np.sum((x - xh) ** 2)
        F = ((rss_r - rss_u) / len(z)) / (rss_u / (len(y) - Z.shape[1]))
        return float(b[1]), float(np.sqrt(V[1, 1])), float(F)

    lq, lp, li = np.log(packs[k95]), np.log(price[k95]), np.log(inc[k95])
    ols_b, ols_se = _ols(np.column_stack([one, lp]), lq)
    cross = tsls(lq, lp, [salestax[k95]], [])
    cross_inc = tsls(lq, lp, [salestax[k95]], [li])
    # ten-year differences, states matched by name
    s95, s85 = np.array(C["state"])[k95], np.array(C["state"])[k85]
    o85 = np.array([np.where(s85 == s)[0][0] for s in s95])
    dq = lq - np.log(packs[k85][o85])
    dp = lp - np.log(price[k85][o85])
    di = li - np.log(inc[k85][o85])
    dst = salestax[k95] - salestax[k85][o85]
    dct = cigtax[k95] - cigtax[k85][o85]
    d1 = tsls(dq, dp, [dst], [di])
    d2 = tsls(dq, dp, [dct], [di])
    d3 = tsls(dq, dp, [dst, dct], [di])
    return {"lp": lp.tolist(), "lq": lq.tolist(), "states": s95.tolist(), "ols": float(ols_b[1]),
            "ols_se": float(ols_se[1]), "cross": cross, "cross_inc": cross_inc, "diff_sales": d1, "diff_cig": d2,
            "diff_both": d3, "dp": dp.tolist(), "dq": dq.tolist(), "packs85": float(packs[k85].mean()),
            "packs95": float(packs[k95].mean())}


def compute_addiction() -> dict:
    A = TRUTH["addiction"]
    r = fm.addiction_path(**A, rational=True)
    m = fm.addiction_path(**A, rational=False)
    T = 40
    i0, i1 = A["announce_at"], A["rise_at"]
    return {"t": r["t"][:T], "price": r["price"][:T], "rational": r["consumption"][:T], "myopic": m["consumption"][:T],
            "rational_stock": r["stock"][:T], "myopic_stock": m["stock"][:T], **A,
            "rational_drop_before": r["consumption"][i1 - 1] / max(r["consumption"][i0 - 1], 1e-9) - 1,
            "myopic_drop_before": m["consumption"][i1 - 1] / max(m["consumption"][i0 - 1], 1e-9) - 1,
            "rational_after": r["consumption"][i1 + 10] / r["consumption"][i0 - 1] - 1,
            "myopic_after": m["consumption"][i1 + 10] / m["consumption"][i1 - 1] - 1}


def film_time(t: float, first: float = 1950.0, last: float = 2023.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    w = data.longrun("children-born-per-woman", "World")
    ys = [y for y in w["year"] if y >= 1950]
    vs = [v for y, v in zip(w["year"], w["value"]) if y >= 1950]
    k = int(np.argmax(vs))
    return {"t": ys, "v": vs, "times": [film_time(t) for t in ys], "first": vs[0], "last": vs[-1], "peak": vs[k],
            "peak_t": ys[k], "v1980": vs[ys.index(1980)], "v2000": vs[ys.index(2000)]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=9, log=False, low=40, high=84)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0], "peak": film_time(f["peak_t"]),
              "y1980": film_time(1980), "y2000": film_time(2000)}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.3, "hz": score.hz(nn), "name": f"{x:.2f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the world's children per woman, 1950-2023 (UN WPP via Our World in Data), as a tune "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ49").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "offenders": compute_offenders,
    "deterrence": compute_deterrence,
    "planner": compute_planner,
    "police": compute_police,
    "murder": compute_murder,
    "participation": compute_participation,
    "household": compute_household,
    "marriage": compute_marriage,
    "fertility": compute_fertility,
    "qq": compute_qq,
    "angrist": compute_angrist,
    "bargain": compute_bargain,
    "star": compute_star,
    "caschools": compute_caschools,
    "maimonides": compute_maimonides,
    "teachers": compute_teachers,
    "grossman": compute_grossman,
    "doctors": compute_doctors,
    "drug": compute_drug,
    "cigarettes": compute_cigarettes,
    "addiction": compute_addiction,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

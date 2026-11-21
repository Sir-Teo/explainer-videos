"""Precompute every number in Part 53 of *Economics, Built* ("Information and Persuasion").

    python -m videos.economics.econ53.compute            # everything missing (under a minute)
    python -m videos.economics.econ53.compute --force prosecutor

Results are cached in ``.cache/econ53/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models: Agora's
information and persuasion (``agora.persuade``) with the Island's Part 53 truths.  Data: the University of
Michigan's median expected inflation and the CPI, via FRED, for the intermission.

Items:
    prosecutor  the prosecutor's arithmetic; conviction as the investigation varies
    concav      the sender's value over the judge's belief and its concave closure; three verdicts; three states
    cheap       Crawford and Sobel's partitions at four biases; the most informative equilibrium by bias
    bayes       a Cournot duopoly with a rival of unknown cost: Bayes-Nash against full information
    beer        the beer-quiche game: two pooling equilibria and the intuitive criterion
    design      two investors and a designer: no information, full information, the best Bayes correlated
                equilibrium
    blackwell   three experiments: a garbling, a pair that cannot be ranked, values in decision problems
    agree       Geanakoplos and Polemarchakis's dialogue; the email game
    global      the regime-change threshold with a flat prior and with public information of rising precision
    cascade     cascades exactly and by simulation; accuracy by signal quality
    chain       Kreps and Wilson's chain store
    bargain     Rubinstein's split by patience; Nash on a frontier; a seller who cannot commit
    relational  Levin's relational contract: effort by discount factor
    film        the intermission's data film: expected against actual inflation, 1978-2026
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import persuade as P

CACHE = Cache("econ53")
load = CACHE.load
TRUTH = island.truths(53)
FILM_SECONDS = 46.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def compute_prosecutor() -> dict:
    T = TRUTH["prosecutor"]
    r = P.prosecutor(T["prior"], T["threshold"])
    pr, th = T["prior"], T["threshold"]
    ps = np.linspace(0, 1, 201)
    post = pr / (pr + (1 - pr) * ps)
    conv = np.where(post >= th - 1e-12, pr + (1 - pr) * ps, 0.0)
    return {**{k: v for k, v in r.items() if k != "signal"}, "p_innocent": r["signal"]["innocent"][0],
            "ps": ps.tolist(), "posterior": post.tolist(), "convict": conv.tolist(),
            "innocent_share": float(r["innocent_convicted"] / r["optimal"])}


def compute_concav() -> dict:
    T = TRUTH["prosecutor"]
    mu = np.linspace(0, 1, 401)
    v = (mu >= T["threshold"] - 1e-12).astype(float)
    cv = P.concavify(mu, v)
    V = TRUTH["verdicts"]
    v3 = np.select([mu < V["thresholds"][0], mu < V["thresholds"][1]], [V["values"][0], V["values"][1]],
                   V["values"][2])
    cv3 = P.concavify(mu, v3)
    G = P.simplex_grid(3, 30)
    vals = (G[:, 0] >= 0.5).astype(float)
    lp = P.persuade_lp([0.2, 0.3, 0.5], G, vals)
    return {"mu": mu.tolist(), "v": v.tolist(), "cv": cv.tolist(), "v3": v3.tolist(), "cv3": cv3.tolist(),
            "at_prior": float(np.interp(T["prior"], mu, cv)), "at_prior3": float(np.interp(T["prior"], mu, cv3)),
            "three": {"value": lp["value"], "posteriors": lp["posteriors"].tolist(), "weights": lp["weights"].tolist()}}


def compute_cheap() -> dict:
    rows = []
    for b in TRUTH["biases"]:
        r = P.cheap_talk(b)
        rows.append({"b": b, "N": r["N"], "bounds": r["bounds"].tolist(), "actions": r["actions"].tolist(),
                     "receiver_loss": r["receiver_loss"], "sender_loss": r["sender_loss"]})
    bs = np.linspace(0.005, 0.3, 120)
    best = [P.cheap_talk(float(b)) for b in bs]
    return {"rows": rows, "bs": bs.tolist(), "N": [r["N"] for r in best],
            "loss": [r["receiver_loss"] for r in best], "babbling": 1 / 12}


def compute_bayes() -> dict:
    C = TRUTH["cournot"]
    a, c1, ch, cl, ph = C["a"], C["c1"], C["c_high"], C["c_low"], C["p_high"]
    ec = ph * ch + (1 - ph) * cl
    q1 = (a - 2 * c1 + ec) / 3
    q2 = {k: (a - c - q1) / 2 for k, c in (("high", ch), ("low", cl))}
    full = {}
    for k, c in (("high", ch), ("low", cl)):
        f1 = (a - 2 * c1 + c) / 3
        f2 = (a - 2 * c + c1) / 3
        full[k] = {"q1": f1, "q2": f2}

    def profit(q, qo, c):
        return (a - q - qo - c) * q

    exp_profit1 = ph * profit(q1, q2["high"], c1) + (1 - ph) * profit(q1, q2["low"], c1)
    full_profit1 = ph * profit(full["high"]["q1"], full["high"]["q2"], c1) + (1 - ph) * profit(
        full["low"]["q1"], full["low"]["q2"], c1)
    return {"a": a, "c1": c1, "c_high": ch, "c_low": cl, "p_high": ph, "q1": q1, "q2": q2, "full": full,
            "profit1": exp_profit1, "full_profit1": full_profit1}


def compute_beer() -> dict:
    B = TRUTH["beer"]
    ps, br, du = B["p_strong"], B["breakfast"], B["duel"]
    prior = {"strong": ps, "weak": 1 - ps}

    def payoff(t, meal, duel):
        pref = "beer" if t == "strong" else "quiche"
        return (br if meal == pref else 0.0) + (0.0 if duel else du)

    def duels(types):
        w = sum(prior[t] for t in types if t == "weak")
        tot = sum(prior[t] for t in types)
        return w / tot > 0.5

    out = {}
    for pool, off in (("beer", "quiche"), ("quiche", "beer")):
        on_duel = duels(("strong", "weak"))
        eq_pay = {t: payoff(t, pool, on_duel) for t in prior}
        dev_best = {t: payoff(t, off, False) for t in prior}
        sustained = all(payoff(t, off, True) <= eq_pay[t] for t in prior)
        could_gain = [t for t in prior if dev_best[t] > eq_pay[t]]
        if could_gain and len(could_gain) < len(prior):
            response_duel = duels(could_gain)
            breaks = any(payoff(t, off, response_duel) > eq_pay[t] for t in could_gain)
        else:
            response_duel, breaks = None, False
        out[pool] = {"equilibrium": bool(sustained), "payoffs": eq_pay, "deviation_best": dev_best,
                     "could_gain": could_gain, "response_duel": response_duel, "survives_intuitive": not breaks}
    return {"p_strong": ps, "breakfast": br, "duel": du, "pools": out}


def _invest_game():
    I = TRUTH["invest"]

    def U(th):
        U0 = np.array([[0.0, 0.0], [th, th + I["together"]]])
        return U0, U0.T.copy()

    (U0g, U1g), (U0b, U1b) = U(I["good"]), U(I["bad"])
    return I, [[U0g, U0b], [U1g, U1b]]


def compute_design() -> dict:
    I, pay = _invest_game()
    pg = I["p_good"]
    obj = [np.array([[0.0, 1.0], [1.0, 2.0]])] * 2
    best = P.bce_lp([pg, 1 - pg], pay, obj)
    full = 2 * pg
    pool_both = pg * (I["good"] + I["together"]) + (1 - pg) * (I["bad"] + I["together"])
    none = 2.0 if pool_both >= 0 else 0.0
    s = best["sigma"]
    return {"p_good": pg, "best": best["value"], "full": full, "none": none, "pool_payoff": pool_both,
            "recommend_bad": float(s[1, 1, 1]), "recommend_good": float(s[0, 1, 1]), "sigma": s,
            "good": I["good"], "bad": I["bad"], "together": I["together"]}


def compute_blackwell() -> dict:
    E = TRUTH["experiments"]
    Pm = np.array(E["P"])
    Q = Pm @ np.array(E["garble"])
    R = np.array(E["R"])
    prior = [0.5, 0.5]
    thresholds = np.linspace(0.02, 0.98, 49)
    vals = {"P": [], "Q": [], "R": []}
    for k in thresholds:
        U = np.array([[0.0, 1 - k], [0.0, -k]])
        for name, X in (("P", Pm), ("Q", Q), ("R", R)):
            vals[name].append(P.decision_value(prior, X, U) - P.decision_value(prior, np.ones((2, 1)), U))
    return {"P": Pm.tolist(), "Q": Q.tolist(), "R": R.tolist(), "garble": E["garble"],
            "PQ": P.garbling(Pm, Q)["garbling"], "QP": P.garbling(Q, Pm)["garbling"],
            "PR": P.garbling(Pm, R)["garbling"], "RP": P.garbling(R, Pm)["garbling"],
            "thresholds": thresholds.tolist(), "values": vals}


def compute_agree() -> dict:
    D = TRUTH["dialogue"]
    prior = [1 / D["n"]] * D["n"]
    r = P.dialogue(prior, list(D["event"]), [list(c) for c in D["a"]], [list(c) for c in D["b"]], D["state"])
    E = TRUTH["email"]
    em = P.email_game(E["eps"], E["p"], E["a"], E["L"])
    eps = np.linspace(0.01, 0.5, 50)
    return {"history": r["history"], "agreed": r["agreed"], "email": em, "eps": eps.tolist(),
            "z": [1 / (2 - e) for e in eps], "dialogue": {k: [list(c) for c in v] if k in ("a", "b") else v
                                                          for k, v in D.items()}}


def compute_global() -> dict:
    G = TRUTH["global"]
    flat = P.global_game(G["c"], G["sigma"])
    rows = [P.global_game(G["c"], G["sigma"], G["prior_mean"], sd) | {"prior_sd": sd} for sd in G["prior_sds"]]
    th = np.linspace(0.001, 0.999, 400)
    curves = []
    for sd in G["prior_sds"]:
        alpha, beta = 1 / sd ** 2, 1 / G["sigma"] ** 2
        from scipy.stats import norm
        lhs = alpha * (th - G["prior_mean"]) - np.sqrt(beta) * norm.ppf(th)
        curves.append({"prior_sd": sd, "lhs": lhs.tolist(), "rhs": float(np.sqrt(alpha + beta) * norm.ppf(G["c"]))})
    return {"flat": flat, "rows": rows, "theta": th.tolist(), "curves": curves, "c": G["c"], "sigma": G["sigma"]}


def compute_cascade() -> dict:
    C = TRUTH["cascade"]
    ch = P.cascade_chain(C["q"], C["n"])
    sim = P.cascade_sim(C["q"], C["n"], C["runs"], C["seed"])
    qs = np.linspace(0.51, 0.95, 45)
    right = [P.cascade_chain(float(q), 200)["limit_right"] for q in qs]
    return {**ch, "q": C["q"], "n": C["n"], "share_right": sim["share_right"], "examples": sim["examples"],
            "qs": qs.tolist(), "right_by_q": right}


def compute_chain() -> dict:
    C = TRUTH["chain"]
    return P.chain_store(C["n"], C["delta"], C["b"], C["a"])


def compute_bargain() -> dict:
    B = TRUTH["bargain"]
    rub = [{"delta": d, **P.rubinstein(d)} for d in B["deltas"]]
    x = np.linspace(0, 1, 401)
    y = np.sqrt(1 - x ** 2)
    nb = P.nash_bargaining(x, y)
    co = P.coase_two_period(B["v_high"], B["v_low"], B["share_high"], B["delta"])
    return {"rubinstein": rub, "frontier_x": x.tolist(), "frontier_y": y.tolist(), "nash": nb, "coase": co,
            **{k: B[k] for k in ("v_high", "v_low", "share_high", "delta")}}


def compute_relational() -> dict:
    R = TRUTH["relational"]
    ds = np.linspace(0.05, 0.95, 91)
    r = P.relational(ds, R["theta"], R["c"])
    return {**r, **R}


def _yoy(series):
    s = data.fred(series)
    d = dict(zip(s["date"], s["value"]))
    out = {}
    for k, v in d.items():
        prev = f"{int(k[:4]) - 1}{k[4:]}"
        if prev in d and np.isfinite(v) and np.isfinite(d[prev]):
            out[k] = 100 * (v / d[prev] - 1)
    return out


def film_time(t: float, first: float = 1978.0, last: float = 2026.75) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    m = data.fred("MICH")
    mich = {d: v for d, v in zip(m["date"], m["value"]) if np.isfinite(v)}
    inf = _yoy("CPIAUCSL")
    ds = sorted(d for d in mich if d in inf)
    t = [int(d[:4]) + (int(d[5:7]) - 1) / 12 for d in ds]
    exp_ = [mich[d] for d in ds]
    act = [inf[d] for d in ds]
    # what happened over the following twelve months, where known
    ahead = []
    for d in ds:
        nd = f"{int(d[:4]) + 1}{d[4:]}"
        ahead.append(inf.get(nd, float("nan")))
    pairs = [(e, a) for e, a in zip(exp_, ahead) if np.isfinite(a)]
    err = np.array([e - a for e, a in pairs])
    return {"t": t, "expected": exp_, "actual": act, "ahead": ahead, "times": [film_time(x) for x in t],
            "first": ds[0], "last": ds[-1], "mean_error": float(err.mean()), "mae": float(np.abs(err).mean()),
            "peak_expected": float(max(exp_)), "peak_expected_t": t[int(np.argmax(exp_))],
            "peak_actual": float(max(act)), "peak_actual_t": t[int(np.argmax(act))]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["expected"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=10, log=False, low=45, high=84)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.15, "hz": score.hz(nn), "name": f"{x:.1f}%"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the median household's expected inflation for the year ahead, 1978-2026 (University "
                               "of Michigan, via FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ53").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "prosecutor": compute_prosecutor,
    "concav": compute_concav,
    "cheap": compute_cheap,
    "bayes": compute_bayes,
    "beer": compute_beer,
    "design": compute_design,
    "blackwell": compute_blackwell,
    "agree": compute_agree,
    "global": compute_global,
    "cascade": compute_cascade,
    "chain": compute_chain,
    "bargain": compute_bargain,
    "relational": compute_relational,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

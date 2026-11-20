"""Precompute every number in Part 45 of *Economics, Built* ("Behavioural Economics").

    python -m videos.economics.econ45.compute            # everything missing (about two minutes)
    python -m videos.economics.econ45.compute --force gym

Results are cached in ``.cache/econ45/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: FRED's personal saving rate; the tables of DellaVigna and Malmendier, Kahneman,
Knetsch and Thaler, List, the field studies of reference dependence, Laibson and O'Donoghue and Rabin, Ashraf,
Karlan and Yin, Madrian and Shea and Thaler and Benartzi, Gabaix and Laibson and Lacetera, Pope and Sydnor, Fehr and
Schmidt, Gneezy and List and List, Bernheim and Rangel, DellaVigna and Linos, Sims, Gabaix and Bordalo, Gennaioli,
Ma and Shleifer) and *Psychology, Built*'s Archive (choices13k, Peterson et al. 2021, fetched on first use).  Models:
Agora's behavioural economics (``agora.behave``) with the Island's Part 45 truths.

Items:
    gym          the Island's gym: who picks which contract, forecast against actual visits, the price per visit
    contract     the contract a gym designs for present-biased members: monopoly and free entry, naif and sophisticate
    disclose     a disclosure rule at the gym: choices and realized gains as more naifs heed it
    mugs         the mug market with and without loss aversion: asks, bids, the volume of trade
    experience   the share of goods traded as traders gain experience
    marathon     finishing times bunched under round numbers; excess and missing mass at each half hour
    golf         putts for par and for birdie: the raw gap and the gap at equal distance
    condos       loss-averse sellers after a fall in prices: the two bounds, markups and time on the market
    odr          a report and a film: when the time-consistent, the naif and the sophisticate act
    seed         a randomized offer of a commitment savings account: take-up, ITT, TOT, who takes it
    enrol        opt-in against automatic enrolment, for naifs and for the time-consistent; Save More Tomorrow
    shrouded     shrouded add-on prices in a competitive market
    cars         left-digit bias in wholesale car prices, and its estimate
    ri           rational inattention: choice rules as attention gets dearer
    social       Fehr-Schmidt players: ultimatum thresholds, offers, the acceptance curve; gift exchange
    nudges       a literature of nudge trials, published by significance, against a unit's full record; the
                 selection model's correction
    forecast     forecasters, rational and diagnostic: error-on-revision slopes, individual and consensus
    c13k         prospect theory fitted to choices13k's described problems (as in Psychology, Built, Part 26)
    film         the intermission's data film: the US personal saving rate, quarterly, 1959-2026
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import behave

CACHE = Cache("econ45")
load = CACHE.load
TRUTH = island.truths(45)
FILM_SECONDS = 52.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def compute_gym() -> dict:
    G = TRUTH["gym"]
    g = behave.island_gym(n=G["n"], fee=G["fee"], per_visit=G["per_visit"], N=G["N"], C=G["C"], b_mean=G["b_mean"],
                          b_sd=G["b_sd"], beta_lo=G["beta_lo"], beta_hi=G["beta_hi"], naive_share=G["naive_share"],
                          busy=G["busy"], seed=G["seed"])
    ch = np.array(g["choice"])
    v, f = np.array(g["visits"]), np.array(g["forecast"])
    naive = np.array(g["naive"])
    mon = ch == "monthly"
    rng = np.random.default_rng(G["seed"])
    pick = rng.choice(np.where(mon)[0], 120, replace=False)
    # a typical naive monthly member: the median forecast among naive monthly members
    nm = np.where(mon & naive)[0]
    i = nm[np.argsort(f[nm])[len(nm) // 2]]
    paid_pass = G["per_visit"] * v[mon]
    return {"share": g["share"], "visits": g["monthly_visits"], "forecast": g["monthly_forecast"],
            "price_per_visit": g["price_per_visit"], "naive_share": g["monthly_naive_share"],
            "regret_share": g["regret_share"], "fee": G["fee"], "per_visit": G["per_visit"],
            "sample_forecast": f[pick].tolist(), "sample_visits": v[pick].tolist(),
            "pass_visits": float(v[ch == "pass"].mean()), "pass_forecast": float(f[ch == "pass"].mean()),
            "pass_naive_share": float(naive[ch == "pass"].mean()),
            "typical": {"forecast": float(f[i]), "visits": float(v[i]), "beta": float(g["beta"][i]),
                        "b": float(g["b"][i])},
            "would_pay_on_pass": float(paid_pass.mean()), "n": G["n"], "members_monthly": int(mon.sum()),
            "hist_visits": np.histogram(v[mon], bins=np.arange(0, 16, 1))[0].tolist(),
            "hist_forecast": np.histogram(f[mon], bins=np.arange(0, 26, 1))[0].tolist()}


def compute_contract() -> dict:
    G = TRUTH["gym"]
    beta, b, C, m = 0.7, G["b_mean"], G["C"], G["m"]
    out = {}
    for name, bh in (("naif", 1.0), ("soph", beta)):
        for market in ("monopoly", "competition"):
            out[f"{name}_{market}"] = behave.gym_contract(beta, bh, b, C, G["N"], m,
                                                          competitive=market == "competition")
    # the same member at a contract priced at cost: the time-consistent benchmark
    out["at_cost"] = behave.gym_member(beta, beta, b, C, G["N"], m)
    out["beta"], out["b"], out["m"] = beta, b, m
    return out


def compute_disclose() -> dict:
    """A disclosure rule on the Island: the gym must tell each would-be member how often members like them go.  A
    share ``heed`` of naive members believe it (their forecasts become right); the others ignore it.  Choices and
    realized monthly gains (long-run value of visits less what is paid), against the status quo."""
    G = TRUTH["gym"]
    rng = np.random.default_rng(G["seed"])
    n = G["n"]
    b = G["b_mean"] * np.exp(G["b_sd"] * rng.standard_normal(n) - G["b_sd"] ** 2 / 2)
    beta = rng.uniform(G["beta_lo"], G["beta_hi"], n)
    naive = rng.random(n) < G["naive_share"]
    out = {}
    for heed in (0.0, 0.5, 1.0):
        listen = naive & (rng.random(n) < heed)
        gains, monthly, regret = [], [], []
        for i in range(n):
            bh = beta[i] if (not naive[i] or listen[i]) else 1.0
            busy_hat = G["busy"] if (not naive[i] or listen[i]) else 0.0
            r = behave.gym_choice(beta[i], bh, b[i], G["C"], G["N"], G["fee"], G["per_visit"], G["busy"], busy_hat)
            gains.append(r["realized"][r["choice"]])
            monthly.append(r["choice"] == "monthly")
            regret.append(r["regret"])
        out[str(heed)] = {"gain": float(np.mean(gains)), "monthly": float(np.mean(monthly)),
                          "regret": float(np.mean(regret))}
    return out


def compute_mugs() -> dict:
    M = TRUTH["mugs"]
    plain = behave.mug_market(M["n"], 1.0, 1.0, M["mu"], M["sigma"], M["reps"], M["seed"])
    loss = behave.mug_market(M["n"], M["lam_goods"], 1.0, M["mu"], M["sigma"], M["reps"], M["seed"])
    # one session, for the picture: the ordered asks and bids
    rng = np.random.default_rng(M["seed"])
    k = M["n"] // 2
    v = np.exp(rng.normal(M["mu"], M["sigma"], M["n"]))
    ask = np.sort(M["lam_goods"] * v[:k])
    ask0 = np.sort(v[:k])
    bid = np.sort(v[k:2 * k])[::-1]
    return {"plain": plain, "loss": loss, "ask": ask.tolist(), "ask0": ask0.tolist(), "bid": bid.tolist(),
            "trades": int(np.sum(bid > ask)), "trades0": int(np.sum(bid > ask0)), "k": k, "n": M["n"],
            "lam": M["lam_goods"]}


def compute_experience() -> dict:
    E_ = TRUTH["experience"]
    return behave.experienced_traders(E_["trades"], E_["lam0"], E_["half_life"], reps=2000, seed=45)


def compute_marathon() -> dict:
    M = TRUTH["marathon"]
    r = behave.marathon(n=M["n"], k=M["k"], eta=M["eta"], lam=M["lam"], base=M["base"], friction=M["friction"],
                        seed=M["seed"])
    marks = (180.0, 210.0, 240.0, 270.0, 300.0, 330.0)
    b = {int(mk): behave.bunching_at(r["T"], mk) for mk in marks}
    one = b[240]
    return {"edges": r["edges"], "h": r["h"], "share_bunched": r["share_bunched"],
            "extra_minutes": r["extra_minutes"], "excess": {k: v["excess"] for k, v in b.items()},
            "missing": {k: v["missing"] for k, v in b.items()}, "mid240": one["mid"], "h240": one["h"],
            "cf240": one["cf"], "n": M["n"], "lam": M["lam"], "eta": M["eta"]}


def compute_golf() -> dict:
    G = TRUTH["golf"]
    return behave.golf(G["n"], G["effect"], G["seed"])


def compute_condos() -> dict:
    C = TRUTH["condos"]
    r = behave.condos(n=C["n"], m=C["m"], seed=C["seed"])
    loss = np.array(r.pop("loss"))
    mk = np.array(r.pop("markup"))
    bins = np.array([0.0, 1e-9, 0.05, 0.10, 0.15, 0.20, 0.30, 0.45])
    mids, means = [], []
    for lo, hi in zip(bins[:-1], bins[1:]):
        s = (loss >= lo) & (loss < hi)
        if s.sum() > 30:
            mids.append(float(loss[s].mean()))
            means.append(float(mk[s].mean()))
    r["bin_loss"], r["bin_markup"] = mids, means
    return r


def compute_odr() -> dict:
    O = TRUTH["odr"]
    return {"cost": behave.odr(O["values"], O["beta"], "cost"), "reward": behave.odr(O["values"], O["beta"], "reward")}


def compute_seed() -> dict:
    S = TRUTH["seed"]
    return behave.commitment_trial(n=S["n"], soph_share=S["soph_share"], flex_mean=S["flex_mean"],
                                   flex_sd=S["flex_sd"], seed=S["seed"])


def compute_enrol() -> dict:
    N = TRUTH["enrol"]
    out = {}
    for name, d in (("opt_in", 0.0), ("auto", N["auto"])):
        for who, naive in (("naif", True), ("tc", False)):
            r = behave.enrolment(n=N["n"], default=d, months=N["months"], beta=N["beta"], naive=naive,
                                 cost_mean=N["cost_mean"], seed=N["seed"])
            out[f"{name}_{who}"] = {"participation": r["participation"], "at_default": r["at_default"]}
    S = TRUTH["smart"]
    out["smart"] = behave.smart(start=S["start"], step=S["step"], cap=S["cap"], raises=S["raises"], beta=S["beta"],
                                lam=S["lam"], seed=45)
    out["months"] = N["months"]
    return out


def compute_shrouded() -> dict:
    return behave.shrouded(**TRUTH["shrouded"])


def compute_cars() -> dict:
    C = TRUTH["cars"]
    return behave.used_cars(n=C["n"], theta=C["theta"], seed=C["seed"])


def compute_ri() -> dict:
    xs = np.linspace(-1, 1, 41)
    prior = np.ones(41) / 41
    U = np.column_stack([np.zeros(41), xs])
    out = {"x": xs.tolist(), "curves": {}, "info": {}}
    for lam in (0.02, 0.1, 0.3, 1.0):
        r = behave.ri_choice(prior, U, lam)
        out["curves"][str(lam)] = r["cond"][:, 1].tolist()
        out["info"][str(lam)] = r["info"]
    # a skewed prior: the new product is usually worse; at a high attention cost it is never chosen
    prior2 = np.where(xs < 0.4, 0.95 / np.sum(xs < 0.4), 0.05 / np.sum(xs >= 0.4))
    skew = behave.ri_choice(prior2, U, 0.6)
    out["skew_pa"] = skew["pa"].tolist()
    out["sparse"] = behave.sparse_weights([4.0, 1.5, 1.0, 0.5, 0.2], 0.6).tolist()
    return out


def compute_social() -> dict:
    S = TRUTH["social"]
    rng = np.random.default_rng(S["seed"])
    alphas = rng.exponential(S["alpha_mean"], S["n"])
    betas = rng.uniform(0, S["beta_hi"], S["n"])
    u = behave.ultimatum(alphas, betas)
    offers = np.array(u["offers"])
    th = np.array(u["thresholds"])
    return {"s": u["s"], "accept": u["accept"], "mean_offer": float(offers.mean()),
            "share_half": float(np.mean(np.isclose(offers, 0.5))), "dictator_half": u["dictator_gives_half"],
            "offer_hist": np.histogram(offers, bins=np.linspace(0, 0.5, 11))[0].tolist(),
            "threshold_hist": np.histogram(th, bins=np.linspace(0, 0.5, 11))[0].tolist(),
            "reject_20": float(np.mean(th > 0.2)), "gift": behave.gift_exchange()}


def compute_nudges() -> dict:
    N = TRUTH["nudges"]
    j = behave.nudge_literature(N["k"], N["mu"], N["tau"], N["control"], *N["journal_n"], N["gamma"], N["seed"])
    u = behave.nudge_literature(N["k"] // 4, N["mu"], N["tau"], N["control"], *N["unit_n"], 1.0, N["seed"] + 1)
    pub = np.array(j["published"])
    x, se = np.array(j["x"]), np.array(j["se"])
    mle = behave.selection_mle(x[pub], se[pub])
    return {"journal": {"x": x[pub].tolist(), "se": se[pub].tolist(), "mean": float(x[pub].mean()),
                        "n": int(pub.sum()), "run": N["k"], "all_mean": j["mean_all"]},
            "unit": {"x": u["x"], "se": u["se"], "mean": u["mean_all"], "n": len(u["x"])},
            "mle": mle, "mu": N["mu"], "control": N["control"]}


def compute_forecast() -> dict:
    F = TRUTH["forecast"]
    kw = dict(T=F["T"], n=F["n"], rho=F["rho"], sd_signal=F["sd_signal"], seed=F["seed"])
    return {"rational": behave.forecasters(theta=0.0, **kw), "diagnostic": behave.forecasters(theta=F["theta"], **kw),
            "theta": F["theta"]}


def compute_c13k() -> dict:
    from explainer.psychology import opendata
    from explainer.psychology.psyche import choice as C

    d = opendata.choices13k()
    desc = np.where(~d["amb"] & ~d["feedback"])[0]
    A = C.pad([d["A"][i] for i in desc])
    B = C.pad([d["B"][i] for i in desc])
    fit = C.fit_model("cpt", A, B, d["b_rate"][desc])
    return {"params": fit["params"], "mse": fit["mse"], "n_problems": int(len(desc)),
            "n_choices": int(d["n"][desc].sum())}


def _quarterly(series: str) -> dict:
    d = data.fred(series)
    q: dict = {}
    for t, v in zip(d["date"], d["value"]):
        if np.isfinite(v):
            y, mo = int(t[:4]), int(t[5:7])
            q.setdefault(y + (mo - 1) // 3 / 4, []).append(v)
    return {k: float(np.mean(v)) for k, v in q.items() if len(v) == 3}


def film_time(t: float, first: float = 1959.0, last: float = 2026.5) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    q = _quarterly("PSAVERT")
    ts = sorted(q)
    v = [q[t] for t in ts]
    k, j = int(np.argmax(v)), int(np.argmin(v))
    sel = [x for t, x in zip(ts, v) if 1960 <= t < 1985]
    return {"t": ts, "v": v, "times": [film_time(t) for t in ts], "peak": v[k], "peak_t": ts[k], "low": v[j],
            "low_t": ts[j], "first": v[0], "last": v[-1], "mean_60_84": float(np.mean(sel))}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=9, log=False, low=40, high=84)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0], "peak": film_time(f["peak_t"]),
              "low": film_time(f["low_t"])}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.3, "hz": score.hz(nn), "name": f"{x:.1f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the US personal saving rate, quarterly averages, 1959-2026 (U.S. Bureau of "
                               "Economic Analysis, via FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ45").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "gym": compute_gym,
    "contract": compute_contract,
    "disclose": compute_disclose,
    "mugs": compute_mugs,
    "experience": compute_experience,
    "marathon": compute_marathon,
    "golf": compute_golf,
    "condos": compute_condos,
    "odr": compute_odr,
    "seed": compute_seed,
    "enrol": compute_enrol,
    "shrouded": compute_shrouded,
    "cars": compute_cars,
    "ri": compute_ri,
    "social": compute_social,
    "nudges": compute_nudges,
    "forecast": compute_forecast,
    "c13k": compute_c13k,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

"""Normative ethics, built (Part 35).

* A felicific ledger: Bentham's dimensions, summed over everyone affected.
* Harsanyi's aggregation theorem on two people: nonlinear social welfare functions break either the social vNM axioms
  or the Pareto principle; the utility possibility frontier with its utilitarian, egalitarian and Nash points.
* Diamond's fairness objection: an ex-ante egalitarian society strictly prefers a mixture of two lotteries it ranks
  equal.
* Distribution: utilitarian sums, prioritarian sums, maximin, Gini and Atkinson indices; levelling down.
* Universalizability: a toy world of promises in which a universalized lying promise defeats itself; contradictions in
  conception and in will; the classic false positives and false negatives.
* The paradox of deontology, and the agent-relative weighting that consequentializes a constraint.
* Trolley cases with the doctrine of double effect; the trolley Price List.
* Scanlon's Transmitter Room: full aggregation against the relevance view.
* Moral uncertainty: expected choiceworthiness under different normalizations, and a moral parliament.
* Rules against acts: a noisy, self-serving act utilitarian against a rule follower and Hare's two-level thinker.
* Nozick's utility monster; Singer's pond with logarithmic welfare, under full and partial compliance.
* Taurek's numbers: saving the many, a fair coin, a weighted lottery.
* Particularism: the best fixed-weight rule of reasons, by exhaustive search, against principles with defeaters.
* Adaptive preferences: desire satisfaction against a capability index as options close.
* The formula of humanity as O'Neill's consent test; the value of moral information under moral uncertainty.
"""

from __future__ import annotations

import itertools
import math

import numpy as np


# ---------------------------------------------------------------------------
# Bentham's ledger
# ---------------------------------------------------------------------------
def felicific() -> dict:
    """Two acts, scored Bentham's way: for each person affected, intensity x duration x certainty, discounted for
    remoteness (propinquity), plus the pleasures and pains that follow (fecundity, purity), summed over everyone
    (extent)."""
    acts = {
        "keep the promise to help a friend move": [
            {"who": "you", "intensity": -2, "hours": 4, "certainty": 1.0, "delay": 0},
            {"who": "your friend", "intensity": 3, "hours": 4, "certainty": 0.9, "delay": 0},
            {"who": "your friend, later", "intensity": 2, "hours": 20, "certainty": 0.8, "delay": 30},
        ],
        "go to the concert instead": [
            {"who": "you", "intensity": 4, "hours": 3, "certainty": 0.9, "delay": 0},
            {"who": "your friend", "intensity": -3, "hours": 4, "certainty": 1.0, "delay": 0},
            {"who": "the friendship, later", "intensity": -2, "hours": 20, "certainty": 0.7, "delay": 30},
        ],
    }
    disc = 0.99

    def score(e):
        return e["intensity"] * e["hours"] * e["certainty"] * disc ** e["delay"]
    out = {}
    for a, es in acts.items():
        rows = [{**e, "value": round(score(e), 2)} for e in es]
        out[a] = {"rows": rows, "total": round(sum(r["value"] for r in rows), 2)}
    best = max(out, key=lambda a: out[a]["total"])
    return {"acts": out, "best": best, "discount_per_day": disc}


# ---------------------------------------------------------------------------
# Harsanyi
# ---------------------------------------------------------------------------
def harsanyi() -> dict:
    """Two people, lotteries over outcomes (u1, u2). (1) Ex-ante egalitarian W = min(E u1, E u2): it ranks the sure
    outcomes (1, 0) and (0, 1) equal (both 0) but their 50:50 mixture higher (0.5): a violation of the vNM axioms for
    society (betweenness). (2) Ex-post egalitarian E[min(u1, u2)]: the 50:50 lottery over (1, 0) and (0, 1) gets 0, the
    sure (0.5, 0.5) gets 0.5, though each person is indifferent between them (expected utility 0.5 both ways): a
    violation of Pareto indifference. Harsanyi (1955): only a weighted sum satisfies both. On the frontier
    u2 = 1 - u1^2: utilitarian, egalitarian and Nash points."""
    ex_ante = {"sure (1, 0)": 0.0, "sure (0, 1)": 0.0, "50:50 mixture": 0.5}
    ex_post = {"50:50 of (1, 0) and (0, 1)": 0.0, "sure (0.5, 0.5)": 0.5}
    individual = {"50:50 of (1, 0) and (0, 1)": [0.5, 0.5], "sure (0.5, 0.5)": [0.5, 0.5]}
    xs = np.linspace(0, 1, 200001)
    fr = 1 - xs ** 2
    util = float(xs[np.argmax(xs + fr)])
    egal = (math.sqrt(5) - 1) / 2
    nash = float(xs[np.argmax(xs * fr)])
    frontier = [[round(float(x), 4), round(float(1 - x * x), 4)] for x in np.linspace(0, 1, 41)]
    return {"ex_ante": ex_ante, "ex_post": ex_post, "individual": individual,
            "utilitarian": [round(util, 4), round(1 - util ** 2, 4)], "egalitarian": [round(egal, 4),
                                                                                    round(1 - egal ** 2, 4)],
            "nash": [round(nash, 4), round(1 - nash ** 2, 4)], "frontier": frontier}


# ---------------------------------------------------------------------------
# Distribution
# ---------------------------------------------------------------------------
def gini(x) -> float:
    x = np.sort(np.asarray(x, float))
    n = len(x)
    return float(sum((2 * (i + 1) - n - 1) * v for i, v in enumerate(x)) / (n * x.sum()))


def atkinson(x, eps: float) -> float:
    x = np.asarray(x, float)
    m = x.mean()
    if eps == 1:
        ede = math.exp(np.log(x).mean())
    else:
        ede = (np.mean(x ** (1 - eps))) ** (1 / (1 - eps))
    return float(1 - ede / m)


def distributions() -> dict:
    """Five people. Equal: (10, 10, 10, 10, 10). Unequal but larger: (2, 6, 10, 16, 26). Spread: (8, 9, 10, 11, 12).
    Levelled down: from (6, 6, 6, 6, 26) to (6, 6, 6, 6, 6), worse for one and better for no one. Each view ranks
    them: total (utilitarian), sum of square roots (prioritarian), the worst-off (maximin), the Gini index and the
    Atkinson index (eps = 1, 2)."""
    D = {"equal": [10, 10, 10, 10, 10], "unequal, larger": [2, 6, 10, 16, 26], "spread": [8, 9, 10, 11, 12],
         "before levelling": [6, 6, 6, 6, 26], "levelled down": [6, 6, 6, 6, 6]}
    out = {}
    for k, x in D.items():
        out[k] = {"people": x, "total": sum(x), "prioritarian": round(sum(math.sqrt(v) for v in x), 3),
                  "maximin": min(x), "gini": round(gini(x), 4), "atkinson1": round(atkinson(x, 1), 4),
                  "atkinson2": round(atkinson(x, 2), 4)}
    return {"rows": out}


# ---------------------------------------------------------------------------
# Kant: universalizability in a toy world
# ---------------------------------------------------------------------------
def promise_world(fractions=None, agents: int = 1000, rounds: int = 40, seed: int = 1785) -> dict:
    """A world of borrowers and lenders. Each round some agents need money and promise to repay; a share f of them,
    following the maxim 'when in need, make a promise I do not intend to keep', will not. Lenders lend when the
    observed rate of kept promises exceeds 1/2. The maxim's purpose, getting money by a promise, succeeds only if
    lenders lend. Universalized (f = 1), trust collapses, no one lends, and the maxim cannot achieve its own end:
    Kant's contradiction in conception."""
    rng = np.random.default_rng(seed)
    fractions = fractions or [round(x, 2) for x in np.linspace(0, 1, 11)]
    out = []
    for f in fractions:
        kept, made, lent_rounds, liar_success = 1.0, 1.0, 0, 0
        trust_path = []
        for _ in range(rounds):
            trust = kept / made
            trust_path.append(round(trust, 3))
            lend = trust > 0.5
            needy = rng.random(agents) < 0.1
            liars = needy & (rng.random(agents) < f)
            honest = needy & ~liars
            if lend:
                lent_rounds += 1
                liar_success += int(liars.sum())
                kept += honest.sum()
                made += needy.sum()
        out.append({"f": f, "final_trust": trust_path[-1], "lent_rounds": lent_rounds,
                    "liars_succeed": bool(liar_success > 0 and lent_rounds > rounds // 2), "trust": trust_path})
    return {"agents": agents, "rounds": rounds, "rows": out}


def maxims() -> dict:
    """Each maxim with a model of the world in which everyone acts on it. Contradiction in conception: the
    universalized world makes the maxim's purpose unattainable. Contradiction in will: the world is conceivable, but no
    agent with needs could will it. Then the classic test cases: maxims the test forbids though they are innocent
    (false positives) and maxims it permits though they are wrong (false negatives)."""
    pw = next(r for r in promise_world()["rows"] if r["f"] == 1.0)     # the same world as the promise chart
    N = 100

    def tennis(f):
        # play at 8 on Sunday because the courts are empty; 4 courts
        return f * N <= 4
    rows = [
        {"maxim": "when in need, make a lying promise to get money", "conception": not (pw["lent_rounds"] > 20),
         "will": True, "test": "forbidden", "intuition": "wrong", "kind": "hit"},
        {"maxim": "never help others in need", "conception": False, "will": True, "test": "forbidden",
         "intuition": "wrong", "kind": "hit"},
        {"maxim": "play tennis at 8 on Sundays, when the courts are empty", "conception": not tennis(1.0),
         "will": False, "test": "forbidden", "intuition": "innocent", "kind": "false positive"},
        {"maxim": "buy toy trains, but never sell them", "conception": True, "will": False, "test": "forbidden",
         "intuition": "innocent", "kind": "false positive"},
        {"maxim": "deceive anyone named Hans born on 3 March 1987, when convenient", "conception": False,
         "will": False, "test": "permitted", "intuition": "wrong", "kind": "false negative"},
    ]
    return {"rows": rows, "promise_final_trust": pw["final_trust"], "tennis_courts": 4, "players": N}


# ---------------------------------------------------------------------------
# The paradox of deontology
# ---------------------------------------------------------------------------
def deontology_paradox(victims: int = 5) -> dict:
    """You can kill one innocent person to prevent five others from killing one each. Ranking outcomes by the number of
    killings says kill (1 < 5). A constraint says do not. Scheffler's paradox: if killing is so bad, why not minimize
    killings? Consequentializing (Portmore, Dreier): rank outcomes agent-relatively, weighting one's own killings by k:
    the constraint is reproduced exactly when k > 5."""
    rows = []
    for k in (1, 3, 5, 6, 10):
        own, others = (1 * k, 0), (0, victims)
        kill_score = own[0] + own[1]
        refrain_score = others[0] + others[1]
        rows.append({"k": k, "kill": kill_score, "refrain": refrain_score,
                     "verdict": "kill" if kill_score < refrain_score else ("either" if kill_score == refrain_score
                                                                           else "refrain")})
    return {"victims": victims, "rows": rows, "threshold": victims}


# ---------------------------------------------------------------------------
# Trolleys
# ---------------------------------------------------------------------------
TROLLEY = [
    {"case": "switch", "act": "divert the trolley onto a side track", "deaths_if_act": 1, "deaths_if_not": 5,
     "harm_is": "side effect", "personal_force": False},
    {"case": "footbridge", "act": "push a large man off the bridge onto the track", "deaths_if_act": 1,
     "deaths_if_not": 5, "harm_is": "means", "personal_force": True},
    {"case": "loop", "act": "divert onto a loop, where the one's body stops the trolley", "deaths_if_act": 1,
     "deaths_if_not": 5, "harm_is": "means", "personal_force": False},
    {"case": "trapdoor", "act": "drop the man through a trapdoor by a switch", "deaths_if_act": 1,
     "deaths_if_not": 5, "harm_is": "means", "personal_force": False},
]


def trolley() -> dict:
    """The doctrine of double effect: harm may be permitted as a side effect of a good act, never intended as a means,
    if the good outweighs it. Act utilitarianism permits whatever minimizes deaths. Greene's personal force tracks
    intuitions in a different place."""
    rows = []
    for c in TROLLEY:
        util = c["deaths_if_act"] < c["deaths_if_not"]
        dde = c["harm_is"] == "side effect" and util
        rows.append({**c, "utilitarian": "permissible" if util else "impermissible",
                     "double_effect": "permissible" if dde else "impermissible"})
    return {"rows": rows, "survey": {"switch": 0.634, "don't switch": 0.133, "push": 0.220, "don't push": 0.562}}


# ---------------------------------------------------------------------------
# Scanlon's Transmitter Room
# ---------------------------------------------------------------------------
def transmitter(viewers: float = 1e9, harm: float = 100.0, relevance: float = 0.5) -> dict:
    """Jones is suffering agonizing shocks in the transmitter room during a broadcast watched by a billion people;
    rescuing him interrupts it for an hour. Full aggregation weighs one harm against the sum of all small losses;
    Scanlon's contractualism compares individual complaints; the relevance view (Voorhoeve 2014) aggregates only
    claims at least a given fraction of the strongest."""
    cases = [("an hour of broadcast", 0.001), ("a severe migraine each", 2.0), ("a broken arm each", 60.0),
             ("a life each, for two people", 100.0)]
    rows = []
    for name, each in cases:
        n = viewers if each < 50 else (2 if each == 100.0 else 3)
        total = n * each
        full = "help the many" if total > harm else "save Jones"
        scanlon = "help the many" if each > harm else ("toss up" if each == harm else "save Jones")
        rel = each >= relevance * harm
        partial = ("help the many" if total > harm else "save Jones") if rel else "save Jones"
        rows.append({"each_loses": name, "per_person": each, "people": n, "total": total, "full": full,
                     "individualist": scanlon, "relevance": partial})
    return {"harm": harm, "relevance": relevance, "rows": rows}


# ---------------------------------------------------------------------------
# Moral uncertainty
# ---------------------------------------------------------------------------
def moral_uncertainty(credence=(0.6, 0.4)) -> dict:
    """Credence 0.6 in a utilitarian theory (choiceworthiness: lives saved) and 0.4 in a deontological one (pushing is
    a grave wrong, -100). Maximizing expected choiceworthiness (MacAskill, Bykvist and Ord 2020) depends on how the
    theories' scales are compared: on the raw numbers, do not push; normalized by range or by variance, push. Add a
    third option both theories accept, shouting a warning that saves two, and every method of expected
    choiceworthiness takes it, while a parliament that simply votes (each theory's seats for its favourite) lets the
    majority theory push. Newberry and Ord's parliament (2021) bargains instead."""
    names = ["utilitarian", "deontological"]
    c = dict(zip(names, credence))

    def run(opts, cw):
        res = {}
        for norm in ("raw", "range", "variance"):
            tot = np.zeros(len(opts))
            for t in names:
                v = np.array(cw[t], float)
                if norm == "range":
                    v = (v - v.min()) / (v.max() - v.min())
                elif norm == "variance":
                    v = (v - v.mean()) / v.std()
                tot += c[t] * v
            res[norm] = {"scores": [round(float(x), 4) for x in tot], "choice": opts[int(np.argmax(tot))]}
        plural = np.zeros(len(opts))
        for t in names:
            plural[int(np.argmax(cw[t]))] += c[t]
        res["plurality"] = {"scores": [round(float(x), 3) for x in plural], "choice": opts[int(np.argmax(plural))]}
        return res
    two = (["push", "do nothing"], {"utilitarian": [4, 0], "deontological": [-100, 0]})
    three = (["push", "do nothing", "shout a warning"], {"utilitarian": [4, 0, 2], "deontological": [-100, 0, 0]})
    return {"credence": c, "two": {"options": two[0], "theories": two[1], "results": run(*two)},
            "three": {"options": three[0], "theories": three[1], "results": run(*three)}}


# ---------------------------------------------------------------------------
# Rules and acts: two-level utilitarianism
# ---------------------------------------------------------------------------
def two_level(n: int = 200000, mu: float = -1.0, sd: float = 1.0, noises=None, biases=(0.0, 0.5),
              threshold: float = 2.0, seed: int = 1981) -> dict:
    """Promise cases. Breaking a promise has true net value D ~ N(mu, sd) against keeping it (usually negative). An
    agent sees an estimate D + b + e, with self-serving bias b and noise e ~ N(0, s). The act utilitarian breaks
    whenever the estimate is positive; the rule follower never breaks; Hare's two-level thinker keeps the rule unless
    the estimate clears a high bar. Average realized value per case, against the noise s, for each bias."""
    rng = np.random.default_rng(seed)
    D = rng.normal(mu, sd, n)
    E0 = rng.normal(0.0, 1.0, n)
    noises = noises if noises is not None else [round(x, 2) for x in np.arange(0.0, 2.01, 0.1)]
    out = {"noises": noises, "threshold": threshold, "mu": mu, "sd": sd,
           "ideal": round(float(np.mean(np.maximum(D, 0))), 4), "curves": {}}
    for b in biases:
        act, two = [], []
        for s in noises:
            est = D + b + s * E0
            act.append(round(float(np.mean(np.where(est > 0, D, 0.0))), 4))
            two.append(round(float(np.mean(np.where(est > threshold, D, 0.0))), 4))
        cross = next((s for s, a in zip(noises, act) if a < 0), None)
        out["curves"][str(b)] = {"act": act, "two_level": two, "rule": [0.0] * len(noises), "act_below_rule_at": cross,
                                 "break_rate_act": round(float(np.mean(D + b + E0 > 0)), 4)}
    return out


# ---------------------------------------------------------------------------
# The utility monster
# ---------------------------------------------------------------------------
def utility_monster(total: int = 100, k: float = 10.0) -> dict:
    """Nozick (1974). Ten ordinary people with u(x) = sqrt(x), and a monster whose utility is k times anyone's:
    u_m(x) = k sqrt(x). Split 100 units to maximize the sum (utilitarian), a concave transform of utilities (the
    prioritarian sum of sqrt u), or the minimum (maximin)."""
    n = 10
    best = {}
    # the monster gets m units, the others share the rest equally (optimal by symmetry and concavity)
    ms = np.linspace(0, total, 10001)
    each = (total - ms) / n
    um, uo = k * np.sqrt(ms), np.sqrt(each)
    rules = {"utilitarian": um + n * uo, "prioritarian": np.sqrt(um) + n * np.sqrt(uo), "maximin": np.minimum(um, uo)}
    rel = {name: w / w.max() for name, w in rules.items()}
    for name, w in rules.items():
        i = int(np.argmax(w))
        best[name] = {"monster": round(float(ms[i]), 2), "each_other": round(float(each[i]), 2),
                      "monster_share": round(float(ms[i] / total), 3)}
    # utilitarian closed form: maximize k sqrt(m) + n sqrt((T - m)/n): m = T k^2 / (k^2 + n)
    exact = total * k ** 2 / (k ** 2 + n)
    idx = sorted(set(list(range(0, len(ms), 100)) + list(range(0, 101, 2))))     # fine near 0, where maximin peaks
    curve = {"m": [round(float(ms[j]), 2) for j in idx],
             **{name: [round(float(rel[name][j]), 4) for j in idx] for name in rules}}
    return {"k": k, "people": n, "total": total, "best": best, "utilitarian_exact": round(exact, 3), "curve": curve}


# ---------------------------------------------------------------------------
# Famine, affluence and morality
# ---------------------------------------------------------------------------
def pond(rich: float = 50000.0, poor: float = 500.0, n_poor: int = 90, n_rich: int = 10) -> dict:
    """Singer (1972) with logarithmic welfare. A dollar is worth 1/income: to someone on 500 it is worth 100 times
    what it is worth to someone on 50,000. Two people: the welfare sum peaks when incomes are equal. A world of 10 rich
    and 90 poor: the gift asked of each rich person if all comply, and of you if you alone do (Murphy 2000)."""
    ratio = rich / poor
    gifts = np.linspace(0, rich - poor, 4951)
    welfare = np.log(rich - gifts) + np.log(poor + gifts)
    i = int(np.argmax(welfare))
    mean = (n_rich * rich + n_poor * poor) / (n_rich + n_poor)
    full = rich - mean                                        # everyone equal at the mean
    alone_level = (rich + n_poor * poor) / (n_poor + 1)       # you give alone until you are as poor as they are
    # Scheffler (1982): an agent-centred prerogative to weight your own welfare M times; maximize
    # M log(rich - g) + log(poor + g): g = (rich - M poor)/(1 + M), and nothing once M >= rich/poor
    prerogative = {str(M): round(max(0.0, (rich - M * poor) / (1 + M)), 0) for M in (1, 10, 100)}
    return {"rich": rich, "poor": poor, "ratio": ratio, "best_gift": round(float(gifts[i]), 0),
            "prerogative": prerogative,
            "gifts": [round(float(g), 0) for g in gifts[::99]],
            "welfare_gain": [round(float(w - welfare[0]), 4) for w in welfare[::99]],
            "world": {"n_rich": n_rich, "n_poor": n_poor, "mean": round(mean, 0), "full_compliance_gift": round(full, 0),
                      "full_share": round(full / rich, 3), "alone_gift": round(rich - alone_level, 0),
                      "alone_share": round((rich - alone_level) / rich, 3)}}


# ---------------------------------------------------------------------------
# Should the numbers count?
# ---------------------------------------------------------------------------
def taurek(many: int = 5, n_trials: int = 100000, seed: int = 1977) -> dict:
    """Taurek (1977): one person on one rock, five on another; you can reach only one rock. Save the many; toss a fair
    coin (Taurek); or hold a weighted lottery, with chances proportional to numbers (Timmermann 2004). Each person's
    chance of survival, and the expected number saved, exact and simulated."""
    rng = np.random.default_rng(seed)
    pols = {"save the many": 1.0, "fair coin": 0.5, "weighted lottery": many / (many + 1)}
    rows = []
    for name, p in pols.items():
        hit = rng.random(n_trials) < p
        sim = float(np.mean(np.where(hit, many, 1)))
        rows.append({"policy": name, "p_many": round(p, 4), "p_one": round(1 - p, 4),
                     "expected_saved": round(p * many + (1 - p), 4), "simulated_saved": round(sim, 3)})
    return {"many": many, "rows": rows}


# ---------------------------------------------------------------------------
# Particularism: can moral judgment be a weighted sum of reasons?
# ---------------------------------------------------------------------------
PART_FEATURES = ["gives pleasure", "the pleasure is cruel", "keeps a promise", "the promise was coerced",
                 "tells a lie", "inside a game"]


def _verdict(f):
    pleasure, cruel, promise, coerced, lie, game = f
    score = 0
    if pleasure:
        score += -1 if cruel else 1            # pleasure counts for, cruel pleasure against
    if promise:
        score += 0 if coerced else 1           # a coerced promise does not bind
    if lie:
        score += 0 if game else -2             # a lie inside a game is no wrong
    return 1 if score >= 0 else 0


def _best_linear(X, y, wmax):
    """Exhaustive search over integer weightings in {-wmax..wmax}^d and half-integer thresholds: the best accuracy of
    'permissible iff the weighted sum of reasons exceeds t', and, among the best, the weighting smallest in L1."""
    W = np.array(list(itertools.product(range(-wmax, wmax + 1), repeat=X.shape[1])), dtype=float)
    S = X @ W.T
    best, pick = -1.0, None
    for t in np.arange(-X.shape[1] * wmax - 0.5, X.shape[1] * wmax + 1, 1.0):
        acc = ((S > t).astype(int) == y[:, None]).mean(axis=0)
        top = acc.max()
        if top > best + 1e-12:
            best, pick = float(top), None
        if abs(top - best) < 1e-12:
            for j in np.where(np.abs(acc - best) < 1e-12)[0]:
                key = (np.abs(W[j]).sum(), tuple(-W[j]))
                if pick is None or key < pick[0]:
                    pick = (key, W[j].tolist(), float(t))
    return {"acc": round(best, 4), "weights": [int(w) for w in pick[1]], "threshold": pick[2], "n_weightings": len(W)}


def particularism(wmax: int = 3) -> dict:
    """Dancy (2004): the holism of reasons. A feature that counts in favour in one case (pleasure) can count against in
    another (cruel pleasure), or not at all (a coerced promise; a lie inside a game). A toy judge scores every
    consistent combination of six features. An atomist gives each basic reason a fixed weight: the best weighting of
    the three basic reasons, found by exhaustive search, misjudges some cases. Principles with defeaters (McKeever and
    Ridge 2006) give the defeaters weights of their own, and fit every case."""
    cases = []
    for f in itertools.product([0, 1], repeat=6):
        pleasure, cruel, promise, coerced, lie, game = f
        if (cruel and not pleasure) or (coerced and not promise) or (game and not lie):
            continue                                   # a defeater needs something to defeat
        cases.append((f, _verdict(f)))
    X = np.array([c[0] for c in cases], dtype=float)
    y = np.array([c[1] for c in cases])
    atom = _best_linear(X[:, [0, 2, 4]], y, wmax)
    full = _best_linear(X, y, wmax)
    w = np.array(atom["weights"], dtype=float)
    wrong = [dict(zip(PART_FEATURES, map(int, X[k]))) for k in range(len(y))
             if int(X[k, [0, 2, 4]] @ w > atom["threshold"]) != y[k]]
    return {"features": PART_FEATURES, "n_cases": len(cases), "permissible": int(y.sum()), "atomistic": atom,
            "with_defeaters": full, "atomistic_wrong": wrong,
            "cases": [{"f": list(map(int, f)), "verdict": int(v)} for f, v in cases]}


# ---------------------------------------------------------------------------
# Adaptive preferences
# ---------------------------------------------------------------------------
def adaptive_preferences(options: int = 10, steps: int = 60, cuts=((10, 4), (30, 4)), adapt: float = 0.15) -> dict:
    """Elster's sour grapes (1983); Sen; Nussbaum (2000). An agent wants ten options (careers, freedoms) equally. At
    two moments, four options are closed off. Desire for an option out of reach decays by the factor (1 - adapt) each
    step, sour grapes; desire-satisfaction welfare is the share of desire that is aimed at options still open. The
    capability index, an objective list in Sen's sense, is the share of options open. Desire satisfaction recovers
    after each loss; capability does not."""
    w = np.ones(options)
    open_ = np.ones(options, dtype=bool)
    k = 0
    sat, cap = [], []
    cut_at = dict(cuts)
    for t in range(steps):
        if t in cut_at:
            open_[k:k + cut_at[t]] = False
            k += cut_at[t]
        sat.append(round(float(w[open_].sum() / w.sum()), 4))
        cap.append(round(float(open_.mean()), 4))
        w = np.where(open_, w, w * (1 - adapt))
    return {"options": options, "steps": steps, "cuts": [list(c) for c in cuts], "adapt": adapt,
            "desire_satisfaction": sat, "capability": cap, "final": {"desire": sat[-1], "capability": cap[-1]},
            "lowest_desire": min(sat)}


# ---------------------------------------------------------------------------
# The formula of humanity as a consent test
# ---------------------------------------------------------------------------
HUMANITY_ACTS = [
    {"act": "take a taxi home", "deceives": False, "coerces": False, "uses_body": False, "wrong": False},
    {"act": "sell a used car, honestly described", "deceives": False, "coerces": False, "uses_body": False,
     "wrong": False},
    {"act": "the lying promise", "deceives": True, "coerces": False, "uses_body": False, "wrong": True},
    {"act": "a confidence trick", "deceives": True, "coerces": False, "uses_body": False, "wrong": True},
    {"act": "your money or your life", "deceives": False, "coerces": True, "uses_body": False, "wrong": True},
    {"act": "push the man from the footbridge", "deceives": False, "coerces": True, "uses_body": True,
     "wrong": True},
    {"act": "a gangster buys a coffee", "deceives": False, "coerces": False, "uses_body": False, "wrong": False,
     "attitude": "merely a tool"},
]


def humanity_test() -> dict:
    """O'Neill (1985): you use someone merely as a means if you involve them in a scheme of action to which they
    could not possibly consent; deception and coercion guarantee that, since the deceived cannot know what they would
    be agreeing to and the coerced are given no say. The test judges the act; Parfit's gangster, who regards the
    barista merely as a tool, passes it, though on an attitude reading of 'merely as a means' he fails."""
    rows = []
    for a in HUMANITY_ACTS:
        could_consent = not (a["deceives"] or a["coerces"])
        attitude_fail = a.get("attitude") == "merely a tool"
        rows.append({**a, "could_consent": could_consent, "act_test": "permitted" if could_consent else "forbidden",
                     "attitude_test": "forbidden" if (attitude_fail or not could_consent) else "permitted",
                     "matches_intuition": (not could_consent) == a["wrong"]})
    return {"rows": rows, "act_matches": sum(r["matches_intuition"] for r in rows),
            "attitude_matches": sum((r["attitude_test"] == "forbidden") == r["wrong"] for r in rows)}


# ---------------------------------------------------------------------------
# The value of moral information
# ---------------------------------------------------------------------------
def moral_information(grid: int = 101) -> dict:
    """The footbridge under moral uncertainty (as in moral_uncertainty): how much is it worth to learn which theory is
    true before acting? VOI(p) = E_theory[max_a CW_t(a)] - max_a E_theory[CW_t(a)], under each normalization, as a
    function of the credence p in the utilitarian theory. Never negative; largest where the choice is closest."""
    opts = ["push", "do nothing"]
    cw = {"utilitarian": np.array([4.0, 0.0]), "deontological": np.array([-100.0, 0.0])}

    def norm(v, kind):
        if kind == "range":
            return (v - v.min()) / (v.max() - v.min())
        if kind == "variance":
            return (v - v.mean()) / v.std()
        return v
    ps = np.linspace(0, 1, grid)
    out = {"p": [round(float(p), 3) for p in ps]}
    for kind in ("raw", "range", "variance"):
        u, d = norm(cw["utilitarian"], kind), norm(cw["deontological"], kind)
        voi, now = [], []
        for p in ps:
            ec = p * u + (1 - p) * d
            informed = p * u.max() + (1 - p) * d.max()
            voi.append(round(float(informed - ec.max()), 4))
            now.append(round(float(ec.max()), 4))
        k = int(np.argmax(voi))
        out[kind] = {"voi": voi, "best_now": now, "peak_p": round(float(ps[k]), 3), "peak": voi[k],
                     "at_0.6": voi[int(round(0.6 * (grid - 1)))], "now_at_0.6": now[int(round(0.6 * (grid - 1)))]}
    return out

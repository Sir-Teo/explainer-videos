"""Precompute every number in Part 2 of *Statistics, Built* ("Chance, Counted").

    python -m videos.stats.stats2.compute            # everything missing (well under a minute)
    python -m videos.stats.stats2.compute --force monty

Results are cached in ``.cache/stats2/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Exact answers come
from the part's build, the probability engine ``explainer.stats.prob`` (Fractions, no rounding); each is checked
against a seeded simulation, and the scenes show both.  The screening example is the World's (``World.screening``).

Items:
    points       the problem of points (1654): Fermat's four continuations, Pascal's recursion table, Pacioli's
                 split, the general answer for a game to n, and 10,000 simulated finishes from 2-1
    galileo      three dice: the six partitions of 9 and of 10 and their 25 vs 27 orderings; de Mere's two bets,
                 exactly and simulated; the number of throws that makes a double six better than even
    counting     Pascal's triangle; arrangements; stars and bars (56 unordered rolls of three dice, not equally
                 likely)
    bertrand     three ways to draw a random chord: 3,000 of each, the running fraction longer than the triangle's
                 side, against 1/3, 1/2 and 1/4
    axioms       inclusion-exclusion for de Mere's first bet; derangements (exact for n <= 8 by enumeration, the
                 series for all n), 10,000 shuffles of 10 hats; the union bound
    conditioning two dice given their sum; the two-child problem; the total-probability tree
    bayes        the World's screening test: the natural-frequency tree, Bayes exactly, the realized fraction;
                 prevalence by age and what a positive means at each age; a second test
    clark        the published numbers of the Sally Clark case (1 in 8,543 and its square) and an odds-form
                 comparison on illustrative inputs
    monty        Monty Hall under four host protocols, exactly; 3,000 simulated games
    independence Bernstein's tetrahedron; the World's two tests, dependent overall and independent given the
                 condition
    variables    the sum of two dice as a function on 36 outcomes; a mixed variable; the Cantor distribution
                 (its staircase at five levels and 20,000 draws)
    expectation  fixed points of a shuffle (exact for n <= 8, 10,000 shuffles of 52 cards); birthdays; the coupon
                 collector for 50 coupons (exact mean and 2,000 simulated collections)
    variance     variance of a die and of sums; the St. Petersburg game: 2^20 simulated games and their running
                 mean against log2 n; Bernoulli's log-utility value
    pgf          the pgf of one and two dice as polynomials; Sicherman's dice, by factoring
"""

from __future__ import annotations

import math
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats.prob import Dist, coin, convolve, die, faces, shuffles
from explainer.stats.world import World

CACHE = Cache("stats2")
load = CACHE.load
W = World()


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def fr(x: F) -> list:
    """A Fraction for JSON: [numerator, denominator]."""
    x = F(x)
    return [x.numerator, x.denominator]


# ---------------------------------------------------------------------------
def p_first_to(a: int, b: int) -> F:
    """P(A wins) when A needs a more points and B needs b, fair rounds: A wins iff A takes at least a of the next
    a + b - 1 rounds (Fermat's trick: play them all, even if the match is decided early)."""
    n = a + b - 1
    return sum((F(math.comb(n, k), 2 ** n) for k in range(a, n + 1)), F(0))


def compute_points():
    # Fermat: A needs 1, B needs 2: play two more rounds, all four ways
    two = coin(heads="A", tails="B") ** 2
    fermat = [("".join(w), "A" in w) for w, _ in two.items()]
    p_a = two.P(lambda w: "A" in w)
    assert p_a == F(3, 4)
    # Pascal: the value to A of each score (A's points, B's points) in a game to three, stake 64
    stake = 64
    value = {}
    for a in range(3, -1, -1):
        for b in range(3, -1, -1):
            if a == 3:
                value[(a, b)] = F(stake)
            elif b == 3:
                value[(a, b)] = F(0)
    for total in range(4, -1, -1):
        for a in range(0, 3):
            b = total - a
            if 0 <= b < 3:
                value[(a, b)] = (value[(a + 1, b)] + value[(a, b + 1)]) / 2
    table = [[float(value[(a, b)]) for b in range(3)] for a in range(3)]
    assert value[(2, 1)] == 48 and value[(2, 2)] == 32
    # the general rule, and a simulated check from 2-1
    g = rng(1654)
    sims = 10_000
    wins = 0
    running = []
    for i in range(sims):
        a, b = 2, 1
        while a < 3 and b < 3:
            if g.random() < 0.5:
                a += 1
            else:
                b += 1
        wins += a == 3
        running.append(wins / (i + 1))
    grid = [[float(p_first_to(a, b)) for b in range(1, 6)] for a in range(1, 6)]
    return {"fermat": fermat, "p_a": fr(p_a), "pascal": table, "stake": stake,
            "pacioli": [stake * 2 / 3, stake / 3], "fair": [48, 16], "sim_n": sims, "sim_p": wins / sims,
            "running": np.array(running[::50]), "grid": grid,
            "p_3_2": fr(p_first_to(3, 2)), "p_2_3": fr(p_first_to(2, 3))}


def compute_galileo():
    three = die() ** 3
    tot = three.map(sum)
    parts = {s: [list(c) for c in combinations_with_replacement(range(1, 7), 3) if sum(c) == s] for s in (9, 10)}
    orders = {s: [len(set(permutations(c))) for c in parts[s]] for s in (9, 10)}
    assert sum(orders[9]) == 25 and sum(orders[10]) == 27
    assert tot.P(9) == F(25, 216) and tot.P(10) == F(27, 216)
    # de Mere: at least one six in four throws of one die; at least one double six in 24 throws of two
    bet1 = (die() ** 4).P(lambda r: 6 in r)
    dd = (die() * die()).map(lambda r: int(r == (6, 6)))
    bet2 = 1 - dd.iid_sum(24).P(0)
    need = next(n for n in range(1, 60) if 1 - F(35, 36) ** n > F(1, 2))
    g = rng(1620)
    n_sims = 100_000
    sim1 = float(((g.integers(1, 7, (n_sims, 4)) == 6).any(axis=1)).mean())
    sim2 = float(((g.integers(1, 7, (n_sims, 24)) + 10 * g.integers(1, 7, (n_sims, 24)) == 66).any(axis=1)).mean())
    sums3 = g.integers(1, 7, (n_sims, 3)).sum(axis=1)
    return {"pmf3": [float(tot.P(s)) for s in range(3, 19)], "parts": parts, "orders": orders,
            "bet1": fr(bet1), "bet2": float(bet2), "bet1_f": float(bet1), "need": need,
            "p_need": float(1 - F(35, 36) ** need), "p_24": float(1 - F(35, 36) ** 24),
            "sim1": sim1, "sim2": sim2, "sim_n": n_sims, "sim_9": float((sums3 == 9).mean()),
            "sim_10": float((sums3 == 10).mean())}


def compute_counting():
    tri = [[math.comb(n, k) for k in range(n + 1)] for n in range(11)]
    unordered = list(combinations_with_replacement(range(1, 7), 3))
    three = die() ** 3
    sorted_dist = three.map(lambda r: tuple(sorted(r)))
    probs = sorted({float(p) for _, p in sorted_dist.items()})
    return {"triangle": tri, "n_unordered": len(unordered), "n_ordered": 216, "unordered_probs": probs,
            "perm_52": str(math.factorial(52)), "perm_52_digits": len(str(math.factorial(52))),
            "c_49_6": math.comb(49, 6), "multinomial_mississippi": math.factorial(11) // (
                math.factorial(4) * math.factorial(4) * math.factorial(2)),
            "stars": math.comb(3 + 6 - 1, 3)}


def compute_bertrand():
    g = rng(1889)
    n = 3000
    r = 1.0
    side = math.sqrt(3) * r
    out = {}
    # 1. two random endpoints on the circle
    t1, t2 = g.uniform(0, 2 * np.pi, n), g.uniform(0, 2 * np.pi, n)
    a = np.column_stack([np.cos(t1), np.sin(t1)])
    b = np.column_stack([np.cos(t2), np.sin(t2)])
    out["ends"] = (a, b)
    # 2. a random radius, a random point on it, the chord perpendicular to it there
    phi, d = g.uniform(0, 2 * np.pi, n), g.uniform(0, 1, n)
    out["radius"] = _chord_from_midpoint(np.column_stack([d * np.cos(phi), d * np.sin(phi)]))
    # 3. a random midpoint, uniform in the disc
    rr, th = np.sqrt(g.uniform(0, 1, n)), g.uniform(0, 2 * np.pi, n)
    out["midpoint"] = _chord_from_midpoint(np.column_stack([rr * np.cos(th), rr * np.sin(th)]))
    res = {}
    for k, (p, q) in out.items():
        length = np.linalg.norm(p - q, axis=1)
        long_ = length > side
        res[k] = {"p": p[:240], "q": q[:240], "long": long_[:240], "frac": float(long_.mean()),
                  "running": np.cumsum(long_) / np.arange(1, n + 1)}
    return {"n": n, "exact": {"ends": 1 / 3, "radius": 1 / 2, "midpoint": 1 / 4},
            **{f"{k}_{f}": v[f] for k, v in res.items() for f in v}}


def _chord_from_midpoint(m):
    d = np.linalg.norm(m, axis=1)
    u = m / np.maximum(d, 1e-12)[:, None]
    perp = np.column_stack([-u[:, 1], u[:, 0]])
    h = np.sqrt(np.clip(1 - d ** 2, 0, None))
    return m + perp * h[:, None], m - perp * h[:, None]


def derangement_p(n: int) -> F:
    return sum((F((-1) ** k, math.factorial(k)) for k in range(n + 1)), F(0))


def compute_axioms():
    # inclusion-exclusion for "at least one six in four throws": A_i = "throw i is a six"
    terms = [F(math.comb(4, k), 6 ** k) for k in range(1, 5)]
    ie = terms[0] - terms[1] + terms[2] - terms[3]
    assert ie == (die() ** 4).P(lambda r: 6 in r)
    exact = []
    for n in range(1, 9):
        p = shuffles(n).P(lambda s: all(s[i] != i for i in range(len(s))))
        assert p == derangement_p(n)
        exact.append(fr(p))
    series = [float(derangement_p(n)) for n in range(1, 13)]
    g = rng(1708)
    shuf = np.argsort(g.random((10_000, 10)), axis=1)
    none = (shuf != np.arange(10)).all(axis=1)
    return {"ie_terms": [fr(t) for t in terms], "ie": fr(ie), "union": fr(F(4, 6)), "exact": exact,
            "series": series, "e_inv": 1 / math.e, "sim_n": 10_000, "sim_p": float(none.mean()),
            "running": np.cumsum(none)[::25] / np.arange(1, 10_001)[::25], "d4": 9, "n4": 24}


def compute_conditioning():
    two = die() * die()
    given8 = two.given(lambda r: sum(r) == 8)
    slice8 = [list(o) for o in given8.support()]
    p_d6_given8 = given8.P(lambda r: 6 in r)
    kids = Dist.uniform(["BB", "BG", "GB", "GG"])
    one_boy = kids.given(lambda w: "B" in w)
    first_boy = kids.given(lambda w: w[0] == "B")
    g = rng(2)
    fam = g.integers(0, 2, (100_000, 2))  # 1 = boy
    any_b = fam.max(axis=1) == 1
    both = fam.min(axis=1) == 1
    # total probability: an urn picked at random (3 urns), a ball drawn
    urns = Dist.uniform(["I", "II", "III"])
    reds = {"I": F(1, 4), "II": F(1, 2), "III": F(3, 4)}
    tree = urns.then(lambda u: coin(reds[u], heads="red", tails="blue"))
    p_red = tree.P(lambda w: w[1] == "red")
    return {"slice8": slice8, "p8": fr(two.P(lambda r: sum(r) == 8)), "p_six_given8": fr(p_d6_given8),
            "p_six": fr(two.P(lambda r: 6 in r)),
            "p_bb_one": fr(one_boy.P("BB")), "p_bb_first": fr(first_boy.P("BB")),
            "sim_bb_one": float(both[any_b].mean()), "sim_n": int(any_b.sum()),
            "p_red": fr(p_red), "reds": {k: fr(v) for k, v in reds.items()},
            "post_urn": {u: fr(tree.given(lambda w: w[1] == "red").P(lambda w, u=u: w[0] == u)) for u in reds}}


def compute_bayes():
    s = W.screening
    a = W.adult
    sick, ta, tb = s["sick"][a], s["test_a"][a], s["test_b"][a]
    n = int(a.sum())
    prev = float(sick.mean())
    sens, spec = W.SCREEN_SENS, W.SCREEN_SPEC
    exact = prev * sens / (prev * sens + (1 - prev) * (1 - spec))
    per = 10_000
    nf = {"sick": round(per * 0.01), "sick_pos": round(per * 0.01 * sens), "well": round(per * 0.99),
          "well_pos": round(per * 0.99 * (1 - spec))}
    nf["post"] = nf["sick_pos"] / (nf["sick_pos"] + nf["well_pos"])
    age = W.age[a]
    groups = [(18, 35), (35, 55), (55, 75), (75, 120)]
    by_age = []
    for lo, hi in groups:
        m = (age >= lo) & (age < hi)
        pv = float(sick[m].mean())
        by_age.append({"lo": lo, "hi": hi, "prev": pv, "post": pv * sens / (pv * sens + (1 - pv) * (1 - spec)),
                       "realized": float(sick[m & ta].mean()), "n": int(m.sum())})
    prior_odds = prev / (1 - prev)
    lr = sens / (1 - spec)
    both = ta & tb
    post2 = prior_odds * lr * lr / (1 + prior_odds * lr * lr)
    # a dot grid of 1,000 adults (a seeded sample) for the icon array
    idx = W.sample(1000, among=a, seed=2)
    return {"n": n, "n_sick": int(sick.sum()), "n_pos": int(ta.sum()), "n_sick_pos": int((sick & ta).sum()),
            "n_well_pos": int((~sick & ta).sum()), "prev": prev, "sens": sens, "spec": spec, "exact": exact,
            "realized": float(sick[ta].mean()), "nf": nf, "by_age": by_age, "prior_odds": prior_odds, "lr": lr,
            "post_odds": prior_odds * lr, "post2": post2, "realized2": float(sick[both].mean()),
            "n_both": int(both.sum()), "grid_sick": s["sick"][idx], "grid_pos": s["test_a"][idx]}


def compute_clark():
    one = 8543
    sq = one ** 2
    # an odds-form comparison on illustrative round inputs (not estimates): both explanations are rare
    return {"one": one, "square": sq, "square_m": sq / 1e6,
            "illus": {"p_two_sids": 1 / 100_000, "p_two_murders": 1 / 1_000_000}}


def monty(protocol: str, q: F = F(1, 2)) -> dict:
    """The contestant picks door 1.  Returns P(car behind door 2 | host opened door 3, showing a goat) and
    P(win by staying | same), under a host protocol."""
    car = Dist.uniform([1, 2, 3])

    def host(c):
        if protocol == "standard":  # always opens a goat door other than 1; picks at random if he can
            return Dist({2: F(1, 2), 3: F(1, 2)}) if c == 1 else Dist({({2: 3, 3: 2}[c]): 1})
        if protocol == "biased":  # prefers door 3 with probability q when both 2 and 3 hide goats
            return Dist({2: 1 - q, 3: q}) if c == 1 else Dist({({2: 3, 3: 2}[c]): 1})
        if protocol == "ignorant":  # opens 2 or 3 at random, whatever is behind it
            return Dist({2: F(1, 2), 3: F(1, 2)})
        if protocol == "devil":  # opens a door only when your pick is the car (tempting you to switch)
            return Dist({2: F(1, 2), 3: F(1, 2)}) if c == 1 else Dist({"none": 1})
        raise ValueError(protocol)

    tree = car.then(host)
    seen = tree.given(lambda w: w[1] == 3 and w[0] != 3)  # door 3 opened, a goat behind it
    return {"switch": fr(seen.P(lambda w: w[0] == 2)), "stay": fr(seen.P(lambda w: w[0] == 1))}


def compute_monty():
    protocols = {k: monty(k) for k in ("standard", "ignorant", "devil")}
    qs = np.linspace(0, 1, 21)
    biased = [float(F(*monty("biased", F(q).limit_denominator(100))["switch"])) for q in qs]
    g = rng(1990)
    n = 3000
    car = g.integers(1, 4, n)
    switch_win = car != 1  # contestant picks 1; standard host; switching wins iff the car is not behind door 1
    return {"protocols": protocols, "qs": qs, "biased": biased, "n": n,
            "running": np.cumsum(switch_win) / np.arange(1, n + 1), "sim_switch": float(switch_win.mean())}


def compute_independence():
    tet = Dist.uniform(["R", "G", "B", "RGB"])
    ev = {c: (lambda w, c=c: c in w) for c in "RGB"}
    pair = tet.P(lambda w: ev["R"](w) and ev["G"](w))
    triple = tet.P(lambda w: all(ev[c](w) for c in "RGB"))
    assert pair == F(1, 4) and triple == F(1, 4)
    s = W.screening
    a = W.adult
    sick, ta, tb = s["sick"][a], s["test_a"][a], s["test_b"][a]
    out = {"single": fr(tet.P(ev["R"])), "pair": fr(pair), "triple": fr(triple),
           "pb": float(tb.mean()), "pb_a": float(tb[ta].mean()),
           "pb_sick": float(tb[sick].mean()), "pb_a_sick": float(tb[ta & sick].mean()),
           "pb_well": float(tb[~sick].mean()), "pb_a_well": float(tb[ta & ~sick].mean())}
    return out


def cantor_cdf(x, levels=30):
    """The Cantor function at x in [0, 1] (to ``levels`` ternary digits)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    y, scale = 0.0, 0.5
    for _ in range(levels):
        x *= 3
        d = int(min(x, 2.999999))
        x -= d
        if d == 1:
            return y + scale
        y += scale * (d // 2)
        scale /= 2
    return y


def compute_variables():
    two = die() * die()
    sums = [[i + j for j in range(1, 7)] for i in range(1, 7)]
    pmf = [float(two.map(sum).P(s)) for s in range(2, 13)]
    g = rng(1883)
    bits = g.integers(0, 2, (20_000, 30))
    cantor = (2 * bits / 3.0 ** np.arange(1, 31)).sum(axis=1)
    xs = np.linspace(0, 1, 601)
    staircase = [cantor_cdf(float(x)) for x in xs]
    levels = []
    for L in range(6):
        # the level-L approximation: uniform on the 2^L intervals of length 3^-L that survive
        levels.append([float(np.clip(sum(_level_mass(x, L)), 0, 1)) for x in xs])
    return {"sums": sums, "pmf": pmf, "cantor": np.sort(cantor), "xs": xs, "staircase": staircase,
            "levels": np.array(levels), "cantor_mean": float(cantor.mean()), "cantor_var": float(cantor.var())}


def _level_mass(x, L):
    """CDF at x of the uniform distribution on the 2^L surviving intervals of the level-L Cantor set."""
    ivs = [(0.0, 1.0)]
    for _ in range(L):
        ivs = [iv for a, b in ivs for iv in ((a, a + (b - a) / 3), (b - (b - a) / 3, b))]
    w = 1.0 / len(ivs)
    return [w * min(max((x - a) / (b - a), 0.0), 1.0) for a, b in ivs]


def compute_expectation():
    fixed = []
    for n in range(1, 9):
        d = shuffles(n).map(lambda s: sum(s[i] == i for i in range(len(s))))
        fixed.append({"n": n, "E": fr(d.E()), "Var": fr(d.var()), "P0": fr(d.P(0))})
    g = rng(52)
    deck = np.argsort(g.random((10_000, 52)), axis=1)
    matches = (deck == np.arange(52)).sum(axis=1)
    counts = np.bincount(matches, minlength=8)[:8] / 10_000
    poisson = [math.exp(-1) / math.factorial(k) for k in range(8)]
    # birthdays
    p_match = [1 - math.prod((365 - i) / 365 for i in range(n)) for n in range(0, 71)]
    n50 = next(n for n, p in enumerate(p_match) if p >= 0.5)
    bd = g.integers(0, 365, (20_000, 23))
    s = np.sort(bd, axis=1)
    sim23 = float((np.diff(s, axis=1) == 0).any(axis=1).mean())
    # coupon collector, 50 kinds
    k = 50
    h = sum(F(1, i) for i in range(1, k + 1))
    mean_t = k * h
    var_t = sum((1 - F(i, k)) / F(i, k) ** 2 for i in range(1, k + 1))  # sum of (1 - p) / p^2, p = i / k
    times = []
    for _ in range(2000):
        seen, t = set(), 0
        while len(seen) < k:
            seen.add(int(g.integers(0, k)))
            t += 1
        times.append(t)
    return {"fixed": fixed, "deck_counts": counts, "poisson": poisson, "deck_mean": float(matches.mean()),
            "deck_var": float(matches.var()), "p_match": p_match, "n50": n50, "p23": p_match[23],
            "sim23": sim23, "pairs23": math.comb(23, 2), "e_pairs23": math.comb(23, 2) / 365,
            "k": k, "H": float(h), "mean_t": float(mean_t), "sd_t": math.sqrt(float(var_t)),
            "times": np.array(times), "sim_mean_t": float(np.mean(times))}


def compute_variance():
    d = die()
    g = rng(1738)
    n = 2 ** 20
    k = g.geometric(0.5, n)  # tosses until the first head
    pay = 2.0 ** k
    running = np.cumsum(pay) / np.arange(1, n + 1)
    pts = np.unique(np.round(np.logspace(0, 20 * math.log10(2), 400)).astype(int)) - 1
    e_log = sum(F(j, 2 ** j) for j in range(1, 200))  # E log2(payout) = sum j 2^-j -> 2
    return {"E": fr(d.E()), "Var": fr(d.var()), "E2": fr(d.moment(2)), "var_two": fr((d + d).var()),
            "var_ten": fr(d.iid_sum(10).var()), "n_games": n, "ns": pts + 1, "running": running[pts],
            "log2": np.log2(pts + 1), "max_pay": float(pay.max()), "e_log2": float(e_log), "ce": 2 ** float(e_log),
            "partial": [float(sum(F(2 ** j, 2 ** j) for j in range(1, m + 1))) for m in range(1, 11)]}


def compute_pgf():
    one = die().pgf()
    two = convolve(one, one)
    assert two == (die() + die()).pgf()
    a, b = faces([1, 2, 2, 3, 3, 4]), faces([1, 3, 4, 5, 6, 8])
    assert (a + b).pgf() == two
    mean = sum(F(k) * c for k, c in enumerate(one))
    second = sum(F(k * (k - 1)) * c for k, c in enumerate(one))
    return {"one": [float(c) for c in one], "two": [float(c) for c in two], "two_counts": [int(c * 36) for c in two],
            "sich_a": [int(c * 6) for c in a.pgf()], "sich_b": [int(c * 6) for c in b.pgf()],
            "mean": fr(mean), "g2": fr(second), "var": fr(second + mean - mean ** 2)}


ITEMS = {
    "points": compute_points, "galileo": compute_galileo, "counting": compute_counting, "bertrand": compute_bertrand,
    "axioms": compute_axioms, "conditioning": compute_conditioning, "bayes": compute_bayes, "clark": compute_clark,
    "monty": compute_monty, "independence": compute_independence, "variables": compute_variables,
    "expectation": compute_expectation, "variance": compute_variance, "pgf": compute_pgf,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

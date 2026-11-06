"""Decision theory, built (Part 33).

Expected utility and its rivals: a money pump, St Petersburg, the von Neumann-Morgenstern construction, Allais and
Ellsberg checked against every utility and every probability, rank-dependent and risk-weighted utility, prospect
theory, the Kelly criterion simulated, the Pasadena game's rearrangements, Newcomb's problem with a predictor of any
accuracy, evidential and causal decision theory on small causal graphs (the smoking lesion, death in Damascus),
dynamic choice (Ulysses), Good's value-of-information theorem checked on random problems, and the two envelopes.
"""

from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------------------
# Preferences: the money pump
# ---------------------------------------------------------------------------
def money_pump(cycles: int = 5, fee: float = 0.01) -> dict:
    """An agent who strictly prefers A to B, B to C and C to A, and will pay a cent to trade up, can be led round the
    cycle for ever: holding A, it pays to swap for C (it prefers C to A), then for B, then for A again."""
    prefers = {("A", "B"), ("B", "C"), ("C", "A")}
    holding, paid, log = "A", 0.0, []
    for _ in range(cycles):
        for offer in ("C", "B", "A"):
            if (offer, holding) in prefers:
                paid += fee
                log.append((holding, offer, round(paid, 2)))
                holding = offer
    return {"trades": len(log), "paid": round(paid, 2), "holding": holding, "log": log[:6], "fee": fee,
            "cyclic": True}


# ---------------------------------------------------------------------------
# St Petersburg
# ---------------------------------------------------------------------------
def revealed_preference() -> dict:
    """Samuelson (1938), Afriat (1967), Varian (1982): prices p_t and chosen bundles x_t. x_i is directly revealed
    preferred to x_j if x_j was affordable when x_i was chosen (p_i . x_j <= p_i . x_i), strictly if strictly cheaper.
    GARP: no x_i revealed preferred (via a chain) to x_j while x_j is strictly directly revealed preferred to x_i. By
    Afriat's theorem, data pass GARP exactly when some monotone, concave utility rationalizes them. Two shoppers: one
    passes; one fails, and Afriat's critical cost efficiency index (the largest share of each budget at which the data
    pass) says how much money the inconsistency wastes."""
    def relations(obs, e=1.0):
        n = len(obs)
        R = [[False] * n for _ in range(n)]
        P = [[False] * n for _ in range(n)]
        for i, (pi, xi) in enumerate(obs):
            ci = float(np.dot(pi, xi))
            for j, (_, xj) in enumerate(obs):
                cj = float(np.dot(pi, xj))
                R[i][j] = cj <= e * ci + 1e-12
                P[i][j] = cj < e * ci - 1e-12
        for k in range(n):                       # transitive closure of R
            for i in range(n):
                for j in range(n):
                    R[i][j] = R[i][j] or (R[i][k] and R[k][j])
        return R, P

    def garp(obs, e=1.0):
        R, P = relations(obs, e)
        n = len(obs)
        return not any(R[i][j] and P[j][i] for i in range(n) for j in range(n) if i != j)

    def ccei(obs):
        lo, hi = 0.0, 1.0
        if garp(obs):
            return 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if garp(obs, mid) else (lo, mid)
        return lo
    consistent = [((1, 2), (4, 1)), ((2, 1), (1, 4))]
    inconsistent = [((1, 2), (2, 2)), ((2, 1), (3.5, 1))]
    out = {}
    for name, obs in (("consistent", consistent), ("inconsistent", inconsistent)):
        rows = []
        for i, (pi, xi) in enumerate(obs):
            rows.append({"prices": list(pi), "bundle": list(xi), "spent": float(np.dot(pi, xi)),
                         "other_costs": float(np.dot(pi, obs[1 - i][1]))})
        out[name] = {"obs": rows, "garp": garp(obs), "ccei": round(ccei(obs), 4)}
    return out


def st_petersburg(plays: int = 10 ** 6, seed: int = 1738) -> dict:
    """A fair coin is tossed until it lands heads; if that is on toss k, you win 2^k ducats. Each term of the expected
    value is 1, so it diverges. With Bernoulli's logarithmic utility the expected utility is finite: E[log2 prize] = 2,
    a certainty equivalent of 4 ducats (from no other wealth). Simulated average winnings grow roughly like log2 of
    the number of plays; Menger's super-game (prizes 2^(2^k)) defeats log utility too."""
    rng = np.random.default_rng(seed)
    k = rng.geometric(0.5, plays)
    prize = 2.0 ** k
    checkpoints = [10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6]
    means = [round(float(prize[:n].mean()), 2) for n in checkpoints]
    eu_log2 = sum((0.5 ** j) * j for j in range(1, 200))
    partial = [j for j in range(1, 11)]                     # partial sums of the expectation: 1, 2, ..., 10
    menger = [round((0.5 ** j) * (2 ** j), 4) for j in range(1, 6)]   # each term of E[log2 prize] in the super-game
    return {"checkpoints": checkpoints, "means": means, "eu_log2": round(eu_log2, 6),
            "ce": round(2 ** eu_log2, 4), "partial": partial, "menger_terms": menger, "max_prize": float(prize.max())}


# ---------------------------------------------------------------------------
# Lotteries, the Marschak-Machina triangle
# ---------------------------------------------------------------------------
def eu(lottery, u) -> float:
    return sum(p * u(x) for x, p in lottery)


def triangle_lines(u_low: float = 0.0, u_mid: float = 0.6, u_high: float = 1.0, levels: int = 7) -> dict:
    """Lotteries over three prizes as points (p_low, p_high) in the triangle. Expected utility indifference curves
    are the lines p_high u_h + p_low u_l + (1 - p_low - p_high) u_m = c: parallel straight lines, with slope
    (u_m - u_l) / (u_h - u_m)."""
    slope = (u_mid - u_low) / (u_high - u_mid)
    lines = []
    for c in np.linspace(u_mid - 0.5, u_high, levels):
        # p_h = (c - u_m + p_l (u_m - u_l)) / (u_h - u_m)
        pts = []
        for pl in np.linspace(0, 1, 101):
            ph = (c - u_mid + pl * (u_mid - u_low)) / (u_high - u_mid)
            if 0 <= ph <= 1 - pl + 1e-9:
                pts.append([round(float(pl), 3), round(float(ph), 3)])
        if len(pts) > 1:
            lines.append(pts)
    return {"slope": round(slope, 4), "lines": lines}


# ---------------------------------------------------------------------------
# Allais
# ---------------------------------------------------------------------------
ALLAIS = {  # prizes in millions
    "1A": [(1, 1.0)],
    "1B": [(5, 0.10), (1, 0.89), (0, 0.01)],
    "2A": [(1, 0.11), (0, 0.89)],
    "2B": [(5, 0.10), (0, 0.90)],
}


def allais(grid: int = 201) -> dict:
    """Allais (1953). Most people prefer 1A to 1B and 2B to 2A. Normalize u(0) = 0, u(5) = 1 and search every u(1) in
    [0, 1]: none makes both preferences come out right under expected utility, because EU(1A) - EU(1B) =
    EU(2A) - EU(2B) = 0.11 u(1) - 0.10 for every u. Risk-weighted expected utility (Buchak) with r(p) = p^2 does
    represent the common pattern, for u(1) between about 0.33 and 0.83 (0.8 shown)."""
    ok = 0
    diffs = []
    for k in range(grid):
        u1 = k / (grid - 1)
        u = {0: 0.0, 1: u1, 5: 1.0}.get
        a = eu(ALLAIS["1A"], u) - eu(ALLAIS["1B"], u)
        b = eu(ALLAIS["2B"], u) - eu(ALLAIS["2A"], u)
        diffs.append((round(u1, 3), round(a, 4), round(b, 4)))
        ok += a > 0 and b > 0
    u1 = 0.8
    r = lambda p: p ** 2   # noqa: E731
    reus = {name: reu(lot, {0: 0.0, 1: u1, 5: 1.0}.get, r) for name, lot in ALLAIS.items()}
    return {"grid": grid, "both_ok": ok, "identity": "0.11 u(1) - 0.10", "u1_demo": u1,
            "reu": {k: round(v, 4) for k, v in reus.items()},
            "reu_pattern": reus["1A"] > reus["1B"] and reus["2B"] > reus["2A"],
            "points": {k: [round(sum(p for x, p in v if x == 0), 3), round(sum(p for x, p in v if x == 5), 3)]
                       for k, v in ALLAIS.items()}}


def reu(lottery, u, r) -> float:
    """Risk-weighted expected utility (Buchak 2013): order outcomes from worst to best; REU = u(x1) + sum_i
    r(P(at least x_i)) (u(x_i) - u(x_{i-1})). With r(p) = p it is expected utility."""
    outs = sorted(lottery, key=lambda xp: u(xp[0]))
    total = u(outs[0][0])
    for i in range(1, len(outs)):
        tail = sum(p for _, p in outs[i:])
        total += r(tail) * (u(outs[i][0]) - u(outs[i - 1][0]))
    return total


# ---------------------------------------------------------------------------
# Ellsberg
# ---------------------------------------------------------------------------
def ellsberg(grid: int = 61) -> dict:
    """Ellsberg (1961): an urn of 90 balls, 30 red and 60 black or yellow in unknown proportion. Most prefer a bet on
    red to a bet on black, and a bet on black-or-yellow to a bet on red-or-yellow. No probability for black (0 to
    60 balls) makes both preferences maximize expected utility; maxmin expected utility over the set of possible
    urns (Gilboa and Schmeidler 1989) yields both."""
    ok = 0
    for nb in range(grid):
        pb = nb / 90
        pr, py = 30 / 90, (60 - nb) / 90
        ok += (pr > pb) and (pb + py > pr + py)
    worst = lambda f: min(f(nb / 90, (60 - nb) / 90) for nb in range(grid))  # noqa: E731
    mm = {"red": worst(lambda b, y: 30 / 90), "black": worst(lambda b, y: b),
          "black or yellow": worst(lambda b, y: b + y), "red or yellow": worst(lambda b, y: 30 / 90 + y)}
    return {"urns": grid, "both_ok": ok, "maxmin": {k: round(v, 4) for k, v in mm.items()},
            "maxmin_pattern": mm["red"] > mm["black"] and mm["black or yellow"] > mm["red or yellow"]}


# ---------------------------------------------------------------------------
# Prospect theory
# ---------------------------------------------------------------------------
def prospect(alpha: float = 0.88, lam: float = 2.25, gamma: float = 0.61, delta: float = 0.69) -> dict:
    """Tversky and Kahneman (1992): value v(x) = x^alpha for gains and -lambda (-x)^alpha for losses; probability
    weights w(p) = p^g / (p^g + (1 - p)^g)^(1/g) (g = 0.61 for gains, 0.69 for losses). The fourfold pattern: for a 5%
    chance of 100 the certainty equivalent exceeds the expected 5 (risk seeking for long shots); for a 95% chance of
    100 it falls below 95 (risk aversion); and the reverse for losses."""
    def w(p, g):
        return p ** g / (p ** g + (1 - p) ** g) ** (1 / g)

    def v(x):
        return x ** alpha if x >= 0 else -lam * (-x) ** alpha

    def ce(x, p):
        g = gamma if x >= 0 else delta
        val = w(p, g) * v(x)
        return val ** (1 / alpha) if val >= 0 else -((-val / lam) ** (1 / alpha))

    four = [{"prospect": f"{int(100 * p)}% chance of {x}", "ev": round(p * x, 2), "ce": round(ce(x, p), 2)}
            for x, p in ((100, 0.05), (100, 0.95), (-100, 0.05), (-100, 0.95))]
    ws = [[round(p, 2), round(w(p, gamma), 4)] for p in np.linspace(0, 1, 41)]
    vs = [[round(x, 1), round(v(x), 3)] for x in np.linspace(-100, 100, 81)]
    return {"fourfold": four, "w_curve": ws, "v_curve": vs, "params": {"alpha": alpha, "lambda": lam,
                                                                        "gamma": gamma, "delta": delta}}


def asian_disease(alpha: float = 0.88, lam: float = 2.25, gamma: float = 0.61, delta: float = 0.69) -> dict:
    """Tversky and Kahneman (1981): 600 people face a disease. Framed as lives saved, most chose the sure program
    (200 saved) over a 1/3 chance of saving all 600; framed as deaths, most chose the 2/3 chance that all 600 die over
    400 dying for sure. The options are identical. Prospect theory, with its 1992 parameters, values them so: concave
    for gains (take the sure thing), convex and loss-averse for losses (gamble)."""
    def w(p, g):
        return p ** g / (p ** g + (1 - p) ** g) ** (1 / g)

    def v(x):
        return x ** alpha if x >= 0 else -lam * (-x) ** alpha
    A = v(200)
    B = w(1 / 3, gamma) * v(600)
    C = v(-400)
    D = w(2 / 3, delta) * v(-600)
    return {"A": round(A, 2), "B": round(B, 2), "C": round(C, 2), "D": round(D, 2),
            "gain_frame_choice": "A" if A > B else "B", "loss_frame_choice": "C" if C > D else "D",
            "reported": {"A": 0.72, "D": 0.78, "n_gain": 152, "n_loss": 155}}


# ---------------------------------------------------------------------------
# The Kelly criterion
# ---------------------------------------------------------------------------
def kelly(p: float = 0.6, bets: int = 1000, paths: int = 1000, fractions=(0.1, 0.2, 0.4, 0.6),
          seed: int = 1956) -> dict:
    """Kelly (1956): betting a fixed fraction f of wealth at even odds on a coin that wins with probability p, wealth
    after n bets is a product, and its long-run growth rate is g(f) = p log(1 + f) + (1 - p) log(1 - f), maximized at
    f* = 2p - 1 (0.2 here). Simulated: the median wealth grows fastest at f*; at twice f* growth is near zero; beyond,
    the typical path is ruined although every bet has positive expectation."""
    rng = np.random.default_rng(seed)
    wins = rng.random((paths, bets)) < p
    out = {}
    for f in fractions:
        logw = np.where(wins, math.log1p(f), math.log1p(-f)).cumsum(axis=1)
        final = logw[:, -1]
        out[str(f)] = {"g": round(p * math.log1p(f) + (1 - p) * math.log1p(-f), 5),
                       "median_log10": round(float(np.median(final) / math.log(10)), 3),
                       "ruined": int((final < math.log(0.01)).sum()),
                       "sample": [[round(float(x / math.log(10)), 3) for x in logw[k, ::20]] for k in range(5)],
                       "mean_log10_of_mean": round(float(bets * math.log10(1 + f * (2 * p - 1))), 2)}
    fs = np.linspace(0.0, 0.6, 61)
    curve = [[round(float(f), 3), round(float(p * math.log1p(f) + (1 - p) * math.log1p(-f)), 5)] for f in fs]
    return {"p": p, "bets": bets, "paths": paths, "f_star": round(2 * p - 1, 3), "by_f": out, "g_curve": curve}


# ---------------------------------------------------------------------------
# Pasadena
# ---------------------------------------------------------------------------
def pasadena(terms: int = 200000) -> dict:
    """Nover and Hajek (2004): toss until heads; if on toss n, the payoff is (-1)^(n-1) 2^n / n. The expectation is the
    alternating harmonic series 1 - 1/2 + 1/3 - ..., which converges to ln 2 in its natural order, but conditionally:
    taken two positive terms to one negative it converges to (3/2) ln 2 (Riemann's rearrangement theorem), and
    rearranged suitably to anything."""
    nat = 0.0
    for n in range(1, terms + 1):
        nat += (-1) ** (n - 1) / n
    pos, neg, s = 1, 2, 0.0
    for _ in range(terms // 3):
        s += 1 / pos + 1 / (pos + 2)
        pos += 4
        s -= 1 / neg
        neg += 2
    return {"natural": round(nat, 5), "ln2": round(math.log(2), 5), "two_one": round(s, 5),
            "three_halves_ln2": round(1.5 * math.log(2), 5)}


# ---------------------------------------------------------------------------
# Newcomb
# ---------------------------------------------------------------------------
def newcomb(accuracies=(0.5, 0.5005, 0.6, 0.9, 0.99), agents: int = 10000, seed: int = 1969) -> dict:
    """Newcomb's problem with a predictor of accuracy p: the opaque box holds 1,000,000 if one-boxing was predicted;
    the clear box always holds 1,000. Evidential expected values: one box p * 1e6; two boxes (1 - p) * 1e6 + 1e3; one
    boxing is better whenever p > 0.5005. Causal decision theory: whatever is in the box, two boxes get 1,000 more.
    Simulated with 10,000 agents at p = 0.9: the one-boxers average far more."""
    rows = []
    for p in accuracies:
        rows.append({"p": p, "one": round(p * 1e6, 1), "two": round((1 - p) * 1e6 + 1e3, 1)})
    rng = np.random.default_rng(seed)
    p = 0.9
    choice = rng.random(agents) < 0.5            # True: one-box
    correct = rng.random(agents) < p
    predicted_one = np.where(correct, choice, ~choice)
    payoff = np.where(predicted_one, 1e6, 0) + np.where(choice, 0, 1e3)
    return {"rows": rows, "threshold": 0.5005, "sim_p": p, "agents": agents,
            "one_mean": round(float(payoff[choice].mean()), 0), "two_mean": round(float(payoff[~choice].mean()), 0),
            "n_one": int(choice.sum())}


def twin_pd(T: float = 5, R: float = 3, P: float = 1, S: float = 0,
            sames=(0.5, 0.6, 0.7143, 0.8, 0.9, 0.99)) -> dict:
    """Lewis (1979): the prisoner's dilemma against a near-copy is a Newcomb problem. Each player's move matches the
    other's with probability r. Evidential values: cooperate r R + (1 - r) S, defect r P + (1 - r) T; cooperation wins
    when r > (T - S) / (T - S + R - P) = 5/7. Causally, defection dominates: whatever the twin does, defecting gains
    T - R or P - S."""
    rows = [{"r": r, "cooperate": round(r * R + (1 - r) * S, 4), "defect": round(r * P + (1 - r) * T, 4)}
            for r in sames]
    return {"payoffs": {"T": T, "R": R, "P": P, "S": S}, "rows": rows,
            "threshold": round((T - S) / (T - S + R - P), 4), "dominance_gain": [T - R, P - S]}


# ---------------------------------------------------------------------------
# Evidential and causal decision theory on small causal graphs
# ---------------------------------------------------------------------------
def smoking_lesion(p_lesion: float = 0.3, smoke_if_lesion: float = 0.9, smoke_if_not: float = 0.2,
                   cancer_if_lesion: float = 0.8, cancer_if_not: float = 0.05, u_smoke: float = 10,
                   u_cancer: float = -100) -> dict:
    """A lesion causes both a taste for smoking and cancer; smoking itself is harmless. Evidential decision theory
    conditions on the act: smoking is evidence of the lesion, so it lowers expected utility. Causal decision theory
    intervenes on the act: do(smoke) leaves the lesion's probability alone, so smoking gains its pleasure."""
    def p_cancer_given(smoke):
        ps_l = smoke_if_lesion if smoke else 1 - smoke_if_lesion
        ps_n = smoke_if_not if smoke else 1 - smoke_if_not
        pl = p_lesion * ps_l / (p_lesion * ps_l + (1 - p_lesion) * ps_n)
        return pl * cancer_if_lesion + (1 - pl) * cancer_if_not, pl

    pc_do = p_lesion * cancer_if_lesion + (1 - p_lesion) * cancer_if_not
    out = {}
    for smoke in (True, False):
        pc, pl = p_cancer_given(smoke)
        out["smoke" if smoke else "abstain"] = {
            "p_lesion_given": round(pl, 4), "edt": round((u_smoke if smoke else 0) + pc * u_cancer, 3),
            "cdt": round((u_smoke if smoke else 0) + pc_do * u_cancer, 3)}
    return {"acts": out, "edt_choice": max(out, key=lambda a: out[a]["edt"]),
            "cdt_choice": max(out, key=lambda a: out[a]["cdt"]), "p_cancer_do": round(pc_do, 4)}


def damascus(p_predict: float = 0.99) -> dict:
    """Death in Damascus (Gibbard and Harper 1978): Death will be where he predicts you will be, and he is reliable.
    Whatever you plan, causal expected utility says go to the other city: given you plan Damascus, Death is probably
    in Damascus, so Aleppo is better, and conversely. No choice is ratifiable (Jeffrey): each, once chosen, recommends
    the other."""
    rows = []
    for plan in ("Damascus", "Aleppo"):
        other = "Aleppo" if plan == "Damascus" else "Damascus"
        p_death_at_plan = p_predict
        cdt_stay = round(1 - p_death_at_plan, 4)          # survive if Death is elsewhere
        cdt_switch = round(p_death_at_plan, 4)
        rows.append({"plan": plan, "stay": cdt_stay, "switch_to": other, "switch": cdt_switch,
                     "ratifiable": cdt_stay >= cdt_switch})
    return {"rows": rows, "ratifiable": [r["plan"] for r in rows if r["ratifiable"]]}


def psychopath_button(p_psycho: float = 0.05, p_psycho_if_press: float = 0.9, u_world: float = 10.0,
                      u_die: float = -100.0) -> dict:
    """Egan (2007): pressing a button would kill all psychopaths. Paul would like that, unless he is one himself;
    he thinks it unlikely that he is, but only a psychopath would press. Causal expected utility uses the
    unconditional credence and says press; once he decides to, his credence that he is a psychopath rises and it says
    do not. Evidential expected utility conditions on pressing and says do not, as almost everyone judges."""
    def value(q):
        return (1 - q) * u_world + q * u_die
    cdt_press = value(p_psycho)
    cdt_after = value(p_psycho_if_press)
    edt_press = value(p_psycho_if_press)
    return {"p_psycho": p_psycho, "p_if_press": p_psycho_if_press, "cdt_press": round(cdt_press, 3),
            "cdt_press_once_decided": round(cdt_after, 3), "edt_press": round(edt_press, 3), "not_press": 0.0,
            "cdt_choice": "press" if cdt_press > 0 else "refrain", "edt_choice": "press" if edt_press > 0 else "refrain"}


# ---------------------------------------------------------------------------
# Dynamic choice: Ulysses and the sirens
# ---------------------------------------------------------------------------
def ulysses() -> dict:
    """Now Ulysses prefers sailing past to staying home, and staying home to being wrecked; he knows that when he hears
    the sirens he will prefer to steer to them. A naive chooser plans to sail past, hears them, and is wrecked. A
    sophisticated chooser predicts his future choice and settles for being bound (or stays home); a resolute chooser
    (McClennen 1990) sails free and sticks to the plan."""
    now = {"past the sirens, free": 3, "past the sirens, bound": 2.5, "home": 1, "wrecked": 0}
    later_steers_to_sirens = True
    naive = "wrecked" if later_steers_to_sirens else "past the sirens, free"
    options_for_sophisticate = {"sail free": "wrecked", "sail bound": "past the sirens, bound", "stay home": "home"}
    soph = max(options_for_sophisticate, key=lambda k: now[options_for_sophisticate[k]])
    return {"now": now, "naive": naive, "sophisticated": options_for_sophisticate[soph], "soph_plan": soph,
            "resolute": "past the sirens, free"}


def discounting(sooner: float = 100.0, later: float = 150.0, gap: int = 5, k: float = 1.0, delta: float = 0.9,
                horizon: int = 30) -> dict:
    """Strotz (1956), Ainslie (1975): 100 on day t or 150 on day t + 5. Exponential discounting (delta^t) ranks the
    pair the same way from every distance; hyperbolic discounting (1 / (1 + k t)) prefers the larger, later reward
    from far away and the smaller, sooner one up close: a preference reversal, so a plan made today is abandoned."""
    rows = []
    for t in range(horizon + 1):
        hs, hl = sooner / (1 + k * t), later / (1 + k * (t + gap))
        es, el = sooner * delta ** t, later * delta ** (t + gap)
        rows.append({"t": t, "hyp_sooner": round(hs, 4), "hyp_later": round(hl, 4), "exp_sooner": round(es, 4),
                     "exp_later": round(el, 4)})
    hyp_pick = ["sooner" if r["hyp_sooner"] > r["hyp_later"] + 1e-12 else "later" for r in rows]
    exp_pick = ["sooner" if r["exp_sooner"] > r["exp_later"] + 1e-12 else "later" for r in rows]
    switch = next(r["t"] for r, p in zip(rows, hyp_pick) if p == "later")
    return {"rows": rows, "hyp_pick": hyp_pick, "exp_pick": exp_pick, "hyp_switch_day": switch,
            "exp_consistent": len(set(exp_pick)) == 1, "k": k, "delta": delta}


# ---------------------------------------------------------------------------
# Good's theorem: the value of information
# ---------------------------------------------------------------------------
def good_theorem(problems: int = 2000, seed: int = 1967) -> dict:
    """Good (1967): for an expected utility maximizer, free information never lowers expected utility. Checked on 2000
    random problems (2 states, 3 acts, a noisy binary test): the value of information is never negative, and
    positive exactly when the test could change the choice. For a risk-weighted agent (r(p) = p^2) a counterexample
    is found (Buchak 2010)."""
    rng = np.random.default_rng(seed)
    neg, pos, minv = 0, 0, 1e9
    for _ in range(problems):
        prior = rng.random()
        U = rng.normal(0, 1, (3, 2))                       # acts x states
        acc = 0.5 + 0.5 * rng.random()
        best_now = max(U[a] @ [prior, 1 - prior] for a in range(3))
        voi_val = 0.0
        for signal in (0, 1):
            like = np.array([acc if signal == 0 else 1 - acc, 1 - acc if signal == 0 else acc])
            joint = np.array([prior, 1 - prior]) * like
            ps = joint.sum()
            post = joint / ps
            voi_val += ps * max(U[a] @ post for a in range(3))
        voi = voi_val - best_now
        minv = min(minv, voi)
        neg += voi < -1e-12
        pos += voi > 1e-12
    # a risk-weighted agent who loses by looking
    r = lambda p: p ** 2   # noqa: E731
    found = None
    for _ in range(20000):
        prior = rng.random()
        U = rng.normal(0, 1, (2, 2))
        acc = 0.5 + 0.5 * rng.random()

        def val(a, pst):
            return reu([(U[a][0], pst[0]), (U[a][1], pst[1])], lambda x: x, r)
        now = max(val(a, [prior, 1 - prior]) for a in range(2))
        # the plan 'look, then choose the best act for each signal', evaluated as one REU lottery over outcomes
        outcomes = []
        for signal in (0, 1):
            like = np.array([acc if signal == 0 else 1 - acc, 1 - acc if signal == 0 else acc])
            joint = np.array([prior, 1 - prior]) * like
            post = joint / joint.sum()
            a = max(range(2), key=lambda k: val(k, post))
            for s in (0, 1):
                outcomes.append((U[a][s], joint[s]))
        look = reu(outcomes, lambda x: x, r)
        if look < now - 0.05:
            found = {"prior": round(float(prior), 3), "accuracy": round(float(acc), 3),
                     "reu_now": round(float(now), 4), "reu_look": round(float(look), 4)}
            break
    return {"problems": problems, "negative": int(neg), "positive": int(pos), "min_voi": round(float(minv), 6),
            "reu_counterexample": found}


def voi_example(prior: float = 0.4, accuracy: float = 0.8) -> dict:
    """Good's theorem drawn: two states (rain, dry), three acts whose expected utilities are straight lines in
    q = P(rain); the value of choosing well is their upper envelope, which is convex. A test splits the prior into
    two posteriors whose average is the prior, so by Jensen the expected envelope after the test is at least the
    envelope now: the value of information is never negative."""
    acts = {"umbrella": (0.6, 0.4), "no umbrella": (0.0, 1.0), "stay in": (0.55, 0.55)}

    def env(q):
        vals = {a: q * r + (1 - q) * d for a, (r, d) in acts.items()}
        best = max(vals, key=vals.get)
        return vals[best], best
    p_says_rain = prior * accuracy + (1 - prior) * (1 - accuracy)
    q_rain = prior * accuracy / p_says_rain
    q_dry = prior * (1 - accuracy) / (1 - p_says_rain)
    now, act_now = env(prior)
    v_rain, a_rain = env(q_rain)
    v_dry, a_dry = env(q_dry)
    after = p_says_rain * v_rain + (1 - p_says_rain) * v_dry
    return {"acts": {a: list(v) for a, v in acts.items()}, "prior": prior, "accuracy": accuracy,
            "p_says_rain": round(p_says_rain, 4), "q_rain": round(q_rain, 4), "q_dry": round(q_dry, 4),
            "now": round(now, 4), "act_now": act_now, "v_rain": round(v_rain, 4), "act_rain": a_rain,
            "v_dry": round(v_dry, 4), "act_dry": a_dry, "after": round(after, 4), "voi": round(after - now, 4)}


# ---------------------------------------------------------------------------
# The two envelopes
# ---------------------------------------------------------------------------
def two_envelopes(kmax: int = 40) -> dict:
    """One envelope holds x, the other 2x. 'If mine holds a, the other holds 2a or a/2 with even odds, so switching gains
    a/4 on average': the argument assumes every amount is equally likely to be the smaller, an improper prior. With a
    proper prior P(x = 2^k) proportional to q^k and a finite expected amount (q = 0.4), switching gains only at the
    smallest amount and loses at every other, and averages zero. Broome's prior (q = 2/3) makes the gain positive at
    every amount, but only because the expected amount is infinite."""
    def table(q):
        px = np.array([q ** k for k in range(kmax)])
        px /= px.sum()
        rows = []
        total = 0.0
        for k in range(kmax + 1):
            a = 2.0 ** k
            # observe a: either a is the smaller (x = a, prob px[k]) or the larger (x = a/2, prob px[k-1])
            ps = px[k] / 2 if k < kmax else 0.0
            pl = px[k - 1] / 2 if k >= 1 else 0.0
            if ps + pl == 0:
                continue
            gain = (ps * a + pl * (-a / 2)) / (ps + pl)
            total += (ps + pl) * gain
            if k <= 6:
                rows.append({"amount": int(a), "p_smaller": round(float(ps / (ps + pl)), 4),
                             "gain": round(float(gain), 4)})
        return rows, round(float(total), 6)
    proper, tot = table(0.4)
    broome, _ = table(2 / 3)
    return {"q": 0.4, "proper": proper, "proper_total": tot, "broome": broome}


# ---------------------------------------------------------------------------
# Parfit's hitchhiker: acts against policies
# ---------------------------------------------------------------------------
def hitchhiker(accuracy: float = 0.99, reward: float = 1000.0, death: float = -1e6) -> dict:
    """Parfit (1984): you are dying in the desert; a driver who reads faces almost perfectly will rescue you only if he
    predicts you will pay him 1,000 once in town. In town, paying is a pure loss, so an act-by-act maximizer (causal or
    evidential, once rescued) will not pay, and so is predicted not to, and is left to die. Evaluated as policies, as
    functional decision theory evaluates them (Yudkowsky and Soares 2017), 'pay' is far better."""
    pay = accuracy * (-reward) + (1 - accuracy) * death
    refuse = (1 - accuracy) * 0.0 + accuracy * death
    return {"accuracy": accuracy, "policy_pay": round(pay, 1), "policy_refuse": round(refuse, 1),
            "in_town_pay": -reward, "in_town_refuse": 0.0}

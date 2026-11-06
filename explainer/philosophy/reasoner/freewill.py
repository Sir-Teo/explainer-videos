"""Free will, built (Part 32).

* The consequence argument's rules on a model: an agent's options are actions, each with a set of outcomes it might
  lead to; 'N p' ('p, and no one has any choice about whether p') holds when p is true and no available action
  guarantees not-p. Rule alpha (from box p, infer N p) and the repaired rule beta-box (from N p and box(p -> q), infer
  N q) hold on every proposition; rule beta (from N p and N(p -> q), infer N q) fails, on McKay and Johnson's (1996)
  coin, because it implies agglomeration (N p, N q, so N(p & q)).
* The Lazy Argument and Chrysippus's 'co-fated' events: a toy causal chain.
* Van Inwagen's rollback: replays of one indeterministic moment converge to a frequency.
* Schurger, Sitt and Dehaene (2012): a leaky stochastic accumulator; averaged backward from threshold crossings, its
  noise alone builds a readiness potential.
* Self-prediction: no public prediction of a contrarian agent can be right; a diagonal over any list of predictors.
* Moral luck: identical drivers, different outcomes.
"""

from __future__ import annotations

import itertools
import math

import numpy as np


# ---------------------------------------------------------------------------
# The N operator on a model of options
# ---------------------------------------------------------------------------
class Options:
    """Worlds, the actual one, and the agent's available actions, each the set of worlds it might lead to."""

    def __init__(self, worlds, actual, actions):
        self.worlds = list(worlds)
        self.actual = actual
        self.actions = {a: frozenset(ws) for a, ws in actions.items()}
        self.all = frozenset(self.worlds)

    def can_ensure(self, X) -> bool:
        """Some available action leads only to worlds in X."""
        return any(ws <= frozenset(X) for ws in self.actions.values())

    def N(self, X) -> bool:
        """X is true, and the agent has no choice about it: nothing it can do guarantees not-X."""
        X = frozenset(X)
        return self.actual in X and not self.can_ensure(self.all - X)

    def box(self, X) -> bool:
        return frozenset(X) == self.all

    def props(self):
        for r in range(len(self.worlds) + 1):
            for c in itertools.combinations(self.worlds, r):
                yield frozenset(c)

    def imp(self, X, Y):
        return (self.all - frozenset(X)) | frozenset(Y)


def coin() -> Options:
    """McKay and Johnson (1996): I do not toss a coin, though I could. If I toss, it lands heads or tails, and nothing
    I can do settles which."""
    return Options(["not tossed", "heads", "tails"], "not tossed",
                   {"refrain": ["not tossed"], "toss": ["heads", "tails"]})


def rule_check(m: Options | None = None) -> dict:
    """Every instance of the rules on every pair of propositions of the model: alpha and beta-box never fail; beta
    fails, and so does agglomeration, at p = 'no heads', q = 'no tails'."""
    m = m or coin()
    P = list(m.props())
    alpha = sum(1 for p in P if m.box(p) and not m.N(p))
    beta, beta_box, agg = [], 0, []
    for p in P:
        for q in P:
            if m.N(p) and m.N(m.imp(p, q)) and not m.N(q):
                beta.append((sorted(p), sorted(q)))
            if m.N(p) and m.box(m.imp(p, q)) and not m.N(q):
                beta_box += 1
            if m.N(p) and m.N(q) and not m.N(p & q):
                agg.append((sorted(p), sorted(q)))
    no_heads = frozenset(["not tossed", "tails"])
    no_tails = frozenset(["not tossed", "heads"])
    return {"props": len(P), "pairs": len(P) ** 2, "alpha_fail": alpha, "beta_fail": len(beta),
            "beta_box_fail": beta_box, "agg_fail": len(agg), "beta_examples": beta[:3],
            "N_no_heads": m.N(no_heads), "N_no_tails": m.N(no_tails), "N_both": m.N(no_heads & no_tails),
            "worlds": m.worlds, "actions": {a: sorted(ws) for a, ws in m.actions.items()}}


def frankfurt() -> dict:
    """Frankfurt (1969), on the same model of options. Jones decides to shoot Smith, on his own. Black, unseen, would
    have intervened at the first sign that Jones was about to decide otherwise, and made him shoot anyway. Jones has
    no choice about whether he shoots (N holds), yet he shoots on his own; what he could have done otherwise is only
    to show the sign, a 'flicker of freedom': he has a choice about whether he shoots on his own."""
    m = Options(["shoots on his own", "shows the sign; Black makes him shoot"], "shoots on his own",
                {"decide to shoot": ["shoots on his own"],
                 "begin to decide otherwise": ["shows the sign; Black makes him shoot"]})
    shoots = frozenset(m.worlds)
    own = frozenset(["shoots on his own"])
    return {"worlds": m.worlds, "N_shoots": m.N(shoots), "N_on_his_own": m.N(own),
            "can_avoid_shooting": m.can_ensure(m.all - shoots), "can_avoid_own": m.can_ensure(m.all - own)}


# ---------------------------------------------------------------------------
# Van Inwagen's rollback
# ---------------------------------------------------------------------------
def rollback(p_truth: float = 0.7, replays: int = 1000, seed: int = 2000) -> dict:
    """Alice, at one undetermined moment, tells the truth or lies. God rolls the universe back to just before and lets
    it run again, a thousand times. The share of replays in which she tells the truth settles down near the
    underlying chance; which way any one replay goes seems a matter of luck (van Inwagen 2000)."""
    rng = np.random.default_rng(seed)
    out = (rng.random(replays) < p_truth).astype(int)
    running = np.cumsum(out) / np.arange(1, replays + 1)
    checkpoints = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    return {"p": p_truth, "replays": replays, "first": out[:40].tolist(),
            "running": [round(float(running[k - 1]), 4) for k in checkpoints], "checkpoints": checkpoints,
            "truths": int(out.sum()), "curve": [round(float(x), 4) for x in running[::5]]}


# ---------------------------------------------------------------------------
# Libet and the leaky stochastic accumulator
# ---------------------------------------------------------------------------
def accumulator(trials: int = 1000, dt: float = 0.001, drift: float = 0.1, leak: float = 0.5, noise: float = 0.1,
                threshold: float = 0.298, max_t: float = 20.0, window: float = 2.0, seed: int = 2012) -> dict:
    """Schurger, Sitt and Dehaene (2012): x' = I - k x + c xi(t), with no decision anywhere in it. A movement happens
    when x first crosses a threshold. Average x backward from each crossing and a slow build-up appears, like
    Libet's readiness potential, though it is only the noise that happened to carry x over. Parameters of the kind
    the paper fitted (drift 0.1, leak 0.5, noise 0.1, threshold 0.298; time in seconds)."""
    rng = np.random.default_rng(seed)
    n = int(max_t / dt)
    w = int(window / dt)
    traces, waits, examples = [], [], []
    sd = noise * math.sqrt(dt)
    for k in range(trials):
        x = 0.0
        hist = np.empty(n)
        crossed = None
        z = rng.normal(0, 1, n)
        for i in range(n):
            x += (drift - leak * x) * dt + sd * z[i]
            hist[i] = x
            if x >= threshold:
                crossed = i
                break
        if crossed is None:
            continue
        waits.append(crossed * dt)
        if crossed >= w:
            traces.append(hist[crossed - w:crossed + 1])
        if len(examples) < 5:
            examples.append([round(float(v), 4) for v in hist[:crossed + 1:20]])
    traces = np.array(traces)
    mean = traces.mean(axis=0)
    t = np.linspace(-window, 0, w + 1)
    onset = None
    base = mean[0]
    for i, v in enumerate(mean):
        if v - base > 0.5 * (mean[-1] - base):
            onset = round(float(t[i]), 3)
            break
    return {"trials": trials, "crossed": len(waits), "averaged": int(len(traces)),
            "mean_wait": round(float(np.mean(waits)), 3), "median_wait": round(float(np.median(waits)), 3),
            "rp_t": [round(float(v), 3) for v in t[::20]], "rp": [round(float(v), 4) for v in mean[::20]],
            "rp_start": round(float(mean[0]), 4), "rp_end": round(float(mean[-1]), 4), "half_rise": onset,
            "examples": examples, "wait_hist": np.histogram(waits, bins=10, range=(0, 20))[0].tolist(),
            "params": {"drift": drift, "leak": leak, "noise": noise, "threshold": threshold}}


# ---------------------------------------------------------------------------
# Self-prediction
# ---------------------------------------------------------------------------
def self_prediction(n_predictors: int = 6) -> dict:
    """A contrarian agent reads any public prediction of its next act (left or right) and does the other. Every one of
    the two possible predictions is wrong (MacKay 1960). More generally, list any predictors you like, each a
    function from situations to predicted acts; the diagonal agent, in situation k, does the opposite of what
    predictor k predicts there, so it differs from every predictor somewhere: Cantor's diagonal, as in Part 7."""
    acts = ["left", "right"]
    contrarian = {p: ("right" if p == "left" else "left") for p in acts}
    public = [{"prediction": p, "act": contrarian[p], "right": contrarian[p] == p} for p in acts]
    rng = np.random.default_rng(1960)
    table = rng.integers(0, 2, (n_predictors, n_predictors)).tolist()
    diag = [1 - table[k][k] for k in range(n_predictors)]
    differs = [any(diag[s] != table[k][s] for s in range(n_predictors)) for k in range(n_predictors)]
    return {"public": public, "public_right": sum(r["right"] for r in public), "table": table, "diagonal": diag,
            "differs": differs}


# ---------------------------------------------------------------------------
# Moral luck
# ---------------------------------------------------------------------------
def moral_luck(drivers: int = 10000, p_child: float = 0.0005, seed: int = 1976) -> dict:
    """Nagel (1979), Williams (1976): ten thousand drivers equally careless, each running one red light; whether a
    child is on the crossing is luck. A few kill someone; the rest go home. Same choice, same character, different
    blame."""
    rng = np.random.default_rng(seed)
    hit = int((rng.random(drivers) < p_child).sum())
    return {"drivers": drivers, "p": p_child, "killed": hit, "home": drivers - hit}


# ---------------------------------------------------------------------------
# Lewis's local miracles, on a reversible deterministic world
# ---------------------------------------------------------------------------
def _rev_step(prev, cur):
    """A second-order reversible cellular automaton: x_{t+1} = (x_{t, c-1} xor x_{t, c} xor x_{t, c+1}) xor x_{t-1},
    on a ring. Deterministic in both directions: x_{t-1} = f(x_t) xor x_{t+1}."""
    f = np.roll(cur, 1) ^ cur ^ np.roll(cur, -1)
    return f ^ prev


def miracles(width: int = 61, steps: int = 30, seed: int = 1979) -> dict:
    """Lewis (1979, 1981). In a deterministic world an agent's cell c at time T has the value it has. Consider a world
    where it differs. With a small miracle, one cell at time T-1 differs and the laws resume: the past up to T-1 is
    exactly ours. Without any miracle, the counterfactual world obeys the laws at every time; running them backward
    from a state that differs at c, the difference spreads into the past at one cell per step, so at time 0 a whole
    stretch of the world differs. Lewis: 'I could have done otherwise' needs only the small miracle, not a different
    remote past."""
    rng = np.random.default_rng(seed)
    x0 = rng.integers(0, 2, width).astype(np.uint8)
    x1 = rng.integers(0, 2, width).astype(np.uint8)
    hist = [x0, x1]
    for _ in range(steps - 1):
        hist.append(_rev_step(hist[-2], hist[-1]))
    H = np.array(hist)                                       # rows t = 0 .. steps
    c = width // 2
    T = steps
    # with a miracle: change cell c at T-1, then let the laws run to T
    alt_prev = H[T - 1].copy()
    alt_prev[c] ^= 1
    alt_T = _rev_step(H[T - 2], alt_prev)
    miracle_changes_act = bool(alt_T[c] != H[T][c])
    # without a miracle: the lawful world whose last two states are (H[T-1], H[T] with c flipped); run backward
    a_next = H[T].copy()
    a_next[c] ^= 1
    a_cur = H[T - 1].copy()
    back = [a_next, a_cur]
    for _ in range(T - 1):
        f = np.roll(a_cur, 1) ^ a_cur ^ np.roll(a_cur, -1)
        a_prev = f ^ a_next
        back.append(a_prev)
        a_next, a_cur = a_cur, a_prev
    B = np.array(back[::-1])                                  # rows t = 0 .. T
    diff = (B != H).astype(int)
    per_t = diff.sum(axis=1).tolist()
    return {"width": width, "steps": steps, "agent": c, "miracle_cells": 1, "miracle_changes_act": miracle_changes_act,
            "lawful_diff_at_0": int(per_t[0]), "lawful_diff_per_t": per_t, "diff": diff.tolist(),
            "actual": H.tolist()}


# ---------------------------------------------------------------------------
# Libet interrupted: the accumulator's prediction
# ---------------------------------------------------------------------------
def interruptus(trials: int = 4000, dt: float = 0.001, drift: float = 0.1, leak: float = 0.5, noise: float = 0.1,
                threshold: float = 0.298, boost: float = 1.0, seed: int = 2013) -> dict:
    """Schurger, Sitt and Dehaene (2012) tested their model by interrupting subjects with a click at random moments
    and asking for an immediate movement. In the model the click adds a strong drift; the time to reach threshold
    then depends on where the noise had already carried x. Trials interrupted when x was high give the fastest
    responses: binned by x at the click, mean response times fall steadily, as the paper's data did."""
    rng = np.random.default_rng(seed)
    sd = noise * math.sqrt(dt)
    xs, rts = [], []
    for _ in range(trials):
        x = 0.0
        t_click = rng.uniform(2.0, 8.0)
        n = int(t_click / dt)
        z = rng.normal(0, 1, n)
        crossed = False
        for i in range(n):
            x += (drift - leak * x) * dt + sd * z[i]
            if x >= threshold:
                crossed = True
                break
        if crossed:
            continue                                         # moved spontaneously before the click
        x_click = x
        rt = 0.0
        while x < threshold and rt < 3.0:
            x += (drift + boost - leak * x) * dt + sd * rng.normal()
            rt += dt
        xs.append(x_click)
        rts.append(rt)
    xs, rts = np.array(xs), np.array(rts)
    qs = np.quantile(xs, [0, 0.25, 0.5, 0.75, 1.0])
    bins = []
    for k in range(4):
        m = (xs >= qs[k]) & (xs <= qs[k + 1])
        bins.append({"x_low": round(float(qs[k]), 3), "x_high": round(float(qs[k + 1]), 3),
                     "mean_rt_ms": round(float(rts[m].mean() * 1000), 1), "n": int(m.sum())})
    return {"trials": trials, "used": int(len(xs)), "bins": bins,
            "corr": round(float(np.corrcoef(xs, rts)[0, 1]), 3), "boost": boost}


# ---------------------------------------------------------------------------
# Degrees of responsibility (Chockler and Halpern 2004)
# ---------------------------------------------------------------------------
def _degree(variables, actual, outcome, who):
    """Degree of responsibility of `who` for the outcome: 1 / (k + 1), where k is the smallest number of other
    variables whose values must change for who's value to become critical (flipping it would then flip the
    outcome), with the outcome unchanged by those other changes."""
    import itertools as it
    others = [v for v in variables if v != who]
    base = outcome(actual)
    for k in range(len(others) + 1):
        for S in it.combinations(others, k):
            w = dict(actual)
            for v in S:
                w[v] = 1 - w[v]
            if outcome(w) != base:
                continue
            w2 = dict(w)
            w2[who] = 1 - w2[who]
            if outcome(w2) != base:
                return 1 / (k + 1), k
    return 0.0, None


def responsibility() -> dict:
    """Chockler and Halpern (2004), a structural-model measure. In an eleven-member vote, each majority voter's degree
    of responsibility for the outcome is 1 if the vote was 6 to 5, and 1/6 if it was 11 to 0. For a harm with many
    hands (harm happens if the designer ships a flaw and either the deployer skips the test or the overseer is
    absent; all three failed), the designer's degree is 1, the deployer's and the overseer's 1/2 each."""
    rows = []
    for yes in range(6, 12):
        voters = [f"v{i}" for i in range(11)]
        actual = {v: (1 if i < yes else 0) for i, v in enumerate(voters)}
        out = lambda w: int(sum(w.values()) >= 6)      # noqa: E731
        d, k = _degree(voters, actual, out, "v0")
        rows.append({"vote": f"{yes}-{11 - yes}", "degree": round(d, 4), "k": k})
    names = ["designer", "deployer", "overseer"]
    actual = {"designer": 1, "deployer": 1, "overseer": 1}       # 1: failed
    harm = lambda w: int(w["designer"] and (w["deployer"] or w["overseer"]))   # noqa: E731
    hands = {n: round(_degree(names, actual, harm, n)[0], 4) for n in names}
    return {"votes": rows, "hands": hands}


# ---------------------------------------------------------------------------
# Reasons-responsiveness (Fischer and Ravizza 1998)
# ---------------------------------------------------------------------------
def reasons_responsive(desire: int = 5, reasons=tuple(range(11))) -> dict:
    """Three mechanisms face eleven scenarios, in which the reason to refrain from taking a drug has strength 0 to 10
    against a desire of strength 5. A reason is sufficient when it outweighs the desire. Weak reactivity: the
    mechanism refrains in at least one scenario with a sufficient reason. Regular receptivity: the scenarios in which
    it refrains form an intelligible pattern (here: if it refrains at r, it refrains at every stronger reason).
    Moderate reasons-responsiveness is both."""
    agents = {
        "a responsive agent": lambda r: r > desire,
        "an erratic agent": lambda r: r in (7, 10),
        "a compulsive agent": lambda r: False,
    }
    out = {}
    for name, refrains in agents.items():
        row = [bool(refrains(r)) for r in reasons]
        weak = any(row[i] for i, r in enumerate(reasons) if r > desire)
        regular = all(row[j] for i in range(len(reasons)) if row[i] for j in range(i, len(reasons)))
        strong = all(row[i] for i, r in enumerate(reasons) if r > desire)
        out[name] = {"refrains": row, "weak": weak, "regular": regular, "strong": strong,
                     "moderate": weak and regular}
    return {"desire": desire, "reasons": list(reasons), "agents": out}


# ---------------------------------------------------------------------------
# Answers fixed in advance: the CHSH bound
# ---------------------------------------------------------------------------
def chsh_local() -> dict:
    """If each particle's answer to each possible setting were fixed in advance (a function of the past), and the
    settings were chosen independently, then for every one of the 16 deterministic assignments the CHSH sum
    E(0,0) + E(0,1) + E(1,0) - E(1,1) is +2 or -2; mixtures of them stay within [-2, 2]. Quantum mechanics predicts,
    and experiments find, values near 2 sqrt 2 = 2.83 (Part 26). The free will theorem rests on the same logic."""
    import itertools as it
    vals = []
    for a0, a1, b0, b1 in it.product((-1, 1), repeat=4):
        s = a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1
        vals.append(s)
    return {"strategies": len(vals), "max": max(vals), "min": min(vals), "values": sorted(set(vals)),
            "tsirelson": round(2 * math.sqrt(2), 4)}


# ---------------------------------------------------------------------------
# Determinism at one level, alternatives at another (List)
# ---------------------------------------------------------------------------
def levels(micro: int = 900, seed: int = 2019) -> dict:
    """List (2014, 2019): a world can be deterministic at the physical level and indeterministic at the level of
    agency. 900 microstates each have exactly one successor (a fixed function). Group them into three agent-level
    states (deliberating, tea, coffee) and ask, from the agent-level state alone, what follows: the transition
    probabilities are not 0 or 1 (from deliberating: tea 0.45, coffee 0.40, still deliberating 0.15). Refine the
    grouping to single microstates and determinism returns."""
    rng = np.random.default_rng(seed)
    names = ["deliberating", "tea", "coffee"]
    size = micro // 3
    frac = {"deliberating": {"deliberating": 0.15, "tea": 0.45, "coffee": 0.40},
            "tea": {"deliberating": 0.10, "tea": 0.90, "coffee": 0.0},
            "coffee": {"deliberating": 0.15, "tea": 0.0, "coffee": 0.85}}
    succ = np.zeros(micro, dtype=int)
    for m_i, m in enumerate(names):
        idx = rng.permutation(np.arange(m_i * size, (m_i + 1) * size))
        start = 0
        for n_i, n in enumerate(names):
            k = int(round(frac[m][n] * size))
            for i in idx[start:start + k]:
                succ[i] = rng.integers(n_i * size, (n_i + 1) * size)
            start += k

    def macro(i):
        return names[int(i) // size]
    counts = {m: {n: 0 for n in names} for m in names}
    for i in range(micro):
        counts[macro(i)][macro(succ[i])] += 1
    probs = {m: {n: round(c / size, 4) for n, c in row.items()} for m, row in counts.items()}
    # the finest grouping: each microstate alone has one successor, so every row is a single 1
    fine_det = len(succ) == micro
    return {"micro": micro, "macro": names, "probs": probs, "fine_deterministic": fine_det,
            "examples": [{"micro": int(i), "next_micro": int(succ[i]), "next_macro": macro(succ[i])}
                         for i in range(0, size, 60)],
            "deterministic_rows": [m for m in names if max(probs[m].values()) == 1.0]}


# ---------------------------------------------------------------------------
# A torn decision: how a tiny difference could decide
# ---------------------------------------------------------------------------
def torn_decision(gamma: float = 0.5, dt: float = 0.001, exponents=(3, 6, 9, 12, 15, 20, 30)) -> dict:
    """A choice as a ball balanced on the hump of a double well, x'' = x - x^3 - gamma x' (Kane's and Balaguer's
    'torn decisions'). Near the top any offset eps grows like e^(lambda t), lambda = (-gamma + sqrt(gamma^2 + 4)) / 2,
    so the ball falls to the side of the sign of eps after a time about ln(1/eps) / lambda: every factor of ten
    smaller adds the same delay, ln 10 / lambda. However small the difference, even at a quantum scale, it decides,
    and quickly; if it is undetermined, so is the choice, and whether that is freedom or mere luck is the question."""
    lam = (-gamma + math.sqrt(gamma ** 2 + 4)) / 2
    rows = []
    for k in exponents:
        for sign in (1, -1):
            x, v, t = sign * 10.0 ** -k, 0.0, 0.0
            while abs(x) < 0.5:
                # RK4 step
                def f(x_, v_):
                    return v_, x_ - x_ ** 3 - gamma * v_
                k1 = f(x, v)
                k2 = f(x + dt / 2 * k1[0], v + dt / 2 * k1[1])
                k3 = f(x + dt / 2 * k2[0], v + dt / 2 * k2[1])
                k4 = f(x + dt * k3[0], v + dt * k3[1])
                x += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
                v += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
                t += dt
            if sign == 1:
                rows.append({"exponent": k, "time": round(t, 2), "side": "right" if x > 0 else "left"})
            else:
                rows[-1]["mirror"] = "left" if x < 0 else "right"
    slope = (rows[-1]["time"] - rows[0]["time"]) / (exponents[-1] - exponents[0])
    return {"gamma": gamma, "lambda": round(lam, 4), "rows": rows, "slope": round(slope, 3),
            "ln10_over_lambda": round(math.log(10) / lam, 3)}


# ---------------------------------------------------------------------------
# Two ledgers for the careless drivers
# ---------------------------------------------------------------------------
def blame_ledgers(drivers: int = 10000, p_child: float = 0.0005, killed: int = 6) -> dict:
    """The same equally careless drivers, blamed two ways. By outcome, the few who kill carry all the blame (one unit
    each) and the rest none. By the risk each imposed (Zimmerman 2002: luck changes what we are responsible for,
    not how responsible we are), every driver carries p units, and the total is the expected harm. That some driver
    kills is almost certain; which one is luck."""
    p_any = 1 - (1 - p_child) ** drivers
    return {"drivers": drivers, "p": p_child, "killed": killed, "outcome_each_killer": 1.0,
            "outcome_total": float(killed), "risk_each": p_child, "risk_total": round(drivers * p_child, 4),
            "p_some_victim": round(p_any, 4), "expected_victims": round(drivers * p_child, 2)}


# ---------------------------------------------------------------------------
# Determinism is not inevitability (Dennett): a deterministic avoider
# ---------------------------------------------------------------------------
def avoider(width: int = 9, height: int = 5, steps: int = 400, seed: int = 2003) -> dict:
    """Dennett (1984, 2003): in a deterministic world some things are avoided, and avoiding is a real capacity. Rocks
    fall one row a step down a strip of `width` columns (a new rock each step, at a column fixed by the seed); an
    agent on the bottom row either stays put (blind) or looks one row up and steps aside when a rock is about to land
    on it (sighted). Everything is determined: rerunning gives the same history. Yet the sighted agent avoids every
    rock that would have hit it, and the counterfactual is true each time: had it stayed, it would have been hit."""
    rng = np.random.default_rng(seed)
    spawns = rng.integers(0, width, size=steps).tolist()

    def run(sighted: bool):
        rocks = []                 # (row, col); row 0 is the top, row height-1 lands on the agent's row
        pos, hits, dodges, frames = width // 2, 0, 0, []
        for t in range(steps):
            rocks.append((0, spawns[t]))
            # look: rocks one row above the agent will land next step
            landing = {c for r, c in rocks if r == height - 2}
            if sighted and pos in landing:
                for cand in (pos - 1, pos + 1, pos - 2, pos + 2):
                    if 0 <= cand < width and cand not in landing:
                        pos = cand
                        dodges += 1
                        break
            rocks = [(r + 1, c) for r, c in rocks]
            hits += sum(1 for r, c in rocks if r == height - 1 and c == pos)
            rocks = [(r, c) for r, c in rocks if r < height - 1]
            if t < 24:
                frames.append({"pos": pos, "rocks": [list(x) for x in rocks]})
        return {"hits": hits, "dodges": dodges, "frames": frames}
    blind, sighted, again = run(False), run(True), run(True)
    return {"width": width, "height": height, "steps": steps, "blind_hits": blind["hits"],
            "sighted_hits": sighted["hits"], "dodges": sighted["dodges"],
            "deterministic": sighted == again, "frames": sighted["frames"]}

"""Psyche's motivation (Part 28): homeostasis, a defended body weight, a hijacked reward, arousal, incentive
salience, self-perception, achievement motivation, effort, waiting, and the meta-analysis of a literature.

* :func:`thermostat`: a negative-feedback loop, dx/dt = -k (x - set) + d(t) - ki * integral, with its exponential
  return to the set point; with a constant disturbance D, proportional control settles at set + D / k, and an
  integral term removes that steady error.
* :func:`body_weight`: energy balance.  Expenditure rises with weight (``per_kg`` kcal a day for each kilogram, as in
  Hall et al.'s 2011 rule of thumb), so weight settles where intake and expenditure meet; with a defended set point,
  hunger raises intake and thrift lowers expenditure as weight falls below it.  :func:`static_rule` is the
  3,500-kcal-a-pound arithmetic that ignores the loop.
* :func:`self_stimulation`: Part 17's learner given two levers, food (worth as much as the animal is hungry) and a
  stimulating current (worth the same whatever its state), with the animal's energy store tracked.
* :func:`arousal_performance`: a sketch of the later reading of Yerkes and Dodson: arousal speeds and narrows; a
  hard task needs cues that narrowing loses first.
* :func:`salt_cue`: a cue learned while it predicted something nasty, then tested in a new state: a cached
  (model-free) value against Zhang, Berridge, Tindell, Smith and Aldridge's (2009) incentive value, which is
  recomputed from the state at once.
* :func:`self_perception`: Bem's self-perception as Bayes: an observer (the child) infers its own interest from what
  it did and why; a promised reward explains the doing, so less interest is inferred (Kelley's discounting).
* :func:`atkinson`: Atkinson's 1957 risk-taking model, T = (M_s - M_af) P (1 - P).
* :func:`evc` and :func:`evc_curve`: the expected value of control (Shenhav, Botvinick and Cohen 2013) in its
  simplest form; :func:`intensity` over difficulty (Brehm's motivational intensity: effort rises with difficulty,
  then drops to nothing when success is not worth its price).
* :func:`remaining_wait` and :func:`give_up_time`: McGuire and Kable's (2013) account of giving up: when the time a
  reward takes is heavy-tailed, the expected remaining wait grows the longer one waits, and quitting is rational.
* :func:`confounded_delay`: delay of gratification and a later outcome when both depend on family background and
  early ability; the coefficient with and without controls.
* :func:`hedges_g`, :func:`random_effects` (DerSimonian-Laird) and :func:`pet` (Egger's regression, the
  precision-effect test); :func:`discount_titration`, the adjusting-amount procedure on a hyperbolic chooser.

Nothing here imports manim.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import norm

__all__ = ["thermostat", "body_weight", "static_rule", "self_stimulation", "arousal_performance", "salt_cue",
           "self_perception", "atkinson", "evc", "evc_curve", "intensity", "remaining_wait", "give_up_time",
           "reward_rate", "confounded_delay", "hedges_g", "random_effects", "pet", "discount_titration"]

KCAL_PER_KG = 7700.0  # energy stored in a kilogram of body tissue, the usual round figure


# --------------------------------------------------------------------------------------------- homeostasis
def thermostat(T: float = 60.0, dt: float = 0.05, k: float = 0.2, ki: float = 0.0, set_point: float = 20.0,
               x0: float = 14.0, disturbance=None) -> dict:
    """dx/dt = -k (x - set) - ki * integral(x - set) + d(t), Euler steps.  With a constant disturbance D and
    ki = 0 the loop settles at set + D / k (proportional control leaves a steady error); any ki > 0 removes it."""
    n = int(round(T / dt))
    t = np.arange(n) * dt
    x = np.empty(n)
    v, acc = x0, 0.0
    for i in range(n):
        d = disturbance(t[i]) if disturbance is not None else 0.0
        acc += (v - set_point) * dt
        v += dt * (-k * (v - set_point) - ki * acc + d)
        x[i] = v
    return {"t": t, "x": x}


def body_weight(days: int = 1100, diet=(100, 400), cut: float = 500.0, W0: float = 80.0, set_point: float = 80.0,
                rho: float = KCAL_PER_KG, base: float = 2400.0, per_kg: float = 24.0, hunger: float = 0.0,
                thrift: float = 0.0) -> dict:
    """Weight W (kg) by day.  Intake = base + hunger (set - W)+ - cut (during the diet); expenditure = base +
    per_kg (W - W0) - thrift (set - W)+.  dW/dt = (intake - expenditure) / rho.  With hunger = thrift = 0 weight has
    a settling point and no defence; with them, falling below the set point is resisted.  The steady loss under a
    cut is cut / (per_kg + hunger + thrift); the time constant is rho / (per_kg + hunger + thrift)."""
    W, In, Out = np.empty(days), np.empty(days), np.empty(days)
    w = W0
    for t in range(days):
        gap = max(set_point - w, 0.0)
        intake = base + hunger * gap - (cut if diet[0] <= t < diet[1] else 0.0)
        out = base + per_kg * (w - W0) - thrift * gap
        w += (intake - out) / rho
        W[t], In[t], Out[t] = w, intake, out
    stiff = per_kg + hunger + thrift
    return {"day": np.arange(days), "W": W, "intake": In, "out": Out, "steady_loss": cut / stiff,
            "tau_days": rho / stiff}


def static_rule(days: int = 1100, diet=(100, 400), cut: float = 500.0, W0: float = 80.0,
                rho: float = KCAL_PER_KG) -> np.ndarray:
    """The static rule: every rho kcal not eaten is a kilogram lost, for as long as the diet lasts."""
    t = np.arange(days)
    on = np.clip(t + 1 - diet[0], 0, diet[1] - diet[0])
    return W0 - cut * on / rho


# --------------------------------------------------------------------------------------------- a hijacked reward
def self_stimulation(steps: int = 3000, stim: float = 0.0, stim_value: float = 1.0, alpha: float = 0.1,
                     beta: float = 10.0, gamma: float = 0.8, seed: int = 0, bins: int = 10, meal: float = 0.1) -> dict:
    """Two levers.  Food is worth the animal's hunger h (0 sated to 1 starving) and lowers it; the current is worth
    ``stim_value`` and changes nothing.  Hunger rises by 0.01 a step and falls by ``meal`` when food is taken;
    the energy store falls by 0.01 a step and rises by ``meal`` with food (capped at 1).  A Q-learner with hunger as its
    state (optimistic start) chooses by softmax.  ``stim = 0`` leaves only the food lever.  A meal changes hunger and energy by
    ``meal``, so staying fed takes one press in ten.  Returns choices, hunger and energy."""
    rng = np.random.default_rng(seed)
    Q = np.full((bins, 2), 2.0 / (1 - gamma))  # optimistic, so both levers get tried in every state
    h, e = 0.3, 0.7
    choice, H, E = np.empty(steps, int), np.empty(steps), np.empty(steps)
    for t in range(steps):
        s = min(int(h * bins), bins - 1)
        q = Q[s].copy()
        if stim <= 0:
            q[1] = -np.inf
        p = np.exp(beta * (q - q.max()))
        p /= p.sum()
        a = int(rng.random() < p[1])
        if a == 0:
            r = h
            h, e = max(h - meal, 0.0), min(e + meal, 1.0)
        else:
            r = stim_value
        h, e = min(h + 0.01, 1.0), max(e - 0.01, 0.0)
        s2 = min(int(h * bins), bins - 1)
        nxt = Q[s2].max() if stim > 0 else Q[s2, 0]
        Q[s, a] += alpha * (r + gamma * nxt - Q[s, a])
        choice[t], H[t], E[t] = a, h, e
    return {"choice": choice, "hunger": H, "energy": E, "Q": Q}


# --------------------------------------------------------------------------------------------- arousal
def arousal_performance(a, cue_limit: float, drive_rate: float = 3.0, width: float = 0.08):
    """Performance against arousal a in [0, 1]: drive 1 - exp(-drive_rate a) times the chance the task's cue is
    still used, 1 / (1 + exp((a - cue_limit) / width)) (Easterbrook's narrowing: a hard task's cue has a low
    limit).  A sketch of the later reading, not a fit to the 1908 data."""
    a = np.asarray(a, float)
    return (1 - np.exp(-drive_rate * a)) / (1 + np.exp((a - cue_limit) / width))


# --------------------------------------------------------------------------------------------- wanting
def salt_cue(train: int = 30, test: int = 10, alpha: float = 0.2, gamma: float = 0.9, sated: float = -1.0,
             depleted: float = 1.0) -> dict:
    """A cue followed by intensely salty water.  Training, in the ordinary state, the salt is worth ``sated``;
    then the body is salt-depleted, where it would be worth ``depleted``, and the cue is presented with no salt
    (extinction).  The cached value V learns only from what is delivered; the incentive value is gamma times the
    outcome's worth in the present state, recomputed at once (Zhang et al. 2009, the multiplicative form with the
    state's factor changing sign).  Returns both values, trial by trial."""
    V, cached, incentive = 0.0, [], []
    for _ in range(train):
        V += alpha * (sated - V)
        cached.append(V)
        incentive.append(gamma * sated)
    for _ in range(test):
        cached.append(V)
        incentive.append(gamma * depleted)
        V += alpha * (0.0 - V)
    return {"trial": np.arange(train + test), "cached": np.array(cached), "incentive": np.array(incentive),
            "switch": train}


# --------------------------------------------------------------------------------------------- self-perception
def self_perception(prior: float = 0.5, base: float = -1.0, interest: float = 2.0, reward: float = 2.0) -> dict:
    """A child draws.  It likes drawing (I = 1) or not (I = 0), with prior P(I = 1) = ``prior``.  It draws with
    probability sigmoid(base + interest I + reward R).  Having drawn, it infers P(I = 1 | drew, R) by Bayes's rule;
    with R = 1 the reward explains part of the drawing, so less interest is inferred."""
    sig = lambda z: 1 / (1 + np.exp(-z))  # noqa: E731
    out = {}
    for name, R in (("no_reward", 0.0), ("reward", 1.0)):
        p1, p0 = sig(base + interest + reward * R), sig(base + reward * R)
        out[name] = float(prior * p1 / (prior * p1 + (1 - prior) * p0))
        out[name + "_p_draw"] = (float(p0), float(p1))
    return out


# --------------------------------------------------------------------------------------------- achievement
def atkinson(P, Ms: float = 1.0, Maf: float = 0.0):
    """Atkinson (1957): the tendency to approach a task with success probability P, (Ms - Maf) P (1 - P): the
    incentive of success is 1 - P, so the product peaks at P = 1/2, attracting the success-oriented and repelling
    the failure-anxious."""
    P = np.asarray(P, float)
    return (Ms - Maf) * P * (1 - P)


# --------------------------------------------------------------------------------------------- effort
def _p_success(u, difficulty: float = 1.0, slope: float = 3.0):
    return norm.cdf(slope * (u - difficulty))


def evc(reward: float, difficulty: float = 1.0, cost: float = 1.0, slope: float = 3.0) -> dict:
    """The intensity of control u >= 0 that maximizes p(success | u) * reward - cost * u**2, its expected value,
    and the chance of success.  u = 0 (not trying) when nothing beats it."""
    f = lambda u: -(_p_success(u, difficulty, slope) * reward - cost * u * u)  # noqa: E731
    r = minimize_scalar(f, bounds=(0.0, 3.0 * difficulty + 3.0), method="bounded")
    u = float(r.x)
    v0 = float(_p_success(0.0, difficulty, slope) * reward)
    if -r.fun < v0:
        u = 0.0
    return {"u": u, "value": float(max(-r.fun, v0)), "p": float(_p_success(u, difficulty, slope))}


def evc_curve(rewards, difficulty: float = 1.0, cost: float = 1.0, slope: float = 3.0) -> dict:
    rows = [evc(r, difficulty, cost, slope) for r in rewards]
    return {"reward": np.asarray(rewards, float), "u": np.array([x["u"] for x in rows]),
            "p": np.array([x["p"] for x in rows])}


def intensity(difficulties, reward: float = 4.0, cost: float = 1.0, slope: float = 3.0) -> dict:
    """The chosen control and the chance of success across task difficulty, for one reward."""
    rows = [evc(reward, d, cost, slope) for d in difficulties]
    return {"difficulty": np.asarray(difficulties, float), "u": np.array([x["u"] for x in rows]),
            "p": np.array([x["p"] for x in rows])}


# --------------------------------------------------------------------------------------------- waiting
def _dist(kind: str):
    """Return-time distributions (minutes) with the same median, about 5: a normal (sd 1.5) and a generalized
    Pareto, heavy-tailed."""
    from scipy.stats import genpareto, truncnorm
    if kind == "normal":
        return truncnorm(-5 / 1.5, np.inf, loc=5, scale=1.5)
    c = 1.2
    scale = 5 * c / (2 ** c - 1)  # median of genpareto(c, scale) is scale (2^c - 1) / c
    return genpareto(c, scale=scale)


def remaining_wait(t, kind: str = "normal", horizon: float = 600.0) -> np.ndarray:
    """E[T - t | T > t], the expected further wait having waited t, by numerical integration of the survival
    function up to ``horizon`` minutes (a heavy tail is cut there)."""
    D = _dist(kind)
    grid = np.linspace(0, horizon, 60001)
    S = D.sf(grid)
    cum = np.concatenate([[0.0], np.cumsum((S[1:] + S[:-1]) / 2 * np.diff(grid))])
    t = np.asarray(t, float)
    St = D.sf(t)
    tail = cum[-1] - np.interp(t, grid, cum)
    return tail / np.maximum(St, 1e-300)


def reward_rate(tau, kind: str = "normal", small: float = 1.0, large: float = 2.0, iti: float = 10.0) -> np.ndarray:
    """The reward per minute of a policy that waits up to tau minutes for the large reward and otherwise takes the
    small one, with ``iti`` minutes between rounds: [F(tau) large + (1 - F(tau)) small] / [E min(T, tau) + iti]."""
    D = _dist(kind)
    out = []
    for x in np.atleast_1d(tau):
        g = np.linspace(0, x, 2001)
        Emin = float(np.trapezoid(D.sf(g), g))
        F = float(D.cdf(x))
        out.append((F * large + (1 - F) * small) / (Emin + iti))
    return np.array(out)


def give_up_time(kind: str = "normal", taus=None, **kw) -> dict:
    taus = np.linspace(0.05, 60, 1200) if taus is None else np.asarray(taus, float)
    r = reward_rate(taus, kind, **kw)
    k = int(np.argmax(r))
    return {"tau": taus, "rate": r, "best": float(taus[k]), "best_rate": float(r[k])}


# --------------------------------------------------------------------------------------------- confounding
def confounded_delay(n: int = 20000, seed: int = 0, b_ses: float = 0.45, b_ability: float = 0.35,
                     b_delay: float = 0.1, d_ses: float = 0.2, d_ability: float = 0.2) -> dict:
    """Standardized background B and early ability A (correlated 0.4); delay at age four depends on both and on
    noise; the age-15 outcome depends on B, A and a little on delay itself.  Returns the bivariate correlation, the
    regression slope of the outcome on delay alone and with B and A controlled, and their ratio."""
    rng = np.random.default_rng(seed)
    B = rng.standard_normal(n)
    A = 0.4 * B + np.sqrt(1 - 0.16) * rng.standard_normal(n)
    delay = d_ses * B + d_ability * A
    delay = delay + np.sqrt(max(1 - delay.var(), 0.05)) * rng.standard_normal(n)
    delay = (delay - delay.mean()) / delay.std()
    y = b_ses * B + b_ability * A + b_delay * delay
    y = y + np.sqrt(max(1 - y.var(), 0.05)) * rng.standard_normal(n)
    y = (y - y.mean()) / y.std()
    r = float(np.corrcoef(delay, y)[0, 1])
    X1 = np.column_stack([np.ones(n), delay])
    X2 = np.column_stack([np.ones(n), delay, B, A])
    b1 = float(np.linalg.lstsq(X1, y, rcond=None)[0][1])
    b2 = float(np.linalg.lstsq(X2, y, rcond=None)[0][1])
    return {"r": r, "alone": b1, "controlled": b2, "shrink": 1 - b2 / b1, "truth": b_delay}


# --------------------------------------------------------------------------------------------- meta-analysis
def hedges_g(m1, s1, n1, m2, s2, n2) -> tuple:
    """Hedges's g for group 1 minus group 2, and its sampling variance."""
    sp = np.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
    d = (m1 - m2) / sp
    J = 1 - 3 / (4 * (n1 + n2) - 9)
    g = J * d
    v = (n1 + n2) / (n1 * n2) + g * g / (2 * (n1 + n2))
    return float(g), float(v)


def random_effects(g, v) -> dict:
    """DerSimonian-Laird: the pooled effect, its 95% interval, tau^2, Q, I^2 and the fixed-effect estimate."""
    g, v = np.asarray(g, float), np.asarray(v, float)
    w = 1 / v
    fe = float((w * g).sum() / w.sum())
    Q = float((w * (g - fe) ** 2).sum())
    df = len(g) - 1
    tau2 = max(0.0, (Q - df) / (w.sum() - (w ** 2).sum() / w.sum()))
    ws = 1 / (v + tau2)
    re = float((ws * g).sum() / ws.sum())
    se = float(1 / np.sqrt(ws.sum()))
    I2 = max(0.0, (Q - df) / Q) if Q > 0 else 0.0
    return {"estimate": re, "lo": re - 1.96 * se, "hi": re + 1.96 * se, "se": se, "tau2": float(tau2), "Q": Q,
            "I2": float(I2), "fixed": fe, "k": len(g)}


def pet(g, se) -> dict:
    """The precision-effect test: weighted least squares of g on its standard error, weights 1/se^2.  The
    intercept estimates the effect of a study with no sampling error; the slope measures small-study bias."""
    g, se = np.asarray(g, float), np.asarray(se, float)
    w = 1 / se ** 2
    X = np.column_stack([np.ones_like(se), se])
    W = np.sqrt(w)
    beta, *_ = np.linalg.lstsq(X * W[:, None], g * W, rcond=None)
    resid = g - X @ beta
    s2 = float((w * resid ** 2).sum() / max(len(g) - 2, 1))
    cov = s2 * np.linalg.inv(X.T @ (X * w[:, None]))
    return {"intercept": float(beta[0]), "slope": float(beta[1]), "se_intercept": float(np.sqrt(cov[0, 0]))}


# --------------------------------------------------------------------------------------------- discounting
def discount_titration(k: float, amount: float = 100.0, delays=(1, 7, 30, 90, 180, 365), steps: int = 6,
                       noise: float = 0.0, seed: int = 0) -> dict:
    """The adjusting-amount procedure: for each delay, offer an immediate amount against ``amount`` later, starting
    at half and moving by a step that halves after each choice, so the immediate offer converges on the
    indifference point.  The chooser is hyperbolic with rate k (per day), with optional logistic noise on the value
    difference.  Returns the indifference points, the fitted k, the area under the curve (Myerson, Green and
    Warusawitharana 2001) and every offer made."""
    rng = np.random.default_rng(seed)
    out, offers = [], []
    for D in delays:
        now, step = amount / 2, amount / 4
        later = amount / (1 + k * D)
        seq = []
        for _ in range(steps):
            seq.append(now)
            diff = now - later
            take_now = (rng.random() < 1 / (1 + np.exp(-diff / noise))) if noise > 0 else bool(diff > 0)
            now = now - step if take_now else now + step
            step /= 2
        seq.append(now)
        offers.append(seq)
        out.append(now)
    ind = np.array(out)
    D = np.asarray(delays, float)
    r = minimize_scalar(lambda kk: ((ind - amount / (1 + kk * D)) ** 2).sum(), bounds=(1e-5, 1.0), method="bounded")
    auc = float(np.trapezoid(np.r_[1.0, ind / amount], np.r_[0.0, D] / D.max()))
    return {"delay": D, "indifference": ind, "k_fit": float(r.x), "auc": auc, "offers": np.array(offers)}

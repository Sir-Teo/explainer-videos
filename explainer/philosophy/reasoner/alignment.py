"""Alignment for Part 42 ("Aligning Reasoners"): Goodhart's law as best-of-N selection on a noisy proxy (light and
heavy-tailed errors); Armstrong and Mindermann's no-free-lunch theorem for preferences, as planner-reward pairs that
explain the same behaviour; the off-switch game (Hadfield-Menell et al. 2017) with a rational and a noisy human;
power-seeking in a small MDP (Turner et al. 2021); Löb's axiom checked on every Kripke frame with up to four worlds;
and modal combat, the Löbian cooperation of proof-based agents (Barasz et al. 2014)."""

from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------------------
# Goodhart's law: optimize a proxy, and the true value bends over
# ---------------------------------------------------------------------------
def goodhart(ns=(1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192), trials: int = 3000,
             seed: int = 1975, df: float = 1.5) -> dict:
    """Regressional Goodhart (Manheim and Garrabrant 2018). Each candidate has a true value V ~ N(0, 1); we see only a
    proxy U = V + E. Pick the candidate with the highest proxy among N: N measures optimization pressure. With
    Gaussian error E ~ N(0, 1) the true value of the pick keeps rising (as half the proxy). With heavy-tailed error
    (Student t with ``df`` degrees of freedom) the pick is increasingly an error outlier, and its true value rises
    and then falls back towards the average: the proxy-vs-true curve bends over."""
    rng = np.random.default_rng(seed)
    out = {"ns": list(ns), "light": {"proxy": [], "true": []}, "heavy": {"proxy": [], "true": []}, "df": df}
    for n in ns:
        for kind in ("light", "heavy"):
            picked_u, picked_v = [], []
            chunk = max(1, min(trials, 2_000_000 // n))
            for start in range(0, trials, chunk):
                m = min(chunk, trials - start)
                V = rng.normal(0, 1, (m, n))
                E = rng.normal(0, 1, (m, n)) if kind == "light" else rng.standard_t(df, (m, n))
                U = V + E
                k = np.argmax(U, axis=1)
                rows = np.arange(m)
                picked_u.append(U[rows, k])
                picked_v.append(V[rows, k])
            out[kind]["proxy"].append(round(float(np.median(np.concatenate(picked_u))), 3))
            out[kind]["true"].append(round(float(np.concatenate(picked_v).mean()), 3))
    for kind in ("light", "heavy"):
        t = out[kind]["true"]
        out[kind]["peak_n"] = ns[int(np.argmax(t))]
        out[kind]["peak"] = max(t)
        out[kind]["last"] = t[-1]
    # a scatter of the two worlds, for the picture
    V = rng.normal(0, 1, 1500)
    out["scatter"] = {"V": V.round(3).tolist(), "light": (V + rng.normal(0, 1, 1500)).round(3).tolist(),
                      "heavy": (V + rng.standard_t(df, 1500)).round(3).tolist()}
    return out


def quantilize(n: int = 4096, qs=(1 / 4096, 1 / 1024, 1 / 256, 1 / 64, 1 / 16, 1 / 4, 1 / 2, 1.0), trials: int = 2000,
               seed: int = 2016, df: float = 1.5) -> dict:
    """Mild optimization (Taylor's quantilizers, 2016): instead of taking the proxy's single best of n candidates,
    pick at random among the top fraction q. Under heavy-tailed proxy error the argmax (q = 1/n) is mostly an error
    outlier; a moderate q keeps much of the true gain; q = 1 is random choice."""
    rng = np.random.default_rng(seed)
    true = {str(q): [] for q in qs}
    for _ in range(trials):
        V = rng.normal(0, 1, n)
        U = V + rng.standard_t(df, n)
        order = np.argsort(-U)
        for q in qs:
            m = max(1, int(round(q * n)))
            true[str(q)].append(V[order[rng.integers(m)]])
    out = [{"q": q, "top": max(1, int(round(q * n))), "true": round(float(np.mean(true[str(q)])), 3)} for q in qs]
    best = max(out, key=lambda r: r["true"])
    return {"n": n, "df": df, "rows": out, "best_q": best["q"], "best_true": best["true"]}


# ---------------------------------------------------------------------------
# No free lunch for preferences (Armstrong and Mindermann 2018)
# ---------------------------------------------------------------------------
def boltzmann(R, beta: float) -> np.ndarray:
    z = beta * np.asarray(R, float)
    z = z - z.max()
    p = np.exp(z)
    return p / p.sum()


def no_free_lunch(options=("tea", "coffee", "water", "juice"), policy=(0.5, 0.3, 0.05, 0.15)) -> dict:
    """An observed policy (how often a person picks each option) is explained exactly by many (planner, reward)
    pairs: a Boltzmann-rational planner with reward log pi; the same with twice the rationality and half the reward;
    an anti-rational planner with the negated reward; and a planner that ignores the reward altogether, with reward
    zero. Each reproduces the policy exactly, so behaviour alone cannot tell values from rationality."""
    pi = np.array(policy, float)
    assert abs(pi.sum() - 1) < 1e-12
    logp = np.log(pi)
    pairs = [
        ("rational", 1.0, logp - logp.min()),
        ("twice as rational", 2.0, (logp - logp.min()) / 2),
        ("anti-rational", -1.0, -(logp - logp.min())),
        ("indifferent", None, np.zeros(len(pi))),
    ]
    out = []
    for name, beta, R in pairs:
        pred = pi.copy() if beta is None else boltzmann(R, beta)
        out.append({"planner": name, "beta": beta, "reward": [round(float(r), 2) for r in R],
                    "predicted": [round(float(x), 3) for x in pred],
                    "error": float(np.abs(pred - pi).max()),
                    "best": options[int(np.argmax(R))] if np.ptp(R) > 0 else None})
    return {"options": list(options), "policy": list(policy), "pairs": out}


# ---------------------------------------------------------------------------
# The off-switch game (Hadfield-Menell, Dragan, Abbeel and Russell 2017)
# ---------------------------------------------------------------------------
_GH_X, _GH_W = np.polynomial.hermite_e.hermegauss(80)
_GH_W = _GH_W / _GH_W.sum()


def off_switch_values(mu: float, sigma: float, beta: float | None = None) -> dict:
    """The robot believes the human's utility for its action is u ~ N(mu, sigma^2). It can act (gets u), switch
    itself off (0), or wait and let the human decide. A rational human (beta None) lets it act iff u > 0, so waiting
    is worth E[max(u, 0)]; a noisy human lets it act with probability 1 / (1 + exp(-beta u)). The incentive to defer
    is the value of waiting minus the better of acting and switching off."""
    if beta is None:  # E[max(u, 0)] in closed form
        if sigma == 0:
            wait = max(mu, 0.0)
        else:
            z = mu / sigma
            wait = mu * 0.5 * (1 + math.erf(z / math.sqrt(2))) + sigma * math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    else:
        u = mu + sigma * _GH_X
        wait = float((_GH_W * u / (1 + np.exp(-beta * u))).sum())
    act = float(mu)
    return {"act": act, "off": 0.0, "wait": wait, "incentive": wait - max(act, 0.0)}


def off_switch(mus=None, sigmas=None, betas=(None, 2.0, 0.5)) -> dict:
    """The incentive to defer on a grid of the robot's mean belief and its uncertainty, for a rational human and for
    noisy ones. With a rational human the incentive is never negative, and zero only when the robot is certain; with
    a noisy human, a confident robot prefers to act or to switch off."""
    mus = np.round(np.linspace(-2, 2, 41), 3) if mus is None else np.asarray(mus)
    sigmas = np.round(np.linspace(0.0, 3.0, 31), 3) if sigmas is None else np.asarray(sigmas)
    grids = {}
    for b in betas:
        key = "rational" if b is None else f"beta={b:g}"
        grids[key] = [[round(off_switch_values(float(m), float(s), b)["incentive"], 4) for m in mus] for s in sigmas]
    # the worked example on the game tree
    ex = off_switch_values(0.5, 1.0)
    ex_noisy = off_switch_values(0.5, 1.0, 0.5)
    Phi = 0.5 * (1 + math.erf(0.5 / math.sqrt(2)))
    phi = math.exp(-0.125) / math.sqrt(2 * math.pi)
    exact_wait = 0.5 * Phi + 1.0 * phi
    return {"mus": mus.tolist(), "sigmas": sigmas.tolist(), "grids": grids,
            "example": {"mu": 0.5, "sigma": 1.0, **{k: round(v, 4) for k, v in ex.items()}, "exact_wait": round(exact_wait, 4)},
            "example_noisy": {"beta": 0.5, **{k: round(v, 4) for k, v in ex_noisy.items()}}}


# ---------------------------------------------------------------------------
# Power-seeking (Turner, Smith, Shah, Critch and Tadepalli 2021)
# ---------------------------------------------------------------------------
POWER_MDP = {
    # state: list of successor states (deterministic actions); absorbing states loop to themselves
    "start": ["off", "hub"],
    "off": ["off"],
    "hub": ["a", "b", "c"],
    "a": ["a"], "b": ["b"], "c": ["c"],
}


def _values(mdp: dict, R: dict, gamma: float, iters: int = 2000) -> dict:
    V = {s: 0.0 for s in mdp}
    for _ in range(iters):
        V = {s: R[s] + gamma * max(V[t] for t in mdp[s]) for s in mdp}
    return V


def power_seeking(gamma: float = 0.99, samples: int = 4000, seed: int = 2021, ks=(1, 2, 3, 4, 5, 6)) -> dict:
    """Rewards on states drawn iid Uniform[0, 1]. From ``start`` the agent can go to ``off`` (an absorbing shutdown
    state) or to ``hub``, from which three absorbing states are reachable. Count the reward functions whose optimal
    policy goes to the hub, and compute each state's POWER: (1 - gamma) / gamma times the expected optimal value,
    minus the state's own reward. Then vary the number k of options behind the hub: the fraction that avoids shutdown
    approaches k / (k + 1)."""
    rng = np.random.default_rng(seed)
    states = list(POWER_MDP)
    to_hub, power = 0, {s: 0.0 for s in states}
    # absorbing state values are closed form: R / (1 - gamma); the hub picks its best absorbing state
    for _ in range(samples):
        R = dict(zip(states, rng.random(len(states))))
        V = {}
        for s in ("off", "a", "b", "c"):
            V[s] = R[s] / (1 - gamma)
        V["hub"] = R["hub"] + gamma * max(V["a"], V["b"], V["c"])
        V["start"] = R["start"] + gamma * max(V["off"], V["hub"])
        to_hub += V["hub"] > V["off"]
        for s in states:
            power[s] += (1 - gamma) / gamma * (V[s] - R[s])
    power = {s: round(v / samples, 4) for s, v in power.items()}
    # three example reward functions, and where an optimal agent goes
    examples, want = [], ["hub", "hub", "off"]
    ex_rng = np.random.default_rng(seed + 1)
    while want:
        R = {s: round(float(x), 2) for s, x in zip(states, ex_rng.random(len(states)))}
        V = _values(POWER_MDP, R, gamma)
        goes = "hub" if V["hub"] > V["off"] else "off"
        if goes == want[0]:
            want.pop(0)
            examples.append({"R": R, "goes": goes, "then": max(("a", "b", "c"), key=lambda t: V[t])})
    # check the closed forms against value iteration on one sample
    R = dict(zip(states, rng.random(len(states))))
    Vi = _values(POWER_MDP, R, gamma)
    assert abs(Vi["off"] - R["off"] / (1 - gamma)) < 1e-6
    frac = {}
    for k in ks:
        Roff = rng.random(samples)
        Rhub = rng.random(samples)
        Rk = rng.random((samples, k))
        v_off = Roff / (1 - gamma)
        v_hub = Rhub + gamma * Rk.max(axis=1) / (1 - gamma)
        frac[str(k)] = round(float((v_hub > v_off).mean()), 4)
    # with gamma -> 1 the hub's own reward is negligible and the fraction is exactly k / (k + 1)
    return {"gamma": gamma, "samples": samples, "to_hub": round(float(to_hub) / samples, 4),
            "power": {s: float(v) for s, v in power.items()},
            "fraction_by_k": frac, "examples": examples, "limit": {str(k): round(k / (k + 1), 4) for k in ks}}


# ---------------------------------------------------------------------------
# Löb's axiom on finite Kripke frames
# ---------------------------------------------------------------------------
def _box(succ, X, n):
    """Worlds all of whose successors lie in X (bitmasks)."""
    out = 0
    for w in range(n):
        if succ[w] & ~X == 0:
            out |= 1 << w
    return out


def lob_frames(nmax: int = 4) -> dict:
    """For every frame (W, R) with |W| <= nmax, check whether Löb's axiom box(box p -> p) -> box p is valid (true at
    every world under every valuation of p), and whether the frame is transitive and irreflexive. On finite frames the
    two coincide: Löb's axiom characterizes the strict partial orders, the frames of the provability logic GL. Also
    count the frames validating 4 (box p -> box box p) and T (box p -> p)."""
    rows = []
    for n in range(1, nmax + 1):
        full = (1 << n) - 1
        pairs = [(i, j) for i in range(n) for j in range(n)]
        lob = spo = agree = t_ok = four_ok = 0
        for bits in range(1 << len(pairs)):
            succ = [0] * n
            for k, (i, j) in enumerate(pairs):
                if bits >> k & 1:
                    succ[i] |= 1 << j
            valid = True
            valid_t = True
            valid_4 = True
            for P in range(1 << n):
                BP = _box(succ, P, n)
                imp = (~BP | P) & full
                if valid and _box(succ, imp, n) & ~BP:
                    valid = False
                if valid_t and BP & ~P:
                    valid_t = False
                if valid_4 and BP & ~_box(succ, BP, n):
                    valid_4 = False
                if not (valid or valid_t or valid_4):
                    break
            irreflexive = all(not (succ[i] >> i & 1) for i in range(n))
            transitive = all((succ[j] & ~succ[i]) == 0 for i in range(n) for j in range(n) if succ[i] >> j & 1)
            is_spo = irreflexive and transitive
            lob += valid
            spo += is_spo
            agree += valid == is_spo
            t_ok += valid_t
            four_ok += valid_4
        rows.append({"n": n, "frames": 1 << len(pairs), "lob_valid": lob, "strict_partial_orders": spo,
                     "agree": agree, "T_valid": t_ok, "four_valid": four_ok})
    return {"rows": rows}


# ---------------------------------------------------------------------------
# Modal combat: proof-based agents in the prisoner's dilemma (Barasz et al. 2014; LaVictoire et al. 2014)
# ---------------------------------------------------------------------------
BOTS = ("CooperateBot", "DefectBot", "FairBot", "PrudentBot")


def _box_seq(seq, k):
    """box(phi) at world k of the linear GL model: phi holds at every world below k (vacuous at world 0)."""
    return all(seq[:k])


def _box_con(seq, k):
    """Provable in PA + Con(PA): phi holds at every world below k except world 0, where box(false) holds."""
    return all(seq[1:k])


def _play(X: str, Y: str, K: int, memo: dict) -> tuple[list[bool], list[bool]]:
    """Cooperation sequences (x_k, y_k) for X against Y on worlds 0..K-1: x_k is 'X cooperates with Y' at world k.
    Every bot's action at world k depends only on lower worlds, so the sequences are computed in order; the truth
    in the standard model of arithmetic is the eventual (stable) value."""
    if (X, Y) in memo:
        return memo[(X, Y)]
    if (Y, X) in memo:
        y, x = memo[(Y, X)]
        return x, y
    x, y = [], []
    vs_db = {}
    for B in (X, Y):
        if B == "PrudentBot":
            other = Y if B == X else X
            vs_db[B] = _play(other, "DefectBot", K, memo)[0] if other != "DefectBot" else [False] * K
    for k in range(K):
        x.append(_act(X, y, k, vs_db.get(X)))
        y.append(_act(Y, x, k, vs_db.get(Y)))
    memo[(X, Y)] = (x, y)
    return x, y


def _act(B: str, opp: list[bool], k: int, opp_vs_db) -> bool:
    if B == "CooperateBot":
        return True
    if B == "DefectBot":
        return False
    if B == "FairBot":
        return _box_seq(opp, k)
    if B == "PrudentBot":
        return _box_seq(opp, k) and _box_con([not v for v in opp_vs_db], k)
    raise KeyError(B)


def modal_combat(K: int = 8) -> dict:
    """The outcome of every pairing of four bots. FairBot cooperates with you iff it can prove you cooperate with it;
    PrudentBot also demands a proof (in PA + Con(PA)) that you defect against DefectBot. By Löb's theorem FairBot
    cooperates with itself; PrudentBot exploits CooperateBot but cooperates with FairBot and with itself."""
    memo: dict = {}
    table, traces = {}, {}
    for X in BOTS:
        for Y in BOTS:
            x, y = _play(X, Y, K, memo)
            assert x[-1] == x[-2] and y[-1] == y[-2], (X, Y)
            table[f"{X}|{Y}"] = "C" if x[-1] else "D"
            traces[f"{X}|{Y}"] = "".join("C" if v else "D" for v in x)
    return {"bots": list(BOTS), "table": table, "traces": traces, "K": K}

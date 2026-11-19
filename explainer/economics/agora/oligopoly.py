"""Competition among the few (Agora, Part 12): how a handful of firms compete, and when they stop.

**Quantities.**  :func:`cournot` (N firms, linear demand, any constant costs: quantities, price, profits, the
Herfindahl index and the Lerner-HHI identity), :func:`cournot_reaction` (best-response lines for two firms),
:func:`cournot_dynamics` (alternating best responses converging to the equilibrium).

**Prices.**  :func:`bertrand` (homogeneous goods: price at the second-lowest cost), :func:`bertrand_differentiated`
(linear differentiated demand: reaction lines and equilibrium), :func:`kreps_scheinkman` (capacities chosen first,
prices second: the Cournot outcome reappears, checked by the rationing argument for capacities at or below the
Cournot levels).

**Space and variety.**  :func:`hotelling` (two firms at the ends of a line, prices c + t), :func:`hotelling_location`
(fixed equal prices: both move to the middle), :func:`salop` (the circle with free entry: n = sqrt(t/F), too many
firms), :func:`dixit_stiglitz` (CES monopolistic competition: markup sigma/(sigma - 1), free-entry variety).

**Commitment.**  :func:`stackelberg` (leader and follower), :func:`dixit_entry` (an incumbent's capacity that
deters, accommodates or blockades entry).

**Collusion.**  :func:`collusion_threshold` (the discount factor that sustains joint profit maximization by grim
trigger, for Cournot and Bertrand with N firms), :func:`green_porter` (trigger-price collusion with unobserved demand
shocks: price wars on the equilibrium path), :func:`leniency_race` (who confesses first under a leniency programme).

**Concentration and mergers.**  :func:`hhi`, :func:`merger_cournot` (Salant, Switzer and Reynolds: a merger of two of
N symmetric Cournot firms, profitable or not, and the cost saving that keeps price from rising, after Farrell and
Shapiro), :func:`williamson` (the welfare trade-off: the deadweight triangle against the cost rectangle),
:func:`mhhi` (common ownership: O'Brien and Salop's modified HHI).

Plain numpy and scipy.
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------------------------------------------
# quantities


def cournot(a: float, b: float, costs) -> dict:
    """Cournot with inverse demand P = a - b Q and constant marginal costs ``costs`` (one per firm).  Interior
    solution q_i = (a - (N + 1) c_i + sum c) / ((N + 1) b), firms with nonpositive output dropped and the rest
    re-solved."""
    c = np.asarray(costs, float)
    active = np.ones(len(c), bool)
    while True:
        ca = c[active]
        n = len(ca)
        q = (a - (n + 1) * ca + ca.sum()) / ((n + 1) * b)
        if (q > 0).all():
            break
        idx = np.where(active)[0]
        active[idx[q <= 0]] = False
    qs = np.zeros(len(c))
    qs[active] = q
    Q = qs.sum()
    P = a - b * Q
    shares = qs / Q
    H = float((shares ** 2).sum())
    profits = (P - c) * qs
    eps = P / (b * Q)                          # the (absolute) elasticity of market demand at the equilibrium
    lerner = float(shares @ ((P - c) / P))     # the share-weighted Lerner index
    return {"q": qs, "Q": float(Q), "P": float(P), "profits": profits, "shares": shares, "hhi": H,
            "eps": float(eps), "lerner": lerner, "lerner_hhi": H / eps}


def cournot_reaction(a: float, b: float, c1: float, c2: float, n: int = 101) -> dict:
    """Firm 1's best response q1 = (a - c1 - b q2) / 2b against q2, and firm 2's against q1."""
    q2 = np.linspace(0, (a - c2) / b, n)
    q1 = np.maximum((a - c1 - b * q2) / (2 * b), 0)
    return {"q2": q2, "r1": q1, "q1": q2.copy() * (a - c1) / (a - c2), "r2": np.maximum(
        (a - c2 - b * (q2 * (a - c1) / (a - c2))) / (2 * b), 0)}


def cournot_dynamics(a: float, b: float, c1: float, c2: float, q0=(0.0, 0.0), steps: int = 12) -> np.ndarray:
    """Alternating best responses from q0: firm 1 moves, then firm 2, and so on."""
    q1, q2 = q0
    path = [(q1, q2)]
    for k in range(steps):
        if k % 2 == 0:
            q1 = max((a - c1 - b * q2) / (2 * b), 0)
        else:
            q2 = max((a - c2 - b * q1) / (2 * b), 0)
        path.append((q1, q2))
    return np.array(path)


# ---------------------------------------------------------------------------------------------------------------
# prices


def bertrand(a: float, b: float, costs, tick: float = 0.01) -> dict:
    """Homogeneous Bertrand: the lowest-cost firm prices just below the second-lowest cost (or at its monopoly price
    if that is lower) and serves the market; with equal lowest costs, price equals cost."""
    c = np.sort(np.asarray(costs, float))
    pm = (a + c[0]) / 2         # the low-cost firm's monopoly price for P = a - b Q
    if len(c) > 1 and abs(c[1] - c[0]) < 1e-12:
        p = c[0]
    else:
        p = min(c[1] - tick if len(c) > 1 else pm, pm)
    Q = max((a - p) / b, 0.0)
    return {"P": float(p), "Q": float(Q), "profit": float((p - c[0]) * Q)}


def bertrand_differentiated(alpha: float, beta: float, gamma: float, c: float) -> dict:
    """Demand q_i = alpha - beta p_i + gamma p_j (0 < gamma < beta), marginal cost c: best response p_i =
    (alpha + beta c + gamma p_j) / (2 beta); symmetric equilibrium p = (alpha + beta c) / (2 beta - gamma)."""
    p = (alpha + beta * c) / (2 * beta - gamma)
    q = alpha - (beta - gamma) * p
    pj = np.linspace(0, 2 * p, 101)
    return {"p": float(p), "q": float(q), "profit": float((p - c) * q), "pj": pj,
            "br": (alpha + beta * c + gamma * pj) / (2 * beta)}


def kreps_scheinkman(a: float, b: float, c: float) -> dict:
    """With capacities chosen first and prices second (efficient rationing, capacity cost c), the subgame-perfect
    outcome is Cournot's: capacities (a - c)/(3b) each, price at the market-clearing level.  Checks that at those
    capacities neither firm gains by undercutting (it cannot sell more) or by raising its price (its residual
    demand makes the clearing price its best reply)."""
    k = (a - c) / (3 * b)
    P = a - 2 * b * k
    # raising price p > P: firm sells the residual (a - p)/b - k; profit (p)(...) on top of sunk capacity cost
    ps = np.linspace(P, a, 400)
    residual = np.maximum((a - ps) / b - k, 0)
    gain_up = float(np.max(ps * residual - P * k))
    return {"k": float(k), "P": float(P), "deviation_gain": gain_up, "cournot": cournot(a, b, [c, c])}


# ---------------------------------------------------------------------------------------------------------------
# space and variety


def hotelling(t: float, c: float, a1: float = 0.0, a2: float = 1.0) -> dict:
    """Hotelling's line [0, 1] with consumers spread evenly, each buying one unit, transport cost t per unit of
    distance and marginal cost c.  With the two firms at the ends the price equilibrium is p = c + t each, the
    market split in half, each firm earning t / 2.  (Only the end locations are implemented: with linear transport
    costs and other locations a price equilibrium may not exist, as d'Aspremont, Gabszewicz and Thisse showed.)"""
    if (a1, a2) != (0.0, 1.0):
        raise ValueError("only the end locations are implemented")
    return {"p": c + t, "split": 0.5, "profit": t / 2}


def hotelling_location(p: float = 1.0, steps: int = 30) -> np.ndarray:
    """With prices fixed and equal, each firm moves to capture more of the line: alternating best responses (move
    just inside the rival) converge to both at the middle."""
    x1, x2 = 0.1, 0.9
    path = [(x1, x2)]
    for k in range(steps):
        if k % 2 == 0:
            x1 = min(x1 + (x2 - x1) / 2, 0.5) if x2 > 0.5 else 0.5
        else:
            x2 = max(x2 - (x2 - x1) / 2, 0.5) if x1 < 0.5 else 0.5
        path.append((x1, x2))
    return np.array(path)


def salop(t: float, F: float, c: float = 0.0) -> dict:
    """Salop's circle of circumference 1 with consumers spread evenly, transport cost t, entry cost F.  With n firms
    equally spaced the price is c + t/n and each firm earns t/n^2 - F, so free entry gives n = sqrt(t/F).  A planner
    who minimizes the total of entry and transport costs, n F + t/(4n), wants n = sqrt(t/(4F)): half as many."""
    n_free = np.sqrt(t / F)
    n_opt = np.sqrt(t / (4 * F))
    return {"n_free": float(n_free), "n_opt": float(n_opt), "p": float(c + t / n_free),
            "cost_free": float(n_free * F + t / (4 * n_free)), "cost_opt": float(n_opt * F + t / (4 * n_opt))}


def dixit_stiglitz(sigma: float, f: float, c: float, L: float) -> dict:
    """CES monopolistic competition with a fixed cost f and marginal cost c (labour), economy of L workers: price
    sigma/(sigma - 1) c; free entry sets each firm's output (sigma - 1) f / c; the number of varieties L / (sigma f)."""
    p = sigma / (sigma - 1) * c
    x = (sigma - 1) * f / c
    n = L / (sigma * f)
    return {"p": float(p), "markup": float(p / c), "x": float(x), "n": float(n)}


# ---------------------------------------------------------------------------------------------------------------
# commitment


def stackelberg(a: float, b: float, c: float) -> dict:
    """Leader commits to q_L = (a - c)/(2b); the follower replies (a - c)/(4b)."""
    qL = (a - c) / (2 * b)
    qF = (a - c) / (4 * b)
    P = a - b * (qL + qF)
    return {"qL": float(qL), "qF": float(qF), "P": float(P), "piL": float((P - c) * qL),
            "piF": float((P - c) * qF), "cournot": cournot(a, b, [c, c])}


def dixit_entry(a: float, b: float, c: float, r: float, F: float) -> dict:
    """Dixit (1980), linear demand P = a - bQ.  The incumbent installs capacity k at r a unit before the entrant
    decides; output up to k then costs it only c, beyond k it costs c + r.  The entrant's cost is c + r a unit and F
    to come in.  After entry the two play Cournot; the incumbent's reply is its reply at cost c, capped at k, but
    never below its reply at cost c + r, so only capacities between S (the Cournot point at cost c + r) and T (the
    entrant's reply crossing the incumbent's reply at cost c) are credible threats.

    Returns the entrant's profit against each k, the points S and T, the monopoly output at cost c + r, the deterring
    capacity, the incumbent's profit by deterring and by accommodating (the best credible Stackelberg point), and the
    regime: "blockaded" (the monopoly output already keeps the entrant out), "deter" (it pays to hold extra
    capacity), "accommodate" (deterring is possible but costs more than sharing) or "impossible" (no credible
    capacity deters)."""
    ce = c + r

    def reply_e(qi):
        return max((a - ce - b * qi) / (2 * b), 0.0)

    def reply_i(qe, k):
        return max((a - ce - b * qe) / (2 * b), min(k, (a - c - b * qe) / (2 * b)))

    def post_entry(k):
        qe = 0.0
        for _ in range(300):
            qi = reply_i(qe, k)
            qe = reply_e(qi)
        qi = reply_i(qe, k)
        P = a - b * (qi + qe)
        return float(qi), float(qe), float((P - ce) * qe - F)

    S = (a - ce) / (3 * b)                                   # both at cost c + r
    T = (a - 2 * c + ce) / (3 * b)                           # incumbent at c, entrant at c + r
    m = (a - ce) / (2 * b)                                   # monopoly output at cost c + r
    ks = np.linspace(0, (a - c) / b, 451)
    prof = np.array([post_entry(k)[2] for k in ks])
    # the output that leaves the entrant exactly nothing: its best reply earns b qe^2, so qe = sqrt(F / b)
    k_zero = (a - ce - 2 * b * np.sqrt(F / b)) / b
    if k_zero <= m:
        regime, deter_k = "blockaded", float(max(k_zero, 0.0))
        pi_deter = (a - b * m - ce) * m
    elif k_zero <= T:
        deter_k = float(k_zero)
        pi_deter = (a - b * deter_k - ce) * deter_k
        regime = "deter"
    else:
        deter_k, pi_deter, regime = None, -np.inf, "impossible"
    qL = min(max(m, S), T)                                   # Stackelberg output, clamped to the credible range
    qF = reply_e(qL)
    pi_acc = (a - b * (qL + qF) - ce) * qL
    if regime == "deter" and pi_deter < pi_acc:
        regime = "accommodate"
    return {"ks": ks, "entrant_profit": prof, "S": float(S), "T": float(T), "monopoly_q": float(m),
            "pi_monopoly": float((a - b * m - ce) * m), "deter_k": deter_k, "pi_deter": float(pi_deter),
            "acc_q": float(qL), "acc_entrant_q": float(qF), "pi_accommodate": float(pi_acc), "regime": regime,
            "deter_pays": regime in ("blockaded", "deter")}


# ---------------------------------------------------------------------------------------------------------------
# collusion


def collusion_threshold(n: int, kind: str = "cournot", a: float = 1.0, b: float = 1.0, c: float = 0.0) -> dict:
    """Grim trigger with N symmetric firms sharing the monopoly profit equally: cheating gives the best one-shot
    deviation, then the static Nash profit for ever.  delta* = (pi_dev - pi_coll) / (pi_dev - pi_nash).  Bertrand:
    pi_dev = whole monopoly profit, pi_nash = 0, so delta* = 1 - 1/N."""
    pim = (a - c) ** 2 / (4 * b)
    pc = pim / n
    if kind == "bertrand":
        pdev, pn = pim, 0.0
    else:
        q_coll = (a - c) / (2 * b * n)
        q_dev = (a - c - b * (n - 1) * q_coll) / (2 * b)
        P_dev = a - b * (q_dev + (n - 1) * q_coll)
        pdev = (P_dev - c) * q_dev
        pn = (a - c) ** 2 / (b * (n + 1) ** 2)
    return {"delta": float((pdev - pc) / (pdev - pn)), "collude": float(pc), "deviate": float(pdev),
            "nash": float(pn)}


def green_porter(periods: int = 300, a: float = 10.0, sd: float = 1.0, trigger: float = 3.5, war: int = 6,
                 q_coll: float = 2.5, q_war: float = 3.33, seed: int = 1984) -> dict:
    """Green and Porter (1984): two firms see only the market price, P = a - Q + e with e ~ N(0, sd); they collude
    (q_coll each) until the price falls below ``trigger``, then revert to Cournot output (q_war) for ``war``
    periods.  Nobody cheats, yet price wars happen when demand is low."""
    rng = np.random.default_rng(seed)
    e = rng.normal(0, sd, periods)
    state, left = "collude", 0
    P, wars = np.zeros(periods), np.zeros(periods, bool)
    for t in range(periods):
        q = q_coll if state == "collude" else q_war
        P[t] = a - 2 * q + e[t]
        wars[t] = state == "war"
        if state == "collude" and P[t] < trigger:
            state, left = "war", war
        elif state == "war":
            left -= 1
            if left <= 0:
                state = "collude"
    return {"P": P, "war": wars, "share_war": float(wars.mean()), "shock": e}


def leniency_race(fine: float, prob_caught: float, n: int = 2, leniency: float = 1.0) -> dict:
    """A cartel's members each choose to confess or stay silent.  Without a confession, the cartel is caught with
    probability ``prob_caught`` and each pays ``fine``; the first to confess pays (1 - leniency) of the fine and the
    others pay it in full.  If a rival confesses you pay the full fine whatever you do, so confessing first is
    dominant when (1 - leniency) fine < prob_caught fine: with full leniency, whenever there is any chance of being
    caught.  A prisoner's dilemma the authorities built on purpose."""
    silent = prob_caught * fine
    confess_alone = (1 - leniency) * fine
    return {"silent": float(silent), "confess_first": float(confess_alone), "dominant": bool(confess_alone < silent)}


# ---------------------------------------------------------------------------------------------------------------
# concentration and mergers


def hhi(shares) -> float:
    """The Herfindahl-Hirschman index on the 0-10,000 scale from percentage shares (or 0-1 shares times 10,000)."""
    s = np.asarray(shares, float)
    if s.sum() <= 1.0001:
        s = 100 * s
    return float((s ** 2).sum())


def merger_cournot(n: int, a: float = 1.0, b: float = 1.0, c: float = 0.0) -> dict:
    """Two of N symmetric Cournot firms merge (becoming one firm with the same cost): the merged firm's profit
    against the two firms' combined profit before (Salant, Switzer and Reynolds 1983), and the marginal cost the
    merged firm needs for the price not to rise (Farrell and Shapiro 1990, linear demand)."""
    before = cournot(a, b, [c] * n)
    after = cournot(a, b, [c] * (n - 1))
    gain = after["profits"][0] - 2 * before["profits"][0]
    # with n - 1 firms, one of cost c_m, the price is (a + c_m + (n - 2) c) / n; it equals the price before,
    # (a + n c) / (n + 1), when c_m = n P_before - a - (n - 2) c
    cm = before["P"] * n - a - (n - 2) * c
    # the price after the merger even if the merged firm's marginal cost fell to nothing
    p_free = (a + (n - 2) * c) / n
    return {"before": before, "after": after, "merger_gain": float(gain), "profitable": bool(gain > 0),
            "cost_for_same_price": float(cm), "saving_needed": float(c - cm), "price_if_free": float(p_free)}


def williamson(eps: float, dp: float, dc: float) -> dict:
    """Williamson (1968): a merger raises price by a share dp and lowers cost by a share dc; the deadweight
    triangle, roughly (1/2) eps dp^2 of revenue, against the cost saving, roughly dc of revenue.  The cost cut that
    just offsets a price rise is dc = (1/2) eps dp^2 (as a share of the pre-merger revenue)."""
    loss = 0.5 * eps * dp ** 2
    return {"loss": float(loss), "saving": float(dc), "net": float(dc - loss), "breakeven_dc": float(loss)}


def mhhi(shares, control, cash) -> dict:
    """O'Brien and Salop's modified HHI: firms j with market shares s_j; investors i with control rights
    gamma[i][j] and cash-flow rights beta[i][j].  MHHI = HHI + sum_{j != k} s_j s_k (sum_i gamma_ij beta_ik) /
    (sum_i gamma_ij beta_ij), on the 0-10,000 scale."""
    s = np.asarray(shares, float)
    if s.sum() <= 1.0001:
        s = 100 * s
    g, bta = np.asarray(control, float), np.asarray(cash, float)
    H = float((s ** 2).sum())
    delta = 0.0
    m = len(s)
    for j in range(m):
        den = float(g[:, j] @ bta[:, j])
        for k in range(m):
            if j != k and den > 0:
                delta += s[j] * s[k] * float(g[:, j] @ bta[:, k]) / den
    return {"hhi": H, "delta": float(delta), "mhhi": H + float(delta)}


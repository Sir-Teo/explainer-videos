"""Spillovers (Part 15): externalities, Coase's bargain, public goods, the commons, prices against quantities, and
congestion.

**Externalities.**  :func:`externality` (a market with linear demand and private marginal cost, and a marginal
damage that rises with output: the market and efficient quantities, the deadweight loss, and Pigou's tax),
:func:`coase` (Coase's 1960 table of the cattle-raiser's steers and the farmer's crop, with the cattle-raiser's
values: the herd under each liability rule, with bargaining and with transaction costs).

**Public goods.**  :func:`public_good` (consumers with values theta_i ln(1 + G): Samuelson's condition, voluntary
provision, Lindahl's prices), :func:`vcm` (a voluntary-contribution game played by Agora's typed players, conditional
cooperators and free riders, with and without punishment).

**The commons.**  :func:`fishery` (Gordon and Schaefer: sustainable yield, open-access effort where the rent is
dissipated, maximum economic yield and maximum sustainable yield).

**Prices or quantities.**  :func:`prices_quantities` (Weitzman 1974: the expected loss of a tax and of a quota when
abatement costs are uncertain, closed form and simulated).

**Networks.**  :func:`lock_in` (Arthur 1989: increasing returns to adoption, and lock-in by early luck).

**Congestion.**  :func:`bottleneck` (Vickrey 1969 in the form of Arnott, de Palma and Lindsey: the equilibrium queue
and its cost, and the time-varying toll that removes it).

Plain numpy.
"""

from __future__ import annotations

import numpy as np

# Coase (1960), p. 3: the annual crop loss, in tons (the crop sells at $1 a ton), with 1 to 4 steers; fencing costs $9
COASE_LOSS = (0.0, 1.0, 3.0, 6.0, 10.0)
COASE_FENCE = 9.0


def externality(a: float = 100.0, b: float = 1.0, c: float = 10.0, e: float = 1.0, d: float = 0.5) -> dict:
    """Inverse demand P = a - b Q, private marginal cost c + e Q, marginal damage d Q (to third parties).  The market
    produces where demand meets private cost; the efficient quantity where it meets social cost, c + (e + d) Q.  The
    deadweight loss is the triangle between social cost and demand from Q* to the market's Q; Pigou's tax is the
    marginal damage at Q*, and with it the market produces Q*."""
    qm = (a - c) / (b + e)
    qs = (a - c) / (b + e + d)
    pm, ps = a - b * qm, a - b * qs
    dwl = 0.5 * (qm - qs) * ((c + (e + d) * qm) - (a - b * qm))
    tax = d * qs
    damage_m, damage_s = 0.5 * d * qm ** 2, 0.5 * d * qs ** 2
    return {"q_market": float(qm), "q_social": float(qs), "p_market": float(pm), "p_social": float(ps),
            "dwl": float(dwl), "tax": float(tax), "damage_market": float(damage_m), "damage_social": float(damage_s),
            "q_with_tax": float((a - c - tax) / (b + e)), "a": a, "b": b, "c": c, "e": e, "d": d}


def coase(values=(5.0, 4.0, 1.5, -1.0), loss=COASE_LOSS, fence: float = COASE_FENCE, crop_price: float = 1.0,
          transaction_cost: float = 0.0) -> dict:
    """Coase's cattle-raiser and farmer.  ``values``: what the 1st, 2nd, ... steer is worth to the cattle-raiser (the
    meat less its other costs; Agora's numbers, Coase gives none); ``loss``: the farmer's total crop loss with 0, 1,
    2, ... steers (Coase's table), at ``crop_price`` a ton; a fence that stops all damage costs ``fence`` a year.
    Returns the herd that maximizes the joint value, and the herd under each liability rule: with costless bargaining
    both give the joint optimum (the Coase theorem); a bargain costs ``transaction_cost``, and is struck only if the
    gain from it is larger.  The payments differ: who pays whom is what the rule decides."""
    vals = np.concatenate([[0.0], np.cumsum(values)])
    dam = np.asarray(loss, float) * crop_price
    n = len(values)
    joint = [vals[k] - min(dam[k], fence) for k in range(n + 1)]
    k_star = int(np.argmax(joint))
    fence_used = bool(dam[k_star] > fence)
    # liable: the cattle-raiser bears the damage (or fences) and chooses the joint optimum himself: no bargain needed
    liable = k_star
    # not liable: the cattle-raiser alone would keep every steer worth something; the farmer would fence or pay
    k_alone = int(np.argmax(vals))
    farmer_cost_alone = min(dam[k_alone], fence)
    gain = joint[k_star] - (vals[k_alone] - farmer_cost_alone)
    not_liable = k_star if gain > transaction_cost else k_alone
    # the farmer's payment to reduce the herd from k_alone to k_star: at least what the cattle-raiser gives up
    payment_min = float(vals[k_alone] - vals[k_star])
    payment_max = float(farmer_cost_alone - min(dam[k_star], fence))
    marginal_damage = np.diff(dam)
    return {"values": list(map(float, values)), "loss": list(map(float, dam)), "marginal_damage": marginal_damage,
            "joint": [float(j) for j in joint], "k_star": k_star, "fence_used": fence_used, "liable": liable,
            "not_liable": not_liable, "k_alone": k_alone, "gain_from_bargain": float(gain),
            "payment_range": (payment_min, payment_max), "transaction_cost": transaction_cost}


def public_good(thetas=(4.0, 3.0, 2.0, 1.0), mc: float = 1.0) -> dict:
    """n consumers value a public good G at theta_i ln(1 + G) (in money); it costs ``mc`` a unit.  Samuelson's
    condition: the sum of marginal benefits, sum theta_i / (1 + G), equals the marginal cost, so G* = sum theta/mc - 1.
    Voluntary provision (the Nash equilibrium of private contributions): only the keenest contributes, up to
    theta_max/(1 + G) = mc.  Lindahl's prices: consumer i pays the share theta_i / sum theta of each unit, and then
    everyone asks for G*."""
    th = np.asarray(thetas, float)
    g_star = max(th.sum() / mc - 1, 0.0)
    g_nash = max(th.max() / mc - 1, 0.0)
    w = lambda g: float(np.sum(th * np.log1p(g)) - mc * g)
    return {"thetas": th.tolist(), "g_star": float(g_star), "g_nash": float(g_nash), "w_star": w(g_star),
            "w_nash": w(g_nash), "lindahl_shares": (th / th.sum()).tolist(),
            "lindahl_prices": (mc * th / th.sum()).tolist(), "mc": mc}


def vcm(groups: int = 400, rounds: int = 10, n: int = 4, endowment: float = 20.0, mpcr: float = 0.4,
        punish: bool = False, share_cc: float = 0.5, share_fr: float = 0.3, slope: float = 0.75,
        punish_slope: float = 1.05,
        punish_cost: float = 1.0, punish_impact: float = 3.0, seed: int = 2000) -> dict:
    """A voluntary-contribution game played by Agora's typed players (a model in the spirit of Fischbacher, Gächter
    and Fehr 2001, not their data).  Each round every player keeps what they don't put in the pot; the pot is
    multiplied by n * mpcr and shared equally.  Conditional cooperators (``share_cc``) put in ``slope`` times what they
    expect the others to give (last round's average; half the endowment in round 1), plus noise; free riders
    (``share_fr``) put in nothing, or a little early on; the rest give a random amount.  With ``punish``, after each
    round cooperators spend ``punish_cost`` to cut ``punish_impact`` from a player who gave well below the group's
    average; a punished player learns to give at least the average from then on, and cooperators, no longer afraid
    of being exploited, give a little more than they expect of others (``punish_slope``).  Returns the
    average contribution as a share of the endowment, round by round."""
    rng = np.random.default_rng(seed)
    kinds = rng.choice(3, size=(groups, n), p=[share_cc, share_fr, 1 - share_cc - share_fr])
    give = np.zeros((groups, n))
    learned = np.zeros((groups, n))           # what a punished free rider has learned to give
    path, payoff = [], []
    others_prev = np.full((groups, n), 0.7 * endowment)        # round 1: cooperators expect others to give 70%
    k = punish_slope if punish else slope
    for t in range(rounds):
        noise = rng.normal(0, endowment * 0.08, (groups, n))
        cc = np.clip(k * others_prev + noise, 0, endowment)
        fr = np.clip(np.where(t < 2, rng.uniform(0, endowment * 0.15, (groups, n)), 0.0), 0, endowment)
        fr = np.maximum(fr, learned)
        rnd = np.maximum(rng.uniform(0, endowment, (groups, n)), learned)
        give = np.where(kinds == 0, cc, np.where(kinds == 1, fr, rnd))
        pot = give.sum(axis=1, keepdims=True)
        pay = endowment - give + mpcr * pot
        if punish:
            mean = give.mean(axis=1, keepdims=True)
            low = give < 0.6 * mean
            punishers = (kinds == 0).sum(axis=1, keepdims=True)
            pay = pay - low * punish_impact * punishers - (kinds == 0) * punish_cost * low.sum(axis=1, keepdims=True)
            # a punished player learns to give enough that the expected punishment no longer pays: about the mean
            learned = np.where(low & (kinds != 0), np.minimum(endowment, np.maximum(learned, mean)), learned)
        tot = give.sum(axis=1, keepdims=True)
        others_prev = (tot - give) / (n - 1)
        path.append(float(give.mean() / endowment))
        payoff.append(float(pay.mean()))
    return {"rounds": list(range(1, rounds + 1)), "share": path, "payoff": payoff, "punish": punish, "mpcr": mpcr,
            "endowment": endowment, "n": n}


def fishery(K: float = 1.0, r: float = 0.5, q: float = 0.01, p: float = 100.0, c: float = 0.3,
            efforts=None) -> dict:
    """Gordon (1954) with Schaefer's growth: the stock grows by r X (1 - X/K) and effort E catches q E X.  In steady
    state X = K (1 - q E / r), so sustainable yield Y(E) = q E K (1 - q E / r).  Revenue p Y, cost c E.  Open access:
    boats enter until revenue equals cost, E_oa = (r/q)(1 - c/(p q K)), where the resource's rent is gone; the rent is
    largest at E_mey = E_oa / 2; the most fish at E_msy = r/(2q)."""
    e_max = r / q
    es = np.linspace(0, e_max, 401) if efforts is None else np.asarray(efforts, float)
    y = q * es * K * (1 - q * es / r)
    rev, cost = p * y, c * es
    e_oa = max((r / q) * (1 - c / (p * q * K)), 0.0)
    e_mey = e_oa / 2
    e_msy = r / (2 * q)
    yy = lambda e: q * e * K * (1 - q * e / r)
    return {"effort": es, "yield": y, "revenue": rev, "cost": cost, "e_oa": float(e_oa), "e_mey": float(e_mey),
            "e_msy": float(e_msy), "rent_mey": float(p * yy(e_mey) - c * e_mey), "rent_oa": float(p * yy(e_oa) - c * e_oa),
            "y_oa": float(yy(e_oa)), "y_mey": float(yy(e_mey)), "y_msy": float(yy(e_msy)),
            "stock_oa": float(K * (1 - q * e_oa / r)), "stock_mey": float(K * (1 - q * e_mey / r))}


def prices_quantities(mb_slope: float, mc_slope: float, sigma: float = 1.0, b0: float = 10.0, c0: float = 2.0,
                      draws: int = 20000, seed: int = 1974) -> dict:
    """Weitzman (1974).  The marginal benefit of abatement Q is b0 - mb_slope Q; its marginal cost c0 + theta +
    mc_slope Q, with theta ~ N(0, sigma^2) unknown to the regulator when it sets either a tax t or a quota Q.  The
    best quota is the expected optimum; the best tax is the marginal cost there.  Expected losses against the
    optimum for each theta: quota, sigma^2 / (2 (mb + mc)); tax, sigma^2 mb^2 / (2 mc^2 (mb + mc)); their difference,
    sigma^2 (mc - mb) / (2 mc^2), favours the tax when marginal cost is steeper than marginal benefit."""
    bb, cc = mb_slope, mc_slope
    q_bar = (b0 - c0) / (bb + cc)
    t = c0 + cc * q_bar
    rng = np.random.default_rng(seed)
    th = rng.normal(0, sigma, draws)
    q_opt = (b0 - c0 - th) / (bb + cc)
    q_tax = (t - c0 - th) / cc

    def loss(qq):
        return 0.5 * (bb + cc) * (qq - q_opt) ** 2

    lq_sim, lt_sim = float(loss(np.full_like(th, q_bar)).mean()), float(loss(q_tax).mean())
    lq = sigma ** 2 / (2 * (bb + cc))
    lt = sigma ** 2 * bb ** 2 / (2 * cc ** 2 * (bb + cc))
    return {"q_bar": float(q_bar), "tax": float(t), "loss_quota": float(lq), "loss_tax": float(lt),
            "loss_quota_sim": lq_sim, "loss_tax_sim": lt_sim, "delta": float(sigma ** 2 * (cc - bb) / (2 * cc ** 2)),
            "prefer": "tax" if lt < lq else "quota", "mb_slope": bb, "mc_slope": cc, "sigma": sigma}


def lock_in(runs: int = 12, adopters: int = 1000, taste: float = 1.0, network: float = 0.1, seed: int = 1989) -> dict:
    """Arthur (1989): adopters arrive one at a time; half prefer technology A by ``taste``, half prefer B; each also
    gains ``network`` for every earlier adopter of the same technology.  Once one technology leads by more than
    taste/network adopters, everyone picks it: the market locks in, to either one, by the luck of who came first.
    Returns, for each run, A's share of adopters so far, its share among the last 50, and when the run locked in."""
    rng = np.random.default_rng(seed)
    paths, recent, winners, lock_at = [], [], [], []
    for _ in range(runs):
        na = nb = 0
        share, picks, locked = [], [], None
        for k in range(adopters):
            likes_a = rng.random() < 0.5
            ua = (taste if likes_a else 0.0) + network * na
            ub = (0.0 if likes_a else taste) + network * nb
            if ua >= ub:
                na += 1
                picks.append(1)
            else:
                nb += 1
                picks.append(0)
            share.append(na / (k + 1))
            if locked is None and abs(na - nb) * network > taste:
                locked = k + 1
        win = np.convolve(picks, np.ones(50) / 50, mode="full")[:adopters]
        paths.append(share)
        recent.append([float(x) for x in win])
        winners.append("A" if na > nb else "B")
        lock_at.append(locked)
    return {"paths": paths, "recent": recent, "winners": winners, "lock_at": lock_at,
            "lead_to_lock": float(taste / network), "adopters": adopters}


def bottleneck(N: float = 6000.0, s: float = 4000.0, alpha: float = 20.0, beta: float = 10.0, gamma: float = 40.0,
               t_star: float = 9.0) -> dict:
    """Vickrey's bottleneck (1969), as Arnott, de Palma and Lindsey solve it: N commuters must pass a road that
    carries s an hour; each wants to arrive at t_star, and counts time in the queue at alpha an hour, arriving early at
    beta an hour, late at gamma.  In equilibrium everyone's cost is the same, delta N / s with delta = beta gamma /
    (beta + gamma); arrivals run at capacity from t_star - (gamma/(beta+gamma)) N/s to t_star + (beta/(beta+gamma))
    N/s, and half the total cost is time in the queue.  A toll that rises and falls with the queue it replaces removes
    the queue, leaves arrivals and schedule costs as they were, and so halves the social cost (the toll is a transfer).
    Returns the queue (in commuters) and the queueing time against the time of arrival at work, and the toll."""
    delta = beta * gamma / (beta + gamma)
    t0 = t_star - gamma / (beta + gamma) * N / s
    t1 = t_star + beta / (beta + gamma) * N / s
    ts = np.linspace(t0, t1, 301)
    # an arrival at time t waits so that queueing plus schedule cost equals the equilibrium cost
    early = ts <= t_star
    sched = np.where(early, beta * (t_star - ts), gamma * (ts - t_star))
    cost_each = delta * N / s
    wait = (cost_each - sched) / alpha                       # hours in the queue, for arrival at work at time t
    queue = wait * s                                         # commuters in the queue
    toll = cost_each - sched                                 # the toll that replaces the queue, in money
    return {"t": ts, "wait_hours": wait, "queue": queue, "toll": toll, "t0": float(t0), "t1": float(t1),
            "cost_each": float(cost_each), "total_cost": float(cost_each * N), "queue_cost": float(cost_each * N / 2),
            "schedule_cost": float(cost_each * N / 2), "max_wait_min": float(60 * wait.max()), "delta": float(delta),
            "N": N, "s": s, "alpha": alpha, "beta": beta, "gamma": gamma, "t_star": t_star}

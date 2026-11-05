"""Market making (Part 38): what a quoting business earns, measured and modelled.

Measurement on a grid of best quotes and the trade tape (Part 36's data): the fill intensity of a quote at a distance
from the mid, fitted as A exp(-k delta) (Avellaneda and Stoikov 2008); a two-sided maker replayed against the real
tape, with its P&L split into spread, adverse selection and inventory. Models: the sniping equilibrium of Budish,
Cramton and Shim (2015), in closed form and simulated, in a continuous market and in frequent batch auctions."""

from __future__ import annotations

import math

import numpy as np

from .lob import mid


# ---------------------------------------------------------------------------
# Fill intensity
# ---------------------------------------------------------------------------
def fill_intensity(b, trades, deltas, horizon: int = 10, tick: float = 0.1) -> dict:
    """For quotes resting ``delta`` ticks from the mid at the start of each window of ``horizon`` grid steps, the
    probability that a taker trades at or through them within the window (buys reach asks above, sells reach bids
    below; both pooled), and the implied Poisson intensity lambda(delta) = -log(1 - P)/window. A least-squares fit of
    log lambda on delta gives A and k."""
    t_grid = np.asarray(b["time"], float)
    m = mid(b)
    step = float(np.median(np.diff(t_grid)))
    tt = np.asarray(trades["time"], float)
    tp = np.asarray(trades["price"], float)
    sg = np.asarray(trades["sign"], float)
    w = ((tt - t_grid[0]) // (step * horizon)).astype(np.int64)
    nw = len(t_grid) // horizon
    ok = (w >= 0) & (w < nw)
    w, tp, sg = w[ok], tp[ok], sg[ok]
    m0 = m[np.arange(nw) * horizon]
    up = np.full(nw, -np.inf)
    dn = np.full(nw, -np.inf)
    buy = sg > 0
    np.maximum.at(up, w[buy], (tp[buy] - m0[w[buy]]) / tick)
    np.maximum.at(dn, w[~buy], (m0[w[~buy]] - tp[~buy]) / tick)
    dt = step * horizon / 1000.0
    P = []
    for d in deltas:
        P.append(0.5 * (float(np.mean(up >= d)) + float(np.mean(dn >= d))))
    P = np.asarray(P)
    lam = -np.log(np.clip(1 - P, 1e-12, 1)) / dt
    okf = (P > 0) & (P < 1)
    k, logA = np.polyfit(np.asarray(deltas, float)[okf], np.log(lam[okf]), 1)
    return {"deltas": np.asarray(deltas, float), "P": P, "lam": lam, "A": float(math.exp(logA)), "k": float(-k),
            "dt": dt}


def glft(A: float, k: float, sigma: float, gamma: float, xi: float | None = None) -> dict:
    """Guéant, Lehalle and Fernandez-Tapia's (2013) closed-form approximation for the optimal quotes of a market maker
    with risk aversion gamma (xi = gamma unless given), fill intensities A exp(-k delta), price volatility sigma: the
    half-spread at zero inventory and the skew per unit of inventory,
        half = (1/xi) log(1 + xi/k) + 1/2 sqrt(sigma^2 gamma / (2 A k) (1 + xi/k)^(1 + k/xi)),
        skew = sqrt(sigma^2 gamma / (2 A k) (1 + xi/k)^(1 + k/xi))."""
    xi = gamma if xi is None else xi
    c = math.sqrt(sigma ** 2 * gamma / (2 * A * k) * (1 + xi / k) ** (1 + k / xi))
    half = (1 / xi) * math.log(1 + xi / k) + 0.5 * c
    return {"half_spread": half, "skew": c, "static": (1 / xi) * math.log(1 + xi / k)}


# ---------------------------------------------------------------------------
# A maker on the tape
# ---------------------------------------------------------------------------
def maker_replay(b, trades, max_inv: int = 5, filt: float | None = None, after=(10, 100, 600), tick: float = 0.1,
                 start: int = 0, stop: int | None = None, fast: bool = False) -> dict:
    """Replay a small two-sided maker against a grid of best quotes and the trade tape. Whenever it has no resting
    order on a side (and its inventory allows, |inventory| < ``max_inv`` units), it joins the back of the best queue on
    that side; when the best price moves away from its order, it cancels and rejoins at the new best. Fills follow
    Part 36's queue logic (trades eat the queue from the front, cancellations pro rata, trades through the price fill).
    With ``filt``, it does not post a bid when the queue imbalance is below ``filt`` (the bid is thin) nor an ask when
    it is above 1 - ``filt``, and cancels such orders. With ``fast``, an idealised maker that cancels before any sweep: a
    step in which trades go through its price never fills it (an upper bound on the value of speed). Returns the fills (step, side +1 buy / -1 sell, price) and,
    per fill, the half-spread earned against the mid at the fill and the markouts at ``after`` steps, in ticks, plus
    the inventory path and the P&L marked to the final mid."""
    pb, pa = np.asarray(b["bid"], float), np.asarray(b["ask"], float)
    qb, qa = np.asarray(b["bq"], float), np.asarray(b["aq"], float)
    m = (pb + pa) / 2
    I = qb / np.maximum(qb + qa, 1e-12)
    t_grid = np.asarray(b["time"], float)
    step = float(np.median(np.diff(t_grid)))
    tt = np.asarray(trades["time"], float)
    tp = np.asarray(trades["price"], float)
    tq = np.asarray(trades["qty"], float)
    ts = np.asarray(trades["sign"], float)
    gi = np.clip(((tt - t_grid[0]) // step).astype(np.int64), 0, len(t_grid) - 1)
    n = len(pb) if stop is None else min(stop, len(pb))
    j = int(np.searchsorted(gi, start))
    inv = 0
    bid = None                      # [price, ahead]
    ask = None
    fills = []
    inv_path = np.zeros(n - start)
    for t in range(start, n):
        sold_at_bid = 0.0          # taker sells at our bid price this step
        bought_at_ask = 0.0
        through_b = through_a = False
        while j < len(gi) and gi[j] == t:
            if ts[j] < 0 and bid is not None:
                if tp[j] < bid[0] - 1e-9:
                    through_b = True
                elif abs(tp[j] - bid[0]) < 1e-9:
                    sold_at_bid += tq[j]
            elif ts[j] > 0 and ask is not None:
                if tp[j] > ask[0] + 1e-9:
                    through_a = True
                elif abs(tp[j] - ask[0]) < 1e-9:
                    bought_at_ask += tq[j]
            j += 1
        # fills
        if fast and through_b:
            bid = None
        if fast and through_a:
            ask = None
        if bid is not None and (through_b or sold_at_bid > bid[1] + 1e-12):
            fills.append((t, 1, bid[0]))
            inv += 1
            bid = None
        elif bid is not None:
            bid[1] = max(bid[1] - sold_at_bid, 0.0)
        if ask is not None and (through_a or bought_at_ask > ask[1] + 1e-12):
            fills.append((t, -1, ask[0]))
            inv -= 1
            ask = None
        elif ask is not None:
            ask[1] = max(ask[1] - bought_at_ask, 0.0)
        # queue updates, cancellations and reposting
        if bid is not None:
            if abs(pb[t] - bid[0]) < 1e-9 and t > 0 and abs(pb[t - 1] - bid[0]) < 1e-9:
                net = qb[t] - qb[t - 1] + sold_at_bid
                if net < 0 and qb[t - 1] > 0:
                    bid[1] -= min(-net, qb[t - 1]) * bid[1] / qb[t - 1]
                bid[1] = max(min(bid[1], qb[t]), 0.0)
            elif pb[t] > bid[0] + 1e-9:
                bid = None                                   # the market moved up: cancel, rejoin below
            elif pb[t] < bid[0] - 1e-9:
                bid[1] = 0.0                                 # alone at the old price
        if ask is not None:
            if abs(pa[t] - ask[0]) < 1e-9 and t > 0 and abs(pa[t - 1] - ask[0]) < 1e-9:
                net = qa[t] - qa[t - 1] + bought_at_ask
                if net < 0 and qa[t - 1] > 0:
                    ask[1] -= min(-net, qa[t - 1]) * ask[1] / qa[t - 1]
                ask[1] = max(min(ask[1], qa[t]), 0.0)
            elif pa[t] < ask[0] - 1e-9:
                ask = None
            elif pa[t] > ask[0] + 1e-9:
                ask[1] = 0.0
        if filt is not None:
            if bid is not None and I[t] < filt:
                bid = None
            if ask is not None and I[t] > 1 - filt:
                ask = None
        if bid is None and inv < max_inv and (filt is None or I[t] >= filt):
            bid = [pb[t], qb[t]]
        if ask is None and inv > -max_inv and (filt is None or I[t] <= 1 - filt):
            ask = [pa[t], qa[t]]
        inv_path[t - start] = inv
    F = np.array(fills, float).reshape(-1, 3)
    out = {"n_fills": int(len(F)), "inv_path": inv_path, "final_inv": inv}
    if len(F):
        st = F[:, 0].astype(int)
        sd = F[:, 1]
        px = F[:, 2]
        out["half_spread"] = sd * (m[np.maximum(st - 1, 0)] - px) / tick
        out["move_in_step"] = sd * (m[st] - m[np.maximum(st - 1, 0)]) / tick
        for h in after:
            k = np.minimum(st + h, n - 1)
            out[f"mk{h}"] = sd * (m[k] - px) / tick
        out["pnl_final"] = float(np.sum(sd * (m[n - 1] - px)) / tick)
        out["fills"] = F
    return out


# ---------------------------------------------------------------------------
# The sniping equilibrium (Budish, Cramton and Shim 2015)
# ---------------------------------------------------------------------------
def bcs_spread(lam_invest: float, lam_jump: float, J: float) -> float:
    """The equilibrium half-spread in BCS's continuous limit order book with a deterministic jump size J: a liquidity
    provider earns lam_invest * s/2 from investors and loses (N-1)/N of the jumps' value to snipers; indifference with
    sniping, lam_invest s/2 - lam_jump (N-1)/N (J - s/2) = lam_jump (1/N)(J - s/2), gives
    s/2 = lam_jump J / (lam_invest + lam_jump), independent of N."""
    return lam_jump * J / (lam_invest + lam_jump)


def bcs_simulate(half: float, lam_invest: float, lam_jump: float, J: float, N: int, T: float, seed: int = 0,
                 batch: float | None = None) -> dict:
    """Simulate BCS's market for time T with one liquidity provider quoting value +- ``half`` and N - 1 snipers, all
    equally fast. Investors arrive at rate lam_invest and trade one unit against the quote, paying ``half``. At a jump
    of +-J, the provider and the snipers race: the provider's cancel wins with probability 1/N, otherwise a sniper
    trades the stale quote and gains J - half. With ``batch`` (frequent batch auctions of that interval), quotes are
    re-set at each auction with the current value, so a jump is never traded against a stale quote: the race prize is
    zero. Returns the provider's and each sniper's profit per unit time."""
    rng = np.random.default_rng(seed)
    n_inv = rng.poisson(lam_invest * T)
    n_jump = rng.poisson(lam_jump * T)
    lp = n_inv * half
    snipe = 0.0
    if batch is None and J > half:
        won = rng.random(n_jump) > 1.0 / N
        lp -= float(np.sum(won)) * (J - half)
        snipe = float(np.sum(won)) * (J - half)
    return {"lp": lp / T, "sniper": snipe / max(N - 1, 1) / T, "n_jump": int(n_jump), "n_inv": int(n_inv)}

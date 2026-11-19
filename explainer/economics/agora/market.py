"""A market of traders with one unit each (Agora, Part 1; Part 2 builds on it).

Each buyer holds a card with a *value*, the most she will pay for one unit; each seller holds a card with a
*cost*, the least he will take.  Nobody sees anyone else's card.  This is the design of Chamberlin (1948) and
Vernon Smith (1962).

* :class:`Market` sorts the cards into a demand and a supply schedule and gives the competitive prediction: the
  quantity, the band of prices that clear the market, and the largest total surplus any allocation can reach.
* :func:`double_auction` runs a continuous double auction (anyone may call out a bid or an offer; a bid at or above
  the best offer, or an offer at or below the best bid, is a trade at the standing quote), period after period with
  the same cards, as in Smith's experiments.  Two kinds of trader:

  - ``"zi"``: Gode and Sunder's (1993) zero-intelligence traders with a budget constraint: every shout is drawn at
    random between the trader's limit and the edge of the price range, and nobody learns anything;
  - ``"zip"``: Cliff's (1997) zero-intelligence-plus traders, who keep a margin over their limit and nudge it after
    every shout by the Widrow-Hoff rule (raise it when deals happen at better prices than yours, lower it when your
    price would not have traded).  They learn from period to period, as Smith's students did.

* :func:`convergence_alpha` is Smith's coefficient of convergence, 100 times the root-mean-square deviation of the
  period's prices from the competitive price, divided by that price; :func:`efficiency` the share of the possible
  surplus that the trades captured.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Market:
    values: tuple  # buyers' limit prices
    costs: tuple  # sellers' limit prices
    floor: float = 0.0  # the lowest price anyone may call
    ceiling: float = 5.0  # the highest

    def __post_init__(self):
        if min(self.costs) < self.floor or max(self.values) > self.ceiling:
            raise ValueError("cards must lie inside the price range")

    # -- the schedules -------------------------------------------------------
    @property
    def v(self) -> np.ndarray:
        """Values, highest first: the demand schedule's steps."""
        return np.sort(np.asarray(self.values, float))[::-1]

    @property
    def c(self) -> np.ndarray:
        """Costs, lowest first: the supply schedule's steps."""
        return np.sort(np.asarray(self.costs, float))

    def demand(self, p: float) -> int:
        """How many buyers would buy at ``p`` (those whose value is at least ``p``)."""
        return int((self.v >= p).sum())

    def supply(self, p: float) -> int:
        """How many sellers would sell at ``p``."""
        return int((self.c <= p).sum())

    def equilibrium(self) -> dict:
        """The competitive prediction.  ``q``: the largest k with the k-th highest value at least the k-th lowest
        cost; ``p_lo``, ``p_hi``: every price in the band clears the market (demand and supply both equal ``q``);
        ``surplus``: the sum of the ``q`` highest values minus the ``q`` lowest costs, the most any allocation of the
        units can create; ``buyers``, ``sellers``: who trades (indices into the sorted schedules)."""
        v, c = self.v, self.c
        n = min(len(v), len(c))
        q = int(sum(1 for k in range(n) if v[k] >= c[k]))
        lo = max(c[q - 1], v[q] if q < len(v) else self.floor)
        hi = min(v[q - 1], c[q] if q < len(c) else self.ceiling)
        surplus = float(v[:q].sum() - c[:q].sum())
        return {"q": q, "p_lo": float(lo), "p_hi": float(hi), "p": float((lo + hi) / 2), "surplus": surplus,
                "cs_at_mid": float((v[:q] - (lo + hi) / 2).sum()), "ps_at_mid": float(((lo + hi) / 2 - c[:q]).sum())}

    def steps(self) -> dict:
        """The two schedules as step functions for drawing: ``demand``: [(q0, q1, value)], ``supply``: [(q0, q1,
        cost)], one unit wide each."""
        return {"demand": [(k, k + 1, float(x)) for k, x in enumerate(self.v)],
                "supply": [(k, k + 1, float(x)) for k, x in enumerate(self.c)]}


def efficiency(market: Market, trades: list[dict]) -> float:
    """Surplus captured by ``trades`` (each with the buyer's value and the seller's cost) over the most possible."""
    got = sum(t["value"] - t["cost"] for t in trades)
    return float(got / market.equilibrium()["surplus"])


def convergence_alpha(prices, p0: float) -> float:
    """Smith's (1962) coefficient of convergence: 100 sqrt(mean (P - P0)^2) / P0, for one period's prices."""
    x = np.asarray(prices, float)
    if len(x) == 0:
        return float("nan")
    return float(100 * np.sqrt(np.mean((x - p0) ** 2)) / p0)


# ---------------------------------------------------------------------------
# Traders
# ---------------------------------------------------------------------------
class _Trader:
    def __init__(self, kind: str, side: str, limit: float, market: Market, rng: np.random.Generator):
        self.kind, self.side, self.limit, self.m, self.rng = kind, side, float(limit), market, rng
        self.active = True
        if kind == "zip":
            # Cliff (1997): initial margins, learning rate beta, momentum gamma, each drawn per trader
            mu = rng.uniform(0.05, 0.35)
            self.margin = mu if side == "sell" else -mu
            self.beta = rng.uniform(0.1, 0.5)
            self.gamma = rng.uniform(0.0, 0.1)
            self.momentum = 0.0

    def quote(self) -> float:
        """The price this trader would call now."""
        if self.kind == "zi":
            if self.side == "buy":
                return float(self.rng.uniform(self.m.floor, self.limit))
            return float(self.rng.uniform(self.limit, self.m.ceiling))
        return self.limit * (1 + self.margin)

    def _move_toward(self, target: float) -> None:
        p = self.quote()
        delta = self.beta * (target - p)
        self.momentum = self.gamma * self.momentum + (1 - self.gamma) * delta
        new = p + self.momentum
        m = new / self.limit - 1
        self.margin = max(0.0, m) if self.side == "sell" else min(0.0, max(-1.0, m))

    def learn(self, price: float, shout_side: str, dealt: bool) -> None:
        """Cliff's update after a shout at ``price`` by a trader on ``shout_side`` ('buy' or 'sell')."""
        if self.kind != "zip":
            return
        rng, p = self.rng, self.quote()
        up = price * rng.uniform(1.0, 1.05) + rng.uniform(0.0, 0.05)
        down = price * rng.uniform(0.95, 1.0) - rng.uniform(0.0, 0.05)
        if self.side == "sell":
            if dealt:
                if p <= price:
                    self._move_toward(up)  # deals happen above my price: ask for more
                elif shout_side == "buy" and self.active:
                    self._move_toward(down)  # a bid was taken below my price: I would not have traded
            elif shout_side == "sell" and p >= price and self.active:
                self._move_toward(down)  # an offer below mine went unanswered: lower
        else:
            if dealt:
                if p >= price:
                    self._move_toward(down)  # deals happen below my price: offer less
                elif shout_side == "sell" and self.active:
                    self._move_toward(up)
            elif shout_side == "buy" and p <= price and self.active:
                self._move_toward(up)


def double_auction(market: Market, kind: str = "zip", periods: int = 6, seed: int = 0, max_steps: int = 600,
                   patience: int = 120, viewer: int | None = None, tax: float = 0.0, tax_on: str = "sell",
                   cap: float | None = None, minimum: float | None = None) -> dict:
    """Run ``periods`` trading periods with the same cards.  Returns ``{"periods": [{"trades": [...], "shouts":
    [...], "alpha", "efficiency", "mean"}], "equilibrium"}``.  A trade records ``price``, ``value``, ``cost``,
    ``buyer``, ``seller`` (indices into the market's ``values`` and ``costs``) and ``step``.  A shout records
    ``price``, ``side`` and whether it was the best quote when it was made.  ``viewer``: the index of a buyer whose
    trades are marked (the card the film hands to you).

    Part 2's wedges and controls:

    * ``tax``: a tax per unit traded, remitted by the sellers (``tax_on="sell"``: a seller keeps the price less the
      tax, so the least he can call is his cost plus the tax) or by the buyers (``"buy"``: a buyer pays the price plus
      the tax).  Each trade then records ``paid`` (what the buyer gives up) and ``received`` (what the seller keeps);
      ``price`` is the price called in the pit.  Alpha is measured against the untaxed competitive price, and
      efficiency counts the tax as surplus (it goes to someone), so what is lost is the trades that did not happen.
    * ``cap`` / ``minimum``: a legal maximum or minimum price.  No bid or offer may break it (quotes are clipped to
      it), and a seller whose cost is above the cap, or a buyer whose value is below the minimum, cannot trade at
      all.  Under a binding cap more buyers want to buy than sellers will sell, and who gets the units is decided by
      who calls first, not by who values them most."""
    if tax_on not in ("sell", "buy"):
        raise ValueError("tax_on is 'sell' or 'buy'")
    rng = np.random.default_rng(seed)
    t_b, t_s = (tax, 0.0) if tax_on == "buy" else (0.0, tax)
    buyers = [_Trader(kind, "buy", v - t_b, market, rng) for v in market.values]
    sellers = [_Trader(kind, "sell", c + t_s, market, rng) for c in market.costs]
    true_v, true_c = list(market.values), list(market.costs)
    eq = market.equilibrium()
    out = []
    for period in range(periods):
        for k, t in enumerate(buyers):
            t.active = (minimum is None or true_v[k] - t_b >= minimum) and true_v[k] - t_b > market.floor
        for k, t in enumerate(sellers):
            t.active = cap is None or true_c[k] + t_s <= cap
        best_bid, best_ask = None, None  # (price, index)
        trades, shouts = [], []
        idle = 0
        for step in range(max_steps):
            live = [("buy", i) for i, b in enumerate(buyers) if b.active] + \
                   [("sell", j) for j, s in enumerate(sellers) if s.active]
            if not live or idle > patience:
                break
            side, i = live[rng.integers(len(live))]
            trader = buyers[i] if side == "buy" else sellers[i]
            q = trader.quote()
            if cap is not None:
                q = min(q, cap)
            if minimum is not None:
                q = max(q, minimum)
            dealt, price = False, q
            if side == "buy":
                if best_ask is not None and q >= best_ask[0]:
                    price, j = best_ask
                    trades.append({"price": price, "buyer": i, "seller": j, "value": true_v[i], "cost": true_c[j],
                                   "paid": price + t_b, "received": price - t_s, "step": step,
                                   "viewer": i == viewer})
                    buyers[i].active = sellers[j].active = False
                    best_bid = best_ask = None
                    dealt = True
                elif best_bid is None or q > best_bid[0]:
                    best_bid = (q, i)
                    shouts.append({"price": q, "side": "buy", "step": step})
            else:
                if best_bid is not None and q <= best_bid[0]:
                    price, j = best_bid
                    trades.append({"price": price, "buyer": j, "seller": i, "value": true_v[j], "cost": true_c[i],
                                   "paid": price + t_b, "received": price - t_s, "step": step,
                                   "viewer": j == viewer})
                    buyers[j].active = sellers[i].active = False
                    best_bid = best_ask = None
                    dealt = True
                elif best_ask is None or q < best_ask[0]:
                    best_ask = (q, i)
                    shouts.append({"price": q, "side": "sell", "step": step})
            idle = 0 if dealt else idle + 1
            for t in buyers + sellers:
                t.learn(price, side, dealt)
        prices = [t["price"] for t in trades]
        out.append({"trades": trades, "shouts": shouts, "n": len(trades),
                    "alpha": convergence_alpha(prices, eq["p"]),
                    "efficiency": efficiency(market, trades) if trades else 0.0,
                    "mean": float(np.mean(prices)) if prices else float("nan"),
                    "paid": float(np.mean([t["paid"] for t in trades])) if trades else float("nan"),
                    "received": float(np.mean([t["received"] for t in trades])) if trades else float("nan")})
    return {"periods": out, "equilibrium": eq, "kind": kind, "seed": seed, "tax": tax, "tax_on": tax_on, "cap": cap,
            "minimum": minimum}

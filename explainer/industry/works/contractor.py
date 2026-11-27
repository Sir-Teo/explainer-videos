"""The Works' contractor (Part 24): sealed bids for jobs whose cost nobody knows exactly, and the cash a contractor holds.

The tender.  A job's true cost is ``cost``.  Each bidder estimates it with an error that is normal with standard deviation
``sd`` (a share of the cost) and bids its estimate plus a markup; the four rivals add ``rival_markup``.  The lowest bid
wins and is paid its bid.  Because the winner is usually the bidder whose estimate was lowest, the margin a winner earns
is well below the markup it added: the winner's curse.  Expectations are exact integrals over the bidder's own error on a
fine grid; the rivals' bids enter through the normal distribution.

The cash.  A contractor bills each month for the work done and is paid ``receive_lag`` months later, less a retention
released at the end; it pays its subcontractors and suppliers ``pay_lag`` months after the work.  When it pays later than
it is paid, its jobs hand it cash while they run (negative working capital), so a growing order book funds itself and a
shrinking one drains cash even when every job makes money.  All numbers are this series' illustrations.  No manim.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.stats import norm


@dataclass(frozen=True)
class Tender:
    cost: float = 100.0         # the job's true cost, $m
    sd: float = 0.05            # each bidder's estimating error, standard deviation as a share of the cost
    rivals: int = 4
    rival_markup: float = 0.08  # what the rivals add to their estimates
    grid: int = 4001

    def _eps(self):
        e = np.linspace(-7 * self.sd, 7 * self.sd, self.grid)
        w = norm.pdf(e / self.sd)
        return e, w / w.sum()

    def _win(self, bids):
        """Chance that every rival bids above ``bids``."""
        rival_eps = bids / (self.cost * (1 + self.rival_markup)) - 1
        return norm.sf(rival_eps / self.sd) ** self.rivals

    def bid(self, markup: float) -> dict:
        """Averages for one tender at ``markup``: the chance of winning, the profit per tender, the margin on work won,
        the chance a won job loses money, and how far below the true cost the winner's estimate was on average."""
        e, w = self._eps()
        b = (1 + markup) * (1 + e) * self.cost
        pw = self._win(b)
        win = float(w @ pw)
        profit = float(w @ (pw * (b - self.cost)))
        revenue = float(w @ (pw * b))
        return {"markup": markup, "win": win, "profit": profit, "margin": profit / revenue if revenue else 0.0,
                "loss_if_won": float(w @ (pw * (b < self.cost))) / win if win else 0.0,
                "est_if_won": float(w @ (pw * e)) / win if win else 0.0}

    def best(self) -> dict:
        ms = np.linspace(0.0, 0.25, 251)
        return max((self.bid(float(m)) for m in ms), key=lambda r: r["profit"])

    def five(self, markup: float, n: int = 5) -> dict:
        """Five tenders: expected wins, expected profit, the chance of winning none, and of winning at least one job that
        loses money."""
        r = self.bid(markup)
        p_bad = r["win"] * r["loss_if_won"]
        return {"wins": n * r["win"], "profit": n * r["profit"], "none": (1 - r["win"]) ** n,
                "any_loss": 1 - (1 - p_bad) ** n, **{k: r[k] for k in ("win", "margin", "loss_if_won", "est_if_won")}}

    def choices(self, markups=(0.02, 0.08, 0.15)) -> dict:
        return {m: self.five(m) for m in markups}


def job_flows(value: float = 100.0, margin: float = 0.03, months: int = 12, receive_lag: int = 2, pay_lag: int = 3,
              retention: float = 0.05, release: int = 6, horizon: int = 36) -> np.ndarray:
    """Monthly net cash of one job started at month 0: paid for its work ``receive_lag`` months after doing it, less
    ``retention`` held until ``release`` months after completion; paying its costs ``pay_lag`` months after the work."""
    out = np.zeros(horizon)
    bill, cost = value / months, value * (1 - margin) / months
    for t in range(months):
        if t + receive_lag < horizon:
            out[t + receive_lag] += bill * (1 - retention)
        if t + pay_lag < horizon:
            out[t + pay_lag] -= cost
    if months + release < horizon:
        out[months + release] += value * retention
    return out


def cash_path(starts, **kw) -> dict:
    """The contractor's cash month by month for jobs started at the counts in ``starts`` (jobs a month), and its profit
    booked as work is done (margin x value / months per active job-month)."""
    horizon = len(starts) + 30
    flows = job_flows(horizon=horizon, **kw)
    cash = np.zeros(horizon)
    for t, n in enumerate(starts):
        if n:
            cash[t:] += n * flows[: horizon - t]
    value, margin, months = kw.get("value", 100.0), kw.get("margin", 0.03), kw.get("months", 12)
    booked = np.zeros(horizon)
    for t, n in enumerate(starts):
        booked[t:t + months] += n * value * margin / months
    return {"cash": np.cumsum(cash), "profit": np.cumsum(booked), "months": horizon}

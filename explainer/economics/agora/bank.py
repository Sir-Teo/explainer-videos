"""Agora's banks (Part 26 of *Economics, Built*): why a bank that makes everyone better off can be run.

* :func:`dd_contract`: Diamond and Dybvig's (1983) economy: a share ``t`` of depositors turn out to need their money
  early; an investment pays ``R`` if held and 1 if cut short.  The deposit contract that insures them, ``c1 > 1``,
  ``c2 = R^(1/gamma) c1``, against autarky's (1, R).
* :func:`dd_stayers`: what a patient depositor gets by waiting when a share ``f`` withdraws early: ``R(1 - f c1)/(1 - f)``
  while the bank lasts; the run threshold where that falls to ``c1``.
* :func:`sequential_service`: a run with depositors served in random order until the bank's assets are gone.
* :func:`global_game`: Morris and Shin's (1998) bank: depositors see the bank's strength with noise, run below a
  threshold; the unique equilibrium threshold ``c / R``, and the share running at each strength, simulated.
* :func:`suspension`: suspending convertibility once the impatient have been paid ends the run.
* :func:`lender_of_last_resort`: a sound but illiquid bank facing withdrawals, selling at fire-sale prices or borrowing
  at a penalty rate against collateral (Bagehot 1873).
* :func:`merton_put`: the value of deposit insurance as a put on the bank's assets (Merton 1977), and why a flat premium
  rewards risk.
* :func:`bond_loss`: the fall in a bond's price when yields rise, and its duration.
* :func:`capital_ratio`: equity over assets and over risk-weighted assets, before and after a loss.
* :func:`deposit_beta`: how much of a rise in the policy rate a deposit rate passed on.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import norm


def _u(c, gamma):
    c = np.asarray(c, float)
    return np.log(c) if abs(gamma - 1) < 1e-12 else c ** (1 - gamma) / (1 - gamma)


def dd_contract(R: float = 1.5, gamma: float = 2.0, t: float = 0.25) -> dict:
    """The optimal deposit contract: max ``t u(c1) + (1 - t) u(c2)`` subject to ``t c1 + (1 - t) c2 / R = 1``;
    ``u'(c1) = R u'(c2)`` gives ``c2 = R^(1/gamma) c1`` and ``c1 = 1/(t + (1 - t) R^(1/gamma - 1))``."""
    c1 = 1.0 / (t + (1 - t) * R ** (1 / gamma - 1))
    c2 = R ** (1 / gamma) * c1
    eu = float(t * _u(c1, gamma) + (1 - t) * _u(c2, gamma))
    ea = float(t * _u(1.0, gamma) + (1 - t) * _u(R, gamma))
    run_threshold = (R - c1) / (c1 * (R - 1))
    return {"c1": float(c1), "c2": float(c2), "autarky": (1.0, R), "eu": eu, "eu_autarky": ea,
            "threshold": float(run_threshold), "R": R, "gamma": gamma, "t": t, "served_in_run": float(1 / c1)}


def dd_stayers(f, c1: float, R: float) -> np.ndarray:
    """A patient depositor's payment at date 2 when a share ``f`` of depositors withdraws ``c1`` at date 1 (the bank
    liquidating at 1 to pay them): ``R(1 - f c1)/(1 - f)`` while ``f c1 < 1``, else nothing."""
    f = np.asarray(f, float)
    out = np.where(f * c1 < 1, R * np.clip(1 - f * c1, 0, None) / np.clip(1 - f, 1e-12, None), 0.0)
    return out


def sequential_service(n: int = 1000, c1: float = 1.2, assets_per: float = 1.0, share_running: float = 1.0,
                       seed: int = 0) -> dict:
    """``n`` depositors, ``share_running`` of whom arrive at the bank in random order asking for ``c1`` each; the bank
    holds ``assets_per`` per depositor, all of it liquidated at 1 if needed.  Returns who is served, in order."""
    rng = np.random.default_rng(seed)
    k = int(round(share_running * n))
    order = rng.permutation(n)[:k]
    cash = assets_per * n
    paid = np.zeros(n)
    served = 0
    for i in order:
        if cash >= c1:
            paid[i] = c1
            cash -= c1
            served += 1
        else:
            paid[i] = cash
            cash = 0.0
            break
    return {"served": served, "asked": k, "share_served": served / max(k, 1), "last_paid": float(paid[order].min()),
            "cash_left": float(cash), "position_cutoff": served}


def global_game(c: float = 1.2, R: float = 2.0, sigma: float = 0.05, n: int = 2000, thetas=None, seed: int = 0) -> dict:
    """Morris and Shin's regime change as a bank: the bank fails if the share withdrawing reaches its strength
    ``theta``.  A depositor who withdraws gets ``c`` (say, from deposit insurance or a sale); one who stays gets ``R``
    if the bank survives and nothing if it fails.  Each sees ``theta + sigma e``; in the unique equilibrium each
    withdraws below a signal ``x*``, and the bank fails exactly when ``theta < theta* = c / R``."""
    theta_star = c / R
    x_star = theta_star - sigma * norm.ppf(1 - c / R)
    thetas = np.linspace(0, 1, 101) if thetas is None else np.asarray(thetas, float)
    rng = np.random.default_rng(seed)
    share, fail = [], []
    for th in thetas:
        x = th + sigma * rng.standard_normal(n)
        a = float(np.mean(x < x_star))
        share.append(a)
        fail.append(bool(a >= th))
    return {"theta_star": float(theta_star), "x_star": float(x_star), "theta": thetas.tolist(), "share": share,
            "fail": fail, "c": c, "R": R, "sigma": sigma}


def suspension(t: float, c1: float, R: float) -> dict:
    """Suspending convertibility after a share ``t`` (the impatient) have withdrawn: the bank pays no more at date 1,
    so a patient depositor who stays is sure of ``R(1 - t c1)/(1 - t) = c2`` and running cannot help: the run
    equilibrium disappears, provided the share of the impatient is known."""
    c2 = float(dd_stayers([t], c1, R)[0])
    return {"c2_guaranteed": c2, "run_pays": c1, "stay": bool(c2 >= c1)}


def lender_of_last_resort(liquid: float, loans: float, deposits: float, equity: float, withdraw: float,
                          fire_price: float = 0.6, haircut: float = 0.2, penalty: float = 0.05) -> dict:
    """A bank with ``liquid`` reserves and ``loans`` worth face value if held faces ``withdraw`` of withdrawals.
    Without a lender it sells loans at ``fire_price`` per unit of face value; with Bagehot's lender it borrows against
    loans, up to ``(1 - haircut)`` of their value, at a ``penalty`` rate.  Returns equity afterwards in each case."""
    need = max(withdraw - liquid, 0.0)
    sold = need / fire_price
    equity_fire = equity - sold * (1 - fire_price)   # selling below value turns the discount into a loss
    feasible_fire = sold <= loans
    can_borrow = need <= (1 - haircut) * loans
    equity_llr = equity - need * penalty
    return {"need": need, "sold": float(sold), "equity_fire": float(equity_fire), "survives_fire": bool(
        feasible_fire and equity_fire > 0), "equity_llr": float(equity_llr), "survives_llr": bool(can_borrow and
                                                                                                  equity_llr > 0)}


def merton_put(V: float, D: float, sigma: float, T: float = 1.0, r: float = 0.0) -> dict:
    """Deposit insurance as a put on the bank's assets (Merton 1977): the insurer pays ``max(D - V_T, 0)``; with
    lognormal assets, the Black-Scholes put.  Equity is the call; with a flat premium, equity gains from more risk."""
    d1 = (np.log(V / D) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put = D * np.exp(-r * T) * norm.cdf(-d2) - V * norm.cdf(-d1)
    call = V * norm.cdf(d1) - D * np.exp(-r * T) * norm.cdf(d2)
    return {"put": float(put), "equity": float(call), "put_per_deposit": float(put / D)}


def bond_loss(coupon: float, years: int, y0: float, y1: float) -> dict:
    """A bond paying ``coupon`` a year for ``years`` years and 1 at the end, priced at yield ``y0`` and then ``y1``:
    the percentage change in price, and its (modified) duration at ``y0``."""
    t = np.arange(1, years + 1)
    cf = np.full(years, coupon, float)
    cf[-1] += 1.0
    p0 = float(np.sum(cf / (1 + y0) ** t))
    p1 = float(np.sum(cf / (1 + y1) ** t))
    mac = float(np.sum(t * cf / (1 + y0) ** t) / p0)
    return {"p0": p0, "p1": p1, "change": p1 / p0 - 1, "duration": mac / (1 + y0)}


def capital_ratio(assets: dict, equity: float, weights: dict | None = None, loss: float = 0.0) -> dict:
    """Equity over total assets (leverage) and over risk-weighted assets, before and after a ``loss``."""
    total = float(sum(assets.values()))
    weights = weights or {k: 1.0 for k in assets}
    rwa = float(sum(v * weights.get(k, 1.0) for k, v in assets.items()))
    return {"leverage": equity / total, "risk_based": equity / rwa, "after_loss": (equity - loss) / (total - loss),
            "after_loss_rb": (equity - loss) / max(rwa - loss, 1e-12), "solvent": equity - loss > 0, "rwa": rwa,
            "total": total}


def deposit_beta(policy_from: float, policy_to: float, deposit_from: float, deposit_to: float) -> float:
    """The share of the change in the policy rate passed on to a deposit rate."""
    return (deposit_to - deposit_from) / (policy_to - policy_from)

"""Markets with private information (Part 13): lemons, signals, screening and selection.

**Lemons.**  :func:`lemons` (Akerlof 1970: sellers know a good's quality, buyers only its distribution; the price at
which the average quality offered is worth the price, for uniform quality with an additive or proportional buyer
premium; partial or total unravelling), :func:`lemons_offers` (one uninformed buyer's offers: who sells, what the
boats bought are worth, the buyer's expected gain), :func:`warranty` (a seller who knows its quality offers a
guarantee only a good seller can afford).

**Signals.**  :func:`spence` (Spence 1973: two worker types, education that costs the low type more and teaches
nothing; the separating range, the least-cost separating equilibrium that the intuitive criterion selects, and the
pooling equilibria).

**Screening.**  :func:`rothschild_stiglitz` (Rothschild and Stiglitz 1976: two risk types and log utility; the
separating menu with full insurance for the high risks and partial cover for the low, the pooling contract that
would break it, and whether the separating pair is an equilibrium).

**Selection in insurance.**  :func:`einav_finkelstein` (the demand and average-cost curves of Einav, Finkelstein and
Cullen 2010: the competitive price where price equals average cost, the efficient price where demand meets marginal
cost, and the welfare triangle), :func:`death_spiral` (a plan priced each year at the average cost of those still
enrolled, as at Harvard after 1995), :func:`positive_correlation` (Chiappori and Salanié's test on simulated drivers,
with adverse and with advantageous selection).

**Credit and reputation.**  :func:`stiglitz_weiss` (after Stiglitz and Weiss 1981: a bank's expected repayment as
the rate rises and the safe borrowers leave; the rate it would rather ration credit at), :func:`reputation` (a buyer's belief that a seller is
honest, updated feedback by feedback, and the price it supports).

Plain numpy and scipy.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq


# ---------------------------------------------------------------------------------------------------------------
# lemons


def lemons(lo: float = 0.0, hi: float = 100.0, premium: float = 30.0, kind: str = "add", n: int = 401) -> dict:
    """Akerlof's market with quality q uniform on [lo, hi], worth q to its owner and v(q) to a buyer: q + premium
    (``kind="add"``) or premium * q (``kind="mult"``).  At a price p every owner with q <= p sells, so the average
    quality offered is (lo + min(p, hi)) / 2, and buyers pay at most its value.  Returns the curve of what the average
    boat offered is worth against the price, and the equilibrium: the highest price at which that value covers the
    price (all trade if it reaches hi, none if only lo)."""
    ps = np.linspace(lo, hi, n)

    def value(p):
        avg = (lo + min(max(p, lo), hi)) / 2
        return avg + premium if kind == "add" else premium * avg

    vals = np.array([value(p) for p in ps])
    ok = vals >= ps - 1e-9
    p_eq = float(ps[ok].max()) if ok.any() else float(lo)
    # refine to the crossing
    if lo < p_eq < hi:
        p_eq = float(brentq(lambda p: value(p) - p, p_eq, min(p_eq + (hi - lo) / (n - 1), hi)))
    share = (min(p_eq, hi) - lo) / (hi - lo)
    efficient = 1.0 if (premium > 0 if kind == "add" else premium > 1) else 0.0
    # the gains from trade lost: every boat above p_eq should change hands
    if kind == "add":
        lost = premium * (1 - share)
    else:
        lost = (premium - 1) * ((hi ** 2 - p_eq ** 2) / 2) / (hi - lo)
    return {"prices": ps, "value_offered": vals, "p_eq": p_eq, "share_traded": float(share),
            "efficient_share": efficient, "lost_gains": float(lost), "lo": lo, "hi": hi, "premium": premium,
            "kind": kind}


def lemons_offers(prices, lo: float = 0.0, hi: float = 100.0, premium: float = 30.0, kind: str = "add") -> list:
    """A single buyer's offers in the lemons market: the chance the owner accepts, the average value of the boats
    accepted to the buyer, and the buyer's expected gain from making the offer."""
    out = []
    for p in prices:
        acc = float(np.clip((p - lo) / (hi - lo), 0, 1))
        avg = (lo + min(max(p, lo), hi)) / 2
        val = avg + premium if kind == "add" else premium * avg
        out.append({"p": float(p), "accept": acc, "value": float(val), "gain_if_sold": float(val - p),
                    "expected_gain": float(acc * (val - p))})
    return out


def warranty(good: float, bad: float, share_good: float, fix_cost: float, chance_breaks_good: float,
             chance_breaks_bad: float) -> dict:
    """A guarantee as a signal: a seller promises to pay ``fix_cost`` if the boat breaks.  It costs a good seller
    ``chance_breaks_good * fix_cost`` and a bad seller ``chance_breaks_bad * fix_cost``; buyers who see the guarantee
    believe the boat is good.  Separation works if the premium a good boat earns is worth the guarantee to a good
    seller but not to a bad one."""
    pool = share_good * good + (1 - share_good) * bad
    gain_good = good - pool - chance_breaks_good * fix_cost
    gain_bad = good - bad - chance_breaks_bad * fix_cost
    return {"pooled_price": float(pool), "good_offers": bool(gain_good > 0), "bad_mimics": bool(gain_bad > 0),
            "separates": bool(gain_good > 0 and gain_bad <= 0)}


# ---------------------------------------------------------------------------------------------------------------
# signals


def spence(theta_low: float = 1.0, theta_high: float = 2.0, cost_low: float = 1.0, cost_high: float = 0.5,
           share_high: float = 0.5) -> dict:
    """Spence's job market with two types of productivity theta_low < theta_high, education that adds nothing to
    productivity and costs cost_low (cost_high) per year to a low (high) type, and competitive employers who pay
    expected productivity.  A separating equilibrium in which highs take e* years and lows none needs
        theta_high - theta_low <= cost_low * e*   (lows don't mimic) and theta_high - theta_low >= cost_high * e*,
    so e* runs from (theta_high - theta_low)/cost_low to (theta_high - theta_low)/cost_high; the intuitive criterion
    (Cho and Kreps 1987) keeps only the cheapest.  Pooling at no education pays everyone the average productivity."""
    gap = theta_high - theta_low
    e_lo, e_hi = gap / cost_low, gap / cost_high
    avg = share_high * theta_high + (1 - share_high) * theta_low
    # the high type's payoff under least-cost separation against pooling at e = 0
    sep_high = theta_high - cost_high * e_lo
    return {"e_min": float(e_lo), "e_max": float(e_hi), "least_cost": float(e_lo), "pool_wage": float(avg),
            "sep_high_net": float(sep_high), "sep_low_net": float(theta_low),
            "high_prefers_pooling": bool(avg > sep_high), "gap": float(gap)}


# ---------------------------------------------------------------------------------------------------------------
# screening


def _eu(W, d, p, cover, premium):
    return (1 - p) * np.log(W - premium) + p * np.log(W - d + cover - premium)


def rothschild_stiglitz(W: float = 100.0, d: float = 60.0, p_low: float = 0.1, p_high: float = 0.4,
                        share_high: float = 0.3, grid: int = 4001) -> dict:
    """Rothschild and Stiglitz's insurance market with log utility, wealth W and a possible loss d, risk types p_low
    and p_high, competitive insurers offering cover x at a fair premium.  The separating menu: the high risks get full
    cover at premium p_high * d; the low risks the largest cover at their fair price p_low that the high risks don't
    prefer to their own.  The pooling contract: full cover at the average risk's fair price.  The separating pair is
    an equilibrium only if no contract at the pooled price, which both types would buy and which would profit, is
    preferred by the low risks (the existence condition: few enough high risks would break it)."""
    full_high = _eu(W, d, p_high, d, p_high * d)
    xs = np.linspace(0, d, grid)
    eu_h = _eu(W, d, p_high, xs, p_low * xs)
    ok = eu_h <= full_high + 1e-12
    x_low = float(xs[ok].max())
    eu_low_sep = float(_eu(W, d, p_low, x_low, p_low * x_low))
    pbar = share_high * p_high + (1 - share_high) * p_low
    # the best pooling contract for the low risks at the average price, any cover
    eu_low_pool = _eu(W, d, p_low, xs, pbar * xs)
    best_pool = float(eu_low_pool.max())
    exists = best_pool <= eu_low_sep + 1e-12
    # the share of high risks above which the separating pair survives
    def gap(lam):
        pb = lam * p_high + (1 - lam) * p_low
        return float(_eu(W, d, p_low, xs, pb * xs).max()) - eu_low_sep
    lam_star = float(brentq(gap, 1e-6, 1 - 1e-6)) if gap(1e-6) > 0 > gap(1 - 1e-6) else float("nan")
    return {"x_high": float(d), "prem_high": float(p_high * d), "x_low": x_low, "prem_low": float(p_low * x_low),
            "eu_low_sep": eu_low_sep, "eu_low_pool": best_pool, "pbar": float(pbar), "exists": bool(exists),
            "share_threshold": lam_star, "W": W, "d": d, "p_low": p_low, "p_high": p_high}


# ---------------------------------------------------------------------------------------------------------------
# selection in insurance markets


def einav_finkelstein(a: float = 0.940, b: float = -0.00070, c0: float = 391.690, c1: float = 0.15524,
                      mcpf: float = 0.3) -> dict:
    """Einav, Finkelstein and Cullen's linear estimates (2010, Table 4): the share buying High coverage at relative
    price p is D(p) = a + b p, and the average incremental cost of those who buy is AC(p) = c0 + c1 p.  In terms of
    the share D: price P(D) = (D - a)/b, AC(D) = c0 + c1 P(D), total cost D * AC(D), marginal cost its derivative.
    The competitive price solves p = AC(p); the efficient one P(D) = MC(D); the welfare loss is the triangle between
    demand and marginal cost over the shares in between; the subsidy that reaches efficiency costs mcpf times its
    outlay."""
    def P(D):
        return (D - a) / b

    def AC(D):
        return c0 + c1 * P(D)

    def MC(D):
        return AC(D) + D * c1 / b

    p_eq = c0 / (1 - c1)
    D_eq = a + b * p_eq
    D_eff = float(brentq(lambda D: P(D) - MC(D), 1e-6, a - 1e-9))
    p_eff = P(D_eff)
    Ds = np.linspace(D_eq, D_eff, 400)
    loss = float(np.trapezoid(P(Ds) - MC(Ds), Ds))
    gap_at_eq = float(P(D_eq) - MC(D_eq))
    subsidy = (p_eq - p_eff) * D_eff
    grid = np.linspace(0.05, 0.94, 200)
    return {"p_eq": float(p_eq), "D_eq": float(D_eq), "p_eff": float(p_eff), "D_eff": D_eff, "loss": loss,
            "gap_at_eq": gap_at_eq, "subsidy_cost": float(mcpf * subsidy), "share_drop": float(D_eff - D_eq),
            "D": grid, "demand": P(grid), "ac": AC(grid), "mc": MC(grid)}


def death_spiral(n: int = 20000, years: int = 5, mean_extra: float = 300.0, sd: float = 1.4, value_mult: float = 1.5,
                 taste_mean: float = -600.0, taste_sd: float = 800.0, base_charge: float = 450.0,
                 seed: int = 1995) -> dict:
    """A generous plan beside a cheaper one.  Each employee's expected extra cost of care in the generous plan, x, is
    lognormal with mean ``mean_extra``; what its extra cover is worth to them is ``value_mult`` x (risk aversion) plus
    a taste for it, normal.  In year 0 the employer holds the employee's extra charge at ``base_charge``; from then on
    the employee pays the plan's extra premium, priced at the average extra cost of those who enrolled the year
    before.  Each year those for whom the plan is no longer worth its charge leave (nobody new joins at a higher
    charge), so the charge climbs and the plan shrinks.  Returns the share enrolled and the charge year by year, and
    the average extra cost of those who stay and of those who leave."""
    rng = np.random.default_rng(seed)
    x = mean_extra * rng.lognormal(-sd ** 2 / 2, sd, n)
    v = value_mult * x + rng.normal(taste_mean, taste_sd, n)
    enrolled = v >= base_charge
    rows = [{"year": 0, "share": float(enrolled.mean()), "charge": float(base_charge),
             "cost_enrolled": float(x[enrolled].mean()), "cost_leavers": float("nan")}]
    for y in range(1, years):
        charge = float(x[enrolled].mean())
        stay = enrolled & (v >= charge)
        leave = enrolled & ~stay
        rows.append({"year": y, "share": float(stay.mean()), "charge": charge,
                     "cost_enrolled": float(x[stay].mean()) if stay.any() else float("nan"),
                     "cost_leavers": float(x[leave].mean()) if leave.any() else float("nan")})
        enrolled = stay
        if not enrolled.any():
            break
    return {"rows": rows, "mean_extra": float(x.mean())}


def positive_correlation(n: int = 20000, selection: str = "adverse", seed: int = 2000) -> dict:
    """Chiappori and Salanié's test on simulated drivers: each has a private accident risk; with ``adverse`` selection
    the riskier buy more cover; with ``advantageous`` selection a private trait (caution) both lowers risk and raises
    the demand for cover; with ``none`` cover is unrelated to risk.  Returns the correlation between full cover and a
    claim, and a 95% interval."""
    rng = np.random.default_rng(seed)
    risk = rng.beta(2, 18, n)                                   # mean 0.1
    if selection == "adverse":
        buy = rng.random(n) < 0.2 + 3.0 * risk
    elif selection == "advantageous":
        caution = rng.random(n)
        risk = np.clip(risk * (1.4 - 0.8 * caution), 0, 1)
        buy = rng.random(n) < 0.15 + 0.6 * caution
    else:
        buy = rng.random(n) < 0.5
    claim = rng.random(n) < risk
    r = float(np.corrcoef(buy.astype(float), claim.astype(float))[0, 1])
    se = (1 - r ** 2) / np.sqrt(n - 1)
    return {"corr": r, "lo": r - 1.96 * se, "hi": r + 1.96 * se, "claim_rate_full": float(claim[buy].mean()),
            "claim_rate_basic": float(claim[~buy].mean()), "share_full": float(buy.mean())}


# ---------------------------------------------------------------------------------------------------------------
# credit and reputation


def stiglitz_weiss(s_safe: float = 0.9, y_safe: float = 160.0, s_risky: float = 0.5, y_risky: float = 130.0,
                   share_safe: float = 0.5, collection_cost: float = 60.0, R_max: float = 280.0) -> dict:
    """A credit market in the spirit of Stiglitz and Weiss (1981).  Two kinds of borrower ask for a loan of 100:
    safe ones whose project succeeds with chance s_safe and is then worth y_safe / s_safe, risky ones with s_risky
    and y_risky / s_risky (y is each project's expected value).  On failure a borrower repays nothing and the bank
    spends ``collection_cost`` trying.  A borrower applies while the project's expected profit, y - s R, is
    positive at the repayment R, so the safe ones leave first, at R = y_safe / s_safe.  The bank's expected
    repayment per loan, the average of s R - (1 - s) cost over those who apply, falls when they do: the rate that
    maximizes it can be below the rate that clears the market, and then the bank rations credit."""
    Rs = np.linspace(100.0, R_max, 1601)
    s = np.array([s_safe, s_risky])
    y = np.array([y_safe, y_risky])
    w = np.array([share_safe, 1 - share_safe])
    ret, share = [], []
    for R in Rs:
        a = y - s * R > 0
        share.append(float(w[a].sum()))
        ret.append(float((w[a] * (s[a] * R - (1 - s[a]) * collection_cost)).sum() / w[a].sum()) if a.any()
                   else float("nan"))
    ret = np.array(ret)
    k = int(np.nanargmax(ret))
    return {"R": Rs, "bank_return": ret, "share_applying": np.array(share), "R_star": float(Rs[k]),
            "return_star": float(ret[k]), "safe_leave": float(y_safe / s_safe), "risky_leave": float(y_risky / s_risky)}


def reputation(prior: float = 0.8, honest_good: float = 0.98, cheat_good: float = 0.7, feedback=None,
               value_honest: float = 100.0, value_cheat: float = 40.0) -> dict:
    """A buyer's belief that a seller is honest, updated by Bayes's rule after each positive or negative feedback (an
    honest seller's sale goes well with chance ``honest_good``, a cheat's with ``cheat_good``), and the price it
    supports: the expected value of buying."""
    fb = list(feedback) if feedback is not None else [1] * 20 + [0] + [1] * 10
    b = prior
    beliefs, prices = [b], [b * value_honest + (1 - b) * value_cheat]
    for f in fb:
        lh = honest_good if f else 1 - honest_good
        lc = cheat_good if f else 1 - cheat_good
        b = b * lh / (b * lh + (1 - b) * lc)
        beliefs.append(b)
        prices.append(b * value_honest + (1 - b) * value_cheat)
    return {"feedback": fb, "belief": np.array(beliefs), "price": np.array(prices)}

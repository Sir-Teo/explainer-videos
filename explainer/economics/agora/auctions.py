"""Auctions (Part 16): an auction house with private and common values, four formats, reserve prices, risk aversion,
the winner's curse, position auctions and the exposure problem.

**Private values.**  :func:`first_price_bid` (the symmetric equilibrium bid with values uniform on [0, 1], n bidders,
a reserve, and constant relative risk aversion), :func:`simulate_formats` (first-price, second-price, English, Dutch
and all-pay auctions run on the same draws of values: revenue equivalence, seen), :func:`myerson` (expected revenue
against the reserve price, by the virtual-value formula, and the optimal reserve).

**Common values.**  :func:`winners_curse` (an object worth V to everyone, each bidder seeing V plus noise: the winner's
expected overestimate, the loss of bidding one's estimate, and the correction that removes it).

**Design.**  :func:`gsp` (position auctions: Vickrey-Clarke-Groves prices, the generalized second price auction's
lowest locally envy-free equilibrium of Edelman, Ostrovsky and Schwarz, and why truthful bidding is not an
equilibrium there), :func:`exposure` (two licences, a bidder who values them only together, and the simultaneous
ascending auction), :func:`multi_unit` (identical units sold by a uniform price, by paying your bids, and by Vickrey's
rule: demand reduction).

**For the viewer.**  :func:`expected_profit` (a bidder's expected profit against rivals who play the equilibrium, for
every bid: Play it), :func:`clock` (an English clock run on one draw of values: who drops out when).

Plain numpy.
"""

from __future__ import annotations

import numpy as np


def first_price_bid(v, n: int, reserve: float = 0.0, alpha: float = 1.0):
    """The symmetric equilibrium bid in a first-price auction with n bidders whose values are uniform on [0, 1].
    Risk neutral (alpha = 1): b(v) = v - (v^n - r^n) / (n v^(n-1)) for v >= r (so (n - 1) v / n with no reserve).
    With utility x^alpha (constant relative risk aversion, no reserve): b(v) = (n - 1) v / (n - 1 + alpha), which is
    higher: a risk-averse bidder pays to lower the chance of losing."""
    v = np.asarray(v, float)
    if alpha != 1.0:
        return (n - 1) * v / (n - 1 + alpha)
    out = np.where(v >= reserve, v - (v ** n - reserve ** n) / (n * np.maximum(v, 1e-12) ** (n - 1)), 0.0)
    return out


def simulate_formats(n: int = 4, draws: int = 50000, reserve: float = 0.0, alpha: float = 1.0, seed: int = 1961) -> dict:
    """Run five auctions on the same draws of private values, uniform on [0, 1]: first-price sealed bid and the Dutch
    clock (strategically the same: bid first_price_bid), second-price sealed bid and the English clock (bid your value;
    the price is the second-highest value, or the reserve), and all-pay (bid ((n - 1)/n) v^n, everyone pays).  Returns
    each format's mean revenue and its standard error, and the theory, (n - 1)/(n + 1) with no reserve."""
    rng = np.random.default_rng(seed)
    v = rng.uniform(0, 1, (draws, n))
    vs = np.sort(v, axis=1)
    top, second = vs[:, -1], vs[:, -2]
    b = first_price_bid(top, n, reserve, alpha)
    first = np.where(top >= reserve, b, 0.0)
    second_p = np.where(top >= reserve, np.maximum(second, reserve), 0.0)
    allpay = ((n - 1) / n) * v ** n
    allpay_rev = allpay.sum(axis=1) if reserve == 0 and alpha == 1.0 else np.full(draws, np.nan)
    out = {}
    for name, r in (("first-price", first), ("Dutch", first), ("second-price", second_p), ("English", second_p),
                    ("all-pay", allpay_rev)):
        out[name] = {"mean": float(np.nanmean(r)), "se": float(np.nanstd(r) / np.sqrt(draws))}
    return {"formats": out, "theory": float((n - 1) / (n + 1)), "n": n, "draws": draws, "reserve": reserve,
            "alpha": alpha, "first_dist": first[:2000].tolist(), "second_dist": second_p[:2000].tolist()}


def myerson(n: int = 2, reserves=None) -> dict:
    """Expected revenue of a second-price (or any standard) auction with a reserve r, values uniform on [0, 1]:
    n * integral_r^1 (2v - 1) v^(n-1) dv = 2n(1 - r^(n+1))/(n + 1) - (1 - r^n), since a bidder's virtual value is
    v - (1 - F(v))/f(v) = 2v - 1.  The optimal reserve sets the virtual value to zero: r* = 1/2, whatever n, and above
    the seller's own value of 0: sometimes the seller should keep the object."""
    rs = np.linspace(0, 1, 201) if reserves is None else np.asarray(reserves, float)
    rev = 2 * n * (1 - rs ** (n + 1)) / (n + 1) - (1 - rs ** n)
    k = int(np.argmax(rev))
    no_sale = 0.5 ** n
    return {"reserve": rs, "revenue": rev, "r_star": float(rs[k]), "rev_star": float(rev[k]),
            "rev_zero": float((n - 1) / (n + 1)), "p_no_sale_at_star": float(no_sale), "n": n}


def winners_curse(ns=(2, 4, 8, 16, 32), value: float = 10.0, noise: float = 3.0, draws: int = 40000,
                  seed: int = 1971) -> dict:
    """A common-value object worth ``value`` to everyone; each of n bidders sees value + e, e uniform on [-noise,
    noise], unbiased.  The highest estimate overstates the value by noise (n - 1)/(n + 1) on average, so a winner who
    bids their estimate loses that much; a bidder who bids their estimate less that amount breaks even (a rough
    correction; the equilibrium shades further).  Returns, for each n, the winner's expected overestimate (simulated
    and exact), and the winner's profit when everyone bids their estimate and when everyone corrects."""
    rng = np.random.default_rng(seed)
    rows = []
    for n in ns:
        e = rng.uniform(-noise, noise, (draws, n))
        top = e.max(axis=1)
        exact = noise * (n - 1) / (n + 1)
        rows.append({"n": int(n), "overestimate": float(top.mean()), "exact": float(exact),
                     "profit_naive": float(-top.mean()), "profit_corrected": float(exact - top.mean())})
    return {"rows": rows, "value": value, "noise": noise}


def gsp(values=(10.0, 8.0, 6.0, 4.0), ctrs=(200.0, 120.0, 60.0)) -> dict:
    """Position auctions: k slots with click rates ``ctrs`` (decreasing), bidders with values per click ``values``
    (sorted, one more bidder than slots or more).  VCG charges the bidder in slot i the externality it imposes on those
    below: p_i = sum_{j >= i} (ctr_j - ctr_{j+1}) v_{j+1} in total.  The generalized second price auction charges each
    the next bid per click; its lowest locally envy-free equilibrium (Edelman, Ostrovsky and Schwarz 2007) has bids
    b_{i+1} ctr_i... giving the same totals as VCG.  Truthful bidding is not an equilibrium of GSP: the top bidder
    gains by dropping a slot when the next value is close.  Returns the payments, the equilibrium bids, and the gain
    the top bidder would make by deviating from truthful bidding."""
    v = np.asarray(values, float)
    c = np.append(np.asarray(ctrs, float), 0.0)
    k = len(ctrs)
    vcg = np.zeros(k)
    for i in range(k):
        vcg[i] = sum((c[j] - c[j + 1]) * v[j + 1] for j in range(i, k))
    # the lowest locally envy-free GSP equilibrium: the bid of the bidder in slot i+1 (i.e. the price per click of
    # slot i) equals vcg[i] / ctr_i
    price_per_click = vcg / c[:k]
    # GSP with truthful bids: slot i pays v_{i+1} per click
    truthful_pay = np.array([c[i] * v[i + 1] for i in range(k)])
    truthful_profit = np.array([c[i] * v[i] - truthful_pay[i] for i in range(k)])
    # the top bidder's best deviation under truthful bidding by the others: take slot j, paying v_{j+1} per click
    dev = [c[j] * (v[0] - v[j + 1]) for j in range(k)]
    return {"values": v.tolist(), "ctrs": list(map(float, ctrs)), "vcg_total": vcg.tolist(),
            "gsp_price_per_click": price_per_click.tolist(), "truthful_pay": truthful_pay.tolist(),
            "truthful_profit_top": float(truthful_profit[0]), "deviation_profits_top": [float(x) for x in dev],
            "best_slot_for_top_if_truthful": int(np.argmax(dev))}


def exposure(both: float = 10.0, alone: float = 1.0, rivals=(4.0, 4.0)) -> dict:
    """Two licences, A and B, sold in a simultaneous ascending auction.  A national bidder values the pair at ``both``
    and either licence alone at ``alone`` (complements: alone + alone < both); two local bidders value one licence each
    at ``rivals``.  The efficient outcome gives the pair to the national bidder if both > the rivals' sum.

    A cautious national bidder bids each licence only up to its stand-alone value: the locals win both, at about that
    price.  A bold one bids until the two prices together reach its pair value: prices rise together; the weaker local
    drops out at its value; the other price rises until the stronger local drops (the national bidder wins both) or the
    prices sum to the pair value first (it stops, holding the cheaper licence it cannot use, at a loss).  That risk is
    the exposure problem: caution wastes the pair's value, boldness risks a loss."""
    r_lo, r_hi = sorted(rivals)
    eff = "national" if both > r_lo + r_hi else "locals"
    cautious = {"national_wins": 0, "national_profit": 0.0, "welfare": float(r_lo + r_hi),
                "prices": (float(alone), float(alone))}
    if r_lo + r_hi <= both:
        bold = {"national_wins": 2, "national_profit": float(both - r_lo - r_hi), "welfare": float(both),
                "prices": (float(r_lo), float(r_hi))}
    else:
        bold = {"national_wins": 1, "national_profit": float(alone - r_lo), "welfare": float(alone + r_hi),
                "prices": (float(r_lo), float(both - r_lo))}
    return {"both": both, "alone": alone, "rivals": [float(r_lo), float(r_hi)], "efficient": eff,
            "efficient_welfare": float(max(both, r_lo + r_hi)), "cautious": cautious, "bold": bold}


def multi_unit(supply: int = 2, big=(10.0, 10.0), small: float = 6.0) -> dict:
    """Identical units (``supply`` of them) for a big bidder with values ``big`` for its first, second, ... unit and a
    small bidder who wants one unit worth ``small``.  Three rules: the uniform price (every winner pays the highest
    losing bid), pay-as-bid (each winning bid pays itself), and Vickrey's (each bidder pays, for the units it wins,
    the bids it displaces).

    Under the uniform price the big bidder's truthful demand sets its own price: bidding for one unit fewer removes
    the losing bid that sets the price.  That is demand reduction (Ausubel and Cramton): the big bidder gains, the
    seller loses, and the units go to the wrong hands.  Returns, for the big bidder bidding for k = 0..len(big) units
    (truthfully on those) while the small one bids its value: units won, price, profit, the seller's revenue and the
    surplus; and Vickrey's outcome for comparison."""
    big = [float(x) for x in big]
    rows = []
    for k in range(len(big) + 1):
        bids = [(b, "big") for b in big[:k]] + [(float(small), "small")]
        bids.sort(key=lambda t: -t[0])
        won, lost = bids[:supply], bids[supply:]
        price = lost[0][0] if lost else 0.0
        n_big = sum(1 for _, w in won if w == "big")
        small_wins = any(w == "small" for _, w in won)
        profit = sum(big[:n_big]) - n_big * price
        revenue = price * len(won)
        surplus = sum(big[:n_big]) + (small if small_wins else 0.0)
        rows.append({"k": k, "big_units": n_big, "small_wins": bool(small_wins), "price": float(price),
                     "big_profit": float(profit), "revenue": float(revenue), "surplus": float(surplus)})
    best = max(rows, key=lambda r: r["big_profit"])
    # Vickrey: truthful bids; the efficient allocation; each pays the others' loss
    all_bids = sorted([(b, "big") for b in big] + [(float(small), "small")], key=lambda t: -t[0])
    won = all_bids[:supply]
    n_big = sum(1 for _, w in won if w == "big")
    small_wins = any(w == "small" for _, w in won)
    others_without_big = small if supply >= 1 else 0.0
    others_with_big = small if small_wins else 0.0
    pay_big = others_without_big - others_with_big
    without_small = sum(sorted(big, reverse=True)[:supply])
    with_small = sum(big[:n_big])
    pay_small = (without_small - with_small) if small_wins else 0.0
    vickrey = {"big_units": n_big, "small_wins": bool(small_wins), "big_pays": float(pay_big),
               "small_pays": float(pay_small), "big_profit": float(sum(big[:n_big]) - pay_big),
               "revenue": float(pay_big + pay_small), "surplus": float(sum(big[:n_big]) + (small if small_wins else 0))}
    return {"rows": rows, "truthful": rows[-1], "best": best, "vickrey": vickrey, "supply": supply,
            "big": big, "small": float(small)}


def expected_profit(value: float = 70.0, rivals: int = 3, top: float = 100.0, bids=None) -> dict:
    """Play it: your value is ``value``; each of ``rivals`` rivals has a value uniform on [0, top] and plays the
    risk-neutral equilibrium.  First-price: rivals bid (n - 1)/n of their values, so a bid b wins with probability
    (b / (top (n - 1)/n))^rivals; your expected profit is (value - b) times that.  Second-price: rivals bid their
    values; a bid b wins when the highest rival value m < b, and you pay m: expected profit is the integral of
    (value - m) over m < b.  Returns both curves, the best bids (value (n - 1)/n and value) and the expected profits
    there."""
    n = rivals + 1
    bs = np.linspace(0, top, 401) if bids is None else np.asarray(bids, float)
    cap = top * (n - 1) / n
    p_first = np.clip(bs / cap, 0, 1) ** rivals
    first = (value - bs) * p_first
    # second price: m has density rivals m^(rivals-1)/top^rivals on [0, top]
    bb = np.minimum(bs, top)
    second = value * (bb / top) ** rivals - rivals / (rivals + 1) * bb ** (rivals + 1) / top ** rivals
    k1, k2 = int(np.argmax(first)), int(np.argmax(second))
    b1 = value * (n - 1) / n
    e1 = (value - b1) * (b1 / cap) ** rivals
    e2 = value * (value / top) ** rivals - rivals / (rivals + 1) * value ** (rivals + 1) / top ** rivals
    return {"bids": bs, "first": first, "second": second, "best_first": float(b1), "best_second": float(value),
            "grid_best_first": float(bs[k1]), "grid_best_second": float(bs[k2]), "profit_first": float(e1),
            "profit_second": float(e2), "p_win": float((value / top) ** rivals), "value": value, "n": n, "top": top}


def clock(values, step: float = 0.01) -> dict:
    """An English clock on one draw of values: the price rises by ``step``; each bidder stays in until the price
    reaches its value.  Returns the prices at which each bidder drops out, the winner, and the price paid (the
    second-highest value, to the step)."""
    v = np.asarray(values, float)
    order = np.argsort(v)
    drops = {int(i): round(float(np.ceil(v[i] / step - 1e-9) * step), 10) for i in order[:-1]}
    winner = int(order[-1])
    return {"values": v.tolist(), "drops": drops, "winner": winner, "price": float(max(drops.values())),
            "order": [int(i) for i in order]}

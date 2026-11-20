"""Agora's insurance (Part 42): what the state should insure, and how generously.

* **Pooling** (:func:`pooling`): the spread of the claim per member as a pool grows, when risks are independent
  and when a recession raises everyone's risk at once.
* **Unemployment insurance, the static model** (:class:`Baily`): an unemployed worker chooses search effort e (the
  chance of finding a job), paying a cost psi(e); benefits b are paid if the search fails, financed by a tax tau on
  the employed, so that (1 - e) b = e tau.  Welfare against b, the optimum, and both sides of the Baily (1978) and
  Chetty (2006) formula: (u'(c_u) - u'(c_e)) / u'(c_e) = eps_{1-e,b} / e, where eps is the elasticity of the chance
  of staying unemployed with respect to b.  Chetty's (2008) split of the response into a liquidity effect and moral
  hazard: de/db = de/dA - de/dw.
* **Unemployment insurance, week by week** (:func:`weekly`): a worker without savings searches each week, with
  benefits for K weeks and a floor after them; the hazard of finding a job rises as exhaustion nears; durations and
  their elasticities with respect to the level and length of benefits.
* **Health insurance** (:class:`Health`): illness of size theta; care m repairs the harm with diminishing returns; a
  patient who pays a share c of the cost chooses m = theta (1 - k c), so insurance raises spending (moral hazard)
  while it removes risk.  Welfare against c, the optimal coinsurance rate, the risk premium and the overuse that
  trade off, and RAND-style arc elasticities.
* **Lotteries and examiners** (:func:`lottery`, :func:`examiners`): Oregon's design (a lottery that offers coverage,
  a first stage, reduced forms and Wald estimates with their uncertainty) and the examiner design for disability
  insurance (leniency as an instrument, against a naive comparison).
* **Defaults** (:func:`defaults`): enrolment under opt-in and automatic enrolment when people act on their choice
  only occasionally.
* **The EITC, tagging and a basic income** (:func:`eitc`, :func:`tagging`, :func:`basic_income`).
* **Pensions** (:func:`payg`): pay-as-you-go arithmetic and the implicit debt.
* **One yardstick** (:func:`mvpf`): the marginal value of public funds, willingness to pay over net cost.

numpy and scipy only.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq, minimize_scalar


def crra(c, gamma: float):
    c = np.asarray(c, float)
    return np.log(c) if abs(gamma - 1.0) < 1e-12 else c ** (1 - gamma) / (1 - gamma)


def crra_prime(c, gamma: float):
    return np.asarray(c, float) ** (-gamma)


# ---------------------------------------------------------------------------------------------------------------
# pooling


def pooling(ns, p_low: float = 0.03, p_high: float = 0.09, q: float = 0.15) -> dict:
    """The standard deviation of the claim per member, relative to its mean, for pools of size n, when each member
    loses their job (a claim of one) with probability p.  Independent: p is the same every year.  Correlated: in a
    recession year (probability q) everyone's chance is p_high, otherwise p_low.  The law of large numbers removes
    the first kind of risk, not the second: the relative spread falls towards sqrt(q (1 - q)) |p_high - p_low| /
    pbar, however large the pool."""
    ns = np.asarray(ns, float)
    pbar = q * p_high + (1 - q) * p_low
    indep = np.sqrt(pbar * (1 - pbar) / ns) / pbar
    within = q * p_high * (1 - p_high) + (1 - q) * p_low * (1 - p_low)
    between = q * (1 - q) * (p_high - p_low) ** 2
    corr = np.sqrt(within / ns + between) / pbar
    return {"n": ns.tolist(), "independent": indep.tolist(), "correlated": corr.tolist(), "pbar": pbar,
            "floor": float(np.sqrt(between) / pbar)}


# ---------------------------------------------------------------------------------------------------------------
# unemployment insurance: the static model


@dataclass
class Baily:
    """The static model of unemployment insurance.  Consumption when employed is A + w - tau, when unemployed A + b
    (A: savings and other resources spent in the period); utility is CRRA with risk aversion gamma; search costs
    psi(e) = theta e^(1 + kappa) / (1 + kappa)."""
    gamma: float = 2.0
    w: float = 1.0
    A: float = 3.0
    theta: float = 0.05
    kappa: float = 8.0

    def effort(self, b: float, tau: float, A=None, w=None) -> float:
        """The worker's choice: u(c_e) - u(c_u) = psi'(e) = theta e^kappa."""
        A = self.A if A is None else A
        w = self.w if w is None else w
        gap = crra(A + w - tau, self.gamma) - crra(A + b, self.gamma)
        if gap <= 0:
            return 0.0
        return float(min((gap / self.theta) ** (1 / self.kappa), 0.999))

    def solve(self, b: float) -> dict:
        """The equilibrium with a balanced budget: e(b, tau) and tau = (1 - e) b / e."""
        tau = 0.0
        for _ in range(200):
            e = self.effort(b, tau)
            new = (1 - e) * b / max(e, 1e-6)
            if abs(new - tau) < 1e-13:
                break
            tau = 0.5 * tau + 0.5 * new
        e = self.effort(b, tau)
        ce, cu = self.A + self.w - tau, self.A + b
        welfare = e * crra(ce, self.gamma) + (1 - e) * crra(cu, self.gamma) - self.theta * e ** (1 + self.kappa) / (
            1 + self.kappa)
        return {"b": b, "tau": tau, "e": e, "ce": ce, "cu": cu, "welfare": float(welfare), "drop": 1 - cu / ce}

    def elasticity(self, b: float, h: float = 1e-4, total: bool = True) -> float:
        """eps_{1-e,b}: the elasticity of the chance of staying unemployed with respect to the benefit.  With
        ``total`` (the default, and what the formula needs) the tax that pays for the benefit adjusts too; otherwise
        the tax is held fixed, as for one worker in a large economy."""
        if total:
            lo, hi = 1 - self.solve(b * (1 - h))["e"], 1 - self.solve(b * (1 + h))["e"]
        else:
            tau = self.solve(b)["tau"]
            lo, hi = 1 - self.effort(b * (1 - h), tau), 1 - self.effort(b * (1 + h), tau)
        return float((np.log(hi) - np.log(lo)) / (np.log(1 + h) - np.log(1 - h)))

    def sides(self, b: float) -> dict:
        """Both sides of the Baily-Chetty formula at b: the gain from moving a dollar from the employed to the
        unemployed state, (u'(c_u) - u'(c_e)) / u'(c_e), and the cost, eps / e."""
        s = self.solve(b)
        gain = crra_prime(s["cu"], self.gamma) / crra_prime(s["ce"], self.gamma) - 1
        return {"gain": float(gain), "cost": self.elasticity(b) / s["e"], **s}

    def optimum(self, lo: float = 0.02, hi: float = 0.98) -> float:
        r = minimize_scalar(lambda b: -self.solve(b)["welfare"], bounds=(lo, hi), method="bounded",
                            options={"xatol": 1e-7})
        return float(r.x)

    def split(self, b: float, h: float = 1e-5) -> dict:
        """Chetty's (2008) decomposition of de/db at b: the liquidity effect de/dA (cash in both states) and the
        moral hazard effect -de/dw (a subsidy to staying unemployed); the liquidity share, and the formula
        (u'(c_u) - u'(c_e))/u'(c_u) that it equals in this model."""
        s = self.solve(b)
        tau = s["tau"]
        dA = (self.effort(b, tau, A=self.A + h) - self.effort(b, tau, A=self.A - h)) / (2 * h)
        dw = (self.effort(b, tau, w=self.w + h) - self.effort(b, tau, w=self.w - h)) / (2 * h)
        db = (self.effort(b + h, tau) - self.effort(b - h, tau)) / (2 * h)
        up_u, up_e = crra_prime(s["cu"], self.gamma), crra_prime(s["ce"], self.gamma)
        return {"de_db": db, "liquidity": dA, "moral_hazard": -dw, "share": dA / db,
                "share_formula": float((up_u - up_e) / up_u), "b": b}


# ---------------------------------------------------------------------------------------------------------------
# unemployment insurance: week by week


def weekly(b: float = 0.5, K: int = 26, floor: float = 0.2, gamma: float = 2.0, beta: float = 0.999,
           theta: float = 600.0, kappa: float = 1.0, w: float = 1.0, horizon: int = 104) -> dict:
    """A worker without savings, unemployed, searches each week with intensity s (the chance of a job next week) at a
    utility cost theta s^(1 + kappa) / (1 + kappa).  Benefits b are paid for K weeks, then the floor.  A job lasts
    for ever.  Solved backwards in the weeks of benefit left: the hazard s by week of unemployment, the survival
    curve, and the expected duration (weeks, truncated at ``horizon`` and adding the expected tail)."""
    u = lambda c: float(crra(c, gamma))  # noqa: E731
    VE = u(w) / (1 - beta)

    def best(cont):
        # max over s of -theta s^(1+k)/(1+k) + beta (s VE + (1 - s) cont): theta s^k = beta (VE - cont)
        gain = beta * (VE - cont)
        s = min((max(gain, 0.0) / theta) ** (1 / kappa), 0.99)
        return s, -theta * s ** (1 + kappa) / (1 + kappa) + beta * (s * VE + (1 - s) * cont)

    # after exhaustion: a fixed point U0 = u(floor) + max_s [...]
    U0 = u(floor) / (1 - beta)
    for _ in range(20000):
        s0, val = best(U0)
        new = u(floor) + val
        if abs(new - U0) < 1e-10:
            break
        U0 = new
    U = [U0]
    S = [s0]
    for k in range(1, K + 1):          # k weeks of benefits left
        s, val = best(U[-1])
        U.append(u(b) + val)
        S.append(s)
    # week t of unemployment (t = 0, 1, ...) has K - t weeks left
    haz = np.array([S[max(K - t, 0)] for t in range(horizon)])
    surv = np.concatenate([[1.0], np.cumprod(1 - haz)])
    dur = float(np.sum(surv[:-1]) + surv[-1] / max(S[0], 1e-9))
    return {"hazard": haz.tolist(), "survival": surv.tolist(), "duration": dur, "b": b, "K": K, "floor": floor,
            "exhaust": float(surv[K])}


def weekly_elasticities(b: float = 0.5, K: int = 26, h: float = 0.05, **kw) -> dict:
    """The elasticity of the expected duration with respect to the benefit level and to the number of weeks."""
    d0 = weekly(b, K, **kw)["duration"]
    db = (np.log(weekly(b * (1 + h), K, **kw)["duration"]) - np.log(weekly(b * (1 - h), K, **kw)["duration"])) / (
        np.log(1 + h) - np.log(1 - h))
    dk = (np.log(weekly(b, K + 4, **kw)["duration"]) - np.log(weekly(b, K - 4, **kw)["duration"])) / (
        np.log(K + 4) - np.log(K - 4))
    return {"duration": d0, "level": float(db), "length": float(dk)}


# ---------------------------------------------------------------------------------------------------------------
# health insurance


@dataclass
class Health:
    """Illness of money-equivalent size theta (lognormal, truncated at ``cap``; zero for the healthy).  Care m, as a
    share x = m / theta of the full course, repairs (theta / k)(x - x^2 / 2) of the harm, which is theta / (2k) if
    untreated; a patient paying a share c of the cost chooses x = 1 - k c.  So at full price the course is 1 - k,
    with free care all of it: k is set so that free care costs 1 / (1 - 0.95 k) times as much as a 95% coinsurance
    plan.  The premium is the insurer's expected cost, (1 - c) E[m].  Utility is CRRA in income less premium,
    out-of-pocket cost and unrepaired harm."""
    gamma: float = 3.0
    income: float = 1.0
    p_sick: float = 0.7
    median: float = 0.03
    sigma: float = 1.3
    cap: float = 0.6
    k: float = 0.316
    n: int = 4000

    def thetas(self):
        from scipy.stats import norm
        q = (np.arange(self.n) + 0.5) / self.n
        th = np.exp(np.log(self.median) + self.sigma * norm.ppf(q))
        return np.minimum(th, self.cap)

    def plan(self, c: float) -> dict:
        th = self.thetas()
        x = np.clip(1 - self.k * c, 0, 1)
        m = th * x
        harm = th / (2 * self.k) * (1 - x) ** 2
        Em = self.p_sick * m.mean()
        prem = (1 - c) * Em
        cons_sick = self.income - prem - c * m - harm
        cons_well = self.income - prem
        Eu = self.p_sick * crra(cons_sick, self.gamma).mean() + (1 - self.p_sick) * float(crra(cons_well,
                                                                                             self.gamma))
        Ec = self.p_sick * cons_sick.mean() + (1 - self.p_sick) * cons_well
        g = self.gamma
        ce = float((Eu * (1 - g)) ** (1 / (1 - g))) if abs(g - 1) > 1e-12 else float(np.exp(Eu))
        # overuse: spending beyond what the care is worth at its cost, against the full-price choice x = 1 - k
        x1 = np.clip(1 - self.k, 0, 1)
        rep = lambda xx: th / self.k * (xx - xx ** 2 / 2)  # noqa: E731
        over = self.p_sick * np.mean(th * (x - x1) - (rep(x) - rep(x1)))
        return {"c": c, "spending": float(Em), "premium": float(prem), "ce": ce, "mean_c": float(Ec),
                "risk_premium": float(Ec - ce), "overuse": float(over)}

    def optimum(self) -> float:
        r = minimize_scalar(lambda c: -self.plan(c)["ce"], bounds=(0.0, 1.0), method="bounded",
                            options={"xatol": 1e-6})
        return float(r.x)


def arc_elasticity(q1: float, q2: float, p1: float, p2: float) -> float:
    """The arc elasticity used by the RAND experiment: the change in quantity over the mean quantity, divided by the
    change in price over the mean price."""
    return float(((q2 - q1) / (q2 + q1)) / ((p2 - p1) / (p2 + p1)))


# ---------------------------------------------------------------------------------------------------------------
# lotteries and examiners


def lottery(n: int = 75000, drawn: float = 0.4, take_up: float = 0.3, other: float = 0.14,
            effects=None, base=None, sds=None, sub=None, seed: int = 0) -> dict:
    """An Oregon-style lottery: n people on the list, a share ``drawn`` selected; selection raises coverage by about
    take_up - (other coverage lost); everyone may also be covered from other sources with probability ``other``.
    Each outcome y = base + effect * covered + noise; ``sub`` gives the number surveyed for each outcome.  Returns
    the first stage and, for each outcome, the reduced form, the Wald (IV) estimate and its standard error."""
    effects = effects or {"ed_visits": 0.41, "depression": -0.09, "catastrophic": -0.045, "systolic": -1.0}
    base = base or {"ed_visits": 1.02, "depression": 0.30, "catastrophic": 0.055, "systolic": 119.0}
    sds = sds or {"ed_visits": 2.4, "depression": None, "catastrophic": None, "systolic": 16.0}
    sub = sub or {"ed_visits": 25000, "depression": 12000, "catastrophic": 12000, "systolic": 12000}
    rng = np.random.default_rng(seed)
    z = rng.random(n) < drawn
    covered = np.where(z, rng.random(n) < take_up + (1 - take_up) * other, rng.random(n) < other)
    fs = covered[z].mean() - covered[~z].mean()
    out = {"n": n, "drawn": int(z.sum()), "first_stage": float(fs), "cover_won": float(covered[z].mean()),
           "cover_lost": float(covered[~z].mean()), "outcomes": {}}
    for k, eff in effects.items():
        m = sub[k]
        idx = rng.choice(n, m, replace=False)
        zz, dd = z[idx], covered[idx]
        if sds[k] is None:               # a binary outcome
            p = np.clip(base[k] + eff * dd, 0, 1)
            y = (rng.random(m) < p).astype(float)
        else:
            y = base[k] + eff * dd + sds[k] * rng.standard_normal(m)
        rf = y[zz].mean() - y[~zz].mean()
        se_rf = np.sqrt(y[zz].var(ddof=1) / zz.sum() + y[~zz].var(ddof=1) / (~zz).sum())
        fs_k = dd[zz].mean() - dd[~zz].mean()
        wald = rf / fs_k
        # the Wald estimator's standard error from the residuals of the IV fit
        resid = y - y.mean() - wald * (dd - dd.mean())
        se_iv = np.sqrt(resid[zz].var(ddof=1) / zz.sum() + resid[~zz].var(ddof=1) / (~zz).sum()) / abs(fs_k)
        out["outcomes"][k] = {"true": eff, "base": base[k], "rf": float(rf), "se_rf": float(se_rf),
                              "fs": float(fs_k), "wald": float(wald), "se": float(se_iv), "m": m,
                              "naive": float(y[dd].mean() - y[~dd].mean())}
    return out


def examiners(n: int = 60000, j: int = 200, spread: float = 0.12, seed: int = 0) -> dict:
    """Disability applicants with severity s (uniform; higher is sicker), each assigned at random to one of j
    examiners whose leniency shifts the bar for allowance.  Without benefits an applicant works with probability
    0.9 (1 - s)^1.5; with benefits not at all.  So the effect of allowance on work is -0.9 (1 - s)^1.5: large for the
    least severe, nothing for the most.  Compares the naive gap between allowed and denied applicants with the
    examiner instrument (two-stage least squares on each examiner's leave-one-out allowance rate) and, by bins of
    leniency, the local effects."""
    rng = np.random.default_rng(seed)
    exam = rng.integers(0, j, n)
    len_ = spread * rng.standard_normal(j)
    s = rng.random(n)
    bar = 0.5 - len_[exam]
    allowed = (s + 0.08 * rng.standard_normal(n)) > bar
    p_work = 0.9 * (1 - s) ** 1.5
    works = np.where(allowed, False, rng.random(n) < p_work)
    y, d = works.astype(float), allowed.astype(float)
    cnt = np.bincount(exam, minlength=j).astype(float)
    tot = np.bincount(exam, weights=d, minlength=j)
    z = (tot[exam] - d) / (cnt[exam] - 1)          # leave-one-out leniency
    zc, dc, yc = z - z.mean(), d - d.mean(), y - y.mean()
    iv = float((zc @ yc) / (zc @ dc))
    fs = float((zc @ dc) / (zc @ zc))
    resid = yc - iv * dc
    se = float(np.sqrt(np.sum((zc * resid) ** 2)) / abs(zc @ dc))
    naive = float(y[allowed].mean() - y[~allowed].mean())
    # who is moved by leniency: applicants near the bar, severity around 0.5
    marg = np.abs(s - 0.5) < 0.12
    true_late = float(-np.mean(p_work[marg]))
    sev = np.linspace(0, 1, 11)
    effect_by_sev = (-0.9 * (1 - sev) ** 1.5).tolist()
    return {"iv": iv, "se": se, "first_stage": fs, "naive": naive, "true_marginal": true_late,
            "allow_rate": float(d.mean()), "leniency_sd": float(np.std(tot / cnt)),
            "severity": sev.tolist(), "effect_by_severity": effect_by_sev,
            "rates": (tot / cnt).tolist()}


# ---------------------------------------------------------------------------------------------------------------
# defaults


def defaults(n: int = 20000, months: int = 48, attention: float = 0.045, want: float = 0.75, default: float = 0.03,
             seed: int = 0) -> dict:
    """Employees act on their savings choice only when they pay attention (each month with probability
    ``attention``); until then they keep the status quo: not enrolled under opt-in, enrolled at the default rate
    under automatic enrolment.  When they act, a share ``want`` enrol at their own preferred rate (spread around 6%,
    with some choosing the default's 3%).  Participation and the share at the default, month by month."""
    rng = np.random.default_rng(seed)
    first = rng.geometric(attention, n)               # the month each employee first acts
    joins = rng.random(n) < want
    rate = np.where(rng.random(n) < 0.15, default, np.clip(rng.normal(0.06, 0.025, n), 0.01, 0.15))
    t = np.arange(months + 1)
    acted = first[None, :] <= t[:, None]
    part_opt = (acted & joins[None, :]).mean(axis=1)
    part_auto = (~acted | joins[None, :]).mean(axis=1)
    at_def_auto = (~acted | (joins & (rate == default))[None, :]).mean(axis=1)
    return {"t": t.tolist(), "opt_in": part_opt.tolist(), "auto": part_auto.tolist(), "at_default": at_def_auto.tolist(),
            "attention": attention, "want": want}


# ---------------------------------------------------------------------------------------------------------------
# the EITC, tagging and a basic income


def eitc(earnings, rate_in: float, top: float, start_out: float, rate_out: float) -> np.ndarray:
    """The credit at each level of earnings: rate_in of earnings up to ``top`` (the plateau's start), the maximum
    until ``start_out``, then withdrawn at rate_out."""
    z = np.asarray(earnings, float)
    mx = rate_in * top
    return np.clip(np.minimum(rate_in * z, mx) - rate_out * np.maximum(z - start_out, 0), 0, None)


def tagging(needy: float = 0.2, catch: float = 0.7, false_tag: float = 0.1) -> dict:
    """Akerlof's tag: a transfer to everyone against one to those with an observable tag (caught for a share
    ``catch`` of the needy and ``false_tag`` of the rest).  Per dollar spent, the share reaching the needy; the share
    of the needy missed."""
    tagged = needy * catch + (1 - needy) * false_tag
    return {"universal": needy, "tagged": needy * catch / tagged, "missed": 1 - catch, "tagged_size": tagged,
            "cost_ratio": tagged}


def basic_income(incomes, t: float, e: float = 0.0) -> dict:
    """A flat tax t on incomes that shrink like (1 - t)^e, paid back as an equal basic income: the basic income, the
    break-even income (B / t), the share of net recipients, and the Gini before and after."""
    from explainer.economics.agora.distribution import gini

    x = np.asarray(incomes, float)
    y = x * (1 - t) ** e
    B = t * y.mean()
    net = B - t * y
    after = y * (1 - t) + B
    return {"t": t, "B": float(B), "break_even": float(B / t) if t > 0 else float("inf"),
            "recipients": float(np.mean(net > 0)), "gini_before": float(gini(x)), "gini_after": float(gini(after)),
            "mean_before": float(x.mean()), "mean_after": float(y.mean())}


# ---------------------------------------------------------------------------------------------------------------
# pensions


def payg(tau: float = 0.124, workers_per_retiree: float = 2.7, n: float = 0.005, g: float = 0.01, r: float = 0.03,
         years: int = 30) -> dict:
    """Pay-as-you-go arithmetic.  The benefit, as a share of the average wage, is the contribution rate times the
    workers per retiree.  Over a working life of ``years`` the system returns the growth of the wage bill, n + g,
    against r for a funded account: the share of each contribution lost, and the same loss computed as the interest
    on the implicit debt that the first retirees' windfall created."""
    grow = (1 + n) * (1 + g)
    replacement = tau * workers_per_retiree
    paygo = grow ** years
    funded = (1 + r) ** years
    loss_share = 1 - paygo / funded
    # the implicit debt is one generation's benefits; rolling it over at r costs (R - G) per unit each generation,
    # which, per unit of contributions, is the same share
    interest = (funded - paygo) / funded
    return {"replacement": replacement, "paygo_return": paygo, "funded_return": funded, "loss_share": loss_share,
            "interest_on_debt": interest, "loss_of_wages": tau * loss_share, "annual_paygo": grow - 1,
            "annual_funded": r}


# ---------------------------------------------------------------------------------------------------------------
# one yardstick


def mvpf(wtp: float, cost: float, fiscal_externality: float = 0.0) -> float:
    """The marginal value of public funds: beneficiaries' willingness to pay over the net cost to the government
    (the cost plus the fiscal externality, which is negative when the policy raises other revenue).  Infinite when the
    policy pays for itself."""
    net = cost + fiscal_externality
    return float("inf") if net <= 0 else wtp / net


def eitc_mvpf(n: int = 40000, scale: float = 0.1, welfare: float = 8000.0, cost: float = 16000.0,
              tax: float = 0.0765, seed: int = 0, params=(0.45, 17880.0, 23350.0, 0.2106)) -> dict:
    """The MVPF of a 10% larger EITC for single parents who decide whether to work.  Potential earnings are lognormal
    around $24,000; working costs F (exponential with mean ``cost``, the time and childcare a job takes); a parent
    works if earnings less payroll tax plus the credit, less F, beat the welfare benefit.  Scaling the credit up pays
    the mechanical cost to those already working (what they would pay for it: willingness to pay), and draws in new
    workers, who pay payroll tax, stop drawing the benefit, and claim the credit.  Returns participation before and
    after, the mechanical cost, the fiscal externality and the MVPF."""
    rng = np.random.default_rng(seed)
    w = np.exp(rng.normal(np.log(24000.0), 0.45, n))
    F = rng.exponential(cost, n)
    r, top, start, rout = params

    def take(sc):
        cr = sc * eitc(w, r, top, start, rout)
        work = w * (1 - tax) + cr - F > welfare
        return work, cr
    w0, c0 = take(1.0)
    w1, c1 = take(1.0 + scale)
    mech = float(np.sum((c1 - c0)[w0]))
    new = w1 & ~w0
    fe = float(np.sum(c1[new] - tax * w[new] - welfare))   # the credit paid, less the tax and benefit saved
    return {"work0": float(w0.mean()), "work1": float(w1.mean()), "mechanical": mech, "fiscal_externality": fe,
            "mvpf": mvpf(mech, mech, fe), "per_dollar_fe": fe / mech}


def ui_mvpf(model: Baily, b: float) -> float:
    """The MVPF of a small rise in unemployment benefits in the static model: (1 + the consumption-smoothing gain)
    over (1 + the behavioural cost)."""
    s = model.sides(b)
    return (1 + s["gain"]) / (1 + s["cost"])


def zero_crossing(f, lo: float, hi: float) -> float:
    return float(brentq(f, lo, hi))

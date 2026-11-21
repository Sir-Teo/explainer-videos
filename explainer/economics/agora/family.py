"""Agora's economic approach (Part 49): crime as a choice, the household as a small factory, marriage as a matching
market, children's quantity and quality, bargaining inside the household, schools and teachers, the demand for
health and addiction.

* **Crime** (:func:`offend_share`, :func:`elasticities`, :func:`play_doubling`, :func:`optimal_enforcement`): Becker's
  potential offenders, each with a gain from an offence, weigh it against a punishment that comes with probability p;
  their attitude to risk, and how much a long sentence's later years count, decide whether doubling the chance or
  doubling the punishment deters more; the authority's cheapest way to deter when catching is costly and fines are
  not.
* **Police and crime measured** (:func:`police_blocks`): blocks where police go where crime is; the naive regression,
  the same with police counted with error, and a random redeployment, against a planted elasticity.
* **The household** (:func:`household_time`): two adults split their time between the market and home production by
  comparative advantage; what a rise in one wage or in home technology does.
* **Marriage** (:func:`choo_siow`, :func:`choo_siow_estimate`): a transferable-utility marriage market with types and
  logit taste shocks; equilibrium matches by iterative proportional fitting; the surplus read back from counts.
* **Children** (:func:`quantity_quality`, :func:`wald`): Becker and Lewis's household chooses how many children and how
  much to spend on each; the Wald estimator for a binary instrument.
* **Bargaining** (:func:`collective`): a household that maximizes a weighted sum of two adults' utilities, the
  weight rising with the share of income each controls; spending on a child good under a unitary and a collective
  household when a benefit is paid to the father or the mother.
* **Schools** (:func:`maimonides`, :func:`teacher_va`): class size under a cap of forty; teachers' value added
  estimated from noisy classes, shrunk, and tested with teacher moves.
* **Health** (:func:`grossman`): the demand for health as a capital stock that depreciates faster with age.
* **Addiction** (:func:`addiction_path`): Becker and Murphy's rational addict and a myopic one facing an announced
  price rise.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------------------------------------------
# crime as a choice
# ---------------------------------------------------------------------------------------------------------------

def _cara(x, a):
    """Constant absolute risk aversion utility: a > 0 averse, a < 0 loving, a = 0 neutral."""
    x = np.asarray(x, float)
    if abs(a) < 1e-12:
        return x
    return (1.0 - np.exp(-a * x)) / a


def felt_punishment(sentence, beta: float = 1.0):
    """How much a sentence of ``sentence`` years is felt today when each later year counts ``beta`` times the one
    before: sum_{t<S} beta^t (a fractional last year counts in proportion).  With beta = 1 it is the sentence."""
    s = np.asarray(sentence, float)
    if abs(beta - 1.0) < 1e-12:
        return s
    return (1.0 - beta ** s) / (1.0 - beta)


def offend_share(p, sentence, gains, a: float = 0.0, beta: float = 1.0) -> float:
    """Share of potential offenders who offend.  Each has a gain g (in the same units as a year of punishment);
    with probability p they are caught and suffer the felt punishment; they offend when the expected utility of
    offending, (1 - p) u(g) + p u(g - F), exceeds u(0) = 0, with u CARA with coefficient ``a``."""
    g = np.asarray(gains, float)
    F = float(felt_punishment(sentence, beta))
    eu = (1.0 - p) * _cara(g, a) + p * _cara(g - F, a)
    return float(np.mean(eu > 0.0))


def elasticities(p, sentence, gains, a: float = 0.0, beta: float = 1.0, h: float = 0.02) -> dict:
    """Elasticities of the offence rate with respect to the probability and to the sentence, by central differences
    on the log scale."""
    def o(pp, ss):
        return offend_share(pp, ss, gains, a, beta)
    ep = (np.log(o(p * np.exp(h), sentence)) - np.log(o(p * np.exp(-h), sentence))) / (2 * h)
    es = (np.log(o(p, sentence * np.exp(h))) - np.log(o(p, sentence * np.exp(-h)))) / (2 * h)
    return {"e_p": float(ep), "e_s": float(es), "rate": o(p, sentence)}


def play_doubling(p, sentence, gains, kinds: dict) -> dict:
    """The Play-it question: starting from (p, sentence), does doubling the chance of being caught or doubling the
    sentence cut offences more?  ``kinds`` maps a name to (a, beta).  Returns, for each kind, the offence rate at the
    start, with the chance doubled and with the sentence doubled."""
    out = {}
    for name, (a, beta) in kinds.items():
        out[name] = {"start": offend_share(p, sentence, gains, a, beta),
                     "double_p": offend_share(min(2 * p, 1.0), sentence, gains, a, beta),
                     "double_s": offend_share(p, 2 * sentence, gains, a, beta)}
    return out


def optimal_enforcement(gains, harm: float, cost_p: float, f_max: float, cost_f: float = 0.0,
                        n_p: int = 121, n_f: int = 121) -> dict:
    """Becker's planner chooses the probability of catching p (costing ``cost_p`` * p per potential offender) and
    a fine f up to ``f_max`` (costing ``cost_f`` * f for each offender punished: zero for a fine, positive for
    prison) to minimize harm from offences plus the cost of enforcement.  Risk-neutral offenders offend when
    g > p f.  Returns the loss surface and the minimum."""
    g = np.sort(np.asarray(gains, float))
    ps = np.linspace(0.005, 1.0, n_p)
    fs = np.linspace(0.0, f_max, n_f)
    L = np.empty((n_p, n_f))
    O = np.empty((n_p, n_f))
    for i, p in enumerate(ps):
        for j, f in enumerate(fs):
            o = 1.0 - np.searchsorted(g, p * f, side="right") / len(g)
            O[i, j] = o
            L[i, j] = harm * o + cost_p * p + cost_f * f * p * o
    i, j = np.unravel_index(np.argmin(L), L.shape)
    return {"p": ps.tolist(), "f": fs.tolist(), "loss": L.tolist(), "offences": O.tolist(), "p_star": float(ps[i]),
            "f_star": float(fs[j]), "loss_star": float(L[i, j]), "offences_star": float(O[i, j])}


def police_blocks(n_blocks: int = 1000, n_periods: int = 2, elasticity: float = -0.3, response: float = 0.8,
                  noise_police: float = 0.35, seed: int = 0) -> dict:
    """Blocks with a propensity to crime; the city sends more police where crime is expected (``response``: the
    elasticity of police to expected crime); crime falls with police at the planted ``elasticity``.  Returns the
    cross-section regression of log crime on log police (biased up by the allocation), the first-difference
    regression with police counted with noise (biased toward zero), and a random redeployment (unbiased)."""
    rng = np.random.default_rng(seed)
    base = rng.normal(0.0, 0.6, n_blocks)                       # log propensity, known to the police
    shock = rng.normal(0.0, 0.25, (n_periods, n_blocks))        # surprises
    lp = 1.0 + response * base[None, :] + rng.normal(0.0, 0.2, (n_periods, n_blocks))
    lc = 2.0 + base[None, :] + elasticity * lp + shock

    def slope(x, y):
        x, y = np.ravel(x), np.ravel(y)
        X = np.column_stack([np.ones_like(x), x])
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        r = y - X @ b
        V = np.linalg.inv(X.T @ X) * (r @ r) / (len(y) - 2)
        return float(b[1]), float(np.sqrt(V[1, 1]))

    naive, naive_se = slope(lp[0], lc[0])
    measured = lp + rng.normal(0.0, noise_police, lp.shape)
    fd, fd_se = slope(measured[1] - measured[0], lc[1] - lc[0])
    true_fd, _ = slope(lp[1] - lp[0], lc[1] - lc[0])
    # a random redeployment: half the blocks get 40% more police
    treat = rng.random(n_blocks) < 0.5
    lp_r = lp[0] + np.log(1.4) * treat
    lc_r = 2.0 + base + elasticity * lp_r + rng.normal(0.0, 0.25, n_blocks)
    effect = float(lc_r[treat].mean() - lc_r[~treat].mean())
    se = float(np.sqrt(lc_r[treat].var(ddof=1) / treat.sum() + lc_r[~treat].var(ddof=1) / (~treat).sum()))
    reliability = float(np.var(lp[1] - lp[0]) / np.var(measured[1] - measured[0]))
    return {"elasticity": elasticity, "naive": naive, "naive_se": naive_se, "fd_noisy": fd, "fd_noisy_se": fd_se,
            "fd_true": true_fd, "reliability": reliability, "experiment": effect / np.log(1.4),
            "experiment_se": se / np.log(1.4), "log_police": lp[0].tolist(), "log_crime": lc[0].tolist(),
            "treat": treat.tolist(), "log_crime_exp": lc_r.tolist()}


# ---------------------------------------------------------------------------------------------------------------
# the household as a small factory
# ---------------------------------------------------------------------------------------------------------------

def household_time(w1: float, w2: float, h1: float, h2: float, alpha: float = 0.4, T: float = 1.0,
                   n: int = 201) -> dict:
    """Two adults with market wages w1, w2 and home productivities h1, h2 split time T each between the market and
    home.  Goods C = w1 (T - t1) + w2 (T - t2); home output Z = h1 t1 + h2 t2; the household maximizes
    (1 - alpha) log C + alpha log Z.  Comparative advantage decides who does what: the optimum puts home time first
    on the adult with the higher h / w.  Returns home times, market hours and the shadow price of home output."""
    grid = np.linspace(0.0, T, n)
    t1, t2 = np.meshgrid(grid, grid, indexing="ij")
    C = w1 * (T - t1) + w2 * (T - t2)
    Z = h1 * t1 + h2 * t2
    with np.errstate(divide="ignore", invalid="ignore"):
        U = np.where((C > 0) & (Z > 0), (1 - alpha) * np.log(np.maximum(C, 1e-300)) +
                     alpha * np.log(np.maximum(Z, 1e-300)), -np.inf)
    i, j = np.unravel_index(np.argmax(U), U.shape)
    a1, a2 = grid[i], grid[j]
    return {"t1": float(a1), "t2": float(a2), "market1": float(T - a1), "market2": float(T - a2),
            "C": float(C[i, j]), "Z": float(Z[i, j]), "utility": float(U[i, j])}


# ---------------------------------------------------------------------------------------------------------------
# marriage as a matching market
# ---------------------------------------------------------------------------------------------------------------

def choo_siow(men, women, phi, tol: float = 1e-12, max_iter: int = 20000) -> dict:
    """Choo and Siow's marriage market.  ``men[i]`` and ``women[j]`` are the numbers of each type; ``phi[i, j]`` the
    joint surplus of an (i, j) marriage relative to both staying single.  With extreme-value tastes, equilibrium
    satisfies mu_ij = sqrt(mu_i0 mu_0j) exp(phi_ij / 2) and the adding-up constraints, solved here by iterating on
    the single counts."""
    m, f, P = np.asarray(men, float), np.asarray(women, float), np.exp(np.asarray(phi, float) / 2.0)
    x, y = np.sqrt(m), np.sqrt(f)                           # sqrt of singles
    for _ in range(max_iter):
        # solve x_i^2 + x_i * sum_j P_ij y_j = m_i for x_i (positive root), then y given x
        b = P @ y
        x_new = (-b + np.sqrt(b ** 2 + 4 * m)) / 2
        c = P.T @ x_new
        y_new = (-c + np.sqrt(c ** 2 + 4 * f)) / 2
        if np.max(np.abs(x_new - x)) + np.max(np.abs(y_new - y)) < tol:
            x, y = x_new, y_new
            break
        x, y = x_new, y_new
    mu = np.outer(x, y) * P
    return {"mu": mu.tolist(), "single_men": (x ** 2).tolist(), "single_women": (y ** 2).tolist(),
            "married_share_men": float(mu.sum() / m.sum()), "married_share_women": float(mu.sum() / f.sum())}


def choo_siow_estimate(mu, single_men, single_women) -> np.ndarray:
    """Read the surplus back from counts: phi_ij = 2 log(mu_ij / sqrt(mu_i0 mu_0j))."""
    mu = np.asarray(mu, float)
    return 2.0 * np.log(mu / np.sqrt(np.outer(single_men, single_women)))


def draw_market(men, women, phi, seed: int = 0) -> dict:
    """A finite market: equilibrium counts drawn as a multinomial sample of the equilibrium, then the surplus
    estimated from the sample (sampling error only)."""
    eq = choo_siow(men, women, phi)
    rng = np.random.default_rng(seed)
    mu = np.asarray(eq["mu"])
    cells = np.concatenate([mu.ravel(), eq["single_men"], eq["single_women"]])
    n = int(round(cells.sum()))
    draw = rng.multinomial(n, cells / cells.sum()).astype(float)
    I, J = mu.shape
    mu_s = draw[: I * J].reshape(I, J)
    sm, sw = draw[I * J: I * J + I], draw[I * J + I:]
    est = choo_siow_estimate(np.maximum(mu_s, 0.5), np.maximum(sm, 0.5), np.maximum(sw, 0.5))
    return {"mu": mu_s.tolist(), "single_men": sm.tolist(), "single_women": sw.tolist(), "phi_hat": est.tolist()}


def sorting_index(mu) -> float:
    """The share of couples on the diagonal (same type) divided by the share expected if couples formed at random
    given the margins."""
    mu = np.asarray(mu, float)
    p = mu / mu.sum()
    rand = np.outer(p.sum(1), p.sum(0))
    return float(np.trace(p) / np.trace(rand))


# ---------------------------------------------------------------------------------------------------------------
# children: quantity and quality
# ---------------------------------------------------------------------------------------------------------------

def quantity_quality(income: float, wage_mother: float, time_per_child: float = 0.15, goods_per_child: float = 0.05,
                     a: float = 0.3, b: float = 0.15) -> dict:
    """Becker and Lewis: utility log c + a log n + b log q; each child takes time (valued at the mother's wage) and
    goods, plus q per unit of quality: c + n (pi_n + q) = income + wage_mother, with pi_n = goods_per_child +
    time_per_child * wage_mother.  The quality price n and the quantity price (pi_n + q) interact.  Solved
    exactly: with full income Y, c = Y / (1 + a), n q = b Y / (1 + a) and n pi_n = (a - b) Y / (1 + a) when a > b,
    so quality q = b pi_n / (a - b) rises with the price of a child and the number falls."""
    Y = income + wage_mother
    pi = goods_per_child + time_per_child * wage_mother
    if a <= b:
        raise ValueError("needs a > b for an interior number of children")
    s = 1 + a
    n = (a - b) * Y / (s * pi)
    q = b * Y / (s * n)
    c = Y / s
    return {"n": float(n), "q": float(q), "c": float(c), "price_child": float(pi), "full_income": float(Y)}


def wald(z, d, y) -> dict:
    """The Wald estimator for a binary instrument z, a binary treatment d and an outcome y: (E[y|z=1] - E[y|z=0]) /
    (E[d|z=1] - E[d|z=0]), with a delta-method standard error, the first stage and the reduced form."""
    z, d, y = (np.asarray(v, float) for v in (z, d, y))
    one, zero = z == 1, z == 0
    fs = d[one].mean() - d[zero].mean()
    rf = y[one].mean() - y[zero].mean()
    beta = rf / fs
    e = y - beta * d                                           # residual in the IV sense
    se = np.sqrt(e[one].var(ddof=1) / one.sum() + e[zero].var(ddof=1) / zero.sum()) / abs(fs)
    fs_se = np.sqrt(d[one].var(ddof=1) / one.sum() + d[zero].var(ddof=1) / zero.sum())
    return {"first_stage": float(fs), "first_stage_se": float(fs_se), "reduced_form": float(rf), "wald": float(beta),
            "se": float(se), "n": int(len(y))}


# ---------------------------------------------------------------------------------------------------------------
# bargaining inside the household
# ---------------------------------------------------------------------------------------------------------------

def collective(y_father: float, y_mother: float, child_taste: tuple = (0.15, 0.40), weight_slope: float = 1.5,
               unitary: bool = False) -> dict:
    """Two adults share a budget between a private good for each and a child good everyone values; adult k's utility
    is (1 - c_k) log x_k + c_k log K, with c = ``child_taste`` (father, mother).  The household maximizes
    lambda u_mother + (1 - lambda) u_father.  In the unitary household lambda is fixed at one half; in the
    collective household lambda rises with the mother's share of income, lambda = Phi(slope (s - 1/2)) over (0, 1)
    with Phi the logistic.  Returns spending on the child good and lambda."""
    Y = y_father + y_mother
    lam = 0.5 if unitary else 1.0 / (1.0 + np.exp(-weight_slope * 4 * (y_mother / Y - 0.5)))
    cf, cm = child_taste
    # first-order conditions: x_f = (1-lam)(1-cf)/mu, x_m = lam (1-cm)/mu, K = (lam cm + (1-lam) cf)/mu
    wf, wm, wk = (1 - lam) * (1 - cf), lam * (1 - cm), lam * cm + (1 - lam) * cf
    tot = wf + wm + wk
    return {"lambda": float(lam), "child": float(Y * wk / tot), "father": float(Y * wf / tot),
            "mother": float(Y * wm / tot)}


# ---------------------------------------------------------------------------------------------------------------
# schools
# ---------------------------------------------------------------------------------------------------------------

def maimonides(enrolment, cap: int = 40):
    """Average class size when a school with e pupils in a grade opens ceil(e / cap) classes."""
    e = np.asarray(enrolment, float)
    return e / np.ceil(e / cap)


def maimonides_study(n_schools: int = 2000, effect: float = -0.02, cap: int = 40, sorting: float = 0.0,
                     seed: int = 0) -> dict:
    """Schools with grade enrolment between 20 and 160; class size by Maimonides' rule (plus a little discretion);
    pupils' scores (in standard deviations) fall by ``effect`` per extra pupil in the class and rise with the
    school's advantage, which is correlated with enrolment.  With ``sorting`` > 0 some schools just above a cutoff
    are there because advantaged families push enrolment over it.  Returns the naive slope, the discontinuity
    estimate (2SLS with the rule as instrument, a linear control in enrolment and a window of 15 around the
    cutoffs) and the data for plotting."""
    rng = np.random.default_rng(seed)
    e = rng.integers(20, 161, n_schools).astype(float)
    adv = 0.004 * (e - 90) + rng.normal(0, 0.3, n_schools)      # bigger schools: richer towns
    if sorting > 0:
        near = (e % cap >= cap - 3) & (e < 160)
        push = near & (rng.random(n_schools) < sorting) & (adv > 0)
        e[push] += cap - (e[push] % cap) + 1
    rule = maimonides(e, cap)
    cs = rule + rng.normal(0, 1.5, n_schools)
    score = adv + effect * cs + rng.normal(0, 0.15, n_schools)
    X = np.column_stack([np.ones(n_schools), cs])
    naive = float(np.linalg.lstsq(X, score, rcond=None)[0][1])
    d = np.minimum(np.abs(e[:, None] - (np.array([cap, 2 * cap, 3 * cap]) + 0.5)[None, :]).min(1), 99)
    w = d <= 15
    Z = np.column_stack([np.ones(w.sum()), rule[w], e[w]])
    Xw = np.column_stack([np.ones(w.sum()), cs[w], e[w]])
    pi = np.linalg.lstsq(Z, Xw, rcond=None)[0]
    Xh = Z @ pi
    b = np.linalg.lstsq(Xh, score[w], rcond=None)[0]
    r = score[w] - Xw @ b
    V = np.linalg.inv(Xh.T @ Xh) * (r @ r) / (w.sum() - 3)
    return {"effect": effect, "naive": naive, "iv": float(b[1]), "iv_se": float(np.sqrt(V[1, 1])),
            "enrolment": e.tolist(), "class_size": cs.tolist(), "rule": rule.tolist(), "score": score.tolist()}


def teacher_va(n_teachers: int = 400, years: int = 4, class_size: int = 25, sd_va: float = 0.12,
               sd_class: float = 0.08, sd_pupil: float = 0.55, sorting: float = 0.0, seed: int = 0) -> dict:
    """Teachers with value added ~ N(0, sd_va^2) teach a class a year, four to a school; a class's mean gain is the
    teacher's effect, a class shock and the pupils' own noise.  Value added is estimated from the years before the
    last two and shrunk by its reliability (empirical Bayes).  With ``sorting`` > 0 schools differ in their pupils'
    advantage, which an estimate that ignores it credits to the teachers.  Returns the spread of raw and shrunk
    estimates against the truth, and Chetty, Friedman and Rockoff's forecast test: in the last year half the
    teachers move between schools, and the change in a school's mean score is regressed on the change in its
    teachers' mean predicted value added (a coefficient of one: unbiased forecasts)."""
    rng = np.random.default_rng(seed)
    va = rng.normal(0, sd_va, n_teachers)
    n_s = n_teachers // 4
    school = np.repeat(np.arange(n_s), 4)[:n_teachers]
    rng.shuffle(school)
    school_eff = rng.normal(0, sd_va, n_s)                    # pupils' advantage, which stays with the school
    new_school = school.copy()
    movers = rng.random(n_teachers) < 0.5
    new_school[movers] = rng.permutation(school[movers])
    means = np.empty((n_teachers, years))
    for t in range(years):
        where = new_school if t == years - 1 else school
        cls = rng.normal(0, sd_class, n_teachers)
        noise = rng.normal(0, sd_pupil / np.sqrt(class_size), n_teachers)
        means[:, t] = va + sorting * school_eff[where] + cls + noise
    raw = means[:, :-2].mean(1)              # leave out the two years the move test compares
    signal = np.var(raw) - (sd_class ** 2 + sd_pupil ** 2 / class_size) / (years - 2)
    rel = max(signal, 1e-9) / np.var(raw)
    shrunk = rel * (raw - raw.mean())
    # the move test: a grade's mean score in a school before and after its teachers change
    d_va, d_score = [], []
    for s_ in range(n_s):
        a, b = school == s_, new_school == s_
        if a.sum() and b.sum():
            d_va.append(shrunk[b].mean() - shrunk[a].mean())
            d_score.append(means[b, -1].mean() - means[a, -2].mean())
    d_va, d_score = np.array(d_va), np.array(d_score)
    X = np.column_stack([np.ones_like(d_va), d_va])
    coef = np.linalg.lstsq(X, d_score, rcond=None)[0]
    r = d_score - X @ coef
    se = np.sqrt((np.linalg.inv(X.T @ X) * (r @ r) / (len(r) - 2))[1, 1])
    return {"sd_true": float(va.std()), "sd_raw": float(raw.std()), "sd_shrunk": float(shrunk.std()),
            "reliability": float(rel), "forecast_coef": float(coef[1]), "forecast_se": float(se),
            "corr_raw": float(np.corrcoef(raw, va)[0, 1]), "true": va.tolist(), "raw": raw.tolist(),
            "shrunk": shrunk.tolist(), "d_va": d_va.tolist(), "d_score": d_score.tolist()}


# ---------------------------------------------------------------------------------------------------------------
# health and addiction
# ---------------------------------------------------------------------------------------------------------------

def grossman(ages, r: float = 0.03, delta0: float = 0.025, delta_growth: float = 0.035, pi_h: float = 1.0,
             a: float = 0.3, h_min: float = 0.25) -> dict:
    """Grossman's demand for health: health is a capital stock that yields healthy time; its marginal efficiency,
    a / H (healthy days per unit of health, falling as health rises), equals its user cost pi_h (r + delta(age)),
    with depreciation delta growing with age.  The optimal stock H* = a / (pi_h (r + delta)) falls with age; life
    ends when it would fall below ``h_min``."""
    ages = np.asarray(ages, float)
    delta = delta0 * np.exp(delta_growth * (ages - ages[0]))
    H = a / (pi_h * (r + delta))
    end = ages[np.argmax(H < h_min)] if np.any(H < h_min) else None
    return {"age": ages.tolist(), "delta": delta.tolist(), "health": H.tolist(),
            "death_age": None if end is None else float(end)}


def addiction_path(T: int = 60, rise_at: int = 20, announce_at: int = 10, price0: float = 1.0, price1: float = 1.5,
                   rational: bool = True, beta: float = 0.95, delta: float = 0.3, alpha: float = 2.0,
                   reinforce: float = 0.2, harm: float = 0.1) -> dict:
    """Becker and Murphy's addict with linear-quadratic utility u = alpha c - c^2 / 2 + reinforce c S - harm S^2 / 2
    - p c, and stock S' = (1 - delta) S + c.  A rational addict knows from ``announce_at`` that the price will rise
    from ``rise_at``; a myopic one optimizes period by period, ignoring the stock's future effects.  The rational
    path is solved by backward induction on the linear policy c = k0 + k1 S given the price path (exact for this
    quadratic problem); returns consumption paths."""
    prices = np.where(np.arange(T) >= rise_at, price1, price0)

    def solve(known_prices):
        # value V_t(S) = v0 + v1 S - v2 S^2 / 2 ; backward from V_T = 0
        v1, v2 = 0.0, 0.0
        pol = []
        for t in range(T - 1, -1, -1):
            p = known_prices[t]
            # maximize alpha c - c^2/2 + reinforce c S - harm S^2/2 - p c + beta (v1 S' - v2 S'^2/2)
            # S' = (1-delta) S + c ; FOC: alpha - c + reinforce S - p + beta (v1 - v2 S') = 0
            k_den = 1.0 + beta * v2
            k0 = (alpha - p + beta * v1) / k_den
            k1 = (reinforce - beta * v2 * (1 - delta)) / k_den
            pol.append((k0, k1))
            # new value coefficients: substitute c = k0 + k1 S
            # quadratic in S: collect
            A = 1 - delta + k1                                  # S' = A S + k0
            c0, c1 = k0, k1
            nv1 = (alpha - p) * c1 - c0 * c1 + reinforce * c0 + beta * (v1 * A - v2 * A * k0)
            nv2 = c1 ** 2 - 2 * reinforce * c1 + harm + beta * v2 * A ** 2
            v1, v2 = nv1, nv2
        return pol[::-1]

    c, S = [], 0.0
    stock = []
    if rational:
        before = solve(np.full(T, price0))
        after = solve(prices)
        for t in range(T):
            k0, k1 = (after if t >= announce_at else before)[t]
            ct = max(k0 + k1 * S, 0.0)
            c.append(ct)
            stock.append(S)
            S = (1 - delta) * S + ct
    else:
        for t in range(T):
            ct = max(alpha - prices[t] + reinforce * S, 0.0)
            c.append(ct)
            stock.append(S)
            S = (1 - delta) * S + ct
    return {"t": list(range(T)), "price": prices.tolist(), "consumption": c, "stock": stock}


__all__ = ["felt_punishment", "offend_share", "elasticities", "play_doubling", "optimal_enforcement",
           "police_blocks", "household_time", "choo_siow", "choo_siow_estimate", "draw_market", "sorting_index",
           "quantity_quality", "wald", "collective", "maimonides", "maimonides_study", "teacher_va", "grossman",
           "addiction_path"]

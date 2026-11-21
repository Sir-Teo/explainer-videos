"""Agora's firm from the inside (Part 62): the Island's industry of plants with managers, incentives and owners.

* **Productivity dispersion** (:func:`dispersion`): plants with log-normal productivity in a market with CES demand;
  plants that cannot cover a fixed cost exit; the spread among survivors falls as competition (substitutability)
  rises (after Syverson).
* **Management scores** (:func:`management`): the Island's firms scored on practices from 1 to 5, by ownership; the
  scores' relation to productivity.
* **Play it** (:func:`practices`): four practices for one plant and their value over three years.
* **The management experiment** (:func:`experiment`): 28 plants in 17 firms, consulting randomized by firm; weekly
  productivity; difference in differences with firm-clustered errors (after Bloom, Eifert, Mahajan, McKenzie and
  Roberts).
* **Piece rates** (:func:`piece_rates`): a switch from hourly pay to piece rates; the gain split into effort and
  sorting (after Lazear's Safelite).
* **The Peter principle** (:func:`peter`): promoting the best seller against the best manager.
* **CEO pay** (:func:`ceo_pay`): Gabaix and Landier's assignment of talent to firm size; pay for luck
  (:func:`pay_for_luck`, after Bertrand and Mullainathan).
* **Capital structure** (:func:`tradeoff`): the tax shield against expected distress costs.
* **Agency** (:func:`perks`): Jensen and Meckling's owner-manager.
* **Private equity** (:func:`buyouts`): establishments of buyout targets and controls; exits, entry and
  reallocation.
* **Knowledge hierarchies** (:func:`hierarchy`): Garicano's teams of workers and a manager; communication and
  knowledge costs.
* **Working from home** (:func:`wfh`): a randomized call-centre trial with performance and quits.
* **Diversification** (:func:`conglomerates`): excess value against stand-alone multiples, and selection.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize, stats

# ---------------------------------------------------------------------------------------------------------------
# dispersion


def dispersion(sigmas=(2.0, 3.0, 4.0, 6.0, 8.0, 10.0), n: int = 4000, sd: float = 0.45, revenue: float = 4000.0,
               fixed: float = 0.25, seed: int = 62) -> dict:
    """Plants draw log productivity from N(0, sd); with CES demand of elasticity sigma, a plant's revenue share is
    phi^(sigma - 1) over the sum, and its profit revenue/sigma less a fixed cost.  Plants with negative profit exit,
    repeatedly, until none would.  Returns, by sigma, the survivors' 90/10 productivity ratio and their number."""
    rng = np.random.default_rng(seed)
    phi = np.exp(rng.normal(0.0, sd, n))
    bins = np.linspace(-1.5, 1.5, 31)
    rows = []
    for s in sigmas:
        alive = np.ones(n, bool)
        for _ in range(200):
            w = phi[alive] ** (s - 1)
            prof = revenue * w / w.sum() / s - fixed
            if (prof >= 0).all():
                break
            idx = np.flatnonzero(alive)
            alive[idx[prof < 0]] = False
        lp = np.log(phi[alive])
        rows.append({"sigma": float(s), "survivors": int(alive.sum()),
                     "ratio_90_10": float(np.exp(np.percentile(lp, 90) - np.percentile(lp, 10))),
                     "cutoff": float(phi[alive].min()), "hist": np.histogram(lp, bins=bins)[0].tolist(),
                     "mean_log": float(lp.mean())})
    return {"rows": rows, "bins": bins.tolist(), "entry_hist": np.histogram(np.log(phi), bins=bins)[0].tolist(),
            "entry_ratio_90_10": float(np.exp(np.percentile(np.log(phi), 90) - np.percentile(np.log(phi), 10)))}


# ---------------------------------------------------------------------------------------------------------------
# management practices

OWNERS = {  # mean management score (1 to 5) and share of the Island's firms
    "dispersed shareholders": (3.15, 0.20),
    "private equity": (3.10, 0.08),
    "family-owned, outside chief executive": (3.00, 0.12),
    "multinational subsidiary": (3.25, 0.10),
    "family-owned, family chief executive": (2.65, 0.30),
    "founder": (2.85, 0.15),
    "government": (2.55, 0.05),
}


def management(n: int = 1500, slope: float = 0.25, seed: int = 62) -> dict:
    """The Island's firms are scored on 18 practices (each 1 to 5, from targets to incentives); a firm's score is
    the mean.  Ownership shifts the mean (OWNERS); log productivity rises by ``slope`` per point of the score, plus
    noise.  Returns each firm's score and log productivity, the means by ownership, and the regression slope."""
    rng = np.random.default_rng(seed)
    names = list(OWNERS)
    shares = np.array([OWNERS[k][1] for k in names])
    own = rng.choice(len(names), n, p=shares / shares.sum())
    mean = np.array([OWNERS[names[k]][0] for k in own])
    latent = mean + rng.normal(0, 0.5, n)
    practices = np.clip(np.round(latent[:, None] + rng.normal(0, 0.7, (n, 18))), 1, 5)
    score = practices.mean(axis=1)
    lp = slope * (score - score.mean()) + rng.normal(0, 0.35, n)
    X = np.column_stack([np.ones(n), score])
    b = np.linalg.lstsq(X, lp, rcond=None)[0]
    by = {names[k]: float(score[own == k].mean()) for k in range(len(names))}
    return {"score": score.tolist(), "log_tfp": lp.tolist(), "owner": [names[k] for k in own], "by_owner": by,
            "slope": float(b[1]), "planted_slope": slope, "share_below_3": float(np.mean(score < 3.0))}


PRACTICES = {  # cost ($000), effect on output (share) or other saving, chance it works, years to full effect
    "record and act on defects": {"cost": 60.0, "output": 0.08, "inventory": 0.0, "p": 0.85},
    "count and cut inventory": {"cost": 40.0, "output": 0.0, "inventory": 0.35, "p": 0.85},
    "a faster loom": {"cost": 600.0, "output": 0.10, "inventory": 0.0, "p": 0.95},
    "pay for performance": {"cost": 150.0, "output": 0.06, "inventory": 0.0, "p": 0.6},
}


def practices(revenue: float = 8000.0, margin: float = 0.25, inventory: float = 1500.0, rate: float = 0.12,
              years: int = 3, seed: int = 62, reps: int = 20000) -> dict:
    """One Island plant ($000s: revenue 8,000, value added at the margin ``margin``, inventory 1,500 carried at
    ``rate`` a year) chooses among four practices (PRACTICES).  Each works with probability p; if it does, output
    rises by its effect (half in the first year) or inventory falls.  Returns each practice's expected net value over
    ``years`` years, its return per dollar, and the spread of outcomes."""
    rng = np.random.default_rng(seed)
    out = {}
    for name, P in PRACTICES.items():
        works = rng.random(reps) < P["p"]
        size = np.clip(rng.normal(1.0, 0.3, reps), 0.2, None)
        gain = 0.0
        for y in range(years):
            ramp = 0.5 if y == 0 else 1.0
            gain = gain + works * size * (P["output"] * ramp * revenue * margin + P["inventory"] * inventory * rate)
        net = gain - P["cost"]
        out[name] = {"cost": P["cost"], "mean_net": float(net.mean()), "per_dollar": float(net.mean() / P["cost"]),
                     "p10": float(np.percentile(net, 10)), "p90": float(np.percentile(net, 90)), "p": P["p"]}
    best = max(out, key=lambda k: out[k]["per_dollar"])
    return {"rows": out, "best": best, "revenue": revenue}


def experiment(firms: int = 17, plants_per=(2, 1), treated_firms: int = 11, weeks: int = 140, effect: float = 0.17,
               start: int = 40, ramp: int = 30, noise: float = 0.08, shift: float = 0.08, seed: int = 62,
               reps: int = 400) -> dict:
    """The Island's management experiment: 17 firms with one or two plants (28 in all), consulting given at random to
    11 firms from week ``start``; adopted practices raise log productivity by up to ``effect``, phased in over
    ``ramp`` weeks.  Weekly log productivity has plant effects, common shocks and noise.  The effect is estimated by
    difference in differences over the year after the start, with standard errors clustered by firm; repeated to show
    the spread of estimates."""
    rng = np.random.default_rng(seed)
    sizes = np.array([plants_per[0]] * 11 + [plants_per[1]] * (firms - 11))
    firm_of = np.repeat(np.arange(firms), sizes)
    P = len(firm_of)
    t = np.arange(weeks)
    phase = np.clip((t - start) / ramp, 0, 1)
    ests, ses, paths = [], [], None
    for r in range(reps):
        tf = rng.permutation(firms) < treated_firms
        treat = tf[firm_of]
        y = (rng.normal(0, 0.3, P)[:, None] + 0.04 * np.sin(t / 9.0)[None, :]
             + rng.normal(0, 0.03, weeks)[None, :] + rng.normal(0, noise, (P, weeks)))
        y = y + effect * treat[:, None] * phase[None, :] * np.clip(rng.normal(1.0, 0.25, P), 0, None)[:, None]
        y = y + (t >= start)[None, :] * rng.normal(0, shift, P)[:, None]       # plants' own fortunes change too
        pre, post = t < start, (t >= start + ramp) & (t < start + ramp + 52)
        d = y[:, post].mean(1) - y[:, pre].mean(1)
        est = d[treat].mean() - d[~treat].mean()
        # firm-clustered standard error of the difference in means
        fd = np.array([d[firm_of == f].mean() for f in range(firms)])
        se = np.sqrt(fd[tf].var(ddof=1) / tf.sum() + fd[~tf].var(ddof=1) / (~tf).sum())
        ests.append(est)
        ses.append(se)
        if r == 0:
            paths = {"treated": y[treat].mean(0).tolist(), "control": y[~treat].mean(0).tolist()}
    return {"effect": effect, "mean_est": float(np.mean(ests)), "sd_est": float(np.std(ests)),
            "first_est": float(ests[0]), "first_se": float(ses[0]), "plants": int(P), "firms": firms,
            "treated_firms": treated_firms, "paths": paths, "weeks": weeks, "start": start, "ramp": ramp,
            "est_draws": [float(v) for v in ests[:80]]}


# ---------------------------------------------------------------------------------------------------------------
# personnel economics


def piece_rates(n: int = 4000, wage: float = 11.0, rate: float = 11.0, cost: float = 30.0, turnover: float = 0.4,
                sd_a: float = 0.3, seed: int = 62) -> dict:
    """Workers differ in ability a (log-normal, median 1) and in their outside option, which rises with ability.
    Under an hourly wage they produce the standard, one unit an hour times a, since effort above it is unpaid; the
    firm's workers are those whose outside option is below the wage.  Under a piece rate of ``rate`` a unit with the
    old wage guaranteed, effort above the standard costs cost (e - 1)^2/2, and each worker takes the better of the
    guarantee at the standard and the interior choice e = 1 + rate a/cost.  Nobody is worse off, so nobody leaves;
    but when ``turnover`` of the workforce is replaced, the new hires are those who prefer the piece rate to their
    outside option, and they are abler.  Returns output per worker under the wage, for the same workers under the
    piece rate, and for the workforce after turnover: the gain splits into effort and sorting."""
    rng = np.random.default_rng(seed)

    def choose(a):
        e_int = 1.0 + rate * a / cost
        u_int = rate * a * e_int - cost * (e_int - 1.0) ** 2 / 2
        u_std = np.maximum(rate * a, wage)
        return np.where(u_int > u_std, e_int, 1.0), np.maximum(u_int, u_std)
    pool = np.exp(rng.normal(0, sd_a, 40 * n))
    outside = wage * pool ** 0.6 + rng.normal(-0.5, 0.8, pool.size)
    staff = pool[outside < wage][:n]
    y0 = staff.mean()
    e, _ = choose(staff)
    y1 = (staff * e).mean()
    _, u = choose(pool)
    willing = pool[u >= outside]
    k = int(turnover * n)
    after = np.r_[staff[: n - k], willing[:k]]
    ea, _ = choose(after)
    y2 = (after * ea).mean()
    return {"output_wage": float(y0), "output_same_workers": float(y1), "output_after": float(y2),
            "gain_total": float(y2 / y0 - 1), "gain_effort": float(y1 / y0 - 1),
            "share_sorting": float((y2 - y1) / (y2 - y0)), "ability_staff": float(staff.mean()),
            "ability_hires": float(willing[:k].mean()), "share_above_standard": float((e > 1.0).mean()),
            "cv_wage": float(staff.std() / y0), "cv_piece": float((after * ea).std() / y2)}


def peter(n_teams: int = 400, team: int = 8, rho: float = 0.2, seed: int = 62) -> dict:
    """Each team's sellers have selling skill s and managing skill m, correlated ``rho``; one is promoted to manage
    the rest, whose sales rise with the manager's m.  Promote the best seller, or the best manager (if the firm could
    see it), or at random.  Returns the promoted person's sales skill and managing skill, and the team's sales after,
    under each rule."""
    rng = np.random.default_rng(seed)
    z1 = rng.normal(0, 1, (n_teams, team))
    z2 = rho * z1 + np.sqrt(1 - rho ** 2) * rng.normal(0, 1, (n_teams, team))
    s, m = z1, z2
    out = {}
    for rule, pick in (("the best seller", s.argmax(1)), ("the best manager", m.argmax(1)),
                       ("at random", rng.integers(0, team, n_teams))):
        idx = np.arange(n_teams)
        ms, ss = m[idx, pick], s[idx, pick]
        rest = (s.sum(1) - ss) / (team - 1)
        sales = 1.0 + 0.1 * rest + 0.08 * ms
        out[rule] = {"sales_skill": float(ss.mean()), "manage_skill": float(ms.mean()),
                     "team_sales": float(sales.mean())}
    return {"rules": out, "rho": rho, "team": team}


# ---------------------------------------------------------------------------------------------------------------
# executives


def ceo_pay(n: int = 500, alpha: float = 1.0, beta: float = 2.0 / 3.0, gamma: float = 1.0, scale: float = 1.0,
            n_star: int = 250, d_star: float = 1.0) -> dict:
    """Gabaix and Landier: firm n (by size rank) has size S(n) = scale x n^(-1/alpha); in equilibrium the CEO of firm n
    is paid w(n) = D(n*) S(n*)^(beta/alpha) S(n)^(gamma - beta/alpha), where n* is a reference firm and beta measures
    how fast talent thins out.  Returns pay by rank, the cross-section elasticity of pay to own size, and pay when
    every firm grows by six."""
    k = np.arange(1, n + 1)

    def w(sc):
        S = sc * k ** (-1.0 / alpha)
        S_star = sc * n_star ** (-1.0 / alpha)
        return d_star * S_star ** (beta / alpha) * S ** (gamma - beta / alpha), S
    w1, S1 = w(scale)
    w6, S6 = w(6.0 * scale)
    return {"rank": k.tolist(), "size": S1.tolist(), "pay": w1.tolist(), "pay_x6": w6.tolist(),
            "elasticity_own_size": gamma - beta / alpha, "ratio_after_sixfold": float(w6[0] / w1[0]),
            "top_over_250th": float(w1[0] / w1[249])}


def pay_for_luck(n: int = 3000, weak_share: float = 0.5, seed: int = 62) -> dict:
    """Firms' performance is the chief executive's skill plus luck (an oil price everyone sees).  A strong board pays
    for skill only; a weak board pays for performance, luck included.  Regressing pay on performance, and on luck
    alone, separately by board: the weak boards' pay moves with luck as much as with skill (after Bertrand and
    Mullainathan)."""
    rng = np.random.default_rng(seed)
    skill = rng.normal(0, 1, n)
    luck = rng.normal(0, 1, n)
    perf = skill + luck
    weak = rng.random(n) < weak_share
    pay = np.where(weak, 0.5 * perf, 0.5 * skill) + rng.normal(0, 0.3, n)
    out = {}
    for name, sel in (("strong board", ~weak), ("weak board", weak)):
        b_perf = np.polyfit(perf[sel], pay[sel], 1)[0]
        b_luck = np.polyfit(luck[sel], pay[sel], 1)[0]
        out[name] = {"on_performance": float(b_perf), "on_luck": float(b_luck)}
    return out


# ---------------------------------------------------------------------------------------------------------------
# finance and governance


def tradeoff(tax: float = 0.21, value: float = 100.0, vol: float = 0.35, distress: float = 0.6) -> dict:
    """The trade-off theory: a firm worth ``value`` unlevered borrows a share L of it; the tax shield is worth
    tax x debt; default happens if next year's value (log-normal, volatility ``vol``) falls below the debt, and then a
    share ``distress`` of the value is lost.  Returns firm value by leverage and the best leverage."""
    Ls = np.linspace(0.0, 0.95, 96)
    vals, pdef = [], []
    for L in Ls:
        D = L * value
        if D <= 0:
            p, loss = 0.0, 0.0
        else:
            z = (np.log(D / value) + 0.5 * vol ** 2) / vol
            p = stats.norm.cdf(z)
            # expected firm value conditional on default, times the distress share
            ev_def = value * stats.norm.cdf(z - vol)
            loss = distress * ev_def
        vals.append(value + tax * D - loss)
        pdef.append(p)
    vals = np.array(vals)
    i = int(np.argmax(vals))
    return {"leverage": Ls.tolist(), "value": vals.tolist(), "p_default": pdef, "best": float(Ls[i]),
            "best_value": float(vals[i]), "gain": float(vals[i] - value)}


def perks(alphas=None, value: float = 100.0, k: float = 3.0) -> dict:
    """Jensen and Meckling: an owner-manager owns a share alpha of a firm worth ``value`` less the perks P they take,
    and enjoys perks worth k ln(1 + P).  They choose P to maximize alpha (value - P) + k ln(1 + P): P = k/alpha - 1.
    Returns perks, firm value and the agency cost by alpha."""
    alphas = np.linspace(0.05, 1.0, 96) if alphas is None else np.asarray(alphas, float)
    P = np.clip(k / alphas - 1.0, 0.0, value)
    return {"alpha": alphas.tolist(), "perks": P.tolist(), "value": (value - P).tolist(),
            "agency_cost": (P - max(k - 1.0, 0.0)).tolist()}


def buyouts(n_targets: int = 300, n_controls: int = 1200, years: int = 6, seed: int = 62) -> dict:
    """Establishments of buyout targets and of matched controls, with productivity and employment.  After a buyout
    the new owners close the least productive establishments faster, open new ones, and shrink the rest a little;
    controls carry on.  Returns employment and productivity paths relative to controls, at the original
    establishments and at the firm (with new establishments)."""
    rng = np.random.default_rng(seed)

    def firm(n, target):
        est = rng.integers(3, 12, n)
        rows_emp_orig, rows_emp_firm, rows_prod = [], [], []
        for f in range(n):
            k = est[f]
            prod = rng.normal(0, 0.35, k)
            emp = np.exp(rng.normal(3.5, 0.6, k)) * np.exp(0.5 * prod)
            alive = np.ones(k, bool)
            new_emp, new_prod = [], []
            e_o, e_f, pr = [], [], []
            for y in range(years + 1):
                if y > 0:
                    hazard = 0.04 + (0.03 if target else 0.0) * (prod < np.percentile(prod, 35))
                    alive &= rng.random(k) > hazard
                    emp = emp * np.exp(rng.normal(-0.003 if target else 0.0, 0.05, k))
                    if target and rng.random() < 0.18:
                        new_emp.append(float(np.exp(rng.normal(3.2, 0.5))))
                        new_prod.append(float(rng.normal(0.25, 0.3)))
                    elif rng.random() < 0.08:
                        new_emp.append(float(np.exp(rng.normal(3.2, 0.5))))
                        new_prod.append(float(rng.normal(0.0, 0.35)))
                eo = emp[alive].sum()
                ef = eo + sum(new_emp)
                w = np.r_[emp[alive], new_emp]
                p = np.r_[prod[alive], new_prod]
                e_o.append(eo)
                e_f.append(ef)
                pr.append(float((w * p).sum() / w.sum()) if w.sum() > 0 else 0.0)
            rows_emp_orig.append(e_o)
            rows_emp_firm.append(e_f)
            rows_prod.append(pr)
        return np.array(rows_emp_orig), np.array(rows_emp_firm), np.array(rows_prod)

    to, tf, tp = firm(n_targets, True)
    co, cf, cp = firm(n_controls, False)
    rel_o = (to.sum(0) / to.sum(0)[0]) / (co.sum(0) / co.sum(0)[0]) - 1
    rel_f = (tf.sum(0) / tf.sum(0)[0]) / (cf.sum(0) / cf.sum(0)[0]) - 1
    rel_p = tp.mean(0) - tp.mean(0)[0] - (cp.mean(0) - cp.mean(0)[0])
    return {"years": list(range(years + 1)), "emp_original": rel_o.tolist(), "emp_firm": rel_f.tolist(),
            "productivity": rel_p.tolist()}


# ---------------------------------------------------------------------------------------------------------------
# organization


def _team_output(zw, zm, h, c):
    """Garicano's team: problems have difficulty z ~ Exp(1); workers solve z < zw, pass the rest to one manager, who
    spends h per problem passed and solves z < zm.  The manager's time sets the span n = 1/(h e^(-zw)).  Net output per
    member: (n (1 - e^(-zm)) - c (n zw + zm)) / (n + 1)."""
    n = 1.0 / (h * np.exp(-zw))
    return (n * (1 - np.exp(-zm)) - c * (n * zw + zm)) / (n + 1), n


def hierarchy(hs=(0.6, 0.4, 0.25, 0.15, 0.1), cs=(0.08, 0.05, 0.03)) -> dict:
    """For each communication cost h and knowledge cost c, the knowledge of workers and managers that maximizes net
    output per team member, the span of control and the output: cheaper communication widens spans and lets workers
    know less (centralization); cheaper knowledge lets workers know more (decentralization)."""
    rows = []
    for c in cs:
        for h in hs:
            def neg(x):
                zw, zm = x
                if zw < 0 or zm < zw:
                    return 1e3
                return -_team_output(zw, zm, h, c)[0]
            best = None
            for zw0 in (0.2, 0.8, 1.5):
                for zm0 in (2.0, 3.5, 5.0):
                    r = optimize.minimize(neg, [zw0, zm0], method="Nelder-Mead",
                                          options={"xatol": 1e-6, "fatol": 1e-9, "maxiter": 4000})
                    if best is None or r.fun < best.fun:
                        best = r
            zw, zm = best.x
            y, n = _team_output(zw, zm, h, c)
            rows.append({"h": h, "c": c, "zw": float(zw), "zm": float(zm), "span": float(n), "output": float(y),
                         "worker_solves": float(1 - np.exp(-zw))})
    return {"rows": rows}


def wfh(n: int = 250, weeks: int = 40, effect_minutes: float = 0.09, effect_rate: float = 0.04,
        quit_office: float = 0.35, quit_home: float = 0.175, seed: int = 62) -> dict:
    """A call centre's volunteers, randomized to work from home or stay in the office for ``weeks`` weeks.  Home
    workers work more minutes a shift (``effect_minutes``) and take more calls a minute (``effect_rate``); quits over
    the trial are ``quit_office`` and ``quit_home``.  Returns the estimated effects with standard errors."""
    rng = np.random.default_rng(seed)
    home = rng.permutation(n) < n // 2
    base_min = rng.normal(420, 25, n)
    base_rate = rng.normal(1.0, 0.12, n)
    minutes = base_min[:, None] * (1 + effect_minutes * home[:, None]) * np.exp(rng.normal(0, 0.06, (n, weeks)))
    rate_ = base_rate[:, None] * (1 + effect_rate * home[:, None]) * np.exp(rng.normal(0, 0.05, (n, weeks)))
    calls = minutes * rate_
    quit_ = rng.random(n) < np.where(home, quit_home, quit_office)

    def diff(x):
        a, b = np.log(x[home].mean(1)), np.log(x[~home].mean(1))
        return float(np.exp(a.mean() - b.mean()) - 1), float(np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)))
    perf, perf_se = diff(calls)
    mins, mins_se = diff(minutes)
    rate_e, rate_se = diff(rate_)
    return {"performance": perf, "performance_se": perf_se, "minutes": mins, "minutes_se": mins_se, "rate": rate_e,
            "rate_se": rate_se, "quit_home": float(quit_[home].mean()), "quit_office": float(quit_[~home].mean()),
            "n": n}


def conglomerates(n: int = 2000, selection: float = 0.08, true_effect: float = -0.06, seed: int = 62) -> dict:
    """Firms with one or several segments; excess value is the log of firm value over the sum of each segment's
    stand-alone value (its sales times the median single-segment multiple).  Diversified firms carry a true effect,
    and firms that diversify were already worth less (``selection``).  Returns the average excess value of
    diversified firms, and the part that was there before they diversified."""
    rng = np.random.default_rng(seed)
    div = rng.random(n) < 0.4
    quality = rng.normal(0, 0.3, n)
    pre = quality - selection * div
    excess = pre + true_effect * div + rng.normal(0, 0.15, n)
    return {"discount": float(excess[div].mean() - excess[~div].mean()),
            "before": float(pre[div].mean() - pre[~div].mean()), "true_effect": true_effect,
            "share_diversified": float(div.mean())}


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("np", "optimize", "stats", "annotations")]

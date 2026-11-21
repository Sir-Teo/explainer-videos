"""Agora's environment and climate (Part 48): exhaustible resources (Hotelling's rule, with falling extraction costs),
the Simon-Ehrlich bet rerun over every window, a fishery under open access and under quotas, a small climate model
fitted to the record (carbon boxes, forcing, a two-layer energy balance), a DICE-style integrated assessment model
with an optimal emissions-control path and the social cost of carbon, fat tails, climate clubs, learning curves,
directed technical change, a temperature-growth panel and a merit-order electricity market with withholding.

numpy and scipy only.  Units: emissions in billions of tonnes of CO2 (GtCO2) a year, concentrations in parts per
million, temperatures in degrees C above 1850-1900, money in trillions of 2019 dollars at PPP unless stated."""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq, minimize

# ---------------------------------------------------------------------------------------------------------------
# exhaustible resources


def hotelling(stock: float = 100.0, choke: float = 10.0, slope: float = 1.0, r: float = 0.05, cost: float = 0.0,
              cost_growth: float = 0.0, years: int = 200) -> dict:
    """A competitive mine with a fixed stock and linear demand q = (choke - p)/slope.  Hotelling's rule: the price
    net of extraction cost (the scarcity rent) rises at the rate of interest, p_t = c_t + lambda (1 + r)^t, and
    lambda is set so that the stock runs out exactly when the price reaches the choke price.  With a constant cost
    (cost_growth = 0) the price rises steadily; with costs falling fast enough the price first falls, then rises.
    Returns the paths and the year of exhaustion."""
    t = np.arange(years, dtype=float)
    c = cost * (1 + cost_growth) ** t

    def path(lam):
        p = np.minimum(c + lam * (1 + r) ** t, choke)
        q = np.maximum(choke - p, 0.0) / slope
        return p, q

    def excess(lam):
        p, q = path(lam)
        return q.sum() - stock

    lo, hi = 1e-9, choke
    if excess(hi) > 0:          # even the highest rent leaves the stock unexhausted within the horizon
        lam = hi
    else:
        lam = brentq(excess, lo, hi)
    p, q = path(lam)
    out = int(np.argmax(q <= 1e-9)) if np.any(q <= 1e-9) else years
    return {"t": t.tolist(), "price": p.tolist(), "quantity": q.tolist(), "cost": c.tolist(), "rent0": float(lam),
            "exhausted": out}


def bet_windows(years, prices: dict, cpi, span: int = 10) -> dict:
    """Simon and Ehrlich's bet rerun for every window of ``span`` years: an equal dollar amount of each metal is
    bought at the start; Ehrlich wins if the bundle is worth more, in real terms, at the end.  ``prices`` maps each
    metal to annual nominal prices aligned with ``years``; ``cpi`` is the price level.  Returns, for each start year,
    the real change in the bundle's value and the share of windows Ehrlich wins."""
    years = np.asarray(years, int)
    cpi = np.asarray(cpi, float)
    real = {m: np.asarray(v, float) / cpi for m, v in prices.items()}
    starts, change = [], []
    for i, y0 in enumerate(years):
        j = np.where(years == y0 + span)[0]
        if not len(j):
            continue
        j = j[0]
        rel = [real[m][j] / real[m][i] for m in real]
        if not np.all(np.isfinite(rel)):
            continue
        starts.append(int(y0))
        change.append(float(np.mean(rel) - 1.0))
    change = np.array(change)
    return {"start": starts, "change": change.tolist(), "ehrlich_share": float(np.mean(change > 0)),
            "n": len(starts)}


# ---------------------------------------------------------------------------------------------------------------
# a fishery


def fishery_curves(growth: float = 0.5, capacity: float = 1.0, catchability: float = 1.0, price: float = 1.0,
                   cost: float = 0.2, efforts=None) -> dict:
    """Gordon and Schaefer's fishery: stock grows logistically, g S (1 - S/K), and catch is q E S.  In the steady
    state S = K (1 - qE/g), so the sustainable catch is qEK(1 - qE/g).  Open access drives effort to where revenue
    equals cost (no rent); a sole owner or a quota stops at the effort that maximizes the rent; the maximum
    sustainable yield lies in between."""
    g, K, q = growth, capacity, catchability
    E = np.linspace(0, g / q, 201) if efforts is None else np.asarray(efforts, float)
    yld = q * E * K * np.clip(1 - q * E / g, 0, None)
    rev, cst = price * yld, cost * E
    e_oa = g / q * (1 - cost / (price * q * K)) if price * q * K > cost else 0.0
    e_mey = e_oa / 2
    e_msy = g / (2 * q)
    rent = lambda e: price * q * e * K * (1 - q * e / g) - cost * e  # noqa: E731
    return {"effort": E.tolist(), "yield": yld.tolist(), "revenue": rev.tolist(), "cost": cst.tolist(),
            "e_open": float(e_oa), "e_mey": float(e_mey), "e_msy": float(e_msy),
            "stock_open": float(K * (1 - q * e_oa / g)), "stock_mey": float(K * (1 - q * e_mey / g)),
            "rent_mey": float(rent(e_mey)), "rent_open": float(rent(e_oa)), "msy": float(g * K / 4)}


def fishery_dynamics(years: int = 80, growth: float = 0.5, capacity: float = 1.0, catchability: float = 1.0,
                     price: float = 1.0, cost: float = 0.2, entry: float = 2.0, stock0: float = 1.0,
                     effort0: float = 0.02, quota: float | None = None, dt: float = 0.1) -> dict:
    """Open access over time (Smith, 1969): boats enter while fishing pays (dE/dt = entry x profit per unit of
    effort) and the stock follows its growth less the catch.  The stock overshoots below its open-access level and
    the fleet with it.  With ``quota``, the catch is capped at that total and boats enter only to share it."""
    g, K, q = growth, capacity, catchability
    n = int(years / dt)
    S, E = stock0, effort0
    ts, Ss, Es, Hs = [], [], [], []
    for k in range(n):
        h = q * E * S
        if quota is not None:
            h = min(h, quota)
        profit_per_effort = (price * h - cost * E) / max(E, 1e-9)
        S = max(S + dt * (g * S * (1 - S / K) - h), 1e-6)
        E = max(E + dt * entry * profit_per_effort * E, 1e-6)
        if k % int(round(1 / dt)) == 0:
            ts.append(k * dt)
            Ss.append(S)
            Es.append(E)
            Hs.append(h)
    return {"t": ts, "stock": Ss, "effort": Es, "catch": Hs}


# ---------------------------------------------------------------------------------------------------------------
# the climate: carbon boxes, forcing and temperature

# the IPCC's fifth-assessment impulse response of atmospheric CO2 (Joos et al. 2013): fractions and timescales
CARBON_A = np.array([0.2173, 0.2240, 0.2824, 0.2763])
CARBON_TAU = np.array([1e9, 394.4, 36.54, 4.304])
PPM_PER_GTC = 1 / 2.124            # 2.124 GtC raise the atmosphere's CO2 by 1 ppm
GTC_PER_GTCO2 = 12 / 44.01
PREINDUSTRIAL_PPM = 278.0
F2X = 5.35 * np.log(2)             # forcing from doubled CO2, W/m^2 (Myhre et al. 1998)


def carbon_cycle(emissions, speed: float = 1.0, boxes0=None) -> dict:
    """Atmospheric CO2 from annual emissions (GtCO2): four boxes, each receiving its fraction of every year's
    emissions and decaying with its timescale (the last three timescales multiplied by ``speed``, so a speed below
    one means faster sinks).  Returns the concentration each year and the final boxes (GtC above pre-industrial)."""
    tau = CARBON_TAU * np.array([1.0, speed, speed, speed])
    decay = np.exp(-1 / tau)
    b = np.zeros(4) if boxes0 is None else np.array(boxes0, float)
    ppm = []
    for e in np.asarray(emissions, float):
        b = b * decay + CARBON_A * e * GTC_PER_GTCO2
        ppm.append(PREINDUSTRIAL_PPM + b.sum() * PPM_PER_GTC)
    return {"ppm": np.array(ppm), "boxes": b}


def ebm(forcing, ecs: float = 3.0, c_up: float = 7.3, c_deep: float = 106.0, gamma: float = 0.73, T0=(0.0, 0.0)):
    """A two-layer energy balance: C dT/dt = F - lambda T - gamma (T - T_deep), C_deep dT_deep/dt = gamma (T -
    T_deep), with lambda = F2x/ECS (annual steps; heat capacities in W yr m^-2 K^-1).  Returns surface and deep
    temperatures."""
    lam = F2X / ecs
    T, D = T0
    out, deep = [], []
    for f in np.asarray(forcing, float):
        T, D = T + (f - lam * T - gamma * (T - D)) / c_up, D + gamma * (T - D) / c_deep
        out.append(T)
        deep.append(D)
    return np.array(out), np.array(deep)


def forcing(ppm, so2_mt=None, ghg_scale: float = 1.0, aerosol: float = 0.0):
    """Radiative forcing: CO2's 5.35 ln(C/C0), scaled up by ``ghg_scale`` for the other greenhouse gases, less
    ``aerosol`` W/m^2 per 100 Mt of sulphur dioxide a year."""
    f = ghg_scale * 5.35 * np.log(np.asarray(ppm, float) / PREINDUSTRIAL_PPM)
    if so2_mt is not None:
        f = f - aerosol * np.asarray(so2_mt, float) / 100.0
    return f


def fit_climate(year, fossil, land, so2_mt, obs_year, obs_ppm, temp_year, temp_anom, ecs: float = 3.0) -> dict:
    """Fit the small climate model to the record in two stages.  Carbon: choose how fast the sinks work (``speed``)
    and how much of the uncertain land-use emissions count (``land_weight``) to match Mauna Loa.  Temperature, with
    the equilibrium sensitivity fixed at ``ecs``: choose the other gases' scale and the aerosols' cooling per 100 Mt
    of SO2 to match HadCRUT5 (anomalies against 1850-1900).  Returns the parameters, fitted series and errors."""
    year = np.asarray(year, int)
    fossil, land = np.asarray(fossil, float), np.nan_to_num(np.asarray(land, float))
    obs_year, obs_ppm = np.asarray(obs_year, int), np.asarray(obs_ppm, float)
    m = np.isin(year, obs_year)
    mo = np.isin(obs_year, year)

    def c_loss(p):
        if p[0] <= 0.02 or p[1] < 0:
            return 1e9
        ppm = carbon_cycle(fossil + p[1] * land, p[0])["ppm"]
        return float(np.mean((ppm[m] - obs_ppm[mo]) ** 2))

    rc = minimize(c_loss, [0.5, 0.6], method="Nelder-Mead", options={"xatol": 1e-5, "fatol": 1e-8})
    speed, lw = rc.x
    ppm = carbon_cycle(fossil + lw * land, speed)["ppm"]
    temp_year, temp_anom = np.asarray(temp_year, int), np.asarray(temp_anom, float)
    base = (temp_year >= 1850) & (temp_year <= 1900)
    obs_t = temp_anom - temp_anom[base].mean()
    mt = np.isin(year, temp_year)
    mto = np.isin(temp_year, year)
    pre = (year >= 1850) & (year <= 1900)

    def model_t(k, b):
        T, _ = ebm(forcing(ppm, so2_mt, k, b), ecs)
        return T - T[pre].mean()

    def t_loss(p):
        return float(np.mean((model_t(*p)[mt] - obs_t[mto]) ** 2))

    rt = minimize(t_loss, [1.2, 0.5], method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-10})
    k, b = rt.x
    T = model_t(k, b)
    F = forcing(ppm, so2_mt, k, b)
    return {"speed": float(speed), "land_weight": float(lw), "ghg_scale": float(k), "aerosol": float(b),
            "ecs": ecs, "ppm": ppm.tolist(), "temp": T.tolist(), "forcing": F.tolist(),
            "ppm_rmse": float(np.sqrt(rc.fun)), "temp_rmse": float(np.sqrt(rt.fun)), "year": year.tolist(),
            "obs_temp": obs_t.tolist(), "temp_year": temp_year.tolist()}


def tcr(ecs: float = 3.0, **kw) -> float:
    """Transient climate response: warming when CO2 has doubled after rising 1% a year for 70 years."""
    T, _ = ebm(5.35 * np.log(1.01 ** np.arange(1, 71)), ecs, **kw)
    return float(T[-1])


# ---------------------------------------------------------------------------------------------------------------
# a DICE-style integrated assessment model


DICE_DEFAULTS = dict(
    start=2025, years=276,                 # annual steps, 2025-2300
    pop0=8.2, pop_max=10.3, pop_rate=0.04,  # billions
    output0=150.0, capital_ratio=3.0, alpha=0.3, depreciation=0.05, savings=0.25,
    tfp_growth0=0.012, tfp_decline=0.006,
    emissions0=39.0, sigma_decline0=0.015, sigma_decline_rate=0.001,
    land0=4.4, land_decline=0.02,
    backstop2050=515.0, backstop_fall_early=0.01, backstop_fall_late=0.001, theta2=2.6,
    damage=0.031 / 9,                       # 3.1% of output at 3 degrees, quadratic (DICE-2023's calibration)
    rho=0.015, eta=1.45,
    so2_0=73.5, so2_decline=0.02,           # Mt of SO2 a year, falling with clean-air policy and fossil use
)


class Dice:
    """A one-sector Ramsey economy (Part 20) with the climate fitted above: output A K^alpha L^(1-alpha) less
    abatement costs theta1 mu^theta2 and damages psi T^2; industrial emissions sigma Y (1 - mu); the carbon boxes,
    forcing and the two-layer temperature.  ``climate`` is the dict from ``fit_climate`` (its last year must be the
    year before ``start``); its boxes and temperatures are carried forward.  Welfare is the discounted sum of
    population-weighted CRRA utility of consumption per head."""

    def __init__(self, climate: dict, boxes0, temps0, **kw):
        p = dict(DICE_DEFAULTS)
        p.update(kw)
        self.p = p
        self.climate = climate
        self.boxes0 = np.array(boxes0, float)
        self.temps0 = tuple(temps0)
        n = p["years"]
        t = np.arange(n, dtype=float)
        self.t = t
        self.year = p["start"] + t
        self.L = p["pop_max"] - (p["pop_max"] - p["pop0"]) * np.exp(-p["pop_rate"] * t)
        gA = p["tfp_growth0"] * np.exp(-p["tfp_decline"] * t)
        self.A_growth = gA
        gs = -p["sigma_decline0"] * (1 - p["sigma_decline_rate"]) ** t
        K0 = p["capital_ratio"] * p["output0"]
        A0 = p["output0"] / (K0 ** p["alpha"] * p["pop0"] ** (1 - p["alpha"]))
        self.A = A0 * np.exp(np.concatenate([[0.0], np.cumsum(gA[:-1])]))
        self.K0 = K0
        sigma0 = p["emissions0"] / p["output0"]
        self.sigma = sigma0 * np.exp(np.concatenate([[0.0], np.cumsum(gs[:-1])]))
        self.land = p["land0"] * (1 - p["land_decline"]) ** t
        yr = self.year
        pb = np.where(yr <= 2050, p["backstop2050"] * (1 + p["backstop_fall_early"]) ** (2050 - yr),
                      p["backstop2050"] * (1 - p["backstop_fall_late"]) ** (yr - 2050))
        self.backstop = pb
        self.theta1 = pb * self.sigma / (1000.0 * p["theta2"])
        self.so2 = p["so2_0"] * (1 - p["so2_decline"]) ** t

    def run(self, mu, savings=None, pulse: float = 0.0, pulse_year: int | None = None) -> dict:
        p = self.p
        n = p["years"]
        mu = np.clip(np.broadcast_to(np.asarray(mu, float), (n,)), 0.0, 1.0)
        s = np.broadcast_to(np.asarray(p["savings"] if savings is None else savings, float), (n,))
        tau = CARBON_TAU * np.array([1.0, self.climate["speed"], self.climate["speed"], self.climate["speed"]])
        decay = np.exp(-1 / tau)
        lam = F2X / self.climate["ecs"]
        k_ghg, aer = self.climate["ghg_scale"], self.climate["aerosol"]
        b = self.boxes0.copy()
        T, D = self.temps0
        K = self.K0
        out = {k: np.zeros(n) for k in ("Y", "Ygross", "C", "c", "K", "E", "Eind", "ppm", "T", "damage",
                                         "abate", "mu")}
        for i in range(n):
            Yg = self.A[i] * K ** p["alpha"] * self.L[i] ** (1 - p["alpha"])
            Om = p["damage"] * T ** 2
            Lam = self.theta1[i] * mu[i] ** p["theta2"]
            Y = Yg * (1 - Om) * (1 - Lam)
            Eind = self.sigma[i] * Yg * (1 - mu[i])
            E = Eind + self.land[i] * (1 - mu[i])
            if pulse and self.year[i] == (pulse_year or p["start"]):
                E = E + pulse
            C = (1 - s[i]) * Y
            out["Y"][i], out["Ygross"][i], out["C"][i], out["c"][i] = Y, Yg, C, C / self.L[i]
            out["K"][i], out["E"][i], out["Eind"][i] = K, E, Eind
            out["damage"][i], out["abate"][i], out["mu"][i] = Om, Lam, mu[i]
            b = b * decay + CARBON_A * E * GTC_PER_GTCO2
            ppm = PREINDUSTRIAL_PPM + b.sum() * PPM_PER_GTC
            F = k_ghg * 5.35 * np.log(ppm / PREINDUSTRIAL_PPM) - aer * self.so2[i] * (1 - mu[i]) / 100.0
            T, D = T + (F - lam * T - 0.73 * (T - D)) / 7.3, D + 0.73 * (T - D) / 106.0
            out["ppm"][i], out["T"][i] = ppm, T
            K = (1 - p["depreciation"]) * K + s[i] * Y
        out["year"] = self.year
        return out

    def welfare(self, run: dict, rho=None, eta=None) -> float:
        rho = self.p["rho"] if rho is None else rho
        eta = self.p["eta"] if eta is None else eta
        c = run["c"]
        u = np.log(c) if abs(eta - 1) < 1e-9 else (c ** (1 - eta) - 1) / (1 - eta)
        return float(np.sum(self.L * u * (1 + rho) ** (-self.t)))

    def mu_path(self, nodes) -> np.ndarray:
        """Control rates from values at 2025, 2030, ..., interpolated linearly; 1 after the last node."""
        nodes = np.clip(np.asarray(nodes, float), 0, 1)
        ny = self.p["start"] + 5 * np.arange(len(nodes))
        mu = np.interp(self.year, ny, nodes)
        mu[self.year > ny[-1]] = np.maximum(nodes[-1], 1.0)
        return mu

    def optimize(self, rho=None, eta=None, n_nodes: int = 36, first: float = 0.05) -> dict:
        """The control path that maximizes welfare (savings held fixed), with this year's rate fixed at ``first``."""
        def neg(x):
            mu = self.mu_path(np.concatenate([[first], x]))
            return -self.welfare(self.run(mu), rho, eta)

        x0 = np.linspace(0.15, 1.0, n_nodes - 1)
        r = minimize(neg, x0, method="L-BFGS-B", bounds=[(0, 1)] * (n_nodes - 1),
                     options={"maxiter": 400})
        mu = self.mu_path(np.concatenate([[first], r.x]))
        return {"mu": mu, "run": self.run(mu), "welfare": -r.fun}

    def scc(self, mu, rho=None, eta=None, rates=(), pulse: float = 1.0) -> dict:
        """The social cost of carbon for a pulse in the first year: the change in consumption it causes, year by
        year, discounted by the Ramsey rule (marginal utility, from rho and eta) and at each constant rate in
        ``rates``.  Dollars (of 2019) per tonne of CO2."""
        rho = self.p["rho"] if rho is None else rho
        eta = self.p["eta"] if eta is None else eta
        base = self.run(mu)
        bumped = self.run(mu, pulse=pulse)
        dC = bumped["C"] - base["C"]                      # trillions of dollars a year
        c = base["c"]
        ramsey = (1 + rho) ** (-self.t) * (c / c[0]) ** (-eta)
        per_t = 1e12 / (pulse * 1e9)
        out = {"ramsey": float(-np.sum(dC * ramsey) * per_t), "dC_per_t": (-dC * per_t).tolist(),
               "c": c.tolist(), "year": self.year.tolist()}
        for r in rates:
            out[f"r{r:g}"] = float(-np.sum(dC * (1 + r) ** (-self.t)) * per_t)
        return out


# ---------------------------------------------------------------------------------------------------------------
# fat tails


def tail_losses(truncations, median: float = 3.0, spread: float = 0.25, df: float = 2.0, eta: float = 2.0,
                n: int = 200000, seed: int = 0) -> dict:
    """Weitzman's point with numbers.  The warming from doubled CO2 is uncertain: thin-tailed (log-normal around
    ``median``) or fat-tailed (a Student t with ``df`` degrees of freedom on its logarithm, same median and
    scale).  Damages are quadratic as in DICE below about 4 degrees and steepen sharply above 6.  For each upper
    truncation of the warming, the certainty-equivalent loss of consumption for an investor with relative risk
    aversion ``eta``: thin tails settle down; fat tails keep growing as the truncation is raised."""
    rng = np.random.default_rng(seed)
    z_thin = rng.standard_normal(n)
    z_fat = rng.standard_t(df, n)
    out = {"truncation": list(map(float, truncations)), "thin": [], "fat": [], "p_above6_thin": 0.0,
           "p_above6_fat": 0.0}

    def omega(T):
        return 1 - 1 / (1 + (0.031 / 9) * T ** 2 + (T / 6.5) ** 7)

    for name, z in (("thin", z_thin), ("fat", z_fat)):
        T = median * np.exp(spread * z)
        out[f"p_above6_{name}"] = float(np.mean(T > 6))
        for cap in truncations:
            Tc = np.minimum(T, cap)
            cons = 1 - omega(Tc)
            ce = np.mean(cons ** (1 - eta)) ** (1 / (1 - eta))
            out[name].append(float(1 - ce))
    return out


# ---------------------------------------------------------------------------------------------------------------
# climate clubs


def club(n: int = 15, cost: float = 0.01, damage: float = 0.03, tariff: float = 0.0, exports: float = 0.2,
         size_sd: float = 0.8, spread: float = 0.5, seed: int = 0) -> dict:
    """A toy of Nordhaus's climate club, in shares of each country's own output.  Countries of different sizes
    (shares of world output w) choose to abate, which costs about ``cost`` (it varies by country, with ``spread``);
    every country gains about ``damage`` (also varying) x the share of
    world output that abates (the damage avoided); members charge non-members a penalty tariff on their exports,
    which costs a non-member ``tariff`` x ``exports`` x the club's share of world output.  Starting from everyone in,
    countries leave (or rejoin) while it pays them; returns the stable club.  Without a tariff a country leaves
    whenever its own share of the benefit, damage x w, is below the cost: free riding unravels the club."""
    rng = np.random.default_rng(seed)
    w = np.exp(size_sd * rng.standard_normal(n))
    w = w / w.sum()
    costs = cost * np.exp(spread * rng.standard_normal(n) - spread ** 2 / 2)
    damages = damage * np.exp(spread * rng.standard_normal(n) - spread ** 2 / 2)
    inside = np.ones(n, bool)

    def payoff(i, ins):
        A = float(np.sum(w[ins]))
        v = damages[i] * A
        if ins[i]:
            v -= costs[i]
        else:
            v -= tariff * exports * A
        return v

    for _ in range(10 * n):
        changed = False
        for i in np.argsort(w):
            trial = inside.copy()
            trial[i] = not inside[i]
            if payoff(i, trial) > payoff(i, inside) + 1e-12:
                inside = trial
                changed = True
                break
        if not changed:
            break
    return {"members": int(inside.sum()), "abatement": float(np.sum(w[inside])), "inside": inside.tolist(),
            "size": w.tolist()}


# ---------------------------------------------------------------------------------------------------------------
# learning and directed technical change


def learning_curve(cumulative, price) -> dict:
    """Wright's law: log price = a + b log cumulative output.  The learning rate is the fall in price with each
    doubling of cumulative output, 1 - 2^b."""
    x, y = np.log(np.asarray(cumulative, float)), np.log(np.asarray(price, float))
    b, a = np.polyfit(x, y, 1)
    e = y - (a + b * x)
    se = float(np.sqrt(np.sum(e ** 2) / (len(x) - 2) / np.sum((x - x.mean()) ** 2)))
    return {"b": float(b), "a": float(a), "se": se, "learning_rate": float(1 - 2 ** b),
            "fit": np.exp(a + b * x).tolist()}


def directed_change(years: int = 150, eps: float = 3.0, gamma: float = 0.02, A_clean0: float = 0.6,
                    A_dirty0: float = 1.0, tax: float = 0.0, subsidy: float = 0.0, policy_years: int = 150,
                    persistent: bool = True) -> dict:
    """A toy after Acemoglu, Aghion, Bursztyn and Hemous (2012).  Clean and dirty inputs substitute with elasticity
    ``eps``; scientists go to whichever sector promises more profit, which (with eps > 1) is the sector already
    ahead, scaled by a carbon tax on dirty input and a subsidy to clean research while policy lasts.  Productivity
    grows in the sector that gets the scientists.  Returns productivities, the clean share of production and the
    research share."""
    Ac, Ad = A_clean0, A_dirty0
    phi = eps - 1
    out = {"t": [], "clean_share": [], "research_clean": []}
    for t in range(years):
        on = t < policy_years
        tx, sb = (tax, subsidy) if on else (0.0, 0.0)
        # profits from improving each sector, relative: market size and price effects summarized by A^(eps-1)
        prof_c = (1 + sb) * Ac ** phi
        prof_d = (1 - tx) ** eps * Ad ** phi
        s_c = 1.0 if prof_c > prof_d else 0.0
        Ac *= 1 + gamma * s_c
        Ad *= 1 + gamma * (1 - s_c)
        # clean share of production at relative price including the tax
        rc = Ac ** phi / (Ac ** phi + ((1 - tx) * Ad) ** phi)
        out["t"].append(t)
        out["clean_share"].append(float(rc))
        out["research_clean"].append(s_c)
    return out


# ---------------------------------------------------------------------------------------------------------------
# damages measured: temperature and growth in a panel


def temperature_growth(codes, years, temp, growth, trends: int = 1, poor=None) -> dict:
    """Burke, Hsiang and Miguel's regression: growth of GDP per head on temperature and its square, with country and
    year fixed effects and country-specific time trends (``trends`` = 1 linear, 2 adds quadratic).  Standard errors
    are clustered by country.  With ``poor`` (a boolean per observation), also a Dell, Jones and Olken style
    regression of growth on temperature and temperature x poor, with country and year effects.  Returns the
    coefficients, the optimum temperature and the response curve."""
    codes = np.asarray(codes)
    years = np.asarray(years, int)
    T = np.asarray(temp, float)
    g = np.asarray(growth, float)
    uc, ci = np.unique(codes, return_inverse=True)
    uy, yi = np.unique(years, return_inverse=True)
    nC, nY, n = len(uc), len(uy), len(g)
    tt = (years - years.mean()) / 10.0

    def design(cols):
        X = [np.column_stack(cols)]
        Dc = np.zeros((n, nC))
        Dc[np.arange(n), ci] = 1.0
        X.append(Dc)
        Dy = np.zeros((n, nY - 1))
        m = yi > 0
        Dy[np.arange(n)[m], yi[m] - 1] = 1.0
        X.append(Dy)
        for d in range(1, trends + 1):
            X.append(Dc * (tt ** d)[:, None])
        return np.hstack(X)

    def ols_cluster(X, k):
        XtX_inv = np.linalg.pinv(X.T @ X)
        b = XtX_inv @ X.T @ g
        e = g - X @ b
        meat = np.zeros((X.shape[1], X.shape[1]))
        for c in range(nC):
            s = ci == c
            u = X[s].T @ e[s]
            meat += np.outer(u, u)
        V = XtX_inv @ meat @ XtX_inv * nC / (nC - 1)
        return b[:k], V[:k, :k]

    b, V = ols_cluster(design([T, T ** 2]), 2)
    opt = -b[0] / (2 * b[1]) if b[1] < 0 else float("nan")
    grid = np.linspace(-5, 30, 141)
    resp = b[0] * (grid - opt) + b[1] * (grid ** 2 - opt ** 2)
    out = {"b1": float(b[0]), "b2": float(b[1]), "se1": float(np.sqrt(V[0, 0])), "se2": float(np.sqrt(V[1, 1])),
           "optimum": float(opt), "grid": grid.tolist(), "response": resp.tolist(), "n": int(n),
           "countries": int(nC), "years": [int(uy[0]), int(uy[-1])]}
    if poor is not None:
        P = np.asarray(poor, float)
        b2, V2 = ols_cluster(design([T, T * P]), 2)
        out["djo_rich"] = float(b2[0])
        out["djo_poor"] = float(b2[0] + b2[1])
        out["djo_poor_se"] = float(np.sqrt(V2[0, 0] + V2[1, 1] + 2 * V2[0, 1]))
        out["djo_rich_se"] = float(np.sqrt(V2[0, 0]))
    return out


# ---------------------------------------------------------------------------------------------------------------
# electricity: the merit order


def merit_order(capacity, cost, demand) -> dict:
    """Plants offer their capacity at marginal cost; the price is the cost of the last plant needed.  ``demand`` is
    a sequence of (inelastic) loads; returns the price at each load, and the supply step curve."""
    order = np.argsort(cost)
    cap, mc = np.asarray(capacity, float)[order], np.asarray(cost, float)[order]
    cum = np.cumsum(cap)
    prices = []
    for d in np.asarray(demand, float):
        k = np.searchsorted(cum, d - 1e-9)
        prices.append(float(mc[min(k, len(mc) - 1)]) if k < len(mc) else float("inf"))
    return {"cum": cum.tolist(), "cost": mc.tolist(), "order": order.tolist(), "price": prices}


def withholding(capacity, cost, owner, firm: int, demand: float, cap_price: float = 1000.0, steps: int = 41) -> dict:
    """One firm considers holding back some of its capacity at a given load.  Holding back pushes the market up the
    merit order to a costlier plant; the firm earns the higher price on what it still sells.  Returns its profit
    at each amount withheld and the best amount."""
    capacity, cost, owner = np.asarray(capacity, float), np.asarray(cost, float), np.asarray(owner)
    own = owner == firm
    own_cap = capacity[own].sum()
    held, profit, price = [], [], []
    for w in np.linspace(0, own_cap, steps):
        cap = capacity.copy()
        # withhold from the firm's costliest plants first
        rest = w
        for i in np.argsort(-cost):
            if own[i] and rest > 0:
                cut = min(cap[i], rest)
                cap[i] -= cut
                rest -= cut
        mo = merit_order(cap, cost, [demand])
        p = min(mo["price"][0], cap_price)
        # dispatch: cheapest first up to demand
        order = np.argsort(cost)
        left, prof = demand, 0.0
        for i in order:
            q = min(cap[i], max(left, 0.0))
            left -= q
            if own[i]:
                prof += (p - cost[i]) * q
        held.append(float(w))
        profit.append(float(prof))
        price.append(float(p))
    k = int(np.argmax(profit))
    return {"held": held, "profit": profit, "price": price, "best": held[k], "best_price": price[k],
            "best_profit": profit[k], "profit_none": profit[0], "price_none": price[0]}

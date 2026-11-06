"""Theories and reality, made computable (Part 18): the flagpole and its shadow, statistical relevance, a toy of
anomaly and revolution (an analogy, not a model of history), the no-miracles argument and its base rate, the
pessimistic meta-induction as data, Fresnel's equations surviving into Maxwell's theory, empirically equivalent
mechanics under a Galilean boost, the 2D Ising model with block-spin renormalization and Onsager's exact
magnetization, a miniature BACON rediscovering Kepler's third law, and inductive risk as a decision.

    from explainer.philosophy.reasoner import science as Sc
    Sc.ising_sw(81, 2.269, 300)         # a Swendsen--Wang sample of the 2D Ising model
    Sc.rg_flow()                        # block-spin coarse-graining below, at and above the critical point
    Sc.no_miracles(0.01)                # P(true | successful) when few candidate theories are true
    Sc.bacon(Sc.PLANETS)                # finds a^3 / T^2 constant
"""

from __future__ import annotations

import itertools
import math
import random

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

from explainer.philosophy.reasoner import prop

TC = 2 / math.log(1 + math.sqrt(2))      # Onsager's critical temperature, J = k = 1: 2.269...


# ---------------------------------------------------------------------------
# Verificationism: Church's (1949) trivialization of Ayer's criterion
# ---------------------------------------------------------------------------
def church_ayer() -> dict:
    """Ayer (1946): a sentence is directly verifiable if, with some observation sentences, it entails an
    observation sentence they do not entail alone; indirectly verifiable if, with directly verifiable premises, it
    entails a directly verifiable sentence they do not entail alone. Church: take independent observation sentences
    o1, o2, o3 and ANY sentence s. D = (~o1 & o2) | (o3 & ~s) is directly verifiable (with o1 it entails o3), and s
    with D entails o2, which D alone does not entail. So every s is verifiable. Each step checked by truth table."""
    D = "(~o1 & o2) | (o3 & ~s)"
    steps = [
        {"claim": "D, o1 |= o3", "ok": prop.entails([prop.parse(D), prop.parse("o1")], prop.parse("o3"))[0]},
        {"claim": "o1 alone does not entail o3", "ok": not prop.entails([prop.parse("o1")], prop.parse("o3"))[0]},
        {"claim": "s, D |= o2", "ok": prop.entails([prop.parse("s"), prop.parse(D)], prop.parse("o2"))[0]},
        {"claim": "D alone does not entail o2", "ok": not prop.entails([prop.parse(D)], prop.parse("o2"))[0]},
    ]
    return {"D": D, "steps": steps, "trivial": all(x["ok"] for x in steps)}


# ---------------------------------------------------------------------------
# Explanation: the flagpole, and statistical relevance
# ---------------------------------------------------------------------------
def flagpole(height: float = 10.0, elevation_deg: float = 37.0) -> dict:
    """Bromberger's flagpole: the same law (tan of the sun's elevation = height / shadow) derives the shadow from the
    height, and the height from the shadow. Both are D-N 'explanations'; only one explains."""
    t = math.tan(math.radians(elevation_deg))
    shadow = height / t
    back = shadow * t
    return {"height": height, "elevation": elevation_deg, "shadow": shadow, "height_from_shadow": back}


def moon_test() -> dict:
    """Newton's moon test, the paradigm of unification: if the force that drops an apple weakens as 1/r^2, the Moon,
    60 Earth radii away, should fall toward the Earth with g / 3600. Its observed centripetal acceleration agrees."""
    g = 9.81
    R = 6.371e6
    r = 3.844e8
    T = 27.32 * 86400
    a_moon = 4 * math.pi ** 2 * r / T ** 2
    predicted = g * (R / r) ** 2
    return {"g": g, "ratio": r / R, "a_moon": a_moon, "predicted": predicted, "agreement": a_moon / predicted}


def salmon_relevance() -> dict:
    """Salmon's statistical relevance: a factor explains only if it changes the probability. Men who take birth-
    control pills do not get pregnant, but the pill is irrelevant; hexed salt dissolves, but the hex is irrelevant.
    Illustrative frequencies: (pregnant | man, pill) = (pregnant | man, no pill) = 0; (pregnant | woman, no pill)
    = 0.2, (pregnant | woman, pill) = 0.01."""
    cells = {("man", "pill"): 0.0, ("man", "no pill"): 0.0, ("woman", "pill"): 0.01, ("woman", "no pill"): 0.2}
    rel = {who: abs(cells[(who, "pill")] - cells[(who, "no pill")]) > 0 for who in ("man", "woman")}
    salt = {"hexed": 1.0, "unhexed": 1.0}
    return {"cells": {f"{a}|{b}": v for (a, b), v in cells.items()}, "relevant": rel,
            "salt": salt, "hex_relevant": salt["hexed"] != salt["unhexed"]}


# ---------------------------------------------------------------------------
# Kuhn: anomalies and a revolution (analogy)
# ---------------------------------------------------------------------------
def kuhn_toy(n: int = 200, years: int = 120, anomaly_rate: float = 0.4, seed: int = 1962) -> dict:
    """An analogy, not history: n scientists work in paradigm A. Anomalies arrive at random (Poisson). Each
    scientist has a tolerance for anomalies (gamma, mean 24) and a social threshold: the share of colleagues who
    must already work in B before she will (uniform up to one half; a few pioneers need none). Granovetter's
    threshold model: the anomalies accumulate steadily, the switch comes as a cascade, and holdouts linger."""
    rng = np.random.default_rng(seed)
    tol = rng.gamma(8.0, 3.0, n)
    social = rng.uniform(0.0, 0.5, n)
    social[rng.random(n) < 0.05] = 0.0
    inB = np.zeros(n, bool)
    anomalies, share, cum = [], [], 0
    for _ in range(years):
        cum += rng.poisson(anomaly_rate)
        for _ in range(60):
            new = inB | ((cum > tol) & (inB.mean() >= social))
            if (new == inB).all():
                break
            inB = new
        anomalies.append(int(cum))
        share.append(float(inB.mean()))
    s = np.array(share)
    jumps = np.diff(np.r_[0.0, s])
    return {"n": n, "anomalies": anomalies, "share_B": share, "t10": int(np.argmax(s >= 0.1)),
            "t90": int(np.argmax(s >= 0.9)) if (s >= 0.9).any() else None, "jump_year": int(np.argmax(jumps)),
            "jump": float(jumps.max())}


# ---------------------------------------------------------------------------
# Realism: no miracles, the base rate, and the meta-induction
# ---------------------------------------------------------------------------
def no_miracles(base_rate: float, p_success_true: float = 0.95, p_success_false: float = 0.05) -> float:
    """P(theory approximately true | it is predictively successful), by Bayes. Putnam's argument assumes the
    likelihoods; Magnus and Callender (2004) point out that the answer depends on the base rate of truth among
    candidate theories, which no one knows."""
    num = p_success_true * base_rate
    return num / (num + p_success_false * (1 - base_rate))


def no_miracles_table(rates=(0.5, 0.2, 0.1, 0.05, 0.01, 0.001)) -> list[dict]:
    return [{"base_rate": r, "posterior": no_miracles(r)} for r in rates]


LAUDAN = [
    ("crystalline spheres", "astronomy", -350, 1600), ("humoral medicine", "medicine", -400, 1850),
    ("effluvial electricity", "physics", 1600, 1750), ("catastrophist geology", "geology", 1750, 1840),
    ("phlogiston", "chemistry", 1700, 1785), ("caloric", "heat", 1780, 1850),
    ("vibratory heat", "heat", 1650, 1800), ("vital force", "physiology", 1750, 1850),
    ("electromagnetic aether", "physics", 1850, 1905), ("optical aether", "optics", 1800, 1905),
    ("circular inertia", "mechanics", 1600, 1690), ("spontaneous generation", "biology", -350, 1860),
]


def meta_induction() -> dict:
    """Laudan's (1981) list of theories that were successful and are now rejected, with rough dates of currency,
    and the naive inductive rate it suggests. The rate is the argument's weakest point: the list is selected."""
    spans = [b - a for _, _, a, b in LAUDAN]
    return {"theories": [{"name": n, "field": f, "from": a, "to": b} for n, f, a, b in LAUDAN],
            "count": len(LAUDAN), "median_span": float(np.median(spans))}


# ---------------------------------------------------------------------------
# Structural realism: Fresnel's equations
# ---------------------------------------------------------------------------
def fresnel(n1: float = 1.0, n2: float = 1.5, points: int = 91) -> dict:
    """Fresnel's (1823) reflection coefficients, derived from an elastic aether, and re-derived by Maxwell's
    electromagnetism with the aether gone: the structure survives the change of ontology. Reflectances R_s, R_p
    against the angle of incidence; Brewster's angle where R_p = 0."""
    out = []
    for k in range(points):
        th = math.radians(k * 90 / (points - 1))
        s = n1 / n2 * math.sin(th)
        if s >= 1:
            out.append([k * 90 / (points - 1), 1.0, 1.0])
            continue
        tt = math.asin(s)
        ci, ct = math.cos(th), math.cos(tt)
        rs = (n1 * ci - n2 * ct) / (n1 * ci + n2 * ct)
        rp = (n2 * ci - n1 * ct) / (n2 * ci + n1 * ct)
        out.append([k * 90 / (points - 1), rs * rs, rp * rp])
    brewster = math.degrees(math.atan(n2 / n1))
    return {"n1": n1, "n2": n2, "curve": out, "brewster": brewster, "normal": ((n1 - n2) / (n1 + n2)) ** 2}


# ---------------------------------------------------------------------------
# Underdetermination: Newton's absolute velocity
# ---------------------------------------------------------------------------
def galilean_twins(v: float = 0.3, steps: int = 2500, dt: float = 0.01) -> dict:
    """Two Newtonian worlds: a two-body orbit whose centre of mass is at absolute rest, and the same orbit with the
    whole system moving at v. Every relative quantity (the separation, the observed angle) is identical at every
    step: no observation distinguishes absolute rest from uniform motion, though the theories differ."""
    def run(boost):
        x1, x2 = np.array([1.0, 0.0]), np.array([-1.0, 0.0])
        v1, v2 = np.array([boost, 0.35]), np.array([boost, -0.35])
        seps, abs1 = [], []
        for _ in range(steps):
            r = x2 - x1
            f = r / (np.linalg.norm(r) ** 3)
            v1 = v1 + f * dt
            v2 = v2 - f * dt
            x1 = x1 + v1 * dt
            x2 = x2 + v2 * dt
            seps.append(float(np.linalg.norm(x2 - x1)))
            abs1.append(x1.tolist())
        return seps, abs1
    s0, a0 = run(0.0)
    s1, a1 = run(v)
    return {"v": v, "max_sep_diff": float(max(abs(a - b) for a, b in zip(s0, s1))), "sep": s0[::20],
            "path_rest": a0[::20], "path_moving": a1[::20]}


# ---------------------------------------------------------------------------
# Emergence and universality: the 2D Ising model
# ---------------------------------------------------------------------------
def ising_sw(L: int, T: float, steps: int, seed: int = 0, start=None) -> np.ndarray:
    """Swendsen--Wang cluster updates for the 2D Ising model (J = 1, periodic): bond equal neighbours with
    probability 1 - exp(-2/T), find clusters, flip each with probability 1/2."""
    rng = np.random.default_rng(seed)
    s = rng.choice([-1, 1], size=(L, L)) if start is None else start.copy()
    p = 1 - math.exp(-2 / T)
    idx = np.arange(L * L).reshape(L, L)
    right, down = np.roll(idx, -1, axis=1), np.roll(idx, -1, axis=0)
    for _ in range(steps):
        br = (s == np.roll(s, -1, axis=1)) & (rng.random((L, L)) < p)
        bd = (s == np.roll(s, -1, axis=0)) & (rng.random((L, L)) < p)
        rows = np.concatenate([idx[br], idx[bd]])
        cols = np.concatenate([right[br], down[bd]])
        g = coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(L * L, L * L))
        nc, lab = connected_components(g, directed=False)
        flip = rng.random(nc) < 0.5
        s = np.where(flip[lab].reshape(L, L), -s, s)
    return s


def block_spin(s: np.ndarray, b: int = 3) -> np.ndarray:
    """Kadanoff's block-spin step: replace each b x b block by the sign of its sum (b odd: no ties)."""
    L = s.shape[0] // b
    return np.sign(s[:L * b, :L * b].reshape(L, b, L, b).sum(axis=(1, 3))).astype(int)


def nn_corr(s: np.ndarray) -> float:
    return float((s * np.roll(s, 1, 0)).mean() + (s * np.roll(s, 1, 1)).mean()) / 2


def rg_flow(L: int = 243, temps=(2.0, TC, 2.6), steps: int = 400, seed: int = 1966) -> dict:
    """Sample at three temperatures and coarse-grain three times (243 -> 81 -> 27 -> 9). Below T_c the blocked
    lattices flow to order (correlation -> 1); above, to disorder (-> 0); at T_c the picture looks the same at
    every scale: the fixed point. Returns the lattices (as lists) and each level's nearest-neighbour correlation."""
    out = {}
    for i, T in enumerate(temps):
        start = np.ones((L, L), int) if T < TC else None
        s = ising_sw(L, T, steps, seed + i, start)
        levels, corr = [s], [nn_corr(s)]
        for _ in range(3):
            levels.append(block_spin(levels[-1]))
            corr.append(nn_corr(levels[-1]))
        out[f"{T:.3f}"] = {"T": T, "corr": corr, "levels": [lv.tolist() for lv in levels],
                           "m": float(abs(s.mean()))}
    return out


def onsager_m(T: float) -> float:
    """Onsager and Yang's exact spontaneous magnetization of the 2D Ising model: (1 - sinh(2/T)^-4)^(1/8)."""
    if T >= TC:
        return 0.0
    return (1 - math.sinh(2 / T) ** -4) ** 0.125


def magnetization_curve(L: int = 48, temps=None, steps: int = 300, burn: int = 100, seed: int = 1944) -> dict:
    """Simulated |m| against Onsager's exact curve; near T_c the exponent beta = 1/8 governs the drop. The liquid-
    gas critical point in two dimensions has the same exponent: universality."""
    temps = temps or [1.5 + 0.1 * k for k in range(17)]
    sim = []
    for i, T in enumerate(temps):
        s = np.ones((L, L), int)
        rng_seed = seed + i
        ms = []
        s = ising_sw(L, T, burn, rng_seed, s)
        for k in range(steps // 10):
            s = ising_sw(L, T, 10, rng_seed + 1000 + k, s)
            ms.append(abs(s.mean()))
        sim.append([T, float(np.mean(ms))])
    exact = [[1.5 + 0.01 * k, onsager_m(1.5 + 0.01 * k)] for k in range(161)]
    return {"L": L, "sim": sim, "exact": exact, "Tc": TC}


# ---------------------------------------------------------------------------
# AI scientists: a miniature BACON
# ---------------------------------------------------------------------------
PLANETS = [("Mercury", 0.387, 0.241), ("Venus", 0.723, 0.615), ("Earth", 1.000, 1.000), ("Mars", 1.524, 1.881),
           ("Jupiter", 5.203, 11.862), ("Saturn", 9.537, 29.457)]


def bacon(data=PLANETS, max_power: int = 3, tol: float = 0.01) -> dict:
    """Langley's BACON (1978), in miniature: search the products a^i T^j (small integer powers) for one that is
    constant across the data, and report the simplest. Returns every term tried with its coefficient of variation."""
    a = np.array([d[1] for d in data])
    t = np.array([d[2] for d in data])
    tried = []
    for i, j in itertools.product(range(-max_power, max_power + 1), repeat=2):
        if i == 0 and j == 0:
            continue
        v = a ** i * t ** j
        cv = float(np.std(v) / abs(np.mean(v)))
        tried.append({"i": i, "j": j, "cv": cv, "mean": float(np.mean(v))})
    found = sorted([x for x in tried if x["cv"] < tol], key=lambda x: (abs(x["i"]) + abs(x["j"]), x["cv"]))
    return {"tried": len(tried), "found": found[:2], "best_cv_other": min(x["cv"] for x in tried if x["cv"] >= tol)}


# ---------------------------------------------------------------------------
# Values in science: inductive risk
# ---------------------------------------------------------------------------
def inductive_risk(cost_fp: float, cost_fn: float, prior: float = 0.3, separation: float = 1.5) -> dict:
    """Rudner (1953): accepting a hypothesis is a decision. A test statistic is N(0,1) if the chemical is safe and
    N(separation, 1) if it is toxic; we declare 'toxic' above a threshold c. The threshold minimizing expected loss
    depends on the costs of the two errors, which are value judgments."""
    def phi(x):
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    best = None
    curve = []
    for k in range(-200, 401):
        c = k / 100
        fp = (1 - phi(c)) * (1 - prior)
        fn = phi(c - separation) * prior
        loss = cost_fp * fp + cost_fn * fn
        curve.append([c, loss])
        if best is None or loss < best[1]:
            best = (c, loss)
    return {"cost_fp": cost_fp, "cost_fn": cost_fn, "threshold": best[0], "loss": best[1],
            "alpha": 1 - phi(best[0]), "power": 1 - phi(best[0] - separation), "curve": curve[::10]}


# ---------------------------------------------------------------------------
# Reduction: temperature as mean kinetic energy
# ---------------------------------------------------------------------------
def kinetic_temperature(T: float = 300.0, n: int = 100000, seed: int = 1857) -> dict:
    """Nagel's showcase reduction, run backwards: sample nitrogen molecules' velocities at temperature T (Maxwell--
    Boltzmann), then recover T from the bridge law <(1/2) m v^2> = (3/2) k T. Also the speed histogram."""
    k = 1.380649e-23
    m = 28.0134 * 1.66053907e-27
    rng = np.random.default_rng(seed)
    v = rng.normal(0, math.sqrt(k * T / m), (n, 3))
    speed = np.linalg.norm(v, axis=1)
    ke = 0.5 * m * (speed ** 2).mean()
    T_back = 2 * ke / (3 * k)
    hist, edges = np.histogram(speed, bins=40, range=(0, 1400))
    return {"T": T, "T_recovered": float(T_back), "rms": float(math.sqrt((speed ** 2).mean())),
            "mean_speed": float(speed.mean()), "hist": hist.tolist(), "edges": edges.tolist(), "n": n}


# ---------------------------------------------------------------------------
# Models and idealization: the small-angle pendulum
# ---------------------------------------------------------------------------
def pendulum_idealization(amplitudes=(5, 10, 20, 30, 45, 60, 90, 120, 150, 170)) -> list[dict]:
    """The idealized pendulum (sin x ~ x) has period 2 pi sqrt(L/g) at every amplitude. The exact period divides
    that by the arithmetic-geometric mean of 1 and cos(amplitude / 2). How false is the idealization, and where?"""
    def agm(a, b):
        for _ in range(60):
            a, b = (a + b) / 2, math.sqrt(a * b)
        return a
    return [{"amp": A, "ratio": 1 / agm(1.0, math.cos(math.radians(A) / 2))} for A in amplitudes]


# ---------------------------------------------------------------------------
# The Copernican revolution: two geometries, one sky
# ---------------------------------------------------------------------------
def copernicus(years: float = 4.0, steps: int = 400) -> dict:
    """Mars seen from the Earth. Heliocentric: both planets on circles about the Sun (radii 1 and 1.524 AU, periods 1
    and 1.881 years). Ptolemaic: Mars on an epicycle of radius 1 turning once a year, carried on a deferent of radius
    1.524 turning once in 1.881 years, about the Earth. The two give the same apparent longitude at every instant,
    including the retrograde loops. What Copernicus explains and Ptolemy must stipulate: the epicycle's one-year
    period, which in his system is the Earth's own orbit."""
    rm, Tm = 1.524, 1.881
    ts = np.linspace(0, years, steps)
    E = np.c_[np.cos(2 * np.pi * ts), np.sin(2 * np.pi * ts)]
    M = rm * np.c_[np.cos(2 * np.pi * ts / Tm), np.sin(2 * np.pi * ts / Tm)]
    helio = M - E
    deferent = rm * np.c_[np.cos(2 * np.pi * ts / Tm), np.sin(2 * np.pi * ts / Tm)]
    epicycle = -np.c_[np.cos(2 * np.pi * ts), np.sin(2 * np.pi * ts)]
    ptol = deferent + epicycle
    lon_h = np.unwrap(np.arctan2(helio[:, 1], helio[:, 0]))
    lon_p = np.unwrap(np.arctan2(ptol[:, 1], ptol[:, 0]))
    retro = np.diff(lon_h) < 0
    episodes = int(np.sum(np.diff(retro.astype(int)) == 1) + (1 if retro[0] else 0))
    return {"t": ts.round(4).tolist(), "lon_deg": np.degrees(lon_h).round(3).tolist(),
            "max_diff_deg": float(np.degrees(np.max(np.abs(lon_h - lon_p)))), "path": helio.round(4).tolist(),
            "retrograde_episodes": episodes, "Tm": Tm, "rm": rm}

"""Life, made computable (Part 19): the Price equation, checked on simulated populations; replicator dynamics on
the simplex; evolutionarily stable strategies and the hawk-dove game; Hamilton's rule, derived from Price and run;
multilevel selection as a Price decomposition, with Simpson's paradox; Paley against Darwin as likelihoods; the
genetic code's redundancy in bits; a parsimony tree; and Lenia, a continuous cellular automaton with gliding
creatures.

    from explainer.philosophy.reasoner import evo as Ev
    Ev.price_check(seed=1)                  # Delta zbar = cov(w, z) / wbar + E(w dz) / wbar, both sides computed
    Ev.replicator(A, x0, steps)             # trajectories of x_i' = x_i (f_i - fbar)
    Ev.hawk_dove(V=2, C=3)                  # the mixed ESS p* = V / C, and its stability
    Ev.lenia(steps=200)                     # an Orbium-like glider in Lenia
"""

from __future__ import annotations

import itertools
import math

import numpy as np


# ---------------------------------------------------------------------------
# The Price equation
# ---------------------------------------------------------------------------
def price_terms(z: np.ndarray, w: np.ndarray, z_off: np.ndarray) -> dict:
    """Price (1970): with parents' trait z_i, fitness w_i (number of offspring) and offspring mean trait z'_i,
    wbar * Delta zbar = cov(w, z) + E(w * (z' - z)). Covariances are population (not sample) covariances."""
    wbar = w.mean()
    zbar = z.mean()
    zbar_next = (w * z_off).sum() / w.sum()
    cov = ((w - wbar) * (z - zbar)).mean()
    trans = (w * (z_off - z)).mean()
    return {"wbar": float(wbar), "zbar": float(zbar), "zbar_next": float(zbar_next),
            "delta": float(zbar_next - zbar), "selection": float(cov / wbar), "transmission": float(trans / wbar)}


def price_check(n: int = 500, seed: int = 1970) -> dict:
    """A population in which taller birds leave more offspring, and offspring are slightly shorter than their
    parents (a transmission bias). Both sides of Price's identity, and the scatter of fitness against trait."""
    rng = np.random.default_rng(seed)
    z = rng.normal(10.0, 1.0, n)
    lam = np.exp(0.4 * (z - 10.0))
    w = rng.poisson(1.5 * lam).astype(float)
    z_off = z - 0.1 + rng.normal(0, 0.05, n)
    t = price_terms(z, w, z_off)
    t["identity_error"] = abs(t["delta"] - (t["selection"] + t["transmission"]))
    t["points"] = np.c_[z[:300], w[:300]].round(3).tolist()
    slope = float(np.cov(z, w, bias=True)[0, 1] / np.var(z))
    t["slope"] = slope
    return t


# ---------------------------------------------------------------------------
# Replicator dynamics and ESS
# ---------------------------------------------------------------------------
def replicator(A, x0, steps: int = 2000, dt: float = 0.01) -> list[list[float]]:
    """Taylor and Jonker (1978): x_i' = x_i ((A x)_i - x.A x), integrated with RK4 and renormalized."""
    A = np.array(A, float)
    x = np.array(x0, float)

    def f(x):
        fit = A @ x
        return x * (fit - x @ fit)
    out = [x.tolist()]
    for _ in range(steps):
        k1 = f(x)
        k2 = f(x + dt / 2 * k1)
        k3 = f(x + dt / 2 * k2)
        k4 = f(x + dt * k3)
        x = np.clip(x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4), 0, None)
        x = x / x.sum()
        out.append(x.tolist())
    return out


def hawk_dove(V: float = 2.0, C: float = 3.0) -> dict:
    """Maynard Smith and Price (1973): hawks fight (cost C to the loser), doves display. Payoffs H-H (V-C)/2, H-D V,
    D-H 0, D-D V/2. If C > V the ESS is mixed: play hawk with probability V/C. Checked: neither pure strategy can
    invade it, and the replicator dynamics converge to it from both sides."""
    A = np.array([[(V - C) / 2, V], [0.0, V / 2]])
    p = V / C if C > V else 1.0
    x = np.array([p, 1 - p])
    fit = A @ x
    invade = {}
    for name, y in (("hawk", np.array([1.0, 0.0])), ("dove", np.array([0.0, 1.0]))):
        # ESS second condition: when payoffs against x tie, x does better against y than y against itself
        first = float(y @ A @ x - x @ A @ x)
        second = float(x @ A @ y - y @ A @ y)
        invade[name] = {"against_ess_gap": first, "stability_margin": second}
    trajs = [[r[0] for r in replicator(A, [h, 1 - h], steps=1500)][::15] for h in (0.05, 0.95)]
    return {"V": V, "C": C, "p_star": p, "payoff_tie": float(fit[0] - fit[1]), "invasion": invade,
            "trajectories": trajs, "A": A.tolist()}


def rps(steps: int = 3000, eps: float = 0.0) -> dict:
    """Rock-paper-scissors on the simplex: with eps = 0 orbits are closed cycles around (1/3, 1/3, 1/3); with a
    small reward for ties (eps > 0) they spiral inward; with a penalty they spiral out to the boundary."""
    A = np.array([[eps, -1, 1], [1, eps, -1], [-1, 1, eps]], float)
    return {"eps": eps, "traj": replicator(A, [0.6, 0.25, 0.15], steps=steps, dt=0.01)[::6]}


# ---------------------------------------------------------------------------
# Kin selection: Hamilton's rule
# ---------------------------------------------------------------------------
def hamilton_sim(r: float, b: float, c: float, n_groups: int = 4000, gens: int = 60, seed: int = 1964) -> dict:
    """Pairs of relatives: with probability r a partner is a copy of the focal individual's type, otherwise drawn
    from the population. Altruists pay c and give b to the partner; baseline fitness 1. The frequency of altruism
    rises iff r b > c (Hamilton 1964), up to drift. Returns the trajectory."""
    rng = np.random.default_rng(seed)
    p = 0.2
    traj = [p]
    for _ in range(gens):
        focal = rng.random(n_groups) < p
        same = rng.random(n_groups) < r
        partner = np.where(same, focal, rng.random(n_groups) < p)
        w_f = 1 - c * focal + b * partner
        w_p = 1 - c * partner + b * focal
        types = np.r_[focal, partner]
        ws = np.r_[w_f, w_p]
        p = float((types * ws).sum() / ws.sum())
        p = min(max(p, 0.0), 1.0)
        traj.append(p)
    return {"r": r, "b": b, "c": c, "rb_minus_c": r * b - c, "traj": traj}


def hamilton_from_price(r: float, b: float, c: float, p: float = 0.3) -> dict:
    """Price's covariance for the pairing model above, exactly: cov(w, z) = p(1-p)(r b - c), so selection favours
    altruism iff r b > c. Computed by enumerating the four pair types."""
    cells = []
    for f, q in itertools.product((1, 0), (1, 0)):
        pf = p if f else 1 - p
        pq = (r if q == f else 0) + (1 - r) * (p if q else 1 - p)
        w = 1 - c * f + b * q
        cells.append((pf * pq, f, w))
    zbar = sum(pr * z for pr, z, _ in cells)
    wbar = sum(pr * w for pr, _, w in cells)
    cov = sum(pr * (z - zbar) * (w - wbar) for pr, z, w in cells)
    return {"cov": cov, "formula": p * (1 - p) * (r * b - c), "wbar": wbar}


# ---------------------------------------------------------------------------
# Levels of selection: the multilevel Price equation and Simpson's paradox
# ---------------------------------------------------------------------------
def multilevel(groups=((10, 2), (10, 8)), b: float = 0.5, c: float = 0.1) -> dict:
    """Groups of size n with k altruists. An altruist pays c; each member gets b times the share of altruists in
    the group. Within every group altruists do worse (Simpson), yet the global share of altruists can rise because
    altruist-rich groups grow. Price splits the change: between-group covariance + average within-group covariance.
    """
    rows = []
    for n, k in groups:
        share = k / n
        wa = 1 - c + b * share
        ws = 1 + b * share
        off_a, off_s = k * wa, (n - k) * ws
        rows.append({"n": n, "k": k, "share": share, "w_alt": wa, "w_self": ws, "off_alt": off_a, "off_self": off_s})
    N = sum(r["n"] for r in rows)
    p0 = sum(r["k"] for r in rows) / N
    off = sum(r["off_alt"] + r["off_self"] for r in rows)
    p1 = sum(r["off_alt"] for r in rows) / off
    # Price decomposition over groups: zbar_g = share, w_g = mean fitness of group
    wg = np.array([(r["off_alt"] + r["off_self"]) / r["n"] for r in rows])
    zg = np.array([r["share"] for r in rows])
    ng = np.array([r["n"] for r in rows], float)
    wbar = (ng * wg).sum() / ng.sum()
    between = float(((ng * (wg - wbar) * (zg - (ng * zg).sum() / ng.sum())).sum() / ng.sum()) / wbar)
    within = 0.0
    for r_, w_ in zip(rows, wg):
        # within-group covariance between being an altruist and fitness
        zz = np.r_[np.ones(r_["k"]), np.zeros(r_["n"] - r_["k"])]
        ww = np.r_[np.full(r_["k"], r_["w_alt"]), np.full(r_["n"] - r_["k"], r_["w_self"])]
        within += r_["n"] * float(((zz - zz.mean()) * (ww - ww.mean())).mean())
    within = within / ng.sum() / wbar
    return {"groups": rows, "p0": p0, "p1": p1, "delta": p1 - p0, "between": between, "within": within,
            "check": abs((p1 - p0) - (between + within))}


# ---------------------------------------------------------------------------
# Design or selection: likelihoods
# ---------------------------------------------------------------------------
def paley_likelihoods() -> dict:
    """Sober's reconstruction: compare P(observation | design) with P(observation | selection) for observations
    that discriminate. The vertebrate eye's blind spot and backward retina, the recurrent laryngeal nerve's detour
    (about 4.6 m in a giraffe for a 0.3 m direct route), shared pseudogenes in humans and chimpanzees: each is more
    probable on common descent and selection than on optimal design. Illustrative probabilities, labeled as such."""
    obs = [("backward retina, blind spot", 0.05, 0.5), ("laryngeal nerve's 4.6 m detour (giraffe)", 0.02, 0.6),
           ("broken vitamin-C gene shared with chimpanzees", 0.01, 0.7)]
    lr = 1.0
    rows = []
    for name, pd, ps in obs:
        lr *= ps / pd
        rows.append({"obs": name, "p_design": pd, "p_selection": ps, "ratio": ps / pd})
    return {"rows": rows, "combined_ratio": lr}


# ---------------------------------------------------------------------------
# Information in biology: the genetic code
# ---------------------------------------------------------------------------
CODE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M", "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T", "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*", "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K", "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W", "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R", "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}


def code_information() -> dict:
    """The standard genetic code: 64 codons, 20 amino acids and stop. A codon carries log2 64 = 6 bits of Shannon
    capacity; the output alphabet needs at most log2 21 = 4.39; with codons uniform, the amino-acid entropy is 4.22
    bits, so 1.78 bits per codon are redundancy. And the share of single-base mutations that are silent."""
    from collections import Counter
    cnt = Counter(CODE.values())
    H = -sum((k / 64) * math.log2(k / 64) for k in cnt.values())
    silent = total = 0
    for codon, aa in CODE.items():
        for i in range(3):
            for base in "TCAG":
                if base == codon[i]:
                    continue
                mut = codon[:i] + base + codon[i + 1:]
                total += 1
                silent += CODE[mut] == aa
    third = sum(1 for codon, aa in CODE.items() for base in "TCAG" if base != codon[2]
                and CODE[codon[:2] + base] == aa)
    return {"codons": 64, "outputs": len(cnt), "capacity": 6.0, "entropy": H, "redundancy": 6.0 - H,
            "silent_share": silent / total, "third_position_silent": third / (64 * 3),
            "degeneracy": dict(sorted(cnt.items(), key=lambda kv: -kv[1]))}


# ---------------------------------------------------------------------------
# Species and cladistics: a small parsimony tree
# ---------------------------------------------------------------------------
TAXA = {
    "lamprey": "00000000", "shark": "10000000", "salmon": "11000000", "frog": "11100000", "lizard": "11111000",
    "pigeon": "11111100", "mouse": "11110010", "chimp": "11110011",
}
CHARS = ["jaws", "bony skeleton", "four limbs", "amniotic egg", "diapsid skull", "feathers", "fur",
         "opposable thumb"]


def fitch_score(tree, seqs) -> int:
    """Fitch's small-parsimony count of character changes on a rooted binary tree (nested tuples of taxon names)."""
    total = 0
    L = len(next(iter(seqs.values())))
    for i in range(L):
        def rec(t):
            nonlocal total
            if isinstance(t, str):
                return {seqs[t][i]}
            a, b = rec(t[0]), rec(t[1])
            if a & b:
                return a & b
            total += 1
            return a | b
        rec(tree)
    return total


def _leaves(t):
    return [t] if isinstance(t, str) else _leaves(t[0]) + _leaves(t[1])


def parsimony_demo() -> dict:
    """The best tree for the character matrix against two alternatives, and where on the best tree each character
    arises: the smallest clade containing every taxon that has it. Birds sit with lizards (both diapsids), so
    `reptiles' without birds is not a clade."""
    good = ("lamprey", ("shark", ("salmon", ("frog", (("lizard", "pigeon"), ("mouse", "chimp"))))))
    alt1 = ("lamprey", ("shark", ("salmon", ("frog", (("lizard", "mouse"), ("pigeon", "chimp"))))))
    alt2 = ("lamprey", (("shark", "chimp"), ("salmon", ("frog", (("lizard", "pigeon"), "mouse")))))
    clades = []

    def walk(t):
        if not isinstance(t, str):
            clades.append(sorted(_leaves(t)))
            walk(t[0])
            walk(t[1])
        else:
            clades.append([t])

    walk(good)
    gains = {}
    for i, c in enumerate(CHARS):
        have = {k for k, v in TAXA.items() if v[i] == "1"}
        gains[c] = min((cl for cl in clades if have <= set(cl)), key=len)
    return {"chars": CHARS, "taxa": TAXA, "tree": good, "gains": gains,
            "scores": {"nested": fitch_score(good, TAXA), "alt1": fitch_score(alt1, TAXA),
                       "alt2": fitch_score(alt2, TAXA)},
            "min_possible": len(CHARS)}


# ---------------------------------------------------------------------------
# Artificial life: Lenia
# ---------------------------------------------------------------------------
def lenia_kernel(R: int, size: int) -> np.ndarray:
    y, x = np.ogrid[-size // 2: size // 2, -size // 2: size // 2]
    r = np.sqrt(x * x + y * y) / R
    k = np.where(r < 1, np.exp(4 - 1 / np.clip(r * (1 - r), 1e-9, None)), 0.0)
    return k / k.sum()


def lenia(size: int = 128, R: int = 13, T: float = 10.0, mu: float = 0.15, sigma: float = 0.015,
          steps: int = 300, seed: int = 2019, init=None, frames: int = 6, movie=None) -> dict:
    """Chan's Lenia (2019): A <- clip(A + (1/T) G(K * A), 0, 1), with a ring kernel K of radius R and a Gaussian
    growth G(u) = 2 exp(-(u - mu)^2 / (2 sigma^2)) - 1. FFT convolution on a torus. Returns snapshots, total mass,
    and the centre of mass over time; ``movie = (start, every, n)`` also records n frames as bytes (0-255)."""
    rng = np.random.default_rng(seed)
    K = np.fft.fft2(np.fft.ifftshift(lenia_kernel(R, size)))
    if init is None:
        A = np.zeros((size, size))
        c = size // 2
        A[c - 10:c + 10, c - 10:c + 10] = rng.random((20, 20))
    else:
        A = init.copy()
    snaps, mass, com, film = [], [], [], []
    every = max(1, steps // (frames - 1))
    ys, xs = np.mgrid[0:size, 0:size]
    for t in range(steps + 1):
        if t % every == 0 and len(snaps) < frames:
            snaps.append(A.round(3).tolist())
        if movie and t >= movie[0] and (t - movie[0]) % movie[1] == 0 and len(film) < movie[2]:
            film.append((A * 255).round().astype(int).tolist())
        m = A.sum()
        mass.append(float(m))
        if m > 0:
            ang_x = np.angle((A * np.exp(2j * np.pi * xs / size)).sum()) % (2 * np.pi) / (2 * np.pi) * size
            ang_y = np.angle((A * np.exp(2j * np.pi * ys / size)).sum()) % (2 * np.pi) / (2 * np.pi) * size
            com.append([float(ang_x), float(ang_y)])
        U = np.real(np.fft.ifft2(K * np.fft.fft2(A)))
        G = 2 * np.exp(-((U - mu) ** 2) / (2 * sigma ** 2)) - 1
        A = np.clip(A + G / T, 0, 1)
    out = {"snaps": snaps, "mass": mass, "com": com, "params": {"R": R, "T": T, "mu": mu, "sigma": sigma}}
    if movie:
        out["movie"] = film
    return out


# Found by the Reasoner's own random search over growth parameters and noise patches (400 trials): from a disc of
# random noise, one crescent-shaped creature condenses, keeps a constant mass of about 47, and glides at about half a
# cell per step, an Orbium-like soliton.
GLIDER = {"size": 96, "R": 10, "mu": 0.16318870907354005, "sigma": 0.01802950850457656,
          "amp": 0.8686347786778776, "radius": 18, "seed": 43}


def lenia_glider(steps: int = 1500, frames: int = 7, movie=None) -> dict:
    g = GLIDER
    rng = np.random.default_rng(g["seed"])
    c = g["size"] // 2
    yy, xx = np.mgrid[0:g["size"], 0:g["size"]]
    A = g["amp"] * rng.random((g["size"], g["size"])) * (np.hypot(yy - c, xx - c) < g["radius"])
    d = lenia(size=g["size"], R=g["R"], mu=g["mu"], sigma=g["sigma"], steps=steps, init=A, frames=frames,
              movie=movie)
    m = np.array(d["mass"])
    com = np.array(d["com"])
    step = np.diff(com[300:], axis=0)
    step = (step + g["size"] / 2) % g["size"] - g["size"] / 2
    d["speed"] = float(np.linalg.norm(step, axis=1).mean())
    d["mass_after"] = float(m[300:].mean())
    d["mass_spread"] = float(m[300:].std() / m[300:].mean())
    d["mass_start"] = float(m[0])
    return d


# ---------------------------------------------------------------------------
# Lewontin's recipe: variation, heredity, differential fitness
# ---------------------------------------------------------------------------
def breeder(h2_values=(0.0, 0.5, 0.9), n: int = 4000, gens: int = 10, keep: float = 0.3, seed: int = 1970) -> dict:
    """Truncation selection on a trait z = genetic + environmental, with heritability h^2 = var(G) / var(z). Keep
    the top share each generation; offspring inherit their parents' mean genetic value plus new environment. Without
    heredity selection achieves nothing; the per-generation response matches the breeder's equation R = h^2 S."""
    rng = np.random.default_rng(seed)
    out = {}
    for h2 in h2_values:
        G = rng.normal(0, np.sqrt(h2), n)
        means, rs, preds = [], [], []
        for _ in range(gens):
            Z = G + rng.normal(0, np.sqrt(1 - h2), n)
            means.append(float(Z.mean()))
            cut = np.quantile(Z, 1 - keep)
            sel = Z >= cut
            S = Z[sel].mean() - Z.mean()
            mothers = rng.choice(np.flatnonzero(sel), n)
            fathers = rng.choice(np.flatnonzero(sel), n)
            G = (G[mothers] + G[fathers]) / 2 + rng.normal(0, np.sqrt(h2 / 2), n)
            preds.append(float(h2 * S))
        for a, b in zip(means[:-1], means[1:]):
            rs.append(b - a)
        out[f"{h2:.1f}"] = {"h2": h2, "means": means, "response": float(np.mean(rs)), "predicted": float(np.mean(preds))}
    return out


# ---------------------------------------------------------------------------
# Cooperation: a small Axelrod tournament
# ---------------------------------------------------------------------------
def axelrod_mini(rounds: int = 200, seed: int = 1980) -> dict:
    """The iterated prisoner's dilemma (T=5, R=3, P=1, S=0), round robin with self-play, among six strategies:
    always cooperate, always defect, tit for tat, grim trigger, random, and tit for two tats. Scores are mean payoffs
    per round."""
    rng = np.random.default_rng(seed)
    P = {("C", "C"): (3, 3), ("C", "D"): (0, 5), ("D", "C"): (5, 0), ("D", "D"): (1, 1)}

    def allc(my, their):
        return "C"

    def alld(my, their):
        return "D"

    def tft(my, their):
        return their[-1] if their else "C"

    def grim(my, their):
        return "D" if "D" in their else "C"

    def rand(my, their):
        return "C" if rng.random() < 0.5 else "D"

    def tf2t(my, their):
        return "D" if their[-2:] == ["D", "D"] else "C"
    strats = {"always cooperate": allc, "always defect": alld, "tit for tat": tft, "grim trigger": grim,
              "random": rand, "tit for two tats": tf2t}
    names = list(strats)
    total = {n: 0.0 for n in names}
    games = {n: 0 for n in names}
    for i, a in enumerate(names):
        for b in names[i:]:
            ha, hb = [], []
            sa = sb = 0
            for _ in range(rounds):
                ma, mb = strats[a](ha, hb), strats[b](hb, ha)
                pa, pb = P[(ma, mb)]
                sa += pa
                sb += pb
                ha.append(ma)
                hb.append(mb)
            total[a] += sa / rounds
            games[a] += 1
            if b != a:
                total[b] += sb / rounds
                games[b] += 1
    scores = {n: total[n] / games[n] for n in names}
    return {"scores": dict(sorted(scores.items(), key=lambda kv: -kv[1])), "rounds": rounds}


# ---------------------------------------------------------------------------
# What is life? Thermodynamics, definitions, and Conway's Life
# ---------------------------------------------------------------------------
def entropy_budget(power: float = 100.0, t_body: float = 310.0, t_env: float = 293.0,
                   solar: float = 1.22e17, t_sun: float = 5772.0, t_earth: float = 255.0) -> dict:
    """Schrodinger's negative entropy, counted. A body that turns food into heat at ``power`` watts and hands the heat
    to cooler surroundings raises the world's entropy at Q (1/T_env - 1/T_body), however orderly it stays. The Earth
    takes in sunlight at the Sun's temperature and radiates the same energy at its own; for radiation the entropy flux
    is (4/3) Q / T, so the planet exports entropy at (4/3) Q (1/T_earth - 1/T_sun)."""
    body = power * (1 / t_env - 1 / t_body)
    s_in = 4 / 3 * solar / t_sun
    s_out = 4 / 3 * solar / t_earth
    photons = t_sun / t_earth
    return {"body": body, "body_in": power / t_body, "body_out": power / t_env, "earth_in": s_in, "earth_out": s_out,
            "earth": s_out - s_in, "photon_ratio": photons, "params": {"power": power, "t_body": t_body,
                                                                         "t_env": t_env, "t_sun": t_sun,
                                                                         "t_earth": t_earth}}


# Properties: C chemical, M metabolism (self-sustaining energy use), A self-maintaining boundary (autopoiesis),
# R reproduction, H heredity with variation, E belongs to a population capable of Darwinian evolution.
LIFE_CASES = {
    "bacterium": "CMARHE",
    "mule": "CMA",
    "virus": "CRHE",
    "fire": "CMR",
    "salt crystal": "CR",
    "Lenia glider": "A",
    "Tierra program": "RHE",
}
LIFE_DEFS = {
    "reproduces": "R",
    "metabolizes": "M",
    "autopoietic": "A",
    "Darwinian": "RHE",
    "NASA (Joyce)": "CME",
}


def life_definitions() -> dict:
    """Each definition as a set of required properties, applied to each case; then which cases each definition
    counts as alive, and how many cases no two definitions agree on."""
    table = {c: {d: set(req) <= set(props) for d, req in LIFE_DEFS.items()} for c, props in LIFE_CASES.items()}
    alive = {d: [c for c in LIFE_CASES if table[c][d]] for d in LIFE_DEFS}
    contested = [c for c in LIFE_CASES if len({table[c][d] for d in LIFE_DEFS}) > 1]
    return {"cases": list(LIFE_CASES), "defs": list(LIFE_DEFS), "props": LIFE_CASES, "table": table, "alive": alive,
            "contested": contested}


def life_step(A: np.ndarray) -> np.ndarray:
    """One step of Conway's Game of Life on a torus: birth on 3 neighbours, survival on 2 or 3."""
    n = sum(np.roll(np.roll(A, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy, dx) != (0, 0))
    return ((n == 3) | ((A == 1) & (n == 2))).astype(int)


def conway_glider(size: int = 10, steps: int = 8) -> dict:
    """The glider: five cells that return to their own shape every four steps, one cell further along the
    diagonal. Returns the frames, the population, and the check that the shape at step 4 is the shape at step 0
    shifted by (1, 1)."""
    A = np.zeros((size, size), int)
    for y, x in ((0, 1), (1, 2), (2, 0), (2, 1), (2, 2)):
        A[y + 1, x + 1] = 1
    frames = [A.tolist()]
    for _ in range(steps):
        A = life_step(A)
        frames.append(A.tolist())
    f = [np.array(x) for x in frames]
    period = next(p for p in range(1, steps + 1) if any(
        np.array_equal(f[p], np.roll(np.roll(f[0], dy, 0), dx, 1)) for dy in range(-2, 3) for dx in range(-2, 3)))
    shift = next((dy, dx) for dy in range(-2, 3) for dx in range(-2, 3)
                 if np.array_equal(f[period], np.roll(np.roll(f[0], dy, 0), dx, 1)))
    return {"frames": frames, "population": [int(x.sum()) for x in f], "period": period, "shift": list(shift),
            "speed": float(max(abs(shift[0]), abs(shift[1])) / period)}


# ---------------------------------------------------------------------------
# More toys: the eye's clock, drift, Fisher's theorem, signals, relatedness, parity, the shadow of the future
# ---------------------------------------------------------------------------
def eye_generations(change: float = 80_129_540.0, step: float = 0.01, h2: float = 0.5, intensity: float = 0.01,
                    cv: float = 0.01) -> dict:
    """Nilsson and Pelger (1994): a flat light-sensitive patch becomes a camera eye through morphological change
    amounting to a factor of about 8e7, i.e. ln(8e7) / ln(1.01) = 1829 steps of 1%. With heritability 0.5, selection
    intensity 0.01 and coefficient of variation 0.01, each generation changes the trait by R = h^2 i CV = 0.005%,
    so the whole sequence takes ln(change) / ln(1 + R) generations."""
    steps = np.log(change) / np.log(1 + step)
    r = h2 * intensity * cv
    gens = np.log(change) / np.log(1 + r)
    return {"steps": float(steps), "per_gen": float(r), "generations": float(gens), "change": change}


def kimura_fix(N: int, s: float) -> float:
    """Fixation probability of a single new mutant (p = 1/N) in a haploid population: (1 - e^{-2s}) / (1 - e^{-2Ns}),
    which is 1/N when s = 0."""
    if abs(s) < 1e-12:
        return 1.0 / N
    return float((1 - np.exp(-2 * s)) / (1 - np.exp(-2 * N * s)))


def wright_fisher(N: int = 100, s_values=(0.0, 0.01, 0.05, -0.01), runs: int = 40000, seed: int = 1930,
                  paths: int = 24, path_N: int = 50, path_gens: int = 120) -> dict:
    """Haploid Wright-Fisher sampling. (1) For a single mutant with advantage s, the share of runs in which it fixes,
    against Kimura's formula. (2) Neutral trajectories from p = 1/2 in a population of ``path_N``: drift alone."""
    rng = np.random.default_rng(seed)
    fix = {}
    for s in s_values:
        k = np.ones(runs, int)
        live = np.ones(runs, bool)
        while live.any():
            p = k[live] / N
            q = p * (1 + s) / (1 + p * s)
            k[live] = rng.binomial(N, q)
            live = (k > 0) & (k < N)
        sim = float((k == N).mean())
        fix[f"{s:+.2f}"] = {"s": s, "sim": sim, "kimura": kimura_fix(N, s), "se": float(np.sqrt(sim * (1 - sim) / runs))}
    traj = []
    for _ in range(paths):
        k, t = path_N // 2, [0.5]
        for _ in range(path_gens):
            k = rng.binomial(path_N, k / path_N)
            t.append(k / path_N)
        traj.append(t)
    lost = sum(t[-1] == 0 for t in traj)
    fixed = sum(t[-1] == 1 for t in traj)
    return {"N": N, "runs": runs, "fix": fix, "paths": traj, "path_N": path_N, "lost": lost, "fixed": fixed}


def fisher_theorem(w=(1.0, 1.2, 1.5), p=(0.5, 0.3, 0.2), gens: int = 30) -> dict:
    """Fisher's fundamental theorem in the Price form: with z = w and faithful transmission,
    w_bar * delta(w_bar) = Var(w). Iterates selection on asexual types; checks the identity each generation and shows
    that selection uses up the variance it feeds on."""
    w = np.array(w, float)
    p = np.array(p, float)
    mean, var, err = [], [], []
    for _ in range(gens):
        wb = float(p @ w)
        v = float(p @ (w - wb) ** 2)
        p2 = p * w / wb
        wb2 = float(p2 @ w)
        mean.append(wb)
        var.append(v)
        err.append(abs(wb * (wb2 - wb) - v))
        p = p2
    return {"mean": mean, "var": var, "max_error": max(err), "w": list(w)}


def lewis_signalling(n: int = 2, rounds: int = 2000, runs: int = 300, seed: int = 1969, curve_every: int = 50) -> dict:
    """Skyrms's version of Lewis's signalling game: a sender sees one of n equiprobable states and sends one of n
    signals; a receiver sees the signal and does one of n acts; both are rewarded when the act fits the state.
    Learning is Roth-Erev reinforcement (urns that start with one ball of each colour). Returns the mean success
    rate over time, the share of runs that reach a perfect signalling system, and which conventions they reach."""
    rng = np.random.default_rng(seed)
    curve = np.zeros(rounds // curve_every)
    perfect, final = 0, []
    conventions = {}
    for _ in range(runs):
        S = np.ones((n, n))
        R = np.ones((n, n))
        hits = np.zeros(rounds)
        for t in range(rounds):
            st = rng.integers(n)
            sig = rng.choice(n, p=S[st] / S[st].sum())
            act = rng.choice(n, p=R[sig] / R[sig].sum())
            if act == st:
                S[st, sig] += 1
                R[sig, act] += 1
                hits[t] = 1
        curve += hits.reshape(-1, curve_every).mean(axis=1)
        sp = S / S.sum(1, keepdims=True)
        rp = R / R.sum(1, keepdims=True)
        succ = float(np.mean([sp[s] @ rp[:, s] for s in range(n)]))
        final.append(succ)
        if succ > 0.9:
            perfect += 1
            key = "".join(str(int(np.argmax(sp[s]))) for s in range(n))
            conventions[key] = conventions.get(key, 0) + 1
    return {"n": n, "rounds": rounds, "runs": runs, "curve": [float(x) for x in curve / runs], "every": curve_every,
            "perfect": perfect / runs, "final_mean": float(np.mean(final)), "conventions": conventions}


def _gene_sets(kind: str, haplo: bool):
    """All equally likely (A, B) genotype pairs for two offspring; genes are labels of parental genes."""
    mom = ("m1", "m2")
    if kind == "half":
        dads = (("f1", "f2"), ("g1", "g2"))
    else:
        dads = (("f",),) * 2 if haplo else (("f1", "f2"),) * 2

    def kids(sex, dad):
        if sex == "son" and haplo:
            return [(m,) for m in mom]
        return [(m, f) for m in mom for f in dad]

    return kids, dads


def relatedness(actor: str, recipient: str, haplo: bool, kind: str = "full") -> float:
    """r from actor to recipient = P(a random gene of the actor is identical by descent with a random gene of the
    recipient) / P(two random genes of the recipient are identical): exact, by enumerating Mendelian outcomes."""
    kids, dads = _gene_sets(kind, haplo)
    num, den, cnt = 0.0, 0.0, 0
    for A in kids(actor, dads[0]):
        for B in kids(recipient, dads[1]):
            num += np.mean([a == b for a in A for b in B])
            den += np.mean([a == b for a in B for b in B])
            cnt += 1
    return float(num / den)


def relatedness_table() -> dict:
    rows = {"full sisters (diploid)": relatedness("daughter", "daughter", False),
            "half sisters (diploid)": relatedness("daughter", "daughter", False, "half"),
            "sister to sister (haplodiploid)": relatedness("daughter", "daughter", True),
            "sister to brother (haplodiploid)": relatedness("daughter", "son", True),
            "brother to sister (haplodiploid)": relatedness("son", "daughter", True),
            "own offspring": 0.5}
    return {"rows": rows}


def mutual_information(joint: np.ndarray) -> float:
    j = np.array(joint, float)
    j = j / j.sum()
    px, py = j.sum(1, keepdims=True), j.sum(0, keepdims=True)
    nz = j > 0
    return float((j[nz] * np.log2(j[nz] / (px @ py)[nz])).sum())


def parity_demo() -> dict:
    """Phenotype P = tall iff gene G = 1 and diet E = 1. How much information does each cause carry about P? It
    depends only on what varies in the background, not on which cause is a gene (Griffiths and Gray's parity)."""
    out = {}
    for name, pg, pe in (("both vary", 0.5, 0.5), ("diet fixed", 0.5, 1.0), ("gene fixed", 1.0, 0.5)):
        jg = np.zeros((2, 2))
        je = np.zeros((2, 2))
        for g in (0, 1):
            for e in (0, 1):
                pr = (pg if g else 1 - pg) * (pe if e else 1 - pe)
                ph = int(g and e)
                jg[g, ph] += pr
                je[e, ph] += pr
        out[name] = {"gene": mutual_information(jg), "diet": mutual_information(je)}
    return out


def shadow(T: float = 5, R: float = 3, P: float = 1, S: float = 0, w: float = 0.75, x0s=(0.08, 0.16, 0.24, 0.4),
           steps: int = 400, dt: float = 0.02) -> dict:
    """Tit for tat against always defect when the game continues with probability w. Expected payoffs over the whole
    game; TFT resists ALLD iff w > (T - R) / (T - P); the replicator dynamics have an unstable interior point x*."""
    L = 1 / (1 - w)
    a, b = R * L, S + w * P * L          # TFT vs TFT, TFT vs ALLD
    c, d = T + w * P * L, P * L          # ALLD vs TFT, ALLD vs ALLD
    xstar = (d - b) / (a - b - c + d)
    trajs = []
    for x0 in x0s:
        x, t = x0, [x0]
        for _ in range(steps):
            f1 = a * x + b * (1 - x)
            f2 = c * x + d * (1 - x)
            fb = x * f1 + (1 - x) * f2
            x = x + dt * x * (f1 - fb) / fb * 10
            x = min(1.0, max(0.0, x))
            t.append(x)
        trajs.append(t)
    ws = np.linspace(0.51, 0.99, 49)
    xs = []
    for ww in ws:
        LL = 1 / (1 - ww)
        aa, bb, cc, dd = R * LL, S + ww * P * LL, T + ww * P * LL, P * LL
        xs.append(float((dd - bb) / (aa - bb - cc + dd)))
    return {"payoffs": [[a, b], [c, d]], "xstar": float(xstar), "threshold": (T - R) / (T - P), "w": w,
            "trajs": trajs, "x0s": list(x0s), "curve_w": [float(x) for x in ws], "curve_x": xs}

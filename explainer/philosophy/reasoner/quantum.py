"""The quantum puzzle, built (Part 26).

A small Hilbert-space toolkit (numpy) and the no-go theorems computed on it.

* The Born rule on a qubit, sampled.
* Bell and CHSH: the singlet's correlation E(a, b) = -cos(a - b); every local deterministic strategy enumerated
  (|S| <= 2); the quantum value 2 sqrt 2 at the optimal angles; Tsirelson's bound checked by a search over angles.
* The CHSH game: all 16 deterministic strategies (best 3/4) and the quantum strategy simulated (cos^2(pi/8)).
* GHZ: the four product observables and every one of the 2^6 local assignments failing.
* The Peres--Mermin square: nine observables whose rows multiply to +I and columns to +I, +I, -I; every one of the
  2^9 value assignments failing.
* PBR: the entangled measurement whose four outcomes are each impossible for one of four product preparations.
* Decoherence: a qubit recorded by n environment qubits, its coherence |rho_01| falling as the product of overlaps.
* Bohmian mechanics: the guidance equation integrated for a two-slit Gaussian wavefunction.
* GRW: localization rates for one particle and for a pointer, and a simulated hit on a superposition.
* Interference in a Mach--Zehnder interferometer, with a which-path marker of any overlap (visibility = overlap).
* Uncertainty on a qubit: [X, Z] = -2iY; Robertson's bound and dX^2 + dZ^2 >= 1, on random states.
* Proper and improper mixtures: half a singlet is I/2, like a coin-flip mixture, but the pair is pure.
* Mermin's device: instruction sets agree on at least 5 of 9 setting pairs; quantum agreement is 1/2.
* The PR box: no-signalling, S = 4; the ladder local 2, quantum 2 sqrt 2, PR 4.
* Kochen--Specker by parity: Cabello's 18 vectors in 9 bases, all 2^18 assignments failing.
* Many worlds: counting branches against weighing them by the Born rule.
* Wigner's friend: a measurement on friend and qubit that tells unitary evolution from collapse.
* The GHZ game: every one of 64 classical strategies wins at most 3/4; the GHZ strategy always wins.
* Spekkens' toy theory: four ontic states, six states of knowledge, three measurements.
"""

from __future__ import annotations

import itertools
import math

import numpy as np

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.array([[1, 0], [0, -1]], complex)


def kron(*ms):
    out = np.array([[1]], complex)
    for m in ms:
        out = np.kron(out, m)
    return out


# ---------------------------------------------------------------------------
# The Born rule
# ---------------------------------------------------------------------------
def born(thetas=(0.0, math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2), shots: int = 2000, seed: int = 1926) -> dict:
    """A qubit cos(theta/2)|0> + sin(theta/2)|1>, measured in the {|0>, |1>} basis: P(0) = cos^2(theta/2). Sampled."""
    rng = np.random.default_rng(seed)
    rows = []
    for th in thetas:
        p0 = math.cos(th / 2) ** 2
        k = int((rng.random(shots) < p0).sum())
        rows.append({"theta_deg": round(math.degrees(th)), "p0": round(p0, 4), "freq0": round(k / shots, 4)})
    return {"shots": shots, "rows": rows}


# ---------------------------------------------------------------------------
# Bell and CHSH
# ---------------------------------------------------------------------------
SINGLET = np.array([0, 1, -1, 0], complex) / math.sqrt(2)


def spin(angle: float) -> np.ndarray:
    """Spin along a direction at `angle` in the x-z plane: cos(angle) Z + sin(angle) X."""
    return math.cos(angle) * Z + math.sin(angle) * X


def correlation(a: float, b: float, state=SINGLET) -> float:
    return float(np.real(state.conj() @ kron(spin(a), spin(b)) @ state))


def chsh(a=0.0, a2=math.pi / 2, b=math.pi / 4, b2=-math.pi / 4) -> dict:
    """S = E(a,b) + E(a,b') + E(a',b) - E(a',b'). Local deterministic strategies: each of Alice's two settings and
    Bob's two settings has a fixed outcome +-1; all 16 give |S| <= 2. The singlet at the standard angles gives
    2 sqrt 2; a grid search over angles never exceeds it (Tsirelson's bound)."""
    local = []
    for A0, A1, B0, B1 in itertools.product((1, -1), repeat=4):
        local.append(A0 * B0 + A0 * B1 + A1 * B0 - A1 * B1)
    E = {"ab": correlation(a, b), "ab'": correlation(a, b2), "a'b": correlation(a2, b), "a'b'": correlation(a2, b2)}
    S = E["ab"] + E["ab'"] + E["a'b"] - E["a'b'"]
    # Tsirelson: search angles
    grid = np.linspace(0, 2 * math.pi, 17)[:-1]
    best = 0.0
    for x1 in grid:
        for x2 in grid:
            for y1 in grid:
                for y2 in grid:
                    # the singlet's correlation is -cos(difference): checked against the matrix computation above
                    s = -(math.cos(x1 - y1) + math.cos(x1 - y2) + math.cos(x2 - y1) - math.cos(x2 - y2))
                    best = max(best, abs(s))
    assert abs(correlation(0.3, 1.1) + math.cos(0.3 - 1.1)) < 1e-12
    curve = [{"angle_deg": d, "quantum": round(-math.cos(math.radians(d)), 4),
              "linear": round(-1 + 2 * d / 180 if d <= 180 else 3 - 2 * d / 180, 4)} for d in range(0, 361, 5)]
    return {"local_values": sorted(set(local)), "local_max": max(abs(v) for v in local), "E": {k: round(v, 4) for k, v
            in E.items()}, "S": round(S, 4), "abs_S": round(abs(S), 4), "tsirelson": round(2 * math.sqrt(2), 4),
            "grid_best": round(best, 4), "curve": curve}


def chsh_game(trials: int = 20000, seed: int = 1964) -> dict:
    """Alice and Bob get random bits x, y and answer a, b without communicating; they win if a XOR b = x AND y.
    Enumerate all 16 deterministic strategies (a = f(x), b = g(y)): the best wins 3/4 of the time. The quantum
    strategy, sharing a Bell pair and measuring at angles 0, pi/2 (Alice) and pi/4, -pi/4 (Bob), wins cos^2(pi/8)."""
    strategies = []
    fs = [(0, 0), (0, 1), (1, 0), (1, 1)]          # f(0), f(1)
    for f in fs:
        for g in fs:
            wins = sum((f[x] ^ g[y]) == (x & y) for x in (0, 1) for y in (0, 1))
            strategies.append({"alice": f, "bob": g, "wins_of_4": wins})
    best = max(s["wins_of_4"] for s in strategies) / 4
    # quantum: |phi+> = (|00> + |11>)/sqrt2 ; measure along angles in the x-z plane
    phi = np.array([1, 0, 0, 1], complex) / math.sqrt(2)
    ang_a = {0: 0.0, 1: math.pi / 2}
    ang_b = {0: math.pi / 4, 1: -math.pi / 4}
    rng = np.random.default_rng(seed)
    wins = 0
    for _ in range(trials):
        x, y = int(rng.integers(2)), int(rng.integers(2))
        A, B = spin(ang_a[x]), spin(ang_b[y])
        # joint probabilities of outcomes (+1 -> bit 0, -1 -> bit 1)
        probs = []
        for sa in (1, -1):
            Pa = (I2 + sa * A) / 2
            for sb in (1, -1):
                Pb = (I2 + sb * B) / 2
                probs.append(float(np.real(phi.conj() @ kron(Pa, Pb) @ phi)))
        k = rng.choice(4, p=np.array(probs) / sum(probs))
        a, b = k // 2, k % 2
        wins += (a ^ b) == (x & y)
    return {"strategies": strategies, "classical_best": best, "quantum_rate": round(wins / trials, 4),
            "quantum_theory": round(math.cos(math.pi / 8) ** 2, 4), "trials": trials}


# ---------------------------------------------------------------------------
# GHZ
# ---------------------------------------------------------------------------
def ghz() -> dict:
    """The GHZ state (|000> + |111>)/sqrt2 is an eigenstate of XXX (+1) and of XYY, YXY, YYX (-1 each). Local values
    x_i, y_i = +-1 for each particle would need x1x2x3 = +1 and x1y2y3 = y1x2y3 = y1y2x3 = -1; multiply the last three:
    x1x2x3 (y1 y2 y3)^2 = -1, contradicting the first. The Reasoner checks the eigenvalues and all 64 assignments."""
    psi = np.zeros(8, complex)
    psi[0] = psi[7] = 1 / math.sqrt(2)
    ops = {"XXX": kron(X, X, X), "XYY": kron(X, Y, Y), "YXY": kron(Y, X, Y), "YYX": kron(Y, Y, X)}
    eig = {}
    for k, O in ops.items():
        v = O @ psi
        eig[k] = round(float(np.real(psi.conj() @ v)), 6)
    ok = 0
    for x1, x2, x3, y1, y2, y3 in itertools.product((1, -1), repeat=6):
        if x1 * x2 * x3 == 1 and x1 * y2 * y3 == -1 and y1 * x2 * y3 == -1 and y1 * y2 * x3 == -1:
            ok += 1
    return {"eigenvalues": eig, "assignments": 64, "consistent_assignments": ok}


# ---------------------------------------------------------------------------
# Peres--Mermin
# ---------------------------------------------------------------------------
PM = [["XI", "IX", "XX"], ["IY", "YI", "YY"], ["XY", "YX", "ZZ"]]


def _pauli2(s):
    m = {"I": I2, "X": X, "Y": Y, "Z": Z}
    return kron(m[s[0]], m[s[1]])


def peres_mermin() -> dict:
    """The Peres--Mermin square of two-qubit observables. In each row and column the three commute; the products of
    rows are +I, +I, +I and of columns +I, +I, -I. A non-contextual assignment of values +-1 to the nine would need
    the product of all nine to be +1 (by rows) and -1 (by columns). The Reasoner computes the operator products and
    checks all 512 assignments."""
    M = [[_pauli2(s) for s in row] for row in PM]
    row_prod, col_prod = [], []
    for r in range(3):
        P = M[r][0] @ M[r][1] @ M[r][2]
        row_prod.append(int(round(float(np.real(P[0, 0])))) if np.allclose(P, P[0, 0] * np.eye(4)) else None)
    for c in range(3):
        P = M[0][c] @ M[1][c] @ M[2][c]
        col_prod.append(int(round(float(np.real(P[0, 0])))) if np.allclose(P, P[0, 0] * np.eye(4)) else None)
    commute = all(np.allclose(M[r][i] @ M[r][j], M[r][j] @ M[r][i]) for r in range(3) for i in range(3)
                  for j in range(3)) and all(np.allclose(M[i][c] @ M[j][c], M[j][c] @ M[i][c]) for c in range(3)
                                             for i in range(3) for j in range(3))
    ok = 0
    best = 0
    for vals in itertools.product((1, -1), repeat=9):
        v = [vals[0:3], vals[3:6], vals[6:9]]
        sat = sum(v[r][0] * v[r][1] * v[r][2] == row_prod[r] for r in range(3)) + \
            sum(v[0][c] * v[1][c] * v[2][c] == col_prod[c] for c in range(3))
        best = max(best, sat)
        ok += sat == 6
    return {"square": PM, "row_products": row_prod, "column_products": col_prod, "commuting": commute,
            "assignments": 512, "consistent_assignments": ok, "best_constraints_met": best}


# ---------------------------------------------------------------------------
# PBR
# ---------------------------------------------------------------------------
def pbr() -> dict:
    """Pusey, Barrett and Rudolph (2012). Prepare each of two systems in |0> or |+>, independently: four product
    states. Measure the pair in an entangled basis whose four outcomes are each orthogonal to one of the four
    preparations. If the quantum states overlapped as states of reality (psi-epistemic), some underlying state would be
    compatible with all four preparations, and the measurement would have to give an outcome forbidden for one of them.
    The Reasoner checks the probability table."""
    k0 = np.array([1, 0], complex)
    k1 = np.array([0, 1], complex)
    kp = (k0 + k1) / math.sqrt(2)
    km = (k0 - k1) / math.sqrt(2)
    preps = {"00": np.kron(k0, k0), "0+": np.kron(k0, kp), "+0": np.kron(kp, k0), "++": np.kron(kp, kp)}
    basis = [(np.kron(k0, k1) + np.kron(k1, k0)) / math.sqrt(2),
             (np.kron(k0, km) + np.kron(k1, kp)) / math.sqrt(2),
             (np.kron(kp, k1) + np.kron(km, k0)) / math.sqrt(2),
             (np.kron(kp, km) + np.kron(km, kp)) / math.sqrt(2)]
    G = np.array([[abs(np.vdot(a, b)) for b in basis] for a in basis])
    table = {p: [round(float(abs(np.vdot(b, s)) ** 2), 4) for b in basis] for p, s in preps.items()}
    forbidden = {p: [i for i, v in enumerate(row) if v < 1e-9] for p, row in table.items()}
    return {"orthonormal": bool(np.allclose(G, np.eye(4))), "table": table, "forbidden": forbidden,
            "overlap": round(float(abs(np.vdot(k0, kp)) ** 2), 4)}


# ---------------------------------------------------------------------------
# Decoherence
# ---------------------------------------------------------------------------
def decoherence(max_env: int = 12, theta: float = 0.6) -> dict:
    """A qubit (|0> + |1>)/sqrt2 interacts with n environment qubits; each records the system imperfectly: |0> leaves
    it in |e0>, |1> in |e1>, with overlap cos(theta). The system's reduced coherence is |rho_01| = (1/2) cos(theta)^n:
    the interference terms vanish exponentially, without any collapse. Computed by building the full state for small
    n, and by the formula beyond."""
    e0 = np.array([1, 0], complex)
    e1 = np.array([math.cos(theta), math.sin(theta)], complex)
    rows = []
    for n in range(0, max_env + 1):
        if n <= 8:
            b0 = np.array([1], complex)
            b1 = np.array([1], complex)
            for _ in range(n):
                b0, b1 = np.kron(b0, e0), np.kron(b1, e1)
            coh = 0.5 * abs(np.vdot(b1, b0))
        else:
            coh = 0.5 * math.cos(theta) ** n
        rows.append({"env": n, "coherence": round(float(coh), 6)})
    return {"theta": theta, "overlap": round(math.cos(theta), 4), "rows": rows}


# ---------------------------------------------------------------------------
# Bohmian trajectories
# ---------------------------------------------------------------------------
def _packet(x, t, x0, s0):
    """A free Gaussian packet (hbar = m = 1), initially centred at x0 with width s0, at rest."""
    st = s0 * (1 + 1j * t / (2 * s0 ** 2))
    return (2 * math.pi * st ** 2) ** -0.25 * np.exp(-(x - x0) ** 2 / (4 * s0 * st))


def bohm(slit: float = 3.0, width: float = 0.3, n_traj: int = 60, t_max: float = 4.0, steps: int = 800,
         seed: int = 1952) -> dict:
    """The two-slit wavefunction just past the slits: two Gaussian packets at +-slit. Bohmian particles move with
    velocity v = Im(psi'/psi) (hbar = m = 1, time standing in for distance downstream). Starting positions are sampled
    from |psi(x, 0)|^2; the trajectories are integrated with RK2. They never cross, and pile up where |psi|^2 has its
    interference maxima. The final positions are compared with the Born-rule density."""
    rng = np.random.default_rng(seed)

    def psi(x, t):
        return (_packet(x, t, -slit, width) + _packet(x, t, slit, width)) / math.sqrt(2)

    def vel(x, t, h=1e-5):
        p = psi(x, t)
        dp = (psi(x + h, t) - psi(x - h, t)) / (2 * h)
        return np.imag(dp / p)

    # sample starting points from |psi(x,0)|^2 by stratified inverse CDF
    xs = np.linspace(-slit - 5 * width, slit + 5 * width, 4001)
    dens = np.abs(psi(xs, 0.0)) ** 2
    cdf = np.cumsum(dens)
    cdf /= cdf[-1]
    us = (np.arange(n_traj) + 0.5) / n_traj
    x0 = np.interp(us, cdf, xs)
    dt = t_max / steps
    traj = [x0.copy()]
    x = x0.copy()
    t = 0.0
    for _ in range(steps):
        k1 = vel(x, t)
        k2 = vel(x + dt * k1, t + dt)
        x = x + dt * (k1 + k2) / 2
        t += dt
        traj.append(x.copy())
    T = np.array(traj)
    order_kept = bool(np.all(np.diff(T, axis=1) > 0))
    xf = np.linspace(-10, 10, 241)
    final_density = np.abs(psi(xf, t_max)) ** 2
    hist, edges = np.histogram(T[-1], bins=20, range=(-10, 10))
    return {"t": [round(i * dt, 3) for i in range(0, steps + 1, 10)],
            "traj": [[round(float(v), 3) for v in T[::10, j]] for j in range(n_traj)],
            "never_cross": order_kept, "x": [round(float(v), 2) for v in xf],
            "density_final": [round(float(v), 5) for v in final_density],
            "density_start": [round(float(v), 5) for v in np.abs(psi(xf, 0.0)) ** 2],
            "hist": hist.tolist(), "slit": slit}


# ---------------------------------------------------------------------------
# GRW
# ---------------------------------------------------------------------------
YEAR = 3.156e7


def grw(lam: float = 1e-16, sigma: float = 1e-7, seed: int = 1986) -> dict:
    """GRW (1986): every particle suffers a spontaneous localization at rate lambda (about 1e-16 per second), which
    multiplies its wavefunction by a Gaussian of width sigma (about 1e-7 m). One particle: a hit every ~10^8 years.
    A pointer of 10^23 particles in a superposition of two positions: the first hit on any of them collapses the
    whole, within about 10^-7 s. A simulated hit on a superposition of two packets 1 micron apart."""
    one = 1 / lam / YEAR
    rows = [{"particles": n, "mean_wait_s": 1 / (n * lam)} for n in (1, 1e6, 1e12, 1e18, 1e23)]
    rng = np.random.default_rng(seed)
    x = np.linspace(-2e-6, 2e-6, 4001)
    d = 1e-6
    w = 5e-8
    psi = np.exp(-(x + d / 2) ** 2 / (4 * w * w)) + np.exp(-(x - d / 2) ** 2 / (4 * w * w))
    psi = psi / np.sqrt(np.trapezoid(np.abs(psi) ** 2, x))
    # the hit centre is chosen with probability density ||L_c psi||^2
    cs = np.linspace(-1.5e-6, 1.5e-6, 601)
    weights = np.array([np.trapezoid(np.abs(np.exp(-(x - c) ** 2 / (2 * sigma ** 2)) * psi) ** 2, x) for c in cs])
    weights /= weights.sum()
    c = float(rng.choice(cs, p=weights))
    after = np.exp(-(x - c) ** 2 / (2 * sigma ** 2)) * psi
    after = after / np.sqrt(np.trapezoid(np.abs(after) ** 2, x))
    left = float(np.trapezoid(np.abs(after[x < 0]) ** 2, x[x < 0]))
    return {"lambda": lam, "sigma": sigma, "one_particle_years": round(one / 1e8, 2), "rows": rows,
            "x_um": [round(float(v) * 1e6, 4) for v in x[::20]], "before": [round(float(v), 4) for v in
                                                                             (np.abs(psi) ** 2)[::20] / 1e6],
            "after": [round(float(v), 4) for v in (np.abs(after) ** 2)[::20] / 1e6], "hit_um": round(c * 1e6, 3),
            "left_weight_after": round(left, 6)}


# ---------------------------------------------------------------------------
# Interference: a Mach--Zehnder interferometer
# ---------------------------------------------------------------------------
H2 = np.array([[1, 1], [1, -1]], complex) / math.sqrt(2)


def interferometer(n_phi: int = 73, overlaps=(1.0, 0.5, 0.0), shots: int = 2000, seed: int = 1801) -> dict:
    """A photon meets a beam splitter, takes both arms (one with phase phi), and meets a second beam splitter.
    Amplitudes to detector D0: (1 + e^{i phi}) / 2, so P(D0) = cos^2(phi / 2). If the arms leave marker states with
    overlap c = <m0|m1> (a which-path record), P(D0) = (1 + c cos phi) / 2: the fringe visibility is exactly c.
    Blocking one arm: each detector fires a quarter of the time, and the photon is absorbed half the time."""
    phis = [2 * math.pi * i / (n_phi - 1) for i in range(n_phi)]
    curves = {}
    for c in overlaps:
        m0 = np.array([1, 0], complex)
        m1 = np.array([c, math.sqrt(max(0.0, 1 - c * c))], complex)
        ys = []
        for ph in phis:
            # path (x) marker; after BS1 and phase: (|0>|m0> + e^{i phi} |1>|m1>) / sqrt2
            st = (np.kron([1, 0], m0) + np.exp(1j * ph) * np.kron([0, 1], m1)) / math.sqrt(2)
            st = np.kron(H2, I2) @ st
            ys.append(float(np.sum(np.abs(st[:2]) ** 2)))
        curves[str(c)] = [round(y, 4) for y in ys]
    vis = {k: round((max(v) - min(v)) / (max(v) + min(v)), 4) for k, v in curves.items()}
    # amplitudes at phi = 0, path by path
    amp = {"D0": [0.5, 0.5], "D1": [0.5, -0.5]}
    rng = np.random.default_rng(seed)
    samples = []
    for ph in (0.0, math.pi / 2, math.pi):
        p0 = math.cos(ph / 2) ** 2
        samples.append({"phi_deg": round(math.degrees(ph)), "p0": round(p0, 4),
                        "freq0": round(float((rng.random(shots) < p0).mean()), 4)})
    blocked = {"D0": 0.25, "D1": 0.25, "absorbed": 0.5}
    return {"phi": [round(p, 4) for p in phis], "curves": curves, "visibility": vis, "amplitudes": amp,
            "samples": samples, "shots": shots, "blocked": blocked}


# ---------------------------------------------------------------------------
# Incompatible questions: uncertainty on a qubit
# ---------------------------------------------------------------------------
def uncertainty(n_random: int = 5000, seed: int = 1927) -> dict:
    """Spin-x and spin-z do not commute: [X, Z] = -2iY. Robertson: dX dZ >= |<[X, Z]>| / 2 = |<Y>|. And because a
    qubit's Bloch vector has length at most 1, dX^2 + dZ^2 = 2 - <X>^2 - <Z>^2 >= 1: no state answers both questions
    sharply. Checked on named states and on random pure and mixed states."""
    comm = X @ Z - Z @ X
    comm_is = bool(np.allclose(comm, -2j * Y))

    def stats(rho):
        ex, ey, ez = (float(np.real(np.trace(rho @ m))) for m in (X, Y, Z))
        dx, dz = math.sqrt(max(0.0, 1 - ex * ex)), math.sqrt(max(0.0, 1 - ez * ez))
        return ex, ey, ez, dx, dz

    named = []
    for name, th in (("|0>", 0.0), ("45 deg", math.pi / 4), ("|+>", math.pi / 2)):
        v = np.array([math.cos(th / 2), math.sin(th / 2)], complex)
        ex, ey, ez, dx, dz = stats(np.outer(v, v.conj()))
        named.append({"state": name, "dX": round(dx, 4), "dZ": round(dz, 4), "sum_sq": round(dx * dx + dz * dz, 4)})
    rng = np.random.default_rng(seed)
    worst_rob, min_sum = 1e9, 1e9
    points = []
    for _ in range(n_random):
        r = rng.normal(size=3)
        r = r / np.linalg.norm(r) * rng.random() ** (1 / 3)        # uniform in the Bloch ball
        rho = (I2 + r[0] * X + r[1] * Y + r[2] * Z) / 2
        ex, ey, ez, dx, dz = stats(rho)
        worst_rob = min(worst_rob, dx * dz - abs(ey))
        min_sum = min(min_sum, dx * dx + dz * dz)
        if len(points) < 400:
            points.append([round(ex, 3), round(ez, 3)])
    return {"commutator_is_minus_2iY": comm_is, "named": named, "n_random": n_random,
            "robertson_slack_min": round(worst_rob, 4), "sum_sq_min": round(min_sum, 4), "points": points}


# ---------------------------------------------------------------------------
# Proper and improper mixtures
# ---------------------------------------------------------------------------
def ptrace_b(rho4):
    return np.einsum("ijkj->ik", rho4.reshape(2, 2, 2, 2))


def mixtures() -> dict:
    """Half of a singlet has reduced state I/2, the same matrix as a 50/50 mixture of |0>, |1> and of |+>, |->: no
    measurement on that half can tell them apart. The pair can: the entangled pair is pure (purity 1) and passes the
    singlet test with certainty; the mixture of product states has purity 1/2 and passes half the time."""
    psi = SINGLET
    rho_pair = np.outer(psi, psi.conj())
    red = ptrace_b(rho_pair)
    k0, k1 = np.array([1, 0], complex), np.array([0, 1], complex)
    kp, km = (k0 + k1) / math.sqrt(2), (k0 - k1) / math.sqrt(2)
    mix_z = (np.outer(k0, k0) + np.outer(k1, k1)) / 2
    mix_x = (np.outer(kp, kp.conj()) + np.outer(km, km.conj())) / 2
    same = bool(np.allclose(red, I2 / 2) and np.allclose(mix_z, I2 / 2) and np.allclose(mix_x, I2 / 2))
    # the global mixture that ignorance of a definite outcome would give
    k01, k10 = np.kron(k0, k1), np.kron(k1, k0)
    rho_mix = (np.outer(k01, k01) + np.outer(k10, k10)) / 2
    pur = {"entangled": round(float(np.real(np.trace(rho_pair @ rho_pair))), 4),
           "mixture": round(float(np.real(np.trace(rho_mix @ rho_mix))), 4)}
    test = {"entangled": round(float(np.real(psi.conj() @ rho_pair @ psi)), 4),
            "mixture": round(float(np.real(psi.conj() @ rho_mix @ psi)), 4)}
    same_local = bool(np.allclose(ptrace_b(rho_mix), red))
    return {"reduced": [[round(float(np.real(x)), 4) for x in row] for row in red], "all_equal_half_I": same,
            "same_locally": same_local, "purity": pur, "singlet_test": test}


# ---------------------------------------------------------------------------
# Mermin's device
# ---------------------------------------------------------------------------
def mermin_device(runs: int = 9000, seed: int = 1981) -> dict:
    """Two detectors, each set at random to 1, 2 or 3, flash red or green. Same settings: always the same colour.
    Instruction sets (a colour for each setting, carried by each particle) agree on at least 5 of the 9 setting pairs.
    The quantum version (|phi+>, Bloch angles 0, 120, 240 degrees) agrees on exactly half of all runs."""
    sets = []
    for cols in itertools.product("RG", repeat=3):
        agree = sum(cols[i] == cols[j] for i in range(3) for j in range(3))
        sets.append({"set": "".join(cols), "agree_of_9": agree})
    worst = min(s["agree_of_9"] for s in sets)
    phi = np.array([1, 0, 0, 1], complex) / math.sqrt(2)
    angs = [0.0, 2 * math.pi / 3, 4 * math.pi / 3]
    rng = np.random.default_rng(seed)
    agree = same_setting = same_agree = 0
    for _ in range(runs):
        i, j = int(rng.integers(3)), int(rng.integers(3))
        E = float(np.real(phi.conj() @ kron(spin(angs[i]), spin(angs[j])) @ phi))
        a = rng.random() < (1 + E) / 2
        agree += a
        if i == j:
            same_setting += 1
            same_agree += a
    return {"sets": sets, "worst_agree_of_9": worst, "quantum_theory": 0.5, "runs": runs,
            "quantum_rate": round(agree / runs, 4), "same_setting_rate": round(same_agree / same_setting, 4),
            "different_setting_theory": 0.25}


# ---------------------------------------------------------------------------
# The PR box
# ---------------------------------------------------------------------------
def pr_box() -> dict:
    """Popescu and Rohrlich (1994): a box with inputs x, y and outputs a, b, uniformly random subject to
    a XOR b = x AND y. It wins the CHSH game every time (S = 4), yet signals nothing: each side's outputs are 50/50
    whatever the other side's input. Quantum boxes are no-signalling too, but stop at 2 sqrt 2."""
    P = {}
    for x in (0, 1):
        for y in (0, 1):
            P[(x, y)] = {(a, b): (0.5 if (a ^ b) == (x & y) else 0.0) for a in (0, 1) for b in (0, 1)}

    def E(x, y):
        return sum(p * (1 if a == b else -1) for (a, b), p in P[(x, y)].items())

    S = E(0, 0) + E(0, 1) + E(1, 0) - E(1, 1)
    win = sum(p for x in (0, 1) for y in (0, 1) for (a, b), p in P[(x, y)].items() if (a ^ b) == (x & y)) / 4
    alice = {f"x={x}, y={y}": sum(p for (a, b), p in P[(x, y)].items() if a == 0) for x in (0, 1) for y in (0, 1)}
    bob = {f"x={x}, y={y}": sum(p for (a, b), p in P[(x, y)].items() if b == 0) for x in (0, 1) for y in (0, 1)}
    # quantum marginals for the CHSH-game strategy
    phi = np.array([1, 0, 0, 1], complex) / math.sqrt(2)
    ang_a, ang_b = {0: 0.0, 1: math.pi / 2}, {0: math.pi / 4, 1: -math.pi / 4}
    qm = {}
    for x in (0, 1):
        for y in (0, 1):
            Pa = (I2 + spin(ang_a[x])) / 2
            qm[f"x={x}, y={y}"] = round(float(np.real(phi.conj() @ kron(Pa, I2) @ phi)), 4)
    ladder = [{"name": "local", "S": 2.0, "win": 0.75},
              {"name": "quantum", "S": round(2 * math.sqrt(2), 4), "win": round(math.cos(math.pi / 8) ** 2, 4)},
              {"name": "PR box", "S": S, "win": win}]
    return {"S": S, "win": win, "alice_marginal": alice, "bob_marginal": bob, "quantum_alice_marginal": qm,
            "ladder": ladder}


# ---------------------------------------------------------------------------
# Kochen--Specker by parity: Cabello's eighteen vectors
# ---------------------------------------------------------------------------
CABELLO = [
    [(0, 0, 0, 1), (0, 0, 1, 0), (1, 1, 0, 0), (1, -1, 0, 0)],
    [(0, 0, 0, 1), (0, 1, 0, 0), (1, 0, 1, 0), (1, 0, -1, 0)],
    [(1, -1, 1, -1), (1, -1, -1, 1), (1, 1, 0, 0), (0, 0, 1, 1)],
    [(1, -1, 1, -1), (1, 1, 1, 1), (1, 0, -1, 0), (0, 1, 0, -1)],
    [(0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 1), (1, 0, 0, -1)],
    [(1, -1, -1, 1), (1, 1, 1, 1), (1, 0, 0, -1), (0, 1, -1, 0)],
    [(1, 1, -1, 1), (1, 1, 1, -1), (1, -1, 0, 0), (0, 0, 1, 1)],
    [(1, 1, -1, 1), (-1, 1, 1, 1), (1, 0, 1, 0), (0, 1, 0, -1)],
    [(1, 1, 1, -1), (-1, 1, 1, 1), (1, 0, 0, 1), (0, 1, -1, 0)],
]


def cabello18() -> dict:
    """Cabello, Estebaranz and Garcia-Alcaine (1996): eighteen directions in four dimensions forming nine orthogonal
    bases, each direction in exactly two. A non-contextual assignment gives each basis exactly one 'yes': nine yeses,
    an odd number, but counting by directions gives twice the number of yes-directions, an even number. All 2^18
    assignments are checked anyway."""
    vecs = sorted({v for b in CABELLO for v in b})
    idx = {v: i for i, v in enumerate(vecs)}
    orth = all(abs(np.dot(b[i], b[j])) < 1e-12 for b in CABELLO for i in range(4) for j in range(i + 1, 4))
    counts = [sum(v in b for b in CABELLO) for v in vecs]
    n = len(vecs)
    bits = ((np.arange(2 ** n)[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int8)
    ok = np.ones(2 ** n, bool)
    best = np.zeros(2 ** n, np.int8)
    for b in CABELLO:
        s = bits[:, [idx[v] for v in b]].sum(axis=1)
        ok &= s == 1
        best += (s == 1)
    return {"n_vectors": n, "n_bases": len(CABELLO), "orthogonal": bool(orth), "each_in_two": all(c == 2 for c in counts),
            "assignments": 2 ** n, "consistent_assignments": int(ok.sum()), "best_bases_met": int(best.max())}


# ---------------------------------------------------------------------------
# Many worlds: counting branches against weighing them
# ---------------------------------------------------------------------------
def branch_count(p: float = 0.9, ns=(10, 50, 200), tol: float = 0.1, plot_n: int = 50) -> dict:
    """Measure a qubit with Born weights p, 1 - p, n times: 2^n branches. The fraction of branches (by count) whose
    observed frequency is within tol of p shrinks to zero; their total Born weight grows to one. Counting branches
    predicts frequencies near 1/2; weighing them predicts the Born rule."""
    rows = []
    for n in ns:
        cnt = wt = 0.0
        for k in range(n + 1):
            if abs(k / n - p) <= tol + 1e-12:
                c = math.comb(n, k)
                cnt += c
                wt += c * p ** k * (1 - p) ** (n - k)
        rows.append({"n": n, "count_fraction": float(f"{cnt / 2 ** n:.3g}"), "born_weight": round(wt, 4),
                     "born_shortfall": float(f"{1 - wt:.2g}")})
    n = plot_n
    count = [math.comb(n, k) / 2 ** n for k in range(n + 1)]
    weight = [math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]
    return {"p": p, "tol": tol, "rows": rows, "plot_n": n, "count_dist": [round(c, 5) for c in count],
            "weight_dist": [round(w, 5) for w in weight]}


# ---------------------------------------------------------------------------
# Wigner's friend: a test that tells unitary from collapse
# ---------------------------------------------------------------------------
def wigner_friend(shots: int = 2000, seed: int = 1961) -> dict:
    """The friend measures a qubit in |+>: by the Schrodinger equation, qubit and memory become
    (|0>|saw 0> + |1>|saw 1>) / sqrt2. Wigner measures the pair in a basis containing that state. If the friend's
    measurement was unitary, Wigner's 'yes' comes with certainty; if it collapsed, half the time."""
    k0, k1 = np.array([1, 0], complex), np.array([0, 1], complex)
    plus = (k0 + k1) / math.sqrt(2)
    cnot = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], complex)
    joint = cnot @ np.kron(plus, k0)
    target = (np.kron(k0, k0) + np.kron(k1, k1)) / math.sqrt(2)
    p_unitary = float(abs(target.conj() @ joint) ** 2)
    rho_c = (np.outer(np.kron(k0, k0), np.kron(k0, k0)) + np.outer(np.kron(k1, k1), np.kron(k1, k1))) / 2
    p_collapse = float(np.real(target.conj() @ rho_c @ target))
    rng = np.random.default_rng(seed)
    return {"p_unitary": round(p_unitary, 4), "p_collapse": round(p_collapse, 4), "shots": shots,
            "freq_unitary": round(float((rng.random(shots) < p_unitary).mean()), 4),
            "freq_collapse": round(float((rng.random(shots) < p_collapse).mean()), 4)}


# ---------------------------------------------------------------------------
# The GHZ game
# ---------------------------------------------------------------------------
GHZ_INPUTS = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]


def ghz_game() -> dict:
    """Three players get bits x, y, z with x XOR y XOR z = 0 (four questions, equally likely) and win if
    a XOR b XOR c = x OR y OR z. All 4^3 = 64 deterministic strategies: the best wins 3/4. Sharing the GHZ state and
    measuring X on input 0, Y on input 1 (outcome +1 -> bit 0), they win every time."""
    fs = [(0, 0), (0, 1), (1, 0), (1, 1)]
    wins = []
    for f in fs:
        for g in fs:
            for h in fs:
                wins.append(sum((f[x] ^ g[y] ^ h[z]) == (x | y | z) for x, y, z in GHZ_INPUTS))
    psi = np.zeros(8, complex)
    psi[0] = psi[7] = 1 / math.sqrt(2)
    m = {0: X, 1: Y}
    q = {}
    for x, y, z in GHZ_INPUTS:
        ev = float(np.real(psi.conj() @ kron(m[x], m[y], m[z]) @ psi))
        need = 1 if (x | y | z) == 0 else -1          # product of +-1 outcomes must be +1 for parity 0
        q["".join(map(str, (x, y, z)))] = round((1 + need * ev) / 2, 6)
    hist = {k: wins.count(k) for k in sorted(set(wins))}
    return {"strategies": len(wins), "classical_best": max(wins) / 4, "histogram": hist, "quantum": q,
            "quantum_win": round(sum(q.values()) / 4, 6)}


# ---------------------------------------------------------------------------
# Spekkens' toy theory
# ---------------------------------------------------------------------------
def spekkens() -> dict:
    """Spekkens (2007): four ontic states; the knowledge balance principle allows at most one bit of the two, so the
    states of maximal knowledge are the six pairs. The three measurements partition the four into pairs. Each state is
    certain under one measurement and 50/50 under the other two, like a qubit's six axis states; distinct
    non-complementary states overlap; and equal mixtures of complementary pairs coincide."""
    ontic = (1, 2, 3, 4)
    states = [frozenset(p) for p in itertools.combinations(ontic, 2)]
    meas = [(frozenset({1, 2}), frozenset({3, 4})), (frozenset({1, 3}), frozenset({2, 4})),
            (frozenset({1, 4}), frozenset({2, 3}))]
    name = lambda st: "".join(map(str, sorted(st)))  # noqa: E731
    table = []
    for st in states:
        table.append({"state": name(st), "p": [len(st & m[0]) / 2 for m in meas]})
    overlaps = {name(st): sum(1 for t in states if t != st and st & t) for st in states}

    def mix(a, b):
        return tuple(sorted(((k, (k in a) / 4 + (k in b) / 4) for k in ontic)))

    same_mix = mix(states[0], states[5]) == mix(states[1], states[4]) == mix(states[2], states[3])
    return {"n_states": len(states), "measurements": [[name(m[0]), name(m[1])] for m in meas], "table": table,
            "overlaps": overlaps, "mixtures_equal": bool(same_mix)}

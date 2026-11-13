"""Quantum algorithms on the simulator (Part 53): reversible computing's cost (Landauer), Bell states and the CHSH
game, no-cloning, Deutsch-Jozsa, Bernstein-Vazirani, Simon, the quantum Fourier transform against the FFT, phase
estimation, Shor's order finding (factoring 15 and 21), Grover's search, and BB84 key distribution."""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

from .sim import H, X, Z, State, phase, ry

K_B = 1.380649e-23


def landauer(T: float = 300.0) -> dict:
    """kT ln 2: the least energy to erase one bit at temperature T (Landauer 1961)."""
    e = K_B * T * math.log(2)
    return {"T": T, "joules": e, "electronvolts": e / 1.602176634e-19, "per_1e18_erasures_W": e * 1e18}


# ---------------------------------------------------------------- entanglement

def bell() -> dict:
    s = State(2).apply(H, 0).cnot(0, 1)
    return {"amplitudes": [[float(a.real), float(a.imag)] for a in s.v], "probs": s.probs().tolist()}


def chsh(trials: int = 200_000, seed: int = 0) -> dict:
    """The CHSH game: a referee sends bits x, y; Alice and Bob answer a, b and win if a XOR b = x AND y.  The best
    classical strategy wins 3/4; sharing a Bell pair and measuring at angles 0, pi/4 (Alice) and pi/8, -pi/8 (Bob)
    wins cos^2(pi/8) ~ 0.854.  Exact quantum value and a sampled one."""
    rng = np.random.default_rng(seed)
    A = {0: 0.0, 1: math.pi / 4}
    B = {0: math.pi / 8, 1: -math.pi / 8}

    def win_prob(x, y):
        s = State(2).apply(H, 0).cnot(0, 1)
        s.apply(ry(-2 * A[x]), 0).apply(ry(-2 * B[y]), 1)        # rotate the measurement bases
        p = s.probs()
        same = p[0] + p[3]
        return same if not (x and y) else 1 - same

    exact = np.mean([win_prob(x, y) for x in (0, 1) for y in (0, 1)])
    xs, ys = rng.integers(0, 2, trials), rng.integers(0, 2, trials)
    probs = {(x, y): win_prob(x, y) for x in (0, 1) for y in (0, 1)}
    wins = rng.random(trials) < np.array([probs[(x, y)] for x, y in zip(xs, ys)])
    # classical: try all 16 deterministic strategies
    best = 0.0
    for a0 in (0, 1):
        for a1 in (0, 1):
            for b0 in (0, 1):
                for b1 in (0, 1):
                    w = np.mean([((a0, a1)[x] ^ (b0, b1)[y]) == (x & y) for x in (0, 1) for y in (0, 1)])
                    best = max(best, w)
    return {"quantum": float(exact), "sampled": float(wins.mean()), "classical": float(best),
            "cos2_pi_8": math.cos(math.pi / 8) ** 2}


# ---------------------------------------------------------------- oracles and interference

def _oracle_phase(state: State, f, n: int):
    """Phase oracle on the first n qubits: |x> -> (-1)^f(x) |x>."""
    signs = np.array([(-1) ** f(x) for x in range(2 ** n)])
    v = state.v.reshape(2 ** n, -1) * signs[:, None]
    state.v = v.reshape(-1)


def deutsch_jozsa(n: int = 4) -> dict:
    """One query decides constant against balanced: after H^n, the oracle and H^n, the probability of measuring
    all zeros is 1 for a constant function and 0 for a balanced one."""
    out = {}
    fns = {"constant 0": lambda x: 0, "constant 1": lambda x: 1, "balanced (parity)": lambda x: bin(x).count("1") % 2,
           "balanced (top bit)": lambda x: x >> (n - 1)}
    for name, f in fns.items():
        s = State(n)
        for q in range(n):
            s.apply(H, q)
        amp_before = s.v.copy()
        _oracle_phase(s, f, n)
        amp_mid = s.v.copy()
        for q in range(n):
            s.apply(H, q)
        out[name] = {"p_zero": float(s.probs()[0]), "after_oracle": [float(a.real) for a in amp_mid],
                     "uniform": [float(a.real) for a in amp_before], "final": [float(a.real) for a in s.v]}
    return {"n": n, "classical_worst_queries": 2 ** (n - 1) + 1, "cases": out}


def bernstein_vazirani(secret: int = 0b1011, n: int = 4) -> dict:
    s = State(n)
    for q in range(n):
        s.apply(H, q)
    _oracle_phase(s, lambda x: bin(x & secret).count("1") % 2, n)
    for q in range(n):
        s.apply(H, q)
    p = s.probs()
    return {"secret": secret, "n": n, "measured": int(np.argmax(p)), "p": float(p.max()), "classical_queries": n}


def simon(secret: int = 0b110, n: int = 3, seed: int = 0) -> dict:
    """Simon's problem: f(x) = f(x XOR s).  Each run of the circuit yields a y with y . s = 0; n - 1 independent
    such y determine s by Gaussian elimination over GF(2).  Classically about 2^(n/2) queries are needed."""
    rng = np.random.default_rng(seed)
    # f: map x and x^s to the same label
    labels, f = {}, {}
    for x in range(2 ** n):
        key = min(x, x ^ secret)
        labels.setdefault(key, len(labels))
        f[x] = labels[key]
    ys = []
    runs = 0
    while True:
        runs += 1
        s = State(2 * n)
        for q in range(n):
            s.apply(H, q)
        # oracle |x>|0> -> |x>|f(x)>
        v = np.zeros_like(s.v)
        for x in range(2 ** n):
            v[(x << n) | f[x]] += s.v[x << n]
        s.v = v
        for q in range(n):
            s.apply(H, q)
        y = s.measure(rng, list(range(n)))
        ys.append(y)
        cand = [c for c in range(1, 2 ** n) if all(bin(c & yy).count("1") % 2 == 0 for yy in ys)]
        if len(cand) == 1:
            break
        if runs > 50:
            break
    return {"secret": secret, "n": n, "ys": ys, "runs": runs, "found": cand[0] if len(cand) == 1 else None,
            "dot_zero": all(bin(secret & y).count("1") % 2 == 0 for y in ys)}


# ---------------------------------------------------------------- QFT, phase estimation, Shor

def qft_matrix(n: int) -> np.ndarray:
    N = 2 ** n
    w = np.exp(2j * math.pi / N)
    j, k = np.meshgrid(np.arange(N), np.arange(N))
    return w ** (j * k) / math.sqrt(N)


def qft(state: State, qubits: list[int]) -> State:
    """The circuit: on each qubit a Hadamard, then controlled phase rotations by 2 pi / 2^k from the later qubits;
    finally reverse the order.  n(n+1)/2 gates for 2^n points."""
    n = len(qubits)
    for i in range(n):
        state.apply(H, qubits[i])
        for k in range(i + 1, n):
            state.controlled(phase(2 * math.pi / 2 ** (k - i + 1)), qubits[k], qubits[i])
    for i in range(n // 2):
        state.apply(np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex),
                    qubits[i], qubits[n - 1 - i])
    return state


def qft_check(n: int = 4, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    v = rng.standard_normal(2 ** n) + 1j * rng.standard_normal(2 ** n)
    v /= np.linalg.norm(v)
    s = State(n)
    s.v = v.copy()
    qft(s, list(range(n)))
    fft = np.fft.ifft(v) * math.sqrt(2 ** n)          # numpy's ifft has the +i sign convention of the QFT
    gates = n * (n + 1) // 2 + n // 2
    return {"n": n, "max_diff_fft": float(np.max(np.abs(s.v - fft))),
            "max_diff_matrix": float(np.max(np.abs(s.v - qft_matrix(n) @ v))), "gates": gates,
            "fft_ops": int(2 ** n * n)}


def phase_estimation(theta: float = 0.3, t: int = 6) -> dict:
    """Estimate the phase of eigenvalue e^{2 pi i theta} of U = phase(2 pi theta) acting on |1>, with t counting
    qubits: the distribution over t-bit estimates peaks at the nearest multiple of 1/2^t."""
    s = State(t + 1, basis=1)                          # target qubit (last) in |1>
    for q in range(t):
        s.apply(H, q)
    for q in range(t):
        power = 2 ** (t - 1 - q)
        s.controlled(phase(2 * math.pi * theta * power), q, t)
    # inverse QFT on the counting register
    inv = State(t)
    v = s.v.reshape(2 ** t, 2)[:, 1]
    inv.v = qft_matrix(t).conj().T @ v
    p = np.abs(inv.v) ** 2
    return {"theta": theta, "t": t, "probs": p.tolist(), "best": int(np.argmax(p)) / 2 ** t,
            "p_best": float(p.max())}


def order_finding(a: int, N: int, t: int | None = None, shots: int = 20, seed: int = 0) -> dict:
    """Shor's algorithm for the order r of a modulo N: a counting register of t qubits in superposition, the work
    register holding a^x mod N (computed classically into the state, since the modular exponentiation circuit is
    not the point), the inverse QFT on the counting register, and continued fractions on each measured value.

    The returned ``r`` is the true order, found classically by trying r = 1, 2, ...; what the measurements gave is
    in ``samples`` (each shot's denominator and whether it is an order) and ``success_rate``."""
    rng = np.random.default_rng(seed)
    t = t or 2 * math.ceil(math.log2(N)) + 1
    Q = 2 ** t
    # the state sum_x |x>|a^x mod N>; measuring the work register first (it does not change the statistics of
    # the counting register) leaves a periodic comb; we keep the full marginal instead
    vals = [pow(a, x, N) for x in range(Q)]
    F = np.zeros(Q)
    for w in set(vals):
        comb = np.array([1.0 if v == w else 0.0 for v in vals])
        amp = np.fft.fft(comb) / Q                     # amplitudes after the inverse QFT, up to phase
        F += np.abs(amp) ** 2 * Q
    probs = F / F.sum()
    true_r = next(r for r in range(1, N) if pow(a, r, N) == 1)
    samples = rng.choice(Q, size=shots, p=probs)
    found = []
    for y in samples:
        fr = Fraction(int(y), Q).limit_denominator(N)
        r = fr.denominator
        found.append({"y": int(y), "fraction": f"{fr.numerator}/{fr.denominator}", "r": r,
                      "ok": pow(a, r, N) == 1})
    return {"a": a, "N": N, "t": t, "Q": Q, "r": true_r, "probs": probs.tolist(), "samples": found,
            "success_rate": sum(f["ok"] for f in found) / shots, "peaks": [int(round(k * Q / true_r))
                                                                           for k in range(true_r)]}


def shor(N: int, a: int, seed: int = 0) -> dict:
    """Order finding, then the classical last step: gcd(a^(r/2) +- 1, N) when r is even and a^(r/2) is not -1.
    The factors are computed from ``order_finding``'s true order ``r`` (found classically), not from the sampled
    measurements, so they do not depend on the seed; ``samples`` shows which shots would have yielded r."""
    o = order_finding(a, N, seed=seed)
    r = o["r"]
    factors = None
    if r % 2 == 0 and pow(a, r // 2, N) != N - 1:
        f1, f2 = math.gcd(pow(a, r // 2) - 1, N), math.gcd(pow(a, r // 2) + 1, N)
        factors = sorted({f1, f2})
    return {**o, "factors": factors}


# ---------------------------------------------------------------- Grover

def grover(n: int = 6, marked: int = 42, max_iters: int = 20) -> dict:
    """Success probability against the number of iterations: sin^2((2k + 1) theta) with sin theta = 1/sqrt(N);
    the best is about (pi/4) sqrt(N) iterations, and more overshoots."""
    N = 2 ** n
    theta = math.asin(1 / math.sqrt(N))
    s = State(n)
    for q in range(n):
        s.apply(H, q)
    uniform = s.v.copy()
    probs = [float(s.probs()[marked])]
    snaps = [s.v.real.tolist()]
    for k in range(max_iters):
        s.v[marked] *= -1                                 # the oracle: a reflection about the unmarked states
        s.v = 2 * uniform * (uniform.conj() @ s.v) - s.v  # the diffusion: a reflection about the uniform state
        probs.append(float(s.probs()[marked]))
        if k < 8:
            snaps.append(s.v.real.tolist())
    best = int(np.argmax(probs))
    return {"n": n, "N": N, "marked": marked, "theta": theta, "probs": probs, "best_iters": best,
            "predicted_iters": math.pi / (4 * theta) - 0.5, "p_best": probs[best],
            "formula": [math.sin((2 * k + 1) * theta) ** 2 for k in range(max_iters + 1)], "snapshots": snaps}


def grover_scaling(ns=(4, 6, 8, 10, 12, 14, 16)) -> list[dict]:
    rows = []
    for n in ns:
        N = 2 ** n
        theta = math.asin(1 / math.sqrt(N))
        k = round(math.pi / (4 * theta) - 0.5)
        rows.append({"n": n, "N": N, "iterations": k, "p": math.sin((2 * k + 1) * theta) ** 2,
                     "classical_expected": (N + 1) / 2})
    return rows


# ---------------------------------------------------------------- BB84

def bb84(n: int = 4000, eve: bool = False, seed: int = 0) -> dict:
    """Bennett and Brassard (1984): Alice sends random bits in random bases (Z or X); Bob measures in random bases;
    they keep the positions where the bases agree.  An eavesdropper who measures and resends in random bases
    causes errors in a quarter of the kept bits."""
    rng = np.random.default_rng(seed)
    bits = rng.integers(0, 2, n)
    abase = rng.integers(0, 2, n)
    bbase = rng.integers(0, 2, n)

    def measure(bit, prep, meas):
        return bit if prep == meas else int(rng.integers(0, 2))

    recv = []
    for b, a, bb in zip(bits, abase, bbase):
        if eve:
            e = int(rng.integers(0, 2))
            b2 = measure(b, a, e)
            recv.append(measure(b2, e, bb))
        else:
            recv.append(measure(b, a, bb))
    recv = np.array(recv)
    keep = abase == bbase
    err = float((recv[keep] != bits[keep]).mean())
    return {"n": n, "eve": eve, "kept": int(keep.sum()), "error_rate": err}


# ---------------------------------------------------------------- no-cloning

def no_cloning() -> dict:
    """A CNOT copies |0> and |1> into a blank qubit, but applied to |+> it makes a Bell pair, not |+>|+>: the
    fidelity with the intended two copies is 1/2."""
    s = State(2).apply(H, 0).cnot(0, 1)
    plus = np.array([1, 1]) / math.sqrt(2)
    target = np.kron(plus, plus)
    return {"fidelity": float(abs(np.vdot(target, s.v)) ** 2), "state": [float(a.real) for a in s.v]}


_ = (X, Z)

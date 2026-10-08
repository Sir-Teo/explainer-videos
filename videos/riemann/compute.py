"""Precompute every piece of real mathematics shown in the Riemann video.

    python -m videos.riemann.compute               # everything missing (~6 min on 4 cores)
    python -m videos.riemann.compute zeros mobius  # specific items
    python -m videos.riemann.compute --force       # recompute

Results are cached in ``.cache/riemann/<name>.npz``; scenes call ``load(name)``
and never evaluate zeta themselves.  Nothing here is a cartoon: the zeros are
mpmath's ``zetazero``, the staircases are exact prime counts, the Mertens walk
is the true Möbius function, and the Gauss sums are summed term by term.

Items:
    zeros       ordinates of the first 1000 nontrivial zeros of zeta (mpmath)
    primes      exact pi(10^k) for k <= 9 (sieve), pi(x) and psi(x) staircases, li(x)
    mobius      mu(n) and the Mertens function M(x) up to 10^7
    race        the mod-4 prime race pi(x;4,3) - pi(x;4,1) up to 10^7
    landscape   zeta(s) on a grid of the complex plane, for domain coloring
    hardy       Hardy's Z(t) = |zeta(1/2+it)| with the sign that makes it real
    riemann_pi  Riemann's explicit formula for pi(x), truncated at K zero pairs
    kummer      cubic Gauss (Kummer) sums sum_x e(x^3/p) for primes p = 1 mod 3
    toy_family  a toy "family of Möbius sums" twisted by quadratic symbols
    spectrum    the primes "played backwards": -sum Lambda(n) w(n) n^(-1/2) cos(g ln n) peaks at the zeros
"""

from __future__ import annotations

import argparse
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "riemann"
N_ZEROS = 1000

# pi(10^k), from OEIS A006880 (values for k >= 10 come from the literature:
# Deleglise-Rivat, Gourdon, Oliveira e Silva, Platt).  k <= 9 are recomputed
# below by sieving, and asserted equal.
PI_POWERS_OF_TEN = {
    1: 4, 2: 25, 3: 168, 4: 1229, 5: 9592, 6: 78498, 7: 664579, 8: 5761455, 9: 50847534,
    10: 455052511, 11: 4118054813, 12: 37607912018, 13: 346065536839, 14: 3204941750802,
    15: 29844570422669, 16: 279238341033925, 17: 2623557157654233, 18: 24739954287740860,
    19: 234057667276344607, 20: 2220819602560918840, 21: 21127269486018731928,
    22: 201467286689315906290, 23: 1925320391606803968923, 24: 18435599767349200867866,
}


# ---------------------------------------------------------------------------
# Number-theoretic building blocks (numpy)
# ---------------------------------------------------------------------------
def sieve(n: int) -> np.ndarray:
    """Boolean array is_prime[0..n]."""
    is_p = np.ones(n + 1, dtype=bool)
    is_p[:2] = False
    is_p[4::2] = False
    for p in range(3, int(n**0.5) + 1, 2):
        if is_p[p]:
            is_p[p * p :: 2 * p] = False
    return is_p


def prime_count_checkpoints(n: int, checkpoints: list[int]) -> dict[int, int]:
    """Exact pi(c) for each checkpoint c <= n, using an odd-only sieve (memory n/2 bytes)."""
    m = (n - 1) // 2  # index i <-> odd number 2i+1, i = 0..m
    odd = np.ones(m + 1, dtype=bool)
    odd[0] = False  # 1 is not prime
    r = int(n**0.5)
    for i in range(1, (r - 1) // 2 + 1):
        if odd[i]:
            p = 2 * i + 1
            odd[(p * p - 1) // 2 :: p] = False
    out = {}
    for c in checkpoints:
        out[c] = int(np.count_nonzero(odd[: (c - 1) // 2 + 1])) + (1 if c >= 2 else 0)
    return out


def mobius(n: int) -> np.ndarray:
    """mu[0..n] (mu[0] = 0)."""
    is_p = sieve(n)
    mu = np.ones(n + 1, dtype=np.int8)
    mu[0] = 0
    for p in np.flatnonzero(is_p):
        mu[p::p] *= -1
        if p * p <= n:
            mu[p * p :: p * p] = 0
    return mu


def li(x: float) -> float:
    import mpmath

    return float(mpmath.li(x))


# ---------------------------------------------------------------------------
# Items
# ---------------------------------------------------------------------------
def _zero(n: int) -> float:
    import mpmath

    mpmath.mp.dps = 20
    return float(mpmath.zetazero(n).imag)


def compute_zeros():
    with ProcessPoolExecutor(4) as ex:
        gammas = np.array(list(ex.map(_zero, range(1, N_ZEROS + 1), chunksize=25)))
    assert abs(gammas[0] - 14.134725141734693) < 1e-9
    assert np.all(np.diff(gammas) > 0)
    return {"gamma": gammas}


def compute_primes():
    import mpmath

    t = time.time()
    checks = [10**k for k in range(1, 10)]
    counts = prime_count_checkpoints(10**9, checks)
    for k in range(1, 10):
        assert counts[10**k] == PI_POWERS_OF_TEN[k], (k, counts[10**k])
    print(f"    sieve to 1e9 in {time.time() - t:.0f}s; pi(10^k) agree with OEIS A006880 for k <= 9")
    mpmath.mp.dps = 40
    ks = np.array(sorted(PI_POWERS_OF_TEN))
    pis = [str(PI_POWERS_OF_TEN[k]) for k in ks]
    lis = [mpmath.li(mpmath.mpf(10) ** int(k)) for k in ks]
    li_minus_pi = [str(int(mpmath.nint(L - PI_POWERS_OF_TEN[k]))) for L, k in zip(lis, ks)]

    N = 10**6
    is_p = sieve(N)
    primes = np.flatnonzero(is_p)
    # psi(x) jumps: log p at every prime power p^k
    pp, logs = [], []
    for p in primes[primes <= 10_000]:
        q = int(p)
        while q <= 10_000:
            pp.append(q)
            logs.append(np.log(p))
            q *= int(p)
    order = np.argsort(pp)
    xs = np.geomspace(2, N, 600)
    return {
        "k": ks,
        "pi": np.array(pis),
        "li_minus_pi": np.array(li_minus_pi),
        "primes": primes,
        "prime_powers": np.array(pp)[order],
        "prime_power_logs": np.array(logs)[order],
        "curve_x": xs,
        "curve_li": np.array([li(x) for x in xs]),
    }


def compute_mobius():
    N = 10**7
    mu = mobius(N)
    M = np.cumsum(mu, dtype=np.int64)
    # Store the full walk on a uniform grid fine enough for any chart, plus extremes.
    step = 100
    xs = np.arange(0, N + 1, step)
    ratio = np.abs(M[1:]) / np.sqrt(np.arange(1, N + 1))
    return {
        "mu_head": mu[:201].astype(np.int64),
        "M_head": M[:20001],
        "x": xs,
        "M": M[xs],
        "M_max_abs": np.array([int(np.abs(M).max())]),
        "max_ratio_beyond_200": np.array([float(ratio[199:].max())]),
        "count_nonzero_mu": np.array([int(np.count_nonzero(mu[1:]))]),
    }


def compute_race():
    N = 10**7
    primes = np.flatnonzero(sieve(N))
    r1 = np.cumsum(primes % 4 == 1)
    r3 = np.cumsum(primes % 4 == 3)
    lead = r3 - r1  # positive when the class 3 mod 4 is ahead
    first_flip = int(primes[np.argmax(lead < 0)])
    assert first_flip == 26861, first_flip  # Leech (1957)
    step = 50
    return {"p": primes[::step], "lead": lead[::step], "first_flip": np.array([first_flip]),
            "p_head": primes[primes <= 100_000], "lead_head": lead[primes <= 100_000],
            "n1": np.array([int(r1[-1])]), "n3": np.array([int(r3[-1])])}


LANDSCAPE = dict(sig=(-4.6, 3.0), t=(-3.0, 33.0), nx=1170, ny=900)


def _zeta_row(args):
    import mpmath

    mpmath.mp.dps = 15
    t, sigmas = args
    out = np.empty(len(sigmas), dtype=np.complex128)
    for i, s in enumerate(sigmas):
        if abs(s - 1) < 1e-9 and abs(t) < 1e-9:
            out[i] = np.inf
        else:
            out[i] = complex(mpmath.zeta(mpmath.mpc(s, t)))
    return out


def compute_landscape():
    g = LANDSCAPE
    sig = np.linspace(*g["sig"], g["nx"])
    ts = np.linspace(g["t"][1], g["t"][0], g["ny"])  # top row first
    with ProcessPoolExecutor(4) as ex:
        rows = list(ex.map(_zeta_row, [(t, sig) for t in ts], chunksize=8))
    Z = np.array(rows).astype(np.complex64)
    return {"Z": Z, "sig": np.array(g["sig"]), "t": np.array(g["t"])}


def compute_hardy():
    import mpmath

    mpmath.mp.dps = 15
    ts = np.linspace(0.0, 52.0, 2601)
    Z = np.array([float(mpmath.siegelz(t)) for t in ts])
    return {"t": ts, "Z": Z}


def _riemann_pi_terms(args):
    """sum over n<=3 of mu(n)/n * Ei(rho log x / n), for one zero rho, on a grid of x."""
    import mpmath

    mpmath.mp.dps = 15
    gamma, xs = args
    rho = mpmath.mpc(0.5, gamma)
    out = np.zeros(len(xs), dtype=np.complex128)
    for i, x in enumerate(xs):
        L = mpmath.log(x)
        acc = mpmath.ei(rho * L) - mpmath.ei(rho * L / 2) / 2 - mpmath.ei(rho * L / 3) / 3
        out[i] = complex(acc)
    return out


def riemann_R(x: float, terms: int = 60) -> float:
    """Riemann's R(x) = sum mu(n)/n li(x^(1/n)), via the Gram series."""
    import mpmath

    return float(mpmath.riemannr(x))


def compute_riemann_pi():
    """pi_K(x) = R(x) - sum_{k<=K} 2 Re R(x^rho_k) - 1/log x + arctan(pi/log x)/pi (Riesel-Göhl form),
    with R(x^rho) truncated to its first three Möbius terms (the rest are invisible at this scale)."""
    gam = load("zeros")["gamma"][:200]
    xs = np.linspace(2.0, 100.0, 1400)
    with ProcessPoolExecutor(4) as ex:
        terms = np.array(list(ex.map(_riemann_pi_terms, [(g, xs) for g in gam], chunksize=5)))
    R = np.array([riemann_R(x) for x in xs])
    L = np.log(xs)
    smooth = R - 1 / L + np.arctan(np.pi / L) / np.pi
    osc = 2 * np.real(terms)  # each row: one conjugate pair
    return {"x": xs, "smooth": smooth, "osc": osc}


def compute_kummer():
    P = 60_000
    primes = np.flatnonzero(sieve(P))
    primes = primes[primes % 3 == 1]
    S = np.empty(len(primes))
    for i, p in enumerate(primes):
        x = np.arange(p, dtype=np.int64)
        S[i] = np.cos(2 * np.pi * ((x * x % p) * x % p) / p).sum()
    norm = S / (2 * np.sqrt(primes))  # = cos(theta_p), theta_p the argument of the cubic Gauss sum
    assert np.all(np.abs(norm) <= 1 + 1e-9)
    return {"p": primes, "S": S, "cos": norm}


def _jacobi_table(primes, H):
    """For each odd prime p: Legendre symbol (u/p) for u = 0..H-1."""
    out = {}
    u = np.arange(H, dtype=np.int64)
    for p in primes:
        p = int(p)
        res = np.zeros(p, dtype=np.int8)
        sq = (np.arange(1, p, dtype=np.int64) ** 2) % p
        res[:] = -1
        res[sq] = 1
        res[0] = 0
        out[p] = res[u % p]
    return out


def compute_toy_family():
    """A_u = sum_{D < n <= 2D, n odd squarefree} mu(n) (u/n) W(n/D), u = 1..H  (Jacobi symbol)."""
    D, H = 4000, 3000
    mu = mobius(2 * D)
    is_p = sieve(2 * D)
    odd_primes = [int(p) for p in np.flatnonzero(is_p) if p > 2]
    table = _jacobi_table(odd_primes, H + 1)
    ns = np.arange(D + 1, 2 * D + 1)
    ns = ns[(ns % 2 == 1) & (mu[ns] != 0)]
    W = np.sin(np.pi * (ns / D - 1)) ** 2  # smooth bump on (D, 2D]
    A = np.zeros(H + 1)
    for n, w in zip(ns, W):
        sym = np.ones(H + 1, dtype=np.int8)
        m = int(n)
        for p in odd_primes:
            if p * p > m:
                break
            if m % p == 0:
                sym = sym * table[p]
                m //= p
        if m > 1:
            sym = sym * table[m]
        A += mu[n] * w * sym
    u = np.arange(H + 1)
    copies = np.array([p * p for p in odd_primes if p * p <= H])
    return {"u": u[1:], "A": A[1:], "D": np.array([D]), "H": np.array([H]), "copies": copies,
            "W2": np.array([float((W**2).sum())]), "n_terms": np.array([len(ns)])}


def compute_spectrum():
    """Fourier-transform the prime powers: f(g) = -sum_{n <= X} Lambda(n) w(n) n^(-1/2) cos(g ln n), with a
    smooth taper w(n) = cos^2(pi ln n / (2 ln X)).  By the explicit formula it has a peak at every zero ordinate."""
    X = 10**6
    primes = np.flatnonzero(sieve(X))
    ns, L = [], []
    for p in primes:
        q = int(p)
        while q <= X:
            ns.append(q)
            L.append(np.log(p))
            q *= int(p)
    ns, L = np.array(ns, dtype=float), np.array(L)
    w = np.cos(np.pi * np.log(ns) / np.log(X) / 2) ** 2
    coef = L * w / np.sqrt(ns)
    g = np.linspace(8, 60, 2200)  # below ~8 the pole at s = 1 dominates
    f = np.empty_like(g)
    for i in range(0, len(g), 200):
        f[i:i + 200] = -(coef * np.cos(np.outer(g[i:i + 200], np.log(ns)))).sum(axis=1)
    peaks = np.array([g[i] for i in range(1, len(f) - 1) if f[i] > f[i - 1] and f[i] > f[i + 1] and f[i] > 0.3 * f.max()])
    zeros = load("zeros")["gamma"]
    zeros = zeros[zeros < 60]
    assert len(peaks) == len(zeros) and np.all(np.abs(peaks - zeros) < 0.15), np.abs(peaks - zeros).max()
    return {"g": g, "f": f, "peaks": peaks, "X": np.array([X])}


ITEMS = {
    "zeros": compute_zeros,
    "primes": compute_primes,
    "mobius": compute_mobius,
    "race": compute_race,
    "landscape": compute_landscape,
    "hardy": compute_hardy,
    "riemann_pi": compute_riemann_pi,
    "kummer": compute_kummer,
    "toy_family": compute_toy_family,
    "spectrum": compute_spectrum,
}


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
_loaded: dict[str, dict] = {}


def path(name: str):
    return DATA_DIR / f"{name}.npz"


def load(name: str) -> dict:
    if name not in _loaded:
        p = path(name)
        if not p.exists():
            raise FileNotFoundError(f"Missing '{name}'. Run: python -m videos.riemann.compute {name}")
        with np.load(p, allow_pickle=False) as data:
            _loaded[name] = {k: data[k] for k in data.files}
    return _loaded[name]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", default=list(ITEMS))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name in args.names:
        if path(name).exists() and not args.force:
            print(f"  cached  {name}")
            continue
        t = time.time()
        print(f"  compute {name} ...", flush=True)
        out = ITEMS[name]()
        tmp = DATA_DIR / f"{name}.tmp.npz"
        np.savez_compressed(tmp, **out)
        tmp.replace(path(name))
        _loaded.pop(name, None)
        print(f"  done    {name} in {time.time() - t:.0f}s", flush=True)


if __name__ == "__main__":
    main()

"""Precompute everything numerical in Part 1 of the analysis series ("The Real Numbers and the Shape of Space").

    python -m videos.analysis1.compute            # everything missing (a few seconds)
    python -m videos.analysis1.compute cantor     # specific items
    python -m videos.analysis1.compute --force    # recompute

Results are cached in ``.cache/analysis1/<name>.npz``; scenes call ``load(name)``.  Every number the narration
quotes is computed here (exactly, with Python fractions and integers, wherever possible) and asserted against
the statement it illustrates; the scenes re-assert the ones they print.

Items:
    sawtooth   the hero function f(x) = (pi - x)/2 on (0, 2 pi) and its Fourier partial sums sum_{k<=n} sin(kx)/k
    hops       Rudin's map q = p - (p^2 - 2)/(p + 2) = (2p + 2)/(p + 2), from p = 1 upward and from p = 2 downward
    sqrt2      decimal nested intervals for sqrt 2 (40 digits) and bisection intervals (exact)
    diagonal   twelve seeded 0-1 sequences, and the diagonal sequence that differs from every one of them
    qorder     the rationals in (0, 1] listed by Cantor's zigzag (duplicates skipped)
    supdist    the sup distance between two functions on [0, 1], found by maximization
    cover      a random open cover of [0, 1] by 70 intervals, and the finite subcover the greedy algorithm finds
    cantor     the Cantor set's intervals to depth 12, the point 1/4, and the Cantor function at depth 14
    bumps      the moving tent bumps in C[0, 1]: pairwise sup distances
"""

from __future__ import annotations

import argparse
import math
import time
from fractions import Fraction

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "analysis1"


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
# The hero function: a sawtooth and its Fourier series
# ---------------------------------------------------------------------------
SAW_NS = [1, 2, 3, 5, 10, 20, 50, 200]


def saw(x):
    """(pi - x)/2 on (0, 2 pi), extended 2 pi-periodically, with value 0 at the jumps."""
    y = np.mod(x, 2 * np.pi)
    out = (np.pi - y) / 2
    return np.where((y == 0), 0.0, out)


def saw_partial(x, n):
    k = np.arange(1, n + 1)[:, None]
    return np.sum(np.sin(k * np.asarray(x)[None, :]) / k, axis=0)


def compute_sawtooth():
    x = np.linspace(-np.pi, 3 * np.pi, 4001)
    sums = np.array([saw_partial(x, n) for n in SAW_NS])
    # every partial sum vanishes at the jump x = 0, 2 pi (each sin(k x) does): the series picks the midpoint
    assert np.allclose(saw_partial(np.array([0.0, 2 * np.pi]), 200), 0.0, atol=1e-10)
    # away from the jump the partial sums converge to (pi - x)/2
    xx = np.array([1.0, 2.0, 4.0])
    err = np.abs(saw_partial(xx, 20000) - saw(xx)).max()
    assert err < 2e-4, err
    # Gibbs: the first peak of S_n near 0+ tends to Si(pi) = 1.85194, i.e. 8.95% of the jump (pi) above pi/2
    from scipy.special import sici
    si_pi = float(sici(np.pi)[0])
    n = 5000
    xs = np.linspace(0.5, 1.5, 2001) * np.pi / (n + 0.5)  # the first peak sits at x = pi / (n + 1/2)
    peak = float(np.max([np.sum(np.sin(np.arange(1, n + 1) * x) / np.arange(1, n + 1)) for x in xs]))
    assert abs(peak - si_pi) < 1e-3, (peak, si_pi)
    assert abs((si_pi - np.pi / 2) / np.pi - 0.0895) < 5e-4  # the overshoot is 8.95% of the jump
    return dict(x=x, sums=sums, ns=np.array(SAW_NS), peak=peak)


# ---------------------------------------------------------------------------
# Rudin 1.1: the set {p : p^2 < 2} has no largest element
# ---------------------------------------------------------------------------
def hop(p: Fraction) -> Fraction:
    return p - (p * p - 2) / (p + 2)


def compute_hops():
    up, down = [Fraction(1)], [Fraction(2)]
    for _ in range(9):
        up.append(hop(up[-1]))
        down.append(hop(down[-1]))
    for a, b in zip(up, up[1:]):
        assert a * a < 2 and b * b < 2 and b > a  # stays below sqrt 2 and climbs
        assert b == (2 * a + 2) / (a + 2)
        assert b * b - 2 == 2 * (a * a - 2) / (a + 2) ** 2  # the identity that proves it
    for a, b in zip(down, down[1:]):
        assert a * a > 2 and b * b > 2 and b < a  # stays above sqrt 2 and descends
    assert up[1:5] == [Fraction(4, 3), Fraction(7, 5), Fraction(24, 17), Fraction(41, 29)]
    assert down[1:4] == [Fraction(3, 2), Fraction(10, 7), Fraction(17, 12)]
    num = lambda fs: np.array([f.numerator for f in fs], dtype=object)  # noqa: E731
    den = lambda fs: np.array([f.denominator for f in fs], dtype=object)  # noqa: E731
    return dict(up_n=num(up), up_d=den(up), down_n=num(down), down_d=den(down),
                up_v=np.array([float(f) for f in up]), down_v=np.array([float(f) for f in down]))


# ---------------------------------------------------------------------------
# sqrt 2: decimal digits as nested intervals, and bisection
# ---------------------------------------------------------------------------
def compute_sqrt2():
    digits = 40
    s = math.isqrt(2 * 10 ** (2 * digits))  # floor(sqrt 2 * 10^digits)
    dec = f"1.{str(s)[1:]}"
    assert dec.startswith("1.41421356237309504880")
    lo = np.array([s // 10 ** (digits - k) for k in range(digits + 1)], dtype=object)  # floor(sqrt2 * 10^k)
    for k in range(digits + 1):  # [lo/10^k, (lo+1)/10^k] contains sqrt 2: lo^2 <= 2*10^(2k) < (lo+1)^2
        assert lo[k] ** 2 <= 2 * 10 ** (2 * k) < (lo[k] + 1) ** 2
    # bisection on [1, 2] for x^2 - 2 (exact dyadic endpoints)
    a, b = Fraction(1), Fraction(2)
    bis = [(a, b)]
    for _ in range(30):
        m = (a + b) / 2
        if m * m < 2:
            a = m
        else:
            b = m
        bis.append((a, b))
        assert a * a < 2 < b * b
    return dict(dec=np.array(dec), lo=lo, bis_a=np.array([float(x) for x, _ in bis]),
                bis_b=np.array([float(y) for _, y in bis]))


# ---------------------------------------------------------------------------
# Cantor's diagonal
# ---------------------------------------------------------------------------
DIAG_ROWS, DIAG_COLS, DIAG_SEED = 12, 16, 2


def compute_diagonal():
    rows = rng(DIAG_SEED).integers(0, 2, size=(DIAG_ROWS, DIAG_COLS))
    diag = np.array([1 - rows[i, i] for i in range(DIAG_ROWS)])
    for i in range(DIAG_ROWS):
        assert diag[i] != rows[i, i]  # differs from row i in place i
    return dict(rows=rows, diag=diag)


# ---------------------------------------------------------------------------
# The rationals, listed by the zigzag
# ---------------------------------------------------------------------------
def compute_qorder():
    """Walk the grid of p/q (p, q >= 1) by anti-diagonals p + q = 2, 3, ...; keep fractions in lowest terms."""
    seen, order, skipped = set(), [], []
    s = 2
    while len(order) < 40:
        for q in range(1, s):
            p = s - q
            f = Fraction(p, q)
            if f in seen:
                skipped.append((p, q))
            else:
                seen.add(f)
                order.append((p, q))
        s += 1
    assert order[:6] == [(1, 1), (2, 1), (1, 2), (3, 1), (1, 3), (4, 1)]
    assert (2, 2) in skipped
    return dict(order=np.array(order), skipped=np.array(skipped))


# ---------------------------------------------------------------------------
# The sup distance between two functions
# ---------------------------------------------------------------------------
def sd_f(x):
    return 0.25 + 0.5 * x ** 2


def sd_g(x):
    return 0.55 + 0.25 * np.sin(7 * x)


def compute_supdist():
    from scipy.optimize import minimize_scalar
    x = np.linspace(0, 1, 200001)
    d = np.abs(sd_f(x) - sd_g(x))
    i = int(np.argmax(d))
    lo, hi = x[max(0, i - 10)], x[min(len(x) - 1, i + 10)]
    r = minimize_scalar(lambda t: -abs(sd_f(t) - sd_g(t)), bounds=(lo, hi), method="bounded",
                        options=dict(xatol=1e-12))
    xs, ds = float(r.x), float(-r.fun)
    assert abs(ds - d.max()) < 1e-6
    return dict(x_star=xs, d_star=ds)


# ---------------------------------------------------------------------------
# A random open cover of [0, 1] and a finite subcover
# ---------------------------------------------------------------------------
COVER_SEED, COVER_N = 11, 70


def compute_cover():
    r = rng(COVER_SEED)
    grid = np.linspace(0, 1, 100001)
    while True:
        c = r.uniform(-0.03, 1.03, COVER_N)
        w = r.uniform(0.015, 0.09, COVER_N)
        a, b = c - w, c + w
        covered = ((grid[None, :] > a[:, None] + 1e-4) & (grid[None, :] < b[:, None] - 1e-4)).any(axis=0)
        if covered.all():
            break
    # greedy: from the left end, always take the interval containing x that reaches furthest right
    chosen, x = [], 0.0
    while True:
        inside = np.where((a < x) & (b > x))[0]
        assert len(inside), x
        j = inside[np.argmax(b[inside])]
        chosen.append(int(j))
        if b[j] > 1:
            break
        x = b[j]
    sub = np.array(chosen)
    cov = ((grid[None, :] > a[sub, None]) & (grid[None, :] < b[sub, None])).any(axis=0)
    assert cov.all()
    return dict(a=a, b=b, chosen=sub)


# ---------------------------------------------------------------------------
# The Cantor set and the Cantor function
# ---------------------------------------------------------------------------
CANTOR_DEPTH = 12


def cantor_intervals(n: int) -> np.ndarray:
    iv = np.array([[0.0, 1.0]])
    for _ in range(n):
        a, b = iv[:, 0], iv[:, 1]
        t = (b - a) / 3
        iv = np.stack([np.stack([a, a + t], 1), np.stack([b - t, b], 1)], 1).reshape(-1, 2)
    return iv


def cantor_function(x: np.ndarray, depth: int = 40) -> np.ndarray:
    """The devil's staircase, by its ternary-digit rule (exact up to depth digits)."""
    x = np.clip(np.asarray(x, float), 0, 1)
    out = np.zeros_like(x)
    y = x.copy()
    scale = 0.5
    done = np.zeros(x.shape, bool)
    for _ in range(depth):
        y = y * 3
        d = np.floor(np.minimum(y, 2.999999999999))
        y = y - d
        hit1 = (d == 1) & ~done
        out = np.where(hit1, out + scale, out)
        done |= hit1
        out = np.where(~done & (d == 2), out + scale, out)
        scale /= 2
    return np.where(x >= 1, 1.0, out)


def compute_cantor():
    out = {}
    for n in range(CANTOR_DEPTH + 1):
        iv = cantor_intervals(n)
        assert len(iv) == 2**n
        assert abs((iv[:, 1] - iv[:, 0]).sum() - (2 / 3) ** n) < 1e-12
        out[f"iv{n}"] = iv
    # 1/4 = 0.020202..._3 lies in the Cantor set and is never an endpoint; zooming about it by 9 repeats the picture
    q = Fraction(1, 4)
    digits = []
    for _ in range(12):
        q *= 3
        d = q.numerator // q.denominator
        digits.append(d)
        q -= d
    assert digits == [0, 2] * 6
    iv = out[f"iv{CANTOR_DEPTH}"]
    assert ((iv[:, 0] <= 0.25) & (iv[:, 1] >= 0.25)).any()
    assert np.abs(iv - 0.25).min() > 1e-9  # 1/4 is never an endpoint (endpoints are k / 3^n)
    xs = np.linspace(0, 1, 6001)
    F = cantor_function(xs)
    assert abs(cantor_function(np.array([0.25]))[0] - 1 / 3) < 1e-12  # F(1/4) = 0.0101..._2 = 1/3
    assert np.all(np.diff(F) >= -1e-12)
    out.update(x=xs, F=F, quarter_digits=np.array(digits))
    return out


# ---------------------------------------------------------------------------
# Bumps in C[0, 1]: closed and bounded, not compact
# ---------------------------------------------------------------------------
def tent(x, n):
    """Height-1 tent on [1/(n+1), 1/n], zero elsewhere."""
    a, b = 1 / (n + 1), 1 / n
    m = (a + b) / 2
    return np.clip(1 - np.abs(x - m) / ((b - a) / 2), 0, None) * ((x >= a) & (x <= b))


def compute_bumps():
    x = np.unique(np.concatenate([np.linspace(0, 1, 200001)] + [[1 / (n + 1), 1 / n, (1 / (n + 1) + 1 / n) / 2]
                                                                 for n in range(1, 13)]))
    T = np.array([tent(x, n) for n in range(1, 13)])
    D = np.array([[np.abs(T[i] - T[j]).max() for j in range(12)] for i in range(12)])
    off = D[~np.eye(12, dtype=bool)]
    assert np.allclose(off, 1.0, atol=1e-9), off.min()
    assert np.allclose(T.max(axis=1), 1.0)
    return dict(D=D)


ITEMS = {
    "sawtooth": compute_sawtooth,
    "hops": compute_hops,
    "sqrt2": compute_sqrt2,
    "diagonal": compute_diagonal,
    "qorder": compute_qorder,
    "supdist": compute_supdist,
    "cover": compute_cover,
    "cantor": compute_cantor,
    "bumps": compute_bumps,
}

_loaded: dict[str, dict] = {}


def path(name: str):
    return DATA_DIR / f"{name}.npz"


def load(name: str) -> dict:
    if name not in _loaded:
        p = path(name)
        if not p.exists():
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(p, **ITEMS[name]())
        with np.load(p, allow_pickle=True) as z:
            _loaded[name] = {k: z[k] for k in z.files}
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
        print(f"  done    {name} in {time.time() - t:.1f}s", flush=True)


if __name__ == "__main__":
    main()

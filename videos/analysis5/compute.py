"""Precompute everything numerical in Part 5 of the analysis series ("Measure: The Lebesgue Integral").

    python -m videos.analysis5.compute            # everything missing (seconds)
    python -m videos.analysis5.compute fubini     # specific items
    python -m videos.analysis5.compute --force    # recompute

Results are cached in ``.cache/analysis5/<name>.npz``; scenes call ``load(name)``.  Every number the narration
quotes is computed here and asserted against the statement it illustrates.

Items:
    escapes     the spike n 1_(0, 1/n], the runaway 1_[n, n+1], the spreading (1/n) 1_[0, n]: integral 1, limit 0
    cantor      covers of the Cantor set (total (2/3)^n) and of the rationals (total eps); the fat Cantor set
                (removed lengths 4^-n, measure 1/2, no interval)
    vitali      the orbit of rotation by 1 radian on the circle: dense (its largest gap)
    simple      Rudin 1.17's dyadic simple functions for f = x^2 + sin 5x + 1: sup |s_n - f| <= 2^-n
    mct         min(1/sqrt x, n) on (0, 1]: integrals 2 - 1/n increasing to 2
    dct         n sin(x/n)/x -> 1 under the lid 1 (integrals n Si(1/n)); the typewriter; Egorov for x^n
    riesz       the Riesz construction for the Riemann integral: mu(V) = sup Lambda f over f < V, for random open V
    lusin       a 100-step function repaired to a continuous one off a set of measure < eps
    fubini      (x^2 - y^2)/(x^2 + y^2)^2 on the unit square: iterated integrals +pi/4 and -pi/4
    convolution ||f * g||_1 <= ||f||_1 ||g||_1 for random functions; the layer-cake formula
"""

from __future__ import annotations

import argparse
import math
import time
from fractions import Fraction

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "analysis5"


def trap(y, x):
    y, x = np.asarray(y, float), np.asarray(x, float)
    return float(np.sum((y[1:] + y[:-1]) * np.diff(x)) / 2)


# ---------------------------------------------------------------------------
def compute_escapes():
    ns = np.array([1, 2, 4, 8, 16, 32])
    # exact integrals and pointwise limits
    spike = [Fraction(n) * Fraction(1, n) for n in ns]  # height n on (0, 1/n]
    run = [Fraction(1) for _ in ns]
    spread = [Fraction(1, n) * n for n in ns]
    assert all(v == 1 for v in spike + run + spread)
    return dict(ns=ns)


def cantor_intervals(depth):
    iv = [(0.0, 1.0)]
    for _ in range(depth):
        iv = [p for a, b in iv for p in ((a, a + (b - a) / 3), (b - (b - a) / 3, b))]
    return np.array(iv)


def fat_cantor(depth):
    """Remove, at stage n = 1, 2, ..., an open middle interval of length 4^-n from each of the 2^(n-1) pieces."""
    iv = [(0.0, 1.0)]
    removed = []
    for n in range(1, depth + 1):
        L = 4.0**-n
        new = []
        for a, b in iv:
            m = (a + b) / 2
            removed.append((m - L / 2, m + L / 2))
            new += [(a, m - L / 2), (m + L / 2, b)]
        iv = new
    return np.array(iv), np.array(removed)


def compute_cantor():
    depths = np.arange(0, 9)
    tot = np.array([np.diff(cantor_intervals(int(d)), axis=1).sum() for d in depths])
    assert np.allclose(tot, (2 / 3) ** depths)
    keep, removed = fat_cantor(12)
    lengths = np.diff(keep, axis=1).ravel()
    measure = lengths.sum()
    assert abs(measure - (0.5 + 0.5 * 0.5**12)) < 1e-12 and lengths.max() < 1e-3
    # the k-th rational (by Cantor's listing) covered by an interval of length eps / 2^k
    rats, seen = [], set()
    for q in range(1, 40):
        for p in range(0, q + 1):
            fr = Fraction(p, q)
            if fr not in seen:
                seen.add(fr)
                rats.append(float(fr))
    rats = np.array(rats)
    eps = 0.5
    cover = eps / 2.0 ** np.arange(1, len(rats) + 1)
    assert cover.sum() <= eps  # eps (1 - 2^-N)
    stage_keep = [fat_cantor(d)[0] for d in range(0, 6)]
    stage_meas = np.array([np.diff(k, axis=1).sum() for k in stage_keep])
    assert np.allclose(stage_meas, 0.5 + 0.5 * 0.5 ** np.arange(0, 6))
    return dict(depths=depths, tot=tot, fat_keep=keep, fat_removed=removed, fat_measure=measure, rats=rats,
                cover=cover, eps=eps, stage_meas=stage_meas, **{f"fat{d}": k for d, k in enumerate(stage_keep)})


# ---------------------------------------------------------------------------
def compute_vitali():
    N = 2000
    ang = np.mod(np.arange(N), 2 * np.pi)
    s = np.sort(ang)
    gaps = np.diff(np.concatenate([s, [s[0] + 2 * np.pi]]))
    assert gaps.max() < 0.02  # every point of the circle is within 0.01 of the orbit's first 2000 points
    Ns = np.array([10, 50, 200, 1000, 2000])
    maxgap = []
    for n in Ns:
        s_ = np.sort(ang[:n])
        maxgap.append(np.diff(np.concatenate([s_, [s_[0] + 2 * np.pi]])).max())
    maxgap = np.array(maxgap)
    assert np.all(np.diff(maxgap) <= 1e-12)
    return dict(ang=ang, maxgap=maxgap, Ns=Ns)


# ---------------------------------------------------------------------------
def compute_simple():
    x = np.linspace(0, 2, 4001)
    f = x**2 + np.sin(5 * x) + 1
    assert f.min() >= 0
    S, errs = [], []
    for n in range(1, 9):
        s = np.where(f < n, np.floor(f * 2**n) / 2**n, n)
        S.append(s)
        errs.append(np.abs(s - f)[f < n].max())
        assert np.all(s <= f + 1e-15) and errs[-1] <= 2.0**-n
        if n > 1:
            assert np.all(s >= S[-2] - 1e-15)  # increasing in n
    return dict(x=x, f=f, S=np.array(S), errs=np.array(errs))


# ---------------------------------------------------------------------------
def compute_mct():
    ns = np.arange(1, 41)
    ints = 2 - 1 / ns  # int_0^1 min(x^-1/2, n) dx = n * n^-2 + (2 - 2/n)
    x = np.linspace(1e-8, 1, 2_000_001)
    for n in (1, 2, 5, 10):
        assert abs(trap(np.minimum(x**-0.5, n), x) - (2 - 1 / n)) < 2e-3
    assert np.all(np.diff(ints) > 0)
    return dict(ns=ns, ints=ints)


def compute_dct():
    from scipy.special import sici
    ns = np.array([1, 2, 3, 5, 10, 30, 100])
    ints = np.array([n * sici(1 / n)[0] for n in ns])  # int_0^1 sin(x/n)/(x/n) dx
    assert np.all(np.diff(ints) > 0) and abs(ints[-1] - 1) < 1e-5 and np.all(ints < 1)
    # the typewriter: f_k = indicator of [j 2^-m, (j + 1) 2^-m] for k = 2^m + j
    xs = np.linspace(0, 1, 997)[1:-1]
    hits = np.zeros_like(xs)
    norms = []
    for m in range(0, 10):
        for j in range(2**m):
            on = (xs >= j / 2**m) & (xs <= (j + 1) / 2**m)
            hits += on
            norms.append(2.0**-m)
    assert hits.min() >= 10  # every x is hit once in every generation: limsup f_k(x) = 1
    norms = np.array(norms)
    # Egorov for x^n on [0, 1]: uniform off [1 - eps, 1]
    eps = 0.05
    egorov = np.array([(1 - eps) ** n for n in (10, 50, 100, 200)])
    assert np.all(np.diff(egorov) < 0) and egorov[-1] < 1e-4
    return dict(ns=ns, ints=ints, norms=norms, egorov=egorov, eps=eps)


# ---------------------------------------------------------------------------
def compute_riesz():
    """Lambda f = int_0^1 f.  For an open set V (a finite union of intervals), f_k = the trapezoid that is 1 on V
    minus 1/k-collars and 0 off V has f_k < V and Lambda f_k -> length(V) (Rudin 2.14's definition of mu(V))."""
    rng = np.random.default_rng(2)
    trials = []
    for _ in range(6):
        a = np.sort(rng.uniform(0, 1, 8))
        iv = [(a[i], a[i + 1]) for i in range(0, 8, 2)]
        length = sum(b - c for c, b in iv)
        lams = []
        for k in (5, 20, 100, 1000, 10**7):
            lam = 0.0
            for c, b in iv:
                w = b - c
                col = min(1 / k, w / 2)
                lam += w - col  # trapezoid: full height on the middle, linear ramps of width col at each end
            lams.append(lam)
        assert all(x <= length + 1e-15 for x in lams) and abs(lams[-1] - length) < 1e-6
        trials.append((length, *lams))
    return dict(trials=np.array(trials), ks=np.array([5, 20, 100, 1000, 10**7]))


# ---------------------------------------------------------------------------
def compute_lusin():
    rng = np.random.default_rng(11)
    jumps = np.sort(rng.choice(np.arange(1, 1000), 99, replace=False)) / 1000  # at least 0.001 apart
    vals = rng.uniform(0, 1, 100)
    eps = 0.05
    delta = eps / (2 * 99) * 0.99  # ramp half-width around each jump
    x = np.linspace(0, 1, 200001)
    idx = np.searchsorted(jumps, x)
    f = vals[idx]
    g = f.copy()
    for k, t in enumerate(jumps):
        m = (x > t - delta) & (x < t + delta)
        g[m] = vals[k] + (vals[k + 1] - vals[k]) * (x[m] - (t - delta)) / (2 * delta)
    bad = np.mean(np.abs(g - f) > 1e-12)
    # g is continuous: its steps on the grid are at most (largest jump) / (2 delta) * dx; f and g differ on < eps
    assert bad < eps and np.abs(np.diff(g)).max() <= (x[1] - x[0]) / (2 * delta) + 1e-12
    return dict(x=x[::10], f=f[::10], g=g[::10], bad=bad, eps=eps, jumps=jumps, vals=vals, delta=delta)


# ---------------------------------------------------------------------------
def compute_fubini():
    from scipy.integrate import quad
    inner_y = lambda x: 1 / (1 + x * x)  # noqa: E731  int_0^1 (x^2 - y^2)/(x^2 + y^2)^2 dy = 1/(1 + x^2)
    for x0 in (0.2, 0.5, 0.9):
        num, _ = quad(lambda y: (x0 * x0 - y * y) / (x0 * x0 + y * y) ** 2, 0, 1, epsabs=1e-12)
        assert abs(num - inner_y(x0)) < 1e-9
    I1, _ = quad(inner_y, 0, 1)
    I2, _ = quad(lambda y: -1 / (1 + y * y), 0, 1)
    assert abs(I1 - math.pi / 4) < 1e-12 and abs(I2 + math.pi / 4) < 1e-12
    # not absolutely integrable: int int |f| = infinity (the integral over [eps, 1]^2 of |f| grows like log(1/eps))
    absint = []
    for e in (1e-1, 1e-2, 1e-3):
        g = np.linspace(e, 1, 1201)
        X, Y = np.meshgrid(g, g)
        F = np.abs((X**2 - Y**2) / (X**2 + Y**2) ** 2)
        absint.append(np.trapezoid(np.trapezoid(F, g, axis=1), g))
    absint = np.array(absint)
    assert np.all(np.diff(absint) > 0.5)
    return dict(I1=I1, I2=I2, absint=absint)


# ---------------------------------------------------------------------------
def compute_convolution():
    rng = np.random.default_rng(8)
    x = np.linspace(-6, 6, 4801)
    dx = x[1] - x[0]
    ratios = []
    for _ in range(20):
        f = sum(rng.normal() * np.exp(-((x - rng.uniform(-3, 3)) ** 2) / rng.uniform(0.05, 0.8)) for _ in range(4))
        g = sum(rng.normal() * np.exp(-((x - rng.uniform(-2, 2)) ** 2) / rng.uniform(0.05, 0.8)) for _ in range(3))
        h = np.convolve(f, g, mode="same") * dx
        ratios.append(np.abs(h).sum() * dx / (np.abs(f).sum() * dx * np.abs(g).sum() * dx))
    ratios = np.array(ratios)
    assert np.all(ratios <= 1 + 1e-6)
    # the layer cake: int f = int_0^inf m{f > t} dt for f >= 0
    f = np.exp(-x * x) * (1.2 + np.sin(3 * x)) ** 2
    ts = np.linspace(0, f.max(), 400001)
    fs = np.sort(f)
    mu = (len(f) - np.searchsorted(fs, ts, side="right")) * dx  # m{f > t}, exactly, for the sampled f
    lhs, rhs = f.sum() * dx, trap(mu, ts)
    assert abs(lhs - rhs) < 1e-4 * lhs
    # the sawtooth integrated term by term on [0, 1] (its partial sums are bounded by Si(pi) < 2: a constant lid)
    from scipy.special import sici
    # 10^7 terms (the tail after N terms is about 1/N), summed in chunks; the narration says "six decimal places"
    termwise = 0.0
    for k0 in range(1, 10_000_001, 1_000_000):
        K = np.arange(k0, k0 + 1_000_000, dtype=float)
        termwise += float(np.sum((1 - np.cos(K)) / K**2))
    exact = math.pi / 2 - 0.25  # int_0^1 (pi - t)/2 dt
    assert abs(termwise - exact) < 5e-7 and f"{termwise:.6f}" == f"{exact:.6f}" and sici(math.pi)[0] < 2
    xs = np.linspace(1e-4, 2 * np.pi - 1e-4, 20001)
    sups = np.array([np.abs(np.cumsum(np.sin(np.outer(np.arange(1, N + 1), xs[::20])) / np.arange(1, N + 1)[:, None],
                                      axis=0)).max() for N in (10, 100, 400)])
    assert np.all(sups < 2)
    return dict(ratios=ratios, x=x, f=f, ts=ts[::400], mu=mu[::400], lhs=lhs, rhs=rhs, termwise=termwise, exact=exact,
                sups=sups, si_pi=sici(math.pi)[0])


def compute_improper():
    """sin x / x: the improper Riemann integral converges to pi/2, but int |sin x|/x diverges like (2/pi) log N,
    so sin x / x is not Lebesgue integrable on (0, infinity)."""
    from scipy.special import sici
    Ns = np.array([10, 100, 1000, 10000])
    si = np.array([sici(float(N))[0] for N in Ns])
    absint = []
    for N in Ns:
        x = np.linspace(1e-9, N, int(N * 400) + 1)
        y = np.abs(np.sin(x)) / x
        absint.append(trap(y, x))
    absint = np.array(absint)
    assert abs(si[-1] - math.pi / 2) < 1e-3 and np.all(np.diff(absint) > 1.4)
    assert np.allclose(np.diff(absint), 2 / math.pi * math.log(10), atol=0.03)
    return dict(Ns=Ns, si=si, absint=absint)


ITEMS = {
    "escapes": compute_escapes,
    "cantor": compute_cantor,
    "vitali": compute_vitali,
    "simple": compute_simple,
    "mct": compute_mct,
    "dct": compute_dct,
    "riesz": compute_riesz,
    "lusin": compute_lusin,
    "fubini": compute_fubini,
    "convolution": compute_convolution,
    "improper": compute_improper,
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

"""Precompute everything numerical in Part 2 of the analysis series ("Limits: Sequences, Series, Continuity and the
Derivative").

    python -m videos.analysis2.compute            # everything missing (about a minute)
    python -m videos.analysis2.compute rearrange  # specific items
    python -m videos.analysis2.compute --force    # recompute

Results are cached in ``.cache/analysis2/<name>.npz``; scenes call ``load(name)``.  Every number the narration
quotes is computed here and asserted against the statement it illustrates.

Items:
    rearrange   Riemann's greedy rearrangement of 1 - 1/2 + 1/3 - ... toward pi, toward -1, and off to +infinity
    sequences   1/n, (-1)^n/n, n^(1/n), (1 + 1/n)^n: thresholds N for given epsilons, and the limits
    limsup      a_n = (-1)^n (1 + 1/n): running sups and infs of the tails
    pseries     partial sums of sum 1/n^p for p = 1, 1.5, 2 up to 10^6, against ln n + gamma, zeta(1.5), pi^2/6
    etail       q! (e - s_q) for q = 1 .. 15, in (0, 1/q): the irrationality of e
    tests       Rudin's example 3.35: ratios and roots of 1/2 + 1/3 + 1/2^2 + 1/3^2 + ...
    power       partial sums of sum z^n / n at |z| = 0.9, 1 (z = -1 and z = 1) and 1.1
    product     the Cauchy product of sum (-1)^n / sqrt(n + 1) with itself: |c_n| >= 2(n + 1)/(n + 2)
    deltas      largest deltas: x^2 at 3; 1/x across (0, 1); sqrt x on [0, 1] (all with eps = 0.1)
    wiggle      x^2 sin(1/x): difference quotients at 0, and the derivative taking every value in [-1, 1] near 0
    taylor      Taylor polynomials of e^x, sin x and 1/(1 + x^2); Lagrange's bound; e^(-1/x^2) and its flat series
"""

from __future__ import annotations

import argparse
import math
import time

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "analysis2"


# ---------------------------------------------------------------------------
# Riemann's rearrangement
# ---------------------------------------------------------------------------
def greedy(target_fn, n_terms: int):
    """Rearrange 1 - 1/2 + 1/3 - ...: take positive terms (1, 1/3, 1/5, ...) while the partial sum is <= the
    current target, negative terms (-1/2, -1/4, ...) while it is above.  ``target_fn(k)`` is the target after k
    terms (a constant, or a staircase to infinity).  Returns the terms used (signed) and partial sums."""
    p, q = 1, 2  # next odd and next even denominator
    s = 0.0
    terms = np.empty(n_terms)
    sums = np.empty(n_terms)
    for k in range(n_terms):
        if s <= target_fn(k):
            t = 1.0 / p
            p += 2
        else:
            t = -1.0 / q
            q += 2
        s += t
        terms[k] = t
        sums[k] = s
    return terms, sums


def compute_rearrange():
    N = 1_000_000
    t_pi, s_pi = greedy(lambda k: math.pi, N)
    t_m1, s_m1 = greedy(lambda k: -1.0, N)

    # off to infinity: aim at 1, then 2, then 3, ... (each step taking one negative term to prove we use them all)
    def stair(k, _state={"target": 1.0, "k": -1}):
        return 1.0 + math.floor(math.log1p(k) * 1.2)

    t_inf, s_inf = greedy(stair, 200_000)
    # the overshoot after the first crossing is at most the size of the last term used, so it shrinks to 0
    last_cross = np.where(np.diff(np.sign(s_pi - math.pi)) != 0)[0]
    assert len(last_cross) > 100
    err_pi = abs(s_pi[-1] - math.pi)
    err_m1 = abs(s_m1[-1] + 1.0)
    assert err_pi < 1e-5 and err_m1 < 1e-5, (err_pi, err_m1)
    k0 = last_cross[10]
    assert np.all(np.abs(s_pi[k0:] - math.pi) <= np.abs(t_pi[k0:]).max() + 1e-15)
    # every term of the original series is used: the counts of positive and negative terms both grow without bound
    n_pos, n_neg = int((t_pi > 0).sum()), int((t_pi < 0).sum())
    assert n_pos > 1000 and n_neg > 1000
    # Pringsheim: taking p positive terms per q negative ones sums to ln 2 + (1/2) ln(p / q); for pi, p/q = e^(2(pi - ln 2))
    ratio_pi = n_pos / n_neg
    assert abs(ratio_pi / math.exp(2 * (math.pi - math.log(2))) - 1) < 0.01, ratio_pi
    # the natural order sums to ln 2
    k = np.arange(1, 2_000_001)
    s_nat = np.cumsum((-1.0) ** (k + 1) / k)
    assert abs(s_nat[-1] - math.log(2)) < 1e-6
    keep = 4000
    return dict(t_pi=t_pi[:keep], s_pi=s_pi[:keep], t_m1=t_m1[:keep], s_m1=s_m1[:keep], t_inf=t_inf[:keep],
                s_inf=s_inf[:keep], final_pi=s_pi[-1], final_m1=s_m1[-1], n_pos=n_pos, n_neg=n_neg, ratio_pi=ratio_pi,
                s_nat=s_nat[:keep], inf_max=s_inf.max())


# ---------------------------------------------------------------------------
# Sequences
# ---------------------------------------------------------------------------
def compute_sequences():
    n = np.arange(1, 1_000_001, dtype=float)
    a = 1 / n
    # |1/n| < 0.01 exactly when n > 100: the smallest working N is 100
    assert np.where(np.abs(a) >= 0.01)[0].max() + 1 == 100
    b = (-1.0) ** n / n
    assert np.where(np.abs(b) >= 0.01)[0].max() + 1 == 100
    r = n ** (1 / n)
    assert abs(r[-1] - 1) < 2e-5 and r[2] == r.max()  # n^(1/n) peaks at n = 3, then decreases to 1
    e_seq = (1 + 1 / n) ** n
    assert abs(e_seq[-1] - math.e) < 2e-6
    idx = np.unique(np.round(np.logspace(0, 6, 400)).astype(int)) - 1
    return dict(n=n[idx], r=r[idx], e_seq=e_seq[idx], a=a[:60], b=b[:60])


def compute_limsup():
    n = np.arange(1, 81, dtype=float)
    a = (-1.0) ** n * (1 + 1 / n)
    sup_tail = np.array([a[k:].max() for k in range(len(a))])
    inf_tail = np.array([a[k:].min() for k in range(len(a))])
    # the true tail sups of the infinite sequence: for even n >= k, 1 + 1/n, largest at the first even index >= k
    true_sup = np.array([1 + 1 / (k + 1 if (k + 1) % 2 == 0 else k + 2) for k in range(len(a))])
    assert np.allclose(sup_tail[:60], true_sup[:60])
    assert abs(sup_tail[60] - 1) < 0.02 and abs(inf_tail[60] + 1) < 0.02
    return dict(n=n, a=a, sup_tail=sup_tail, inf_tail=inf_tail)


# ---------------------------------------------------------------------------
# Series
# ---------------------------------------------------------------------------
def compute_pseries():
    N = 1_000_000
    n = np.arange(1, N + 1, dtype=float)
    out = {}
    for p, key in ((1.0, "p1"), (1.5, "p15"), (2.0, "p2")):
        out[key] = np.cumsum(1 / n**p)
    gamma = 0.5772156649015329
    assert abs(out["p1"][-1] - (math.log(N) + gamma)) < 1e-6
    assert abs(out["p2"][-1] - math.pi**2 / 6) < 1.1e-6
    zeta15 = 2.612375348685488
    assert abs(out["p15"][-1] - zeta15) < 2.1e-3  # the tail is ~ 2 / sqrt(N)
    idx = np.unique(np.round(np.logspace(0, 6, 500)).astype(int)) - 1
    return dict(n=n[idx], p1=out["p1"][idx], p15=out["p15"][idx], p2=out["p2"][idx], gamma=gamma, zeta15=zeta15)


def compute_etail():
    import mpmath as mp
    mp.mp.dps = 60
    e = mp.e
    vals = []
    s = mp.mpf(0)
    fact = mp.mpf(1)
    for q in range(0, 16):
        if q > 0:
            fact *= q
        s += 1 / fact
        if q >= 1:
            t = fact * (e - s)
            assert 0 < t < mp.mpf(1) / q
            vals.append(float(t))
    return dict(q=np.arange(1, 16), tail=np.array(vals))


def compute_tests():
    # Rudin 3.35(b): 1/2 + 1/3 + 1/2^2 + 1/3^2 + 1/2^3 + 1/3^3 + ...
    a = []
    for k in range(1, 41):
        a += [2.0**-k, 3.0**-k]
    a = np.array(a)
    ratios = a[1:] / a[:-1]
    roots = a ** (1 / np.arange(1, len(a) + 1))
    # the ratios oscillate between (2/3)^n -> 0 and (1/2)(3/2)^n -> infinity: the ratio test says nothing
    assert ratios[::2].min() < 1e-6 and ratios[1::2].max() > 1e6
    # but the n-th roots tend to 1/sqrt 2 along the powers of 1/2: the root test proves convergence
    assert abs(roots[-2] - 1 / math.sqrt(2)) < 0.01 and roots.max() < 1
    assert abs(a.sum() - 1.5) < 1e-9  # 1 + 1/2
    return dict(a=a, ratios=ratios, roots=roots)


def compute_power():
    n = np.arange(1, 4001, dtype=float)
    out = {}
    for key, z in (("in", 0.9 * np.exp(0.8j)), ("m1", -1.0 + 0j), ("p1", 1.0 + 0j), ("out", 1.1 * np.exp(0.8j))):
        out[key] = np.cumsum(z**n / n)
    assert abs(out["m1"][-1] + math.log(2)) < 2e-4
    assert abs(out["in"][-1] - (-np.log(1 - 0.9 * np.exp(0.8j)))) < 1e-9
    assert abs(out["out"][-1]) > 1e100 or not np.isfinite(abs(out["out"][-1])) or abs(out["out"][-1]) > 1e10
    assert out["p1"][-1].real > 8.8  # the harmonic series, about ln 4000 + 0.577
    return {k: v for k, v in out.items()}


def compute_product():
    N = 60
    a = np.array([(-1.0) ** n / math.sqrt(n + 1) for n in range(N)])
    c = np.array([sum(a[k] * a[n - k] for k in range(n + 1)) for n in range(N)])
    bound = np.array([2 * (n + 1) / (n + 2) for n in range(N)])
    assert np.all(np.abs(c) >= bound - 1e-12)  # Rudin 3.49: so c_n does not tend to 0
    return dict(a=a, c=c, bound=bound)


# ---------------------------------------------------------------------------
# Continuity
# ---------------------------------------------------------------------------
def compute_deltas():
    from explainer.analysis.gameboard import largest_delta
    eps = 0.1
    d_sq = largest_delta(lambda x: x**2, 3.0, 9.0, eps, 1.0, samples=200001)
    exact = math.sqrt(9.1) - 3
    assert abs(d_sq - exact) < 1e-5, (d_sq, exact)
    xs = np.array([0.9, 0.7, 0.5, 0.3, 0.2, 0.1, 0.05])
    d_inv = np.array([largest_delta(lambda x: 1 / x, x0, 1 / x0, eps, x0, samples=200001, domain=(0, np.inf))
                      for x0 in xs])
    exact_inv = xs - 1 / (1 / xs + eps)  # the left side binds: 1/(x - delta) = 1/x + eps
    assert np.allclose(d_inv, exact_inv, rtol=1e-3, atol=1e-6)
    # sqrt is uniformly continuous on [0, 1]: delta = eps^2 works at every point, though sqrt is not Lipschitz
    x = np.linspace(0, 1, 20001)
    d = eps**2
    worst = max(np.max(np.abs(np.sqrt(np.clip(x + h, 0, 1)) - np.sqrt(x))) for h in np.linspace(-d, d, 41)[1:-1])
    assert worst < eps
    return dict(d_sq=d_sq, exact_sq=exact, xs=xs, d_inv=d_inv, eps=eps)


# ---------------------------------------------------------------------------
# Derivatives
# ---------------------------------------------------------------------------
def compute_wiggle():
    h = np.array([10.0**-k for k in range(1, 9)])
    q = h * np.sin(1 / h)  # (f(h) - f(0)) / h for f(x) = x^2 sin(1/x)
    assert np.all(np.abs(q) <= h)
    x = np.linspace(1e-4, 0.02, 400001)
    fp = 2 * x * np.sin(1 / x) - np.cos(1 / x)
    assert fp.min() < -0.99 and fp.max() > 0.99  # f' takes values near both ends of [-1, 1] arbitrarily close to 0
    # Darboux: for every c in [-0.9, 0.9], f' - c changes sign on (0, 0.02)
    for c in np.linspace(-0.9, 0.9, 19):
        assert (fp - c).min() < 0 < (fp - c).max()
    return dict(h=h, q=q)


def compute_taylor():
    import sympy as sp
    x = sp.symbols("x")
    # e^(-1/x^2): every derivative at 0 is 0
    f = sp.exp(-1 / x**2)
    zeros = []
    g = f
    for k in range(5):
        g = sp.diff(g, x)
        L = sp.limit(g, x, 0)
        zeros.append(int(L == 0))
    assert all(zeros)
    # Lagrange's bound for e^x at x = 1: |e - P_n(1)| <= e / (n + 1)!
    errs, bounds = [], []
    for n in range(0, 11):
        P = sum(1 / math.factorial(k) for k in range(n + 1))
        errs.append(math.e - P)
        bounds.append(math.e / math.factorial(n + 1))
        assert 0 < errs[-1] <= bounds[-1]
    return dict(zeros=np.array(zeros), errs=np.array(errs), bounds=np.array(bounds))


ITEMS = {
    "rearrange": compute_rearrange,
    "sequences": compute_sequences,
    "limsup": compute_limsup,
    "pseries": compute_pseries,
    "etail": compute_etail,
    "tests": compute_tests,
    "power": compute_power,
    "product": compute_product,
    "deltas": compute_deltas,
    "wiggle": compute_wiggle,
    "taylor": compute_taylor,
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

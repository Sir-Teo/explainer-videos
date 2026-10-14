"""Precompute everything numerical in Part 2 of the analysis series ("Limits: Sequences, Series, Continuity and the
Derivative").

    python -m videos.analysis2.compute            # everything missing (about a minute)
    python -m videos.analysis2.compute rearrange  # specific items
    python -m videos.analysis2.compute --force    # recompute

Results are cached in ``.cache/analysis2/<name>.npz``; scenes call ``load(name)``.  Every number the narration
quotes is computed here and asserted against the statement it illustrates.

Items:
    rearrange   Riemann's greedy rearrangement of 1 - 1/2 + 1/3 - ... toward pi, toward -1, and off to +infinity
    swing       a rearrangement of 1 - 1/2 + 1/3 - ... swinging between 0 and 1 forever (Rudin 3.54 with alpha < beta);
                the sawtooth series at x = 1 rearranged to sum to 3 instead of (pi - 1)/2
    sequences   1/n, (-1)^n/n, n^(1/n), (1 + 1/n)^n: thresholds N for given epsilons, and the limits
    cauchy      tails of 1 - 1/2 + 1/3 - ... (diameter 1/(N+1)); continued-fraction convergents of sqrt 2 (diameter
                1/(q_N q_{N+1})); a spiral in the plane and the hulls of its tails; (1 + 1/n)^n rising to e
    limsup      a_n = (-1)^n (1 + 1/n): running sups and infs of the tails; a sequence listing every rational in
                [0, 1]; n^(1/n) under its binomial bound; n^10 / 1.1^n
    pseries     partial sums of sum 1/n^p for p = 1, 1.5, 2 up to 10^6, against ln n + gamma, zeta(1.5), pi^2/6
    etail       q! (e - s_q) for q = 1 .. 15, in (0, 1/q): the irrationality of e
    tests       Rudin's example 3.35: ratios and roots of 1/2 + 1/3 + 1/2^2 + 1/3^2 + ...
    power       partial sums of sum z^n / n at |z| = 0.9, 1 (z = -1 and z = 1) and 1.1
    abel        summation by parts checked; the partial sums of e^{ikx} on their circle; the sawtooth series
                sum sin(kx)/k converging at x = 1 (Dirichlet's test)
    product     the Cauchy product of sum (-1)^n / sqrt(n + 1) with itself: |c_n| >= 2(n + 1)/(n + 2)
    deltas      largest deltas: x^2 at 3; 1/x across (0, 1); sqrt x on [0, 1] (all with eps = 0.1)
    thomae      Thomae's function on the rationals of denominator <= 60, and the delta that wins at 1/sqrt 2;
                an increasing function that jumps at every rational (Rudin 4.31)
    wiggle      x^2 sin(1/x): difference quotients at 0, and the derivative taking every value in [-1, 1] near 0;
                Rudin's nowhere-differentiable function, its difference quotients at 0.3 growing like 3^m
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


def compute_swing():
    # take positive terms until the sum passes beta, negative terms until it drops below alpha, and repeat
    alpha, beta = 0.0, 1.0
    p, q, s, up = 1, 2, 0.0, True
    n_terms = 400_000
    sums, terms = np.empty(n_terms), np.empty(n_terms)
    for k in range(n_terms):
        if up:
            t = 1.0 / p
            p += 2
        else:
            t = -1.0 / q
            q += 2
        s += t
        sums[k], terms[k] = s, t
        if up and s > beta:
            up = False
        elif not up and s < alpha:
            up = True
    # the turning points overshoot beta and alpha by at most the last term used, which tends to 0
    peaks = [k for k in range(1, n_terms - 1) if sums[k] > beta and terms[k] > 0 and terms[k + 1] < 0]
    troughs = [k for k in range(1, n_terms - 1) if sums[k] < alpha and terms[k] < 0 and terms[k + 1] > 0]
    assert len(peaks) >= 5 and len(troughs) >= 5
    for k in peaks:
        assert 0 < sums[k] - beta <= terms[k]
    for k in troughs:
        assert 0 < alpha - sums[k] <= -terms[k]
    # the sawtooth series at x = 1, terms sin(k)/k: positive and negative parts both diverge, so greedy works too
    K = 2_000_000
    k = np.arange(1, K + 1)
    tk = np.sin(k) / k
    pos, neg = tk[tk > 0], tk[tk < 0]
    target = 3.0
    i = j = 0
    s = 0.0
    out = np.empty(6000)
    for m in range(len(out)):
        if s <= target:
            s += pos[i]
            i += 1
        else:
            s += neg[j]
            j += 1
        out[m] = s
    s_all = s
    # the rest of the run, sampled at log-spaced term counts (so it can be drawn on a log axis out to the end)
    rec_at = set(np.unique(np.round(np.logspace(math.log10(len(out)) + 0.01, 6.4, 500)).astype(int)).tolist())
    lk, ls = [], []
    cnt = len(out)
    while i < len(pos) - 1 and j < len(neg) - 1:
        if s_all <= target:
            s_all += pos[i]
            i += 1
        else:
            s_all += neg[j]
            j += 1
        cnt += 1
        if cnt in rec_at:
            lk.append(cnt)
            ls.append(s_all)
    lk.append(cnt)
    ls.append(s_all)
    assert cnt == i + j and abs(s_all - target) < 1e-4 and abs(np.sum(tk) - (math.pi - 1) / 2) < 1e-5
    keep = 40000
    return dict(alpha=alpha, beta=beta, sums=sums[:keep], terms=terms[:keep], peaks=np.array([k for k in peaks if k < keep]),
                troughs=np.array([k for k in troughs if k < keep]), sin_sums=out, sin_final=s_all,
                sin_used=np.array([i, j]), sin_lk=np.array(lk), sin_ls=np.array(ls))


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


def compute_cauchy():
    from fractions import Fraction as Fr

    from scipy.spatial import ConvexHull
    # the alternating harmonic series: every later partial sum lies between s_N and s_{N+1}, so diam E_N = 1/(N + 1)
    M = 200_000
    k = np.arange(1, M + 1, dtype=float)
    s = np.cumsum((-1.0) ** (k + 1) / k)
    diam = np.array([s[N - 1:].max() - s[N - 1:].min() for N in range(1, 41)])
    assert np.allclose(diam, 1 / np.arange(2, 42), rtol=1e-12, atol=1e-14)
    # the smallest N with diam E_N < eps
    N_eps = {e: next(N for N in range(1, 100) if Fr(1, N + 1) < Fr(e).limit_denominator(1000)) for e in (0.1, 0.05)}
    assert N_eps == {0.1: 10, 0.05: 20}, N_eps
    # the convergents of sqrt 2 = [1; 2, 2, 2, ...]: p/q with p^2 - 2 q^2 = +-1, alternating around sqrt 2
    conv = [Fr(1), Fr(3, 2)]
    while len(conv) < 14:
        conv.append(Fr(2 * conv[-1].numerator + conv[-2].numerator, 2 * conv[-1].denominator + conv[-2].denominator))
    for c in conv:
        assert abs(c.numerator ** 2 - 2 * c.denominator ** 2) == 1
    cdiam = [abs(conv[i] - conv[i + 1]) for i in range(len(conv) - 1)]
    assert all(cdiam[i] == Fr(1, conv[i].denominator * conv[i + 1].denominator) for i in range(len(cdiam)))
    # the tail E_N lies between c_N and c_{N+1}: the even convergents rise, the odd ones fall, all toward sqrt 2
    for i in range(len(conv) - 2):
        lo, hi = sorted((conv[i], conv[i + 1]))
        assert all(lo <= c <= hi for c in conv[i:])
    # a spiral in the plane, z_n = c + r^n e^{i n theta}: the convex hulls of its tails are nested, diameters -> 0
    n = np.arange(0, 60)
    z = 0.92 ** n * np.exp(1j * 0.75 * n) * 3.0
    pts = np.c_[z.real, z.imag]
    hulls, hdiam = [], []
    for N in range(0, 12):
        P = pts[N:]
        h = P[ConvexHull(P).vertices]
        hulls.append(np.r_[h, np.zeros((60 - len(h), 2)) + np.nan])
        d = np.sqrt(((P[:, None, :] - P[None, :, :]) ** 2).sum(-1)).max()
        hdiam.append(d)
    assert all(hdiam[i + 1] < hdiam[i] for i in range(len(hdiam) - 1))
    # (1 + 1/n)^n rises, stays below 3, and its supremum is e
    m = np.arange(1, 201, dtype=float)
    e_seq = (1 + 1 / m) ** m
    assert np.all(np.diff(e_seq) > 0) and e_seq.max() < 3 and abs(e_seq[-1] - math.e) < 0.007
    e_N = int(np.where(math.e - e_seq >= 0.1)[0].max() + 1)  # past e_N, every term is within 0.1 of e
    return dict(s=s[:60], diam=diam, num=np.array([c.numerator for c in conv]),
                den=np.array([c.denominator for c in conv]), pts=pts, hulls=np.array(hulls), hdiam=np.array(hdiam),
                e_seq=e_seq, e_N=e_N)


def compute_limsup():
    n = np.arange(1, 81, dtype=float)
    a = (-1.0) ** n * (1 + 1 / n)
    sup_tail = np.array([a[k:].max() for k in range(len(a))])
    inf_tail = np.array([a[k:].min() for k in range(len(a))])
    # the true tail sups of the infinite sequence: for even n >= k, 1 + 1/n, largest at the first even index >= k
    true_sup = np.array([1 + 1 / (k + 1 if (k + 1) % 2 == 0 else k + 2) for k in range(len(a))])
    assert np.allclose(sup_tail[:60], true_sup[:60])
    assert abs(sup_tail[60] - 1) < 0.02 and abs(inf_tail[60] + 1) < 0.02
    # every rational in [0, 1], listed by denominator: 0, 1, 1/2, 1/3, 2/3, 1/4, 3/4, ...  (each point of [0, 1] is a
    # subsequential limit, so the upper limit is 1 and the lower limit 0)
    from math import gcd
    rats = [0.0, 1.0] + [p / q for q in range(2, 41) for p in range(1, q) if gcd(p, q) == 1]
    rats = np.array(rats)
    # n^(1/n) - 1 <= sqrt(2 / (n - 1)): from n = (1 + x)^n >= n (n - 1) x^2 / 2
    m = np.arange(2, 1_000_001, dtype=float)
    x = m ** (1 / m) - 1
    assert np.all(x <= np.sqrt(2 / (m - 1)) + 1e-15)
    # n^10 / 1.1^n: powers win for a while, the exponential always wins
    k = np.arange(1, 1001, dtype=float)
    lg = 10 * np.log10(k) - k * np.log10(1.1)
    peak = int(k[lg.argmax()])
    assert peak == 105 and 15 < lg.max() < 16
    cross = int(k[(lg < 0) & (k > 10)][0])  # the first n past the hump where n^10 < 1.1^n
    assert cross == 686 and np.all(lg[cross - 1:] < 0)
    return dict(n=n, a=a, sup_tail=sup_tail, inf_tail=inf_tail, rats=rats, lg=lg, peak=peak, lg_max=lg.max(),
                cross=cross)


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
    # Oresme: the block 1/(2^k + 1) + ... + 1/2^(k+1) is at least 1/2 (exactly, in fractions)
    from fractions import Fraction as Fr
    blocks = [sum(Fr(1, j) for j in range(2**k + 1, 2 ** (k + 1) + 1)) for k in range(0, 8)]
    assert all(b >= Fr(1, 2) for b in blocks)
    # Cauchy condensation (Rudin 3.27): with t_k = sum_{j <= k} 2^j a_{2^j},  s_n <= t_k for n < 2^(k+1)  and
    # s_{2^k} >= t_k / 2
    for key, p in (("p1", 1.0), ("p15", 1.5), ("p2", 2.0)):
        t = np.cumsum([2.0**j * (2.0**j) ** -p for j in range(0, 20)])
        for k in range(0, 19):
            assert out[key][2 ** (k + 1) - 2] <= t[k] + 1e-12  # s_n for n = 2^(k+1) - 1
            assert out[key][2**k - 1] >= t[k] / 2 - 1e-12
    # 1/(n log n) diverges, but only like log log n (Rudin 3.29)
    m = np.arange(2, N + 1, dtype=float)
    nlog = np.cumsum(1 / (m * np.log(m)))
    assert abs(nlog[-1] - np.log(np.log(N))) < 2.0
    idx = np.unique(np.round(np.logspace(0, 6, 500)).astype(int)) - 1
    return dict(n=n[idx], p1=out["p1"][idx], p15=out["p15"][idx], p2=out["p2"][idx], gamma=gamma, zeta15=zeta15,
                blocks=np.array([float(b) for b in blocks]), nlog_end=nlog[-1])


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
    # Rudin 3.30: 0 < e - s_n < 1 / (n! n);  3.31: t_n = (1 + 1/n)^n = sum_k (1/k!) prod_{j<k} (1 - j/n) <= s_n
    s_n = [sum(1 / mp.factorial(k) for k in range(n + 1)) for n in range(0, 16)]
    for n in range(1, 16):
        assert 0 < e - s_n[n] < 1 / (mp.factorial(n) * n)
    terms = {}
    for n in (1, 2, 3, 5, 10, 20, 50, 200):
        c = [float(1 / mp.factorial(k) * mp.fprod([1 - mp.mpf(j) / n for j in range(k)])) for k in range(0, 9)]
        terms[n] = c
        full = mp.fsum(1 / mp.factorial(k) * mp.fprod([1 - mp.mpf(j) / n for j in range(k)]) for k in range(n + 1))
        assert abs(full - (1 + mp.mpf(1) / n) ** n) < mp.mpf(10) ** -40 and full <= s_n[min(n, 15)] + 1e-30
    err_s10, err_t10 = float(e - s_n[10]), float(e - (1 + mp.mpf(1) / 10) ** 10)
    assert err_s10 < 3e-8 and 0.12 < err_t10 < 0.13
    return dict(q=np.arange(1, 16), tail=np.array(vals), tn_n=np.array(list(terms)),
                tn_terms=np.array(list(terms.values())), err_s10=err_s10, err_t10=err_t10)


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
    # 1/(1 + x^2) = 1 - x^2 + x^4 - ...: radius 1 (the poles at +-i), though the function is smooth on the whole line
    for x, conv in ((0.9, True), (1.1, False)):
        P = np.cumsum([(-x * x) ** k for k in range(200)])
        if conv:
            assert abs(P[-1] - 1 / (1 + x * x)) < 1e-15
        else:
            assert abs(P[-1]) > 1e15
    return {k: v for k, v in out.items()}


def compute_abel():
    rng = np.random.default_rng(3)
    # summation by parts (Rudin 3.41): sum_{n=p}^q a_n b_n = sum_{n=p}^{q-1} A_n (b_n - b_{n+1}) + A_q b_q - A_{p-1} b_p
    a, b = rng.normal(size=40), np.sort(rng.random(40))[::-1]
    A = np.cumsum(a)
    for p, q in ((0, 39), (5, 30), (12, 13)):
        lhs = np.sum(a[p:q + 1] * b[p:q + 1])
        rhs = np.sum(A[p:q] * (b[p:q] - b[p + 1:q + 1])) + A[q] * b[q] - (A[p - 1] if p > 0 else 0.0) * b[p]
        assert abs(lhs - rhs) < 1e-12
    # the partial sums of e^{ikx}, k = 1..n, lie on the circle |w - c| = 1 / (2 |sin(x/2)|) through 0
    x = 1.0
    k = np.arange(1, 401)
    W = np.cumsum(np.exp(1j * k * x))
    c = np.exp(1j * x) / (1 - np.exp(1j * x)) * 1.0  # W_n = c (1 - e^{inx}), so |W_n - c| = |c|
    r = 1 / (2 * abs(math.sin(x / 2)))
    assert abs(abs(c) - r) < 1e-12 and np.allclose(np.abs(W - c), r)
    # so sum sin(kx)/k converges (Dirichlet's test), to the sawtooth (pi - x)/2; Dirichlet's bound on the tail:
    # |sum_{k > n} sin(kx)/k| <= 2 M / (n + 1) with M = r
    S = np.cumsum(np.sin(k * x) / k)
    Kbig = np.arange(1, 400_001)
    S_inf = np.sum(np.sin(Kbig * x) / Kbig)
    assert abs(S_inf - (math.pi - x) / 2) < 1e-5
    for n in (10, 50, 200):
        assert abs(S_inf - S[n - 1]) <= 2 * r / (n + 1) + 1e-5
    return dict(x=x, W=W[:60], c=c, r=r, S=S, target=(math.pi - x) / 2)


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


def compute_thomae():
    from fractions import Fraction as Fr
    from math import gcd
    Q = 60
    pq = [(p, q) for q in range(1, Q + 1) for p in range(0, q + 1) if gcd(p, q) == 1]
    x = np.array([p / q for p, q in pq])
    y = np.array([1 / q for p, q in pq])
    # continuity at x0 = 1/sqrt 2 with eps = 0.1: only the points with 1/q >= eps (q <= 10) can break it; delta is the
    # distance to the nearest of them
    x0, eps = 1 / math.sqrt(2), 0.1
    big = np.array([p / q for p, q in pq if 1 / q >= eps])
    delta = float(np.abs(big - x0).min())
    nearest = min(((p, q) for p, q in pq if 1 / q >= eps), key=lambda t: abs(t[0] / t[1] - x0))
    assert nearest == (7, 10) and abs(delta - (x0 - 0.7)) < 1e-15
    inside = (np.abs(x - x0) < delta)
    assert np.all(y[inside] < eps)
    # an increasing function with a jump at every rational p/q of (0, 1), of size proportional to 1/q^3 (Rudin 4.31;
    # denominators up to 40 drawn)
    rats = [Fr(p, q) for q in range(2, 41) for p in range(1, q) if gcd(p, q) == 1]
    c = np.array([1.0 / v.denominator ** 3 for v in rats])
    c = c / c.sum()
    r = np.array([float(v) for v in rats])
    grid = np.linspace(0, 1, 8001)
    F = np.array([c[r < g].sum() for g in grid])
    assert np.all(np.diff(F) >= 0)
    return dict(x=x, y=y, x0=x0, eps=eps, delta=delta, nearest=np.array(nearest), r=r, c=c, grid=grid, F=F)


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
    # Rudin 7.18: f = sum (3/4)^n phi(4^n x), phi = distance to the nearest even integer, is continuous and nowhere
    # differentiable: with delta_m = +-(1/2) 4^-m (sign chosen so no integer lies strictly between 4^m x and
    # 4^m (x + delta_m)), the difference quotient has size >= (3^m + 1)/2
    x0 = 0.3
    quot = []
    for m in range(1, 9):
        dm = 0.5 * 4.0**-m
        if math.floor(4**m * x0) != math.floor(4**m * x0 + 4**m * dm - 1e-12):
            dm = -dm
        qm = (rough(np.array([x0 + dm]))[0] - rough(np.array([x0]))[0]) / dm
        quot.append(qm)
        assert abs(qm) >= (3**m + 1) / 2 - 1e-6
    return dict(h=h, q=q, rough_quot=np.array(quot))


def rough(x, terms: int = 24):
    """Rudin's nowhere-differentiable function (7.18): sum_n (3/4)^n phi(4^n x), phi(x) = |x| on [-1, 1], period 2."""
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    for n in range(terms):
        y = 4.0**n * x
        out += 0.75**n * np.abs(y - 2 * np.round(y / 2))
    return out


def compute_taylor():
    import sympy as sp
    x = sp.symbols("x")
    # e^(-1/x^2): every derivative at 0 is 0
    f = sp.exp(-1 / x**2)
    zeros = []
    g = f
    for k in range(10):
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
    # log(1 + x): the Taylor polynomials converge at x = 0.5 and blow up at x = 1.5 (radius 1)
    for xv, ok in ((0.5, True), (1.5, False)):
        P = np.cumsum([(-1) ** (k + 1) * xv**k / k for k in range(1, 120)])
        assert (abs(P[-1] - math.log(1 + xv)) < 1e-12) == ok
    # e^(-1/x^2) is below x^10 on (0, 0.2]: flatter than any polynomial at 0
    xx = np.linspace(1e-3, 0.2, 2000)
    assert np.all(np.exp(-1 / xx**2) < xx**10)
    return dict(zeros=np.array(zeros), errs=np.array(errs), bounds=np.array(bounds))


ITEMS = {
    "rearrange": compute_rearrange,
    "swing": compute_swing,
    "sequences": compute_sequences,
    "cauchy": compute_cauchy,
    "limsup": compute_limsup,
    "pseries": compute_pseries,
    "etail": compute_etail,
    "tests": compute_tests,
    "power": compute_power,
    "abel": compute_abel,
    "product": compute_product,
    "deltas": compute_deltas,
    "thomae": compute_thomae,
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

"""Precompute everything numerical in Part 8 of the analysis series ("Banach Spaces").

    python -m videos.analysis8.compute            # everything missing (a minute)
    python -m videos.analysis8.compute lebesgue   # specific items
    python -m videos.analysis8.compute --force    # recompute

Results are cached in ``.cache/analysis8/<name>.npz``; scenes call ``load(name)``.  Every number the narration
quotes is computed here and asserted against the statement it illustrates.

Items:
    lebesgue    the Lebesgue constants ||D_n||_1 to n = 10^6 (Fejer's sum), against (4/pi^2) log n + 1.27; the
                continuous near-extremal f_n with s_n(f_n)(0) close to ||D_n||_1
    volterra    the Volterra operator on L^2[0, 1]: norm 2/pi; singular values 2/((2k - 1) pi)
    baire       nested intervals dodging the rationals; a dense G_delta of measure zero
    openmap     a bounded bijection of R^2 and of l^2 (finite section): T(B) contains the ball of radius 1/||T^-1||
    separation  two convex polygons separated by a hyperplane through the midpoint of their closest points; gauges
    weak        <e_n, y> -> 0 for 50 random y in l^2; sin(nx) -> 0 weakly; Mazur's averages of sin(nx)
    alaoglu     probability measures on [0, 1] with no limit, and a subsequence whose moments converge
    extreme     extreme points of the l^p balls in R^3 by the splitting test; the L^1 ball has none
    compact     the Green's operator of -u'' on [0, 1]: eigenvalues 1/(n pi)^2, eigenvectors sines
    haar        Haar measure on SO(3) from random unit quaternions: invariance of averages
"""

from __future__ import annotations

import argparse
import math
import time

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "analysis8"


def trap(y, x):
    y, x = np.asarray(y), np.asarray(x, float)
    return np.sum((y[1:] + y[:-1]) * np.diff(x)) / 2


def _cross2(u, v):
    return u[0] * v[1] - u[1] * v[0]


def lebesgue_constant(n: int) -> float:
    """||D_n||_1 = (1/2pi) int |D_n|, by Fejer's formula: 1/(2n+1) + (2/pi) sum_{k=1}^n tan(pi k/(2n+1)) / k."""
    k = np.arange(1, n + 1, dtype=float)
    return 1 / (2 * n + 1) + (2 / math.pi) * float(np.sum(np.tan(math.pi * k / (2 * n + 1)) / k))


# ---------------------------------------------------------------------------
def compute_lebesgue():
    # Fejer's formula against direct quadrature for small n
    x = np.linspace(-math.pi, math.pi, 400001)
    for n in (1, 2, 5, 10, 30):
        with np.errstate(invalid="ignore", divide="ignore"):
            D = np.sin((n + 0.5) * x) / np.sin(x / 2)
        D[np.isclose(x, 0)] = 2 * n + 1
        direct = trap(np.abs(D), x) / (2 * math.pi)
        assert abs(direct - lebesgue_constant(n)) < 1e-6
    ns = np.array([1, 3, 10, 30, 100, 300, 1000, 3000, 10**4, 3 * 10**4, 10**5, 3 * 10**5, 10**6])
    L = np.array([lebesgue_constant(int(n)) for n in ns])
    asym = 4 / math.pi**2 * np.log(ns) + 1.2703
    assert np.all(np.abs(L[2:] - asym[2:]) / L[2:] < 0.01) and np.all(np.diff(L) > 0)
    # a continuous f_n with |f_n| <= 1 and s_n(f_n)(0) close to ||D_n||_1: a smoothed sign(D_n)
    near = []
    for n in (10, 100, 1000):
        xx = np.linspace(-math.pi, math.pi, 2_000_001)
        with np.errstate(invalid="ignore", divide="ignore"):
            D = np.sin((n + 0.5) * xx) / np.sin(xx / 2)
        D[np.isclose(xx, 0)] = 2 * n + 1
        f = np.tanh(D / 0.05)  # continuous, |f| <= 1, = sign(D) except near the zeros of D
        s0 = trap(f * D, xx) / (2 * math.pi)
        near.append(s0)
        assert s0 <= lebesgue_constant(n) and s0 > 0.97 * lebesgue_constant(n)
    # the kernel itself for the picture
    xs = np.linspace(-math.pi, math.pi, 4001)
    with np.errstate(invalid="ignore", divide="ignore"):
        D20 = np.sin(20.5 * xs) / np.sin(xs / 2)
    D20[np.isclose(xs, 0)] = 41
    return dict(ns=ns, L=L, asym=asym, near=np.array(near), near_ns=np.array([10, 100, 1000]), xs=xs, D20=D20)


def compute_volterra():
    N = 2000
    h = 1 / N
    V = np.tril(np.ones((N, N))) * h - np.eye(N) * h / 2  # midpoint rule for (Vf)(x) = int_0^x f
    s = np.linalg.svd(V, compute_uv=False)
    exact = 2 / ((2 * np.arange(1, 7) - 1) * math.pi)
    assert abs(s[0] - 2 / math.pi) < 1e-5 and np.allclose(s[:6], exact, atol=1e-4)
    return dict(s=s[:12], exact=exact, norm=s[0])


def _rationals(count):
    """The first ``count`` rationals in (0, 1), in the order of increasing denominator."""
    out, seen = [], set()
    q = 2
    while len(out) < count:
        for p in range(1, q):
            if math.gcd(p, q) == 1 and (p, q) not in seen:
                seen.add((p, q))
                out.append(p / q)
                if len(out) == count:
                    break
        q += 1
    return np.array(out)


def compute_baire():
    rats = _rationals(400)
    # nested closed intervals, each avoiding the next rational: the intersection is a point not in the list
    rng = np.random.default_rng(13)
    a, b = 0.0, 1.0
    ivs = []
    for q in rats[:30]:
        third = (b - a) / 3
        cand = [(c, d) for c, d in ((a, a + third), (b - third, b)) if not (c <= q <= d)]
        # keep a closed third that misses q (a coin decides when both do)
        a, b = cand[rng.integers(len(cand))]
        ivs.append((a, b))
    x = (a + b) / 2
    assert all(not (c <= q <= d) for (c, d), q in zip(ivs, rats[:30]))
    assert np.min(np.abs(rats[:30] - x)) > (b - a)  # the limit point is none of the listed rationals
    # a dense open set of small measure: intervals of length eps 2^-k around the k-th rational
    eps_list = np.array([0.5, 0.1, 0.02])
    measures = []
    grid = np.linspace(0, 1, 400001)
    for eps in eps_list:
        cover = np.zeros_like(grid, dtype=bool)
        for k, q in enumerate(rats):
            r = eps * 2.0 ** (-(k + 1)) / 2
            lo, hi = np.searchsorted(grid, [q - r, q + r])
            cover[lo:hi] = True
        measures.append(cover.mean())
    measures = np.array(measures)
    assert np.all(measures <= eps_list + 1e-3)
    return dict(rats=rats[:60], ivs=np.array(ivs), x=x, eps=eps_list, measures=measures)


def compute_openmap():
    T = np.array([[1.2, 0.7], [-0.3, 0.9]])
    s = np.linalg.svd(T, compute_uv=False)
    r_in = s[-1]
    assert abs(r_in - 1 / np.linalg.norm(np.linalg.inv(T), 2)) < 1e-12
    th = np.linspace(0, 2 * np.pi, 3601)
    img = np.c_[np.cos(th), np.sin(th)] @ T.T
    assert np.abs(np.linalg.norm(img, axis=1).min() - r_in) < 1e-5
    # l^2, finite section: T = I + K with a small random K
    rng = np.random.default_rng(0)
    N = 60
    K = rng.normal(size=(N, N)) / (3 * math.sqrt(N))
    T2 = np.eye(N) + K
    s2 = np.linalg.svd(T2, compute_uv=False)
    # random unit vectors y with |y| < s_min are hit by some x in the unit ball
    for _ in range(50):
        y = rng.normal(size=N)
        y *= 0.99 * s2[-1] / np.linalg.norm(y)
        x = np.linalg.solve(T2, y)
        assert np.linalg.norm(x) <= 1
    return dict(T=T, s=s, r_in=r_in, img=img, s2_min=s2[-1], s2_max=s2[0])


def compute_separation():
    rng = np.random.default_rng(12)

    def hull(P):
        P = P[np.lexsort((P[:, 1], P[:, 0]))]

        def half(pts):
            h = []
            for p in pts:
                while len(h) >= 2 and _cross2(h[-1] - h[-2], p - h[-2]) <= 0:
                    h.pop()
                h.append(p)
            return h

        lower, upper = half(P), half(P[::-1])
        return np.array(lower[:-1] + upper[:-1])

    A = hull(rng.normal(size=(12, 2)) * [0.8, 0.6] + [-1.6, 0.3])
    B = hull(rng.normal(size=(12, 2)) * [0.6, 0.7] + [1.4, -0.4])

    def seg_closest(p, a, b):
        t = np.clip(np.dot(p - a, b - a) / np.dot(b - a, b - a), 0, 1)
        return a + t * (b - a)

    best = (np.inf, None, None)
    for P_, Q_ in ((A, B), (B, A)):
        for p in P_:
            for a, b in zip(Q_, np.roll(Q_, -1, axis=0)):
                q = seg_closest(p, a, b)
                dd = np.linalg.norm(p - q)
                if dd < best[0]:
                    best = (dd, p, q) if P_ is A else (dd, q, p)
    dist, pa, pb = best
    nrm = (pb - pa) / np.linalg.norm(pb - pa)
    c = float(nrm @ (pa + pb) / 2)
    assert np.all(A @ nrm < c - 1e-9) and np.all(B @ nrm > c + 1e-9)
    # the gauge of an ellipse x^2/a^2 + y^2/b^2 <= 1
    a_, b_ = 1.5, 0.8
    pts = np.array([[0.6, 0.3], [1.5, 0.8], [-2.0, 0.5]])
    gauge = np.sqrt(pts[:, 0] ** 2 / a_**2 + pts[:, 1] ** 2 / b_**2)
    return dict(A=A, B=B, pa=pa, pb=pb, nrm=nrm, c=c, dist=dist, ell=np.array([a_, b_]), pts=pts, gauge=gauge)


def compute_weak():
    rng = np.random.default_rng(21)
    K = 4000
    k = np.arange(1, K + 1)
    Y = rng.normal(size=(50, K)) * k ** -0.75
    Y /= np.linalg.norm(Y, axis=1, keepdims=True)
    ns = np.array([1, 10, 100, 1000])
    inner = np.abs(Y[:, ns - 1]).max(axis=0)  # max over the 50 y of |<e_n, y>|
    assert np.all(np.diff(inner) < 0) and inner[-1] < 0.02
    # sin(nx) -> 0 weakly in L^2(0, 2 pi): against a fixed g
    x = np.linspace(0, 2 * np.pi, 200001)
    g = np.exp(-((x - 2.0) ** 2)) + 0.3 * x
    pair = np.array([abs(trap(np.sin(n * x) * g, x)) for n in (1, 4, 16, 64, 256)])
    norms = np.array([math.sqrt(trap(np.sin(n * x) ** 2, x)) for n in (1, 4, 16, 64, 256)])
    assert np.all(np.abs(norms - math.sqrt(math.pi)) < 1e-6) and pair[-1] < 0.02 * pair[0] and np.all(np.diff(pair) < 0)
    # Mazur: averages of sin(nx), n = 1..N, have L^2 norm sqrt(pi / N)
    Ns = np.array([1, 4, 16, 64])
    avg = np.array([math.sqrt(trap(np.mean([np.sin(n * x) for n in range(1, N + 1)], axis=0) ** 2, x)) for N in Ns])
    assert np.allclose(avg, np.sqrt(np.pi / Ns), rtol=1e-4)
    return dict(ns=ns, inner=inner, pair=pair, pair_ns=np.array([1, 4, 16, 64, 256]), norms=norms, Ns=Ns, avg=avg)


def compute_alaoglu():
    bins = 24
    xc = (np.arange(bins) + 0.5) / bins

    def mu(n):
        w = 1 + 0.9 * np.sin(2 * np.pi * xc * 2 + n)
        return w / w.sum()

    def moments(w):
        return np.array([np.sum(w * xc**k) for k in range(1, 5)])

    allm = np.array([moments(mu(n)) for n in range(1, 200)])
    assert np.ptp(allm[:, 0]) > 0.05  # the full sequence keeps oscillating
    sub = np.array([6, 44, 710, 103993])  # n mod 2 pi -> 0
    subm = np.array([moments(mu(n)) for n in sub])
    lim = moments(mu(0))
    errs = np.abs(subm - lim).max(axis=1)
    assert np.all(np.diff(errs) < 0) and errs[-1] < 1e-5
    return dict(xc=xc, sub=sub, subm=subm, lim=lim, errs=errs, w_first=np.array([mu(n) for n in (1, 2, 3, 4)]),
                w_sub=np.array([mu(n) for n in sub]), w_lim=mu(0), m1=allm[:60, 0])


def compute_extreme():
    rng = np.random.default_rng(31)

    def pnorm(v, p):
        return np.abs(v).max(axis=-1) if np.isinf(p) else (np.abs(v) ** p).sum(axis=-1) ** (1 / p)

    def normal(x, p):
        if p == 1:
            return np.sign(x)
        if np.isinf(p):
            n = np.zeros(3)
            i = int(np.argmax(np.abs(x)))
            n[i] = np.sign(x[i])
            return n
        return x

    def is_extreme(x, p, trials=400, eps=1e-3):
        """x is extreme iff no small v has x + v and x - v both in the ball; such a v must be tangent to the ball
        (n . v = 0 for an outward normal n), so the test searches the tangent directions."""
        n = normal(x, p)
        n = n / np.linalg.norm(n)
        V = rng.normal(size=(trials, 3))
        V -= np.outer(V @ n, n)
        V *= eps / np.linalg.norm(V, axis=1, keepdims=True)
        return not np.any((pnorm(x + V, p) <= 1 + 1e-12) & (pnorm(x - V, p) <= 1 + 1e-12))

    out = {}
    for p, name in ((1.0, "p1"), (2.0, "p2"), (np.inf, "pinf")):
        cands = rng.normal(size=(300, 3))
        cands /= pnorm(cands, p)[:, None]
        verts = np.vstack([np.eye(3), -np.eye(3)]) if p == 1 else (
            np.array([[sx, sy, sz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)], float) if np.isinf(p) else None)
        ext_random = np.mean([is_extreme(c, p) for c in cands[:120]])
        out[f"ext_{name}"] = ext_random
        if verts is not None:
            assert all(is_extreme(v, p) for v in verts)
            out[f"verts_{name}"] = verts
    assert out["ext_p1"] == 0 and out["ext_pinf"] == 0 and out["ext_p2"] == 1
    # the L^1 ball: f = 2x on [0, 1] (norm 1) is the average of two other unit vectors
    x = np.linspace(0, 1, 400001)
    f = 2 * x
    a = 1 / math.sqrt(2)  # the half-mass point: int_0^a 2x = 1/2
    g1 = np.where(x <= a, 2 * f, 0)
    g2 = np.where(x > a, 2 * f, 0)
    assert abs(trap(g1, x) - 1) < 1e-4 and abs(trap(g2, x) - 1) < 1e-4 and np.allclose((g1 + g2) / 2, f)
    out.update(dict(l1_a=a))
    return out


def compute_compact():
    N = 2000
    h = 1 / (N + 1)
    xs = np.arange(1, N + 1) * h
    G = np.minimum.outer(xs, xs) * (1 - np.maximum.outer(xs, xs)) * h
    w, v = np.linalg.eigh(G)
    w, v = w[::-1], v[:, ::-1]
    exact = 1 / (np.arange(1, 11) * math.pi) ** 2
    assert np.allclose(w[:10], exact, rtol=2e-3)
    vecs = []
    for n in range(1, 5):
        s = np.sin(n * math.pi * xs)
        s /= np.linalg.norm(s)
        vn = v[:, n - 1] * np.sign(v[:, n - 1] @ s)
        assert np.abs(vn - s).max() < 1e-3
        vecs.append(vn / np.abs(vn).max())
    return dict(w=w[:30], exact=exact, xs=xs[::10], vecs=np.array(vecs)[:, ::10])


def compute_haar():
    rng = np.random.default_rng(41)
    q = rng.normal(size=(10000, 4))
    q /= np.linalg.norm(q, axis=1, keepdims=True)
    w, x, y, z = q.T
    R = np.stack([
        np.stack([1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], -1),
        np.stack([2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)], -1),
        np.stack([2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)], -1),
    ], 1)
    assert np.allclose(np.einsum("nij,nkj->nik", R, R), np.eye(3), atol=1e-12)
    v0 = np.array([0.0, 0.0, 1.0])
    pts = R @ v0  # images of the north pole: uniform on the sphere
    f = lambda P: P[:, 2] ** 2 + 0.5 * P[:, 0]  # noqa: E731  a test function on the sphere
    avg = f(pts).mean()
    R0 = R[17]
    avg_shift = f((R @ R0) @ v0).mean()  # right-translate the measure by R0
    assert abs(avg - 1 / 3) < 0.02 and abs(avg_shift - 1 / 3) < 0.02 and abs(pts.mean(axis=0)).max() < 0.03
    return dict(pts=pts[:1500], avg=avg, avg_shift=avg_shift, mean=pts.mean(axis=0))


ITEMS = {
    "lebesgue": compute_lebesgue,
    "volterra": compute_volterra,
    "baire": compute_baire,
    "openmap": compute_openmap,
    "separation": compute_separation,
    "weak": compute_weak,
    "alaoglu": compute_alaoglu,
    "extreme": compute_extreme,
    "compact": compute_compact,
    "haar": compute_haar,
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

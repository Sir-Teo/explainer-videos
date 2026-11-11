"""Spectral graph theory (Part 56).  The Laplacian L = D - A and its normalized form; the Fiedler vector and the sweep
cut; Cheeger's inequality checked; lazy random walks and their mixing against the spectral-gap bound; the series'
own graphs (Part 18's city grid, Part 36's internet, a word co-occurrence graph from the novels) and their spectra.
After Spielman, *Spectral and Algebraic Graph Theory*, and Chung, *Spectral Graph Theory*."""

from __future__ import annotations

import math
import random

import numpy as np


def laplacian(A: np.ndarray, normalized: bool = False) -> np.ndarray:
    d = A.sum(axis=1)
    if not normalized:
        return np.diag(d) - A
    dm = np.where(d > 0, 1 / np.sqrt(np.maximum(d, 1e-300)), 0.0)
    return np.diag((d > 0).astype(float)) - dm[:, None] * A * dm[None, :]


def sbm(sizes=(40, 40, 40), p_in: float = 0.25, p_out: float = 0.02, seed: int = 0):
    """A stochastic block model: planted communities, dense inside, sparse between."""
    rng = np.random.default_rng(seed)
    labels = np.repeat(np.arange(len(sizes)), sizes)
    n = len(labels)
    P = np.where(labels[:, None] == labels[None, :], p_in, p_out)
    U = rng.random((n, n))
    A = np.triu((U < P).astype(float), 1)
    return A + A.T, labels


def connected(A) -> bool:
    n = len(A)
    if not n:
        return False
    seen, stack = {0}, [0]
    while stack:
        u = stack.pop()
        for v in np.flatnonzero(A[u]):
            if v not in seen:
                seen.add(int(v))
                stack.append(int(v))
    return len(seen) == n


def conductance(A, S) -> float:
    S = np.asarray(S, bool)
    d = A.sum(axis=1)
    cut = A[S][:, ~S].sum()
    return float(cut / min(d[S].sum(), d[~S].sum()))


def sweep(A) -> dict:
    """Order vertices by the second eigenvector of the normalized Laplacian (scaled by D^-1/2) and take the prefix of
    least conductance."""
    d = A.sum(axis=1)
    N = laplacian(A, normalized=True)
    w, V = np.linalg.eigh(N)
    f = V[:, 1] / np.sqrt(d)
    order = np.argsort(f)
    best, best_k, curve = 9.0, 1, []
    S = np.zeros(len(A), bool)
    vol_tot = d.sum()
    vol, cut = 0.0, 0.0
    for k, v in enumerate(order[:-1]):
        # update cut incrementally
        cut += d[v] - 2 * A[v, S].sum()
        S[v] = True
        vol += d[v]
        phi = cut / min(vol, vol_tot - vol)
        curve.append(float(phi))
        if phi < best:
            best, best_k = phi, k + 1
    return {"lambda2": float(w[1]), "order": order.tolist(), "phi": float(best), "k": int(best_k), "curve": curve,
            "fiedler": f.tolist()}


def partition_experiment(seed: int = 0) -> dict:
    """Two planted communities: the Fiedler vector's signs against the truth; and three communities with the first
    three eigenvectors."""
    A, lab = sbm((60, 60), 0.2, 0.03, seed)
    L = laplacian(A)
    w, V = np.linalg.eigh(L)
    guess = (V[:, 1] > 0).astype(int)
    acc = max((guess == lab).mean(), (guess != lab).mean())
    s = sweep(A)
    true_phi = conductance(A, lab == 0)
    return {"n": len(A), "edges": int(A.sum() / 2), "accuracy": float(acc), "fiedler": V[:, 1].tolist(),
            "labels": lab.tolist(), "eigenvalues": w[:12].tolist(), "sweep_phi": s["phi"], "true_phi": true_phi,
            "sweep_curve": s["curve"], "lambda2": float(w[1])}


def cheeger_check(trials: int = 60, seed: int = 0) -> list[dict]:
    """lambda2 / 2 <= phi(G) <= sqrt(2 lambda2), with phi found exactly by brute force on small graphs (n = 12) and
    the sweep cut's phi, which the proof shows is at most sqrt(2 lambda2)."""
    rng = np.random.default_rng(seed)
    rows = []
    for t in range(trials):
        n = 12
        p = rng.uniform(0.2, 0.6)
        A = np.triu((rng.random((n, n)) < p).astype(float), 1)
        A = A + A.T
        if not connected(A):
            continue
        lam2 = np.linalg.eigvalsh(laplacian(A, True))[1]
        best = 9.0
        for mask in range(1, 2 ** (n - 1)):
            S = np.array([(mask >> i) & 1 for i in range(n)], bool)
            best = min(best, conductance(A, S))
        rows.append({"lambda2": float(lam2), "phi": float(best), "sweep": sweep(A)["phi"],
                     "lower": float(lam2 / 2), "upper": float(math.sqrt(2 * lam2))})
    return rows


# ---------------------------------------------------------------- random walks

def mixing(A, steps: int = 200, start: int = 0) -> dict:
    """The lazy walk W = (I + D^-1 A)/2 from one vertex: total-variation distance to the stationary distribution
    pi = d / 2m per step, against the bound sqrt(d_max / d_start)... in its standard form
    ||p_t - pi||_TV <= (1/2) sqrt(1/pi_min) (1 - gamma/2)^t, gamma the normalized spectral gap."""
    d = A.sum(axis=1)
    W = 0.5 * (np.eye(len(A)) + A / d[:, None])
    pi = d / d.sum()
    p = np.zeros(len(A))
    p[start] = 1.0
    tv, dists = [], []
    for t in range(steps + 1):
        tv.append(float(0.5 * np.abs(p - pi).sum()))
        if t in (0, 1, 2, 5, 10, 20, 50):
            dists.append(p.tolist())
        p = p @ W
    gam = float(np.linalg.eigvalsh(laplacian(A, True))[1])
    bound = [float(0.5 * math.sqrt(1 / pi.min()) * (1 - gam / 2) ** t) for t in range(steps + 1)]
    t_mix = next((t for t, v in enumerate(tv) if v < 0.25), None)
    return {"tv": tv, "bound": bound, "gap": gam, "t_mix": t_mix, "snapshots": dists}


def cycle(n):
    A = np.zeros((n, n))
    for i in range(n):
        A[i, (i + 1) % n] = A[(i + 1) % n, i] = 1
    return A


def grid(w, h):
    n = w * h
    A = np.zeros((n, n))
    for x in range(w):
        for y in range(h):
            i = x * h + y
            if x + 1 < w:
                A[i, i + h] = A[i + h, i] = 1
            if y + 1 < h:
                A[i, i + 1] = A[i + 1, i] = 1
    return A


def random_regular(n: int, d: int, seed: int = 0) -> np.ndarray:
    """A random simple d-regular graph: pair stubs at random, choosing each partner among the remaining stubs that
    would not make a loop or a repeated edge (Steger and Wormald 1999), restarting if stuck."""
    rng = random.Random(seed)
    if n < 1 or not 0 <= d < n or n * d % 2:
        raise ValueError("a simple d-regular graph needs n > d >= 0 and even n*d")
    for _ in range(200):
        stubs = [v for v in range(n) for _ in range(d)]
        A = np.zeros((n, n))
        ok = True
        while stubs:
            for _ in range(100):
                i, j = rng.randrange(len(stubs)), rng.randrange(len(stubs))
                a, b = stubs[i], stubs[j]
                if i != j and a != b and not A[a, b]:
                    break
            else:
                ok = False
                break
            A[a, b] = A[b, a] = 1
            for k in sorted((i, j), reverse=True):
                stubs.pop(k)
        if ok:
            return A
    raise RuntimeError("no simple graph found")


def barbell(k: int):
    n = 2 * k
    A = np.zeros((n, n))
    A[:k, :k] = 1
    A[k:, k:] = 1
    np.fill_diagonal(A, 0)
    A[k - 1, k] = A[k, k - 1] = 1
    return A


def mixing_experiment(n: int = 64) -> dict:
    graphs = {"cycle": cycle(n), "grid": grid(8, 8), "random 4-regular": random_regular(n, 4, seed=1),
              "barbell": barbell(n // 2)}
    return {name: {k: v for k, v in mixing(A, steps=300).items() if k != "snapshots"} | {
        "edges": int(A.sum() / 2)} for name, A in graphs.items()}


# ---------------------------------------------------------------- the series' graphs

def series_graphs(seed: int = 0) -> dict:
    """Spectra of Part 18's city grid, Part 36's tiered internet and a word co-occurrence graph from the novels:
    lambda2 of the normalized Laplacian (how well connected), and the sweep cut's conductance."""
    from explainer.cs.algo.graphs import grid_city
    from explainer.cs.net.bgp import tiered
    out = {}
    adj, _ = grid_city(16, 16, random.Random(seed))
    nodes = list(adj)
    ix = {v: i for i, v in enumerate(nodes)}
    A = np.zeros((len(nodes), len(nodes)))
    for u, nb in adj.items():
        for v, _ in nb:
            A[ix[u], ix[v]] = 1
    out["city grid (Part 18)"] = A
    rel, _ = tiered(random.Random(seed))
    nodes = sorted(rel)
    ix = {v: i for i, v in enumerate(nodes)}
    A = np.zeros((len(nodes), len(nodes)))
    for u, nb in rel.items():
        for v in nb:
            A[ix[u], ix[v]] = 1
    out["internet (Part 36)"] = A
    out["words (the novels)"] = word_graph()
    rows = {}
    for name, A in out.items():
        keep = A.sum(axis=1) > 0
        A = A[keep][:, keep]
        w = np.linalg.eigvalsh(laplacian(A, True))
        s = sweep(A)
        rows[name] = {"n": int(len(A)), "edges": int(A.sum() / 2), "lambda2": float(w[1]),
                      "spectrum": w.tolist()[:: max(1, len(w) // 120)], "sweep_phi": s["phi"], "sweep_k": s["k"]}
    return rows


def word_graph(top: int = 300, window: int = 5, min_count: int = 8) -> np.ndarray:
    """The top words of one novel, joined when they occur within a few words of each other often enough."""
    import re
    from videos.cs.cs6.compute import novels
    text = next(iter(novels().values())).lower()
    words = re.findall(r"[a-z]+", text)
    from collections import Counter
    stop = {"the", "and", "of", "to", "a", "in", "i", "it", "that", "was", "he", "she", "her", "his", "you", "is",
            "with", "for", "as", "had", "not", "be", "at", "on", "but", "my", "have", "him", "me", "so", "by", "all"}
    c = Counter(w for w in words if w not in stop)
    vocab = [w for w, _ in c.most_common(top)]
    ix = {w: i for i, w in enumerate(vocab)}
    C = np.zeros((top, top))
    seq = [ix.get(w, -1) for w in words]
    for i, a in enumerate(seq):
        if a < 0:
            continue
        for b in seq[i + 1:i + window]:
            if b >= 0 and b != a:
                C[a, b] += 1
                C[b, a] += 1
    return (C >= min_count).astype(float)


# ---------------------------------------------------------------- expanders

def regular_spectra(n: int = 400, ds=(3, 4, 6, 8, 12), seed: int = 0) -> list[dict]:
    """Random d-regular graphs: the second largest |eigenvalue| of A against the Alon-Boppana / Ramanujan bound
    2 sqrt(d - 1); and the expander mixing lemma's error bound checked on random vertex sets."""
    rng = np.random.default_rng(seed)
    rows = []
    for d in ds:
        A = random_regular(n, d, seed=seed + d)
        w = np.sort(np.abs(np.linalg.eigvalsh(A)))[::-1]
        lam = float(w[1])
        worst = 0.0
        for _ in range(200):
            S = rng.random(n) < rng.uniform(0.1, 0.5)
            T = rng.random(n) < rng.uniform(0.1, 0.5)
            e = A[S][:, T].sum()
            dev = abs(e - d * S.sum() * T.sum() / n) / math.sqrt(S.sum() * T.sum())
            worst = max(worst, dev)
        rows.append({"d": d, "lambda": lam, "ramanujan": 2 * math.sqrt(d - 1), "mixing_worst": worst,
                     "mixing_bound": lam})
    return rows


def rotation_map_regular(A: np.ndarray):
    """For a d-regular graph: Rot(v, i) = (w, j), w the i-th neighbour of v and v the j-th neighbour of w."""
    nbrs = [list(np.flatnonzero(A[v])) for v in range(len(A))]
    rot = {}
    for v, nb in enumerate(nbrs):
        for i, w in enumerate(nb):
            rot[(v, i)] = (w, nbrs[w].index(v))
    return rot, nbrs


def zigzag(G: np.ndarray, H: np.ndarray) -> np.ndarray:
    """The zig-zag product (Reingold, Vadhan and Wigderson 2000) of a D-regular G on N vertices with a d-regular H on
    D vertices: vertices (v, a); an edge for each (i, j): a small step in H, a big step in G, a small step in H.
    The result is d^2-regular on N D vertices."""
    rG, _ = rotation_map_regular(G)
    rH, nH = rotation_map_regular(H)
    N, D = len(G), len(H)
    d = len(nH[0])
    Z = np.zeros((N * D, N * D))
    for v in range(N):
        for a in range(D):
            for i in range(d):
                a1, _ = rH[(a, i)]                    # zig: a step in the cloud
                w, b1 = rG[(v, a1)]                   # the big step between clouds
                for j in range(d):
                    b, _ = rH[(b1, j)]                # zag: a step in the next cloud
                    Z[v * D + a, w * D + b] += 1
    return Z


def zigzag_experiment(seed: int = 0) -> dict:
    """G: a random 8-regular graph on 60 vertices; H: a random 3-regular graph on 8 vertices.  The product has degree
    9 and 480 vertices; its normalized second eigenvalue against the RVW bound (their Theorem 4.3), and the
    simpler lambda_G + lambda_H + lambda_H^2."""
    D, d = 8, 3
    G = random_regular(60, D, seed=seed + 11)
    H = random_regular(D, d, seed=seed + 5)
    Z = zigzag(G, H)
    def lam(A, deg):
        w = np.sort(np.abs(np.linalg.eigvalsh(A)))[::-1]
        return float(w[1] / deg)
    lg, lh, lz = lam(G, D), lam(H, d), lam(Z, d * d)
    sq = Z @ Z
    tight = 0.5 * (1 - lh ** 2) * lg + 0.5 * math.sqrt((1 - lh ** 2) ** 2 * lg ** 2 + 4 * lh ** 2)
    return {"N": 60, "D": D, "d": d, "vertices": int(len(Z)), "degree": int(Z.sum(axis=1)[0]), "lambda_G": lg,
            "lambda_H": lh, "lambda_Z": lz, "bound": tight, "simple_bound": lg + lh + lh ** 2,
            "regular": bool(np.allclose(Z.sum(axis=1), d * d)), "self_loops_after_two_steps": float(sq[0, 0])}


# ---------------------------------------------------------------- electrical networks and solvers

def effective_resistance(A: np.ndarray) -> np.ndarray:
    """Electrical resistance, infinite between different connected components."""
    L = laplacian(A)
    Lp = np.linalg.pinv(L)
    dg = np.diag(Lp)
    resistance = np.maximum(0, dg[:, None] + dg[None, :] - 2 * Lp)
    component = np.full(len(A), -1)
    for root in range(len(A)):
        if component[root] >= 0:
            continue
        component[root] = root
        stack = [root]
        while stack:
            u = stack.pop()
            for v in np.flatnonzero(A[u]):
                if component[v] < 0:
                    component[v] = root
                    stack.append(int(v))
    resistance[component[:, None] != component[None, :]] = np.inf
    return resistance


def commute_check(A: np.ndarray, a: int, b: int, walks: int = 2000, seed: int = 0) -> dict:
    """Commute time C(a, b) = 2 m R_eff(a, b), against simulated walks a -> b -> a."""
    rng = random.Random(seed)
    nbrs = [list(np.flatnonzero(A[v])) for v in range(len(A))]
    R = effective_resistance(A)[a, b]
    if not math.isfinite(R):
        raise ValueError("commute-time simulation needs endpoints in the same component")
    m = A.sum() / 2
    if walks <= 0:
        raise ValueError("walk count must be positive")
    if a == b:
        return {"R_eff": 0.0, "predicted": 0.0, "measured": 0.0, "m": int(m)}
    tot = 0
    for _ in range(walks):
        v, steps, phase = a, 0, 0
        while True:
            v = rng.choice(nbrs[v])
            steps += 1
            if phase == 0 and v == b:
                phase = 1
            elif phase == 1 and v == a:
                break
        tot += steps
    return {"R_eff": float(R), "predicted": float(2 * m * R), "measured": tot / walks, "m": int(m)}


def sparsify(A: np.ndarray, eps: float = 0.5, seed: int = 0, C: float = 4.0):
    """Spielman and Srivastava (2008): keep each edge with probability proportional to its weight times its effective
    resistance, reweighted, about C n log n / eps^2 samples."""
    rng = np.random.default_rng(seed)
    n = len(A)
    R = effective_resistance(A)
    iu = np.triu_indices(n, 1)
    w = A[iu]
    mask = w > 0
    edges = np.stack([iu[0][mask], iu[1][mask]], 1)
    p = w[mask] * R[iu][mask]
    p = p / p.sum()
    q = int(C * n * math.log(n) / eps ** 2)
    draws = rng.choice(len(edges), size=q, p=p)
    Hs = np.zeros_like(A)
    for k in draws:
        a, b = edges[k]
        Hs[a, b] += w[mask][k] / (q * p[k])
        Hs[b, a] = Hs[a, b]
    return Hs, int((Hs[iu] > 0).sum()), int(mask.sum())


def solver_experiment(w: int = 20, h: int = 15, p: float = 0.3, weak: float = 0.002, seed: int = 0) -> dict:
    """An ill-conditioned dense graph: a w x h grid of unit-weight edges plus many random weak edges.  CG on L x = b
    (b orthogonal to ones) plain, and preconditioned by the Laplacian of its spectral sparsifier (applied through a
    pseudo-inverse here, for illustration); and the sparsifier's quality, the range of x^T L_H x / x^T L_G x."""
    rng = np.random.default_rng(seed)
    n = w * h
    A = grid(w, h)
    R = np.triu((rng.random((n, n)) < p).astype(float), 1) * weak
    A = A + R + R.T
    Hs, kept, total = sparsify(A, eps=0.7, seed=seed)
    LG, LH = laplacian(A), laplacian(Hs)
    ratios = []
    for _ in range(200):
        x = rng.standard_normal(n)
        x -= x.mean()
        ratios.append(float(x @ LH @ x / (x @ LG @ x)))
    b = rng.standard_normal(n)
    b -= b.mean()
    LHp = np.linalg.pinv(LH)

    def pcg(M=None, tol=1e-10):
        x = np.zeros(n)
        r = b.copy()
        z = M @ r if M is not None else r
        pdir = z.copy()
        rz = r @ z
        it = 0
        while np.linalg.norm(r) > tol * np.linalg.norm(b) and it < 5000:
            Ap = LG @ pdir
            a = rz / (pdir @ Ap)
            x += a * pdir
            r -= a * Ap
            z = M @ r if M is not None else r
            rz2 = r @ z
            pdir = z + rz2 / rz * pdir
            rz = rz2
            it += 1
        return it
    wG = np.linalg.eigvalsh(LG)
    return {"n": n, "edges": total, "sparsifier_edges": kept, "ratio_min": min(ratios), "ratio_max": max(ratios),
            "cg_iters": pcg(), "pcg_iters": pcg(LHp), "kappa_L": float(wG[-1] / wG[1])}

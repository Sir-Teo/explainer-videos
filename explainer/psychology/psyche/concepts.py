"""Psyche categorises (Part 22 of *Psychology, Built*): prototypes and exemplars, attention that learns, psychological
space, a universal law of generalization, similarity as features, levels of categorization, a semantic network,
Bayesian concept learning, meaning from co-occurrence, and categories in practice.

Categorisation: the prototype model and Nosofsky's generalized context model (GCM), both with attention weights and
a choice rule; ALCOVE (Kruschke 1992), the GCM with error-driven learning of association weights and attention,
trial by trial, on the six problems of Shepard, Hovland and Jenkins (1961), fitted to Nosofsky et al.'s (1994) learning
curves; a prototype network trained by the delta rule on the same problems, which cannot learn the non-linear ones.
Psychological space: classical (Torgerson) and non-metric (Shepard-Kruskal, by SMACOF with monotone regression)
multidimensional scaling; Shepard's (1957, 1987) generalization measure from a confusion matrix, the exponential law
fitted to it, and the gradient from consequential regions under any prior on their size. Similarity as features:
Tversky's (1977) contrast model and his count of asymmetries by prominence. Levels: Corter and Gluck's (1992) category
utility in a nested world. A semantic network: spreading activation with a fan. Bayesian concept learning:
Tenenbaum's number game with the size principle. Meaning from co-occurrence: positive pointwise mutual information and
its singular value decomposition, nearest neighbours and analogies by cosine, and representational similarity
analysis. In practice: the polythetic count of a diagnosis and a simulated card sort.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize


# ============================================================================================== categorisation
def minkowski(x, y, w, r: float = 1.0):
    """Attention-weighted Minkowski distance between rows of x and rows of y: (n, m)."""
    x, y = np.atleast_2d(x), np.atleast_2d(y)
    diff = np.abs(x[:, None, :] - y[None, :, :]) ** r
    return (diff @ np.asarray(w, float)) ** (1.0 / r)


def gcm_prob(stimuli, exemplars, labels, c: float = 2.0, w=None, r: float = 1.0, gamma: float = 1.0,
             bias=None) -> np.ndarray:
    """The generalized context model (Nosofsky 1986): similarity to every stored exemplar, eta = exp(-c d), summed
    by category; P(J | x) = b_J S_J^gamma / sum_K b_K S_K^gamma.  Returns (n stimuli, n categories)."""
    exemplars = np.atleast_2d(exemplars)
    labels = np.asarray(labels)
    w = np.full(exemplars.shape[1], 1.0 / exemplars.shape[1]) if w is None else np.asarray(w, float)
    eta = np.exp(-c * minkowski(stimuli, exemplars, w, r))
    cats = np.unique(labels)
    S = np.stack([eta[:, labels == k].sum(1) for k in cats], 1) ** gamma
    b = np.ones(len(cats)) if bias is None else np.asarray(bias, float)
    S = S * b
    return S / S.sum(1, keepdims=True)


def prototype_prob(stimuli, exemplars, labels, c: float = 2.0, w=None, r: float = 1.0, gamma: float = 1.0) -> np.ndarray:
    """The prototype model: each category is its central tendency (the mean of its exemplars); similarity to each
    prototype, exp(-c d), through the same choice rule."""
    exemplars = np.atleast_2d(exemplars)
    labels = np.asarray(labels)
    cats = np.unique(labels)
    protos = np.stack([exemplars[labels == k].mean(0) for k in cats])
    w = np.full(exemplars.shape[1], 1.0 / exemplars.shape[1]) if w is None else np.asarray(w, float)
    eta = np.exp(-c * minkowski(stimuli, protos, w, r)) ** gamma
    return eta / eta.sum(1, keepdims=True)


# the eight stimuli of three binary dimensions, and the six problems of Shepard, Hovland and Jenkins (1961): the
# category (0 or 1) of each stimulus, in the order of the rows of SHJ_STIMULI
SHJ_STIMULI = np.array([[a, b, c] for a in (0, 1) for b in (0, 1) for c in (0, 1)], float)
SHJ_TYPES = {
    1: np.array([0, 0, 0, 0, 1, 1, 1, 1]),  # one dimension decides
    2: np.array([0, 0, 1, 1, 1, 1, 0, 0]),  # exclusive-or of two dimensions; the third is irrelevant
    3: np.array([0, 0, 0, 1, 1, 0, 1, 1]),
    4: np.array([0, 0, 0, 1, 0, 1, 1, 1]),  # a family-resemblance structure: linearly separable
    5: np.array([0, 0, 0, 1, 1, 1, 1, 0]),
    6: np.array([0, 1, 1, 0, 1, 0, 0, 1]),  # parity: every dimension needed
}


def shj_check() -> dict:
    """Each type has four members per category, and Types I and IV are linearly separable."""
    return {t: int(v.sum()) for t, v in SHJ_TYPES.items()}


def alcove(labels, c: float = 6.5, phi: float = 2.0, lw: float = 0.03, la: float = 0.0033, blocks: int = 16,
           orders: int = 50, rng=None, attention_learning: bool = True, return_attention: bool = False):
    """ALCOVE (Kruschke 1992) on one of the six problems: one hidden node per stimulus (exemplar), activation
    a_j = exp(-c sum_i alpha_i |h_ji - x_i|); category outputs o_k = sum_j w_kj a_j; P(k) = exp(phi o_k) / sum exp(phi
    o_K); humble teachers t_k = max(+1, o_k) for the right category and min(-1, o_k) for the wrong one; gradient descent
    on 1/2 sum (t - o)^2 for w (rate lw) and for the attention strengths alpha (rate la, kept non-negative).  Trained on
    blocks of the eight stimuli in random order; returns the mean probability of error per block, averaged over
    ``orders`` random orders."""
    rng = rng or np.random.default_rng(0)
    H = SHJ_STIMULI
    y = np.asarray(labels)
    err = np.zeros(blocks)
    final_attention = np.zeros(3)
    for _ in range(orders):
        alpha = np.full(3, 1.0 / 3)
        W = np.zeros((2, 8))
        for b in range(blocks):
            for s in rng.permutation(8):
                x = H[s]
                d = np.abs(H - x)  # (8 hidden, 3 dims)
                a = np.exp(-c * d @ alpha)
                o = W @ a
                p = np.exp(phi * o - np.max(phi * o))
                p /= p.sum()
                err[b] += 1.0 - p[y[s]]
                t = np.where(np.arange(2) == y[s], np.maximum(1.0, o), np.minimum(-1.0, o))
                delta = t - o
                if attention_learning:
                    back = (delta @ W) * a  # (8,)
                    alpha = np.maximum(0.0, alpha - la * (back @ (c * d)))
                W += lw * np.outer(delta, a)
        final_attention += alpha
    if return_attention:
        return err / (orders * 8), final_attention / orders
    return err / (orders * 8)


def alcove_attention(labels, c, phi, lw, la, blocks: int = 16, orders: int = 50, rng=None) -> np.ndarray:
    """The attention strengths ALCOVE ends with on a problem, averaged over random orders."""
    return alcove(labels, c, phi, lw, la, blocks, orders, rng, return_attention=True)[1]


def delta_rule_network(labels, lr: float = 0.01, phi: float = 2.0, blocks: int = 16, orders: int = 50,
                       rng=None) -> np.ndarray:
    """A prototype network: the three dimensions (coded +1/-1) and a bias wired straight to two category outputs,
    trained by the delta rule.  It can only draw a straight boundary, so it cannot learn Types II, III, V or VI
    perfectly.  Returns the mean probability of error per block."""
    rng = rng or np.random.default_rng(0)
    X = np.hstack([2 * SHJ_STIMULI - 1, np.ones((8, 1))])
    y = np.asarray(labels)
    err = np.zeros(blocks)
    for _ in range(orders):
        W = np.zeros((2, 4))
        for b in range(blocks):
            for s in rng.permutation(8):
                o = W @ X[s]
                p = np.exp(phi * o - np.max(phi * o))
                p /= p.sum()
                err[b] += 1.0 - p[y[s]]
                t = np.where(np.arange(2) == y[s], 1.0, -1.0)
                W += lr * np.outer(t - o, X[s])
    return err / (orders * 8)


def fit_alcove_shj(observed: dict, x0=(6.5, 3.0, 0.1, 0.3), orders: int = 30, attention: bool = True) -> dict:
    """Least-squares fit of ALCOVE's c, phi, lambda_w and lambda_a to the six learning curves (``observed[t]`` is the
    error per block for type t), with common random orders.  With ``attention=False`` the attention strengths stay
    equal (lambda_a = 0) and three parameters are fitted: the generalized context model with learnt associations."""
    types = sorted(observed)

    def unpack(theta):
        if attention:
            return np.exp(theta)
        c, phi, lw = np.exp(theta)
        return np.array([c, phi, lw, 0.0])

    def pred(theta):
        c, phi, lw, la = unpack(theta)
        return {t: alcove(SHJ_TYPES[t], c, phi, lw, la, blocks=len(observed[t]), orders=orders,
                          rng=np.random.default_rng(7), attention_learning=attention) for t in types}

    def loss(theta):
        p = pred(theta)
        return float(sum(np.sum((p[t] - np.asarray(observed[t])) ** 2) for t in types))

    start = np.log(np.asarray(x0, float)[: 4 if attention else 3])
    r = minimize(loss, start, method="Nelder-Mead", options={"maxiter": 300, "xatol": 1e-3, "fatol": 1e-6})
    c, phi, lw, la = unpack(r.x)
    return {"params": {"c": c, "phi": phi, "lw": lw, "la": la}, "sse": float(r.fun), "pred": pred(r.x)}


# ============================================================================================== psychological space
def classical_mds(D, k: int = 2) -> tuple[np.ndarray, np.ndarray]:
    """Torgerson's classical scaling: double-centre the squared distances, B = -1/2 J D^2 J, and take the top k
    eigenvectors scaled by the square roots of their eigenvalues.  Returns the coordinates (n, k) and all
    eigenvalues, largest first."""
    D = np.asarray(D, float)
    n = len(D)
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (D ** 2) @ J
    vals, vecs = np.linalg.eigh(B)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    X = vecs[:, :k] * np.sqrt(np.maximum(vals[:k], 0))
    return X, vals


def stress(D, X) -> float:
    """Kruskal's stress-1 of a configuration X against target distances D."""
    D = np.asarray(D, float)
    E = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
    iu = np.triu_indices(len(D), 1)
    return float(np.sqrt(np.sum((D[iu] - E[iu]) ** 2) / np.sum(D[iu] ** 2)))



def _pava(y, w=None) -> np.ndarray:
    """Pool-adjacent-violators: the non-decreasing least-squares fit to y (in the given order)."""
    y = np.asarray(y, float)
    w = np.ones_like(y) if w is None else np.asarray(w, float)
    vals, wts, sizes = [], [], []
    for yi, wi in zip(y, w):
        vals.append(yi); wts.append(wi); sizes.append(1)
        while len(vals) > 1 and vals[-2] > vals[-1]:
            v = (vals[-2] * wts[-2] + vals[-1] * wts[-1]) / (wts[-2] + wts[-1])
            wts[-2] += wts[-1]; sizes[-2] += sizes[-1]; vals[-2] = v
            vals.pop(); wts.pop(); sizes.pop()
    return np.repeat(vals, sizes)


def nonmetric_mds(dissim, k: int = 2, iters: int = 300, rng=None, starts: int = 4) -> dict:
    """Kruskal's non-metric scaling by SMACOF: only the rank order of the dissimilarities is used.  Each iteration
    replaces them by the monotone (PAVA) regression of the current distances on them, normalises, and takes a
    Guttman-transform step.  Several starts (one classical); returns the best configuration and its stress-1."""
    D = np.asarray(dissim, float)
    n = len(D)
    iu = np.triu_indices(n, 1)
    order = np.argsort(D[iu], kind="stable")
    rng = rng or np.random.default_rng(0)
    best = None
    for s in range(starts):
        X = classical_mds(D, k)[0] if s == 0 else rng.standard_normal((n, k))
        for _ in range(iters):
            E = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
            dh = np.empty(len(order))
            dh[order] = _pava(E[iu][order])
            dh *= np.sqrt(len(dh) / np.sum(dh ** 2))
            Dh = np.zeros((n, n))
            Dh[iu] = dh
            Dh = Dh + Dh.T
            with np.errstate(divide="ignore", invalid="ignore"):
                Bm = np.where(E > 0, -Dh / E, 0.0)
            np.fill_diagonal(Bm, 0)
            np.fill_diagonal(Bm, -Bm.sum(1))
            X = Bm @ X / n
        E = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
        dh = np.empty(len(order))
        dh[order] = _pava(E[iu][order])
        st = float(np.sqrt(np.sum((E[iu] - dh) ** 2) / np.sum(E[iu] ** 2)))
        if best is None or st < best["stress"]:
            best = {"X": X - X.mean(0), "stress": st}
    return best

def shepard_generalization(P) -> np.ndarray:
    """Shepard's (1957) measure of generalization from a matrix of response probabilities P[i, j] (stimulus i,
    response j): g_ij = sqrt(P_ij P_ji / (P_ii P_jj)), symmetric, 1 on the diagonal.  Under Luce's choice model it
    is the similarity eta_ij, free of response bias."""
    P = np.asarray(P, float)
    d = np.diag(P)
    with np.errstate(divide="ignore", invalid="ignore"):
        g = np.sqrt(np.clip(P * P.T, 0, None) / np.outer(d, d))
    return g


def fit_exponential_law(dist, gen) -> dict:
    """Fit g = exp(-k d) (through g = 1 at d = 0) by least squares on log g, and report the variance explained in
    log g."""
    d, g = np.asarray(dist, float), np.asarray(gen, float)
    ok = (g > 0) & np.isfinite(g) & (d > 0)
    k = -np.sum(d[ok] * np.log(g[ok])) / np.sum(d[ok] ** 2)
    res = np.log(g[ok]) + k * d[ok]
    tot = np.log(g[ok]) - np.log(g[ok]).mean()
    return {"k": float(k), "r2_log": float(1 - np.sum(res ** 2) / np.sum(tot ** 2))}


def consequential_region_gradient(d, sizes=None, density=None) -> np.ndarray:
    """Shepard's (1987) derivation in one dimension: a stimulus at 0 had a consequence; the consequential region is
    an interval of unknown size s and position containing 0.  The probability that a stimulus at distance d is also
    in it, averaged over sizes s with prior density p(s) (by default an Erlang prior), is
    g(d) = integral p(s) max(0, 1 - d/s) ds, which is close to exp(-d) for most priors."""
    d = np.atleast_1d(np.asarray(d, float))
    s = np.linspace(1e-3, 30, 6000) if sizes is None else np.asarray(sizes, float)
    p = s * np.exp(-s) if density is None else np.asarray(density, float)
    p = p / np.trapezoid(p, s)
    return np.array([np.trapezoid(p * np.clip(1 - x / s, 0, None), s) for x in d])


# ============================================================================================== similarity as features
def contrast_similarity(A: set, B: set, theta: float = 1.0, alpha: float = 0.8, beta: float = 0.2,
                        f=len) -> float:
    """Tversky's (1977) contrast model: S(a, b) = theta f(A & B) - alpha f(A - B) - beta f(B - A).  With alpha > beta
    the subject's distinctive features count more than the referent's, so a sparse subject is more similar to a rich
    referent than the reverse."""
    return theta * f(A & B) - alpha * f(A - B) - beta * f(B - A)


def morse_duration(code: str, dot: float = 0.05, dash: float = 0.15, gap: float = 0.05) -> float:
    """The temporal length of a Morse signal in seconds, as Rothkopf played them: dots 0.05 s, dashes 0.15 s, with
    0.05 s of silence between beeps."""
    return sum(dot if c == "." else dash for c in code) + gap * (len(code) - 1)


def prominence_asymmetry(S, prominence, decimals: int = 0) -> dict:
    """Tversky's (1977) test of asymmetry: for every pair whose members differ in prominence, compare s(q, p), the
    less prominent q first, with s(p, q).  ``S[i, j]`` is the similarity with i first (in percent); values are compared
    after rounding to ``decimals``.  Returns the counts, the mean difference and a two-sided sign test."""
    from scipy.stats import binomtest

    S = np.asarray(S, float)
    pr = np.asarray(prominence, float)
    more = fewer = ties = 0
    diffs = []
    n = len(S)
    for i in range(n):
        for j in range(i + 1, n):
            if np.isclose(pr[i], pr[j]):
                continue
            q, p = (i, j) if pr[i] < pr[j] else (j, i)
            a, b = round(S[q, p], decimals), round(S[p, q], decimals)
            diffs.append(S[q, p] - S[p, q])
            more += a > b
            fewer += a < b
            ties += a == b
    return {"pairs": len(diffs), "more": int(more), "fewer": int(fewer), "ties": int(ties),
            "mean_diff": float(np.mean(diffs)), "sign_p": float(binomtest(more, more + fewer).pvalue)}


# ============================================================================================== levels of categorization
def category_utility(F, members) -> float:
    """Corter & Gluck's (1992) category utility of one category: P(c) * sum_k [P(f_k | c)^2 - P(f_k)^2], the gain in
    the expected number of features guessed correctly from knowing that a thing belongs to c.  ``F`` is a binary
    (objects, features) array, ``members`` a boolean mask of the category."""
    F = np.asarray(F, float)
    m = np.asarray(members, bool)
    return float(m.mean() * np.sum(F[m].mean(0) ** 2 - F.mean(0) ** 2))


def nested_world(n_super: int = 3, n_basic: int = 3, n_sub: int = 2, f_super: int = 1, f_basic: int = 6,
                 f_sub: int = 1) -> tuple[np.ndarray, list]:
    """An illustrative three-level taxonomy: every object has its superordinate's ``f_super`` features, its basic
    category's ``f_basic`` and its subordinate's ``f_sub``.  Returns the features and, per object, its
    (superordinate, basic, subordinate) labels."""
    nf = n_super * f_super + n_super * n_basic * f_basic + n_super * n_basic * n_sub * f_sub
    rows, labels = [], []
    for s in range(n_super):
        for b in range(n_basic):
            for u in range(n_sub):
                r = np.zeros(nf)
                r[s * f_super:(s + 1) * f_super] = 1
                o = n_super * f_super + (s * n_basic + b) * f_basic
                r[o:o + f_basic] = 1
                o = n_super * f_super + n_super * n_basic * f_basic + ((s * n_basic + b) * n_sub + u) * f_sub
                r[o:o + f_sub] = 1
                rows.append(r)
                labels.append((s, (s, b), (s, b, u)))
    return np.array(rows), labels


def level_utilities(F, labels) -> np.ndarray:
    """The mean category utility of the categories at each level of ``labels`` (as from ``nested_world``)."""
    out = []
    for lv in range(len(labels[0])):
        L = [lab[lv] for lab in labels]
        out.append(np.mean([category_utility(F, [x == c for x in L]) for c in dict.fromkeys(L)]))
    return np.array(out)


# ============================================================================================== categories in practice
def polythetic_count(n_symptoms: int = 9, need: int = 5, core: int = 2) -> int:
    """The number of symptom sets that meet a polythetic rule: at least ``need`` of ``n_symptoms``, including at
    least one of the first ``core`` (DSM-5's major depressive episode: 5 of 9, with depressed mood or loss of
    interest).  227 for the default."""
    from math import comb

    return sum(comb(n_symptoms, k) - comb(n_symptoms - core, k) for k in range(need, n_symptoms + 1))


def card_sort(F, n_people: int = 40, rng=None, c: float = 3.0, groups=(3, 4, 5)) -> np.ndarray:
    """A simulated open card sort.  Each person weights the features at random (a Dirichlet draw), so attends to
    different properties, and sorts the items into a number of piles by average-linkage clustering of the
    weighted distances.  Returns the co-occurrence matrix: the share of people who put each pair in one pile."""
    from scipy.cluster.hierarchy import fcluster, linkage
    from scipy.spatial.distance import pdist

    rng = rng or np.random.default_rng(0)
    F = np.asarray(F, float)
    n = len(F)
    co = np.zeros((n, n))
    for _ in range(n_people):
        w = rng.dirichlet(np.ones(F.shape[1]))
        d = pdist(F * np.sqrt(w))  # weighted Euclidean distance
        d = d + rng.uniform(0, 0.01, d.shape)  # a little jitter breaks ties between equal distances
        lab = fcluster(linkage(d, "average"), t=int(rng.choice(groups)), criterion="maxclust")
        co += lab[:, None] == lab[None, :]
    return co / n_people


# ============================================================================================== a semantic network
def spreading_activation(adjacency, source, steps: int = 4, decay: float = 0.5, fan: bool = True) -> np.ndarray:
    """Activation spreading from ``source`` through a weighted graph: each step every node passes ``decay`` of its
    activation to its neighbours, divided among them when ``fan`` (Anderson's fan effect).  Returns the activation of
    every node after each step (steps + 1, n)."""
    A = np.asarray(adjacency, float)
    if fan:
        out = A.sum(1, keepdims=True)
        A = np.divide(A, out, out=np.zeros_like(A), where=out > 0)
    a = np.zeros(len(A))
    a[source] = 1.0
    hist = [a.copy()]
    for _ in range(steps):
        a = a + decay * (A.T @ a)
        hist.append(a.copy())
    return np.array(hist)


# ============================================================================================== Bayesian concept learning
def number_game_hypotheses(n: int = 100) -> tuple[list, np.ndarray, np.ndarray]:
    """Tenenbaum's number game: hypotheses about which numbers 1..n a concept picks out.  Mathematical concepts
    (even, odd, squares, cubes, primes, multiples of 3..12, powers of 2..10, ending in 0..9) share half the prior
    equally; intervals [a, b] share the other half with an Erlang prior on their size (scale 10).  Returns names, the
    membership matrix (hypotheses, n) and the prior."""
    nums = np.arange(1, n + 1)
    names, rows = [], []

    def add(name, members):
        m = np.isin(nums, members)
        if m.any():
            names.append(name)
            rows.append(m)

    add("even", nums[nums % 2 == 0])
    add("odd", nums[nums % 2 == 1])
    add("squares", [k * k for k in range(1, 11)])
    add("cubes", [k ** 3 for k in range(1, 5)])
    add("primes", [p for p in nums if p > 1 and all(p % q for q in range(2, int(p ** 0.5) + 1))])
    for k in range(3, 13):
        add(f"multiples of {k}", nums[nums % k == 0])
    for b in range(2, 11):
        add(f"powers of {b}", [b ** e for e in range(1, 8) if b ** e <= n])
    for dgt in range(10):
        add(f"ending in {dgt}", nums[nums % 10 == dgt])
    n_math = len(names)
    sizes = []
    for a in range(1, n + 1):
        for b in range(a, n + 1):
            names.append(f"{a} to {b}")
            rows.append((nums >= a) & (nums <= b))
            sizes.append(b - a + 1)
    H = np.array(rows)
    sizes = np.array(sizes, float)
    erlang = (sizes / 10.0 ** 2) * np.exp(-sizes / 10.0)
    prior = np.r_[np.full(n_math, 0.5 / n_math), 0.5 * erlang / erlang.sum()]
    return names, H, prior


def number_game(examples, n: int = 100) -> dict:
    """Generalization in the number game: the posterior over hypotheses after the examples, with the size principle
    p(X | h) = (1 / |h|)^len(X) for hypotheses that contain every example, and the probability that each number 1..n
    is in the concept, sum_h p(h | X) [y in h].  Returns the generalization curve and the top hypotheses."""
    names, H, prior = number_game_hypotheses(n)
    X = np.asarray(examples) - 1
    size = H.sum(1).astype(float)
    consistent = H[:, X].all(1)
    like = np.where(consistent, size ** (-float(len(X))), 0.0)
    post = prior * like
    post /= post.sum()
    gen = post @ H
    top = np.argsort(post)[::-1][:5]
    return {"gen": gen, "top": [(names[i], float(post[i])) for i in top]}


# ============================================================================================== meaning from co-occurrence
def cooccurrence(tokens, vocab: list, window: int = 4) -> np.ndarray:
    """Symmetric co-occurrence counts of the words in ``vocab`` within ``window`` tokens of each other."""
    index = {w: i for i, w in enumerate(vocab)}
    ids = np.array([index.get(t, -1) for t in tokens])
    n = len(vocab)
    flat = np.zeros(n * n)
    for off in range(1, window + 1):
        a, b = ids[:-off], ids[off:]
        ok = (a >= 0) & (b >= 0)
        flat += np.bincount(a[ok] * n + b[ok], minlength=n * n)
        flat += np.bincount(b[ok] * n + a[ok], minlength=n * n)
    return flat.reshape(n, n)


def ppmi_svd(C, k: int = 50) -> np.ndarray:
    """Word vectors from counts: positive pointwise mutual information, PPMI = max(0, log p(w, c) / (p(w) p(c))),
    then a truncated SVD, U_k S_k^(1/2) (latent semantic analysis in its modern form).  Rows are unit length."""
    C = np.asarray(C, float)
    total = C.sum()
    pw = C.sum(1, keepdims=True) / total
    pc = C.sum(0, keepdims=True) / total
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log((C / total) / (pw * pc))
    P = np.where(np.isfinite(pmi) & (pmi > 0), pmi, 0.0)
    U, S, _ = np.linalg.svd(P, full_matrices=False)
    V = U[:, :k] * np.sqrt(S[:k])
    return V / np.maximum(np.linalg.norm(V, axis=1, keepdims=True), 1e-12)


def neighbours(V, vocab: list, word: str, n: int = 5) -> list:
    """The n nearest words to ``word`` by cosine, with their similarities."""
    i = vocab.index(word)
    sims = V @ V[i]
    order = [j for j in np.argsort(sims)[::-1] if j != i][:n]
    return [(vocab[j], float(sims[j])) for j in order]


# common function words left out of the word vectors' vocabulary


def rsa(D1, D2) -> float:
    """Representational similarity analysis: the Spearman correlation of two dissimilarity matrices' upper
    triangles (Kriegeskorte, Mur and Bandettini, 2008)."""
    from scipy.stats import spearmanr

    D1, D2 = np.asarray(D1, float), np.asarray(D2, float)
    iu = np.triu_indices(len(D1), 1)
    return float(spearmanr(D1[iu], D2[iu]).statistic)


def hue_angle_distances(nm, s_weight: float = 1.0) -> np.ndarray:
    """Distances between monochromatic lights as differences of hue angle in the opponent plane of Part 13
    (red-green L - M against blue-yellow S - (L + M)/2, intensity divided out, the plane centred on the lights)."""
    from explainer.psychology.psyche import vision

    lms = np.array([vision.cone_excitations(vision.monochromatic(float(x))) for x in nm])
    lms = lms / lms.sum(1, keepdims=True)
    op = vision.opponent(lms)
    a, b = op[:, 1] - op[:, 1].mean(), s_weight * (op[:, 2] - op[:, 2].mean())
    ang = np.arctan2(b, a)
    return np.abs(np.angle(np.exp(1j * (ang[:, None] - ang[None]))))


def analogy(V, vocab: list, a: str, b: str, c: str, n: int = 4) -> list:
    """a is to b as c is to ?: the words nearest (by cosine) to b - a + c, leaving out the three cue words."""
    idx = {w: k for k, w in enumerate(vocab)}
    v = V[idx[b]] - V[idx[a]] + V[idx[c]]
    v = v / np.linalg.norm(v)
    order = np.argsort(-(V @ v))
    return [vocab[k] for k in order if vocab[k] not in (a, b, c)][:n]


STOPWORDS = tuple("""the of and to a in i was her it he that she not be you had as his for with but is have at my him so all
me on by which they this were would no from or could been very what any their there an will one more must said do if mr
am them we than should are such when only much did own being who may can how its your has well every then before might
never into again little out now some know think nothing too say up shall nor s""".split())

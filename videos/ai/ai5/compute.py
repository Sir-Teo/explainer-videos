"""Precompute everything numerical in Part 5 of the AI series ("Randomness in Motion").

    python -m videos.ai.ai5.compute              # everything missing (Part 1's books and passage: .cache/ai1)
    python -m videos.ai.ai5.compute --force bayes

Results are cached in ``.cache/ai5/<name>.json`` (+ ``.npz``).

Items:
    galton       a Galton board: 1,000 balls through 12 rows of pegs, and the binomial and normal curves
    clt          the sum of k dice, exactly, for k = 1, 2, 3, 6, 12: the bell appears
    mle          a Gaussian fitted to the Galton balls: the log-likelihood over (mu, sigma) and its peak
    bayes        how often is a letter "e"? the posterior after 0, 10, 100, 1,000 and 10,000 letters of the passage
    temperature  GPT-2's next-token distribution at temperatures 0.5, 1, 2, and samples at each
    markov       Part 1's letter-pair table as a Markov chain: from "q", the distribution settles to the letter
                 frequencies; how fast (the second eigenvalue)
    montecarlo   pi from random points, error against N; a rare event by plain and by importance sampling
    mcmc         Metropolis sampling of a two-peaked density in the plane
    brownian     random walks with finer and finer steps; Brownian paths; the spread growing like sqrt(t)
    diffusion    an Ornstein-Uhlenbeck process; data with two peaks diffused into noise, and its score; the
                 Fokker-Planck equation solved on a grid against 20,000 particles
    shape        points filling the letters "AI" diffused into noise in the plane, and brought back with the
                 exact score of the noised data (a preview of Part 21)
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai5")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def ai1():
    from videos.ai.ai1 import compute as c1

    return c1


# ---------------------------------------------------------------------------
def compute_galton():
    g = rng(1889)  # Galton's Natural Inheritance, 1889
    rows, n = 12, 1000
    steps = g.integers(0, 2, size=(n, rows))  # 0 = left, 1 = right
    bins = steps.sum(1)
    counts = np.bincount(bins, minlength=rows + 1)
    binom = np.array([math.comb(rows, k) for k in range(rows + 1)]) / 2 ** rows
    x = np.linspace(-0.5, rows + 0.5, 200)
    normal = np.exp(-0.5 * ((x - rows / 2) / math.sqrt(rows / 4)) ** 2) / math.sqrt(2 * math.pi * rows / 4)
    chi2 = float(((counts - n * binom) ** 2 / (n * binom)).sum())
    assert chi2 < 30, chi2  # the 1,000 balls agree with the binomial
    return dict(rows=rows, n=n, steps=steps[:80], bins=bins, counts=counts, binom=binom, x=x, normal=normal, chi2=chi2)


def compute_clt():
    die = np.ones(6) / 6
    out, d = {}, np.array([1.0])
    for k in range(1, 13):
        d = np.convolve(d, die)
        if k in (1, 2, 3, 6, 12):
            out[f"k{k}"] = d.copy()  # P(sum = k + i), i = 0 .. 5k
    return dict(ks=[1, 2, 3, 6, 12], **out)


def compute_mle():
    gb = load("galton")
    x = np.asarray(gb["bins"], float)
    n = len(x)
    mus, sigmas = np.linspace(3.0, 9.0, 61), np.linspace(0.8, 4.0, 65)
    M, S = np.meshgrid(mus, sigmas, indexing="ij")
    # average log-likelihood (nats per ball) of a normal density at the 1,000 positions
    ss = ((x[None, None, :] - M[..., None]) ** 2).mean(-1)
    ll = -0.5 * np.log(2 * math.pi * S ** 2) - ss / (2 * S ** 2)
    mu_hat, sigma_hat = float(x.mean()), float(x.std())
    i, j = np.unravel_index(np.argmax(ll), ll.shape)
    assert abs(mus[i] - mu_hat) < 0.1 and abs(sigmas[j] - sigma_hat) < 0.06
    assert abs(sigma_hat - math.sqrt(3)) < 0.1  # 12 fair left/right bounces: variance 12 / 4
    ll_hat = float(-0.5 * math.log(2 * math.pi * sigma_hat ** 2) - 0.5)
    return dict(mus=mus, sigmas=sigmas, ll=ll, mu_hat=mu_hat, sigma_hat=sigma_hat, ll_hat=ll_hat, n=n)


# ---------------------------------------------------------------------------
NS = [0, 10, 100, 1000, 10000]


def compute_bayes():
    c1 = ai1()
    t = c1.text("passage27").replace(" ", "")  # letters only
    assert len(t) > 10000
    e_true = t.count("e") / len(t)
    ps = np.linspace(0, 1, 2001)
    out = dict(ns=NS, ps=ps[::4], e_all=e_true, n_all=len(t), head=t[:60])
    for n in NS:
        k = t[:n].count("e")
        a, b = 1 + k, 1 + n - k  # a uniform prior, Beta(1, 1)
        logpost = (a - 1) * np.log(np.maximum(ps, 1e-300)) + (b - 1) * np.log(np.maximum(1 - ps, 1e-300))
        post = np.exp(logpost - logpost.max())
        post /= post.sum() * (ps[1] - ps[0])
        cdf = np.cumsum(post) * (ps[1] - ps[0])
        lo, hi = float(ps[np.searchsorted(cdf, 0.025)]), float(ps[np.searchsorted(cdf, 0.975)])
        out[f"k{n}"] = int(k)
        out[f"post{n}"] = post[::4]
        out[f"mean{n}"] = (k + 1) / (n + 2)  # Laplace's rule of succession
        out[f"mle{n}"] = k / n if n else None
        out[f"ci{n}"] = [lo, hi]
    assert out["ci10000"][0] < e_true < out["ci10000"][1]
    return out


# ---------------------------------------------------------------------------
PROMPT = "Spade sat down in the armchair, and"
PROMPT2 = "Holmes took out his magnifying"
TEMPS = [0.5, 1.0, 2.0]


def compute_temperature():
    import torch

    from videos.ai.ai5.decoding import gpt2

    torch.set_grad_enabled(False)
    tok, model = gpt2()
    ids = tok(PROMPT, return_tensors="pt")["input_ids"]
    z = model(ids).logits[0, -1].numpy().astype(float)
    top = np.argsort(-z)[:10]
    out = dict(prompt=PROMPT, temps=TEMPS, top_tokens=[tok.decode([int(i)]) for i in top], top=top,
               logits=z.astype(np.float32))
    for T in TEMPS:
        p = np.exp((z - z.max()) / T)
        p /= p.sum()
        out[f"p{T}"] = p[top]
        out[f"H{T}"] = float(-(p[p > 0] * np.log2(p[p > 0])).sum())
    samples = {}
    for k, T in enumerate([0.0] + TEMPS):
        torch.manual_seed(11 + k)
        gen = model.generate(ids, max_new_tokens=24, do_sample=T > 0, temperature=T if T > 0 else None,
                             top_k=0, pad_token_id=tok.eos_token_id)
        samples[str(T)] = tok.decode(gen[0, ids.shape[1]:]).replace("\n", " ")
    out["samples"] = samples
    assert out["H0.5"] < out["H1.0"] < out["H2.0"]
    # a confident context, for the truncation rules: one word is nearly certain
    ids2 = tok(PROMPT2, return_tensors="pt")["input_ids"]
    z2 = model(ids2).logits[0, -1].numpy().astype(float)
    top2 = np.argsort(-z2)[:10]
    out.update(prompt2=PROMPT2, logits2=z2.astype(np.float32), top2=top2, top_tokens2=[tok.decode([int(i)]) for i in top2])
    return out


# ---------------------------------------------------------------------------
def compute_markov():
    c1 = ai1()
    if not c1.path("bigram").exists():
        c1._save("bigram", c1.ITEMS["bigram"]())
    P = np.asarray(c1.load("bigram")["cond"])  # rows: the letter now; columns: the next
    if not c1.path("letters").exists():
        c1._save("letters", c1.ITEMS["letters"]())
    freq = np.asarray(c1.load("letters")["p"])
    start = c1.ALPHA27.index("q")
    d = np.zeros(27)
    d[start] = 1.0
    dists, tv = [d.copy()], [0.5 * np.abs(d - freq).sum()]
    for _ in range(12):
        d = d @ P
        dists.append(d.copy())
        tv.append(0.5 * float(np.abs(d - freq).sum()))
    w = np.sort(np.abs(np.linalg.eigvals(P)))[::-1]
    # the chain's own stationary distribution (left eigenvector of eigenvalue 1)
    vals, vecs = np.linalg.eig(P.T)
    st = np.real(vecs[:, np.argmin(np.abs(vals - 1))])
    st /= st.sum()
    assert 0.5 * np.abs(st - freq).sum() < 0.01  # it is the letter frequencies
    assert tv[-1] < 0.01 and w[0] > 0.999 and w[1] < 0.75
    # three states: vowel, consonant, space (the joint pair table, pooled)
    cls = np.array([0 if ch == " " else 1 if ch in "aeiou" else 2 for ch in c1.ALPHA27])
    J = freq[:, None] * P
    J3 = np.array([[J[np.ix_(cls == a, cls == b)].sum() for b in range(3)] for a in range(3)])
    P3 = J3 / J3.sum(1, keepdims=True)
    vals3, vecs3 = np.linalg.eig(P3.T)
    pi3 = np.real(vecs3[:, np.argmin(np.abs(vals3 - 1))])
    pi3 /= pi3.sum()
    walk, x = [], 1  # one walker, from "vowel"
    g = rng(1906)  # Markov, 1906
    for _ in range(400):
        x = int(g.choice(3, p=P3[x]))
        walk.append(x)
    return dict(dists=np.array(dists), tv=np.array(tv), freq=freq, stationary=st, lam2=float(w[1]), start="q", P=P,
                P3=P3, pi3=pi3, walk3=walk, states3=["space", "vowel", "consonant"])


# ---------------------------------------------------------------------------
def compute_montecarlo():
    g = rng(31415)
    N = 4000
    pts = g.random((N, 2)) * 2 - 1
    inside = (pts ** 2).sum(1) <= 1
    est = 4 * np.cumsum(inside) / np.arange(1, N + 1)
    # the error shrinks like 1 / sqrt(N): 200 independent runs at each N
    Ns = np.array([10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000])
    rms = []
    for n in Ns:
        runs = [4 * ((g.random((n, 2)) * 2 - 1) ** 2).sum(1).__le__(1).mean() for _ in range(200)]
        rms.append(float(np.sqrt(np.mean((np.array(runs) - math.pi) ** 2))))
    slope = float(np.polyfit(np.log(Ns), np.log(rms), 1)[0])
    assert -0.6 < slope < -0.4
    # a rare event: P(Z > 4) for a standard normal
    true = 0.5 * math.erfc(4 / math.sqrt(2))
    n = 10000
    z = g.normal(size=n)
    plain_hits = int((z > 4).sum())
    y = g.normal(loc=4.0, size=n)  # propose from N(4, 1) instead, and weight
    wts = np.exp(-0.5 * y ** 2) / np.exp(-0.5 * (y - 4) ** 2)
    is_est = float(np.mean((y > 4) * wts))
    assert abs(is_est - true) / true < 0.05
    return dict(pts=pts[:1500], inside=inside[:1500], est=est, N=N, Ns=Ns, rms=np.array(rms), slope=slope,
                true=true, n=n, plain_hits=plain_hits, plain_est=plain_hits / n, is_est=is_est, is_y=y[:400],
                is_w=wts[:400])


# ---------------------------------------------------------------------------
def density2(x, y):
    """Two bumps in the plane (unnormalized)."""
    return (np.exp(-((x + 1.6) ** 2 + (y + 0.6) ** 2) / 0.7) + 0.7 * np.exp(-((x - 1.5) ** 2 + (y - 0.9) ** 2) / 0.5))


def compute_mcmc():
    g = rng(1953)  # Metropolis et al., 1953
    x = np.array([-3.0, 2.0])
    chain, acc = [x.copy()], 0
    for _ in range(6000):
        y = x + g.normal(scale=0.7, size=2)
        if g.random() < density2(*y) / density2(*x):
            x = y
            acc += 1
        chain.append(x.copy())
    chain = np.array(chain)
    left = float(np.mean(chain[1000:, 0] < 0))
    # the true share of the left bump: 0.7 / (0.7 + 0.7 * 0.5) = 2/3
    assert abs(left - 2 / 3) < 0.12, left
    return dict(chain=chain, accept=acc / 6000, left=left, true_left=2 / 3)


# ---------------------------------------------------------------------------
def compute_brownian():
    g = rng(1905)  # Einstein, 1905
    out = {}
    for n in (8, 64, 1024):
        steps = g.choice([-1.0, 1.0], size=(3, n)) / math.sqrt(n)
        out[f"walk{n}"] = np.concatenate([np.zeros((3, 1)), np.cumsum(steps, 1)], 1)
    paths = np.concatenate([np.zeros((60, 1)), np.cumsum(g.normal(size=(60, 400)) * math.sqrt(1 / 400), 1)], 1)
    ends = np.cumsum(g.normal(size=(20000, 4)) * 0.5, 1)  # W at t = 0.25, 0.5, 0.75, 1
    var = ends.var(0)
    assert np.allclose(var, [0.25, 0.5, 0.75, 1.0], rtol=0.05)
    return dict(**out, paths=paths, ends=np.array([np.histogram(ends[:, k], bins=40, range=(-3, 3))[0] for k in range(4)]),
                var=var)


# ---------------------------------------------------------------------------
def compute_diffusion():
    g = rng(2020)
    # Ornstein-Uhlenbeck: dx = -theta x dt + sigma dW, from x0 = 2.5
    theta, sigma, dt, T = 1.0, 0.8, 0.01, 4.0
    n = int(T / dt)
    x = np.full(40, 2.5)
    paths = [x.copy()]
    for _ in range(n):
        x = x - theta * x * dt + sigma * math.sqrt(dt) * g.normal(size=40)
        paths.append(x.copy())
    paths = np.array(paths).T
    ts = np.array([0.25, 0.5, 1.0, 2.0, 4.0])
    mean = 2.5 * np.exp(-theta * ts)
    var = sigma ** 2 / (2 * theta) * (1 - np.exp(-2 * theta * ts))
    # data with two peaks, noised the way diffusion models do: x_t = sqrt(a) x_0 + sqrt(1 - a) noise
    xs = np.linspace(-4, 4, 401)
    data_mu, data_s, data_w = np.array([-1.5, 1.2]), np.array([0.35, 0.5]), np.array([0.45, 0.55])
    alphas = np.array([1.0, 0.8, 0.5, 0.2, 0.0])
    dens, scores = [], []
    for a in alphas:
        mu, var_ = math.sqrt(a) * data_mu, a * data_s ** 2 + (1 - a)
        comp = data_w[:, None] * np.exp(-0.5 * (xs[None] - mu[:, None]) ** 2 / var_[:, None]) / np.sqrt(2 * math.pi * var_[:, None])
        p = comp.sum(0)
        dens.append(p)
        dp = (comp * (-(xs[None] - mu[:, None]) / var_[:, None])).sum(0)
        scores.append(dp / p)  # the score: the slope of log p
    dens = np.array(dens)
    assert abs(dens[-1].max() - 1 / math.sqrt(2 * math.pi)) < 1e-6  # all noise: a standard normal
    # Fokker-Planck for dx = -x/2 dt + dW (the same noising, alpha = e^{-t}):
    #   dp/dt = d/dx (x p / 2) + 1/2 d2p/dx2, solved on the grid, against 20,000 particles
    h, fdt = xs[1] - xs[0], 0.0002
    p = dens[0].copy()
    part = np.concatenate([g.normal(data_mu[k], data_s[k], size=int(20000 * data_w[k])) for k in range(2)])
    fp_ts = [0.0, 0.25, 0.7, 1.6, 4.0]
    fp, hist, t, k = [p.copy()], [np.histogram(part, bins=80, range=(-4, 4), density=True)[0]], 0.0, 1
    while k < len(fp_ts):
        flux = 0.5 * xs * p
        p = p + fdt * ((np.roll(flux, -1) - np.roll(flux, 1)) / (2 * h)
                       + 0.5 * (np.roll(p, -1) - 2 * p + np.roll(p, 1)) / h ** 2)
        p[0] = p[-1] = 0.0
        part = part - 0.5 * part * fdt + math.sqrt(fdt) * g.normal(size=part.size)
        t += fdt
        if t >= fp_ts[k] - 1e-9:
            fp.append(p.copy())
            hist.append(np.histogram(part, bins=80, range=(-4, 4), density=True)[0])
            k += 1
    fp, hist = np.array(fp), np.array(hist)
    # the grid solution matches the exact noised density at alpha = e^{-t}, and so do the particles
    fp_err, hist_err = [], []
    for k, tt in enumerate(fp_ts):
        a = math.exp(-tt)
        mu, var_ = math.sqrt(a) * data_mu, a * data_s ** 2 + (1 - a)
        exact = (data_w[:, None] * np.exp(-0.5 * (xs[None] - mu[:, None]) ** 2 / var_[:, None])
                 / np.sqrt(2 * math.pi * var_[:, None])).sum(0)
        fp_err.append(float(np.abs(fp[k] - exact).max()))
        hist_err.append(float(np.abs(hist[k] - exact[2::5][:80]).max()))
    assert max(fp_err) < 0.01 and max(hist_err) < 0.08, (fp_err, hist_err)
    return dict(theta=theta, sigma=sigma, dt=dt, ou_paths=paths[:, ::4], ou_t=np.arange(0, n + 1, 4) * dt, ts=ts, ou_mean=mean,
                ou_var=var, xs=xs, alphas=alphas, dens=dens, scores=np.array(scores), fp_ts=fp_ts, fp=fp, fp_hist=hist,
                fp_err=fp_err, hist_err=hist_err)


# ---------------------------------------------------------------------------
def glyph_points(text="AI", n=1500, seed=0):
    """Points filling the letters, scaled to about 4.8 units wide and centred."""
    import subprocess

    from PIL import Image, ImageDraw, ImageFont

    font = None
    for name in ("Latin Modern Roman:bold", "DejaVu Serif:bold"):
        try:
            f = subprocess.run(["fc-match", "-f", "%{file}", name], capture_output=True, text=True).stdout.strip()
            font = ImageFont.truetype(f, 400)
            break
        except Exception:
            continue
    font = font or ImageFont.load_default(400)
    img = Image.new("L", (900, 520), 0)
    ImageDraw.Draw(img).text((450, 260), text, fill=255, font=font, anchor="mm")
    a = np.asarray(img) > 128
    ys, xs = np.nonzero(a)
    g = rng(seed)
    k = g.choice(len(xs), size=n, replace=False)
    pts = np.stack([xs[k] + g.random(n), -(ys[k] + g.random(n))], 1).astype(float)
    pts -= (pts.max(0) + pts.min(0)) / 2
    return pts * (2.4 / np.abs(pts[:, 0]).max())


def compute_shape():
    g = rng(2015)  # Sohl-Dickstein et al., 2015
    data = glyph_points("AI", 1500)
    s0 = 0.03  # each data point a tiny blob
    # forward: dx = -x/2 dt + dW from t = 0 to 5, so x_t = sqrt(a) x_0 + sqrt(1 - a) noise with a = e^{-t}
    T, steps, keep = 5.0, 500, 10
    dt = T / steps
    idx = g.choice(len(data), size=600, replace=False)
    x = data[idx] + s0 * g.normal(size=(600, 2))
    fwd = [x.copy()]
    for k in range(steps):
        x = x - 0.5 * x * dt + math.sqrt(dt) * g.normal(size=x.shape)
        if (k + 1) % keep == 0:
            fwd.append(x.copy())
    fwd = np.array(fwd)  # (51, 600, 2)

    def score(x, t):
        a = math.exp(-t)
        mu, var = math.sqrt(a) * data, a * s0 ** 2 + 1 - a
        d2 = ((x[:, None, :] - mu[None]) ** 2).sum(-1)
        w = np.exp(-(d2 - d2.min(1, keepdims=True)) / (2 * var))
        w /= w.sum(1, keepdims=True)
        return (w @ mu - x) / var

    # backward: the reverse-time SDE, dx = [x/2 + score] dt + dW as time runs from 5 down to 0
    x = g.normal(size=(600, 2))
    bwd = [x.copy()]
    ts = np.linspace(T, 0, steps + 1)
    for k in range(steps):
        x = x + (0.5 * x + score(x, ts[k])) * dt + math.sqrt(dt) * g.normal(size=x.shape)
        if (k + 1) % keep == 0:
            bwd.append(x.copy())
    bwd = np.array(bwd)
    # the reverse process lands on the letters: each final point is close to some data point
    final_d = np.sqrt(((bwd[-1][:, None] - data[None]) ** 2).sum(-1)).min(1)
    assert np.median(final_d) < 0.1, np.median(final_d)
    # the score field on a grid at a few noise levels
    gx = np.linspace(-3.2, 3.2, 17)
    gy = np.linspace(-1.8, 1.8, 10)
    G = np.stack(np.meshgrid(gx, gy), -1).reshape(-1, 2)
    field = {f"field{t}": score(G, t) for t in (2.0, 0.5, 0.1)}
    return dict(data=data, fwd=fwd, bwd=bwd, T=T, grid=G, final_med=float(np.median(final_d)), **field)


# ---------------------------------------------------------------------------
# Chapter 1: the law of large numbers, and the central limit theorem by repeated convolution
# ---------------------------------------------------------------------------
def compute_lln():
    """Bernoulli's law: the running share of heads in six runs of 5,000 fair flips."""
    g = rng(1713)  # Ars Conjectandi, 1713
    n = 5000
    flips = g.integers(0, 2, size=(6, n))
    run = np.cumsum(flips, 1) / np.arange(1, n + 1)
    idx = np.unique(np.round(np.logspace(0, math.log10(n), 160)).astype(int)) - 1
    return dict(n=n, idx=idx + 1, run=run[:, idx], final=run[:, -1])


def _conv_family(kind: str, dx: float, ns):
    """The density of a sum of n independent pieces, by convolving the piece's density with itself again and again
    on a grid of spacing dx (masses of the cells [i dx - dx/2, i dx + dx/2]).  Returns, for each n in ``ns``, the
    standardized sum's density on a grid and its Kolmogorov distance from the standard normal CDF."""
    from scipy.signal import fftconvolve
    from scipy.special import ndtr

    if kind == "exp":  # Exp(1): mean 1, variance 1, skewed
        edges = (np.arange(0, int(40 / dx) + 2) - 0.5) * dx
        edges[0] = 0.0
        F = 1 - np.exp(-edges)
        mu, var = 1.0, 1.0
    else:  # Uniform(0, 1): symmetric
        edges = (np.arange(0, int(1 / dx) + 2) - 0.5) * dx
        F = np.clip(edges, 0, 1)
        mu, var = 0.5, 1 / 12
    piece = np.diff(F)
    piece /= piece.sum()
    out, d, k = {}, np.array([1.0]), 0
    rho = None
    xs0 = np.arange(len(piece)) * dx
    rho = float((piece * np.abs(xs0 - mu) ** 3).sum())
    for n in range(1, max(ns) + 1):
        d = fftconvolve(d, piece)
        d = np.maximum(d, 0)
        d /= d.sum()
        if n in ns:
            xs = np.arange(len(d)) * dx
            sd = math.sqrt(n * var)
            cdf_hi = np.cumsum(d)  # P(S <= x_i + dx/2)
            z_hi = (xs + dx / 2 - n * mu) / sd
            z_lo = (xs - dx / 2 - n * mu) / sd
            dist = float(max(np.abs(cdf_hi - ndtr(z_hi)).max(), np.abs(cdf_hi - d - ndtr(z_lo)).max()))
            zg = np.linspace(-4, 4, 161)
            dens = np.interp(zg, (xs - n * mu) / sd, d / dx * sd, left=0.0, right=0.0)
            out[n] = (dist, dens)
            k += 1
    return out, rho / var ** 1.5


def compute_conv():
    """Sums of n pieces, n = 1 ... 64, for a skewed piece (exponential) and a symmetric one (uniform): the density by
    repeated convolution, and its distance from the bell (Kolmogorov: the largest gap between the CDFs), against
    the Berry-Esseen bound C rho / (sigma^3 sqrt n), C = 0.4748 (Shevtsova 2011)."""
    from scipy.stats import gamma

    ns = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
    show = [1, 2, 3, 5, 10, 30]
    out = dict(ns=ns, show=show, zg=np.linspace(-4, 4, 161), C=0.4748)
    for kind, dx in (("exp", 0.005), ("uni", 0.001)):
        res, ratio = _conv_family(kind, dx, sorted(set(ns) | set(show)))
        out[f"{kind}_dist"] = np.array([res[n][0] for n in ns])
        out[f"{kind}_dens"] = np.array([res[n][1] for n in show])
        out[f"{kind}_ratio"] = ratio  # rho / sigma^3
        out[f"{kind}_bound"] = 0.4748 * ratio / np.sqrt(np.array(ns, float))
        out[f"{kind}_slope"] = float(np.polyfit(np.log(ns[3:]), np.log(out[f"{kind}_dist"][3:]), 1)[0])
    # the grid convolution agrees with the exact answer for exponentials (a sum of n is Gamma(n, 1))
    from scipy.special import ndtr  # noqa: F401
    for j, n in enumerate(ns):
        z = np.linspace(-6, 8, 4001)
        exact = float(np.abs(gamma.cdf(n + z * math.sqrt(n), n) - ndtr(z)).max())
        assert abs(exact - out["exp_dist"][j]) < 2e-3, (n, exact, out["exp_dist"][j])
    assert abs(out["exp_ratio"] - (12 / math.e - 2)) < 1e-2 and abs(out["uni_ratio"] - (1 / 32) / (1 / 12) ** 1.5) < 1e-2
    assert np.all(out["exp_dist"] <= out["exp_bound"]) and np.all(out["uni_dist"] <= out["uni_bound"])
    return out


# ---------------------------------------------------------------------------
# Chapter 2: Gaussians in several dimensions, and conditioning
# ---------------------------------------------------------------------------
def compute_gauss():
    """A correlated pair (sd 1 and 1.4, correlation 0.75): 2,000 points to draw, and 400,000 to check the conditional
    of x1 given x2 = 1.5 against the Schur complement; then the same check in four dimensions, two given two."""
    g = rng(1886)  # Galton's regression, 1886
    s1, s2, r = 1.0, 1.4, 0.75
    S = np.array([[s1 * s1, r * s1 * s2], [r * s1 * s2, s2 * s2]])
    L = np.linalg.cholesky(S)
    z = g.normal(size=(400000, 2))
    x = z @ L.T
    a, w = 1.5, 0.02
    sl = np.abs(x[:, 1] - a) < w
    m_th, v_th = S[0, 1] / S[1, 1] * a, S[0, 0] - S[0, 1] ** 2 / S[1, 1]
    m_emp, v_emp = float(x[sl, 0].mean()), float(x[sl, 0].var())
    n_sl = int(sl.sum())
    assert abs(m_emp - m_th) < 4 * math.sqrt(v_th / n_sl) + 0.02 and abs(v_emp / v_th - 1) < 0.08
    evals, evecs = np.linalg.eigh(S)
    # four dimensions: condition (x1, x2) on (x3, x4) = b
    A = g.normal(size=(4, 4))
    S4 = A @ A.T / 4 + 0.5 * np.eye(4)
    L4 = np.linalg.cholesky(S4)
    X = g.normal(size=(3_000_000, 4)) @ L4.T
    b = np.array([0.6, -0.4])
    box = (np.abs(X[:, 2] - b[0]) < 0.04) & (np.abs(X[:, 3] - b[1]) < 0.04)
    Saa, Sab, Sbb = S4[:2, :2], S4[:2, 2:], S4[2:, 2:]
    m4 = Sab @ np.linalg.solve(Sbb, b)
    C4 = Saa - Sab @ np.linalg.solve(Sbb, Sab.T)
    m4e, C4e = X[box, :2].mean(0), np.cov(X[box, :2].T)
    n4 = int(box.sum())
    assert np.abs(m4e - m4).max() < 0.05 and np.abs(C4e - C4).max() < 0.05, (m4e, m4, C4e, C4)
    return dict(S=S, L=L, pts=x[:2000], z=z[:2000], a=a, w=w, n_slice=n_sl, slice_x1=x[sl, 0][:400], m_th=m_th,
                v_th=v_th, m_emp=m_emp, v_emp=v_emp, evals=evals, evecs=evecs, S4=S4, b4=b, m4=m4, C4=C4, m4e=m4e,
                C4e=C4e, n4=n4, err4=float(max(np.abs(m4e - m4).max(), np.abs(C4e - C4).max())), r=r, s1=s1, s2=s2)


# ---------------------------------------------------------------------------
# Chapters 3 and 4: the bias of maximum likelihood; Fisher information and the Cramér-Rao bound
# ---------------------------------------------------------------------------
def compute_mlebias():
    """sigma^2 by maximum likelihood (divide by n) and by Bessel's correction (divide by n - 1), on 40,000 samples of
    each size n from a standard normal."""
    g = rng(1922)  # Fisher, 1922
    ns = [2, 3, 5, 10, 20, 50, 100]
    R = 40000
    out = dict(ns=ns, R=R)
    mle, bes, se = [], [], []
    for n in ns:
        x = g.normal(size=(R, n))
        v = x.var(1)  # divide by n: the maximum-likelihood estimate
        mle.append(float(v.mean()))
        bes.append(float((v * n / (n - 1)).mean()))
        se.append(float(v.std() / math.sqrt(R)))
        if n == 5:
            out["hist5"] = np.histogram(v, bins=40, range=(0, 4))[0]
    out.update(mle=np.array(mle), bessel=np.array(bes), se=np.array(se), theory=np.array([(n - 1) / n for n in ns]))
    assert np.all(np.abs(out["mle"] - out["theory"]) < 5 * out["se"] + 1e-3)
    return out


def _cauchy_mle(x):
    """The maximum-likelihood location of each row of x (standard Cauchy samples).  The likelihood can have several
    peaks, so local climbs start from every data point (small samples) or from a grid around the median (large ones,
    where the peak is near the median), and the highest peak wins."""
    R, n = x.shape
    med = np.median(x, 1)

    def ll(t):
        return -np.log1p((x - t[:, None]) ** 2).sum(1)

    def climb(t):
        for _ in range(40):
            u = x - t[:, None]
            s = (2 * u / (1 + u * u)).sum(1)
            h = (2 * (u * u - 1) / (1 + u * u) ** 2).sum(1)
            t = t + np.clip(np.where(h > 1e-9, s / np.maximum(h, 1e-9), s), -0.3, 0.3)
        return t

    def score(t):
        u = x - t[:, None]
        return (2 * u / (1 + u * u)).sum(1)

    starts = [x[:, j] for j in range(n)] + [med] if n <= 20 else [med + o for o in np.linspace(-3, 3, 25)]
    best, best_ll = None, None
    for s0 in starts:
        t = climb(s0.copy())
        v = ll(t)
        if best is None:
            best, best_ll = t, v
        else:
            better = v > best_ll
            best, best_ll = np.where(better, t, best), np.where(better, v, best_ll)
    # polish: bisection on the score, which falls through zero at the peak
    lo, hi = best - 0.05, best + 0.05
    for _ in range(12):
        bad = (score(lo) < 0) | (score(hi) > 0)
        if not bad.any():
            break
        lo, hi = np.where(bad, best - 2 * (best - lo), lo), np.where(bad, best + 2 * (hi - best), hi)
    for _ in range(60):
        mid = (lo + hi) / 2
        pos = score(mid) > 0
        lo, hi = np.where(pos, mid, lo), np.where(pos, hi, mid)
    best = (lo + hi) / 2
    u = x - best[:, None]
    assert np.abs((2 * u / (1 + u * u)).sum(1)).max() < 1e-6
    return best, med


def compute_fisher():
    """The location of a Cauchy distribution: the maximum-likelihood estimate against the median and the mean, on
    4,000 samples of each size; n times the variance against the Cramér-Rao bound 1/I = 2.  And the score at the
    true value: mean 0, variance I = 1/2 per point."""
    g = rng(1925)  # Fisher, 1925
    ns = [5, 10, 20, 50, 100, 200, 500]
    R = 4000
    mle_v, med_v, mean_iqr, mle_v_se = [], [], [], []
    hists = {}
    for n in ns:
        x = g.standard_cauchy(size=(R, n))
        t, med = _cauchy_mle(x)
        mle_v.append(float(n * t.var()))
        med_v.append(float(n * med.var()))
        mle_v_se.append(float(n * t.var() * math.sqrt(2 / (R - 1))))
        mean_iqr.append(float(np.subtract(*np.percentile(x.mean(1), [75, 25]))))
        if n in (10, 100):
            hists[f"mle{n}"] = np.histogram(t, bins=48, range=(-1.2, 1.2))[0]
            hists[f"med{n}"] = np.histogram(med, bins=48, range=(-1.2, 1.2))[0]
            hists[f"mean{n}"] = np.histogram(x.mean(1), bins=48, range=(-1.2, 1.2))[0]
    x = g.standard_cauchy(size=200000)
    s = 2 * x / (1 + x * x)
    score_mean, score_var = float(s.mean()), float(s.var())
    assert abs(score_var - 0.5) < 0.01 and abs(score_mean) < 0.01
    assert abs(mle_v[-1] - 2) < 0.25 and abs(med_v[-1] - math.pi ** 2 / 4) < 0.3
    return dict(ns=ns, R=R, mle_nvar=np.array(mle_v), med_nvar=np.array(med_v), mle_nvar_se=np.array(mle_v_se),
                mean_iqr=np.array(mean_iqr), score_mean=score_mean, score_var=score_var, cr=2.0,
                med_limit=math.pi ** 2 / 4, **hists)


# ---------------------------------------------------------------------------
# Chapter 5: Bayes; MAP as regularization
# ---------------------------------------------------------------------------
def compute_map():
    """Ten noisy points from sin(2 pi x); a degree-9 polynomial by maximum likelihood (least squares) and by MAP with a
    Gaussian prior on the weights (ridge, lambda = sigma^2 / tau^2), over 200 training sets; test error against lambda."""
    g = rng(2006)  # Bishop's Pattern Recognition and Machine Learning, 2006: the same example
    n, deg, sig = 10, 9, 0.25
    lams = np.logspace(-10, 1, 45)
    xt = np.linspace(0, 1, 200)
    Pt = np.vander(xt, deg + 1, increasing=True)
    yt = np.sin(2 * np.pi * xt)
    errs, mle_err = [], []
    keep = {}
    for s in range(200):
        x = np.linspace(0, 1, n)
        y = np.sin(2 * np.pi * x) + sig * g.normal(size=n)
        P = np.vander(x, deg + 1, increasing=True)
        w_mle = np.linalg.lstsq(P, y, rcond=None)[0]
        mle_err.append(float(np.mean((Pt @ w_mle - yt) ** 2)))
        row = []
        for lam in lams:
            w = np.linalg.solve(P.T @ P + lam * np.eye(deg + 1), P.T @ y)
            row.append(float(np.mean((Pt @ w - yt) ** 2)))
        errs.append(row)
        if s == 0:
            keep = dict(x=x, y=y, w_mle=w_mle)
    errs = np.array(errs)
    med = np.median(errs, 0)
    best = int(np.argmin(med))
    x, y = keep["x"], keep["y"]
    P = np.vander(x, deg + 1, increasing=True)
    fits = {}
    for name, lam in (("best", lams[best]), ("big", 1.0)):
        fits[name] = Pt @ np.linalg.solve(P.T @ P + lam * np.eye(deg + 1), P.T @ y)
    return dict(n=n, deg=deg, sigma=sig, lams=lams, med_err=med, q25=np.percentile(errs, 25, 0),
                q75=np.percentile(errs, 75, 0), mle_med=float(np.median(mle_err)), best_lam=float(lams[best]),
                best_err=float(med[best]), x=x, y=y, xt=xt, fit_mle=np.clip(Pt @ keep["w_mle"], -3, 3),
                fit_best=fits["best"], fit_big=fits["big"], w_mle_norm=float(np.linalg.norm(keep["w_mle"])),
                tau_best=float(sig / math.sqrt(lams[best])))


# ---------------------------------------------------------------------------
# Chapter 6: maximum entropy
# ---------------------------------------------------------------------------
def _maxent_grid(x, feats, targets, iters=60):
    """The maximum-entropy density on grid x with E[f_k] = targets: p = exp(lam . f) / Z, lam by Newton's method on
    the dual (log Z - lam . targets; its gradient is E_p[f] - target, its Hessian the covariance of f)."""
    F = np.stack([f(x) for f in feats], 1)
    lam = np.zeros(len(feats))
    for _ in range(iters):
        a = F @ lam
        p = np.exp(a - a.max())
        p /= p.sum()
        m = p @ F
        Cv = (F * p[:, None]).T @ F - np.outer(m, m)
        lam = lam - np.linalg.solve(Cv + 1e-12 * np.eye(len(feats)), m - targets)
    return p, lam


def compute_maxent():
    """Jaynes's die (1962): faces 1-6 with average 4.5.  The maximum-entropy answer by Newton's method, fitted again by
    plain gradient steps on the dual (the training replayed); 20,000 other dice with the same average, all lower in
    entropy.  Then on the line: fix the mean and the variance and the answer is the bell; fix the mean distance
    from 0 and it is Laplace's two-sided exponential."""
    k = np.arange(1, 7, dtype=float)
    p, lam = _maxent_grid(k, [lambda v: v], np.array([4.5]))
    H = float(-(p * np.log(p)).sum())
    assert abs(p @ k - 4.5) < 1e-12
    # gradient ascent on the dual, from the uniform die
    path, lam_t, eta = [], 0.0, 0.04
    for t in range(61):
        q = np.exp(lam_t * k)
        q /= q.sum()
        path.append((lam_t, *q))
        lam_t += eta * (4.5 - q @ k)
    path = np.array(path)
    assert abs(path[-1, 0] - lam[0]) < 1e-3
    # other dice with the same average: the max-ent die plus random moves that keep the total and the average
    g = rng(1957)  # Jaynes, 1957
    N = np.linalg.svd(np.stack([np.ones(6), k]))[2][2:].T  # a basis of moves that change neither
    others = []
    while len(others) < 20000:
        d = N @ g.normal(size=4)
        t = g.uniform(0.05, 1.0) * np.min(np.where(d < 0, -p / np.minimum(d, -1e-12), np.inf))
        q = p + t * d
        if q.min() > 0:
            others.append(q)
    others = np.array(others)
    assert np.abs(others @ k - 4.5).max() < 1e-9
    Ho = -(others * np.log(others)).sum(1)
    assert Ho.max() < H
    # on the line
    x = np.linspace(-8, 8, 4001)
    pg, lg = _maxent_grid(x, [lambda v: v, lambda v: v * v], np.array([0.0, 1.0]))
    pl, ll_ = _maxent_grid(x, [lambda v: np.abs(v)], np.array([1.0]))
    dx = x[1] - x[0]
    gauss = np.exp(-x * x / 2) / math.sqrt(2 * math.pi)
    lap = 0.5 * np.exp(-np.abs(x))
    err_g, err_l = float(np.abs(pg / dx - gauss).max()), float(np.abs(pl / dx - lap).max())
    assert err_g < 1e-3 and err_l < 1e-2
    hist = np.histogram(Ho, bins=40, range=(Ho.min(), H))[0]
    return dict(p=p, lam=float(lam[0]), H=H, H_uniform=math.log(6), path=path, others=others[:6], H_others_max=float(Ho.max()),
                H_hist=hist, H_lo=float(Ho.min()), n_others=len(Ho), x=x[::10], gauss_fit=(pg / dx)[::10],
                lap_fit=(pl / dx)[::10], gauss_lams=lg, lap_lam=float(ll_[0]), err_g=err_g, err_l=err_l)


# ---------------------------------------------------------------------------
# Chapter 7: concentration
# ---------------------------------------------------------------------------
def compute_tails():
    """The average of n = 100 fair coin flips: P(average - 1/2 >= eps), exactly (binomial) and over 1,000,000
    simulated runs, against the bounds of Markov, Chebyshev, Chernoff and Hoeffding; and the n each guarantees."""
    from scipy.stats import binom

    g = rng(1963)  # Hoeffding, 1963
    n = 100
    sims = g.binomial(n, 0.5, size=1_000_000) / n
    eps = np.round(np.arange(0.02, 0.31, 0.01), 2)
    exact = np.array([binom.sf(math.ceil(n * (0.5 + e) - 1e-9) - 1, n, 0.5) for e in eps])
    sim = np.array([(sims - 0.5 >= e - 1e-12).mean() for e in eps])

    def kl(a, b=0.5):
        return a * math.log(a / b) + (1 - a) * math.log((1 - a) / (1 - b))

    markov = 0.5 / (0.5 + eps)
    cheb = np.minimum(1.0, 0.25 / (n * eps ** 2))
    chern = np.exp(-n * np.array([kl(0.5 + e) for e in eps]))
    hoeff = np.exp(-2 * n * eps ** 2)
    assert np.all(exact <= chern + 1e-15) and np.all(chern <= hoeff + 1e-15) and np.all(exact <= cheb)
    # how many flips guarantee P(average - 1/2 >= 0.05) <= 0.05?
    e0, d0 = 0.05, 0.05
    need = dict(chebyshev=math.ceil(0.25 / (e0 ** 2 * d0)), hoeffding=math.ceil(math.log(1 / d0) / (2 * e0 ** 2)),
                chernoff=math.ceil(math.log(1 / d0) / kl(0.5 + e0)))
    m = 1
    while binom.sf(math.ceil(m * (0.5 + e0) - 1e-9) - 1, m, 0.5) > d0 or binom.sf(
            math.ceil((m + 1) * (0.5 + e0) - 1e-9) - 1, m + 1, 0.5) > d0:
        m += 1
    need["exact"] = m
    j = int(np.argmin(np.abs(eps - 0.1)))
    return dict(n=n, eps=eps, exact=exact, sim=sim, markov=markov, cheb=cheb, chern=chern, hoeff=hoeff, need=need,
                e0=e0, d0=d0, j10=j, hist=np.bincount(np.rint(sims * n).astype(int), minlength=n + 1))


# ---------------------------------------------------------------------------
# Chapter 8: sampling
# ---------------------------------------------------------------------------
def compute_draws():
    """Inverse-CDF exponentials, rejection-sampled Beta(2, 5), Box-Muller normals; the Gumbel-max trick against the
    softmax; Gumbel-softmax at six temperatures."""
    from scipy.stats import beta, kstest

    g = rng(1951)  # von Neumann, 1951
    u = g.random(20000)
    ex = -np.log1p(-u)
    ks_exp = float(kstest(ex, "expon").statistic)
    # rejection: Beta(2, 5) under the box of height M = max density
    M = float(beta.pdf(0.2, 2, 5))
    xp, up = g.random(20000), g.random(20000) * M
    acc = up < beta.pdf(xp, 2, 5)
    rate = float(acc.mean())
    ks_beta = float(kstest(xp[acc], beta(2, 5).cdf).statistic)
    # Box-Muller
    u1, u2 = g.random(50000), g.random(50000)
    R = np.sqrt(-2 * np.log1p(-u1))
    z1, z2 = R * np.cos(2 * np.pi * u2), R * np.sin(2 * np.pi * u2)
    z = np.concatenate([z1, z2])
    ks_bm = float(kstest(z, "norm").statistic)
    corr = float(np.corrcoef(z1, z2)[0, 1])
    # Gumbel-max: argmax(z + Gumbel noise) against the softmax of six scores
    zl = np.array([2.0, 1.4, 1.0, 0.3, -0.2, -1.0])
    p = np.exp(zl - zl.max())
    p /= p.sum()
    N = 200000
    G = -np.log(-np.log(g.random((N, 6))))
    pick = np.argmax(zl + G, 1)
    freq = np.bincount(pick, minlength=6) / N
    chi2 = float((((freq - p) * N) ** 2 / (N * p)).sum())
    assert np.abs(freq - p).max() < 0.006 and chi2 < 25
    # Gumbel-softmax: y = softmax((z + G) / tau)
    taus = [0.1, 0.25, 0.5, 1.0, 2.0, 5.0]
    onehot, bias, examples = [], [], {}
    G2 = -np.log(-np.log(g.random((20000, 6))))
    for tau in taus:
        a = (zl + G2) / tau
        y = np.exp(a - a.max(1, keepdims=True))
        y /= y.sum(1, keepdims=True)
        onehot.append(float(y.max(1).mean()))
        bias.append(float(np.abs(y.mean(0) - p).sum()))
        examples[f"y{tau}"] = y[:3]
    return dict(ex=ex[:2000], ks_exp=ks_exp, M=M, rate=rate, ks_beta=ks_beta, xp=xp[:600], up=up[:600],
                acc=acc[:600], bm_u=np.stack([u1[:600], u2[:600]], 1), bm_z=np.stack([z1[:600], z2[:600]], 1),
                ks_bm=ks_bm, corr=corr, z_hist=np.histogram(z, bins=60, range=(-4, 4))[0],
                ex_hist=np.histogram(ex, bins=50, range=(0, 5))[0],
                beta_hist=np.histogram(xp[acc], bins=40, range=(0, 1))[0], scores=zl, p=p, freq=freq, chi2=chi2, N=N,
                taus=taus, onehot=np.array(onehot), gs_bias=np.array(bias), **examples)


# ---------------------------------------------------------------------------
# Chapter 10: mixing and the spectral gap
# ---------------------------------------------------------------------------
def _mixing_time(P, pi, eps=0.25):
    """The smallest t with max over starts of TV(P^t(x, .), pi) <= eps, for a reversible P (by its eigenvectors)."""
    D = np.sqrt(pi)
    Sym = D[:, None] * P / D[None, :]
    Sym = (Sym + Sym.T) / 2
    w, V = np.linalg.eigh(Sym)

    def tv(t):
        Pt = (V * w ** t) @ V.T / D[:, None] * D[None, :]
        return 0.5 * np.abs(Pt - pi[None]).sum(1).max()

    lo, hi = 0, 1
    while tv(hi) > eps:
        lo, hi = hi, hi * 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lo, hi = (mid, hi) if tv(mid) > eps else (lo, mid)
    ws = np.sort(w)[::-1]
    return hi, float(1 - max(ws[1], abs(ws[-1])))


def compute_mixing():
    """A walk on 41 sites, Metropolis moves of one site left or right (half the time it stays: lazy), aimed at a
    two-well distribution exp(-beta U) with U = 4 (x^2 - 1)^2; as the barrier beta rises, the spectral gap shrinks and
    the mixing time grows, between the two bounds (t_rel - 1) ln 2 and t_rel ln(4 / pi_min)."""
    K = 41
    xs = np.linspace(-1.6, 1.6, K)
    U = 4 * (xs ** 2 - 1) ** 2
    betas = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
    rows = []
    keepP = None
    for b in betas:
        pi = np.exp(-b * U)
        pi /= pi.sum()
        P = np.zeros((K, K))
        for i in range(K):
            for j in (i - 1, i + 1):
                if 0 <= j < K:
                    P[i, j] = 0.25 * min(1.0, pi[j] / pi[i])
            P[i, i] = 1 - P[i].sum()
        db = float(np.abs(pi[:, None] * P - (pi[:, None] * P).T).max())
        assert db < 1e-15
        assert np.abs(pi @ P - pi).max() < 1e-14
        tm, gap = _mixing_time(P, pi)
        trel = 1 / gap
        rows.append((b, gap, tm, (trel - 1) * math.log(2), trel * math.log(4 / pi.min())))
        if b == 2.0:
            keepP, keep_pi = P, pi
    rows = np.array(rows)
    assert np.all(rows[:, 3] <= rows[:, 2] + 1) and np.all(rows[:, 2] <= rows[:, 4])
    # from the left end, the distribution at a few times (beta = 2): first one well fills, then slowly the other
    d = np.zeros(K)
    d[0] = 1
    ts, snaps = [0, 30, 300, 3000, 30000, 100000, 300000], []
    t = 0
    for T in ts:
        while t < T:
            d = d @ keepP
            t += 1
        snaps.append(d.copy())
    # English is not reversible: the letter chain's detailed-balance gap
    mk = load("markov")
    Pl, fr = np.asarray(mk["P"]), np.asarray(mk["freq"])
    flow = fr[:, None] * Pl
    asym = float(np.abs(flow - flow.T).max())
    i, j = np.unravel_index(int(np.argmax(np.abs(flow - flow.T))), flow.shape)
    A = " abcdefghijklmnopqrstuvwxyz"
    return dict(xs=xs, U=U, betas=betas, gap=rows[:, 1], tmix=rows[:, 2], lower=rows[:, 3], upper=rows[:, 4],
                pi=keep_pi, ts=ts, snaps=np.array(snaps), slope=float(np.polyfit(np.log(1 / rows[:, 1]),
                                                                                  np.log(rows[:, 2]), 1)[0]),
                asym=asym, asym_pair=A[i] + A[j], flow_ij=float(flow[i, j]), flow_ji=float(flow[j, i]))


# ---------------------------------------------------------------------------
# Chapter 11: importance weights in many dimensions
# ---------------------------------------------------------------------------
def compute_ess():
    """Target N(0, I_d), proposal N(0, 1.25^2 I_d): the effective sample size of 5,000 weighted draws, (sum w)^2 /
    sum w^2, against the dimension, five seeds; theory n / E_q[w^2] = n (s^2 / sqrt(2 s^2 - 1))^-d."""
    s, n = 1.25, 5000
    dims = [1, 2, 5, 10, 20, 50, 100, 200]
    ess, top = [], []
    for seed in range(5):
        g = rng(1949 + seed)  # Metropolis and Ulam, 1949
        row, trow = [], []
        for d in dims:
            y = g.normal(size=(n, d)) * s
            logw = -0.5 * (y ** 2).sum(1) * (1 - 1 / s ** 2) + d * math.log(s)
            w = np.exp(logw - logw.max())
            row.append(float(w.sum() ** 2 / (w ** 2).sum()))
            trow.append(float(w.max() / w.sum()))
        ess.append(row)
        top.append(trow)
    ess, top = np.array(ess), np.array(top)
    theory = n / (s ** 2 / math.sqrt(2 * s ** 2 - 1)) ** np.array(dims, float)
    # the rare-event example of the Monte Carlo chapter: its weights' ESS
    mc = load("montecarlo")
    w = np.asarray(mc["is_w"])
    return dict(s=s, n=n, dims=dims, ess=ess, top=top, theory=theory, ess_rare=float(w.sum() ** 2 / (w ** 2).sum()),
                n_rare=len(w))


# ---------------------------------------------------------------------------
# Chapter 12: the score-function estimator
# ---------------------------------------------------------------------------
def _rosen(th):
    x, y = th[..., 0], th[..., 1]
    return (1 - x) ** 2 + 5 * (y - x * x) ** 2


def compute_scorefn():
    """d/dmu E[x^2], x ~ N(mu, 1), at mu = 1 (truly 2): the score-function estimate's variance against a baseline b,
    and the reparameterized estimate's; then evolution strategies (the same estimator, for a smoothed function) on a
    curved valley, 8 seeds, with and without a baseline, at equal budgets of evaluations."""
    g = rng(1992)  # Williams, 1992
    mu, N = 1.0, 400000
    x = mu + g.normal(size=N)
    s = x - mu  # the score of N(mu, 1) with respect to mu
    f = x ** 2
    bs = np.linspace(-2, 6, 33)
    var_b = np.array([float(((f - b) * s).var()) for b in bs])
    mean_sf = float((f * s).mean())
    b_star = float((f * s * s).mean() / (s * s).mean())
    var_star = float(((f - b_star) * s).var())
    var_rep = float((2 * x).var())  # d/dmu (mu + eps)^2 = 2 (mu + eps)
    assert abs(mean_sf - 2) < 0.03 and var_star < var_b[np.argmin(np.abs(bs))]
    # evolution strategies on f(x, y) = (1 - x)^2 + 5 (y - x^2)^2, from (-1.2, 1.4): the estimate's error at the
    # start (2,000 draws of a population of 16), plain, with the population's mean as baseline, and mirrored
    sig, pop, lr, steps = 0.1, 16, 0.02, 1000
    th0 = np.array([-1.2, 1.4])
    gtrue = np.array([-2 * (1 - th0[0]) - 20 * th0[0] * (th0[1] - th0[0] ** 2), 10 * (th0[1] - th0[0] ** 2)])
    gerr = {}
    for kind in ("plain", "base", "mirror"):
        gg = rng(1973)  # Rechenberg, 1973
        e_ = []
        for _ in range(2000):
            e = gg.normal(size=(pop, 2))
            if kind == "mirror":
                e = np.concatenate([e[: pop // 2], -e[: pop // 2]])
            F = _rosen(th0 + sig * e)
            if kind != "plain":
                F = F - F.mean()
            e_.append(float((((F[:, None] * e).mean(0) / sig - gtrue) ** 2).sum()))
        gerr[kind] = float(np.mean(e_))
    runs = {"plain": [], "base": []}
    finals = {"plain": [], "base": []}
    for kind in ("plain", "base"):
        for seed in range(8):
            gg = rng(2017 + seed)  # Salimans et al., 2017
            th = th0.copy()
            path = [th.copy()]
            for _ in range(steps):
                e = gg.normal(size=(pop, 2))
                F = _rosen(th + sig * e)
                if kind == "base":
                    F = F - F.mean()
                th = th - lr * (F[:, None] * e).mean(0) / sig
                path.append(th.copy())
                if not np.isfinite(th).all() or np.abs(th).max() > 10:  # diverged
                    break
            path = np.array(path)
            finals[kind].append(float(_rosen(th)) if np.abs(th).max() <= 10 else float("inf"))
            runs[kind].append(np.pad(path, ((0, steps + 1 - len(path)), (0, 0)), mode="edge")[::5])
    fp, fb = np.array(finals["plain"]), np.array(finals["base"])
    return dict(mu=mu, N=N, bs=bs, var_b=var_b, mean_sf=mean_sf, b_star=b_star, var_star=var_star, var_rep=var_rep,
                var_0=float((f * s).var()), sig=sig, pop=pop, lr=lr, steps=steps, gerr_plain=gerr["plain"],
                gerr_base=gerr["base"], gerr_mirror=gerr["mirror"], gnorm2=float((gtrue ** 2).sum()),
                paths_plain=np.clip(np.array(runs["plain"]), -10, 10), paths_base=np.clip(np.array(runs["base"]), -10, 10),
                final_plain=np.where(np.isfinite(fp), fp, -1.0), final_base=np.where(np.isfinite(fb), fb, -1.0),
                div_plain=int((~np.isfinite(fp)).sum()), div_base=int((~np.isfinite(fb)).sum()))


# ---------------------------------------------------------------------------
# Chapter 13: Metropolis-Hastings and Langevin dynamics on the two bumps
# ---------------------------------------------------------------------------
def score2(P):
    """grad log density2 at points P (n, 2)."""
    x, y = P[..., 0], P[..., 1]
    e1 = np.exp(-((x + 1.6) ** 2 + (y + 0.6) ** 2) / 0.7)
    e2 = 0.7 * np.exp(-((x - 1.5) ** 2 + (y - 0.9) ** 2) / 0.5)
    gx = e1 * (-2 * (x + 1.6) / 0.7) + e2 * (-2 * (x - 1.5) / 0.5)
    gy = e1 * (-2 * (y + 0.6) / 0.7) + e2 * (-2 * (y - 0.9) / 0.5)
    p = e1 + e2 + 1e-300
    return np.stack([gx / p, gy / p], -1)


def _iact(v):
    """Integrated autocorrelation time (Sokal's window, c = 5)."""
    v = v - v.mean()
    n = len(v)
    f = np.fft.rfft(v, 2 * n)
    ac = np.fft.irfft(f * np.conj(f))[:n]
    ac /= ac[0]
    taus = 1 + 2 * np.cumsum(ac[1:])
    m = np.nonzero(np.arange(1, n) >= 5 * taus)[0]
    tau = taus[m[0]] if len(m) else taus[-1]
    return float(max(tau, 1.0))


def compute_langevin():
    """Three samplers of the two bumps, 20,000 steps each, five seeds, from (-3, 2): random-walk Metropolis (step 0.7),
    unadjusted Langevin (step h = 0.05 and 0.3) and Metropolis-adjusted Langevin (h = 0.3).  Measured: the share in
    the left bump (truly 2/3), the spread within it (truly 0.35 per coordinate), hops between the bumps, and the
    integrated autocorrelation time.  Then 1,500 particles under Langevin dynamics from broad noise, with their
    density on a grid every few steps (the 3D picture)."""
    dens = density2

    def logp(P):
        return np.log(dens(P[..., 0], P[..., 1]) + 1e-300)

    configs = [("rwm", 0.7), ("ula", 0.05), ("ula", 0.3), ("mala", 0.3)]
    T = 20000
    res = {}
    for kind, h in configs:
        rows = []
        for seed in range(5):
            g = rng(1908 + seed)  # Langevin, 1908
            x = np.array([-3.0, 2.0])
            chain = np.empty((T, 2))
            acc = 0
            for t in range(T):
                if kind == "rwm":
                    y = x + h * g.normal(size=2)
                    ok = math.log(g.random()) < logp(y) - logp(x)
                elif kind == "ula":
                    y = x + h * score2(x) + math.sqrt(2 * h) * g.normal(size=2)
                    ok = True
                else:
                    y = x + h * score2(x) + math.sqrt(2 * h) * g.normal(size=2)
                    fwd = -((y - x - h * score2(x)) ** 2).sum() / (4 * h)
                    bwd = -((x - y - h * score2(y)) ** 2).sum() / (4 * h)
                    ok = math.log(g.random()) < logp(y) - logp(x) + bwd - fwd
                if ok:
                    x = y
                    acc += 1
                chain[t] = x
            c = chain[1000:]
            left = c[:, 0] < 0
            side = np.where(c[:, 0] < -0.8, -1, np.where(c[:, 0] > 0.8, 1, 0))
            s_ = side[side != 0]
            hops = int((np.diff(s_) != 0).sum())
            rows.append(dict(left=float(left.mean()), spread=float(c[left, 0].var()), hops=hops,
                             iact=_iact(c[:, 0]), accept=acc / T))
            if seed == 0:
                res[f"{kind}{h}_chain"] = chain[:4000:4]
        for key in rows[0]:
            res[f"{kind}{h}_{key}"] = np.array([r[key] for r in rows])
    # the particle flow: 1,500 particles from broad noise, N(0, 2^2 I), unadjusted Langevin with h = 0.02
    g = rng(2011)  # Welling and Teh, 2011
    P = 2.0 * g.normal(size=(1500, 2))
    h, steps = 0.02, 400
    frames, grids, gt = [P.copy()], [], []
    gx, gy = np.linspace(-4, 4, 41), np.linspace(-3, 3, 31)
    GX, GY = np.meshgrid(gx, gy)
    target = dens(GX, GY)
    target /= target.sum() * (gx[1] - gx[0]) * (gy[1] - gy[0])

    def kde(Q, bw=0.28):
        d2 = (GX[..., None] - Q[:, 0]) ** 2 + (GY[..., None] - Q[:, 1]) ** 2
        return np.exp(-d2 / (2 * bw * bw)).sum(-1) / (len(Q) * 2 * math.pi * bw * bw)

    grid_at = [0, 10, 25, 50, 100, 200, 400]
    l1 = []
    for k in range(steps + 1):
        if k in grid_at:
            K_ = kde(P)
            grids.append(K_)
            gt.append(k * h)
            l1.append(float(np.abs(K_ - target).sum() * (gx[1] - gx[0]) * (gy[1] - gy[0])))
        if k == steps:
            break
        P = P + h * score2(P) + math.sqrt(2 * h) * g.normal(size=P.shape)
        if (k + 1) % 5 == 0:
            frames.append(P.copy())
    res.update(frames=np.array(frames)[:, :600], grids=np.array(grids), grid_t=np.array(gt), grid_steps=grid_at,
               target=target, gx=gx, gy=gy, l1=np.array(l1), flow_h=h, flow_left=float((P[:, 0] < 0).mean()))
    res["configs"] = [f"{k}{h}" for k, h in configs]
    return res


# ---------------------------------------------------------------------------
# Chapters 14-16: quadratic variation, Itô's lemma, Euler-Maruyama
# ---------------------------------------------------------------------------
def compute_qv():
    """Sum (dW)^2 and sum |dW| over [0, 1] at 2^k steps, k = 2..14, on 400 Brownian paths: the quadratic variation
    settles at t = 1 (spread sqrt(2 / n)), the total variation grows like sqrt(2n / pi)."""
    g = rng(1923)  # Wiener, 1923
    K = 14
    n = 2 ** K
    ks = list(range(2, K + 1))
    qv, tv = [], []
    keep = None
    for chunk in range(4):
        dW = g.normal(size=(100, n)) / math.sqrt(n)
        W = np.concatenate([np.zeros((100, 1)), np.cumsum(dW, 1)], 1)
        if chunk == 0:
            keep = W[0]
        q_, t_ = [], []
        for k in ks:
            inc = np.diff(W[:, :: 2 ** (K - k)], axis=1)
            q_.append((inc ** 2).sum(1))
            t_.append(np.abs(inc).sum(1))
        qv.append(np.array(q_).T)
        tv.append(np.array(t_).T)
    qv, tv = np.concatenate(qv), np.concatenate(tv)
    ns = np.array([2 ** k for k in ks], float)
    assert abs(qv[:, -1].mean() - 1) < 0.01 and abs(qv[:, -1].std() / math.sqrt(2 / n) - 1) < 0.15
    path_qv = np.cumsum(np.diff(keep) ** 2)
    return dict(ks=ks, ns=ns, qv_mean=qv.mean(0), qv_sd=qv.std(0), tv_mean=tv.mean(0), tv_theory=np.sqrt(2 * ns / math.pi),
                path=keep[::16], path_qv=path_qv[15::16], n=n, qv_example=qv[:6])


def compute_ito():
    """Riemann sums of the integral of W dW over [0, 1]: left points (Itô) against midpoints (Stratonovich), on 2,000
    paths, and Itô's lemma checked path by path for f(W) = e^W."""
    g = rng(1944)  # Itô, 1944
    ns = [10, 30, 100, 300, 1000, 3000, 10000]
    M = 2000
    left_err, strat_err, lemma_rms, naive_rms = [], [], [], []
    examples = {}
    for n in ns:
        dW = g.normal(size=(M, n)) / math.sqrt(n)
        W = np.concatenate([np.zeros((M, 1)), np.cumsum(dW, 1)], 1)
        left = (W[:, :-1] * dW).sum(1)
        strat = (0.5 * (W[:, :-1] + W[:, 1:]) * dW).sum(1)
        W1 = W[:, -1]
        left_err.append(float(np.sqrt(np.mean((left - (W1 ** 2 - 1) / 2) ** 2))))
        strat_err.append(float(np.sqrt(np.mean((strat - W1 ** 2 / 2) ** 2))))
        # e^{W_1} - 1 = sum e^{W} dW + 1/2 sum e^{W} dt (Itô's lemma); without the second term (ordinary calculus)
        eW = np.exp(W[:, :-1])
        ito = (eW * dW).sum(1) + 0.5 * eW.sum(1) / n
        lemma_rms.append(float(np.sqrt(np.mean((np.exp(W1) - 1 - ito) ** 2))))
        naive_rms.append(float(np.sqrt(np.mean((np.exp(W1) - 1 - (eW * dW).sum(1)) ** 2))))
        if n == 1000:
            examples = dict(left_mean=float(left.mean()), strat_mean=float(strat.mean()), w2_mean=float((W1 ** 2).mean()),
                            path=W[0, ::10], ito_run=np.concatenate([[0], np.cumsum(W[0, :-1] * dW[0])])[::10])
    z = g.normal(size=400000)
    e_mean = float(np.exp(z).mean())
    slope = float(np.polyfit(np.log(ns), np.log(lemma_rms), 1)[0])
    assert abs(e_mean - math.exp(0.5)) < 0.02 and slope < -0.4
    return dict(ns=ns, M=M, left_err=np.array(left_err), strat_err=np.array(strat_err), lemma_rms=np.array(lemma_rms),
                naive_rms=np.array(naive_rms), e_mean=e_mean, e_half=math.exp(0.5), lemma_slope=slope, **examples)


def compute_em():
    """Euler-Maruyama on geometric Brownian motion dX = mu X dt + sigma X dW (mu = 2, sigma = 1, X0 = 1, T = 1),
    against the exact solution from the same Brownian increments, 20,000 paths, steps h = 2^-1 ... 2^-9: the strong
    error E|X_h - X| and the weak error |E[X_h - X]|, and their slopes."""
    g = rng(1955)  # Maruyama, 1955
    mu, sig, T, M = 2.0, 1.0, 1.0, 20000
    K = 9
    nf = 2 ** K
    dWf = g.normal(size=(M, nf)) * math.sqrt(T / nf)
    W1 = dWf.sum(1)
    exact = np.exp((mu - sig ** 2 / 2) * T + sig * W1)
    hs, strong, weak, weak_se = [], [], [], []
    for k in range(1, K + 1):
        n = 2 ** k
        h = T / n
        dW = dWf.reshape(M, n, -1).sum(2)
        X = np.ones(M)
        for j in range(n):
            X = X + mu * X * h + sig * X * dW[:, j]
        hs.append(h)
        strong.append(float(np.abs(X - exact).mean()))
        weak.append(float(abs((X - exact).mean())))
        weak_se.append(float((X - exact).std() / math.sqrt(M)))
    hs = np.array(hs)
    s_slope = float(np.polyfit(np.log(hs[2:]), np.log(strong[2:]), 1)[0])
    w_slope = float(np.polyfit(np.log(hs[2:]), np.log(weak[2:]), 1)[0])
    # one path at three step sizes, against the exact path
    n_show = [4, 16, 256]
    t_f = np.linspace(0, T, nf + 1)
    Wp = np.concatenate([[0], np.cumsum(dWf[0])])
    exact_path = np.exp((mu - sig ** 2 / 2) * t_f + sig * Wp)
    paths = {}
    for n in n_show:
        dW = dWf[0].reshape(n, -1).sum(1)
        X = [1.0]
        for j in range(n):
            X.append(X[-1] * (1 + mu * T / n + sig * dW[j]))
        paths[f"em{n}"] = np.array(X)
    return dict(mu=mu, sigma=sig, T=T, M=M, hs=hs, strong=np.array(strong), weak=np.array(weak),
                weak_se=np.array(weak_se), strong_slope=s_slope, weak_slope=w_slope, exact_path=exact_path[::4],
                n_show=n_show, **paths)


# ---------------------------------------------------------------------------
# Chapter 9: decoding the novels model, judged by GPT-2 (videos/ai/ai5/decoding.py; about 40 minutes, resumable)
# ---------------------------------------------------------------------------
def compute_decoding():
    import torch

    from videos.ai.ai5 import decoding

    torch.set_num_threads(2)
    return decoding.compute(CACHE)


ITEMS = {
    "galton": compute_galton,
    "clt": compute_clt,
    "mle": compute_mle,
    "bayes": compute_bayes,
    "temperature": compute_temperature,
    "markov": compute_markov,
    "montecarlo": compute_montecarlo,
    "mcmc": compute_mcmc,
    "brownian": compute_brownian,
    "diffusion": compute_diffusion,
    "shape": compute_shape,
    "lln": compute_lln,
    "conv": compute_conv,
    "gauss": compute_gauss,
    "mlebias": compute_mlebias,
    "fisher": compute_fisher,
    "map": compute_map,
    "maxent": compute_maxent,
    "tails": compute_tails,
    "draws": compute_draws,
    "mixing": compute_mixing,
    "ess": compute_ess,
    "scorefn": compute_scorefn,
    "langevin": compute_langevin,
    "qv": compute_qv,
    "ito": compute_ito,
    "em": compute_em,
    "decoding": compute_decoding,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

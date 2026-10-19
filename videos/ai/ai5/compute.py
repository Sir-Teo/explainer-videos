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
TEMPS = [0.5, 1.0, 2.0]


def compute_temperature():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_grad_enabled(False)
    tok = AutoTokenizer.from_pretrained("openai-community/gpt2")
    model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2", dtype=torch.float32)
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
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

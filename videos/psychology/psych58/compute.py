"""Precompute every number in Part 58 of *Psychology, Built* ("The Efficient, Predictive Brain").

    python -m videos.psychology.psych58.compute            # everything missing (a minute)

Results are cached in ``.cache/psych58/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.efficient``).

Items:
    images      six dead-leaves images (one kept for display), their patches' spectrum, the whitening filter
    sparse      Olshausen-Field sparse coding on whitened patches, with snapshots; localization against random and PCA
    laughlin    a contrast distribution and the histogram-matching response curve
    codes       twenty response levels, equal-width or matched to the distribution: bits per response
    bias        efficient-coding bias for orientation with a cardinal prior (repulsive)
    rd          rate-distortion generalization gradients at three costs of error
    norm        divisive normalization: contrast responses with and without a mask
    pc          a two-level predictive-coding network settling on expected and surprising inputs
    fe          the variational free energy of a Gaussian model over the approximate posterior's mean
    tilt        the tilt after-effect from adaptation in a population code
    samples     resource-rational sampling: accuracy and reward rate against the number of samples
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import efficient as E

CACHE = Cache("psych58")
load = CACHE.load


def _images():
    return [E.dead_leaves(seed=5800 + s) for s in range(6)]


def compute_images() -> dict:
    imgs = _images()
    X = E.patches(imgs, n=20000, seed=5801)
    Xw, W, ev = E.zca(X)
    centre = W[:, 8 * 4 + 4].reshape(8, 8)  # the whitening filter for a pixel near the middle
    return {"image": imgs[0], "spectrum": ev, "white_spectrum": np.linalg.eigvalsh(np.cov(Xw, rowvar=False))[::-1],
            "filter": centre}


def compute_sparse() -> dict:
    imgs = _images()
    X = E.patches(imgs, n=20000, seed=5801)
    Xw, _, _ = E.zca(X, eps=1.0)
    Xw = Xw / Xw.std()
    d = E.learn_dictionary(Xw, atoms=64, lam=0.4, epochs=400, seed=5802, snapshots=(0, 10, 50, 400))
    loc = E.localization(d["D"])
    rng = np.random.default_rng(5803)
    R = rng.standard_normal(d["D"].shape)
    R /= np.linalg.norm(R, axis=0)
    rloc = E.localization(R)
    C = np.cov(X, rowvar=False)
    _, V = np.linalg.eigh(C)
    pcs = V[:, ::-1][:, :64]
    ploc = E.localization(pcs)
    out = {"D": d["D"], "err": d["err"], "sparsity": d["sparsity"], "pcs": pcs,
           "loc": loc["localization"], "ori": loc["orientedness"], "rand_loc": rloc["localization"],
           "rand_ori": rloc["orientedness"], "pca_loc": ploc["localization"], "pca_ori": ploc["orientedness"]}
    for k, v in d["snapshots"].items():
        out[f"snap{k}"] = v
    return out


def _contrasts():
    imgs = _images()
    rng = np.random.default_rng(5804)
    c = []
    for im in imgs:
        for _ in range(1500):
            y, x = rng.integers(2, im.shape[0] - 3, 2)
            m = im[y - 2:y + 3, x - 2:x + 3].mean()
            c.append((im[y, x] - m) / max(m, 0.05))
    return np.clip(np.array(c), -1, 1)


def compute_laughlin() -> dict:
    return E.laughlin(_contrasts())


def compute_codes() -> dict:
    """Twenty response levels for local contrast: equal-width bins against bins at the quantiles (Laughlin's code).
    The entropy of the response (bits per response) and the share of levels the commonest contrasts get."""
    c = _contrasts()
    out = {}
    for name, edges in (("linear", np.linspace(-1, 1, 21)), ("matched", np.quantile(c, np.linspace(0, 1, 21)))):
        counts = np.histogram(c, bins=edges)[0] / len(c)
        p = counts[counts > 0]
        out[name + "_bits"] = float(-(p * np.log2(p)).sum())
        out[name + "_use"] = counts
        out[name + "_central"] = int(np.sum((edges[1:] > -0.1) & (edges[:-1] < 0.1)))
    out["max_bits"] = float(np.log2(20))
    return out


def compute_bias() -> dict:
    return E.efficient_bias("cardinal", noise=0.08)


def compute_rd() -> dict:
    return E.generalization(betas=(0.02, 0.1, 0.5))


def compute_norm() -> dict:
    c = np.logspace(-2, 0, 60)
    return {"c": c, "none": E.normalization(c), "mask_low": E.normalization(c, mask=0.2),
            "mask_high": E.normalization(c, mask=0.5)}


def compute_pc() -> dict:
    rng = np.random.default_rng(5805)
    D = rng.standard_normal((16, 4)) / 2
    prior = np.array([1.0, 0.5, -0.5, 0.0])
    x_exp = D @ prior + 0.05 * rng.standard_normal(16)
    x_sur = D @ np.array([-1.0, 1.0, 0.5, 1.0]) + 0.05 * rng.standard_normal(16)
    a = E.predictive_coding(D, x_exp, prior, steps=60, lr=0.1)
    b = E.predictive_coding(D, x_sur, prior, steps=60, lr=0.1)
    return {"exp_e0": a["e0"], "sur_e0": b["e0"], "exp_e1": a["e1"], "sur_e1": b["e1"]}


def compute_fe() -> dict:
    return E.free_energy_gaussian(x=2.0, prior_sd=1.0, noise_sd=0.5)


def compute_tilt() -> dict:
    return E.tilt_aftereffect(adapter=0.0)


def compute_samples() -> dict:
    return E.samples_value()


ITEMS = {"images": compute_images, "sparse": compute_sparse, "laughlin": compute_laughlin, "codes": compute_codes, "bias": compute_bias,
         "rd": compute_rd, "norm": compute_norm, "pc": compute_pc, "fe": compute_fe, "tilt": compute_tilt,
         "samples": compute_samples}

if __name__ == "__main__":
    CACHE.main(ITEMS)

"""Precompute every number in Part 14 of *Psychology, Built* ("Seeing as Inference").

    python -m videos.psychology.psych14.compute            # everything missing (about three minutes)
    python -m videos.psychology.psych14.compute --force cnn

Results are cached in ``.cache/psych14/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.infer``).  Simulated observers run thousands of trials a point, so the
numbers shown are close to the model's own and no single run is singled out.

Items:
    shadow      a checkerboard under a soft shadow: luminance, reflectance, illumination, two equal squares, and a
                retinex's reflectance estimate
    inverse     one retinal size from many object sizes at many distances
    depth       disparity against distance; a random-dot stereogram
    bayes       a prior, a likelihood and their posterior; shrinkage against the likelihood's width
    cues        visual and haptic height discrimination: single-cue thresholds, the predicted and observed combined
                threshold and the weights, at four levels of visual noise
    motion      perceived speed against contrast; MAP velocity for two edges against contrast
    light       shaded discs lit from above and from below
    templates   a square, the same square moved and turned, and a disc: distances between the images
    cnn         a small network trained on shapes with their own textures, and on shuffled textures: accuracy and
                the share of cue-conflict decisions that follow texture
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import infer as I

CACHE = Cache("psych14")
load = CACHE.load


def compute_shadow() -> dict:
    cs = I.checker_shadow()
    R = I.retinex(cs["luminance"])
    A, B = cs["A"], cs["B"]
    return {"lum": cs["luminance"], "refl": cs["reflectance"], "illum": cs["illumination"], "retinex": R,
            "A": list(A), "B": list(B), "lum_A": float(cs["luminance"][A]), "lum_B": float(cs["luminance"][B]),
            "ret_A": float(R[A]), "ret_B": float(R[B]), "refl_A": float(cs["reflectance"][A]),
            "refl_B": float(cs["reflectance"][B])}


def compute_inverse() -> dict:
    angle = 2.0  # degrees on the retina
    d = np.linspace(0.5, 10, 50)
    size = np.array([I.perceived_size(angle, x) for x in d])
    return {"angle": angle, "d": d, "size": size}


def compute_depth() -> dict:
    d = np.linspace(0.3, 10, 200)
    disp = np.array([I.disparity_arcmin(x, 0.01) for x in d])
    left, right = I.random_dot_stereogram(150, 56, 6, seed=1414)
    return {"d": d, "disp": disp, "left": left, "right": right, "at_half": I.disparity_arcmin(0.5, 0.01),
            "at_two": I.disparity_arcmin(2.0, 0.01), "at_ten": I.disparity_arcmin(10.0, 0.01)}


def compute_bayes() -> dict:
    x = np.linspace(-4, 8, 400)
    pm, ps, obs, ls = 0.0, 1.5, 4.0, 1.0
    post_m, post_s = I.posterior(pm, ps, obs, ls)
    g = lambda m, s: np.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))  # noqa: E731
    lsd = np.linspace(0.2, 4, 100)
    shrink = np.array([I.posterior(pm, ps, obs, s)[0] for s in lsd])
    return {"x": x, "prior": g(pm, ps), "like": g(obs, ls), "post": g(post_m, post_s), "prior_m": pm, "prior_s": ps,
            "obs": obs, "like_s": ls, "post_m": float(post_m), "post_s": post_s, "lsd": lsd, "shrink": shrink}


def compute_cues() -> dict:
    rng = np.random.default_rng(1402)
    d = np.linspace(-14, 14, 15)
    n = 2000
    sh = 4.0
    fh = I.fit_cumulative(d, I.two_interval(sh, d, n, rng), n)
    rows = []
    for sv in (1.5, 3.0, 4.5, 6.0):
        fv = I.fit_cumulative(d, I.two_interval(sv, d, n, rng), n)
        _, pred_sd, w = I.combine([0, 0], [fv["sd"], fh["sd"]])
        true_w = I.combine([0, 0], [sv, sh])[2]
        fc = I.fit_cumulative(d, I.two_interval(None, d, n, rng, weights=true_w, sds=(sv, sh)), n)
        conflict = 6.0
        fk = I.fit_cumulative(d, I.two_interval(None, d, n, rng, weights=true_w, sds=(sv, sh), conflict=conflict), n)
        w_obs = (fk["pse"] / conflict) + 0.5  # pse = conflict (wv - 1/2)
        rows.append({"sv": sv, "fit_v": fv["sd"], "pred_w": float(w[0]), "obs_w": float(w_obs), "pred_sd": pred_sd,
                     "obs_sd": fc["sd"]})
    # one psychometric picture: vision, touch, both, at the middle noise level
    sv = 3.0
    ex = {"d": d, "v": I.two_interval(sv, d, n, rng), "h": I.two_interval(sh, d, n, rng),
          "both": I.two_interval(None, d, n, rng, weights=I.combine([0, 0], [sv, sh])[2], sds=(sv, sh))}
    return {"rows": rows, "fit_h": fh["sd"], "sh": sh, "ex_d": ex["d"], "ex_v": ex["v"], "ex_h": ex["h"],
            "ex_both": ex["both"], "ex_sv": sv}


def compute_motion() -> dict:
    c = np.geomspace(0.02, 1.0, 100)
    sp = I.speed_estimate(1.0, c)
    cons = I.edge_constraints((1.0, 0.0), (20, 60))
    lsd = (0.02, 0.3, 1.0)
    vs = [I.map_velocity(cons, s) for s in lsd]
    return {"c": c, "speed": sp, "normals": [list(n) for n, _ in cons], "nspeeds": [s for _, s in cons],
            "lsd": list(lsd), "v": [list(v) for v in vs], "va": list(I.vector_average(cons)),
            "angles": [math.degrees(math.atan2(v[1], v[0])) for v in vs], "speeds": [float(np.linalg.norm(v)) for v in vs]}


def compute_light() -> dict:
    n = 64
    yy, xx = np.mgrid[:n, :n] - (n - 1) / 2
    r = np.sqrt(xx ** 2 + yy ** 2) / (n / 2 - 2)
    disc = r < 1
    shade = 0.5 - 0.4 * (yy / (n / 2)) * disc  # lighter at the top
    top = np.where(disc, shade, 0.5)
    return {"top": top, "bottom": top[::-1].copy()}


def compute_templates() -> dict:
    n = 40
    yy, xx = np.mgrid[:n, :n] + 0.5

    def square(cx, cy, half, turn=0.0):
        c, s = math.cos(turn), math.sin(turn)
        u, v = (xx - cx) * c + (yy - cy) * s, -(xx - cx) * s + (yy - cy) * c
        return ((np.abs(u) < half) & (np.abs(v) < half)).astype(float)

    base = square(20, 20, 8)
    moved = square(29, 24, 8)
    turned = square(20, 20, 8, math.pi / 4)
    disc = (((xx - 20) ** 2 + (yy - 20) ** 2) < 9.0 ** 2).astype(float)
    imgs = {"square": base, "moved": moved, "turned": turned, "disc": disc}
    dist = {k: float(np.sqrt(((v - base) ** 2).sum())) for k, v in imgs.items() if k != "square"}
    return {**imgs, "dist_moved": dist["moved"], "dist_turned": dist["turned"], "dist_disc": dist["disc"]}


def compute_cnn() -> dict:
    X, y, t = I.shape_texture_images(600, mode="paired", seed=1)
    Xt, yt, _ = I.shape_texture_images(300, mode="paired", seed=2)
    net = I.TinyConvNet(seed=0)
    loss_a = net.fit(X, y, steps=400, lr=0.1)
    X2, y2, _ = I.shape_texture_images(600, mode="shuffled", seed=3)
    Xs, ys, _ = I.shape_texture_images(300, mode="shuffled", seed=4)
    net2 = I.TinyConvNet(seed=0)
    loss_b = net2.fit(X2, y2, steps=400, lr=0.1)
    Xc, yc, tc = I.shape_texture_images(6, mode="conflict", seed=5)
    return {"loss_paired": np.array(loss_a), "loss_shuffled": np.array(loss_b),
            "acc_paired": float((net.predict(Xt) == yt).mean()), "acc_shuffled": float((net2.predict(Xs) == ys).mean()),
            "bias_paired": I.texture_bias(net), "bias_shuffled": I.texture_bias(net2),
            "examples": X[:6], "example_labels": y[:6], "conflict": Xc, "conflict_shape": yc, "conflict_texture": tc,
            "conflict_pred": net.predict(Xc)}


ITEMS = {
    "shadow": compute_shadow,
    "inverse": compute_inverse,
    "depth": compute_depth,
    "bayes": compute_bayes,
    "cues": compute_cues,
    "motion": compute_motion,
    "light": compute_light,
    "templates": compute_templates,
    "cnn": compute_cnn,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)

"""Lab 22: add up light along a ray two ways, and project a 3D Gaussian onto a screen."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor

TITLE = "Light through a volume, and a Gaussian on a screen"
GOAL = ("Render a ray through a uniform ball, whose colour is known exactly, by a Riemann sum and by NeRF's "
        "alpha-compositing sum; then project a 3D Gaussian through a pinhole camera and compare the covariance "
        "J W S W' J' (J from the series' autodiff) with the covariance of 200,000 exactly projected draws.")
TASKS = [
    "Raise the ball's density from 2 to 20. Which of the two sums still returns a colour between 0 and 1?",
    "Put a second, blue ball behind the first and check that the weights T_i alpha_i split the pixel between them and the background.",
    "Move the Gaussian off the optical axis (mu = (1, 0.5, 4)) and see which entries of J become non-zero and how the splat tilts.",
]


def render(t_edges, density, kind):
    """A white medium's colour along a ray sampled on segments [t_i, t_i+1], density read at each midpoint."""
    delta = np.diff(t_edges)
    sig = density(0.5 * (t_edges[:-1] + t_edges[1:]))
    if kind == "nerf":
        alpha = 1 - np.exp(-sig * delta)
        T = np.concatenate([[1.0], np.cumprod(1 - alpha)])
    else:  # the Riemann sum of T sigma c dt
        alpha = sig * delta
        T = np.exp(-np.concatenate([[0.0], np.cumsum(sig * delta)]))
    w = T[:-1] * alpha
    return w.sum(), w, T


def jacobian(t, f):
    """The 2 x 3 Jacobian of (u, v) = (f t_x / t_z, f t_y / t_z), one backward pass per row."""
    rows = []
    for axis in (0, 1):
        tt = Tensor(t, requires_grad=True)
        (tt[axis] * f / tt[2]).backward()
        rows.append(tt.grad.copy())
    return np.array(rows)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. a ray through the centre of a ball of radius 1 and density 2, entering at t = 1 and leaving at t = 3
    dens, near, far = 2.0, 0.0, 4.0
    density = lambda t: dens * ((t > 1.0) & (t < 3.0))
    exact = 1 - np.exp(-dens * 2.0)
    Ns = [8, 16, 32, 64, 128, 256]
    err = {"riemann": [], "nerf": []}
    for N in Ns:
        for kind in err:
            e = []
            for _ in range(200):  # NeRF's stratified sampling: one random cut in each of N equal bins
                cuts = near + (far - near) * (np.arange(N) + rng.random(N)) / N
                edges = np.concatenate([[near], cuts, [far]])
                C, w, T = render(edges, density, kind)
                e.append(abs(C - exact))
                if kind == "nerf":
                    assert abs(w.sum() - (1 - T[-1])) < 1e-12, "the weights sum to 1 - T_(N+1)"
            err[kind].append(np.mean(e))
    for kind in err:
        lab.row(f"{kind} sum: mean |error| at N = 8, 32, 128", "  ".join(f"{err[kind][i]:.4f}" for i in (0, 2, 4)) +
                (f"   (exact colour {exact:.4f})" if kind == "nerf" else ""))
    assert all(a < b for a, b in zip(err["nerf"], err["riemann"])), "alpha compositing beats the Riemann sum"
    assert err["nerf"][-1] < 0.25 * err["nerf"][2] and err["nerf"][-1] < 0.005, "and converges"
    C, w, _ = render(np.linspace(near, far, 5), lambda t: 10 * density(t), "riemann")
    lab.row("Riemann sum, density 20, 4 segments", f"colour {C:.2f}: brighter than white")
    assert C > 1 and render(np.linspace(near, far, 5), lambda t: 10 * density(t), "nerf")[0] <= 1

    # 2. a Gaussian with covariance R S S' R' seen by a camera at the origin looking along z
    f, depth = 1.0, 4.0
    c, sn = np.cos(np.radians(55)), np.sin(np.radians(55))
    q = np.array([[c, 0, -sn], [0, 1, 0], [sn, 0, c]])  # the long axis leans 55 degrees into the depth
    shape = np.array([1.0, 0.6, 0.3])
    mu = np.array([0.4, -0.3, depth])
    J = jacobian(mu, f)
    J_formula = np.array([[f / mu[2], 0, -f * mu[0] / mu[2] ** 2], [0, f / mu[2], -f * mu[1] / mu[2] ** 2]])
    assert np.abs(J - J_formula).max() < 1e-12, "autodiff's Jacobian is the derived one"
    sizes = [0.02, 0.05, 0.1, 0.15]
    disc, keep = [], None
    for s in sizes:
        Sigma = q @ np.diag((s * depth * shape) ** 2) @ q.T
        pts = rng.multivariate_normal(mu, Sigma, 200_000)
        uv = f * pts[:, :2] / pts[:, 2:3]  # the exact projection of every draw
        sample, lin = np.cov(uv.T), J @ Sigma @ J.T
        disc.append(np.linalg.norm(sample - lin) / np.linalg.norm(sample))
        if s == 0.1:
            keep = (uv[:1500], lin)
    lab.row("autodiff J against the formula", f"largest difference {np.abs(J - J_formula).max():.1e}")
    lab.row("covariance discrepancy at size/depth " + ", ".join(str(s) for s in sizes), "  ".join(f"{d:.3f}" for d in disc))
    lab.note = ("NeRF's sum is exact on every segment of constant density, so its only error is at the ball's edge; "
                "the splat's covariance is a linearization, right for small Gaussians and worse as they grow "
                "against their depth.")
    assert disc[0] < 0.02, "small Gaussians: the linearization matches the exact projection"
    assert disc[-1] > 3 * disc[0] and disc[-1] > disc[1], "larger Gaussians: it drifts"

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].loglog(Ns, err["riemann"], "o-", color=labs.RED, label="Riemann sum of T sigma c dt")
    ax[0].loglog(Ns, err["nerf"], "o-", color=labs.GREEN, label="NeRF: sum of T_i alpha_i c_i")
    ax[0].set(title="A ray through a uniform ball: error of the colour", xlabel="samples along the ray", ylabel="mean |error|")
    ax[0].legend()
    uv, lin = keep
    centre = f * mu[:2] / mu[2]
    ax[1].scatter(uv[:, 0], uv[:, 1], s=3, color=labs.BLUE, alpha=0.35, label="exactly projected draws")
    vals, vecs = np.linalg.eigh(lin)
    ang = np.linspace(0, 2 * np.pi, 200)
    for k, ls in ((1, "-"), (2, "--")):
        ell = centre[:, None] + vecs @ (k * np.sqrt(vals)[:, None] * np.array([np.cos(ang), np.sin(ang)]))
        ax[1].plot(ell[0], ell[1], color=labs.GOLD, ls=ls, label=f"J W S W' J': {k} sd")
    ax[1].set(title="A Gaussian of size/depth 0.1 on the screen", xlabel="u", ylabel="v", aspect="equal")
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab

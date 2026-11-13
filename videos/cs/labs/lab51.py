"""Lab 51: watch Monte Carlo noise fall as 1/sqrt(N), test Russian roulette for bias, and put four BRDFs in a white furnace."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np

from explainer.cs.graphics import brdf, curves, transform

TITLE = "Samples of light: noise, roulette and the white furnace"
GOAL = ("Estimate the light falling on a surface from a bright-overhead sky with the series' uniform and "
        "cosine-weighted samplers and fit how the error falls with the sample count, end paths in a room of albedo "
        "0.73 by Russian roulette and by a hard cut-off, and check which shading models conserve energy.")
TASKS = [
    "Change the sky from 1 + 3 cos^4 to a constant 1. What happens to the cosine-weighted estimator's error, and why is f cos / p then the same for every sample?",
    "Play roulette with survival probability 0.5 instead of 0.73. The mean is still right in theory: compute the second moment of the throughput, (rho^2 / q)^k, and explain what you see.",
    "Call transform.resolvable(1000, near, 1000) for near = 0.01, 0.1 and 1. How large a gap can a 24-bit depth buffer resolve at distance 1000, and what does moving the near plane buy?",
]

RHO = 0.73
EXACT = 2 * np.pi  # the integral of (1 + 3 cos^4) cos over the hemisphere


def sky(w):
    return 1 + 3 * w[..., 2] ** 4


def estimates(sampler, n, trials, rng):
    w, pdf = sampler(rng.random((trials, n)), rng.random((trials, n)))
    return (sky(w) * w[..., 2] / pdf).mean(axis=1)


def room(q, paths, rng, cut=None):
    """Light reaching the eye in a closed room of albedo RHO whose walls all emit 1: 1 + rho + rho^2 + ...
    Roulette survives each bounce with probability q and divides by q; a cut-off simply stops after `cut` bounces."""
    total, beta, alive, rays = np.ones(paths), np.ones(paths), np.ones(paths, bool), 0
    for bounce in range(1, 400):
        if cut is not None:
            if bounce > cut:
                break
            beta = beta * RHO
        else:
            alive &= rng.random(paths) < q
            beta = np.where(alive, beta * RHO / q, 0.0)
        if not alive.any():
            break
        rays += int(alive.sum())
        total += np.where(alive, beta, 0.0)
    return total.mean(), total.std() / np.sqrt(paths), rays / paths


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the error of a Monte Carlo estimate falls as 1 / sqrt(N); importance sampling lowers the whole line
    ns, trials = (16, 64, 256, 1024, 4096), 400
    rms = {}
    for name, sampler in (("uniform", brdf.sample_uniform_hemisphere), ("cosine", brdf.sample_cosine_hemisphere)):
        rms[name] = [float(np.sqrt(np.mean((estimates(sampler, n, trials, rng) - EXACT) ** 2))) / EXACT for n in ns]
        slope = float(np.polyfit(np.log(ns), np.log(rms[name]), 1)[0])
        assert abs(slope + 0.5) < 0.08, "the error falls as N^(-1/2)"
        lab.row(f"{name} sampling: relative error at 16, 256, 4096 samples",
                f"{rms[name][0]:.3f}, {rms[name][2]:.4f}, {rms[name][4]:.4f}   fitted slope {slope:.2f} (theory -0.50)")
    gain = (rms["uniform"][2] / rms["cosine"][2]) ** 2
    assert gain > 1.5, "sampling in proportion to the cosine lowers the variance"
    lab.row("variance, uniform over cosine-weighted", f"{gain:.1f} times")

    # 2. Russian roulette is unbiased; cutting paths off is not
    exact = 1 / (1 - RHO)
    m_r, se_r, rays_r = room(RHO, 200_000, rng)
    m_9, se_9, rays_9 = room(0.9, 200_000, rng)
    m_c, _, rays_c = room(None, 1, rng, cut=5)
    assert abs(m_r - exact) < 4 * se_r and abs(m_9 - exact) < 4 * se_9, "roulette keeps the mean"
    assert abs(m_c - (1 - RHO ** 6) / (1 - RHO)) < 1e-9 and m_c < exact - 0.5, "a cut-off loses the later bounces"
    lab.row("room of albedo 0.73: exact 1/(1 - 0.73)", f"{exact:.3f}")
    lab.row("roulette, survive with q = 0.73", f"{m_r:.3f} ± {se_r:.3f}   {rays_r:.2f} rays a path")
    lab.row("roulette, survive with q = 0.90", f"{m_9:.3f} ± {se_9:.3f}   {rays_9:.2f} rays a path")
    lab.row("cut off after 5 bounces", f"{m_c:.3f} (biased low)   {rays_c:.0f} rays a path")

    # 3. the white furnace: light returned by a surface lit equally from everywhere
    head_on = brdf.direction(0.0)
    furnace = {}
    for model, param in (("lambert", 1.0), ("phong", 10), ("blinn_phong", 10), ("ggx", 1.0)):
        quad = brdf.albedo_quadrature(model, param, head_on, theta_panels=64, n_phi=256)
        mc, se = brdf.albedo_mc(model, param, head_on, samples=100_000, seed=seed)
        assert abs(mc - quad) < 4 * se + 2e-3, model
        furnace[model] = quad
    assert abs(furnace["lambert"] - 1) < 1e-3 and abs(furnace["phong"] - 1) < 5e-3
    assert furnace["blinn_phong"] > 1.05 and furnace["ggx"] < 0.4, "one model creates energy, one loses it"
    lab.row("white furnace, seen head-on", "  ".join(f"{k} {v:.3f}" for k, v in furnace.items()))

    # 4. two exact checks: de Casteljau against Bernstein's polynomials, slerp's constant step
    pts = np.array([(0, 0), (1, 2), (3, 2.2), (4, 0.2)], float)
    t = float(rng.uniform(0.05, 0.95))
    bern = (1 - t) ** 3 * pts[0] + 3 * t * (1 - t) ** 2 * pts[1] + 3 * t * t * (1 - t) * pts[2] + t ** 3 * pts[3]
    assert np.allclose(curves.de_casteljau(pts, t)["point"], bern, atol=1e-12)
    sl = transform.slerp_vs_euler()
    steps = sl["slerp"]["per_step_deg"]
    assert max(steps) - min(steps) < 1e-6 and abs(sl["slerp"]["total_deg"] - sl["geodesic_deg"]) < 1e-6
    assert sl["euler"]["total_deg"] > sl["geodesic_deg"] + 50
    lab.row("turning between two orientations", f"slerp {sl['slerp']['total_deg']:.1f} degrees in equal steps of "
            f"{steps[0]:.2f}; Euler angles {sl['euler']['total_deg']:.1f}, unevenly")
    lab.note = ("Every estimator's error falls on a line of slope -1/2 and good sampling only lowers the line; "
                "roulette shortens paths without bias where a cut-off darkens the picture; and a shading model can "
                "create or lose energy without anyone noticing until it is put in a furnace.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    ax[0].loglog(ns, rms["uniform"], "o-", color=labs.ORANGE, label="uniform over the hemisphere")
    ax[0].loglog(ns, rms["cosine"], "o-", color=labs.BLUE, label="cosine-weighted")
    ax[0].loglog(ns, rms["uniform"][0] * np.sqrt(ns[0] / np.array(ns)), color=labs.MUTED, ls="--", label="1 / sqrt(N)")
    ax[0].set(title="Error of the estimated irradiance", xlabel="samples N", ylabel="relative RMS error, 400 trials")
    ax[0].legend()
    angles = np.array([0, 15, 30, 45, 60, 70, 80, 85])
    for (model, param, label), color in zip((("lambert", 1.0, "Lambert"), ("phong", 10, "Phong, n = 10 (normalized)"),
                                             ("blinn_phong", 10, "Blinn-Phong, n = 10"), ("ggx", 1.0, "GGX, alpha = 1")),
                                            (labs.GREEN, labs.BLUE, labs.RED, labs.PURPLE)):
        ax[1].plot(angles, [brdf.albedo_quadrature(model, param, brdf.direction(float(a)), theta_panels=48, n_phi=192)
                            for a in angles], "o-", color=color, label=label)
    ax[1].axhline(1, color=labs.MUTED, ls="--", lw=1)
    ax[1].set(title="White furnace: share of the light returned", xlabel="viewing angle from the normal (degrees)",
              ylabel="directional albedo", ylim=(0, 1.3))
    ax[1].legend(fontsize=8, loc="lower left")
    lab.fig = fig
    return lab

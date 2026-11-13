"""Lab 27: run Gibbs, random-walk Metropolis and HMC on one correlated normal, and count effective draws."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import ppl

TITLE = "Three samplers, one correlated normal"
GOAL = ("Sample a bivariate normal with correlation 0.95 by Gibbs, by random-walk Metropolis and by Hamiltonian Monte "
        "Carlo (statkit.ppl on autodiff), check Gibbs's effective sample size against (1 - rho^2)/(1 + rho^2), and "
        "check that leapfrog keeps the spring's energy while Euler's grows like (1 + eps^2)^steps.")
TASKS = [
    "Set RHO = 0.99. Gibbs's ESS per sweep should fall to about 0.01: does HMC, with EPS and L retuned, suffer as much?",
    "Sweep the random walk's scale over 0.05, 0.3 and 3 and record acceptance and ESS. Where is the ESS highest?",
    "Replace the target by Neal's funnel (v ~ N(0, 9), x ~ N(0, e^v)) and run ppl.sample on it centred and "
    "non-centred. Compare the 5% point of v with -4.93.",
]

RHO, EPS, L = 0.95, 0.18, 12


def gibbs(n, rng):
    x, s, out = np.zeros(2), np.sqrt(1 - RHO ** 2), np.empty((n, 2))
    for i in range(n):
        x[0] = RHO * x[1] + s * rng.standard_normal()
        x[1] = RHO * x[0] + s * rng.standard_normal()
        out[i] = x
    return out


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. The integrator.  A unit spring is a standard normal target: H = q^2/2 + p^2/2 = 0.5 at (1, 0).
    spring = ppl.Model({"q": (1, "real")}, lambda p: (p["q"] * p["q"] * -0.5).sum())
    eps, steps = 0.3, 60
    q, p = np.array([1.0]), np.array([0.0])
    lp, g = spring.logp_grad(q)
    leap = [0.5]
    for _ in range(steps):
        q, p, lp, g = ppl.leapfrog(spring, q, p, g, eps, np.ones(1))
        leap.append(float(-lp + 0.5 * p @ p))
    qe, pe, euler = 1.0, 0.0, [0.5]
    for _ in range(steps):
        qe, pe = qe + eps * pe, pe - eps * qe
        euler.append(0.5 * (qe * qe + pe * pe))
    leap, euler = np.array(leap), np.array(euler)
    lab.row("spring, 60 steps of 0.3: Euler's energy", f"0.5 -> {euler[-1]:.1f}   (theory 0.5 (1 + eps^2)^60 = {0.5 * 1.09 ** 60:.1f})")
    lab.row("spring: leapfrog's largest energy error", f"{np.abs(leap - 0.5).max():.4f}   (bound eps^2/8 = {eps ** 2 / 8:.4f})")
    assert abs(euler[-1] - 0.5 * (1 + eps ** 2) ** steps) < 1e-6 and 87 < euler[-1] < 89
    assert np.abs(leap - 0.5).max() <= eps ** 2 / 8 + 1e-9, "leapfrog's energy error stays bounded"

    # 2. Three samplers on the same target.
    n_g = 20000
    G = gibbs(n_g, rng).reshape(4, n_g // 4, 2)
    log_density = lambda x: -0.5 * (x[0] ** 2 - 2 * RHO * x[0] * x[1] + x[1] ** 2) / (1 - RHO ** 2)
    n_r = 20000
    rw = ppl.rwm(log_density, np.zeros(2), 0.5, n_r, rng)
    R = rw["draws"].reshape(4, n_r // 4, 2)
    target = ppl.Model({"a": (1, "real"), "b": (1, "real")},
                       lambda p: ppl.normal_lpdf(p["a"], 0.0, 1.0) + ppl.normal_lpdf(p["b"], p["a"] * RHO, np.sqrt(1 - RHO ** 2)))
    n_h = 800
    hm = ppl.hmc(target, np.zeros(2), EPS, L, n_h, rng, record=True)
    H = hm["draws"].reshape(4, n_h // 4, 2)

    theory = (1 - RHO ** 2) / (1 + RHO ** 2)
    res = {}
    for name, D, cost in (("Gibbs", G, 1), ("random walk", R, 1), ("HMC", H, L)):
        flat = D.reshape(-1, 2)
        e = ppl.ess_basic(D[..., 0])
        res[name] = dict(ess=e / len(flat), sd=flat[:, 0].std(), corr=np.corrcoef(flat.T)[0, 1], rhat=ppl.rhat(D[..., 0]))
        r = res[name]
        lab.row(f"{name}: sd of x1, correlation", f"{r['sd']:.2f}, {r['corr']:.3f}   (truth 1, {RHO})")
        lab.row(f"{name}: ESS per iteration", f"{r['ess']:.3f}" + (f"   (theory {theory:.3f})" if name == "Gibbs" else "")
                + (f"   ({r['ess'] / cost:.3f} per gradient)" if name == "HMC" else ""))
    lab.row("acceptance: random walk, HMC", f"{rw['accept'].mean():.0%}, {hm['accept'].mean():.0%}")
    lab.note = ("All three chains have the right stationary law, but each Gibbs sweep or random-walk step is worth a "
                "few hundredths of an independent draw, while one HMC trajectory is worth most of one.")
    for name, r in res.items():
        tol = 0.12 if name == "Gibbs" else 0.2
        assert abs(r["sd"] - 1) < tol and abs(r["corr"] - RHO) < 0.03, f"{name} samples the target"
    assert abs(res["Gibbs"]["ess"] / theory - 1) < 0.3, "Gibbs's x1 is an AR(1) with coefficient rho^2"
    assert res["HMC"]["ess"] > 5 * res["Gibbs"]["ess"] and res["HMC"]["ess"] > 5 * res["random walk"]["ess"]
    assert hm["accept"].mean() > 0.9

    fig, ax = labs.figure(2, size=(11, 4.2))
    t = np.linspace(0, 2 * np.pi, 200)
    for r in (1, 2):
        ex = r * np.cos(t)
        ey = r * (RHO * np.cos(t) + np.sqrt(1 - RHO ** 2) * np.sin(t))
        ax[0].plot(ex, ey, color=labs.GRID, lw=1)
    gz = G.reshape(-1, 2)[:25]
    stairs = np.column_stack([np.repeat(gz[:, 0], 2)[1:], np.repeat(gz[:, 1], 2)[:-1]])
    ax[0].plot(stairs[:, 0], stairs[:, 1], color=labs.RED, lw=1, label="Gibbs: 25 sweeps")
    for k, path in enumerate(hm["paths"][:6]):
        ax[0].plot(path[:, 0], path[:, 1], color=labs.GOLD, lw=1.4, label="HMC: 6 trajectories" if k == 0 else None)
        ax[0].plot(path[-1, 0], path[-1, 1], "o", color=labs.GOLD, ms=4)
    ax[0].set(title="The same target, two ways to move", xlabel="x1", ylabel="x2", xlim=(-3, 3), ylim=(-3, 3))
    ax[0].legend(loc="upper left")
    lags = np.arange(41)

    def acf(D):
        x = D[..., 0] - D[..., 0].mean()
        return np.array([1.0] + [np.mean(x[:, :-k] * x[:, k:]) / np.mean(x * x) for k in lags[1:]])

    ax[1].plot(lags, acf(G), color=labs.RED, label="Gibbs")
    ax[1].plot(lags, RHO ** (2 * lags), color=labs.MUTED, ls="--", label="theory: rho^(2 lag)")
    ax[1].plot(lags, acf(R), color=labs.BLUE, label="random walk")
    ax[1].plot(lags, acf(H), color=labs.GOLD, label="HMC")
    ax[1].axhline(0, color=labs.GRID, lw=1)
    ax[1].set(title="Autocorrelation of x1", xlabel="lag (iterations)", ylabel="autocorrelation")
    ax[1].legend()
    lab.fig = fig
    return lab

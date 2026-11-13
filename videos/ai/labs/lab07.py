"""Lab 7: run EM on a two-bell mixture and draw the lower bound each E step builds under the log-likelihood."""

import numpy as np

from videos.coursekit import labs

TITLE = "EM never goes downhill: the bound under the likelihood"
GOAL = ("Fit a mixture of two Gaussians to unlabelled points by EM, and check the chapter's proof in numbers: the "
        "bound touches the log-likelihood where the E step was taken, lies below it everywhere else, and the gap is a KL divergence.")
TASKS = [
    "Move the two sources closer (means -0.6 and 0.6). How many rounds does EM need now, and how well does it recover the labels?",
    "Make the E step hard: give each point wholly to its likelier bell (k-means with variances). Does the log-likelihood still never fall?",
    "Start both bells at the same mean. Explain from the M step's formulas why EM cannot leave that start.",
]


def log_joint(x, theta):
    """log p(x_i, z = k; theta) for both bells: an (n, 2) array.  theta = (pi_1, mu_1, mu_2, sd_1, sd_2)."""
    pi, mu, sd = np.array([theta[0], 1 - theta[0]]), np.array(theta[1:3]), np.array(theta[3:5])
    return np.log(pi) - 0.5 * np.log(2 * np.pi * sd ** 2) - 0.5 * ((x[:, None] - mu) / sd) ** 2


def log_lik(x, theta):
    return np.logaddexp(*log_joint(x, theta).T).sum()


def e_step(x, theta):
    lj = log_joint(x, theta)
    return np.exp(lj - np.logaddexp(*lj.T)[:, None])


def m_step(x, q):
    nk = q.sum(0)
    mu = (q * x[:, None]).sum(0) / nk
    sd = np.sqrt((q * (x[:, None] - mu) ** 2).sum(0) / nk)
    return np.array([nk[0] / len(x), mu[0], mu[1], sd[0], sd[1]])


def bound(x, q, theta):
    """Jensen's lower bound B(q, theta) = sum_i sum_k q_ik log(p(x_i, k; theta) / q_ik)."""
    return (q * (log_joint(x, theta) - np.log(np.maximum(q, 1e-300)))).sum()


def run(seed=0):
    rng = np.random.default_rng(seed)
    n = 400
    z = rng.random(n) < 0.4
    x = np.where(z, rng.normal(-1.6, 0.7, n), rng.normal(1.4, 1.0, n))
    theta = np.array([0.5, -0.3, 0.4, 1.5, 1.5])  # a poor start: two wide bells side by side
    thetas, lls, worst_touch, worst_above, worst_kl = [theta], [log_lik(x, theta)], 0.0, -np.inf, 0.0
    curves = []
    for k in range(40):
        q = e_step(x, theta)
        new = m_step(x, q)
        ts = np.linspace(0, 1.25, 51)
        line = [theta + t * (new - theta) for t in ts]
        ll_line = np.array([log_lik(x, th) for th in line])
        b_line = np.array([bound(x, q, th) for th in line])
        worst_touch = max(worst_touch, abs(ll_line[0] - b_line[0]))  # the bound touches at the E step's parameters
        worst_above = max(worst_above, (b_line - ll_line).max())  # ... and is never above the likelihood
        post = e_step(x, new)  # the gap at the new parameters is KL(q || posterior there)
        kl = (q * (np.log(np.maximum(q, 1e-300)) - np.log(np.maximum(post, 1e-300)))).sum()
        worst_kl = max(worst_kl, abs((log_lik(x, new) - bound(x, q, new)) - kl))
        if k in (0, 1, 4):
            curves.append((k, ts, ll_line, b_line))
        theta = new
        thetas.append(theta)
        lls.append(log_lik(x, theta))
    lls = np.array(lls)
    agree = np.mean((e_step(x, theta)[:, 0] > 0.5) == z)
    agree = max(agree, 1 - agree)

    lab = labs.Lab()
    lab.row("log-likelihood per point: start, round 1, round 40", f"{lls[0] / n:.4f}   {lls[1] / n:.4f}   {lls[-1] / n:.4f}")
    lab.row("smallest change in one round", f"{np.diff(lls).min():.2e}   (never negative)")
    lab.row("bound minus likelihood where the E step was taken", f"{worst_touch:.1e}   (they touch)")
    lab.row("largest (bound - likelihood) along any step", f"{worst_above:.1e}   (the bound stays below)")
    lab.row("gap at the new parameters minus KL(q || posterior)", f"{worst_kl:.1e}")
    lab.row("fitted means and sds", f"{theta[1]:.2f}, {theta[2]:.2f};  {theta[3]:.2f}, {theta[4]:.2f}   (truth -1.6, 1.4; 0.7, 1.0)")
    lab.row("points given to their true source", f"{agree:.1%}, with no labels")
    lab.note = ("Each E step builds a curve that touches the log-likelihood from below; the M step climbs to that "
                "curve's top, so the likelihood above it can only have risen.")

    assert np.all(np.diff(lls) > -1e-9), "the log-likelihood never falls"
    assert worst_touch < 1e-8 and worst_above < 1e-8, "a lower bound, tight at the current parameters"
    assert worst_kl < 1e-7, "the gap is the KL divergence from q to the posterior"
    assert agree > 0.9 and abs(theta[1] + 1.6) < 0.3 and abs(theta[2] - 1.4) < 0.3, "the sources are recovered"

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.linspace(x.min() - 0.5, x.max() + 0.5, 300)
    ax[0].hist(x, bins=40, density=True, color=labs.GREY, alpha=0.45, label="400 unlabelled points")
    for th, color, name in ((thetas[0], labs.RED, "the start"), (thetas[-1], labs.GOLD, "after 40 rounds")):
        ax[0].plot(grid, np.exp(log_joint(grid, th)).sum(1), color=color, label=name)
    ax[0].set(title="The mixture before and after EM", xlabel="x", ylabel="density")
    ax[0].legend()
    for (k, ts, ll_line, b_line), color in zip(curves, (labs.BLUE, labs.PURPLE, labs.TEAL)):
        rise = ll_line[40] - ll_line[0]  # ts[40] = 1: each round is drawn in units of its own gain
        ax[1].plot(ts, (ll_line - ll_line[0]) / rise, color=color, label=f"round {k + 1}: log-likelihood")
        ax[1].plot(ts, (b_line - ll_line[0]) / rise, color=color, ls="--", label=f"round {k + 1}: the E step's bound")
    ax[1].axvline(1, color=labs.MUTED, lw=0.8, ls=":")
    ax[1].set(title="Along each step: the bound touches at 0, peaks at 1", xlabel="from this round's parameters (0) to the next round's (1)",
              ylabel="rise, as a share of the round's gain", ylim=(-0.75, 1.3))
    ax[1].legend(ncol=1, loc="lower right")
    lab.fig = fig
    return lab

"""Lab 31: put error bars on a benchmark gap, fit an arena's ratings, and play the control game against its formula."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor

TITLE = "Measuring honestly, and the arithmetic of control"
GOAL = ("Simulate a 500-question benchmark for two models two points apart and compare the unpaired and paired standard "
        "errors of their gap with its true spread; fit Bradley-Terry ratings to simulated votes with the series' autodiff "
        "and check the fixed point; then play chapter 10's control game and compare with its closed form.")
TASKS = [
    "Lower the item correlation (shared = 0.2). How much of pairing's advantage is left, and why?",
    "Give the arena 300 votes instead of 6,000 and refit. How far do the ratings move, in Elo points (400 / ln 10 per unit)?",
    "Raise the monitor's separation mu from 2 to 3. What are q and the blue team's safety under trusted monitoring now?",
]


def red_wins(p, q, s, n):
    """Trusted monitoring: each round red attacks with probability p; an attack is caught with probability q (blue
    wins), otherwise it works with probability s (red wins).  P(red wins within n rounds)."""
    c, w = p * q, p * (1 - q) * s
    return w / (c + w) * (1 - (1 - c - w) ** n)


def red_wins_upfront(p, s, n, audited):
    """Upfront auditing: the first ``audited`` problems are all checked, none after."""
    return (1 - p) ** audited * (1 - (1 - p * s) ** (n - audited))


def run(seed=0):
    rng = np.random.default_rng(seed)

    # 1. one benchmark, two models: items share a difficulty, so the models' right answers are correlated
    n, reps, acc, shared = 500, 3000, (0.70, 0.68), 0.8
    hard = rng.standard_normal((reps, n, 1))
    own = rng.standard_normal((reps, n, 2))
    latent = np.sqrt(shared) * hard + np.sqrt(1 - shared) * own
    right = latent < stats.norm.ppf(acc)  # [replication, item, model]
    score = right.mean(1)
    gap = score[:, 0] - score[:, 1]
    se_one = np.sqrt(acc[0] * (1 - acc[0]) / n)
    se_unpaired = np.sqrt((score * (1 - score) / n).sum(1)).mean()  # as if the two scores were independent
    diff = right[:, :, 0].astype(float) - right[:, :, 1]
    se_paired = (diff.std(1, ddof=1) / np.sqrt(n)).mean()
    rho = np.mean([np.corrcoef(right[k, :, 0], right[k, :, 1])[0, 1] for k in range(200)])
    worse_ge = (gap <= 0).mean()

    # 2. an arena: Bradley-Terry ratings by gradient ascent on the log-likelihood
    M, votes = 6, 6000
    theta_true = np.linspace(-1, 1, M)
    i = rng.integers(M, size=votes)
    j = (i + rng.integers(1, M, size=votes)) % M
    i_won = rng.random(votes) < 1 / (1 + np.exp(-(theta_true[i] - theta_true[j])))
    winner, loser = np.where(i_won, i, j), np.where(i_won, j, i)
    theta = Tensor(np.zeros(M), requires_grad=True)
    for _ in range(400):
        theta.grad = np.zeros(M)
        d = theta[winner] - theta[loser]
        ((-d).exp() + 1.0).log().mean().backward()  # -log sigma(theta_w - theta_l), averaged over the votes
        theta.data -= 4.0 * theta.grad
    fitted = theta.data - theta.data.mean()
    wins = np.bincount(winner, minlength=M)
    expected = np.zeros(M)
    p_ij = 1 / (1 + np.exp(-(fitted[i] - fitted[j])))
    np.add.at(expected, i, p_ij)
    np.add.at(expected, j, 1 - p_ij)
    fixed_point = np.abs(expected - wins).max()

    # 3. the control game: suspicion of honest code ~ N(0, 1), of backdoored code ~ N(mu, 1), the top 2% audited
    mu, s, audit, N = 2.0, 0.3, 0.02, 5000
    q = stats.norm.sf(stats.norm.isf(audit) - mu)
    ps = np.geomspace(1e-5, 1, 400)
    tm, up = red_wins(ps, q, s, N), red_wins_upfront(ps, s, N, int(audit * N))
    safety_tm, safety_up, p_up = 1 - tm.max(), 1 - up.max(), ps[up.argmax()]
    p_sim, games = 0.002, 4000  # played out round by round
    first = lambda hit: np.where(hit.any(1), hit.argmax(1), N)
    red_won = 0
    for _ in range(8):  # 500 games at a time, to keep the table of random numbers small
        u = rng.random((games // 8, N), dtype=np.float32)
        caught, landed = u < p_sim * q, (u >= p_sim * q) & (u < p_sim * (q + (1 - q) * s))
        red_won += (first(landed) < first(caught)).sum()
    red_sim = red_won / games
    red_formula = red_wins(p_sim, q, s, N)
    mc_se = np.sqrt(red_formula * (1 - red_formula) / games)

    lab = labs.Lab()
    lab.row("one model's standard error (500 items, 70%)", f"{100 * se_one:.1f} points")
    lab.row("true spread of the measured gap", f"{100 * gap.std():.2f} points   unpaired SE says {100 * se_unpaired:.2f}, paired SE says {100 * se_paired:.2f}")
    lab.row("item correlation between the models", f"{rho:.2f}   so sqrt(2(1 - rho)) = {np.sqrt(2 * (1 - rho)):.2f} of one model's error")
    lab.row("the worse model ties or wins", f"{worse_ge:.0%} of benchmarks")
    lab.row("Bradley-Terry: expected wins against actual", f"largest difference {fixed_point:.1e} votes; ratings within {np.abs(fitted - theta_true).max():.2f} of the truth")
    lab.row("control: an attack is caught with probability q", f"{q:.2f}")
    lab.row("control: red wins at attack rate 0.2%", f"simulated {red_sim:.3f}   formula {red_formula:.3f}")
    lab.row("control: blue's safety", f"upfront auditing {safety_up:.0%} (red attacks {p_up:.4%} of the time)   trusted monitoring {safety_tm:.0%}")
    lab.note = ("Comparing two models on the same items cuts the gap's error by the factor the item correlation allows; and "
                "in the control game the attack rate drops out, so safety is set by how often the monitor catches an attack.")

    assert abs(se_paired / gap.std() - 1) < 0.05, "the paired standard error is the gap's true spread"
    assert se_unpaired > 1.3 * gap.std(), "the unpaired one overstates it when items are shared"
    assert abs(gap.std() / (np.sqrt(2 * (1 - rho)) * se_one) - 1) < 0.08, "Var(X - Y) = 2 (1 - rho) sigma^2"
    assert fixed_point < 1e-6, "at the maximum-likelihood ratings, expected wins equal actual wins"
    assert np.abs(fitted - theta_true).max() < 0.2 and np.all(np.diff(fitted) > 0), "and the ratings recover the order"
    assert abs(red_sim - red_formula) < 4 * mc_se, "the geometric series matches the game played out"
    assert abs(safety_tm - q / (q + (1 - q) * s)) < 1e-3, "with many rounds the attack rate drops out"
    assert abs(safety_tm - 0.75) < 0.01 and abs(safety_up - 0.22) < 0.01, "the film's 75% and 22%"

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.linspace(-0.1, 0.14, 61)
    ax[0].hist(gap, bins=bins, density=True, color=labs.BLUE, alpha=0.55, label=f"{reps:,} simulated benchmarks")
    grid = np.linspace(-0.1, 0.14, 300)
    ax[0].plot(grid, stats.norm.pdf(grid, 0.02, se_unpaired), color=labs.RED, label="normal with the unpaired SE")
    ax[0].plot(grid, stats.norm.pdf(grid, 0.02, se_paired), color=labs.GREEN, label="normal with the paired SE")
    ax[0].axvline(0, color=labs.MUTED, ls="--", lw=1)
    ax[0].set(title="The measured gap between two models 2 points apart", xlabel="accuracy of A minus accuracy of B")
    ax[0].set_xlim(-0.1, 0.24)
    ax[0].legend(loc="upper right")
    ax[1].semilogx(ps, up, color=labs.RED, label="upfront auditing")
    ax[1].semilogx(ps, tm, color=labs.BLUE, label="trusted monitoring")
    ax[1].plot([p_sim], [red_sim], "o", color=labs.GOLD, label="played out round by round")
    ax[1].axhline((1 - q) * s / (q + (1 - q) * s), color=labs.MUTED, ls="--", lw=1)
    ax[1].set(title="The control game: red's chance of winning", xlabel="how often red attacks (per problem)",
              ylabel="P(red wins)", ylim=(0, 1))
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab

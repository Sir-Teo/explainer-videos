"""Lab 22: consumption and saving: Friedman's cross-section on simulated households, Hall's test on US data, Campbell
and Mankiw's instrument, the buffer-stock household by the endogenous grid method and its propensity to spend, the
wealthy hand-to-mouth, and when a pay-as-you-go pension raises welfare in Diamond's economy."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import household as hh
from explainer.economics.agora import olg
from explainer.economics.island import truths

TITLE = "Consumption and saving: permanent income, the buffer stock and overlapping generations"
GOAL = ("Recover Keynes's function from households who follow Friedman's rule; test Hall's random walk on US data; "
        "estimate the share of rule-of-thumb households by instrumental variables; solve a buffer-stock household and "
        "measure how much of a windfall it spends; see why spending follows liquid wealth; and find when a pension is "
        "a free lunch.")
TASKS = [
    "Friedman: double the spread of transitory income. What happens to the cross-section slope and to the share "
    "consumed by the poorest tenth? Check the slope against the formula.",
    "Buffer stock: raise the chance of a year with no income from 0.5% to 2%. How do the target and the average "
    "propensity to spend a windfall change?",
    "Diamond: find the patience (beta a generation) at which the economy is exactly at the golden rule, R = 1 + n.",
]


def _quarterly():
    f = {k: np.array(data.fred(k)["value"], float) for k in ("PCEND", "PCES", "DNDGRG3M086SBEA", "DSERRG3M086SBEA",
                                                             "DSPIC96")}
    dates = data.fred("PCEND")["date"]
    C = f["PCEND"] / f["DNDGRG3M086SBEA"] * 100 + f["PCES"] / f["DSERRG3M086SBEA"] * 100
    Y = f["DSPIC96"]
    q = {}
    for d, c, y in zip(dates, C, Y):
        q.setdefault((int(d[:4]), (int(d[5:7]) - 1) // 3), []).append((c, y))
    keys = sorted(k for k in q if len(q[k]) == 3 and 1959 <= k[0] <= 2019)
    Cq = np.array([np.mean([a for a, _ in q[k]]) for k in keys])
    Yq = np.array([np.mean([b for _, b in q[k]]) for k in keys])
    return np.diff(np.log(Cq)), np.diff(np.log(Yq))


def run(seed=0):
    lab = labs.Lab()
    T = truths(22)

    pop = T["population"]
    f = hh.friedman_cross_section(**{**pop, "seed": pop["seed"] + seed})
    assert abs(f["elasticity"] - f["elasticity_theory"]) < 0.03     # Friedman's attenuation formula
    lab.row("Friedman: cross-section C = a + bY; log slope (formula)",
            f"a = {f['intercept']:.2f}, b = {f['slope']:.2f}; {f['elasticity']:.3f} ({f['elasticity_theory']:.3f})")
    lab.row("share consumed, poorest and richest tenth; C/Y over 60 years",
            f"{f['apc_by_decile'][0]:.2f}, {f['apc_by_decile'][-1]:.2f}; {min(f['apc_time']):.3f}-"
            f"{max(f['apc_time']):.3f}")

    dc, dy = _quarterly()
    n = len(dc)
    idx = np.arange(4, n)
    X = np.column_stack([np.ones(len(idx)), dy[idx - 2], dy[idx - 3], dy[idx - 4]])
    b = np.linalg.lstsq(X, dc[idx], rcond=None)[0]
    e = dc[idx] - X @ b
    V = e @ e / (len(idx) - 4) * np.linalg.inv(X.T @ X)
    R = np.eye(4)[1:]
    F = float((R @ b) @ np.linalg.inv(R @ V @ R.T) @ (R @ b) / 3)
    lab.row("Hall's test, US 1960-2019: income growth at lags 2-4; joint F",
            f"{b[1]:.3f}, {b[2]:.3f}, {b[3]:.3f}; F = {F:.1f}")

    rt = T["rule_of_thumb"]
    reps = [hh.rule_of_thumb(lam=rt["lam"], T=rt["T"], seed=rt["seed"] + seed + k) for k in range(100)]
    lab.row(f"Campbell-Mankiw on 100 island economies (lambda = {rt['lam']}): mean OLS; median IV",
            f"{np.mean([r['ols'] for r in reps]):.2f}; {np.median([r['iv'] for r in reps]):.2f}")

    B = T["buffer"]
    bs = hh.buffer_stock(**B)
    m = np.array(bs["m"])
    assert np.all(np.diff(bs["c"]) >= -1e-9) and np.interp(0.5, m, bs["mpc"]) > np.interp(5.0, m, bs["mpc"])
    lab.row("buffer stock: target cash; MPC at m = 0.5, 1, 5",
            f"{bs['target']:.2f}; " + ", ".join(f"{np.interp(x, m, bs['mpc']):.2f}" for x in (0.5, 1.0, 5.0)))
    s = hh.simulate_mpc(bs, n=10000, windfall=1 / 12, seed=T["mpc"]["seed"] + seed)
    lab.row("10,000 households: share of a month's windfall spent within the year (permanent income)",
            f"{s['mean_mpc']:.3f} ({hh.pih(1 / 12, T['pih']['r'])['share']:.3f})")

    I = T["illiquid"]
    owner = hh.buffer_stock(**{**B, "beta": B["beta"] * B["R"] / I["R_h"]})
    h = hh.hand_to_mouth(bs, owner, n=10000, own=I["own"], median=I["median"], sd=I["sd"], short=I["short"],
                         seed=I["seed"] + seed)
    lab.row("hand-to-mouth: MPC owners, renters; correlation with net worth, with liquid wealth",
            f"{h['mpc_owners']:.2f}, {h['mpc_renters']:.2f}; {h['corr_net']:+.2f}, {h['corr_liquid']:+.2f}")

    o = T["olg"]
    for beta in o["betas"]:
        st = olg.diamond_steady(beta=beta, alpha=o["alpha"], n=o["n"], A=o["A"])
        assert (st["R"] < 1 + o["n"]) == (st["k"] > st["k_gold"])  # inefficient exactly when beyond the golden rule
        pw = olg.pension_welfare(o["pensions"], beta=beta, alpha=o["alpha"], n=o["n"], A=o["A"])
        best = o["pensions"][int(np.argmax(pw["utility"]))]
        lab.row(f"Diamond, beta {beta}: R against 1 + n; k* against golden; best pension",
                f"{st['R']:.2f} vs {1 + o['n']:.1f}; {st['k']:.2f} vs {st['k_gold']:.2f}; d = {best:g}")

    lab.note = ("Households who consume a fixed share of permanent income look Keynesian in a cross-section, because "
                "measured income mixes luck with permanent income. US consumption growth is predicted by income growth "
                "two to four quarters back, against Hall. Prudence and impatience give a buffer stock, a concave "
                "consumption function and a propensity to spend windfalls many times larger than permanent income's; "
                "it follows liquid wealth, not net worth. A pay-as-you-go pension raises welfare only when the economy "
                "has more capital than the golden rule.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot(m, bs["c"], color=labs.BLUE, label="with income risk")
    sure = hh.buffer_stock(**{**B, "perm_sd": 0.0, "tran_sd": 0.0, "p_zero": 0.0})
    ax[0].plot(m, sure["c"], color=labs.ORANGE, label="no risk")
    ax[0].plot([0, 2], [0, 2], color="grey", lw=0.8)
    ax[0].set(title="The buffer-stock consumption function", xlabel="cash on hand m", ylabel="consumption c(m)")
    ax[0].legend()
    for beta, col in zip(o["betas"], (labs.BLUE, labs.ORANGE)):
        pw = olg.pension_welfare(o["pensions"], beta=beta, alpha=o["alpha"], n=o["n"], A=o["A"])
        u = np.array(pw["utility"])
        ax[1].plot(o["pensions"], 100 * (np.exp((u - u[0]) / (1 + beta)) - 1), color=col, label=f"beta = {beta}")
    ax[1].axhline(0, color="grey", lw=0.8)
    ax[1].set(title="A pay-as-you-go pension's welfare effect", xlabel="pension per worker d",
              ylabel="% of consumption")
    ax[1].legend()
    lab.fig = fig
    return lab

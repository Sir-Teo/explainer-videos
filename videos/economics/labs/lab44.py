"""Lab 44: dynamics, platforms and antitrust: Rust's bus engine model estimated by the nested fixed point on his data,
the myopic alternative and the CCP short cut, a Markov-perfect duopoly, double marginalization, a two-sided platform,
lock-in, the inverted U between competition and innovation, Q-learning price setters, and Baron and Myerson's
regulator."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import io
from explainer.economics.island import truths

TITLE = "Dynamics, platforms and antitrust"
GOAL = ("Estimate Zurcher's costs from his choices and test whether he looked ahead; compare the nested fixed point "
        "with conditional choice probabilities; solve a dynamic duopoly; price a two-sided platform; see a worse "
        "technology win; trace the inverted U; watch two learning algorithms collude; and regulate a firm that knows "
        "more than you.")
TASKS = [
    "Rust: estimate on groups 1-3 only, then on group 4 only. Do the costs differ across bus models, and what does "
    "the likelihood-ratio test of pooling say?",
    "Platforms: give side 1 a stronger taste for side 2 (alpha1 from 0.2 to 0.8). Which price falls, and why?",
    "Algorithms: shorten the memory to nothing (state = 0 always) by editing the learner. Does the profit gain "
    "survive?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(44)

    R = io.rust_panel(data.rust_buses(), groups=T["rust"]["groups"])
    p = io.rust_transitions(R["dx"])
    nf = io.rust_nfxp(R["x"], R["d"], p)
    my = io.rust_nfxp(R["x"], R["d"], p, beta=0.0, start=(5.0, 50.0))
    lab.row("Rust's groups 1-4: bus-months, rebuilds; monthly steps of 0, 1, 2", f"{len(R['x']):,}, {R['d'].sum()}; "
            + ", ".join(f"{100 * x:.1f}%" for x in p))
    lab.row("NFXP at beta 0.9999: RC, theta (se); log likelihood", f"{nf['RC']:.2f}, {nf['theta1']:.2f} "
            f"({nf['se'][0]:.2f}, {nf['se'][1]:.2f}); {nf['loglik']:.1f}")
    lab.row("myopic (beta 0): log likelihood; likelihood-ratio statistic", f"{my['loglik']:.1f}; "
            f"{2 * (nf['loglik'] - my['loglik']):.1f}")
    assert nf["loglik"] > my["loglik"]
    cc = io.rust_ccp(R["x"], R["d"], p, degree=2)
    lab.row("CCP (quadratic first step): RC, theta", f"{cc['RC']:.2f}, {cc['theta1']:.2f}")

    D = T["duopoly"]
    eq = io.pm_duopoly(K=D["K"], M=D["M"], a=D["a"], delta=D["delta"], beta=D["beta"])
    X = eq["X"]
    lab.row("duopoly: investment when level (mean), two ahead, two behind",
            f"{np.mean(np.diag(X)):.2f}, {np.mean([X[i + 2, i] for i in range(D['K'] - 2)]):.2f}, "
            f"{np.mean([X[i, i + 2] for i in range(D['K'] - 2)]):.2f}")

    V = io.double_marginalization(**T["vertical"])
    lab.row("double marginalization: integrated price; separate firms' price; joint profit",
            f"{V['p_int']:.0f}; {V['p_sep']:.0f}; {V['profit_int']:.0f} against {V['profit_m'] + V['profit_r']:.0f}")
    P = T["platform"]
    for a2 in (0.2, 0.8, 1.2):
        r = io.platform(P["a1"], P["a2"], P["alpha1"], a2)
        lab.row(f"platform with alpha2 = {a2}: prices to sides 1 and 2", f"{r['p'][0]:.3f}, {r['p'][1]:.3f}")
    L = T["lockin"]
    lk = io.inferior_lockin(L["quality"], 0.02, L["adopters"], 200, L["seed"] + seed)
    lab.row("lock-in: share of runs the worse first mover wins (network effect 0.02)",
            f"{100 * lk['share_a_wins']:.0f}%")

    N = T["innovation"]
    inn = [io.step_by_step(d_, N["pi1"], N["r"], N["h"])["innovation"] for d_ in (0.05, 0.4, 1.0)]
    lab.row("innovation at low, middle and high competition", ", ".join(f"{x:.3f}" for x in inn))
    assert inn[1] > inn[0] and inn[1] > inn[2]

    q = io.q_learning(max_iter=1_500_000, stable=50_000, seed=T["qlearn"]["seed"] + seed)
    lab.row("Q-learning: limit prices (Nash, monopoly); profit gain", f"{q['prices'][0]:.3f}, {q['prices'][1]:.3f} "
            f"({q['nash']:.3f}, {q['monopoly']:.3f}); {q['gain']:.2f}")

    B = io.baron_myerson(**T["regulation"])
    lab.row("regulation: high-cost output, efficient and chosen; the low type's rent",
            f"{B['q_hi_full']:.1f}, {B['q_hi']:.1f}; {B['rent']:.1f}")

    lab.note = ("Zurcher's choices reveal the costs he weighed, and they reject a superintendent who ignored the "
                "future. Firms race hardest when close; platforms charge the side others follow the least; "
                "network effects can lock in a worse technology; learning algorithms can find collusive prices on "
                "their own.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    m = io.Rust(nf["RC"], nf["theta1"], p)
    ax[0].plot(np.arange(90) * 5, m.prob_replace(), color=labs.ORANGE)
    ax[0].set(title="Rust: chance of a rebuild", xlabel="thousand miles since the last rebuild", ylim=(0, 0.08))
    ds = np.linspace(0.02, 1.0, 40)
    ax[1].plot(ds, [io.step_by_step(d_, N["pi1"], N["r"], N["h"])["innovation"] for d_ in ds], color=labs.BLUE)
    ax[1].set(title="the inverted U", xlabel="competition", ylabel="innovation")
    lab.fig = fig
    return lab

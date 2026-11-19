"""Lab 9: general equilibrium: the box, the core, existence, stability, risk sharing and planning."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import ge
from explainer.economics.island import truths

TITLE = "General equilibrium: the box, the core, existence and stability"
GOAL = ("Find the competitive equilibrium of the Edgeworth box and check that it is on the contract curve; watch the "
        "core shrink as the economy is replicated; find an approximate equilibrium of a three-good economy with "
        "Sperner's labelling and Scarf's walk, and the exact one with Newton's method; run the auctioneer on the "
        "island and on Scarf's economy; share risk with Arrow securities; and read the prices off Kantorovich's "
        "linear programme.")
TASKS = [
    "The box: let Ana spend 60% of her wealth on fish instead of 40%. What happens to the price of fish, to the lens "
    "and to the core with five copies of each trader?",
    "Scarf's economy: start the auctioneer from three different prices. Check that the sum of squared prices and "
    "their product stay constant, and measure how the time for one turn depends on the start.",
    "Kantorovich: make a boat need three planks and one mast. Which machines change jobs, how many sets a day can "
    "the yard make, and what are the new resolving multipliers?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(9)

    # the box
    b = T["box"]
    A = ge.Trader((b["ana"]["a"], 1 - b["ana"]["a"]), b["ana"]["e"])
    B = ge.Trader((b["bo"]["a"], 1 - b["bo"]["a"]), b["bo"]["e"])
    eq = ge.box_equilibrium(A, B)
    assert np.allclose(ge.excess([A, B], [eq["p"], 1.0]), 0, atol=1e-12)
    assert abs(eq["xA"][1] - float(ge.contract_curve(A, B, eq["xA"][0]))) < 1e-9
    lab.row("the box: price of a fish (baskets); Ana's bundle", f"{eq['p']:.4f}; ({eq['xA'][0]:.3f}, "
                                                                f"{eq['xA'][1]:.3f})")
    widths = []
    for r in (1, 2, 5):
        lo, hi = ge.core_interval(A, B, r)
        widths.append(hi - lo)
        lab.row(f"the core with {r} cop{'y' if r == 1 else 'ies'} of each: Ana's fish", f"{lo:.3f} to {hi:.3f}")
    assert widths[0] > widths[1] > widths[2]

    # existence and computation: three goods
    th = T["three"]
    T3 = [ge.Trader(a, e) for _, a, e in th["traders"]]

    def z(p):
        return ge.excess(T3, p)

    exact = np.array(ge.newton(z, [1.0, 1.0, 1.0])["p"])
    exact /= exact.sum()
    for N in (12, 48):
        w = ge.sperner_walk(ge.sperner_labels(z, N), N)
        lab.row(f"Scarf's walk on a grid of {N}: rooms, and the error in prices",
                f"{w['rooms']}, {np.max(np.abs(np.array(w['p']) - exact)):.4f}")
    lab.row("the exact equilibrium (prices adding to 1)", ", ".join(f"{x:.4f}" for x in exact))

    # stability
    out = ge.scarf_path(np.array(T["scarf_start"]), T=60.0)
    lab.row("Scarf's cycle: the range of sum p^2 and of p1 p2 p3 along the path",
            f"{np.ptp(out['norm']):.1e}, {np.ptp(out['product']):.1e}")
    assert np.ptp(out["norm"]) < 1e-6

    # production
    c = T["crusoe"]
    cr = ge.crusoe(c["A"], c["alpha"], c["hours"], c["b"])
    lab.row("Crusoe: hours worked, planned and by the market; the wage", f"{cr['plan']['L']:.4f}, "
                                                                        f"{cr['market']['L']:.4f}; "
                                                                        f"{cr['market']['w']:.4f}")

    # risk sharing
    rk = T["risk"]
    ad = ge.arrow_debreu(rk["e0"], rk["E"], rk["probs"], rk["beta"], rk["gamma"])
    bo = ge.bond_only(rk["e0"], rk["E"], rk["probs"], rk["beta"], rk["gamma"])
    lab.row("certainty equivalents: Arrow securities, a bond alone", f"{ad['ce'][0]:.2f}, {bo['ce'][0]:.2f}")

    # planning
    k = T["plan"]
    kp = ge.kantorovich(k["rates"], k["kit"])
    lab.row("Kantorovich: sets a day; value of a day on each machine", f"{kp['sets']:.2f}; " +
            ", ".join(f"{m}: {v:.3f}" for m, v in zip(k["machines"], kp["machine_value"])))
    lab.note = ("The equilibrium of the box clears both markets and sits on the contract curve; the core narrows "
                "toward it as traders multiply; Scarf's walk lands within a hundredth of the exact prices on a fine "
                "grid; the auctioneer circles for ever in Scarf's economy, keeping two quantities constant; the "
                "market reproduces Crusoe's own plan; Arrow securities remove risk the bond cannot; and the "
                "dual of the planner's programme prices every machine's day.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    X = np.add(A.e, B.e)
    xs = np.linspace(0.05, X[0] - 0.05, 300)
    ax[0].plot(xs, ge.cd_indifference(A.a[0], A.utility(A.e), xs), color=labs.ORANGE, lw=2, label="Ana through ω")
    ax[0].plot(xs, X[1] - ge.cd_indifference(B.a[0], B.utility(B.e), X[0] - xs), color=labs.BLUE, lw=2,
               label="Bo through ω")
    ax[0].plot(xs, ge.contract_curve(A, B, xs), color="goldenrod", lw=2, label="contract curve")
    ax[0].plot(*A.e, "ko")
    ax[0].plot(*eq["xA"], "o", color="goldenrod")
    ax[0].set(xlim=(0, X[0]), ylim=(0, X[1]), title="The Edgeworth box", xlabel="Ana's fish",
              ylabel="Ana's coconuts")
    ax[0].legend(fontsize=8)
    P = np.array(out["p"])
    Q = P / P.sum(axis=1, keepdims=True)
    ax[1].plot(Q[:, 0], Q[:, 1], color=labs.BLUE, lw=2)
    ax[1].plot([1 / 3], [1 / 3], "o", color=labs.ORANGE)
    ax[1].set(title="Scarf's cycle (prices adding to 1)", xlabel="good 1's price", ylabel="good 2's price")
    lab.fig = fig
    return lab

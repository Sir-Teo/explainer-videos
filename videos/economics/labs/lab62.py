"""Lab 62: the firm from the inside: productivity dispersion and competition, management scores, a management
experiment randomized by firm, piece rates and sorting, the Peter principle, executive pay, capital structure,
agency, buyouts, knowledge hierarchies, working from home, and the diversification discount."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import org as O

TITLE = "Inside the firm"
GOAL = ("Run the Island's plants, managers and owners: measure how productivity differs, test whether management "
        "causes it, and see how pay, promotion, debt and ownership change what people inside the firm do.")
TASKS = [
    "Make buyers switch less easily (O.dispersion(sigmas=(1.5, 2.0))). What happens to the survivors' 90/10 ratio and "
    "their number?",
    "Cut the experiment to 8 firms (O.experiment(firms=8, treated_firms=5, plants_per=(2, 1), reps=200)). How wide is "
    "the spread of estimates now?",
    "Raise the correlation between selling and managing skill to 0.8 (O.peter(rho=0.8)). Does promoting the best "
    "seller still cost the team?",
]


def run(seed=0):
    lab = labs.Lab()
    D = O.dispersion(seed=62 + seed)
    lab.row("survivors' 90/10 productivity ratio by elasticity 2, 3, 6, 10 (entrants)",
            ", ".join(f"{r['ratio_90_10']:.2f}" for r in D["rows"] if r["sigma"] in (2, 3, 6, 10))
            + f" ({D['entry_ratio_90_10']:.2f})")
    M = O.management(seed=62 + seed)
    lab.row("management: productivity slope per point of score (planted 0.25); lowest and highest owner",
            f"{M['slope']:.3f}; {min(M['by_owner'], key=M['by_owner'].get)}, "
            f"{max(M['by_owner'], key=M['by_owner'].get)}")
    P = O.practices(seed=62 + seed)
    lab.row("four practices: net value per dollar over three years",
            ", ".join(f"{k} {v['per_dollar']:+.2f}" for k, v in P["rows"].items()))
    X = O.experiment(reps=200, seed=62 + seed)
    assert abs(X["mean_est"] - X["effect"]) < 3 * X["sd_est"] / np.sqrt(200)       # centred on the truth
    lab.row("the experiment: first run (se); mean and spread over 200 runs (planted 0.17)",
            f"{X['first_est']:.3f} ({X['first_se']:.3f}); {X['mean_est']:.3f}, {X['sd_est']:.3f}")
    Pc = O.piece_rates(seed=62 + seed)
    lab.row("piece rates: output gain, same workers and after turnover; share from sorting",
            f"{100 * Pc['gain_effort']:.1f}%, {100 * Pc['gain_total']:.1f}%; {100 * Pc['share_sorting']:.0f}%")
    Pe = O.peter(seed=62 + seed)["rules"]
    lab.row("promotion: team sales under the best seller, the best manager, at random",
            ", ".join(f"{Pe[k]['team_sales']:.3f}" for k in ("the best seller", "the best manager", "at random")))
    C = O.ceo_pay()
    L = O.pay_for_luck(seed=62 + seed)
    lab.row("CEO pay: elasticity to own size; pay after six-fold growth; weak boards' pay for luck",
            f"{C['elasticity_own_size']:.2f}; x{C['ratio_after_sixfold']:.1f}; {L['weak board']['on_luck']:.2f}")
    T = O.tradeoff()
    lab.row("trade-off: best debt share and the gain in value", f"{100 * T['best']:.0f}%, {T['gain']:.1f}")
    pk = O.perks(alphas=[1.0, 0.5, 0.1])
    lab.row("perks at manager shares 100%, 50%, 10%", ", ".join(f"{v:.0f}" for v in pk["perks"]))
    B = O.buyouts(seed=62 + seed)
    lab.row("buyouts: jobs at old establishments after 2 and 5 years; whole firm after 5",
            f"{100 * B['emp_original'][2]:+.1f}%, {100 * B['emp_original'][5]:+.1f}%; {100 * B['emp_firm'][5]:+.1f}%")
    H = O.hierarchy(hs=(0.6, 0.1), cs=(0.05,))["rows"]
    lab.row("hierarchy: share workers solve, expensive and cheap communication", f"{H[0]['worker_solves']:.2f}, "
            f"{H[1]['worker_solves']:.2f}")
    W = O.wfh(seed=62 + seed)
    lab.row("working from home: performance (se); quits at home and in the office",
            f"{100 * W['performance']:.1f}% ({100 * W['performance_se']:.1f}); {100 * W['quit_home']:.0f}%, "
            f"{100 * W['quit_office']:.0f}%")
    G = O.conglomerates(seed=62 + seed)
    lab.row("diversification discount measured; the part there before", f"{100 * G['discount']:.1f}%, "
            f"{100 * G['before']:.1f}%")
    f = data.fred("OPHNFB")
    v = np.array(f["value"], float)
    years = (len(v) - 1) / 4
    lab.row("output per hour, American business: average growth since 1947",
            f"{100 * ((v[-1] / v[0]) ** (1 / years) - 1):.2f}% a year ({f['date'][0][:4]}-{f['date'][-1][:4]})")

    lab.note = ("Every number above is a comparison: plants with plants, treated with control, before with after. "
                "The firm is where economics meets the people who do the work.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    sig = [r["sigma"] for r in D["rows"]]
    ax[0].plot(sig, [r["ratio_90_10"] for r in D["rows"]], marker="o", color=labs.ORANGE)
    ax[0].set(title="survivors' productivity spread", xlabel="elasticity of substitution", ylabel="90/10 ratio")
    ax[1].hist(X["est_draws"], bins=20, color="tab:green", alpha=0.8)
    ax[1].axvline(X["effect"], color="k", lw=1, ls="--")
    ax[1].set(title="the management experiment, rerun", xlabel="estimated effect", ylabel="runs")
    lab.fig = fig
    return lab

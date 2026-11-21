"""Lab 56: the core exam: twelve questions in micro, macro and econometrics, each solved by its formula and checked
by brute force (a grid, a simulation, an optimizer), printed as a marked answer sheet."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import exam

TITLE = "The core exam"
GOAL = ("Work the twelve questions of a first-year core examination, and check every answer the way a grader would: "
        "against a special case, a brute-force computation or a simulation.")
TASKS = [
    "Lower alpha in kinked_budget to 0.3. Where does the consumer end up, and what is the MRS there?",
    "Run reserve_auction with n = 3 and r = 0.5. Does the best reserve change with the number of bidders?",
    "Run staggered_did(never=False). Why does two-way fixed effects get the sign wrong?",
]


def run(seed=0):
    lab = labs.Lab()
    k = exam.kinked_budget()
    lab.row("Q1 demand (segment); dx/dp2; CV against Laspeyres",
            f"{k['x']:.1f} ({k['where']}); {k['total']:.2f}; {k['cv']:.3f} vs {k['laspeyres']:.2f}")
    e = exam.externality_box()
    lab.row("Q2 equilibrium x_A; efficient x_A; Pigouvian tax; welfare gain",
            f"{e['xa_eq']:.2f}; {e['xa_po']:.3f}; {e['tax']:.2f}; {e['gain']:.3f}")
    a = exam.reserve_auction(draws=200_000, seed=56 + seed)
    lab.row("Q3 revenue: formula, simulated first price, simulated second price",
            f"{a['rev']:.4f}, {a['rev_fp_sim']:.4f}, {a['rev_sp_sim']:.4f}")
    assert abs(a["rev_fp_sim"] - a["rev"]) < 5e-3
    s = exam.screening()
    lab.row("Q4 q_L, q_H, rent, profit (first best)",
            f"{s['q_l']:.2f}, {s['q_h']:.2f}, {s['rent']:.2f}, {s['profit']:.3f} ({s['first_best']:.2f})")
    r = exam.ramsey_tax()
    lab.row("Q5 k* before and after; c on impact; c* after",
            f"{r['k_old']:.3f} -> {r['k_new']:.3f}; {r['c0']:.3f}; {r['c_new']:.3f}")
    assert r["c0"] > r["c_old"] > r["c_new"]
    m = exam.mccall_expiring()
    lab.row("Q6 reservation wage by periods of benefit left (0..8)", ", ".join(f"{x:.3f}" for x in m["res"]))
    d = exam.discretion()
    lab.row("Q7 inflation bias; average gap; response to a cost shock (pi, x); loss: discretion, commitment",
            f"{d['pi_bar']:.2f}; {d['x_bar']:.2f}; ({d['a_pi']:.2f}, {d['a_x']:.2f}); "
            f"{d['loss_d']:.2f}, {d['loss_c']:.2f}")
    g = exam.aiyagari_gap(rs=np.array([0.0, 0.02, 0.035]))
    lab.row("Q8 Aiyagari: r* against rho; capital against the riskless economy's",
            f"{100 * g['r']:.2f}% < {100 * g['rho']:.2f}%; {g['K']:.2f} vs {g['K_rep']:.2f}")
    sd = exam.supply_demand(seed=56 + seed)
    lab.row("Q9 OLS (plim); Wald (s.e.); truth", f"{sd['ols']:.3f} ({sd['plim_ols']:.3f}); {sd['wald']:.3f} "
            f"({sd['se_wald']:.3f}); {-sd['b']:.1f}")
    gm = exam.euler_gmm(seed=56 + seed)
    t2 = gm["two"]
    lab.row("Q10 two-step GMM: beta, gamma (s.e.); J on df, p",
            f"{t2['theta'][0]:.4f}, {t2['theta'][1]:.3f} ({t2['se'][0]:.4f}, {t2['se'][1]:.3f}); "
            f"{t2['J']:.2f} on {gm['df']}, {t2['p_J']:.2f}")
    st = exam.staggered_did()
    lab.row("Q11 TWFE against the average effect; imputation", f"{st['twfe']:.3f} vs {st['att']:.3f}; "
            f"{st['imputation']:.3f}")
    for b in st["bacon"]:
        lab.row(f"    Goodman-Bacon: {b['kind']} (cohort {b['g']:.0f})", f"{b['est']:.2f} with weight {b['w']:.3f}")
    lv = exam.long_run_var(reps=60, seed=56 + seed)
    lab.row("Q12 B (population) and its mean estimate over 60 samples",
            f"{np.round(lv['B'], 3).tolist()} / {np.round(lv['B_est_mean'], 3).tolist()}")

    lab.note = ("Every answer was computed twice, by the formula a candidate writes and by brute force; the solvers "
                "assert that the two agree. The habit to take into the exam room: check before the grader does.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    th, q = np.array(s["theta"]), np.array(s["q"])
    ax[0].plot(th, th, color="white", label="first best")
    ax[0].plot(th, q, color=labs.ORANGE, label="screening")
    ax[0].scatter([1, 2], [s["q_l"], s["q_h"]], color=labs.GREEN, label="two types", zorder=3)
    ax[0].set(title="Q4: quality by type", xlabel="theta", ylabel="q")
    ax[0].legend()
    t = np.arange(len(d["pi_d"]))
    ax[1].plot(t, d["pi_d"], color=labs.ORANGE, label="inflation, discretion")
    ax[1].plot(t, d["pi_c"], color=labs.ORANGE, ls="--", label="inflation, commitment")
    ax[1].plot(t, d["x_d"], color=labs.PURPLE, label="gap, discretion")
    ax[1].plot(t, d["x_c"], color=labs.PURPLE, ls="--", label="gap, commitment")
    ax[1].axhline(0, color="grey", lw=0.8)
    ax[1].set(title="Q7: a unit cost shock", xlabel="quarters")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab

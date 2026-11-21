"""Lab 66: geoeconomics and industrial policy: the reciprocal formula, the effective tariff rate, tariffs with revenue
in the quantitative trade model with and without retaliation, the two-bloc tariff war, the repeated game, the cost
of losing a supplier, resilience, the infant-industry tests and Brander and Spencer's subsidy race."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import tradewar as T

TITLE = "Geoeconomics and industrial policy"
GOAL = ("Compute what tariffs do in the quantitative trade model, when a tariff war starts and what it costs, what "
        "dependence on a supplier is worth to the supplier, and when an infant industry deserves protection.")
TASKS = [
    "Make trade more responsive (theta = 8) in the two-bloc war (T.two_bloc(Xb, us, 8.0)). How do the optimal tariff "
    "and the Nash losses change?",
    "Raise the discount rate in the infant-industry model to 15% (T.infant_industry(0.30, r=0.15)). Does the fast "
    "learner still pass Bastable's test?",
    "In Brander and Spencer's race, raise the firms' cost (T.brander_spencer(c=4)). Is the subsidy race still a "
    "prisoners' dilemma?",
]
TWO_BLOC = np.array([[0.214084, 0.020899], [0.020899, 0.744118]])   # US and the rest, CEPII 2019, deficits purged


def run(seed=0):
    lab = labs.Lab()
    v = T.reciprocal_rate(136.6, 13.1)
    v945 = T.reciprocal_rate(136.6, 13.1, phi=0.945)
    assert abs(v - 0.452) < 0.001 and abs(v945 - 0.120) < 0.001           # 45% and 12%
    lab.row("the reciprocal formula for Vietnam: as published (phi = 0.25), and with phi = 0.945",
            f"{100 * v:.0f}% and {100 * v945:.0f}%")
    c, m = data.fred("B235RC1Q027SBEA"), data.fred("A255RC1Q027SBEA")
    dm = dict(zip(m["date"], m["value"]))
    eff = {d: x / dm[d] for d, x in zip(c["date"], c["value"]) if d in dm}
    lab.row("the effective US tariff rate: 2017Q1, 2025Q1, its 2025 peak, latest",
            f"{100 * eff['2017-01-01']:.1f}%, {100 * eff['2025-01-01']:.1f}%, "
            f"{100 * max(x for d, x in eff.items() if d.startswith('2025')):.1f}%, {100 * eff[max(eff)]:.1f}%")
    rows = []
    for th in (2.0, 4.0, 8.0):
        for retal in (False, True):
            t = np.array([[0, 0.15], [0.15 if retal else 0.0, 0]])
            R = T.tariff_hat(TWO_BLOC, t, th)
            rows.append(f"theta {th:.0f}{' with' if retal else ''}: US {100 * R['welfare'][0]:+.2f}%")
    lab.row("a 15% US tariff, two blocs: US real income without and with retaliation", "; ".join(rows))
    B = T.two_bloc(TWO_BLOC, 0, 4.0, grid=np.round(np.linspace(0, 0.6, 13), 3))
    assert B["nash_us"] < 0 and B["nash_ro"] < 0 < B["optimal_us"]       # a prisoners' dilemma
    lab.row("the two-bloc war: optimal tariff; Nash tariffs; welfare at Nash (US, rest)",
            f"{100 * B['optimal']:.0f}%; {100 * B['nash'][0]:.0f}% and {100 * B['nash'][1]:.0f}%; "
            f"{100 * B['nash_us']:+.2f}% and {100 * B['nash_ro']:+.2f}%")
    st = T.stage_payoffs(B, 0.25)
    rep = T.repeated(st)
    lab.row("ten rounds: the best plan against each kind of partner", "; ".join(f"{k}: {v_}"
                                                                         for k, v_ in rep["best"].items()))
    lab.row("losing a supplier with 20% of spending (theta 2, 4, 8)",
            ", ".join(f"{100 * float(T.cutoff_loss(0.2, th)):.1f}%" for th in (2, 4, 8)))
    Rs = T.resilience()
    lab.row("resilience: the firm's and society's share from the risky supplier", f"{100 * Rs['x_private']:.0f}% "
            f"and {100 * Rs['x_social']:.0f}%")
    inf = {b: T.infant_industry(b, r=0.10) for b in (0.15, 0.20, 0.30)}
    lab.row("infant industries: Mill's and Bastable's tests for three learning rates",
            "; ".join(f"b = {b}: Mill {'yes' if x['mill'] else 'no'}, Bastable {'yes' if x['bastable'] else 'no'}"
                      for b, x in inf.items()))
    Bs = T.brander_spencer()
    assert Bs["both"]["w1"] < Bs["none"]["w1"] < Bs["one"]["w1"]
    lab.row("Brander and Spencer: country 1's welfare with no subsidies, alone, both",
            f"{Bs['none']['w1']:.2f}, {Bs['one']['w1']:.2f}, {Bs['both']['w1']:.2f}")

    lab.note = ("A large country can gain from a tariff only while others do not answer; dependence is power in "
                "proportion to how hard the supplier is to replace.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    g = np.array(B["grid"])
    ax[0].plot(B["br_us"], g, color="tab:blue", label="US best response")
    ax[0].plot(g, B["br_ro"], color=labs.ORANGE, label="rest's best response")
    ax[0].scatter([B["nash"][0]], [B["nash"][1]], color="tab:red", zorder=3, label="Nash")
    ax[0].set(title="the tariff war", xlabel="US tariff", ylabel="rest's tariff")
    ax[0].legend(fontsize=8)
    s = np.linspace(0, 0.5, 51)
    for th in (2, 4, 8):
        ax[1].plot(100 * s, 100 * T.cutoff_loss(s, th), label=f"theta {th}")
    ax[1].set(title="the cost of losing a supplier", xlabel="its share of spending, %", ylabel="loss, % of income")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab

"""Lab 14: incentives: teams, the principal-agent problem, the optimal linear share, informativeness, multitasking,
tournaments, career concerns and the ratchet, efficiency wages, sharecropping and relational contracts."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import contracts as ct
from explainer.economics.data import tables
from explainer.economics.island import truths

TITLE = "Incentives: contracts when effort is hidden"
GOAL = ("Measure the free rider's loss in a team; solve the two-outcome principal-agent problem and Holmström and "
        "Milgrom's linear contract; remove a common shock; watch multitasking drop the unmeasured task; compute "
        "tournament effort, career concerns and the ratchet; find Shapiro and Stiglitz's equilibrium unemployment; "
        "solve for the best crop share; simulate Friday's contract; and find when a relational contract holds.")
TASKS = [
    "Linear contract: make Friday twice as averse to risk (r = 0.4). What is the best share now, and how much of the "
    "first-best surplus is lost? Which of the two costs (less effort, more risk) grew?",
    "Multitasking: make the two tasks nearly the same hours (substitutability 0.9). At what bonus is the unmeasured task "
    "dropped? What does that say about bonuses for jobs whose tasks compete for the same time?",
    "Shapiro and Stiglitz: double the chance of catching a shirker (0.5 to 1). How do the wage and unemployment change, "
    "and why does better monitoring raise employment?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(14)

    t = T["team"]
    tm = ct.team(18, t["a"], t["c"])
    assert abs(tm["lost"] - 17 ** 2 / 18 ** 2) < 1e-12
    lab.row("team of 18: each one's effort (alone = 1); surplus lost", f"{tm['e_eq']:.3f}; {tm['lost']:.3f}")

    d = T["discrete"]
    two = ct.two_outcome(d["p_high"], d["p_low"], d["y_high"], d["y_low"], d["cost"], d["reservation"])
    lab.row("two outcomes: wages after a good and a poor harvest; risk premium", f"{two['w_high']:.2f}, "
            f"{two['w_low']:.2f}; {two['risk_cost']:.2f}")

    p = T["playit"]
    la = ct.linear_agency(p["r"], p["c"], p["sigma"])
    assert abs(la["beta_star"] - 2 / 3) < 1e-12
    lab.row("linear contract: best share; surplus; first best", f"{la['beta_star']:.3f}; {la['surplus']:.2f}; "
            f"{la['first_best_surplus']:.2f}")
    for b in (1 / 3, 1.0):
        assert abs(ct.linear_agency(p["r"], p["c"], p["sigma"], beta=b)["surplus"] - 2.5) < 1e-9

    rp = T["rpe"]
    rel = ct.relative_performance(rp["r"], rp["c"], rp["common"], rp["own"])
    lab.row("informativeness: share on own output and on output less the common shock",
            f"{rel['beta_own']:.3f}, {rel['beta_relative']:.3f}")

    mt = T["multitask"]
    m = ct.multitask(mt["s"], mt["c"], mt["base"], betas=np.linspace(0, 2, 201))
    drop = float(m["beta"][np.argmax(m["e2"] <= 1e-12)])
    lab.row("multitasking: the bonus at which the unmeasured task is dropped", f"{drop:.2f}")

    to = T["tournament"]
    tr = ct.tournament([1.0, 2.0], to["sigma"], to["c"])
    lab.row("tournament: effort per unit of prize gap; at twice the noise",
            f"{tr['g0']:.3f}; {ct.tournament([1.0], 2 * to['sigma'], to['c'])['g0']:.3f}")

    ca = ct.career_concerns(**T["careers"])
    lab.row("career concerns: implicit incentive in years 1, 15, 30; explicit share in year 1 and 30",
            f"{ca['implicit'][0]:.2f}, {ca['implicit'][14]:.2f}, {ca['implicit'][-1]:.2f}; "
            f"{ca['explicit'][0]:.2f}, {ca['explicit'][-1]:.2f}")
    ra = T["ratchet"]
    rt = ct.ratchet(1.0, ra["c"], ra["delta"], ra["bonus"])
    lab.row("ratchet: effort with a fixed target and with a ratchet", f"{rt['effort_fixed_target']:.2f}, "
            f"{rt['effort_ratchet']:.2f}")

    ss = ct.shapiro_stiglitz(**T["shirking"])
    lab.row("Shapiro-Stiglitz: employed of 100; wage; unemployment", f"{ss['L_eq']:.1f}; {ss['w_eq']:.2f}; "
            f"{ss['u_eq']:.3f}")

    sc = ct.sharecrop(**T["sharecrop"])
    lab.row("sharecropping: best share; surplus at a wage, a rent and the best share",
            f"{sc['s_star']:.3f}; {sc['surplus_wage']:.1f}, {sc['surplus_rent']:.1f}, {sc['surplus_best']:.1f}")

    rc = ct.relational([0.25, 0.5, 0.75], **T["relational"])
    lab.row("relational contract: effort sustained at continuation 0.25, 0.5, 0.75",
            ", ".join(f"{x:.1f}" for x in rc["effort"]))

    # Friday's contract simulated: 20,000 days at the best share, to check the cost of risk by Monte Carlo
    rng = np.random.default_rng(1987 + seed)
    b, c, r, sig = la["beta_star"], p["c"], p["r"], p["sigma"]
    e = b / c
    y = e + rng.normal(0, sig, 20_000)
    alpha = -b * e + c * e ** 2 / 2 + r * b ** 2 * sig ** 2 / 2
    pay = alpha + b * y
    ce = -np.log(np.mean(np.exp(-r * (pay - c * e ** 2 / 2)))) / r      # CARA certainty equivalent of the pay
    lab.row("simulated: Friday's certainty equivalent at the best contract (theory 0)", f"{ce:.3f}")

    lz = tables.LAZEAR_2000.data
    lab.row("Safelite: output per worker; from incentives, about", f"+{100 * lz['gain_published']:.0f}%; half")
    lab.note = ("A team of eighteen loses 89% of its surplus to free riding; the cheapest pay for hard work still "
                "exposes Friday to risk; the best linear share is two-thirds, and removing the common shock raises it "
                "to 0.85; a bonus on the measured task drops the other at 1; tournament effort halves when noise "
                "doubles; career concerns fade as explicit pay should rise; a ratchet cuts effort to a tenth; "
                "efficiency wages leave 14% unemployed; the best crop share is 0.61; and a relational contract "
                "reaches first best once the relationship is likely enough to go on.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    bs = np.linspace(0, 1, 101)
    ax[0].plot(bs, [ct.linear_agency(p["r"], p["c"], p["sigma"], beta=x)["surplus"] for x in bs], color=labs.BLUE,
               lw=2, label="Friday's contract")
    ax[0].axhline(la["first_best_surplus"], color="grey", ls="--", label="if effort could be seen")
    ax[0].set(title="Profit against the share", xlabel="Friday's share", ylabel="baskets a day")
    ax[0].legend()
    ax[1].plot(m["beta"], m["e1"], color=labs.BLUE, lw=2, label="measured task")
    ax[1].plot(m["beta"], m["e2"], color=labs.ORANGE, lw=2, label="unmeasured task")
    ax[1].set(title="Multitasking", xlabel="bonus on the measured task", ylabel="effort")
    ax[1].legend()
    lab.fig = fig
    return lab

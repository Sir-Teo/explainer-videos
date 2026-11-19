"""Lab 17: markets by design: the Boston rule and deferred acceptance, stable matchings and who proposes, Clarke's
pivot rule, the bilateral-trade bound, top trading cycles, kidney exchange, the assignment game, and what a school
lottery reveals."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import matching as mt
from explainer.economics.data import tables
from explainer.economics.island import truths

TITLE = "Markets by design: matching, mechanisms and clearinghouses"
GOAL = ("Run the Boston rule and deferred acceptance on the same lists and find who gains by lying; list every stable "
        "matching of a small market and see each side's best; make the truth pay with Clarke's rule; bound the gains "
        "from trade; trade huts by top trading cycles; find the most transplants in a kidney pool; split an "
        "assignment game's surplus; and estimate a school's effect from its lottery.")
TASKS = [
    "The workshops: give the kiln a second place. Does the Boston rule still punish your truthful list? Does any "
    "other child now gain by lying?",
    "The kidney pool: allow cycles of up to four pairs. How many transplants are possible without the altruist's chain?",
    "The lottery: set the sibling share to zero. Do the comparison that ignores type and the one within type now agree, "
    "and why?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(17)

    p = T["playit"]
    students = {k: list(v) for k, v in p["students"].items()}
    schools = {s: list(p["lottery"]) for s in p["capacity"]}
    cap = dict(p["capacity"])
    b = mt.boston(students, schools, cap)["match"]
    d = mt.deferred_acceptance(students, schools, cap)["match"]
    lab.row("workshops: your place under Boston (truth / kiln first) and under DA (truth)",
            f"{b['you']} / " + next(r["gets"] for r in mt.outcomes_by_report("you", students, schools, cap)
                                    if r["report"][0] == "kiln") + f"; {d['you']}")
    lab.row("blocking pairs under Boston; under DA", f"{mt.blocking_pairs(b, students, schools, cap)}; "
            f"{mt.blocking_pairs(d, students, schools, cap)}")

    bd = T["board"]
    pa = {k: list(v) for k, v in bd["apprentices"].items()}
    pw = {k: list(v) for k, v in bd["workshops"].items()}
    st = mt.all_stable(pa, pw)
    lab.row("the board: stable matchings; DA rounds with apprentices / workshops asking",
            f"{len(st)}; {mt.deferred_acceptance(pa, pw)['rounds']} / {mt.deferred_acceptance(pw, pa)['rounds']}")

    pv = mt.pivotal(**T["bridge"])
    lab.row("footbridge: build?; Clarke taxes", f"{pv['build']}; {pv['tax']}")

    tr = mt.bilateral_trade(seed=1983 + seed)
    lab.row("bilateral trade: efficient, posted price, double auction (exact; simulated)",
            ", ".join(f"{tr['exact'][k]:.4f} ({tr['sim'][k]:.4f})" for k in ("efficient", "posted", "double")))

    h = mt.top_trading_cycles({k: list(v) for k, v in T["huts"].items()})
    lab.row("huts: allocation by top trading cycles", str(h["alloc"]))

    k = T["kidneys"]
    kr = mt.kidney_exchange({q: set(v) for q, v in k["compat"].items()}, k["max_cycle"],
                            {a: set(v) for a, v in k["altruists"].items()}, k["max_chain"])
    lab.row("kidneys: transplants with swaps of two, cycles of three, and a chain",
            f"{kr['pairs_only']}, {kr['cycles']}, {kr['with_chains']}")

    g = mt.assignment_game(T["assignment"]["values"])
    lab.row("assignment game: total; sellers' payoffs at the buyers' and sellers' ends",
            f"{g['total']:.0f}; {g['buyer_optimal']['sellers']} / {g['seller_optimal']['sellers']}")

    lt = dict(T["lottery"])
    reps = lt.pop("reps")
    rows = np.array([[r["ols_everyone"], r["iv_no_controls"], r["iv_type_controls"]]
                     for r in (mt.lottery_study(**{**lt, "seed": lt["seed"] + 1 + j + 1000 * seed})
                               for j in range(min(reps, 60)))])
    lab.row("lottery study (60 lotteries): OLS, IV ignoring type, IV within type (truth 0.4)",
            ", ".join(f"{m:.2f}" for m in rows.mean(axis=0)))
    den = tables.SCHOOL_EFFECTS.data["denver"]
    lab.row("Denver charters (2SLS): first stage; math; math without score controls",
            f"{den['first_stage'][0]:.3f}; {den['math'][0]:.3f}; {den['math_no_score_controls'][0]:.3f}")

    lab.note = ("The Boston rule hands you the loft for the truth and the kiln for a lie; deferred acceptance gives the "
                "kiln for the truth and is stable. The board has three stable matchings, each side's best found by "
                "letting it ask. Clarke's rule makes Ana pay 15 she cannot be refunded; the best bilateral mechanism "
                "gets 84 percent of the gains; cycles of three and a chain place every patient; and a lottery is an "
                "experiment only within each applicant type.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].hist(rows[:, 1], bins=15, color=labs.ORANGE, alpha=0.7, label="ignoring type")
    ax[0].hist(rows[:, 2], bins=15, color=labs.BLUE, alpha=0.7, label="within type")
    ax[0].axvline(lt["effect"], color="black", ls="--")
    ax[0].set(title="What a lottery reveals", xlabel="estimated effect", ylabel="lotteries")
    ax[0].legend()
    c = np.linspace(0, 1, 101)
    ax[1].fill_between(c, c, 1, color=labs.BLUE, alpha=0.2, label="every good trade")
    ax[1].fill_between(c[c <= 0.75], c[c <= 0.75] + 0.25, 1, color=labs.ORANGE, alpha=0.4, label="the double auction")
    ax[1].set(xlim=(0, 1), ylim=(0, 1), title="Myerson and Satterthwaite", xlabel="seller's cost", ylabel="buyer's value")
    ax[1].legend()
    lab.fig = fig
    return lab

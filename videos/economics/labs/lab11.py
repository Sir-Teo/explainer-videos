"""Lab 11: games: dominance, Nash equilibria, mixing, backward induction, repetition, learning and levels of
thinking."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import games as gm
from explainer.economics.island import truths

TITLE = "Games: equilibrium, repetition, learning and levels of thinking"
GOAL = ("Find every equilibrium of the battle of the sexes by support enumeration; solve the penalty kick by "
        "indifference; solve the entry game and the centipede by backward induction; find grim trigger's threshold "
        "and the folk theorem's region; run Axelrod's tournament with and without mistakes; compute chicken's best "
        "correlated equilibrium; watch the replicator and regret matching; and fit the cognitive hierarchy to the "
        "guessing game's means.")
TASKS = [
    "Tournament: add a strategy to games.STRATEGIES that cooperates unless the other defected twice in the last three "
    "rounds. Where does it rank with and without 5% noise?",
    "The penalty: make the kicker's natural side more accurate (score 0.98 when the keeper guesses wrong). How do the "
    "kicker's and the keeper's mixtures move? Which one changes more, and why (the indifference principle)?",
    "The guessing game: refit tau when p = 1/2, using Nagel's first-round mean of 27.05. Is it deeper or shallower "
    "than the 2/3 sessions?",
]


def _bimatrix(cells):
    A = np.array([[cells[0][0], cells[1][0]], [cells[2][0], cells[3][0]]], float)
    B = np.array([[cells[0][1], cells[1][1]], [cells[2][1], cells[3][1]]], float)
    return A, B


def run(seed=0):
    lab = labs.Lab()
    T = truths(11)

    # Nash equilibria
    A, B = _bimatrix(T["grammar"]["battle"])
    eqs = gm.support_enumeration(A, B)
    assert len(eqs) == 3
    lab.row("battle of the sexes: equilibria (Pr Ana regatta, Pr Bo regatta)",
            "; ".join(f"({e['p'][0]:.3f}, {e['q'][0]:.3f})" for e in eqs))
    pd = T["pd"]
    P = np.array([[pd["R"], pd["S"]], [pd["T"], pd["P"]]])
    assert gm.pure_nash(P, P.T) == [(1, 1)]

    # mixing
    S = np.array(T["penalty"]["score"])
    m = gm.mixed_2x2(S, 1 - S)
    lab.row("penalty: kicker left, keeper left, scoring rate", f"{m['p']:.3f}, {m['q']:.3f}, {m['row_payoff']:.3f}")

    # trees
    e = T["entry"]
    bi = gm.backward_induction(gm.entry_game(e["fight"], e["accommodate"], e["stay_out"]))
    c = T["centipede"]
    ci = gm.backward_induction(gm.centipede(c["moves"], c["start"], c["grow"]))
    lab.row("entry game and centipede: subgame-perfect paths", f"{' then '.join(bi['path'])}; {ci['path'][0]} at once")

    # repetition
    thr = gm.grim_threshold(pd["T"], pd["R"], pd["P"], pd["S"])
    fr = gm.folk_region(P, P.T)
    lab.row("grim trigger's threshold; the minmax point", f"{thr:.2f}; {fr['minmax']}")
    t = T["tournament"]
    clean = gm.tournament(t["field"], t["rounds"], 0.0, t["repeats"], t["seed"])
    noisy = gm.tournament(t["field"], t["rounds"], t["noise"], t["repeats"], t["seed"])
    lab.row("tournament winners: without and with 5% mistakes", f"{clean['ranking'][0]}, {noisy['ranking'][0]}")
    lab.row("tit for tat's rank: without and with mistakes",
            f"{clean['ranking'].index('TFT') + 1}, {noisy['ranking'].index('TFT') + 1}")

    # coordination, evolution, learning
    A, B = _bimatrix(T["grammar"]["chicken"])
    ce = gm.correlated_equilibrium(A, B)
    mixed = gm.mixed_2x2(A, B)
    assert ce["row_payoff"] > mixed["row_payoff"]
    lab.row("chicken: mixed equilibrium against the best correlated one (each)",
            f"{mixed['row_payoff']:.3f} against {ce['row_payoff']:.3f}")
    h = T["hawkdove"]
    HD = np.array([[(h["V"] - h["C"]) / 2, h["V"]], [0, h["V"] / 2]])
    x = gm.replicator(HD, [0.1, 0.9], T=60)
    lab.row("hawk and dove: share of hawks after the replicator", f"{x[-1][0]:.4f} (V/C = {h['V'] / h['C']:.2f})")
    R = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], float)
    rm = gm.regret_matching(R, -R, rounds=20000, seed=seed + 2000)
    lab.row("regret matching on rock-paper-scissors: average strategy; regret a round",
            ", ".join(f"{v:.3f}" for v in rm["row"][-1]) + f"; {rm['regret_row']:.4f}")

    # levels of thinking
    t_n, t_f = gm.fit_tau(36.73), gm.fit_tau(18.9)
    lab.row("cognitive hierarchy: tau for Nagel's 36.73 and the FT's 18.9", f"{t_n:.2f}, {t_f:.2f}")
    assert t_f > t_n
    lab.note = ("Three equilibria in the battle of the sexes, one of them mixed; the penalty kick scores the same "
                "either way in equilibrium; backward induction rules out the empty threat and unravels the centipede; "
                "cooperation needs patience of one half; the forgiving strategies win the tournament, and repair "
                "beats reciprocity once there are mistakes; the traffic light beats mixing; the replicator finds the "
                "hawks' stable share; regret matching finds the rock-paper-scissors equilibrium; and people think one "
                "to four steps ahead.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    sc = np.array(clean["score"])
    order = np.argsort(-sc)
    ax[0].barh([clean["names"][i] for i in order][::-1], sc[order][::-1], color=labs.BLUE)
    ax[0].set(title="Axelrod's round robin, no mistakes", xlabel="points a round")
    taus = np.linspace(0.05, 6, 120)
    ax[1].plot(taus, [gm.cognitive_hierarchy(v)["mean"] for v in taus], color=labs.ORANGE, lw=2)
    ax[1].axhline(36.73, color="grey", ls="--")
    ax[1].axhline(18.9, color="grey", ls=":")
    ax[1].set(title="The cognitive hierarchy's mean choice", xlabel="tau", ylabel="mean choice")
    lab.fig = fig
    return lab

"""Lab 53: information and persuasion: the prosecutor's design and its concave closure, cheap talk by bias, Bayes-Nash
quantities, the best Bayes correlated equilibrium for two investors, a garbling check, the dialogue to agreement, the
global game's thresholds, cascades exactly and simulated, the chain store, bargaining and relational effort."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import persuade as P
from explainer.economics.island import truths

TITLE = "Information and persuasion"
GOAL = ("Compute what a sender who controls information can achieve, how much talk can carry, and how information "
        "spreads, freezes and coordinates when many people learn from each other.")
TASKS = [
    "Make the judge stricter (a standard of 0.7). How many defendants can the prosecutor get convicted now?",
    "Raise the adviser's bias in cheap talk from 0.05 to 0.15. How many messages survive?",
    "Make each hint right 90% of the time. How often does a queue lock onto the worse restaurant?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(53)

    pr = P.prosecutor(**T["prosecutor"])
    lab.row("prosecutor: convicted with none, full, designed investigation",
            f"{pr['none']:.2f}, {pr['full']:.2f}, {pr['optimal']:.2f}")
    mu = np.linspace(0, 1, 401)
    cv = P.concavify(mu, (mu >= T["prosecutor"]["threshold"]).astype(float))
    at = float(np.interp(T["prosecutor"]["prior"], mu, cv))
    lab.row("concave closure at the prior", f"{at:.3f}")
    assert abs(at - pr["optimal"]) < 1e-6

    for b in T["biases"]:
        r = P.cheap_talk(b)
        lab.row(f"cheap talk, bias {b}: messages, receiver's loss", f"{r['N']}, {r['receiver_loss']:.4f}")

    C = T["cournot"]
    ec = C["p_high"] * C["c_high"] + (1 - C["p_high"]) * C["c_low"]
    q1 = (C["a"] - 2 * C["c1"] + ec) / 3
    lab.row("Bayes-Nash Cournot: firm 1's quantity", f"{q1:.3f}")

    I = T["invest"]

    def U(th):
        U0 = np.array([[0.0, 0.0], [th, th + I["together"]]])
        return U0, U0.T.copy()

    (U0g, U1g), (U0b, U1b) = U(I["good"]), U(I["bad"])
    best = P.bce_lp([I["p_good"], 1 - I["p_good"]], [[U0g, U0b], [U1g, U1b]],
                    [np.array([[0.0, 1.0], [1.0, 2.0]])] * 2)
    lab.row("information design: expected investors, best design against full disclosure",
            f"{best['value']:.2f} against {2 * I['p_good']:.2f}")

    E = T["experiments"]
    Q = np.array(E["P"]) @ np.array(E["garble"])
    lab.row("Blackwell: Q a garbling of P? P of Q? R of P?",
            f"{P.garbling(E['P'], Q)['garbling']}, {P.garbling(Q, E['P'])['garbling']}, "
            f"{P.garbling(E['P'], E['R'])['garbling']}")

    D = T["dialogue"]
    dl = P.dialogue([1 / D["n"]] * D["n"], list(D["event"]), [list(c) for c in D["a"]], [list(c) for c in D["b"]],
                    D["state"])
    lab.row("dialogue: announced posteriors", ", ".join(f"{h['posterior']:.3f}" for h in dl["history"]))

    G = T["global"]
    sharp = P.global_game(G["c"], G["sigma"], G["prior_mean"], G["prior_sds"][-1])["thetas"]
    lab.row("global game: flat-prior threshold; thresholds with sharp public news",
            f"{P.global_game(G['c'], G['sigma'])['theta']:.2f}; {[round(x, 3) for x in sharp]}")

    Cs = T["cascade"]
    ch = P.cascade_chain(Cs["q"], Cs["n"])
    sim = P.cascade_sim(Cs["q"], Cs["n"], 5000, seed)
    lab.row("cascades: right in the end, exactly and simulated", f"{ch['limit_right']:.3f}, {sim['share_right']:.3f}")

    Cn = T["chain"]
    lab.row("chain store: towns at the end where entry can occur", f"{P.chain_store(**Cn)['k_star']}")
    B = T["bargain"]
    co = P.coase_two_period(B["v_high"], B["v_low"], B["share_high"], B["delta"])
    lab.row("Rubinstein at delta 0.9; Coase seller's plan and delay",
            f"{P.rubinstein(0.9)['first']:.3f}; {co['best']['plan']}, {co['best']['delay']:.2f}")
    R = T["relational"]
    rel = P.relational([0.25, 0.5, 0.75], R["theta"], R["c"])
    lab.row("relational effort at delta 0.25, 0.5, 0.75", ", ".join(f"{e:.2f}" for e in rel["effort"]))

    lab.note = ("A sender who commits gets the concave closure of her value at the prior; talk carries less as "
                "interests diverge; obedient recommendations coordinate receivers; garbling orders experiments only "
                "sometimes; announcements of beliefs lead to agreement; private noise selects one equilibrium; "
                "cascades stop learning; reputations deter; private values delay bargains; the future enforces "
                "promises.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ps = np.linspace(0, 1, 201)
    p0, t = T["prosecutor"]["prior"], T["prosecutor"]["threshold"]
    post = p0 / (p0 + (1 - p0) * ps)
    conv = np.where(post >= t - 1e-12, p0 + (1 - p0) * ps, 0.0)
    ax[0].plot(ps, conv, color=labs.ORANGE, label="convicted")
    ax[0].plot(ps, post, color=labs.PURPLE, label="belief after a flag")
    ax[0].set(title="the prosecutor's design", xlabel="share of innocent flagged")
    ax[0].legend()
    x = np.arange(1, Cs["n"] + 1)
    ax[1].plot(x, ch["right"], color=labs.GREEN, label="right cascade")
    ax[1].plot(x, ch["wrong"], color=labs.RED, label="wrong cascade")
    ax[1].set(title="cascades", xlabel="diners")
    ax[1].legend()
    lab.fig = fig
    return lab

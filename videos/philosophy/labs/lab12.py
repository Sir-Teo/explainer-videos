"""Lab 12: run the muddy children, the coordinated attack and Zollman's scientists, and check each against its theorem."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import epistemic as ep

TITLE = "Common knowledge: made by an announcement, never by messengers"
GOAL = ("Check that with k muddy children the muddy ones know in round k and the clean ones a round later, that "
        "nothing happens without the father, that each delivered message adds one level of mutual knowledge and "
        "never common knowledge, and that Zollman's sparse network finds the truth more often than the complete one.")
TASKS = [
    "Run ep.muddy_rounds(4, (1, 1, 0, 0)) and compare its sizes with Problem 2: 16, 15, 11, then one world.",
    "Raise eps in ep.zollman_run from 0.01 to 0.05. Does the cycle still beat the complete network, and why?",
    "Add 60 to every guess before calling ep.diversity. Which of the three terms changes, and which cannot?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # the muddy children: random groups, against the theorem
    checked = []
    for _ in range(8):
        n = int(rng.integers(3, 7))
        actual = tuple(int(x) for x in rng.integers(0, 2, n))
        if sum(actual) == 0:
            actual = (1,) + actual[1:]
        r = ep.muddy_rounds(n, actual)
        k = sum(actual)
        assert r["knows_at"] == [k if m else k + 1 for m in actual], (actual, r["knows_at"])
        checked.append((n, k))
    eight = ep.muddy_rounds(8)
    assert eight["sizes"][:6] == [256, 255, 247, 219, 163, 93] and set(eight["knows_at"]) == {8}
    before = ep.everyone_knew_already(3)
    assert ep.without_father(3) and before == {"everyone_knows": True, "common": False, "after": True}
    lab.row("8 random groups of 3 to 6 children", "with k muddy, the muddy know in round k, the clean in round k + 1: all 8")
    lab.row("eight muddy children", f"worlds left {eight['sizes']}; all know in round {eight['knows_at'][0]}")
    lab.row("three muddy, before the father speaks", f"everyone knows 'someone is muddy': {before['everyone_knows']}; "
                                                     f"common knowledge: {before['common']}; after: {before['after']}")

    # the coordinated attack
    tower = ep.attack_depth(8)
    assert all(t["depth"] == t["delivered"] - 1 and not t["common"] for t in tower)
    lab.row("coordinated attack, 0 to 8 messages", f"levels of 'everyone knows' {[t['depth'] for t in tower[1:]]}; common knowledge: never")

    # Fitch and Aumann
    fitch = ep.fitch_check()
    assert fitch["valid_in_T"] and not fitch["valid_in_K"]
    g = ep.GP_EXAMPLE
    talk = ep.agreement_dialogue(g["states"], g["prior"], g["A"], g["B"], g["event"], g["actual"])
    assert talk[0]["A"] != talk[0]["B"] and talk[-1]["A"] == talk[-1]["B"], "they start apart and end agreed"
    lab.row("agreement dialogue", " → ".join(str(t["says"]) for t in talk))

    # the diversity prediction theorem on a random crowd
    truth = 1198.0
    guesses = list(truth + rng.normal(0, 40, 800) + rng.normal(0, 60, 800))
    d = ep.diversity(guesses, truth)
    assert abs(d["crowd_error"] - (d["average_error"] - d["diversity"])) < 1e-6 * d["average_error"]
    assert d["crowd_error"] < 0.05 * d["average_error"]
    shared = ep.diversity([x + 60 for x in guesses], truth)
    assert abs(shared["diversity"] - d["diversity"]) < 1e-6 * d["diversity"] and shared["crowd_error"] > 2000
    lab.row("800 guesses at the ox", f"crowd error {d['crowd_error']:.1f} = average error {d['average_error']:.0f} − diversity {d['diversity']:.0f}")
    lab.row("the same crowd with a shared bias of 60", f"crowd error {shared['crowd_error']:.0f}; diversity unchanged")

    # Zollman's networks
    runs, out = 100, {}
    for kind in ("cycle", "complete"):
        res = [ep.zollman_run(kind, rng=rng) for _ in range(runs)]
        out[kind] = (sum(ok for ok, _ in res) / runs, float(np.mean([t for ok, t in res if ok])))
    assert out["cycle"][0] > out["complete"][0] + 0.1 and out["cycle"][1] > 3 * out["complete"][1]
    lab.row(f"Zollman, {runs} runs each", f"cycle right {out['cycle'][0]:.0%} in {out['cycle'][1]:.0f} rounds; "
                                         f"complete right {out['complete'][0]:.0%} in {out['complete'][1]:.0f} rounds")
    lab.note = ("A public announcement makes common knowledge at once, and the children's reasoning runs on it; "
                "messengers who may be lost add one level of 'everyone knows' each and never get there. Among "
                "scientists, hearing everything spreads early bad luck to everyone: the sparse network is slower "
                "and more often right.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    sizes = eight["sizes"]
    labels = ["start", "father"] + [f"round {i}" for i in range(1, len(sizes) - 1)]
    ax[0].bar(range(len(sizes)), sizes, color=labs.BLUE)
    for i, v in enumerate(sizes):
        ax[0].text(i, v + 5, str(v), ha="center", color=labs.INK, fontsize=9)
    ax[0].set_xticks(range(len(sizes)), labels, rotation=35, ha="right", fontsize=8)
    ax[0].set(title="Eight muddy children: worlds still possible", ylabel="worlds", ylim=(0, 290))
    ax[0].set_axisbelow(True)
    n = [t["delivered"] for t in tower]
    ax[1].step(n, [max(t["depth"], 0) for t in tower], where="mid", color=labs.GOLD, label="levels of 'everyone knows the plan'")
    ax[1].plot(n, n, color=labs.MUTED, ls="--", label="messages delivered")
    ax[1].axhline(9.2, color=labs.RED, lw=1.5)
    ax[1].text(0.1, 9.45, "common knowledge needs every level: never reached", color=labs.RED, fontsize=9)
    ax[1].set(title="The coordinated attack: one storey per messenger", xlabel="messages delivered", ylim=(-0.3, 10.3),
              yticks=range(0, 9, 2))
    ax[1].legend(loc="center left")
    lab.fig = fig
    return lab

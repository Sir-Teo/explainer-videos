"""Lab 24: every syllogism's validity by brute force and four accounts of people's answers scored on open data; the
information in each card of the selection task; the Tower of Hanoi's state space searched three ways; the nine
dots inside and outside the box; and mental rotation rates fitted person by person to open data."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import opendata
from explainer.psychology.psyche import reason as R

TITLE = "Reasoning and problem solving"
GOAL = ("Find the valid syllogisms and see which account of people's answers fits; compute the information in "
        "each card; search the Tower of Hanoi; prove the nine dots need the outside of the box; and fit each "
        "person's speed of mental rotation.")
TASKS = [
    "Drop the assumption that every term names something (allow empty sets in R._models). Which syllogisms lose "
    "their conclusion, and does logic's fit to people improve or worsen?",
    "Add a fifth account to R.predict that says 'no valid conclusion' whenever the two premises are both "
    "particular or both negative. How many commonest answers does it now predict?",
    "Fit rotation rates separately for 'same' and 'mirror' trials. Is a mirror pair rotated at the same speed, or "
    "do people give up early?",
]


def run(seed=0):
    out = labs.Lab()

    # 1. syllogisms
    d = opendata.syllogisms_ragni2016()
    parsed = [R.parse_ccobra(t, r) for t, r in zip(d["task"], d["response"])]
    T = R.response_table([a for a, _ in parsed], [b for _, b in parsed])
    n_valid = sum(R.valid_conclusions(t) != ["NVC"] for t in R.TASKS)
    out.row("syllogisms with a valid conclusion (existential import)", f"{n_valid} of 64")
    assert n_valid == 27
    ri = {r: k for k, r in enumerate(R.RESPONSES)}
    for acct in ("logic", "atmosphere", "matching", "phm"):
        hits = sum(int(np.argmax(T[k])) in [ri[r] for r in R.predict(t, acct)] for k, t in enumerate(R.TASKS))
        out.row(f"commonest answer predicted: {acct}", f"{hits} of 64")

    # 2. the selection task
    g = R.selection_information(0.1, 0.2)
    out.row("expected information gain, bits: p, q, not-q, not-p",
            ", ".join(f"{g[c]:.3f}" for c in ("p", "q", "not-q", "not-p")))
    assert g["p"] > g["q"] > g["not-q"] > g["not-p"]

    # 3. the Tower of Hanoi
    S, E = R.hanoi_graph(3)
    lens = np.array([len(R.hill_climb(3, rng=s)) - 1 for s in range(101)])
    lat = R.goal_stack_solver(4)["latency"]
    out.row("3 discs: states, legal moves; hill-climber median moves (shortest 7)",
            f"{len(S)}, {len(E)}; {np.median(lens):.0f}")
    out.row("4 discs: goal-stack pauses longest before moves", ", ".join(str(int(k) + 1) for k in np.argsort(-lat)[:4]))

    # 4. the nine dots
    out.row("nine dots: drawings turning inside the square; outside it", f"{len(R.nine_dots(0, 2))}; "
            f"{len(R.nine_dots(-1, 3))}")

    # 5. mental rotation
    m = opendata.mental_rotation()
    ok = m["same"] & m["correct"]
    slopes = []
    for s_ in np.unique(m["subject"]):
        f = R.rotation_fit(m["angle"][ok & (m["subject"] == s_)], m["rt"][ok & (m["subject"] == s_)])
        slopes.append(f["slope"])
    slopes = np.array(slopes)
    out.row("rotation: people with a rising slope; median rate", f"{(slopes > 0).sum()} of {len(slopes)}; "
            f"{1000 / np.median(slopes):.0f} degrees a second")

    out.note = ("Only logic predicts the 'no valid conclusion' answers, and the shortcuts do better where a "
                "conclusion follows; the p "
                "card carries the most information and not-p almost none; a hill-climber wanders where subgoals "
                "would not; the nine dots have no solution inside the square; and nearly everyone turns a picture "
                "at a steady speed.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    angles = np.array([0, 50, 100, 150])
    means = [np.mean(m["rt"][ok & (m["angle"] == a)]) for a in angles]
    ax[0].plot(angles, means, "o-", color=labs.GOLD, label="people (trial means)")
    ax[0].set(title="Mental rotation", xlabel="angle (degrees)", ylabel="time to say 'same' (ms)")
    ax[0].legend(fontsize=8)
    ax[1].hist(lens, bins=range(5, 60, 2), color=labs.BLUE)
    ax[1].axvline(7, color="#ef6f6c", ls="--")
    ax[1].set(title="Hill-climbing the tower (3 discs)", xlabel="moves", ylabel="runs")
    out.fig = fig
    return out

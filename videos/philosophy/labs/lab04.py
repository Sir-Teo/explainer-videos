"""Lab 4: check each modal axiom against its frame condition on every small frame, then model-check Peterson's protocol."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import modal

TITLE = "Axioms, frames, and a protocol"
GOAL = ("For T, D, B, 4, 5 and Löb's axiom, count the frames on three worlds where the axiom is valid and compare "
        "with the frames that have the matching shape of arrows; repeat on random five-world frames; then explore "
        "the state graphs of Peterson's algorithm and its broken variant.")
TASKS = [
    "Add the axiom '<>[]p -> []<>p' to the table. Which frames on three worlds validate it? Guess the condition on "
    "the arrows before you look.",
    "Check '[]<>p -> <>[]p' (McKinsey) on every three-world frame and try to state its frame condition in "
    "first-order terms.",
    "In modal.peterson, make a third variant that never sets the turn. Does mutual exclusion still hold? Is every "
    "waiting process eventually served?",
]

NAMES = {"T": "reflexive", "D": "serial", "B": "symmetric", "4": "transitive", "5": "euclidean",
         "L": "transitive, no cycles"}
EXPECT = {"T": 64, "D": 343, "B": 64, "4": 171, "5": 39, "L": 19}  # the film's counts on three worlds


def closure(R, n, kind):
    R = set(R)
    if kind == "T":
        R |= {(w, w) for w in range(n)}
    if kind == "B":
        R |= {(v, u) for u, v in R}
    if kind in ("4", "L"):
        if kind == "L":
            R = {(u, v) for u, v in R if u < v}  # a strict order to start from
        while True:
            new = {(u, x) for u, v in R for w, x in R if v == w} - R
            if not new:
                break
            R |= new
    return R


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    counts = {}
    for name in "TDB45L":
        r = modal.correspondence(name, 3)
        counts[name] = r["valid"]
        lab.row(f"{name}: {r['formula']}", f"valid on {r['valid']:>3} of {r['frames']} frames; "
                                           f"agrees with '{NAMES[name]}' on {r['agree']}")
        assert r["agree"] == r["frames"] == 512 and r["mismatch"] is None, f"{name} matches its frame condition"
        assert r["valid"] == EXPECT[name]

    # Random frames on five worlds (2^25 of them, too many to list): half are pushed into the class, half are not.
    n, trials, agree, inside = 5, 240, 0, 0
    for k in range(trials):
        name = "TB4L5D"[k % 6]
        R = {(u, v) for u in range(n) for v in range(n) if rng.random() < rng.uniform(0.1, 0.6)}
        if rng.random() < 0.5:
            R = closure(R, n, name)
        f, cond = modal.parse(modal.AXIOMS[name][0]), modal.AXIOMS[name][1]
        valid, shaped = modal.valid_on_frame(f, R, n), cond(R, n)
        agree += valid == shaped
        inside += shaped
    lab.row("random frames on 5 worlds", f"axiom and condition agree on {agree} of {trials} ({inside} have the shape)")
    assert agree == trials and 30 < inside < trials - 30, "both kinds of frame were tried, and the match is exact"

    good, bad = modal.peterson(), modal.peterson(broken=True)
    ok, _, n_good = modal.mutual_exclusion(good)
    ok_bad, trace, n_bad = modal.mutual_exclusion(bad)
    lab.row("Peterson's algorithm", f"{n_good} reachable states, {len(good.graph()[1])} edges, mutual exclusion holds: {ok}")
    lab.row("the broken variant", f"{n_bad} states; both critical after {len(trace) - 1} steps")
    assert ok and n_good == 34 and len(good.graph()[1]) == 62
    assert not ok_bad and n_bad == 50 and len(trace) - 1 == 8 and trace[-1][0] == trace[-1][1] == 4
    for a, b in zip(trace, trace[1:]):
        assert b in [t for _, t in bad.step(a)], "the counterexample is a real run"
    lab.note = ("Each axiom is valid on exactly the frames with its shape of arrows, on every frame tried; the same "
                "world-by-world evaluation, run over a program's states, proves Peterson's protocol and finds the "
                "eight-step failure of its broken twin.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    x = np.arange(6)
    ax[0].bar(x, [counts[k] for k in "TDB45L"], color=labs.BLUE)
    for i, k in enumerate("TDB45L"):
        ax[0].text(i, counts[k] + 8, f"{counts[k]}\n" + NAMES[k].replace(", ", ",\n"), ha="center", va="bottom",
                   fontsize=8.5, color=labs.INK)
    ax[0].set(title="Frames on 3 worlds (of 512) where the axiom is valid", xticks=x, ylim=(0, 440),
              xticklabels=["T", "D", "B", "4", "5", "Löb"], ylabel="frames")

    def by_depth(system):
        order, parent = system.explore()
        depth = {}
        for s in order:
            depth[s] = 0 if parent[s] is None else depth[parent[s][0]] + 1
        d = np.bincount(list(depth.values()))
        bad_at = [depth[s] for s in order if s[0] == 4 and s[1] == 4]
        return d, bad_at

    dg, _ = by_depth(good)
    db, bad_at = by_depth(bad)
    ax[1].plot(range(len(dg)), dg, "o-", color=labs.GREEN, label=f"Peterson: {n_good} states, never both critical")
    ax[1].plot(range(len(db)), db, "o-", color=labs.RED, label=f"broken variant: {n_bad} states")
    ax[1].axvline(min(bad_at), color=labs.RED, ls="--", lw=1)
    ax[1].text(min(bad_at) - 0.15, 0.6, "both critical", color=labs.RED, ha="right", fontsize=9)
    ax[1].set(title="Reachable states by number of steps from the start", xlabel="steps", ylabel="new states",
              ylim=(0, max(db.max(), dg.max()) + 4))
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab

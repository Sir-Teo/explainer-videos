"""Lab 8: run Kripke's construction and revision theory on sentences that talk about their own truth."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import truth

TITLE = "Kripke's fixed points and revision sequences, computed"
GOAL = ("Iterate Kripke's jump on the film's world of thirteen sentences and on a random world, check that the "
        "stages only ever add values and end in the least of all fixed points, and compare Kripke's verdicts with "
        "revision theory's.")
TASKS = [
    "Add the pair P: 'Q is true', Q: 'P is true' to the world. How many fixed points are there now, and why?",
    "Replace the liar by truth.REVENGE's sentence inside a copy of WORLD and call truth.iterate. What happens to s8?",
    "Change revision_verdicts' steps from 12 to 3. Which verdicts change, and what does that say about 'stably'?",
]


def below(a, b):
    """a is below b in the information order: b agrees with a wherever a has a value."""
    return all(a[k] == "n" or a[k] == b[k] for k in a)


def random_world(rng, size=6):
    names = [f"r{i}" for i in range(size)]
    pick = lambda: ("T", names[int(rng.integers(size))])  # noqa: E731
    world = {}
    for name in names:
        kind = int(rng.integers(6))
        world[name] = [("fact", True), ("fact", False), pick(), ("not", pick()), ("and", pick(), ("not", pick())),
                       ("or", pick(), pick())][kind]
    return world


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    world = truth.WORLD
    stages = truth.kripke_stages(world)
    lfp, fps, kinds = stages[-1], truth.fixed_points(world), truth.classify(world)
    count = {k: sum(v == k for v in kinds.values()) for k in ("grounded", "ungrounded", "paradoxical")}
    lab.row("the film's world", f"{len(world)} sentences; the jump closes after {len(stages) - 1} stages")
    lab.row("fixed points", f"{len(fps)}   (the truth-teller H can be t, f or n; the liar L is n in all of them)")
    lab.row("grounded / ungrounded / paradoxical", f"{count['grounded']} / {count['ungrounded']} / {count['paradoxical']}")
    assert all(below(a, b) for a, b in zip(stages, stages[1:])), "the stages only add values"
    assert truth.is_fixed(world, lfp) and all(below(lfp, fp) for fp in fps), "the least fixed point is below every other"
    assert len(fps) == 3 and {fp["H"] for fp in fps} == {"t", "f", "n"} and all(fp["L"] == "n" for fp in fps)
    assert (count["grounded"], count["ungrounded"], count["paradoxical"]) == (6, 2, 5)

    # Kripke's theorem on random worlds, against brute force over all 3^6 interpretations
    checked = 0
    for _ in range(12):
        w = random_world(rng)
        st = truth.kripke_stages(w)
        brute = truth.all_fixed_points(w)
        assert all(below(a, b) for a, b in zip(st, st[1:])) and st[-1] in brute
        assert all(below(st[-1], fp) for fp in brute), "least among all fixed points"
        key = lambda d: tuple(sorted(d.items()))  # noqa: E731
        assert sorted(map(key, truth.fixed_points(w))) == sorted(map(key, brute)), "every fixed point extends the least"
        checked += len(brute)
    lab.row("12 random worlds of 6 sentences", f"{checked} fixed points found by brute force; the staged one is least in each")

    # revenge: the exclusion liar has no fixed point
    orbit = "".join(s["R"] for s in truth.iterate(truth.REVENGE, 6))
    assert truth.all_fixed_points(truth.REVENGE) == [] and orbit == "ntftftf"
    lab.row("the revenge sentence R", f"stages {' '.join(orbit)}: no fixed point among t, f, n")

    # revision theory over every starting hypothesis
    verdicts = truth.revision_verdicts(world)
    assert verdicts["L"] == "unstable" and verdicts["H"] == "depends"
    assert kinds["s8"] == "paradoxical" and verdicts["s8"] == "stably true", "where Kripke and revision disagree"
    assert all(verdicts[n] in ("stably true", "stably false") for n, k in kinds.items() if k == "grounded")
    assert all((verdicts[n] == "stably true") == (lfp[n] == "t") for n, k in kinds.items() if k == "grounded")
    lab.row("revision, all 8,192 starting guesses", f"L {verdicts['L']}, H {verdicts['H']}, s8 {verdicts['s8']} (Kripke: {kinds['s8']})")
    yablo = [len(truth.yablo_solutions(n)) for n in range(1, 9)]
    assert yablo == [1] * 8
    lab.row("Yablo's staircase cut to 1..8 sentences", f"consistent assignments: {yablo}")
    lab.note = ("Kripke's stages only ever add values and stop at the least fixed point, where the liar has none; "
                "revision theory keeps two values and the liar never settles. They part on 'the liar is true or not "
                "true': no value for Kripke, stably true under revision.")

    from matplotlib.colors import ListedColormap
    fig, ax = labs.figure(2, size=(11, 4.8))
    names = list(world)
    code = {"n": 0, "f": 1, "t": 2}
    cmap = ListedColormap([labs.GRID, labs.RED, labs.GREEN])
    grid = np.array([[code[s[n]] for s in stages] for n in names])
    ax[0].imshow(grid, cmap=cmap, vmin=0, vmax=2, aspect="auto")
    for i, n in enumerate(names):
        for j, s in enumerate(stages):
            ax[0].text(j, i, s[n], ha="center", va="center", color=labs.BG if s[n] != "n" else labs.MUTED, fontsize=9)
    ax[0].set_xticks(range(len(stages)), [f"stage {j}" for j in range(len(stages))])
    ax[0].set_yticks(range(len(names)), [f"{n}: {truth.GLOSS[n]}" for n in names], fontsize=8)
    ax[0].set(title="Kripke's jump: green true, red false, grey neither")
    start = {n: bool(rng.integers(2)) for n in names}
    seq = truth.revision(world, start, 9)
    grid = np.array([[2 if h[n] else 1 for h in seq] for n in names])
    ax[1].imshow(grid, cmap=cmap, vmin=0, vmax=2, aspect="auto")
    ax[1].set_xticks(range(len(seq)), [str(j) for j in range(len(seq))])
    ax[1].set_yticks(range(len(names)), [f"{n}   {verdicts[n]}" for n in names], fontsize=8)
    ax[1].set(title="Revision from a random guess (verdicts: all guesses)", xlabel="revision stage")
    for a in ax:
        a.grid(False)
    lab.fig = fig
    return lab

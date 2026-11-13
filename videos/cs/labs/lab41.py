"""Lab 41: name objects as git does, rebuild by hashes instead of clocks, and install packages iff a formula is satisfiable."""

from videos.coursekit import labs

import itertools
import math

import numpy as np

from explainer.cs.vcs import build
from explainer.cs.vcs import deps
from explainer.cs.vcs import git

TITLE = "Three machines, one idea: hashes, rebuilds and version solving"
GOAL = ("Check the series' object store against two ids every git installation produces, and count the objects one "
        "edit renames in a random tree. Rebuild a 202-target project after six kinds of edit with make's timestamps "
        "and with hashes and early cutoff. Then turn random 3-SAT formulas into package universes and check that "
        "the solver installs them exactly when brute force finds a satisfying assignment.")
TASKS = [
    "Edit a file one directory deeper (add a level to the path). How many objects get new names, and how many are shared?",
    "Call build.build_traces(p, built, cutoff=False) for the comment edits. Which rebuild counts change, and why?",
    "Raise the number of variables from 10 to 14 and watch where the installable share crosses one half. Does it move towards 4.26?",
]
RATIOS = (1, 2, 3, 4, 5, 6, 8, 10)
N_VARS, TRIALS = 10, 16


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. content addresses: the two ids below are what `git hash-object` prints for an empty file and "hello world"
    assert git.obj_id("blob", b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
    assert git.obj_id("blob", b"hello world\n") == "3b18e512dba79e4c8300dd08aeb37f8e728b8dad"
    files = {f"d{i}/e{j}/f{k}.txt": f"file {i}{j}{k} {rng.integers(1 << 30)}\n".encode()
             for i in range(3) for j in range(3) for k in range(3)}
    victim = sorted(files)[int(rng.integers(len(files)))]
    edited = dict(files, **{victim: files[victim] + b"one more line\n"})
    c = git.changed_ids(files, edited)
    renamed = c["objects_b"] - c["shared"]
    depth = victim.count("/")
    lab.row("blob ids of '' and 'hello world'", "e69de29b..., 3b18e512...   identical to git's")
    lab.row(f"edit {victim} in a tree of {c['objects_a']} objects", f"{renamed} objects renamed (the blob and {depth + 1} trees above it), {c['shared']} shared")
    assert renamed == depth + 2 and c["root_a"] != c["root_b"], "an edit renames exactly the objects on its path to the root"

    # 2. builds: make's clocks against hashes with early cutoff
    s = build.scenarios(seed=seed)
    rows = {r["edit"].split(" \\")[0]: r for r in s["rows"]}
    for name in ("a comment in one source", "a real change in one header", "every file touched"):
        lab.row(f"rebuild after: {name}", f"make {rows[name]['make']}   hashes {rows[name]['traces']}   of {s['targets']} targets")
    assert all(r["traces"] <= r["make"] for r in s["rows"]), "hashes never rebuild more than timestamps"
    assert rows["a comment in one source"]["make"] == 3 and rows["a comment in one source"]["traces"] == 1, "early cutoff"
    assert rows["every file touched"]["make"] == s["targets"] and rows["every file touched"]["traces"] == 0
    assert rows["a real change in one header"]["traces"] == s["h3_users"] + 2, "a real change reaches its users, the library and the tests"
    b = git.bisect(1_000_000, int(rng.integers(1, 1_000_000)))
    assert b["steps"] <= math.ceil(math.log2(1_000_000)), "bisection is binary search"

    # 3. version solving is satisfiability: installable iff satisfiable, formula by formula
    share, agree, total = [], 0, 0
    assignments = np.array(list(itertools.product((False, True), repeat=N_VARS)))
    for ratio in RATIOS:
        ok = 0
        for _ in range(TRIALS):
            clauses = [[int(v) * int(rng.choice((-1, 1))) for v in rng.choice(np.arange(1, N_VARS + 1), 3, replace=False)]
                       for _ in range(ratio * N_VARS)]
            sat = np.ones(len(assignments), bool)
            for cl in clauses:
                sat &= np.any([assignments[:, abs(l) - 1] == (l > 0) for l in cl], axis=0)
            universe, root = deps.from_3sat(N_VARS, clauses)
            chosen, _, _ = universe.solve(root, seed=seed)
            installable = chosen is not None
            assert installable == bool(sat.any()), "the packages install exactly when the formula is satisfiable"
            assert not installable or deps.check_assignment(clauses, chosen), "and the chosen versions satisfy it"
            agree, total, ok = agree + 1, total + 1, ok + installable
        share.append(ok / TRIALS)
    lab.row(f"{total} random 3-SAT formulas as packages", f"solver and brute force agree on {agree}   bisecting 1,000,000 commits: {b['steps']} tests")
    lab.row("installable share at clause ratios " + ", ".join(map(str, RATIOS)), "   ".join(f"{x:.0%}" for x in share))
    assert share[0] > 0.9 and share[-1] <= 0.2, "few constraints: always installable; many: never"
    lab.note = ("Names that are hashes of content make an edit rename only its path to the root, let a build skip "
                "everything whose inputs hash the same, and leave version choice as the one hard problem: it is "
                "3-SAT in disguise.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    order = ["a comment in one source", "a real change in one source", "a comment in one header",
             "a real change in one header", "every file touched"]
    y = np.arange(len(order))
    ax[0].set_axisbelow(True)
    ax[0].barh(y - 0.2, [rows[k]["make"] for k in order], 0.4, color=labs.RED, label="make: timestamps")
    ax[0].barh(y + 0.2, [rows[k]["traces"] for k in order], 0.4, color=labs.GREEN, label="hashes, with early cutoff")
    for k, name in enumerate(order):
        ax[0].text(rows[name]["make"] + 3, k - 0.2, str(rows[name]["make"]), va="center", color=labs.INK, fontsize=9)
        ax[0].text(rows[name]["traces"] + 3, k + 0.2, str(rows[name]["traces"]), va="center", color=labs.INK, fontsize=9)
    labels = ["comment in\na source", "real change\nin a source", "comment in\na header", "real change\nin a header", "fresh checkout\n(all touched)"]
    ax[0].set(title=f"Targets rebuilt, of {s['targets']}", xlabel="targets rebuilt", yticks=y, yticklabels=labels, xlim=(0, s["targets"] * 1.15))
    ax[0].invert_yaxis()
    ax[0].legend(loc="center right")
    ax[1].plot(RATIOS, share, color=labs.GOLD, marker="o", label="installable (solver) = satisfiable (brute force)")
    ax[1].axvline(4.26, color=labs.MUTED, ls="--", lw=1)
    ax[1].text(4.36, 0.93, "4.26: the threshold\nfor large formulas", color=labs.MUTED, fontsize=9, va="top")
    ax[1].set(title=f"Random 3-SAT with {N_VARS} variables, as packages", xlabel="constraints per variable (clauses / variables)",
              ylabel="share that can be installed", ylim=(-0.05, 1.12))
    ax[1].legend(loc="center right")
    lab.fig = fig
    return lab

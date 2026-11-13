"""Lab 6: flip the diagonal of random tables, count sets built from nothing, and watch Goodstein's ordinals fall while the numbers climb."""

from math import gcd

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import sets as st

TITLE = "The diagonal, sets from nothing, and Goodstein's sequences"
GOAL = ("Check Cantor's theorem on every function from a small set to its power set and on random tables; verify "
        "Ackermann's numbering of the hereditarily finite sets and the sizes of the first stages; then run "
        "Goodstein's sequences and compare the growing numbers with the strictly falling ordinals attached to them.")
TASKS = [
    "Run st.goodstein(3, 20) and st.goodstein(5, 12). The first reaches 0 in five steps; estimate from the ordinals "
    "why the second will not within the lifetime of the universe.",
    "Print st.ackermann_decode(n) with st.show_set for n = 0 ... 20, and find the codes of the von Neumann numbers "
    "0 to 4 (st.von_neumann). What is the pattern?",
    "Compute (w + 1) * 2 and 2 * (w + 1) with st.Ord (w = st.OMEGA) and explain the difference from the "
    "definition of ordinal multiplication.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # Cantor's theorem, exhaustively: no f : X -> P(X) has the diagonal set among its values.
    total = 0
    for n in (1, 2, 3, 4):
        r = st.cantor_check(n)
        total += r["functions"]
        assert r["functions"] == (2 ** n) ** n and r["all_miss"]
    # ... and on random 0/1 tables, where row i is read as the set f(i).
    worst = 10 ** 9
    for _ in range(300):
        n = int(rng.integers(2, 40))
        rows = rng.integers(0, 2, size=(n, n)).tolist()
        d = st.diagonal(rows)
        dist = [sum(a != b for a, b in zip(d, row)) for row in rows]
        worst = min(worst, min(dist))
        assert all(d[i] != rows[i][i] for i in range(n)) and d not in rows
    lab.row("functions X -> P(X) checked, |X| = 1 ... 4", f"{total}   (2 + 16 + 512 + 65,536); none reaches the diagonal set")
    lab.row("300 random tables: least distance of the flipped diagonal from a row", f"{worst}   (never 0)")
    assert total == 2 + 16 + 512 + 65536 and worst >= 1

    # Sets from nothing.
    sizes = [st.V_size(n) for n in range(6)]
    codes_ok = all(st.ackermann_code(st.ackermann_decode(n)) == n for n in range(4096))
    distinct = len({st.ackermann_decode(n) for n in range(4096)})
    lab.row("sizes of the stages V_0 ... V_5", f"{sizes}   (each is 2 to the one before)")
    lab.row("Ackermann's numbering on n < 4096", f"decode then code is the identity: {codes_ok}; {distinct} distinct sets")
    assert sizes == [0, 1, 2, 4, 16, 65536] and all(sizes[k + 1] == 2 ** sizes[k] for k in range(1, 5))
    assert codes_ok and distinct == 4096
    assert all(st.rank(st.ackermann_decode(n)) <= 4 for n in range(16)) and st.transitive(st.von_neumann(5))

    # The fractions counted: the Calkin-Wilf order lists each positive rational once.
    cw = st.calkin_wilf(255)
    assert len(set(cw)) == 255 and all(gcd(a, b) == 1 for a, b in cw)
    assert all((a, b) in set(cw) for a in range(1, 9) for b in range(1, 9) if a + b <= 9 and gcd(a, b) == 1)

    # Ordinal arithmetic, and Goodstein's sequences.
    w, one, two = st.OMEGA, st.ONE, st.Ord.nat(2)
    assert one + w == w and w < w + one and two * w == w and w * two == w + w and w * two > w
    g3 = [t["value"] for t in st.goodstein(3, 20)]
    g4 = st.goodstein(4, 8)
    start = int(rng.integers(5, 16))
    g = st.goodstein(start, 12)
    values = [t["value"] for t in g if t["value"] is not None]
    ords = [t["ordinal"] for t in g]
    lab.row("Goodstein from 3", f"{g3}")
    lab.row("Goodstein from 4", f"{[t['value'] for t in g4]}   (the film's first terms)")
    lab.row(f"Goodstein from {start}: values", "  ".join(f"{v:.3g}" if v > 10 ** 6 else str(v) for v in values[:7]) + "  ...")
    lab.row(f"Goodstein from {start}: ordinals strictly fall", f"{all(b < a for a, b in zip(ords, ords[1:]))} over {len(ords)} terms")
    assert g3 == [3, 3, 3, 2, 1, 0]
    assert [t["value"] for t in g4] == [4, 26, 41, 60, 83, 109, 139, 173]
    assert all(b > a for a, b in zip(values, values[1:])), "the numbers climb"
    assert all(b < a for a, b in zip(ords, ords[1:])), "the ordinals fall, and no ordinal sequence falls forever"
    assert [st.hydra2_steps(k) for k in (1, 2, 3)] == [3, 13, 22539988369405]
    lab.note = ("The flipped diagonal differs from every row, so no list of rows is complete; and a sequence whose "
                "numbers explode still ends, because the ordinals attached to it can only fall finitely often.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    for m, color in ((3, labs.GREEN), (4, labs.BLUE), (start, labs.GOLD)):
        seq = [t["value"] for t in st.goodstein(m, 12) if t["value"] is not None]
        ax[0].plot(range(len(seq)), seq, "o-", color=color, ms=4, label=f"start {m}")
    ax[0].set_yscale("symlog", linthresh=1)
    ax[0].set(title="Goodstein's sequences: the numbers", xlabel="step", ylabel="value (log scale above 1)",
              ylim=(-0.3, None))
    ax[0].legend(loc="upper left")
    qs = np.array([a / b for a, b in cw])
    ax[1].scatter(np.arange(1, 256), qs, s=9, color=labs.BLUE)
    for k in (1, 3, 7, 15, 31, 63, 127):
        ax[1].axvline(k + 0.5, color=labs.GRID, lw=0.8)
    ax[1].set(title="The first 255 fractions in Calkin-Wilf order", xlabel="position in the list",
              ylabel="the fraction (log scale)", yscale="log")
    ax[1].set_yticks([1 / 8, 1 / 4, 1 / 2, 1, 2, 4, 8], ["1/8", "1/4", "1/2", "1", "2", "4", "8"])
    ax[1].minorticks_off()
    lab.fig = fig
    return lab

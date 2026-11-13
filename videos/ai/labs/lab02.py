"""Lab 2: count the leaves minimax and alpha-beta examine on uniform game trees, against Knuth and Moore's formula."""

import numpy as np

from videos.coursekit import labs

TITLE = "Alpha-beta: the same move from far fewer leaves"
GOAL = ("Build uniform game trees with random leaf values, search them with minimax and with alpha-beta under three "
        "move orders (best first, random, worst first), and check that every search returns the same value while "
        "best-first ordering examines exactly b^ceil(d/2) + b^floor(d/2) - 1 leaves.")
TASKS = [
    "Order the moves by a noisy guess of their value (true value plus noise of sd 0.1, 0.3, 1). How good must the "
    "guess be to stay near the best case?",
    "Draw the leaf values from {0, 1} instead of a continuum (a win/loss game). Why can alpha-beta now examine "
    "fewer leaves than the formula?",
    "Add iterative deepening: search to depth 1, 2, ..., d, ordering each level by the previous search's values, "
    "and count the total leaves against one random-order search to depth d.",
]


def minimax_values(leaves, b, d):
    """The minimax value of every node, level by level: values[k] holds the b^k nodes at depth k (root maximizes)."""
    values = [None] * (d + 1)
    values[d] = leaves
    for k in range(d - 1, -1, -1):
        children = values[k + 1].reshape(-1, b)
        values[k] = children.max(axis=1) if k % 2 == 0 else children.min(axis=1)
    return values


def alphabeta(values, b, d, order, rng=None):
    """Alpha-beta from the root; ``order`` is 'best', 'worst' or 'random'.  Returns (value, leaves examined)."""
    count = 0

    def visit(k, i, alpha, beta):
        nonlocal count
        if k == d:
            count += 1
            return values[d][i]
        kids = np.arange(i * b, (i + 1) * b)
        if order == "random":
            kids = rng.permutation(kids)
        else:  # sort by the children's true values: descending is best-first for the maximizer
            kids = kids[np.argsort(values[k + 1][kids])]
            if (order == "best") == (k % 2 == 0):
                kids = kids[::-1]
        if k % 2 == 0:
            best = -np.inf
            for c in kids:
                best = max(best, visit(k + 1, c, alpha, beta))
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
        else:
            best = np.inf
            for c in kids:
                best = min(best, visit(k + 1, c, alpha, beta))
                beta = min(beta, best)
                if alpha >= beta:
                    break
        return best

    return visit(0, 0, -np.inf, np.inf), count


def best_case(b, d):
    return b ** ((d + 1) // 2) + b ** (d // 2) - 1


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    table = {}
    for b, d in ((2, 10), (3, 7), (4, 6), (6, 4)):
        values = minimax_values(rng.random(b ** d), b, d)
        got = {o: alphabeta(values, b, d, o, rng) for o in ("best", "random", "worst")}
        table[(b, d)] = got
        lab.row(f"b = {b}, d = {d}: minimax examines", f"{b ** d} leaves")
        lab.row(f"b = {b}, d = {d}: alpha-beta, best first",
                f"{got['best'][1]}   (formula {best_case(b, d)});  random order {got['random'][1]};  "
                f"worst first {got['worst'][1]}")
        for o, (value, count) in got.items():
            assert value == values[0][0], f"alpha-beta ({o}) must return the minimax value"
        assert got["best"][1] == best_case(b, d), "Knuth and Moore's best case, exactly"
        assert best_case(b, d) < got["random"][1] < b ** d, "random order prunes, but less"
        assert got["random"][1] < got["worst"][1] <= b ** d
    b, depths = 3, np.arange(1, 9)
    curves = {"minimax": [], "worst first": [], "random order": [], "best first": []}
    for d in depths:
        values = minimax_values(rng.random(b ** d), b, d)
        curves["minimax"].append(b ** d)
        curves["worst first"].append(alphabeta(values, b, d, "worst")[1])
        curves["random order"].append(np.mean([alphabeta(values, b, d, "random", rng)[1] for _ in range(5)]))
        curves["best first"].append(alphabeta(values, b, d, "best")[1])
    growth = {k: (v[-1] / v[-3]) ** 0.5 for k, v in curves.items()}  # leaves multiply by this per extra ply
    lab.row("b = 3: growth per ply", "   ".join(f"{k} {g:.2f}" for k, g in growth.items()) + f"   (sqrt 3 = {3 ** 0.5:.2f})")
    assert abs(growth["best first"] - np.sqrt(b)) < 0.05, "best-first ordering searches twice as deep for the same work"
    assert 1.5 * curves["best first"][-1] < curves["random order"][-1] < curves["minimax"][-1] / 1.5
    lab.note = ("Alpha-beta never changes the answer, only the work: with the best move tried first the tree's "
                "effective branching factor falls from b to its square root, so the same work searches twice as "
                "deep; a random order lands in between.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    colors = {"minimax": labs.RED, "worst first": labs.ORANGE, "random order": labs.BLUE, "best first": labs.GREEN}
    for name, ys in curves.items():
        ax[0].plot(depths, ys, "o-", ms=4, color=colors[name], label=name)
    ax[0].plot(depths, [best_case(b, d) for d in depths], "--", color=labs.INK, lw=1,
               label=r"$b^{\lceil d/2\rceil}+b^{\lfloor d/2\rfloor}-1$")
    ax[0].set(title="Leaves examined, branching factor 3", xlabel="depth d (plies)", ylabel="leaves", yscale="log")
    ax[0].legend()
    labels = [f"b={b}, d={d}" for b, d in table]
    x = np.arange(len(table))
    for k, (o, color) in enumerate((("worst", labs.ORANGE), ("random", labs.BLUE), ("best", labs.GREEN))):
        share = [table[key][o][1] / key[0] ** key[1] for key in table]
        ax[1].bar(x + (k - 1) * 0.26, share, 0.26, color=color, label=f"{o} first" if o != "random" else "random order")
    ax[1].set(title="Share of the tree's leaves alpha-beta examines", ylabel="fraction of minimax's leaves", ylim=(0, 1.05))
    ax[1].set_xticks(x, labels)
    ax[1].legend()
    lab.fig = fig
    return lab

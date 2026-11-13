"""Lab 15: a matrix as a memory: fill it with outer products, count the crosstalk, then write with the delta rule."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor

TITLE = "A matrix that remembers: crosstalk, and the delta rule"
GOAL = ("Store N key-value pairs in one matrix by adding outer products, read them back, and compare the error with "
        "the (N - 1)/d the part derives for random keys in d dimensions. Then check with the series' autodiff that "
        "the delta rule is one gradient step on the squared read error, and overwrite facts under three write rules.")
TASKS = [
    "Make the keys exactly orthogonal (np.linalg.qr of a random matrix) for N <= d. What happens to every error?",
    "Run the delta rule with beta = 0.5 and beta = 2 in the overwrite test. Which one forgets the old value?",
    "Sweep the decay alpha from 0.5 to 1 in the overwrite test and find the best value. Why is 1 the worst?",
]

D, DV = 64, 16  # numbers in a key, numbers in a value


def pairs(rng, n):
    K = rng.standard_normal((n, D))
    return K / np.linalg.norm(K, axis=1, keepdims=True), rng.standard_normal((n, DV))


def write(S, k, v, rule, alpha=0.9, beta=1.0):
    """One write into the memory S (values x keys)."""
    if rule == "add":  # linear attention: S + v k^T
        return S + np.outer(v, k)
    if rule == "decay":  # shrink everything first, then add
        return alpha * S + np.outer(v, k)
    return S + beta * np.outer(v - S @ k, k)  # delta: write only the difference from what is read


def read_error(S, K, V):
    """Mean squared read error over the pairs, relative to the size of a value."""
    return np.mean(np.sum((K @ S.T - V) ** 2, axis=1)) / np.mean(np.sum(V ** 2, axis=1))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. adding fills up: the error of reading pair j is the sum of the other values, each times a key overlap
    Ns = np.array([2, 4, 8, 16, 32, 64, 128])
    added, delta = [], []
    for n in Ns:
        ea, ed = [], []
        for _ in range(max(30, 480 // n)):
            K, V = pairs(rng, n)
            Sa = np.zeros((DV, D))
            Sd = np.zeros((DV, D))
            for k, v in zip(K, V):
                Sa, Sd = write(Sa, k, v, "add"), write(Sd, k, v, "delta")
            ea.append(read_error(Sa, K, V))
            ed.append(read_error(Sd, K, V))
        added.append(np.mean(ea))
        delta.append(np.mean(ed))
    added, delta, theory = np.array(added), np.array(delta), (Ns - 1) / D
    for i in (3, 5):
        lab.row(f"adding, {Ns[i]} pairs in {D} dimensions: read error", f"{added[i]:.3f}   (theory (N-1)/d = {theory[i]:.3f})")
    lab.row(f"delta rule, {Ns[5]} pairs in one pass: read error", f"{delta[5]:.3f}")
    assert np.all(np.abs(added / theory - 1) < 0.12), "crosstalk grows like (N - 1)/d"
    assert np.all(delta < 0.75 * added), "writing only the difference leaves less crosstalk (later writes still disturb)"

    # 2. the delta rule is one step of gradient descent on the squared read error, by autodiff
    K, V = pairs(rng, 1)
    k, v, beta = K[0], V[0], 0.7
    S0 = rng.standard_normal((DV, D))
    S = Tensor(S0, requires_grad=True)
    (((S @ k - v) ** 2).sum() * 0.5).backward()
    by_gradient = S0 - beta * S.grad
    by_rule = S0 @ (np.eye(D) - beta * np.outer(k, k)) + beta * np.outer(v, k)
    u = np.linalg.qr(np.column_stack([k, rng.standard_normal(D)]))[0][:, 1]  # a direction at right angles to k
    gap = np.abs(by_gradient - by_rule).max()
    lab.row("gradient step against S(I - beta k k^T) + beta v k^T", f"largest difference {gap:.1e}")
    assert gap < 1e-12, "the delta rule is a gradient step on (1/2)|Sk - v|^2"
    assert np.allclose(by_rule @ k, (1 - beta) * S0 @ k + beta * v), "the answer for k moves a share beta toward v"
    assert np.allclose(by_rule @ u, S0 @ u), "directions at right angles to k are untouched"

    # 3. the world changes: 16 keys, each given a new value four times; then ask for the latest
    M, rounds, err = 16, 4, {"add": [], "decay": [], "delta": []}
    for _ in range(30):
        K, _ = pairs(rng, M)
        mem = {rule: np.zeros((DV, D)) for rule in err}
        for _ in range(rounds):
            V = rng.standard_normal((M, DV))
            for j in rng.permutation(M):
                for rule in err:
                    mem[rule] = write(mem[rule], K[j], V[j], rule)
        for rule in err:
            err[rule].append(read_error(mem[rule], K, V))
    err = {rule: float(np.mean(e)) for rule, e in err.items()}
    lab.row("after 4 rewrites of 16 keys: error on the latest values", f"adding {err['add']:.2f}   decaying {err['decay']:.2f}   delta rule {err['delta']:.2f}")
    lab.note = ("Adding never erases: its error is the crosstalk (N - 1)/d plus every value ever written under the "
                "key. Decay forgets everything a little. The delta rule, one least-squares step per token, replaces "
                "the old value and leaves the directions at right angles to the key alone.")
    assert err["add"] > rounds - 1, "adding answers with every value ever written"
    assert err["delta"] < err["decay"] < err["add"] and err["delta"] < 0.5, "the delta rule corrects"

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].loglog(Ns, added, "o-", color=labs.BLUE, label="adding outer products")
    ax[0].loglog(Ns, theory, "--", color=labs.MUTED, label="theory: (N - 1)/d")
    ax[0].loglog(Ns, delta, "o-", color=labs.GOLD, label="delta rule, one pass")
    ax[0].axvline(D, color=labs.GRID, lw=1.2)
    ax[0].annotate("N = d", (D, added.min()), textcoords="offset points", xytext=(-34, 0), color=labs.MUTED)
    ax[0].set(title=f"Reading back N pairs from a {DV} x {D} matrix", xlabel="pairs stored, N", ylabel="read error / size of a value")
    ax[0].legend(loc="upper left")
    names = ["adding", "decaying (0.9)", "delta rule"]
    bars = ax[1].bar(names, [err["add"], err["decay"], err["delta"]], color=[labs.BLUE, labs.PURPLE, labs.GOLD], width=0.6)
    ax[1].bar_label(bars, fmt="%.2f", color=labs.INK, padding=3)
    ax[1].set_axisbelow(True)
    ax[1].set(title="16 keys rewritten 4 times: error on the latest value", ylabel="read error / size of a value", ylim=(0, err["add"] * 1.15))
    lab.fig = fig
    return lab

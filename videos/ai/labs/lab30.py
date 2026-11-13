"""Lab 30: squeeze five features through two numbers, dense and then sparse, and watch superposition appear."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor

TITLE = "More ideas than dimensions"
GOAL = ("Train chapter 6's toy model, x_hat = ReLU(W^T W x + b) with five features and two hidden numbers, by the series' "
        "autodiff: once with every feature always on and once with each on 5% of the time. Count the features it keeps, "
        "and check how nearly perpendicular random directions are in 2 to 1,024 dimensions.")
TASKS = [
    "Sweep the chance a feature is on over 1, 0.5, 0.3, 0.1, 0.05. At which density does a third feature first get a direction?",
    "Make all five features equally important (importance = 1). Is the sparse solution a regular pentagon now?",
    "Remove the ReLU from the model. Show that it can no longer keep more than two features, however sparse they are.",
]

N, M = 5, 2
IMPORTANCE = 0.9 ** np.arange(N)  # the first feature matters most, as in the film
ROWS, COLS = np.meshgrid(np.arange(M), np.arange(N))  # W[ROWS, COLS] is W transposed, as a node of the graph


def model(W, b, x):
    """x_hat = ReLU(W^T W x + b) for a batch of rows x."""
    return ((Tensor(x) @ W[ROWS, COLS]) @ W + b).relu()


def train(density, rng, steps=2000, batch=256, lr=0.01):
    """Adam on the importance-weighted squared error; returns W (2 x 5), b and the loss curve."""
    W = Tensor(0.3 * rng.standard_normal((M, N)), requires_grad=True)
    b = Tensor(np.zeros(N), requires_grad=True)
    mom, var, losses = [0.0, 0.0], [0.0, 0.0], []
    for t in range(1, steps + 1):
        x = rng.random((batch, N)) * (rng.random((batch, N)) < density)
        W.grad, b.grad = np.zeros((M, N)), np.zeros(N)
        loss = (((model(W, b, x) - x) ** 2) * IMPORTANCE).mean()
        loss.backward()
        losses.append(float(loss.data))
        for k, p in enumerate((W, b)):  # Adam
            mom[k] = 0.9 * mom[k] + 0.1 * p.grad
            var[k] = 0.999 * var[k] + 0.001 * p.grad ** 2
            p.data -= lr * (mom[k] / (1 - 0.9 ** t)) / (np.sqrt(var[k] / (1 - 0.999 ** t)) + 1e-8)
    return W.data, b.data, np.array(losses)


def run(seed=0):
    rng = np.random.default_rng(seed)
    out = {}
    for name, density in (("dense", 1.0), ("sparse", 0.05)):
        W, b, losses = train(density, rng)
        norms = np.linalg.norm(W, axis=0)
        kept = norms > 0.5
        x = rng.random((20_000, N)) * (rng.random((20_000, N)) < density)
        loss = float((((model(Tensor(W), Tensor(b), x).data - x) ** 2) * IMPORTANCE).mean())
        # the best a model with two dedicated directions can do: rebuild features 1 and 2, output the mean of the rest
        rest = x[:, 2:]
        dedicated = float((((rest - rest.mean(0)) ** 2) * IMPORTANCE[2:]).sum(1).mean() / N)
        out[name] = dict(W=W, b=b, norms=norms, kept=kept, loss=loss, dedicated=dedicated, losses=losses, density=density)

    dense, sparse = out["dense"], out["sparse"]
    Wd = dense["W"][:, dense["kept"]]
    cos_dense = abs(Wd[:, 0] @ Wd[:, 1]) / np.prod(np.linalg.norm(Wd, axis=0)) if dense["kept"].sum() == 2 else 1.0
    # one sparse feature on alone: what the other outputs read before and after the bias and the ReLU
    Ws, bs = sparse["W"], sparse["b"]
    k = int(np.argmax(sparse["norms"]))
    raw = Ws.T @ Ws[:, k]
    leak_raw = np.abs(np.delete(raw, k)).max()
    leak_out = np.delete(np.maximum(raw + bs, 0), k).max()

    # random directions: the spread of the cosine is 1 / sqrt(d)
    dims = np.array([2, 16, 128, 1024])
    spread = []
    for d in dims:
        u, v = rng.standard_normal((2, 4000, d))
        spread.append(np.std((u * v).sum(1) / np.linalg.norm(u, axis=1) / np.linalg.norm(v, axis=1)))
    spread = np.array(spread)

    lab = labs.Lab()
    lab.row("always on: features given a direction", f"{dense['kept'].sum()} of {N}   (lengths {'  '.join(f'{v:.2f}' for v in dense['norms'])})")
    lab.row("always on: angle between the two kept", f"cosine {cos_dense:.3f}")
    lab.row("on 5% of the time: features given a direction", f"{sparse['kept'].sum()} of {N}   (lengths {'  '.join(f'{v:.2f}' for v in sparse['norms'])})")
    lab.row("on 5% of the time: loss", f"{sparse['loss']:.5f}   (two dedicated directions: {sparse['dedicated']:.5f})")
    lab.row("one sparse feature on alone: largest reading elsewhere, in size", f"{leak_raw:.2f} before the bias and ReLU, {leak_out:.2f} after")
    lab.row("random directions: spread of the cosine times sqrt(d)", "  ".join(f"d={d}: {s * np.sqrt(d):.2f}" for d, s in zip(dims, spread)))
    lab.note = ("With features always on the network keeps the two most important at right angles and drops the rest; "
                "when they are rare it gives more of them a direction and lets the bias and the ReLU absorb the interference.")

    assert dense["kept"].sum() == 2 and dense["kept"][:2].all(), "dense: the two most important features, nothing else"
    assert cos_dense < 0.1, "and they are perpendicular"
    assert sparse["kept"].sum() >= 4, "sparse: more features than dimensions"
    assert sparse["loss"] < 0.7 * sparse["dedicated"], "superposition beats two dedicated directions when features are rare"
    assert leak_out < 0.5 * leak_raw, "the bias and the ReLU remove most of the interference"
    assert np.all(np.abs(spread * np.sqrt(dims) - 1) < 0.08), "random cosines have spread 1/sqrt(d)"

    fig, ax = labs.figure(2, size=(11, 4.2))
    for name, color in (("dense", labs.BLUE), ("sparse", labs.GOLD)):
        W = out[name]["W"]
        for i in range(N):
            ax[0].annotate("", xy=W[:, i], xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=color, lw=1 + 1.6 * IMPORTANCE[i]))
            if np.linalg.norm(W[:, i]) > 0.3:
                ax[0].text(*(1.12 * W[:, i]), str(i + 1), color=color, ha="center", va="center", fontsize=9)
        ax[0].plot([], [], color=color, label="always on" if name == "dense" else "on 5% of the time")
    ax[0].set(title="Where each feature points in the two hidden numbers", xlim=(-1.6, 1.6), ylim=(-1.45, 1.45), aspect="equal")
    ax[0].legend(loc="lower left")
    ax[1].loglog(dims, spread, "o", color=labs.GOLD, label="measured, 4,000 pairs")
    grid = np.geomspace(2, 1024, 50)
    ax[1].loglog(grid, 1 / np.sqrt(grid), color=labs.MUTED, ls="--", label=r"$1/\sqrt{d}$")
    ax[1].set(title="Random directions are nearly perpendicular", xlabel="dimension d", ylabel="spread of the cosine")
    ax[1].legend()
    lab.fig = fig
    return lab

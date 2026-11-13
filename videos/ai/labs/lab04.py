"""Lab 4: check the series' autodiff against finite differences, and find the V-curve of the gradient check."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor, cross_entropy, log_softmax

TITLE = "The gradient check and its V-curve"
GOAL = ("Build a two-layer network on the series' autodiff library, take its gradient with one backward pass, and "
        "compare directional derivatives with central and forward finite differences for steps from 1e-1 to 1e-12: "
        "the error falls like h squared until round-off, growing like 1/h, takes over.")
TASKS = [
    "Cast the parameters and the data to float32 inside loss_at (np.float32) for the finite differences only. "
    "Where does the V's minimum move, and how deep is it now?",
    "Break the library on purpose: in a copy of Tensor.tanh return g * (1 - t) instead of g * (1 - t * t). "
    "Which numbers in the table expose the bug?",
    "Train the network: repeat p.data -= 0.5 * p.grad for 300 steps (zeroing the gradients each time) and plot "
    "the loss. Then rerun the check at the trained weights.",
]
SIZES = ((6, 8), (8,), (8, 4), (4,))  # W1, b1, W2, b2: 6 inputs, 8 tanh units, 4 classes


def forward(params, x, y, shift=0.0):
    W1, b1, W2, b2 = params
    logits = (x @ W1 + b1).tanh() @ W2 + b2 + shift
    return cross_entropy(logits, y), logits


def loss_at(theta, x, y):
    """The loss as a plain function of one flat parameter vector (no gradients requested)."""
    params, i = [], 0
    for shape in SIZES:
        n = int(np.prod(shape))
        params.append(Tensor(theta[i:i + n].reshape(shape)))
        i += n
    return float(forward(params, Tensor(x), y)[0].data)


def run(seed=0):
    rng = np.random.default_rng(seed)
    x, y = rng.standard_normal((16, 6)), rng.integers(0, 4, 16)
    params = [Tensor(rng.standard_normal(s) * 0.5, requires_grad=True) for s in SIZES]
    logits_in = Tensor(np.zeros((16, 4)), requires_grad=True)  # a zero added to the logits, to read dL/dlogits
    loss, logits = forward(params, Tensor(x), y, shift=logits_in)
    loss.backward()
    theta = np.concatenate([p.data.ravel() for p in params])
    grad = np.concatenate([p.grad.ravel() for p in params])
    lab = labs.Lab()
    lab.row("parameters, loss", f"{theta.size}, {float(loss.data):.4f} nats")

    # Part 1's formula at the logits: (softmax - one-hot) / batch size.
    q = np.exp(log_softmax(Tensor(logits.data)).data)
    formula = (q - np.eye(4)[y]) / len(y)
    lab.row("dL/dlogits: library against (q - y)/n", f"largest difference {np.abs(logits_in.grad - formula).max():.1e}")
    assert np.abs(logits_in.grad - formula).max() < 1e-14

    # Directional derivatives along eight random unit directions.
    hs = 10.0 ** np.arange(-1, -12.01, -0.25)
    dirs = rng.standard_normal((8, theta.size))
    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    central, fwd = np.empty((8, len(hs))), np.empty((8, len(hs)))
    base = loss_at(theta, x, y)
    for i, v in enumerate(dirs):
        exact = grad @ v
        for j, h in enumerate(hs):
            central[i, j] = abs((loss_at(theta + h * v, x, y) - loss_at(theta - h * v, x, y)) / (2 * h) - exact) / abs(exact)
            fwd[i, j] = abs((loss_at(theta + h * v, x, y) - base) / h - exact) / abs(exact)
    c, f = np.median(central, axis=0), np.median(fwd, axis=0)
    c, f = np.maximum(c, 1e-17), np.maximum(f, 1e-17)
    right = (hs <= 1e-2) & (hs >= 1e-3)  # truncation rules here
    left = (hs <= 1e-8) & (hs >= 1e-11)  # round-off rules here
    slope_r = np.polyfit(np.log10(hs[right]), np.log10(c[right]), 1)[0]
    slope_l = np.polyfit(np.log10(hs[left]), np.log10(c[left]), 1)[0]
    slope_f = np.polyfit(np.log10(hs[right]), np.log10(f[right]), 1)[0]
    lab.row("central difference: best step", f"h = {hs[c.argmin()]:.1e}, relative error {c.min():.1e}")
    lab.row("forward difference: best step", f"h = {hs[f.argmin()]:.1e}, relative error {f.min():.1e}")
    lab.row("slopes of the central V", f"{slope_r:+.2f} on the right (theory +2), {slope_l:+.2f} on the left (theory -1)")
    lab.row("slope of the forward error", f"{slope_f:+.2f} on the right (theory +1)")
    lab.note = ("The backward pass agrees with finite differences to about ten digits, and no further: a finite "
                "difference trades truncation error (too large a step) against cancellation (too small a step), so "
                "a gradient check passes at the bottom of the V, not at the smallest step.")
    assert c.min() < 1e-8, "the library's gradient matches central differences"
    assert 1.8 < slope_r < 2.2 and 0.8 < slope_f < 1.2, "truncation: h squared for central, h for forward"
    assert -1.4 < slope_l < -0.6, "round-off grows like 1/h"
    assert 1e-7 < hs[c.argmin()] < 1e-3 and hs[f.argmin()] < hs[c.argmin()], "the minimum sits near eps^(1/3)"
    assert f.min() > 20 * c.min(), "forward differences cannot check as tightly"

    fig, ax = labs.figure(2, size=(11, 4.2))
    for row in central:
        ax[0].loglog(hs, np.maximum(row, 1e-17), color=labs.BLUE, alpha=0.25, lw=1)
    ax[0].loglog(hs, c, color=labs.BLUE, label="central difference (median of 8 directions)")
    ax[0].loglog(hs, f, color=labs.RED, label="forward difference")
    eps = np.finfo(float).eps
    ax[0].loglog(hs, eps / hs, ":", color=labs.MUTED, lw=1, label=r"$\varepsilon/h$, round-off")
    ax[0].loglog(hs, c[right][0] * (hs / hs[right][0]) ** 2, "--", color=labs.MUTED, lw=1, label=r"$\propto h^2$, truncation")
    ax[0].set(title="Finite differences against the backward pass", xlabel="step h", ylabel="relative error",
              ylim=(1e-14, 1e5))
    ax[0].legend(loc="upper left")
    order = np.argsort(np.abs(grad))[::-1][:40]
    fd = np.array([(loss_at(theta + 1e-5 * e, x, y) - loss_at(theta - 1e-5 * e, x, y)) / 2e-5 for e in np.eye(theta.size)[order]])
    ax[1].bar(np.arange(40), grad[order], color=labs.BLUE, label="backward pass")
    ax[1].plot(np.arange(40), fd, "o", ms=3.5, color=labs.GOLD, label="central difference, h = 1e-5")
    ax[1].set(title="The 40 largest partial derivatives, two ways", xlabel="parameter (sorted by size of derivative)",
              ylabel="dL / d parameter")
    ax[1].legend()
    lab.fig = fig
    return lab

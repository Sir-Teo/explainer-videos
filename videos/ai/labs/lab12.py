"""Lab 12: the coordinate check: four Adam steps at growing width, in the standard parametrization and in muP."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor

TITLE = "One learning rate for every width: the coordinate check"
GOAL = ("Train a two-hidden-layer tanh network for four Adam steps at widths 32 to 512, with gradients from the "
        "series' autodiff, and measure how far the output and the hidden coordinates move. With one learning rate for "
        "every width (the standard parametrization) the movement grows with width; with muP's rules it does not.")
TASKS = [
    "Keep muP's learning rates but start the output layer at the standard size (variance 1/n). What moves now?",
    "Replace Adam by plain SGD (step = -lr * gradient). Which muP learning rates must change, and to what power of n?",
    "Shrink every learning rate by n ** -0.5 on top of muP and watch the hidden coordinates: this is the lazy limit.",
]

D_IN, BASE, STEPS, LR, REPEATS = 8, 32, 4, 1e-4, 2
WIDTHS = (32, 64, 128, 256, 512)


def forward(params, X):
    """f(x) = v . tanh(W2 tanh(W1 x)); returns (output, second hidden layer's pre-activations)."""
    W1, W2, v = params
    z2 = (Tensor(X) @ W1).tanh() @ W2
    return z2.tanh() @ v, z2


def moves(n, mup, X, y, rng):
    """Mean absolute change of the output and of a hidden pre-activation after STEPS Adam steps at width n."""
    out_sd = np.sqrt(BASE) / n if mup else 1 / np.sqrt(n)  # muP starts the output layer small; equal at the base width
    params = [Tensor(rng.standard_normal((D_IN, n)) / np.sqrt(D_IN), requires_grad=True),
              Tensor(rng.standard_normal((n, n)) / np.sqrt(n), requires_grad=True),
              Tensor(rng.standard_normal((n, 1)) * out_sd, requires_grad=True)]
    scale = BASE / n if mup else 1.0  # muP: hidden and output learning rates shrink like 1/n
    lrs = [LR, LR * scale, LR * scale]
    m = [np.zeros_like(p.data) for p in params]
    s = [np.zeros_like(p.data) for p in params]
    f0, z0 = (t.data.copy() for t in forward(params, X))
    for t in range(1, STEPS + 1):
        for p in params:
            p.grad = np.zeros_like(p.data)
        out, _ = forward(params, X)
        (((out - y) ** 2).mean() * 0.5).backward()
        for i, p in enumerate(params):  # Adam (Kingma & Ba 2014) with bias correction
            m[i] = 0.9 * m[i] + 0.1 * p.grad
            s[i] = 0.999 * s[i] + 0.001 * p.grad ** 2
            p.data -= lrs[i] * (m[i] / (1 - 0.9 ** t)) / (np.sqrt(s[i] / (1 - 0.999 ** t)) + 1e-12)
    f1, z1 = (t.data for t in forward(params, X))
    return np.abs(f1 - f0).mean(), np.abs(z1 - z0).mean()


def run(seed=0):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((32, D_IN))
    y = np.sin(X[:, :1] * 2) + 0.5 * X[:, 1:2]
    lab = labs.Lab()
    res = {}
    for name, mup in (("standard", False), ("muP", True)):
        both = np.array([np.mean([moves(n, mup, X, y, rng) for _ in range(REPEATS)], axis=0) for n in WIDTHS])
        res[name] = dict(out=both[:, 0], hid=both[:, 1],
                         out_slope=np.polyfit(np.log(WIDTHS), np.log(both[:, 0]), 1)[0],
                         hid_slope=np.polyfit(np.log(WIDTHS), np.log(both[:, 1]), 1)[0])
        r = res[name]
        lab.row(f"{name}: output moves at width 32 / 512", f"{r['out'][0]:.4f} / {r['out'][-1]:.4f}   (slope {r['out_slope']:+.2f} on log axes)")
        lab.row(f"{name}: a hidden coordinate moves", f"{r['hid'][0]:.4f} / {r['hid'][-1]:.4f}   (slope {r['hid_slope']:+.2f})")
    lab.row("theory", "random sums grow like n^0.5, aligned updates like n: slope 0 needs lr ~ 1/n")
    lab.note = ("With one learning rate the update to every coordinate is a sum of n aligned terms and grows with the "
                "width; muP's 1/n learning rates keep each layer's movement the same size at "
                "every width, so a rate tuned on the small model can be reused.")
    sp, mu = res["standard"], res["muP"]
    assert sp["out_slope"] > 0.4 and sp["hid_slope"] > 0.6, "standard parametrization: the update grows with width"
    assert abs(mu["out_slope"]) < 0.25 and abs(mu["hid_slope"]) < 0.25, "muP: flat in width"
    assert sp["out"][-1] > 2.5 * mu["out"][-1], "at the largest width the standard network has moved several times further"
    assert mu["hid"][-1] > 0.6 * mu["hid"][0], "muP's hidden layer still learns (it is not lazy)"

    fig, ax = labs.figure(2, size=(11, 4.2))
    for a, key, title in ((ax[0], "out", "How far the output moves in four Adam steps"),
                          (ax[1], "hid", "How far a hidden coordinate moves")):
        a.loglog(WIDTHS, sp[key], "o-", color=labs.RED, label=f"standard: slope {sp[key + '_slope']:+.2f}")
        a.loglog(WIDTHS, mu[key], "o-", color=labs.GREEN, label=f"muP: slope {mu[key + '_slope']:+.2f}")
        a.set(title=title, xlabel="width n", ylabel="mean absolute change")
        a.set_xticks(WIDTHS, labels=[str(w) for w in WIDTHS])
        a.tick_params(axis="x", which="minor", bottom=False, labelbottom=False)
        a.legend()
    lab.fig = fig
    return lab

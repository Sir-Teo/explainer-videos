"""Lab 23: sum over every CTC alignment by the forward recursion, and check it against brute force and autodiff."""

import itertools

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor, log_softmax

TITLE = "CTC: every alignment at once"
GOAL = ("For random frame-by-frame probabilities over {blank, a, b}, compute p(y | x) by the forward recursion on the "
        "2L + 1 extended states, compare it with a brute-force sum over all 3^T paths, and check that the gradient the "
        "series' autodiff sends back to the logits is the lattice's posterior occupancy minus the softmax.")
TASKS = [
    "Set T = 2 and ask for 'aa'. What does the recursion return, and which missing path explains it?",
    "Replace the sum in the recursion by a maximum (Viterbi) and compare the best path's share of p(y | x) before and after training the logits.",
    "Take 200 gradient steps on the logits for 'ab' with T = 12 and plot where the blanks end up.",
]

BLANK = 0
NAMES = "-ab"


def collapse(path):
    """CTC's map B: merge repeats, then drop blanks."""
    out, prev = [], None
    for k in path:
        if k != prev and k != BLANK:
            out.append(k)
        prev = k
    return tuple(out)


def extended(y):
    ext = [BLANK]
    for k in y:
        ext += [k, BLANK]
    return ext


def forward(logp, y):
    """p(y | x) as a Tensor, and the forward variables alpha (T x (2L+1)), from log-probabilities (T x K)."""
    ext, T = extended(y), logp.data.shape[0]
    p, zero = logp.exp(), Tensor(0.0)
    alpha = [[p[0, ext[s]] if s < 2 else zero for s in range(len(ext))]]
    for t in range(1, T):
        row = []
        for s in range(len(ext)):
            reach = alpha[-1][s] + (alpha[-1][s - 1] if s >= 1 else zero)
            if s >= 2 and ext[s] != BLANK and ext[s] != ext[s - 2]:
                reach = reach + alpha[-1][s - 2]  # skip the blank, unless it separates a repeated letter
            row.append(reach * p[t, ext[s]])
        alpha.append(row)
    total = alpha[-1][-1] + alpha[-1][-2]
    return total, np.array([[float(a.data) for a in row] for row in alpha])


def backward_vars(prob, y):
    ext = extended(y)
    T, S = prob.shape[0], len(ext)
    beta = np.zeros((T, S))
    beta[-1, -1] = beta[-1, -2] = 1.0
    for t in range(T - 2, -1, -1):
        for s in range(S):
            b = beta[t + 1, s] * prob[t + 1, ext[s]]
            if s + 1 < S:
                b += beta[t + 1, s + 1] * prob[t + 1, ext[s + 1]]
            if s + 2 < S and ext[s + 2] != BLANK and ext[s + 2] != ext[s]:
                b += beta[t + 1, s + 2] * prob[t + 1, ext[s + 2]]
            beta[t, s] = b
    return beta


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    T, K = 6, 3
    logits = Tensor(rng.standard_normal((T, K)), requires_grad=True)
    prob = np.exp(log_softmax(logits).data)
    paths = list(itertools.product(range(K), repeat=T))
    weight = np.array([np.prod(prob[np.arange(T), list(pth)]) for pth in paths])
    labels = [collapse(pth) for pth in paths]

    worst = 0.0
    for y in [(1, 2), (1, 1), (2, 1, 2), (1,)]:
        brute = weight[[lab_ == y for lab_ in labels]].sum()
        fwd = float(forward(log_softmax(logits), y)[0].data)
        worst = max(worst, abs(brute - fwd))
        lab.row(f"p('{''.join(NAMES[k] for k in y)}' | x): brute force over {len(paths)} paths", f"{brute:.6f}   forward recursion {fwd:.6f}")
    assert worst < 1e-12, "the recursion is the sum over paths"
    assert abs(weight.sum() - 1) < 1e-12

    # counting: with every probability 1 the recursion counts the paths (Problem 5: five paths for 'ab' at T = 3)
    count = round(float(forward(Tensor(np.zeros((3, K))), (1, 2))[0].data))
    count_aa = round(float(forward(Tensor(np.zeros((2, K))), (1, 1))[0].data))
    lab.row("paths of 3 frames that collapse to 'ab'", f"{count}   (aab, abb, -ab, a-b, ab-)")
    lab.row("paths of 2 frames that collapse to 'aa'", f"{count_aa}   (a repeated letter needs a blank between)")
    assert count == 5 and count_aa == 0

    # the gradient: d log p(y|x) / d logit[t, k] = occupancy of symbol k at frame t - softmax[t, k]
    y = (1, 2)
    total, alpha = forward(log_softmax(logits), y)
    logp = total.log()
    logp.backward()
    beta, ext = backward_vars(prob, y), extended(y)
    gamma = alpha * beta / np.exp(float(logp.data))  # the posterior over extended states, frame by frame
    occ = np.zeros((T, K))
    for s, k in enumerate(ext):
        occ[:, k] += gamma[:, s]
    grad_gap = np.abs(logits.grad - (occ - prob)).max()
    lab.row("gradient: autodiff against occupancy - softmax", f"largest difference {grad_gap:.1e}")
    assert np.allclose(gamma.sum(1), 1) and grad_gap < 1e-10, "the CTC gradient is occupancy minus softmax"

    # gradient ascent on the logits: the model learns an alignment nobody gave it
    history = [float(np.exp(logp.data))]
    for _ in range(60):
        logits.data += 1.0 * logits.grad
        logits.grad[:] = 0
        total, alpha = forward(log_softmax(logits), y)
        logp = total.log()
        logp.backward()
        history.append(float(np.exp(logp.data)))
    prob2 = np.exp(log_softmax(logits).data)
    gamma2 = alpha * backward_vars(prob2, y) / history[-1]
    best = "".join(NAMES[k] for k in prob2.argmax(1))
    lab.row("p('ab' | x) before and after 60 steps on the logits", f"{history[0]:.4f} to {history[-1]:.4f}   best path '{best}'")
    lab.note = ("The forward recursion adds up every alignment in T(2L + 1) steps instead of 3^T, and its gradient "
                "tells each frame which symbol it should have voted for: the alignment is learned, never labelled.")
    assert all(b > a - 1e-12 for a, b in zip(history, history[1:])) and history[-1] > 0.9, "ascent raises p(y | x)"
    assert collapse(prob2.argmax(1)) == y, "the best path collapses to the label"

    fig, ax = labs.figure(2, size=(11, 4.2))
    for a, g, title in ((ax[0], gamma, "Posterior over the lattice, random logits"), (ax[1], gamma2, "After 60 gradient steps")):
        im = a.imshow(g.T, origin="lower", aspect="auto", cmap="magma", vmin=0, vmax=1)
        a.set_yticks(range(len(ext)), [("blank" if k == BLANK else NAMES[k]) for k in ext])
        a.set_xticks(range(T), [str(t + 1) for t in range(T)])
        a.set(title=title, xlabel="frame", ylabel="extended state of 'ab'")
        a.grid(False)
        for t in range(T):
            for s in range(len(ext)):
                if g[t, s] > 0.005:
                    a.text(t, s, f"{g[t, s]:.2f}", ha="center", va="center", fontsize=8, color=labs.INK if g[t, s] < 0.8 else labs.BG)
    fig.colorbar(im, ax=ax[1], label="probability of being in the state")
    lab.fig = fig
    return lab

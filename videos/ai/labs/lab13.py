"""Lab 13: train one layer of linear attention to learn inside the prompt, and compare it with a gradient step."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor

TITLE = "Learning inside the prompt: attention against one gradient step"
GOAL = ("Each prompt holds 16 examples (x, y) of its own hidden linear rule and a question. Train a one-layer, "
        "softmax-free attention on such prompts with the series' autodiff, then compare its answers and its learned "
        "matrices with one step of gradient descent on the prompt's examples.")
TASKS = [
    "Change the number of examples N from 16 to 4 and to 64. How do the learned step size and the error move?",
    "Add noise to the answers (y += 0.5 * rng.standard_normal) and retrain. Does the layer learn a smaller step?",
    "Give x unequal scales (multiply its first coordinate by 3). Is the learned x block still a multiple of I?",
]

D, N = 4, 16  # numbers per x, examples per prompt


def prompts(rng, B):
    """B prompts: G[b] = (1/N) sum_i z_i z_i^T over the example tokens z_i = (x_i, y_i); the question token
    z_q = (x_q, 0); the true answer w . x_q; and the examples themselves."""
    X = rng.standard_normal((B, N, D))
    w = rng.standard_normal((B, D))
    y = np.einsum("bnd,bd->bn", X, w)
    Z = np.concatenate([X, y[:, :, None]], axis=2)
    xq = rng.standard_normal((B, D))
    zq = np.concatenate([xq, np.zeros((B, 1))], axis=1)
    return np.einsum("bnj,bnk->bjk", Z, Z) / N, zq, np.einsum("bd,bd->b", w, xq), (X, y, xq)


def attention(P, Q, G, zq):
    """Linear attention's answer at the question: (1/N) sum_i (P . z_i) (z_i^T Q z_q).  Keys and queries are
    compared through Q; P reads the value that each example passes on."""
    read = (Tensor(G) * P).sum(axis=1)  # for each prompt: sum_i (P . z_i) z_i^T / N
    return ((read @ Q) * Tensor(zq)).sum(axis=1)


def gd_step(X, y, xq, eta):
    """The prediction after one gradient step from w = 0 on L(w) = (1/2N) sum_i (w . x_i - y_i)^2, by autodiff."""
    w = Tensor(np.zeros(D), requires_grad=True)
    (((Tensor(X) @ w - y) ** 2).sum() * (0.5 / len(y))).backward()
    return float((w.data - eta * w.grad) @ xq)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    eta_star = N / (N + D + 1)  # the step that minimizes the expected error for Gaussian x: E[S^2] = (N + D + 1)/N I

    # the algebra first: a gradient step is linear attention with keys x_i, query x_q and values (eta/N) y_i
    _, _, _, (X, y, xq) = prompts(rng, 1)
    by_gd = gd_step(X[0], y[0], xq[0], eta_star)
    by_attention = eta_star / N * float(np.sum(y[0] * (X[0] @ xq[0])))
    lab.row("one prompt: gradient step / attention form", f"{by_gd:+.6f} / {by_attention:+.6f}")
    assert abs(by_gd - by_attention) < 1e-10, "one gradient step from zero is linear attention"

    P = Tensor(0.1 * rng.standard_normal((1, D + 1, 1)), requires_grad=True)
    Q = Tensor(0.1 * rng.standard_normal((D + 1, D + 1)), requires_grad=True)
    params, m, v, curve = [P, Q], [0.0, 0.0], [0.0, 0.0], []
    for t in range(1, 1501):  # Adam on fresh prompts every step
        G, zq, target, _ = prompts(rng, 256)
        for p in params:
            p.grad = np.zeros_like(p.data)
        loss = ((attention(P, Q, G, zq) - target) ** 2).mean()
        loss.backward()
        curve.append(float(loss.data))
        for i, p in enumerate(params):
            m[i] = 0.9 * m[i] + 0.1 * p.grad
            v[i] = 0.999 * v[i] + 0.001 * p.grad ** 2
            p.data -= 0.02 * (m[i] / (1 - 0.9 ** t)) / (np.sqrt(v[i] / (1 - 0.999 ** t)) + 1e-9)

    G, zq, target, (X, y, xq) = prompts(rng, 4000)
    answer = attention(P, Q, G, zq).data
    step = eta_star / N * np.einsum("bn,bnd,bd->b", y, X, xq)  # one gradient step, on every test prompt
    mse, mse_step = np.mean((answer - target) ** 2), np.mean((step - target) ** 2)
    corr = np.corrcoef(answer, step)[0, 1]
    p, q = P.data[0, :, 0], Q.data
    M = p[D] * q[:D, :D] + np.outer(p[:D], q[D, :D])  # what multiplies w^T S ... x_q in the layer's answer
    off = np.linalg.norm(M - eta_star * np.eye(D)) / np.linalg.norm(eta_star * np.eye(D))
    lab.row("error before training / after", f"{curve[0]:.2f} / {mse:.3f}   (answering 0 costs {D}.00)")
    lab.row("error of one gradient step", f"{mse_step:.3f}   (theory {D * (1 - eta_star):.3f})")
    lab.row("correlation of the two answers", f"{corr:.4f}   on 4,000 new prompts")
    lab.row("learned step size (mean diagonal of the x block)", f"{np.trace(M) / D:.3f}   (best step N/(N+d+1) = {eta_star:.3f})")
    lab.row("distance of the x block from a multiple of I", f"{off:.3f}")
    lab.note = ("Nothing told the layer about gradient descent, yet training on prompts alone drives it to an identity "
                "block that compares x's and one entry that passes on the y's: the same map as one least-squares step.")
    assert abs(mse_step - D * (1 - eta_star)) < 0.12, "the gradient step's error matches d (1 - eta*)"
    assert abs(mse - mse_step) < 0.1 * mse_step, "the trained layer is as good as the best single gradient step"
    assert corr > 0.97, "and gives nearly the same answers"
    assert off < 0.2, "its matrices have the gradient step's block structure"

    fig, ax = labs.figure(2, size=(11, 4.4))
    shown = p[D] * q
    lim = np.abs(shown).max()
    im = ax[0].imshow(shown, cmap="RdBu", vmin=-lim, vmax=lim)
    names = [f"x{i + 1}" for i in range(D)] + ["y"]
    ax[0].set_xticks(range(D + 1), names)
    ax[0].set_yticks(range(D + 1), names)
    ax[0].grid(False)
    ax[0].set(title="The learned query-key matrix (blue positive)", xlabel="question's coordinate", ylabel="example's coordinate")
    fig.colorbar(im, ax=ax[0], shrink=0.8)
    ax[1].scatter(step[:400], answer[:400], s=8, color=labs.BLUE, alpha=0.7, label=f"400 prompts, correlation {corr:.3f}")
    r = np.abs(step[:400]).max()
    ax[1].plot([-r, r], [-r, r], color=labs.GOLD, lw=1.2, label="equal answers")
    ax[1].set(title="Trained attention against one gradient step", xlabel="answer of one gradient step", ylabel="answer of the attention layer")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab

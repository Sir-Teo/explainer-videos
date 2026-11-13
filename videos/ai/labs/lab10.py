"""Lab 10: backpropagate through time in a recurrent network and watch the gradient vanish or explode with the spectral radius."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor

TITLE = "Vanishing and exploding gradients through time"
GOAL = ("Run a tanh recurrent network for 60 steps, get the gradient of a final-state loss at every earlier step from the "
        "series' autodiff, and check it against the product of Jacobians and the bound sigma_max(W)^(T-k), at four spectral radii.")
TASKS = [
    "Clip the gradient at each step back to norm 1 at radius 1.5. What happens to the direction of the gradient at step 0?",
    "Make W orthogonal (the Q of a QR factorization). What do the linear and the tanh gradient norms do now?",
    "Add a forget gate: c_t = f c_(t-1) + (1 - f) tanh(...). Find the f that gives the cell path a half-life of 30 steps.",
]


def gradients(W, U, xs, v, linear=False):
    """dL/dh_k for k = 0..T, with L = v . h_T, by autodiff: a zero 'probe' is added to every state, and its gradient
    is the gradient at that state."""
    T, n = len(xs), len(v)
    probes = [Tensor(np.zeros(n), requires_grad=True) for _ in range(T + 1)]
    h, states = probes[0], []
    for t in range(T):
        a = Tensor(W) @ h + U @ xs[t]
        h = (a if linear else a.tanh()) + probes[t + 1]
        states.append(h.data.copy())
    (h * v).sum().backward()
    return np.array([p.grad for p in probes]), states


def by_hand(W, states, v):
    """The same gradients from the chapter's product: dL/dh_(k-1) = W' (tanh'(a_k) (.) dL/dh_k)."""
    g, out = v.copy(), [v.copy()]
    for h in reversed(states):
        g = W.T @ ((1 - h ** 2) * g)
        out.append(g.copy())
    return np.array(out[::-1])


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, T = 32, 60
    G = rng.standard_normal((n, n)) / np.sqrt(n)
    G /= np.abs(np.linalg.eigvals(G)).max()  # spectral radius 1
    U, xs, v = rng.standard_normal((n, 4)) / 2, 0.3 * rng.standard_normal((T, 4)), rng.standard_normal(n)
    v /= np.linalg.norm(v)
    radii, steps_back = (0.5, 0.9, 1.1, 1.5), np.arange(T + 1)[::-1]  # steps back from the loss: T at h_0, 0 at h_T
    lab, out, worst_hand, worst_bound = labs.Lab(), {}, 0.0, -np.inf
    for rho in radii:
        W = rho * G
        smax = np.sqrt(np.linalg.eigvalsh(W.T @ W)[-1])
        g_tanh, states = gradients(W, U, xs, v)
        g_lin, _ = gradients(W, U, xs, v, linear=True)
        worst_hand = max(worst_hand, np.abs(g_tanh - by_hand(W, states, v)).max() / np.abs(g_tanh).max())
        nt, nl = np.linalg.norm(g_tanh, axis=1), np.linalg.norm(g_lin, axis=1)
        worst_bound = max(worst_bound, np.max(np.log(nt) - steps_back * np.log(smax)))  # log of norm / bound, at most 0
        slope = np.polyfit(steps_back[:T // 2], np.log(nl[:T // 2]), 1)[0]  # the far half: the transient has died out
        out[rho] = dict(tanh=nt, lin=nl, smax=smax, slope=slope)
        lab.row(f"radius {rho}: gradient at step 0 / at step {T}", f"tanh {nt[0]:.1e}   linear {nl[0]:.1e}   bound {smax ** T:.1e}")
        lab.row(f"radius {rho}: linear network's factor per step", f"{np.exp(slope):.3f}   (spectral radius {rho})")
    half = np.log(2) / -np.log(0.99)
    lab.row("LSTM cell path, forget gate 0.99: half-life", f"{half:.1f} steps   (0.99^69 = {0.99 ** 69:.3f})")
    lab.note = ("Each step back multiplies the gradient by W' and by tanh' (at most 1): below radius 1 it vanishes "
                "exponentially, above 1 the linear network explodes, and the bound sigma_max^(T-k) always holds.")

    assert worst_hand < 1e-10, "autodiff agrees with the product of Jacobians"
    assert worst_bound < 1e-9, "the norm never exceeds sigma_max(W)^(T-k)"
    for rho in radii:
        assert abs(out[rho]["slope"] - np.log(rho)) < 0.12, "a linear network's gradient changes by the spectral radius per step"
        assert out[rho]["tanh"][0] <= out[rho]["smax"] ** T
    assert out[0.5]["tanh"][0] < 1e-8 and out[0.9]["tanh"][0] < 0.2, "below radius 1 the gradient vanishes"
    assert out[1.5]["lin"][0] > 1e6, "above radius 1 the linear network's gradient explodes"
    assert abs(0.99 ** half - 0.5) < 1e-12

    fig, ax = labs.figure(2, size=(11, 4.2))
    for rho, color in zip(radii, (labs.BLUE, labs.TEAL, labs.GOLD, labs.RED)):
        ax[0].semilogy(steps_back, out[rho]["tanh"], color=color, label=f"radius {rho}")
        ax[0].semilogy(steps_back, out[rho]["lin"], color=color, ls="--", lw=1.1)
    ax[0].plot([], [], color=labs.MUTED, label="solid: tanh,  dashed: linear")
    ax[0].set(title="Gradient norm against steps back in time", xlabel="steps back from the loss (T - k)", ylabel="norm of dL/dh_k",
              ylim=(1e-20, 1e12))
    ax[0].legend(loc="lower left", ncol=2)
    r = out[1.1]
    ax[1].semilogy(steps_back, r["smax"] ** steps_back, color=labs.MUTED, ls=":", label=f"the bound, sigma_max = {r['smax']:.2f}")
    ax[1].semilogy(steps_back, r["lin"], color=labs.GOLD, ls="--", label="linear network")
    ax[1].semilogy(steps_back, r["tanh"], color=labs.GOLD, label="tanh network")
    ax[1].semilogy(steps_back, 0.99 ** steps_back, color=labs.GREEN, label="LSTM cell path, forget gate 0.99")
    ax[1].set(title="Radius 1.1: the bound, and a path that does not decay", xlabel="steps back from the loss (T - k)", ylabel="norm, or factor")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab

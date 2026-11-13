"""Lab 25: turn a molecule under an invariant energy, fool message passing with two graphs, and over-smooth a third."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor

TITLE = "Symmetry, checked three ways"
GOAL = ("Differentiate an energy built on distances with the series' autodiff and check that its force turns with the "
        "molecule while a network on raw coordinates does not; run colour refinement and a sum-aggregating network on "
        "the triangular prism and K3,3; and measure how fast repeated averaging erases node features.")
TASKS = [
    "Replace the rotation by a reflection (flip one axis). Does the distance energy change? What would it take to tell a molecule from its mirror image?",
    "Give the nodes of the prism and of K3,3 random features instead of constant ones and rerun the sum network. What have you traded away?",
    "Raise the number of edges between the communities (p_out = 0.1) and watch lambda_2 and the number of layers before the features are gone.",
]


def rotation(rng):
    q, r = np.linalg.qr(rng.standard_normal((3, 3)))
    q = q * np.sign(np.diag(r))
    return q if np.linalg.det(q) > 0 else q[:, ::-1]


def energy_and_force(x, w, pairs_only=True):
    """E and F = -dE/dx for a small tanh network, on squared distances (invariant) or on raw coordinates."""
    xt = Tensor(x, requires_grad=True)
    if pairs_only:
        i, j = np.triu_indices(len(x), 1)
        d = xt[i] - xt[j]
        feat = (d * d).sum(axis=1, keepdims=True)  # |x_i - x_j|^2, one row per pair
    else:
        feat = xt
    e = (((feat @ w[0] + w[1]).tanh() @ w[2]).tanh()).sum()
    e.backward()
    return float(e.data), -xt.grad


def refine(A, rounds=6):
    """1-WL colour refinement: the sorted histogram of colours after each round, hashable across graphs."""
    colours = [0] * len(A)
    for _ in range(rounds):
        sig = [(colours[v], tuple(sorted(colours[u] for u in np.flatnonzero(A[v])))) for v in range(len(A))]
        colours = [hash(s) for s in sig]
    return sorted(colours)


def sum_network(A, weights):
    """A message-passing network with sum aggregation and a sum read-out, from the same feature on every node."""
    h = np.ones((len(A), 1))
    for W in weights:
        h = np.tanh((h + A @ h) @ W)
    return h.sum(0)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. five particles, turned and shifted
    x = rng.standard_normal((5, 3))
    R, t = rotation(rng), rng.standard_normal(3)
    w_inv = [0.2 * rng.standard_normal((1, 8)), rng.standard_normal(8), 0.4 * rng.standard_normal((8, 1))]
    w_raw = [0.5 * rng.standard_normal((3, 8)), rng.standard_normal(8), 0.4 * rng.standard_normal((8, 1))]
    out = {}
    for name, w, pairs in (("distances", w_inv, True), ("raw coordinates", w_raw, False)):
        e0, f0 = energy_and_force(x, w, pairs)
        e1, f1 = energy_and_force(x @ R.T + t, w, pairs)
        out[name] = (abs(e1 - e0), np.abs(f1 - f0 @ R.T).max(), np.abs(f0.sum(0)).max(), np.abs(f0).max())
        lab.row(f"energy on {name}: |E(Rx + t) - E(x)|", f"{out[name][0]:.1e}   force error |F(Rx + t) - R F(x)| {out[name][1]:.1e}")
    assert out["distances"][0] < 1e-10 and out["distances"][1] < 1e-10, "invariant energy, equivariant force"
    assert out["distances"][2] < 1e-10 < 1e-3 < out["distances"][3], "and the (non-zero) forces sum to zero"
    assert out["raw coordinates"][0] > 1e-3 and out["raw coordinates"][1] > 1e-3, "a network on coordinates has neither"
    angles = np.linspace(0, 2 * np.pi, 121)
    turn = lambda a: np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    sweep = {name: [energy_and_force(x @ turn(a).T, w, pairs)[0] for a in angles]
             for name, w, pairs in (("distances", w_inv, True), ("raw coordinates", w_raw, False))}

    # 2. the triangular prism and K3,3: both 3-regular on six nodes
    prism = np.zeros((6, 6), int)
    for a, b in [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (0, 3), (1, 4), (2, 5)]:
        prism[a, b] = prism[b, a] = 1
    k33 = np.zeros((6, 6), int)
    k33[:3, 3:] = k33[3:, :3] = 1
    tri = [int(np.trace(np.linalg.matrix_power(A, 3)) // 6) for A in (prism, k33)]
    weights = [rng.standard_normal((1, 6)), rng.standard_normal((6, 6)), rng.standard_normal((6, 6)), rng.standard_normal((6, 4))]
    gap = np.abs(sum_network(prism, weights) - sum_network(k33, weights)).max()
    separated = 0
    for _ in range(200):  # random graphs are another matter
        g1, g2 = (np.triu(rng.random((10, 10)) < 0.5, 1) for _ in range(2))
        separated += refine(g1 + g1.T) != refine(g2 + g2.T)
    lab.row("triangles in the prism and in K3,3", f"{tri[0]} and {tri[1]}")
    lab.row("1-WL colour histograms equal; sum network's outputs differ by", f"{refine(prism) == refine(k33)}; {gap:.1e}")
    lab.row("random 10-node pairs that 1-WL separates", f"{separated} of 200")
    assert tri == [2, 0] and refine(prism) == refine(k33), "1-WL cannot see the triangles"
    assert gap < 1e-12, "so no message-passing network can"
    assert separated >= 195, "though it separates almost all random graphs"

    # 3. over-smoothing on three communities
    n, sizes = 60, 20
    y = np.repeat(np.arange(3), sizes)
    P = np.where(y[:, None] == y[None, :], 0.3, 0.02)
    A = np.triu(rng.random((n, n)) < P, 1)
    A = (A + A.T).astype(float)
    ring = np.arange(n)
    A[ring, (ring + 1) % n] = A[(ring + 1) % n, ring] = 1  # a ring through every node keeps the graph connected
    M = A + np.eye(n)
    d = M.sum(1)
    Ahat = M / np.sqrt(np.outer(d, d))
    lam = np.sort(np.linalg.eigvalsh(Ahat))[::-1]
    lam2 = max(abs(lam[1]), abs(lam[-1]))
    H = np.eye(3)[y] + 0.5 * rng.standard_normal((n, 3))
    H0 = H.copy()
    dirichlet = lambda h: float(np.trace(h.T @ (np.eye(n) - Ahat) @ h))  # zero only when h is proportional to sqrt(deg)
    energies = [dirichlet(H)]
    for _ in range(64):
        H = Ahat @ H
        energies.append(dirichlet(H))
    energies = np.array(energies)
    rate = (energies[60] / energies[40]) ** (1 / 20)
    u1 = np.sqrt(d) / np.linalg.norm(np.sqrt(d))
    left = np.linalg.norm(H - np.outer(u1, u1 @ H)) / np.linalg.norm(H0)
    lab.row("averaging matrix: top eigenvalues", f"{lam[0]:.4f}, {lam[1]:.4f}, {lam[2]:.4f}")
    lab.row("Dirichlet energy: factor per layer, layers 40 to 60", f"{rate:.4f}   (lambda_2 squared = {lam2 ** 2:.4f})")
    lab.row("after 64 layers: what is left off sqrt(degree), over |H|", f"{left:.1e}   (bound lambda_2^64 = {lam2 ** 64:.1e})")
    lab.note = ("A symmetry that is built in holds to rounding error for any weights, trained or not; the same structure "
                "sets the limits: message passing sees what colour refinement sees, and averaging forgets at the rate "
                "of the second eigenvalue.")
    assert abs(lam[0] - 1) < 1e-10 and lam2 < 1, "a connected graph: one eigenvalue at 1"
    assert lam2 ** 2 - 0.03 < rate <= lam2 ** 2 + 1e-9, "the energy decays like lambda_2^(2k)"
    assert left <= lam2 ** 64 * (1 + 1e-9), "and the features collapse onto sqrt(degree)"

    fig, ax = labs.figure(2, size=(11, 4.2))
    deg = np.degrees(angles)
    ax[0].plot(deg, sweep["raw coordinates"], color=labs.RED, label="network on raw coordinates")
    ax[0].plot(deg, sweep["distances"], color=labs.GREEN, label="network on distances")
    ax[0].set(title="Turn the molecule: the predicted energy", xlabel="angle of the turn (degrees)", ylabel="energy")
    ax[0].set_xticks([0, 90, 180, 270, 360])
    ax[0].legend()
    k = np.arange(65)
    ax[1].semilogy(k, energies / energies[0], color=labs.BLUE, label="Dirichlet energy of the features")
    ax[1].semilogy(k, energies[40] / energies[0] * lam2 ** (2.0 * (k - 40)), color=labs.GOLD, ls="--", label="slope of lambda_2^(2k)")
    ax[1].set(title="Over-smoothing: energy against depth", xlabel="rounds of averaging k", ylabel="share of the starting energy")
    ax[1].legend()
    lab.fig = fig
    return lab

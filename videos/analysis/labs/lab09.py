"""Lab 9: differentiate the sawtooth's Fourier series term by term, and test it as a distribution."""

import numpy as np

from videos.coursekit import labs

TITLE = "A divergent series that converges as a distribution"
GOAL = ("The sawtooth sum sin(nx)/n has derivative -1/2 + pi*delta near 0. Differentiate the series term by term, "
        "pair the partial sums of cos(nx) with a random smooth test function, and compare with -1/2 int phi + pi phi(0); "
        "then check Plancherel and Poisson summation numerically.")
TASKS = [
    "Differentiate once more: pair -sum n sin(nx) with phi. The limit is the action of pi*delta', which is -pi phi'(0).",
    "Replace the smooth bump by the tent max(0, 1 - |x|/a). How fast does the pairing converge now, and why?",
    "In the Plancherel check, use the box on [-1, 1]: how far out must the frequency grid reach for 3 digits?",
]


def bump(u):
    """The test function exp(-1 / (1 - u^2)) on (-1, 1), 0 outside: smooth, compactly supported."""
    out = np.zeros_like(u)
    inside = np.abs(u) < 1
    out[inside] = np.exp(-1 / (1 - u[inside] ** 2))
    return out


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. A random test function supported in [-a, a], a < 2 pi, so only the jump at 0 is inside its support.
    a, tilt = rng.uniform(1.5, 3.0), rng.uniform(-0.5, 0.5)
    x = np.linspace(-a, a, 40001)
    dx = x[1] - x[0]
    phi = bump(x / a) * (1 + tilt * x) * np.e  # phi(0) = 1
    limit = -0.5 * np.sum(phi) * dx + np.pi * 1.0  # <-1/2 + pi delta, phi>
    Ns = np.arange(1, 201)
    pair_n = np.array([np.sum(np.cos(n * x) * phi) * dx for n in Ns])  # <cos(nx), phi>
    pairing = np.cumsum(pair_n)
    err = np.abs(pairing - limit)
    # pointwise the series has no limit: at x = 1 the partial sums keep oscillating
    pointwise = np.cumsum(np.cos(Ns * 1.0))
    assert err[-1] < 1e-8 and err[59] < 1e-4, "the differentiated series converges to -1/2 + pi delta on test functions"
    assert np.ptp(pointwise[100:]) > 1.5, "but its partial sums at a point never settle"
    # the definition of the derivative: <S', phi> = -<S, phi'>, with S the sawtooth (pi - x)/2 on (0, 2 pi), odd
    saw = np.where(x > 0, (np.pi - x) / 2, np.where(x < 0, (-np.pi - x) / 2, 0.0))
    by_definition = -np.sum(saw * np.gradient(phi, dx)) * dx
    assert abs(by_definition - limit) < 1e-6, "-<sawtooth, phi'> is the same number"
    lab.row("test function", f"bump on [-{a:.3f}, {a:.3f}] times (1 + {tilt:+.3f} x), phi(0) = 1")
    lab.row("-1/2 int phi + pi phi(0)", f"{limit:.10f}")
    lab.row("-<sawtooth, phi'>  (the definition)", f"{by_definition:.10f}")
    lab.row("<sum_{n<=N} cos(nx), phi>, N = 5, 20, 60, 200", "  ".join(f"{pairing[n - 1]:.8f}" for n in (5, 20, 60, 200)))
    lab.row("sum_{n<=N} cos(n) at the point x = 1, same N", "  ".join(f"{pointwise[n - 1]:+.3f}" for n in (5, 20, 60, 200)))

    # 2. Plancherel, in Rudin's convention f^(t) = (2 pi)^(-1/2) int f(x) e^(-ixt) dx: a random wave packet.
    xs = np.linspace(-12, 12, 2401)
    ts = np.linspace(-14, 14, 2801)
    packet = sum(rng.normal() * np.exp(-((xs - rng.uniform(-3, 3)) ** 2) / (2 * rng.uniform(0.5, 1.5) ** 2))
                 * np.cos(rng.uniform(0, 5) * xs) for _ in range(4))
    hat = (np.exp(-1j * np.outer(ts, xs)) @ packet) * (xs[1] - xs[0]) / np.sqrt(2 * np.pi)
    n_x, n_t = np.sum(packet**2) * (xs[1] - xs[0]), np.sum(np.abs(hat) ** 2) * (ts[1] - ts[0])
    assert abs(n_x - n_t) < 1e-8 * n_x, "Plancherel: the transform preserves the L2 norm"
    lab.row("Plancherel: |f|^2 and |f^|^2 for a random packet", f"{n_x:.10f}  {n_t:.10f}")

    # 3. Poisson summation for the Gaussian: Jacobi's identity for the theta function, at random t.
    n = np.arange(-60, 61)
    t = rng.uniform(0.2, 3.0, 5)
    left = np.array([np.sum(np.exp(-np.pi * n**2 * s)) for s in t])
    right = np.array([np.sum(np.exp(-np.pi * n**2 / s)) / np.sqrt(s) for s in t])
    assert np.abs(left / right - 1).max() < 1e-12, "sum e^(-pi n^2 t) = t^(-1/2) sum e^(-pi n^2 / t)"
    lab.row("Jacobi's identity, worst relative gap at 5 random t", f"{np.abs(left / right - 1).max():.1e}")
    lab.note = ("The series sum cos(nx) diverges at every point, yet against a smooth test function its partial sums "
                "converge faster than any power of 1/N to the action of the sawtooth's derivative, -1/2 + pi delta: "
                "term-by-term differentiation is correct in the space of distributions.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    xx = np.linspace(-a, a, 1500)
    ax[0].plot(xx, sum(np.cos(k * xx) for k in range(1, 21)), color=labs.BLUE, lw=1, label="sum of cos(nx), n <= 20")
    ax[0].plot(xx, 8 * bump(xx / a) * (1 + tilt * xx) * np.e, color=labs.GOLD, label="test function phi (8 times)")
    ax[0].axhline(-0.5, color=labs.MUTED, ls="--", lw=1, label="-1/2")
    ax[0].set(title="The differentiated series: a spike at 0 over -1/2", xlabel="x")
    ax[0].legend(loc="upper right")
    ax[1].semilogy(Ns, err + 1e-17, color=labs.GREEN, label="|<partial sum, phi> - limit|")
    ax[1].semilogy(Ns, np.abs(pointwise + 0.5) + 1e-17, color=labs.RED, lw=0.8, alpha=0.8, label="|partial sum at x = 1, plus 1/2|")
    ax[1].set(title="Converges on test functions, not at points", xlabel="terms N", ylim=(1e-16, 30))
    ax[1].legend(loc="lower left")
    lab.fig = fig
    return lab

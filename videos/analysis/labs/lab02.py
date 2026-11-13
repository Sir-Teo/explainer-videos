"""Lab 2: rearrange the alternating harmonic series to any sum, and fail to do it to an absolutely convergent one."""

from math import exp, log, pi

import numpy as np

from videos.coursekit import labs

TITLE = "Riemann's rearrangement theorem, run as an algorithm"
GOAL = ("Reorder 1 - 1/2 + 1/3 - ... by the greedy rule (below the target take a positive term, above it a negative "
        "one), check the overshoot bound and Pringsheim's ratio, then run the same rule on the series with terms 1/k².")
TASKS = [
    "Use two targets: climb above 1, then fall below 0, and repeat. Check that the partial sums have upper limit 1 and lower limit 0.",
    "Take three positive terms for every negative one, in blocks. Predict the sum from Pringsheim's ratio before computing it.",
    "Rearrange the sawtooth series, the sum of sin(k)/k, to the target 3: split its terms by sign first, then run the greedy rule.",
]


def greedy(target, n_terms, p=1.0):
    """The greedy rearrangement of sum (-1)^(k+1) / k^p toward ``target``: partial sums, the count of positive
    terms after each step, and the larger of the last positive and the last negative term used so far."""
    sums, pos, last = np.empty(n_terms), np.empty(n_terms, int), np.empty(n_terms)
    s, i_pos, i_neg, up, down = 0.0, 0, 0, 0.0, 0.0
    for i in range(n_terms):
        if s <= target:
            i_pos += 1
            up = (2 * i_pos - 1) ** -p
            s += up
        else:
            i_neg += 1
            down = (2 * i_neg) ** -p
            s -= down
        sums[i], pos[i], last[i] = s, i_pos, max(up, down)
    return sums, pos, last


def blocks(n_blocks, p, n_pos=2, n_neg=1):
    """The sum of the rearrangement that takes ``n_pos`` positive terms, then ``n_neg`` negative ones, in blocks."""
    odd = (2.0 * np.arange(1, n_pos * n_blocks + 1) - 1) ** -p
    even = (2.0 * np.arange(1, n_neg * n_blocks + 1)) ** -p
    return odd.sum() - even.sum()


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    n = 200_000
    k = np.arange(1, n + 1)
    natural = np.sum((-1.0) ** (k + 1) / k)
    lab.row("natural order, 200,000 terms", f"{natural:.6f}   (ln 2 = {log(2):.6f})")
    assert abs(natural - log(2)) < 1 / n

    targets = [("pi", pi), ("-1", -1.0), ("a random target", float(rng.uniform(-2, 3)))]
    runs = {}
    for name, t in targets:
        sums, pos, last = greedy(t, n)
        runs[name] = (t, sums, pos)
        crossed = np.flatnonzero(np.diff(np.sign(sums - t)) != 0)[0] + 1
        assert np.all(np.abs(sums[crossed:] - t) <= last[crossed:] + 1e-12), "the overshoot is at most the last term used on that side"
        ratio, predicted = pos[-1] / (n - pos[-1]), exp(2 * (t - log(2)))
        lab.row(f"greedy toward {name} = {t:.4f}", f"sum {sums[-1]:.5f}   last terms used at most {last[-1]:.1e}")
        lab.row("  positive per negative terms", f"{ratio:.4f}   (Pringsheim: e^(2(T - ln 2)) = {predicted:.4f})")
        assert abs(sums[-1] - t) < 1e-3 and abs(ratio / predicted - 1) < 0.03

    # A fixed pattern, two positive terms per negative one: the ratio 2 must give T = ln 2 + (1/2) ln 2.
    two_one = blocks(400_000, 1.0)
    lab.row("blocks + + -, terms 1/k", f"{two_one:.5f}   (1.5 ln 2 = {1.5 * log(2):.5f}; natural order ln 2 = {log(2):.5f})")
    assert abs(two_one - 1.5 * log(2)) < 1e-5
    # The same pattern on the absolutely convergent series: the sum does not move.
    absolute = blocks(400_000, 2.0)
    lab.row("blocks + + -, terms 1/k²", f"{absolute:.5f}   (natural order pi²/12 = {pi * pi / 12:.5f})")
    assert abs(absolute - pi * pi / 12) < 1e-5
    # And the greedy rule cannot reach pi: the positive pile is finite (pi²/8), so the walk never takes a negative term.
    sums2, pos2, _ = greedy(pi, 20_000, p=2.0)
    lab.row("greedy toward pi, terms 1/k²", f"stalls at {sums2[-1]:.4f} < pi²/8 = {pi * pi / 8:.4f}; negative terms used: {20_000 - pos2[-1]}")
    assert sums2[-1] < pi * pi / 8 < pi and pos2[-1] == 20_000
    lab.note = ("A conditionally convergent series has two infinite piles, so the greedy walk reaches any target with "
                "an overshoot bounded by the last term; an absolutely convergent one has finite piles and one sum.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    show = 300
    for (name, (t, sums, pos)), color in zip(runs.items(), (labs.GOLD, labs.GREEN, labs.PURPLE)):
        ax[0].plot(np.arange(1, show + 1), sums[:show], color=color, lw=1.2, label=f"toward {name}")
        ax[0].axhline(t, color=color, lw=0.8, ls="--")
        steps = np.arange(1, n + 1)
        ax[1].loglog(steps[9:], (pos[9:] + 0.5) / (steps[9:] - pos[9:] + 0.5), color=color, lw=1.2, label=f"toward {name}")
        ax[1].axhline(exp(2 * (t - log(2))), color=color, lw=0.8, ls="--")
    ax[0].plot(np.arange(1, show + 1), np.cumsum((-1.0) ** (k[:show] + 1) / k[:show]), color=labs.MUTED, lw=1.2,
               label="natural order (ln 2)")
    ax[0].set(title="The same terms, three orders, three sums", xlabel="terms used", ylabel="partial sum", ylim=(-1.4, 5.2))
    ax[0].legend(loc="upper right", ncols=2)
    ax[1].set(title="Positive per negative terms (dashed: Pringsheim's ratio)", xlabel="terms used", ylim=(1e-2, 3e4))
    ax[1].legend(loc="upper right", ncols=3)
    lab.fig = fig
    return lab

"""Lab 42: break paragraphs greedily and by Knuth-Plass, check the dynamic program against every possible set of breaks, and count nested layouts."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import itertools

import numpy as np

from explainer.cs.web import layout as ly
from explainer.cs.web import platform as pf

TITLE = "Greedy against total-fit line breaking, checked by brute force"
GOAL = ("Break random paragraphs with the series' greedy and Knuth-Plass routines, check on short paragraphs that "
        "the dynamic program's badness is the least over all sets of breaks and that greedy uses the fewest lines, "
        "then count the layouts of nested flex containers and check two WCAG contrast ratios.")
TASKS = [
    "Change the cost in the brute-force check from the cube of the shortfall to its square, and count how many of the short paragraphs Knuth-Plass (which uses the cube) no longer breaks optimally.",
    "Narrow the line from 420 to 250 px and compare how often Knuth-Plass uses one line more than greedy. Why can it never use fewer?",
    "Call ly.flex(600, [(300, 1, 1), (300, 1, 3), (200, 0, 1)]) and check by hand that the shrunk sizes sum to 600 and that the third item gives up exactly as much as the first.",
]

LINE, SHORT, SPACE = 420.0, 230.0, 5.0


def badness(lines, widths, line):
    return ly.line_stats(lines, widths, SPACE, line)["badness"]


def every_breaking(widths, line):
    """Every way to cut the words into lines that fit."""
    n = len(widths)
    for mask in itertools.product((0, 1), repeat=n - 1):
        cuts = [0] + [i + 1 for i, m in enumerate(mask) if m] + [n]
        lines = [list(range(a, b)) for a, b in zip(cuts, cuts[1:])]
        if all(sum(widths[a:b]) + SPACE * (b - a - 1) <= line for a, b in zip(cuts, cuts[1:])):
            yield lines


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. short paragraphs on a narrow line: every set of breaks, against the dynamic program and the greedy rule
    ties, tried = 0, 0
    for _ in range(20):
        widths = [float(w) for w in rng.uniform(25, 110, 11)]
        g, k = ly.greedy(None, widths, SPACE, SHORT), ly.knuth_plass(None, widths, SPACE, SHORT)
        allb = list(every_breaking(widths, SHORT))
        tried += len(allb)
        least = min(badness(b, widths, SHORT) for b in allb)
        assert abs(badness(k, widths, SHORT) - least) < 1e-9, "Knuth-Plass finds the least badness"
        assert len(g) == min(len(b) for b in allb), "greedy uses the fewest lines"
        ties += badness(g, widths, SHORT) - least < 1e-9
    lab.row("20 paragraphs of 11 words", f"Knuth-Plass optimal on 20 of 20 ({tried:,} feasible break sets tried); greedy optimal on {ties}")

    # 2. long paragraphs: how much better, and at what price in lines
    ratio, extra, worst_g, worst_k, shown = [], 0, [], [], None
    for _ in range(300):
        widths = [float(w) for w in rng.uniform(15, 95, int(rng.integers(60, 140)))]
        g, k = ly.greedy(None, widths, SPACE, LINE), ly.knuth_plass(None, widths, SPACE, LINE)
        sg, sk = ly.line_stats(g, widths, SPACE, LINE), ly.line_stats(k, widths, SPACE, LINE)
        assert sk["badness"] <= sg["badness"] + 1e-9 and sk["lines"] >= sg["lines"]
        ratio.append(sk["badness"] / sg["badness"])
        extra += sk["lines"] > sg["lines"]
        worst_g.append(sg["max_slack"])
        worst_k.append(sk["max_slack"])
        if shown is None and sk["lines"] == sg["lines"] and sk["badness"] < 0.7 * sg["badness"]:
            shown = (g, k, widths)
    ratio = np.array(ratio)
    assert np.median(ratio) < 0.97 and np.mean(ratio < 1 - 1e-9) > 0.6, "total fit is better on most paragraphs"
    assert np.mean(worst_k) < np.mean(worst_g)
    lab.row("300 long paragraphs: badness, Knuth-Plass / greedy", f"median {np.median(ratio):.2f}; below 1 on {int(np.sum(ratio < 1 - 1e-9))}, never above")
    lab.row("worst line's shortfall, mean", f"greedy {np.mean(worst_g):.1f} px   Knuth-Plass {np.mean(worst_k):.1f} px")
    lab.row("paragraphs where Knuth-Plass takes an extra line", f"{extra} of 300")

    # 3. nested intrinsic sizing: 2^(d+1) - 1 layouts without a cache, 2d + 1 with one
    depths = list(range(1, 17))
    naive = [ly.nested_measure(d, False) for d in depths]
    cached = [ly.nested_measure(d, True) for d in depths]
    assert naive == [2 ** (d + 1) - 1 for d in depths] and cached == [2 * d + 1 for d in depths]
    lab.row("nested flex, depth 16", f"{naive[-1]:,} layouts without a cache (2^17 - 1), {cached[-1]} with one (2d + 1)")

    # 4. flexbox conserves the container, and the contrast ratio's two landmarks
    sizes = ly.flex(600, [(300, 1, 1), (300, 1, 3), (200, 0, 1)])["sizes"]
    assert abs(sum(sizes) - 600) < 1e-9 and abs((300 - sizes[1]) - 3 * (300 - sizes[0])) < 1e-9
    assert abs(pf.contrast("#000000", "#ffffff") - 21) < 1e-9 and pf.grey_threshold() == "#767676"
    assert pf.contrast("#767676", "#ffffff") >= 4.5 > pf.contrast("#777777", "#ffffff")
    lab.row("contrast", f"black on white {pf.contrast('#000000', '#ffffff'):.0f}; lightest passing grey {pf.grey_threshold()} "
                        f"({pf.contrast('#767676', '#ffffff'):.2f}), #777777 fails ({pf.contrast('#777777', '#ffffff'):.2f})")
    lab.note = ("Greedy minimizes the number of lines and nothing else; the dynamic program minimizes the whole "
                "paragraph's badness, and brute force confirms that no set of breaks does better.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    g, k, widths = shown
    for lines, color, name, lw, ms in ((g, labs.RED, "greedy", 4.0, 9), (k, labs.GOLD, "Knuth-Plass", 1.6, 4)):
        short = [LINE - sum(widths[i] for i in ln) - SPACE * (len(ln) - 1) for ln in lines[:-1]]
        ax[0].plot(range(1, len(short) + 1), short, "o-", color=color, lw=lw, ms=ms,
                   label=f"{name}: badness {badness(lines, widths, LINE):.2f}")
    ax[0].xaxis.get_major_locator().set_params(integer=True)
    ax[0].set(title="One paragraph: each line's shortfall", xlabel="line (the last is not counted)",
              ylabel="shortfall (px of 420)", ylim=(0, None))
    ax[0].legend()
    ax[1].semilogy(depths, naive, "o-", color=labs.RED, label="no cache: 2^(d+1) - 1")
    ax[1].semilogy(depths, cached, "o-", color=labs.GREEN, label="cache by (box, width): 2d + 1")
    ax[1].set(title="Layouts of nested flex containers", xlabel="nesting depth d", ylabel="layout calls")
    ax[1].legend()
    lab.fig = fig
    return lab

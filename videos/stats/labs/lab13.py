"""Lab 13: lay four varieties out on a field with a fertility gradient three ways, and compare what each design estimates."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import design

TITLE = "Systematic, randomized, blocked: three layouts on one field"
GOAL = ("Harvest the field-trial simulator two thousand times under a systematic layout, a completely randomized "
        "one and randomized complete blocks, and compare the bias, the spread and the power of each with theory.")
TASKS = [
    "Set gradient=0 and hump=0 in design.Field. What does blocking cost when there is nothing to block on (look at the error df)?",
    "Block on rows instead of columns (transpose the layout). Why is that worse than not blocking at all?",
    "Replace the columns by a 4 x 4 Latin square repeated three times, analysed with design.latin_anova, and compare the power.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    field = design.Field(rows=4, cols=12, gradient=6.0, hump=4.0, noise=2.0)
    fert, sigma = field.fertility, field.noise
    k, b, reps = 4, 12, 2000
    effect = np.array([0.0, 1.0, 2.0, 3.0])  # variety D (3) yields 3 more than variety A (0)
    truth = effect[3] - effect[0]

    def systematic():  # varieties in order from west to east, three columns each
        return np.repeat(np.arange(k), b // k)[None, :].repeat(k, axis=0)

    def crd():
        return rng.permutation(np.repeat(np.arange(k), b)).reshape(k, b)

    def rcbd():  # every column (a block) holds each variety once, in random order
        return np.column_stack([rng.permutation(k) for _ in range(b)])

    out = {}
    for name, layout in (("systematic", systematic), ("randomized", crd), ("blocked", rcbd)):
        est, rej, rej0 = np.empty(reps), 0, 0
        for r in range(reps):
            lay = layout()
            y = field.harvest(effect[lay], rng)
            groups = [y[lay == t] for t in range(k)]
            est[r] = groups[3].mean() - groups[0].mean()
            y0 = field.harvest(np.zeros_like(fert), rng)  # the null: no variety differs
            if name == "blocked":
                by_block = lambda v: np.array([[v[lay[:, j] == t, j][0] for j in range(b)] for t in range(k)])  # noqa: E731
                rej += design.rcbd(by_block(y))["p"] < 0.05
                rej0 += design.rcbd(by_block(y0))["p"] < 0.05
            else:
                rej += design.oneway(groups)["p"] < 0.05
                rej0 += design.oneway([y0[lay == t] for t in range(k)])["p"] < 0.05
        out[name] = dict(est=est, mean=est.mean(), sd=est.std(ddof=1), power=rej / reps, size=rej0 / reps)

    # theory: a difference of two group means of 12 plots each, under each randomization
    s2_all = fert.var(ddof=1)  # the whole field's fertility variance
    s2_col = fert.var(axis=0, ddof=1).mean()  # the fertility variance left inside a column
    sd_crd = np.sqrt((s2_all + sigma ** 2) * 2 / b)
    sd_rcbd = np.sqrt((s2_col + sigma ** 2) * 2 / b)
    s, c, r = out["systematic"], out["randomized"], out["blocked"]
    lab = labs.Lab()
    lab.row("true difference, variety D minus variety A", f"{truth:.2f}")
    lab.row("systematic: mean estimate", f"{s['mean']:.2f}   (bias {s['mean'] - truth:+.2f}; F test rejects a true null {s['size']:.0%} of the time)")
    lab.row("randomized: mean, sd of the estimate", f"{c['mean']:.2f}, {c['sd']:.2f}   (theory {truth:.2f}, {sd_crd:.2f})")
    lab.row("blocked: mean, sd of the estimate", f"{r['mean']:.2f}, {r['sd']:.2f}   (theory {truth:.2f}, {sd_rcbd:.2f})")
    lab.row("F test at 5%: size under the null", f"randomized {c['size']:.1%}   blocked {r['size']:.1%}")
    lab.row("F test at 5%: power", f"randomized {c['power']:.0%}   blocked {r['power']:.0%}")
    lab.note = ("The systematic layout measures the field, not the varieties. Randomization removes the bias and "
                "makes the F test honest; blocking on the gradient takes the gradient out of the error, so the same "
                "48 plots detect the effect far more often.")
    assert s["mean"] - truth > 3 * c["sd"] and s["size"] > 0.9, "the systematic layout is biased by the gradient"
    assert abs(c["mean"] - truth) < 5 * sd_crd / np.sqrt(reps) and abs(r["mean"] - truth) < 5 * sd_rcbd / np.sqrt(reps), "unbiased"
    assert abs(c["sd"] / sd_crd - 1) < 0.08 and abs(r["sd"] / sd_rcbd - 1) < 0.08, "the randomization variances"
    assert abs(c["size"] - 0.05) < 0.02 and abs(r["size"] - 0.05) < 0.02, "both randomized designs hold their level"
    assert r["power"] > c["power"] + 0.3, "blocking buys power"

    fig, ax = labs.figure(2, size=(11, 4.2), gridspec_kw={"width_ratios": [1, 1.25]})
    im = ax[0].imshow(fert, cmap="YlGn", aspect="auto", vmax=fert.max() + 8)  # headroom keeps the letters legible
    lay = rcbd()
    for i in range(k):
        for j in range(b):
            ax[0].text(j, i, "ABCD"[lay[i, j]], ha="center", va="center", color="#0E1117", fontsize=10, fontweight="bold")
    ax[0].set(title="Fertility (hidden) and one blocked layout", xlabel="column = block, west to east", ylabel="row",
              xticks=range(b), yticks=range(k))
    ax[0].grid(False)
    fig.colorbar(im, ax=ax[0], shrink=0.8, label="fertility")
    lo, hi = min(c["est"].min(), truth - 1), s["est"].max()
    bins = np.linspace(lo, hi, 90)
    for name, color in (("systematic", labs.RED), ("randomized", labs.BLUE), ("blocked", labs.GOLD)):
        ax[1].hist(out[name]["est"], bins=bins, density=True, color=color, alpha=0.65, label=name)
    ax[1].axvline(truth, color=labs.INK, ls="--", lw=1, label="truth")
    ax[1].set(title="Estimates of D minus A over 2,000 harvests", xlabel="estimated difference", ylabel="density")
    ax[1].legend()
    lab.fig = fig
    return lab

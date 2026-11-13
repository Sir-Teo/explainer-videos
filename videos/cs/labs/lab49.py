"""Lab 49: stress four case studies: a feed's fan-out, a dispatcher's matching, a crawler's Bloom filter, a ledger's retries."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import math

import numpy as np

from explainer.cs.design import cases

TITLE = "Four designs under test: fan-out, dispatch, dedup and double entry"
GOAL = ("Cost a news feed on a power-law follower graph by pushing, pulling and the hybrid, match riders to drivers "
        "greedily and by optimal assignment, measure a Bloom filter's false positives against its formula, and "
        "replay payments with retries to see which invariant catches a double charge.")
TASKS = [
    "Set reads_per_user_day to 0.2 in cases.feed_cost, so that people post more than they read. Which end of the threshold scale is cheapest now, and why does the ratio of pull to push equal reads over posts?",
    "Give the dispatcher 60 riders and 61 drivers, then 60 and 200. How does the gap between greedy and optimal pickup distance change with spare drivers?",
    "Run cases.ot_experiment with start='ab' and with a 40-character string. Why does applying operations as sent converge more often on the long string, and does transformation still converge every time?",
]

USERS, F_MIN, ALPHA = 100_000, 20, 2.1


def run(seed=0):
    lab = labs.Lab()

    # 1. fan-out on write, on read, and the hybrid at three thresholds
    feed = cases.feed_cost(users=USERS, seed=seed)
    ratio = feed["pull_reads"] / feed["push_writes"]
    assert abs(ratio - feed["reads"] / feed["posts"]) < 1e-9, "pull over push is reads over posts: the means are equal"
    hybrid = feed["hybrid"]  # thresholds 100, 1,000, 10,000 and 'nobody is pulled'
    totals = [h["total"] for h in hybrid]
    assert all(a > b for a, b in zip(totals, totals[1:])), "with reads above posts, raising the threshold only saves"
    assert abs(totals[-1] - feed["push_writes"]) < 1e-6 and all(h["max_fanout_per_post"] < h["threshold"] for h in hybrid)
    lab.row("follower graph", f"median {feed['median_followers']:.0f}, mean {feed['mean_followers']:.0f}, "
                              f"largest {feed['max_followers']:,}")
    lab.row("operations a day: push all, pull all", f"{feed['push_writes'] / 1e6:.1f} M, {feed['pull_reads'] / 1e6:.1f} M "
                                                    f"(ratio {ratio:.0f} = reads / posts)")
    for h in hybrid[:3]:
        model = USERS * (F_MIN / h["threshold"]) ** (ALPHA - 1)  # accounts above the threshold under the Pareto law
        assert abs(h["celebrities"] - model) < 5 * math.sqrt(model) + 5, "the tail follows the power law"
        lab.row(f"hybrid, pull accounts with {h['threshold']:,}+ followers",
                f"{h['total'] / 1e6:.1f} M a day; pulls {h['celebrities']:,} accounts (power law: {model:,.0f}); "
                f"worst post {h['max_fanout_per_post']:,} writes")

    # 2. dispatch: the optimal assignment of a batch against nearest free driver
    d = cases.dispatch(riders=60, drivers=70, rounds=40, seed=seed + 2)
    gain = d["batched_mean"] / d["greedy_mean"]
    assert d["batched_mean"] < d["greedy_mean"] and 0.7 < gain < 0.92, "the assignment cuts the mean pickup by a sixth or so"
    assert d["batched_worst"] < d["greedy_worst"]
    lab.row("dispatch, 60 riders and 70 drivers", f"mean pickup {d['greedy_mean']:.2f} km greedy, {d['batched_mean']:.2f} km "
            f"optimal; worst in a round {d['greedy_worst']:.2f} against {d['batched_worst']:.2f} km")

    # 3. the crawler's Bloom filter against (1 - exp(-kn/m))^k
    bits = (4.8, 7.2, 9.6, 12.0)
    bloom = [cases.bloom_check(n=20_000, bits_per=b) for b in bits]
    for b in bloom:
        assert abs(b["false_positive"] - b["theory"]) < 4 * math.sqrt(b["theory"] / 20_000) + 0.001
    lab.row("Bloom filter at 9.6 bits a URL", f"{bloom[2]['hashes']} hashes, false positives {bloom[2]['false_positive']:.2%} "
            f"measured, {bloom[2]['theory']:.2%} from the formula")

    # 4. the ledger: sum = 0 holds with and without idempotency keys, so it cannot see a double charge
    keyed = cases.ledger(n=3000, seed=seed + 4, idempotent=True)
    bare = cases.ledger(n=3000, seed=seed + 4, idempotent=False)
    assert keyed["sum"] == 0 and bare["sum"] == 0 and keyed["double_charges"] == 0 and bare["double_charges"] > 100
    assert keyed["entries"] <= 3000 and bare["entries"] - bare["double_charges"] <= 3000, "at most one first charge each"
    lab.row("3,000 payments with retries", f"without keys {bare['entries']:,} entries, {bare['double_charges']} charged twice; "
            f"with keys {keyed['entries']:,} and 0; both ledgers sum to {bare['sum']}")
    ot = cases.ot_experiment(trials=2000, seed=seed + 5)
    assert ot["converged_transformed"] == 1.0 and ot["converged_naive"] < 0.2
    lab.row("2,000 concurrent pairs of edits", f"converged: transformed {ot['converged_transformed']:.0%}, as sent "
            f"{ot['converged_naive']:.1%}")
    lab.note = ("Counted in operations pushing everything is cheapest and the hybrid buys only a bound on one post's "
                "fan-out; the optimal batch beats greedy; the filter errs as the formula says; and a ledger needs "
                "'one entry per payment' beside 'sums to zero'.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    names = ["pull all"] + [f"pull {h['threshold']:,}+" for h in hybrid[:3]] + ["push all"]
    push = [0.0] + [h["push_writes"] / 1e6 for h in hybrid]
    pull = [feed["pull_reads"] / 1e6] + [h["pull_reads"] / 1e6 for h in hybrid]
    x = np.arange(5)
    ax[0].bar(x, push, color=labs.BLUE, label="timeline writes (pushed)")
    ax[0].bar(x, pull, bottom=push, color=labs.ORANGE, label="fetches at read time (pulled)")
    ax[0].set(title="A feed's daily operations, by who is pulled", ylabel="millions a day")
    ax[0].set_xticks(x, names)
    ax[0].legend()
    grid = np.linspace(4, 13, 60)
    theory = [(1 - math.exp(-max(1, round(b * math.log(2))) / b)) ** max(1, round(b * math.log(2))) for b in grid]
    ax[1].semilogy(grid, theory, color=labs.GOLD, label="(1 - exp(-kn/m))^k, k = round(0.69 m/n)")
    ax[1].semilogy(bits, [b["false_positive"] for b in bloom], "o", color=labs.BLUE, label="measured on 20,000 URLs")
    ax[1].axhline(0.01, color=labs.MUTED, ls="--", lw=1)
    ax[1].set(title="A Bloom filter's false positives", xlabel="bits per URL", ylabel="false-positive rate")
    ax[1].legend()
    lab.fig = fig
    return lab

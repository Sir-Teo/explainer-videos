"""Lab 40: apply Parnas's four changes to both KWIC decompositions, then test Brooks' law and a schedule's tail."""

from videos.coursekit import labs

import math

import numpy as np

from explainer.cs.se import kwic
from explainer.cs.se import process

TITLE = "What a change costs: Parnas's modules, Brooks' law, and estimates"
GOAL = ("Build the keyword-in-context index of a random text with both of Parnas's decompositions, apply his four "
        "changes to each, and count the modules whose source had to change while the index stays the same. Then run "
        "the part's two process models: four people added to a six-person project at different months, and twenty "
        "lognormal tasks planned at their medians.")
TASKS = [
    "Set ramp=1.0 and mentor=0.0 in process.brooks (newcomers productive at once). Until which month does adding four people still help?",
    "Plan each task at its mean instead of its median (multiply the plan by exp(sigma^2 / 2)). How often is the project on time now?",
    "Raise channel_cost from 0.02 to 0.04. Which team size finishes first from the start, and why is it smaller?",
]
WORDS = "pebble gate adder stack queue graph proof cache packet clock ledger novel index shift module secret".split()
SIGMAS = (0.3, 0.6, 1.0)
FILM_ON_TIME = (0.27, 0.12, 0.04)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # Parnas: the same index from both decompositions, before and after each change
    text = "\n".join(" ".join(rng.choice(WORDS, size=int(rng.integers(2, 6)))) for _ in range(8))
    e = kwic.experiment(text)
    n_shifts = sum(len(line.split()) for line in text.splitlines())
    assert len(e["index"]) == n_shifts, "one index line per circular shift"
    for r in e["rows"]:
        d1, d2 = r["d1"], r["d2"]
        lab.row(f"change: {r['change']}", f"flowchart modules {d1['n']} of {d1['of']} ({d1['lines']} lines)   "
                                          f"hidden decisions {d2['n']} of {d2['of']} ({d2['lines']} lines)")
        assert d1["same_output"] and d2["same_output"], "every variant still prints the same index"
        assert d2["n"] == 1, "with one secret per module, each change stays inside one module"
    touched = [r["d1"]["n"] for r in e["rows"]]
    assert sorted(touched) == [1, 2, 3, 3], "the flowchart decomposition spreads three of the four changes"

    # Brooks: 120 person-months, six people, four more added at month m
    base = process.brooks()
    months = np.arange(0, 22.5, 1.0)
    finish = np.array([process.brooks(add_at=float(m), add=4) for m in months])
    worst = months[int(np.argmax(finish))]
    lab.row("six people, nobody added", f"finish in month {base:.1f}   (120 / (6 x 0.9) = {120 / 5.4:.1f})")
    lab.row("four added in month 2, and in month 16", f"month {finish[2]:.1f}, and month {finish[16]:.1f}   the film: 17.8 and 22.6")
    assert abs(base - 120 / 5.4) < 0.1, "the baseline is work over six people's output, less five channels each"
    assert finish[2] < base - 3 and finish[16] > base, "added early they help; added late they make the project later"
    assert process.channels(10) == 45 and process.channels(6) == 15, "n(n - 1)/2 channels"
    sizes = (2, 4, 6, 8, 12, 16, 24, 32, 40)
    from_start = [process.brooks(team=n) for n in sizes]
    assert sizes[int(np.argmin(from_start))] == 24, "from the start, 24 people is fastest; more is slower again"

    # estimates: twenty lognormal tasks, plan = the sum of the medians
    on_time = []
    for sigma, film in zip(SIGMAS, FILM_ON_TIME):
        s = process.schedule(sigma=sigma, trials=20_000, seed=seed)
        on_time.append(s)
        lab.row(f"20 tasks, sigma = {sigma}: on time", f"{s['on_time']:.1%} (the film: {film:.0%})   P80 {s['p80']:.0f} days against a plan of 100   "
                                                  f"mean task {s['mean_task']:.2f} = 5 e^(sigma^2/2) = {5 * math.exp(sigma ** 2 / 2):.2f}")
        assert abs(s["on_time"] - film) < 0.02, "the plan of medians is rarely met"
        assert abs(s["mean_task"] - 5 * math.exp(sigma ** 2 / 2)) < 0.03 * (1 + 3 * sigma), "a lognormal's mean exceeds its median"
    assert on_time[0]["on_time"] > on_time[1]["on_time"] > on_time[2]["on_time"]
    lab.note = ("Hiding one decision per module kept every change inside one module; people added late cost more "
                f"than they give (worst when added in month {worst:.0f}); and a plan that adds up medians is met "
                "about one time in eight when tasks vary by a factor of e^0.6.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    names = ["store words\npacked", "change the\ninput format", "store shifts\nin full", "alphabetize\non demand"]
    order = ["store words packed", "change the input format", "store shifts in full", "alphabetize on demand"]
    rows = {r["change"]: r for r in e["rows"]}
    x = np.arange(4)
    ax[0].set_axisbelow(True)
    ax[0].bar(x - 0.2, [rows[c]["d1"]["n"] for c in order], 0.4, color=labs.RED, label="flowchart decomposition (5 modules)")
    ax[0].bar(x + 0.2, [rows[c]["d2"]["n"] for c in order], 0.4, color=labs.GREEN, label="one hidden decision each (6 modules)")
    ax[0].set(title="Parnas's KWIC: modules a change touches", ylabel="modules whose source changed", xticks=x,
              xticklabels=names, ylim=(0, 4.4), yticks=[0, 1, 2, 3])
    ax[0].legend(loc="upper right")
    ax[1].plot(months, finish, color=labs.GOLD, marker="o", ms=3.5, label="four people added in month m")
    ax[1].axhline(base, color=labs.BLUE, ls="--", label=f"nobody added: month {base:.1f}")
    ax[1].fill_between(months, base, finish, where=finish > base, color=labs.RED, alpha=0.3, label="Brooks' law: later")
    ax[1].set(title="Brooks' law, with its condition", xlabel="month m in which the four join", ylabel="month the project finishes")
    ax[1].legend(loc="lower right")
    lab.fig = fig
    return lab

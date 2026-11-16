"""Lab 51: human factors: Fitts's law, a vigilance watch by signal detection, the prevalence effect, the ironies of
automation, an alarm's two criteria, correlated Swiss cheese and fatigue."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import work as Wk

TITLE = "Human Factors"
GOAL = ("Fit Fitts's law, watch a simulated operator's sensitivity and criterion change over a two-hour watch, and "
        "find the alarm threshold that gets the most real events answered.")
TASKS = [
    "Halve the vigilance decline in sensitivity (d_loss = 0.25). How much of the fall in hits is left, and why?",
    "Raise the alarm's base rate from 1% to 10%. Where does the best threshold move, and what share is answered?",
    "Make the Swiss cheese layers five instead of four. How much does correlation 0.6 still cost?",
]


def run(seed=0):
    out = labs.Lab()
    f = Wk.fitts_trials(seed=seed + 1)
    assert 0.12 < f["b"] < 0.18 and f["r"] > 0.9
    out.row("Fitts's law fitted: a, b (s per bit), r", f"{f['a']:.3f}, {f['b']:.3f}, {f['r']:.2f}")
    v = Wk.vigilance(watchers=60, seed=seed + 2)
    assert v["hit"][-1] < v["hit"][0] and v["c"][-1] > v["c"][0]
    out.row("hits by half hour", ", ".join(f"{h:.2f}" for h in v["hit"]))
    out.row("d' by half hour; c by half hour", ", ".join(f"{d:.2f}" for d in v["d"]) + "; "
            + ", ".join(f"{c:.2f}" for c in v["c"]))
    p = Wk.prevalence_partial(prevs=(0.5, 0.1, 0.02, 0.01), shift=0.35)
    assert np.all(np.diff(p["miss"]) > 0)
    out.row("misses at prevalence 50%, 10%, 2%, 1%", ", ".join(f"{m:.2f}" for m in p["miss"]))
    t = Wk.takeover(seed=seed + 3)
    assert np.all(np.diff(t["within"]) < 0) and np.all(np.diff(t["system_fail"]) < 0)
    out.row("takeovers within 7 s at reliability .9 to .9999", ", ".join(f"{w:.2f}" for w in t["within"]))
    a = Wk.alarm()
    out.row("best alarm threshold; share of events answered", f"{a['best']:.1f}; {a['best_caught']:.2f}")
    ch = [Wk.swiss_cheese(rho=r, n=200000, seed=seed + 4) for r in (0.0, 0.6)]
    assert ch[1] > 10 * ch[0]
    out.row("Swiss cheese, independent and rho 0.6", f"{ch[0]:.5f}, {ch[1]:.4f}")
    out.row("hours awake like 0.05% and 0.10% alcohol", "17, 24")

    out.note = ("The human limits are lawful and measurable; the designer chooses where the criteria sit, how much "
                "practice the operator keeps, and whether the defences share their causes.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    ax[0].scatter(f["ID"], f["t"], s=6, color="grey")
    xs = np.linspace(f["ID"].min(), f["ID"].max(), 20)
    ax[0].plot(xs, f["a"] + f["b"] * xs, color=labs.BLUE)
    ax[0].set(title="Fitts's law", xlabel="index of difficulty (bits)", ylabel="movement time (s)")
    ax[1].plot(a["threshold"], a["hit"], label="events alarmed")
    ax[1].plot(a["threshold"], a["ppv"], label="alarms that are real")
    ax[1].plot(a["threshold"], a["caught"], label="events answered")
    ax[1].axvline(a["best"], color="green", ls=":")
    ax[1].set(title="an alarm's two criteria", xlabel="threshold (sensor SDs)", ylabel="rate")
    ax[1].legend()
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())

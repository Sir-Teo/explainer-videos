"""Lab 52: designing for minds: the keystroke-level model, pointing throughput, menus, foraging, the
problem-discovery curve, graphical perception and contrast."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import work as Wk

TITLE = "Designing for Minds"
GOAL = ("Predict task times by adding operators, measure pointing as throughput, and see why five users find fewer "
        "problems than the famous curve promises.")
TASKS = [
    "Write a keystroke-level model for logging in with a password manager and without one. Which operators dominate?",
    "Make the problems equally findable (a = b large, same mean). How close does the simulated curve come to "
    "1 - (1 - p)^n?",
    "Find a text colour on white that just passes 4.5 : 1 and one that just fails.",
]


def run(seed=0):
    out = labs.Lab()
    t = {k: Wk.klm_time(v) for k, v in {"shortcut": "MKKKKK", "menu": "HMPBBMPBBMPBB"}.items()}
    assert t["menu"] > 2.5 * t["shortcut"]
    out.row("KLM: shortcut; menu (s)", f"{t['shortcut']:.2f}; {t['menu']:.2f}")
    f = [Wk.fitts_effective(n=40, distance=d, width=w, a=0.2, b=0.2, seed=seed + i)
         for i, (d, w) in enumerate([(64, 32), (256, 16), (512, 8)])]
    tp = np.mean([x["throughput"] for x in f])
    assert 2.5 < tp < 5.5
    out.row("throughput at three IDs (bit/s)", ", ".join(f"{x['throughput']:.2f}" for x in f) + f"; mean {tp:.2f}")
    m = Wk.menu_time(practised=False, read=0.25)
    out.row("unfamiliar menu: best breadth for 64 items", str(int(m["breadth"][np.argmin(m["time"])])))
    lv = Wk.mvt_leave(20.0)
    out.row("foraging: leave a page after (travel 20 s)", f"{lv['t']:.1f} s")
    d = Wk.discovery(np.array([1, 5, 15]), a=0.6, b=1.34, seed=seed + 7)
    assert d["hetero"][1] < d["homog"][1]
    out.row("five users: equal p; unequal p", f"{d['homog'][1]:.2f}; {d['hetero'][1]:.2f}")
    errs = {e: Wk.graphical_error(e, seed=seed + 9)["log_err"] for e in ("position", "length", "angle", "area")}
    assert errs["position"] < errs["angle"] < errs["area"]
    out.row("chart error (log2): position, length, angle, area", ", ".join(f"{v:.2f}" for v in errs.values()))
    out.row("contrast: #767676 on white", f"{Wk.contrast_ratio((118, 118, 118), (255, 255, 255)):.2f} : 1")

    out.note = ("The keystroke-level model and Fitts's law predict skilled performance well; the five-user rule and "
                "the 21-day habit were rules of thumb, and the measured numbers are less flattering.")

    fig, ax = labs.figure(2, size=(11, 4.0))
    n = np.arange(1, 21)
    dd = Wk.discovery(n, a=0.6, b=1.34, seed=seed + 3)
    ax[0].plot(n, dd["homog"], label="all problems alike")
    ax[0].plot(n, dd["hetero"], label="problems that differ")
    ax[0].set(title="problems found", xlabel="users", ylabel="share")
    ax[0].legend()
    mm = Wk.menu_time()
    ax[1].plot(mm["breadth"], mm["time"], "o-", label="practised")
    ax[1].plot(m["breadth"], m["time"], "o-", label="unfamiliar")
    ax[1].set(xscale="log", title="64 items: time by breadth", xlabel="items per menu", ylabel="seconds")
    ax[1].legend()
    out.fig = fig
    return out


if __name__ == "__main__":
    print(run())

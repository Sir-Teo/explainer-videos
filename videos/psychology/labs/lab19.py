"""Lab 19: absolute judgment as a channel; the phonological loop with and without suppression; Sperling's partial
report; Brown-Peterson forgetting under SIMPLE, trial by trial; Sternberg's scanning and Townsend's mimicry; slots and
the K formula; continuous report with mixture, swap and process models, fitted to Bays, Catalao and Husain's open data
(or, offline, to Psyche); a ring attractor's diffusion; and a brain-training trial against two kinds of control."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import opendata
from explainer.psychology.psyche import wm

TITLE = "Working memory: span, forgetting, scanning, capacity and precision"
GOAL = ("Measure the capacity of absolute judgment in bits; run the phonological loop and abolish the word-length "
        "effect; see why the first Brown-Peterson trial forgets nothing; show that a parallel search can draw "
        "Sternberg's line; recover K from hits and false alarms; fit slots, averaging, equal and variable precision "
        "to real continuous-report data; and watch a ring attractor's memory diffuse.")
TASKS = [
    "In `wm.loop_span`, find the word duration at which the loop's span falls to the suppressed span. What does the "
    "model then predict for the word-length effect at faster and slower speech?",
    "Simulate a slots observer (`wm.simulate_report('slots', (3, 15), ...)`) with 50, 200 and 800 trials per set size "
    "and fit both the slots and the variable-precision models. How many trials does AIC need to pick the truth?",
    "Halve the ring attractor's noise. By what factor does the variance of the memory at 2 s change, and why?",
]


def run(seed=0):
    out = labs.Lab()
    rng = np.random.default_rng(seed)

    # 1. absolute judgment and recoding
    n = np.array([2, 4, 6, 10, 20])
    out.row("information transmitted (bits) with 2, 4, 6, 10, 20 categories",
            ", ".join(f"{v:.2f}" for v in wm.absolute_judgment(n)))
    out.row("binary digits held with 7 chunks, grouping 1 to 5", ", ".join(f"{wm.recoded_span(g):.0f}" for g in range(1, 6)))

    # 2. the loop
    for dur in (0.3, 0.8):
        a, b = wm.loop_span(dur, n=4000, rng=rng), wm.loop_span(dur, suppress=True, n=4000, rng=rng)
        out.row(f"span for {dur} s words: loop, suppressed", f"{a['span']:.2f}, {b['span']:.2f}")

    # 3. partial report
    r = wm.partial_report([0, 150, 300, 500, 1000])
    out.row("letters available at cue delays 0, 150, 300, 500, 1000 ms (whole report 4.5)",
            ", ".join(f"{v:.1f}" for v in r["available"]))

    # 4. forgetting, trial by trial
    d = np.array([3.0, 18.0])
    for t in (1, 2, 3, 10):
        out.row(f"Brown-Peterson recall after 3 and 18 s, trial {t}", ", ".join(f"{v:.2f}" for v in wm.brown_peterson(d, t)))
    assert wm.brown_peterson([18.0], 1)[0] > 0.95 > wm.brown_peterson([18.0], 3)[0]  # no forgetting on trial 1 only

    # 5. scanning
    k = np.arange(1, 7)
    for m in ("serial", "self", "parallel", "limited"):
        y = [wm.sternberg_rts(int(s), True, m, n=4000, rng=rng).mean() for s in k]
        out.row(f"{m} scanning, yes trials: slope (ms per item)", f"{np.polyfit(k, y, 1)[0]:.1f}")

    # 6. slots and K
    for N in (2, 4, 6, 8):
        c = wm.change_detection(N, K=3.5, n=20000, rng=rng)
        assert abs(wm.k_cowan(c["H"], c["FA"], N) - min(N, 3.5)) < 0.2  # the formula recovers the slots
        out.row(f"change detection, {N} items: H, F, Cowan's K", f"{c['H']:.2f}, {c['FA']:.2f}, "
                f"{wm.k_cowan(c['H'], c['FA'], N):.2f}")

    # 7. continuous report: open data if it can be fetched, else Psyche
    if opendata.available("bays_2009"):
        b = opendata.bays_2009()
        e, N, s, ne = b["error"], b["set_size"], b["subject"], b["nontarget_error"]
        source = "Bays et al. (2009)"
    else:
        N = np.repeat([1, 2, 4, 6], 600)
        e = wm.simulate_report("variable", (25.0, 1.0, 15.0), N, rng)
        s, ne = np.ones(len(N), int), np.full((len(N), 5), np.nan)
        source = "Psyche (offline: the open data could not be fetched)"
    out.row("continuous-report data", source)
    mix = {}
    for n_ in (1, 2, 4, 6):
        m = N == n_
        f = wm.fit_mixture(e[m])
        mix[n_] = f
        line = f"g = {f['g']:.2f}, s.d. = {np.degrees(f['sd']):.0f} deg"
        if n_ > 1 and np.isfinite(ne[m]).any():
            sw = wm.fit_swap(e[m], ne[m])
            line += f"; swaps {sw['pN']:.2f}"
        out.row(f"mixture fit, {n_} item{'s' if n_ > 1 else ''} (pooled)", line)
    first = s == s.min()
    fits = {mo: wm.fit_model(mo, e[first], N[first]) for mo in wm.MODELS}
    best = min(f["aic"] for f in fits.values())
    out.row("one observer: AIC above the best, slots / averaging / equal / variable",
            " / ".join(f"{fits[mo]['aic'] - best:.0f}" for mo in wm.MODELS))

    # 8. the ring attractor
    ring = wm.ring_attractor(delay=2000, trials=80, rng=rng)
    var = np.var(ring["angle"], 0)
    i1, i2 = np.searchsorted(ring["t"], 500), len(ring["t"]) - 1
    assert 2.0 < var[i2] / var[i1] < 7.0  # about linear growth: diffusion
    out.row("ring attractor: memory s.d. at 0.5 and 2 s (deg); variance ratio",
            f"{np.degrees(np.sqrt(var[i1])):.1f}, {np.degrees(np.sqrt(var[i2])):.1f}; {var[i2] / var[i1]:.1f}")

    # 9. training
    tr = {c: [wm.training_trial(40, control=c, rng=rng)["far"] for _ in range(200)] for c in ("passive", "active")}
    out.row("far transfer d, mean over 200 trials: no-contact control, active control",
            f"{np.mean(tr['passive']):.2f}, {np.mean(tr['active']):.2f}")

    out.note = ("The judgment channel saturates near 2.7 bits; recoding multiplies binary span. Suppression abolishes "
                "the word-length effect. The first Brown-Peterson trial forgets nothing. Limited-capacity parallel "
                "scanning has the serial slope. Cowan's K recovers the slots. On the open data, precision falls "
                "continuously and variable precision usually wins. The ring's variance grows linearly with delay. "
                "Expectation looks like transfer only against a no-contact control.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    edges = np.linspace(-np.pi, np.pi, 37)
    for n_, col in zip((1, 2, 4, 6), (labs.PINK, labs.BLUE, labs.GREEN, labs.GOLD)):
        h, _ = np.histogram(e[N == n_], edges, density=True)
        ax[0].step(np.degrees(edges[:-1]), h, where="post", color=col, lw=1.4, label=f"{n_} items")
    ax[0].set(title=f"Continuous-report errors: {source}", xlabel="error, degrees", ylabel="density")
    ax[0].legend(fontsize=8)
    ax[1].plot(ring["t"] / 1000, np.degrees(np.sqrt(var)), color=labs.BLUE, lw=1.8)
    ax[1].set(title="Ring attractor: the memory blurs", xlabel="delay, s", ylabel="s.d. of the memory, degrees")
    out.fig = fig
    return out

"""Lab 2: study a game that does nothing, six wrong ways and one right way, then shuffle and reshuffle."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import lab as plab
from explainer.psychology.pool import Pool

TITLE = "Six ways to find an effect that is not there, and the shuffle that does not"
GOAL = ("Run Campbell and Stanley's six unsound designs on the Pool for a treatment whose true effect is zero, "
        "then the randomized experiment; check that a shuffle balances a trait nobody measured, and test a real "
        "effect by reshuffling the labels.")
TASKS = [
    "Give the regression design a screening test of 5, 20 and 80 trials (plab.Lab(pool, n_trials=...)). How does "
    "the spurious effect change, and why?",
    "Plant a real effect of -8 ms and run the cross-over with counterbalanced=False. By how much is it wrong, and "
    "what does that number equal?",
    "Replace randomize by alternate (assignment in turn) after sorting the people by eagerness. What happens to "
    "the balance of age?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    out = labs.Lab()
    pool = Pool()
    L = plab.Lab(pool, seed=seed)
    n = 200

    # 1. the unsound designs, each with the true effect zero
    quick = plab.Lab(pool, seed=seed, n_trials=5)  # a short screening test regresses more
    est = {}
    for name in plab.THREATS:
        e = (quick if name == "regression" else L).threat(name, n=n)
        est[name] = e
        lo, hi = e.ci()
        out.row(f"{name}: effect reported (ms)", f"{e.effect:+.1f}   [{lo:+.1f}, {hi:+.1f}]   (truth: 0)")
        assert hi < 0, f"{name} reports an effect that is not there"

    # 2. the randomized experiment, many times
    studies = L.replicate("randomized", studies=300, n=n)
    sig = np.mean([L.randomized(n=n, study=s).p < 0.05 for s in range(300)])
    out.row("randomized, 300 studies: mean effect (ms)", f"{studies.mean():+.2f} +- {studies.std() / np.sqrt(300):.2f}")
    out.row("... share 'significant' at 5%", f"{100 * sig:.0f}%")
    assert abs(studies.mean()) < 4 * studies.std() / np.sqrt(300), "unbiased"
    assert 0.01 < sig < 0.11, "and wrong only as often as it says"

    # 3. what a shuffle balances
    ids = pool.sample(n, seed=seed + 11)
    keen = pool.keen[ids]
    z = np.array([plab.balance(keen, plab.randomize(n, 2, rng)) for _ in range(2000)])
    chosen = plab.balance(keen, (keen > np.median(keen)).astype(int))
    out.row("eagerness, shuffled groups: mean and SD of the difference (SD units)", f"{z.mean():+.3f}, {z.std():.3f}")
    out.row("... predicted SD, sqrt(4 / n)", f"{np.sqrt(4 / n):.3f}")
    out.row("eagerness, self-selected groups", f"{chosen:+.2f}")
    assert abs(z.mean()) < 0.02 and abs(z.std() - np.sqrt(4 / n)) < 0.02, "balanced in expectation, by a known amount"
    assert chosen > 1.0

    # 4. a real effect, judged by the deck that dealt it
    planted = -8.0
    pid = pool.sample(n, seed=seed + 23)
    g = plab.randomize(n, 2, rng)
    y = pool.session_rt(pid, 0, 20, seed=seed + 23, shift=planted * g)
    d = plab.difference(y, g)
    rt = plab.randomization_test(y, g, 5000, rng)
    out.row("a planted effect of -8 ms: estimate (ms)", f"{d.effect:+.1f}   [{d.ci()[0]:+.1f}, {d.ci()[1]:+.1f}]")
    out.row("... p by reshuffling the labels, and by Welch's t", f"{rt['p']:.3f}, {d.p:.3f}")
    assert abs(rt["p"] - d.p) < 0.03, "the two tests agree"
    many = L.replicate("randomized", studies=300, n=n, effect=planted)
    out.row("... 300 such studies: mean and SD of the estimate (ms)", f"{many.mean():+.1f}, {many.std():.1f}")
    assert abs(many.mean() - planted) < 4 * many.std() / np.sqrt(300), "one study wanders; the design is unbiased"

    # 5. pairing
    between = L.replicate("randomized", 200, n=40, effect=planted)
    within = L.replicate("crossover", 200, n=40, effect=planted)
    carry = L.replicate("crossover", 200, n=40, effect=planted, counterbalanced=False)
    out.row("40 people, two groups: SD of the estimate (ms)", f"{between.std():.1f}")
    out.row("40 people, each both ways: SD of the estimate (ms)", f"{within.std():.1f}")
    out.row("... control always first: mean estimate (ms)", f"{carry.mean():+.1f}   (truth: {planted:+.0f})")
    assert within.std() < 0.4 * between.std(), "pairing buys precision"
    assert abs(within.mean() - planted) < 1.0 and carry.mean() < planted - 3, "and needs a balanced order"
    out.note = ("Every unsound design found that a useless treatment works; the shuffled one did not, and it "
                "balanced a trait it never measured. Pairing sharpens the estimate, provided the order is "
                "counterbalanced.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    names = list(plab.THREATS)
    ys = np.arange(len(names))[::-1]
    for y_, name in zip(ys, names):
        e = est[name]
        lo, hi = e.ci()
        ax[0].plot([lo, hi], [y_, y_], color=labs.PINK, lw=3)
        ax[0].plot(e.effect, y_, "o", color=labs.PINK)
    ax[0].axvline(0, color=labs.GREEN, lw=2)
    ax[0].set_yticks(ys, names)
    ax[0].set(title="Six designs, a treatment that does nothing", xlabel="effect reported (ms); the truth is 0")
    bins = np.linspace(-30, 15, 46)
    ax[1].hist(between, bins=bins, color=labs.BLUE, alpha=0.5, label="two groups of 20")
    ax[1].hist(within, bins=bins, color=labs.PURPLE, alpha=0.7, label="40 people, each both ways")
    ax[1].hist(carry, bins=bins, color=labs.PINK, alpha=0.6, label="... control always first")
    ax[1].axvline(planted, color=labs.GREEN, lw=2)
    ax[1].set(title="A real effect of -8 ms, 200 studies of each design", xlabel="effect reported (ms)")
    ax[1].legend()
    out.fig = fig
    return out

"""Lab 8: an average that finds a wave, an echo in the blood, a brain of noise, and a correlation from nothing."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import imaging as I

TITLE = "From a noisy trace to a map, and three ways the map misleads"
GOAL = ("Average simulated EEG trials until a wave a quarter the size of the noise appears, and check the "
        "square-root law; convolve events with the haemodynamic response and fit a voxel by least squares; "
        "threshold brains of pure noise by four rules; select voxels by their correlation with a score and "
        "measure it again on fresh data; and work out what a study of 25 people can detect.")
TASKS = [
    "Halve the size of the N400 in erp_trials (edit erp_template, or scale the difference wave) and find how many "
    "trials per condition you now need for the difference to be four times its standard error. Why does the "
    "answer quadruple?",
    "In null_tmaps, raise the smoothness of the noise from fwhm=3 to fwhm=6 voxels. What happens to the share of "
    "empty brains that the uncorrected rule lights up, and why does Bonferroni become more conservative?",
    "Run voodoo with 40 subjects and the threshold that gives p < 0.001 for that sample (about r = 0.48). What "
    "correlation does the circular analysis report now? What does that say about which published correlations "
    "to distrust most?",
]


def run(seed=0):
    out = labs.Lab()

    # 1. averaging
    t = np.arange(-100.0, 800.0, 4.0)
    odd = I.erp_trials(1600, t, "n400", rng=np.random.default_rng(seed + 80))
    usual = I.erp_trials(1600, t, "none", rng=np.random.default_rng(seed + 81))
    noise = odd - I.erp_template(t, "n400")
    for n in (4, 25, 100, 400):
        left = float(np.sqrt((noise.reshape(-1, n, len(t)).mean(axis=1) ** 2).mean()))
        out.row(f"noise left in an average of {n} trials; 20 / sqrt(n)", f"{left:.2f}, {20 / np.sqrt(n):.2f} microvolts")
    diff = odd.mean(axis=0) - usual.mean(axis=0)
    win = (t > 300) & (t < 500)
    out.row("'socks' minus 'butter', 300 to 500 ms; the wave put in", f"{diff[win].mean():.1f}, "
            f"{(I.erp_template(t, 'n400') - I.erp_template(t, 'none'))[win].mean():.1f} microvolts")
    assert abs(float(np.sqrt((noise.reshape(-1, 100, len(t)).mean(axis=1) ** 2).mean())) - 2.0) < 0.4
    assert diff[win].mean() < -2.0

    # 2. the echo and the linear model
    tt = np.linspace(0, 30, 3001)
    h = I.hrf(tt)
    out.row("the haemodynamic response: peak, lowest point", f"{tt[np.argmax(h)]:.1f} s, {tt[np.argmin(h)]:.1f} s")
    both = I.bold([10.0, 16.0], 60, 1.0)
    out.row("two events: largest gap between the sum of responses and the response to both",
            f"{np.abs(both - I.bold([10.0], 60, 1.0) - I.bold([16.0], 60, 1.0)).max():.1e}")
    brain = I.SyntheticBrain(regions=((16, 15, 3.0, 0.20), (30, 33, 4.0, 0.16)))
    s = brain.scan(rng=np.random.default_rng(seed + 82))
    fit = I.glm(s["Y"][:, 16, 15], s["X"], [1, 0])
    out.row("one active voxel (true weight 0.20): fitted weight, t", f"{fit['beta'][0, 0]:.2f}, {fit['t'][0]:.1f}")
    assert abs(tt[np.argmax(h)] - 5.0) < 0.1 and 0.0 < fit["beta"][0, 0] < 0.45

    # 3. four rules, on a brain with something in it and on brains of noise
    null_maps, mask = I.null_tmaps(400, rng=np.random.default_rng(seed + 83))
    extent = I.cluster_extent(I.null_tmaps(400, rng=np.random.default_rng(seed + 84))[0], mask, s["df"])
    rates = I.familywise_rates(null_maps, mask, s["df"], extent)
    for rule in ("uncorrected", "bonferroni", "fdr", "cluster"):
        hit = I.threshold_map(s["t"], s["df"], brain.mask, rule, extent=extent)
        out.row(f"{rule}: true voxels found of {int(brain.active.sum())}; empty brains with something",
                f"{int((hit & brain.active).sum())}; {100 * rates[rule]:.0f}%")
    out.row("chance of any false alarm in 100,000 independent tests at p < 0.001", f"{I.chance_of_any(100_000):.4f}")
    assert rates["uncorrected"] > 0.3 and rates["bonferroni"] < 0.08

    # 4. the cluster rule on the wrong kind of noise
    c = I.cluster_calibration(brains=300, long_tail=0.5, rng=np.random.default_rng(seed + 85))
    out.row("cluster rule: empty brains passing, noise as assumed and with a long tail",
            f"{100 * c['gaussian']:.0f}%, {100 * c['long_tail']:.0f}%")
    assert c["long_tail"] > c["gaussian"]

    # 5. circular selection
    v = I.voodoo(subjects=16, voxels=10_000, threshold=0.7, rng=np.random.default_rng(seed + 86))
    out.row("16 people, 10,000 voxels of noise: voxels with r > 0.7", str(v["selected"]))
    out.row("... their mean correlation, in the same data and in fresh data", f"{v['r_same']:.2f}, {v['r_fresh']:.2f}")
    out.row("the ceiling for reliabilities 0.5 and 0.8; for 0.4 and 0.8", f"{I.r_ceiling(0.5, 0.8):.2f}, {I.r_ceiling(0.4, 0.8):.2f}")
    assert v["r_same"] > 0.7 and abs(v["r_fresh"]) < 0.3

    # 6. reading backwards, and how many people
    out.row("reverse inference with odds multiplied by 2.3: priors 0.5, 0.2, 0.1 become",
            ", ".join(f"{I.reverse_inference(p, 0.23, 0.10)['posterior']:.2f}" for p in (0.5, 0.2, 0.1)))
    st = I.small_study(0.06, 25, rng=np.random.default_rng(seed + 87))
    out.row("25 people, true r = 0.06: studies significant; their mean |r|; wrong sign",
            f"{100 * st['power']:.0f}%; {st['mean_sig_r']:.2f}; {100 * st['wrong_sign']:.0f}%")
    out.row("people needed for 80% power at r = 0.2, 0.06, 0.01",
            ", ".join(f"{I.n_for_correlation(r):,}" for r in (0.2, 0.06, 0.01)))
    assert st["mean_sig_r"] > 0.4 and I.n_for_correlation(0.2) == 194
    out.note = ("Averaging leaves what is locked to the event and shrinks the rest by the square root of the number "
                "of trials. The blood's response peaks five seconds late, and under the linear assumption "
                "responses add, which is what lets an experiment's design predict a voxel's signal. A map is a "
                "test in every voxel: uncorrected, nearly half of empty slices show something, and each "
                "correction that prevents it misses real voxels. Voxels chosen by their correlation report a "
                "correlation set by the threshold, not by the brain, and it vanishes in fresh data. An "
                "unselective region moves a prior only a little. And 25 people can only ever report a brain-"
                "behaviour correlation of 0.4 or more, whatever the truth is.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(t, odd[0], color=labs.GREY, lw=0.6, label="one trial")
    ax[0].plot(t, odd[:25].mean(axis=0), color=labs.BLUE, lw=1.2, label="average of 25")
    ax[0].plot(t, odd[:400].mean(axis=0), color=labs.GREEN, lw=2, label="average of 400")
    ax[0].plot(t, I.erp_template(t, "n400"), color=labs.PINK, lw=1.2, ls="--", label="the wave put in")
    ax[0].set(title="Averaging trials locked to a word", xlabel="time after the word (ms)", ylabel="microvolts",
              ylim=(-30, 30))
    ax[0].legend(loc="upper right", fontsize=8)
    edges = np.linspace(-1, 1, 41)
    ax[1].hist(v["r_all"], edges, color=labs.GREY)
    ax[1].axvline(0.7, color=labs.PINK, lw=1.5, ls="--")
    ax[1].set(title=f"10,000 voxels of noise: {v['selected']} pass r > 0.7, mean {v['r_same']:.2f}",
              xlabel="correlation with the score, 16 people", ylabel="voxels")
    out.fig = fig
    return out

"""Lab 15: decibels and the threshold in quiet, the cochlea as a gammatone filter bank, masking by the power-spectrum
model, pitch by summary autocorrelation (the missing fundamental), interaural delays and a Jeffress array, categorical
identification and the label model of discrimination, the McGurk effect as cue combination, the gate, and a fragile
count of smells."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import hearing as H

TITLE = "The other senses: filters, pitch, delays and gates"
GOAL = ("Put sound in decibels and find where the ear is most sensitive; build the cochlea as a bank of gammatone "
        "filters and watch a tone excite its own place; measure a critical band by band-widening; recover a missing "
        "fundamental by autocorrelation; locate a tone from microsecond delays with a Jeffress array; predict "
        "categorical discrimination from labels; fuse a voice and a face by reliability; rub away pain with a gate; "
        "and see how a count of smells depends on one threshold.")
TASKS = [
    "Make a harmonic complex from harmonics 10 to 13 of 150 Hz, then shift every component up by 30 Hz. What pitch does "
    "the summary autocorrelation report for each, and why does the shifted one not stay at 150 Hz?",
    "Run the Jeffress array with a 1500 Hz tone from 30 degrees. How many peaks are there, and which is the true delay? "
    "Then add a 700 Hz tone from the same place and sum the two arrays' counts.",
    "With hearing.mcgurk, find the ratio of visual to auditory noise at which half of all trials are heard as /d/, "
    "and the ratio at which the voice wins nine times in ten.",
]


def run(seed=0):
    out = labs.Lab()
    rng = np.random.default_rng(seed)

    # 1. levels and the threshold in quiet
    f = np.geomspace(20, 16000, 2000)
    tq = H.threshold_in_quiet(f)
    out.row("threshold in quiet: most sensitive frequency (Hz) and its level (dB SPL)", f"{f[np.argmin(tq)]:.0f}, {tq.min():.1f}")
    out.row("pressure ratio from 0 to 130 dB SPL", f"{H.pressure(130) / H.pressure(0):.3g}")

    # 2. the cochlea and masking
    cfs = H.erb_space(80, 7000, 48)
    for ft in (500, 2000):
        ex = H.excitation(H.tone(ft, 0.2), cfs)
        out.row(f"a {ft} Hz tone: the most excited channel (Hz)", f"{cfs[np.argmax(ex)]:.0f}")
    out.row("ERB at 1 kHz and 4 kHz (Hz)", f"{H.erb(1000):.0f}, {H.erb(4000):.0f}")
    thr = [H.masked_threshold(2000, b, 20.0) for b in (50, 100, 240, 500, 1000)]
    out.row("band-widening at 2 kHz: thresholds for bands of 50 to 1000 Hz (dB)", ", ".join(f"{t:.1f}" for t in thr))

    # 3. pitch
    for name, hs in (("1-6", range(1, 7)), ("3-6", range(3, 7)), ("5-8", range(5, 9))):
        p = H.pitch(H.harmonic_complex(200, hs, 0.25))
        out.row(f"harmonics {name} of 200 Hz: pitch by autocorrelation (Hz)", f"{p:.1f}")
        assert abs(p - 200) < 4, "the missing fundamental is found"

    # 4. where
    true = float(H.itd(30))
    L = H.phase_locked_spikes(500, 0.0, 3.0, rng, rate=0.5)
    R = H.phase_locked_spikes(500, true, 3.0, rng, rate=0.5)
    delays = np.arange(-700, 701, 25) * 1e-6
    counts = H.jeffress(L, R, delays)
    best = delays[np.argmax(counts)]
    out.row("ITD at 30 and 90 degrees (microseconds)", f"{true * 1e6:.0f}, {H.itd(90) * 1e6:.0f}")
    out.row("Jeffress array: busiest detector (microseconds) and the direction it implies (deg)",
            f"{best * 1e6:.0f}, {H.azimuth_from_itd(best):.1f}")

    # 5. speech
    steps = np.arange(1, 15)
    p = H.identification(steps, 7.5, 0.6)
    abx = H.abx_from_labels(p[:-2], p[2:])
    out.row("ABX predicted from labels, two steps apart: within a category and at the boundary",
            f"{abx[0]:.2f}, {abx.max():.2f}")
    sh = H.mcgurk(0.0, 2.0, 0.45, 0.45, n=20000, rng=rng)
    out.row("McGurk with equal reliabilities: shares heard as b, d, g", ", ".join(f"{v:.2f}" for v in sh))

    # 6. the gate and smell
    out.row("gate: T for an injury of 1, with no touch and while rubbing", f"{H.gate(0, 1):.2f}, {H.gate(1.2, 1):.2f}")
    est = {t: H.bushdid_estimate(128, 30, t) for t in (0.4, 0.6, 0.8)}
    out.row("discriminable mixtures of 30 from 128 at overlap thresholds 40%, 60%, 80%",
            ", ".join(f"{v:.2g}" for v in est.values()))
    out.note = ("The ear is most sensitive near 3 kHz and spans a few million-fold in pressure. Each channel of the "
                "filter bank answers its own frequency, and only noise inside one filter masks. Autocorrelation finds "
                "200 Hz with or without the fundamental. Microsecond delays give direction, with ambiguity by whole "
                "cycles. Labels alone predict a discrimination peak at the boundary; equal reliabilities fuse ba and ga "
                "into da; rubbing closes the gate; and a count of smells swings by twelve orders of magnitude with one "
                "threshold.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    lags, s_full = H.summary_autocorrelation(H.harmonic_complex(200, range(1, 7), 0.25), max_lag=0.015)
    _, s_miss = H.summary_autocorrelation(H.harmonic_complex(200, range(3, 7), 0.25), max_lag=0.015)
    ax[0].plot(lags * 1000, s_full, color=labs.BLUE, lw=1.6, label="harmonics 1-6")
    ax[0].plot(lags * 1000, s_miss, color=labs.PINK, lw=1.6, label="harmonics 3-6")
    ax[0].axvline(5, color=labs.GREY, lw=0.8)
    ax[0].set(title="Summary autocorrelation: a peak at 5 ms", xlabel="lag (ms)", ylabel="summary")
    ax[0].legend(fontsize=8)
    ax[1].bar(delays * 1e6, counts, width=20, color=labs.GREEN)
    ax[1].axvline(true * 1e6, color=labs.PINK, lw=1.2)
    ax[1].set(title="A Jeffress array, 500 Hz from 30 degrees", xlabel="internal delay (microseconds)",
              ylabel="coincidences")
    out.fig = fig
    return out

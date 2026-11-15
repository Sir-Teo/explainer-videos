"""Lab 51: synthesis, computed: sawtooths and their aliasing, the ladder against its circuit, and fitting a patch."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import dynamics as D
from explainer.music.monochord import synth as S

TITLE = "Synthesis, computed"
GOAL = ("Measure how four sawtooths alias, step the ladder's circuit three ways against a reference, and fit a patch to a "
        "sound you design.")
TASKS = [
    "Change NOTE. How does each sawtooth's aliasing change from octave to octave, and why does the naive one lose 3 dB an octave?",
    "Change CUTOFF, K and DRIVE. At what K does the forward-step model's error grow fastest? Does the trapezoid keep its lead?",
    "Edit TARGET (a hidden patch: cutoff, k, mix). Does the search find it? Then make the target a drawbar organ and explain the fit.",
]
NOTE = 1760.0
CUTOFF, K, DRIVE = 1500.0, 3.0, 1.0
TARGET = (900.0, 3.0, 0.25)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    names = ("naive", "PolyBLEP", "BLIT", "additive")
    fns = (S.saw_naive, S.saw_polyblep, S.saw_blit, S.saw_additive)
    al = [D.alias_energy(fn(NOTE, SR), NOTE, SR) for fn in fns]
    lab.row(f"aliasing at {NOTE:g} Hz (dB re the note): " + ", ".join(names), ", ".join(f"{a:.1f}" for a in al))
    x = DRIVE * S.saw_polyblep(220.0, 2400)
    ref = S.ladder_ode(x, CUTOFF, K)

    def err(y):
        return 10 * np.log10(np.sum((y - ref) ** 2) / np.sum(ref ** 2))
    rows = {"forward": [err(S.ladder(x, CUTOFF, K, oversample=r, half=False)) for r in (1, 2, 4)],
            "corrected": [err(S.ladder(x, CUTOFF, K, oversample=r)) for r in (1, 2, 4)],
            "trapezoid": [err(S.ladder_trap(x, CUTOFF, K, oversample=r)) for r in (1, 2, 4)]}
    for k, v in rows.items():
        lab.row(f"ladder, {k}: error at 1x, 2x, 4x (dB)", ", ".join(f"{e:.1f}" for e in v))
    f = 261.63
    tgt = S.patch(f, 8192, *TARGET)
    fit = S.fit_patch(tgt, f)
    lab.row("hidden patch (cutoff, k, mix)", f"{TARGET[0]:.0f} Hz, {TARGET[1]:g}, {TARGET[2]:g}")
    lab.row("found", f"{fit['cutoff']:.0f} Hz, {fit['res']:g}, {fit['mix']:g}; distance {fit['distance_db']:.2f} dB")
    assert rows["trapezoid"][0] < rows["forward"][0] and fit["distance_db"] < 3.0

    # sound: the hidden patch and the fit; ear problem: naive or PolyBLEP high notes, at random
    n = int(1.2 * SR)
    env = S.adsr(n, SR, gate_s=1.0, a=0.01, d=0.2, s=0.8, r=0.15)
    clips = [Clip(0.4 * S.patch(f, n, *TARGET) * env, SR), Clip(0.4 * S.patch(f, n, fit["cutoff"], fit["res"], fit["mix"]) * env, SR)]
    answers = []
    for i in range(3):
        m = 2093.0 * 2 ** (int(rng.integers(0, 12)) / 12)
        if rng.random() < 0.5:
            clips.append(Clip(0.25 * S.saw_naive(m, n) * env, SR))
            answers.append("naive")
        else:
            clips.append(Clip(0.25 * S.saw_polyblep(m, n) * env, SR))
            answers.append("PolyBLEP")
    lab.audio = concat(clips, gap=0.6)
    lab.row("ear problem: the last three are naive or PolyBLEP (listen first)", ", ".join(answers))

    fig, (ax1, ax2) = labs.figure(2)
    for k, c in zip(rows, ("C3", "C1", labs.GOLD)):
        ax1.plot([1, 2, 4], rows[k], "o-", color=c, label=k)
    ax1.set_xscale("log", base=2)
    ax1.set_xlabel("times 48 kHz")
    ax1.set_ylabel("error, dB")
    ax1.legend(fontsize=7)
    ht = S.harmonic_levels(tgt, f)
    hf = S.harmonic_levels(S.patch(f, 8192, fit["cutoff"], fit["res"], fit["mix"]), f)
    j = np.arange(1, len(ht) + 1) / 2
    ax2.stem(j - 0.08, ht, linefmt="C7-", markerfmt="C7o", basefmt=" ", bottom=-60)
    ax2.stem(j + 0.08, hf, linefmt="C3-", markerfmt="C3o", basefmt=" ", bottom=-60)
    ax2.set_xlabel("multiple of the note")
    ax2.set_ylabel("dB")
    lab.fig = fig
    lab.note = ("A naive sawtooth's drop between samples folds harmonics back; a band-limited step at each jump cuts them. "
                "The ladder's circuit converges at 6 dB per doubling by forward steps and 12 by the trapezoid. A patch is "
                "found by a distance and a search, and a distance can only say a sound is out of reach, not why.")
    return lab

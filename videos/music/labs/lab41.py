"""Lab 41: orchestration, computed: instruments resynthesised from measured spectra, fusion on a harmonic series,
sections, the roughness of spacings, and a solver that spells a target spectrum with instruments."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import orchestra as O

TITLE = "Orchestration, computed"
GOAL = ("Put instruments on each other's harmonics and measure how well they fuse; voice a chord and measure its "
        "roughness; and ask the solver to orchestrate a target of your choosing.")
TASKS = [
    "Edit COMBO (instrument, key number, level in dB). Which combinations fuse above 99%? Detune one by a semitone.",
    "Change VOICING. Find the lowest close-position triad whose roughness is below the open voicing's.",
    "Change FORMANTS (the target vowel) and BUDGET. How many instruments does the error need to fall below 10 dB?",
]
COMBO = [("horn", 60, 0.0), ("celesta", 84, -8.0), ("piccolo", 79, -11.0), ("piccolo", 88, -13.0)]
VOICING = [48, 52, 55]
FORMANTS = (730.0, 1090.0, 2440.0)        # 'ah'; try (270, 2290, 3010) for 'ee'
BUDGET = 4


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    f0 = O.hz(COMBO[0][1])
    fus = O.fusion([(n, m, 10 ** (g / 20)) for n, m, g in COMBO], f0, cents=20)
    assert 0.0 <= fus <= 1.0
    lab.row("COMBO: share of power within 20 cents of the melody's harmonic series", f"{fus:.1%}")
    for n, m, _ in COMBO[1:]:
        k = 2 ** ((m - COMBO[0][1]) / 12)
        lab.row(f"  {n} on key {m}: frequency ratio to the melody", f"{k:.3f} (nearest harmonic {max(1, round(k))})")
    def bright(combo):
        ps = [p for n, m, g in combo for p in O.partials(n, m, 10 ** (g / 20))]
        return sum(f * a * a for f, a in ps) / sum(a * a for _, a in ps)
    lab.row("COMBO: brightness (spectral centroid) of the melody alone / of the whole (Hz)", f"{bright(COMBO[:1]):.0f} / {bright(COMBO):.0f}")
    r = O.voicing_roughness(VOICING)
    lab.row(f"VOICING {VOICING}: roughness on strings (open C-G-E is {O.voicing_roughness([36, 43, 52]):.2f})", f"{r:.2f}")
    tgt = O.vowel_target(FORMANTS, f0=130.81)
    res = O.match(tgt, 130.81, budget=BUDGET)
    lab.row("solver: candidates, then error by number of instruments (dB a band)",
            f"{res['candidates']}; " + ", ".join(f"{k}: {v:.1f}" for k, v in res["error_by_size"].items()))
    lab.row("solver: the best group", "; ".join(f"{c['instrument']} on harmonic {c['harmonic']}" for c in res["chosen"]))

    # sound: the combination, then the solver's match; ear problem: sections of random sizes, level-matched
    beat = 0.5
    mel = [(0, 0.0, 1.0), (0, 1.0, 1.0), (7, 2.0, 1.0), (7, 3.0, 1.0), (9, 4.0, 1.0), (9, 5.0, 1.0), (7, 6.0, 2.0)]
    parts = []
    for n, m, g in COMBO:
        for dm, a, d in mel:
            parts.append((Clip(O.note(n, m + dm, d * beat * 0.97), SR), a * beat, g))
    combo = Clip(mix(parts, duration=8 * beat + 0.6).y, SR).at_level(-20.0)
    match = Clip(mix([(Clip(O.note(c["instrument"], c["key"], 2.0), SR), 0.0, 20 * np.log10(max(c["gain"], 1e-4))) for c in res["chosen"]],
                     duration=2.4).y, SR).at_level(-20.0)
    sizes, clips = [], []
    for i in range(3):
        k = int(rng.choice([1, 3, 12]))
        clips.append(Clip(O.section("violin", 67, 2.0, players=k, seed=10 + i), SR).at_level(-20.0))
        sizes.append(str(k))
    lab.audio = concat([combo, match] + clips, gap=0.8)
    lab.row("ear problem: players in each held G4, in order (listen first)", ", ".join(sizes))

    fig, (ax1, ax2) = labs.figure(2)
    cols = [labs.GOLD, "#60A5FA", "#F472B6", "#A3E635", "#22D3EE", "#F59E0B"]
    for j, (n, m, g) in enumerate(COMBO):
        ps = [p for p in O.partials(n, m, 10 ** (g / 20)) if p[0] / f0 < 17]
        ax1.vlines([p[0] / f0 + 0.12 * j for p in ps], -60, [max(-60, 20 * np.log10(p[1] + 1e-9)) for p in ps], lw=3,
                   color=cols[j % len(cols)], label=f"{n} (key {m})")
    ax1.set_xlabel("frequency / melody's fundamental")
    ax1.set_ylabel("dB")
    ax1.set_title(f"COMBO's partials: {fus:.1%} on one series")
    ax1.legend(fontsize=7)
    e = O.ERB_EDGES
    c = np.sqrt(e[1:] * e[:-1])
    tb = np.array(res["target_bands"])
    ax2.semilogx(c, 10 * np.log10(tb / tb.max() + 1e-6), color=labs.GOLD, label="target")
    approx = sum(O.band_power(O.partials(ch["instrument"], ch["key"], np.sqrt(max(ch["gain"], 0)))) for ch in res["chosen"])
    ax2.semilogx(c, 10 * np.log10(approx / max(approx.max(), 1e-12) + 1e-6), color="C0", label=f"best {BUDGET}")
    ax2.set_ylim(-50, 3)
    ax2.set_xlabel("Hz")
    ax2.set_title("band power: the target and the match")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("An instrument on a harmonic of another adds only partials the series already has, so they fuse; the "
                "solver fits loudnesses by nonnegative least squares and keeps the best small group.")
    return lab

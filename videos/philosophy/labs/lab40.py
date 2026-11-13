"""Lab 40: find the consonant intervals as dips in a roughness curve, then stretch the timbre and watch them move."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import aesthetics

TITLE = "Where consonance comes from, and when a panel of critics converges"
GOAL = ("Compute the Pythagorean comma, build the dissonance curve of two harmonic tones and check that its dips sit "
        "on 6:5, 5:4, 4:3, 3:2, 5:3 and 2:1, then stretch the partials by a random amount and check that every dip "
        "moves to the stretched ratio. Then average panels of simulated critics with and without a shared prejudice.")
TASKS = [
    "Call aesthetics.dissonance_curve with n_partials=1 (pure tones). Which of the six dips survive, and what does "
    "that say about consonance as a property of ratios?",
    "Raise the look-elsewhere tolerance in aesthetics.golden from 3% to 5% and the number of lengths from 8 to 12. "
    "How often does a random building now contain the golden ratio?",
    "Give the prejudiced judges a shared bias of 0.5 instead of 1.2 (edit the kinds in aesthetics.critics). What "
    "does their panel's correlation with quality converge to, against 1 / sqrt(1 + 0.25)?",
]
JUST = {"6:5": 6 / 5, "5:4": 5 / 4, "4:3": 4 / 3, "3:2": 3 / 2, "5:3": 5 / 3, "2:1": 2.0}


def _worst_gap(minima, exponent, top):
    """The largest distance, in cents, from a predicted dip (a just ratio raised to the exponent) to a dip found."""
    found = [m["ratio"] for m in minima if 1.05 < m["ratio"] < top]
    return max(min(abs(aesthetics.cents(f / r ** exponent)) for f in found) for r in JUST.values()), len(found)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    t = aesthetics.tuning()
    fifth = next(e for e in t["equal"] if e["interval"] == "fifth")
    lab.row("twelve fifths against seven octaves", f"{t['comma_num']}/{t['comma_den']} = {t['comma_cents']:.2f} cents   (film: 23.46)")
    lab.row("equal temperament's fifth", f"{fifth['error']:+.2f} cents from 3:2")
    assert (t["comma_num"], t["comma_den"]) == (3 ** 12, 2 ** 19) and t["comma_num"] != t["comma_den"]
    assert abs(t["comma_cents"] - 1200 * math.log2(1.5 ** 12 / 2 ** 7)) < 0.01 and abs(fifth["error"] + 1.96) < 0.01

    harmonic = aesthetics.dissonance_curve()
    gap, n_found = _worst_gap(harmonic["minima"], 1.0, 2.05)
    lab.row("harmonic tones: dips found between 1 and 2", f"{n_found}, each within {gap:.1f} cents of a just ratio   (film: exactly six)")
    assert n_found == 6 and gap < 2.0 and harmonic["lowest_after_unison"] == 2.0

    stretch = round(float(rng.uniform(1.9, 2.2)), 3)
    stretched = aesthetics.dissonance_curve(stretch=stretch)
    exponent = math.log2(stretch)
    gap_s, n_s = _worst_gap(stretched["minima"], exponent, stretch * 1.02)
    lab.row(f"partials stretched to an 'octave' of {stretch}", f"{n_s} dips, each within {gap_s:.1f} cents of (p/q)^{exponent:.3f}")
    lab.row("... its deepest dip after the unison", f"{stretched['lowest_after_unison']:.3f}   (theory: {stretch})")
    assert n_s == 6 and gap_s < 4.0, "the dips follow the partials, not the whole-number ratios"
    assert abs(stretched["lowest_after_unison"] - stretch) < 0.003
    if abs(stretch - 2) > 0.03:
        assert all(abs(aesthetics.cents(m["ratio"] / 2.0)) > 10 for m in stretched["minima"]), "2:1 is no longer a dip"

    w = aesthetics.wallpaper()
    lab.row("wallpaper groups built and told apart", f"{len(w['groups'])} built, {w['distinct']} distinct names   (Fedorov: 17)")
    assert len(w["groups"]) == 17 and w["distinct"] == 17 and w["all_seventeen"]

    gold = aesthetics.golden(trials=6000, seed=1876 + seed)
    lab.row("random 'buildings' with a golden ratio within 3%", f"{gold['p_some_hit']:.0%}   (film: 70%)")
    assert abs(gold["p_some_hit"] - 0.70) < 0.04

    panel = aesthetics.critics(panels=(1, 4, 16, 64), trials=80, seed=1757 + seed)["correlation"]
    limit = 1 / math.sqrt(1 + 1.2 ** 2)
    lab.row("64 true judges: correlation with quality", f"{panel['true judges'][-1]:.3f}   (film: 0.998)")
    lab.row("64 judges with a shared prejudice", f"{panel['prejudiced judges'][-1]:.3f}   (theory: about 1/sqrt(1 + 1.2^2) = {limit:.3f})")
    assert panel["true judges"][-1] > 0.99 and panel["novices"][-1] > panel["novices"][0] + 0.3
    assert abs(panel["prejudiced judges"][-1] - limit) < 0.05, "averaging removes noise, not a shared bias"
    assert panel["prejudiced judges"][-1] - panel["prejudiced judges"][0] < 0.08
    lab.note = ("Consonance sits where partials coincide, so it belongs to the timbre as much as to the ratio. And "
                "a panel's average converges on quality only when its members' errors are independent.")

    fig, ax = labs.figure(2, size=(11.5, 4.3))
    ax[0].plot(harmonic["r"], harmonic["d"], color=labs.BLUE, label="harmonic partials")
    ax[0].plot(stretched["r"], stretched["d"], color=labs.ORANGE, label=f"stretched: 'octave' = {stretch}")
    for k, (name, r) in enumerate(JUST.items()):
        ax[0].axvline(r, color=labs.MUTED, lw=0.8, ls=":")
        ax[0].text(r, 1.03 + 0.07 * (k % 2), name, ha="center", fontsize=8, color=labs.MUTED)
    ax[0].set(title="Roughness of two tones against their interval", xlabel="frequency ratio", ylabel="roughness (1 = the peak)",
              ylim=(0, 1.17))
    ax[0].legend(loc="upper right", bbox_to_anchor=(1, 0.9))
    sizes = [1, 4, 16, 64]
    for kind, color in (("true judges", labs.GREEN), ("novices", labs.BLUE), ("prejudiced judges", labs.RED)):
        ax[1].plot(sizes, panel[kind], "o-", color=color, label=kind)
    ax[1].axhline(limit, color=labs.RED, ls="--", lw=1, label="the prejudice's ceiling")
    ax[1].set(title="Hume's panel, as an analogy", xlabel="critics on the panel", xscale="log", xticks=sizes,
              xticklabels=[str(s) for s in sizes], ylabel="correlation of the average verdict with quality", ylim=(0.4, 1.02))
    ax[1].legend(loc="center right")
    lab.fig = fig
    return lab

"""Lab 25: measure triangles in the Poincaré disk, boost events, and recover a spacetime's dimension from order."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import spacetime as st

TITLE = "Geometry from measurement, dimension from order"
GOAL = ("Draw random triangles in the Poincaré disk and check their angle sums against the hyperbolic law of "
        "cosines, find the boost that puts a spacelike event in the present, and sprinkle 400 events into flat "
        "spacetime of 2, 3 and 4 dimensions to recover the dimension from the causal order alone.")
TASKS = [
    "Raise the sprinkling to n = 1600 events (st.causal_set(n=1600, seed=seed), a few seconds). By how much does "
    "the dimension estimate's error shrink?",
    "Make the event timelike, for example (1.0, 0.6), and call st.rietdijk_putnam on it. What speed would the "
    "boost need, and why does the Lorentz transformation fail there?",
    "Solve a new circuit with st.deutsch_fixed_point: a Hadamard on the time-travelling qubit instead of a NOT. "
    "Is the fixed point unique?",
]


def _cosine_sum(P):
    """The angle sum of the hyperbolic triangle P, in degrees, from its three side lengths."""
    a, b, c = st.hyp_dist(P[1], P[2]), st.hyp_dist(P[0], P[2]), st.hyp_dist(P[0], P[1])

    def ang(a, b, c):
        return math.acos((math.cosh(b) * math.cosh(c) - math.cosh(a)) / (math.sinh(b) * math.sinh(c)))

    return math.degrees(ang(a, b, c) + ang(b, c, a) + ang(c, a, b))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. triangles: the library reads angles off the drawn arcs; the law of cosines reads them off distances
    drawn, theory, size = [], [], []
    while len(drawn) < 40:
        P = rng.uniform(-0.8, 0.8, (3, 2))
        d1, d2 = P[1] - P[0], P[2] - P[0]
        if max(np.hypot(*p) for p in P) > 0.85 or abs(d1[0] * d2[1] - d1[1] * d2[0]) < 0.05:
            continue
        t = st.hyp_triangle(*map(tuple, P))
        drawn.append(t["sum_deg"])
        theory.append(_cosine_sum(P))
        size.append(max(t["lengths"]))
    drawn, theory, size = np.array(drawn), np.array(theory), np.array(size)
    gap = float(np.abs(drawn - theory).max())
    lab.row("40 random triangles: angle sums", f"{drawn.min():.1f} to {drawn.max():.1f} degrees   (Euclid: 180)")
    lab.row("drawn arcs against the law of cosines", f"largest gap {gap:.2f} degrees")
    assert theory.max() < 180 and drawn.max() < 180 + gap, "every hyperbolic triangle falls short of two right angles"
    assert gap < 4.0, "angles read off the arcs agree with angles computed from the distances"
    rows = st.disk_triangles()["rows"]
    lab.row("centred triangles, vertex radius 0.1 to 0.9", f"sums {rows[0]['sum_deg']} to {rows[-1]['sum_deg']} "
            f"degrees, areas {rows[0]['area']} to {rows[-1]['area']}   (limit pi = {math.pi:.4f})")
    assert all(a["area"] < b["area"] < math.pi for a, b in zip(rows, rows[1:])), "the area is the defect, below pi"

    # 2. the Rietdijk-Putnam boost, and the interval it leaves alone
    kept = 0
    for _ in range(200):
        x = rng.uniform(0.5, 3) * rng.choice([-1, 1])
        t = rng.uniform(-0.95, 0.95) * abs(x)
        rp = st.rietdijk_putnam((t, x))
        tp, xp = st.lorentz(t / x, [(t, x)])[0]
        assert rp["spacelike"] and abs(rp["t_prime"]) < 1e-9, "the boost v = t/x puts the event in the present"
        assert abs((tp * tp - xp * xp) - (t * t - x * x)) < 1e-9, "the interval is the same in both frames"
        kept += 1
    order = [st.lorentz(v, [(2.0, 0.5)])[0][0] > 0 for v in np.linspace(-0.99, 0.99, 199)]
    lab.row("200 spacelike events", f"{kept} made simultaneous with here-now by v = t/x, interval unchanged")
    lab.row("a timelike event (2, 0.5) in 199 frames", f"later than here-now in {sum(order)}")
    assert all(order), "no boost reverses the order of timelike-separated events"

    # 3. a causal set: dimension from the fraction of related pairs
    cs = st.causal_set(n=400, seed=seed)
    for r in cs["rows"]:
        lab.row(f"sprinkling in {r['d']} dimensions", f"related pairs {r['fraction']:.3f} (theory {r['theory']:.3f}), "
                f"estimated dimension {r['estimate']:.2f}")
        assert abs(r["estimate"] - r["d"]) < 0.45, "the order alone recovers the dimension"
    lab.note = ("Angle sums below 180 degrees are measurable facts about the disk; which events are simultaneous is "
                "frame-relative for spacelike pairs only; and the fraction of causally related pairs carries the "
                "dimension, with no coordinates kept.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].scatter(size, drawn, s=22, color=labs.BLUE, label="read off the drawn arcs")
    ax[0].scatter(size, theory, s=22, facecolors="none", edgecolors=labs.GOLD, label="law of cosines")
    ax[0].axhline(180, color=labs.MUTED, ls="--", lw=1)
    ax[0].text(size.max(), 188, "Euclid: 180", color=labs.MUTED, va="center", ha="right")
    ax[0].set(title="Hyperbolic triangles: larger means a smaller angle sum", xlabel="longest side (hyperbolic length)",
              ylabel="angle sum (degrees)", ylim=(0, 196))
    ax[0].legend(loc="lower left")
    ds = np.linspace(1.6, 4.6, 80)
    ax[1].plot(ds, [st.ordering_fraction(d) for d in ds], color=labs.MUTED, label="Myrheim-Meyer formula")
    ax[1].scatter([r["d"] for r in cs["rows"]], [r["fraction"] for r in cs["rows"]], s=60, color=labs.GOLD, zorder=3,
                  label="400 sprinkled events")
    for r in cs["rows"]:
        ax[1].annotate(f"estimate {r['estimate']:.2f}", (r["d"], r["fraction"]), xytext=(8, 8),
                       textcoords="offset points", color=labs.INK)
    ax[1].set(title="Dimension from causal order alone", xlabel="dimension of the spacetime",
              ylabel="fraction of related pairs")
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab

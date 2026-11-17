"""Lab 7: lesions in a diagram, one resource that fakes two, a map of the visual field, and one patient's score."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import brain as B

TITLE = "Lesions, dissociations, a map and one patient"
GOAL = ("Lesion Wernicke and Lichtheim's diagram and read off three aphasias; reproduce Lashley's mass action in a "
        "model cortex where every job has a place; count how often one damaged resource and noisy tests give a "
        "'double dissociation'; integrate the magnification of the visual cortex and place your blind spot on a "
        "screen; compare one patient with eight controls; and watch an artery pull a lesion map off its target.")
TASKS = [
    "Add a module to the language diagram so that a lesion can spare repetition and abolish understanding (the "
    "task routes are in B.LICHTHEIM.tasks; build a new B.Architecture). Which link did you have to make separate, "
    "and what does the new lesion do to speaking?",
    "In B.dissociations, double the noise of the tests (noise=0.10) and then double the strictness of the cutoff "
    "(cutoff_z=-3). What happens to the chance that a screen of 100 one-resource patients shows both patterns, "
    "and what does the stricter cutoff cost in patients correctly called impaired?",
    "Run B.lesion_study with the critical region moved to (22, 34), further from the trunk, and to (22, 22), next "
    "to it. How does the map's displacement change, and why does distance along the branch matter?",
]


def run(seed=0):
    out = labs.Lab()
    g = np.random.default_rng(seed + 70)

    # 1. the diagram, lesioned
    table = B.LICHTHEIM.table(B.APHASIAS)
    for name, scores in table.items():
        out.row(f"cut {name}: understand, speak, repeat",
                ", ".join(f"{scores[t]:.0f}" for t in ("understand speech", "speak", "repeat")))
    front, back, path = (table[k] for k in table)
    assert front["understand speech"] == 1 and front["speak"] == 0
    assert back["understand speech"] == 0 and back["speak"] == 1
    assert path["understand speech"] == 1 and path["speak"] == 1 and path["repeat"] == 0

    # 2. Lashley's result from a brain in which every job has a place
    one = B.maze_lesions((5,), rng=np.random.default_rng(seed + 71))
    six = B.maze_lesions((0, 2, 4, 6, 8, 10), rng=np.random.default_rng(seed + 71))
    out.row("one place: errors against amount removed, against place hit (r)",
            f"{one['r_size']:.2f}, {one['r_place']:.2f}")
    out.row("six ways: errors against amount removed, against place hit (r)",
            f"{six['r_size']:.2f}, {six['r_place']:.2f}")
    assert one["r_place"] > 0.9 and six["r_size"] > 0.8 and six["r_place"] < 0.4

    # 3. one resource, noisy tests, and a large screen
    quiet = B.dissociations("one", noise=0.0, rng=np.random.default_rng(seed + 72))
    noisy = B.dissociations("one", noise=0.05, rng=np.random.default_rng(seed + 72))
    two = B.dissociations("two", noise=0.05, rng=np.random.default_rng(seed + 72))
    chance = B.chance_of_double(noisy["a_only"], noisy["b_only"], 100)
    out.row("one resource, perfect tests: fail only A, only B", f"{quiet['a_only']:.3f}, {quiet['b_only']:.3f}")
    out.row("one resource, noisy tests: fail only A, only B", f"{noisy['a_only']:.3f}, {noisy['b_only']:.4f}")
    out.row("two resources, noisy tests: fail only A, only B", f"{two['a_only']:.3f}, {two['b_only']:.3f}")
    out.row("chance a screen of 100 one-resource patients shows both", f"{chance:.2f}")
    assert quiet["b_only"] == 0 and 0 < noisy["b_only"] < 0.02 and 0.3 < chance < 0.7 and two["b_only"] > 0.1

    # 4. the map of the visual field, and the blind spot
    out.row("mm of cortex per degree at 0, 1, 10, 40 degrees",
            ", ".join(f"{float(B.magnification(e)):.1f}" for e in (0, 1, 10, 40)))
    out.row("cortical distance to 1 and to 8 degrees (mm)",
            f"{float(B.cortical_distance(1.0)):.1f}, {float(B.cortical_distance(8.0)):.1f}")
    out.row("share of the map within 1 and within 10 degrees",
            f"{float(B.area_share(1.0)):.2f}, {float(B.area_share(10.0)):.2f}")
    spot = B.blind_spot(57.0)
    out.row("blind spot on a screen at 57 cm: from, to, width (cm)",
            f"{spot['near']:.1f}, {spot['far']:.1f}, {spot['width']:.1f}")
    assert abs(float(B.cortical_distance(8.0)) - 17.3 * np.log(1 + 8 / 0.75)) < 1e-9
    assert 0.4 < float(B.area_share(10.0)) < 0.5 and 5 < spot["width"] < 7

    # 5. one patient against eight controls
    controls = np.array([34.0, 31.0, 38.0, 29.0, 35.0, 33.0, 36.0, 30.0])
    ch = B.crawford_howell(24.0, controls)
    from scipy import stats

    out.row("patient 24 against eight controls: z, and 1 in", f"{ch['z']:.2f}, {1 / stats.norm.cdf(ch['z']):.0f}")
    out.row("... the single-case t on 7 df, and 1 in", f"{ch['t']:.2f}, {1 / ch['p']:.0f}")
    out.row("a healthy person fails at least one of 10, of 20 tests", f"{1 - 0.95 ** 10:.2f}, {1 - 0.95 ** 20:.2f}")
    assert abs(ch["t"] - ch["z"] / np.sqrt(9 / 8)) < 1e-9 and ch["p"] > 5 * stats.norm.cdf(ch["z"])

    # 6. a lesion map, with and without an artery
    art = [B.lesion_study(rng=np.random.default_rng(seed + 700 + k)) for k in range(12)]
    any_ = [B.lesion_study(rng=np.random.default_rng(seed + 700 + k), vascular=False) for k in range(12)]
    d_art, d_any = np.mean([s["displacement"] for s in art]), np.mean([s["displacement"] for s in any_])
    toward = np.mean([s["shift"][1] for s in art])
    out.row("map's centre off target, 12 studies: with an artery, lesions anywhere (voxels)",
            f"{d_art:.1f}, {d_any:.1f}")
    out.row("... mean shift toward the trunk, with an artery (voxels)", f"{-toward:.1f}")
    assert d_art > d_any and toward < 0
    out.note = ("A diagram of boxes and arrows makes predictions: cut one link and one task fails. A task that can "
                "be done several ways hides where its parts are. One resource and noisy tests give the occasional "
                "patient who looks like the reverse case, and a large screen finds one about half the time. The "
                "visual cortex gives the ten degrees around the centre of gaze nearly half its area. Against eight controls a "
                "z-score overstates how rare a patient is by a factor of about nine. And a lesion map is pulled "
                "toward the artery, because damage upstream goes with damage downstream.")

    one_study = art[0]
    fig, ax = labs.figure(2, size=(11, 4.4))
    ecc = np.linspace(0, 40, 400)
    ax[0].plot(ecc, [float(B.area_share(e)) for e in ecc], color=labs.GREEN, lw=2)
    ax[0].axvline(10, color=labs.GREY, lw=1, ls="--")
    ax[0].set(title="Share of the visual map within a given distance of the centre of gaze",
              xlabel="eccentricity (degrees)", ylabel="share of the map", ylim=(0, 1))
    im = np.nan_to_num(one_study["tmap"], nan=0.0)
    ax[1].imshow(im, origin="lower", cmap="magma")
    ax[1].contour(one_study["critical"].astype(float), levels=[0.5], colors="white", linewidths=1.5)
    ax[1].plot(*one_study["centre"], "+", color=labs.PINK, ms=14, mew=2.5)
    ax[1].axhline(20, color="white", lw=0.8, ls=":")
    ax[1].set(title="A lesion map: the region that matters (ring) and where the map points (+)",
              xlabel="voxel", ylabel="voxel")
    out.fig = fig
    return out

"""The brain as parts that can be damaged: what a lesion can and cannot tell you (videos/psychology/SYLLABUS.md,
Part 7).

**A box-and-arrow architecture.**  A :class:`Architecture` is a set of modules and, for each task, the modules the
task passes through.  A lesion lowers a module's capacity, and a task's performance is the product of the
capacities on its route, scaled between chance and ceiling.  Two architectures are given: Wernicke and
Lichtheim's diagram of language (:data:`LICHTHEIM`), which predicted a syndrome nobody had yet described, and a
memory architecture in which new facts, old facts, a short span and a skill use different parts
(:data:`MEMORY`).

**Lashley's result.**  :func:`maze_lesions` removes blocks of a model cortex in which every job has its own
place, and tests a task that needs one place or one that can be done several ways: with several, the damage
that matters is how much, not where ("mass action"), though nothing in the model is spread out.

**The logic of dissociation.**  A patient who fails task A and passes task B does not show that A and B use
different parts: if both draw on one resource and A needs more of it, every patient fails A first.  The reverse
patient would show it, in a world without noise.  :func:`dissociations` simulates patients under a one-resource
and a two-resource model, classifies each against controls, and counts how often a screen of N patients turns up
both patterns: with noisy tests, a single resource produces "double dissociations" too.

**One patient against a small control sample.**  :func:`crawford_howell` is the modified t-test that treats the
control mean and standard deviation as estimates (Crawford and Howell 1998), the working tool of single-case
neuropsychology.

**Maps.**  The cortical magnification of human primary visual cortex, M(E) = 17.3 / (E + 0.75) mm per degree
(Horton and Hoyt 1991), its integral along a meridian, and the area given to the centre of gaze; the geometry of
the blind spot on a screen.

**Lesion-symptom mapping.**  :func:`lesion_study` makes strokes that spread from an arterial trunk across a
sheet of cortex, lets a deficit depend on one small region, and maps the deficit voxel by voxel.  Because
damage upstream goes with damage downstream, the peak of the map is displaced from the region that matters.

Nothing here imports manim.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy import stats

# ---------------------------------------------------------------------------------------------------------------
# A box-and-arrow architecture
# ---------------------------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Architecture:
    """Modules, and for each task the modules on its route (all are needed)."""

    modules: tuple
    tasks: dict
    chance: dict = field(default_factory=dict)

    def performance(self, lesion: dict | None = None) -> dict:
        """Each task's score, 0 to 1: chance plus (1 - chance) times the product of the capacities on its
        route.  ``lesion`` maps a module to the share of it destroyed."""
        lesion = lesion or {}
        unknown = set(lesion) - set(self.modules)
        if unknown:
            raise KeyError(f"no such module: {sorted(unknown)}")
        out = {}
        for task, route in self.tasks.items():
            cap = math.prod(1.0 - float(lesion.get(m, 0.0)) for m in route)
            c = self.chance.get(task, 0.0)
            out[task] = c + (1 - c) * cap
        return out

    def impaired(self, lesion: dict, cutoff: float = 0.5) -> tuple:
        """The tasks a lesion brings below ``cutoff``."""
        return tuple(t for t, p in self.performance(lesion).items() if p < cutoff)

    def table(self, lesions: dict) -> dict:
        """Performance on every task for each named lesion (a dict of dicts)."""
        return {name: self.performance(les) for name, les in lesions.items()}

    def dissociates(self, task_a: str, task_b: str) -> dict:
        """Which single complete lesions impair A and spare B, and which do the reverse."""
        a_only, b_only = [], []
        for m in self.modules:
            hit = self.impaired({m: 1.0})
            if task_a in hit and task_b not in hit:
                a_only.append(m)
            if task_b in hit and task_a not in hit:
                b_only.append(m)
        return {"a_only": tuple(a_only), "b_only": tuple(b_only), "double": bool(a_only and b_only)}


# Wernicke (1874) and Lichtheim (1885): a centre for the sound images of words (A), a centre for the motor images
# of words (M), a pathway between them, and the store of concepts (B) connected to both.
LICHTHEIM = Architecture(
    modules=("hearing", "word sounds", "pathway", "word movements", "articulation", "concepts"),
    tasks={
        "understand speech": ("hearing", "word sounds", "concepts"),
        "speak": ("concepts", "word movements", "articulation"),
        "repeat": ("hearing", "word sounds", "pathway", "word movements", "articulation"),
    },
)
APHASIAS = {
    "word movements (Broca's area)": {"word movements": 1.0},
    "word sounds (Wernicke's area)": {"word sounds": 1.0},
    "the pathway between them": {"pathway": 1.0},
}

# Memory after H.M.: what was removed (the hippocampal system) is needed to lay down new facts and events, and
# for nothing else on this list.
MEMORY = Architecture(
    modules=("hippocampal system", "cortical stores", "working span", "skill system"),
    tasks={
        "recall today tomorrow": ("hippocampal system", "cortical stores"),
        "recall childhood": ("cortical stores",),
        "repeat seven digits": ("working span",),
        "learn mirror tracing": ("skill system",),
    },
)

# ---------------------------------------------------------------------------------------------------------------
# Lashley's result from a localized brain
# ---------------------------------------------------------------------------------------------------------------


def maze_lesions(routes=(5,), animals: int = 400, regions: int = 12, noise: float = 4.0, rng=None) -> dict:
    """Rats with a block of cortex removed, tested on a maze.

    The model brain is a row of ``regions`` pieces, each with its own job.  The maze can be solved by any of the
    strategies in ``routes`` (one region each); the animal's errors rise with the share of those strategies it
    has lost.  With one route the task has one place; with several, spread out, it has many.  Each lesion is a
    run of 1 to 7 adjacent regions at a random position.  Returns each animal's lesion size, whether it took
    region ``routes[0]``, its errors, and how well the errors are predicted by size and by place."""
    rng = rng or np.random.default_rng(0)
    routes = np.asarray(routes)
    size = rng.integers(1, 8, animals)
    start = np.array([rng.integers(0, regions - s + 1) for s in size])
    cut = (np.arange(regions)[None, :] >= start[:, None]) & (np.arange(regions)[None, :] < (start + size)[:, None])
    lost = cut[:, routes].mean(axis=1)
    errors = np.maximum(10 + 60 * lost + noise * rng.standard_normal(animals), 0)
    hit = cut[:, routes[0]]
    r_size = float(np.corrcoef(size, errors)[0, 1])
    r_place = float(np.corrcoef(hit, errors)[0, 1])
    # within lesions of one size, how much do errors still depend on where the lesion was?
    within = [float(errors[size == k].std()) for k in range(1, 8)]
    return {"size": size / regions, "hit": hit, "errors": errors, "r_size": r_size, "r_place": r_place,
            "spread_within_size": float(np.mean(within)), "start": start, "regions": regions}


# ---------------------------------------------------------------------------------------------------------------
# Dissociations with noisy tests
# ---------------------------------------------------------------------------------------------------------------


def _score(resource, threshold, slope):
    return stats.norm.cdf((np.asarray(resource, float) - threshold) / slope)


def dissociations(model: str = "one", patients: int = 20_000, noise: float = 0.05, control_sd: float = 0.05,
                  cutoff_z: float = -2.0, rng=None, thresholds=(0.55, 0.35), slope: float = 0.12) -> dict:
    """Simulated patients tested on tasks A and B against a control distribution.

    ``model="one"``: both tasks draw on one resource R (what a lesion leaves, uniform on 0..1); A needs more of
    it than B.  ``model="two"``: each task has its own resource, damaged independently.  Controls have the whole
    resource and their scores spread with standard deviation ``control_sd``; a patient is impaired on a task
    when the measured score falls ``cutoff_z`` of those standard deviations below the controls' mean.  The
    measured score is the true one plus normal noise of standard deviation ``noise`` (one testing session).
    Returns the share of patients with A impaired alone, B impaired alone, both, and neither."""
    rng = rng or np.random.default_rng(0)
    if model == "one":
        r = rng.uniform(0, 1, patients)
        ra, rb = r, r
    elif model == "two":
        ra, rb = rng.uniform(0, 1, patients), rng.uniform(0, 1, patients)
    else:
        raise ValueError(model)
    a = _score(ra, thresholds[0], slope) + noise * rng.standard_normal(patients)
    b = _score(rb, thresholds[1], slope) + noise * rng.standard_normal(patients)
    ca, cb = _score(1.0, thresholds[0], slope), _score(1.0, thresholds[1], slope)
    ia, ib = (a - ca) / control_sd < cutoff_z, (b - cb) / control_sd < cutoff_z
    return {"a_only": float(np.mean(ia & ~ib)), "b_only": float(np.mean(~ia & ib)), "both": float(np.mean(ia & ib)),
            "neither": float(np.mean(~ia & ~ib)), "a": a, "b": b, "impaired_a": ia, "impaired_b": ib,
            "resource_a": ra, "resource_b": rb}


def chance_of_double(share_a_only: float, share_b_only: float, screened: int) -> float:
    """The chance that a screen of ``screened`` patients contains at least one of each single dissociation."""
    pa, pb = share_a_only, share_b_only
    n = screened
    return float(1 - (1 - pa) ** n - (1 - pb) ** n + (1 - pa - pb) ** n)


def crawford_howell(case: float, controls) -> dict:
    """One patient's score against a small control sample: t = (x - mean) / (s sqrt((n + 1) / n)) on n - 1
    degrees of freedom (Crawford and Howell 1998).  Returns t, the one-tailed p for a deficit, and the estimated
    share of the control population scoring below the patient."""
    c = np.asarray(controls, float)
    n = len(c)
    if n < 2:
        raise ValueError("at least two controls")
    t = (case - c.mean()) / (c.std(ddof=1) * math.sqrt((n + 1) / n))
    p = float(stats.t.cdf(t, n - 1))
    return {"t": float(t), "df": n - 1, "p": p, "below": p, "z": float((case - c.mean()) / c.std(ddof=1))}


# ---------------------------------------------------------------------------------------------------------------
# Maps
# ---------------------------------------------------------------------------------------------------------------
M0, E2 = 17.3, 0.75  # Horton and Hoyt (1991): mm of cortex per degree at eccentricity E is M0 / (E + E2)


def magnification(ecc_deg):
    """Millimetres of primary visual cortex per degree of visual field at eccentricity ``ecc_deg``."""
    return M0 / (np.asarray(ecc_deg, float) + E2)


def cortical_distance(ecc_deg):
    """Millimetres of cortex between the centre of gaze and eccentricity ``ecc_deg``, along a meridian."""
    return M0 * np.log1p(np.asarray(ecc_deg, float) / E2)


def cortical_area(ecc_deg):
    """Square millimetres of one hemisphere's primary visual cortex given to its half of the field out to
    ``ecc_deg`` (areal magnification M^2, integrated over the half disc)."""
    e = np.asarray(ecc_deg, float)
    return math.pi * M0 ** 2 * (np.log((e + E2) / E2) - e / (e + E2))


def area_share(ecc_deg, field_deg: float = 90.0):
    """The share of the map out to ``field_deg`` that lies within ``ecc_deg`` of the centre of gaze."""
    return cortical_area(ecc_deg) / cortical_area(field_deg)


def screen_offset(angle_deg, distance):
    """How far from the fixation mark, on a flat screen at ``distance``, a point ``angle_deg`` away lies."""
    return distance * np.tan(np.radians(angle_deg))


def blind_spot(distance: float, centre_deg: float = 15.0, width_deg: float = 5.5) -> dict:
    """Where the blind spot of an eye fixating a mark falls on a screen at ``distance`` (same units)."""
    lo, hi = centre_deg - width_deg / 2, centre_deg + width_deg / 2
    return {"near": float(screen_offset(lo, distance)), "centre": float(screen_offset(centre_deg, distance)),
            "far": float(screen_offset(hi, distance)), "width": float(screen_offset(hi, distance) - screen_offset(lo, distance))}


# ---------------------------------------------------------------------------------------------------------------
# Lesion-symptom mapping
# ---------------------------------------------------------------------------------------------------------------


def _territories(size: int, branches) -> tuple:
    """Assign each voxel of the sheet to the trunk (a band along the middle row) or to the nearest branch, with
    its distance out along that vessel."""
    mid = size // 2
    yy, xx = np.mgrid[0:size, 0:size]
    bx = np.asarray(branches)
    which = np.abs(xx[..., None] - bx).argmin(axis=-1)  # nearest branch, by column
    on_trunk = np.abs(yy - mid) <= 1
    return yy, xx, mid, which, on_trunk


def lesion_study(patients: int = 400, size: int = 40, critical=(22, 26), radius: float = 3.0, noise: float = 0.5,
                 rng=None, vascular: bool = True, branches=(4, 10, 16, 22, 28, 34)) -> dict:
    """Strokes on a ``size`` x ``size`` sheet, a deficit that depends on one small disc, and a voxelwise map.

    With ``vascular`` the sheet is fed by one artery: a trunk along the middle row, entering at the left, with
    branches running up and down from it.  Each stroke is a blockage at a random point of the tree, and it
    destroys the tissue fed from beyond that point: a blockage on the trunk takes every branch that leaves it
    further along, and a blockage on a branch takes the rest of that branch.  Without ``vascular`` lesions are
    discs anywhere.  The deficit is the share of the critical disc destroyed, plus noise.  The map is the t
    statistic, voxel by voxel, of the deficit in patients with damage there against those without.  Returns the
    lesions' overlap, the map, its peak, the centre of its top twentieth, and how far that centre lies from the
    middle of the critical region."""
    rng = rng or np.random.default_rng(0)
    yy, xx, mid, which, on_trunk = _territories(size, branches)
    bx = np.asarray(branches)
    crit = (xx - critical[0]) ** 2 + (yy - critical[1]) ** 2 <= radius ** 2
    lesions = np.zeros((patients, size, size), bool)
    for k in range(patients):
        if not vascular:
            cx, cy, r = rng.uniform(0, size), rng.uniform(0, size), rng.uniform(3, 9)
            lesions[k] = (xx - cx) ** 2 + (yy - cy) ** 2 <= r ** 2
        elif rng.random() < 0.35:  # a blockage on the trunk, at column x0: everything fed from beyond it
            x0 = rng.uniform(2, size - 2)
            lesions[k] = np.where(on_trunk, xx >= x0, bx[which] >= x0)
        else:  # a blockage on one branch, on one side, at height h0: the rest of that branch
            b, side, h0 = rng.integers(len(bx)), rng.choice((-1, 1)), rng.uniform(1.5, size / 2 - 3)
            lesions[k] = (~on_trunk) & (which == b) & (np.sign(yy - mid) == side) & (np.abs(yy - mid) >= h0)
    deficit = lesions[:, crit].mean(axis=1) + noise * rng.standard_normal(patients)
    n1 = lesions.sum(axis=0)
    n0 = patients - n1
    ok = (n1 >= 10) & (n0 >= 10)
    flat = lesions.reshape(patients, -1).astype(float)
    s1 = flat.T @ deficit
    q1 = flat.T @ deficit ** 2
    tot, tot2 = deficit.sum(), (deficit ** 2).sum()
    n1f, n0f = n1.reshape(-1).astype(float), n0.reshape(-1).astype(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        m1, m0 = s1 / n1f, (tot - s1) / n0f
        v1 = (q1 - n1f * m1 ** 2) / (n1f - 1)
        v0 = ((tot2 - q1) - n0f * m0 ** 2) / (n0f - 1)
        t = (m1 - m0) / np.sqrt(v1 / n1f + v0 / n0f)
    tmap = np.where(ok, t.reshape(size, size), np.nan)
    peak = np.unravel_index(np.nanargmax(tmap), tmap.shape)
    top = tmap >= np.nanquantile(tmap, 0.95)
    cx, cy = float(xx[top].mean()), float(yy[top].mean())
    inside = float(np.mean(crit[top]))
    return {"overlap": n1 / patients, "tmap": tmap, "critical": crit, "peak": (int(peak[1]), int(peak[0])),
            "centre": (cx, cy), "displacement": float(math.hypot(cx - critical[0], cy - critical[1])),
            "shift": (float(cx - critical[0]), float(cy - critical[1])), "top": top, "top_inside": inside,
            "deficit": deficit, "lesions": lesions}

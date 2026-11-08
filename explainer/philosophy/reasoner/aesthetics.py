"""Aesthetics for Part 40 ("Beauty"): Pythagorean tuning and equal temperament; sensory roughness and the
dissonance curve (Plomp and Levelt 1965, in Sethares's parametrization); the seventeen wallpaper groups, generated
from their symmetry operations and classified by a flowchart; compression as a measure of order; the golden-ratio
look-elsewhere effect; and a panel of Hume's critics, as an analogy."""

from __future__ import annotations

import itertools
import math
import zlib

import numpy as np


# ---------------------------------------------------------------------------
# Tuning
# ---------------------------------------------------------------------------
def cents(r: float) -> float:
    return 1200 * math.log2(r)


JUST = {"octave": (2, 1), "fifth": (3, 2), "fourth": (4, 3), "major third": (5, 4), "minor third": (6, 5),
        "major sixth": (5, 3)}
SEMITONES = {"octave": 12, "fifth": 7, "fourth": 5, "major third": 4, "minor third": 3, "major sixth": 9}


def tuning() -> dict:
    """Stack twelve perfect fifths (3/2) and compare with seven octaves: the Pythagorean comma 3^12 / 2^19.
    Then equal temperament: every semitone 2^(1/12), and how far each tempered interval is from the just ratio."""
    comma = 3 ** 12 / 2 ** 19
    spiral = []
    r = 1.0
    for k in range(13):
        spiral.append({"k": k, "ratio": round(r, 6), "cents_mod_octave": round(cents(r) % 1200, 2)})
        r *= 1.5
    et = []
    for name, (p, q) in JUST.items():
        just = cents(p / q)
        tempered = 100 * SEMITONES[name]
        et.append({"interval": name, "just": f"{p}:{q}", "just_cents": round(just, 2), "et_cents": tempered,
                   "error": round(tempered - just, 2)})
    return {"comma": round(comma, 6), "comma_num": 3 ** 12, "comma_den": 2 ** 19, "comma_cents": round(cents(comma), 2),
            "spiral": spiral, "equal": et, "semitone": round(2 ** (1 / 12), 6)}


# ---------------------------------------------------------------------------
# Roughness (Plomp and Levelt 1965; Sethares 1993)
# ---------------------------------------------------------------------------
def _pair_dissonance(f1, f2, a1, a2):
    b1, b2, xs, s1, s2 = 3.5, 5.75, 0.24, 0.0207, 18.96
    lo, hi = np.minimum(f1, f2), np.maximum(f1, f2)
    s = xs / (s1 * lo + s2)
    d = hi - lo
    return np.minimum(a1, a2) * (np.exp(-b1 * s * d) - np.exp(-b2 * s * d))


def dissonance(partials, amps, ratios, base: float = 261.63) -> np.ndarray:
    """Total roughness of two tones with the given partials (multiples of the fundamental) sounded at interval r:
    the sum over all pairs of partials, within and across the two tones."""
    f = np.asarray(partials, float) * base
    a = np.asarray(amps, float)
    out = []
    for r in ratios:
        F = np.concatenate([f, f * r])
        A = np.concatenate([a, a])
        tot = 0.0
        for i in range(len(F)):
            for j in range(i + 1, len(F)):
                tot += _pair_dissonance(F[i], F[j], A[i], A[j])
        out.append(tot)
    return np.array(out)


def _minima(x, y, depth=0.02):
    mins = []
    for i in range(1, len(y) - 1):
        if y[i] < y[i - 1] and y[i] <= y[i + 1]:
            left = y[max(0, i - 25):i].max()
            right = y[i + 1:i + 26].max() if i + 1 < len(y) else y[i]
            if min(left, right) - y[i] > depth * y.max():
                mins.append(i)
    return mins


def dissonance_curve(n_partials: int = 6, decay: float = 0.88, stretch: float = 2.0, lo: float = 1.0,
                     hi: float = 2.3, steps: int = 1301) -> dict:
    """The dissonance curve of two harmonic tones (partials 1..n, amplitudes decay^k), and its local minima. With
    ``stretch`` other than 2, partials are stretched (k-th partial at k^log2(stretch)), as in Sethares's tuned
    timbres, and the minima move with them."""
    ks = np.arange(1, n_partials + 1)
    partials = ks ** math.log2(stretch)
    amps = decay ** (ks - 1)
    r = np.linspace(lo, hi, steps)
    d = dissonance(partials, amps, r)
    d = d / d.max()
    mins = [float(r[i]) for i in _minima(r, d)]
    names = {1.0: "unison", 6 / 5: "6:5", 5 / 4: "5:4", 4 / 3: "4:3", 3 / 2: "3:2", 5 / 3: "5:3", 2.0: "2:1"}
    near = []
    for m in mins:
        best = min(names, key=lambda q: abs(q - m))
        near.append({"ratio": round(m, 3), "nearest_just": names[best], "off_cents": round(cents(m / best), 1)})
    return {"r": [round(x, 4) for x in r[::10]], "d": [round(float(x), 4) for x in d[::10]], "minima": near,
            "stretch": stretch, "n_partials": n_partials, "lowest_after_unison": round(float(r[1 + int(np.argmin(d[1:]))]), 3)}


# ---------------------------------------------------------------------------
# The seventeen wallpaper groups
# ---------------------------------------------------------------------------
def _rot(deg):
    t = math.radians(deg)
    return np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])


_I = np.eye(2)
_MV = np.array([[-1.0, 0.0], [0.0, 1.0]])      # mirror in a vertical line
_MH = np.array([[1.0, 0.0], [0.0, -1.0]])      # mirror in a horizontal line
_LAT = {"oblique": ((1.0, 0.0), (0.3, 0.9)), "rectangular": ((1.0, 0.0), (0.0, 0.7)),
        "centred": ((1.0, 0.0), (0.5, 0.35)), "square": ((1.0, 0.0), (0.0, 1.0)),
        "hexagonal": ((1.0, 0.0), (0.5, math.sqrt(3) / 2))}


def _cosets():
    """Coset representatives (A, t) of each group modulo its lattice, in Cartesian coordinates, from the standard
    lists of symmetry operations. p3m1 and p31m are built two ways and named by the classifier."""
    z = (0.0, 0.0)
    rot4 = [_rot(90 * k) for k in range(4)]
    rot3 = [_rot(120 * k) for k in range(3)]
    rot6 = [_rot(60 * k) for k in range(6)]
    G = {
        "p1": ("oblique", [(_I, z)]),
        "p2": ("oblique", [(_I, z), (-_I, z)]),
        "pm": ("rectangular", [(_I, z), (_MV, z)]),
        "pg": ("rectangular", [(_I, z), (_MV, (0.0, 0.35))]),
        "cm": ("centred", [(_I, z), (_MV, z)]),
        "pmm": ("rectangular", [(_I, z), (-_I, z), (_MV, z), (_MH, z)]),
        "pmg": ("rectangular", [(_I, z), (-_I, z), (_MV, (0.5, 0.0)), (_MH, (0.5, 0.0))]),
        "pgg": ("rectangular", [(_I, z), (-_I, z), (_MV, (0.5, 0.35)), (_MH, (0.5, 0.35))]),
        "cmm": ("centred", [(_I, z), (-_I, z), (_MV, z), (_MH, z)]),
        "p4": ("square", [(R, z) for R in rot4]),
        "p4m": ("square", [(R, z) for R in rot4] + [(_MV @ R, z) for R in rot4]),
        "p4g": ("square", [(R, z) for R in rot4] + [(_MV @ R, (0.5, 0.5)) for R in rot4]),
        "p3": ("hexagonal", [(R, z) for R in rot3]),
        "p3, mirrors A": ("hexagonal", [(R, z) for R in rot3] + [(_MH @ R, z) for R in rot3]),
        "p3, mirrors B": ("hexagonal", [(R, z) for R in rot3] + [(_MV @ R, z) for R in rot3]),
        "p6": ("hexagonal", [(R, z) for R in rot6]),
        "p6m": ("hexagonal", [(R, z) for R in rot6] + [(_MH @ R, z) for R in rot6]),
    }
    return G


def _elements(lat, cos, rng=3):
    a1, a2 = np.array(_LAT[lat][0]), np.array(_LAT[lat][1])
    out = []
    for A, t in cos:
        for i in range(-rng, rng + 1):
            for j in range(-rng, rng + 1):
                out.append((A, np.array(t) + i * a1 + j * a2))
    return out


def _order(A):
    M = np.eye(2)
    for k in range(1, 7):
        M = M @ A
        if np.allclose(M, np.eye(2), atol=1e-9):
            return k
    return 0


def _lines_equal(l1, l2):
    (p1, d1), (p2, d2) = l1, l2
    if abs(d1[0] * d2[1] - d1[1] * d2[0]) > 1e-6:
        return False
    w = p2 - p1
    return abs(w[0] * d1[1] - w[1] * d1[0]) < 1e-6


def _on_line(c, line):
    p, d = line
    w = c - p
    return abs(w[0] * d[1] - w[1] * d[0]) < 1e-6


def classify(lat, cos) -> dict:
    """Name a wallpaper group from its elements, by the standard flowchart: the highest order of rotation; whether
    there are mirrors; in how many directions; whether there are glide reflections on axes that are not mirrors;
    and whether rotation centres lie on mirrors."""
    els = _elements(lat, cos)
    rot_orders, mirrors, glides, centres = [1], [], [], {}
    for A, t in els:
        if np.linalg.det(A) > 0:
            k = _order(A)
            if k > 1:
                rot_orders.append(k)
                c = np.linalg.solve(np.eye(2) - A, t)
                if np.all(np.abs(c) < 1.6):
                    centres.setdefault(k, []).append(c)
        else:
            w, V = np.linalg.eig(A)
            d = np.real(V[:, int(np.argmin(np.abs(w - 1)))])
            v = (A @ t + t) / 2
            if np.linalg.norm(v) < 1e-9:
                mirrors.append((t / 2, d))
            else:
                glides.append(((t - A @ t) / 4, d))
    n = max(rot_orders)
    dirs = []
    for _, d in mirrors:
        if not any(abs(d[0] * e[1] - d[1] * e[0]) < 1e-6 for e in dirs):
            dirs.append(d)
    essential = any(not any(_lines_equal(g, m) for m in mirrors) for g in glides)

    def all_on(k):
        return all(any(_on_line(c, m) for m in mirrors) for c in centres.get(k, []))

    def some_on(k):
        return any(any(_on_line(c, m) for m in mirrors) for c in centres.get(k, []))

    has_m = bool(mirrors)
    if n == 1:
        name = ("cm" if essential else "pm") if has_m else ("pg" if glides else "p1")
    elif n == 2:
        if has_m:
            name = ("pmm" if all_on(2) else "cmm") if len(dirs) >= 2 else "pmg"
        else:
            name = "pgg" if glides else "p2"
    elif n == 4:
        name = ("p4m" if some_on(4) else "p4g") if has_m else "p4"
    elif n == 3:
        name = ("p3m1" if all_on(3) else "p31m") if has_m else "p3"
    else:
        name = "p6m" if has_m else "p6"
    return {"name": name, "rotation": n, "mirrors": has_m, "mirror_directions": len(dirs),
            "essential_glide": essential, "glides": bool(glides)}


ORBIFOLD = {"p1": "o", "p2": "2222", "pm": "**", "pg": "××", "cm": "*×", "pmm": "*2222",
            "pmg": "22*", "pgg": "22×", "cmm": "2*22", "p4": "442", "p4m": "*442", "p4g": "4*2", "p3": "333",
            "p3m1": "*333", "p31m": "3*3", "p6": "632", "p6m": "*632"}


def wallpaper() -> dict:
    """Generate each of the seventeen groups from its symmetry operations, classify it from scratch, and check that
    the seventeen names that come out are all different."""
    out = []
    for key, (lat, cos) in _cosets().items():
        c = classify(lat, cos)
        out.append({"built_as": key, "lattice": lat, **c, "orbifold": ORBIFOLD[c["name"]],
                    "point_group_order": len(cos)})
    names = [o["name"] for o in out]
    return {"groups": out, "distinct": len(set(names)), "all_seventeen": sorted(set(names)) == sorted(ORBIFOLD)}


def pattern(group: str, motif=None, cells: int = 2) -> dict:
    """Copies of an asymmetric motif under one group's operations, for drawing: a list of polygons."""
    G = _cosets()
    key = {o["name"]: o["built_as"] for o in wallpaper()["groups"]}[group]
    lat, cos = G[key]
    a1, a2 = np.array(_LAT[lat][0]), np.array(_LAT[lat][1])
    motif = np.array(motif if motif is not None else [(0.08, 0.06), (0.30, 0.10), (0.20, 0.16), (0.12, 0.26)])
    polys, flip = [], []
    for A, t in cos:
        img = motif @ A.T + np.array(t)
        for i in range(-cells, cells + 1):
            for j in range(-cells, cells + 1):
                polys.append((img + i * a1 + j * a2).round(4).tolist())
                flip.append(bool(np.linalg.det(A) < 0))
    return {"group": group, "lattice": lat, "polys": polys, "flip": flip, "a1": a1.tolist(), "a2": a2.tolist()}


# ---------------------------------------------------------------------------
# Order and complexity: compression (Schmidhuber's compression progress, as a toy)
# ---------------------------------------------------------------------------
def _ca(rule: int, width: int = 64, rows: int = 64, seed=None) -> np.ndarray:
    table = [(rule >> k) & 1 for k in range(8)]
    g = np.zeros((rows, width), np.uint8)
    if seed is None:
        g[0, width // 2] = 1
    else:
        g[0] = np.random.default_rng(seed).integers(0, 2, width)
    for r in range(1, rows):
        p = g[r - 1]
        idx = (np.roll(p, 1) << 2) | (p << 1) | np.roll(p, -1)
        g[r] = np.array(table, np.uint8)[idx]
    return g


def images(size: int = 64, seed: int = 1933) -> dict:
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:size, 0:size]
    return {"blank": np.zeros((size, size), np.uint8), "stripes": ((xx // 4) % 2).astype(np.uint8),
            "rule 90": _ca(90, size, size, seed=seed), "rule 30": _ca(30, size, size, seed=seed + 1),
            "noise": rng.integers(0, 2, (size, size)).astype(np.uint8)}


def compressibility(seed: int = 1933) -> dict:
    """zlib-compressed size of each 64 x 64 black-and-white image, as a fraction of its raw size in bits."""
    out = []
    for name, im in images(seed=seed).items():
        raw = np.packbits(im).tobytes()
        out.append({"image": name, "ratio": round(len(zlib.compress(raw, 9)) / len(raw), 3)})
    return {"images": out}


def compression_progress(seed: int = 1933) -> dict:
    """An observer reads each image row by row and predicts each cell from the three cells above it, learning a
    table of counts as it goes (Laplace smoothing). Bits needed per row fall as it learns; Schmidhuber's
    `interestingness' is that fall, the compression progress. Constant images are already predictable; noise never
    becomes predictable; a rule-generated pattern starts costly and becomes free."""
    out = {}
    for name, im in images(seed=seed).items():
        counts = np.ones((8, 2))
        bits = []
        for r in range(1, im.shape[0]):
            p = im[r - 1].astype(int)
            ctx = (np.roll(p, 1) << 2) | (p << 1) | np.roll(p, -1)
            row_bits = 0.0
            for c, v in zip(ctx, im[r]):
                row_bits += -math.log2(counts[c, v] / counts[c].sum())
                counts[c, v] += 1
            bits.append(round(row_bits / im.shape[1], 4))
        first, last = float(bits[0]), float(np.mean(bits[-8:]))
        out[name] = {"bits_per_cell": bits, "first": round(first, 4), "last": round(last, 4),
                     "progress": round(first - last, 3)}
    return out


# ---------------------------------------------------------------------------
# The golden ratio: looking for it everywhere
# ---------------------------------------------------------------------------
PHI = (1 + 5 ** 0.5) / 2


def golden(trials: int = 20000, n_lengths: int = 8, tol: float = 0.03, seed: int = 1876) -> dict:
    """Fibonacci ratios converge to phi. Then a look-elsewhere test: measure n random lengths on an imaginary
    building (uniform between 1 and 10); how often is some ratio of two of them within tol of phi?"""
    fib = [1, 1]
    while len(fib) < 16:
        fib.append(fib[-1] + fib[-2])
    ratios = [{"n": i + 1, "ratio": round(fib[i + 1] / fib[i], 6)} for i in range(1, 15)]
    rng = np.random.default_rng(seed)
    L = rng.uniform(1, 10, (trials, n_lengths))
    hit = 0
    per = []
    for row in L:
        rs = [max(a, b) / min(a, b) for a, b in itertools.combinations(row, 2)]
        k = sum(abs(r / PHI - 1) < tol for r in rs)
        per.append(k)
        hit += k > 0
    return {"phi": round(PHI, 6), "fibonacci": ratios, "trials": trials, "lengths": n_lengths,
            "pairs": n_lengths * (n_lengths - 1) // 2, "tol": tol, "p_some_hit": round(float(hit) / trials, 3),
            "mean_hits": round(float(np.mean(per)), 2)}


# ---------------------------------------------------------------------------
# Hume's true judges, as an analogy
# ---------------------------------------------------------------------------
def critics(works: int = 30, panels=(1, 2, 4, 8, 16, 32, 64), trials: int = 400, seed: int = 1757) -> dict:
    """Thirty works with a hidden quality. A critic's verdict = quality + her idiosyncratic taste + noise. Novices
    are noisy (sd 1.5) with strong idiosyncrasy (sd 1.0); Hume's true judges, practised and delicate, have little
    of either (0.4, 0.3); prejudiced judges are as skilled but share a bias toward a fashionable feature unrelated
    to quality. How well does the average verdict of a panel track quality, as the panel grows? (An analogy: it
    models the structure of Hume's claim, not any real criticism.)"""
    rng = np.random.default_rng(seed)
    kinds = {"novices": (1.5, 1.0, 0.0), "true judges": (0.4, 0.3, 0.0), "prejudiced judges": (0.4, 0.3, 1.2)}
    out = {k: [] for k in kinds}
    for n in panels:
        acc = {k: [] for k in kinds}
        for _ in range(trials):
            q = rng.normal(0, 1, works)
            fashion = rng.normal(0, 1, works)
            for k, (noise, idio, bias) in kinds.items():
                v = np.zeros(works)
                for _ in range(n):
                    v += q + rng.normal(0, idio, works) * rng.normal(0, 1, works) + rng.normal(0, noise, works) + \
                        bias * fashion
                acc[k].append(np.corrcoef(v / n, q)[0, 1])
        for k in kinds:
            out[k].append(round(float(np.mean(acc[k])), 3))
    return {"panels": list(panels), "correlation": out, "kinds": {k: list(v) for k, v in kinds.items()}}


def temperaments() -> dict:
    """Three ways to share out the comma. Pythagorean: pure fifths, the comma dumped on one `wolf' fifth.
    Quarter-comma meantone: fifths narrowed by a quarter of the syntonic comma 81/80 so that major thirds are pure,
    with a wolf of its own. Equal temperament: every fifth narrowed by a twelfth of the Pythagorean comma."""
    pyth_fifth = cents(1.5)
    syntonic = cents(81 / 80)
    mean_fifth = pyth_fifth - syntonic / 4
    et_fifth = 700.0
    out = []
    for name, f in (("Pythagorean", pyth_fifth), ("quarter-comma meantone", mean_fifth), ("equal", et_fifth)):
        third = (4 * f) % 1200                       # four fifths up, folded into the octave
        wolf = 8400 - 11 * f                         # the twelfth fifth that closes the circle
        out.append({"system": name, "fifth": round(f, 2), "major_third": round(third, 2),
                    "third_error": round(third - cents(5 / 4), 2), "wolf": round(wolf, 2)})
    return {"systems": out, "syntonic_cents": round(syntonic, 2), "just_third": round(cents(5 / 4), 2)}


def elements(group: str, window=(-0.2, 1.8)) -> dict:
    """The symmetry elements of one group inside a window: mirror lines, glide axes that are not mirrors, and
    rotation centres with their orders, for drawing over the pattern."""
    G = _cosets()
    key = {o["name"]: o["built_as"] for o in wallpaper()["groups"]}[group]
    lat, cos = G[key]
    lo, hi = window
    mirrors, glides, centres = [], [], []
    for A, t in _elements(lat, cos, rng=3):
        if np.linalg.det(A) > 0:
            k = _order(A)
            if k > 1:
                c = np.linalg.solve(np.eye(2) - A, t)
                if lo - 1e-9 <= c[0] <= hi + 1e-9 and lo - 1e-9 <= c[1] <= hi + 1e-9:
                    if not any(np.allclose(c, x["at"], atol=1e-6) and k <= x["order"] for x in centres):
                        centres = [x for x in centres if not (np.allclose(c, x["at"], atol=1e-6) and x["order"] < k)]
                        centres.append({"at": c.round(4).tolist(), "order": k})
        else:
            w, V = np.linalg.eig(A)
            d = np.real(V[:, int(np.argmin(np.abs(w - 1)))])
            v = (A @ t + t) / 2
            line = (t / 2, d) if np.linalg.norm(v) < 1e-9 else ((t - A @ t) / 4, d)
            store = mirrors if np.linalg.norm(v) < 1e-9 else glides
            if not any(_lines_equal(line, m) for m in store):
                store.append(line)
    glides = [g for g in glides if not any(_lines_equal(g, m) for m in mirrors)]

    def clip(line):
        p, d = np.array(line[0]), np.array(line[1])
        ts = []
        for axis in (0, 1):
            if abs(d[axis]) > 1e-9:
                for b in (lo, hi):
                    s = (b - p[axis]) / d[axis]
                    q = p + s * d
                    if lo - 1e-6 <= q[1 - axis] <= hi + 1e-6:
                        ts.append(q)
        if len(ts) < 2:
            return None
        ts = sorted(ts, key=lambda q: (q[0], q[1]))
        return [ts[0].round(4).tolist(), ts[-1].round(4).tolist()]

    seg_m = [s for s in (clip(m) for m in mirrors) if s and np.linalg.norm(np.subtract(s[0], s[1])) > 1e-3]
    seg_g = [s for s in (clip(g) for g in glides) if s and np.linalg.norm(np.subtract(s[0], s[1])) > 1e-3]
    return {"group": group, "mirrors": seg_m, "glides": seg_g, "centres": centres}


GOLDEN_ANGLE = 360 * (1 - 1 / PHI)


def phyllotaxis(angles=(137.0, GOLDEN_ANGLE, 137.6), n: int = 400) -> dict:
    """Vogel's model of a sunflower head (1979): seed k at angle k times the divergence angle, radius sqrt(k).
    At the golden angle the seeds pack evenly; a few tenths of a degree away, they form gaps and spokes. Report
    how evenly each angle fills the disc: the smallest distance between seeds, relative to the golden angle's."""
    out = []
    for a in angles:
        k = np.arange(1, n + 1)
        th = np.radians(a) * k
        r = np.sqrt(k)
        pts = np.stack([r * np.cos(th), r * np.sin(th)], axis=1)
        dmin = min(np.linalg.norm(pts[i] - pts[j]) for i in range(60, n) for j in range(i + 1, min(n, i + 60)))
        out.append({"angle": round(float(a), 3), "pts": pts.round(3).tolist(), "min_gap": round(float(dmin), 3)})
    return {"golden_angle": round(GOLDEN_ANGLE, 3), "n": n, "patterns": out}

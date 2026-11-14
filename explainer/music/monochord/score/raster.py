"""A page as pixels, and a first attempt at reading it back (Part 10's frontier: optical music recognition).

``page`` draws notes on staves as a bitmap, the way a scanner would see a clean print.  ``read_page`` is the textbook
pipeline: find the staff lines by adding up the ink in every row, take them away, find the blobs that are left, and
turn each blob's height on the staff into a note.  ``distort`` tilts the page and adds specks, which is all it takes
to break the first step; ``deskew`` repairs the tilt.  None of this is a real music reader: it reads only what
``page`` draws.
"""

from __future__ import annotations

import numpy as np
from scipy import ndimage


def page(notes, per_line: int = 14, space: int = 12, margin: int = 40, gap: int = 8) -> np.ndarray:
    """A bitmap (True is ink).  ``notes`` is a list of (position, filled): the position in half-spaces above the
    bottom line of the staff (0 is the bottom line, 8 the top), and whether the notehead is filled (a quarter) or
    hollow (a half).  ``per_line`` notes to a system."""
    notes = list(notes)
    rows = int(np.ceil(len(notes) / per_line))
    step = 3 * space
    width = 2 * margin + per_line * step + space
    height = 2 * margin + rows * 4 * space + (rows - 1) * gap * space + 4 * space
    img = np.zeros((height, width), dtype=bool)
    yy, xx = np.mgrid[0:height, 0:width]
    for r in range(rows):
        bottom = margin + 2 * space + r * (4 + gap) * space + 4 * space          # the y of the bottom line
        for k in range(5):
            y = bottom - k * space
            img[y - 1: y + 1, margin // 2: width - margin // 2] = True
        for c, (pos, filled) in enumerate(notes[r * per_line: (r + 1) * per_line]):
            cx = margin + space + c * step + step // 2
            cy = bottom - pos * space / 2.0
            a, b = 0.68 * space, 0.46 * space                                    # the notehead: an ellipse, slightly tilted
            u = (xx - cx) * np.cos(0.35) - (yy - cy) * np.sin(0.35)
            v = (xx - cx) * np.sin(0.35) + (yy - cy) * np.cos(0.35)
            d = (u / a) ** 2 + (v / b) ** 2
            img |= (d <= 1.0) if filled else ((d <= 1.0) & (d >= 0.42))
            up = pos < 4
            x = int(round(cx + (a - 1 if up else -a + 1)))
            y0, y1 = (int(cy - 3.4 * space), int(cy)) if up else (int(cy), int(cy + 3.4 * space))
            img[max(y0, 0): y1, x - 1: x + 1] = True
            for led in range(-2, int(pos) - 1, -2):                              # ledger lines below the staff
                yl = int(round(bottom - led * space / 2.0))
                img[yl - 1: yl + 1, int(cx - 1.1 * a): int(cx + 1.1 * a)] = True
            for led in range(10, int(pos) + 1, 2):                               # and above it
                yl = int(round(bottom - led * space / 2.0))
                img[yl - 1: yl + 1, int(cx - 1.1 * a): int(cx + 1.1 * a)] = True
    return img


def distort(img: np.ndarray, skew: float = 0.0, specks: float = 0.0, seed: int = 0) -> np.ndarray:
    """The page as a careless scan: turned by ``skew`` degrees, with a fraction ``specks`` of its pixels flipped."""
    out = img.astype(float)
    if skew:
        out = ndimage.rotate(out, skew, reshape=False, order=1, mode="constant", cval=0.0)
    out = out > 0.5
    if specks:
        rng = np.random.default_rng(seed)
        out = out ^ (rng.random(out.shape) < specks)
    return out


def row_profile(img: np.ndarray) -> np.ndarray:
    """The fraction of each row that is ink: staff lines stand out as five spikes."""
    return img.mean(axis=1)


def staff_lines(img: np.ndarray, level: float = 0.5) -> list[float]:
    """The y of every staff line: rows more than ``level`` ink, joined when they touch."""
    rows = np.flatnonzero(row_profile(img) > level)
    lines, run = [], []
    for r in rows:
        if run and r - run[-1] > 1:
            lines.append(float(np.mean(run)))
            run = []
        run.append(r)
    if run:
        lines.append(float(np.mean(run)))
    return lines


def deskew(img: np.ndarray, limit: float = 3.0, step: float = 0.05) -> tuple[np.ndarray, float]:
    """Turn the page until the rows are as unequal as they can be: the staff lines are then level.  Returns the
    page and the angle it was turned by."""
    best, angle = -1.0, 0.0
    small = img[::2, ::2].astype(float)
    for a in np.arange(-limit, limit + step / 2, step):
        v = float(np.var(ndimage.rotate(small, a, reshape=False, order=1).mean(axis=1)))
        if v > best:
            best, angle = v, float(a)
    return ndimage.rotate(img.astype(float), angle, reshape=False, order=1) > 0.5, angle


def read_page(img: np.ndarray) -> list[tuple[int, bool]]:
    """The notes of a page, as (position, filled), system by system, left to right.  An empty list if no staves are
    found."""
    lines = staff_lines(img)
    if len(lines) < 5 or len(lines) % 5:
        return []
    systems = [lines[k: k + 5] for k in range(0, len(lines), 5)]
    space = float(np.median([np.diff(s).mean() for s in systems]))
    clean = img.copy()
    for y in lines:                                         # take away each staff line, except where something crosses it
        rows = [r for r in range(int(np.floor(y)) - 1, int(np.ceil(y)) + 2) if 0 < r < img.shape[0] - 1 and img[r].mean() > 0.3]
        if not rows:
            continue
        touched = img[rows[0] - 1] | img[rows[-1] + 1]      # ink just above or just below the line
        for r in rows:
            clean[r] &= touched
    k = max(int(round(0.45 * space)), 2)                    # a notehead is wider than a stem or a speck
    filled_in = ndimage.binary_fill_holes(ndimage.binary_closing(clean, structure=np.ones((3, 3))))
    blobs = ndimage.binary_opening(filled_in, structure=np.ones((k + 1, k + 2)))
    lab, n = ndimage.label(blobs)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), start=1):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        if not (0.6 * space <= w <= 2.2 * space and 0.5 * space <= h <= 1.6 * space):
            continue
        cy, cx = ndimage.center_of_mass(lab == i)
        s = int(np.argmin([abs(cy - np.mean(sy)) for sy in systems]))
        pos = int(round((systems[s][-1] - cy) / (space / 2.0)))
        region = lab[sl] == i
        ink = float((img[sl] & region).sum()) / max(float(region.sum()), 1.0)       # a hollow head is a ring: less ink
        out.append((s, cx, pos, ink > 0.85))
    out.sort(key=lambda r: (r[0], r[1]))
    return [(pos, filled) for _, _, pos, filled in out]


def accuracy(read, truth) -> float:
    """One minus the edit distance between what was read and what was written, per note written."""
    a, b = list(read), list(truth)
    d = np.arange(len(b) + 1)
    for i in range(1, len(a) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(b) + 1):
            cur = min(d[j] + 1, d[j - 1] + 1, prev + (a[i - 1] != b[j - 1]))
            prev, d[j] = d[j], cur
    return max(0.0, 1.0 - float(d[-1]) / max(len(b), 1))

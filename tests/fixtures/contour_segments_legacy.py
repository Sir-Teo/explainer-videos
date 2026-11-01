"""Frozen contour_segments before the exact-level repair.

Copied from explainer/ai/viz.py SHA256
68c7ea8f062a7c8d0e54ee94e819c09f1b8c882931babddd3a0b4c8cee61f5aa.
Only a compatibility fixture; do not update to mirror production.
"""

def contour_segments(xs, ys, Z, level):
    """Marching squares: the segments where the grid values Z[i, j] (at ys[i], xs[j]) cross ``level``."""
    segs = []
    for i in range(len(ys) - 1):
        for j in range(len(xs) - 1):
            c = [(xs[j], ys[i], Z[i, j]), (xs[j + 1], ys[i], Z[i, j + 1]), (xs[j + 1], ys[i + 1], Z[i + 1, j + 1]), (xs[j], ys[i + 1], Z[i + 1, j])]
            pts = []
            for k in range(4):
                (x1, y1, z1), (x2, y2, z2) = (c[k], c[(k + 1) % 4])
                if (z1 - level) * (z2 - level) < 0:
                    t = (level - z1) / (z2 - z1)
                    pts.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
            if len(pts) == 2:
                segs.append(pts)
            elif len(pts) == 4:
                segs += [pts[:2], pts[2:]]
    return segs

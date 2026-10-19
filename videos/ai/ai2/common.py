"""Helpers shared by the scenes of Part 2 ("Thinking Machines: the symbolic era")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 2
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
GCOST = C.TRUE_P  # g: the cost so far
HEUR = C.MODEL_Q  # h: the heuristic estimate of the cost to go
FCOL = C.BITS  # f = g + h; the frontier
PATH = C.REWARD  # a path or plan found; true; satisfied
FAIL = C.PENALTY  # dead ends, conflicts, false
MAXC, MINC = C.MODEL_Q, C.TRUE_P  # the player to move (max) and the opponent (min): as in Part 26
LEARN = C.NEURAL  # anything learned: a learned clause, learned weights
SYMBOL = C.CONTEXT  # logic: symbols, clauses
HOT, COLD = C.HOT, C.COLD  # annealing's temperature
HIST = C.HUMAN  # people and history
WALL = "#3A4250"
EMPTY = "#141A24"

COLORS = {r"g": GCOST, r"h": HEUR, r"f": FCOL, r"h^*": PATH, r"C^*": PATH}


def rgb(c) -> np.ndarray:
    return np.array(ManimColor(c).to_rgb())


def image_from_rgb(arr: np.ndarray, width: float, height: float | None = None, smooth=False) -> ImageMobject:
    """An (H, W, 3) array of floats in [0, 1] as a picture of the given size (nearest-neighbour unless smooth)."""
    a = np.clip(arr, 0, 1)
    img = ImageMobject((np.concatenate([a, np.ones(a.shape[:2] + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear" if smooth else "nearest"])
    img.stretch_to_fit_width(width)
    if height is not None:
        img.stretch_to_fit_height(height)
    else:
        img.stretch_to_fit_height(width * arr.shape[0] / arr.shape[1])
    return img


def frontier_rgb(free, order, t, color=FCOL, old=GCOST, band=40.0) -> np.ndarray:
    """A grid search after t expansions: walls grey, unexplored dark, expanded cells shaded from ``old`` (long ago)
    toward ``color`` (just now), the newest ``band`` cells brightest: the frontier as a wavefront."""
    H, W = free.shape
    out = np.empty((H, W, 3))
    out[:] = rgb(EMPTY)
    out[~free.astype(bool)] = rgb(WALL)
    o = np.asarray(order)
    done = (o >= 0) & (o < t)
    if done.any():
        age = np.clip((t - o[done]) / band, 0, 1)[:, None]
        c_new, c_old = rgb(color), rgb(old) * 0.55 + rgb(EMPTY) * 0.45
        out[done] = c_new * (1 - age) + c_old * age
    return out


def grid_frame(img: ImageMobject, color=GREY_D) -> SurroundingRectangle:
    return SurroundingRectangle(img, buff=0, color=color, stroke_width=1.5)


def cell_center(img: ImageMobject, shape, r, c) -> np.ndarray:
    """The centre of grid cell (r, c) (row 0 at the top) inside the picture."""
    H, W = shape
    x0, y1 = img.get_left()[0], img.get_top()[1]
    return np.array([x0 + (c + 0.5) * img.width / W, y1 - (r + 0.5) * img.height / H, 0.0])


def path_line(img, shape, cells, color=PATH, width=5) -> VMobject:
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [cell_center(img, shape, r, c) for r, c in cells])


def tile_board(perm, size=3, cell=0.62, center=ORIGIN, color=GCOST, font_size=30, highlight=()) -> VGroup:
    """A sliding-tile board: ``perm[i]`` is the tile at position i (0 the blank), row by row."""
    g = VGroup()
    frame = Square(size * cell + 0.12, stroke_color=GREY_C, stroke_width=2, fill_color=EMPTY, fill_opacity=1)
    g.add(frame)
    tiles = VGroup()
    for i, t in enumerate(perm):
        r, c = divmod(i, size)
        pos = np.array([(c - (size - 1) / 2) * cell, ((size - 1) / 2 - r) * cell, 0])
        if t == 0:
            continue
        sq = RoundedRectangle(width=cell * 0.9, height=cell * 0.9, corner_radius=0.06, stroke_width=0,
                              fill_color=(FCOL if t in highlight else color), fill_opacity=0.85).move_to(pos)
        num = Text(str(t), font=MONO, font_size=font_size, color=WHITE).move_to(pos)
        tiles.add(VGroup(sq, num))
    g.add(tiles)
    g.tiles = tiles
    return g.move_to(center)


def queens_board(q, cell=0.42, center=ORIGIN, attack_pairs=True) -> VGroup:
    """An n x n board with one queen per column at row q[c]; attacking pairs joined by thin red lines."""
    n = len(q)
    g = VGroup()
    sq = VGroup()
    for r in range(n):
        for c in range(n):
            sq.add(Square(cell, stroke_width=0, fill_color=("#2A3242" if (r + c) % 2 else "#1B2130"),
                          fill_opacity=1).move_to([(c - (n - 1) / 2) * cell, ((n - 1) / 2 - r) * cell, 0]))
    g.add(sq)

    def at(c):
        return np.array([(c - (n - 1) / 2) * cell, ((n - 1) / 2 - q[c]) * cell, 0])

    lines = VGroup()
    if attack_pairs:
        for i in range(n):
            for j in range(i + 1, n):
                if q[i] == q[j] or abs(q[i] - q[j]) == j - i:
                    lines.add(Line(at(i), at(j), color=FAIL, stroke_width=2, stroke_opacity=0.8))
    g.add(lines)
    qs = VGroup(*[Circle(radius=cell * 0.32, stroke_width=0, fill_color=HEUR, fill_opacity=1).move_to(at(c))
                  for c in range(n)])
    g.add(qs)
    g.lines, g.queens = lines, qs
    return g.move_to(center)


def tour_mob(ax, xy, tour, color=PATH, width=3) -> VMobject:
    pts = [ax.c2p(*xy[i]) for i in list(tour) + [tour[0]]]
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)


def node_box(text: str, color, font_size=24, pad=0.22, height=0.62) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 2 * pad, height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


def said(text: str, who: str = "machine", chars: int = 46, font_size: int = 20, max_lines: int = 3,
         color=None) -> VGroup:
    """A line typed in a conversation (a person or ELIZA): monospaced, wrapped, never translated."""
    import textwrap

    col = color or (C.USER if who == "user" else C.ASSISTANT)
    lines = textwrap.wrap(" ".join(text.split()), chars) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: chars - 3] + "..."
    t = data_text("\n".join(lines), font=MONO, font_size=font_size, color=WHITE, line_spacing=0.8)
    box = RoundedRectangle(width=t.width + 0.36, height=t.height + 0.3, corner_radius=0.12, stroke_color=col,
                           stroke_width=2.2, fill_color=col, fill_opacity=0.08)
    return VGroup(box, t.move_to(box))


def logic_tex(text: str) -> str:
    """A clause from the prover's text form ('¬Rain ∨ Wet', '□') as MathTex."""
    if text == "□":
        return r"\square"
    s = text.replace("¬", r"\lnot ").replace("∨", r"\lor")
    s = s.replace("_", r"\_")
    s = __import__("re").sub(r"\b([A-Z][A-Za-z0-9]*)\b", r"\\mathrm{\1}", s)
    return s


def bar_row(values, labels, colors, width=6.0, height=0.36, font_size=22, vmax=None, fmt=lambda v: f"{v:,.0f}",
            log=False, gap=0.22, label_width=None) -> VGroup:
    """Horizontal bars with a label on the left and the value on the right (log scale if asked)."""
    vals = np.asarray(values, float)
    if log:
        vals = np.log10(np.maximum(vals, 1))
    vmax = vmax or vals.max()
    rows = VGroup()
    names = [label(t, font_size=font_size, color=c) for t, c in zip(labels, colors)]
    lw = label_width or max(n.width for n in names)
    for v, raw, nm, col in zip(vals, values, names, colors):
        w = max(width * v / vmax, 0.02)
        bar = Rectangle(width=w, height=height, stroke_width=0, fill_color=col, fill_opacity=0.85)
        row = VGroup(nm, bar)
        nm.move_to(ORIGIN, aligned_edge=RIGHT)
        bar.next_to(ORIGIN, RIGHT, buff=0.2)
        val = MathTex(fmt(raw).replace(",", "{,}"), font_size=font_size + 2, color=col).next_to(bar, RIGHT, buff=0.15)
        row.add(val)
        row.bar, row.value, row.name = bar, val, nm
        rows.add(row)
    rows.arrange(DOWN, buff=gap, aligned_edge=LEFT)
    for r in rows:
        r.name.align_to(rows, LEFT)
        r.name.shift(RIGHT * (lw - r.name.width))
        r.bar.next_to(r.name, RIGHT, buff=0.25).align_to(r.name, ORIGIN)
        r.bar.set_x(rows.get_left()[0] + lw + 0.25 + r.bar.width / 2)
        r.value.next_to(r.bar, RIGHT, buff=0.15)
    return rows

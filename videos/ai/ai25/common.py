"""Helpers shared by the scenes of Part 25 ("Symmetry and Science")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 25
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
STRUCT = "#5CD0B3"  # the symmetry built into the network (Deep Sets, GIN, EGNN, invariant nets, FNO, triangle updates)
PLAIN = "#FF6B8B"  # no symmetry built in (a plain MLP, a CNN, per-pair updates)
AUG = "#C792EA"  # symmetry learned from transformed copies of the data (augmentation)
GNN_C = "#7C9CF0"  # message passing that ignores geometry (coordinates as plain numbers)
SYM = "#7FD3FF"  # the group, its actions: rotations, permutations, shifts
TRUE_C = C.TRUE_P  # the truth: the real structure, the solver's field
PRED_C = C.MODEL_Q  # a model's prediction
MIRROR_C = "#E3A8F0"  # mirror images
PAIR_C = "#F7D154"  # the pair representation, triangles
MSA_C = "#9BE37B"  # sequences, alignments (and, in chapter 15, stable compounds)
MESH_C = "#7FD3FF"  # meshes
LEAN_C = "#7C9CF0"  # formal proofs
SEARCH_C = "#F2A541"  # search and evolution
HIST = C.HUMAN  # history cards
PANEL = "#121722"
BG_HEX = "#0E1117"

KIND_COLOR = {"egnn": STRUCT, "inv": STRUCT, "deepsets": STRUCT, "gin": STRUCT, "fno": STRUCT, "triangle": STRUCT,
              "gnn": GNN_C, "mlp": PLAIN, "cnn": PLAIN, "pairwise": PLAIN, "mlp_aug": AUG, "recycle": PAIR_C}
KIND_NAME = {"egnn": r"EGNN", "inv": r"invariant net", "deepsets": r"Deep Sets", "gnn": r"plain GNN",
             "mlp": r"MLP", "mlp_aug": r"MLP + rotations", "cnn": r"CNN", "fno": r"FNO",
             "pairwise": r"per-pair updates", "triangle": r"triangle updates", "recycle": r"triangles + recycling"}

# categorical colours for 1-WL's node colours
WL_COLORS = ["#BBBBBB", "#58A6FF", "#FF9F45", "#5CD0B3", "#FF6B8B", "#C792EA", "#F7D154", "#9BE37B", "#7FD3FF",
             "#E3A8F0"]
COMM_COLORS = ["#58A6FF", "#FF9F45", "#5CD0B3"]  # the three communities of chapter 4


def rgb_of(c) -> np.ndarray:
    return np.array(ManimColor(c).to_rgb())


BG_RGB = rgb_of(BG_HEX)


def mean_spread(vals):
    v = np.asarray(vals, float)
    return float(v.mean()), float(v.min()), float(v.max())


def words_num(n: int) -> str:
    """Small counts spoken as words (the narrator reads 'three seeds' better than '3 seeds')."""
    w = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
    return w[n] if 0 <= n < len(w) else str(n)


def pct(x: float, digits=0) -> str:
    return f"{100 * x:.{digits}f}"


# ---------------------------------------------------------------------------
# Pictures from arrays
# ---------------------------------------------------------------------------
def to_image(rgb: np.ndarray, width: float, height: float | None = None, smooth=False) -> ImageMobject:
    """An (h, w, 3) array in [0, 1] as an ImageMobject, rows top to bottom."""
    a = np.clip(rgb, 0, 1)
    img = ImageMobject((np.concatenate([a, np.ones(a.shape[:2] + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear" if smooth else "nearest"])
    img.stretch_to_fit_width(width)
    img.stretch_to_fit_height(height if height is not None else width * a.shape[0] / a.shape[1])
    return img


def ramp(t: np.ndarray, stops) -> np.ndarray:
    """Values t in [0, 1] through a piecewise-linear colour ramp (list of hex colours)."""
    cols = np.array([rgb_of(c) for c in stops])
    t = np.clip(np.asarray(t, float), 0, 1) * (len(cols) - 1)
    i = np.minimum(np.floor(t).astype(int), len(cols) - 2)
    f = (t - i)[..., None]
    return cols[i] * (1 - f) + cols[i + 1] * f


SEQ = ("#0E1117", "#1B2A6B", "#2E6FB0", "#3FB8AF", "#F2D16B", "#FFF3C4")  # distances, intensities
DIV = ("#3D7DD8", "#8FB9EE", "#0E1117", "#F2A07B", "#E0533D")  # signed fields: blue negative, red positive


def matrix_image(M, size=2.6, vmin=None, vmax=None, stops=SEQ, mask=None, smooth=False) -> ImageMobject:
    """A matrix as a square picture (row 0 at the top); ``mask`` False cells are drawn as the panel colour."""
    M = np.asarray(M, float)
    lo = np.nanmin(M) if vmin is None else vmin
    hi = np.nanmax(M) if vmax is None else vmax
    rgb = ramp((M - lo) / max(hi - lo, 1e-12), stops)
    if mask is not None:
        rgb[~np.asarray(mask, bool)] = rgb_of(PANEL)
    return to_image(rgb, size, size * M.shape[0] / M.shape[1], smooth=smooth)


def field_image(W, size=2.6, vmax=None, smooth=True) -> ImageMobject:
    """A signed 2D field (vorticity) with the diverging ramp, symmetric about zero."""
    W = np.asarray(W, float)
    v = float(np.abs(W).max()) if vmax is None else vmax
    return to_image(ramp(0.5 + 0.5 * W / max(v, 1e-12), DIV), size, size, smooth=smooth)


def framed(img: Mobject, color=GREY_D, buff=0.04) -> Group:
    return Group(img, SurroundingRectangle(img, buff=buff, color=color, stroke_width=1.2))


# ---------------------------------------------------------------------------
# Graphs and point clouds
# ---------------------------------------------------------------------------
def graph_mob(pos, edges, colors=None, scale=1.6, center=ORIGIN, node_r=0.11, edge_color=GREY_B, edge_w=2.0,
              node_color=GREY_A, stroke=True) -> VGroup:
    """A graph drawn from a layout (n x 2, roughly in [-1, 1]): ``g.nodes`` (Dots, in node order), ``g.edges``."""
    P = np.asarray(pos, float)
    pts = [np.array([center[0] + scale * p[0], center[1] + scale * p[1], 0.0]) for p in P]
    E = VGroup(*[Line(pts[a], pts[b], color=edge_color, stroke_width=edge_w) for a, b in edges])
    N = VGroup()
    for i, p in enumerate(pts):
        c = colors[i] if colors is not None else node_color
        d = Dot(p, radius=node_r, color=c)
        if stroke:
            d.set_stroke(BG_HEX, width=1.5, background=True)
        N.add(d)
    g = VGroup(E, N)
    g.nodes, g.edges, g.pts = N, E, pts
    return g


def recolor(g: VGroup, colors) -> list:
    return [d.animate.set_color(c) for d, c in zip(g.nodes, colors)]


def project(X, angle=0.0, tilt=0.35):
    """3D points to the screen after turning by ``angle`` about the vertical axis and tilting by ``tilt``; also
    returns depth (towards the viewer positive)."""
    X = np.asarray(X, float)
    x, y, z = X[:, 0], X[:, 1], X[:, 2]
    x, z = x * np.cos(angle) + z * np.sin(angle), -x * np.sin(angle) + z * np.cos(angle)
    y, z = y * np.cos(tilt) - z * np.sin(tilt), y * np.sin(tilt) + z * np.cos(tilt)
    return np.c_[x, y], z


def chain3d(X, scale=0.12, center=ORIGIN, angle=0.0, tilt=0.35, color=TRUE_C, width=3.0, dots=True, dot_r=0.035,
            gradient=None) -> VGroup:
    """A C-alpha trace drawn in perspective-free projection; nearer segments brighter.  ``gradient``: colour the
    chain from N to C terminus along this list of colours (as structure viewers do)."""
    P2, depth = project(np.asarray(X) - np.asarray(X).mean(0), angle, tilt)
    pts = [np.array([center[0] + scale * p[0], center[1] + scale * p[1], 0.0]) for p in P2]
    dn = (depth - depth.min()) / max(np.ptp(depth), 1e-9)
    n = len(pts)
    g = VGroup()
    segs = VGroup()
    for i in range(n - 1):
        c = color if gradient is None else interpolate_color(ManimColor(gradient[0]), ManimColor(gradient[-1]),
                                                             i / max(n - 2, 1))
        if gradient is not None and len(gradient) == 3:
            t = i / max(n - 2, 1)
            c = (interpolate_color(ManimColor(gradient[0]), ManimColor(gradient[1]), 2 * t) if t < 0.5 else
                 interpolate_color(ManimColor(gradient[1]), ManimColor(gradient[2]), 2 * t - 1))
        op = 0.35 + 0.65 * 0.5 * (dn[i] + dn[i + 1])
        segs.add(Line(pts[i], pts[i + 1], color=c, stroke_width=width, stroke_opacity=op))
    g.add(segs)
    g.segs = segs
    if dots:
        ds = VGroup(*[Dot(p, radius=dot_r, color=GREY_A).set_opacity(0.4 + 0.6 * dn[i]) for i, p in enumerate(pts)])
        g.add(ds)
        g.dots = ds
    g.pts = pts
    return g


CHAIN_GRAD = ("#58A6FF", "#5CD0B3", "#F7D154")  # N to C terminus


def chain2d_mob(P, scale=0.5, center=ORIGIN, color=STRUCT, width=3.0, dot_r=0.05) -> VGroup:
    """A 2D chain (n x 2): bonds and atoms."""
    pts = [np.array([center[0] + scale * p[0], center[1] + scale * p[1], 0.0]) for p in np.asarray(P, float)]
    g = VGroup(VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts),
               VGroup(*[Dot(p, radius=dot_r, color=color) for p in pts]))
    return g


def points2d(P, scale=1.0, center=ORIGIN, color=WHITE, r=0.05) -> VGroup:
    return VGroup(*[Dot([center[0] + scale * p[0], center[1] + scale * p[1], 0], radius=r, color=color)
                    for p in np.asarray(P, float)])


# ---------------------------------------------------------------------------
# Cards, labels, charts
# ---------------------------------------------------------------------------
def node_box(text: str, color, font_size=24, pad=0.22, height=0.62, width=None) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=width or (t.width + 2 * pad), height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


def take_away(text: str, color=C.BITS, font_size=28, width=12.0) -> VGroup:
    """The chapter's takeaway: a line in a soft box at the bottom of the frame."""
    t = wrapped_label(text, width, font_size, color)
    box = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.35, corner_radius=0.14, stroke_color=color,
                           stroke_width=1.5, fill_color="#0B0F17", fill_opacity=0.92)
    return VGroup(box, t.move_to(box)).to_edge(DOWN, buff=0.35)


def caption(mob: Mobject, text: str, color=GREY_A, font_size=22, direction=UP, buff=0.15) -> Tex:
    return label(text, font_size=font_size, color=color).next_to(mob, direction, buff=buff)


def crossfade(a: Mobject, b: Mobject) -> AnimationGroup:
    return AnimationGroup(FadeOut(a), FadeIn(b))


def hbars(rows, vmax, width=5.0, row_h=0.5, font_size=22, name_w=3.2, fmt=None, spread=None) -> VGroup:
    """Horizontal bars: rows of (name, value, colour); ``spread`` (lo, hi) per row as a whisker; values printed."""
    g = VGroup()
    g.rows = VGroup()
    for i, (name, v, col) in enumerate(rows):
        y = -i * row_h
        nm = label(name, font_size=font_size, color=col)
        if nm.width > name_w:
            nm.width = name_w
        nm.move_to([-0.2 - nm.width / 2, y, 0])
        w = max(width * v / vmax, 0.02)
        bar = Rectangle(width=w, height=row_h * 0.6, stroke_width=0, fill_color=col, fill_opacity=0.85)
        bar.move_to([w / 2, y, 0])
        row = VGroup(nm, bar)
        right = w
        if spread is not None:
            lo, hi = spread[i]
            a, b = width * lo / vmax, width * hi / vmax
            wh = VGroup(Line([a, y, 0], [b, y, 0], color=WHITE, stroke_width=1.6),
                        Line([a, y - 0.08, 0], [a, y + 0.08, 0], color=WHITE, stroke_width=1.6),
                        Line([b, y - 0.08, 0], [b, y + 0.08, 0], color=WHITE, stroke_width=1.6))
            row.add(wh)
            right = max(right, b)
        val = label(fmt(v) if fmt else f"${v:.2f}$", font_size=font_size, color=col)
        val.move_to([right + 0.15 + val.width / 2, y, 0])
        row.add(val)
        row.bar, row.val, row.name = bar, val, nm
        g.rows.add(row)
    g.add(g.rows)
    return g


def stack_label(lines, font_size=24, color=WHITE, buff=0.18) -> VGroup:
    return VGroup(*[label(t, font_size=font_size, color=color) for t in lines]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=buff)


def check_mark(ok: bool) -> Mobject:
    return MathTex(r"\checkmark" if ok else r"\times", font_size=36 if ok else 40,
                   color=C.INTERVAL if ok else GREY_C)


def log_axes(x_vals, y_lo, y_hi, x_length=5.6, y_length=3.4, xlabel="", ylabel="", center=ORIGIN, font_size=20,
             yticks=None, xticks=None, xfmt=None, yfmt=None):
    """Axes with log10 on both: x from the first to the last of ``x_vals``, y from 10^y_lo to 10^y_hi."""
    lx = np.log10(np.asarray(x_vals, float))
    return axes([float(lx[0]), float(lx[-1])], [y_lo, y_hi], x_length=x_length, y_length=y_length, xlabel=xlabel,
                ylabel=ylabel, xticks=list(np.log10(xticks)) if xticks is not None else list(lx),
                yticks=yticks if yticks is not None else list(range(int(np.ceil(y_lo)), int(np.floor(y_hi)) + 1)),
                xfmt=xfmt or (lambda v: f"{10 ** v:,.0f}".replace(",", "{,}")),
                yfmt=yfmt or (lambda v: f"10^{{{int(round(v))}}}"), center=center, font_size=font_size)


def years_line(events, x0=-6.4, x1=6.4, y0=-0.2, T0=1940, T1=2027, font_size=18, ticks=(1950, 1970, 1990, 2010)):
    """A horizontal timeline with events (year, text, colour), labels alternating above and below, kept apart."""
    X = lambda yr: x0 + (x1 - x0) * (yr - T0) / (T1 - T0)  # noqa: E731
    line = Line([x0, y0, 0], [x1, y0, 0], color=GREY_C, stroke_width=2)
    tk = VGroup()
    for yr in ticks:
        tk.add(Line([X(yr), y0 - 0.06, 0], [X(yr), y0 + 0.06, 0], color=GREY_C, stroke_width=1.5))
        tk.add(label(str(yr), font_size=16, color=GREY_C).next_to([X(yr), y0, 0], DOWN, buff=0.1))
    items = VGroup()
    for k, (yr, txt, col) in enumerate(events):
        dot = Dot([X(yr), y0, 0], radius=0.07, color=col)
        yl = label(str(yr), font_size=font_size + 2, color=col)
        tx = label(txt, font_size=font_size, color=WHITE)
        grp = VGroup(yl, tx).arrange(DOWN, buff=0.06)
        up = k % 2 == 0
        grp.next_to(dot, UP if up else DOWN, buff=0.3 if up else 0.45)
        items.add(VGroup(dot, Line(dot.get_center(), dot.get_center(), color=col, stroke_width=1.2), grp))
    for side in (0, 1):
        same = [items[k] for k in range(len(items)) if k % 2 == side]
        for a, b in zip(same, same[1:]):
            gap = b[2].get_left()[0] - a[2].get_right()[0]
            if gap < 0.12:
                b[2].shift(RIGHT * (0.12 - gap))
        if same and same[-1][2].get_right()[0] > 6.9:
            sh = same[-1][2].get_right()[0] - 6.9
            same[-1][2].shift(LEFT * sh)
            for i in range(len(same) - 2, -1, -1):
                gap = same[i + 1][2].get_left()[0] - same[i][2].get_right()[0]
                if gap < 0.12:
                    same[i][2].shift(LEFT * (0.12 - gap))
    for it in items:
        dot, stem, grp = it
        end = [grp.get_x(), grp.get_bottom()[1] if grp.get_y() > y0 else grp.get_top()[1], 0]
        stem.put_start_and_end_on(dot.get_center(), end)
    return VGroup(line, tk), items

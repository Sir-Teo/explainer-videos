"""The instruments of *Industry, Built* (SYLLABUS §2.2-2.6), drawn the same way in every part.

* :func:`phone` - a phone, front or back;  :func:`exploded` - its layers pulled apart, isometric;
* :func:`region_map` - tiles for the regions of the world economy, placed roughly where they sit on a globe;
* :class:`DollarColumn` - the Dollar: one payment as a column of slices, labelled on the right;
* :func:`margin_ladder` - horizontal bars of a share (a margin) for a list of companies;
* :func:`treemap` - blocks with areas proportional to values (market shares);
* :func:`plot_axes` - plain axes with tick labels in the series' face; :func:`year_bars` - a bar per year;
* :func:`coin` - a gold coin, for money moving along a chain.
"""

from __future__ import annotations

import numpy as np
from manim import (DOWN, LEFT, ORIGIN, RIGHT, UP, Axes, Circle, DashedLine, Dot, Line, Polygon, Rectangle,
                   RoundedRectangle, VGroup, VMobject)

from explainer.industry.kit import T, TB, money
from explainer.industry.style import I, REGION, REGION_NAME


# --------------------------------------------------------------------------------------------------------------------
# The phone
# --------------------------------------------------------------------------------------------------------------------

def phone(h: float = 4.0, back: bool = False, body: str = "#2B303B", screen: str = "#101722",
          glow: str | None = None) -> VGroup:
    """A modern phone, ``h`` tall: rounded body, screen with an island, or (``back``) a three-lens camera plateau."""
    w = h * 0.49
    shell = RoundedRectangle(corner_radius=h * 0.085, width=w, height=h, fill_color=body, fill_opacity=1,
                             stroke_color="#5A6272", stroke_width=2.2)
    g = VGroup(shell)
    if not back:
        scr = RoundedRectangle(corner_radius=h * 0.07, width=w * 0.9, height=h * 0.95, fill_color=screen,
                               fill_opacity=1, stroke_width=0)
        island = RoundedRectangle(corner_radius=h * 0.018, width=w * 0.3, height=h * 0.036, fill_color="#000000",
                                  fill_opacity=1, stroke_width=0).move_to(scr.get_top() + DOWN * h * 0.05)
        g.add(scr, island)
        if glow:
            scr.set_fill(glow, opacity=0.25)
    else:
        plate = RoundedRectangle(corner_radius=h * 0.05, width=w * 0.52, height=w * 0.52, fill_color="#3A404D",
                                 fill_opacity=1, stroke_color="#666E7E", stroke_width=1.2)
        plate.move_to(shell.get_corner(UP + LEFT) + np.array([w * 0.32, -w * 0.32, 0]))
        lenses = VGroup()
        for dx, dy in ((-0.11, 0.11), (-0.11, -0.11), (0.11, 0.0)):
            ring = Circle(radius=w * 0.085, fill_color="#0B0E13", fill_opacity=1, stroke_color="#8A93A5",
                          stroke_width=1.5).move_to(plate.get_center() + np.array([dx * w, dy * w, 0]))
            lenses.add(ring, Circle(radius=w * 0.03, fill_color="#2E4A6B", fill_opacity=1, stroke_width=0)
                       .move_to(ring))
        g.add(plate, lenses)
    return g


LAYERS_PHONE = (
    ("cover", "Cover glass", I.CASE),
    ("display", "Display", I.DISPLAY),
    ("frame", "Frame", I.CASE),
    ("board", "Logic board", I.CHIP),
    ("battery", "Battery", I.POWER),
    ("camera", "Cameras", I.CAMERA),
    ("back", "Back glass", I.CASE),
)


def slab(w: float, d: float, color: str, opacity: float = 0.85, stroke: float = 1.6) -> Polygon:
    """A thin rectangular layer seen from above at an angle: a parallelogram ``w`` wide and ``d`` deep."""
    skew = np.array([0.55 * d, 0.45 * d, 0])
    p = [ORIGIN - skew / 2 + LEFT * w / 2, ORIGIN - skew / 2 + RIGHT * w / 2, ORIGIN + skew / 2 + RIGHT * w / 2,
         ORIGIN + skew / 2 + LEFT * w / 2]
    return Polygon(*p, fill_color=color, fill_opacity=opacity, stroke_color=color, stroke_width=stroke)


def exploded(layers=LAYERS_PHONE, w: float = 3.2, d: float = 1.9, gap: float = 0.78) -> VGroup:
    """Layers stacked from the top down with ``gap`` between them; each item is VGroup(slab, details)."""
    out = VGroup()
    for i, (key, _, color) in enumerate(layers):
        s = slab(w, d, color, 0.32 if key in ("cover", "back") else 0.8)
        extra = VGroup()
        if key == "board":  # chips on the board
            for (x, y, sw, sh, c) in ((-0.55, 0.05, 0.5, 0.36, I.CHIP), (0.05, 0.1, 0.34, 0.26, I.MEMORY),
                                      (0.55, -0.05, 0.3, 0.22, I.RF), (0.15, -0.28, 0.24, 0.16, I.POWER)):
                chip = slab(sw, sh, c, 1.0, 1.0).move_to(s.get_center() + np.array([x, y, 0]))
                extra.add(chip)
        if key == "camera":
            for x in (-0.95, -0.55):
                extra.add(Circle(radius=0.16, fill_color="#0B0E13", fill_opacity=1, stroke_color=I.CAMERA,
                                 stroke_width=1.5).stretch(0.75, 1).move_to(s.get_center() + np.array([x, 0.25, 0])))
        if key == "battery":
            s.stretch(0.62, 0)
        out.add(VGroup(s, extra).shift(DOWN * i * gap))
    return out.move_to(ORIGIN)


# --------------------------------------------------------------------------------------------------------------------
# The map of regions
# --------------------------------------------------------------------------------------------------------------------

REGION_POS = {
    "US": (-5.3, 0.9), "Europe": (-2.4, 1.6), "India": (-0.3, -0.6), "China": (1.8, 0.9),
    "Korea": (3.9, 1.7), "Japan": (5.9, 1.0), "Taiwan": (4.0, -0.3), "SE Asia": (1.9, -1.5),
}


def region_map(regions=None, w: float = 1.75, h: float = 0.82, size: float = 20, scale: float = 1.0) -> dict:
    """{region: VGroup(tile, name)} placed roughly as on a globe (Americas left, East Asia right)."""
    out = {}
    for r, (x, y) in REGION_POS.items():
        if regions and r not in regions:
            continue
        tile = RoundedRectangle(corner_radius=0.12, width=w, height=h, fill_color=REGION[r], fill_opacity=0.16,
                                stroke_color=REGION[r], stroke_width=2)
        name = T(REGION_NAME[r] if len(REGION_NAME[r]) < 15 else r, size, "#E8EAED")
        if name.width > w - 0.15:
            name.scale_to_fit_width(w - 0.15)
        g = VGroup(tile, name.move_to(tile)).move_to(np.array([x, y, 0]) * scale)
        out[r] = g
    return out


# --------------------------------------------------------------------------------------------------------------------
# The Dollar
# --------------------------------------------------------------------------------------------------------------------

class DollarColumn(VGroup):
    """One payment drawn as a column of slices, bottom to top, each labelled on the right.

    ``items``: [(label, amount, colour, note)].  The labels are spread evenly beside the column and joined to their
    slices by thin leaders, so a slice of $30 is as legible as one of $500.  ``self.slices[i]``, ``self.labels[i]``
    and ``self.leaders[i]`` animate item by item.
    """

    def __init__(self, items, total: float | None = None, height: float = 6.2, width: float = 1.5,
                 label_x: float = 1.0, size: float = 21, fmt=money, label_width: float = 5.2, gap: float = 0.0):
        super().__init__()
        total = total or sum(a for _, a, _, _ in items)
        self.items, self.total, self.height = items, total, height
        self.slices, self.labels, self.leaders = VGroup(), VGroup(), VGroup()
        y = -height / 2
        for label, amt, color, note in items:
            hh = max(height * amt / total, 0.012)
            r = Rectangle(width=width, height=hh, fill_color=color, fill_opacity=0.9, stroke_color="#0E1117",
                          stroke_width=1.2)
            r.move_to(np.array([0, y + hh / 2, 0]))
            self.slices.add(r)
            y += hh + gap
        n = len(items)
        ys = np.linspace(-height / 2 + 0.2, height / 2 - 0.2, n) if n > 1 else [0.0]
        for (label, amt, color, note), r, ly in zip(items, self.slices, ys):
            head = VGroup(TB(fmt(amt), size, color), T(label, size, "#E8EAED")).arrange(RIGHT, buff=0.16)
            lab = VGroup(head)
            if note:
                lab.add(T(note, size * 0.72, "#9AA3B2"))
                lab.arrange(DOWN, aligned_edge=LEFT, buff=0.04)
            if lab.width > label_width:
                lab.scale_to_fit_width(label_width)
            lab.move_to(np.array([width / 2 + label_x, ly, 0]), aligned_edge=LEFT)
            a = r.get_right()
            b = lab.get_left() + LEFT * 0.08
            mid = np.array([a[0] + 0.35, b[1], 0])
            lead = VMobject(stroke_color=color, stroke_width=1.4, stroke_opacity=0.8)
            lead.set_points_as_corners([a, np.array([a[0] + 0.2, a[1], 0]), mid, b])
            self.labels.add(lab)
            self.leaders.add(lead)
        self.add(self.slices, self.leaders, self.labels)

    def top_label(self, text: str, size: float = 30, color: str = I.MONEY):
        return TB(text, size, color).next_to(self.slices, UP, buff=0.18)


def bar_split(items, total: float, width: float = 12.0, height: float = 0.75) -> VGroup:
    """One payment as a horizontal bar split left to right: [(label, amount, colour)]."""
    g = VGroup()
    x = -width / 2
    for _, amt, color in items:
        w = max(width * amt / total, 0.01)
        g.add(Rectangle(width=w, height=height, fill_color=color, fill_opacity=0.9, stroke_color="#0E1117",
                        stroke_width=1.2).move_to(np.array([x + w / 2, 0, 0])))
        x += w
    return g


# --------------------------------------------------------------------------------------------------------------------
# Comparisons
# --------------------------------------------------------------------------------------------------------------------

def margin_ladder(items, max_value: float = 1.0, bar_len: float = 6.0, row_h: float = 0.46, size: float = 20,
                  name_w: float = 4.2, fmt=lambda v: f"{100 * v:.0f}%") -> VGroup:
    """Rows of (name, value, colour, note): the name on the left, a bar for the value, the value and note after it.
    Returns VGroup(rows); each row is VGroup(name, track, bar, value_text)."""
    rows = VGroup()
    for k, (name, v, color, note) in enumerate(items):
        nm = T(name, size, "#E8EAED")
        if nm.width > name_w:
            nm.scale_to_fit_width(name_w)
        nm.move_to(np.array([-0.15, -k * row_h, 0]), aligned_edge=RIGHT)
        track = Rectangle(width=bar_len, height=row_h * 0.58, fill_color="#1A202B", fill_opacity=1, stroke_width=0)
        track.move_to(np.array([bar_len / 2, -k * row_h, 0]))
        L = max(bar_len * max(v, 0) / max_value, 0.02)
        bar = Rectangle(width=L, height=row_h * 0.58, fill_color=color, fill_opacity=0.92, stroke_width=0)
        bar.move_to(np.array([L / 2, -k * row_h, 0]))
        val = TB(fmt(v), size, color)
        if note:
            val = VGroup(val, T(note, size * 0.78, "#9AA3B2")).arrange(RIGHT, buff=0.14)
        val.next_to(bar, RIGHT, buff=0.14)
        rows.add(VGroup(nm, track, bar, val))
    return rows


def _squarify(values, x, y, w, h):
    """Bruls, Huizing and van Wijk's squarified treemap: rectangles (x, y, w, h) for ``values`` (sorted, desc)."""
    rects = []
    vals = list(values)
    total = sum(vals)
    scale = w * h / total
    areas = [v * scale for v in vals]

    def worst(row, side):
        s = sum(row)
        return max(max(side * side * r / (s * s), (s * s) / (side * side * r)) for r in row)

    while areas:
        side = min(w, h)
        row = [areas[0]]
        i = 1
        while i < len(areas) and worst(row + [areas[i]], side) <= worst(row, side):
            row.append(areas[i])
            i += 1
        s = sum(row)
        if w >= h:  # lay the row down the left edge
            cw = s / h
            yy = y
            for a in row:
                rh = a / cw
                rects.append((x, yy, cw, rh))
                yy += rh
            x, w = x + cw, w - cw
        else:  # along the top edge
            rh = s / w
            xx = x
            for a in row:
                cw = a / rh
                rects.append((xx, y, cw, rh))
                xx += cw
            y, h = y + rh, h - rh
        areas = areas[i:]
    return rects


def treemap(items, width: float = 8.0, height: float = 5.0, size: float = 22) -> VGroup:
    """[(name, value, colour, sub)] as blocks with area proportional to value, largest top left."""
    order = sorted(range(len(items)), key=lambda i: -items[i][1])
    rects = _squarify([items[i][1] for i in order], 0.0, 0.0, width, height)
    out = [None] * len(items)
    for i, (x, y, w, h) in zip(order, rects):
        name, v, color, sub = items[i]
        r = Rectangle(width=w, height=h, fill_color=color, fill_opacity=0.82, stroke_color="#0E1117",
                      stroke_width=3)
        r.move_to(np.array([x + w / 2 - width / 2, height / 2 - (y + h / 2), 0]))
        lab = VGroup(TB(name, size, "#0E1117"))
        if sub:
            lab.add(T(sub, size * 0.78, "#0E1117"))
        lab.arrange(DOWN, buff=0.06)
        if lab.width > w - 0.16 or lab.height > h - 0.12:
            lab.scale(min((w - 0.16) / lab.width, (h - 0.12) / lab.height, 1))
        lab.move_to(r)
        out[i] = VGroup(r, lab)
    return VGroup(*out)


def plot_axes(x_range, y_range, x_length=10.0, y_length=4.6, xticks=None, yticks=None, xfmt=None, yfmt=None,
              xlabel: str = "", ylabel: str = "", size: float = 18, grid: bool = True) -> VGroup:
    """Axes with tick labels in the series' face.  Returns VGroup(axes, decorations); use ``.ax`` for c2p."""
    ax = Axes(x_range=[x_range[0], x_range[1], (x_range[1] - x_range[0])], y_range=[y_range[0], y_range[1],
              (y_range[1] - y_range[0])], x_length=x_length, y_length=y_length, tips=False,
              axis_config={"stroke_color": "#5B6372", "stroke_width": 1.6, "include_ticks": False})
    deco = VGroup()
    xfmt = xfmt or (lambda v: f"{v:g}")
    yfmt = yfmt or (lambda v: f"{v:g}")
    for v in (xticks or []):
        deco.add(T(xfmt(v), size, "#9AA3B2").next_to(ax.c2p(v, y_range[0]), DOWN, buff=0.14))
    for v in (yticks or []):
        deco.add(T(yfmt(v), size, "#9AA3B2").next_to(ax.c2p(x_range[0], v), LEFT, buff=0.14))
        if grid and v != y_range[0]:
            deco.add(DashedLine(ax.c2p(x_range[0], v), ax.c2p(x_range[1], v), stroke_color="#2A3140",
                                stroke_width=1, dash_length=0.06))
    if xlabel:
        deco.add(T(xlabel, size, "#9AA3B2").next_to(ax.x_axis, DOWN, buff=0.55))
    if ylabel:
        deco.add(T(ylabel, size, "#9AA3B2").next_to(ax.y_axis, UP, buff=0.18).align_to(ax.y_axis, LEFT))
    g = VGroup(ax, deco)
    g.ax = ax
    return g


def year_bars(pa: VGroup, years, values, color: str, width: float = 0.55, opacity: float = 0.9) -> VGroup:
    """A bar per year on axes from :func:`plot_axes` (bars start at the axis' bottom)."""
    ax = pa.ax
    y0 = ax.y_range[0]
    bars = VGroup()
    for yr, v in zip(years, values):
        p0, p1 = ax.c2p(yr, y0), ax.c2p(yr, v)
        h = max(p1[1] - p0[1], 0.005)
        bars.add(Rectangle(width=width, height=h, fill_color=color, fill_opacity=opacity, stroke_width=0)
                 .move_to(np.array([p0[0], p0[1] + h / 2, 0])))
    return bars


def coin(r: float = 0.11, color: str = I.MONEY) -> VGroup:
    return VGroup(Circle(radius=r, fill_color=color, fill_opacity=1, stroke_color="#8A6A12", stroke_width=1.5),
                  T("$", r * 140, "#5A4300").scale(0.9))


def arrow_line(a, b, color: str = "#9AA3B2", width: float = 2.0) -> VGroup:
    from manim import Arrow
    return Arrow(a, b, buff=0.08, stroke_width=width, color=color, max_tip_length_to_length_ratio=0.12,
                 tip_length=0.16)

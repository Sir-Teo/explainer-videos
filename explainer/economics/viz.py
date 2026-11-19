"""The visual instruments of *Economics, Built* (videos/economics/SYLLABUS.md, section 3), on top of
``explainer.ai.viz``.

* Glyphs: :func:`person`, :func:`islander` (the Island's cast, one colour each), :func:`palm`, :func:`fish_glyph`,
  :func:`coconut`, :func:`island_shape`, :func:`cart`, :func:`loaf`, :func:`pin_glyph`, :func:`coin`.
* :func:`game_stage`: the "Play it" frame, for the game the viewer plays.
* :func:`trader_card`: a buyer's or a seller's card, with its private limit price (Chamberlin 1948; Smith 1962).
* :func:`step_curve`, :func:`market_steps`: demand and supply as the staircases the cards make.
* :func:`tableau_map`: the series map as plumbing.  Five sectors (households, firms, banks, the government, the
  rest of the world) joined by pipes; each part opens one, and what is still sealed at the end is the list of open
  problems.  :func:`flowing` sets dots moving along an open pipe.
* Cards: :func:`study_card` (a design, its sample and its estimate), :func:`dial_face` and :func:`dial_board` (the
  Dials), :func:`fact_card` (your guess, the data, Agora), :func:`call_card` (Called it?), :func:`is_ought_card`
  (where a part turns from what a policy does to whether to do it), :func:`quote_card`, :func:`source_card`.
* Shared with *Psychology, Built*: :func:`point_cards`, :func:`flow_chain`, :func:`quadrant`, :func:`heading`,
  :func:`panel`, :func:`hist` (ideas drawn as pictures, not lists).
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.viz import *  # noqa: F401,F403
from explainer.analysis import label, wrapped_label
from explainer.economics.style import DESIGN_COLOR, DIAL_STATUS, E
from explainer.psychology.viz import CARD_FILL, PANEL_FILL, flow_chain, heading, hist, panel, point_cards, quadrant  # noqa: F401

__all__ = ["person", "islander", "palm", "fish_glyph", "coconut", "island_shape", "cart", "loaf", "pin_glyph", "coin",
           "scissors_logo", "game_stage", "trader_card", "step_curve", "market_steps", "SECTORS", "PIPES", "tableau_map", "flowing",
           "SECTOR_SIZE", "study_card", "dial_face", "dial_board", "fact_card", "call_card", "is_ought_card", "quote_card",
           "source_card", "point_cards", "flow_chain", "quadrant", "heading", "panel", "hist", "CARD_FILL",
           "PANEL_FILL", "accent_card", "dial_card"]


def accent_card(w: float, h: float, color, fill_opacity: float = 0.96, center=ORIGIN) -> VGroup:
    """A dark card with a coloured bar down its left edge."""
    box = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=color, stroke_width=1.8,
                           fill_color=CARD_FILL, fill_opacity=fill_opacity)
    bar = Rectangle(width=0.08, height=max(h - 0.3, 0.1), stroke_width=0, fill_color=color, fill_opacity=1)
    bar.move_to(box.get_left() + RIGHT * 0.14)
    g = VGroup(box, bar).move_to(center)
    g.box, g.bar = box, bar
    return g


# ---------------------------------------------------------------------------
# Glyphs
# ---------------------------------------------------------------------------
def person(height: float = 0.6, color=GREY_A, fill: float = 0.92) -> VGroup:
    """A small figure: a round head on a domed body."""
    r = height * 0.24
    head = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=fill)
    bw = height * 0.74
    body = ArcBetweenPoints(RIGHT * bw / 2, LEFT * bw / 2, angle=PI, stroke_width=0, fill_color=color,
                            fill_opacity=fill)
    body.stretch_to_fit_height(height - 2 * r - height * 0.07)
    head.next_to(body, UP, buff=height * 0.07)
    g = VGroup(body, head)
    g.head, g.body = head, body
    return g.move_to(ORIGIN)


def islander(key: str, height: float = 0.8, name: bool = False, font_size=20) -> VGroup:
    """One of the Island's cast (``explainer.economics.island.CAST``) in their own colour; Crusoe wears a hat.
    ``name``: the name underneath."""
    from explainer.economics.island import CAST

    who = CAST[key]
    p = person(height, who.color)
    g = VGroup(p)
    if key == "crusoe":
        brim = Ellipse(width=height * 0.62, height=height * 0.09, stroke_width=0, fill_color="#8A6A3B",
                       fill_opacity=1).move_to(p.head.get_top() + DOWN * height * 0.03)
        crown = RoundedRectangle(width=height * 0.34, height=height * 0.16, corner_radius=height * 0.05,
                                 stroke_width=0, fill_color="#8A6A3B", fill_opacity=1)
        crown.next_to(brim, UP, buff=-height * 0.03)
        g.add(brim, crown)
    if name:
        g.add(label(who.name, font_size=font_size, color=who.color).next_to(p, DOWN, buff=0.1))
    g.person = p
    return g


def palm(height: float = 2.0, color="#5DBB63", trunk="#9C7A4B", nuts: bool = True) -> VGroup:
    """A palm tree: a leaning trunk, a crown of fronds and (optionally) three coconuts."""
    h = height
    base, top = np.array([0, -h / 2, 0]), np.array([h * 0.16, h * 0.32, 0])
    stem = VMobject(stroke_color=trunk, stroke_width=h * 7)
    stem.set_points_smoothly([base, base + np.array([h * 0.02, h * 0.3, 0]), top])
    fronds = VGroup()
    for ang in (0.35, 0.95, 1.6, 2.25, 2.85):
        tip = top + h * 0.48 * np.array([math.cos(ang), math.sin(ang) * 0.55 - 0.18, 0])
        mid = (top + tip) / 2 + h * 0.12 * np.array([0, 1, 0])
        leaf = VMobject(stroke_color=color, stroke_width=h * 9)
        leaf.set_points_smoothly([top, mid, tip])
        fronds.add(leaf)
    g = VGroup(stem, fronds)
    if nuts:
        g.add(VGroup(*[coconut(h * 0.055).move_to(top + h * np.array([dx, -0.05, 0])) for dx in (-0.05, 0.03, 0.1)]))
    g.top = top
    return g


def coconut(r: float = 0.12, color=None) -> VGroup:
    color = color or E.COCONUT
    c = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)
    eyes = VGroup(*[Dot(radius=r * 0.13, color="#4A3423").move_to(c.get_center() + r * np.array([dx, dy, 0]))
                    for dx, dy in ((-0.28, 0.25), (0.28, 0.25), (0, -0.15))])
    return VGroup(c, eyes)


def fish_glyph(length: float = 0.6, color=None) -> VGroup:
    color = color or E.FISH
    body = Ellipse(width=length * 0.75, height=length * 0.36, stroke_width=0, fill_color=color, fill_opacity=1)
    tail = Polygon(body.get_right() + LEFT * length * 0.04, body.get_right() + RIGHT * length * 0.22 + UP * length * 0.16,
                   body.get_right() + RIGHT * length * 0.22 + DOWN * length * 0.16, stroke_width=0, fill_color=color,
                   fill_opacity=1)
    eye = Dot(body.get_left() + RIGHT * length * 0.14 + UP * length * 0.04, radius=length * 0.03, color=BACKGROUND)
    return VGroup(tail, body, eye)


def island_shape(width: float = 6.0, height: float = 3.0, seed: int = 4) -> VGroup:
    """An island seen from above: a ring of sand round a green interior, on a sea marked by two ripples."""
    rng = np.random.default_rng(seed)
    angles = np.linspace(0, TAU, 14, endpoint=False)
    rad = 1 + 0.12 * rng.standard_normal(len(angles))
    pts = [np.array([width / 2 * r * math.cos(a), height / 2 * r * math.sin(a), 0]) for a, r in zip(angles, rad)]
    sand = VMobject(stroke_width=0, fill_color="#C9B38A", fill_opacity=0.9)
    sand.set_points_smoothly(pts + [pts[0]])
    green = sand.copy().scale(0.82).set_fill("#3E7D4B", 0.95)
    ripples = VGroup(*[sand.copy().scale(s).set_fill(opacity=0).set_stroke("#3A5C7A", 1.5, opacity=0.6)
                       for s in (1.08, 1.18)])
    g = VGroup(ripples, sand, green)
    g.sand, g.green = sand, green
    return g


def loaf(width: float = 0.5, color="#D9A25F") -> VGroup:
    body = RoundedRectangle(width=width, height=width * 0.45, corner_radius=width * 0.2, stroke_width=0,
                            fill_color=color, fill_opacity=1)
    cuts = VGroup(*[Line(body.get_center() + width * np.array([dx - 0.06, -0.08, 0]),
                         body.get_center() + width * np.array([dx + 0.06, 0.1, 0]), color="#8C5A2B",
                         stroke_width=2) for dx in (-0.18, 0, 0.18)])
    return VGroup(body, cuts)


def cart(width: float = 1.1, color="#8A6A3B", load=None) -> VGroup:
    """A farm cart with two wheels, loaded (``load``: a mobject, default three loaves)."""
    box = Polygon([-width / 2, 0, 0], [width / 2, 0, 0], [width * 0.42, -width * 0.28, 0],
                  [-width * 0.42, -width * 0.28, 0], stroke_width=0, fill_color=color, fill_opacity=1)
    wheels = VGroup(*[Circle(radius=width * 0.13, stroke_color="#5B4527", stroke_width=width * 3,
                             fill_color=BACKGROUND, fill_opacity=1).move_to([dx * width, -width * 0.32, 0])
                      for dx in (-0.28, 0.28)])
    shaft = Line([width / 2, -width * 0.05, 0], [width * 0.82, -width * 0.18, 0], color=color, stroke_width=width * 4)
    if load is None:
        load = VGroup(*[loaf(width * 0.32) for _ in range(3)]).arrange(RIGHT, buff=width * 0.02)
    load.next_to(box, UP, buff=-width * 0.04)
    return VGroup(shaft, box, wheels, load)


def pin_glyph(height: float = 0.8, color=GREY_A) -> VGroup:
    shaft = Line(DOWN * height / 2, UP * height * 0.42, color=color, stroke_width=height * 5)
    head = Dot(UP * height * 0.44, radius=height * 0.07, color=color)
    return VGroup(shaft, head)


def coin(r: float = 0.22, color=None) -> VGroup:
    color = color or E.ACCENT
    outer = Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.25)
    inner = Circle(radius=r * 0.68, stroke_color=color, stroke_width=1.5)
    return VGroup(outer, inner)


def scissors_logo(size: float = 1.6, stroke_width: float = 7) -> VGroup:
    """The series' mark: Marshall's scissors.  A falling blue blade (demand) and a rising amber one (supply) that
    cross at a point, the price."""
    d = Line(np.array([-size / 2, size / 2, 0]), np.array([size / 2, -size / 2, 0]), color=E.DEMAND,
             stroke_width=stroke_width)
    s = Line(np.array([-size / 2, -size / 2, 0]), np.array([size / 2, size / 2, 0]), color=E.SUPPLY,
             stroke_width=stroke_width)
    p = Dot(ORIGIN, radius=stroke_width * 0.018, color=WHITE)
    g = VGroup(d, s, p)
    g.demand, g.supply, g.price = d, s, p
    return g


# ---------------------------------------------------------------------------
# Play it
# ---------------------------------------------------------------------------
def game_stage(width: float = 9.0, height: float = 5.0, tag: str = r"Play it", center=ORIGIN) -> VGroup:
    """The frame for a game the viewer plays: a bordered stage in the series' accent and a tag with a coin.
    ``.box`` is the stage (draw at ``stage.box.get_center()``), ``.tag`` the label."""
    box = RoundedRectangle(width=width, height=height, corner_radius=0.2, stroke_color=E.ACCENT, stroke_width=3,
                           fill_color="#07090D", fill_opacity=1)
    t = label(tag, font_size=26, color=E.ACCENT)
    tg = VGroup(coin(0.15), t).arrange(RIGHT, buff=0.14)
    plate = RoundedRectangle(width=tg.width + 0.4, height=tg.height + 0.22, corner_radius=0.1, stroke_color=E.ACCENT,
                             stroke_width=2, fill_color=BACKGROUND, fill_opacity=1)
    plate.move_to(box.get_corner(UL) + RIGHT * (plate.width / 2 + 0.35))
    tg.move_to(plate)
    g = VGroup(box, plate, tg).move_to(center)
    g.box, g.tag = box, VGroup(plate, tg)
    return g


def trader_card(side: str, limit: float, you: bool = False, width: float = 1.7, font_size=34,
                show_rule: bool = True) -> VGroup:
    """A trader's card, as handed out in Chamberlin's and Smith's classrooms: BUYER (blue) or SELLER (amber), the
    private limit price, and what it means ("pay at most" or "take at least").  ``you``: the card the viewer
    holds, ringed in the accent."""
    buyer = side == "buy"
    color = E.DEMAND if buyer else E.SUPPLY
    h = width * 1.4
    box = RoundedRectangle(width=width, height=h, corner_radius=0.12, stroke_color=E.ACCENT if you else color,
                           stroke_width=4 if you else 2, fill_color="#10151F", fill_opacity=1)
    band = Rectangle(width=width - 0.08, height=h * 0.22, stroke_width=0, fill_color=color, fill_opacity=0.85)
    band.move_to(box.get_top() + DOWN * (h * 0.11 + 0.04))
    who = label(r"BUYER" if buyer else r"SELLER", font_size=font_size * 0.55, color=BACKGROUND).move_to(band)
    price = label(rf"\${limit:.2f}", font_size=font_size, color=WHITE).move_to(box.get_center() + DOWN * h * 0.04)
    g = VGroup(box, band, who, price)
    if show_rule:
        rule = label(r"pay at most" if buyer else r"take at least", font_size=font_size * 0.42, color=GREY_A)
        rule.next_to(price, DOWN, buff=0.12)
        g.add(rule)
        g.rule = rule
    if you:
        tag = label(r"you", font_size=font_size * 0.5, color=E.ACCENT).next_to(box, UP, buff=0.08)
        g.add(tag)
    g.box, g.price, g.side, g.limit = box, price, side, limit
    return g


def step_curve(ax, steps, color, stroke_width=4) -> VMobject:
    """A staircase on ``ax`` from ``[(q0, q1, p), ...]``: flat at height p from q0 to q1, vertical between steps."""
    pts = []
    for k, (q0, q1, p) in enumerate(steps):
        a, b = ax.c2p(q0, p), ax.c2p(q1, p)
        if pts:
            pts.append(a)
        else:
            pts.append(a)
        pts.append(b)
    m = VMobject(stroke_color=color, stroke_width=stroke_width)
    m.set_points_as_corners(pts)
    return m


def market_steps(ax, steps: dict, stroke_width=4) -> VGroup:
    """Demand (blue) and supply (amber) staircases from :meth:`explainer.economics.agora.market.Market.steps`."""
    d = step_curve(ax, steps["demand"], E.DEMAND, stroke_width)
    s = step_curve(ax, steps["supply"], E.SUPPLY, stroke_width)
    g = VGroup(d, s)
    g.demand, g.supply = d, s
    return g


# ---------------------------------------------------------------------------
# The Tableau
# ---------------------------------------------------------------------------
SECTORS = {  # key: (name, colour, centre)
    "households": (r"households", E.HOUSEHOLDS, np.array([-4.9, 0.0, 0])),
    "firms": (r"firms", E.FIRMS, np.array([1.7, 0.0, 0])),
    "government": (r"government", E.GOVERNMENT, np.array([-1.6, 2.75, 0])),
    "banks": (r"banks", E.BANKS, np.array([-1.6, -2.75, 0])),
    "world": (r"rest of the world", E.WORLD, np.array([5.6, 0.0, 0])),
}
SECTOR_SIZE = (2.6, 1.2)
# (key, from, to, label, the part that opens it, the route's points, where the label sits, its alignment)
PIPES = [
    ("spending", "households", "firms", r"spending", 2, ((-3.6, 0.32), (-1.6, 1.0), (0.4, 0.32)),
     (-2.55, 1.02), DOWN),
    ("goods", "firms", "households", r"goods and services", 2, ((0.4, -0.32), (-1.6, -1.0), (-3.6, -0.32)),
     (-2.55, -1.05), UP),
    ("labour", "households", "firms", r"labour", 24, ((-3.6, 0.0), (-1.6, 0.0), (0.4, 0.0)), (-2.6, 0.2), ORIGIN),
    ("taxes", "households", "government", r"taxes", 41, ((-4.9, 0.6), (-4.75, 2.45), (-2.9, 2.75)),
     (-5.55, 1.75), ORIGIN),
    ("public", "government", "firms", r"public spending", 32, ((-0.3, 2.75), (1.55, 2.5), (1.7, 0.6)),
     (2.85, 1.75), ORIGIN),
    ("saving", "households", "banks", r"saving", 22, ((-4.9, -0.6), (-4.75, -2.45), (-2.9, -2.75)),
     (-5.6, -1.75), ORIGIN),
    ("loans", "banks", "firms", r"loans", 26, ((-0.3, -2.5), (1.55, -2.35), (1.7, -0.6)), (2.35, -1.75), ORIGIN),
    ("money", "government", "banks", r"money", 25, ((-1.6, 2.15), (-1.6, 0.0), (-1.6, -2.15)), (-1.05, 1.62),
     ORIGIN),
    ("trade", "firms", "world", r"trade", 35, ((3.0, 0.0), (3.65, 0.0), (4.3, 0.0)), (3.65, 0.3), ORIGIN),
    ("capital", "world", "banks", r"capital flows", 34, ((5.6, -0.6), (5.45, -2.8), (4.6, -3.05), (-0.3, -3.05)),
     (2.4, -3.35), ORIGIN),
]


def tableau_map(open_pipes=(), lit=(), width: float = 13.4, font_size=22, sealed_labels: bool = True) -> VGroup:
    """The economy as plumbing, after Quesnay's *Tableau* (1758) and Phillips's machine (1949).  Five tanks, the
    sectors; ten pipes between them, each labelled with the part that opens it.  Pipes in ``open_pipes`` are drawn in
    the colour of the sector they leave, with an arrow; the rest are sealed (dashed, grey, with a valve).  Sectors in
    ``lit`` glow.  Returns a VGroup with ``.sector[key]`` (each with ``.box``, ``.level`` and ``.name``),
    ``.pipe[key]`` (each with ``.path``, ``.label``, ``.valve``, ``.part``) and ``.paths`` (the pipe curves by key,
    for :func:`flowing`)."""
    g = VGroup()
    g.sector, g.pipe, g.paths = {}, {}, {}
    tanks = VGroup()
    w, h = SECTOR_SIZE
    for key, (name, color, pos) in SECTORS.items():
        box = RoundedRectangle(width=w, height=h, corner_radius=0.22, stroke_color=color,
                               stroke_width=3.5 if key in lit else 2.2, fill_color=color,
                               fill_opacity=0.24 if key in lit else 0.1).move_to(pos)
        level = Rectangle(width=w - 0.3, height=0.18, stroke_width=0, fill_color=color, fill_opacity=0.55)
        level.move_to(box.get_bottom() + UP * 0.22)
        nm = label(name, font_size=font_size + 2, color=color)
        if nm.width > w - 0.3:
            nm.width = w - 0.3
        nm.move_to(box.get_center() + UP * 0.12)
        s = VGroup(box, level, nm)
        s.box, s.name, s.level = box, nm, level
        g.sector[key] = s
        tanks.add(s)
    pipes = VGroup()
    for key, a, b, text, part, route, at, align in PIPES:
        pts = [np.array([x, y, 0.0]) for x, y in route]
        path = VMobject()
        if len(pts) == 3 and np.allclose(np.cross(pts[1] - pts[0], pts[2] - pts[1]), 0):
            path.set_points_as_corners(pts)
        else:
            path.set_points_smoothly(pts)
        is_open = key in open_pipes
        color = SECTORS[a][1] if is_open else GREY_D
        if is_open:
            line = path.copy().set_stroke(color, 4)
            tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.12)
            tangent = path.point_from_proportion(1.0) - path.point_from_proportion(0.97)
            tip.rotate(math.atan2(tangent[1], tangent[0]) - PI / 2).move_to(path.point_from_proportion(0.985))
            line = VGroup(line, tip)
            valve = VectorizedPoint(path.point_from_proportion(0.5))
        else:
            line = DashedVMobject(path.copy().set_stroke(GREY_D, 2.5), num_dashes=max(8, int(path.get_arc_length() * 4)))
            valve = VGroup(Circle(radius=0.11, stroke_color=GREY_C, stroke_width=2, fill_color=BACKGROUND,
                                  fill_opacity=1), Line(LEFT * 0.08, RIGHT * 0.08, color=GREY_C, stroke_width=2))
            valve.move_to(path.point_from_proportion({"spending": 0.62, "goods": 0.62, "labour": 0.25}.get(key, 0.5)))
        lab_text = text if is_open or not sealed_labels else rf"{text}\ \ ({part})"
        lab = label(lab_text, font_size=font_size - 4, color=color if is_open else GREY_B)
        lab.move_to(np.array([at[0], at[1], 0.0]))
        pp = VGroup(line, valve, lab)
        pp.path, pp.label, pp.valve, pp.part, pp.open, pp.line = path, lab, valve, part, is_open, line
        g.pipe[key] = pp
        g.paths[key] = path
        pipes.add(pp)
    # the bare curves ride along, invisible, so that scaling or moving the map moves what flowing() follows
    rails = VGroup(*g.paths.values()).set_stroke(opacity=0).set_fill(opacity=0)
    g.add(pipes, tanks, rails)
    g.tanks, g.pipes, g.rails = tanks, pipes, rails
    if g.width > width:
        g.width = width
    return g


def flowing(path: VMobject, color, n: int = 6, period: float = 3.0, radius: float = 0.055) -> VGroup:
    """``n`` dots moving along ``path`` in a loop, one lap every ``period`` seconds (an updater; clear it before
    fading)."""
    t = ValueTracker(0.0)
    dots = VGroup(*[Dot(radius=radius, color=color) for _ in range(n)])

    def upd(m, dt):
        t.increment_value(dt / period)
        for k, d in enumerate(m):
            d.move_to(path.point_from_proportion((t.get_value() + k / n) % 1.0))

    dots.add_updater(upd)
    upd(dots, 0)
    return dots


# ---------------------------------------------------------------------------
# Cards
# ---------------------------------------------------------------------------
def study_card(title: str, who: str, rows, design: str = "", width: float = 6.2, font_size=22,
               color=None) -> VGroup:
    """A study: its title, who and when, and rows ``(key, value)``: what varied, the sample, the result.  ``design``
    (``RCT``, ``IV``, ``DiD``, ...) is shown as a chip in the design's colour."""
    color = color or DESIGN_COLOR.get(design, E.SOURCE)
    t = wrapped_label(title, width - 0.8, font_size + 4, WHITE)
    w = label(who, font_size=font_size - 4, color=GREY_B)
    head = VGroup(t, w).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    body = VGroup()
    for k, v in rows:
        kk = label(k, font_size=font_size - 4, color=color)
        vv = wrapped_label(v, width - 2.4, font_size - 2, GREY_A)
        body.add(VGroup(kk, vv).arrange(RIGHT, buff=0.25, aligned_edge=UP))
    for r in body:
        r[1].shift(RIGHT * (1.5 - r[0].width))
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    card = accent_card(width, inner.height + 0.6, color)
    inner.move_to(card).align_to(card.box, LEFT).shift(RIGHT * 0.38)
    g = VGroup(card, inner)
    if design:
        chip_t = label(design, font_size=font_size - 6, color=BACKGROUND)
        chip = RoundedRectangle(width=chip_t.width + 0.3, height=chip_t.height + 0.14, corner_radius=0.08,
                                stroke_width=0, fill_color=color, fill_opacity=1)
        chip_t.move_to(chip)
        ch = VGroup(chip, chip_t).move_to(card.box.get_corner(UR) + LEFT * (chip.width / 2 + 0.2) + DOWN * 0.3)
        g.add(ch)
    g.card, g.head, g.body = card, head, body
    return g


def dial_face(name: str, first: int, radius: float = 0.75, status: str | None = None, value=None, span=(0, 1),
              font_size=18) -> VGroup:
    """One of the Dials as a gauge: an arc with ticks, its name under it and the part that fills it.  An empty dial
    (no ``status``) has no needle and says where it will be measured; a filled one points at ``value`` on ``span``
    and its arc takes the status colour."""
    color = DIAL_STATUS.get(status, GREY_D) if status else GREY_D
    arc = Arc(radius=radius, start_angle=PI * 1.15, angle=-PI * 1.3, stroke_color=color, stroke_width=5)
    ticks = VGroup()
    for k in range(11):
        a = PI * 1.15 - PI * 1.3 * k / 10
        inner = radius * (0.82 if k % 5 else 0.74)
        ticks.add(Line(inner * np.array([math.cos(a), math.sin(a), 0]),
                       radius * 0.95 * np.array([math.cos(a), math.sin(a), 0]), color=GREY_C, stroke_width=1.5))
    hub = Dot(radius=radius * 0.07, color=GREY_B)
    g = VGroup(arc, ticks, hub)
    if status and value is not None:
        f = (value - span[0]) / (span[1] - span[0])
        a = PI * 1.15 - PI * 1.3 * min(max(f, 0), 1)
        needle = Line(ORIGIN, radius * 0.85 * np.array([math.cos(a), math.sin(a), 0]), color=WHITE, stroke_width=3)
        g.add(needle)
        g.needle = needle
    nm = wrapped_label(name, radius * 3.0, font_size, WHITE).next_to(arc, DOWN, buff=0.18)
    sub = label(rf"Part {first}" if not status else status, font_size=font_size - 3,
                color=GREY_B if not status else color).next_to(nm, DOWN, buff=0.08)
    g.add(nm, sub)
    g.arc, g.name, g.sub = arc, nm, sub
    return g


def dial_board(rows, cols: int = 4, radius: float = 0.62, width: float = 13.0, font_size=17) -> VGroup:
    """A grid of dials from :func:`explainer.economics.dials.board` rows (``name``, ``first``, ``status``)."""
    faces = VGroup(*[dial_face(r["name"], r["first"], radius, None if r["n"] == 0 else r["status"],
                               font_size=font_size) for r in rows])
    faces.arrange_in_grid(cols=cols, buff=(0.5, 0.35), cell_alignment=UP)
    if faces.width > width:
        faces.width = width
    faces.faces = list(faces)
    return faces


def dial_card(dial, lo: float, hi: float, width: float = 12.4, font_size=22, ticks=None, short=None) -> VGroup:
    """One dial opened up: its name and status, its estimates as dots on one axis from ``lo`` to ``hi`` (each in its
    design's colour, labelled with who and what), and what the range means for policy.  ``short``: optional labels,
    one per estimate, to use instead of the author and year."""
    from explainer.economics.dials import DESIGNS  # noqa: F401  (the colours below cover every design)

    color = DIAL_STATUS.get(dial.status, GREY_C)
    name = wrapped_label(dial.name, width - 3.4, font_size + 6, WHITE)
    chip_t = label(dial.status, font_size=font_size - 4, color=BACKGROUND)
    chip = RoundedRectangle(width=chip_t.width + 0.3, height=chip_t.height + 0.16, corner_radius=0.08, stroke_width=0,
                            fill_color=color, fill_opacity=1)
    chip_t.move_to(chip)
    head = VGroup(name, VGroup(chip, chip_t)).arrange(RIGHT, buff=0.4, aligned_edge=UP)
    span = width - 1.6
    axis = Line(LEFT * span / 2, RIGHT * span / 2, color=GREY_C, stroke_width=2)

    def X(v):
        return axis.get_left() + RIGHT * span * (v - lo) / (hi - lo)

    marks = VGroup()
    for v in (ticks if ticks is not None else np.linspace(lo, hi, 5)):
        marks.add(Line(X(v) + UP * 0.08, X(v) + DOWN * 0.08, color=GREY_C, stroke_width=2))
        marks.add(MathTex(f"{v:g}".replace("-", "-"), font_size=font_size - 4, color=GREY_B).next_to(X(v), DOWN,
                                                                                                    buff=0.15))
    dots = VGroup()
    for k, e in enumerate(dial.estimates):
        c = DESIGN_COLOR.get(e.design, GREY_B)
        d = Dot(X(e.value), radius=0.1, color=c)
        txt = short[k] if short else rf"{e.who} ({e.year})"
        t = label(txt, font_size=font_size - 5, color=c)
        up = k % 2 == 0
        t.next_to(d, UP if up else DOWN, buff=0.32 if up else 0.62)
        stem = Line(d.get_center(), t.get_bottom() if up else t.get_top(), color=c, stroke_width=1.2,
                    stroke_opacity=0.6)
        dots.add(VGroup(stem, d, t))
    meaning = wrapped_label(dial.meaning, width - 1.0, font_size - 2, GREY_A) if dial.meaning else VGroup()
    body = VGroup(axis, marks, dots)
    inner = VGroup(head, body, meaning).arrange(DOWN, buff=0.75, aligned_edge=LEFT)
    card = accent_card(width, inner.height + 1.0, color)
    inner.move_to(card)
    head.align_to(card.box, LEFT).shift(RIGHT * 0.45)
    if dial.meaning:
        meaning.align_to(card.box, LEFT).shift(RIGHT * 0.45)
    g = VGroup(card, inner)
    g.card, g.head, g.axis, g.marks, g.dots, g.meaning = card, head, axis, marks, dots, meaning
    return g


def fact_card(statement: str, columns=((r"your guess", None), (r"the data", None), (r"Agora", None)),
              width: float = 12.4, font_size=24, colors=(None, WHITE, None)) -> VGroup:
    """One of the Facts: the statement, then three columns, each a heading and a mobject (or ``None`` for a column
    still empty, drawn as a dashed slot).  ``.slots[i]`` is the place to put column ``i``'s content later."""
    colors = [c or d for c, d in zip(colors, (E.ACCENT, WHITE, E.AGORA))]
    tag = label(r"Fact", font_size=font_size - 6, color=E.ACCENT)
    st = wrapped_label(statement, width - 1.0, font_size + 4, WHITE)
    head = VGroup(tag, st).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    cw = (width - 1.0) / 3
    cols = VGroup()
    slots = []
    for (title, content), color in zip(columns, colors):
        t = label(title, font_size=font_size - 2, color=color)
        slot = DashedVMobject(RoundedRectangle(width=cw - 0.2, height=1.5, corner_radius=0.1, stroke_color=GREY_D,
                                               stroke_width=1.5), num_dashes=40)
        col = VGroup(t, slot).arrange(DOWN, buff=0.15)
        if content is not None:
            if content.width > cw - 0.4:
                content.width = cw - 0.4
            if content.height > 1.3:
                content.height = 1.3
            content.move_to(slot)
            col.add(content)
        cols.add(col)
        slots.append(slot)
    cols.arrange(RIGHT, buff=0.2)
    inner = VGroup(head, cols).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    card = accent_card(width, inner.height + 0.6, E.ACCENT)
    inner.move_to(card).align_to(card.box, LEFT).shift(RIGHT * 0.42)
    g = VGroup(card, inner)
    g.card, g.head, g.cols, g.slots = card, head, cols, slots
    return g


def call_card(who: str, when: str, said: str, outcome: str, verdict: str, width: float = 11.0, font_size=24,
              said_value: Mobject | None = None, outcome_value: Mobject | None = None) -> VGroup:
    """Called it?  Who predicted what, when; what happened; and a verdict stamp (``right`` green, ``wrong`` red,
    ``partly right`` amber)."""
    vcolor = {"right": E.GAIN, "wrong": E.MISS, "partly right": "#F2C14E"}.get(verdict, GREY_B)
    tag = label(r"Called it?", font_size=font_size - 4, color=E.PRED)
    w = label(rf"{who}, \ {when}", font_size=font_size - 2, color=GREY_A)
    head = VGroup(tag, w).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
    cw = (width - 1.2) / 2

    def col(title, text, value, color):
        t = label(title, font_size=font_size - 4, color=color)
        body = wrapped_label(text, cw - 0.2, font_size, WHITE)
        parts = [t, body] + ([value] if value is not None else [])
        return VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.14)

    left = col(r"said", said, said_value, E.PRED)
    right = col(r"happened", outcome, outcome_value, WHITE)
    cols = VGroup(left, right).arrange(RIGHT, buff=0.6, aligned_edge=UP)
    inner = VGroup(head, cols).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    card = accent_card(width, inner.height + 0.7, E.PRED)
    inner.move_to(card).align_to(card.box, LEFT).shift(RIGHT * 0.42)
    st = label(verdict, font_size=font_size + 6, color=vcolor)
    stamp = VGroup(RoundedRectangle(width=st.width + 0.4, height=st.height + 0.25, corner_radius=0.08,
                                    stroke_color=vcolor, stroke_width=3), st)
    st.move_to(stamp[0])
    stamp.rotate(-0.12).move_to(card.box.get_corner(UR) + LEFT * (stamp.width / 2 + 0.3) + DOWN * 0.45)
    g = VGroup(card, inner, stamp)
    g.card, g.stamp, g.left, g.right = card, stamp, left, right
    return g


def is_ought_card(is_text: str, ought_text: str, judgment: str, width: float = 11.6, font_size=26) -> VGroup:
    """The step from what a policy does to whether to do it: *is* (white), the value judgment the step needs (the
    middle, in its own colour), *ought*."""
    def row(tag, text, color):
        t = label(tag, font_size=font_size - 2, color=color)
        b = wrapped_label(text, width - 2.6, font_size, color)
        r = VGroup(t, b).arrange(RIGHT, buff=0.35, aligned_edge=UP)
        r[1].shift(RIGHT * (1.4 - r[0].width))
        return r

    a = row(r"is", is_text, WHITE)
    j = row(r"needs", judgment, E.OUGHT)
    o = row(r"ought", ought_text, E.ACCENT)
    arrows = [MathTex(r"\Downarrow", font_size=font_size + 4, color=GREY_B) for _ in range(2)]
    inner = VGroup(a, arrows[0], j, arrows[1], o).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    for ar in arrows:
        ar.shift(RIGHT * 0.5)
    card = accent_card(width, inner.height + 0.7, E.OUGHT)
    inner.move_to(card).align_to(card.box, LEFT).shift(RIGHT * 0.42)
    g = VGroup(card, inner)
    g.card, g.is_row, g.judgment, g.ought = card, a, j, o
    return g


def quote_card(text: str, who: str, width: float = 9.0, font_size=28, color=None) -> VGroup:
    """A passage, with its author and source under it."""
    color = color or E.SOURCE
    mark = label(r"``", font_size=font_size * 2.2, color=color)
    q = wrapped_label(text, width - 1.1, font_size, WHITE)
    w = wrapped_label(who, width - 1.1, font_size - 8, GREY_B)
    inner = VGroup(q, w).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    card = accent_card(width, inner.height + 0.8, color)
    inner.move_to(card).shift(RIGHT * 0.25)
    mark.move_to(card.box.get_corner(UL) + RIGHT * 0.55 + DOWN * 0.42)
    inner.shift(RIGHT * 0.25)
    g = VGroup(card, inner, mark)
    g.card, g.quote, g.who = card, q, w
    return g


def source_card(lines, title: str = r"Sources", width: float = 12.6, font_size=21) -> VGroup:
    """A part's sources on one card: ``lines`` of citations."""
    head = label(title, font_size=font_size + 10)
    rows = VGroup(*[wrapped_label(t, width - 0.6, font_size, GREY_A) for t in lines])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    g = VGroup(head, rows).arrange(DOWN, buff=0.4)
    head.set_x(0)
    if g.height > 7.2:
        g.height = 7.2
    return g.move_to(ORIGIN)

"""Pictures for *Industry, Built*: the things an industry is made of, drawn flat in the 3Blue1Brown manner and built to
move.

Every glyph is a ``VGroup`` with its moving parts named, so a scene can animate them:

* power: :func:`wind_turbine` (``.rotor`` turns with :func:`spin`), :func:`solar_panel`, :func:`solar_farm`,
  :func:`cooling_tower` (nuclear; ``.steam`` rises with :func:`puff`), :func:`gas_plant`, :func:`coal_plant`,
  :func:`dam`, :func:`pylon`;
* making and moving: :func:`castle` (a business behind its moat), :func:`factory` (``.smoke``),
  :func:`conveyor` (items ride it with :func:`run_belt`),
  :func:`plane` (side view), :func:`cabin` (a seat map whose seats fill), :func:`wafer`, :func:`chip`, :func:`truck`,
  :func:`ship`, :func:`server_rack`;
* the city and its people: :func:`skyline` (``.windows`` light up), :func:`house`, :func:`shop`, :func:`person`,
  :func:`crowd`; :func:`sun`, :func:`moon`, :func:`sky` (a background whose colour follows the hour);
* money: :func:`coin`, :func:`coin_stack`, :func:`note_bill`, :func:`coin_flow` (coins flying from one place to
  another);
* readouts: :func:`number` (a live number from cached digits), :func:`counter` (a live string, slow), :func:`memo_redraw` (a label
  from a few strings, each typeset once), :func:`gauge` (a dial whose needle follows a tracker).

Text goes through :func:`tx`, the repo's LaTeX ``label`` with the characters TeX treats specially escaped, so plain
strings such as "$1,099 (43%)" can be passed as they are.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (DOWN, LEFT, ORIGIN, PI, RIGHT, TAU, UP, Arc, Circle, DecimalNumber, Dot, Ellipse, Line, MathTex,
                   Polygon,
                   Rectangle, RoundedRectangle, Square, Triangle, ValueTracker, VGroup, VMobject, always_redraw,
                   interpolate_color, ManimColor)

from explainer.analysis import label

STEEL = "#8B95A7"
DARK = "#1B2230"
GLASS = "#2B3A55"
LIT = "#F6C453"


# ---------------------------------------------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------------------------------------------
_ESC = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
        "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}", "¢": r"\textcent{}",
        "→": r"$\to$", "←": r"$\leftarrow$", "×": r"$\times$", "·": r"$\cdot$", "≈": r"$\approx$",
        "−": "-", "–": "--", "—": "---", "…": r"\ldots{}", "’": "'", "‘": "`", "“": "``", "”": "''",
        "€": r"\texteuro{}", "£": r"\pounds{}", "°": r"$^\circ$", "≥": r"$\geq$", "≤": r"$\leq$", "±": r"$\pm$"}


def esc(s: str) -> str:
    """Escape a plain string for TeX text mode."""
    return "".join(_ESC.get(ch, ch) for ch in s)


def tx(s: str, size: float = 28, color="#E8EAED", bold: bool = False, italic: bool = False):
    """Plain text set in the repo's LaTeX face (escaped; ``\\n`` breaks lines)."""
    body = r"\\".join(esc(line) for line in s.split("\n"))
    if bold:
        body = r"\textbf{" + body + "}"
    if italic:
        body = r"\emph{" + body + "}"
    return label(body, font_size=size, color=color)


# ---------------------------------------------------------------------------------------------------------------
# Power
# ---------------------------------------------------------------------------------------------------------------
def wind_turbine(h: float = 2.4, color: str = "#E8EAED") -> VGroup:
    """A three-bladed turbine on a tapered tower; ``g.rotor`` (hub and blades) turns about ``g.hub``."""
    base_w, top_w = 0.09 * h, 0.035 * h
    tower = Polygon([-base_w / 2, 0, 0], [base_w / 2, 0, 0], [top_w / 2, h, 0], [-top_w / 2, h, 0],
                    stroke_width=0, fill_color=color, fill_opacity=0.9)
    nacelle = RoundedRectangle(corner_radius=0.03 * h, width=0.16 * h, height=0.07 * h, stroke_width=0,
                               fill_color=color, fill_opacity=1).move_to([0.04 * h, h + 0.01 * h, 0])
    hub = Circle(radius=0.035 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([-0.05 * h, h + 0.01 * h, 0])
    blades = VGroup()
    L = 0.55 * h
    for k in range(3):
        b = Polygon([0, 0.02 * h, 0], [L, 0.008 * h, 0], [L, -0.004 * h, 0], [0, -0.02 * h, 0], stroke_width=0,
                    fill_color=color, fill_opacity=0.95)
        b.rotate(PI / 2 + k * TAU / 3, about_point=ORIGIN)
        blades.add(b)
    blades.shift(hub.get_center())
    rotor = VGroup(blades, hub)
    g = VGroup(tower, nacelle, rotor)
    g.rotor, g.hub = rotor, hub
    return g


def spin(turbine: VGroup, speed: float = 1.6) -> VGroup:
    """Turn a turbine's rotor at ``speed`` radians a second (an updater; remove with ``clear_updaters``)."""
    turbine.rotor.add_updater(lambda m, dt: m.rotate(-speed * dt, about_point=turbine.hub.get_center()))
    return turbine


def solar_panel(w: float = 1.4, cells=(3, 6)) -> VGroup:
    """A tilted panel of cells on a post."""
    h = 0.45 * w
    skew = 0.18 * w
    pts = [[-w / 2, 0, 0], [w / 2, 0, 0], [w / 2 + skew, h, 0], [-w / 2 + skew, h, 0]]
    frame = Polygon(*pts, stroke_color="#9DB7E0", stroke_width=1.5, fill_color="#1F4E8C", fill_opacity=1)
    grid = VGroup()
    rows, cols = cells
    for i in range(1, rows):
        f = i / rows
        grid.add(Line([-w / 2 + skew * f, h * f, 0], [w / 2 + skew * f, h * f, 0], stroke_color="#9DB7E0",
                      stroke_width=0.8, stroke_opacity=0.7))
    for j in range(1, cols):
        x = -w / 2 + w * j / cols
        grid.add(Line([x, 0, 0], [x + skew, h, 0], stroke_color="#9DB7E0", stroke_width=0.8, stroke_opacity=0.7))
    post = Line([skew / 2, 0, 0], [skew / 2, -0.35 * w, 0], stroke_color=STEEL, stroke_width=3)
    g = VGroup(post, frame, grid)
    g.face = frame
    return g


def solar_farm(n: int = 4, w: float = 0.9) -> VGroup:
    return VGroup(*[solar_panel(w) for _ in range(n)]).arrange(RIGHT, buff=0.12)


def _hyperboloid(h: float, w: float, n: int = 30):
    """Points of a cooling tower's outline: waist at 70% of the height."""
    left, right = [], []
    for i in range(n + 1):
        y = h * i / n
        t = (y - 0.7 * h) / h
        half = w * (0.33 + 0.9 * t * t) if y < 0.7 * h else w * (0.33 + 0.45 * t * t * 3)
        left.append([-half, y, 0])
        right.append([half, y, 0])
    return left + right[::-1]


def cooling_tower(h: float = 2.0, color: str = "#C9D3E0") -> VGroup:
    """A nuclear plant's cooling tower, with ``g.steam`` puffs above it (animate with :func:`puff`)."""
    body = Polygon(*_hyperboloid(h, 0.42 * h), stroke_width=0, fill_color=color, fill_opacity=0.95)
    shade = Polygon(*_hyperboloid(h, 0.42 * h), stroke_width=0, fill_color=DARK, fill_opacity=0.22)
    shade.stretch(0.45, 0).align_to(body, RIGHT)
    steam = VGroup(*[Circle(radius=0.12 * h * (1 + 0.25 * k), stroke_width=0, fill_color="#F1F4F8",
                            fill_opacity=0.55 - 0.1 * k).move_to([0.05 * h * (k % 2), h * (1.08 + 0.17 * k), 0])
                     for k in range(4)])
    g = VGroup(body, shade, steam)
    g.steam = steam
    return g


def puff(group: VGroup, top: float = 0.9, speed: float = 0.35) -> VGroup:
    """Let a group of round puffs drift up and fade, then start again (an updater)."""
    base = [m.get_center().copy() for m in group]
    state = {"t": 0.0}

    def upd(m, dt):
        state["t"] += dt
        for k, c in enumerate(m):
            ph = (state["t"] * speed + k / len(m)) % 1.0
            c.move_to(base[0] + UP * top * ph + RIGHT * 0.15 * math.sin(6 * ph + k))
            c.set_fill(opacity=0.55 * (1 - ph))
    group.add_updater(upd)
    return group


def gas_plant(h: float = 1.4, color: str = "#F2A65A") -> VGroup:
    """A gas plant: a turbine hall and one tall slim stack."""
    hall = RoundedRectangle(corner_radius=0.05, width=1.3 * h, height=0.55 * h, stroke_width=0, fill_color=STEEL,
                            fill_opacity=0.95).move_to([0, 0.275 * h, 0])
    stack = Rectangle(width=0.12 * h, height=1.05 * h, stroke_width=0, fill_color="#C9D3E0",
                      fill_opacity=1).move_to([0.45 * h, 0.525 * h, 0])
    band = Rectangle(width=0.12 * h, height=0.06 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [0.45 * h, 0.95 * h, 0])
    flame = VGroup(*[Rectangle(width=0.16 * h, height=0.05 * h, stroke_width=0, fill_color=color,
                               fill_opacity=0.9).move_to([-0.3 * h + 0.25 * h * k, 0.38 * h, 0]) for k in range(3)])
    door = Rectangle(width=0.16 * h, height=0.22 * h, stroke_width=0, fill_color=DARK, fill_opacity=1).move_to(
        [-0.35 * h, 0.11 * h, 0])
    smoke = VGroup(*[Circle(radius=0.07 * h * (1 + 0.3 * k), stroke_width=0, fill_color="#B7C0CC",
                            fill_opacity=0.4).move_to([0.45 * h, 1.12 * h + 0.14 * h * k, 0]) for k in range(3)])
    g = VGroup(hall, stack, band, flame, door, smoke)
    g.smoke = smoke
    return g


def coal_plant(h: float = 1.4) -> VGroup:
    """A coal plant: a boiler house, two thick stacks and a coal pile."""
    house_ = Rectangle(width=1.1 * h, height=0.7 * h, stroke_width=0, fill_color=STEEL, fill_opacity=0.95).move_to(
        [0, 0.35 * h, 0])
    stacks = VGroup(*[Rectangle(width=0.16 * h, height=1.25 * h, stroke_width=0, fill_color="#A7B0BD",
                                fill_opacity=1).move_to([x * h, 0.625 * h, 0]) for x in (0.2, 0.42)])
    pile = Polygon([-1.05 * h, 0, 0], [-0.45 * h, 0, 0], [-0.75 * h, 0.32 * h, 0], stroke_width=0, fill_color="#2A2A2E",
                   fill_opacity=1)
    smoke = VGroup(*[Circle(radius=0.09 * h * (1 + 0.3 * k), stroke_width=0, fill_color="#8C929B",
                            fill_opacity=0.5).move_to([0.3 * h, 1.35 * h + 0.17 * h * k, 0]) for k in range(3)])
    g = VGroup(pile, house_, stacks, smoke)
    g.smoke = smoke
    return g


def dam(h: float = 1.2) -> VGroup:
    """A hydro dam: a wedge of concrete, a lake behind it, water out of its foot."""
    wall = Polygon([-0.15 * h, 0, 0], [0.45 * h, 0, 0], [0.12 * h, h, 0], [-0.15 * h, h, 0], stroke_width=0,
                   fill_color="#B9C2CF", fill_opacity=1)
    lake = Polygon([-1.2 * h, 0, 0], [-0.15 * h, 0, 0], [-0.15 * h, 0.85 * h, 0], [-1.2 * h, 0.85 * h, 0],
                   stroke_width=0, fill_color="#3B7DD8", fill_opacity=0.75)
    out = Polygon([0.45 * h, 0, 0], [1.1 * h, 0, 0], [1.1 * h, 0.12 * h, 0], [0.45 * h, 0.12 * h, 0], stroke_width=0,
                  fill_color="#7EC8F5", fill_opacity=0.8)
    return VGroup(lake, wall, out)


def pylon(h: float = 1.6, color: str = STEEL) -> VGroup:
    legs = VGroup(Line([-0.25 * h, 0, 0], [-0.06 * h, h, 0]), Line([0.25 * h, 0, 0], [0.06 * h, h, 0]))
    arms = VGroup(Line([-0.3 * h, 0.8 * h, 0], [0.3 * h, 0.8 * h, 0]), Line([-0.22 * h, 0.62 * h, 0],
                                                                             [0.22 * h, 0.62 * h, 0]))
    cross = VGroup(*[Line([-0.25 * h + 0.19 * h * f, h * f, 0], [0.25 * h - 0.19 * h * (f + 0.2), h * (f + 0.2), 0])
                     for f in (0.0, 0.2, 0.4)])
    g = VGroup(legs, arms, cross)
    g.set_stroke(color, width=2)
    return g


# ---------------------------------------------------------------------------------------------------------------
# Making and moving
# ---------------------------------------------------------------------------------------------------------------
def castle(w: float = 2.0, color: str = "#C9D3E0", moat: float = 0.0, water: str = "#3B7DD8") -> VGroup:
    """A castle (wall, towers, gate) on its ``g.ground``; ``moat`` > 0 rings it with water (``g.moat``) that wide."""
    h = 0.42 * w
    wall = Rectangle(width=0.8 * w, height=h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, h / 2, 0])
    towers = VGroup()
    for x in (-0.42 * w, 0.42 * w):
        t = Rectangle(width=0.18 * w, height=1.45 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
            [x, 0.725 * h, 0])
        cren = VGroup(*[Square(0.05 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
            [x + dx * 0.06 * w, 1.45 * h + 0.025 * w, 0]) for dx in (-1, 0, 1)])
        towers.add(VGroup(t, cren))
    keep = Rectangle(width=0.26 * w, height=1.75 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [0, 0.875 * h, 0])
    flag = VGroup(Line([0, 1.75 * h, 0], [0, 2.05 * h, 0], stroke_color=color, stroke_width=2),
                  Polygon([0, 2.05 * h, 0], [0.12 * w, 1.98 * h, 0], [0, 1.91 * h, 0], stroke_width=0,
                          fill_color="#E8554E", fill_opacity=1))
    merl = VGroup(*[Square(0.045 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [x, h + 0.0225 * w, 0]) for x in np.linspace(-0.3 * w, 0.3 * w, 6)])
    gate = Arc(radius=0.08 * w, start_angle=0, angle=PI, stroke_width=0, fill_color=DARK, fill_opacity=1).move_to(
        [0, 0.12 * w, 0])
    door = Rectangle(width=0.16 * w, height=0.12 * w, stroke_width=0, fill_color=DARK, fill_opacity=1).move_to(
        [0, 0.06 * w, 0])
    shade = Rectangle(width=0.8 * w, height=h, stroke_width=0, fill_color=DARK, fill_opacity=0.12).move_to(
        [0.2 * w, h / 2, 0]).stretch(0.5, 0)
    g = VGroup(wall, shade, merl, towers, keep, flag, door, gate)
    g.ground = Line([-0.6 * w, 0, 0], [0.6 * w, 0, 0])
    if moat > 0:
        ring = Ellipse(width=1.25 * w + 2 * moat, height=0.25 * w + 0.5 * moat, stroke_width=0, fill_color=water,
                       fill_opacity=0.85).move_to([0, 0.0, 0])
        inner = Ellipse(width=1.2 * w, height=0.22 * w, stroke_width=0, fill_color="#3E4A3A", fill_opacity=1).move_to(
            [0, 0.0, 0])
        g.moat = VGroup(ring, inner)
        g.add_to_back(g.moat)
    return g


def factory(w: float = 2.4, color: str = STEEL) -> VGroup:
    """A works with a saw-tooth roof, a chimney (``g.smoke``) and lit windows (``g.windows``)."""
    h = 0.42 * w
    body = Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([0, h / 2, 0])
    teeth = VGroup()
    n = 4
    for k in range(n):
        x0 = -w / 2 + w * k / n
        teeth.add(Polygon([x0, h, 0], [x0 + w / n, h, 0], [x0 + w / n, h + 0.22 * w, 0], stroke_width=0,
                          fill_color=color, fill_opacity=0.95))
    chimney = Rectangle(width=0.1 * w, height=0.6 * w, stroke_width=0, fill_color="#A7B0BD",
                        fill_opacity=1).move_to([0.38 * w, 0.3 * w, 0])
    windows = VGroup(*[Rectangle(width=0.12 * w, height=0.1 * w, stroke_width=0, fill_color=GLASS,
                                 fill_opacity=1).move_to([-0.36 * w + 0.18 * w * k, 0.2 * w, 0]) for k in range(4)])
    smoke = VGroup(*[Circle(radius=0.05 * w * (1 + 0.3 * k), stroke_width=0, fill_color="#B7C0CC",
                            fill_opacity=0.45).move_to([0.38 * w, 0.66 * w + 0.09 * w * k, 0]) for k in range(3)])
    g = VGroup(chimney, body, teeth, windows, smoke)
    g.windows, g.smoke = windows, smoke
    return g


def conveyor(length: float = 6.0, n: int = 8, item_color: str = LIT, item: float = 0.32) -> VGroup:
    """A belt on rollers with ``n`` boxes on it (``g.items``); :func:`run_belt` sets them moving."""
    belt = RoundedRectangle(corner_radius=0.12, width=length, height=0.24, stroke_color=STEEL, stroke_width=2,
                            fill_color=DARK, fill_opacity=1)
    rollers = VGroup(*[Circle(radius=0.09, stroke_color=STEEL, stroke_width=1.5, fill_color="#2E3645",
                              fill_opacity=1).move_to([-length / 2 + 0.2 + (length - 0.4) * k / 9, 0, 0])
                       for k in range(10)])
    items = VGroup(*[RoundedRectangle(corner_radius=0.04, width=item, height=item, stroke_width=0,
                                      fill_color=item_color, fill_opacity=0.95).move_to(
        [-length / 2 + length * (k + 0.5) / n, 0.12 + item / 2, 0]) for k in range(n)])
    g = VGroup(belt, rollers, items)
    g.items, g.length = items, length
    return g


def run_belt(belt: VGroup, speed: float = 0.8) -> VGroup:
    """Move a conveyor's items to the right, wrapping round (an updater on ``belt.items``)."""
    left = belt[0].get_left()[0]
    L = belt.length

    def upd(m, dt):
        for it in m:
            x = it.get_center()[0] + speed * dt
            if x > left + L:
                x -= L
            it.set_x(x)
    belt.items.add_updater(upd)
    return belt


def plane(length: float = 4.0, color: str = "#E8EAED", windows: bool = True) -> VGroup:
    """An airliner in side view, nose to the right."""
    L = length
    fus = RoundedRectangle(corner_radius=0.07 * L, width=0.9 * L, height=0.14 * L, stroke_width=0, fill_color=color,
                           fill_opacity=1)
    nose = Polygon([0.45 * L, 0.07 * L, 0], [0.55 * L, 0.0, 0], [0.45 * L, -0.07 * L, 0], stroke_width=0,
                   fill_color=color, fill_opacity=1)
    nose_cap = Arc(radius=0.07 * L, start_angle=-PI / 2, angle=PI, stroke_width=0, fill_color=color,
                   fill_opacity=1).move_to([0.47 * L, 0, 0])
    tail = Polygon([-0.45 * L, 0.06 * L, 0], [-0.3 * L, 0.06 * L, 0], [-0.43 * L, 0.26 * L, 0],
                   [-0.5 * L, 0.26 * L, 0], stroke_width=0, fill_color=color, fill_opacity=1)
    wing = Polygon([-0.05 * L, -0.02 * L, 0], [0.12 * L, -0.02 * L, 0], [-0.12 * L, -0.2 * L, 0],
                   [-0.2 * L, -0.2 * L, 0], stroke_width=0, fill_color="#B9C2CF", fill_opacity=1)
    engine = RoundedRectangle(corner_radius=0.02 * L, width=0.12 * L, height=0.05 * L, stroke_width=0,
                              fill_color="#9AA4B2", fill_opacity=1).move_to([-0.02 * L, -0.1 * L, 0])
    parts = [tail, fus, nose, wing, engine]
    if windows:
        win = VGroup(*[Circle(radius=0.012 * L, stroke_width=0, fill_color=GLASS, fill_opacity=1).move_to(
            [-0.35 * L + 0.035 * L * k, 0.025 * L, 0]) for k in range(21)])
        cockpit = Polygon([0.43 * L, 0.04 * L, 0], [0.5 * L, 0.01 * L, 0], [0.43 * L, 0.01 * L, 0], stroke_width=0,
                          fill_color=GLASS, fill_opacity=1)
        parts += [win, cockpit]
    del nose_cap
    return VGroup(*parts)


def cabin(rows: int = 20, seats=(3, 3), size: float = 0.22, gap: float = 0.05) -> VGroup:
    """A top-down seat map: ``g.seats`` in boarding order (front to back); colour them to show who is aboard."""
    seats_g = VGroup()
    a, b = seats
    for r in range(rows):
        for c in range(a + b):
            x = r * (size + gap)
            y = (c - (a + b) / 2 + 0.5) * (size + gap) + (0.18 if c >= a else -0.18) * 0 + (size * 0.6 if c >= a else 0)
            seats_g.add(RoundedRectangle(corner_radius=0.04, width=size, height=size, stroke_width=0,
                                         fill_color="#2E3645", fill_opacity=1).move_to([x, y, 0]))
    seats_g.move_to(ORIGIN)
    hull = RoundedRectangle(corner_radius=0.4, width=seats_g.width + 0.9, height=seats_g.height + 0.35,
                            stroke_color=STEEL, stroke_width=2, fill_opacity=0).move_to(seats_g)
    g = VGroup(hull, seats_g)
    g.seats = seats_g
    return g


def wafer(r: float = 1.2, die: float = 0.16, color: str = "#B58CFF") -> VGroup:
    """A silicon wafer with its grid of dies (``g.dies``)."""
    disc = Circle(radius=r, stroke_color="#C9D3E0", stroke_width=2, fill_color="#3A3F52", fill_opacity=1)
    dies = VGroup()
    n = int(2 * r / die)
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x, y = i * die, j * die
            if math.hypot(abs(x) + die / 2, abs(y) + die / 2) < r * 0.96:
                dies.add(Square(die * 0.86, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to([x, y, 0]))
    notch = Triangle(stroke_width=0, fill_color="#0E1117", fill_opacity=1).scale(0.06).move_to([0, -r + 0.03, 0])
    g = VGroup(disc, dies, notch)
    g.dies = dies
    return g


def chip(s: float = 0.8, color: str = "#B58CFF") -> VGroup:
    body = RoundedRectangle(corner_radius=0.06 * s, width=s, height=s, stroke_width=0, fill_color="#2E3645",
                            fill_opacity=1)
    core = Square(0.55 * s, stroke_width=0, fill_color=color, fill_opacity=0.9)
    pins = VGroup()
    for k in range(5):
        f = -0.4 + 0.2 * k
        for d, vertical in ((UP, True), (DOWN, True), (LEFT, False), (RIGHT, False)):
            p = Line(ORIGIN, d * 0.12 * s, stroke_color="#C9D3E0", stroke_width=2)
            along = RIGHT if vertical else UP
            p.move_to(d * (0.5 * s + 0.06 * s) + along * f * s)
            pins.add(p)
    return VGroup(pins, body, core)


def truck(w: float = 1.6, color: str = "#7EC8F5") -> VGroup:
    box = RoundedRectangle(corner_radius=0.04, width=0.68 * w, height=0.38 * w, stroke_width=0, fill_color=color,
                           fill_opacity=0.95).move_to([-0.12 * w, 0.27 * w, 0])
    cab = RoundedRectangle(corner_radius=0.05, width=0.24 * w, height=0.26 * w, stroke_width=0, fill_color="#C9D3E0",
                           fill_opacity=1).move_to([0.36 * w, 0.21 * w, 0])
    win = Rectangle(width=0.1 * w, height=0.08 * w, stroke_width=0, fill_color=GLASS, fill_opacity=1).move_to(
        [0.4 * w, 0.26 * w, 0])
    wheels = VGroup(*[Circle(radius=0.07 * w, stroke_width=0, fill_color="#20242C", fill_opacity=1).move_to(
        [x * w, 0.07 * w, 0]) for x in (-0.35, -0.2, 0.36)])
    return VGroup(box, cab, win, wheels)


def ship(w: float = 3.0, boxes: int = 12) -> VGroup:
    hull = Polygon([-0.5 * w, 0.12 * w, 0], [0.5 * w, 0.12 * w, 0], [0.42 * w, 0, 0], [-0.44 * w, 0, 0],
                   stroke_width=0, fill_color="#C0392B", fill_opacity=0.95)
    deck = Rectangle(width=0.98 * w, height=0.03 * w, stroke_width=0, fill_color="#2E3645", fill_opacity=1).move_to(
        [0, 0.135 * w, 0])
    cols = ["#7EC8F5", "#F2A65A", "#7BD88F", "#F2C14E", "#B58CFF", "#E8554E"]
    stack = VGroup()
    for k in range(boxes):
        r, c = divmod(k, 6)
        stack.add(Rectangle(width=0.12 * w, height=0.06 * w, stroke_color="#0E1117", stroke_width=1,
                            fill_color=cols[(k * 5) % len(cols)], fill_opacity=0.95).move_to(
            [-0.36 * w + 0.125 * c * w, 0.18 * w + 0.062 * r * w, 0]))
    bridge = Rectangle(width=0.07 * w, height=0.14 * w, stroke_width=0, fill_color="#E8EAED", fill_opacity=1).move_to(
        [0.4 * w, 0.21 * w, 0])
    g = VGroup(hull, deck, stack, bridge)
    g.boxes = stack
    return g


def server_rack(h: float = 1.6, lit: float = 0.7) -> VGroup:
    frame = RoundedRectangle(corner_radius=0.04, width=0.5 * h, height=h, stroke_color=STEEL, stroke_width=2,
                             fill_color="#161B25", fill_opacity=1)
    units = VGroup()
    n = 9
    for k in range(n):
        y = -0.45 * h + 0.9 * h * (k + 0.5) / n
        units.add(Rectangle(width=0.42 * h, height=0.07 * h, stroke_width=0, fill_color="#2E3645",
                            fill_opacity=1).move_to([0, y, 0]))
        units.add(Dot([0.15 * h, y, 0], radius=0.012 * h, color="#7BD88F" if (k / n) < lit else "#3A4152"))
    return VGroup(frame, units)


# ---------------------------------------------------------------------------------------------------------------
# The city and its people
# ---------------------------------------------------------------------------------------------------------------
def skyline(w: float = 5.0, seed: int = 4) -> VGroup:
    """A row of towers; ``g.windows`` is every window, in random order, so lighting the first k shows demand."""
    rng = np.random.default_rng(seed)
    towers, windows = VGroup(), []
    x = -w / 2
    while x < w / 2 - 0.25:
        bw = rng.uniform(0.35, 0.75)
        bh = rng.uniform(0.9, 2.6)
        t = Rectangle(width=bw, height=bh, stroke_width=0, fill_color="#1E2633", fill_opacity=1).move_to(
            [x + bw / 2, bh / 2, 0])
        towers.add(t)
        for i in range(int(bh / 0.22) - 1):
            for j in range(max(1, int(bw / 0.16))):
                windows.append(Rectangle(width=0.07, height=0.08, stroke_width=0, fill_color="#2A3446",
                                         fill_opacity=1).move_to([x + 0.1 + j * 0.16, 0.18 + i * 0.22, 0]))
        x += bw + rng.uniform(0.04, 0.12)
    order = rng.permutation(len(windows))
    win = VGroup(*[windows[i] for i in order])
    g = VGroup(towers, win)
    g.windows = win
    return g


def light(windows: VGroup, share: float, on: str = LIT, off: str = "#2A3446") -> None:
    """Light the first ``share`` of a skyline's windows."""
    k = int(round(share * len(windows)))
    for i, wdw in enumerate(windows):
        wdw.set_fill(on if i < k else off)


def house(w: float = 0.8, color: str = "#C9D3E0") -> VGroup:
    body = Rectangle(width=w, height=0.6 * w, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to(
        [0, 0.3 * w, 0])
    roof = Polygon([-0.6 * w, 0.6 * w, 0], [0.6 * w, 0.6 * w, 0], [0, 1.0 * w, 0], stroke_width=0, fill_color="#E8554E",
                   fill_opacity=0.95)
    door = Rectangle(width=0.18 * w, height=0.32 * w, stroke_width=0, fill_color=DARK, fill_opacity=1).move_to(
        [0, 0.16 * w, 0])
    win = Square(0.18 * w, stroke_width=0, fill_color=GLASS, fill_opacity=1).move_to([0.27 * w, 0.38 * w, 0])
    return VGroup(body, roof, door, win)


def shop(w: float = 1.2, color: str = "#7BD88F") -> VGroup:
    body = Rectangle(width=w, height=0.6 * w, stroke_width=0, fill_color="#C9D3E0", fill_opacity=0.95).move_to(
        [0, 0.3 * w, 0])
    awning = VGroup(*[Polygon([-w / 2 + w * k / 6, 0.62 * w, 0], [-w / 2 + w * (k + 1) / 6, 0.62 * w, 0],
                              [-w / 2 + w * (k + 1) / 6, 0.5 * w, 0], [-w / 2 + w * k / 6, 0.5 * w, 0],
                              stroke_width=0, fill_color=color if k % 2 == 0 else "#E8EAED", fill_opacity=1)
                      for k in range(6)])
    window = Rectangle(width=0.5 * w, height=0.25 * w, stroke_width=0, fill_color=GLASS, fill_opacity=1).move_to(
        [-0.15 * w, 0.25 * w, 0])
    door = Rectangle(width=0.16 * w, height=0.3 * w, stroke_width=0, fill_color=DARK, fill_opacity=1).move_to(
        [0.3 * w, 0.15 * w, 0])
    return VGroup(body, awning, window, door)


def pig(w: float = 1.0, color: str = "#F2A7B5") -> VGroup:
    """A hog, facing right: body, head, snout, ear, legs and a curled tail."""
    body = Ellipse(width=w, height=0.6 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, 0.42 * w, 0])
    head = Circle(radius=0.2 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0.45 * w, 0.52 * w, 0])
    snout = Ellipse(width=0.14 * w, height=0.12 * w, stroke_width=0, fill_color="#E58A9C", fill_opacity=1).move_to(
        [0.64 * w, 0.48 * w, 0])
    ear = Polygon([0.36 * w, 0.68 * w, 0], [0.46 * w, 0.84 * w, 0], [0.5 * w, 0.66 * w, 0], stroke_width=0,
                  fill_color="#E58A9C", fill_opacity=1)
    eye = Dot([0.5 * w, 0.58 * w, 0], radius=0.022 * w, color=DARK)
    legs = VGroup(*[Rectangle(width=0.09 * w, height=0.2 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [x * w, 0.1 * w, 0]) for x in (-0.3, -0.14, 0.14, 0.3)])
    tail = Arc(radius=0.06 * w, start_angle=0, angle=1.6 * PI, stroke_color=color, stroke_width=3).move_to(
        [-0.53 * w, 0.55 * w, 0])
    return VGroup(legs, body, tail, head, ear, snout, eye)


def crane(h: float = 2.0, color: str = "#F2C14E") -> VGroup:
    """A shipyard's gantry crane: two legs, a beam and a hanging hook."""
    legs = VGroup(*[Rectangle(width=0.06 * h, height=h, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [x * h, 0.5 * h, 0]) for x in (-0.35, 0.35)])
    beam = Rectangle(width=0.95 * h, height=0.08 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [0, h, 0])
    cable = Line([0.1 * h, h, 0], [0.1 * h, 0.62 * h, 0], stroke_color="#C9D3E0", stroke_width=1.5)
    hook = Arc(radius=0.04 * h, start_angle=PI, angle=PI, stroke_color="#C9D3E0", stroke_width=2).move_to(
        [0.1 * h, 0.6 * h, 0])
    return VGroup(legs, beam, cable, hook)


def person(h: float = 0.6, color: str = "#C9D3E0") -> VGroup:
    r = h * 0.22
    head = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, h - r, 0])
    body = Arc(radius=h * 0.36, start_angle=0, angle=PI, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [0, h * 0.2, 0])
    body.stretch_to_fit_height(h * 0.48).move_to([0, h * 0.24, 0])
    return VGroup(body, head)


def crowd(n: int = 10, h: float = 0.5, color: str = "#C9D3E0", cols: int = 10) -> VGroup:
    g = VGroup(*[person(h, color) for _ in range(n)])
    g.arrange_in_grid(rows=math.ceil(n / cols), cols=min(n, cols), buff=(0.08, 0.1))
    return g


def sun(r: float = 0.45) -> VGroup:
    disc = Circle(radius=r, stroke_width=0, fill_color="#F6C453", fill_opacity=1)
    rays = VGroup(*[Line(ORIGIN, RIGHT * 0.32 * r, stroke_color="#F6C453", stroke_width=3).shift(RIGHT * 1.2 * r)
                    .rotate(k * TAU / 12, about_point=ORIGIN) for k in range(12)])
    return VGroup(rays, disc)


def moon(r: float = 0.35) -> VGroup:
    disc = Circle(radius=r, stroke_width=0, fill_color="#E8EAED", fill_opacity=1)
    bite = Circle(radius=r, stroke_width=0, fill_color="#0E1117", fill_opacity=1).shift(RIGHT * 0.4 * r + UP * 0.15 * r)
    return VGroup(disc, bite)


def sky_color(hour: float, night: str = "#0B1220", day: str = "#1C3557") -> ManimColor:
    """The sky's colour at an hour of the day (darkest at midnight, brightest at 1 pm)."""
    s = max(0.0, math.sin(math.pi * (hour - 6) / 14)) if 6 <= hour <= 20 else 0.0
    return interpolate_color(ManimColor(night), ManimColor(day), s)


def sun_height(hour: float) -> float:
    """How high the sun is, 0 at night to 1 at solar noon (6 am to 8 pm)."""
    return max(0.0, math.sin(math.pi * (hour - 6) / 14)) if 6 <= hour <= 20 else 0.0


# ---------------------------------------------------------------------------------------------------------------
# Money
# ---------------------------------------------------------------------------------------------------------------
def coin(r: float = 0.14, color: str = "#F6C453") -> VGroup:
    disc = Circle(radius=r, stroke_color="#8A6A12", stroke_width=1.5, fill_color=color, fill_opacity=1)
    rim = Circle(radius=0.72 * r, stroke_color="#8A6A12", stroke_width=1, fill_opacity=0)
    return VGroup(disc, rim)


def coin_stack(n: int, r: float = 0.14, color: str = "#F6C453") -> VGroup:
    g = VGroup()
    for k in range(n):
        e = Ellipse(width=2 * r, height=0.7 * r, stroke_color="#8A6A12", stroke_width=1, fill_color=color,
                    fill_opacity=1).move_to([0, k * 0.22 * r, 0])
        g.add(e)
    return g


def coin_flow(src, dst, n: int = 6, r: float = 0.1, arc: float = -0.7, lag: float = 0.12, run_time: float = 1.6,
              color: str = "#F6C453"):
    """Coins flying from ``src`` to ``dst`` along an arc: returns ``(coins, animation)``; add the coins, play the
    animation, then remove them (or leave them where they landed)."""
    from manim import ArcBetweenPoints, LaggedStart, MoveAlongPath, smooth
    src, dst = np.array(src, dtype=float), np.array(dst, dtype=float)
    coins = VGroup(*[coin(r, color) for _ in range(n)])
    for c in coins:
        c.move_to(src)
    anims = [MoveAlongPath(c, ArcBetweenPoints(src, dst, angle=arc), rate_func=smooth) for c in coins]
    return coins, LaggedStart(*anims, group=coins, lag_ratio=lag, run_time=run_time)


def note_bill(w: float = 1.0, color: str = "#7BD88F") -> VGroup:
    body = RoundedRectangle(corner_radius=0.05, width=w, height=0.45 * w, stroke_color="#2F6B3A", stroke_width=1.5,
                            fill_color=color, fill_opacity=0.95)
    ring = Circle(radius=0.14 * w, stroke_color="#2F6B3A", stroke_width=1.5, fill_opacity=0)
    sign = label(r"\$", font_size=34 * w, color="#2F6B3A")
    return VGroup(body, ring, sign)


# ---------------------------------------------------------------------------------------------------------------
# Readouts
# ---------------------------------------------------------------------------------------------------------------
def counter(tracker: ValueTracker, fmt=lambda v: f"{v:,.0f}", size: float = 36, color="#E8EAED", anchor=None):
    """A number that follows ``tracker`` (re-typeset each frame through ``tx``); ``anchor`` keeps its left edge."""
    def make():
        m = tx(fmt(tracker.get_value()), size, color, bold=True)
        if anchor is not None:
            m.move_to(anchor, aligned_edge=LEFT)
        return m
    return always_redraw(make)


def number(fn, decimals: int = 0, prefix: str = "", suffix: str = "", size: float = 36, color="#E8EAED",
           commas: bool = True, sign: bool = False) -> VGroup:
    """A live number, ``fn()`` each frame, built from cached digit glyphs (fast: no new TeX per frame).

    ``prefix`` and ``suffix`` are TeX-escaped text such as "$" or "%" or " GW"."""
    n = DecimalNumber(fn(), num_decimal_places=decimals, group_with_commas=commas, include_sign=sign,
                      font_size=size, color=color)
    g = VGroup()
    pre = tx(prefix, size, color) if prefix else None
    suf = tx(suffix, size, color) if suffix else None
    if pre is not None:
        g.add(pre)
        n.next_to(pre, RIGHT, buff=0.04)
    g.add(n)
    if suf is not None:
        suf.next_to(n, RIGHT, buff=0.06)
        g.add(suf)

    def upd(_m):
        n.set_value(fn())
        if pre is not None:
            n.next_to(pre, RIGHT, buff=0.04)
        if suf is not None:
            suf.next_to(n, RIGHT, buff=0.06)
    g.add_updater(upd)
    g.number = n
    return g


def memo_redraw(key_fn, make, place=None):
    """Like ``always_redraw``, but builds each distinct ``key_fn()`` once with ``make(key)`` and reuses copies, so
    labels that cycle through a few strings are typeset once each.  ``place(m)`` positions the copy each frame."""
    cache = {}

    def f():
        k = key_fn()
        if k not in cache:
            cache[k] = make(k)
        m = cache[k].copy()
        if place is not None:
            place(m)
        return m
    return always_redraw(f)


def gauge(tracker: ValueTracker, lo: float, hi: float, r: float = 1.0, color: str = "#F6C453",
          bands=(("#7BD88F", 0.6), ("#F2C14E", 0.85), ("#E8554E", 1.0))) -> VGroup:
    """A half-dial from ``lo`` to ``hi`` whose needle follows ``tracker``."""
    arcs = VGroup()
    start = 0.0
    for col, end in bands:
        arcs.add(Arc(radius=r, start_angle=PI - start * PI, angle=-(end - start) * PI, stroke_color=col,
                     stroke_width=10))
        start = end

    hub = Dot(ORIGIN, radius=0.06, color=color)

    def needle():
        f = (min(max(tracker.get_value(), lo), hi) - lo) / (hi - lo)
        ang = PI - f * PI
        c = hub.get_center()
        return Line(c, c + np.array([0.85 * r * math.cos(ang), 0.85 * r * math.sin(ang), 0]), stroke_color=color,
                    stroke_width=5)
    g = VGroup(arcs, always_redraw(needle), hub)
    return g

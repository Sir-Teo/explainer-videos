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
* oil and gas: :func:`barrel`, :func:`pumpjack` (``.beam`` rocks with :func:`nod`), :func:`derrick`, :func:`platform`,
  :func:`tank` (``.oil`` at a level), :func:`column` (a distillation tower with its ``.cuts``), :func:`tanker`;
* mining and metals: :func:`open_pit` (benches, ``.ore`` below), :func:`haul_truck`, :func:`mill_drum` (``.drum``
  turns), :func:`flotation_cell` (``.froth``), :func:`cathode`, :func:`gold_bar`, :func:`battery` (``.charge``);
* farming and food: :func:`wheat` (tall or dwarf, ``.head``), :func:`corn_plant` (``.cob``), :func:`field` (rows of
  plants), :func:`tractor` (``.wheels``), :func:`grain_elevator`, :func:`cow`, :func:`chicken`, :func:`loaf`,
  :func:`cocoa_pod`, :func:`sack`;
* heavy materials: :func:`converter` (Bessemer's; ``.vessel`` tilts about ``.pivot``, ``.sparks``),
  :func:`blast_furnace` (``.stoves``, ``.tap``), :func:`eaf` (``.electrodes``, ``.arc``, ``.pool``), :func:`ladle`,
  :func:`coil`, :func:`ibeam`, :func:`rebar`, :func:`slab`, :func:`pile` (pellets, coal, scrap), :func:`sparks`,
  :func:`rotary_kiln` (``.tube``, ``.flame``, ``.tower``), :func:`silo`, :func:`mixer_truck` (``.drum``),
  :func:`quarry`, :func:`potline` (``.pots``, ``.bus``), :func:`can`, :func:`carton`, :func:`banana`;
* chemicals: :func:`molecule` (ball and stick: H2, N2, NH3, CH4, C2H6, C2H4; ``.atoms``, ``.bonds``), :func:`chain`
  (polyethylene), :func:`cracker_unit` (``.flames``, ``.towers``), :func:`cylinder`, :func:`paint_can`,
  :func:`pellet_bag`;
* cars: :func:`model_t` (``.wheels``), :func:`chassis` (Ford's line, ``.added`` stage by stage), :func:`pickup`, :func:`suv`,
  :func:`press` (``.ram`` comes down ``.stroke`` on the ``.blank``), :func:`robot_arm` (``.lower``/``.upper`` about
  ``.shoulder``/``.elbow``), :func:`paint_booth` (``.mist``), :func:`engine` (``.pistons``), :func:`battery_pack`
  (``.modules``), :func:`showroom` (``.car``, ``.bay``), :func:`car_carrier`, :func:`wrench`, :func:`kanban`;
* aerospace: :func:`turbofan` (a cutaway: ``.fan``, ``.core``, ``.flame``, ``.bypass``), :func:`fan_face` (``.rotor``
  turns with :func:`spin` about ``.hub``), :func:`fighter`, :func:`missile`;
* machinery: :func:`excavator` (``.boom`` turns about ``.pivot``), :func:`elevator` (a shaft whose ``.car`` stops at
  ``.floor_y(k)``), :func:`gear`;
* medicines: :func:`capsule` (``.halves``), :func:`tablet`, :func:`flask` (``.liquid``, ``.bubbles``), :func:`vial`;
* medical technology: :func:`surgical_robot` (``.arms``, ``.table``), :func:`scanner` (``.ring``, ``.bed``),
  :func:`pacemaker` (``.lead``), :func:`test_tubes` (``.tubes``), :func:`glucose_sensor` (``.ring``), :func:`hospital`
  (``.windows``);
* consumer goods: :func:`soap` (``.bubbles``), :func:`detergent` (``.label``), :func:`cereal_box`, :func:`can`,
  :func:`shelf` (``.packs``, ``.store``), :func:`cart`;
* fashion: :func:`tshirt` (``.print``), :func:`handbag` (``.clasp``), :func:`sneaker` (``.sole``, ``.stripe``),
  :func:`hanger`, :func:`rail` (``.items`` on a ``.bar``), :func:`sewing_machine` (``.needle``), :func:`price_tag`
  (``.label``, ``.strike`` for a markdown);
* construction: :func:`tower_crane` (``.hook``), :func:`skyscraper_frame` (``.floors`` rise one by one), :func:`bridge`
  (``.deck``), :func:`toll_road` (``.gantry``, ``.cars``), :func:`hardhat`, :func:`blueprint` (``.plan``);
* homes: :func:`house_frame` (``.studs``, ``.trusses``), :func:`plot_lot` (``.stakes``), :func:`sale_sign` (``.board``),
  :func:`house_key`;
* shipping: :func:`container` (a box with its ribs and doors), :func:`quay_crane` (``.boom``, ``.spreader``),
  :func:`shoebox`;
* property: :func:`office_tower` (``.windows`` in random order, lit with :func:`light` to show occupancy),
  :func:`warehouse` (``.docks``, ``.trucks``), :func:`mall` (``.stores``, which can go dark), :func:`cell_tower`
  (``.antennas``), :func:`lease` (``.lines``, ``.signature``);
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
from manim import (DOWN, LEFT, ORIGIN, PI, RIGHT, TAU, UL, UP, UR, Arc, Circle, CubicBezier, DashedLine, DecimalNumber, Dot, Ellipse, Line, MathTex,
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
        "→": r"$\to$", "←": r"$\leftarrow$", "↔": r"$\leftrightarrow$", "×": r"$\times$", "·": r"$\cdot$", "≈": r"$\approx$",
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


def car(w: float = 2.4, color: str = "#7EC8F5") -> VGroup:
    """A saloon car in side view, facing right; ``w`` is its length."""
    body = Polygon([-0.5 * w, 0.08 * w, 0], [0.5 * w, 0.08 * w, 0], [0.5 * w, 0.19 * w, 0], [0.44 * w, 0.22 * w, 0],
                   [0.2 * w, 0.24 * w, 0], [-0.45 * w, 0.24 * w, 0], [-0.5 * w, 0.2 * w, 0],
                   stroke_width=0, fill_color=color, fill_opacity=0.95)
    roof = Polygon([0.18 * w, 0.24 * w, 0], [0.06 * w, 0.36 * w, 0], [-0.26 * w, 0.36 * w, 0], [-0.4 * w, 0.24 * w, 0],
                   stroke_width=0, fill_color=color, fill_opacity=0.95)
    glass = VGroup(Polygon([0.15 * w, 0.245 * w, 0], [0.05 * w, 0.34 * w, 0], [-0.08 * w, 0.34 * w, 0], [-0.08 * w, 0.245 * w, 0],
                           stroke_width=0, fill_color=GLASS, fill_opacity=1),
                   Polygon([-0.11 * w, 0.245 * w, 0], [-0.11 * w, 0.34 * w, 0], [-0.25 * w, 0.34 * w, 0], [-0.36 * w, 0.245 * w, 0],
                           stroke_width=0, fill_color=GLASS, fill_opacity=1))
    lamp = VGroup(Rectangle(width=0.03 * w, height=0.03 * w, stroke_width=0, fill_color="#F6E27A", fill_opacity=1).move_to([0.485 * w, 0.17 * w, 0]),
                  Rectangle(width=0.02 * w, height=0.03 * w, stroke_width=0, fill_color="#E8554E", fill_opacity=1).move_to([-0.49 * w, 0.19 * w, 0]))
    wheels = VGroup()
    for x in (-0.3, 0.3):
        wheels.add(VGroup(Circle(radius=0.085 * w, stroke_width=0, fill_color="#20242C", fill_opacity=1),
                          Circle(radius=0.04 * w, stroke_width=0, fill_color="#9AA3B2", fill_opacity=1)).move_to([x * w, 0.085 * w, 0]))
    return VGroup(body, roof, glass, lamp, wheels)


def phone(h: float = 1.2, color: str = "#2E3645", screen: str = "#7EC8F5") -> VGroup:
    """A smartphone, front on; ``h`` is its height."""
    body = RoundedRectangle(corner_radius=0.08 * h, width=0.5 * h, height=h, stroke_color="#C9D3E0", stroke_width=2,
                            fill_color=color, fill_opacity=1)
    glass = RoundedRectangle(corner_radius=0.05 * h, width=0.44 * h, height=0.9 * h, stroke_width=0, fill_color=screen,
                             fill_opacity=0.85)
    cam = Dot(radius=0.018 * h, color="#0E1117").move_to([0, 0.41 * h, 0])
    return VGroup(body, glass, cam)


def capitol(w: float = 1.6, color: str = "#C9D3E0") -> VGroup:
    """A government building: steps, six columns and a pediment; sits on y = 0."""
    steps = VGroup(*[Rectangle(width=w * (1.0 - 0.06 * k), height=0.04 * w, stroke_width=0, fill_color=color,
                               fill_opacity=0.9 - 0.1 * k).move_to([0, 0.02 * w + 0.04 * w * k, 0]) for k in range(3)])
    base = 0.12 * w
    cols = VGroup(*[Rectangle(width=0.06 * w, height=0.38 * w, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to(
        [x * w, base + 0.19 * w, 0]) for x in np.linspace(-0.36, 0.36, 6)])
    beam = Rectangle(width=0.86 * w, height=0.06 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, base + 0.41 * w, 0])
    ped = Polygon([-0.46 * w, base + 0.44 * w, 0], [0.46 * w, base + 0.44 * w, 0], [0, base + 0.62 * w, 0], stroke_width=0,
                  fill_color=color, fill_opacity=1)
    return VGroup(steps, cols, beam, ped)


def chip_fab(w: float = 2.4, color: str = "#C9D3E0", accent: str = "#7EC8F5") -> VGroup:
    """A chip fab: a long windowless cleanroom block with air handlers on the roof and an office wing; sits on y = 0."""
    h = 0.3 * w
    body = Rectangle(width=0.78 * w, height=h, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([0.11 * w, h / 2, 0])
    band = Rectangle(width=0.78 * w, height=0.035 * w, stroke_width=0, fill_color=accent, fill_opacity=0.9).move_to(
        [0.11 * w, 0.7 * h, 0])
    office = Rectangle(width=0.22 * w, height=0.62 * h, stroke_width=0, fill_color="#9AA3B2", fill_opacity=0.95).move_to(
        [-0.39 * w, 0.31 * h, 0])
    glass = VGroup(*[Rectangle(width=0.17 * w, height=0.05 * w, stroke_width=0, fill_color=GLASS, fill_opacity=1).move_to(
        [-0.39 * w, (0.18 + 0.22 * k) * h, 0]) for k in range(2)])
    fans = VGroup(*[RoundedRectangle(corner_radius=0.01 * w, width=0.09 * w, height=0.05 * w, stroke_width=0, fill_color="#6B7486",
                                     fill_opacity=1).move_to([x * w, h + 0.025 * w, 0]) for x in np.linspace(-0.18, 0.42, 6)])
    return VGroup(body, band, office, glass, fans)


def pcb(w: float = 2.0, color: str = "#2F6B4F", parts: bool = False, seed: int = 3) -> VGroup:
    """A printed circuit board seen from above: the green board, copper traces and pads (``g.pads``); with ``parts``,
    chips and passives sit on the pads (``g.parts``)."""
    h = 0.6 * w
    board = RoundedRectangle(corner_radius=0.04 * w, width=w, height=h, stroke_color="#1E4A36", stroke_width=2,
                             fill_color=color, fill_opacity=1)
    rng = np.random.default_rng(seed)
    traces = VGroup()
    for _ in range(9):
        y = rng.uniform(-0.4, 0.4) * h
        x0, x1 = sorted(rng.uniform(-0.45, 0.45, 2) * w)
        traces.add(Line([x0, y, 0], [x1, y, 0], stroke_color="#C9A24A", stroke_width=1.5, stroke_opacity=0.7))
    spots = [(-0.28, 0.12, 0.26, 0.26), (0.12, 0.1, 0.18, 0.18), (0.33, -0.1, 0.12, 0.2), (-0.05, -0.22, 0.2, 0.1),
             (-0.36, -0.22, 0.08, 0.05), (0.3, 0.25, 0.08, 0.05), (0.0, 0.3, 0.06, 0.04), (-0.15, 0.32, 0.06, 0.04)]
    pads = VGroup(*[Rectangle(width=a * w, height=b * h, stroke_width=0, fill_color="#B8B8B0", fill_opacity=0.85).move_to(
        [x * w, y * h, 0]) for x, y, a, b in spots])
    g = VGroup(board, traces, pads)
    g.pads = pads
    if parts:
        cols = ["#20242C", "#2E3645", "#20242C", "#3A4250", "#C49A6C", "#C49A6C", "#7A5C3A", "#7A5C3A"]
        ps = VGroup(*[Rectangle(width=pd.width * 0.9, height=pd.height * 0.9, stroke_width=0, fill_color=c, fill_opacity=1).move_to(pd)
                      for pd, c in zip(pads, cols)])
        g.add(ps)
        g.parts = ps
    return g


def laptop(w: float = 1.0, color: str = "#9AA3B2", screen: str = "#7EC8F5") -> VGroup:
    """An open laptop, front on: the screen above a keyboard deck seen in perspective."""
    lid = RoundedRectangle(corner_radius=0.04 * w, width=0.8 * w, height=0.52 * w, stroke_width=0, fill_color=color,
                           fill_opacity=1).move_to([0, 0.34 * w, 0])
    glass = Rectangle(width=0.7 * w, height=0.42 * w, stroke_width=0, fill_color=screen, fill_opacity=0.85).move_to([0, 0.34 * w, 0])
    deck = Polygon([-0.4 * w, 0.07 * w, 0], [0.4 * w, 0.07 * w, 0], [0.5 * w, -0.03 * w, 0], [-0.5 * w, -0.03 * w, 0],
                   stroke_width=0, fill_color=color, fill_opacity=1)
    return VGroup(lid, glass, deck)


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


def bottle(h: float = 1.0, color: str = "#7EC8F5", water: float = 0.8) -> VGroup:
    """A plastic water bottle: body, shoulder, cap and a label; ``water`` is how full it is (0-1)."""
    w = 0.36 * h
    body = RoundedRectangle(corner_radius=0.08 * h, width=w, height=0.72 * h, stroke_color=color, stroke_width=2,
                            fill_color=color, fill_opacity=0.15).move_to([0, 0.36 * h, 0])
    fill = RoundedRectangle(corner_radius=0.06 * h, width=w * 0.92, height=0.7 * h * water, stroke_width=0,
                            fill_color=color, fill_opacity=0.55).align_to(body, DOWN).shift(UP * 0.01 * h)
    shoulder = Polygon([-w / 2, 0.72 * h, 0], [w / 2, 0.72 * h, 0], [0.09 * h, 0.86 * h, 0], [-0.09 * h, 0.86 * h, 0],
                       stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.15)
    cap = Rectangle(width=0.2 * h, height=0.08 * h, stroke_width=0, fill_color="#3B7DD8", fill_opacity=1).move_to(
        [0, 0.9 * h, 0])
    label = Rectangle(width=w, height=0.18 * h, stroke_width=0, fill_color="#E8EAED", fill_opacity=0.9).move_to(
        [0, 0.42 * h, 0])
    return VGroup(fill, body, shoulder, cap, label)


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


# ---------------------------------------------------------------------------------------------------------------
# Oil and gas (Part 8)
# ---------------------------------------------------------------------------------------------------------------
OIL = "#2B2118"
CRUDE = "#4A3426"


def barrel(h: float = 1.0, color: str = "#2F6FA8", label: str = "") -> VGroup:
    """A 42-gallon oil barrel standing up: body, hoops, top ellipse (``g.top``), optional text on it."""
    w = 0.66 * h
    body = RoundedRectangle(corner_radius=0.06 * h, width=w, height=h, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([0, h / 2, 0])
    hoops = VGroup(*[Rectangle(width=w * 1.02, height=0.035 * h, stroke_width=0, fill_color="#1B2230",
                               fill_opacity=0.8).move_to([0, y * h, 0]) for y in (0.18, 0.5, 0.82)])
    top = Ellipse(width=w, height=0.14 * h, stroke_width=0, fill_color="#5A8FC2", fill_opacity=1).move_to([0, h, 0])
    shine = Rectangle(width=0.06 * w, height=0.8 * h, stroke_width=0, fill_color="#FFFFFF", fill_opacity=0.14).move_to(
        [-0.28 * w, 0.5 * h, 0])
    g = VGroup(body, hoops, shine, top)
    if label:
        t = tx(label, 22 * h, "#E8EAED", bold=True).move_to([0, 0.66 * h, 0])
        if t.width > 0.9 * w:
            t.scale_to_fit_width(0.9 * w)
        g.add(t)
    g.top = top
    return g


def pumpjack(w: float = 2.0, color: str = "#E8554E") -> VGroup:
    """A nodding donkey: base, samson post, walking beam (``g.beam``) with its horse head, crank and polished rod.
    :func:`nod` sets the beam rocking."""
    base = Rectangle(width=w, height=0.06 * w, stroke_width=0, fill_color=STEEL, fill_opacity=1).move_to([0, 0.03 * w, 0])
    post = Polygon([-0.12 * w, 0.06 * w, 0], [0.12 * w, 0.06 * w, 0], [0, 0.55 * w, 0], stroke_width=0,
                   fill_color="#5B6372", fill_opacity=1)
    beam = VGroup(
        Rectangle(width=0.9 * w, height=0.05 * w, stroke_width=0, fill_color=color, fill_opacity=1),
        Polygon([0.45 * w, 0.06 * w, 0], [0.55 * w, 0.02 * w, 0], [0.55 * w, -0.14 * w, 0], [0.45 * w, -0.06 * w, 0],
                stroke_width=0, fill_color=color, fill_opacity=1),
        Rectangle(width=0.1 * w, height=0.1 * w, stroke_width=0, fill_color="#3E4553", fill_opacity=1).move_to(
            [-0.43 * w, -0.05 * w, 0])).move_to([0.03 * w, 0.56 * w, 0])
    crank = Circle(radius=0.08 * w, stroke_width=3, stroke_color="#5B6372", fill_color="#3E4553",
                   fill_opacity=1).move_to([-0.38 * w, 0.18 * w, 0])
    rod = Line([0.53 * w, 0.48 * w, 0], [0.53 * w, 0.06 * w, 0], stroke_color="#C9D3E0", stroke_width=2)
    arm = Line([-0.38 * w, 0.18 * w, 0], [-0.4 * w, 0.52 * w, 0], stroke_color="#8C929B", stroke_width=3)
    pivot = Dot([0, 0.56 * w, 0], radius=0.001, fill_opacity=0)
    g = VGroup(base, arm, crank, post, rod, beam, pivot)
    g.beam, g.pivot, g.rod = beam, pivot, rod
    return g


def nod(jack: VGroup, speed: float = 0.7, amp: float = 0.16) -> VGroup:
    """Rock a :func:`pumpjack`'s beam about its pivot, ``speed`` strokes a second (remove with ``clear_updaters``)."""
    state = {"t": 0.0, "a": 0.0}

    def upd(m, dt):
        state["t"] += dt
        a = amp * math.sin(TAU * speed * state["t"])
        m.beam.rotate(a - state["a"], about_point=m.pivot.get_center())
        state["a"] = a
    jack.add_updater(upd)
    return jack


def derrick(h: float = 2.0, color: str = "#C9D3E0") -> VGroup:
    """A drilling rig's derrick: a tapering lattice tower on a floor, with a drill string (``g.pipe``)."""
    w0, w1 = 0.5 * h, 0.12 * h
    legs = VGroup(Line([-w0 / 2, 0, 0], [-w1 / 2, h, 0]), Line([w0 / 2, 0, 0], [w1 / 2, h, 0])).set_stroke(color, 3)
    rungs = VGroup()
    for k in range(1, 7):
        y = h * k / 7
        x = (w0 + (w1 - w0) * k / 7) / 2
        xn = (w0 + (w1 - w0) * (k - 1) / 7) / 2
        rungs.add(Line([-x, y, 0], [x, y, 0]), Line([-xn, y - h / 7, 0], [x, y, 0]))
    rungs.set_stroke(color, 1.5)
    floor = Rectangle(width=0.8 * h, height=0.05 * h, stroke_width=0, fill_color=STEEL, fill_opacity=1).move_to(
        [0, 0.025 * h, 0])
    pipe = Line([0, h, 0], [0, -0.6 * h, 0], stroke_color="#8C929B", stroke_width=3)
    g = VGroup(pipe, legs, rungs, floor)
    g.pipe = pipe
    return g


def platform(w: float = 3.0, color: str = "#F2C14E") -> VGroup:
    """An offshore production platform on legs above a waterline (``g.sea``), with a flare stack."""
    deck_y = 0.55 * w
    legs = VGroup(*[Rectangle(width=0.05 * w, height=deck_y + 0.25 * w, stroke_width=0, fill_color="#8C929B",
                              fill_opacity=1).move_to([x * w, (deck_y - 0.25 * w) / 2, 0]) for x in (-0.3, -0.1, 0.1, 0.3)])
    deck = Rectangle(width=0.8 * w, height=0.06 * w, stroke_width=0, fill_color=STEEL, fill_opacity=1).move_to(
        [0, deck_y, 0])
    mods = VGroup(Rectangle(width=0.3 * w, height=0.14 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [-0.2 * w, deck_y + 0.1 * w, 0]), Rectangle(width=0.2 * w, height=0.22 * w, stroke_width=0, fill_color="#E8EAED",
                                                     fill_opacity=1).move_to([0.12 * w, deck_y + 0.14 * w, 0]))
    tower = derrick(0.35 * w).move_to([0.12 * w, deck_y + 0.42 * w, 0])
    flare = VGroup(Line([0.38 * w, deck_y, 0], [0.48 * w, deck_y + 0.35 * w, 0], stroke_color="#8C929B", stroke_width=3),
                   Circle(radius=0.035 * w, stroke_width=0, fill_color="#F2A65A", fill_opacity=0.9).move_to(
                       [0.49 * w, deck_y + 0.38 * w, 0]))
    sea = Rectangle(width=1.4 * w, height=0.25 * w, stroke_width=0, fill_color="#1F4E79", fill_opacity=0.85).move_to(
        [0, 0.08 * w, 0])
    g = VGroup(legs, sea, deck, mods, tower[1:], flare)
    g.sea, g.flare = sea, flare
    return g


def tank(w: float = 1.4, level: float = 0.5, color: str = "#C9D3E0") -> VGroup:
    """A round storage tank seen from the side, cut open: shell, roof and the oil inside (``g.oil``) at ``level``."""
    h = 0.7 * w
    shell = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2, fill_color="#20262F",
                      fill_opacity=1).move_to([0, h / 2, 0])
    roof = Arc(radius=w * 0.9, start_angle=PI / 2 - 0.58, angle=1.16, stroke_color=color, stroke_width=2).move_to(
        [0, h + 0.07 * w, 0])
    oil_ = Rectangle(width=w * 0.96, height=max(h * level * 0.96, 0.001), stroke_width=0, fill_color=CRUDE,
                     fill_opacity=1).move_to([0, 0.02 * h + h * level * 0.48, 0])
    g = VGroup(shell, oil_, roof)
    g.oil, g.h, g.w = oil_, h, w
    return g


def column(h: float = 3.0, color: str = "#C9D3E0") -> VGroup:
    """A refinery's distillation column with draw-off pipes (``g.cuts``, bottom to top) and a furnace below."""
    w = 0.22 * h
    tower = RoundedRectangle(corner_radius=0.1 * w, width=w, height=h, stroke_color=color, stroke_width=2,
                             fill_color="#20262F", fill_opacity=1).move_to([0, h / 2, 0])
    trays = VGroup(*[Line([-w / 2, h * k / 7, 0], [w / 2, h * k / 7, 0], stroke_color="#3E4553", stroke_width=1.5)
                     for k in range(1, 7)])
    cuts = VGroup(*[Line([w / 2, h * (k + 0.5) / 7, 0], [w / 2 + 0.35 * h, h * (k + 0.5) / 7, 0],
                         stroke_color=color, stroke_width=2) for k in range(6)])
    furnace = Rectangle(width=0.9 * w, height=0.18 * h, stroke_width=0, fill_color="#5B6372", fill_opacity=1).move_to(
        [-0.9 * w, 0.09 * h, 0])
    g = VGroup(furnace, tower, trays, cuts)
    g.cuts, g.tower = cuts, tower
    return g


def tanker(w: float = 3.0, color: str = "#4A5A70") -> VGroup:
    """A crude tanker: long low hull, deck pipes and a bridge at the stern."""
    hull = Polygon([-0.5 * w, 0.1 * w, 0], [0.5 * w, 0.1 * w, 0], [0.44 * w, 0, 0], [-0.46 * w, 0, 0],
                   stroke_width=0, fill_color=color, fill_opacity=1)
    stripe = Rectangle(width=0.96 * w, height=0.02 * w, stroke_width=0, fill_color="#C0392B", fill_opacity=1).move_to(
        [0, 0.02 * w, 0])
    deck = Line([-0.45 * w, 0.115 * w, 0], [0.32 * w, 0.115 * w, 0], stroke_color="#8C929B", stroke_width=2)
    bridge = Rectangle(width=0.1 * w, height=0.12 * w, stroke_width=0, fill_color="#E8EAED", fill_opacity=1).move_to(
        [0.4 * w, 0.16 * w, 0])
    funnel = Rectangle(width=0.03 * w, height=0.06 * w, stroke_width=0, fill_color="#C0392B", fill_opacity=1).move_to(
        [0.43 * w, 0.25 * w, 0])
    return VGroup(hull, stripe, deck, bridge, funnel)


# ---------------------------------------------------------------------------------------------------------------
# Mining and metals (Part 9)
# ---------------------------------------------------------------------------------------------------------------
COPPER = "#D9824B"


def open_pit(w: float = 5.0, depth: float = 1.8, benches: int = 5, color: str = "#8A6E52") -> VGroup:
    """An open pit seen in section: stepped benches down to a floor; ``g.ore`` is the ore body below the floor."""
    pts = [[-w / 2, 0, 0]]
    step_w = (w * 0.38) / benches
    for k in range(benches):
        x = -w / 2 + (k + 1) * step_w
        pts += [[x - step_w * 0.4, -depth * k / benches, 0], [x, -depth * (k + 1) / benches, 0]]
    floor_l = pts[-1][0]
    pts += [[-floor_l, -depth, 0]]
    for k in range(benches, 0, -1):
        x = w / 2 - k * step_w
        pts += [[x, -depth * (k - 1) / benches - depth / benches, 0], [x + step_w * 0.6, -depth * (k - 1) / benches, 0]]
    pts += [[w / 2, 0, 0]]
    rock = Polygon([-w / 2 - 0.3, 0, 0], *pts, [w / 2 + 0.3, 0, 0], [w / 2 + 0.3, -depth - 1.0, 0],
                   [-w / 2 - 0.3, -depth - 1.0, 0], stroke_width=0, fill_color=color, fill_opacity=0.0)
    ground = Polygon([-w / 2 - 0.3, 0, 0], *pts, [w / 2 + 0.3, 0, 0], [w / 2 + 0.3, -depth - 1.0, 0],
                     [-w / 2 - 0.3, -depth - 1.0, 0], stroke_width=0, fill_color=color, fill_opacity=1)
    edge = VMobject(stroke_color="#C9A98A", stroke_width=2).set_points_as_corners(pts)
    ore = Ellipse(width=w * 0.35, height=0.55, stroke_width=0, fill_color=COPPER, fill_opacity=0.85).move_to(
        [0, -depth - 0.45, 0])
    g = VGroup(ground, ore, edge)
    del rock
    g.ore, g.floor = ore, -depth
    return g


def haul_truck(w: float = 1.6, color: str = "#F2C14E") -> VGroup:
    """A giant mine haul truck: tipping body (``g.body``), cab, and two big wheels."""
    body = Polygon([-0.5 * w, 0.18 * w, 0], [0.2 * w, 0.18 * w, 0], [0.24 * w, 0.42 * w, 0], [-0.52 * w, 0.46 * w, 0],
                   stroke_width=0, fill_color=color, fill_opacity=1)
    cab = Rectangle(width=0.18 * w, height=0.16 * w, stroke_width=0, fill_color="#E8EAED", fill_opacity=1).move_to(
        [0.36 * w, 0.32 * w, 0])
    frame = Rectangle(width=0.95 * w, height=0.06 * w, stroke_width=0, fill_color="#3E4553", fill_opacity=1).move_to(
        [0, 0.16 * w, 0])
    wheels = VGroup(*[Circle(radius=0.13 * w, stroke_color="#8C929B", stroke_width=2, fill_color="#20242C",
                             fill_opacity=1).move_to([x * w, 0.13 * w, 0]) for x in (-0.3, 0.3)])
    g = VGroup(frame, body, cab, wheels)
    g.body = body
    return g


def mill_drum(r: float = 0.7, color: str = "#8B95A7") -> VGroup:
    """A grinding mill seen end-on: a drum (``g.drum``) with lifter bars and balls inside; rotate ``g.drum`` to turn it."""
    shell = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color="#20262F", fill_opacity=1)
    lifters = VGroup(*[Line(ORIGIN, RIGHT * 0.18 * r, stroke_color=color, stroke_width=3).rotate(
        a, about_point=ORIGIN).shift(r * 0.82 * np.array([math.cos(a), math.sin(a), 0])) for a in np.linspace(0, TAU, 9)[:-1]])
    balls = VGroup(*[Circle(radius=0.1 * r, stroke_width=0, fill_color="#C9D3E0", fill_opacity=0.9).move_to(
        [(k % 4 - 1.5) * 0.22 * r, -0.55 * r + (k // 4) * 0.18 * r, 0]) for k in range(8)])
    drum = VGroup(shell, lifters)
    g = VGroup(drum, balls)
    g.drum = drum
    return g


def flotation_cell(w: float = 1.4, color: str = "#5DA9E9") -> VGroup:
    """A flotation tank: slurry, an impeller shaft, and a froth layer on top (``g.froth``) where copper-bearing
    bubbles collect."""
    tank = Rectangle(width=w, height=0.8 * w, stroke_color="#C9D3E0", stroke_width=2, fill_color=color,
                     fill_opacity=0.35).move_to([0, 0.4 * w, 0])
    shaft = Line([0, 0.95 * w, 0], [0, 0.15 * w, 0], stroke_color="#8C929B", stroke_width=3)
    froth = VGroup(*[Circle(radius=0.05 * w, stroke_width=0, fill_color=COPPER, fill_opacity=0.9).move_to(
        [(k - 4.5) * 0.1 * w, 0.82 * w + (k % 2) * 0.04 * w, 0]) for k in range(10)])
    g = VGroup(tank, shaft, froth)
    g.froth, g.tank = froth, tank
    return g


def cathode(h: float = 1.0, color: str = COPPER) -> VGroup:
    """A copper cathode plate hanging from its bar."""
    plate = Rectangle(width=0.8 * h, height=h, stroke_width=0, fill_color=color, fill_opacity=1)
    sheen = Rectangle(width=0.08 * h, height=0.9 * h, stroke_width=0, fill_color="#FFFFFF", fill_opacity=0.15).shift(
        LEFT * 0.25 * h)
    bar = Rectangle(width=1.0 * h, height=0.06 * h, stroke_width=0, fill_color="#8C929B", fill_opacity=1).shift(
        UP * 0.55 * h)
    return VGroup(plate, sheen, bar)


def gold_bar(w: float = 1.0) -> VGroup:
    """A gold bar in perspective: top face and front face."""
    front = Polygon([-0.5 * w, 0, 0], [0.5 * w, 0, 0], [0.42 * w, 0.22 * w, 0], [-0.42 * w, 0.22 * w, 0], stroke_width=0,
                    fill_color="#D4A017", fill_opacity=1)
    top = Polygon([-0.42 * w, 0.22 * w, 0], [0.42 * w, 0.22 * w, 0], [0.32 * w, 0.32 * w, 0], [-0.32 * w, 0.32 * w, 0],
                  stroke_width=0, fill_color="#F6C453", fill_opacity=1)
    return VGroup(front, top)


def battery(h: float = 1.0, color: str = "#7BD88F", charge: float = 0.7) -> VGroup:
    """A battery cell: case, terminal and charge bar (``g.charge``)."""
    case = RoundedRectangle(corner_radius=0.06 * h, width=0.5 * h, height=h, stroke_color="#C9D3E0", stroke_width=2,
                            fill_opacity=0)
    term = Rectangle(width=0.2 * h, height=0.08 * h, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).next_to(
        case, UP, buff=0)
    ch = Rectangle(width=0.4 * h, height=0.9 * h * charge, stroke_width=0, fill_color=color, fill_opacity=0.85).align_to(
        case, DOWN).shift(UP * 0.05 * h)
    g = VGroup(case, term, ch)
    g.charge = ch
    return g


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


# ---------------------------------------------------------------------------------------------------------------
# Maps


_LAND = None


def world_map(width: float = 12.0, lon=(-170.0, 180.0), lat=(-56.0, 78.0), color: str = "#243044",
              stroke: str = "#34425A") -> VGroup:
    """A schematic world map (Natural Earth's 1:110m land, equirectangular) cropped to ``lon`` and ``lat`` and
    ``width`` wide, centred on the origin.  ``g.p(lon, lat)`` gives a point on it (follows the map if it moves)."""
    global _LAND
    if _LAND is None:
        import json
        from pathlib import Path

        _LAND = json.loads((Path(__file__).resolve().parent / "data" / "world_land.json").read_text())["polygons"]
    k = width / (lon[1] - lon[0])
    h = k * (lat[1] - lat[0])
    g = VGroup()

    def xy(lo, la):
        return np.array([(min(max(lo, lon[0]), lon[1]) - lon[0]) * k - width / 2,
                         (min(max(la, lat[0]), lat[1]) - lat[0]) * k - h / 2, 0.0])
    for ring in _LAND:
        xs = [q[0] for q in ring]
        ys = [q[1] for q in ring]
        if max(xs) < lon[0] or min(xs) > lon[1] or max(ys) < lat[0] or min(ys) > lat[1]:
            continue
        g.add(Polygon(*[xy(a, b) for a, b in ring], stroke_color=stroke, stroke_width=1, fill_color=color,
                      fill_opacity=1))
    frame = Rectangle(width=width, height=h, stroke_width=0, fill_opacity=0)
    g.add(frame)

    def p(lo, la):
        return frame.get_center() + (xy(lo, la) - np.array([0.0, 0.0, 0.0])) * (frame.width / width)
    g.p = p
    g.frame = frame
    return g



# ---------------------------------------------------------------------------------------------------------------
# Farming and food


WHEATC = "#E2B85C"
LEAF = "#6FAF5A"


def wheat(h: float = 1.6, dwarf: bool = False, color: str = WHEATC) -> VGroup:
    """A wheat plant: a stem, two leaves and an eared head (``g.head``).  The dwarf variety is short and thick with a
    heavier head, the old tall variety thin and lodging-prone."""
    stem_h = h * (0.55 if dwarf else 1.0)
    w = 3.5 if not dwarf else 6.0
    stem = Line([0, 0, 0], [0, stem_h, 0], stroke_color="#C9A24A", stroke_width=w)
    leaves = VGroup(*[Arc(radius=0.25 * h, start_angle=a, angle=0.9, stroke_color=LEAF, stroke_width=3).move_to(
        [s_ * 0.1 * h, stem_h * f, 0]) for a, s_, f in ((PI * 0.15, 1, 0.35), (PI * 0.6, -1, 0.55))])
    n = 6 if dwarf else 5
    size = 0.045 * h * (1.35 if dwarf else 1.0)
    grains = VGroup()
    for k in range(n):
        for side in (-1, 1):
            grains.add(Ellipse(width=size, height=size * 1.6, stroke_width=0, fill_color=color, fill_opacity=1).rotate(
                side * 0.35).move_to([side * size * 0.45, stem_h + k * size * 1.05, 0]))
    awns = VGroup(*[Line([0, stem_h + n * size * 1.05, 0], [x * size, stem_h + n * size * 1.05 + 0.18 * h, 0],
                         stroke_color=color, stroke_width=1.2) for x in (-1, 0, 1)])
    head = VGroup(grains, awns)
    g = VGroup(stem, leaves, head)
    g.head = head
    return g


def corn_plant(h: float = 1.8) -> VGroup:
    """A maize plant: a stalk, leaves, a tassel and a cob (``g.cob``)."""
    stalk = Line([0, 0, 0], [0, h, 0], stroke_color="#7FA34E", stroke_width=6)
    leaves = VGroup(*[Arc(radius=0.35 * h, start_angle=a, angle=1.0, stroke_color=LEAF, stroke_width=4).move_to(
        [s_ * 0.18 * h, h * f, 0]) for a, s_, f in ((PI * 0.1, 1, 0.3), (PI * 0.55, -1, 0.45), (PI * 0.12, 1, 0.62),
                                                    (PI * 0.6, -1, 0.75))])
    tassel = VGroup(*[Line([0, h, 0], [x * 0.08 * h, h + 0.14 * h, 0], stroke_color="#D9C27A", stroke_width=2)
                      for x in (-1, -0.4, 0.4, 1)])
    cob = VGroup(Ellipse(width=0.13 * h, height=0.3 * h, stroke_width=0, fill_color="#F2C14E", fill_opacity=1),
                 Ellipse(width=0.15 * h, height=0.32 * h, stroke_color="#8DBF5E", stroke_width=2, fill_opacity=0)
                 ).rotate(-0.35).move_to([0.09 * h, 0.5 * h, 0])
    g = VGroup(stalk, leaves, tassel, cob)
    g.cob = cob
    return g


def field(w: float = 6.0, rows: int = 3, n: int = 10, kind: str = "corn", h: float = 0.6) -> VGroup:
    """Rows of plants on brown soil: ``kind`` is "corn" or "wheat" (or "dwarf")."""
    soil = Rectangle(width=w, height=0.18 * rows + 0.1, stroke_width=0, fill_color="#6B4F33", fill_opacity=1)
    plants = VGroup()
    for r in range(rows):
        for k in range(n):
            pl = corn_plant(h) if kind == "corn" else wheat(h, dwarf=(kind == "dwarf"))
            pl.move_to([-w / 2 + (k + 0.5) * w / n + (r % 2) * 0.12, 0, 0], aligned_edge=DOWN).shift(
                UP * (soil.get_top()[1] - 0.12 * r) + DOWN * 0.02)
            plants.add(pl)
    g = VGroup(soil, plants)
    g.plants = plants
    return g


def tractor(w: float = 1.6, color: str = "#3FA34D") -> VGroup:
    """A farm tractor facing right: body, cab, exhaust and a big rear and small front wheel (``g.wheels``)."""
    body = Rectangle(width=0.62 * w, height=0.22 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [0.12 * w, 0.32 * w, 0])
    cab = Rectangle(width=0.26 * w, height=0.3 * w, stroke_color=color, stroke_width=3, fill_color=GLASS,
                    fill_opacity=1).move_to([-0.17 * w, 0.55 * w, 0])
    pipe = Rectangle(width=0.03 * w, height=0.18 * w, stroke_width=0, fill_color=STEEL, fill_opacity=1).move_to(
        [0.28 * w, 0.52 * w, 0])
    rear = VGroup(Circle(radius=0.22 * w, stroke_color="#20242C", stroke_width=6, fill_color="#2E3440", fill_opacity=1),
                  Circle(radius=0.08 * w, stroke_width=0, fill_color="#F2C14E", fill_opacity=1)).move_to(
        [-0.2 * w, 0.22 * w, 0])
    front = VGroup(Circle(radius=0.12 * w, stroke_color="#20242C", stroke_width=5, fill_color="#2E3440", fill_opacity=1),
                   Circle(radius=0.045 * w, stroke_width=0, fill_color="#F2C14E", fill_opacity=1)).move_to(
        [0.33 * w, 0.12 * w, 0])
    g = VGroup(pipe, body, cab, rear, front)
    g.wheels = VGroup(rear, front)
    return g


def grain_elevator(h: float = 2.0, color: str = "#C9D3E0") -> VGroup:
    """A country grain elevator: a row of silos and a taller head house."""
    silos = VGroup(*[VGroup(Rectangle(width=0.22 * h, height=0.7 * h, stroke_color="#8B95A7", stroke_width=1.5,
                                      fill_color=color, fill_opacity=1),
                            Arc(radius=0.11 * h, start_angle=0, angle=PI, stroke_width=0, fill_color=color,
                                fill_opacity=1).shift(UP * 0.35 * h)) for _ in range(3)]).arrange(RIGHT, buff=0.02 * h)
    head = Rectangle(width=0.18 * h, height=h, stroke_color="#8B95A7", stroke_width=1.5, fill_color="#AEB8C6",
                     fill_opacity=1).next_to(silos, RIGHT, buff=0).align_to(silos, DOWN)
    roof = Polygon(head.get_corner(UL), head.get_corner(UR), head.get_top() + UP * 0.08 * h, stroke_width=0,
                   fill_color="#8B95A7", fill_opacity=1)
    spout = Line(head.get_top() + DOWN * 0.15 * h, head.get_corner(UR) + RIGHT * 0.25 * h + DOWN * 0.55 * h,
                 stroke_color="#8B95A7", stroke_width=3)
    return VGroup(silos, head, roof, spout)


def cow(w: float = 1.2, color: str = "#E8EAED", spots: str = "#2B2B2B") -> VGroup:
    """A beef animal facing right: body, head, horns, legs, tail and a few patches."""
    body = RoundedRectangle(corner_radius=0.12 * w, width=w, height=0.48 * w, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([0, 0.5 * w, 0])
    head = RoundedRectangle(corner_radius=0.06 * w, width=0.26 * w, height=0.22 * w, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([0.6 * w, 0.66 * w, 0])
    muzzle = Rectangle(width=0.1 * w, height=0.14 * w, stroke_width=0, fill_color="#F2A7B5", fill_opacity=1).move_to(
        [0.71 * w, 0.62 * w, 0])
    horns = VGroup(*[Line([0.55 * w, 0.77 * w, 0], [0.55 * w + d * 0.06 * w, 0.86 * w, 0], stroke_color="#D9C27A",
                          stroke_width=3) for d in (-1, 1)])
    legs = VGroup(*[Rectangle(width=0.08 * w, height=0.28 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [x * w, 0.14 * w, 0]) for x in (-0.38, -0.24, 0.24, 0.38)])
    patches = VGroup(Ellipse(width=0.3 * w, height=0.2 * w, stroke_width=0, fill_color=spots, fill_opacity=1).move_to(
        [-0.15 * w, 0.56 * w, 0]), Ellipse(width=0.18 * w, height=0.14 * w, stroke_width=0, fill_color=spots,
                                           fill_opacity=1).move_to([0.22 * w, 0.44 * w, 0]))
    tail = Line([-0.5 * w, 0.62 * w, 0], [-0.58 * w, 0.32 * w, 0], stroke_color=color, stroke_width=3)
    eye = Dot([0.63 * w, 0.7 * w, 0], radius=0.02 * w, color=DARK)
    return VGroup(legs, tail, body, patches, head, muzzle, horns, eye)


def chicken(w: float = 0.7, color: str = "#F4F1E8") -> VGroup:
    """A chicken facing right: body, head, comb, beak and legs."""
    body = Ellipse(width=w, height=0.75 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, 0.55 * w, 0])
    tail = Polygon([-0.45 * w, 0.6 * w, 0], [-0.68 * w, 0.95 * w, 0], [-0.4 * w, 0.85 * w, 0], stroke_width=0,
                   fill_color=color, fill_opacity=1)
    head = Circle(radius=0.17 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0.42 * w, 0.95 * w, 0])
    comb = VGroup(*[Circle(radius=0.05 * w, stroke_width=0, fill_color="#E8554E", fill_opacity=1).move_to(
        [0.36 * w + k * 0.07 * w, 1.13 * w, 0]) for k in range(3)])
    beak = Polygon([0.57 * w, 0.98 * w, 0], [0.72 * w, 0.93 * w, 0], [0.57 * w, 0.88 * w, 0], stroke_width=0,
                   fill_color="#F2A65A", fill_opacity=1)
    eye = Dot([0.46 * w, 0.98 * w, 0], radius=0.025 * w, color=DARK)
    legs = VGroup(*[Line([x * w, 0.22 * w, 0], [x * w, 0.0, 0], stroke_color="#F2A65A", stroke_width=3)
                    for x in (-0.08, 0.1)])
    return VGroup(legs, tail, body, head, comb, beak, eye)


def loaf(w: float = 1.2, color: str = "#C98A4B") -> VGroup:
    """A loaf of bread, side view: a domed crust and a few scores."""
    crust = VMobject(stroke_width=0, fill_color=color, fill_opacity=1).set_points_smoothly(
        [[-0.5 * w, 0, 0], [-0.52 * w, 0.22 * w, 0], [-0.3 * w, 0.42 * w, 0], [0, 0.46 * w, 0], [0.3 * w, 0.42 * w, 0],
         [0.52 * w, 0.22 * w, 0], [0.5 * w, 0, 0], [-0.5 * w, 0, 0]])
    scores = VGroup(*[Line([x * w - 0.06 * w, 0.28 * w, 0], [x * w + 0.06 * w, 0.4 * w, 0], stroke_color="#F2D3A0",
                           stroke_width=3) for x in (-0.22, 0, 0.22)])
    return VGroup(crust, scores)


def cocoa_pod(h: float = 1.0, color: str = "#C9732F") -> VGroup:
    """A cocoa pod: a ridged, pointed oval."""
    pod = VMobject(stroke_width=0, fill_color=color, fill_opacity=1).set_points_smoothly(
        [[0, -0.5 * h, 0], [0.24 * h, -0.3 * h, 0], [0.3 * h, 0, 0], [0.22 * h, 0.3 * h, 0], [0, 0.5 * h, 0],
         [-0.22 * h, 0.3 * h, 0], [-0.3 * h, 0, 0], [-0.24 * h, -0.3 * h, 0], [0, -0.5 * h, 0]])
    ridges = VGroup(*[Line([x * h, -0.38 * h, 0], [x * h, 0.38 * h, 0], stroke_color="#8E4A1C", stroke_width=2)
                      for x in (-0.12, 0, 0.12)])
    stem = Line([0, 0.5 * h, 0], [0, 0.62 * h, 0], stroke_color="#6B4F33", stroke_width=4)
    return VGroup(pod, ridges, stem)


def sack(h: float = 0.8, color: str = "#D9C9A3", label_: str = "") -> VGroup:
    """A grain sack with a tied neck and an optional label."""
    body = RoundedRectangle(corner_radius=0.12 * h, width=0.7 * h, height=0.8 * h, stroke_width=0, fill_color=color,
                            fill_opacity=1)
    neck = Polygon([-0.18 * h, 0.38 * h, 0], [0.18 * h, 0.38 * h, 0], [0.1 * h, 0.52 * h, 0], [-0.1 * h, 0.52 * h, 0],
                   stroke_width=0, fill_color=color, fill_opacity=1)
    tie = Line([-0.14 * h, 0.44 * h, 0], [0.14 * h, 0.44 * h, 0], stroke_color="#8A6E52", stroke_width=3)
    g = VGroup(body, neck, tie)
    if label_:
        g.add(tx(label_, 22 * h, "#5A4300", bold=True).move_to(body))
    return g


# ---------------------------------------------------------------------------------------------------------------
# Heavy materials (Part 11)
# ---------------------------------------------------------------------------------------------------------------
MOLTEN = "#FF8A3D"
HOT = "#FFD166"
IRON = "#5B6270"
REFRACTORY = "#8C4B33"


def _smooth(pts, **kw) -> VMobject:
    m = VMobject(**kw)
    m.set_points_smoothly([np.array(p, dtype=float) for p in pts] + [np.array(pts[0], dtype=float)])
    return m


def sparks(n: int = 18, spread: float = 0.9, length: float = 1.0, seed: int = 3, color: str = HOT) -> VGroup:
    """A fan of short glowing streaks rising from the origin (a converter's blow, a tap hole)."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for _ in range(n):
        a = PI / 2 + rng.uniform(-spread, spread) / 2
        r0, r1 = rng.uniform(0.1, 0.6) * length, rng.uniform(0.7, 1.15) * length
        g.add(Line(r0 * np.array([math.cos(a), math.sin(a), 0]), r1 * np.array([math.cos(a), math.sin(a), 0]),
                   stroke_color=interpolate_color(ManimColor(color), ManimColor(MOLTEN), rng.uniform(0, 0.8)),
                   stroke_width=rng.uniform(1.5, 3.5)))
    return g


def converter(h: float = 1.6) -> VGroup:
    """Bessemer's converter: a pear-shaped vessel on trunnions (``g.vessel``; rotate it about ``g.pivot`` to pour)
    with the blow's sparks (``g.sparks``) and the glow of the charge at its mouth (``g.glow``)."""
    pts = [(-0.34, 0.05), (-0.42, 0.35), (-0.36, 0.62), (-0.2, 0.86), (-0.1, 0.98), (0.1, 0.98), (0.2, 0.86),
           (0.36, 0.62), (0.42, 0.35), (0.34, 0.05), (0.0, -0.04)]
    shell = _smooth([(x * h, y * h, 0) for x, y in pts], stroke_color=STEEL, stroke_width=3, fill_color=IRON,
                    fill_opacity=1)
    band = Rectangle(width=0.9 * h, height=0.07 * h, stroke_width=0, fill_color="#3E4553", fill_opacity=1).move_to(
        [0, 0.42 * h, 0])
    mouth = Ellipse(width=0.2 * h, height=0.06 * h, stroke_width=0, fill_color=HOT, fill_opacity=1).move_to([0, 0.98 * h, 0])
    vessel = VGroup(shell, band, mouth)
    pivot = np.array([0, 0.42 * h, 0])
    stand = VGroup(*[Polygon([s * 0.5 * h, -0.2 * h, 0], [s * 0.56 * h, -0.2 * h, 0], [s * 0.5 * h, 0.44 * h, 0],
                             [s * 0.44 * h, 0.44 * h, 0], stroke_width=0, fill_color="#3E4553", fill_opacity=1)
                     for s in (-1, 1)])
    axle = Circle(radius=0.05 * h, stroke_width=0, fill_color=STEEL, fill_opacity=1).move_to(pivot)
    glow = Circle(radius=0.18 * h, stroke_width=0, fill_color=HOT, fill_opacity=0.35).move_to([0, 1.0 * h, 0])
    sp = sparks(22, 1.1, 0.9 * h).shift([0, 1.0 * h, 0])
    g = VGroup(stand, vessel, axle, glow, sp)
    g.vessel, g.pivot, g.sparks, g.glow = vessel, pivot, sp, glow
    return g


def blast_furnace(h: float = 3.0) -> VGroup:
    """A blast furnace: the shell narrowing to its throat, a skip incline that charges ore and coke at the top
    (``g.top``), three hot stoves (``g.stoves``) blowing hot air, and the tap hole (``g.tap``) where iron runs out."""
    prof = [(-0.16, 0.0), (-0.16, 0.18), (-0.22, 0.34), (-0.18, 0.78), (-0.1, 0.86), (0.1, 0.86), (0.18, 0.78),
            (0.22, 0.34), (0.16, 0.18), (0.16, 0.0)]
    shell = Polygon(*[(x * h, y * h, 0) for x, y in prof], stroke_color=STEEL, stroke_width=2, fill_color=IRON,
                    fill_opacity=1)
    lining = Polygon(*[(x * 0.7 * h, (y * 0.92 + 0.04) * h, 0) for x, y in prof], stroke_width=0, fill_color=REFRACTORY,
                     fill_opacity=0.55)
    top = Rectangle(width=0.14 * h, height=0.1 * h, stroke_width=0, fill_color="#3E4553", fill_opacity=1).move_to(
        [0, 0.91 * h, 0])
    stack = Rectangle(width=0.04 * h, height=0.12 * h, stroke_width=0, fill_color="#3E4553", fill_opacity=1).move_to(
        [0.05 * h, 1.02 * h, 0])
    skip = Line([0.7 * h, 0.02 * h, 0], [0.08 * h, 0.9 * h, 0], stroke_color=STEEL, stroke_width=4)
    stoves = VGroup()
    for k in range(3):
        x = -0.42 * h - 0.17 * k * h
        body = Rectangle(width=0.13 * h, height=0.62 * h, stroke_width=0, fill_color="#6C7686", fill_opacity=1).move_to(
            [x, 0.31 * h, 0])
        dome = Arc(radius=0.065 * h, start_angle=0, angle=PI, stroke_width=0, fill_color="#6C7686",
                   fill_opacity=1).move_to([x, 0.62 * h + 0.032 * h, 0])
        stoves.add(VGroup(body, dome))
    main = Line([-0.42 * h, 0.5 * h, 0], [-0.2 * h, 0.5 * h, 0], stroke_color="#A7B0BD", stroke_width=6)
    tap = VGroup(Circle(radius=0.035 * h, stroke_width=0, fill_color=HOT, fill_opacity=1).move_to([0.17 * h, 0.08 * h, 0]),
                 Polygon([0.17 * h, 0.06 * h, 0], [0.42 * h, 0.02 * h, 0], [0.42 * h, 0.0, 0], [0.17 * h, 0.04 * h, 0],
                         stroke_width=0, fill_color=MOLTEN, fill_opacity=1))
    g = VGroup(stoves, main, skip, shell, lining, top, stack, tap)
    g.stoves, g.tap, g.top, g.shell = stoves, tap, top, shell
    return g


def eaf(w: float = 2.0) -> VGroup:
    """An electric arc furnace: a shallow refractory bowl (``g.pool`` of molten steel), a roof, and three graphite
    electrodes (``g.electrodes``) striking an arc (``g.arc``)."""
    bowl = Arc(radius=0.5 * w, start_angle=PI, angle=PI, stroke_width=0, fill_color=REFRACTORY, fill_opacity=1)
    bowl = VGroup(Polygon(*bowl.get_points()[::3], stroke_width=0, fill_color=REFRACTORY, fill_opacity=1))
    shell = Rectangle(width=1.0 * w, height=0.28 * w, stroke_width=0, fill_color=IRON, fill_opacity=1).move_to(
        [0, 0.14 * w, 0])
    pool = Ellipse(width=0.86 * w, height=0.14 * w, stroke_width=0, fill_color=MOLTEN, fill_opacity=0.95).move_to(
        [0, 0.02 * w, 0])
    roof = Polygon([-0.52 * w, 0.28 * w, 0], [0.52 * w, 0.28 * w, 0], [0.34 * w, 0.42 * w, 0], [-0.34 * w, 0.42 * w, 0],
                   stroke_width=0, fill_color="#4A505C", fill_opacity=1)
    electrodes = VGroup(*[Rectangle(width=0.06 * w, height=0.62 * w, stroke_width=0, fill_color="#9AA3B2",
                                    fill_opacity=1).move_to([x * w, 0.52 * w, 0]) for x in (-0.14, 0, 0.14)])
    arc = VGroup(Circle(radius=0.2 * w, stroke_width=0, fill_color=HOT, fill_opacity=0.35).move_to([0, 0.12 * w, 0]),
                 Circle(radius=0.1 * w, stroke_width=0, fill_color="#FFFFFF", fill_opacity=0.8).move_to([0, 0.12 * w, 0]))
    g = VGroup(bowl, shell, pool, arc, roof, electrodes)
    g.pool, g.electrodes, g.arc = pool, electrodes, arc
    return g


def ladle(h: float = 0.8, full: bool = True) -> VGroup:
    """A ladle of molten metal (``g.metal``)."""
    body = Polygon([-0.42 * h, h, 0], [0.42 * h, h, 0], [0.32 * h, 0, 0], [-0.32 * h, 0, 0], stroke_color=STEEL,
                   stroke_width=2, fill_color=IRON, fill_opacity=1)
    metal = Ellipse(width=0.8 * h, height=0.14 * h, stroke_width=0, fill_color=MOLTEN if full else IRON,
                    fill_opacity=1).move_to([0, 0.96 * h, 0])
    hook = Arc(radius=0.46 * h, start_angle=0.15, angle=PI - 0.3, stroke_color=STEEL, stroke_width=3).move_to(
        [0, 1.15 * h, 0])
    g = VGroup(hook, body, metal)
    g.metal = metal
    return g


def coil(r: float = 0.5, color: str = "#AEB6C4") -> VGroup:
    """A coil of steel sheet seen end-on: wound rings (``g.rings``) round an eye."""
    rings = VGroup(*[Circle(radius=r * (0.35 + 0.65 * k / 7), stroke_color=interpolate_color(
        ManimColor(color), ManimColor("#6C7686"), (k % 2) * 0.5), stroke_width=2.5) for k in range(8)])
    disk = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.9)
    eye = Circle(radius=0.33 * r, stroke_width=0, fill_color="#0E1117", fill_opacity=1)
    g = VGroup(disk, rings, eye)
    g.rings = rings
    return g


def ibeam(w: float = 1.2, color: str = STEEL) -> VGroup:
    """An I-beam's section: two flanges and a web."""
    t = 0.14 * w
    pts = [(-w / 2, w / 2), (w / 2, w / 2), (w / 2, w / 2 - t), (t / 3, w / 2 - t), (t / 3, -w / 2 + t), (w / 2, -w / 2 + t),
           (w / 2, -w / 2), (-w / 2, -w / 2), (-w / 2, -w / 2 + t), (-t / 3, -w / 2 + t), (-t / 3, w / 2 - t),
           (-w / 2, w / 2 - t)]
    return VGroup(Polygon(*[(x, y, 0) for x, y in pts], stroke_color="#C9D3E0", stroke_width=1.5, fill_color=color,
                          fill_opacity=1))


def rebar(length: float = 2.0, n: int = 5, color: str = "#9C6B4E") -> VGroup:
    """A bundle of ribbed reinforcing bars."""
    g = VGroup()
    for k in range(n):
        y = (k - (n - 1) / 2) * 0.09
        bar = Line([-length / 2, y, 0], [length / 2, y, 0], stroke_color=color, stroke_width=5)
        ribs = VGroup(*[Line([x, y - 0.035, 0], [x + 0.03, y + 0.035, 0], stroke_color="#6E4A35", stroke_width=1.5)
                        for x in np.linspace(-length / 2 + 0.05, length / 2 - 0.05, int(length * 10))])
        g.add(VGroup(bar, ribs))
    return g


def slab(w: float = 1.6, hot: bool = True) -> VGroup:
    """A cast slab of steel, glowing (``hot``) or cold."""
    return VGroup(RoundedRectangle(corner_radius=0.04, width=w, height=0.18 * w, stroke_width=0,
                                   fill_color=MOLTEN if hot else STEEL, fill_opacity=1),
                  Rectangle(width=0.92 * w, height=0.04 * w, stroke_width=0, fill_color=HOT if hot else "#C9D3E0",
                            fill_opacity=0.6).shift(UP * 0.04 * w))


def pile(w: float = 1.2, color: str = "#8A5A44", n: int = 80, seed: int = 1, shape: str = "round") -> VGroup:
    """A heap of lumps (ore pellets ``round``, coal or scrap ``jagged``) in a rough cone."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for _ in range(n):
        x = rng.uniform(-0.5, 0.5) * w
        ymax = 0.45 * w * (1 - abs(x) / (0.5 * w))
        y = rng.uniform(0, max(ymax, 0.02 * w))
        s = rng.uniform(0.04, 0.07) * w
        c = interpolate_color(ManimColor(color), ManimColor("#FFFFFF"), rng.uniform(0, 0.18))
        if shape == "round":
            m = Circle(radius=s / 2, stroke_width=0, fill_color=c, fill_opacity=1)
        else:
            k = rng.integers(3, 6)
            ang = np.sort(rng.uniform(0, TAU, k))
            m = Polygon(*[(s * math.cos(a) * rng.uniform(0.6, 1.2), s * math.sin(a) * rng.uniform(0.4, 1.0), 0)
                          for a in ang], stroke_width=0, fill_color=c, fill_opacity=1)
        g.add(m.move_to([x, y + s / 2, 0]))
    return g


def rotary_kiln(w: float = 4.0, tilt: float = 0.06) -> VGroup:
    """A cement plant's rotary kiln: a long, gently sloping tube (``g.tube``, with riding rings) on piers, a flame
    at its lower end (``g.flame``) and the preheater tower at its upper end (``g.tower``) where limestone goes in."""
    tube = VGroup(RoundedRectangle(corner_radius=0.06 * w, width=w, height=0.12 * w, stroke_width=0, fill_color="#9AA3B2",
                                   fill_opacity=1))
    for x in (-0.3, 0.0, 0.3):
        tube.add(Rectangle(width=0.035 * w, height=0.15 * w, stroke_width=0, fill_color="#6C7686",
                           fill_opacity=1).shift(RIGHT * x * w))
    tube.rotate(tilt).shift(UP * 0.22 * w)
    piers = VGroup(*[Rectangle(width=0.04 * w, height=0.18 * w - x * tilt * w, stroke_width=0, fill_color="#4A505C",
                               fill_opacity=1).move_to([x * w, (0.09 * w - x * tilt * w / 2) + x * tilt * w, 0]).align_to(
        [0, 0, 0], DOWN) for x in (-0.3, 0.0, 0.3)])
    flame = VGroup(Ellipse(width=0.16 * w, height=0.09 * w, stroke_width=0, fill_color=MOLTEN, fill_opacity=0.9),
                   Ellipse(width=0.09 * w, height=0.05 * w, stroke_width=0, fill_color=HOT, fill_opacity=1)).move_to(
        tube.get_left() + RIGHT * 0.04 * w)
    top = tube.get_right()
    tower = VGroup(Rectangle(width=0.14 * w, height=0.62 * w, stroke_color=STEEL, stroke_width=1.5, fill_color="#2E3645",
                             fill_opacity=1).move_to([top[0] + 0.05 * w, 0.31 * w, 0]))
    for k in range(4):
        tower.add(Triangle(stroke_width=0, fill_color="#6C7686", fill_opacity=1).rotate(PI).scale(0.035 * w).move_to(
            [top[0] + 0.05 * w + (0.03 if k % 2 else -0.03) * w, 0.12 * w + 0.12 * w * k, 0]))
    g = VGroup(piers, tube, flame, tower)
    g.tube, g.flame, g.tower = tube, flame, tower
    return g


def silo(h: float = 1.4, color: str = "#C9D3E0") -> VGroup:
    """A cement silo on legs."""
    body = Rectangle(width=0.4 * h, height=0.6 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, 0.6 * h, 0])
    cap = Ellipse(width=0.4 * h, height=0.1 * h, stroke_width=0, fill_color="#E8EAED", fill_opacity=1).move_to([0, 0.9 * h, 0])
    cone = Polygon([-0.2 * h, 0.3 * h, 0], [0.2 * h, 0.3 * h, 0], [0.04 * h, 0.16 * h, 0], [-0.04 * h, 0.16 * h, 0],
                   stroke_width=0, fill_color="#A7B0BD", fill_opacity=1)
    legs = VGroup(*[Line([s * 0.18 * h, 0.3 * h, 0], [s * 0.22 * h, 0, 0], stroke_color=STEEL, stroke_width=2)
                    for s in (-1, 1)])
    return VGroup(legs, cone, body, cap)


def mixer_truck(w: float = 1.8, color: str = "#E8EAED") -> VGroup:
    """A ready-mix concrete truck: cab, chassis, wheels, and a turning drum (``g.drum``; its stripes ``g.stripes``)."""
    chassis = Rectangle(width=0.95 * w, height=0.05 * w, stroke_width=0, fill_color="#3E4553", fill_opacity=1).move_to(
        [0, 0.12 * w, 0])
    cab = RoundedRectangle(corner_radius=0.03 * w, width=0.22 * w, height=0.26 * w, stroke_width=0, fill_color="#F2C14E",
                           fill_opacity=1).move_to([0.37 * w, 0.27 * w, 0])
    win = Rectangle(width=0.1 * w, height=0.08 * w, stroke_width=0, fill_color=GLASS, fill_opacity=1).move_to(
        [0.42 * w, 0.32 * w, 0])
    drum_shape = _smooth([(-0.42 * w, 0.2 * w, 0), (-0.1 * w, 0.15 * w, 0), (0.2 * w, 0.2 * w, 0), (0.22 * w, 0.32 * w, 0),
                          (0.05 * w, 0.45 * w, 0), (-0.25 * w, 0.42 * w, 0), (-0.44 * w, 0.32 * w, 0)],
                         stroke_width=0, fill_color=color, fill_opacity=1)
    stripes = VGroup(*[Line([x * w, 0.17 * w, 0], [(x + 0.1) * w, 0.44 * w, 0], stroke_color="#E8554E", stroke_width=4)
                       for x in (-0.33, -0.18, -0.03)])
    drum = VGroup(drum_shape, stripes)
    wheels = VGroup(*[Circle(radius=0.065 * w, stroke_width=0, fill_color="#20242C", fill_opacity=1).move_to(
        [x * w, 0.065 * w, 0]) for x in (-0.36, -0.22, 0.36)])
    g = VGroup(chassis, drum, cab, win, wheels)
    g.drum, g.stripes, g.wheels = drum, stripes, wheels
    return g


def quarry(w: float = 4.0, depth: float = 1.4, color: str = "#9AA0A6") -> VGroup:
    """A stone quarry in section: stepped benches in grey rock."""
    g = open_pit(w, depth, 4, color)
    g.ore.set_opacity(0)
    g[2].set_stroke(color="#C9D3E0")
    return g


def potline(w: float = 4.0, n: int = 6) -> VGroup:
    """An aluminium smelter's potline: a row of electrolytic pots (``g.pots``, molten tops ``g.tops``) on a bus bar
    (``g.bus``) that carries the current."""
    pots, tops = VGroup(), VGroup()
    pw = w / n * 0.78
    for k in range(n):
        x = -w / 2 + w * (k + 0.5) / n
        pots.add(Rectangle(width=pw, height=0.38 * pw, stroke_color=STEEL, stroke_width=1.5, fill_color=IRON,
                           fill_opacity=1).move_to([x, 0.19 * pw, 0]))
        tops.add(Rectangle(width=0.8 * pw, height=0.07 * pw, stroke_width=0, fill_color="#E8EAED",
                           fill_opacity=0.9).move_to([x, 0.36 * pw, 0]))
    bus = Line([-w / 2 - 0.1, 0.62 * pw, 0], [w / 2 + 0.1, 0.62 * pw, 0], stroke_color="#F6C453", stroke_width=5)
    drops = VGroup(*[Line([p.get_center()[0], 0.62 * pw, 0], [p.get_center()[0], 0.4 * pw, 0], stroke_color="#F6C453",
                          stroke_width=2.5) for p in pots])
    g = VGroup(bus, drops, pots, tops)
    g.pots, g.tops, g.bus = pots, tops, bus
    return g


def can(h: float = 0.8, color: str = "#C9D3E0", band: str = "#E8554E") -> VGroup:
    """A drinks can."""
    body = RoundedRectangle(corner_radius=0.08 * h, width=0.5 * h, height=0.86 * h, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([0, 0.47 * h, 0])
    top = Ellipse(width=0.42 * h, height=0.08 * h, stroke_color="#8B95A7", stroke_width=1.5, fill_color="#E8EAED",
                  fill_opacity=1).move_to([0, 0.92 * h, 0])
    stripe = Rectangle(width=0.5 * h, height=0.26 * h, stroke_width=0, fill_color=band, fill_opacity=0.9).move_to(
        [0, 0.48 * h, 0])
    sheen = Rectangle(width=0.05 * h, height=0.7 * h, stroke_width=0, fill_color="#FFFFFF", fill_opacity=0.25).move_to(
        [-0.14 * h, 0.47 * h, 0])
    return VGroup(body, stripe, sheen, top)


def carton(w: float = 1.0, color: str = "#C49A6C") -> VGroup:
    """A corrugated cardboard box in three-quarter view, taped."""
    front = Polygon([0, 0, 0], [w, 0, 0], [w, 0.7 * w, 0], [0, 0.7 * w, 0], stroke_color="#8A6E52", stroke_width=1.5,
                    fill_color=color, fill_opacity=1)
    side = Polygon([w, 0, 0], [1.35 * w, 0.25 * w, 0], [1.35 * w, 0.95 * w, 0], [w, 0.7 * w, 0], stroke_color="#8A6E52",
                   stroke_width=1.5, fill_color="#A57E52", fill_opacity=1)
    top = Polygon([0, 0.7 * w, 0], [w, 0.7 * w, 0], [1.35 * w, 0.95 * w, 0], [0.35 * w, 0.95 * w, 0],
                  stroke_color="#8A6E52", stroke_width=1.5, fill_color="#D9B48A", fill_opacity=1)
    tape = Polygon([0.45 * w, 0.7 * w, 0], [0.55 * w, 0.7 * w, 0], [0.9 * w, 0.95 * w, 0], [0.8 * w, 0.95 * w, 0],
                   stroke_width=0, fill_color="#E8D7B8", fill_opacity=1)
    g = VGroup(front, side, top, tape)
    return g.move_to(ORIGIN)


def banana(h: float = 0.6, color: str = "#F2D04E") -> VGroup:
    """A banana."""
    outer = Arc(radius=h, start_angle=-PI * 0.75, angle=PI * 0.5)
    inner = Arc(radius=h * 0.74, start_angle=-PI * 0.7, angle=PI * 0.4).shift(UP * h * 0.06)
    pts = list(outer.get_points()[::4]) + list(inner.get_points()[::-4])
    body = Polygon(*pts, stroke_color="#C9A227", stroke_width=1.5, fill_color=color, fill_opacity=1)
    stem = Line(outer.get_end(), outer.get_end() + np.array([0.06 * h, 0.08 * h, 0]), stroke_color="#6B5A2A",
                stroke_width=4)
    return VGroup(body, stem).move_to(ORIGIN)


# ---------------------------------------------------------------------------------------------------------------
# Chemicals (Part 12)
# ---------------------------------------------------------------------------------------------------------------
ATOM = {"H": ("#E8EAED", 0.11), "C": ("#4A505C", 0.17), "N": ("#5DA9E9", 0.16), "O": ("#E8554E", 0.16),
        "Cl": ("#7BD88F", 0.18), "Ar": ("#B58CFF", 0.17)}

# 2-D layouts, in units of a bond length: (element, x, y), and bonds as (i, j, order)
MOLECULES = {
    "H2": ([("H", -0.5, 0), ("H", 0.5, 0)], [(0, 1, 1)]),
    "N2": ([("N", -0.55, 0), ("N", 0.55, 0)], [(0, 1, 3)]),
    "O2": ([("O", -0.55, 0), ("O", 0.55, 0)], [(0, 1, 2)]),
    "Ar": ([("Ar", 0, 0)], []),
    "NH3": ([("N", 0, 0.1), ("H", -0.85, -0.45), ("H", 0.85, -0.45), ("H", 0, 0.95)], [(0, 1, 1), (0, 2, 1), (0, 3, 1)]),
    "CH4": ([("C", 0, 0), ("H", -0.9, 0), ("H", 0.9, 0), ("H", 0, 0.9), ("H", 0, -0.9)],
            [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)]),
    "C2H6": ([("C", -0.5, 0), ("C", 0.5, 0), ("H", -1.2, 0.7), ("H", -1.2, -0.7), ("H", -1.4, 0), ("H", 1.2, 0.7),
              ("H", 1.2, -0.7), ("H", 1.4, 0)],
             [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (1, 5, 1), (1, 6, 1), (1, 7, 1)]),
    "C2H4": ([("C", -0.55, 0), ("C", 0.55, 0), ("H", -1.25, 0.7), ("H", -1.25, -0.7), ("H", 1.25, 0.7), ("H", 1.25, -0.7)],
             [(0, 1, 2), (0, 2, 1), (0, 3, 1), (1, 4, 1), (1, 5, 1)]),
}


def molecule(kind: str, bond: float = 0.42, label: bool = False) -> VGroup:
    """A ball-and-stick molecule (H2, N2, O2, Ar, NH3, CH4, C2H6, C2H4): ``g.atoms`` and ``g.bonds``."""
    atoms_, bonds_ = MOLECULES[kind]
    pts = [np.array([x * bond, y * bond, 0]) for _, x, y in atoms_]
    bonds = VGroup()
    for i, j, order in bonds_:
        d = pts[j] - pts[i]
        n = np.array([-d[1], d[0], 0]) / (np.linalg.norm(d) + 1e-9)
        for k in range(order):
            off = (k - (order - 1) / 2) * 0.06 * n
            bonds.add(Line(pts[i] + off, pts[j] + off, stroke_color="#C9D3E0", stroke_width=3))
    atoms = VGroup(*[Circle(radius=ATOM[e][1] * bond / 0.42, stroke_color="#0E1117", stroke_width=1.5,
                            fill_color=ATOM[e][0], fill_opacity=1).move_to(p) for (e, _, _), p in zip(atoms_, pts)])
    g = VGroup(bonds, atoms)
    if label:
        g.add(tx(kind.replace("2", "₂"), 16, "#C9D3E0").next_to(g, DOWN, buff=0.1))
    g.atoms, g.bonds = atoms, bonds
    return g


def chain(n: int = 6, bond: float = 0.3) -> VGroup:
    """A strand of polyethylene: a zig-zag of ``n`` carbons with their hydrogens."""
    g = VGroup()
    cs = [np.array([k * bond * 0.9, (0.25 if k % 2 else -0.25) * bond, 0]) for k in range(n)]
    for a, b in zip(cs, cs[1:]):
        g.add(Line(a, b, stroke_color="#C9D3E0", stroke_width=3))
    for k, c in enumerate(cs):
        for s in (1, -1):
            h = c + np.array([0, s * 0.75 * bond, 0]) + np.array([0, (0.2 if k % 2 else -0.2) * bond, 0])
            g.add(Line(c, h, stroke_color="#C9D3E0", stroke_width=2))
            g.add(Circle(radius=0.08 * bond / 0.3, stroke_width=0, fill_color=ATOM["H"][0], fill_opacity=1).move_to(h))
        g.add(Circle(radius=0.12 * bond / 0.3, stroke_width=0, fill_color=ATOM["C"][0], fill_opacity=1).move_to(c))
    return g.move_to(ORIGIN)


def cracker_unit(w: float = 4.0) -> VGroup:
    """A steam cracker: the furnace box with its flames (``g.flames``) and stack, a quench tower and the separation
    columns (``g.towers``) that split the cracked gas."""
    box = Rectangle(width=0.32 * w, height=0.42 * w, stroke_color=STEEL, stroke_width=2, fill_color="#2E3645",
                    fill_opacity=1).move_to([-0.34 * w, 0.21 * w, 0])
    coils = VGroup(*[Line([-0.46 * w + 0.06 * w * k, 0.05 * w, 0], [-0.46 * w + 0.06 * w * k, 0.38 * w, 0],
                          stroke_color="#A7B0BD", stroke_width=2) for k in range(5)])
    flames = VGroup(*[VGroup(Ellipse(width=0.05 * w, height=0.12 * w, stroke_width=0, fill_color="#FF8A3D", fill_opacity=0.9),
                             Ellipse(width=0.025 * w, height=0.07 * w, stroke_width=0, fill_color="#FFD166", fill_opacity=1)
                             ).move_to([-0.43 * w + 0.06 * w * k, 0.08 * w, 0]) for k in range(4)])
    stack = Rectangle(width=0.05 * w, height=0.3 * w, stroke_width=0, fill_color="#6C7686", fill_opacity=1).move_to(
        [-0.34 * w, 0.57 * w, 0])
    quench = Rectangle(width=0.08 * w, height=0.38 * w, stroke_width=0, fill_color="#9AA3B2", fill_opacity=1).move_to(
        [-0.08 * w, 0.19 * w, 0])
    towers = VGroup(*[RoundedRectangle(corner_radius=0.02 * w, width=0.06 * w, height=h * w, stroke_width=0,
                                       fill_color="#C9D3E0", fill_opacity=1).move_to([x * w, h * w / 2, 0])
                      for x, h in ((0.08, 0.5), (0.2, 0.62), (0.32, 0.45), (0.44, 0.55))])
    pipe = Line([-0.18 * w, 0.3 * w, 0], [0.46 * w, 0.3 * w, 0], stroke_color="#6C7686", stroke_width=4)
    g = VGroup(pipe, stack, box, coils, flames, quench, towers)
    g.flames, g.towers, g.box = flames, towers, box
    return g


def cylinder(h: float = 0.9, color: str = "#7EC8F5") -> VGroup:
    """A gas cylinder with its valve."""
    body = RoundedRectangle(corner_radius=0.12 * h, width=0.32 * h, height=0.85 * h, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([0, 0.43 * h, 0])
    neck = Rectangle(width=0.1 * h, height=0.08 * h, stroke_width=0, fill_color="#8B95A7", fill_opacity=1).move_to(
        [0, 0.89 * h, 0])
    valve = Rectangle(width=0.2 * h, height=0.05 * h, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to(
        [0, 0.95 * h, 0])
    return VGroup(body, neck, valve)


def paint_can(h: float = 0.7, color: str = "#E8554E") -> VGroup:
    """A tin of paint with a drip."""
    body = Rectangle(width=0.8 * h, height=0.8 * h, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to(
        [0, 0.4 * h, 0])
    lid = Ellipse(width=0.8 * h, height=0.16 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, 0.8 * h, 0])
    drip = Polygon([-0.2 * h, 0.8 * h, 0], [-0.1 * h, 0.8 * h, 0], [-0.13 * h, 0.55 * h, 0], [-0.17 * h, 0.55 * h, 0],
                   stroke_width=0, fill_color=color, fill_opacity=1)
    label_ = Rectangle(width=0.8 * h, height=0.28 * h, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to(
        [0, 0.38 * h, 0])
    handle = Arc(radius=0.42 * h, start_angle=0.3, angle=PI - 0.6, stroke_color="#8B95A7", stroke_width=2).move_to(
        [0, 0.95 * h, 0])
    return VGroup(handle, body, label_, lid, drip)


def pellet_bag(h: float = 0.8, color: str = "#E8EAED") -> VGroup:
    """A sack of plastic pellets, the form in which polymer is sold."""
    bag = RoundedRectangle(corner_radius=0.1 * h, width=0.7 * h, height=h, stroke_width=0, fill_color=color, fill_opacity=1)
    dots = VGroup(*[Circle(radius=0.035 * h, stroke_width=0, fill_color="#7EC8F5", fill_opacity=0.9).move_to(
        [(-0.2 + 0.1 * (k % 5)) * h, (-0.15 + 0.08 * (k // 5)) * h, 0]) for k in range(15)])
    tag = tx("PE", 18 * h, "#0E1117", bold=True).move_to([0, 0.3 * h, 0])
    return VGroup(bag, dots, tag)


# ---------------------------------------------------------------------------------------------------------------
# Water and waste (Part 14)
# ---------------------------------------------------------------------------------------------------------------
WATER = "#5DA9E9"


def drop(h: float = 0.5, color: str = WATER) -> VGroup:
    """A drop of water, point up."""
    body = Circle(radius=0.32 * h, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([0, -0.18 * h, 0])
    tip = Polygon([-0.27 * h, -0.02 * h, 0], [0.27 * h, -0.02 * h, 0], [0, 0.5 * h, 0], stroke_width=0, fill_color=color,
                  fill_opacity=0.95)
    shine = Arc(radius=0.2 * h, start_angle=PI * 0.6, angle=PI * 0.45, stroke_color="#FFFFFF", stroke_width=2,
                stroke_opacity=0.6).move_to([-0.1 * h, -0.12 * h, 0])
    return VGroup(tip, body, shine)


def tap(h: float = 1.0, color: str = "#C9D3E0") -> VGroup:
    """A kitchen tap; ``g.spout`` is the point the water leaves."""
    post = Rectangle(width=0.12 * h, height=0.5 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [-0.3 * h, 0.25 * h, 0])
    arm = Rectangle(width=0.55 * h, height=0.1 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [-0.05 * h, 0.5 * h, 0])
    nose = Rectangle(width=0.1 * h, height=0.16 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [0.2 * h, 0.42 * h, 0])
    handle = RoundedRectangle(corner_radius=0.03 * h, width=0.3 * h, height=0.07 * h, stroke_width=0,
                              fill_color="#E8554E", fill_opacity=1).move_to([-0.3 * h, 0.62 * h, 0])
    base = Rectangle(width=0.3 * h, height=0.05 * h, stroke_width=0, fill_color=STEEL, fill_opacity=1).move_to(
        [-0.3 * h, 0.0, 0])
    g = VGroup(post, arm, nose, handle, base)
    g.spout = np.array([0.2 * h, 0.33 * h, 0])
    return g


def water_tower(h: float = 2.0, color: str = "#C9D3E0") -> VGroup:
    """A water tower: a tank on four legs."""
    tank = RoundedRectangle(corner_radius=0.12 * h, width=0.6 * h, height=0.32 * h, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([0, 0.78 * h, 0])
    cap = Polygon([-0.32 * h, 0.93 * h, 0], [0.32 * h, 0.93 * h, 0], [0, 1.03 * h, 0], stroke_width=0, fill_color=color,
                  fill_opacity=1)
    band = Rectangle(width=0.6 * h, height=0.05 * h, stroke_width=0, fill_color=WATER, fill_opacity=0.9).move_to(
        [0, 0.74 * h, 0])
    legs = VGroup(*[Line([x * h, 0, 0], [0.7 * x * h, 0.62 * h, 0], stroke_color=STEEL, stroke_width=3)
                    for x in (-0.26, -0.09, 0.09, 0.26)])
    braces = VGroup(*[Line([-0.24 * h + 0.05 * k * h, y * h, 0], [0.24 * h - 0.05 * k * h, y * h, 0], stroke_color=STEEL,
                           stroke_width=2) for k, y in enumerate((0.2, 0.42))])
    return VGroup(legs, braces, tank, band, cap)


def wheelie_bin(h: float = 0.8, color: str = "#4F6D4F", lid: str = "#3D4F3D") -> VGroup:
    """A wheeled kerbside bin."""
    body = Polygon([-0.27 * h, 0.9 * h, 0], [0.27 * h, 0.9 * h, 0], [0.22 * h, 0.06 * h, 0], [-0.22 * h, 0.06 * h, 0],
                   stroke_width=0, fill_color=color, fill_opacity=1)
    top = RoundedRectangle(corner_radius=0.02 * h, width=0.6 * h, height=0.08 * h, stroke_width=0, fill_color=lid,
                           fill_opacity=1).move_to([0, 0.94 * h, 0])
    handle = Rectangle(width=0.06 * h, height=0.1 * h, stroke_width=0, fill_color=lid, fill_opacity=1).move_to(
        [0.3 * h, 0.9 * h, 0])
    wheel = Circle(radius=0.08 * h, stroke_width=0, fill_color="#20242C", fill_opacity=1).move_to([0.2 * h, 0.06 * h, 0])
    ribs = VGroup(*[Line([-0.18 * h + 0.12 * k * h, 0.2 * h, 0], [-0.2 * h + 0.13 * k * h, 0.8 * h, 0], stroke_color=lid,
                         stroke_width=1.5, stroke_opacity=0.7) for k in range(4)])
    return VGroup(body, ribs, top, handle, wheel)


def bin_lorry(w: float = 2.0, color: str = "#7BD88F") -> VGroup:
    """A rear-loading refuse lorry: cab at the right, body, hopper at the back (left).  ``g.hopper`` is the loading
    point."""
    body = RoundedRectangle(corner_radius=0.06 * w, width=0.62 * w, height=0.36 * w, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([-0.06 * w, 0.29 * w, 0])
    hopper = Polygon([-0.37 * w, 0.47 * w, 0], [-0.46 * w, 0.4 * w, 0], [-0.46 * w, 0.12 * w, 0], [-0.37 * w, 0.12 * w, 0],
                     stroke_width=0, fill_color="#5E6B78", fill_opacity=1)
    mouth = Rectangle(width=0.05 * w, height=0.12 * w, stroke_width=0, fill_color=DARK, fill_opacity=1).move_to(
        [-0.44 * w, 0.2 * w, 0])
    stripe = Rectangle(width=0.62 * w, height=0.03 * w, stroke_width=0, fill_color="#F6C453", fill_opacity=1).move_to(
        [-0.06 * w, 0.2 * w, 0])
    cab = Polygon([0.26 * w, 0.4 * w, 0], [0.4 * w, 0.4 * w, 0], [0.46 * w, 0.28 * w, 0], [0.46 * w, 0.1 * w, 0],
                  [0.26 * w, 0.1 * w, 0], stroke_width=0, fill_color="#E8EAED", fill_opacity=1)
    win = Polygon([0.33 * w, 0.37 * w, 0], [0.39 * w, 0.37 * w, 0], [0.44 * w, 0.28 * w, 0], [0.33 * w, 0.28 * w, 0],
                  stroke_width=0, fill_color=GLASS, fill_opacity=1)
    chassis = Rectangle(width=0.9 * w, height=0.04 * w, stroke_width=0, fill_color="#2E3645", fill_opacity=1).move_to(
        [0, 0.1 * w, 0])
    wheels = VGroup(*[VGroup(Circle(radius=0.07 * w, stroke_width=0, fill_color="#20242C", fill_opacity=1),
                             Circle(radius=0.03 * w, stroke_width=0, fill_color=STEEL, fill_opacity=1)).move_to([x * w, 0.07 * w, 0])
                      for x in (-0.28, -0.14, 0.34)])
    g = VGroup(body, stripe, hopper, mouth, chassis, cab, win, wheels)
    g.hopper = np.array([-0.46 * w, 0.2 * w, 0])
    return g


def bale(s: float = 0.6, color: str = "#B58E5A") -> VGroup:
    """A strapped bale of sorted recyclables (cardboard by default)."""
    face = Square(s, stroke_width=0, fill_color=color, fill_opacity=1)
    top = Polygon([-s / 2, s / 2, 0], [s / 2, s / 2, 0], [0.72 * s, 0.68 * s, 0], [-0.28 * s, 0.68 * s, 0], stroke_width=0,
                  fill_color=interpolate_color(ManimColor(color), ManimColor("#FFFFFF"), 0.2), fill_opacity=1)
    side = Polygon([s / 2, s / 2, 0], [0.72 * s, 0.68 * s, 0], [0.72 * s, -0.32 * s, 0], [s / 2, -s / 2, 0], stroke_width=0,
                   fill_color=interpolate_color(ManimColor(color), ManimColor("#000000"), 0.25), fill_opacity=1)
    layers = VGroup(*[Line([-s / 2, y * s, 0], [s / 2, y * s, 0], stroke_color="#000000", stroke_width=1, stroke_opacity=0.25)
                      for y in np.linspace(-0.4, 0.4, 7)])
    straps = VGroup(*[Line([x * s, -s / 2, 0], [x * s, s / 2, 0], stroke_color="#2E3645", stroke_width=2) for x in (-0.2, 0.2)])
    return VGroup(face, side, top, layers, straps)


def landfill_section(w: float = 8.0, h: float = 3.0, fill: float = 1.0) -> VGroup:
    """A modern landfill in cross-section: a lined pit (membrane over compacted clay, a leachate collection layer with
    pipes), cells of waste each covered daily with soil, a final cap and gas wells.  ``fill`` (0-1) is how much of the
    airspace above the liner is used.  Parts: ``g.clay``, ``g.liner``, ``g.drain``, ``g.pipes``, ``g.cells`` (bottom up),
    ``g.cap``, ``g.wells``, ``g.ground`` (a Line at grade)."""
    depth = 0.45 * h
    floor_w = 0.55 * w
    rim = [(-w / 2, 0), (-floor_w / 2, -depth), (floor_w / 2, -depth), (w / 2, 0)]
    soil = Polygon([-w / 2 - 0.3, 0.02, 0], [w / 2 + 0.3, 0.02, 0], [w / 2 + 0.3, -depth - 0.35 * h, 0],
                   [-w / 2 - 0.3, -depth - 0.35 * h, 0], stroke_width=0, fill_color="#3B3026", fill_opacity=1)
    pit = Polygon(*[[x, y, 0] for x, y in rim], stroke_width=0, fill_color="#0E1117", fill_opacity=1)
    clay = VMobject(stroke_color="#8A6A45", stroke_width=12).set_points_as_corners(
        [[x, y - 0.09, 0] for x, y in rim])
    liner = VMobject(stroke_color="#1F1F1F", stroke_width=5).set_points_as_corners([[x, y - 0.01, 0] for x, y in rim])
    drain = Rectangle(width=floor_w, height=0.1, stroke_width=0, fill_color="#9AA3B2", fill_opacity=0.9).move_to(
        [0, -depth + 0.05, 0])
    pipes = VGroup(*[Circle(radius=0.04, stroke_width=0, fill_color="#F2A65A", fill_opacity=1).move_to([x, -depth + 0.05, 0])
                     for x in np.linspace(-floor_w / 2 + 0.3, floor_w / 2 - 0.3, 6)])
    # cells: horizontal lifts, each a band of waste with a thin daily cover; they rise above grade into a mound
    n = 7
    lift = (depth + 0.55 * h) / n
    cells = VGroup()
    for k in range(n):
        y0 = -depth + 0.1 + k * lift
        y1 = y0 + lift
        def half(y):
            if y <= 0:     # inside the pit: the side slope
                return floor_w / 2 + (w / 2 - floor_w / 2) * (y + depth) / depth
            return w / 2 - (y / (0.55 * h)) * 0.32 * w     # above grade: the mound narrows
        a0, a1 = half(y0) - 0.05, half(y1) - 0.05
        band = Polygon([-a0, y0, 0], [a0, y0, 0], [a1, y1, 0], [-a1, y1, 0], stroke_width=0,
                       fill_color=["#6B6F7A", "#5E6370", "#727786"][k % 3], fill_opacity=1)
        cover = Line([-a1, y1, 0], [a1, y1, 0], stroke_color="#8A6A45", stroke_width=3)
        cells.add(VGroup(band, cover))
    used = max(1, int(round(fill * n)))
    for k in range(used, n):
        cells[k].set_opacity(0)
    top_y = -depth + 0.1 + n * lift
    a_top = w / 2 - 0.32 * w - 0.05
    cap = VMobject(stroke_color="#7BD88F", stroke_width=8).set_points_as_corners(
        [[-w / 2, 0, 0], [-a_top, top_y, 0], [a_top, top_y, 0], [w / 2, 0, 0]])
    wells = VGroup(*[Line([x, top_y + 0.25, 0], [x, -depth + 0.4, 0], stroke_color="#F6C453", stroke_width=3)
                     for x in (-0.18 * w, 0.0, 0.18 * w)])
    ground = Line([-w / 2 - 0.3, 0, 0], [w / 2 + 0.3, 0, 0], stroke_color="#7BD88F", stroke_width=2)
    g = VGroup(soil, pit, clay, liner, drain, pipes, cells, cap, wells, ground)
    g.soil, g.pit, g.clay, g.liner, g.drain, g.pipes, g.cells, g.cap, g.wells, g.ground = (soil, pit, clay, liner, drain,
                                                                                         pipes, cells, cap, wells, ground)
    return g


# ---------------------------------------------------------------------------------------------------------------
# Cars (Part 17)
# ---------------------------------------------------------------------------------------------------------------
def _wheel(r: float, spokes: int = 0, tyre: str = "#20242C", hub: str = "#9AA3B2") -> VGroup:
    g = VGroup(Circle(radius=r, stroke_width=0, fill_color=tyre, fill_opacity=1),
               Circle(radius=0.5 * r, stroke_width=0, fill_color=hub, fill_opacity=1))
    if spokes:
        g.add(*[Line([0, 0, 0], [0.85 * r * math.cos(TAU * k / spokes), 0.85 * r * math.sin(TAU * k / spokes), 0],
                     stroke_color=hub, stroke_width=1.6) for k in range(spokes)])
        g[1].set_fill(tyre).scale(0.5)
    return g


def model_t(w: float = 2.4, color: str = "#2B2B2B") -> VGroup:
    """A car of 1913 in side view, facing right: a tall open body, an upright windscreen, a folded roof, wooden-spoked
    wheels (``g.wheels``)."""
    s = w
    hood = Polygon([0.12 * s, 0.2 * s, 0], [0.47 * s, 0.2 * s, 0], [0.47 * s, 0.31 * s, 0], [0.12 * s, 0.33 * s, 0],
                   stroke_width=0, fill_color=color, fill_opacity=1)
    radiator = Rectangle(width=0.04 * s, height=0.15 * s, stroke_width=0, fill_color="#C9A227", fill_opacity=1).move_to(
        [0.49 * s, 0.26 * s, 0])
    tub = Polygon([-0.45 * s, 0.2 * s, 0], [0.12 * s, 0.2 * s, 0], [0.12 * s, 0.37 * s, 0], [-0.08 * s, 0.37 * s, 0],
                  [-0.12 * s, 0.42 * s, 0], [-0.42 * s, 0.42 * s, 0], stroke_width=0, fill_color=color, fill_opacity=1)
    screen = Line([0.12 * s, 0.37 * s, 0], [0.1 * s, 0.6 * s, 0], stroke_color="#9AA3B2", stroke_width=2.5)
    roof = VMobject(stroke_color="#4A4A4A", stroke_width=4).set_points_smoothly(
        [[0.1 * s, 0.6 * s, 0], [-0.15 * s, 0.63 * s, 0], [-0.4 * s, 0.6 * s, 0], [-0.44 * s, 0.42 * s, 0]])
    fender = VGroup(*[Arc(radius=0.14 * s, start_angle=0, angle=PI, stroke_color=color, stroke_width=5).move_to(
        [x * s, 0.2 * s, 0]) for x in (-0.3, 0.33)])
    wheels = VGroup(*[_wheel(0.12 * s, spokes=10).move_to([x * s, 0.12 * s, 0]) for x in (-0.3, 0.33)])
    lamp = Circle(radius=0.025 * s, stroke_width=0, fill_color="#F6E27A", fill_opacity=1).move_to([0.45 * s, 0.36 * s, 0])
    g = VGroup(roof, tub, hood, radiator, screen, fender, wheels, lamp)
    g.wheels = wheels
    return g


def chassis(w: float = 2.4, color: str = "#8B95A7", parts: int = 0) -> VGroup:
    """A bare chassis on its wheels, as it moved down Ford's line: two rails, cross members, and up to five stages of
    parts added (``parts``: axles, engine, radiator, steering, body)."""
    rails = VGroup(*[Rectangle(width=0.9 * w, height=0.03 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [0, y * w, 0]) for y in (0.2, 0.235)])
    cross = VGroup(*[Rectangle(width=0.02 * w, height=0.06 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [x * w, 0.217 * w, 0]) for x in (-0.42, -0.15, 0.12, 0.42)])
    wheels = VGroup(*[_wheel(0.11 * w, spokes=10).move_to([x * w, 0.11 * w, 0]) for x in (-0.3, 0.33)])
    added = VGroup(
        VGroup(*[Rectangle(width=0.015 * w, height=0.1 * w, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to(
            [x * w, 0.16 * w, 0]) for x in (-0.3, 0.33)]),
        Rectangle(width=0.18 * w, height=0.1 * w, stroke_width=0, fill_color="#5C6472", fill_opacity=1).move_to([0.28 * w, 0.3 * w, 0]),
        Rectangle(width=0.04 * w, height=0.14 * w, stroke_width=0, fill_color="#C9A227", fill_opacity=1).move_to([0.43 * w, 0.32 * w, 0]),
        Line([0.08 * w, 0.25 * w, 0], [-0.02 * w, 0.44 * w, 0], stroke_color="#C9D3E0", stroke_width=3),
        Polygon([-0.45 * w, 0.25 * w, 0], [0.12 * w, 0.25 * w, 0], [0.12 * w, 0.39 * w, 0], [-0.42 * w, 0.44 * w, 0],
                stroke_width=0, fill_color="#2B2B2B", fill_opacity=1))
    for k, m in enumerate(added):
        if k >= parts:
            m.set_opacity(0)
    g = VGroup(added[4], rails, cross, wheels, added[0], added[1], added[2], added[3])
    g.wheels, g.added = wheels, added
    return g


def pickup(w: float = 2.6, color: str = "#E8554E") -> VGroup:
    """A full-size pickup truck in side view, facing right (``g.wheels``, ``g.bed``)."""
    cab = Polygon([-0.08 * w, 0.14 * w, 0], [0.5 * w, 0.14 * w, 0], [0.5 * w, 0.27 * w, 0], [0.3 * w, 0.29 * w, 0],
                  [0.18 * w, 0.42 * w, 0], [-0.08 * w, 0.42 * w, 0], stroke_width=0, fill_color=color, fill_opacity=0.95)
    bed = Polygon([-0.5 * w, 0.14 * w, 0], [-0.08 * w, 0.14 * w, 0], [-0.08 * w, 0.3 * w, 0], [-0.5 * w, 0.3 * w, 0],
                  stroke_width=0, fill_color=interpolate_color(ManimColor(color), ManimColor("#000000"), 0.2), fill_opacity=0.95)
    glass = VGroup(Polygon([0.16 * w, 0.4 * w, 0], [0.27 * w, 0.29 * w, 0], [0.06 * w, 0.29 * w, 0], [0.06 * w, 0.4 * w, 0],
                           stroke_width=0, fill_color=GLASS, fill_opacity=1),
                   Rectangle(width=0.1 * w, height=0.1 * w, stroke_width=0, fill_color=GLASS, fill_opacity=1).move_to(
                       [-0.01 * w, 0.345 * w, 0]))
    grille = Rectangle(width=0.03 * w, height=0.1 * w, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to(
        [0.49 * w, 0.21 * w, 0])
    wheels = VGroup(*[_wheel(0.1 * w).move_to([x * w, 0.1 * w, 0]) for x in (-0.32, 0.32)])
    g = VGroup(bed, cab, glass, grille, wheels)
    g.wheels, g.bed = wheels, bed
    return g


def suv(w: float = 2.4, color: str = "#7BD88F") -> VGroup:
    """A crossover or SUV in side view, facing right (``g.wheels``)."""
    body = Polygon([-0.5 * w, 0.1 * w, 0], [0.5 * w, 0.1 * w, 0], [0.5 * w, 0.23 * w, 0], [0.4 * w, 0.27 * w, 0],
                   [0.22 * w, 0.29 * w, 0], [0.08 * w, 0.42 * w, 0], [-0.46 * w, 0.42 * w, 0], [-0.5 * w, 0.32 * w, 0],
                   stroke_width=0, fill_color=color, fill_opacity=0.95)
    glass = VGroup(Polygon([0.06 * w, 0.4 * w, 0], [0.19 * w, 0.29 * w, 0], [-0.08 * w, 0.29 * w, 0], [-0.08 * w, 0.4 * w, 0],
                           stroke_width=0, fill_color=GLASS, fill_opacity=1),
                   Polygon([-0.11 * w, 0.4 * w, 0], [-0.11 * w, 0.29 * w, 0], [-0.44 * w, 0.29 * w, 0], [-0.44 * w, 0.4 * w, 0],
                           stroke_width=0, fill_color=GLASS, fill_opacity=1))
    wheels = VGroup(*[_wheel(0.1 * w).move_to([x * w, 0.1 * w, 0]) for x in (-0.31, 0.31)])
    g = VGroup(body, glass, wheels)
    g.wheels = wheels
    return g


def press(h: float = 2.0, color: str = "#5C6472") -> VGroup:
    """A stamping press: a frame, a ram that comes down (``g.ram``; move it by ``g.stroke``) on a die, and a steel blank
    (``g.blank``)."""
    frame = VGroup(Rectangle(width=0.12 * h, height=h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([-0.4 * h, 0.5 * h, 0]),
                   Rectangle(width=0.12 * h, height=h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0.4 * h, 0.5 * h, 0]),
                   Rectangle(width=0.92 * h, height=0.16 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, h, 0]),
                   Rectangle(width=0.92 * h, height=0.1 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, 0.05 * h, 0]))
    die = Polygon([-0.3 * h, 0.1 * h, 0], [0.3 * h, 0.1 * h, 0], [0.22 * h, 0.2 * h, 0], [-0.22 * h, 0.2 * h, 0],
                  stroke_width=0, fill_color="#3A4152", fill_opacity=1)
    ram = Rectangle(width=0.6 * h, height=0.22 * h, stroke_width=0, fill_color="#8B95A7", fill_opacity=1).move_to([0, 0.78 * h, 0])
    blank = Rectangle(width=0.62 * h, height=0.02 * h, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to([0, 0.215 * h, 0])
    g = VGroup(frame, die, blank, ram)
    g.ram, g.blank, g.die, g.stroke = ram, blank, die, 0.45 * h
    return g


def robot_arm(h: float = 1.6, color: str = "#F2A65A") -> VGroup:
    """A six-axis welding robot, simplified: base, a lower and an upper link and a torch (``g.lower``, ``g.upper``,
    ``g.tip``; ``g.shoulder`` and ``g.elbow`` are the points to rotate them about)."""
    base = Polygon([-0.2 * h, 0, 0], [0.2 * h, 0, 0], [0.12 * h, 0.15 * h, 0], [-0.12 * h, 0.15 * h, 0],
                   stroke_width=0, fill_color="#3A4152", fill_opacity=1)
    shoulder = np.array([0, 0.18 * h, 0])
    elbow = shoulder + np.array([0.18 * h, 0.5 * h, 0])
    wrist = elbow + np.array([0.42 * h, -0.12 * h, 0])
    lower = VGroup(Line(shoulder, elbow, stroke_color=color, stroke_width=14 * h / 1.6),
                   Circle(radius=0.06 * h, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to(shoulder))
    upper = VGroup(Line(elbow, wrist, stroke_color=color, stroke_width=10 * h / 1.6),
                   Circle(radius=0.05 * h, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to(elbow),
                   Line(wrist, wrist + np.array([0.04 * h, -0.14 * h, 0]), stroke_color="#C9D3E0", stroke_width=4))
    tip = Dot(wrist + np.array([0.04 * h, -0.15 * h, 0]), radius=0.03 * h, color="#F6E27A")
    upper.add(tip)
    g = VGroup(base, lower, upper)
    g.lower, g.upper, g.tip, g.shoulder, g.elbow = lower, upper, tip, shoulder, elbow
    return g


def paint_booth(w: float = 2.4, color: str = "#2E3645") -> VGroup:
    """A paint booth with spray nozzles in its roof (``g.nozzles``) and a mist (``g.mist``)."""
    box = RoundedRectangle(corner_radius=0.05 * w, width=w, height=0.5 * w, stroke_color="#5C6472", stroke_width=2,
                           fill_color=color, fill_opacity=0.6).move_to([0, 0.25 * w, 0])
    nozzles = VGroup(*[Triangle(stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).scale(0.03 * w).rotate(PI).move_to(
        [x * w, 0.46 * w, 0]) for x in np.linspace(-0.35, 0.35, 5)])
    mist = VGroup(*[Polygon([x * w, 0.44 * w, 0], [(x - 0.06) * w, 0.2 * w, 0], [(x + 0.06) * w, 0.2 * w, 0],
                            stroke_width=0, fill_color="#7EC8F5", fill_opacity=0.18) for x in np.linspace(-0.35, 0.35, 5)])
    g = VGroup(box, mist, nozzles)
    g.nozzles, g.mist = nozzles, mist
    return g


def engine(w: float = 1.4, color: str = "#8B95A7") -> VGroup:
    """A petrol engine block with four cylinders (``g.pistons``), a head and a sump."""
    block = Rectangle(width=w, height=0.5 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, 0.35 * w, 0])
    head = Rectangle(width=1.04 * w, height=0.14 * w, stroke_width=0, fill_color="#5C6472", fill_opacity=1).move_to([0, 0.67 * w, 0])
    sump = Polygon([-0.45 * w, 0.1 * w, 0], [0.45 * w, 0.1 * w, 0], [0.35 * w, 0, 0], [-0.35 * w, 0, 0], stroke_width=0,
                   fill_color="#3A4152", fill_opacity=1)
    pistons = VGroup(*[Rectangle(width=0.16 * w, height=0.18 * w, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to(
        [x * w, 0.45 * w, 0]) for x in (-0.33, -0.11, 0.11, 0.33)])
    g = VGroup(sump, block, head, pistons)
    g.pistons = pistons
    return g


def battery_pack(w: float = 2.4, rows: int = 2, cols: int = 6, color: str = "#7BD88F") -> VGroup:
    """An electric car's battery pack seen from above: a tray of modules (``g.modules``)."""
    tray = RoundedRectangle(corner_radius=0.04 * w, width=w, height=0.38 * w, stroke_color="#C9D3E0", stroke_width=2,
                            fill_color="#1A202B", fill_opacity=1)
    mw, mh = 0.9 * w / cols, 0.3 * w / rows
    modules = VGroup(*[RoundedRectangle(corner_radius=0.01 * w, width=mw * 0.88, height=mh * 0.84, stroke_width=0,
                                        fill_color=color, fill_opacity=0.85).move_to(
        [-0.45 * w + mw * (c + 0.5), -0.15 * w + mh * (r + 0.5), 0]) for r in range(rows) for c in range(cols)])
    g = VGroup(tray, modules)
    g.modules = modules
    return g


def showroom(w: float = 2.8, color: str = "#C9D3E0", sign: str = "") -> VGroup:
    """A car dealer's showroom: a glass front, a car inside (``g.car``), a sign (``g.sign``) and a service bay
    (``g.bay``) to one side."""
    glass = Rectangle(width=0.68 * w, height=0.36 * w, stroke_color=color, stroke_width=2, fill_color=GLASS,
                      fill_opacity=0.5).move_to([-0.16 * w, 0.18 * w, 0])
    roof = Rectangle(width=1.02 * w, height=0.04 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, 0.38 * w, 0])
    bay = Rectangle(width=0.3 * w, height=0.36 * w, stroke_width=0, fill_color="#3A4152", fill_opacity=1).move_to([0.35 * w, 0.18 * w, 0])
    door = VGroup(*[Line([0.22 * w, y * w, 0], [0.48 * w, y * w, 0], stroke_color="#5C6472", stroke_width=1.5)
                    for y in np.linspace(0.04, 0.32, 7)])
    inside = car(0.42 * w, "#F6C453").move_to([-0.16 * w, 0.1 * w, 0])
    g = VGroup(glass, inside, bay, door, roof)
    if sign:
        lab = tx(sign, 14, "#0E1117", bold=True)
        plate = RoundedRectangle(corner_radius=0.02 * w, width=lab.width + 0.2, height=lab.height + 0.1, stroke_width=0,
                                 fill_color="#F6C453", fill_opacity=1).move_to([-0.16 * w, 0.45 * w, 0])
        lab.move_to(plate)
        g.sign = VGroup(plate, lab)
        g.add(g.sign)
    g.car, g.bay = inside, VGroup(bay, door)
    return g


def car_carrier(w: float = 3.2, color: str = "#E8EAED") -> VGroup:
    """A roll-on roll-off car carrier: a tall boxy hull with decks (``g.decks``) and a stern ramp (``g.ramp``)."""
    hull = Polygon([-0.5 * w, 0.06 * w, 0], [0.46 * w, 0.06 * w, 0], [0.5 * w, 0.14 * w, 0], [0.5 * w, 0.3 * w, 0],
                   [-0.5 * w, 0.3 * w, 0], stroke_width=0, fill_color=color, fill_opacity=0.95)
    keel = Polygon([-0.5 * w, 0.06 * w, 0], [0.46 * w, 0.06 * w, 0], [0.42 * w, 0, 0], [-0.46 * w, 0, 0], stroke_width=0,
                   fill_color="#C0392B", fill_opacity=1)
    decks = VGroup(*[Line([-0.48 * w, y * w, 0], [0.46 * w, y * w, 0], stroke_color="#9AA3B2", stroke_width=1.2)
                     for y in (0.12, 0.18, 0.24)])
    bridge = Rectangle(width=0.08 * w, height=0.05 * w, stroke_width=0, fill_color="#2E3645", fill_opacity=1).move_to(
        [0.4 * w, 0.325 * w, 0])
    ramp = Line([-0.5 * w, 0.08 * w, 0], [-0.62 * w, -0.02 * w, 0], stroke_color="#9AA3B2", stroke_width=4)
    g = VGroup(keel, hull, decks, bridge, ramp)
    g.decks, g.ramp = decks, ramp
    return g


def wrench(h: float = 0.8, color: str = "#C9D3E0") -> VGroup:
    handle = RoundedRectangle(corner_radius=0.04 * h, width=0.14 * h, height=0.8 * h, stroke_width=0, fill_color=color,
                              fill_opacity=1)
    jaw = VGroup(Circle(radius=0.16 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, 0.45 * h, 0]),
                 Rectangle(width=0.1 * h, height=0.14 * h, stroke_width=0, fill_color="#0E1117", fill_opacity=1).move_to([0, 0.56 * h, 0]))
    return VGroup(handle, jaw).rotate(-PI / 5)


def kanban(w: float = 0.9, color: str = "#F6C453", text: str = "") -> VGroup:
    """A kanban card: the slip that tells the process before it what to make, and how many."""
    card_ = RoundedRectangle(corner_radius=0.05 * w, width=w, height=0.6 * w, stroke_width=0, fill_color=color, fill_opacity=1)
    lines = VGroup(*[Line([-0.38 * w, y * w, 0], [0.38 * w, y * w, 0], stroke_color="#5A4300", stroke_width=1.5)
                     for y in (0.12, 0.0, -0.12)])
    g = VGroup(card_, lines)
    if text:
        g.add(tx(text, 12, "#0E1117", bold=True).move_to([0, 0.2 * w, 0]))
        lines.shift(DOWN * 0.05 * w)
    return g


# ---------------------------------------------------------------------------------------------------------------
# Aerospace (Part 18)
# ---------------------------------------------------------------------------------------------------------------
def turbofan(w: float = 3.0, color: str = "#B58CFF") -> VGroup:
    """A turbofan in side cutaway, intake to the left: the nacelle, the ``.fan``, the ``.core`` (compressor stages,
    ``.flame`` in the combustor, turbine stages) and the ``.bypass`` streams that carry most of the thrust."""
    nac_top = Polygon([-0.5 * w, 0.34 * w, 0], [0.3 * w, 0.3 * w, 0], [0.32 * w, 0.24 * w, 0], [-0.46 * w, 0.27 * w, 0],
                      stroke_width=0, fill_color=STEEL, fill_opacity=1)
    nac_bot = nac_top.copy().flip(RIGHT, about_point=ORIGIN)
    blades = VGroup(*[Polygon([-0.395 * w, (y + 0.02) * w, 0], [-0.355 * w, (y + 0.035) * w, 0], [-0.355 * w, (y - 0.005) * w, 0],
                              [-0.395 * w, (y - 0.02) * w, 0], stroke_width=0, fill_color=color, fill_opacity=0.9)
                      for y in np.linspace(-0.23, 0.23, 9)])
    hub = Polygon([-0.46 * w, 0, 0], [-0.36 * w, 0.06 * w, 0], [-0.36 * w, -0.06 * w, 0], stroke_width=0,
                  fill_color="#C9D3E0", fill_opacity=1)
    fan = VGroup(blades, hub)
    casing = Polygon([-0.32 * w, 0.11 * w, 0], [0.38 * w, 0.08 * w, 0], [0.5 * w, 0.04 * w, 0], [0.5 * w, -0.04 * w, 0],
                     [0.38 * w, -0.08 * w, 0], [-0.32 * w, -0.11 * w, 0], stroke_width=0, fill_color="#3A4152", fill_opacity=1)
    comp = VGroup(*[Line([x * w, (0.09 - 0.05 * k / 6) * w, 0], [x * w, -(0.09 - 0.05 * k / 6) * w, 0], stroke_color="#7EC8F5",
                         stroke_width=2) for k, x in enumerate(np.linspace(-0.28, -0.04, 7))])
    flame = VGroup(*[Ellipse(width=0.07 * w, height=0.03 * w, stroke_width=0, fill_color=c, fill_opacity=0.95).move_to([0.03 * w, y * w, 0])
                     for c, y in (("#F6C453", 0.035), ("#F2A65A", 0.0), ("#F6C453", -0.035))])
    turb = VGroup(*[Line([x * w, 0.07 * w, 0], [x * w, -0.07 * w, 0], stroke_color="#F2A65A", stroke_width=2.5)
                    for x in np.linspace(0.12, 0.3, 4)])
    shaft = Line([-0.36 * w, 0, 0], [0.42 * w, 0, 0], stroke_color="#C9D3E0", stroke_width=2)
    core = VGroup(casing, comp, flame, turb, shaft)
    bypass = VGroup(*[Line([-0.3 * w, s * 0.18 * w, 0], [0.38 * w, s * 0.17 * w, 0], stroke_color="#7EC8F5", stroke_width=2,
                           stroke_opacity=0.7).add_tip(tip_length=0.06 * w) for s in (1, -1)])
    g = VGroup(nac_top, nac_bot, core, fan, bypass)
    g.fan, g.core, g.flame, g.bypass, g.blades = fan, core, flame, bypass, blades
    return g


def fan_face(r: float = 1.0, color: str = "#B58CFF", blades: int = 18) -> VGroup:
    """A jet engine seen from the front: the nacelle lip and the fan (``.rotor``, turned by :func:`spin` about
    ``.hub``)."""
    lip = Circle(radius=r, stroke_color=STEEL, stroke_width=0.14 * r * 40, fill_color="#0E1117", fill_opacity=1)
    rotor = VGroup(*[Polygon([0, 0, 0], [0.95 * r * np.cos(a), 0.95 * r * np.sin(a), 0],
                             [0.95 * r * np.cos(a + 0.18), 0.95 * r * np.sin(a + 0.18), 0], stroke_width=0, fill_color=color,
                             fill_opacity=0.85) for a in np.linspace(0, TAU, blades, endpoint=False)])
    hub = Circle(radius=0.18 * r, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1)
    swirl = Line([0, 0, 0], [0.12 * r, 0, 0], stroke_color="#0E1117", stroke_width=3)
    g = VGroup(lip, rotor, hub, swirl)
    g.rotor, g.hub = VGroup(rotor, swirl), hub
    return g


def fighter(length: float = 3.0, color: str = "#7BD88F") -> VGroup:
    """A fighter jet seen from above, nose to the right."""
    L = length
    body = Polygon([0.5 * L, 0, 0], [0.3 * L, 0.05 * L, 0], [-0.45 * L, 0.06 * L, 0], [-0.5 * L, 0.03 * L, 0],
                   [-0.5 * L, -0.03 * L, 0], [-0.45 * L, -0.06 * L, 0], [0.3 * L, -0.05 * L, 0], stroke_width=0,
                   fill_color=color, fill_opacity=1)
    wings = Polygon([0.1 * L, 0.05 * L, 0], [-0.2 * L, 0.36 * L, 0], [-0.3 * L, 0.36 * L, 0], [-0.22 * L, 0.05 * L, 0],
                    [-0.22 * L, -0.05 * L, 0], [-0.3 * L, -0.36 * L, 0], [-0.2 * L, -0.36 * L, 0], [0.1 * L, -0.05 * L, 0],
                    stroke_width=0, fill_color=color, fill_opacity=0.85)
    tails = Polygon([-0.36 * L, 0.05 * L, 0], [-0.48 * L, 0.17 * L, 0], [-0.52 * L, 0.17 * L, 0], [-0.47 * L, 0.04 * L, 0],
                    [-0.47 * L, -0.04 * L, 0], [-0.52 * L, -0.17 * L, 0], [-0.48 * L, -0.17 * L, 0], [-0.36 * L, -0.05 * L, 0],
                    stroke_width=0, fill_color=color, fill_opacity=0.85)
    canopy = Ellipse(width=0.14 * L, height=0.04 * L, stroke_width=0, fill_color=GLASS, fill_opacity=1).move_to([0.28 * L, 0, 0])
    return VGroup(wings, tails, body, canopy)


def missile(length: float = 2.0, color: str = "#C9D3E0") -> VGroup:
    """A missile in side view, nose to the right."""
    L = length
    body = Rectangle(width=0.8 * L, height=0.07 * L, stroke_width=0, fill_color=color, fill_opacity=1)
    nose = Polygon([0.4 * L, 0.035 * L, 0], [0.52 * L, 0, 0], [0.4 * L, -0.035 * L, 0], stroke_width=0, fill_color=color,
                   fill_opacity=1)
    fins = VGroup(*[Polygon([-0.4 * L, s * 0.035 * L, 0], [-0.28 * L, s * 0.035 * L, 0], [-0.42 * L, s * 0.12 * L, 0],
                            stroke_width=0, fill_color="#E8554E", fill_opacity=1) for s in (1, -1)])
    return VGroup(body, nose, fins)


# ---------------------------------------------------------------------------------------------------------------
# Machinery (Part 19)
# ---------------------------------------------------------------------------------------------------------------
def excavator(w: float = 3.0, color: str = "#F6C453") -> VGroup:
    """A tracked excavator facing right: ``.tracks``, ``.cab``, and the ``.boom`` (with its stick and bucket) that turns
    about ``.pivot``."""
    tracks = RoundedRectangle(corner_radius=0.08 * w, width=0.62 * w, height=0.14 * w, stroke_width=0, fill_color="#3A4152",
                              fill_opacity=1).move_to([-0.12 * w, 0.07 * w, 0])
    wheels = VGroup(*[Circle(radius=0.04 * w, stroke_width=0, fill_color="#8B95A7", fill_opacity=1).move_to([x * w, 0.07 * w, 0])
                      for x in (-0.37, -0.26, -0.15, -0.04, 0.07)])
    body = Polygon([-0.42 * w, 0.15 * w, 0], [0.12 * w, 0.15 * w, 0], [0.12 * w, 0.3 * w, 0], [-0.42 * w, 0.3 * w, 0],
                   stroke_width=0, fill_color=color, fill_opacity=1)
    cab = Polygon([-0.02 * w, 0.3 * w, 0], [0.12 * w, 0.3 * w, 0], [0.12 * w, 0.46 * w, 0], [0.0 * w, 0.46 * w, 0],
                  stroke_width=0, fill_color=color, fill_opacity=1)
    glass = Polygon([0.01 * w, 0.33 * w, 0], [0.1 * w, 0.33 * w, 0], [0.1 * w, 0.43 * w, 0], [0.02 * w, 0.43 * w, 0],
                    stroke_width=0, fill_color=GLASS, fill_opacity=1)
    pivot = np.array([0.12 * w, 0.26 * w, 0])
    boom = Polygon(pivot + np.array([0, 0.03 * w, 0]), pivot + np.array([0.3 * w, 0.28 * w, 0]),
                   pivot + np.array([0.33 * w, 0.24 * w, 0]), pivot + np.array([0.02 * w, -0.03 * w, 0]), stroke_width=0,
                   fill_color=color, fill_opacity=1)
    tip = pivot + np.array([0.32 * w, 0.26 * w, 0])
    stick = Polygon(tip + np.array([-0.02 * w, 0, 0]), tip + np.array([0.02 * w, 0, 0]), tip + np.array([0.1 * w, -0.32 * w, 0]),
                    tip + np.array([0.06 * w, -0.32 * w, 0]), stroke_width=0, fill_color=color, fill_opacity=0.95)
    end = tip + np.array([0.08 * w, -0.32 * w, 0])
    bucket = Polygon(end, end + np.array([0.1 * w, -0.02 * w, 0]), end + np.array([0.06 * w, -0.1 * w, 0]),
                     end + np.array([-0.04 * w, -0.08 * w, 0]), stroke_width=0, fill_color="#5C6472", fill_opacity=1)
    arm = VGroup(boom, stick, bucket)
    g = VGroup(tracks, wheels, body, cab, glass, arm)
    g.tracks, g.cab, g.boom = VGroup(tracks, wheels), VGroup(cab, glass), arm
    g.pivot = Dot(pivot, radius=0.001, fill_opacity=0)
    g.add(g.pivot)
    return g


def elevator(h: float = 3.0, floors: int = 6, color: str = "#7EC8F5") -> VGroup:
    """A building's elevator shaft in section: the floors, the shaft and the ``.car`` (move it with ``.floor_y(k)``)."""
    w = 0.42 * h
    shaft = Rectangle(width=0.32 * w, height=h, stroke_color="#8B95A7", stroke_width=2, fill_color="#141A24", fill_opacity=1)
    walls = Rectangle(width=w, height=h, stroke_color="#5C6472", stroke_width=2, fill_opacity=0)
    lines = VGroup(*[Line([-w / 2, -h / 2 + k * h / floors, 0], [w / 2, -h / 2 + k * h / floors, 0], stroke_color="#3A4152",
                          stroke_width=1.5) for k in range(1, floors)])
    car = Rectangle(width=0.26 * w, height=0.8 * h / floors, stroke_width=0, fill_color=color, fill_opacity=1)
    car.move_to([0, -h / 2 + 0.5 * h / floors, 0])
    cable = Line([0, h / 2, 0], car.get_top(), stroke_color="#C9D3E0", stroke_width=1.2)
    cable.add_updater(lambda m: m.put_start_and_end_on([car.get_x(), walls.get_top()[1], 0], car.get_top()))
    g = VGroup(walls, lines, shaft, cable, car)
    g.car, g.cable = car, cable
    g.floor_y = lambda k: walls.get_bottom()[1] + (k + 0.5) * h / floors
    return g


def gear(r: float = 0.6, teeth: int = 12, color: str = "#8B95A7") -> VGroup:
    """A gear wheel (turn it with ``rotate``)."""
    pts = []
    for k in range(teeth * 2):
        a = k * PI / teeth
        rr = r if k % 2 == 0 else 0.82 * r
        pts += [[rr * np.cos(a - 0.12), rr * np.sin(a - 0.12), 0], [rr * np.cos(a + 0.12), rr * np.sin(a + 0.12), 0]]
    body = Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=1)
    hole = Circle(radius=0.25 * r, stroke_width=0, fill_color="#0E1117", fill_opacity=1)
    return VGroup(body, hole)


# ---------------------------------------------------------------------------------------------------------------
# Medicines (Part 20)
# ---------------------------------------------------------------------------------------------------------------
def capsule(w: float = 0.8, color: str = "#E8554E", other: str = "#F5F5F5") -> VGroup:
    """A two-coloured capsule, lying flat (``.halves``)."""
    h = 0.42 * w
    left = VGroup(RoundedRectangle(corner_radius=h / 2, width=w / 2 + h / 2, height=h, stroke_width=0, fill_color=color,
                                   fill_opacity=1).move_to([-w / 4 + h / 4 - h / 4, 0, 0]))
    right = VGroup(RoundedRectangle(corner_radius=h / 2, width=w / 2 + h / 2, height=h, stroke_width=0, fill_color=other,
                                    fill_opacity=1).move_to([w / 4 - h / 4 + h / 4, 0, 0]))
    cover_l = Rectangle(width=h / 2, height=h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([-h / 4, 0, 0])
    cover_r = Rectangle(width=h / 2, height=h, stroke_width=0, fill_color=other, fill_opacity=1).move_to([h / 4, 0, 0])
    shine = Line([-w / 3, h / 4, 0], [w / 3, h / 4, 0], stroke_color=WHITE_SOFT, stroke_width=2, stroke_opacity=0.5)
    g = VGroup(left, right, cover_l, cover_r, shine)
    g.halves = VGroup(VGroup(left, cover_l), VGroup(right, cover_r))
    return g


WHITE_SOFT = "#FFFFFF"


def tablet(r: float = 0.3, color: str = "#F5F5F5") -> VGroup:
    """A round tablet with a score line."""
    disc = Circle(radius=r, stroke_color="#C9D3E0", stroke_width=2, fill_color=color, fill_opacity=1)
    score = Line([-0.7 * r, 0, 0], [0.7 * r, 0, 0], stroke_color="#9AA3B2", stroke_width=2)
    return VGroup(disc, score)


def flask(h: float = 1.4, color: str = "#7BD88F") -> VGroup:
    """A conical laboratory flask with liquid (``.liquid``) and bubbles (``.bubbles``)."""
    neck_w, base_w = 0.22 * h, 0.8 * h
    glass = Polygon([-neck_w / 2, h / 2, 0], [neck_w / 2, h / 2, 0], [neck_w / 2, 0.15 * h, 0], [base_w / 2, -h / 2, 0],
                    [-base_w / 2, -h / 2, 0], [-neck_w / 2, 0.15 * h, 0], stroke_color="#C9D3E0", stroke_width=3,
                    fill_color="#141A24", fill_opacity=1)
    liq = Polygon([-0.27 * h, -0.12 * h, 0], [0.27 * h, -0.12 * h, 0], [base_w / 2 - 0.03 * h, -h / 2 + 0.03 * h, 0],
                  [-base_w / 2 + 0.03 * h, -h / 2 + 0.03 * h, 0], stroke_width=0, fill_color=color, fill_opacity=0.85)
    bubbles = VGroup(*[Circle(radius=0.03 * h, stroke_width=0, fill_color=WHITE_SOFT, fill_opacity=0.6).move_to([x * h, y * h, 0])
                       for x, y in ((-0.1, -0.3), (0.05, -0.22), (0.12, -0.38), (-0.02, -0.4))])
    g = VGroup(glass, liq, bubbles)
    g.liquid, g.bubbles = liq, bubbles
    return g


def vial(h: float = 1.0, color: str = "#7EC8F5") -> VGroup:
    """A small glass vial with a coloured cap and liquid (``.liquid``)."""
    w = 0.42 * h
    body = RoundedRectangle(corner_radius=0.08 * h, width=w, height=0.8 * h, stroke_color="#C9D3E0", stroke_width=2,
                            fill_color="#141A24", fill_opacity=1).move_to([0, -0.1 * h, 0])
    cap = Rectangle(width=w * 1.05, height=0.18 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, 0.39 * h, 0])
    liq = Rectangle(width=w * 0.86, height=0.45 * h, stroke_width=0, fill_color=color, fill_opacity=0.55).move_to([0, -0.25 * h, 0])
    g = VGroup(body, liq, cap)
    g.liquid = liq
    return g


# ----------------------------------------------------------------------------------------------------------------------
# Medical technology (Part 21)
# ----------------------------------------------------------------------------------------------------------------------

def surgical_robot(h: float = 2.0, color: str = "#C9D3E0", accent: str = "#7EC8F5") -> VGroup:
    """A patient-side surgical robot: a cart on a column with a boom and four arms that reach down to the table
    (``g.arms``, each with ``.tip``), beside an operating table (``g.table``)."""
    cart = RoundedRectangle(corner_radius=0.04 * h, width=0.5 * h, height=0.18 * h, stroke_width=0, fill_color="#3A4152",
                            fill_opacity=1).move_to([-0.55 * h, 0.09 * h, 0])
    col = Rectangle(width=0.1 * h, height=0.75 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([-0.55 * h, 0.55 * h, 0])
    boom = Rectangle(width=0.95 * h, height=0.07 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([-0.1 * h, 0.93 * h, 0])
    arms = VGroup()
    for k, x in enumerate((-0.45, -0.2, 0.05, 0.3)):
        top = np.array([x * h, 0.9 * h, 0])
        knee = top + np.array([0.06 * h, -0.22 * h, 0])
        tip = np.array([(0.02 + 0.06 * (k - 1.5)) * h, 0.38 * h, 0])
        arm = VGroup(Line(top, knee, stroke_color=color, stroke_width=7 * h / 2),
                     Line(knee, tip, stroke_color=accent if k == 1 else color, stroke_width=5 * h / 2),
                     Dot(knee, radius=0.025 * h, color="#5C6472"))
        arm.tip = tip
        arms.add(arm)
    table = VGroup(Rectangle(width=0.9 * h, height=0.05 * h, stroke_width=0, fill_color="#5C6472", fill_opacity=1).move_to([0.05 * h, 0.32 * h, 0]),
                   Line([0.05 * h, 0.3 * h, 0], [0.05 * h, 0.0, 0], stroke_color="#5C6472", stroke_width=6))
    g = VGroup(table, cart, col, boom, arms)
    g.arms, g.table = arms, table
    return g


def scanner(w: float = 2.0, color: str = "#E8EAED", accent: str = "#7EC8F5") -> VGroup:
    """A CT or MRI scanner: a ring (``g.ring``) with a patient bed (``g.bed``) sliding through it."""
    ring = VGroup(Circle(radius=0.38 * w, stroke_width=0, fill_color=color, fill_opacity=1),
                  Circle(radius=0.2 * w, stroke_width=0, fill_color="#0E1117", fill_opacity=1),
                  Arc(radius=0.29 * w, start_angle=PI * 0.15, angle=PI * 0.7, stroke_color=accent, stroke_width=4)
                  ).move_to([0, 0.42 * w, 0])
    base = Rectangle(width=0.5 * w, height=0.08 * w, stroke_width=0, fill_color="#5C6472", fill_opacity=1).move_to([0, 0.04 * w, 0])
    bed = VGroup(RoundedRectangle(corner_radius=0.02 * w, width=0.9 * w, height=0.06 * w, stroke_width=0, fill_color="#9AA3B2",
                                  fill_opacity=1).move_to([0.55 * w, 0.4 * w, 0]),
                 Rectangle(width=0.06 * w, height=0.36 * w, stroke_width=0, fill_color="#5C6472", fill_opacity=1).move_to([0.8 * w, 0.2 * w, 0]))
    g = VGroup(bed, base, ring)
    g.ring, g.bed = ring, bed
    return g


def pacemaker(s: float = 0.8, color: str = "#C9D3E0", lead: str = "#F2A65A") -> VGroup:
    """An implanted pacemaker: a rounded titanium can with a header and a lead (``g.lead``)."""
    can = RoundedRectangle(corner_radius=0.3 * s, width=0.9 * s, height=0.75 * s, stroke_color="#9AA3B2", stroke_width=2,
                           fill_color=color, fill_opacity=1)
    header = RoundedRectangle(corner_radius=0.06 * s, width=0.5 * s, height=0.16 * s, stroke_width=0, fill_color="#7EC8F5",
                              fill_opacity=0.8).next_to(can, UP, buff=0)
    wire = CubicBezier(header.get_top(), header.get_top() + np.array([0.1, 0.5, 0]) * s,
                       header.get_top() + np.array([0.7, 0.3, 0]) * s, header.get_top() + np.array([0.9, 0.7, 0]) * s,
                       stroke_color=lead, stroke_width=3)
    g = VGroup(wire, can, header)
    g.lead = wire
    return g


def test_tubes(n: int = 5, h: float = 0.9, colors=("#E8554E", "#F6C453", "#7EC8F5", "#7BD88F", "#B58CFF")) -> VGroup:
    """A rack of blood-sample tubes with coloured caps (``g.tubes``)."""
    tubes = VGroup()
    for i in range(n):
        x = (i - (n - 1) / 2) * 0.28 * h
        body = RoundedRectangle(corner_radius=0.06 * h, width=0.16 * h, height=0.8 * h, stroke_color="#C9D3E0", stroke_width=2,
                                fill_color="#141A24", fill_opacity=1).move_to([x, 0.4 * h, 0])
        blood = Rectangle(width=0.13 * h, height=0.45 * h, stroke_width=0, fill_color="#B03A3A", fill_opacity=0.9).move_to([x, 0.27 * h, 0])
        cap = Rectangle(width=0.19 * h, height=0.12 * h, stroke_width=0, fill_color=colors[i % len(colors)], fill_opacity=1).move_to([x, 0.84 * h, 0])
        tubes.add(VGroup(body, blood, cap))
    rack = Rectangle(width=0.28 * h * n, height=0.1 * h, stroke_width=0, fill_color="#5C6472", fill_opacity=1).move_to([0, 0.3 * h, 0])
    g = VGroup(tubes, rack)
    g.tubes = tubes
    return g


def glucose_sensor(r: float = 0.4, color: str = "#E8EAED", ring: str = "#7BD88F") -> VGroup:
    """A wearable glucose sensor: a round patch with a coloured ring and a reading (``g.ring``)."""
    patch = Circle(radius=r, stroke_color="#9AA3B2", stroke_width=2, fill_color=color, fill_opacity=1)
    rg = Circle(radius=0.68 * r, stroke_color=ring, stroke_width=5)
    dot = Dot(radius=0.12 * r, color="#3A4152")
    g = VGroup(patch, rg, dot)
    g.ring = rg
    return g


def hospital(w: float = 1.8, color: str = "#C9D3E0", cross: str = "#E8554E") -> VGroup:
    """A hospital building with rows of windows (``g.windows``) and a red cross on its front."""
    body = Rectangle(width=w, height=0.7 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, 0.35 * w, 0])
    wing = Rectangle(width=0.45 * w, height=0.45 * w, stroke_width=0, fill_color="#9AA3B2", fill_opacity=1).move_to([0.72 * w, 0.225 * w, 0])
    windows = VGroup(*[Square(0.07 * w, stroke_width=0, fill_color="#2A3446", fill_opacity=1).move_to([(-0.38 + 0.13 * i) * w,
                                                                                                         (0.22 + 0.15 * j) * w, 0])
                       for i in range(7) for j in range(3) if not (i == 3 and j == 2)])
    door = Rectangle(width=0.16 * w, height=0.16 * w, stroke_width=0, fill_color="#2A3446", fill_opacity=1).move_to([0, 0.08 * w, 0])
    cr = VGroup(Rectangle(width=0.16 * w, height=0.05 * w, stroke_width=0, fill_color=cross, fill_opacity=1),
                Rectangle(width=0.05 * w, height=0.16 * w, stroke_width=0, fill_color=cross, fill_opacity=1)).move_to([0, 0.6 * w, 0])
    g = VGroup(wing, body, windows, door, cr)
    g.windows = windows
    return g


# ----------------------------------------------------------------------------------------------------------------------
# Consumer goods (Part 22)
# ----------------------------------------------------------------------------------------------------------------------

def soap(w: float = 1.0, color: str = "#F2A7B5") -> VGroup:
    """A bar of soap with a stamped oval and a few bubbles (``g.bubbles``)."""
    bar = RoundedRectangle(corner_radius=0.18 * w, width=w, height=0.55 * w, stroke_width=0, fill_color=color, fill_opacity=1)
    stamp = Ellipse(width=0.6 * w, height=0.28 * w, stroke_color="#FFFFFF", stroke_width=2, stroke_opacity=0.6)
    bubbles = VGroup(*[Circle(radius=r * w, stroke_color="#DDE6F0", stroke_width=1.5).move_to([x * w, y * w, 0])
                       for x, y, r in ((0.45, 0.4, 0.07), (0.3, 0.52, 0.05), (0.55, 0.6, 0.04))])
    g = VGroup(bar, stamp, bubbles)
    g.bubbles = bubbles
    return g


def detergent(h: float = 1.2, color: str = "#F2A65A", label: str = "#FFFFFF") -> VGroup:
    """A detergent jug with a handle, a cap and a label (``g.label``)."""
    body = RoundedRectangle(corner_radius=0.08 * h, width=0.7 * h, height=0.85 * h, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([0, 0.425 * h, 0])
    handle = Rectangle(width=0.12 * h, height=0.3 * h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0.26 * h, 0.95 * h, 0])
    hole = Rectangle(width=0.1 * h, height=0.18 * h, stroke_width=0, fill_color="#0E1117", fill_opacity=1).move_to([0.17 * h, 0.95 * h, 0])
    cap = Rectangle(width=0.2 * h, height=0.12 * h, stroke_width=0, fill_color="#3A4152", fill_opacity=1).move_to([-0.18 * h, 0.9 * h, 0])
    lab = Circle(radius=0.2 * h, stroke_width=0, fill_color=label, fill_opacity=0.9).move_to([0, 0.4 * h, 0])
    g = VGroup(body, handle, hole, cap, lab)
    g.label = lab
    return g


def cereal_box(h: float = 1.4, color: str = "#E8554E", accent: str = "#F6C453") -> VGroup:
    """A cereal box seen front on, with a bowl on it."""
    box = Rectangle(width=0.7 * h, height=h, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, 0.5 * h, 0])
    band = Rectangle(width=0.7 * h, height=0.18 * h, stroke_width=0, fill_color=accent, fill_opacity=1).move_to([0, 0.85 * h, 0])
    bowl = VGroup(Arc(radius=0.2 * h, start_angle=PI, angle=PI, stroke_color="#FFFFFF", stroke_width=3),
                  *[Dot([x * h, 0.4 * h, 0], radius=0.025 * h, color=accent) for x in (-0.1, -0.03, 0.05, 0.12)]).move_to([0, 0.36 * h, 0])
    return VGroup(box, band, bowl)


def can(h: float = 1.0, color: str = "#E8554E", band: str = "#FFFFFF") -> VGroup:
    """A drinks can with a white wave across it."""
    body = RoundedRectangle(corner_radius=0.06 * h, width=0.55 * h, height=h, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([0, 0.5 * h, 0])
    top = Rectangle(width=0.5 * h, height=0.06 * h, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to([0, 1.0 * h, 0])
    wave = CubicBezier([-0.27 * h, 0.45 * h, 0], [-0.1 * h, 0.6 * h, 0], [0.1 * h, 0.35 * h, 0], [0.27 * h, 0.52 * h, 0],
                       stroke_color=band, stroke_width=4)
    return VGroup(body, top, wave)


def shelf(w: float = 6.0, rows: int = 3, n: int = 8, colors=("#F2A65A", "#7EC8F5", "#E8554E", "#7BD88F", "#B58CFF"),
          store: str = "#C9D3E0", store_share: float = 0.3) -> VGroup:
    """A supermarket shelf of ``rows`` boards, each with ``n`` packs (``g.packs``); the store label's packs, the right-hand
    ``store_share`` of each row, are plain grey (``g.store``)."""
    boards, packs, storeg = VGroup(), VGroup(), VGroup()
    pw = w / n
    for j in range(rows):
        y = j * 0.9
        boards.add(Rectangle(width=w, height=0.06, stroke_width=0, fill_color="#5C6472", fill_opacity=1).move_to([0, y, 0]))
        for i in range(n):
            own = i >= n * (1 - store_share)
            p = RoundedRectangle(corner_radius=0.04, width=pw * 0.8, height=0.7, stroke_width=0,
                                 fill_color=store if own else colors[(i + j) % len(colors)], fill_opacity=0.95).move_to(
                [-w / 2 + pw * (i + 0.5), y + 0.4, 0])
            (storeg if own else packs).add(p)
    g = VGroup(boards, packs, storeg)
    g.packs, g.store = packs, storeg
    return g


def cart(w: float = 1.2, color: str = "#C9D3E0") -> VGroup:
    """A shopping trolley."""
    basket = Polygon([-0.5 * w, 0.6 * w, 0], [0.45 * w, 0.6 * w, 0], [0.35 * w, 0.2 * w, 0], [-0.38 * w, 0.2 * w, 0],
                     stroke_color=color, stroke_width=3, fill_opacity=0)
    grid = VGroup(*[Line([x * w, 0.58 * w, 0], [x * w * 0.85, 0.22 * w, 0], stroke_color=color, stroke_width=1.5)
                    for x in (-0.25, 0, 0.25)])
    handle = Line([-0.5 * w, 0.6 * w, 0], [-0.62 * w, 0.75 * w, 0], stroke_color=color, stroke_width=3)
    frame = Line([-0.38 * w, 0.2 * w, 0], [-0.4 * w, 0.08 * w, 0], stroke_color=color, stroke_width=3)
    wheels = VGroup(*[Circle(radius=0.05 * w, stroke_color=color, stroke_width=3).move_to([x * w, 0.04 * w, 0]) for x in (-0.35, 0.3)])
    base = Line([-0.4 * w, 0.08 * w, 0], [0.33 * w, 0.08 * w, 0], stroke_color=color, stroke_width=3)
    return VGroup(basket, grid, handle, frame, base, wheels)


def tshirt(w: float = 1.0, color: str = "#7EC8F5", accent: str = "#FFFFFF") -> VGroup:
    """A T-shirt laid flat, front on, with a neckline and a small chest print (``g.print``)."""
    pts = [(-0.18, 0.5), (-0.5, 0.36), (-0.62, 0.08), (-0.4, -0.02), (-0.34, 0.12), (-0.34, -0.5), (0.34, -0.5), (0.34, 0.12),
           (0.4, -0.02), (0.62, 0.08), (0.5, 0.36), (0.18, 0.5)]
    body = Polygon(*[[x * w, y * w, 0] for x, y in pts], stroke_width=0, fill_color=color, fill_opacity=1)
    neck = Arc(radius=0.18 * w, start_angle=PI, angle=PI, stroke_color="#0E1117", stroke_width=3).move_to([0, 0.44 * w, 0])
    pr = Circle(radius=0.08 * w, stroke_width=0, fill_color=accent, fill_opacity=0.85).move_to([0.14 * w, 0.18 * w, 0])
    g = VGroup(body, neck, pr)
    g.print = pr
    return g


def handbag(w: float = 1.0, color: str = "#C8752E", hardware: str = "#F6C453") -> VGroup:
    """A structured leather handbag with a top handle, a flap and a clasp (``g.clasp``)."""
    body = Polygon([-0.5 * w, -0.35 * w, 0], [0.5 * w, -0.35 * w, 0], [0.42 * w, 0.25 * w, 0], [-0.42 * w, 0.25 * w, 0],
                   stroke_width=0, fill_color=color, fill_opacity=1)
    flap = Polygon([-0.42 * w, 0.25 * w, 0], [0.42 * w, 0.25 * w, 0], [0.36 * w, -0.02 * w, 0], [-0.36 * w, -0.02 * w, 0],
                   stroke_color="#0E1117", stroke_width=1.5, stroke_opacity=0.5, fill_color=color, fill_opacity=1)
    handle = Arc(radius=0.26 * w, start_angle=0, angle=PI, stroke_color=color, stroke_width=7 * w).move_to([0, 0.38 * w, 0])
    clasp = RoundedRectangle(corner_radius=0.02 * w, width=0.14 * w, height=0.09 * w, stroke_width=0, fill_color=hardware,
                             fill_opacity=1).move_to([0, -0.02 * w, 0])
    stitch = DashedLine([-0.45 * w, -0.3 * w, 0], [0.45 * w, -0.3 * w, 0], stroke_color="#F3E2C7", stroke_width=1.2, dash_length=0.03 * w)
    g = VGroup(handle, body, flap, clasp, stitch)
    g.clasp = clasp
    return g


def sneaker(w: float = 1.0, color: str = "#FFFFFF", sole: str = "#C9D3E0", accent: str = "#E8554E") -> VGroup:
    """A running shoe in profile, toe to the right, with a sole (``g.sole``) and a swoosh-free stripe (``g.stripe``)."""
    upper = Polygon([-0.5 * w, -0.1 * w, 0], [-0.48 * w, 0.28 * w, 0], [-0.28 * w, 0.3 * w, 0], [-0.05 * w, 0.12 * w, 0],
                    [0.32 * w, 0.05 * w, 0], [0.52 * w, -0.02 * w, 0], [0.55 * w, -0.1 * w, 0], stroke_width=0, fill_color=color,
                    fill_opacity=1)
    so = RoundedRectangle(corner_radius=0.05 * w, width=1.1 * w, height=0.12 * w, stroke_width=0, fill_color=sole,
                          fill_opacity=1).move_to([0.02 * w, -0.15 * w, 0])
    stripe = CubicBezier([-0.36 * w, 0.0, 0], [-0.1 * w, -0.05 * w, 0], [0.1 * w, 0.02 * w, 0], [0.3 * w, 0.06 * w, 0],
                         stroke_color=accent, stroke_width=5 * w)
    laces = VGroup(*[Line([x * w, (0.2 - 0.6 * (x + 0.3)) * w, 0], [(x + 0.06) * w, (0.25 - 0.6 * (x + 0.3)) * w, 0],
                          stroke_color="#5C6472", stroke_width=2) for x in (-0.25, -0.17, -0.09)])
    g = VGroup(so, upper, stripe, laces)
    g.sole, g.stripe = so, stripe
    return g


def hanger(w: float = 1.0, color: str = "#C9D3E0") -> VGroup:
    """A coat hanger."""
    hook = Arc(radius=0.08 * w, start_angle=-PI / 2, angle=1.5 * PI, stroke_color=color, stroke_width=3).move_to([0, 0.38 * w, 0])
    stem = Line([0, 0.3 * w, 0], [0, 0.22 * w, 0], stroke_color=color, stroke_width=3)
    tri = Polygon([0, 0.22 * w, 0], [0.5 * w, -0.05 * w, 0], [-0.5 * w, -0.05 * w, 0], stroke_color=color, stroke_width=3,
                  fill_opacity=0)
    return VGroup(hook, stem, tri)


def rail(w: float = 5.0, n: int = 7, colors=("#7EC8F5", "#E8554E", "#F6C453", "#7BD88F", "#B58CFF", "#F2A65A"),
         gap: float | None = None) -> VGroup:
    """A clothes rail with ``n`` T-shirts on hangers (``g.items``; each item is VGroup(hanger, shirt)) and a ``g.bar``."""
    bar = Line([-w / 2, 0, 0], [w / 2, 0, 0], stroke_color="#9AA3B2", stroke_width=5)
    legs = VGroup(Line([-w / 2, 0, 0], [-w / 2 - 0.2, -2.2, 0], stroke_color="#9AA3B2", stroke_width=4),
                  Line([w / 2, 0, 0], [w / 2 + 0.2, -2.2, 0], stroke_color="#9AA3B2", stroke_width=4))
    step = gap if gap is not None else w / (n + 0.5)
    items = VGroup()
    for i in range(n):
        x = -w / 2 + step * (i + 0.75)
        h = hanger(0.7).move_to([x, -0.15, 0])
        s = tshirt(0.75, color=colors[i % len(colors)]).move_to([x, -0.7, 0])
        items.add(VGroup(h, s))
    g = VGroup(legs, bar, items)
    g.items, g.bar = items, bar
    return g


def sewing_machine(w: float = 1.4, color: str = "#E8E2D4", needle: str = "#C9D3E0") -> VGroup:
    """An industrial sewing machine in profile: arm, head, needle (``g.needle`` moves up and down) and table."""
    table = Rectangle(width=1.4 * w, height=0.06 * w, stroke_width=0, fill_color="#5C6472", fill_opacity=1).move_to([0, 0, 0])
    base = RoundedRectangle(corner_radius=0.04 * w, width=1.0 * w, height=0.14 * w, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([0, 0.1 * w, 0])
    pillar = RoundedRectangle(corner_radius=0.04 * w, width=0.2 * w, height=0.5 * w, stroke_width=0, fill_color=color,
                              fill_opacity=1).move_to([0.36 * w, 0.4 * w, 0])
    arm = RoundedRectangle(corner_radius=0.05 * w, width=0.9 * w, height=0.16 * w, stroke_width=0, fill_color=color,
                           fill_opacity=1).move_to([0.0, 0.62 * w, 0])
    head = RoundedRectangle(corner_radius=0.03 * w, width=0.16 * w, height=0.26 * w, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([-0.38 * w, 0.5 * w, 0])
    nd = Line([-0.38 * w, 0.37 * w, 0], [-0.38 * w, 0.2 * w, 0], stroke_color=needle, stroke_width=2.5)
    wheel = Circle(radius=0.1 * w, stroke_color="#9AA3B2", stroke_width=3).move_to([0.5 * w, 0.62 * w, 0])
    cloth = Rectangle(width=0.5 * w, height=0.03 * w, stroke_width=0, fill_color="#7EC8F5", fill_opacity=1).move_to([-0.38 * w, 0.185 * w, 0])
    g = VGroup(table, base, pillar, arm, head, wheel, cloth, nd)
    g.needle = nd
    return g


def price_tag(text: str = "$40", w: float = 0.9, color: str = "#F6C453", cut: bool = False) -> VGroup:
    """A swing tag with a price (``g.label``); ``cut`` strikes the price through, for a markdown (``g.strike``)."""
    body = Polygon([-0.5 * w, 0.22 * w, 0], [0.3 * w, 0.22 * w, 0], [0.5 * w, 0, 0], [0.3 * w, -0.22 * w, 0], [-0.5 * w, -0.22 * w, 0],
                   stroke_width=0, fill_color=color, fill_opacity=1)
    hole = Circle(radius=0.04 * w, stroke_width=0, fill_color="#0E1117", fill_opacity=1).move_to([0.32 * w, 0, 0])
    lab = tx(text, 22 * w, "#0E1117", bold=True).move_to([-0.1 * w, 0, 0])
    g = VGroup(body, hole, lab)
    g.label = lab
    g.strike = Line(lab.get_corner(DOWN + LEFT), lab.get_corner(UP + RIGHT), stroke_color="#E8554E", stroke_width=4)
    if cut:
        g.add(g.strike)
    return g


def tower_crane(h: float = 3.0, color: str = "#F6C453") -> VGroup:
    """A tower crane: a lattice mast, a jib to the right with its trolley and hook (``g.hook``), a counter-jib with its
    weight to the left, and the operator's cab."""
    mast = VGroup(Line([-0.08 * h, 0, 0], [-0.08 * h, h, 0], stroke_color=color, stroke_width=3),
                  Line([0.08 * h, 0, 0], [0.08 * h, h, 0], stroke_color=color, stroke_width=3),
                  *[Line([-0.08 * h, y, 0], [0.08 * h, y + 0.1 * h, 0], stroke_color=color, stroke_width=1.5)
                    for y in np.arange(0, h - 0.1 * h, 0.1 * h)])
    jib = Line([-0.4 * h, h, 0], [0.9 * h, h, 0], stroke_color=color, stroke_width=4)
    apex = VGroup(Line([0, h, 0], [0, 1.18 * h, 0], stroke_color=color, stroke_width=3),
                  Line([0, 1.18 * h, 0], [0.9 * h, h, 0], stroke_color=color, stroke_width=1.5),
                  Line([0, 1.18 * h, 0], [-0.4 * h, h, 0], stroke_color=color, stroke_width=1.5))
    weight = Rectangle(width=0.16 * h, height=0.1 * h, stroke_width=0, fill_color="#5C6472", fill_opacity=1).move_to([-0.32 * h, 0.94 * h, 0])
    cab = Rectangle(width=0.12 * h, height=0.08 * h, stroke_width=0, fill_color="#7EC8F5", fill_opacity=1).move_to([0.12 * h, 0.95 * h, 0])
    cable = Line([0.6 * h, h, 0], [0.6 * h, 0.7 * h, 0], stroke_color="#C9D3E0", stroke_width=1.5)
    hook = VGroup(cable, Rectangle(width=0.06 * h, height=0.04 * h, stroke_width=0, fill_color="#9AA3B2", fill_opacity=1).move_to([0.6 * h, 0.69 * h, 0]))
    g = VGroup(mast, jib, apex, weight, cab, hook)
    g.hook = hook
    return g


def skyscraper_frame(floors: int = 20, w: float = 1.6, floor_h: float = 0.16, color: str = "#9AA3B2",
                     glass: str = "#2A3A52") -> VGroup:
    """A building's steel frame drawn floor by floor from the ground: ``g.floors[k]`` is the k-th storey (its slab, its
    columns and a glazed panel), so a scene can raise the building a floor at a time."""
    fl = VGroup()
    cols = 5
    for k in range(floors):
        y0 = k * floor_h
        slab = Line([-w / 2, y0 + floor_h, 0], [w / 2, y0 + floor_h, 0], stroke_color=color, stroke_width=2.5)
        posts = VGroup(*[Line([-w / 2 + i * w / (cols - 1), y0, 0], [-w / 2 + i * w / (cols - 1), y0 + floor_h, 0],
                              stroke_color=color, stroke_width=1.5) for i in range(cols)])
        pane = Rectangle(width=w, height=floor_h, stroke_width=0, fill_color=glass, fill_opacity=0.8).move_to([0, y0 + floor_h / 2, 0])
        fl.add(VGroup(pane, posts, slab))
    base = Line([-w / 2 - 0.3, 0, 0], [w / 2 + 0.3, 0, 0], stroke_color="#5C6472", stroke_width=3)
    g = VGroup(base, fl)
    g.floors = fl
    return g


def bridge(w: float = 5.0, color: str = "#C9D3E0") -> VGroup:
    """A cable-stayed bridge in elevation: deck (``g.deck``), two towers and fans of stays, over water."""
    deck = Line([-w / 2, 0, 0], [w / 2, 0, 0], stroke_color=color, stroke_width=5)
    towers, stays = VGroup(), VGroup()
    for x in (-w / 4, w / 4):
        towers.add(Line([x, -0.6, 0], [x, 1.1, 0], stroke_color=color, stroke_width=5))
        for d in (0.25, 0.5, 0.75, 1.0):
            stays.add(Line([x, 1.05, 0], [x - d * w / 4.4, 0, 0], stroke_color=color, stroke_width=1.2))
            stays.add(Line([x, 1.05, 0], [x + d * w / 4.4, 0, 0], stroke_color=color, stroke_width=1.2))
    water = Rectangle(width=w * 1.05, height=0.5, stroke_width=0, fill_color="#1E4E79", fill_opacity=0.8).move_to([0, -0.6, 0])
    g = VGroup(water, towers, stays, deck)
    g.deck = deck
    return g


def toll_road(w: float = 5.0, color: str = "#5C6472") -> VGroup:
    """A motorway seen from the side with a toll gantry (``g.gantry``) and cars (``g.cars``) that can drive along it."""
    road = Rectangle(width=w, height=0.35, stroke_width=0, fill_color=color, fill_opacity=1)
    lines = VGroup(*[Line([x, 0, 0], [x + 0.3, 0, 0], stroke_color="#F6C453", stroke_width=2) for x in np.arange(-w / 2 + 0.2, w / 2 - 0.3, 0.6)])
    k = w / 5.0
    gantry = VGroup(Line([0.6 * k, 0.15, 0], [0.6 * k, 1.1, 0], stroke_color="#C9D3E0", stroke_width=3),
                    Line([0.6 * k, 1.1, 0], [0.6 * k + 1.0, 1.1, 0], stroke_color="#C9D3E0", stroke_width=3),
                    Rectangle(width=0.5, height=0.22, stroke_width=0, fill_color="#7BD88F", fill_opacity=1).move_to([0.6 * k + 0.6, 0.98, 0]))
    cars = VGroup(*[car(0.7, color=c).move_to([x * k, 0.35, 0]) for x, c in ((-1.8, "#7EC8F5"), (-0.4, "#E8554E"), (1.9, "#F6C453"))])
    g = VGroup(road, lines, gantry, cars)
    g.gantry, g.cars = gantry, cars
    return g


def hardhat(w: float = 0.8, color: str = "#F6C453") -> VGroup:
    """A builder's hard hat."""
    dome = Arc(radius=0.35 * w, start_angle=0, angle=PI, stroke_width=0, fill_color=color, fill_opacity=1)
    brim = RoundedRectangle(corner_radius=0.03 * w, width=0.95 * w, height=0.08 * w, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([0.05 * w, -0.02 * w, 0])
    ridge = Line([0, 0.02 * w, 0], [0, 0.34 * w, 0], stroke_color="#0E1117", stroke_width=2, stroke_opacity=0.4)
    return VGroup(dome, brim, ridge)


def blueprint(w: float = 1.4, color: str = "#2F6FB5") -> VGroup:
    """An architect's drawing: a blue sheet with a plan of rooms in white lines (``g.plan``)."""
    sheet = Rectangle(width=w, height=0.72 * w, stroke_width=0, fill_color=color, fill_opacity=1)
    s = w * 0.36
    plan = VGroup(Rectangle(width=2 * s, height=1.2 * s, stroke_color="#FFFFFF", stroke_width=2),
                  Line([-0.2 * s, 0.6 * s, 0], [-0.2 * s, -0.6 * s, 0], stroke_color="#FFFFFF", stroke_width=1.5),
                  Line([-s, 0.0, 0], [-0.2 * s, 0.0, 0], stroke_color="#FFFFFF", stroke_width=1.5),
                  Line([0.4 * s, 0.6 * s, 0], [0.4 * s, -0.1 * s, 0], stroke_color="#FFFFFF", stroke_width=1.5))
    g = VGroup(sheet, plan)
    g.plan = plan
    return g


def house_frame(w: float = 1.6, color: str = "#D9B382") -> VGroup:
    """A house under construction: timber studs, a top plate and roof trusses (``g.studs``, ``g.trusses``) on a slab."""
    slab = Rectangle(width=w * 1.05, height=0.06 * w, stroke_width=0, fill_color="#9AA3B2", fill_opacity=1).move_to([0, -0.03 * w, 0])
    studs = VGroup(*[Line([x, 0, 0], [x, 0.55 * w, 0], stroke_color=color, stroke_width=2.5) for x in np.linspace(-w / 2, w / 2, 9)])
    plate = Line([-w / 2, 0.55 * w, 0], [w / 2, 0.55 * w, 0], stroke_color=color, stroke_width=3)
    trusses = VGroup(Line([-0.58 * w, 0.55 * w, 0], [0, 0.9 * w, 0], stroke_color=color, stroke_width=3),
                     Line([0.58 * w, 0.55 * w, 0], [0, 0.9 * w, 0], stroke_color=color, stroke_width=3),
                     *[Line([x, 0.55 * w, 0], [x, 0.55 * w + 0.35 * w * (1 - abs(x) / (0.58 * w)), 0], stroke_color=color,
                            stroke_width=1.5) for x in np.linspace(-0.4 * w, 0.4 * w, 5)])
    g = VGroup(slab, studs, plate, trusses)
    g.studs, g.trusses = studs, trusses
    return g


def plot_lot(w: float = 1.6, color: str = "#7BD88F") -> VGroup:
    """An empty building lot: a patch of ground marked out by four corner stakes and a string line (``g.stakes``)."""
    ground = Polygon([-w / 2, 0, 0], [w / 2, 0, 0], [0.38 * w, 0.3 * w, 0], [-0.38 * w, 0.3 * w, 0], stroke_width=0,
                     fill_color=color, fill_opacity=0.35)
    corners = [[-w / 2, 0, 0], [w / 2, 0, 0], [0.38 * w, 0.3 * w, 0], [-0.38 * w, 0.3 * w, 0]]
    stakes = VGroup(*[Line(c, [c[0], c[1] + 0.14 * w, 0], stroke_color="#F2A65A", stroke_width=3) for c in corners])
    string = Polygon(*[[c[0], c[1] + 0.1 * w, 0] for c in corners], stroke_color="#F6C453", stroke_width=1.2, fill_opacity=0)
    g = VGroup(ground, string, stakes)
    g.stakes = stakes
    return g


def sale_sign(w: float = 0.9, text: str = "FOR SALE", color: str = "#E8554E") -> VGroup:
    """A for-sale sign on a post (``g.board``)."""
    post = Line([0, 0, 0], [0, 1.0 * w, 0], stroke_color="#C9D3E0", stroke_width=4)
    arm = Line([0, 0.95 * w, 0], [0.75 * w, 0.95 * w, 0], stroke_color="#C9D3E0", stroke_width=3)
    board = Rectangle(width=0.7 * w, height=0.4 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0.4 * w, 0.68 * w, 0])
    lab = tx(text, 13 * w, "#FFFFFF", bold=True).move_to(board)
    if lab.width > board.width * 0.9:
        lab.scale_to_fit_width(board.width * 0.9)
    g = VGroup(post, arm, board, lab)
    g.board = board
    return g


def house_key(w: float = 0.9, color: str = "#F6C453") -> VGroup:
    """A door key."""
    bow = Circle(radius=0.18 * w, stroke_color=color, stroke_width=5).move_to([-0.3 * w, 0, 0])
    blade = Line([-0.12 * w, 0, 0], [0.45 * w, 0, 0], stroke_color=color, stroke_width=6)
    teeth = VGroup(*[Line([x * w, 0, 0], [x * w, -0.1 * w, 0], stroke_color=color, stroke_width=5) for x in (0.25, 0.35, 0.43)])
    return VGroup(bow, blade, teeth)


# ---------------------------------------------------------------------------------------------------------------
# Property (Part 26)
# ---------------------------------------------------------------------------------------------------------------
def office_tower(w: float = 1.4, floors: int = 14, cols: int = 5, seed: int = 7) -> VGroup:
    """A glass office tower with a crown; ``g.windows`` is every window in random order, so ``light(g.windows, 0.87)``
    shows a building 87% occupied."""
    h = w * floors / cols * 0.8
    body = Rectangle(width=w, height=h, stroke_color="#5B6B84", stroke_width=1.5, fill_color="#1E2633",
                     fill_opacity=1).move_to([0, h / 2, 0])
    crown = Polygon([-0.42 * w, h, 0], [0.42 * w, h, 0], [0.25 * w, h + 0.12 * w, 0], [-0.25 * w, h + 0.12 * w, 0],
                    stroke_width=0, fill_color="#5B6B84", fill_opacity=1)
    mast = Line([0, h + 0.12 * w, 0], [0, h + 0.32 * w, 0], stroke_color="#8B95A7", stroke_width=2)
    cw, ch = w / cols, h / floors
    wins = [Rectangle(width=0.62 * cw, height=0.55 * ch, stroke_width=0, fill_color="#2A3446", fill_opacity=1).move_to(
        [-w / 2 + (j + 0.5) * cw, (i + 0.55) * ch, 0]) for i in range(floors) for j in range(cols)]
    order = np.random.default_rng(seed).permutation(len(wins))
    windows = VGroup(*[wins[k] for k in order])
    door = Rectangle(width=0.22 * w, height=0.5 * ch, stroke_width=0, fill_color=LIT, fill_opacity=0.8).move_to([0, 0.25 * ch, 0])
    g = VGroup(body, crown, mast, windows, door)
    g.windows = windows
    return g


def warehouse(w: float = 2.4, docks: int = 6, trucks: int = 2) -> VGroup:
    """A logistics shed: a long low box with a shallow roof, dock doors along the front (``g.docks``) and lorries backed
    up to some of them (``g.trucks``)."""
    h = 0.32 * w
    body = Rectangle(width=w, height=h, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to([0, h / 2, 0])
    roof = Polygon([-0.52 * w, h, 0], [0.52 * w, h, 0], [0.5 * w, h + 0.05 * w, 0], [-0.5 * w, h + 0.05 * w, 0],
                   stroke_width=0, fill_color="#8B95A7", fill_opacity=1)
    band = Rectangle(width=w, height=0.04 * w, stroke_width=0, fill_color="#4F8FE6", fill_opacity=1).move_to([0, 0.8 * h, 0])
    dw = w / (docks + 1)
    dock = VGroup(*[Rectangle(width=0.55 * dw, height=0.5 * h, stroke_width=0, fill_color="#5B6B84", fill_opacity=1).move_to(
        [-w / 2 + (k + 1) * dw, 0.25 * h, 0]) for k in range(docks)])
    lorries = VGroup()
    for k in range(min(trucks, docks)):
        x = -w / 2 + (2 * k + 1) * dw
        box = Rectangle(width=0.62 * dw, height=0.4 * h, stroke_color="#5B6B84", stroke_width=1.5, fill_color="#E8EAED",
                        fill_opacity=1).move_to([x, 0.2 * h, 0])
        lorries.add(box)
    g = VGroup(body, roof, band, dock, lorries)
    g.docks, g.trucks = dock, lorries
    return g


def mall(w: float = 2.6, stores: int = 7, colors=("#E8554E", "#F6C453", "#4F8FE6", "#7BD88F", "#B48EF0")) -> VGroup:
    """A shopping mall: a long front with an entrance arch and a row of shop windows (``g.stores``) whose awnings can
    be greyed to show empty units."""
    h = 0.36 * w
    body = Rectangle(width=w, height=h, stroke_width=0, fill_color="#D7DDE6", fill_opacity=1).move_to([0, h / 2, 0])
    arch = Arc(radius=0.14 * w, start_angle=0, angle=PI, stroke_color="#5B6B84", stroke_width=4).move_to([0, h + 0.04 * w, 0])
    entrance = Rectangle(width=0.22 * w, height=0.6 * h, stroke_width=0, fill_color=GLASS, fill_opacity=1).move_to([0, 0.3 * h, 0])
    sw = (w - 0.3 * w) / stores
    units = VGroup()
    for k in range(stores):
        x = -w / 2 + 0.02 * w + (k + 0.5) * sw + (0.28 * w if k >= stores // 2 else 0)
        win = Rectangle(width=0.8 * sw, height=0.45 * h, stroke_width=0, fill_color=GLASS, fill_opacity=1).move_to([x, 0.3 * h, 0])
        aw = Rectangle(width=0.86 * sw, height=0.1 * h, stroke_width=0, fill_color=colors[k % len(colors)], fill_opacity=1).move_to([x, 0.6 * h, 0])
        units.add(VGroup(win, aw))
    g = VGroup(body, arch, entrance, units)
    g.stores = units
    return g


def cell_tower(h: float = 2.0, color: str = "#8B95A7") -> VGroup:
    """A lattice mobile-phone mast with antenna panels (``g.antennas``), each panel a tenant."""
    legs = VGroup(Line([-0.18 * h, 0, 0], [-0.03 * h, h, 0], stroke_color=color, stroke_width=3),
                  Line([0.18 * h, 0, 0], [0.03 * h, h, 0], stroke_color=color, stroke_width=3))
    braces = VGroup()
    for k in range(6):
        y0, y1 = k * h / 6, (k + 1) * h / 6
        x0, x1 = 0.18 * h - 0.15 * h * y0 / h, 0.18 * h - 0.15 * h * y1 / h
        braces.add(Line([-x0, y0, 0], [x1, y1, 0], stroke_color=color, stroke_width=1.2),
                   Line([x0, y0, 0], [-x1, y1, 0], stroke_color=color, stroke_width=1.2))
    ant = VGroup()
    for k, (y, c) in enumerate(((0.92, "#E8554E"), (0.78, "#4F8FE6"), (0.64, "#F6C453"))):
        for sgn in (-1, 1):
            ant.add(Rectangle(width=0.035 * h, height=0.1 * h, stroke_width=0, fill_color=c, fill_opacity=1).move_to(
                [sgn * 0.09 * h, y * h, 0]))
    g = VGroup(legs, braces, ant)
    g.antennas = ant
    return g


def lease(w: float = 1.2, color: str = "#E8EAED") -> VGroup:
    """A signed lease: a page with ruled lines (``g.lines``), a heading and a signature (``g.signature``)."""
    page = Polygon([-w / 2, -0.65 * w, 0], [w / 2, -0.65 * w, 0], [w / 2, 0.5 * w, 0], [0.32 * w, 0.65 * w, 0],
                   [-w / 2, 0.65 * w, 0], stroke_width=0, fill_color=color, fill_opacity=1)
    head = Rectangle(width=0.5 * w, height=0.07 * w, stroke_width=0, fill_color="#5B6B84", fill_opacity=1).move_to([-0.1 * w, 0.48 * w, 0])
    lines = VGroup(*[Line([-0.38 * w, y * w, 0], [(0.38 if k % 3 else 0.2) * w, y * w, 0], stroke_color="#9AA3B2", stroke_width=1.5)
                     for k, y in enumerate(np.linspace(0.32, -0.3, 8))])
    sig = VGroup(CubicBezier([-0.32 * w, -0.48 * w, 0], [-0.2 * w, -0.32 * w, 0], [-0.1 * w, -0.62 * w, 0], [0.02 * w, -0.46 * w, 0],
                             stroke_color="#4F8FE6", stroke_width=2.5),
                 CubicBezier([0.02 * w, -0.46 * w, 0], [0.12 * w, -0.36 * w, 0], [0.2 * w, -0.56 * w, 0], [0.34 * w, -0.44 * w, 0],
                             stroke_color="#4F8FE6", stroke_width=2.5))
    g = VGroup(page, head, lines, sig)
    g.lines, g.signature = lines, sig
    return g


# ---------------------------------------------------------------------------------------------------------------
# Shipping (Part 27)
# ---------------------------------------------------------------------------------------------------------------
def container(w: float = 2.0, color: str = "#E8554E", feet: int = 40) -> VGroup:
    """A shipping container seen from the side: corrugated ribs, corner castings and door bars at one end; 40 or 20 feet
    long (``feet``), 8.5 feet high."""
    h = w * 8.5 / feet
    body = Rectangle(width=w, height=h, stroke_color="#0E1117", stroke_width=1.5, fill_color=color, fill_opacity=1)
    n = max(6, int(feet / 2))
    ribs = VGroup(*[Line([-w / 2 + w * (k + 0.5) / n, -0.42 * h, 0], [-w / 2 + w * (k + 0.5) / n, 0.42 * h, 0],
                         stroke_color="#0E1117", stroke_width=0.8, stroke_opacity=0.45) for k in range(n)])
    corners = VGroup(*[Square(side_length=0.12 * h, stroke_width=0, fill_color="#2E3645", fill_opacity=1).move_to(
        [sx * (w / 2 - 0.06 * h), sy * (h / 2 - 0.06 * h), 0]) for sx in (-1, 1) for sy in (-1, 1)])
    bars = VGroup(*[Line([w / 2 - k * 0.07 * h, -0.4 * h, 0], [w / 2 - k * 0.07 * h, 0.4 * h, 0], stroke_color="#E8EAED",
                         stroke_width=1.5) for k in (1.6, 2.6)])
    return VGroup(body, ribs, corners, bars)


def quay_crane(h: float = 3.0, color: str = "#F2A65A") -> VGroup:
    """A ship-to-shore container crane: two A-frame legs, a boom reaching out over the water (``g.boom``) and a spreader
    hanging from its trolley (``g.spreader``)."""
    legs = VGroup(Line([-0.25 * h, 0, 0], [-0.18 * h, 0.62 * h, 0], stroke_color=color, stroke_width=5),
                  Line([0.12 * h, 0, 0], [0.05 * h, 0.62 * h, 0], stroke_color=color, stroke_width=5),
                  Line([-0.22 * h, 0.3 * h, 0], [0.09 * h, 0.3 * h, 0], stroke_color=color, stroke_width=3))
    boom = Line([-0.45 * h, 0.62 * h, 0], [0.75 * h, 0.62 * h, 0], stroke_color=color, stroke_width=6)
    apex = VGroup(Line([-0.12 * h, 0.62 * h, 0], [-0.06 * h, 0.9 * h, 0], stroke_color=color, stroke_width=3),
                  Line([-0.06 * h, 0.9 * h, 0], [0.62 * h, 0.64 * h, 0], stroke_color=color, stroke_width=1.5),
                  Line([-0.06 * h, 0.9 * h, 0], [-0.42 * h, 0.64 * h, 0], stroke_color=color, stroke_width=1.5))
    cab = Rectangle(width=0.07 * h, height=0.05 * h, stroke_width=0, fill_color="#E8EAED", fill_opacity=1).move_to([0.45 * h, 0.585 * h, 0])
    rope = Line([0.45 * h, 0.56 * h, 0], [0.45 * h, 0.32 * h, 0], stroke_color="#C9D3E0", stroke_width=1.2)
    spreader = Rectangle(width=0.16 * h, height=0.02 * h, stroke_width=0, fill_color="#F6C453", fill_opacity=1).move_to([0.45 * h, 0.31 * h, 0])
    g = VGroup(legs, boom, apex, cab, rope, spreader)
    g.boom, g.spreader = boom, VGroup(rope, spreader)
    return g


def shoebox(w: float = 1.0, color: str = "#F2A65A") -> VGroup:
    """A shoebox with a lid and a trainer printed on the side."""
    box = Rectangle(width=w, height=0.42 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, 0.21 * w, 0])
    lid = Rectangle(width=1.04 * w, height=0.1 * w, stroke_width=0, fill_color="#E8EAED", fill_opacity=1).move_to([0, 0.44 * w, 0])
    shoe = sneaker(0.5 * w).move_to([0, 0.2 * w, 0])
    return VGroup(box, lid, shoe)


def semi(w: float = 3.0, color: str = "#E8EAED", cab_color: str = "#E8554E", box: bool = True) -> VGroup:
    """A tractor-trailer in side view, facing right: ``w`` is its length; a 53-foot box trailer (``box``) or a flat
    chassis for a container (``g.deck``); ``g.trailer`` and ``g.tractor`` for colouring."""
    def wheel(x, r=0.035 * w):
        return VGroup(Circle(radius=r, stroke_width=0, fill_color="#20242C", fill_opacity=1).move_to([x, r, 0]),
                      Circle(radius=0.45 * r, stroke_width=0, fill_color="#9AA3B2", fill_opacity=1).move_to([x, r, 0]))
    tl = 0.76 * w
    trailer = Rectangle(width=tl, height=0.2 * w if box else 0.02 * w, stroke_color="#0E1117", stroke_width=1,
                        fill_color=color if box else "#5C6472", fill_opacity=1)
    trailer.move_to([-w / 2 + tl / 2, (0.1 * w if box else 0.01 * w) + 0.075 * w, 0])
    skirt = Rectangle(width=0.3 * tl, height=0.025 * w, stroke_width=0, fill_color="#5C6472", fill_opacity=1).move_to(
        [-w / 2 + 0.55 * tl, 0.068 * w, 0])
    hood = RoundedRectangle(corner_radius=0.015 * w, width=0.12 * w, height=0.09 * w, stroke_width=0, fill_color=cab_color,
                            fill_opacity=1).move_to([w / 2 - 0.06 * w, 0.1 * w, 0])
    cabin = RoundedRectangle(corner_radius=0.02 * w, width=0.13 * w, height=0.17 * w, stroke_width=0, fill_color=cab_color,
                             fill_opacity=1).move_to([w / 2 - 0.17 * w, 0.14 * w, 0])
    glass = Polygon([w / 2 - 0.11 * w, 0.2 * w, 0], [w / 2 - 0.12 * w, 0.165 * w, 0], [w / 2 - 0.17 * w, 0.165 * w, 0],
                    [w / 2 - 0.17 * w, 0.2 * w, 0], stroke_width=0, fill_color=GLASS, fill_opacity=1)
    stack = Rectangle(width=0.008 * w, height=0.12 * w, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to(
        [w / 2 - 0.235 * w, 0.2 * w, 0])
    frame = Rectangle(width=0.28 * w, height=0.015 * w, stroke_width=0, fill_color="#2E3645", fill_opacity=1).move_to(
        [w / 2 - 0.14 * w, 0.06 * w, 0])
    wheels = VGroup(*[wheel(x) for x in (-w / 2 + 0.06 * w, -w / 2 + 0.14 * w, w / 2 - 0.3 * w, w / 2 - 0.22 * w,
                                         w / 2 - 0.06 * w)])
    tractor = VGroup(frame, hood, cabin, glass, stack)
    g = VGroup(trailer, skirt, tractor, wheels)
    g.trailer, g.tractor, g.deck = trailer, tractor, trailer
    return g


def locomotive(w: float = 2.0, color: str = "#F6C453") -> VGroup:
    """A diesel-electric freight locomotive in side view, cab at the right; ``w`` is its length."""
    body = Rectangle(width=0.78 * w, height=0.2 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [-0.08 * w, 0.17 * w, 0])
    cab = Polygon([0.31 * w, 0.07 * w, 0], [0.48 * w, 0.07 * w, 0], [0.48 * w, 0.2 * w, 0], [0.42 * w, 0.29 * w, 0],
                  [0.31 * w, 0.29 * w, 0], stroke_width=0, fill_color=color, fill_opacity=1)
    win = Polygon([0.42 * w, 0.27 * w, 0], [0.46 * w, 0.21 * w, 0], [0.38 * w, 0.21 * w, 0], [0.38 * w, 0.27 * w, 0],
                  stroke_width=0, fill_color=GLASS, fill_opacity=1)
    stripe = Rectangle(width=0.95 * w, height=0.02 * w, stroke_width=0, fill_color="#E8554E", fill_opacity=1).move_to(
        [0.0, 0.11 * w, 0])
    frame = Rectangle(width=0.98 * w, height=0.03 * w, stroke_width=0, fill_color="#2E3645", fill_opacity=1).move_to([0, 0.06 * w, 0])
    louvres = VGroup(*[Line([-0.4 * w + k * 0.06 * w, 0.14 * w, 0], [-0.4 * w + k * 0.06 * w, 0.24 * w, 0],
                            stroke_color="#0E1117", stroke_width=1, stroke_opacity=0.4) for k in range(10)])
    trucks_ = VGroup(*[VGroup(*[Circle(radius=0.03 * w, stroke_width=0, fill_color="#20242C", fill_opacity=1).move_to(
        [c + d * w, 0.03 * w, 0]) for d in (-0.07, 0.0, 0.07)]) for c in (-0.3 * w, 0.28 * w)])
    return VGroup(body, cab, win, stripe, louvres, frame, trucks_)


def railcar(w: float = 1.6, kind: str = "box", color: str = "#B58CFF") -> VGroup:
    """A freight car in side view: ``kind`` is box, hopper (coal or grain), tank or well (a double-stacked container car)."""
    frame = Rectangle(width=w, height=0.025 * w, stroke_width=0, fill_color="#2E3645", fill_opacity=1).move_to([0, 0.07 * w, 0])
    wheels = VGroup(*[Circle(radius=0.035 * w, stroke_width=0, fill_color="#20242C", fill_opacity=1).move_to([x * w, 0.035 * w, 0])
                      for x in (-0.42, -0.32, 0.32, 0.42)])
    if kind == "hopper":
        body = Polygon([-0.48 * w, 0.32 * w, 0], [0.48 * w, 0.32 * w, 0], [0.42 * w, 0.1 * w, 0], [0.12 * w, 0.08 * w, 0],
                       [-0.12 * w, 0.08 * w, 0], [-0.42 * w, 0.1 * w, 0], stroke_width=0, fill_color=color, fill_opacity=1)
        load = Polygon([-0.46 * w, 0.32 * w, 0], [0.46 * w, 0.32 * w, 0], [0.3 * w, 0.37 * w, 0], [-0.3 * w, 0.37 * w, 0],
                       stroke_width=0, fill_color="#20242C", fill_opacity=1)
        body = VGroup(body, load)
    elif kind == "tank":
        body = RoundedRectangle(corner_radius=0.1 * w, width=0.96 * w, height=0.22 * w, stroke_width=0, fill_color=color,
                                fill_opacity=1).move_to([0, 0.2 * w, 0])
    elif kind == "well":
        a = container(0.46 * w, color=color, feet=40).move_to([-0.24 * w, 0.14 * w, 0])
        b = container(0.46 * w, color="#7EC8F5", feet=40).move_to([0.24 * w, 0.14 * w, 0])
        c = container(0.92 * w, color="#F2A65A", feet=40).next_to(VGroup(a, b), UP, buff=0.004 * w)
        body = VGroup(a, b, c)
    else:
        body = Rectangle(width=0.96 * w, height=0.26 * w, stroke_color="#0E1117", stroke_width=1, fill_color=color,
                         fill_opacity=1).move_to([0, 0.215 * w, 0])
        door = Rectangle(width=0.16 * w, height=0.22 * w, stroke_color="#0E1117", stroke_width=1, fill_opacity=0).move_to(
            [0, 0.215 * w, 0])
        body = VGroup(body, door)
    return VGroup(body, frame, wheels)


def train(n: int = 8, car_w: float = 1.0, kinds=("hopper",), colors=("#B58CFF",), loco_color: str = "#F6C453") -> VGroup:
    """A locomotive at the front (right) and ``n`` cars behind it (``g.cars``), all on one line."""
    loco = locomotive(1.25 * car_w, color=loco_color)
    cars = VGroup(*[railcar(car_w, kind=kinds[i % len(kinds)], color=colors[i % len(colors)]) for i in range(n)])
    cars.arrange(LEFT, buff=0.04 * car_w, aligned_edge=DOWN)
    g = VGroup(cars, loco)
    loco.next_to(cars, RIGHT, buff=0.04 * car_w, aligned_edge=DOWN)
    g.cars, g.loco = cars, loco
    return g


def van(w: float = 1.6, color: str = "#8B5E3C") -> VGroup:
    """A delivery van in side view, facing right."""
    body = Polygon([-0.5 * w, 0.08 * w, 0], [0.5 * w, 0.08 * w, 0], [0.5 * w, 0.22 * w, 0], [0.4 * w, 0.42 * w, 0],
                   [-0.5 * w, 0.42 * w, 0], stroke_width=0, fill_color=color, fill_opacity=1)
    glass = Polygon([0.37 * w, 0.4 * w, 0], [0.46 * w, 0.24 * w, 0], [0.3 * w, 0.24 * w, 0], [0.3 * w, 0.4 * w, 0],
                    stroke_width=0, fill_color=GLASS, fill_opacity=1)
    door = Rectangle(width=0.18 * w, height=0.3 * w, stroke_color="#0E1117", stroke_width=1, fill_opacity=0).move_to(
        [0.08 * w, 0.25 * w, 0])
    wheels = VGroup(*[_wheel(0.075 * w).move_to([x * w, 0.075 * w, 0]) for x in (-0.32, 0.32)])
    return VGroup(body, glass, door, wheels)


def parcel(w: float = 0.6, color: str = "#C89F6A") -> VGroup:
    """A cardboard parcel, three-quarter view, with tape and a label."""
    front = Polygon([-0.5 * w, 0, 0], [0.3 * w, 0, 0], [0.3 * w, 0.6 * w, 0], [-0.5 * w, 0.6 * w, 0], stroke_width=0,
                    fill_color=color, fill_opacity=1)
    side = Polygon([0.3 * w, 0, 0], [0.5 * w, 0.15 * w, 0], [0.5 * w, 0.75 * w, 0], [0.3 * w, 0.6 * w, 0], stroke_width=0,
                   fill_color="#A87F4E", fill_opacity=1)
    top = Polygon([-0.5 * w, 0.6 * w, 0], [0.3 * w, 0.6 * w, 0], [0.5 * w, 0.75 * w, 0], [-0.3 * w, 0.75 * w, 0], stroke_width=0,
                  fill_color="#DDB98A", fill_opacity=1)
    tape = Polygon([-0.14 * w, 0.6 * w, 0], [-0.02 * w, 0.6 * w, 0], [0.18 * w, 0.75 * w, 0], [0.06 * w, 0.75 * w, 0],
                   stroke_width=0, fill_color="#E8E2D4", fill_opacity=0.9)
    label = Rectangle(width=0.28 * w, height=0.18 * w, stroke_width=0, fill_color="#F5F5F5", fill_opacity=1).move_to(
        [-0.12 * w, 0.3 * w, 0])
    return VGroup(front, side, top, tape, label)


def web_page(w: float = 3.2, cols: int = 4, rows: int = 2, sponsored=(), accent: str = "#F6C453",
             tile: str = "#2E3645") -> VGroup:
    """A shop's results page in a browser window: a title bar, a search box and a grid of product tiles (``g.tiles``,
    row by row), each with a picture, a name line and a price line.  Tiles whose index is in ``sponsored`` carry an
    ``accent`` outline and a small 'ad' flag (``g.flags``)."""
    h = 0.62 * w
    frame = RoundedRectangle(corner_radius=0.03 * w, width=w, height=h, stroke_color="#9AA3B2", stroke_width=2,
                             fill_color="#161B24", fill_opacity=1)
    bar = Rectangle(width=w, height=0.07 * w, stroke_width=0, fill_color="#2E3645", fill_opacity=1).move_to([0, h / 2 - 0.035 * w, 0])
    dots = VGroup(*[Dot(radius=0.009 * w, color=c).move_to([-0.47 * w + 0.03 * w * k, h / 2 - 0.035 * w, 0])
                    for k, c in enumerate(("#E8554E", "#F6C453", "#7BD88F"))])
    search = RoundedRectangle(corner_radius=0.015 * w, width=0.6 * w, height=0.05 * w, stroke_color="#6B7486", stroke_width=1,
                              fill_color="#0E1117", fill_opacity=1).move_to([0, h / 2 - 0.12 * w, 0])
    gw, gh = 0.92 * w, h - 0.2 * w
    tw, th = gw / cols * 0.86, gh / rows * 0.86
    tiles, flags = VGroup(), VGroup()
    for i in range(rows * cols):
        r, c = divmod(i, cols)
        x = -gw / 2 + gw / cols * (c + 0.5)
        y = (h / 2 - 0.17 * w) - gh / rows * (r + 0.5)
        ad = i in sponsored
        box = RoundedRectangle(corner_radius=0.01 * w, width=tw, height=th, stroke_color=accent if ad else "#3A4250",
                               stroke_width=2.5 if ad else 1, fill_color=tile, fill_opacity=1).move_to([x, y, 0])
        pic = Rectangle(width=0.7 * tw, height=0.5 * th, stroke_width=0, fill_color="#4A5568", fill_opacity=1).move_to(
            [x, y + 0.14 * th, 0])
        name = Line([x - 0.35 * tw, y - 0.2 * th, 0], [x + 0.3 * tw, y - 0.2 * th, 0], stroke_color="#9AA3B2", stroke_width=2)
        price = Line([x - 0.35 * tw, y - 0.33 * th, 0], [x - 0.05 * tw, y - 0.33 * th, 0], stroke_color="#7BD88F", stroke_width=3)
        t = VGroup(box, pic, name, price)
        if ad:
            f = RoundedRectangle(corner_radius=0.005 * w, width=0.22 * tw, height=0.12 * th, stroke_width=0, fill_color=accent,
                                 fill_opacity=1).move_to([x + 0.33 * tw, y + 0.4 * th, 0])
            flags.add(f)
            t.add(f)
        tiles.add(t)
    g = VGroup(frame, bar, dots, search, tiles)
    g.tiles, g.flags = tiles, flags
    return g


def drive_robot(w: float = 0.7, color: str = "#F2A65A", pod: bool = True) -> VGroup:
    """A warehouse drive unit in side view, a low squat robot on wheels; with ``pod``, a shelf pod of bins rides on top
    (``g.pod``)."""
    body = RoundedRectangle(corner_radius=0.08 * w, width=w, height=0.22 * w, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([0, 0.15 * w, 0])
    wheels = VGroup(*[_wheel(0.05 * w).move_to([x * w, 0.05 * w, 0]) for x in (-0.32, 0.32)])
    g = VGroup(body, wheels)
    g.pod = VGroup()
    if pod:
        legs = VGroup(*[Rectangle(width=0.04 * w, height=0.12 * w, stroke_width=0, fill_color="#6B7486", fill_opacity=1).move_to(
            [x * w, 0.32 * w, 0]) for x in (-0.4, 0.4)])
        bins = VGroup(*[Rectangle(width=0.84 * w, height=0.24 * w, stroke_color="#0E1117", stroke_width=1, fill_color=c,
                                  fill_opacity=1).move_to([0, 0.5 * w + 0.25 * w * k, 0])
                        for k, c in enumerate(("#3D7CC9", "#5A8FD0", "#3D7CC9", "#5A8FD0"))])
        g.pod = VGroup(legs, bins)
        g.add(g.pod)
    return g


def pallet(w: float = 1.4, rows: int = 3, cols: int = 4, color: str = "#C89F6A") -> VGroup:
    """A wooden pallet with cases stacked on it (``g.cases``, bottom row first), front view; sits on y = 0."""
    base = VGroup(*[Rectangle(width=w, height=0.035 * w, stroke_width=0, fill_color="#8B6B43", fill_opacity=1).move_to(
        [0, y * w, 0]) for y in (0.0175, 0.1)])
    legs = VGroup(*[Rectangle(width=0.1 * w, height=0.05 * w, stroke_width=0, fill_color="#6E5233", fill_opacity=1).move_to(
        [x * w, 0.06 * w, 0]) for x in (-0.42, 0, 0.42)])
    cw, ch = 0.96 * w / cols, 0.2 * w
    cases = VGroup()
    for r_ in range(rows):
        for c_ in range(cols):
            box = Rectangle(width=cw * 0.96, height=ch * 0.94, stroke_color="#0E1117", stroke_width=1, fill_color=color,
                            fill_opacity=1).move_to([-0.48 * w + cw * (c_ + 0.5), 0.12 * w + ch * (r_ + 0.5), 0])
            tape = Line(box.get_top() + DOWN * 0.001, box.get_top() + DOWN * ch * 0.3, stroke_color="#E8E2D4", stroke_width=2)
            cases.add(VGroup(box, tape))
    g = VGroup(base, legs, cases)
    g.cases = cases
    return g


def invoice(w: float = 1.0, terms: str = "net 30", color: str = "#E8EAED") -> VGroup:
    """A paper invoice with a heading bar, line items, a total and its payment terms (``g.terms``)."""
    h = 1.3 * w
    paper = Polygon([-0.5 * w, -0.5 * h, 0], [0.5 * w, -0.5 * h, 0], [0.5 * w, 0.38 * h, 0], [0.38 * w, 0.5 * h, 0],
                    [-0.5 * w, 0.5 * h, 0], stroke_width=0, fill_color=color, fill_opacity=1)
    bar = Rectangle(width=0.8 * w, height=0.08 * h, stroke_width=0, fill_color="#7EC8F5", fill_opacity=1).move_to([-0.05 * w, 0.36 * h, 0])
    lines = VGroup(*[Line([-0.4 * w, y * h, 0], [0.3 * w, y * h, 0], stroke_color="#9AA3B2", stroke_width=2) for y in (0.18, 0.08, -0.02, -0.12)])
    total = Line([0.05 * w, -0.24 * h, 0], [0.4 * w, -0.24 * h, 0], stroke_color="#20242C", stroke_width=4)
    t = tx(terms, 22 * w, "#E8554E", bold=True)
    if t.width > 0.55 * w:
        t.scale_to_fit_width(0.55 * w)
    t.move_to([-0.15 * w, -0.38 * h, 0])
    g = VGroup(paper, bar, lines, total, t)
    g.terms = t
    return g


def restaurant(w: float = 2.0, color: str = "#E8554E", sign: str = "#F6C453") -> VGroup:
    """A quick-service restaurant in side view: a low building with a band of colour, big windows, a door, a pole sign
    (``g.sign``) and a drive-through lane with a car at the window (``g.car``); sits on y = 0."""
    h = 0.34 * w
    body = Rectangle(width=0.7 * w, height=h, stroke_width=0, fill_color="#E8EAED", fill_opacity=1).move_to([0, h / 2, 0])
    band = Rectangle(width=0.74 * w, height=0.08 * w, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, h + 0.02 * w, 0])
    roof = Polygon([-0.37 * w, h + 0.06 * w, 0], [0.37 * w, h + 0.06 * w, 0], [0.3 * w, h + 0.12 * w, 0], [-0.3 * w, h + 0.12 * w, 0],
                   stroke_width=0, fill_color="#9AA3B2", fill_opacity=1)
    wins = VGroup(*[Rectangle(width=0.12 * w, height=0.14 * w, stroke_width=0, fill_color=GLASS, fill_opacity=1).move_to(
        [x * w, 0.18 * w, 0]) for x in (-0.24, -0.1, 0.04)])
    door = Rectangle(width=0.07 * w, height=0.2 * w, stroke_width=0, fill_color="#5A6577", fill_opacity=1).move_to([0.2 * w, 0.1 * w, 0])
    pole = Rectangle(width=0.02 * w, height=0.55 * w, stroke_width=0, fill_color="#9AA3B2", fill_opacity=1).move_to([-0.48 * w, 0.275 * w, 0])
    board = RoundedRectangle(corner_radius=0.02 * w, width=0.16 * w, height=0.12 * w, stroke_width=0, fill_color=sign,
                             fill_opacity=1).move_to([-0.48 * w, 0.58 * w, 0])
    lane = Line([0.36 * w, 0.0, 0], [0.62 * w, 0.0, 0], stroke_color="#6B7486", stroke_width=3)
    car_ = car(0.2 * w, color="#7EC8F5").move_to([0.5 * w, 0.045 * w, 0])
    g = VGroup(body, band, roof, wins, door, pole, board, lane, car_)
    g.sign, g.car = board, car_
    return g


def burger(w: float = 0.8) -> VGroup:
    """A hamburger, front view: bun, lettuce, cheese, patty and the bottom bun."""
    top = Polygon(*[[0.5 * w * np.cos(t), 0.28 * w + 0.3 * w * np.sin(t), 0] for t in np.linspace(0, PI, 24)], stroke_width=0,
                  fill_color="#D9A35B", fill_opacity=1)
    top_base = Rectangle(width=w, height=0.04 * w, stroke_width=0, fill_color="#D9A35B", fill_opacity=1).move_to([0, 0.28 * w, 0])
    seeds = VGroup(*[Ellipse(width=0.06 * w, height=0.03 * w, stroke_width=0, fill_color="#F5E6C8", fill_opacity=1).move_to(
        [x * w, y * w, 0]) for x, y in ((-0.2, 0.5), (0.0, 0.58), (0.2, 0.5), (-0.08, 0.42), (0.12, 0.4))])
    lettuce = Rectangle(width=1.04 * w, height=0.05 * w, stroke_width=0, fill_color="#7BD88F", fill_opacity=1).move_to([0, 0.235 * w, 0])
    cheese = Polygon([-0.5 * w, 0.21 * w, 0], [0.5 * w, 0.21 * w, 0], [0.38 * w, 0.15 * w, 0], [-0.38 * w, 0.15 * w, 0], stroke_width=0,
                     fill_color="#F6C453", fill_opacity=1)
    patty = RoundedRectangle(corner_radius=0.04 * w, width=w, height=0.12 * w, stroke_width=0, fill_color="#6B3E26", fill_opacity=1).move_to(
        [0, 0.13 * w, 0])
    bottom = RoundedRectangle(corner_radius=0.05 * w, width=0.96 * w, height=0.1 * w, stroke_width=0, fill_color="#C88E4A",
                              fill_opacity=1).move_to([0, 0.03 * w, 0])
    return VGroup(bottom, patty, cheese, lettuce, top, top_base, seeds)


def hotel(w: float = 1.6, floors: int = 12, cols: int = 6, color: str = "#F6C453", seed: int = 11) -> VGroup:
    """A hotel tower in front view: a pale slab with rows of room windows (``g.windows``, random order, so
    ``light(g.windows, 0.69)`` shows a hotel 69% full), a lit sign on the roof (``g.sign``), a canopy over the entrance and
    a low podium for the lobby and restaurants; sits on y = 0."""
    pod_h = 0.22 * w
    h = w * floors / cols * 0.62
    podium = Rectangle(width=1.3 * w, height=pod_h, stroke_width=0, fill_color="#8B95A7", fill_opacity=1).move_to([0, pod_h / 2, 0])
    body = Rectangle(width=w, height=h, stroke_color="#5B6B84", stroke_width=1.2, fill_color="#C9D3E0",
                     fill_opacity=1).move_to([0, pod_h + h / 2, 0])
    cw, ch = w / cols, h / floors
    wins = [Rectangle(width=0.6 * cw, height=0.5 * ch, stroke_width=0, fill_color="#2A3446", fill_opacity=1).move_to(
        [-w / 2 + (j + 0.5) * cw, pod_h + (i + 0.5) * ch, 0]) for i in range(floors) for j in range(cols)]
    order = np.random.default_rng(seed).permutation(len(wins))
    windows = VGroup(*[wins[k] for k in order])
    sign = RoundedRectangle(corner_radius=0.03 * w, width=0.62 * w, height=0.13 * w, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to([0, pod_h + h + 0.1 * w, 0])
    canopy = Polygon([-0.3 * w, 0.17 * w, 0], [0.3 * w, 0.17 * w, 0], [0.36 * w, 0.13 * w, 0], [-0.36 * w, 0.13 * w, 0],
                     stroke_width=0, fill_color=color, fill_opacity=1)
    door = Rectangle(width=0.22 * w, height=0.12 * w, stroke_width=0, fill_color=LIT, fill_opacity=0.85).move_to([0, 0.06 * w, 0])
    g = VGroup(podium, body, windows, sign, canopy, door)
    g.windows, g.sign = windows, sign
    return g


def bed(w: float = 1.0, color: str = "#7EC8F5") -> VGroup:
    """A hotel bed in side view: headboard, mattress, pillow and duvet; sits on y = 0."""
    frame = Rectangle(width=w, height=0.1 * w, stroke_width=0, fill_color="#8B95A7", fill_opacity=1).move_to([0, 0.13 * w, 0])
    legs = VGroup(*[Rectangle(width=0.05 * w, height=0.08 * w, stroke_width=0, fill_color="#5B6B84", fill_opacity=1).move_to(
        [x * w, 0.04 * w, 0]) for x in (-0.45, 0.45)])
    head = RoundedRectangle(corner_radius=0.04 * w, width=0.08 * w, height=0.5 * w, stroke_width=0, fill_color="#5B6B84",
                            fill_opacity=1).move_to([-0.48 * w, 0.3 * w, 0])
    mattress = RoundedRectangle(corner_radius=0.03 * w, width=0.92 * w, height=0.1 * w, stroke_width=0, fill_color="#E8EAED",
                                fill_opacity=1).move_to([0.02 * w, 0.23 * w, 0])
    pillow = Ellipse(width=0.22 * w, height=0.1 * w, stroke_width=0, fill_color="#FFFFFF", fill_opacity=1).move_to([-0.3 * w, 0.32 * w, 0])
    duvet = RoundedRectangle(corner_radius=0.03 * w, width=0.6 * w, height=0.07 * w, stroke_width=0, fill_color=color,
                             fill_opacity=1).move_to([0.17 * w, 0.31 * w, 0])
    return VGroup(legs, frame, head, mattress, pillow, duvet)


def cruise_ship(w: float = 3.6, decks: int = 5, color: str = "#E8EAED", funnel: str = "#E8554E", seed: int = 5) -> VGroup:
    """A cruise ship in side view: a dark hull, stacked white decks of cabin windows (``g.windows``, random order for
    ``light``), a funnel and a waterline; sits on y = 0."""
    hull_h = 0.12 * w
    hull = Polygon([-0.5 * w, hull_h, 0], [0.52 * w, hull_h, 0], [0.44 * w, 0, 0], [-0.46 * w, 0, 0],
                   stroke_width=0, fill_color="#1F3A5F", fill_opacity=1)
    deck_h = 0.045 * w
    decks_g, wins = VGroup(), []
    for d in range(decks):
        span = 0.94 - 0.07 * d
        x0 = -0.47 * w + 0.03 * d * w
        y = hull_h + (d + 0.5) * deck_h
        decks_g.add(Rectangle(width=span * w, height=deck_h, stroke_color="#C9D3E0", stroke_width=0.6, fill_color=color,
                              fill_opacity=1).move_to([x0 + span * w / 2, y, 0]))
        n = int(span * 34)
        for k in range(n):
            wins.append(Rectangle(width=0.012 * w, height=0.018 * w, stroke_width=0, fill_color="#2A3446", fill_opacity=1).move_to(
                [x0 + (k + 0.5) * span * w / n, y, 0]))
    order = np.random.default_rng(seed).permutation(len(wins))
    windows = VGroup(*[wins[k] for k in order])
    top_y = hull_h + decks * deck_h
    stack = Polygon([0.12 * w, top_y, 0], [0.22 * w, top_y, 0], [0.24 * w, top_y + 0.1 * w, 0], [0.15 * w, top_y + 0.1 * w, 0],
                    stroke_width=0, fill_color=funnel, fill_opacity=1)
    water = Line([-0.6 * w, 0.01 * w, 0], [0.62 * w, 0.01 * w, 0], stroke_color="#4F8FE6", stroke_width=3)
    g = VGroup(hull, decks_g, windows, stack, water)
    g.windows = windows
    return g


def chip_stack(w: float = 0.6, n: int = 5, color: str = "#E8554E") -> VGroup:
    """A stack of casino chips, slightly offset, each with a white edge band; sits on y = 0."""
    g = VGroup()
    for k in range(n):
        c = Ellipse(width=w, height=0.3 * w, stroke_color="#FFFFFF", stroke_width=1.5, fill_color=color, fill_opacity=1).move_to(
            [0.02 * w * ((k % 2) * 2 - 1), 0.15 * w + 0.09 * w * k, 0])
        g.add(c)
    return g


def ferris_wheel(w: float = 2.0, cars: int = 10, color: str = "#B58CFF") -> VGroup:
    """A Ferris wheel on an A-frame with ``cars`` gondolas (``g.wheel`` rotates about ``g.hub``); sits on y = 0."""
    r = 0.42 * w
    hub = [0, 0.5 * w, 0]
    rim = Circle(radius=r, stroke_color=color, stroke_width=3).move_to(hub)
    spokes = VGroup(*[Line(hub, [hub[0] + r * np.cos(t), hub[1] + r * np.sin(t), 0], stroke_color=color, stroke_width=1.2)
                      for t in np.linspace(0, TAU, cars, endpoint=False)])
    gond = VGroup(*[RoundedRectangle(corner_radius=0.01 * w, width=0.07 * w, height=0.06 * w, stroke_width=0,
                                     fill_color=["#F6C453", "#7EC8F5", "#FF8FB1", "#7BD88F"][k % 4], fill_opacity=1).move_to(
        [hub[0] + r * np.cos(t), hub[1] + r * np.sin(t) - 0.03 * w, 0]) for k, t in enumerate(np.linspace(0, TAU, cars, endpoint=False))])
    legs = VGroup(Line([-0.25 * w, 0, 0], hub, stroke_color="#8B95A7", stroke_width=3),
                  Line([0.25 * w, 0, 0], hub, stroke_color="#8B95A7", stroke_width=3))
    wheel = VGroup(rim, spokes, gond)
    g = VGroup(legs, wheel, Dot(hub, radius=0.03 * w, color="#C9D3E0"))
    g.wheel, g.hub = wheel, np.array(hub)
    return g

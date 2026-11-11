"""Schematic symbols for the hardware layer (Parts 3 to 6): logic gates, switches, relays, transistors and wires.

    g = gate("NAND").move_to(ORIGIN)        # g.inp[0], g.inp[1], g.out are pin positions (call them: they follow g)
    w = wire(a.out(), g.inp[0]())           # an orthogonal wire from one pin to another
    sw = switch(closed=False)               # sw.set(True) gives the animation that closes it
    t = nmos(); p = pmos()                  # transistors as switches, with gate / drain / source pins

Gates use the distinctive-shape (ANSI) symbols.  Pins are functions so that they track the mobject after it moves.
A signal's value is shown by colour: ``ONE`` (high, true) and ``ZERO`` (low, false); ``live(w, v)`` recolours a wire.
"""

from __future__ import annotations

import numpy as np
from manim import (DOWN, LEFT, ORIGIN, PI, RIGHT, UP, Arc, ArcBetweenPoints, Circle, CubicBezier, Dot, Line,
                   Polygon, Rectangle, RoundedRectangle, VGroup, VMobject)

from explainer.style import C

WIRE = "#8B95A7"
ONE = C.CS_TRUE
ZERO = "#3A4352"
GATE_STROKE = "#D7DCE4"
GATE_FILL = "#151B26"


def _pin(mob, rel):
    """A pin at a fixed position relative to the mobject's bounding box: rel in [-1, 1]^2."""
    def at():
        c = mob.get_center()
        return c + np.array([rel[0] * mob.width / 2, rel[1] * mob.height / 2, 0])
    return at


class Gate(VGroup):
    """A logic gate symbol.  kind: AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF.  ``inp`` is a list of pin functions (top
    first), ``out`` the output pin function."""

    def __init__(self, kind="AND", n_inputs=2, size=1.0, stroke=GATE_STROKE, fill=GATE_FILL, stroke_width=3):
        super().__init__()
        kind = kind.upper()
        self.kind = kind
        h, w = 1.0 * size, 1.25 * size
        bubble = kind in ("NAND", "NOR", "NOT", "XNOR")
        base = kind.replace("N", "", 1) if kind in ("NAND", "NOR") else kind
        if kind in ("NOT", "BUF"):
            body = Polygon([-w * 0.42, h * 0.42, 0], [-w * 0.42, -h * 0.42, 0], [w * 0.36, 0, 0])
            n_inputs = 1
        elif base == "AND":
            body = VMobject()
            body.set_points_as_corners([[w * 0.0, h / 2, 0], [-w / 2, h / 2, 0], [-w / 2, -h / 2, 0], [0, -h / 2, 0]])
            arc = Arc(radius=h / 2, start_angle=-PI / 2, angle=PI).shift(RIGHT * 0)
            body.append_points(arc.points)
            body.add_line_to(np.array([0, h / 2, 0]))
        else:  # OR, XOR, XNOR
            body = VMobject()
            back = CubicBezier([-w / 2, h / 2, 0], [-w * 0.3, h * 0.25, 0], [-w * 0.3, -h * 0.25, 0],
                               [-w / 2, -h / 2, 0])
            lower = CubicBezier([-w / 2, -h / 2, 0], [-w * 0.05, -h / 2, 0], [w * 0.3, -h * 0.3, 0], [w / 2, 0, 0])
            upper = CubicBezier([w / 2, 0, 0], [w * 0.3, h * 0.3, 0], [-w * 0.05, h / 2, 0], [-w / 2, h / 2, 0])
            body.set_points(np.concatenate([back.reverse_points().points if False else back.points, lower.points,
                                            upper.points]))
            if base in ("XOR", "XNOR"):
                extra = CubicBezier([-w * 0.62, h / 2, 0], [-w * 0.42, h * 0.25, 0], [-w * 0.42, -h * 0.25, 0],
                                    [-w * 0.62, -h / 2, 0]).set_stroke(stroke, stroke_width)
                self.add(extra)
        body.set_stroke(stroke, stroke_width).set_fill(fill, 1)
        self.body = body
        self.add(body)
        tip = body.get_right()
        if bubble:
            b = Circle(radius=0.09 * size, stroke_color=stroke, stroke_width=stroke_width, fill_color=fill,
                       fill_opacity=1).move_to(tip + RIGHT * 0.09 * size)
            self.add(b)
            tip = b.get_right()
        lead = 0.28 * size
        x_in = -w / 2 if base != "XOR" and kind not in ("XOR", "XNOR") else -w * 0.62
        if kind in ("NOT", "BUF"):
            x_in = -w * 0.42
        ys = [0.0] if n_inputs == 1 else list(np.linspace(h * 0.28, -h * 0.28, n_inputs))
        self.leads = VGroup()
        for y in ys:
            x0 = x_in
            if base in ("OR", "XOR", "XNOR") and kind not in ("NOT", "BUF"):
                x0 = -w * 0.36 if base == "OR" else -w * 0.48
            self.leads.add(Line([x_in - lead, y, 0], [x0, y, 0], stroke_width=stroke_width * 0.8, color=WIRE))
        self.leads.add(Line(tip, tip + RIGHT * lead, stroke_width=stroke_width * 0.8, color=WIRE))
        self.add(self.leads)
        self._ys = ys
        self._tip = tip + RIGHT * lead
        self._xin = x_in - lead
        # pins as functions of the current position
        self.inp = [self._make_pin(i) for i in range(len(ys))]

    def _make_pin(self, i):
        def at():
            return self.leads[i].get_start()
        return at

    def out(self):
        return self.leads[-1].get_end()


def gate(kind="AND", n_inputs=2, size=1.0, **kw) -> Gate:
    return Gate(kind, n_inputs, size, **kw)


def wire(a, b, color=WIRE, stroke_width=3, via="h") -> VMobject:
    """An orthogonal wire from point a to point b: horizontal, vertical, horizontal (via="h") or vertical first."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if via == "h":
        xm = (a[0] + b[0]) / 2
        pts = [a, [xm, a[1], 0], [xm, b[1], 0], b]
    elif via == "v":
        pts = [a, [a[0], b[1], 0], b]
    else:  # "hv": horizontal then vertical
        pts = [a, [b[0], a[1], 0], b]
    m = VMobject(color=color, stroke_width=stroke_width)
    m.set_points_as_corners([np.asarray(p, float) for p in pts])
    return m


def live(m, value: int):
    """Recolour a wire (or any stroke) for the logic value it carries."""
    return m.animate.set_stroke(ONE if value else ZERO)


def junction(p, color=WIRE, r=0.06) -> Dot:
    return Dot(p, radius=r, color=color)


class Switch(VGroup):
    """A knife switch between two contacts: open or closed.  ``.left``, ``.right`` are the contacts."""

    def __init__(self, closed=False, length=1.2, color=GATE_STROKE):
        super().__init__()
        self.length = length
        self.a = Dot(LEFT * length / 2, radius=0.07, color=color)
        self.b = Dot(RIGHT * length / 2, radius=0.07, color=color)
        self.blade = Line(self.a.get_center(), self._blade_end(closed), color=color, stroke_width=4)
        self.closed = closed
        # an invisible mirror of the open blade keeps the bounding box centred on the contacts, so that move_to
        # puts the contacts (not the raised blade) where the wires are
        open_end = self._blade_end(False)
        mirror = Line(self.a.get_center(), [open_end[0], -open_end[1], 0], stroke_opacity=0)
        self.add(mirror, self.a, self.b, self.blade)

    def _blade_end(self, closed):
        if closed:
            return self.b.get_center()
        ang = 0.55
        return self.a.get_center() + self.length * np.array([np.cos(ang), np.sin(ang), 0])

    def left(self):
        return self.a.get_center()

    def right(self):
        return self.b.get_center()

    def set(self, closed: bool):
        from manim import Transform
        new = Line(self.a.get_center(), self._blade_end(closed), color=self.blade.get_color(), stroke_width=4)
        self.closed = closed
        return Transform(self.blade, new)


def switch(closed=False, length=1.2, **kw) -> Switch:
    return Switch(closed, length, **kw)


class Relay(VGroup):
    """An electromagnetic relay: a coil that, when energized, pulls an armature to close a contact."""

    def __init__(self, normally_open=True, scale=1.0):
        super().__init__()
        coil = VGroup(*[Arc(radius=0.12, start_angle=PI / 2, angle=-PI, stroke_width=3, color="#D9A15B").move_to(
            [0, 0.42 - 0.24 * k, 0]) for k in range(4)])
        core = Rectangle(width=0.18, height=1.1, stroke_width=0, fill_color="#5B6575", fill_opacity=1).move_to(
            LEFT * 0.12)
        self.coil = VGroup(core, coil).move_to(LEFT * 0.6)
        self.pivot = Dot(RIGHT * 0.05 + UP * 0.75, radius=0.06, color=GATE_STROKE)
        self.contact = Dot(RIGHT * 1.05 + DOWN * 0.15, radius=0.07, color=GATE_STROKE)
        self.normally_open = normally_open
        self.arm = Line(self.pivot.get_center(), self._arm_end(False), color=GATE_STROKE, stroke_width=5)
        self.add(self.coil, self.pivot, self.contact, self.arm)
        self.scale(scale)
        self.energized = False

    def _arm_end(self, energized):
        p = self.pivot.get_center()
        closed = energized if self.normally_open else not energized
        tgt = self.contact.get_center()
        if closed:
            return tgt
        return p + (tgt - p) * 0.92 + UP * 0.32 * self.contact.width / 0.14

    def energize(self, on: bool = True):
        from manim import AnimationGroup, Transform
        self.energized = on
        new = Line(self.pivot.get_center(), self._arm_end(on), color=GATE_STROKE, stroke_width=5)
        return AnimationGroup(Transform(self.arm, new), *[c.animate.set_stroke("#FFB347" if on else "#D9A15B")
                                                         for c in self.coil[1]])


class Transistor(VGroup):
    """A MOSFET symbol: gate on the left, drain on top, source at the bottom; pMOS has a bubble on the gate."""

    def __init__(self, kind="n", scale=1.0, color=GATE_STROKE):
        super().__init__()
        self.kind = kind
        ch = Line(UP * 0.45, DOWN * 0.45, color=color, stroke_width=4).shift(RIGHT * 0.1)
        g = Line(UP * 0.38, DOWN * 0.38, color=color, stroke_width=4).shift(LEFT * 0.08)
        d = VGroup(Line(ch.get_top() + DOWN * 0.08, ch.get_top() + DOWN * 0.08 + RIGHT * 0.4, color=color,
                        stroke_width=3),
                   Line(ch.get_top() + DOWN * 0.08 + RIGHT * 0.4, ch.get_top() + DOWN * 0.08 + RIGHT * 0.4 + UP * 0.45,
                        color=color, stroke_width=3))
        s = VGroup(Line(ch.get_bottom() + UP * 0.08, ch.get_bottom() + UP * 0.08 + RIGHT * 0.4, color=color,
                        stroke_width=3),
                   Line(ch.get_bottom() + UP * 0.08 + RIGHT * 0.4, ch.get_bottom() + UP * 0.08 + RIGHT * 0.4 + DOWN * 0.45,
                        color=color, stroke_width=3))
        lead_end = g.get_center() + LEFT * 0.45
        if kind == "p":
            bub = Circle(radius=0.08, stroke_color=color, stroke_width=3).move_to(g.get_center() + LEFT * 0.11)
            lead = Line(bub.get_left(), lead_end, color=color, stroke_width=3)
            self.add(bub)
        else:
            lead = Line(g.get_center(), lead_end, color=color, stroke_width=3)
        self.channel = ch
        self.add(ch, g, d, s, lead)
        self._d, self._s, self._g = d, s, lead
        self.scale(scale)

    def drain(self):
        return self._d[1].get_end()

    def source(self):
        return self._s[1].get_end()

    def gate_pin(self):
        return self._g.get_end()

    def conduct(self, on: bool):
        return self.channel.animate.set_stroke(ONE if on else GATE_STROKE, 6 if on else 4)


def nmos(scale=1.0, **kw) -> Transistor:
    return Transistor("n", scale, **kw)


def pmos(scale=1.0, **kw) -> Transistor:
    return Transistor("p", scale, **kw)


def rail(p, label_text="", width=1.4, color=GATE_STROKE):
    """A supply rail (a short horizontal bar) at p."""
    return Line(np.asarray(p) + LEFT * width / 2, np.asarray(p) + RIGHT * width / 2, color=color, stroke_width=4)


def ground(p, color=GATE_STROKE) -> VGroup:
    p = np.asarray(p, float)
    return VGroup(*[Line(p + DOWN * 0.1 * k + LEFT * (0.3 - 0.1 * k), p + DOWN * 0.1 * k + RIGHT * (0.3 - 0.1 * k),
                         color=color, stroke_width=3) for k in range(3)])


def lamp(on=False, radius=0.28) -> VGroup:
    """A lamp: a circle with a cross, lit or not."""
    c = Circle(radius=radius, stroke_color=GATE_STROKE, stroke_width=3,
               fill_color="#FFE08A" if on else GATE_FILL, fill_opacity=1)
    x = VGroup(Line(c.get_center() + np.array([-0.7, -0.7, 0]) * radius, c.get_center() + np.array([0.7, 0.7, 0]) * radius,
                    color=GATE_STROKE, stroke_width=2),
               Line(c.get_center() + np.array([-0.7, 0.7, 0]) * radius, c.get_center() + np.array([0.7, -0.7, 0]) * radius,
                    color=GATE_STROKE, stroke_width=2))
    g = VGroup(c, x)
    g.bulb = c
    return g


def light(l, on: bool):
    return l.bulb.animate.set_fill("#FFE08A" if on else GATE_FILL, 1)

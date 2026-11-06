"""Helpers shared by the scenes of Part 9 ("What Is Mathematics About?")."""

from __future__ import annotations

import re

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import mathphil as M  # noqa: F401
from explainer.philosophy.reasoner import types as T  # noqa: F401

from .compute import load  # noqa: F401

PART = 9
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
ABSTRACT = "#9DB4FF"   # abstract objects, the platonist's heaven
CONCRETE = "#E0B07A"   # the concrete world: eggs, cicadas, points
PROOF = "#7FE0C8"      # proofs as programs
NUM = "#FFD166"


def term_tex(s: str) -> str:
    """A lambda term (or type) as printed by the Reasoner, as TeX for MathTex."""
    out = s.replace(" ", r"\ ")
    for a, b in (("λ", r"\lambda{}"), ("⟨", r"\langle{}"), ("⟩", r"\rangle{}"), ("⇒", r"\Rightarrow{}"),
                 ("→", r"\to{}"), ("∧", r"\wedge{}"), ("∨", r"\vee{}"), ("¬", r"\lnot{}"), ("⊥", r"\bot{}"),
                 ("|", r"\mid{}")):
        out = out.replace(a, b)
    for w in ("fst", "snd", "inl", "inr", "case", "of", "abort"):
        out = re.sub(rf"\b{w}\b", lambda m: rf"\mathsf{{{m.group(0)}}}", out)
    return out


def term_mob(s: str, font_size=30, color=PROOF) -> MathTex:
    return MathTex(term_tex(s), font_size=font_size, color=color)


def nested_boxes(n: int, kind: str, unit=0.32, color=ABSTRACT) -> VGroup:
    """Zermelo's n (the set containing Zermelo's n - 1) or von Neumann's n (the set of all smaller numbers), as boxes
    inside boxes. The empty set is an empty box."""
    def zer(k):
        if k == 0:
            return Square(side_length=unit, stroke_color=color, stroke_width=2)
        inner = zer(k - 1)
        outer = SurroundingRectangle(inner, buff=0.12, corner_radius=0.05, stroke_color=color, stroke_width=2)
        return VGroup(outer, inner)

    def vn(k):
        if k == 0:
            return Square(side_length=unit, stroke_color=color, stroke_width=2)
        kids = VGroup(*[vn(j) for j in range(k)]).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        outer = SurroundingRectangle(kids, buff=0.12, corner_radius=0.05, stroke_color=color, stroke_width=2)
        return VGroup(outer, kids)
    return zer(n) if kind == "Z" else vn(n)


def project(p, ax=0.45, ay=0.3, s=1.0):
    """A simple oblique projection of a point in space to the screen."""
    x, y, z = p
    return np.array([s * (x + ax * z), s * (y + ay * z), 0.0])


def wire(points: dict, faces, scale=1.0, color=GREY_A, fill=None, ax=0.45, ay=0.3, width=2.5) -> VGroup:
    """A polyhedron (vertex coordinates and faces) drawn as a projected wireframe, centred on the origin."""
    es = {frozenset((f[k], f[(k + 1) % len(f)])) for f in faces for k in range(len(f))}
    g = VGroup()
    if fill:
        for f in faces:
            g.add(Polygon(*[project(points[v], ax, ay, scale) for v in f], stroke_width=0, fill_color=fill,
                          fill_opacity=0.12))
    for e in es:
        a, b = tuple(e)
        g.add(Line(project(points[a], ax, ay, scale), project(points[b], ax, ay, scale), color=color,
                   stroke_width=width))
    dots = VGroup(*[Dot(project(p, ax, ay, scale), radius=0.045, color=WHITE) for p in points.values()])
    g.add(dots)
    return g.move_to(ORIGIN)


# vertices 0..3 at the bottom, 4..7 above them, in the order the faces of mathphil.POLYHEDRA['cube'] use
CUBE_PTS = {0: (0, 0, 0), 1: (1, 0, 0), 2: (1, 1, 0), 3: (0, 1, 0), 4: (0, 0, 1), 5: (1, 0, 1), 6: (1, 1, 1),
            7: (0, 1, 1)}
TETRA_PTS = {0: (0, 0, 0), 1: (1.2, 0, 0), 2: (0.6, 0, 1.0), 3: (0.6, 1.0, 0.35)}
TWIN_PTS = {0: (0, 0, 0), 1: (-1.2, -0.2, 0), 2: (-0.6, -0.2, 1.0), 3: (-0.6, -1.1, 0.3), 4: (1.2, 0.2, 0),
            5: (0.6, 0.2, 1.0), 6: (0.6, 1.1, 0.3)}


def frame_pts() -> dict:
    o = [(0, 0), (3, 0), (3, 3), (0, 3)]
    i = [(1, 1), (2, 1), (2, 2), (1, 2)]
    pts = {}
    for h in (0, 1):
        for k in range(4):
            pts[("o", k, h)] = (o[k][0], h * 0.9, o[k][1])
            pts[("i", k, h)] = (i[k][0], h * 0.9, i[k][1])
    return pts


def circle_loop(turns: int, radius=1.4, color=PROOF, center=ORIGIN) -> VMobject:
    """A loop based at the circle's rightmost point that winds `turns` times, drawn as a gentle outward spiral just
    off the circle so each winding can be seen; zero turns is an excursion that goes out and comes back."""
    c = np.array(center, dtype=float)
    if turns == 0:
        def f(t):
            ang = 1.6 * np.sin(PI * t)
            r = radius + 0.18 + 0.25 * np.sin(PI * t)
            return c + r * np.array([np.cos(ang), np.sin(ang), 0])
    else:
        def f(t):
            ang = 2 * PI * turns * t
            r = radius + 0.15 + 0.16 * abs(turns) * t
            return c + r * np.array([np.cos(ang), np.sin(ang), 0])
    return ParametricFunction(f, t_range=[0, 1, 0.002], color=color, stroke_width=3)


def caption(text: str, font_size=24, color=GREY_A, buff=0.4) -> Mobject:
    return label(text, font_size=font_size, color=color).to_edge(DOWN, buff=buff)


def rows_at(pairs, x_left=-6.2, x_right=0.4, y0=1.6, dy=0.62, font_size=24, left_color=WHITE, right_color=GREY_A,
            math_left=False, left_size=None) -> VGroup:
    """Two aligned columns: a formula or name on the left, its gloss on the right."""
    g = VGroup()
    for i, (a, b) in enumerate(pairs):
        y = y0 - i * dy
        la = (MathTex(a, font_size=left_size or font_size + 6, color=left_color) if math_left
              else label(a, font_size=left_size or font_size, color=left_color))
        la.move_to([x_left, y, 0], aligned_edge=LEFT)
        lb = label(b, font_size=font_size - 2, color=right_color).move_to([x_right, y, 0], aligned_edge=LEFT)
        g.add(VGroup(la, lb))
    return g

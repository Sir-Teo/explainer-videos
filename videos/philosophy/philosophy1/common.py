"""Helpers shared by the scenes of Part 1 ("Calculemus")."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 1
TERM = P.CLAIM
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
S_C, M_C, P_C = "#6FB7FF", "#C3A6FF", "#FF9F68"   # the three terms of a syllogism


def venn3(radius=1.15, center=ORIGIN, names=("S", "M", "P"), colors=(S_C, M_C, P_C), font_size=34) -> VGroup:
    """Three circles; ``g.region(r)`` is the area of region r = (in S, in M, in P), as a filled shape to show."""
    offs = [np.array([-0.62, -0.42, 0]), np.array([0, 0.62, 0]), np.array([0.62, -0.42, 0])]
    circles = [Circle(radius=radius, stroke_color=c, stroke_width=3).move_to(np.asarray(center) + o * radius)
               for c, o in zip(colors, offs)]
    labels = VGroup()
    for c, o, n, col in zip(circles, offs, names, colors):
        labels.add(MathTex(n, font_size=font_size, color=col).move_to(c.get_center() + o * 1.25 + o / np.linalg.norm(o) * 0.25))
    g = VGroup(*circles, labels)
    g.circles, g.labels = circles, labels

    def region(r, color=GOAL, opacity=0.45):
        shape = None
        for inside, c in zip(r, circles):
            if inside:
                shape = c.copy() if shape is None else Intersection(shape, c)
        box = Square(radius * 6).move_to(center)
        if shape is None:
            shape = box
        for inside, c in zip(r, circles):
            if not inside:
                shape = Difference(shape, c)
        return shape.set_stroke(width=0).set_fill(color, opacity=opacity)

    g.region = region
    return g


def hexagram(bits, width=0.9, gap=0.14, color=WHITE, stroke=0.11) -> VGroup:
    """Six lines, the first bit at the top: a solid line for 1 (yang), a broken line for 0 (yin)."""
    g = VGroup()
    for i, b in enumerate(bits):
        y = -i * (stroke + gap)
        if b:
            g.add(Rectangle(width=width, height=stroke, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, y, 0]))
        else:
            w = width * 0.42
            g.add(Rectangle(width=w, height=stroke, stroke_width=0, fill_color=color, fill_opacity=1).move_to([-width / 2 + w / 2, y, 0]),
                  Rectangle(width=w, height=stroke, stroke_width=0, fill_color=color, fill_opacity=1).move_to([width / 2 - w / 2, y, 0]))
    return g.move_to(ORIGIN)


def wheel(letters, radius=2.0, color=CONN, font_size=30, center=ORIGIN) -> VGroup:
    ring = Circle(radius=radius, stroke_color=color, stroke_width=2.5)
    ring2 = Circle(radius=radius - 0.55, stroke_color=color, stroke_width=1.5, stroke_opacity=0.6)
    labs = VGroup()
    for i, L in enumerate(letters):
        ang = PI / 2 - TAU * i / len(letters)
        labs.add(MathTex(rf"\mathrm{{{L}}}", font_size=font_size, color=color).move_to(
            [(radius - 0.28) * np.cos(ang), (radius - 0.28) * np.sin(ang), 0]))
    g = VGroup(ring, ring2, labs).move_to(center)
    g.labs = labs
    return g


def bubble(who: str, text: str, color, font_size=26) -> VGroup:
    head = VGroup(Circle(radius=0.4, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15),
                  label(who, font_size=26, color=color))
    head[1].move_to(head[0])
    t = wrapped_label(text, 7.5, font_size, WHITE)
    box = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.36, corner_radius=0.16, stroke_color=color,
                           stroke_width=2, fill_color="#0B0F17", fill_opacity=0.95)
    t.move_to(box)
    b = VGroup(box, t).next_to(head, RIGHT, buff=0.3)
    return VGroup(head, b)

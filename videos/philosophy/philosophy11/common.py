"""Helpers shared by the scenes of Part 11 ("What Is Knowledge?")."""

from __future__ import annotations

import numpy as np

from explainer.philosophy.studio import *  # noqa: F403
from explainer.philosophy.reasoner import knowledge as Kn  # noqa: F401

from .compute import load  # noqa: F401

PART = 11
OK, BAD, GOAL, HIST, CONN = P.TRUE, P.FALSE, P.CONCL, P.HIST, P.RULE
BEL = "#9DB4FF"       # belief
JUST = "#E8C07D"      # justification, evidence
LUCK = "#F28EC2"      # luck
KNOW = "#5EE6D0"      # knowledge
SKEP = "#C3A6FF"      # the skeptic


def mark(ok: bool, font_size=30) -> Mobject:
    """A green tick or a red cross."""
    return MathTex(r"\checkmark" if ok else r"\times", font_size=font_size, color=OK if ok else BAD)


def check_rows(rows, font_size=24, buff=0.22, mark_x=None) -> VGroup:
    """Rows of (text, verdict), the verdicts lined up on the right. ``g.marks`` and ``g.texts``."""
    texts = VGroup(*[label(t, font_size=font_size, color=WHITE) for t, _ in rows]).arrange(DOWN, aligned_edge=LEFT,
                                                                                             buff=buff)
    x = mark_x if mark_x is not None else texts.get_right()[0] + 0.5
    marks = VGroup(*[mark(v, font_size + 6).move_to([x, t.get_y(), 0]) for t, (_, v) in zip(texts, rows)])
    g = VGroup(texts, marks)
    g.texts, g.marks = texts, marks
    return g


class SpheresView(VGroup):
    """Lewis's spheres, drawn: the actual world at the centre, every other world on a ring by its distance (one ring
    per distinct distance), green where p is true and red where it is false, with a white ring round the worlds
    where the subject believes p. ``self.dot[w]``, ``self.ring[d]``, ``self.name[w]``, ``self.pos[w]``."""

    def __init__(self, data: dict, p: str, center=ORIGIN, step=0.62, angles: dict | None = None, labels=True,
                 font_size=17, dot_r=0.13, names: dict | None = None):
        super().__init__()
        c = np.asarray(center, float)
        dists = sorted({w["dist"] for w in data["worlds"]})
        self.radius = {d: step * i for i, d in enumerate(dists)}
        self.ring = {}
        rings = VGroup()
        for d in dists[1:]:
            r = Circle(radius=self.radius[d], stroke_color=GREY_D, stroke_width=1.5).move_to(c)
            self.ring[d] = r
            rings.add(r)
        self.dot, self.name, self.pos, self.halo = {}, {}, {}, {}
        dots, labs, halos = VGroup(), VGroup(), VGroup()
        by_d = {}
        for w in data["worlds"]:
            by_d.setdefault(w["dist"], []).append(w)
        for d, ws in by_d.items():
            for i, w in enumerate(ws):
                if angles and w["name"] in angles:
                    a = angles[w["name"]]
                else:
                    a = PI / 2 + (i - (len(ws) - 1) / 2) * 0.9 + (0.35 if d % 2 else 0)
                pt = c + self.radius[d] * np.array([np.cos(a), np.sin(a), 0])
                self.pos[w["name"]] = pt
                col = OK if w["true"][p] else BAD
                dt = Dot(pt, radius=dot_r, color=col)
                self.dot[w["name"]] = dt
                dots.add(dt)
                if w["believes"][p]:
                    h = Circle(radius=dot_r + 0.07, stroke_color=WHITE, stroke_width=2.5).move_to(pt)
                    self.halo[w["name"]] = h
                    halos.add(h)
                if labels:
                    nm = (names or {}).get(w["name"], w["name"])
                    t = label(nm, font_size=font_size, color=GREY_A)
                    direction = (pt - c) / (np.linalg.norm(pt - c) or 1)
                    if np.linalg.norm(pt - c) < 1e-6:
                        direction = DOWN
                    t.next_to(dt, direction if abs(direction[1]) > 0.5 else (RIGHT if direction[0] > 0 else LEFT),
                              buff=0.12)
                    self.name[w["name"]] = t
                    labs.add(t)
        self.rings, self.dots, self.labs, self.halos = rings, dots, labs, halos
        self.center_pt = c
        self.add(rings, dots, halos, labs)

    def disc(self, d, color=KNOW, opacity=0.12) -> Circle:
        """The nearby worlds: everything within distance d, shaded."""
        r = self.radius[d] + 0.25
        return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color,
                      fill_opacity=opacity).move_to(self.center_pt)


def legend(font_size=18) -> VGroup:
    items = VGroup(
        VGroup(Dot(radius=0.09, color=OK), label(r"$p$ true", font_size=font_size, color=GREY_A)).arrange(RIGHT,
                                                                                                   buff=0.12),
        VGroup(Dot(radius=0.09, color=BAD), label(r"$p$ false", font_size=font_size, color=GREY_A)).arrange(
            RIGHT, buff=0.12),
        VGroup(Circle(radius=0.12, stroke_color=WHITE, stroke_width=2.5),
               label(r"believes $p$", font_size=font_size, color=GREY_A)).arrange(RIGHT, buff=0.12))
    return items.arrange(RIGHT, buff=0.45)


def clock(t_minutes: float, radius=1.0, color=WHITE, stopped=False) -> VGroup:
    """A clock face showing a time (minutes after midnight); ``g.hour``, ``g.minute``."""
    face = Circle(radius=radius, stroke_color=color, stroke_width=3)
    ticks = VGroup(*[Line(radius * 0.86 * np.array([np.cos(a), np.sin(a), 0]),
                          radius * np.array([np.cos(a), np.sin(a), 0]), color=color, stroke_width=2)
                     for a in [PI / 2 - TAU * k / 12 for k in range(12)]])
    h = (t_minutes / 60.0) % 12
    m = t_minutes % 60
    ah = PI / 2 - TAU * h / 12
    am = PI / 2 - TAU * m / 60
    hour = Line(ORIGIN, radius * 0.5 * np.array([np.cos(ah), np.sin(ah), 0]), color=color, stroke_width=5)
    minute = Line(ORIGIN, radius * 0.8 * np.array([np.cos(am), np.sin(am), 0]), color=color, stroke_width=3)
    g = VGroup(face, ticks, hour, minute, Dot(radius=0.05, color=color))
    if stopped:
        g.add(label(r"stopped", font_size=18, color=BAD).next_to(face, DOWN, buff=0.12))
    g.hour, g.minute, g.face = hour, minute, face
    return g


def barn(color=BAD, w=0.8, h=0.6, fill=0.5, fake=False) -> VGroup:
    """A barn front: walls, a gambrel roof and a door. A facade is drawn dashed, with no depth."""
    pts = [[-w / 2, 0, 0], [w / 2, 0, 0], [w / 2, h, 0], [w * 0.3, h * 1.45, 0], [0, h * 1.65, 0],
           [-w * 0.3, h * 1.45, 0], [-w / 2, h, 0]]
    body = Polygon(*pts, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    door = Rectangle(width=w * 0.32, height=h * 0.6, stroke_color=WHITE, stroke_width=1.5).move_to(
        [0, h * 0.3, 0])
    g = VGroup(body, door)
    if fake:
        prop_ = Line([w * 0.15, h * 0.2, 0], [w * 0.55, -0.02, 0], color=GREY_B, stroke_width=2)
        g.add(prop_)
    return g


def coins(n=10, color=JUST, r=0.09) -> VGroup:
    g = VGroup(*[Circle(radius=r, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=0.6)
                 for _ in range(n)])
    g.arrange_in_grid(rows=2, buff=0.05)
    return g


def person(name: str, color=WHITE, font_size=22, scale=1.0) -> VGroup:
    head = Circle(radius=0.22 * scale, stroke_color=color, stroke_width=3)
    body = Line(head.get_bottom(), head.get_bottom() + DOWN * 0.55 * scale, color=color, stroke_width=3)
    arms = Line(LEFT * 0.3 * scale, RIGHT * 0.3 * scale, color=color, stroke_width=3).move_to(
        body.get_center() + UP * 0.1 * scale)
    legs = VGroup(Line(body.get_end(), body.get_end() + np.array([-0.22, -0.4, 0]) * scale, color=color,
                       stroke_width=3),
                  Line(body.get_end(), body.get_end() + np.array([0.22, -0.4, 0]) * scale, color=color,
                       stroke_width=3))
    fig = VGroup(head, body, arms, legs)
    if not name:
        g = VGroup(fig)
        g.fig, g.lab = fig, None
        return g
    lab = label(name, font_size=font_size, color=color).next_to(fig, DOWN, buff=0.12)
    g = VGroup(fig, lab)
    g.fig, g.lab = fig, lab
    return g


def caption(text: str, font_size=24, color=GREY_A, buff=0.4) -> Mobject:
    return label(text, font_size=font_size, color=color).to_edge(DOWN, buff=buff)


def stack(lines, font_size=24, buff=0.22, width=None, aligned_edge=ORIGIN) -> VGroup:
    """Lines (text or (text, color)) stacked, each limited to ``width`` before arranging."""
    g = VGroup()
    for x in lines:
        t, c = (x, WHITE) if isinstance(x, str) else x
        m = label(t, font_size=font_size, color=c)
        if width and m.width > width:
            m.width = width
        g.add(m)
    return g.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)

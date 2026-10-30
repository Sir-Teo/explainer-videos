from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, PART, VALUE


def warp(p):
    x, y = p[0], p[1]
    return np.array([x + 0.45 * math.sin(1.1 * y), y + 0.45 * math.sin(1.1 * x), 0.0])


def jac(x, y):
    return np.array([[1.0, 0.495 * math.cos(1.1 * y)], [0.495 * math.cos(1.1 * x), 1.0]])


def grid_lines(lo, hi, n, f, steps=30, color=BLUE_C, width=2.0):
    """The lines x = const and y = const of a square [lo, hi]^2, n of each, mapped by f."""
    g = VGroup()
    for t in np.linspace(lo, hi, n):
        for horiz in (True, False):
            pts = [f(np.array([s, t]) if horiz else np.array([t, s])) for s in np.linspace(lo, hi, steps)]
            g.add(VMobject(color=color, stroke_width=width).set_points_smoothly(pts))
    return g


class Jacobian(VoiceoverScene):
    def construct(self):
        self.card()
        self.bend()
        self.det_and_chain()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Maps that bend: the Jacobian", r"What does a curved map look like up close?", part=PART)
        with self.voiceover("Chapter three. Maps that bend."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def bend(self):
        pl = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1], background_line_style={"stroke_color": BLUE_D,
                         "stroke_width": 1.5, "stroke_opacity": 0.7}, faded_line_ratio=1)
        pl.prepare_for_nonlinear_transform()
        p0 = np.array([1.2, 0.6])
        P = warp(p0)
        J = jac(*p0)
        c = np.array([4.0, -1.0, 0])
        R = 2.2
        lens = Circle(radius=R, color=WHITE, stroke_width=3).move_to(c)
        lens_bg = Circle(radius=R, stroke_width=0, fill_color=BACKGROUND, fill_opacity=1).move_to(c)
        r = ValueTracker(1.6)

        def inset():
            rr = r.get_value()
            k = R * 0.62 / rr

            def curved(q):
                return c + k * (warp(p0 + q) - P)

            def straight(q):
                return c + k * np.array([*(J @ q), 0])

            return VGroup(grid_lines(-rr, rr, 7, curved, color=BLUE_C, width=3),
                          grid_lines(-rr, rr, 7, straight, color=GRAD, width=2).set_opacity(0.8))

        ins = always_redraw(inset)
        spot = always_redraw(lambda: Circle(radius=r.get_value() * 1.25, color=WHITE, stroke_width=2).move_to(P))
        dot = glow_dot(P, color=WHITE, radius=0.07, layers=3)
        Jt = MathTex(r"J = \begin{bmatrix} \partial f_1/\partial x & \partial f_1/\partial y \\ \partial f_2/\partial x & "
                     r"\partial f_2/\partial y \end{bmatrix}", font_size=36, color=GRAD).to_corner(UL, buff=0.45)
        Jb = BackgroundRectangle(Jt, color=BACKGROUND, fill_opacity=0.9, buff=0.12)
        key = VGroup(label(r"the map", font_size=24, color=BLUE_C), label(r"its Jacobian", font_size=24, color=GRAD))
        key.arrange(RIGHT, buff=0.5).next_to(lens, DOWN, buff=0.15)
        tag = label(r"illustrative map", font_size=22, color=GREY_B).to_corner(DL, buff=0.35)
        with self.voiceover(
            "Now let a function take a whole vector to another vector, the way a layer of a network does. "
            "<bookmark mark='a'/> Here's one that bends the plane: the grid lines curve. <bookmark mark='b'/> But zoom "
            "in close to any point, and the curves straighten out. Up close, every smooth map looks like a matrix: "
            "its Jacobian, the table of all its partial derivatives."
        ) as vo:
            self.play(Create(pl, lag_ratio=0.05), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(pl.animate.apply_function(warp), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(dot), Create(spot), FadeIn(lens_bg), Create(lens), FadeIn(ins), FadeIn(key))
            self.play(r.animate.set_value(0.08), run_time=4.0, rate_func=smooth)
            self.play(FadeIn(Jb), Write(Jt))
        ins.clear_updaters()
        spot.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def det_and_chain(self):
        p0 = np.array([1.2, 0.6])
        J = jac(*p0)
        det = float(np.linalg.det(J))
        dc = definition_card(
            r"the Jacobian",
            r"For $f: \mathbb{R}^n \to \mathbb{R}^m$, the $m \times n$ matrix of partial derivatives, $J_{ij} = "
            r"\partial f_i / \partial x_j$: the one matrix with $f(x + h) = f(x) + J\,h + o(\|h\|)$. \ A gradient is the "
            r"Jacobian of a function with one output, stood up as a column.", width=12.6, font_size=26)
        dc.to_edge(UP, buff=0.3)
        sq = Square(side_length=1.4, stroke_width=0, fill_color=VALUE, fill_opacity=0.5).move_to([-5.0, -1.4, 0])
        par = Polygon(*[np.array([*(J @ v), 0]) * 1.4 + np.array([-1.9, -1.4, 0]) for v in
                        (np.array([-0.5, -0.5]), np.array([0.5, -0.5]), np.array([0.5, 0.5]), np.array([-0.5, 0.5]))],
                      stroke_width=0, fill_color=GRAD, fill_opacity=0.55)
        arrow_ = Arrow([-4.1, -1.4, 0], [-3.1, -1.4, 0], color=GREY_B, stroke_width=4)
        dl = MathTex(rf"\text{{area}} \times \det J = {det:.2f}", font_size=34, color=GRAD).move_to([-3.4, -3.0, 0])
        colors = {r"J_{f \circ g}(x)": WHITE, r"J_f(g(x))": GRAD, r"J_g(x)": VALUE}
        chain = cmath(r"J_{f \circ g}(x)", "=", r"J_f(g(x))", r"\,", r"J_g(x)", colors=colors, font_size=44)
        chain.move_to([3.4, -1.55, 0])
        cw = label(r"one map after another: \\ multiply their Jacobians", font_size=26, color=GREY_A).next_to(chain, DOWN, buff=0.3)
        shapes = label(r"$(m \times k)\,(k \times n)$: \ the shapes chain like the maps", font_size=22, color=GREY_B)
        shapes.next_to(cw, DOWN, buff=0.3)
        cells = VGroup(*[Square(side_length=0.36, stroke_color=GRAD, stroke_width=1.5, fill_color=GRAD, fill_opacity=0.15)
                         for _ in range(15)]).arrange_in_grid(rows=3, cols=5, buff=0)
        cells.move_to([3.2, 0.15, 0])
        rb = Brace(cells, LEFT, color=GREY_B)
        rl = label(r"$m$ outputs", font_size=22, color=GREY_A).next_to(rb, LEFT, buff=0.1)
        cb = Brace(cells, UP, color=GREY_B)
        cl_ = label(r"$n$ inputs", font_size=22, color=GREY_A).next_to(cb, UP, buff=0.08)
        jij = MathTex(r"J_{ij}", font_size=24, color=GRAD).move_to(cells[7])
        shape_pic = VGroup(cells, rb, rl, cb, cl_, jij)
        with self.voiceover(
            "In general, a map from n numbers to m numbers has an m by n Jacobian: one row per output, one column "
            "per input, the one matrix that makes the straight-line guess best. A gradient is the special case of a "
            "single output. <bookmark mark='a'/> The Jacobian's determinant, from part three, says how much the "
            "map stretches area near the point. <bookmark mark='b'/> And the chain rule for maps is matrix "
            "multiplication: the Jacobian of one map after another is the product of their Jacobians, each taken "
            "where its input lands. That product is the whole of backpropagation, as chapter five will show."
        ) as vo:
            self.play(FadeIn(dc, shift=UP * 0.2))
            self.play(FadeIn(shape_pic), FadeIn(sq), GrowArrow(arrow_))
            vo.wait_until("a")
            self.play(TransformFromCopy(sq, par), FadeIn(dl))
            vo.wait_until("b")
            self.play(Write(chain))
            self.play(FadeIn(cw), FadeIn(shapes))
        self.wait(0.3)
        self.clear_scene()

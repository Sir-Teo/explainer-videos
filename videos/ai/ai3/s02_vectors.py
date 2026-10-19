from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import I_COLOR, J_COLOR, arrow, load, plane


class Vectors(VoiceoverScene):
    def construct(self):
        self.card()
        self.arrows()
        self.two_moves()
        self.basis()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Arrows and lists of numbers", r"What is a vector?", part=3)
        with self.voiceover("Chapter one. Vectors."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def arrows(self):
        pl = plane()
        v = np.array([3.0, 2.0, 0])
        a = arrow(v, color=C.BITS)
        dx = DashedLine(ORIGIN, [3, 0, 0], color=I_COLOR, stroke_width=4)
        dy = DashedLine([3, 0, 0], v, color=J_COLOR, stroke_width=4)
        col = Matrix([["3"], ["2"]], bracket_h_buff=0.12).scale(0.9).next_to(v, UR, buff=0.15)
        col.get_entries()[0].set_color(I_COLOR)
        col.get_entries()[1].set_color(J_COLOR)
        bg = BackgroundRectangle(col, color=BACKGROUND, fill_opacity=0.85, buff=0.1)
        three = Matrix([["3"], ["2"], ["1"]], bracket_h_buff=0.12).scale(0.9).move_to(col)
        g = load("gpt2")
        bar = np.asarray(g["barcodes"])[0][:12]
        many = MathTex(r"\begin{bmatrix}" + r" \\ ".join(f"{x:+.2f}" for x in bar[:5]) + r" \\ \vdots \\ "
                       + f"{bar[-1]:+.2f}" + r"\end{bmatrix}", font_size=30).move_to(col)
        if many.get_top()[1] > 3.7:  # keep the tall column on screen
            many.shift(DOWN * (many.get_top()[1] - 3.7))
        n768 = label(r"$768$ numbers: \ GPT-2's \texttt{dog}", font_size=26, color=GREY_A).next_to(many, DOWN, buff=0.15)
        with self.voiceover(
            "A vector is an arrow from the origin, <bookmark mark='a'/> or, just as well, a list of numbers: how far "
            "to go along each axis. <bookmark mark='b'/> Two numbers in the plane, three in space, and 768 in GPT-2."
        ) as vo:
            self.play(Create(pl, lag_ratio=0.05), run_time=1.5)
            self.play(GrowArrow(a))
            vo.wait_until("a")
            self.play(Create(dx), Create(dy))
            self.play(FadeIn(bg), Write(col))
            vo.wait_until("b")
            self.play(ReplacementTransform(col, three))
            self.play(ReplacementTransform(three, many), FadeIn(n768), bg.animate.stretch_to_fit_height(4.2).move_to(many))
        self.wait(0.3)
        self.play(FadeOut(VGroup(dx, dy, many, n768, bg, a)))
        self.pl = pl

    # ------------------------------------------------------------------
    def two_moves(self):
        u, w = np.array([2.0, 1.0, 0]), np.array([-1.0, 2.0, 0])
        au, aw = arrow(u, color=I_COLOR), arrow(w, color=J_COLOR)
        lu = MathTex(r"\mathbf{u}", font_size=40, color=I_COLOR).next_to(u, DOWN + RIGHT, buff=0.1)
        lw = MathTex(r"\mathbf{v}", font_size=40, color=J_COLOR).next_to(w, LEFT, buff=0.15)
        aw2 = arrow(u + w, start=u, color=J_COLOR)
        s = arrow(u + w, color=C.BITS)
        ls = MathTex(r"\mathbf{u} + \mathbf{v}", font_size=40, color=C.BITS).next_to(u + w, UP, buff=0.15)
        para = Polygon(ORIGIN, u, u + w, w, stroke_width=0, fill_color=C.BITS, fill_opacity=0.12)
        k = ValueTracker(1.0)
        base = np.array([3.5, -2.2, 0])
        sc = always_redraw(lambda: arrow(base + u * k.get_value(), start=base, color=I_COLOR))
        kl = always_redraw(lambda: MathTex(rf"{k.get_value():.1f}\,\mathbf{{u}}", font_size=36, color=I_COLOR)
                           .next_to(base + u * k.get_value(), RIGHT, buff=0.15))
        with self.voiceover(
            "Two moves make all of linear algebra. <bookmark mark='a'/> Add two vectors: walk along one, then along "
            "the other. <bookmark mark='b'/> And scale a vector: stretch it, shrink it, or flip it around."
        ) as vo:
            self.play(GrowArrow(au), GrowArrow(aw), FadeIn(lu), FadeIn(lw))
            vo.wait_until("a")
            self.play(TransformFromCopy(aw, aw2), run_time=1.2)
            self.play(GrowArrow(s), FadeIn(ls), FadeIn(para))
            vo.wait_until("b")
            self.add(sc, kl)
            for v in (2.0, 0.5, -1.0, 1.0):
                self.play(k.animate.set_value(v), run_time=0.9)
        sc.clear_updaters()
        kl.clear_updaters()
        self.wait(0.3)
        self.play(FadeOut(VGroup(aw2, s, ls, para, sc, kl)))
        self.u, self.w, self.au, self.aw, self.lu, self.lw = u, w, au, aw, lu, lw

    # ------------------------------------------------------------------
    def basis(self):
        u, w = self.u, self.w
        a, b = ValueTracker(1.0), ValueTracker(1.0)
        comb = always_redraw(lambda: arrow(a.get_value() * u + b.get_value() * w, color=C.BITS))
        tip = always_redraw(lambda: glow_dot(a.get_value() * u + b.get_value() * w, color=C.BITS, radius=0.07, layers=3))
        trail = TracedPath(lambda: a.get_value() * u + b.get_value() * w, stroke_color=C.BITS, stroke_width=2,
                           stroke_opacity=0.6)
        read = always_redraw(lambda: MathTex(rf"{a.get_value():+.1f}\,\mathbf{{u}} {b.get_value():+.1f}\,\mathbf{{v}}",
                                             font_size=36, color=C.BITS).to_corner(UL, buff=0.5)
                             .add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1))
        M = np.array([[u[0], w[0]], [u[1], w[1]]])
        skew = plane(x_range=(-12, 12), y_range=(-12, 12))
        skew.set_color(C.BITS).set_opacity(0.0)
        with self.voiceover(
            "Mix the two moves: a times u, plus b times v. <bookmark mark='a'/> As a and b vary, the tip sweeps out "
            "the whole plane. <bookmark mark='b'/> u and v are then a basis: every vector has exactly one pair of "
            "coordinates in it. The usual axes are just the most familiar basis."
        ) as vo:
            self.add(trail, comb, tip, read)
            vo.wait_until("a")
            for va, vb in ((2.0, -1.0), (-1.5, -1.5), (-2.0, 1.5), (1.5, 1.8), (0.5, 0.0)):
                self.play(a.animate.set_value(va), b.animate.set_value(vb), run_time=1.0)
            vo.wait_until("b")
            self.add(skew)
            self.play(skew.animate.set_opacity(0.45), run_time=0.3)
            self.play(ApplyMatrix(M, skew), run_time=2.0)
        for m in (comb, tip, read):
            m.clear_updaters()
        trail.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

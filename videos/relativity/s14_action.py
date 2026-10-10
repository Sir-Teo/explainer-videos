from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import redraw, boxed, label, ladder, mtex, note, stack


class Action(VoiceoverScene):
    def construct(self):
        self.intro()
        self.volume()
        self.vary()
        self.lovelock()

    # ------------------------------------------------------------------
    def intro(self):
        top = label(r"David Hilbert, G\"ottingen, 20 November 1915: the variational route", font_size=32,
                    color=GREY_A).to_edge(UP, buff=0.45)
        part = mtex(r"\text{a particle:}\quad", r"S = -mc^2\!\int d\tau", font_size=40)
        part[1].set_color(C.PROPER_TIME)
        field = mtex(r"\text{a field:}\quad", r"S = \int \mathcal L\,\sqrt{-g}\;d^4x", font_size=40)
        VGroup(part, field).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(top, DOWN, buff=0.6)
        which = label(r"Which scalar can we build from $g_{\mu\nu}$ with at most two derivatives?", font_size=32)
        which.next_to(field, DOWN, buff=0.7)
        ans = mtex(r"\mathcal L", r"\;\propto\;", r"R", r"\ -\ 2\Lambda", font_size=48)
        ans[2].set_color(C.CURVATURE)
        ans[3].set_color(C.LAMBDA)
        ans.next_to(which, DOWN, buff=0.4)
        S = mtex(r"S", r"=", r"\frac{c^4}{16\pi G}\int \big(R - 2\Lambda\big)\sqrt{-g}\;d^4x", r"+", r"S_{\text{matter}}",
                 font_size=46)
        S[2].set_color(C.CURVATURE)
        S[4].set_color(C.MATTER)
        Sb = boxed(S, color=C.CURVATURE, buff=0.25).to_edge(DOWN, buff=0.5)
        Sl = label(r"the Einstein--Hilbert action", font_size=26, color=C.CURVATURE).next_to(Sb, UP, buff=0.1)
        with self.voiceover(
            "There's a second road to the same equation. David Hilbert took it, in a paper he submitted five days before "
            "Einstein presented his final version. <bookmark mark='p'/> We saw that a free particle moves so as to make its "
            "proper time, its action, stationary. <bookmark mark='f'/> A field's action is an integral over all of "
            "spacetime of a scalar Lagrangian, weighted by the square root of minus the determinant of the metric. "
            "<bookmark mark='w'/> So which scalar should the gravitational field use? It has to be built from the metric "
            "with at most two derivatives. <bookmark mark='r'/> Apart from a constant, there's essentially one choice: the "
            "Ricci scalar. <bookmark mark='s'/> This is the Einstein–Hilbert action. The constant in front is chosen so "
            "that Newton comes out right."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("p")
            self.play(FadeIn(part))
            vo.wait_until("f")
            self.play(FadeIn(field))
            vo.wait_until("w")
            self.play(FadeIn(which))
            vo.wait_until("r")
            self.play(Write(ans))
            vo.wait_until("s")
            self.play(Write(S), Create(Sb[0]), FadeIn(Sl))
        self.clear_scene()

    # ------------------------------------------------------------------
    def volume(self):
        P0 = np.array([-5.2, -2.2, 0])
        e1 = np.array([2.7, 0.0, 0])
        tilt = ValueTracker(0.0)

        def e2():
            a = tilt.get_value()
            return np.array([1.3 * a, 2.4 + 0.5 * a, 0])

        def cell():
            v = e2()
            poly = Polygon(P0, P0 + e1, P0 + e1 + v, P0 + v, stroke_color=C.METRIC, stroke_width=3, fill_color=C.METRIC,
                           fill_opacity=0.25)
            a1 = Arrow(P0, P0 + e1, buff=0, color=GREY_A, stroke_width=5, max_tip_length_to_length_ratio=0.15)
            a2 = Arrow(P0, P0 + v, buff=0, color=GREY_A, stroke_width=5, max_tip_length_to_length_ratio=0.15)
            return VGroup(poly, a1, a2)

        cm = redraw(cell)
        heads = MathTex(r"\text{area} = \sqrt{\det g}\;dx^1dx^2 =", font_size=34)
        heads.move_to([-3.0, 2.6, 0])
        val = DecimalNumber(2.7 * 2.4, num_decimal_places=2, font_size=34)
        val.add_updater(lambda m: m.set_value(abs(np.cross(e1, e2())[2])).next_to(heads, RIGHT, buff=0.15))
        val.update()  # waits freeze frames when no updater is time-based
        rows = stack(
            mtex(r"\delta\det g", r"=", r"\det g\; g^{\mu\nu}\,\delta g_{\mu\nu}", font_size=38),
            mtex(r"\delta\sqrt{-g}", r"=", r"-\tfrac12\sqrt{-g}\;g_{\mu\nu}\,\delta g^{\mu\nu}", font_size=38),
            buff=0.5,
        )
        rows.move_to([3.2, 0.2, 0])
        rows[1][0].set_color(C.METRIC)
        whys = VGroup(note(r"Jacobi's formula", font_size=24).next_to(rows[0], UP, buff=0.15),
                      note(r"using $g^{\mu\nu}\delta g_{\mu\nu} = -g_{\mu\nu}\delta g^{\mu\nu}$", font_size=24)
                      .next_to(rows[1], DOWN, buff=0.15))
        with self.voiceover(
            "First, that square root. <bookmark mark='c'/> A coordinate cell is a little parallelogram spanned by the "
            "basis vectors, and its true area is the square root of the determinant of the metric, times the coordinate "
            "steps. <bookmark mark='t'/> Change the metric, and the area changes. So the square root of minus g times d "
            "four x is the true four-dimensional volume, the same in every coordinate system. <bookmark mark='j'/> We'll "
            "need how it responds to a small change in the metric. Jacobi's formula for the derivative of a determinant "
            "gives it: <bookmark mark='k'/> the variation of root minus g is minus one half root minus g, g mu nu, delta "
            "g upper mu nu."
        ) as vo:
            vo.wait_until("c")
            self.add(cm)
            self.play(FadeIn(heads))
            self.add(val)
            vo.wait_until("t")
            self.play(tilt.animate.set_value(1.0), run_time=2)
            self.play(tilt.animate.set_value(-0.6), run_time=2)
            vo.wait_until("j")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("k")
            self.play(Write(rows[1]), FadeIn(whys[1]))
        cm.clear_updaters()
        val.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def vary(self):
        title = label(r"Varying the action", font_size=36).to_corner(UL, buff=0.4)
        rows = [
            mtex(r"\delta S_H", r"=", r"\frac{c^4}{16\pi G}\int\Big[\delta\big(\sqrt{-g}\big)R + \sqrt{-g}\;\delta\big(g^{\mu\nu}R_{\mu\nu}\big)\Big]d^4x",
                 font_size=34),
            mtex(r"\delta S_H", r"=", r"\frac{c^4}{16\pi G}\int\sqrt{-g}\Big[R_{\mu\nu} - \tfrac12 R\,g_{\mu\nu}\Big]\delta g^{\mu\nu}\,d^4x",
                 r"+", r"\frac{c^4}{16\pi G}\int\sqrt{-g}\;g^{\mu\nu}\delta R_{\mu\nu}\,d^4x", font_size=34),
            mtex(r"\delta S_H", r"=", r"\frac{c^4}{16\pi G}\int\sqrt{-g}\;G_{\mu\nu}\,\delta g^{\mu\nu}\,d^4x", font_size=34),
            mtex(r"\delta S_M", r"=", r"-\tfrac12\int\sqrt{-g}\;T_{\mu\nu}\,\delta g^{\mu\nu}\,d^4x", font_size=34),
            mtex(r"0", r"=", r"\frac{c^4}{16\pi G}\,G_{\mu\nu} - \tfrac12\,T_{\mu\nu}", font_size=38),
            mtex(r"G_{\mu\nu}", r"=", r"\frac{8\pi G}{c^4}\,T_{\mu\nu}", font_size=48),
        ]
        whys = [
            note(r"(set $\Lambda = 0$ for now)", font_size=22),
            note(r"$\delta\sqrt{-g}$ from Jacobi", font_size=22),
            note(r"Palatini: the last term is a total divergence", font_size=22),
            note(r"this \emph{defines} $T_{\mu\nu}$", font_size=22),
            note(r"$\delta S = 0$ for every $\delta g^{\mu\nu}$", font_size=22),
            None,
        ]
        rows[1][4].set_color(GREY_B)
        rows[2][2].set_color(C.CURVATURE)
        rows[3][2].set_color(C.MATTER)
        rows[5][0].set_color(C.CURVATURE)
        rows[5][2].set_color(C.MATTER)
        x0 = -2.2
        for r, w in zip(rows, whys):
            r.shift((x0 - r[1].get_center()[0]) * RIGHT)
            if w is not None:
                w.next_to(r, DOWN, buff=0.08).align_to(r, RIGHT)
        step = ladder(self, rows, whys, keep=4, top=2.4, x=x0, buff=0.75)
        pal = VGroup(
            mtex(r"\delta R^\rho{}_{\sigma\mu\nu} = \nabla_\mu\,\delta\Gamma^\rho{}_{\nu\sigma} - \nabla_\nu\,\delta\Gamma^\rho{}_{\mu\sigma}",
                 font_size=32),
            mtex(r"\Rightarrow\ g^{\mu\nu}\delta R_{\mu\nu} = \nabla_\sigma\big(g^{\mu\nu}\delta\Gamma^\sigma{}_{\mu\nu} - "
                 r"g^{\mu\sigma}\delta\Gamma^\lambda{}_{\lambda\mu}\big)", font_size=32),
            label(r"a divergence integrates to the boundary, where $\delta g = 0$: it drops out", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now vary the metric. <bookmark mark='a'/> Two things change: the volume factor, and the Ricci scalar, which "
            "is the inverse metric times Ricci. <bookmark mark='b'/> The volume factor gives minus one half R g mu nu. "
            "Varying the inverse metric in R gives R mu nu. And there's a leftover piece, the variation of Ricci itself."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
        with self.voiceover(
            "<bookmark mark='p'/> That leftover is harmless. The variation of the Riemann tensor is a difference of "
            "covariant derivatives of the variation of gamma, the Palatini identity, so the leftover term is a total "
            "divergence. It integrates to the boundary of the region, where we hold the metric fixed, and drops out. "
            "<bookmark mark='c'/> What survives is the Einstein tensor, times the variation of the metric. It appears "
            "here by itself: nobody had to guess the one half."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(pal, lag_ratio=0.3), run_time=2)
            vo.wait_until("c")
            self.play(FadeOut(pal))
            step(2)
        with self.voiceover(
            "<bookmark mark='m'/> For the matter, the response of its action to a change in the metric is what defines "
            "the stress–energy tensor. <bookmark mark='z'/> The total action is stationary for every possible variation "
            "of the metric only if the bracket vanishes: <bookmark mark='e'/> G mu nu equals eight pi G over c to the fourth "
            "times T mu nu. The same equation, from one line of input."
        ) as vo:
            vo.wait_until("m")
            step(3)
            vo.wait_until("z")
            step(4)
            vo.wait_until("e")
            step(5)
            self.play(Circumscribe(rows[5], color=C.CURVATURE))
        self.clear_scene()

    # ------------------------------------------------------------------
    def lovelock(self):
        thm = VGroup(
            label(r"Lovelock's theorem (1971)", font_size=36, color=C.CURVATURE),
            label(r"In four dimensions, the only symmetric, divergence-free tensors", font_size=30),
            label(r"built from $g_{\mu\nu}$ and its first two derivatives are", font_size=30),
            mtex(r"a\,G_{\mu\nu} + b\,g_{\mu\nu}", font_size=46),
        ).arrange(DOWN, buff=0.25).move_to(UP * 1.2)
        thm[3].set_color(C.CURVATURE)
        concl = label(r"Given the requirements, Einstein's equation is not a guess: it is the only option.",
                      font_size=30, color=GREY_A).next_to(thm, DOWN, buff=0.7)
        noether = label(r"(and invariance of $S_{\text{matter}}$ under coordinate changes gives $\nabla_\mu T^{\mu\nu} = 0$ "
                        r"automatically)", font_size=26, color=GREY_A).next_to(concl, DOWN, buff=0.35)
        hist = label(r"Hilbert submitted his paper on 20 November 1915; Einstein presented his equations on 25 November.",
                     font_size=24, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Two routes, one destination. And in 1971, David Lovelock proved that this isn't a coincidence. "
            "<bookmark mark='t'/> In four dimensions, the only symmetric, divergence-free tensors you can build from the "
            "metric and its first two derivatives are combinations of the Einstein tensor and the metric itself. "
            "<bookmark mark='c'/> So once you accept the requirements, Einstein's equation isn't a guess. It's the only "
            "possibility. <bookmark mark='n'/> Even energy conservation comes for free from the action: it follows from "
            "the fact that the action doesn't care about coordinates. <bookmark mark='h'/> As for priority: Hilbert "
            "submitted his variational paper on the twentieth of November; Einstein presented his equations on the "
            "twenty-fifth. The physical ideas that led there were Einstein's, built over eight years."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm, lag_ratio=0.2), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(concl))
            vo.wait_until("n")
            self.play(FadeIn(noether))
            vo.wait_until("h")
            self.play(FadeIn(hist))
        self.clear_scene()

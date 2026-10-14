from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import square_axes


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.ledger_row()
        self.next_time()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        items = [
            (r"outer measure: \ the cheapest countable cover; \ $\mathbb Q$ and the Cantor set have measure $0$",
             C.MEASURE),
            (r"Vitali: \ not every set can have a length", C.PATHOLOGY),
            (r"$\sigma$-algebras; \ measurable functions; \ limits are free", C.SEQ),
            (r"measures: \ countably additive, \ continuous along monotone sequences", C.MEASURE),
            (r"the integral as a supremum over simple functions; \ monotone convergence", C.FUNC),
            (r"Fatou: \ mass can escape in the limit, \ never appear", C.CONNECTED_SET),
            (r"dominated convergence: \ a lid is all you need", C.EPS),
            (r"Riesz: \ every positive functional on $C_c$ is an integral", C.FUNCTIONAL),
            (r"Lebesgue measure; \ Riemann integrable $\iff$ continuous a.e.", C.SEQ),
            (r"Lusin: \ measurable is nearly continuous", C.APPROX),
            (r"Fubini--Tonelli, \ and the function whose two integrals disagree", C.CLOSED_SET),
            (r"convolution; \ the sawtooth integrated term by term; \ the layer cake", C.MEASURE),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(DOWN * 0.3)
        head = label(r"Part 5, in twelve lines", font_size=40).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Let's take stock. Lebesgue gave lengths to sets by covering them as cheaply as possible, and Vitali "
            "showed that some sets must be left out. The sets that remain form a sigma-algebra, and measurable "
            "functions are closed under limits. The integral is a supremum over simple functions, and three limit "
            "theorems govern it: monotone convergence, Fatou's lemma, and dominated convergence, which needs only a "
            "lid. Riesz showed that measures come from positive functionals; Lebesgue measure comes from Riemann's "
            "integral, and agrees with it whenever Riemann's exists. Measurable functions are nearly continuous; "
            "Fubini lets us integrate in either order, when the absolute value is integrable; and the sawtooth can "
            "finally be integrated term by term."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger_row(self):
        before = ledger(filled=4, highlight=5).scale(0.95)
        after = ledger(filled=5, highlight=5).scale(0.95)
        with self.voiceover(
            "The ledger's fifth row. <bookmark mark='a'/> The space: a set with a sigma-algebra and a measure. <bookmark mark='c2'/> Its "
            "completeness theorem belongs to the next part. <bookmark mark='c3'/> Lebesgue measure is regular, approximated by compact sets "
            "from inside. <bookmark mark='c4'/> The swap: the limit of the integrals is the integral of the limit, under a lid. <bookmark mark='c5'/> And "
            "Fourier's series may now be integrated term by term."
        ) as vo:
            self.play(FadeIn(before))
            vo.wait_until("a")
            self.play(FadeOut(before.rows[4]), *[TransformFromCopy(after.rows[4][i], after.rows[4][i]) for i in (0, 1)],
                      Indicate(before.head[1], color=C.EPS), run_time=1.5)
            for k_ in range(2, len(after.rows[4])):  # each cell arrives with its sentence
                vo.wait_until(f"c{k_}")
                self.play(TransformFromCopy(after.rows[4][k_], after.rows[4][k_]),
                          Indicate(before.head[k_], color=C.EPS), run_time=1.2)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: Part 6, \ $L^p$ and Hilbert space", font_size=38).to_edge(UP, buff=0.3)
        ax = square_axes([-1.4, 1.4, 1], [-1.4, 1.4, 1], 1.9).move_to([-3.4, -0.45, 0])
        pT = ValueTracker(1.0)

        def ball():
            p = pT.get_value()
            th = np.linspace(0, 2 * np.pi, 600)
            c, s = np.cos(th), np.sin(th)
            r = (np.abs(c) ** p + np.abs(s) ** p) ** (-1 / p)
            return VMobject(color=C.DIST, stroke_width=4, fill_color=C.DIST, fill_opacity=0.15).set_points_as_corners(
                [ax.c2p(rr * a, rr * b) for rr, a, b in zip(r, c, s)])

        b = always_redraw(ball)
        pl = always_redraw(lambda: MathTex(rf"\{{|x|_p \le 1\}}, \ p = {pT.get_value():.3g}", font_size=30,
                                           color=C.DIST).next_to(ax, DOWN, buff=0.15))
        side = VGroup(
            MathTex(r"\|f\|_p = \Big(\int |f|^p\,d\mu\Big)^{1/p}", font_size=34),
            label(r"distances between functions", font_size=26, color=GREY_A),
            label(r"$L^1$, $L^2$, $L^\infty$: \ each complete (Riesz--Fischer)", font_size=26),
            label(r"$L^2$: \ angles and projections, \ Pythagoras", font_size=26, color=C.INNER),
            label(r"in infinitely many dimensions", font_size=26, color=C.INNER),
            label(r"and Fourier series converge in $L^2$, for every $f \in L^2$", font_size=26, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.0, -0.6, 0])
        # the case p = 2: a vector, its orthogonal projection onto a line through 0, the right angle (Pythagoras)
        u = np.array([math.cos(0.35), math.sin(0.35)])
        v = np.array([0.45, 1.05])
        P = float(v @ u) * u
        assert abs(float((v - P) @ u)) < 1e-12 and abs(v @ v - P @ P - (v - P) @ (v - P)) < 1e-12

        def pt(w):
            return ax.c2p(float(w[0]), float(w[1]))

        ell = Line(pt(-1.35 * u), pt(1.35 * u), color=C.INNER, stroke_width=2, stroke_opacity=0.7)
        va = Arrow(pt([0, 0]), pt(v), buff=0, color=WHITE, stroke_width=4, tip_length=0.2)
        pa = Arrow(pt([0, 0]), pt(P), buff=0, color=C.INNER, stroke_width=5, tip_length=0.2)
        drop = DashedLine(pt(v), pt(P), color=GREY_B, stroke_width=2.5)
        ra = RightAngle(Line(pt(P), pt(P - 0.5 * u)), Line(pt(P), pt(v)), length=0.18, color=GREY_B, stroke_width=2)
        vl = MathTex("f", font_size=28).next_to(pt(v), UP, buff=0.08)
        pl_ = MathTex(r"Pf", font_size=28, color=C.INNER).next_to(pt(P), DOWN + RIGHT, buff=0.08)
        proj = VGroup(ell, va, pa, drop, ra, vl, pl_)
        with self.voiceover(
            "Next time, in Part 6: distances between functions. <bookmark mark='a'/> The p-norms measure functions "
            "in different ways; in the plane their unit balls run from a diamond, through the circle, to a square. "
            "<bookmark mark='b'/> With Lebesgue's integral, every one of these spaces is complete. And the case p "
            "equals two has angles and projections: Pythagoras in infinitely many dimensions, which is exactly the "
            "geometry Fourier series were waiting for."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(b), FadeIn(pl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(pT.animate.set_value(2.0), run_time=2.0)
            self.play(pT.animate.set_value(12.0), run_time=2.5)
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), pT.animate.set_value(2.0), run_time=1.5)
            self.play(FadeIn(side[3:5]), Create(ell), GrowArrow(va), FadeIn(vl))
            self.play(Create(drop), GrowArrow(pa), FadeIn(pl_), Create(ra))
            self.play(FadeIn(side[5]))
        for m in (b, pl):
            m.clear_updaters()
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        lines = VGroup(
            label(r"Following W.~Rudin, \textit{Real and Complex Analysis}, 3rd ed.\ (1987), chapters 1, 2 and 8, "
                  r"and \textit{Principles}, chapter 11", font_size=24),
            label(r"H.~Lebesgue (1902), \ G.~Vitali (1905), \ P.~Fatou (1906), \ G.~Fubini (1907), \ L.~Tonelli (1909), "
                  r"\ F.~Riesz (1909)", font_size=22, color=GREY_A),
            label(r"N.~Lusin (1912), \ D.~Egorov (1911), \ P.~Urysohn, \ C.~Carath\'eodory, \ J.~E.~Littlewood (1944)",
                  font_size=22, color=GREY_A),
            label(r"Companions: \ T.~Tao, \textit{An Introduction to Measure Theory}; \ G.~Folland, \textit{Real Analysis}",
                  font_size=22, color=GREY_A),
            label(r"Every number on screen is computed and checked; \ Vitali's set is the one labeled schematic.",
                  font_size=24, color=C.EPS),
            label(r"Animated with Manim Community; narrated by Kokoro-82M.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        with self.voiceover(
            "This part followed chapters one, two and eight of Rudin's Real and Complex Analysis. Thanks for "
            "watching, and see you in Part 6."
        ):
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lines], lag_ratio=0.25), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(lines))

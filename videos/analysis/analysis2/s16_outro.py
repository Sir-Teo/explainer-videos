from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.vector()
        self.recap()
        self.ledger_row()
        self.next_time()
        self.credits()

    # ------------------------------------------------------------------
    def vector(self):
        head = VGroup(label(r"Vector-valued functions (Rudin 5.16--5.19): \ the mean value theorem fails", font_size=30),
                      MathTex(r"f(t) = e^{it} = (\cos t, \sin t), \quad 0 \le t \le 2\pi", font_size=34)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        o = np.array([-3.2, -0.6, 0])
        R = 2.0
        circ = Circle(radius=R, color=GREY_D, stroke_width=2).move_to(o)
        tT = ValueTracker(0.0)
        trace = always_redraw(lambda: Arc(radius=R, start_angle=0, angle=max(tT.get_value(), 1e-4), color=C.FUNC,
                                          stroke_width=5, arc_center=o))
        dot = always_redraw(lambda: Dot(o + R * np.array([np.cos(tT.get_value()), np.sin(tT.get_value()), 0]),
                                        radius=0.08, color=C.FUNC))
        vel = always_redraw(lambda: Arrow(o + R * np.array([np.cos(tT.get_value()), np.sin(tT.get_value()), 0]),
                                          o + R * np.array([np.cos(tT.get_value()), np.sin(tT.get_value()), 0])
                                          + 1.2 * np.array([-np.sin(tT.get_value()), np.cos(tT.get_value()), 0]),
                                          buff=0, color=C.DELTA, stroke_width=4, tip_length=0.18))
        start = Dot(o + R * RIGHT, radius=0.1, color=WHITE)
        facts = VGroup(MathTex(r"f(2\pi) - f(0) = 0", font_size=34, color=WHITE),
                       MathTex(r"|f'(t)| = 1 \text{ for every } t", font_size=34, color=C.DELTA),
                       label(r"so $f(2\pi) - f(0) = 2\pi\, f'(\xi)$ is impossible", font_size=28, color=C.PATHOLOGY),
                       label(r"\textbf{Rudin 5.19}: \ the inequality survives:", font_size=28),
                       MathTex(r"|f(b) - f(a)| \le (b - a)\, |f'(\xi)| \text{ for some } \xi", font_size=32,
                               color=C.CONNECTED_SET),
                       VGroup(label(r"the form that works in every later space", font_size=24, color=GREY_A),
                              label(r"(Part 4: $\R^n$; \ Banach spaces)", font_size=24, color=GREY_A)
                              ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        facts.next_to(o + R * RIGHT, RIGHT, buff=0.7)
        with self.voiceover(
            "One last result, to close the part. <bookmark mark='a'/> Let a point go once around the unit circle at "
            "unit speed. <bookmark mark='b'/> It ends where it started, so the total change is zero, <bookmark mark='c'/> "
            "but the velocity always has length one, so no instant has the average velocity, which is zero. For "
            "vector-valued functions the mean value theorem fails. <bookmark mark='d'/> What survives is an inequality: "
            "the total change is at most the elapsed time times the speed at some moment. That inequality, not the "
            "equation, is the version that carries over to many dimensions and to the infinite-dimensional spaces to "
            "come."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(circ), FadeIn(start), FadeIn(trace), FadeIn(dot), FadeIn(vel))
            self.play(tT.animate.set_value(2 * np.pi), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(facts[0]))
            vo.wait_until("c")
            self.play(FadeIn(facts[1]), FadeIn(facts[2]))
            vo.wait_until("d")
            self.play(FadeIn(facts[3]), FadeIn(facts[4]), FadeIn(facts[5]))
        for m in (trace, dot, vel):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        items = [
            (r"convergence is a game: \ $\varepsilon$ first, then $N$", C.EPS),
            (r"Cauchy sequences converge exactly in complete spaces; \ $\Q$ is not one", C.HOLE),
            (r"lim sup and lim inf: \ the high- and low-water marks of the tail", C.UPPER_SUM),
            (r"series: \ comparison, condensation, \ $\sum 1/n^p$ converges iff $p > 1$", C.SEQ),
            (r"$e = \sum 1/n! = \lim (1 + 1/n)^n$, \ and $e$ is irrational", C.CUT_HIGH),
            (r"root and ratio tests; \ power series converge in disks", C.EPS),
            (r"summation by parts: \ the sawtooth series converges at every $x$", C.APPROX),
            (r"conditionally convergent series can be rearranged to anything", C.PATHOLOGY),
            (r"continuity: \ preimages of open sets are open", C.OPEN_SET),
            (r"on compact sets: \ extreme values, uniform continuity", C.COMPACT_SET),
            (r"on connected sets: \ intermediate values; \ Thomae's function", C.CONNECTED_SET),
            (r"derivatives: \ mean value, Darboux, Taylor; \ $e^{-1/x^2}$", C.FUNC),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(DOWN * 0.2)
        head = label(r"Part 2, in twelve lines", font_size=40).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Let's take stock. Convergence is a game where epsilon moves first. Cauchy sequences let us test "
            "convergence without knowing the limit, and they converge exactly in complete spaces, which the rationals "
            "are not. Upper and lower limits describe what's left when there's no limit. For series we have comparison, "
            "condensation, and the root and ratio tests; e is irrational; power series converge in disks. Summation by "
            "parts proved that the sawtooth series converges at every point, and Riemann showed that conditionally "
            "convergent series can be rearranged to sum to anything. Continuity became a statement about open sets, and "
            "compactness and connectedness gave the extreme value theorem, uniform continuity, and intermediate values. "
            "Finally, the derivative: the mean value theorem, Darboux's theorem, Taylor's theorem, and a smooth function "
            "its Taylor series can't see."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger_row(self):
        before = ledger(filled=1, highlight=2).scale(0.95)
        after = ledger(filled=2, highlight=2).scale(0.95)
        after.shift(before.head.get_center() - after.head.get_center())  # the new row lands exactly in the old one's place
        cells = after.rows[1]
        assert len(cells) == 6
        with self.voiceover(
            "And the ledger gets its second row. <bookmark mark='a'/> The space: sequences and series of numbers. "
            "<bookmark mark='b'/> Complete means Cauchy sequences converge. <bookmark mark='c'/> Compactness means every "
            "sequence has a convergent subsequence. <bookmark mark='d'/> The limits we may swap: we may reorder a sum "
            "when it converges absolutely. <bookmark mark='e'/> And Fourier's series: it converges at each point, though "
            "not yet in any stronger sense, and we don't yet know to what, in general."
        ) as vo:
            self.play(FadeIn(before))
            vo.wait_until("a")
            self.play(FadeOut(before.rows[1]), FadeIn(cells[0], shift=RIGHT * 0.1), FadeIn(cells[1], shift=RIGHT * 0.1))
            self.play(Indicate(cells[1], color=C.EPS, scale_factor=1.06), run_time=0.6)
            for i, mk in zip(range(2, 6), "bcde"):
                vo.wait_until(mk)
                self.play(FadeIn(cells[i], shift=RIGHT * 0.1), run_time=0.6)
                self.play(Indicate(cells[i], color=C.EPS, scale_factor=1.06), run_time=0.6)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: Part 3, \ Integration and the first function space", font_size=38).to_edge(UP, buff=0.35)
        M = 6
        cs = 0.72
        o = np.array([-4.6, 2.05, 0])
        cells = VGroup()
        for m in range(1, M + 1):
            for n in range(1, M + 1):
                v = m / (m + n)
                sq = Square(side_length=cs * 0.94, stroke_width=0, fill_color=interpolate_color(ManimColor(C.SEQ),
                                                                                               ManimColor(C.EPS), v),
                            fill_opacity=0.85).move_to(o + np.array([(n - 1) * cs, -(m - 1) * cs, 0]))
                t = MathTex(rf"\tfrac{{{m}}}{{{m + n}}}", font_size=20, color=BLACK).move_to(sq)
                cells.add(VGroup(sq, t))
        gl = MathTex(r"s_{mn} = \frac{m}{m + n}", font_size=32).next_to(cells, DOWN, buff=0.3)
        mn = VGroup(MathTex(r"n \to", font_size=28, color=GREY_A).next_to(cells, UP, buff=0.12),
                    MathTex(r"m", r"\downarrow", font_size=28, color=GREY_A).arrange(DOWN, buff=0.05).next_to(cells, LEFT,
                                                                                                            buff=0.15))
        lims = VGroup(MathTex(r"\lim_{n\to\infty} \lim_{m\to\infty} s_{mn} = 1", font_size=34, color=C.EPS),
                      MathTex(r"\lim_{m\to\infty} \lim_{n\to\infty} s_{mn} = 0", font_size=34, color=C.SEQ),
                      label(r"Rudin 7.2: \ the order of two limits matters", font_size=26, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.0, 0.6, 0])
        q = label(r"When may we integrate a Fourier series term by term? \ That is an interchange of limits.",
                  font_size=28, color=C.EPS).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Next time, in Part 3, integration, and the first real function space. <bookmark mark='a'/> It starts from "
            "Rudin's main problem. In this grid, m over m plus n, go far down a column and the entries approach one; go "
            "far along a row and they approach zero. <bookmark mark='b'/> Take the limits in one order and you get one, "
            "in the other order, zero. <bookmark mark='c'/> Integrating a Fourier series term by term is exactly such "
            "an interchange, and Part 3 is about when it's allowed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.02), FadeIn(gl), FadeIn(mn), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(lims))
            vo.wait_until("c")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        lines = VGroup(
            label(r"Following W.~Rudin, \textit{Principles of Mathematical Analysis}, 3rd ed.\ (1976), chapters 3--5",
                  font_size=24),
            label(r"B.~Bolzano (1817), \ A.-L.~Cauchy (1821, 1823), \ N.~H.~Abel, \ P.~G.~L.~Dirichlet,", font_size=24,
                  color=GREY_A),
            label(r"B.~Riemann (1854), \ F.~Mertens, \ G.~Darboux (1875), \ J.~Thomae (1875)", font_size=24,
                  color=GREY_A),
            label(r"Companions: S.~Abbott, \textit{Understanding Analysis}; \ C.~Pugh, \textit{Real Mathematical Analysis};"
                  r" \ T.~Tao, \textit{Analysis I}", font_size=24, color=GREY_A),
            label(r"Every number on screen is computed and checked; schematics are labeled.", font_size=24, color=C.EPS),
            label(rf"Animated with Manim Community; narrated by {narration_credit()}.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        with self.voiceover(
            "This part followed chapters three to five of Rudin's Principles of Mathematical Analysis. Thanks for "
            "watching, and see you in Part 3."
        ):
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lines], lag_ratio=0.25), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(lines))

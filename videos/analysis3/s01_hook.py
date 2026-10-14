from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import load, plain_axes, polyline, saw, saw_partial


class Hook(VoiceoverScene):
    def construct(self):
        self.recap()
        self.grid()
        self.failures()
        self.fourier()
        self.plan()

    # ------------------------------------------------------------------
    def recap(self):
        led = ledger(filled=2, highlight=3).scale(0.9)
        with self.voiceover(
            "So far we have built the real numbers and learned to take limits: of sequences, of sums, of difference "
            "quotients. <bookmark mark='l'/> That's two rows of the ledger. This part is about the third row, and it "
            "starts from the question that Rudin calls the main problem of his seventh chapter."
        ) as vo:
            self.play(FadeIn(led))
            vo.wait_until("l")
            self.play(Indicate(VGroup(led.rows[0], led.rows[1]), color=C.EPS, scale_factor=1.03))
        self.play(FadeOut(led))

    # ------------------------------------------------------------------
    def grid(self):
        M = 6
        cs = 0.72
        o = np.array([-5.0, 2.05, 0])
        cells = VGroup()
        for m in range(1, M + 1):
            for n in range(1, M + 1):
                v = m / (m + n)
                # a neutral value ramp (dark near 0, light near 1); the text flips to stay legible
                sq = Square(side_length=cs * 0.94, stroke_width=0, fill_opacity=0.9,
                            fill_color=interpolate_color(ManimColor("#2B3442"), ManimColor(GREY_A), v))
                sq.move_to(o + np.array([(n - 1) * cs, -(m - 1) * cs, 0]))
                cells.add(VGroup(sq, MathTex(rf"\frac{{{m}}}{{{m + n}}}", font_size=24,
                                             color=BLACK if v > 0.45 else WHITE).move_to(sq)))
        n_l = MathTex(r"n \to", font_size=28, color=GREY_B).next_to(cells[0], UP, buff=0.2).align_to(cells[0], LEFT)
        m_l = MathTex(r"m \downarrow", font_size=28, color=GREY_B).next_to(cells[0], LEFT, buff=0.2)
        rows_to = VGroup(*[MathTex(r"\to 0", font_size=24, color=C.SEQ).next_to(cells[m * M + M - 1], RIGHT, buff=0.15)
                           for m in range(M)])
        cols_to = VGroup(*[MathTex(r"\downarrow\!1", font_size=24, color=C.LIMIT).next_to(cells[(M - 1) * M + n], DOWN,
                                                                                          buff=0.12) for n in range(M)])
        main = VGroup(MathTex(r"s_{mn} = \frac{m}{m + n}", font_size=36),
                      MathTex(r"\lim_{m\to\infty}\,\lim_{n\to\infty} s_{mn} = 0", font_size=34, color=C.SEQ),
                      MathTex(r"\lim_{n\to\infty}\,\lim_{m\to\infty} s_{mn} = 1", font_size=34, color=C.LIMIT),
                      label(r"Rudin 7.1--7.2: \ when may two limits be swapped?", font_size=28, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.3, 0.5, 0])
        with self.voiceover(
            "Here is the grid from the end of Part 2: m over m plus n. <bookmark mark='r'/> Walk along any row, "
            "letting n grow, and the entries go to zero; then let m grow, and you still have zero. "
            "<bookmark mark='c'/> Walk down any column first, and the entries go to one. Same numbers, two orders, "
            "two answers. <bookmark mark='q'/> Rudin's main problem is exactly this: when may two limits be swapped? "
            "Continuity, integrals, derivatives and infinite sums are all limits, so the question comes up everywhere."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.02), FadeIn(n_l), FadeIn(m_l),
                      FadeIn(main[0]), run_time=1.6)
            vo.wait_until("r")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows_to], lag_ratio=0.12), FadeIn(main[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in cols_to], lag_ratio=0.12), FadeIn(main[2]))
            vo.wait_until("q")
            self.play(FadeIn(main[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def failures(self):
        d = load("failures")
        head = label(r"Three sequences of functions $f_n \to f$, \ and three swaps that fail", font_size=32)
        head.to_edge(UP, buff=0.3)
        W, H = 3.9, 2.9
        xs = (-4.55, 0.0, 4.55)
        y0 = -0.35
        n1, n2, n3 = ValueTracker(1.0), ValueTracker(1.0), ValueTracker(1.0)
        x = np.linspace(0, 1, 900)
        # 1. x^n: continuity lost
        ax1 = plain_axes([0, 1, 0.5], [0, 1.1, 0.5], W, H).move_to([xs[0], y0, 0])
        g1 = always_redraw(lambda: polyline(ax1, x, x ** n1.get_value(), color=C.FUNC, stroke_width=3.5))
        lim1 = VGroup(Line(ax1.c2p(0, 0), ax1.c2p(0.985, 0), color=WHITE, stroke_width=3),
                      Circle(radius=0.06, color=WHITE, stroke_width=2.5).set_fill(BACKGROUND, 1).move_to(ax1.c2p(1, 0)),
                      Dot(ax1.c2p(1, 1), radius=0.07, color=WHITE))
        t1 = MathTex(r"f_n(x) = x^n", font_size=30, color=C.FUNC).next_to(ax1, UP, buff=0.2)
        v1 = VGroup(MathTex(r"\lim_n \lim_{x \to 1} f_n = 1", font_size=26),
                    MathTex(r"\lim_{x \to 1} \lim_n f_n = 0", font_size=26),
                    label(r"continuous $f_n$, discontinuous $f$", font_size=22, color=C.PATHOLOGY)
                    ).arrange(DOWN, buff=0.12).next_to(ax1, DOWN, buff=0.3)
        # 2. n^2 x (1 - x^2)^n: the integral lost (Rudin 7.6)
        # the bump's peak n^2 x (1 - x^2)^n is at x = 1/sqrt(2n + 1); up to n = 10 it stays under 15 (no clipping)
        peak = lambda n: n * n / np.sqrt(2 * n + 1) * (2 * n / (2 * n + 1)) ** n  # noqa: E731
        xp = np.linspace(0, 1, 200001)
        for n_ in (1, 5, 9, 10):
            assert abs((n_ * n_ * xp * (1 - xp * xp) ** n_).max() - peak(n_)) < 1e-6
        assert 13 < peak(10) < 14.5
        ax2 = plain_axes([0, 1, 0.5], [0, 15, 5], W, H).move_to([xs[1], y0, 0])
        g2 = always_redraw(lambda: runs(ax2, x, n2.get_value() ** 2 * x * (1 - x * x) ** n2.get_value(), C.FUNC, 3.5))
        lim2 = Line(ax2.c2p(0, 0), ax2.c2p(1, 0), color=WHITE, stroke_width=3)
        t2 = MathTex(r"f_n(x) = n^2 x (1 - x^2)^n", font_size=30, color=C.FUNC).next_to(ax2, UP, buff=0.2)
        int2 = always_redraw(lambda: MathTex(
            rf"\int_0^1 f_n = \frac{{n^2}}{{2n + 2}} = {n2.get_value() ** 2 / (2 * n2.get_value() + 2):.2f}",
            font_size=26).next_to(ax2, DOWN, buff=0.3))
        v2 = VGroup(label(r"$f_n \to 0$ at every $x$, \ but $\int f_n \to \infty$", font_size=22, color=C.PATHOLOGY)
                    ).next_to(ax2, DOWN, buff=1.05)
        # 3. sin(nx)/sqrt n: the derivative lost (Rudin 7.5)
        ax3 = plain_axes([0, 2 * np.pi, np.pi], [-1.1, 1.1, 1], W, H).move_to([xs[2], y0, 0])
        x3 = np.linspace(0, 2 * np.pi, 1500)
        g3 = always_redraw(lambda: polyline(ax3, x3, np.sin(round(n3.get_value()) * x3) / np.sqrt(round(n3.get_value())),
                                            color=C.FUNC, stroke_width=2.5))
        lim3 = Line(ax3.c2p(0, 0), ax3.c2p(2 * np.pi, 0), color=WHITE, stroke_width=2)
        t3 = MathTex(r"f_n(x) = \frac{\sin nx}{\sqrt n}", font_size=30, color=C.FUNC).next_to(ax3, UP, buff=0.12)
        der3 = always_redraw(lambda: MathTex(
            rf"\sup|f_n| = {1 / np.sqrt(round(n3.get_value())):.3f}, \quad", rf"f_n'(0) = \sqrt n = {np.sqrt(round(n3.get_value())):.2f}",
            font_size=24).set_color_by_tex("f_n'", C.EPS).next_to(ax3, DOWN, buff=0.3))
        # the tangent at 0, of slope f_n'(0) = sqrt n (drawn up to height 1.05, inside the axes): it steepens
        tan3 = always_redraw(lambda: Line(ax3.c2p(0, 0), ax3.c2p(1.05 / np.sqrt(round(n3.get_value())), 1.05),
                                          color=C.EPS, stroke_width=3.5))
        assert abs(np.gradient(np.sin(24 * x3) / np.sqrt(24), x3)[0] - np.sqrt(24)) < 0.05
        v3 = label(r"$f_n \to 0$ uniformly, \ $f_n'$ does not converge", font_size=22, color=C.PATHOLOGY).next_to(
            ax3, DOWN, buff=1.05)
        # the three panels on common baselines: n-labels above the tallest title, red verdicts on one row
        y_n = max(t_.get_top()[1] for t_ in (t1, t2, t3)) + 0.28
        nls = [always_redraw(lambda t=t, tt=tt: MathTex(rf"n = {round(t.get_value())}", font_size=28, color=C.FUNC).move_to(
            [tt.get_x(), y_n, 0])) for t, tt in ((n1, t1), (n2, t2), (n3, t3))]
        v2.set_y(v1[2].get_y())
        v3.set_y(v1[2].get_y())
        assert abs(d["bump_int"][-1] - 89**2 / 180) < 1e-3 and abs(d["sup_s"][-1] - 1 / np.sqrt(89)) < 1e-12
        with self.voiceover(
            "Here are three sequences of functions where swapping fails. <bookmark mark='a'/> First, x to the n on "
            "the interval from zero to one. Each one is continuous. As n grows, the graphs fall to zero everywhere "
            "except at one, where they stay at one. The limit jumps, so a limit of continuous functions need not be "
            "continuous: approaching one first and then letting n grow gives one, and the other order gives zero. "
            "<bookmark mark='b'/> Second, Rudin's example: n squared x times one minus x squared to the n. At every "
            "single x these go to zero, but the bump grows taller and narrower, and its area, n squared over two n "
            "plus two, goes to infinity. The integral of the limit is zero; the limit of the integrals is infinite. "
            "<bookmark mark='c'/> Third, sine of n x over root n. These go to zero as uniformly as you could ask, "
            "since the largest value is one over root n. But they wiggle faster and faster: the slope at zero is root "
            "n, which grows without bound. The derivatives of the limit are zero, and the limit of the derivatives "
            "doesn't exist."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax1), FadeIn(t1), Create(g1), FadeIn(lim1), FadeIn(nls[0]))
            self.play(n1.animate.set_value(40), run_time=4.0, rate_func=smooth)
            self.play(FadeIn(v1[:2]))
            self.play(FadeIn(v1[2]))
            vo.wait_until("b")
            self.play(Create(ax2), FadeIn(t2), FadeIn(lim2), FadeIn(g2), FadeIn(int2), FadeIn(nls[1]))
            self.play(n2.animate.set_value(10), run_time=5.0, rate_func=linear)
            self.play(FadeIn(v2))
            vo.wait_until("c")
            self.play(Create(ax3), FadeIn(t3), FadeIn(lim3), FadeIn(g3), FadeIn(der3), FadeIn(nls[2]), Create(tan3))
            self.play(n3.animate.set_value(24), run_time=5.0, rate_func=linear)
            self.play(FadeIn(v3))
        for m in (g1, g2, g3, int2, der3, tan3, *nls):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fourier(self):
        ax = plain_axes([-np.pi, 3 * np.pi, np.pi], [-2.0, 2.0, 1], 10.5, 3.6).move_to([0, -0.9, 0])
        x = np.linspace(-np.pi, 3 * np.pi, 2400)
        saw_g = VGroup(*[Line(ax.c2p(a + 1e-3, saw(np.array([a + 1e-3]))[0]), ax.c2p(b - 1e-3, saw(np.array([b - 1e-3]))[0]),
                              color=WHITE, stroke_width=4) for a, b in ((-np.pi, 0), (0, 2 * np.pi), (2 * np.pi, 3 * np.pi))])
        saw_g.set_z_index(2)
        cur = polyline(ax, x, saw_partial(x, 3), color=C.APPROX, stroke_width=2.5)
        swap = MathTex(r"\int \sum_{k=1}^{\infty} \frac{\sin kx}{k}\,dx", r"\;\overset{?}{=}\;",
                       r"\sum_{k=1}^{\infty} \int \frac{\sin kx}{k}\,dx", font_size=40).to_edge(UP, buff=0.5)
        swap[0].set_color(WHITE)
        swap[2].set_color(C.APPROX)
        note_ = label(r"a Fourier series is a limit, so integrating it term by term is a swap of two limits",
                      font_size=28, color=C.EPS).next_to(swap, DOWN, buff=0.3)
        with self.voiceover(
            "And this is why the question matters for Fourier's series. <bookmark mark='a'/> The sawtooth is the sum "
            "of sine k x over k. <bookmark mark='b'/> Integrating it term by term means integrating each sine and adding "
            "up, but the sum is itself a limit, so that's a swap of two limits, and we've just seen such swaps fail. "
            "This part finds conditions that make them legal."
        ) as vo:
            self.play(Create(ax), FadeIn(saw_g))
            vo.wait_until("a")
            self.play(Create(cur))
            for N in (8, 30):
                self.play(Transform(cur, polyline(ax, x, saw_partial(x, N), color=C.APPROX, stroke_width=2.5)), run_time=0.9)
            vo.wait_until("b")
            self.play(Write(swap))
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        chapters = [
            r"Upper and lower sums", r"Which functions are integrable?", r"Integrating against a staircase",
            r"The fundamental theorem, and length", r"Uniform convergence", r"Uniform limits, and the space $C(X)$",
            r"Integrals and derivatives of limits", r"A continuous function with no derivative", r"Equicontinuity",
            r"Arzel\`a--Ascoli", r"Weierstrass approximation", r"Stone--Weierstrass", r"Power series, and $\pi$",
            r"Fourier series", r"Parseval, Gibbs, and $\pi^2/6$",
        ]
        items = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=26) for i, t in enumerate(chapters)])
        col1 = VGroup(*items[:8]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        col2 = VGroup(*items[8:]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        cols = VGroup(col1, col2).arrange(RIGHT, buff=0.9, aligned_edge=UP).shift(DOWN * 0.35)
        head = label(r"Part 3: Integration and the first function space", font_size=42).to_edge(UP, buff=0.45)
        sub = label(r"Rudin, \textit{Principles}, chapters 6--8", font_size=26, color=GREY_B).next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "Here's the plan, following chapters six to eight of Rudin's Principles. <bookmark mark='a'/> First the "
            "integral itself: Riemann's version and Stieltjes' generalization, which functions it can handle, and the "
            "fundamental theorem of calculus. <bookmark mark='b'/> Then uniform convergence, the condition that makes "
            "the swaps legal, and the first space whose points are functions. We'll meet a continuous function with no "
            "derivative anywhere, and the compactness theorem of Arzelà and Ascoli. <bookmark mark='c'/> Then "
            "approximation: every continuous function is nearly a polynomial. And finally the payoff: power series, "
            "and what we can now say about Fourier series."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(4)], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(4, 10)], lag_ratio=0.25))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(10, 15)], lag_ratio=0.25))
        self.wait(0.6)
        self.clear_scene()

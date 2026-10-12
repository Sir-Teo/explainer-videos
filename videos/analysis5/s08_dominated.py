from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import area_under, load, plain_axes, polyline


class Dominated(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.lid()
        self.typewriter()
        self.egorov()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Dominated convergence", r"When may a limit pass under the integral sign?",
                            lit=(1902,), part=5)
        with self.voiceover("Chapter seven: Lebesgue's dominated convergence theorem, the answer this part promised."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def theorem(self):
        head = VGroup(
            label(r"\textbf{RCA 1.34} \ $f_n \to f$ pointwise, \ $|f_n| \le g$ for all $n$, \ $\int g < \infty$ "
                  r"$\Rightarrow$", font_size=30),
            MathTex(r"\int |f_n - f|\,d\mu \to 0, \qquad \text{so} \quad \int f_n\,d\mu \to \int f\,d\mu", font_size=38,
                    color=C.EPS)).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.35)
        rows = [
            MathTex(r"2g - |f_n - f|", r"\ge", r"0", font_size=34),
            MathTex(r"\int 2g", r"\le", r"\liminf \int \big(2g - |f_n - f|\big)", font_size=34),
            MathTex(r"\int 2g", r"\le", r"\int 2g - \limsup \int |f_n - f|", font_size=34),
            MathTex(r"\limsup \int |f_n - f|", r"\le", r"0", font_size=34),
        ]
        whys = [why(r"$|f_n - f| \le |f_n| + |f| \le 2g$"), why(r"Fatou, \ with $2g - |f_n - f| \to 2g$"),
                why(r"linearity"), why(r"subtract $\int 2g < \infty$")]
        step = ladder(self, rows, whys, keep=4, top=1.0, buff=0.4, x=-0.4)
        with self.voiceover(
            "<bookmark mark='a'/> The theorem: if f n converges to f at every point, and all the f n lie under one "
            "integrable function g, the lid, then the integrals converge, and in fact the integral of the "
            "difference goes to zero. <bookmark mark='b'/> The proof is Fatou's lemma applied to the right functions. "
            "Two g minus the difference is non-negative, <bookmark mark='c'/> and it converges to two g, so Fatou "
            "bounds the integral of two g by the lower limit of its integrals. <bookmark mark='d'/> Pull out the "
            "integral of two g, <bookmark mark='e'/> which is finite because the lid is integrable, and the upper "
            "limit of the integral of the difference is at most zero. The lid is the whole story."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            for i, mk in enumerate("bcde"):
                vo.wait_until(mk)
                step(i)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lid(self):
        x = np.linspace(0, 8, 2401)
        W, H = 6.0, 3.0
        ax = plain_axes([0, 8, 2], [0, 1.1, 0.5], W, H).move_to([-3.5, 0.0, 0])
        bx = plain_axes([0, 8, 2], [0, 1.1, 0.5], W, H).move_to([3.5, 0.0, 0])
        nT = ValueTracker(1.0)

        def spread():
            n = nT.get_value()
            y = np.where(x <= n, 1 / n, 0.0)
            return VGroup(area_under(ax, x, y, C.MEASURE, 0.4), polyline(ax, x, y, color=C.FUNC, stroke_width=3))

        def good():
            n = nT.get_value()
            y = np.where(x <= n, np.clip(1 - x / n, 0, None) ** n, 0.0)
            return VGroup(area_under(bx, x, y, C.MEASURE, 0.4), polyline(bx, x, y, color=C.FUNC, stroke_width=3))

        g1, g2 = always_redraw(spread), always_redraw(good)
        lidg = polyline(bx, x, np.exp(-x), color=C.EPS, stroke_width=3)
        lidl = MathTex(r"g = e^{-x}", font_size=28, color=C.EPS).next_to(bx.c2p(1.2, 0.55), RIGHT, buff=0.1)
        t1 = MathTex(r"\tfrac1n \mathbf 1_{[0, n]}", font_size=30).next_to(ax, UP, buff=0.1)
        t2 = MathTex(r"\big(1 - \tfrac xn\big)^n \mathbf 1_{[0, n]}", font_size=30).next_to(bx, UP, buff=0.1)
        r1 = always_redraw(lambda: MathTex(rf"\sup|f_n| = {1 / nT.get_value():.3f} \to 0, \quad \int f_n = 1",
                                           font_size=28, color=C.PATHOLOGY).next_to(ax, DOWN, buff=0.2))
        r2 = always_redraw(lambda: MathTex(
            rf"\int f_n = \tfrac{{n}}{{n + 1}} = {nT.get_value() / (nT.get_value() + 1):.3f} \to 1 = \int e^{{-x}}",
            font_size=28, color=C.CONNECTED_SET).next_to(bx, DOWN, buff=0.2))
        xs = np.linspace(0, 50, 20001)
        for n in (1, 2, 5, 20):
            fn = np.where(xs <= n, np.clip(1 - xs / n, 0, None) ** n, 0.0)
            assert np.all(fn <= np.exp(-xs) + 1e-12)
            assert abs(np.sum((fn[1:] + fn[:-1]) * np.diff(xs)) / 2 - n / (n + 1)) < 1e-3
        head = label(r"On an infinite interval, \ uniform convergence is not enough; \ a lid is", font_size=30)
        head.to_edge(UP, buff=0.3)
        verdicts = VGroup(label(r"uniformly to $0$, \ no integrable lid: \ the swap fails", font_size=24,
                                color=C.PATHOLOGY).next_to(ax, DOWN, buff=1.0),
                          label(r"under the lid $e^{-x}$: \ the swap is legal", font_size=24,
                                color=C.CONNECTED_SET).next_to(bx, DOWN, buff=1.0))
        with self.voiceover(
            "<bookmark mark='a'/> Compare two sequences on the half-line. On the left, the spreading sequence: it "
            "converges to zero uniformly, the strongest convergence Part 3 knew, yet every function has integral one. "
            "Part 3's theorem needed a bounded interval. <bookmark mark='b'/> On the right, one minus x over n, to "
            "the n. These lie under the single integrable lid, e to the minus x, <bookmark mark='c'/> so dominated "
            "convergence applies: the integrals, n over n plus one, converge to the integral of the limit, which is "
            "one."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(bx), FadeIn(t1), FadeIn(t2))
            vo.wait_until("a")
            self.play(FadeIn(g1), FadeIn(r1))
            self.play(nT.animate.set_value(6.0), run_time=3.0, rate_func=linear)
            self.play(FadeIn(verdicts[0]))
            vo.wait_until("b")
            self.play(nT.animate.set_value(1.0), run_time=0.6)
            self.play(FadeIn(g2), Create(lidg), FadeIn(lidl))
            vo.wait_until("c")
            self.play(FadeIn(r2))
            self.play(nT.animate.set_value(8.0), run_time=4.0, rate_func=linear)
            self.play(FadeIn(verdicts[1]))
        for m in (g1, g2, r1, r2):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def typewriter(self):
        d = load("dct")
        norms = d["norms"]
        ax = plain_axes([0, 1, 0.25], [0, 1.2, 0.5], 7.6, 3.2).move_to([-2.5, 0.1, 0])
        kT = ValueTracker(1)

        def bar():
            k = int(kT.get_value())
            m = int(math.floor(math.log2(k)))
            j = k - 2**m
            a, b = j / 2**m, (j + 1) / 2**m
            r = Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0], height=ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1],
                          stroke_color=C.FUNC, stroke_width=3, fill_color=C.MEASURE, fill_opacity=0.45)
            return r.move_to(ax.c2p((a + b) / 2, 0.5))

        b_ = always_redraw(bar)
        lab = always_redraw(lambda: MathTex(
            rf"f_{{{int(kT.get_value())}}} = \mathbf 1_{{[j 2^{{-m}}, (j+1) 2^{{-m}}]}}, \quad m = "
            rf"{int(math.floor(math.log2(int(kT.get_value()))))}: \ \int f_k = 2^{{-m}} = "
            rf"{2.0 ** -int(math.floor(math.log2(int(kT.get_value())))):.4f}", font_size=28, color=C.MEASURE)
            .next_to(ax, UP, buff=0.12))
        probe = DashedLine(ax.c2p(0.37, 0), ax.c2p(0.37, 1.2), color=C.SEQ, stroke_width=2)
        pl = MathTex(r"x = 0.37", font_size=24, color=C.SEQ).next_to(probe, DOWN, buff=0.1)
        lamps = VGroup(
            VGroup(label(r"in area: \ $\int |f_k| \to 0$", font_size=26, color=C.MEASURE),
                   Dot(radius=0.1, color=C.CONNECTED_SET)),
            VGroup(label(r"at each point: \ $f_k(x) = 1$ once per sweep, \ forever", font_size=26, color=C.SEQ),
                   Dot(radius=0.1, color=C.PATHOLOGY)),
            VGroup(label(r"uniformly: \ $\sup f_k = 1$", font_size=26, color=C.EPS), Dot(radius=0.1, color=C.PATHOLOGY)),
        )
        for row in lamps:
            row.arrange(RIGHT, buff=0.3)
        lamps.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0.0, -2.6, 0])
        head = label(r"The typewriter: \ converges in area, \ at no point", font_size=32).to_edge(UP, buff=0.2)
        side = VGroup(label(r"a subsequence does converge", font_size=24, color=GREY_A),
                      label(r"a.e. \ (Part 6: Riesz--Fischer)", font_size=24, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([5.3, 0.1, 0])
        assert norms[-1] < 0.002
        with self.voiceover(
            "<bookmark mark='a'/> Convergence of integrals and convergence at points are genuinely different. The "
            "typewriter sequence sweeps an indicator across the interval, then sweeps again at half the width, and "
            "so on. <bookmark mark='b'/> Its integrals go to zero. <bookmark mark='c'/> But every point is covered once "
            "in every sweep, so at no point do the values converge: they keep returning to one. "
            "<bookmark mark='d'/> Converging in area does not imply converging at points, though, as Part 6 will "
            "show, a subsequence always does."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(probe), FadeIn(pl))
            vo.wait_until("a")
            self.play(FadeIn(b_), FadeIn(lab))
            self.play(kT.animate.set_value(15.99), run_time=6.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(lamps[0]))
            vo.wait_until("c")
            self.play(kT.animate.set_value(31.99), run_time=3.0, rate_func=linear)
            self.play(FadeIn(lamps[1:]))
            vo.wait_until("d")
            self.play(FadeIn(side))
        for m in (b_, lab):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def egorov(self):
        d = load("dct")
        eg, eps = d["egorov"], float(d["eps"])
        ax = plain_axes([0, 1, 0.25], [0, 1.05, 0.5], 7.0, 4.2).move_to([-2.9, -0.8, 0])
        x = np.linspace(0, 1, 1201)
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.APPROX), k / 5) for k in range(6)]
        curves = VGroup(*[polyline(ax, x, x**n, color=c, stroke_width=2.5) for n, c in zip((1, 3, 10, 30, 100, 300), cols)])
        strip = Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(1 - eps, 0)[0], height=ax.c2p(0, 1.05)[1] - ax.c2p(0, 0)[1],
                          stroke_width=0, fill_color=C.PATHOLOGY, fill_opacity=0.18).move_to(ax.c2p(1 - eps / 2, 0.525))
        sl = MathTex(rf"[1 - \varepsilon, 1], \ \varepsilon = {eps}", font_size=24, color=C.PATHOLOGY).next_to(
            strip, UP, buff=0.05).shift(LEFT * 0.5)
        head = VGroup(label(r"Egorov (RCA, Exercise 3.16): \ on a finite measure space, \ a.e. convergence is",
                            font_size=28),
                      label(r"uniform off a set of measure as small as you like", font_size=28, color=C.EPS)
                      ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.25)
        tab = VGroup(MathTex(r"n", r"\quad \sup_{[0, 1 - \varepsilon]} x^n", font_size=28, color=GREY_A))
        for n, v in zip((10, 50, 100, 200), eg):
            tab.add(MathTex(rf"{n}", r"\quad " + (f"{v:.4f}" if v > 1e-3 else sci(float(v), 1)), font_size=28))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.9, -0.3, 0])
        for row in tab[1:]:
            row[1].align_to(tab[0][1], LEFT)
        note_ = VGroup(label(r"infinite measure breaks it:", font_size=24, color=GREY_A),
                       label(r"$\mathbf 1_{[n, \infty)} \to 0$ everywhere, \ never uniformly", font_size=24,
                             color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(tab, DOWN, buff=0.35)
        assert np.all(np.diff(eg) < 0)
        with self.voiceover(
            "<bookmark mark='a'/> One more bridge back to Part 3. Egorov's theorem: on a space of finite measure, "
            "convergence almost everywhere is uniform once you remove a set of arbitrarily small measure. "
            "<bookmark mark='b'/> x to the n converges to zero except at one, but not uniformly. Cut out a sliver "
            "of width epsilon at the right end, <bookmark mark='c'/> and on the rest the convergence is uniform: the "
            "largest value is one minus epsilon to the n. <bookmark mark='d'/> On an infinite measure space this "
            "fails: indicators of the rays from n to infinity converge to zero everywhere, but never uniformly."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in curves], lag_ratio=0.2), run_time=2.5)
            self.play(FadeIn(strip), FadeIn(sl))
            vo.wait_until("c")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

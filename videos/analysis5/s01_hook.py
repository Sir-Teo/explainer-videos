from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import area_under, interval_band, plain_axes, polyline


class Hook(VoiceoverScene):
    def construct(self):
        self.recap()
        self.dirichlet()
        self.escapes()
        self.slicing()
        self.plan()

    # ------------------------------------------------------------------
    def recap(self):
        led = ledger(filled=4, highlight=5).scale(0.9)
        with self.voiceover(
            "Four rows of the ledger, and the same column keeps asking the same question: when may a limit pass "
            "through an integral? <bookmark mark='l'/> So far the answer has been: when the convergence is uniform. "
            "This part changes the integral, and gets a far better answer."
        ) as vo:
            self.play(FadeIn(led))
            vo.wait_until("l")
            self.play(Indicate(VGroup(*[r[4] for r in led.rows[:4]]), color=C.EPS, scale_factor=1.05))
        self.play(FadeOut(led))

    # ------------------------------------------------------------------
    def dirichlet(self):
        ax = plain_axes([0, 1, 0.25], [0, 1.1, 0.5], 9.0, 3.6).move_to([-1.4, -0.9, 0])
        x = np.linspace(0, 1, 6001)

        def g(m, n):
            return np.cos(math.factorial(m) * np.pi * x) ** (2 * n)

        frames = [(1, 1), (1, 6), (1, 60), (2, 60), (3, 60), (3, 400), (4, 400), (5, 2000)]
        curves = [polyline(ax, x, g(m, n), color=C.APPROX, stroke_width=2.5 if n < 100 else 1.4) for m, n in frames]
        labs = [MathTex(rf"\cos(m!\,\pi x)^{{2n}}: \quad m = {m},\ n = {n}", font_size=30, color=C.APPROX)
                .next_to(ax, UP, buff=0.1) for m, n in frames]
        # where the limit in n is 1: x = k / m!
        spikes = {m: [k / math.factorial(m) for k in range(math.factorial(m) + 1)] for m in (1, 2, 3)}
        for m in (1, 2, 3):
            assert np.allclose(np.cos(math.factorial(m) * np.pi * np.array(spikes[m])) ** 2, 1)
        side = VGroup(
            label(r"$n \to \infty$: \ $1$ where $m!\,x$ is an integer, \ else $0$", font_size=26),
            label(r"then $m \to \infty$: \ $1$ at every rational, \ $0$ elsewhere", font_size=26, color=C.PATHOLOGY),
            label(r"each stage has integral $0$; \ the limit has no Riemann integral", font_size=26,
                  color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        head = label(r"Dirichlet's function as a double limit of continuous functions", font_size=32).to_edge(UP,
                                                                                                         buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Here's a function from Part 3's museum, built as a limit. Take the cosine of m "
            "factorial pi x, raised to the power two n. <bookmark mark='b'/> As n grows, the curve collapses onto "
            "spikes at the points where m factorial times x is a whole number. <bookmark mark='c'/> Now let m grow "
            "too. The spikes multiply, and in the double limit we get Dirichlet's function: one at every rational, "
            "zero at every irrational. <bookmark mark='d'/> Every stage is continuous, and every limit in n has "
            "integral zero, but the final limit has no Riemann integral at all. The integral itself breaks under "
            "limits."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(labs[0]))
            vo.wait_until("b")
            cur, cl = curves[0], labs[0]
            for k in (1, 2):
                self.play(ReplacementTransform(cur, curves[k]), FadeTransform(cl, labs[k]), run_time=1.2)
                cur, cl = curves[k], labs[k]
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            for k in range(3, len(frames)):
                self.play(ReplacementTransform(cur, curves[k]), FadeTransform(cl, labs[k]), run_time=1.0)
                cur, cl = curves[k], labs[k]
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def escapes(self):
        W, H = 3.9, 2.6
        cx = (-4.55, 0.0, 4.55)
        cy = 0.15
        axs = [plain_axes([0, 4, 1], yr, W, H).move_to([c, cy, 0]) for c, yr in
               zip(cx, ([0, 8.4, 2], [0, 1.2, 0.5], [0, 1.2, 0.5]))]
        n1, n2, n3 = ValueTracker(1.0), ValueTracker(1.0), ValueTracker(1.0)
        x = np.linspace(0.0005, 4, 4000)

        def spike():
            n = n1.get_value()
            y = np.where(x <= 1 / n, n, 0.0)
            return VGroup(area_under(axs[0], x, np.minimum(y, 8.4), C.MEASURE, 0.45),
                          polyline(axs[0], x, np.minimum(y, 8.4), color=C.FUNC, stroke_width=3))

        def run():
            n = n2.get_value() - 1
            y = np.where((x >= n) & (x <= n + 1), 1.0, 0.0)
            return VGroup(area_under(axs[1], x, y, C.MEASURE, 0.45), polyline(axs[1], x, y, color=C.FUNC, stroke_width=3))

        def spread():
            n = n3.get_value()
            y = np.where(x <= n, 1 / n, 0.0)
            return VGroup(area_under(axs[2], x, y, C.MEASURE, 0.45), polyline(axs[2], x, y, color=C.FUNC, stroke_width=3))

        g1, g2, g3 = always_redraw(spike), always_redraw(run), always_redraw(spread)
        titles = VGroup(MathTex(r"n\,\mathbf 1_{(0, 1/n]}", font_size=30), MathTex(r"\mathbf 1_{[n-1, n]}", font_size=30),
                        MathTex(r"\tfrac1n \mathbf 1_{[0, n]}", font_size=30))
        names = VGroup(label(r"up: \ the spike", font_size=24, color=GREY_A),
                       label(r"sideways: \ the runaway", font_size=24, color=GREY_A),
                       label(r"thin: \ the spreading", font_size=24, color=GREY_A))
        for t_, nm, a in zip(titles, names, axs):
            t_.next_to(a, UP, buff=0.1)
            nm.next_to(a, DOWN, buff=0.15)
        verdict = VGroup(MathTex(r"\int f_n = 1 \text{ for every } n, \qquad f_n(x) \to 0 \text{ for every } x", font_size=32),
                         MathTex(r"\lim \int f_n = 1 \ne 0 = \int \lim f_n", font_size=34, color=C.PATHOLOGY)
                         ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        head = label(r"Three ways for mass to escape", font_size=34).to_edge(UP, buff=0.3)
        # the envelopes sup_n f_n: none is integrable
        xe = np.linspace(0.02, 4, 800)
        env1 = np.minimum(np.floor(1 / xe), 8.4)  # sup_n n 1_(0, 1/n](x) = floor(1/x)
        env2 = np.ones_like(xe)
        env3 = 1 / np.maximum(np.ceil(xe), 1)
        envs = VGroup(*[polyline(a, xe, e, color=C.EPS, stroke_width=3).set_stroke(opacity=0.9) for a, e in
                        zip(axs, (env1, env2, env3))])
        lid = label(r"a lid $g \ge |f_n|$ for all $n$ \ (yellow: the smallest) \ has $\int g = \infty$ in all three",
                    font_size=26, color=C.EPS).to_edge(DOWN, buff=0.3)
        # floor(1/x) >= 1/x - 1, whose integral diverges; 1 on [0, inf) diverges; 1/ceil(x) >= 1/(x + 1) diverges
        assert np.all(np.floor(1 / xe) >= 1 / xe - 1) and np.all(env3 >= 1 / (xe + 1))
        with self.voiceover(
            "<bookmark mark='a'/> The theme of this part is mass escaping. Here are three sequences of functions, each "
            "with integral exactly one. <bookmark mark='b'/> The first gets taller and narrower; the second slides off "
            "to the right; the third spreads thinner and thinner. <bookmark mark='c'/> At every single point, all "
            "three go to zero, so the limit has integral zero, while every function in the sequence has integral one. "
            "<bookmark mark='d'/> What would stop the escape is a lid: one integrable function lying above every "
            "function of the sequence. Here the smallest possible lids have infinite integral. Lebesgue's dominated "
            "convergence theorem will say that a lid is all you need."
        ) as vo:
            self.play(FadeIn(head), *[Create(a) for a in axs], FadeIn(titles), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(g3))
            vo.wait_until("b")
            self.play(n1.animate.set_value(8), n2.animate.set_value(4), n3.animate.set_value(4), run_time=5.0,
                      rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(verdict))
            vo.wait_until("d")
            self.play(FadeOut(verdict), Create(envs), run_time=1.5)
            self.play(FadeIn(lid))
        for m in (g1, g2, g3):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def slicing(self):
        ax = plain_axes([0, 1, 0.25], [0, 1.2, 0.5], 6.0, 3.6).move_to([-3.6, -0.3, 0])
        bx = plain_axes([0, 1, 0.25], [0, 1.2, 0.5], 6.0, 3.6).move_to([3.4, -0.3, 0])
        x = np.linspace(0, 1, 1601)
        f = 0.55 + 0.35 * np.sin(7 * x) * np.cos(2 * x) + 0.1 * np.sin(23 * x)
        fa, fb = polyline(ax, x, f, color=WHITE, stroke_width=3), polyline(bx, x, f, color=WHITE, stroke_width=3)
        edges = np.linspace(0, 1, 13)
        mids = (edges[:-1] + edges[1:]) / 2
        hts = 0.55 + 0.35 * np.sin(7 * mids) * np.cos(2 * mids) + 0.1 * np.sin(23 * mids)
        vstrips = VGroup(*[Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0], height=ax.c2p(0, h)[1] - ax.c2p(0, 0)[1],
                                     stroke_color=C.FUNC, stroke_width=1.2, fill_color=C.FUNC, fill_opacity=0.35)
                           .move_to(ax.c2p((a + b) / 2, h / 2)) for a, b, h in zip(edges[:-1], edges[1:], hts)])
        levels = np.arange(0.1, 1.05, 0.1)
        hbands = VGroup()
        sets = VGroup()
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.MEASURE), k / len(levels)) for k in range(len(levels))]
        for k, t in enumerate(levels):
            on = f > t
            runs_, start = [], None
            for i in range(len(x) + 1):
                o = i < len(x) and on[i]
                if o and start is None:
                    start = i
                elif not o and start is not None:
                    runs_.append((x[start], x[i - 1]))
                    start = None
            band = VGroup(*[Rectangle(width=bx.c2p(b, 0)[0] - bx.c2p(a, 0)[0], height=bx.c2p(0, 0.1)[1] - bx.c2p(0, 0)[1],
                                      stroke_width=0, fill_color=cols[k], fill_opacity=0.55)
                            .move_to(bx.c2p((a + b) / 2, t - 0.05)) for a, b in runs_])
            hbands.add(band)
            sets.add(interval_band(bx, runs_, bx.c2p(0, 0)[1] - 0.35 - 0.11 * k, cols[k], height=0.07))
        tl = VGroup(label(r"Riemann: \ slice the domain", font_size=26).next_to(ax, UP, buff=0.12),
                    label(r"Lebesgue: \ slice the range", font_size=26).next_to(bx, UP, buff=0.12))
        quote = label(r"``I have to pay a certain sum; I count the coins by value'' \ (Lebesgue, 1926)", font_size=24,
                      color=GREY_A).to_edge(UP, buff=0.25)
        honest = VGroup(label(r"the honest difference: \ each slice needs the length of $\{x : f(x) > t\}$,", font_size=26),
                        label(r"which can be any set at all \ (for Dirichlet's function: \ the rationals)", font_size=26,
                              color=C.EPS)).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "<bookmark mark='a'/> Lebesgue described his integral with a picture of counting money: rather than adding "
            "the coins in the order you meet them, sort them by value first. <bookmark mark='b'/> Riemann slices the "
            "domain into strips. <bookmark mark='c'/> Lebesgue slices the range into layers, and for each layer he "
            "needs the total length of the set where f exceeds that level. <bookmark mark='d'/> But the picture hides "
            "the real change. Those sets can be complicated: for Dirichlet's function, the set where it exceeds one "
            "half is the set of rationals. The new idea is a way to give a length to such sets, and the first chapter "
            "is about exactly that."
        ) as vo:
            self.play(FadeIn(quote))
            vo.wait_until("a")
            self.play(Create(ax), Create(bx), Create(fa), Create(fb))
            vo.wait_until("b")
            self.play(FadeIn(tl[0]), LaggedStart(*[FadeIn(s_, shift=UP * 0.1) for s_ in vstrips], lag_ratio=0.08),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(tl[1]), LaggedStart(*[FadeIn(b_) for b_ in hbands], lag_ratio=0.12), run_time=2.0)
            self.play(LaggedStart(*[TransformFromCopy(b_, s_) for b_, s_ in zip(hbands, sets)], lag_ratio=0.12),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(honest))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        chapters = [
            r"A length for every set", r"A set with no length", r"$\sigma$-algebras and measurable functions",
            r"Measures", r"The integral, and monotone convergence", r"Fatou's lemma", r"Dominated convergence",
            r"Every positive functional is an integral", r"Lebesgue measure, and Riemann revisited",
            r"Measurable is nearly continuous", r"Product measures and Fubini", r"Convolution and the layer cake",
        ]
        items = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=26) for i, t in enumerate(chapters)])
        col1 = VGroup(*items[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        col2 = VGroup(*items[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        cols = VGroup(col1, col2).arrange(RIGHT, buff=0.9, aligned_edge=UP).shift(DOWN * 0.4)
        head = label(r"Part 5: Measure and the Lebesgue integral", font_size=42).to_edge(UP, buff=0.45)
        sub = label(r"Rudin, \textit{Real and Complex Analysis}, chapters 1, 2 and 8; \ \textit{Principles}, chapter 11",
                    font_size=24, color=GREY_B).next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "The plan follows Rudin's Real and Complex Analysis. <bookmark mark='a'/> First, which sets can have a "
            "length, and why not all of them can. <bookmark mark='b'/> Then the integral and its three great limit "
            "theorems: monotone convergence, Fatou's lemma and dominated convergence. <bookmark mark='c'/> Then where "
            "measures come from, and how the new integral compares with Riemann's. <bookmark mark='d'/> And finally, "
            "integrals in several variables, Fubini's theorem, and convolution."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(4)], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(4, 7)], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(7, 10)], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(10, 12)], lag_ratio=0.3))
        self.wait(0.6)
        self.clear_scene()

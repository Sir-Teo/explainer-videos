from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis2.common import load, plain_axes, polyline


class Tests(VoiceoverScene):
    def construct(self):
        self.card()
        self.root_test()
        self.ratio_vs_root()
        self.power_series()
        self.hidden_poles()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"Root, ratio and power series", r"How do you compare a series with a geometric one?",
                            lit=(1821,), part=2)
        with self.voiceover(
            "Chapter six. The geometric series is the yardstick: the root and ratio tests are ways of laying a "
            "series against it."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def _log_axes(self, n_max=30):
        # y is log10 of the term, shifted up by 8 so the horizontal axis sits at 10^-8, along the bottom
        ax = plain_axes([0, n_max + 1, 5], [0, 8.5, 2], 10.6, 4.2, numbers=False).move_to([0.3, -1.25, 0])
        ticks = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=22, color=GREY_B).next_to(ax.c2p(0, k + 8), LEFT, buff=0.1)
                         for k in (-8, -6, -4, -2, 0)])
        nt = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
                      for k in (5, 10, 15, 20, 25, 30)])
        return ax, VGroup(ticks, nt)

    def root_test(self):
        d = load("tests")
        a = d["a"]
        n_max = 30
        thm = VGroup(label(r"\textbf{Root test} (Rudin 3.33) \ Let $\alpha = \limsup \sqrt[n]{|a_n|}$.", font_size=30),
                     label(r"$\alpha < 1$: \ converges; \qquad $\alpha > 1$: \ diverges; \qquad $\alpha = 1$: \ no "
                           r"information", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        ax, ticks = self._log_axes(n_max)
        n = np.arange(1, n_max + 1)
        dots = VGroup(*[Dot(ax.c2p(k, math.log10(a[k - 1]) + 8), radius=0.055, color=C.SEQ if k % 2 else C.FREQ)
                        for k in n])
        ex = MathTex(r"\tfrac12 + \tfrac13 + \tfrac1{2^2} + \tfrac1{3^2} + \tfrac1{2^3} + \tfrac1{3^3} + \cdots",
                     font_size=32).move_to([3.0, 1.15, 0])
        ex_r = note(r"Rudin 3.35(b); \ log scale").next_to(ex, DOWN, buff=0.1)
        beta = 0.75
        env = polyline(ax, np.array([0, n_max + 1]), np.array([8, 8 + (n_max + 1) * math.log10(beta)]), color=C.EPS,
                       stroke_width=3)
        env_l = MathTex(r"\beta^n,\ \beta = 0.75", font_size=28, color=C.EPS).next_to(
            ax.c2p(n_max * 0.62, 8 + n_max * 0.62 * math.log10(beta)), UR, buff=0.08)
        why_ = label(r"$\alpha < \beta < 1$: \ eventually $\sqrt[n]{|a_n|} < \beta$, \ i.e.\ $|a_n| < \beta^n$: "
                     r"\ compare with the geometric series", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The root test. <bookmark mark='t'/> Take the upper limit of the n-th roots of the terms, and call it "
            "alpha. If alpha is less than one, the series converges; if it's bigger than one, it diverges; if it's "
            "exactly one, the test says nothing. <bookmark mark='a'/> Here's a series from Rudin that interleaves powers "
            "of a half and of a third. On a logarithmic scale a geometric series is a straight line. "
            "<bookmark mark='b'/> The n-th roots approach one over root two at most, so choose beta between that and "
            "one: from some point on, every term lies under beta to the n, <bookmark mark='c'/> and comparison with the "
            "geometric series does the rest."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(ticks), FadeIn(ex), FadeIn(ex_r))
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.04))
            vo.wait_until("b")
            self.play(Create(env), FadeIn(env_l))
            vo.wait_until("c")
            self.play(FadeIn(why_))
        assert np.all(np.log10(a[:n_max]) < n * math.log10(beta))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ratio_vs_root(self):
        d = load("tests")
        ratios, roots = d["ratios"], d["roots"]
        n_max = 30
        thm = VGroup(label(r"\textbf{Ratio test} (Rudin 3.34) \ $\limsup \left|\tfrac{a_{n+1}}{a_n}\right| < 1$: "
                           r"converges; \ \ $\left|\tfrac{a_{n+1}}{a_n}\right| \ge 1$ from some $n$ on: diverges",
                           font_size=28),).to_edge(UP, buff=0.35)
        axl = plain_axes([0, n_max + 1, 10], [-6, 6, 2], 5.6, 3.6, numbers=False).move_to([-3.4, -0.55, 0])
        axr = plain_axes([0, n_max + 1, 10], [0, 1.2, 0.5], 5.6, 3.6, numbers=False).move_to([3.4, -0.55, 0])
        lt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(axl.c2p(0, k), LEFT, buff=0.08)
                      for k in (-6, 0, 6)])
        rt = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(axr.c2p(0, v), LEFT, buff=0.08)
                      for v in (0, 0.5, 1)])
        one_l = DashedLine(axl.c2p(0, 0), axl.c2p(n_max + 1, 0), color=WHITE, stroke_width=1.5)
        one_r = DashedLine(axr.c2p(0, 1), axr.c2p(n_max + 1, 1), color=WHITE, stroke_width=1.5)
        rd = VGroup(*[Dot(axl.c2p(k, np.clip(math.log10(ratios[k - 1]), -6, 6)), radius=0.05,
                          color=C.PATHOLOGY) for k in range(1, n_max + 1)])
        od = VGroup(*[Dot(axr.c2p(k, roots[k - 1]), radius=0.05, color=C.CONNECTED_SET) for k in range(1, n_max + 1)])
        tl = MathTex(r"\left|\tfrac{a_{n+1}}{a_n}\right|", font_size=30, color=C.PATHOLOGY).next_to(axl, UP, buff=0.1)
        tr = MathTex(r"\sqrt[n]{|a_n|}", font_size=30, color=C.CONNECTED_SET).next_to(axr, UP, buff=0.1)
        vl = label(r"$\to 0$ and $\to \infty$: \ the ratio test is silent", font_size=24, color=C.PATHOLOGY).next_to(
            axl, DOWN, buff=0.2)
        vr = label(r"$\limsup = 1/\sqrt2 < 1$: \ the root test proves convergence", font_size=24,
                   color=C.CONNECTED_SET).next_to(axr, DOWN, buff=0.2)
        with self.voiceover(
            "The ratio test compares consecutive terms instead. <bookmark mark='t'/> If the ratios are eventually below "
            "something less than one, the series converges. <bookmark mark='a'/> For the same series, the ratios jump "
            "between two thirds to the k, which goes to zero, and half of three halves to the k, which goes to "
            "infinity. The ratio test can't decide. <bookmark mark='b'/> But the n-th roots settle down, below one: the "
            "root test proves convergence."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(Create(axl), FadeIn(lt), Create(one_l), FadeIn(tl))
            self.play(LaggedStart(*[FadeIn(x) for x in rd], lag_ratio=0.04), FadeIn(vl))
            vo.wait_until("b")
            self.play(Create(axr), FadeIn(rt), Create(one_r), FadeIn(tr))
            self.play(LaggedStart(*[FadeIn(x) for x in od], lag_ratio=0.04), FadeIn(vr))
        chain = MathTex(r"\liminf \left|\tfrac{a_{n+1}}{a_n}\right| \le \liminf \sqrt[n]{|a_n|} \le \limsup "
                        r"\sqrt[n]{|a_n|} \le \limsup \left|\tfrac{a_{n+1}}{a_n}\right|", font_size=32, color=C.EPS)
        chain.to_edge(DOWN, buff=0.25)
        chain_n = note(r"Rudin 3.37: \ whenever the ratio test decides, the root test does too").next_to(chain, UP,
                                                                                                        buff=0.1)
        with self.voiceover(
            "<bookmark mark='c'/> This is no accident. The upper limit of the roots is always at most the upper limit "
            "of the ratios, so whenever the ratio test gives an answer, the root test gives the same one. The ratio "
            "test is just easier to compute."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeOut(vl), FadeOut(vr), FadeIn(chain), FadeIn(chain_n))
        assert ratios[::2].min() < 1e-6 and ratios[1::2].max() > 1e6
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def power_series(self):
        d = load("power")
        o = np.array([-3.3, -0.4, 0])
        u = 1.25

        def P(z):
            return o + u * np.array([z.real, z.imag, 0.0])

        plane = NumberPlane(x_range=[-2.6, 2.6, 1], y_range=[-2.4, 2.4, 1], x_length=5.2 * u, y_length=4.8 * u,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.5},
                            axis_config={"stroke_color": GREY_C}).move_to(o)
        disk = Circle(radius=u, stroke_color=C.EPS, stroke_width=3, fill_color=C.EPS, fill_opacity=0.1).move_to(o)
        disk_l = MathTex(r"|z| = R = 1", font_size=26, color=C.EPS).next_to(P(np.exp(0.25j * np.pi)), UR, buff=0.05)
        thm = VGroup(label(r"\textbf{Power series} (Rudin 3.39)", font_size=30),
                     MathTex(r"\sum c_n z^n, \quad R = \frac{1}{\limsup \sqrt[n]{|c_n|}}", font_size=34),
                     label(r"converges for $|z| < R$, \ diverges for $|z| > R$", font_size=26, color=GREY_A)
                     ).arrange(DOWN, buff=0.15).move_to([3.6, 2.4, 0])
        ex = MathTex(r"\sum_{n \ge 1} \frac{z^n}{n}: \quad c_n = \tfrac1n,\ \ \sqrt[n]{1/n} \to 1,\ \ R = 1", font_size=30)
        ex.next_to(thm, DOWN, buff=0.35)

        def path(key, n, color, rmax=2.35):
            s = np.concatenate([[0j], d[key][:n]])
            keep = np.where(np.abs(s) > rmax)[0]
            if len(keep):
                s = s[: keep[0]]
            m = VMobject(color=color, stroke_width=3)
            m.set_points_as_corners([P(z) for z in s])
            return m

        cases = [
            ("in", 400, C.CONNECTED_SET, r"|z| = 0.9: \ \text{converges to } -\log(1 - z)"),
            ("m1", 400, C.SEQ, r"z = -1: \ 1 - \tfrac12 + \tfrac13 - \cdots \text{ converges}"),
            ("p1", 4000, C.PATHOLOGY, r"z = 1: \ \text{the harmonic series diverges}"),
            ("out", 200, C.FREQ, r"|z| = 1.1: \ \text{terms grow; diverges}"),
        ]
        legend = VGroup(*[MathTex(t, font_size=26, color=c) for _, _, c, t in cases]).arrange(DOWN, aligned_edge=LEFT,
                                                                                              buff=0.22)
        legend.next_to(ex, DOWN, buff=0.4).align_to(thm, LEFT).shift(LEFT * 0.3)
        paths = [path(k, n, c) for k, n, c, _ in cases]
        lim = Dot(P(-np.log(1 - 0.9 * np.exp(0.8j))), radius=0.06, color=WHITE)
        with self.voiceover(
            "The root test's best use is power series, where z is a complex number. <bookmark mark='t'/> A power "
            "series converges inside a disk and diverges outside it; the radius is one over the upper limit of the "
            "n-th roots of the coefficients. <bookmark mark='e'/> For the sum of z to the n over n, the radius is one. "
            "Each picture is the path of partial sums in the plane. <bookmark mark='a'/> Inside the disk, the path "
            "spirals in to a limit. <bookmark mark='b'/> On the boundary anything can happen: at minus one it "
            "converges, to minus log two; <bookmark mark='c'/> at one it's the harmonic series, crawling off to "
            "infinity. <bookmark mark='d'/> Outside, the terms themselves grow, and the path spirals out."
        ) as vo:
            self.play(Create(plane), FadeIn(disk), FadeIn(disk_l))
            vo.wait_until("t")
            self.play(FadeIn(thm))
            vo.wait_until("e")
            self.play(FadeIn(ex))
            for mk, pth, leg in zip("abcd", paths, legend):
                vo.wait_until(mk)
                self.play(Create(pth), FadeIn(leg), run_time=1.8)
                if mk == "a":
                    self.play(FadeIn(lim))
        assert abs(d["m1"][-1] + math.log(2)) < 2e-4
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hidden_poles(self):
        ax = plain_axes([-2, 2, 1], [-1, 2, 1], 6.2, 4.0, numbers=True, font_size=20).move_to([-3.2, -0.7, 0])
        f = ax.plot(lambda x: 1 / (1 + x * x), x_range=[-2, 2], color=C.FUNC, stroke_width=4)
        f_l = MathTex(r"\frac{1}{1 + x^2}", font_size=32, color=C.FUNC).next_to(ax.c2p(-2, 1.6), RIGHT, buff=0.1)

        def taylor(N):
            def g(x):
                return sum((-x * x) ** k for k in range(N + 1))

            # draw only where the partial sum is inside the axes' range: the flailing leaves through the top
            x = np.linspace(-1.6, 1.6, 3201)
            y = g(x)
            ok = (y > -1.0) & (y < 2.0)
            runs, start = VGroup(), None
            for i in range(len(x) + 1):
                if i < len(x) and ok[i]:
                    start = i if start is None else start
                elif start is not None:
                    if i - start > 1:
                        runs.add(polyline(ax, x[start:i], y[start:i], color=C.APPROX, stroke_width=3))
                    start = None
            return runs

        series = MathTex(r"= 1 - x^2 + x^4 - x^6 + \cdots", font_size=32, color=C.APPROX).next_to(f_l, RIGHT, buff=0.1)
        Tn = taylor(2)
        Ts = [taylor(N) for N in (2, 4, 8, 16, 30)]
        wall = VGroup(DashedLine(ax.c2p(-1, -1), ax.c2p(-1, 2), color=C.PATHOLOGY, stroke_width=2),
                      DashedLine(ax.c2p(1, -1), ax.c2p(1, 2), color=C.PATHOLOGY, stroke_width=2))
        q = label(r"smooth on all of $\R$, \ so why stop at $|x| = 1$?", font_size=28).move_to([3.4, 2.7, 0])
        o = np.array([3.4, -0.7, 0])
        u = 1.3
        plane = NumberPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=4 * u, y_length=4 * u,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.5},
                            axis_config={"stroke_color": GREY_C}).move_to(o)
        disk = Circle(radius=u, stroke_color=C.EPS, stroke_width=3, fill_color=C.EPS, fill_opacity=0.1).move_to(o)
        poles = VGroup(*[VGroup(Cross(scale_factor=0.12, stroke_color=C.PATHOLOGY, stroke_width=5).move_to(o + u * s * UP),
                                MathTex(t, font_size=28, color=C.PATHOLOGY).next_to(o + u * s * UP, RIGHT, buff=0.15))
                         for s, t in ((1, r"i"), (-1, r"-i"))])
        real = Line(o + LEFT * 2 * u, o + RIGHT * 2 * u, color=C.FUNC, stroke_width=5)
        ans = label(r"$1 + z^2 = 0$ at $z = \pm i$: \ the disk can't reach past them", font_size=26,
                    color=C.PATHOLOGY).next_to(plane, DOWN, buff=0.2)
        fwd = VGroup(label(r"The real line can't see why.", font_size=24, color=C.EPS),
                     label(r"Part 7: power series live in $\mathbb{C}$.", font_size=24, color=C.EPS)
                     ).arrange(DOWN, buff=0.08).next_to(ax, DOWN, buff=0.3)
        with self.voiceover(
            "One last puzzle. <bookmark mark='a'/> One over one plus x squared is as smooth as a function can be, on "
            "the whole real line. Its power series is one minus x squared plus x to the fourth, and so on. "
            "<bookmark mark='b'/> But the series only converges between minus one and one: past that, the partial sums "
            "flail. <bookmark mark='q'/> Nothing happens to the function at x equal to one. So why stop there? "
            "<bookmark mark='c'/> Look in the complex plane. The function blows up at i and at minus i, where one plus "
            "z squared is zero, and a disk centered at zero can't grow past them. Its radius is one, and the real "
            "interval is just the disk's shadow. <bookmark mark='d'/> The real line can't see the reason. We'll come "
            "back to this in Part 7, where power series turn out to live naturally in the complex plane."
        ) as vo:
            self.play(Create(ax), Create(f), FadeIn(f_l), FadeIn(series))
            vo.wait_until("b")
            self.play(Create(Tn))
            for T in Ts[1:]:
                self.play(Transform(Tn, T), run_time=0.7)
            self.play(Create(wall))
            vo.wait_until("q")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(Create(plane), Create(real))
            self.play(FadeIn(poles), FadeIn(disk), FadeIn(ans))
            vo.wait_until("d")
            self.play(FadeIn(fwd))
        self.wait(0.5)
        self.clear_scene()

from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis9.common import bump, load, plain_axes, polyline


class Sobolev(VoiceoverScene):
    def construct(self):
        self.card()
        self.decay()
        self.lemma()
        self.sawtooth()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(10, r"Sobolev spaces", r"How smooth is a function whose transform decays?", lit=(1945,), part=9)
        with self.voiceover("Chapter ten: Sobolev spaces, where smoothness is measured by the transform."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def decay(self):
        d = load("decay")
        t, box, tri, bmp = d["t"], d["box"], d["tri"], d["bump"]
        lt = np.log10(t)
        ax = plain_axes([0, 2.4, 0.5], [-8, 0, 2], 6.4, 4.2, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([2.6, -0.2, 0])
        xl = MathTex(r"\log_{10} t", font_size=22).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = MathTex(r"\log_{10} |\hat f|", font_size=22).next_to(ax.y_axis, UP, buff=0.1)
        cols = [C.PATHOLOGY, C.APPROX, C.TEST_FN]
        curves = [polyline(ax, lt, np.log10(v), color=c, stroke_width=4) for v, c in zip((box, tri, bmp), cols)]
        tags = VGroup(
            MathTex(r"\sim 1/t", font_size=24, color=cols[0]).next_to(ax.c2p(2.4, math.log10(box[-1])), RIGHT, buff=0.1),
            MathTex(r"\sim 1/t^2", font_size=24, color=cols[1]).next_to(ax.c2p(2.4, math.log10(tri[-1])), RIGHT, buff=0.1),
            MathTex(r"\text{faster than } t^{-N}", font_size=24, color=cols[2]).next_to(ax.c2p(2.0, -7.2), RIGHT, buff=0.1),
        )
        slopes = [np.polyfit(lt[200:], np.log10(v[200:]), 1)[0] for v in (box, tri)]
        assert abs(slopes[0] + 1) < 1e-9 and abs(slopes[1] + 2) < 1e-9 and bmp[-1] < 1e-6
        # the three functions, small, in a column on the left
        x = np.linspace(-2, 2, 801)
        fs = [np.where(np.abs(x) <= 1, 1.0, 0.0), np.clip(1 - np.abs(x), 0, None), bump(x) / bump(np.array([0.0]))[0]]
        names = [r"\text{box: a jump}", r"\text{triangle: a kink}", r"\text{bump: } C^\infty"]
        hs = [r"H^s \iff s < \tfrac12", r"H^s \iff s < \tfrac32", r"H^s \text{ for every } s"]
        small = VGroup()
        for k, (fx, nm, h, c) in enumerate(zip(fs, names, hs, cols)):
            a = plain_axes([-2, 2, 1], [0, 1.2, 1], 2.4, 0.9).move_to([-5.3, 1.7 - 1.65 * k, 0])
            if k == 0:
                g = VGroup(Line(a.c2p(-2, 0), a.c2p(-1, 0), color=c, stroke_width=3),
                           Line(a.c2p(-1, 1), a.c2p(1, 1), color=c, stroke_width=3),
                           Line(a.c2p(1, 0), a.c2p(2, 0), color=c, stroke_width=3))
            else:
                g = polyline(a, x, fx, color=c, stroke_width=3)
            n_ = MathTex(nm, font_size=22, color=c).next_to(a, UP, buff=0.04)
            h_ = MathTex(h, font_size=22, color=c).next_to(a, RIGHT, buff=0.15)
            small.add(VGroup(a, g, n_, h_))
        norm = MathTex(r"\|f\|_{H^s}^2 = \int (1 + t^2)^s\, |\hat f(t)|^2\, dt", font_size=30, color=C.EPS).to_edge(
            UP, buff=0.95).shift(RIGHT * 2.6)
        head = label(r"Smoothness, \ read off the transform", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Differentiating multiplies the transform by i t, so smoothness in space is decay in "
            "frequency. On a log-log plot: <bookmark mark='b'/> a box, which jumps, has a transform decaying like one "
            "over t. <bookmark mark='c'/> A triangle, which only has kinks, decays like one over t squared. "
            "<bookmark mark='d'/> And the smooth bump plunges faster than any power. <bookmark mark='e'/> The Sobolev "
            "norm turns this into a scale: weight the transform by one plus t squared to the power s. The box has "
            "finite norm exactly for s below one half, the triangle for s below three halves, the bump for every s. "
            "And s needn't be a whole number."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            for k, mk in enumerate(("b", "c", "d")):
                vo.wait_until(mk)
                self.play(Create(small[k][0]), Create(small[k][1]), FadeIn(small[k][2]), Create(curves[k]),
                          FadeIn(tags[k]), run_time=1.5)
            vo.wait_until("e")
            self.play(Write(norm))
            self.play(LaggedStart(*[FadeIn(s_[3]) for s_ in small], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lemma(self):
        ax = plain_axes([0, 6, 1], [0, 40, 10], 5.6, 3.0, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.5, 0.5, 0])
        xl = MathTex(r"\log_{10} T", font_size=22).next_to(ax.x_axis, DOWN, buff=0.35)
        ss = [0.4, 0.5, 0.6]
        cols = [C.PATHOLOGY, C.EPS, C.TEST_FN]

        def partial(s, T):
            # int_{-T}^{T} (1 + t^2)^(-s) dt, with t = sinh w: 2 int_0^asinh T cosh(w)^(1 - 2s) dw
            w = np.linspace(0, math.asinh(T), 20001)
            g = np.cosh(w) ** (1 - 2 * s)
            return float(np.sum((g[1:] + g[:-1]) * np.diff(w)))

        Lg = np.linspace(0, 6, 241)
        vals = {s: np.array([partial(s, 10**L) for L in Lg]) for s in ss}
        # s = 0.6 converges to sqrt(pi) Gamma(0.1) / Gamma(0.6) (the tail past T is 10 T^-0.2); s = 0.5 is 2 asinh T
        lim6 = math.sqrt(math.pi) * math.gamma(0.1) / math.gamma(0.6)
        assert abs(vals[0.6][-1] + 10 * 1e6**-0.2 - lim6) < 0.01 and abs(vals[0.5][-1] - 2 * math.asinh(1e6)) < 1e-6
        LT = ValueTracker(0.0)

        def pics():
            m = Lg <= LT.get_value() + 1e-9
            return VGroup(*[runs(ax, Lg[m], vals[s][m], c, 3.5) for s, c in zip(ss, cols)])

        gr = always_redraw(pics)
        rd = always_redraw(lambda: VGroup(*[MathTex(
            rf"s = {s}: \ \int_{{-T}}^{{T}}(1 + t^2)^{{-s}}dt = {partial(s, 10 ** LT.get_value()):.3f}", font_size=24,
            color=c) for s, c in zip(ss, cols)]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, DOWN, buff=0.6))
        lim = DashedLine(ax.c2p(0, lim6), ax.c2p(6, lim6), color=C.TEST_FN, stroke_width=2)
        liml = MathTex(rf"\sqrt\pi\,\Gamma(0.1)/\Gamma(0.6) = {lim6:.3f}", font_size=20, color=C.TEST_FN).next_to(
            ax.c2p(0.2, lim6), UP, buff=0.06).align_to(ax.c2p(0.2, 0), LEFT)
        lad = VGroup(
            MathTex(r"|f(x)| \le \tfrac{1}{\sqrt{2\pi}}\int |\hat f(t)|\,dt", font_size=28),
            MathTex(r"= \tfrac{1}{\sqrt{2\pi}}\int (1 + t^2)^{-s/2} \cdot (1 + t^2)^{s/2}|\hat f(t)|\,dt", font_size=28),
            MathTex(r"\le \tfrac{1}{\sqrt{2\pi}}\Big(\int (1 + t^2)^{-s}\,dt\Big)^{1/2}\,\|f\|_{H^s}", font_size=28,
                    color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.5, 1.1, 0])
        why = label(r"Cauchy--Schwarz, \ in frequency", font_size=22, color=GREY_A).next_to(lad, DOWN, buff=0.15)
        rows = VGroup(
            label(r"finite exactly when $2s > 1$: \ then $H^s \subset C_0$", font_size=24, color=C.TEST_FN),
            label(r"\textbf{FA 7.25} \ (Sobolev) \ in $\mathbb R^n$: \ $s > k + \tfrac n2$ $\Rightarrow$ $H^s \subset C^k$",
                  font_size=24, color=C.EPS),
            label(r"in $n$ dimensions $\int (1 + |\xi|^2)^{-s} d\xi$ needs $2s > n$: \ the dimension costs smoothness",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(why, DOWN, buff=0.3)
        head = label(r"Sobolev's lemma, \ in three lines", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> When does a finite Sobolev norm force a function to be continuous? The inversion "
            "formula bounds f by the integral of the size of f hat. <bookmark mark='b'/> Split the integrand into a "
            "weight and the rest, and apply Cauchy-Schwarz, in frequency. The Sobolev norm appears, times the "
            "integral of the weight. <bookmark mark='c'/> That integral is finite only when s is more than a half. "
            "Watch it as the cutoff T runs out: at s equal to 0.4 it grows without bound, at one half it grows like a "
            "logarithm, and at 0.6 it settles. <bookmark mark='d'/> So in one dimension, H s functions are continuous "
            "once s passes one half. In n dimensions the weight's integral needs two s bigger than n, and each extra "
            "half derivative buys one continuous derivative."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(lad[0]))
            vo.wait_until("b")
            self.play(FadeIn(lad[1]))
            self.play(FadeIn(lad[2]), FadeIn(why))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl), FadeIn(rd))
            self.add(gr)
            self.play(LT.animate.set_value(6.0), run_time=5.0, rate_func=linear)
            self.play(Create(lim), FadeIn(liml), FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1:]))
        for m in (rd, gr):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sawtooth(self):
        d = load("sobolev")
        ss, cps, sums, inc = d["ss"], d["checkpoints"], d["sums"], d["inc"]
        n = np.arange(1, 10**6 + 1, dtype=float)
        Ns = np.unique(np.geomspace(10, 10**6, 120).astype(int))
        cols = [C.TEST_FN, C.APPROX, C.EPS, C.PATHOLOGY]
        ax = plain_axes([1, 6, 1], [0, 32, 8], 6.2, 3.8, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.2, -0.4, 0])
        xl = MathTex(r"\log_{10} N", font_size=22).next_to(ax.x_axis, DOWN, buff=0.35)
        curves, tags = [], []
        for s, c, row in zip(ss, cols, sums):
            cs = np.cumsum((1 + n * n) ** s / n**2)
            assert np.allclose(cs[cps - 1], row)
            curves.append(polyline(ax, np.log10(Ns), cs[Ns - 1], color=c, stroke_width=3.5))
            tags.append(MathTex(rf"s = {s:g}", font_size=24, color=c).next_to(ax.c2p(6, cs[-1]), RIGHT, buff=0.1))
        top = MathTex(r"\sum_{n \le N} (1 + n^2)^s\, \Big|\frac1n\Big|^2", font_size=28).next_to(ax, UP, buff=0.1)
        ratios = inc[:, 1:] / inc[:, :-1]
        tab = VGroup(MathTex(r"s", r"\quad \text{gain per decade, ratio}", r"\quad 10^{2s - 1}", font_size=22,
                             color=GREY_A))
        for s, r_, c in zip(ss, ratios, cols):
            tab.add(MathTex(f"{s:g}", rf"\quad {r_.mean():.3f}", rf"\quad {10 ** (2 * s - 1):.3f}", font_size=24,
                            color=c))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.6, 1.3, 0])
        for row in tab[1:]:
            row[1].align_to(tab[0][1], LEFT)
            row[2].align_to(tab[0][2], LEFT)
        assert np.allclose(ratios.mean(axis=1), 10 ** (2 * ss - 1), rtol=0.03)
        rows = VGroup(
            label(r"the sawtooth $\sum \sin(nx)/n$ has coefficients $1/n$:", font_size=22),
            label(r"in $H^s$ \ $\iff$ \ $\sum (1 + n^2)^s/n^2 < \infty$ \ $\iff$ \ $s < \tfrac12$", font_size=24,
                  color=C.EPS),
            label(r"at $s = \tfrac12$ each decade adds $\log 10 = 2.3026$: \ a logarithm", font_size=22, color=GREY_A),
            label(r"sharp: \ $s > \tfrac12$ would make it continuous, \ and it jumps", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(tab, DOWN, buff=0.35)
        head = label(r"The sawtooth sits exactly at $s = \tfrac12$", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The Fourier thread once more. The sawtooth's coefficients are one over n, so its "
            "Sobolev norm is this sum. <bookmark mark='b'/> Summed to a million terms: at s equal to 0.3 and 0.45 the "
            "sums level off, each decade adding a fixed fraction of the last one; at one half, every decade adds "
            "exactly the log of ten; above one half, the gains grow. <bookmark mark='c'/> So the sawtooth is in H s "
            "exactly for s below one half. And that's sharp, because above one half, Sobolev's lemma would make it "
            "continuous, and it jumps."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(top), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in curves], lag_ratio=0.3), run_time=3.0)
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tags], lag_ratio=0.2), FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(rows[1:3]))
            self.play(FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()

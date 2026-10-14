from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import area_under, interval_band, layer_cake, load, plain_axes, polyline
from videos.analysis5.compute import trap


class Convolution(VoiceoverScene):
    def construct(self):
        self.card()
        self.slide()
        self.young()
        self.fourier()
        self.layer_cake()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(12, r"Convolution and the layer cake", r"Averaging a function against another", lit=(),
                            part=5)
        with self.voiceover("Chapter twelve: convolution, and one last look at slicing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def slide(self):
        x = np.linspace(-3, 3, 2401)
        dx = x[1] - x[0]
        f = np.where(np.abs(x) < 1.6, 1.0, 0.0) * (0.6 + 0.4 * np.sign(np.sin(3 * x)))
        g = np.exp(-x * x / 0.08)
        g /= g.sum() * dx
        h = np.convolve(f, g, mode="same") * dx
        ax = plain_axes([-3, 3, 1], [0, 1.6, 0.5], 9.0, 3.6).move_to([-0.8, -0.6, 0])
        fg = polyline(ax, x, f, color=WHITE, stroke_width=3)
        xT = ValueTracker(-2.6)

        def kern():
            x0 = xT.get_value()
            k = np.exp(-(x - x0) ** 2 / 0.08)
            k = k / k.max() * 1.4
            return VGroup(polyline(ax, x, k, color=C.APPROX, stroke_width=2.5),
                          DashedLine(ax.c2p(x0, 0), ax.c2p(x0, 1.6), color=C.APPROX, stroke_width=1.5))

        kg = always_redraw(kern)
        trace = always_redraw(lambda: polyline(ax, x[x <= xT.get_value()], h[x <= xT.get_value()], color=C.EPS,
                                               stroke_width=4) if xT.get_value() > -2.55 else VMobject())
        head = VGroup(label(r"Convolution", font_size=34),
                      MathTex(r"(f * g)(x) = \int f(x - y)\, g(y)\,dy", font_size=34),
                      label(r"a $g$-weighted average of $f$ around $x$ \ (RCA 8.13--8.14; \ Part 3's Landau kernel)",
                            font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)

        def swatch(tex, color):
            return VGroup(Line(ORIGIN, RIGHT * 0.45, color=color, stroke_width=4),
                          MathTex(tex, font_size=30, color=color)).arrange(RIGHT, buff=0.12)

        # f and f * g named in a key above the plot (the sliding kernel sweeps every point under the plot's top);
        # g's name rides on the kernel
        key = VGroup(swatch("f", WHITE), swatch("f * g", C.EPS)).arrange(RIGHT, buff=0.5)
        key.next_to(ax, UP, buff=0.15).align_to(ax, RIGHT)
        labs = VGroup(key[0],
                      always_redraw(lambda: MathTex("g", font_size=30, color=C.APPROX).next_to(
                          ax.c2p(xT.get_value() + 0.12, 1.4), RIGHT, buff=0.05)),
                      key[1])
        assert key.get_bottom()[1] > ax.c2p(0, 1.6)[1] and key.get_top()[1] < head.get_bottom()[1] - 0.1
        with self.voiceover(
            "<bookmark mark='a'/> Convolution averages one function against another. At each point x, weight the "
            "values of f near x by a bump g, and add. <bookmark mark='b'/> Slide the bump along: the averages trace a "
            "smoothed copy of f. This is Part 3's Landau construction, now for any integrable f."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(fg), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(FadeIn(kg), FadeIn(labs[1]))
            vo.wait_until("b")
            self.add(trace)
            # stop at 2.3: the kernel's tail is then still inside the axes (it ends at x = 3)
            self.play(xT.animate.set_value(2.3), FadeIn(labs[2]), run_time=6.0, rate_func=linear)
        for m in (kg, trace, labs[1]):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def young(self):
        d = load("convolution")
        ratios = d["ratios"]
        rows = [
            MathTex(r"\int |f * g|", r"\le", r"\int\!\!\int |f(x - y)|\,|g(y)|\,dy\,dx", font_size=34),
            MathTex(r"\int |f * g|", r"\le", r"\int |g(y)| \Big(\int |f(x - y)|\,dx\Big) dy", font_size=34),
            MathTex(r"\|f * g\|_1", r"\le", r"\|f\|_1\, \|g\|_1", font_size=38),
        ]
        whys = [why(r"the triangle inequality, \ inside"), why(r"Tonelli: \ swap the order"),
                why(r"translation invariance")]
        step = ladder(self, rows, whys, keep=3, top=2.35, buff=0.38, x=-1.6)
        head = VGroup(label(r"$f, g \in L^1$ $\Rightarrow$ $f * g$ is defined a.e., \ and in $L^1$", font_size=34),
                      note(r"(RCA 8.14)")).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.3)
        # one signed pair, drawn: cancellation makes the inequality strict
        xs = np.linspace(-4, 4, 3201)
        dx = xs[1] - xs[0]
        f1 = np.sin(2 * xs) * np.exp(-xs**2 / 2)
        g1 = np.clip(1 - np.abs(xs) / 0.7, 0, None)
        h1 = np.convolve(f1, g1, mode="same") * dx
        nf, ng, nh = trap(np.abs(f1), xs), trap(np.abs(g1), xs), trap(np.abs(h1), xs)
        assert abs(ng - 0.7) < 1e-4 and nh <= nf * ng
        px = plain_axes([-4, 4, 1], [-1, 1, 1], 6.4, 2.0).move_to([-3.4, -2.55, 0])
        pic = VGroup(px, polyline(px, xs, f1, color=WHITE, stroke_width=2.5),
                     polyline(px, xs, g1, color=C.APPROX, stroke_width=2.5),
                     polyline(px, xs, h1, color=C.EPS, stroke_width=3.5))
        pk = VGroup(MathTex(rf"\|f\|_1 = {nf:.4f}", font_size=24), MathTex(rf"\|g\|_1 = {ng:.4f}", font_size=24,
                                                                              color=C.APPROX),
                    MathTex(rf"\|f * g\|_1 = {nh:.4f} \le {nf * ng:.4f}", font_size=24, color=C.EPS)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(px, RIGHT, buff=0.35)
        out = MathTex(rf"\text{{20 random pairs: }} \ \frac{{\|f * g\|_1}}{{\|f\|_1 \|g\|_1}} \le {ratios.max():.4f}",
                      font_size=30, color=C.EPS).next_to([0.9, -1.3, 0], RIGHT, buff=0)
        assert ratios.max() <= 1 + 1e-6
        with self.voiceover(
            "<bookmark mark='a'/> Is the convolution of two integrable functions integrable? The proof is Fubini at "
            "work. Bound the integral of the absolute value by a double integral, <bookmark mark='b'/> swap the order, "
            "which Tonelli allows for non-negative functions, <bookmark mark='c'/> and the inner integral is just the "
            "integral of f, shifted. The norm of a convolution is at most the product of the norms. "
            "<bookmark mark='d'/> Checked on twenty random pairs."
        ) as vo:
            self.play(FadeIn(head), Create(pic[0]), Create(pic[1]), Create(pic[2]), FadeIn(pk[:2]))
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                step(i)
            self.play(Create(pic[3]), FadeIn(pk[2]))
            vo.wait_until("d")
            self.play(FadeIn(out))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fourier(self):
        d = load("convolution")
        termwise, exact, sups, si = float(d["termwise"]), float(d["exact"]), d["sups"], float(d["si_pi"])
        ax = plain_axes([0, 2 * np.pi, np.pi / 2], [-2.1, 2.1, 1], 6.8, 3.4).move_to([-3.1, 0.0, 0])
        x = np.linspace(1e-3, 2 * np.pi - 1e-3, 2000)
        n = np.arange(1, 61)
        s60 = (np.sin(np.outer(n, x)) / n[:, None]).sum(axis=0)
        sg = polyline(ax, x, s60, color=C.APPROX, stroke_width=2.5)
        lid = VGroup(DashedLine(ax.c2p(0, 2), ax.c2p(2 * np.pi, 2), color=C.EPS, stroke_width=2.5),
                     DashedLine(ax.c2p(0, -2), ax.c2p(2 * np.pi, -2), color=C.EPS, stroke_width=2.5))
        ll = MathTex(r"|s_N| \le 2", font_size=28, color=C.EPS).next_to(ax.c2p(4.5, 2), UP, buff=0.05)
        shade = area_under(ax, x[x <= 1], s60[x <= 1], C.MEASURE, 0.45)
        head = VGroup(label(r"Part 3's opening question, answered", font_size=34),
                      MathTex(r"\int_0^1 \sum_{k \ge 1} \frac{\sin kt}{k}\,dt \overset{?}{=} "
                              r"\sum_{k \ge 1} \int_0^1 \frac{\sin kt}{k}\,dt", font_size=34)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        rows = VGroup(
            label(r"the partial sums are bounded:", font_size=26),
            MathTex(rf"\sup_{{N, x}} |s_N(x)| = \text{{Si}}(\pi) = {si:.4f} < 2", font_size=30),
            label(r"so the constant $2$ is a lid on $[0, 1]$: \ dominated convergence", font_size=26, color=C.EPS),
            MathTex(rf"\sum_k \frac{{1 - \cos k}}{{k^2}} = {termwise:.6f}", font_size=30, color=C.MEASURE),
            MathTex(rf"\int_0^1 \frac{{\pi - t}}{{2}}\,dt = \frac{{\pi}}{{2}} - \frac14 = {exact:.6f}", font_size=30,
                    color=C.MEASURE),
            label(r"term-by-term integration: \ legal", font_size=26, color=C.CONNECTED_SET),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.7, -0.7, 0])
        for r_ in rows:
            if r_.width > 6.0:
                r_.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.7, -0.7, 0])
        assert np.all(sups < 2) and np.all(sups <= si + 1e-9) and abs(termwise - exact) < 1e-5
        with self.voiceover(
            "<bookmark mark='a'/> And now the question that opened Part 3: may the sawtooth series be integrated term "
            "by term? <bookmark mark='b'/> Its partial sums never exceed the sine integral of pi, about 1.85, at any "
            "point, for any N. So on the interval from zero to one, the constant two is a lid, <bookmark mark='c'/> "
            "and dominated convergence makes the swap legal. Integrating term by term gives the sum of one minus "
            "cosine k over k squared; integrating the sawtooth itself gives pi over two minus a quarter. "
            "<bookmark mark='d'/> They agree to six decimal places. The convergence is not uniform, there's a jump, "
            "and it doesn't matter: a lid is enough."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(sg))
            vo.wait_until("b")
            self.play(Create(lid), FadeIn(ll), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(shade))
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def layer_cake(self):
        d = load("convolution")
        x, f, ts, mu, lhs, rhs = d["x"], d["f"], d["ts"], d["mu"], float(d["lhs"]), float(d["rhs"])
        ax = plain_axes([-3, 3, 1], [0, 5.0, 1], 6.4, 3.6).move_to([-3.4, -0.6, 0])
        m = np.abs(x) <= 3
        fg = polyline(ax, x[m], f[m], color=WHITE, stroke_width=3)
        dt = f.max() / 10
        # ten layers, each over the level set of its midpoint height (an upper sum from t = 0 would lay a full-width
        # slab of height dt under the whole window, area 5.2 for an integral of 3.44)
        layers = layer_cake(ax, x, f, dt, n=10, mask=m)
        assert abs(layers.area - lhs) < 0.02 * lhs
        # the right panel turned on its side: t vertical on the left panel's scale, m{f > t} horizontal, so each
        # layer's pieces slide over end to end into a bar of length m{f > t} at the same height
        bx = plain_axes([0, 4, 1], [0, 5, 1], 4.0, 3.6).move_to([3.4, -0.6, 0])
        assert abs((bx.c2p(0, 1)[1] - bx.c2p(0, 0)[1]) - (ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1])) < 1e-9
        bars = VGroup()
        for k, rr in enumerate(layers.runs):
            u0, bar = 0.0, VGroup()
            for a_, b_ in rr:
                lo_, hi_ = layers.lo[k], layers.hi[k]
                bar.add(Rectangle(width=bx.c2p(u0 + b_ - a_, 0)[0] - bx.c2p(u0, 0)[0],
                                  height=bx.c2p(0, hi_)[1] - bx.c2p(0, lo_)[1], stroke_width=0.5, stroke_color=BLACK,
                                  fill_color=layers.cols[k], fill_opacity=0.55).move_to(
                    bx.c2p(u0 + (b_ - a_) / 2, (lo_ + hi_) / 2)))
                u0 += b_ - a_
            assert abs(u0 - layers.widths[k]) < 1e-12 and len(bar) == len(layers[k])
            bars.add(bar)
        # the curve t -> m{f > t}, sideways; it runs off the right edge only as t -> 0 (m{f > 0} is the whole window)
        keep = mu <= 4.0
        t_in = float(np.interp(4.0, mu[::-1], ts[::-1]))
        assert np.all(np.diff(mu) <= 0) and np.all(np.diff(keep.astype(int)) >= 0) and t_in < 0.02
        cpts = [(4.0, t_in)] + [(a_, b_) for a_, b_ in zip(mu[keep], ts[keep])]
        mg = VMobject(color=C.MEASURE, stroke_width=3).set_points_as_corners([bx.c2p(a_, b_) for a_, b_ in cpts])
        mshade = Polygon(bx.c2p(0, t_in), *[bx.c2p(a_, b_) for a_, b_ in cpts], bx.c2p(0, ts[-1]), stroke_width=0,
                         fill_color=C.MEASURE, fill_opacity=0.25)
        bl = MathTex(r"m\{f > t\} \text{ at height } t", font_size=28, color=C.MEASURE).next_to(bx, UP, buff=0.1)
        head = VGroup(label(r"The layer cake", font_size=34),
                      MathTex(r"\int f\,dm = \int_0^\infty m\{f > t\}\,dt", r"\quad \text{\small (RCA 8.16)}",
                              font_size=36, color=C.EPS)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        head[1][1].set_color(GREY_B)
        nums = MathTex(rf"\int f = {lhs:.5f}, \qquad \int_0^\infty m\{{f > t\}}\,dt = {rhs:.5f}", font_size=30)
        nums.to_edge(DOWN, buff=0.3)
        assert abs(lhs - rhs) < 1e-4
        with self.voiceover(
            "<bookmark mark='a'/> Finally, Lebesgue's coins as a theorem: the layer cake formula. The integral of a "
            "non-negative function is the integral, over all heights t, of the measure of the set where f exceeds t. "
            "<bookmark mark='b'/> Slice the area into horizontal layers; <bookmark mark='c'/> each layer's width is "
            "the measure of a level set, and as a function of t, those widths have the same total area. It's "
            "Tonelli's theorem, applied to the region under the graph."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(fg))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in layers], lag_ratio=0.12), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(bl))
            self.play(LaggedStart(*[TransformFromCopy(l_, b_) for l_, b_ in zip(layers, bars)], lag_ratio=0.15),
                      run_time=2.5)
            self.play(Create(mg), FadeIn(mshade))
            self.play(FadeIn(nums))
        self.wait(0.4)
        self.clear_scene()

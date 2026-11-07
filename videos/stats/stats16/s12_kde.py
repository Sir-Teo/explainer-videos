from __future__ import annotations

import numpy as np

from videos.stats.stats16.common import *  # noqa: F403


def height_axes(center, x_length=8.4, y_length=3.8, ymax=0.05, font_size=20, xlabel=r"height, \ cm"):
    return axes([140, 205], [0, ymax], x_length=x_length, y_length=y_length, xlabel=xlabel, ylabel=r"density",
                xticks=[150, 165, 180, 195], yticks=[0, 0.02, 0.04], center=list(center), font_size=font_size)


class Density(VoiceoverScene):
    def construct(self):
        self.card()
        self.histograms()
        self.bumps()
        self.bandwidth()
        self.tradeoff()
        self.choosing()

    def card(self):
        card = chapter_card(11, r"Density estimates, \ a first look", r"A histogram without the bins", part=PART)
        with self.voiceover("Chapter eleven. Density estimates, a first look."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def histograms(self):
        d = load("kde")
        x = np.asarray(d["x"])
        A = height_axes([-3.4, 0.8, 0], x_length=5.8, y_length=3.4, font_size=18)
        B = height_axes([3.4, 0.8, 0], x_length=5.8, y_length=3.4, font_size=18)
        e1 = np.arange(130, 221, 10.0)
        e2 = np.arange(135, 226, 10.0)
        h1 = hist_bars(A.ax, e1, np.histogram(x, e1)[0] / (60 * 10), color=DATA, opacity=0.8)
        h2 = hist_bars(B.ax, e2, np.histogram(x, e2)[0] / (60 * 10), color=DATA, opacity=0.8)
        ta = label(r"bins starting at 140", font_size=20).next_to(A, UP, buff=0.12)
        tb = label(r"the same bins, \ shifted 5 cm", font_size=20).next_to(B, UP, buff=0.12)
        rows = fit_rows(VGroup(
            label(r"60 heights from the World: \ same data, \ same bin width, \ two shapes", font_size=24),
            label(r"a histogram depends on where the bins start, \ and it's a staircase", font_size=22, color=RES),
        ), 12.4, 0.25, [0, -2.4, 0])
        tag = simulated_tag(r"the World: \ 60 adults", corner=DR)
        with self.voiceover(
            "Everything in this part has avoided assuming a shape for the distribution. The last chapter estimates the shape "
            "itself. <bookmark mark='a'/> Here are sixty heights from the World, as a histogram with ten-centimetre bins. "
            "<bookmark mark='b'/> And here are the same sixty heights, with the same bin width, the bins just shifted by five "
            "centimetres. The peak has moved, and its shape has changed. <bookmark mark='c'/> A histogram depends on an "
            "arbitrary choice of where the bins start, and it's a staircase, where a smooth density may be a useful approximation."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ta), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in h1], lag_ratio=0.1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(tb), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in h2], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def bumps(self):
        d = load("kde")
        x = np.asarray(d["x"])
        A = height_axes([-1.2, 0.4, 0], x_length=9.4, y_length=4.4)
        ax = A.ax
        ks = KernelSum(ax, x, d["silverman"], grid=np.linspace(140, 205, 300), bump_color=GREY_B, total_color=BOOT, rug_color=DATA)
        rows = [
            cmath(r"\hat f_h(x)", r"=", r"\frac{1}{nh} \sum_i K\Big(\frac{x - x_i}{h}\Big)", font_size=30),
            cmath(r"K", r"=", r"\text{the normal density}", font_size=28),
            cmath(r"h", r"=", rf"{d['silverman']:.2f}\ \text{{cm}}", font_size=28),
        ]
        g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.6, 2.2, 0])
        for r_ in g:
            if r_.width > 3.6:
                r_.width = 3.6
        hist = historical_tag(r"Rosenblatt (1956); \ Parzen (1962)", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Murray Rosenblatt in 1956, and Emanuel Parzen in 1962, proposed the fix. Mark each "
            "observation on the axis. <bookmark mark='b'/> Over each one, put a small bump: a normal curve centred at the "
            "observation, with width h and area one over n. <bookmark mark='c'/> Add the bumps up. <bookmark mark='d'/> The sum "
            "is a kernel density estimate: smooth, with total area one, and no bins to place. Where observations crowd "
            "together their bumps pile up; where they're sparse, the estimate is low. It's a histogram whose bins are centred "
            "on every point at once."
        ) as vo:
            self.play(FadeIn(A), FadeIn(hist))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(r_) for r_ in ks.rug], lag_ratio=0.02))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b_) for b_ in ks.bumps], lag_ratio=0.03), FadeIn(g[1]), FadeIn(g[2]), run_time=2.5)
            vo.wait_until("c")
            self.play(TransformFromCopy(ks.bumps, ks.total), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(g[0]), ks.bumps.animate.set_stroke(opacity=0.3))
        self.clear_scene()

    def bandwidth(self):
        d = load("kde")
        x = np.asarray(d["x"])
        grid = np.asarray(d["grid"])
        tx, ty = np.asarray(d["true_x"]), np.asarray(d["true_y"])
        A = height_axes([-1.4, 0.3, 0], x_length=8.8, y_length=4.4)
        ax = A.ax
        truth = polyline(ax, tx, ty, S.TRUTH, 2.5, opacity=0.9)
        cs = [polyline(ax, grid, d[k], col, 3.5) for k, col in (("small", RES), ("mid", BOOT), ("big", S.ALT))]
        rug = VGroup(*[Line(ax.c2p(v, 0), ax.c2p(v, 0) + UP * 0.15, color=DATA, stroke_width=2) for v in x])
        rows = fit_rows(VGroup(
            label(r"the World population histogram", font_size=22, color=S.TRUTH),
            label(r"$h = 1$: \ every point its own peak", font_size=22, color=RES),
            label(rf"$h = {d['silverman']:.1f}$: \ Silverman's rule", font_size=22, color=BOOT),
            label(r"$h = 10$: \ smeared flat", font_size=22, color=S.ALT),
        ), 4.0, 0.4, [5.0, 0.6, 0])
        with self.voiceover(
            "Everything depends on one choice, the bandwidth h. <bookmark mark='a'/> In gold, the World population histogram of "
            "heights, which a real analysis never sees. <bookmark mark='b'/> With h equal to one centimetre, every observation "
            "is its own little peak: the estimate tracks this sample's accidents. <bookmark mark='c'/> With h about four, the "
            "estimate follows the truth well. <bookmark mark='d'/> With h equal to ten, it's smeared: the peak is too low and "
            "the tails too fat. Too small a bandwidth is noisy, too large is biased. It's the bias–variance trade-off, which "
            "we'll meet everywhere from now on."
        ) as vo:
            self.play(FadeIn(A), FadeIn(rug))
            vo.wait_until("a")
            self.play(Create(truth), FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(Create(cs[k]), FadeIn(rows[k + 1]))
        self.clear_scene()

    def tradeoff(self):
        rows = [
            cmath(r"\text{bias}", r"\approx", r"\tfrac12 h^2 f''(x)", font_size=32),
            cmath(r"\text{variance}", r"\approx", r"\frac{f(x)}{2\sqrt\pi\, nh}", font_size=32),
            cmath(r"h_{\text{opt}}", r"\propto", r"n^{-1/5},\ \ \text{MSE} \propto n^{-4/5}", font_size=32),
            cmath(r"\text{Silverman}", r":", r"h = 0.9 \min\big(s, \tfrac{\text{IQR}}{1.34}\big)\, n^{-1/5}", font_size=30),
        ]
        rows[3][2].set_color(BOOT)
        whys = [why(r"a wide bump flattens peaks: \ curvature"), why(r"a narrow bump sees few points"),
                why(r"slower than a parametric $1/n$: \ a smooth nonparametric model"), why(r"(1986): \ a rule of thumb for near-normal data")]
        with self.voiceover(
            "<bookmark mark='a'/> For IID draws from a twice-differentiable density at an interior point, the Gaussian-kernel trade-off can be written down. A wide bump flattens peaks and fills valleys: the bias is "
            "about one half h squared times the curvature of the density. <bookmark mark='b'/> A narrow bump averages over few "
            "points: the variance is about the density over n h, times a constant. <bookmark mark='c'/> Balancing the two, the "
            "best bandwidth shrinks like n to the minus one fifth, and the mean squared error like n to the minus four fifths: "
            "slower than the one over n of a parametric model. These rates require smoothness, positive density and nonzero curvature for the pointwise balance; they are not assumption-free. "
            "<bookmark mark='d'/> Bernard Silverman's rule of thumb, from his 1986 book, picks a bandwidth a little narrower than "
            "the best one for normal data, with a guard against outliers: four point one six centimetres for our sixty heights."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def choosing(self):
        rows = fit_rows(VGroup(
            label(r"choosing $h$ from the data: \ cross-validation, \ chapter ten, \ again", font_size=24, color=OBS),
            label(r"the kernel's shape matters little; \ the bandwidth matters a lot", font_size=24),
            label(r"in many dimensions it fails: \ the curse of dimensionality (Part 29)", font_size=24, color=RES),
            label(r"a smoothed bootstrap: \ resample from $\hat f_h$ instead of $\hat F_n$", font_size=24, color=BOOT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The bandwidth can also be chosen by cross-validation: leave each point out, and ask how "
            "well the estimate from the others predicts it. <bookmark mark='b'/> Which kernel you use matters little; the "
            "normal, the Epanechnikov parabola, all give similar pictures for the same effective width. "
            "<bookmark mark='c'/> In many dimensions kernel estimates need astronomically many points, the curse of "
            "dimensionality: Part 29 takes this up with nonparametric regression. <bookmark mark='d'/> And kernels and the "
            "bootstrap meet: resampling from the smooth estimate instead of the raw data is the smoothed bootstrap, one cure "
            "for the spiky bootstrap of the median in chapter seven."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

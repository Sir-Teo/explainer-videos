from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, SPOT, illustration, load, predict


class MC(VoiceoverScene):
    def construct(self):
        m = load("mc")
        ml = load("mc_live")
        self.card()
        self.funnel(ml)
        self.proof(ml)
        self.cost(m, ml)

    def card(self):
        c = chapter_card(1, r"Monte Carlo: an average with an error bar", r"How many paths for a price to one basis point?",
                         lit=(1949,), part=PART)
        with self.voiceover("Chapter one. Monte Carlo: an average with an error bar."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def funnel(self, ml):
        ex = ml["exact"]
        ck = np.log10(np.asarray(ml["ck"], float))
        runs = ml["runs"]
        g = axes([1, 6], [5, 16], x_length=8.4, y_length=4.6, xlabel=r"paths $n$", ylabel=r"running estimate of the call",
                 xticks=[1, 2, 3, 4, 5, 6], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[6, 8, 10, 12, 14], font_size=16)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        truth = DashedLine(ax.c2p(1, ex), ax.c2p(6, ex), stroke_color=WHITE, stroke_width=1.5)
        tr = ValueTracker(1.0)
        cols = [OPT, QC.THETA, QC.DELTA]
        m0 = np.asarray(runs[0]["mean"])
        se0 = np.asarray(runs[0]["se"])

        def upto():
            return int(np.searchsorted(ck, tr.get_value(), side="right"))

        def band_():
            k = max(upto(), 2)
            lo = np.clip(m0[:k] - 1.96 * se0[:k], 5, 16)
            hi = np.clip(m0[:k] + 1.96 * se0[:k], 5, 16)
            pts = [ax.c2p(x, y) for x, y in zip(ck[:k], hi)] + [ax.c2p(x, y) for x, y in zip(ck[:k][::-1], lo[::-1])]
            return Polygon(*pts, stroke_width=0, fill_color=OPT, fill_opacity=0.18)

        def line(j):
            mm = np.asarray(runs[j]["mean"])

            def make():
                k = max(upto(), 2)
                return VMobject(stroke_color=cols[j], stroke_width=2.5 if j == 0 else 1.5).set_points_as_corners(
                    [ax.c2p(x, np.clip(y, 5, 16)) for x, y in zip(ck[:k], mm[:k])])
            return always_redraw(make)

        band_m = always_redraw(band_)
        lines = [line(j) for j in range(3)]
        rd = VGroup(readout(r"n =", lambda: 10 ** tr.get_value(), digits=0, font_size=28, color=OPT),
                    readout(r"\hat V_n =", lambda: m0[max(upto(), 1) - 1], digits=3, font_size=28, color=OPT),
                    readout(r"\pm", lambda: 1.96 * se0[max(upto(), 1) - 1], digits=3, font_size=28, color=OPT)
                    ).arrange(RIGHT, buff=0.9).next_to(g, UP, buff=0.05).align_to(g, RIGHT)
        leg = legend([(OPT, r"seed 1 and its 95\% band"), (QC.THETA, r"seed 2"), (QC.DELTA, r"seed 3"),
                      (WHITE, rf"Black--Scholes: {ex:.4f}")], font_size=17).next_to(g, RIGHT, buff=0.25).align_to(g, UP)
        w = {k: 1.96 * se0[int(np.searchsorted(ck, k))] for k in (2, 4, 6)}
        side = wrapped_label(rf"the band's half-width: {w[2]:.2f} at $10^2$, {w[4]:.3f} at $10^4$, {w[6]:.4f} at $10^6$:"
                             r" a hundred times the paths for each tenfold narrowing", 3.4, 18, GREY_A)
        side.next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        src = illustration(r"one-year at-the-money call, 20\% volatility, 5\% rates; three seeds to a million paths")
        with self.voiceover(
            "A price is an expectation, so simulate the stock to expiry, pay the option, discount, and average. "
            "Here are three independent runs of that average for a one-year call, as the number of paths grows "
            "from ten to a million, on a log scale. <bookmark mark='a'/> Early on the estimates swing by whole "
            "dollars. Around the first run, the shaded band is its own ninety-five percent error bar, computed from "
            "the same paths. <bookmark mark='b'/> The band is a funnel. Its width at a hundred paths, ten thousand and "
            "a million falls by ten each time, while the paths grow a hundredfold. That square root is the whole "
            "story of this chapter."
        ) as vo:
            self.play(FadeIn(g), FadeIn(truth), FadeIn(leg), FadeIn(src), FadeIn(band_m), *[FadeIn(x) for x in lines],
                      FadeIn(rd))
            vo.wait_until("a")
            self.play(tr.animate.set_value(3.5), run_time=4, rate_func=linear)
            vo.wait_until("b")
            self.play(tr.animate.set_value(6.0), run_time=max(vo.remaining(1.0) - 1, 2), rate_func=linear)
            self.play(FadeIn(side))
        for x in [band_m, rd, *lines]:
            x.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def proof(self, ml):
        rows = [
            cmath(r"V", r"=", r"e^{-rT}\,\mathbb{E}^{\mathbb{Q}}\big[f(S_T)\big]", font_size=36, colors={r"V": OPT}),
            cmath(r"\hat V_n", r"=", r"\frac1n\sum_{i=1}^n Y_i \;\longrightarrow\; V\ \ \text{almost surely}", font_size=34,
                  colors={r"\hat V_n": OPT}),
            cmath(r"\sqrt n\,(\hat V_n - V)", r"\Rightarrow", r"N(0, \sigma_Y^2),\qquad \hat V_n \pm 1.96\,\frac{s_n}{\sqrt n}",
                  font_size=34),
            cmath(r"n(\varepsilon)", r"=", r"\Big(\frac{1.96\,\sigma_Y}{\varepsilon}\Big)^2", font_size=36,
                  colors={r"n(\varepsilon)": BAD}),
            cmath(r"\text{error}", r"\approx", r"\sigma_Y\sqrt{c / C}\quad\Rightarrow\quad\text{compare}\ \sigma_Y^2\,c",
                  font_size=34, colors={r"\text{error}": GOOD}),
        ]
        whys = [why(r"Part 9: under the pricing measure the discounted price is an expectation"),
                why(r"$Y_i$ the discounted payoffs of independent paths; the strong law of large numbers needs only "
                    r"$\mathbb{E}|Y| < \infty$"),
                why(r"the central limit theorem ($\sigma_Y^2 < \infty$), and the sample deviation $s_n \to \sigma_Y$ "
                    r"(Slutsky): an interval from the run itself"),
                why(r"solve the half-width for $n$: no dimension appears, which is why simulation wins with many assets"),
                why(r"with cost $c$ per path and budget $C$, $n = C/c$: an estimator is worth $1/(\sigma_Y^2 c)$ "
                    r"(Hammersley and Handscomb 1964)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why a funnel. Part nine showed that a price is a discounted expectation under the pricing measure. "
            "<bookmark mark='a'/> The average of independent payoffs converges to it, almost surely, by the strong "
            "law of large numbers. <bookmark mark='b'/> How fast is the central limit theorem: the error times root n "
            "is approximately normal, with the payoff's variance, so the estimate plus or minus 1.96 standard errors "
            "is a ninety-five percent interval, built from the run itself. <bookmark mark='c'/> Solve its half-width "
            "for n: the paths needed grow with the square of the accuracy, and the dimension of the problem never "
            "appears. <bookmark mark='d'/> And if each path costs c, a fixed budget buys an error of sigma times root "
            "c over the budget. So an estimator's worth is one over its variance times its cost, the yardstick for "
            "every trick in the next three chapters."
        ) as vo:
            for i, mk in enumerate("abcd"):
                step(i)
                vo.wait_until(mk)
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def cost(self, m, ml):
        sd = ml["sd"]
        n95 = ml["cent_paths"]
        cov = ml["coverage"]
        stats = VGroup(
            MathTex(rf"\sigma_Y \approx {sd:.1f}", font_size=34, color=OPT),
            MathTex(rf"\pm 1\ \text{{cent at }}95\%:\ n \approx {n95 / 1e6:.1f}\ \text{{million paths}}", font_size=32,
                    color=BAD),
            MathTex(rf"\text{{coverage of the band at }}n = 10^4:\ {100 * cov:.1f}\%\ \text{{of }}{ml['cover_seeds']:,}"
                    .replace(",", "{,}") + r"\ \text{runs}", font_size=30, color=GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(UP, buff=0.8).to_edge(LEFT, buff=0.8)
        be = wrapped_label(r"Berry--Esseen: the interval's coverage error is of order $\mathbb{E}|Y|^3/(\sigma^3\sqrt n)$; "
                           r"for a payoff that is rarely non-zero (deep out of the money) that constant is huge, and "
                           r"the error bar itself is unreliable until $n$ is large (chapter 4)", 6.4, 19, GREY_A)
        be.next_to(stats, DOWN, buff=0.45).align_to(stats, LEFT)
        q = predict(r"Estimator A has twice B's standard deviation and costs a quarter as much per path. Which do you "
                    r"run?", width=5.4, font_size=22).to_corner(DR, buff=0.4)
        ans = MathTex(r"\sigma^2 c:\ (2\sigma)^2\cdot\tfrac c4 = \sigma^2 c", font_size=30, color=GOOD).next_to(q, UP, buff=0.3)
        with self.voiceover(
            f"Put numbers in. For this call the payoff's standard deviation is about {sd:.0f}. An error bar of plus "
            f"or minus one cent, at ninety-five percent, needs about {n95 / 1e6:.1f} million paths. "
            "<bookmark mark='a'/> Is the band honest? Run the experiment a thousand times with ten thousand paths "
            f"each: the true price falls inside the band in {100 * cov:.1f} percent of them, as it should. The "
            "Berry–Esseen theorem says how fast that coverage becomes exact, and warns that payoffs which are rarely "
            "non-zero need many more paths before the band can be trusted. <bookmark mark='b'/> Pause and predict. "
            "Estimator A is twice as noisy as B but four times cheaper per path. Which should you run? "
            "<bookmark mark='c'/> Neither wins: variance times cost is the same. Every method in this part is judged "
            "by that product."
            " Monte Carlo needs random numbers and paths. Next: how they are made."
        ) as vo:
            self.play(FadeIn(stats[0]), FadeIn(stats[1]))
            vo.wait_until("a")
            self.play(FadeIn(stats[2]), FadeIn(be))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(ans))
        self.wait(0.5)
        self.clear_scene()

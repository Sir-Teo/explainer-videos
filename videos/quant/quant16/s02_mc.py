from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, SPOT, illustration, load, predict, axes, data_range, pause_card, flat_camera


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
        yr = data_range(*[r["mean"] for r in runs], np.asarray(runs[0]["mean"]) - 1.96*np.asarray(runs[0]["se"]), np.asarray(runs[0]["mean"]) + 1.96*np.asarray(runs[0]["se"]))
        g = axes([1, 6], yr, x_length=8.4, y_length=4.6, xlabel=r"paths $n$", ylabel=r"running estimate of the call",
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
            lo = m0[:k] - 1.96 * se0[:k]
            hi = m0[:k] + 1.96 * se0[:k]
            pts = [ax.c2p(x, y) for x, y in zip(ck[:k], hi)] + [ax.c2p(x, y) for x, y in zip(ck[:k][::-1], lo[::-1])]
            return Polygon(*pts, stroke_width=0, fill_color=OPT, fill_opacity=0.18)

        def line(j):
            mm = np.asarray(runs[j]["mean"])

            def make():
                k = max(upto(), 2)
                return VMobject(stroke_color=cols[j], stroke_width=2.5 if j == 0 else 1.5).set_points_as_corners(
                    [ax.c2p(x, y) for x, y in zip(ck[:k], mm[:k])])
            return always_redraw(make)

        band_m = always_redraw(band_)
        lines = [line(j) for j in range(3)]
        rd = VGroup(readout(r"n =", lambda: 10 ** tr.get_value(), digits=0, font_size=28, color=OPT),
                    readout(r"\hat V_n =", lambda: m0[max(upto(), 1) - 1], digits=3, font_size=28, color=OPT),
                    readout(r"\pm", lambda: 1.96 * se0[max(upto(), 1) - 1], digits=3, font_size=28, color=OPT)
                    ).arrange(RIGHT, buff=0.9).next_to(g, UP, buff=0.05).align_to(g, RIGHT)
        # the numbers widen as n grows (10 -> 1,000,000): keep the three readouts spaced as they do
        rd.add_updater(lambda m: m.arrange(RIGHT, buff=0.6).next_to(g, UP, buff=0.05).align_to(g, RIGHT))
        leg = legend([(OPT, r"seed 1: pointwise normal 95\% interval"), (QC.THETA, r"seed 2"), (QC.DELTA, r"seed 3"),
                      (WHITE, rf"Black--Scholes: {ex:.4f}")], font_size=17).next_to(g, RIGHT, buff=0.25).align_to(g, UP)
        w = {k: 1.96 * se0[int(np.searchsorted(ck, k))] for k in (2, 4, 6)}
        side = wrapped_label(rf"the band's half-width: {w[2]:.2f} at $10^2$, {w[4]:.3f} at $10^4$, {w[6]:.4f} at $10^6$:"
                             r" a hundred times the paths for each tenfold narrowing", 3.4, 18, GREY_A)
        side.next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        src = illustration(r"one-year at-the-money call, 20\% volatility, 5\% rates; three seeds to a million paths")
        with self.voiceover(
            "Simulate independent terminal prices under Black–Scholes, discount each payoff and average. Here are three fixed-seed runs, from ten to a million paths. <bookmark mark='a'/> The shaded band around the first run is its pointwise normal approximation, estimate plus or minus 1.96 estimated standard errors. It is not an exact finite-sample interval or a simultaneous confidence band over every displayed path count. The full estimates and band remain visible. <bookmark mark='b'/> At large sample sizes, fixed payoff variance gives inverse-square-root sampling error. A hundred times more paths gives about ten times smaller standard error; realized errors and widths fluctuate. This terminal Black–Scholes experiment has no time-stepping bias."
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
                why(r"nonzero finite variance and iid draws; CLT and $s_n \to \sigma_Y$: asymptotic pointwise 95\% coverage; "
                    r"(Slutsky): an interval from the run itself"),
                why(r"solve the half-width for $n$: the exponent is dimension-free; variance and single-path cost may still grow with dimension"),
                why(r"with cost $c$ per path and budget $C$, $n = C/c$: an estimator is worth $1/(\sigma_Y^2 c)$ "
                    r"(Hammersley and Handscomb 1964)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Under the pricing measure, a discounted payoff has expectation V. <bookmark mark='a'/> For independent identically distributed paths, finite absolute first moment gives almost-sure convergence by the strong law. <bookmark mark='b'/> Positive finite variance gives the central limit theorem; consistent sample variance and Slutsky then give an asymptotic pointwise ninety-five percent interval. This is a sampling statement, separate from discretization or model error. <bookmark mark='c'/> Solving the target normal half-width gives n approximately equal to 1.96 squared times payoff variance divided by epsilon squared. The exponent does not contain dimension, but variance and the cost of one path can depend on dimension. <bookmark mark='d'/> With cost c per independent draw and budget C, sampling standard error is approximately sigma times the square root of c over C. Compare variance times cost at a fixed bias target, including any fitting or preprocessing costs when material."
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
        be = wrapped_label(r"Berry--Esseen: the interval's coverage error is of order $\mathbb{E}|Y-\mathbb EY|^3/(\sigma^3\sqrt n)$; "
                           r"for a payoff that is rarely non-zero (deep out of the money) that constant is huge, and "
                           r"the error bar itself is unreliable until $n$ is large (chapter 4)", 6.4, 19, GREY_A)
        be.next_to(stats, DOWN, buff=0.45).align_to(stats, LEFT)
        q = predict(r"Estimator A has twice B's standard deviation and costs a quarter as much per path. Which do you "
                    r"run?", width=5.4, font_size=22).to_corner(DR, buff=0.4)
        ans = MathTex(r"\sigma^2 c:\ (2\sigma)^2\cdot\tfrac c4 = \sigma^2 c", font_size=30, color=GOOD).next_to(q, UP, buff=0.3)
        with self.voiceover(
            f"For this discounted call payoff, the original standard deviation is about {sd:.1f}. A target normal half-width of one cent requires about {n95 / 1e6:.1f} million independent paths. <bookmark mark='a'/> Across {ml['cover_seeds']} fixed-seed repetitions with {ml['cover_n']} paths, the empirical pointwise coverage is {100 * cov:.1f} percent. That frequency has sampling uncertainty and is not a guarantee for other payoffs. Berry–Esseen requires a finite third absolute centered moment and positive variance; its constant can be large for rare payoffs. <bookmark mark='b'/> If estimator A has twice B's per-draw standard deviation and costs a quarter as much, which has smaller sampling variance at the same large budget? <bookmark mark='c'/> Their variance-cost products tie under those assumptions. Bias, dependence, setup cost and the required total accuracy can change the decision. Next, random numbers and paths."
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

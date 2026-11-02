from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load, real_data, tbar


class Overlap(VoiceoverScene):
    def construct(self):
        o = load("overlap")
        s = load("stambaugh")
        self.card()
        self.scatter(o)
        self.size(o)
        self.stambaugh(s)

    def card(self):
        c = chapter_card(1, r"Overlapping data and predictive regressions", r"How many independent observations do you "
                         r"have?", part=PART)
        with self.voiceover("Chapter one. Overlapping data, and predictive regressions."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def scatter(self, o):
        dy, fwd = np.asarray(o["dy"]), np.asarray(o["fwd"])
        g = axes([dy.min() - 0.1, dy.max() + 0.1], [-1.0, 1.4], x_length=6.4, y_length=4.4,
                 xlabel=r"log dividend yield at the start", ylabel=r"real log return over the next five years",
                 xticks=list(np.log([0.02, 0.04, 0.08])), xfmt=lambda u: f"{100 * np.exp(u):.0f}\\%",
                 yticks=[-0.5, 0, 0.5, 1.0], font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.02, color=DATA_C, fill_opacity=0.6) for a, b in
                        zip(dy[::3], fwd[::3])])
        e = o["est"]
        xs = np.linspace(dy.min(), dy.max(), 20)
        fit = curve(ax, xs, np.mean(fwd) + e["naive"]["beta"] * (xs - np.mean(dy)), EST, stroke_width=3)
        g2 = axes([0, 3], [0, 16], x_length=4.4, y_length=3.0, ylabel=r"$t$-statistic of the slope", xticks=[],
                  yticks=[0, 2, 8, 16], font_size=16).to_corner(UR, buff=0.5).shift(DOWN * 0.6)
        a2 = g2.ax
        cols = [BAD, GOOD, GOOD]
        names = [r"naive", r"Newey--West", r"Hansen--Hodrick"]
        bars = VGroup(*[tbar(a2, i + 0.5, e[k]["t"], c, width=0.55) for i, (k, c) in enumerate(zip(["naive", "nw", "hh"], cols))])
        vals = VGroup(*[MathTex(f"{e[k]['t']:.1f}", font_size=22, color=c).next_to(b, UP, buff=0.06)
                        for k, c, b in zip(["naive", "nw", "hh"], cols, bars)])
        nl = VGroup(*[label(n_, font_size=16, color=GREY_B).next_to(a2.c2p(i + 0.5, 0), DOWN, buff=0.1)
                      for i, n_ in enumerate(names)])
        side = wrapped_label(rf"{o['n']:,} overlapping five-year windows; neighbours share 59 of their 60 months, so the "
                             r"errors are correlated and the naive standard error is far too small".replace(",", "{,}"),
                             5.0, 20, GREY_A).next_to(g2, DOWN, buff=0.7).align_to(g2, LEFT)
        src = real_data(r"Shiller's monthly data, 1871--2020, real total returns")
        with self.voiceover(
            "Part three met this problem with the CAPE. Here it is again with the dividend yield: does a high yield "
            "predict high returns over the next five years? Each dot is a month since 1871, and the return of the "
            "five years that followed. <bookmark mark='a'/> The slope is positive. Ordinary least squares reports a "
            "t-statistic of fifteen. <bookmark mark='b'/> But each dot shares fifty-nine of its sixty months with "
            "its neighbour. The errors are correlated, and the usual formula, which assumes they are not, divides by "
            "a sample size seventeen hundred when the honest count is nearer thirty. Whitney Newey and Kenneth West "
            "gave a standard error that allows for correlation: it gives a t-statistic of two point eight. Lars Hansen "
            "and Robert Hodrick's version, built for overlapping horizons, gives two point five."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002, run_time=2))
            vo.wait_until("a")
            self.play(Create(fit), FadeIn(g2), FadeIn(nl), GrowFromEdge(bars[0], DOWN), FadeIn(vals[0]))
            vo.wait_until("b")
            self.play(FadeIn(side))
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(vals[1]), GrowFromEdge(bars[2], DOWN), FadeIn(vals[2]))
        self.wait(0.4)
        self.clear_scene()

    def size(self, o):
        sz = o["size"]
        g = axes([0, 3], [0, 0.85], x_length=6.0, y_length=4.4, ylabel=r"how often a true null is rejected at 5\%",
                 xticks=[], yticks=[0, 0.05, 0.25, 0.5, 0.75], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=18)
        g.to_edge(LEFT, buff=0.9).shift(DOWN * 0.2)
        ax = g.ax
        ks = ["naive", "nw", "hh"]
        names = [r"naive", r"Newey--West", r"Hansen--Hodrick"]
        cols = [BAD, ALT, ALT]
        bars = VGroup(*[tbar(ax, i + 0.5, sz[k], c, width=0.55) for i, (k, c) in enumerate(zip(ks, cols))])
        vals = VGroup(*[MathTex(f"{100 * sz[k]:.0f}\\%", font_size=26, color=c).next_to(b, UP, buff=0.06)
                        for k, c, b in zip(ks, cols, bars)])
        nl = VGroup(*[label(n_, font_size=18, color=GREY_B).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.1)
                      for i, n_ in enumerate(names)])
        five = DashedLine(ax.c2p(0, 0.05), ax.c2p(3, 0.05), color=GOOD, stroke_width=2)
        side = VGroup(
            label(r"400 simulated worlds where nothing predicts anything:", font_size=21, color=GREY_A),
            label(r"iid returns, a predictor as persistent as the yield", font_size=21, color=GREY_A),
            label(r"(monthly $\rho = 0.99$), five-year overlapping horizons", font_size=21, color=GREY_A),
            wrapped_label(r"the corrections help a lot, but with a persistent predictor and overlapping returns "
                          r"they still reject three times too often: use them, and still distrust $t \approx 2$",
                          4.8, 21, ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4)
        side[3].shift(DOWN * 0.3)
        with self.voiceover(
            "How good are the corrections? Simulate four hundred worlds in which returns are pure noise and the "
            "predictor is as persistent as the dividend yield, and run the same regression in each. "
            f"<bookmark mark='a'/> The naive t-test finds significance in {100 * sz['naive']:.0f} percent of them. "
            f"<bookmark mark='b'/> Newey-West in {100 * sz['nw']:.0f} percent, Hansen-Hodrick in "
            f"{100 * sz['hh']:.0f}: far better, still three times the five percent promised. With overlapping returns "
            "and a slow-moving predictor, a t-statistic of two is weak evidence, whatever the standard error."
        ) as vo:
            self.play(FadeIn(g), FadeIn(nl), Create(five), FadeIn(side[:3]))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(vals[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(vals[1]), GrowFromEdge(bars[2], DOWN), FadeIn(vals[2]))
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def stambaugh(self, s):
        sims = {k: np.asarray(v) for k, v in s["sims"].items()}
        g = axes([-0.25, 0.35], [0, 14], x_length=7.0, y_length=4.2, xlabel=r"estimated slope $\hat\beta$ (true $\beta = 0$)",
                 ylabel=r"density", xticks=[-0.2, 0, 0.2], yticks=[], font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        edges = np.linspace(-0.25, 0.35, 61)
        outs = VGroup()
        for k, col in (("150", EST), ("50", ALT)):
            h, _ = np.histogram(np.clip(sims[k], -0.25, 0.35), edges, density=True)
            pts = [ax.c2p(edges[0], 0)]
            for i, v in enumerate(h):
                pts += [ax.c2p(edges[i], min(v, 14)), ax.c2p(edges[i + 1], min(v, 14))]
            pts.append(ax.c2p(edges[-1], 0))
            outs.add(VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(pts))
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 14), color=GREY_B, stroke_width=2)
        means = VGroup(*[DashedLine(ax.c2p(sims[k].mean(), 0), ax.c2p(sims[k].mean(), 12), color=c, stroke_width=2)
                         for k, c in (("150", EST), ("50", ALT))])
        leg = legend([(ALT, rf"50 years: mean {sims['50'].mean():+.3f}"), (EST, rf"150 years: mean {sims['150'].mean():+.3f}")],
                     font_size=21)
        side = VGroup(
            leg,
            MathTex(r"\mathbb{E}[\hat\beta - \beta] \approx -\frac{\sigma_{uv}}{\sigma_v^2}\,\frac{1 + 3\rho}{T}",
                    font_size=32),
            label(rf"annual dividend yield, 1871--2020: $\rho = {s['rho']:.2f}$, corr$(u, v) = {s['corr_uv']:.2f}$",
                  font_size=20, color=GREY_A),
            MathTex(rf"\hat\beta = {s['beta']:.3f}\ (t = {s['t']:.1f}) \;\to\; {s['beta_corrected']:.3f}", font_size=30,
                    color=EST),
            label(r"half of the estimated predictability is bias", font_size=21, color=BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "There is a second problem, and it biases the slope itself. A price-based predictor like the dividend "
            "yield is persistent, and its surprises are the mirror image of return surprises: when prices jump, the "
            "yield falls. Robert Stambaugh showed in 1999 what that does. <bookmark mark='a'/> Simulate a world where "
            "the yield predicts nothing. With fifty years of data the estimated slopes are centred well above zero; "
            "with a hundred and fifty, closer, but still positive. <bookmark mark='b'/> The bias follows a formula: "
            "it grows with the persistence and the mirror-image correlation, and shrinks with the sample. "
            "<bookmark mark='c'/> On a century and a half of annual data the dividend yield's slope is three "
            "hundredths, with a t-statistic of one. Correct for Stambaugh's bias and half of it disappears. Much of "
            "the famous predictability of returns is the statistics of persistent regressors."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(Create(outs[1]), Create(means[1]), FadeIn(leg[0]))
            self.play(Create(outs[0]), Create(means[0]), FadeIn(leg[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

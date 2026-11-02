from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load, real_data, tbar


class Sharpe(VoiceoverScene):
    def construct(self):
        b = load("bootstrap")
        s = load("snr")
        e = load("ellipse")
        self.card()
        self.boot(b)
        self.years(s)
        self.ellipse(e)

    def card(self):
        c = chapter_card(4, r"The bootstrap and the signal-to-noise problem", r"How long before you know?", part=PART)
        with self.voiceover("Chapter four. The bootstrap, and the signal-to-noise problem."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def boot(self, b):
        bb = np.asarray(b["boot_block"])
        g = axes([0.0, 0.9], [0, 4.0], x_length=6.6, y_length=4.0, xlabel=r"annualised Sharpe ratio of the US market",
                 ylabel=r"density", xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[], font_size=18).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.2)
        ax = g.ax
        edges = np.linspace(0, 0.9, 46)
        h, _ = np.histogram(np.clip(bb, 0, 0.9), edges, density=True)
        bars = VGroup(*[Rectangle(width=ax.c2p(edges[1] - edges[0], 0)[0] - ax.c2p(0, 0)[0] - 0.01,
                                  height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0, fill_color=EST,
                                  fill_opacity=0.8).move_to(ax.c2p((edges[i] + edges[i + 1]) / 2, 0), aligned_edge=DOWN)
                        for i, v in enumerate(h)])
        est = DashedLine(ax.c2p(b["sr_a"], 0), ax.c2p(b["sr_a"], 4), color=WHITE, stroke_width=2)
        rows = VGroup(
            MathTex(rf"\widehat{{SR}} = {b['sr_a']:.2f} \ \text{{a year, }} 1926\text{{--}}2020", font_size=30),
            label(r"standard errors:", font_size=22, color=GREY_A),
            MathTex(rf"\text{{iid formula (Lo 2002): }} {b['se_iid']:.3f}", font_size=28, color=GREY_A),
            MathTex(rf"\text{{with fat tails (Mertens 2002): }} {b['se_mertens']:.3f}", font_size=28, color=GREY_A),
            MathTex(rf"\text{{block bootstrap (12 months): }} {b['se_block']:.3f}", font_size=28, color=EST),
            MathTex(rf"\text{{stationary bootstrap: }} {b['se_stationary']:.3f}", font_size=28, color=EST),
            wrapped_label(r"resample whole blocks of months, so volatility clusters and autocorrelation come along "
                          r"(K\"unsch 1989; Politis and Romano 1994)", 4.8, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Kenneth French's monthly market excess return, July 1926 -- December 2020")
        with self.voiceover(
            "How precisely do we know the American market's Sharpe ratio, its excess return per unit of risk? Over "
            "ninety-four years of monthly data it is about zero point four four a year. If the months were "
            "independent, its standard error would be about a tenth, and fat tails barely change that. "
            "<bookmark mark='a'/> But months are not independent: volatility clusters. The bootstrap answers by "
            "resampling the data, and for dependent data it must resample whole blocks of months, so that the "
            "clustering comes along. <bookmark mark='b'/> The block bootstrap's standard error is about twelve "
            "hundredths, a fifth larger. Even after ninety-four years, the Sharpe ratio of the stock market is known "
            "only to within plus or minus a quarter."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(bb_, DOWN) for bb_ in bars], lag_ratio=0.02, run_time=2), Create(est),
                      FadeIn(rows[6]))
            vo.wait_until("b")
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()

    def years(self, s):
        sr, yrs = np.asarray(s["sr"]), np.asarray(s["years"])
        g = axes([0.2, 2.0], [0, 100], x_length=5.8, y_length=4.2, xlabel=r"true Sharpe ratio, annual",
                 ylabel=r"years for an expected $t$ of 2", xticks=[0.5, 1.0, 1.5, 2.0], yticks=[0, 16, 50, 100],
                 font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, sr, np.minimum(yrs, 100), EST, stroke_width=3.5)
        dots = VGroup(Dot(ax.c2p(0.5, 16), radius=0.08, color=BAD), Dot(ax.c2p(1.0, 4), radius=0.08, color=GOOD))
        T = np.asarray(s["T"])
        g2 = axes([0, 30], [0, 0.5], x_length=5.0, y_length=3.0, xlabel=r"years of data", ylabel=r"chance it looks worse "
                  r"than zero", xticks=[0, 10, 20, 30], yticks=[0, 0.25, 0.5], yfmt=lambda u: f"{100 * u:.0f}\\%",
                  font_size=16).to_corner(UR, buff=0.5)
        a2 = g2.ax
        cols = {"0.25": BAD, "0.5": ALT, "1.0": GOOD}
        pl = VGroup(*[curve(a2, T, np.asarray(s["p_neg"][k]), c, stroke_width=3) for k, c in cols.items()])
        leg = legend([(BAD, r"SR 0.25"), (ALT, r"SR 0.5"), (GOOD, r"SR 1")], font_size=19).next_to(g2, DOWN, buff=0.3)
        eq = MathTex(r"t \approx SR\,\sqrt{T} \;\Rightarrow\; T \approx (2 / SR)^2", font_size=32).next_to(leg, DOWN, buff=0.4)
        with self.voiceover(
            "This is the deepest problem in quantitative finance: the signal is small and the noise is large. The "
            "t-statistic of a strategy's mean return is roughly its Sharpe ratio times the square root of the "
            "number of years. <bookmark mark='a'/> So a strategy with a true Sharpe ratio of a half, a good "
            "strategy, needs sixteen years of data before its t-statistic is expected to reach two. A Sharpe of "
            "one needs four. <bookmark mark='b'/> And over shorter spans, good strategies often look bad. After "
            "five years, a Sharpe-of-a-half strategy has about a one-in-eight chance of having lost money, and a "
            "Sharpe-of-a-quarter strategy nearly one in three. Funds are closed, and strategies abandoned, on "
            "evidence like that."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(dots))
            vo.wait_until("b")
            self.play(FadeIn(g2), LaggedStart(*[Create(p) for p in pl], lag_ratio=0.3), FadeIn(leg))
        self.wait(0.4)
        self.clear_scene()

    def ellipse(self, e):
        g = axes([-0.3, 0.35], [0.2, 1.2], x_length=6.6, y_length=4.6, xlabel=r"$\alpha$, annual", ylabel=r"$\beta$",
                 xticks=[-0.2, 0, 0.2], xfmt=lambda u: f"{100 * u:.0f}\\%", yticks=[0.4, 0.8, 1.2], font_size=18)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        cols = {"5": BAD, "20": ALT, "60": GOOD}
        shapes = VGroup()
        for k, c in cols.items():
            v = e[k]
            V = np.asarray(v["V"])
            w, U = np.linalg.eigh(V)
            r = np.sqrt(5.991)  # 95% for two parameters
            th = np.linspace(0, 2 * np.pi, 120)
            pts = (U @ (r * np.sqrt(np.maximum(w, 0))[:, None] * np.vstack([np.cos(th), np.sin(th)]))).T
            pts += np.array([v["alpha"], v["beta"]])
            poly = VMobject(stroke_color=c, stroke_width=3).set_points_smoothly(
                [ax.c2p(np.clip(a, -0.3, 0.35), np.clip(b_, 0.2, 1.2)) for a, b_ in pts])
            dot = Dot(ax.c2p(v["alpha"], v["beta"]), radius=0.06, color=c)
            shapes.add(VGroup(poly, dot))
        zero = DashedLine(ax.c2p(0, 0.2), ax.c2p(0, 1.2), color=GREY_B, stroke_width=2)
        leg = legend([(BAD, rf"5 years: $\alpha = {100 * e['5']['alpha']:.0f}\%$"),
                      (ALT, rf"20 years: $\alpha = {100 * e['20']['alpha']:.0f}\%$"),
                      (GOOD, rf"60 years: $\alpha = {100 * e['60']['alpha']:.0f}\%$")], font_size=22)
        side = VGroup(
            label(r"tobacco stocks against the market, to 2020", font_size=22, color=GREY_A), leg,
            wrapped_label(r"95\% confidence regions for $(\alpha, \beta)$: the beta is pinned down in a few years, the "
                          r"alpha takes decades, because it is the mean of a noisy series", 4.6, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Here is the same problem in two dimensions. Regress tobacco stocks on the market, and draw the ninety-five "
            "percent confidence region for alpha, the excess return, and beta, the market exposure. "
            "<bookmark mark='a'/> With five years of data, the region spans an alpha from about minus twenty-five "
            "to plus fifteen percent a year. <bookmark mark='b'/> With twenty years, and with sixty, it narrows. Notice its "
            "shape: beta is pinned down quickly, because it comes from how the two series move together, every "
            "month. Alpha is a mean, and means of noisy returns take decades to estimate."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(shapes[0][0]), FadeIn(shapes[0][1]), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(shapes[1][0]), FadeIn(shapes[1][1]), FadeIn(leg[1]))
            self.play(Create(shapes[2][0]), FadeIn(shapes[2][1]), FadeIn(leg[2]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data


class Series(VoiceoverScene):
    def construct(self):
        s = load("spurious")
        c = load("coint")
        self.card()
        self.stationarity()
        self.spurious(s)
        self.coint(c)

    def card(self):
        c = chapter_card(1, r"Unit roots, spurious regression, cointegration", r"When do two trends really move together?",
                         part=PART)
        with self.voiceover("Chapter one. Unit roots, spurious regression, and cointegration."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def stationarity(self):
        rng = np.random.default_rng(4)
        n = 300
        e = rng.standard_normal(n)
        ar = np.zeros(n)
        walk = np.cumsum(e)
        for t in range(1, n):
            ar[t] = 0.8 * ar[t - 1] + e[t]
        g1 = axes([0, n], [-6, 6], x_length=5.6, y_length=2.6, xticks=[], yticks=[0], font_size=14)
        lo, hi = float(walk.min()) - 2, float(walk.max()) + 2
        g2 = axes([0, n], [lo, hi], x_length=5.6, y_length=2.6, xticks=[], yticks=[0], font_size=14)
        VGroup(g1, g2).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.1)
        l1 = curve(g1.ax, np.arange(n), ar, VOL, stroke_width=2)
        l2 = curve(g2.ax, np.arange(n), walk, RET, stroke_width=2)
        t1 = MathTex(r"x_t = 0.8\,x_{t-1} + \varepsilon_t", font_size=30, color=VOL).next_to(g1, UP, buff=0.15)
        t2 = MathTex(r"x_t = x_{t-1} + \varepsilon_t", font_size=30, color=RET).next_to(g2, UP, buff=0.15)
        c1 = label(r"stationary: pulled back, its variance is finite", font_size=20, color=GREY_A).next_to(g1, DOWN, buff=0.15)
        c2 = label(r"a unit root: shocks are permanent, variance grows with $t$", font_size=20, color=GREY_A).next_to(g2, DOWN, buff=0.15)
        notes = VGroup(
            label(r"Box--Jenkins (1970): make the series stationary, then model what is left with ARMA", font_size=22,
                  color=GREY_A),
            label(r"the Dickey--Fuller test asks: is the pull back zero? $\Delta x_t = a + \gamma\,x_{t-1} + \dots$, "
                  r"unit root if $\gamma = 0$", font_size=22, color=GREY_A),
            label(r"log prices have unit roots (ADF: Bitcoin $t = 0.96$, nowhere near $-2.86$); returns do not", font_size=22,
                  color=ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Two kinds of time series. A stationary one, like this one, is pulled back toward its mean, and its "
            "variance stays finite. <bookmark mark='a'/> A random walk has a unit root: every shock is permanent, and "
            "its variance grows without limit. <bookmark mark='b'/> George Box and Gwilym Jenkins built time-series "
            "modelling in 1970 on a simple rule: first make the series stationary, then model what remains. The "
            "Dickey-Fuller test asks whether a series has a unit root. Log prices do, returns don't, which is why "
            "this series models returns."
        ) as vo:
            self.play(FadeIn(g1), Create(l1), FadeIn(t1), FadeIn(c1))
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(l2), FadeIn(t2), FadeIn(c2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in notes], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def spurious(self, s):
        r2 = np.asarray(s["r2"])
        t, lb, lm = (np.asarray(s[k]) for k in ("t", "lb", "lm"))
        g = axes([2017.6, 2021], [0, 1], x_length=6.4, y_length=3.2, xticks=[2018, 2019, 2020], xfmt=lambda u: f"{int(u)}",
                 yticks=[], ylabel=r"rescaled log prices", font_size=16).to_edge(LEFT, buff=0.6).shift(UP * 0.6)
        ax = g.ax

        def sc(x):
            return (x - x.min()) / (x.max() - x.min())

        l1 = curve(ax, t, sc(lb), FC, stroke_width=2.5)
        l2 = curve(ax, t, sc(lm), RET, stroke_width=2.5)
        leg = legend([(FC, r"Bitcoin"), (RET, r"US stock market")], font_size=19).next_to(g, DOWN, buff=0.2).align_to(g, LEFT)
        bl, bd = s["btc_levels"], s["btc_diffs"]
        res = VGroup(
            MathTex(rf"\text{{levels: }} t = {bl['t']:.0f},\ R^2 = {bl['r2']:.2f}", font_size=28, color=BAD),
            MathTex(rf"\text{{daily changes: }} t = {bd['t']:.1f},\ R^2 = {bd['r2']:.2f}", font_size=28, color=GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(leg, DOWN, buff=0.3).align_to(g, LEFT)
        side = VGroup(
            label(r"2{,}000 pairs of independent random walks:", font_size=22, color=GREY_A),
            MathTex(rf"\text{{levels: }} |t| > 1.96 \text{{ in }} {100 * s['rej_levels']:.0f}\%", font_size=30, color=BAD),
            MathTex(rf"\text{{differences: }} {100 * s['rej_diffs']:.0f}\%", font_size=30, color=GOOD),
            label(rf"median $R^2$ in levels: {s['median_r2']:.2f}", font_size=22, color=GREY_A),
            wrapped_label(r"Granger and Newbold (1974): regressing one trending series on another finds a relationship "
                          r"almost always; difference the series, or test for cointegration", 4.6, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "That matters, because regressing one wandering series on another is a trap. Clive Granger and Paul "
            "Newbold showed it in 1974. <bookmark mark='a'/> Generate two thousand pairs of random walks that have "
            f"nothing to do with each other, and regress one on the other. The t-statistic exceeds two in "
            f"{100 * s['rej_levels']:.0f} percent of them. In changes, five percent, as it should be. "
            "<bookmark mark='b'/> Bitcoin against the American stock market, 2017 to 2020, in log price levels: a "
            "t-statistic of twenty-four and an R squared of forty percent. In daily changes there is a real link, "
            "but a much weaker one: five percent of the variance, most of it from 2020."
        ) as vo:
            self.play(FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(l1), Create(l2), FadeIn(leg))
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def coint(self, c):
        t, bp = np.asarray(c["t"]), np.asarray(c["basis_bp"])
        g = axes([2020, 2021], [-80, 40], x_length=6.0, y_length=4.0, ylabel=r"perpetual minus spot, basis points",
                 xticks=[2020, 2020.5, 2021], xfmt=lambda u: {2020: "Jan", 2020.5: "Jul", 2021: "Jan"}[round(u * 2) / 2],
                 yticks=[-80, -40, 0, 40], font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, t, np.clip(bp, -80, 40), VOL, stroke_width=2.5)
        k = int(np.argmin(bp))
        crash = label(rf"{bp[k]:.0f} bp: 12 March", font_size=18, color=BAD).next_to(ax.c2p(t[k], -80), RIGHT, buff=0.1)
        side = VGroup(
            MathTex(r"\log F_t = a + b \log S_t + u_t", font_size=32),
            MathTex(rf"\text{{ADF on each: }} t = {c['adf_spot_t']:.2f},\ {c['adf_fut_t']:.2f}", font_size=26, color=GREY_A),
            MathTex(rf"\text{{on the residual: }} t = {c['eg_t']:.1f} \ (5\%: -3.34)", font_size=28, color=GOOD),
            label(rf"the basis mean-reverts with a half-life of {c['half_life_days']:.1f} days", font_size=22, color=VOL),
            label(rf"an independent walk against Bitcoin: $t = {c['fake_t']:.1f}$, not cointegrated", font_size=21,
                  color=GREY_B),
            wrapped_label(r"Engle and Granger (1987): two unit-root series are cointegrated if a combination of them is "
                          r"stationary; arbitrage ties a future to its spot. Johansen (1991) handles many series.", 4.8,
                          20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Binance BTCUSDT spot and USD-M perpetual, daily closes, 2020")
        with self.voiceover(
            "Sometimes two wandering series really are tied together. Bitcoin's spot price and its perpetual future "
            "each have a unit root. <bookmark mark='a'/> But the gap between them, the basis, does not wander: here it "
            "is through 2020, in basis points, snapping back toward zero. Robert Engle and Clive Granger called such "
            "series cointegrated in 1987: some combination of them is stationary. Test the residual of one regressed "
            "on the other, and it rejects a unit root decisively; the basis has a half-life of about a day. "
            "<bookmark mark='b'/> The tie is arbitrage, and Part two's funding rate is the mechanism. Cointegration is "
            "the statistics of pairs trading, which Part thirty-three builds into a strategy."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
            self.play(FadeIn(crash))
            self.play(FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("b")
            self.play(FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

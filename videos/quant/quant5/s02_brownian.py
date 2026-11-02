from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, load, real_data


class Brownian(VoiceoverScene):
    def construct(self):
        v = load("variation")
        s = load("signature")
        self.card()
        self.donsker()
        self.variations(v)
        self.signature(s)

    def card(self):
        c = chapter_card(1, r"Brownian motion and quadratic variation", r"How rough is a price?", lit=(1923,), part=PART)
        with self.voiceover("Chapter one. Brownian motion, and quadratic variation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def donsker(self):
        rng = np.random.default_rng(2)
        steps = rng.choice([-1.0, 1.0], 4096)
        g = axes([0, 1], [-2.0, 2.0], x_length=9.0, y_length=3.8, xlabel=r"time", ylabel=r"$S_{\lfloor nt\rfloor}/\sqrt{n}$",
                 xticks=[0, 0.5, 1], yticks=[-2, -1, 0, 1, 2], font_size=18).shift(DOWN * 1.0)
        ax = g.ax
        lines = []
        for n, col in [(16, GREY_B), (128, BM), (4096, ITO)]:
            x = np.cumsum(steps.reshape(n, 4096 // n).sum(axis=1))
            y = np.concatenate([[0.0], x]) / np.sqrt(4096)
            tt = np.linspace(0, 1, n + 1)
            lines.append(curve(ax, tt, y, col, stroke_width=2.5 if n < 4096 else 1.6))
        th = theorem_card(r"Donsker's invariance principle", r"A random walk with steps of mean 0 and variance 1, "
                          r"rescaled by $\sqrt{n}$ in space and $n$ in time, converges in law to Brownian motion, "
                          r"whatever the steps' distribution.", who=r"Donsker (1951)", color=ITO, width=8.6,
                          font_size=22).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Brownian motion is what a random walk looks like from far away. Take sixteen coin-toss steps, then "
            "a hundred and twenty-eight, then four thousand, shrinking time by n and space by the square root of n. "
            "<bookmark mark='a'/> The picture converges, and Monroe Donsker proved in 1951 that the limit is the "
            "same Brownian motion whatever the steps were, as long as they have mean zero and finite variance. That "
            "universality is why Brownian motion, and not some other process, sits under so much of finance."
        ) as vo:
            self.play(FadeIn(g), Create(lines[0]))
            self.play(lines[0].animate.set_stroke(opacity=0.35), Create(lines[1]))
            self.play(lines[1].animate.set_stroke(opacity=0.35), Create(lines[2]), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(th, shift=DOWN * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def variations(self, v):
        n = np.log2(np.asarray(v["n"]))
        g = axes([2, 16], [-2.2, 2.2], x_length=7.2, y_length=4.6, xlabel=r"grid points $n$ (log scale)",
                 ylabel=r"sum over the grid (log scale)", xticks=[2, 6, 10, 14], xfmt=lambda u: rf"2^{{{int(u)}}}",
                 yticks=[-2, -1, 0, 1, 2], yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1", font_size=18)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        l1 = curve(ax, n, np.log10(v["v1"]), JUMP, stroke_width=3.5)
        l2 = curve(ax, n, np.log10(v["v2"]), ITO, stroke_width=3.5)
        l3 = curve(ax, n, np.log10(v["v3"]), BM, stroke_width=3.5)
        leg = legend([(JUMP, r"$\sum |\Delta W|$: total variation, grows like $\sqrt{n}$"),
                      (ITO, r"$\sum (\Delta W)^2$: quadratic variation, $\to T = 1$"),
                      (BM, r"$\sum |\Delta W|^3 \to 0$")], font_size=21)
        side = VGroup(leg, MathTex(r"(dW)^2 = dt", font_size=46, color=ITO),
                      wrapped_label(r"a smooth path has zero quadratic variation; a Brownian path has infinite length "
                                    r"and a quadratic variation equal to elapsed time", 4.8, 21, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "How rough is that limit? Cut one Brownian path into finer and finer pieces and add up three things. "
            "<bookmark mark='a'/> The sizes of the steps: the path's length. It grows without bound, like the square "
            "root of the number of pieces. A Brownian path is infinitely long in any interval. <bookmark mark='b'/> "
            "The squares of the steps: they settle, at exactly the elapsed time. <bookmark mark='c'/> The cubes: "
            "they vanish. So squares are the one power that neither blows up nor disappears. That is the rule "
            "behind all of stochastic calculus: d W squared equals d t."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(l1), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(l2), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(Create(l3), FadeIn(leg[2]))
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def signature(self, s):
        m = np.log10(np.asarray(s["minutes"]))
        vol = np.asarray(s["vol_annual"])
        g = axes([0, np.log10(1440) + 0.1], [0.6, 0.85], x_length=7.4, y_length=4.4,
                 xlabel=r"sampling interval (log scale)", ylabel=r"Bitcoin's 2020 volatility, from realized variance",
                 xticks=list(np.log10([1, 5, 15, 60, 240, 1440])),
                 xfmt=lambda u: {1: "1 min", 5: "5 min", 15: "15 min", 60: "1 h", 240: "4 h", 1440: "1 day"}[round(10 ** u)],
                 yticks=[0.6, 0.7, 0.8], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, m, vol, BM, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=BM) for a, b in zip(m, vol)])
        side = VGroup(
            MathTex(rf"\text{{every minute: }} {100 * vol[0]:.0f}\%", font_size=32, color=JUMP),
            MathTex(rf"\text{{every day: }} {100 * vol[-1]:.0f}\%", font_size=32, color=DRIFT),
            wrapped_label(r"the volatility signature plot (Andersen, Bollerslev, Diebold and Labys 2000): at the "
                          r"finest scales, the bid--ask bounce adds noise whose squares add up too", 4.6, 21, GREY_A),
            wrapped_label(r"realized variance estimates quadratic variation only between the noise and the sampling "
                          r"error; Part 7 builds volatility forecasts on it", 4.6, 21, ITO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        src = real_data(r"Binance BTCUSDT one-minute candles, 2020; subsampled over up to 30 offsets")
        with self.voiceover(
            "If prices were Brownian, their quadratic variation would be their variance, and you could measure it "
            "exactly by sampling faster and faster. Try it on Bitcoin in 2020. <bookmark mark='a'/> Summing squared "
            "daily returns gives a volatility of seventy-one percent. Summing squared one-minute returns gives "
            "eighty. <bookmark mark='b'/> At the finest scales the measured price bounces between the bid and the "
            "ask, and that noise has squares too, which add up. The curve is called the volatility signature plot. "
            "Practitioners sample at around five minutes, a compromise between noise and too few observations, and "
            "Part seven builds forecasts on it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dots), FadeIn(side[1]), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

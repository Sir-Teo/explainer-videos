from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import BTC, GAUSS, LOSS, PART, REAL, TAIL, VOL, bars, load, real_data


class Clusters(VoiceoverScene):
    def construct(self):
        c = load("cluster")
        self.card()
        self.strip(c)
        self.acf(c)
        self.leverage(c)

    def card(self):
        c = chapter_card(6, r"Volatility clusters", r"Is the size of today's move a clue to tomorrow's?",
                         lit=(1929, 1987, 2008), part=PART)
        with self.voiceover("Chapter six. Volatility clusters."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def strip(self, c):
        t, r = np.asarray(c["t_all"]), np.asarray(c["r_all"])
        g = axes([1926, 2021], [-0.2, 0.2], x_length=12.0, y_length=2.6, ylabel=r"daily return",
                 xticks=[1930, 1950, 1970, 1990, 2010], yticks=[-0.1, 0, 0.1], xfmt=lambda v: f"{int(v)}",
                 yfmt=lambda v: f"{100 * v:+.0f}\\%" if v else "0", font_size=16).to_edge(UP, buff=0.55)
        ax = g.ax
        line = VMobject(stroke_width=0.7, color=REAL).set_points_as_corners(
            [ax.c2p(a, float(np.clip(b, -0.19, 0.19))) for a, b in zip(t, r)])
        g2 = axes([1926, 2021], [0, 0.9], x_length=12.0, y_length=2.2, ylabel=r"volatility, each month (annualized)",
                  xticks=[1930, 1950, 1970, 1990, 2010], yticks=[0, 0.4, 0.8], xfmt=lambda v: f"{int(v)}",
                  yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16).next_to(g, DOWN, buff=0.45)
        a2 = g2.ax
        rv = curve(a2, np.asarray(c["rv_t"]), np.clip(np.asarray(c["rv"]), 0, 0.89), VOL, stroke_width=2)
        ann = VGroup()
        for yr, txt in ((1932.5, r"1929--33"), (1987.8, r"1987"), (2008.8, r"2008"), (2020.2, r"2020")):
            ann.add(label(txt, font_size=18, color=TAIL).next_to(a2.c2p(yr, 0.85), UP, buff=0.02))
        src = real_data(r"Ken French's daily US market returns, 1926--2020")
        with self.voiceover(
            "Ninety-four years of daily returns on one line. <bookmark mark='a'/> It is not static. There are long "
            "calm stretches, and storms: the early 1930s, 1987, 2008, March 2020. Big moves come in clusters. "
            "<bookmark mark='b'/> Below, each month's volatility. It wanders over a range of ten to one, and it "
            "lingers: a wild month is followed by wild months, a calm one by calm ones. In 1963 Benoit Mandelbrot "
            "put it in one sentence: large changes tend to be followed by large changes, of either sign, and small "
            "changes by small changes."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(line), run_time=5, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(rv), run_time=3)
            self.play(LaggedStart(*[FadeIn(a) for a in ann], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def acf(self, c):
        lags = np.asarray(c["lags"], float)
        g = axes([0, np.log10(260)], [-0.08, 0.35], x_length=7.4, y_length=4.6, xlabel=r"lag, trading days (log scale)",
                 ylabel=r"autocorrelation", xticks=[0, 1, 2], xfmt=lambda v: f"{10 ** v:.0f}",
                 yticks=[0, 0.1, 0.2, 0.3], font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        x = np.log10(lags)
        band = Rectangle(width=ax.x_length, height=ax.c2p(0, c["band"])[1] - ax.c2p(0, -c["band"])[1], stroke_width=0,
                         fill_color=GREY_D, fill_opacity=0.5).move_to(ax.c2p(np.log10(260) / 2, 0))
        l_r = curve(ax, x, np.clip(np.asarray(c["acf_r"]), -0.08, 0.35), REAL, stroke_width=2.5)
        l_a = curve(ax, x, np.clip(np.asarray(c["acf_abs"]), -0.08, 0.35), VOL, stroke_width=3.5)
        l_s = curve(ax, x, np.clip(np.asarray(c["acf_shuffled"]), -0.08, 0.35), GAUSS, stroke_width=2)
        xb = np.log10(np.asarray(c["btc_lags"], float))
        l_b = curve(ax, xb, np.clip(np.asarray(c["btc_acf_abs"]), -0.08, 0.35), BTC, stroke_width=2.5)
        leg = legend([(REAL, r"returns $r_t$"), (VOL, r"size of the move $|r_t|$"),
                      (GAUSS, r"$|r_t|$, the days shuffled"), (BTC, r"Bitcoin's $|r_t|$, 2017--2020")], font_size=22)
        leg.to_edge(RIGHT, buff=0.5).shift(UP * 1.9)
        facts = VGroup(
            MathTex(rf"\rho_1(r) = {c['acf_r'][0]:+.2f}", font_size=30, color=REAL),
            MathTex(rf"\rho_1(|r|) = {c['acf_abs'][0]:.2f}", font_size=30, color=VOL),
            MathTex(rf"\rho_{{250}}(|r|) = {c['acf_abs'][-1]:.2f}", font_size=30, color=VOL),
            MathTex(rf"\rho_k(|r|) \approx k^{{-{c['beta']:.2f}}}", font_size=30, color=VOL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(leg, DOWN, buff=0.45).align_to(leg, LEFT)
        lesson = wrapped_label(r"uncorrelated, but not independent: a martingale, not a random walk", 4.3, 24,
                               QC.IDEA).next_to(facts, DOWN, buff=0.4).align_to(leg, LEFT)
        with self.voiceover(
            "Clustering can be measured. The blue line is the autocorrelation of returns themselves, lag by lag "
            "out to a year: inside the grey band of noise almost everywhere. The direction of tomorrow's move is "
            "not predictable from today's, just as Samuelson said. <bookmark mark='a'/> The teal line is the "
            "autocorrelation of the size of the move, the absolute return. "
            f"{c['acf_abs'][0]:.2f} at one day, and still {c['acf_abs'][-1]:.2f} a year later. It decays slowly, "
            f"roughly like the lag to the power minus {c['beta']:.2f}, a long memory. <bookmark mark='c'/> Shuffle "
            "the days into random order, the grey line, and the memory is gone: it was in the order, not in the "
            "days. <bookmark mark='d'/> Bitcoin, in orange, clusters too, with a shorter memory. "
            "<bookmark mark='e'/> So the market is a martingale but not a random walk: the direction is "
            "unpredictable, the size is not. Robert Engle's model of exactly this, ARCH, won him a Nobel prize, and "
            "it is the subject of Part seven."
        ) as vo:
            self.play(FadeIn(g), FadeIn(band))
            self.play(Create(l_r), FadeIn(leg[0]), run_time=2)
            self.play(FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(Create(l_a), FadeIn(leg[1]), run_time=2)
            self.play(FadeIn(facts[1]), FadeIn(facts[2]))
            self.play(FadeIn(facts[3]))
            vo.wait_until("c")
            self.play(Create(l_s), FadeIn(leg[2]))
            vo.wait_until("d")
            self.play(Create(l_b), FadeIn(leg[3]))
            vo.wait_until("e")
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()

    def leverage(self, c):
        k = np.asarray(c["lev_k"])
        lev = np.asarray(c["lev"])
        g = axes([-21, 21], [-0.14, 0.04], x_length=7.8, y_length=4.2, xlabel=r"lag $k$, trading days",
                 ylabel=r"$\operatorname{corr}(r_t,\ |r_{t+k}|)$", xticks=[-20, -10, 0, 10, 20],
                 yticks=[-0.1, -0.05, 0], font_size=18).to_edge(LEFT, buff=0.8).shift(DOWN * 0.6)
        ax = g.ax
        bb = bars(ax, k, lev, ax.x_length / 42 * 0.7, VOL, LOSS)
        left = label(r"past size, today's direction", font_size=22, color=GREY_A).next_to(ax.c2p(-11, 0.04), DOWN,
                                                                                            buff=0.05)
        right = label(r"today's direction, future size", font_size=22, color=LOSS).next_to(ax.c2p(11, 0.04), DOWN,
                                                                                            buff=0.05)
        card = definition_card(r"The leverage effect", r"Falling prices raise future volatility; rising prices "
                               r"don't lower it as much. Named by Fischer Black (1976): a falling share price raises "
                               r"a firm's debt relative to its equity.", width=4.4, color=LOSS, font_size=22)
        card.to_edge(RIGHT, buff=0.3).shift(UP * 0.4)
        nums = MathTex(rf"k = 1\dots 5:\ {np.mean(lev[(k >= 1) & (k <= 5)]):+.2f}\qquad "
                       rf"k = -5\dots -1:\ {np.mean(lev[(k <= -1) & (k >= -5)]):+.2f}", font_size=28)
        nums.next_to(g, UP, buff=0.4)
        with self.voiceover(
            "One more asymmetry. Correlate today's return with the size of moves to come, and with the size of "
            "moves before. <bookmark mark='a'/> To the right, today's return against future volatility: negative "
            f"for weeks. About {np.mean(lev[(k >= 1) & (k <= 5)]):+.2f} for the next five days. A fall today "
            "means bigger moves tomorrow. <bookmark mark='b'/> To the left, past volatility against today's "
            "direction: close to nothing. Volatility does not predict the direction; the direction predicts the "
            "volatility. <bookmark mark='c'/> Fischer Black named it the leverage effect in 1976, reasoning that a "
            "falling share price makes a company more indebted and so riskier. The effect is too large for that "
            "story alone, and it will come back as the skew of option prices, in Parts ten and twelve: markets "
            "charge more for protection against falls, because falls bring storms."
        ) as vo:
            self.play(FadeIn(g), FadeIn(left), FadeIn(right))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, UP if v < 0 else DOWN) for b_, v in zip(bb, lev) if True][21:],
                                  lag_ratio=0.08), run_time=2)
            self.play(FadeIn(nums))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, UP if v < 0 else DOWN) for b_, v in zip(bb, lev)][:21],
                                  lag_ratio=0.08), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(card, shift=LEFT * 0.2))
        self.wait(0.4)
        self.clear_scene()

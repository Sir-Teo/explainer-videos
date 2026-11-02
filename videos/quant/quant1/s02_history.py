from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import BTC, GAUSS, PART, REAL, load, real_data


class History(VoiceoverScene):
    def construct(self):
        r = load("regnault")
        self.card()
        self.people()
        self.fan(r)
        self.law(r)

    def card(self):
        c = chapter_card(1, r"Paris, 1863 and 1900", r"Why should a price move like a coin?", lit=(1900,), part=PART)
        with self.voiceover("Chapter one. Paris, 1863 and 1900."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def people(self):
        c1 = history_card(1863, r"Jules Regnault, a stockbroker's assistant",
                          r"\textit{Calcul des chances et philosophie de la Bourse}: the price's deviation grows in "
                          r"proportion to the square root of time", width=6.0, font_size=23)
        c2 = history_card(1900, r"Louis Bachelier, Paris",
                          r"\textit{Th\'eorie de la sp\'eculation}: French government bonds (\textit{rentes}) and "
                          r"their options, priced with a random walk; Poincar\'e's report; graded "
                          r"\textit{honorable}", width=6.0, font_size=23)
        c3 = history_card(1955, r"Leonard Savage, then Paul Samuelson",
                          r"Savage comes across Bachelier's work and sends postcards to economists asking whether "
                          r"they know it; Samuelson tracks down the thesis and builds on it", width=6.0, font_size=23)
        cards = VGroup(c1, c2, c3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(LEFT, buff=0.6)
        sq = MathTex(r"\text{spread} \propto \sqrt{t}", font_size=56, color=QC.IDEA).to_edge(RIGHT, buff=1.2).shift(UP * 1.6)
        walk = MathTex(r"P_{t+1} = P_t + \varepsilon_{t+1}", font_size=48, color=REAL).next_to(sq, DOWN, buff=1.0)
        bach = wrapped_label(r"Bachelier: the price is as likely to rise as to fall; the speculator's mathematical "
                             r"expectation is zero", 5.0, 22, GREY_A)
        bach.next_to(walk, DOWN, buff=0.4).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "The idea that prices move by chance is older than modern finance. In 1863 Jules Regnault, a "
            "stockbroker's assistant in Paris, published a book on chance and the philosophy of the Bourse. Its main "
            "claim: how far a price strays grows with the square root of time. Four times as long, twice as far. "
            "<bookmark mark='a'/> In 1900 Louis Bachelier, a student of Henri Poincaré, defended a thesis on the "
            "theory of speculation. He modelled the price of French government bonds as a random walk, a sum of "
            "independent little moves, and used it to price options on them, decades before anyone else. His "
            "starting principle was blunt: the expectation of the speculator is zero. Poincaré's report praised "
            "it; the jury graded it honorable, and the mathematics of chance in markets went quiet for fifty "
            "years. <bookmark mark='b'/> In the 1950s the statistician Leonard Savage came across Bachelier's work "
            "in a library and sent postcards to economists asking if they knew it. Paul Samuelson tracked down the "
            "thesis, and the random walk entered economics."
        ) as vo:
            self.play(FadeIn(c1, shift=RIGHT * 0.2))
            self.play(Write(sq))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=RIGHT * 0.2))
            self.play(Write(walk), FadeIn(bach))
            vo.wait_until("b")
            self.play(FadeIn(c3, shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fan(self, r):
        Y = r["yearly"]
        n, m = Y.shape
        sd1 = r["sd1"]
        g = axes([0, m - 1], [-0.75, 0.75], x_length=9.6, y_length=5.0, xlabel=r"trading days into the year",
                 ylabel=r"log return since the start of the year", xticks=[0, 63, 126, 189, 252],
                 yticks=[-0.6, -0.3, 0, 0.3, 0.6], yfmt=lambda v: f"{100 * v:+.0f}\\%" if v else "0", font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        t = np.arange(m)
        lines = VGroup(*[curve(ax, t, np.clip(y, -0.74, 0.74), REAL, stroke_width=1.1).set_stroke(opacity=0.35)
                         for y in Y])
        env = VGroup()
        for k, op in ((1, 0.95), (2, 0.6)):
            for s in (1, -1):
                env.add(curve(ax, t, s * k * sd1 * np.sqrt(t), QC.IDEA, stroke_width=3).set_stroke(opacity=op))
        lab1 = MathTex(r"\pm\,\sigma\sqrt t", font_size=30, color=QC.IDEA).next_to(ax.c2p(252, sd1 * np.sqrt(252)),
                                                                                    RIGHT, buff=0.1)
        lab2 = MathTex(r"\pm\,2\sigma\sqrt t", font_size=26, color=QC.IDEA).next_to(ax.c2p(252, 2 * sd1 * np.sqrt(252)),
                                                                                    RIGHT, buff=0.1)
        side = VGroup(
            label(rf"{n} stretches of 252 trading days,", font_size=24),
            label(r"one line each, all starting at zero", font_size=24),
            MathTex(rf"\sigma_{{\text{{day}}}} = {100 * sd1:.2f}\%", font_size=34, color=QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.5).shift(DOWN * 2.3)
        src = real_data(r"US market, July 1926 to December 2020: Ken French's daily value-weighted returns, "
                        r"dividends included")
        with self.voiceover(
            f"Regnault's law can be checked on data he never saw. Here are {n} stretches of two hundred and "
            "fifty-two trading days of the American stock market, every year since 1926, each drawn from zero. "
            "<bookmark mark='a'/> The gold curves are the square-root law: one daily standard deviation, "
            f"{100 * sd1:.2f} percent, times the square root of the number of days. Two thirds of a bell curve lies "
            "inside the inner pair, ninety-five percent inside the outer. The spaghetti spreads out just as "
            "Regnault said: fast at first, then slower, never in a straight line."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.03, run_time=5))
            vo.wait_until("a")
            self.play(*[Create(e) for e in env], FadeIn(lab1), FadeIn(lab2), FadeIn(side), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    def law(self, r):
        h, sd = np.asarray(r["h"], float), np.asarray(r["sd"], float)
        hb, sdb = np.asarray(r["h_btc"], float), np.asarray(r["sd_btc"], float)
        g = axes([0, np.log10(600)], [np.log10(0.006), np.log10(0.9)], x_length=7.4, y_length=4.8,
                 xlabel=r"horizon, trading days (log scale)", ylabel=r"standard deviation of the return (log scale)",
                 xticks=[0, 1, 2], xfmt=lambda v: f"{10 ** v:g}", yticks=[np.log10(0.01), np.log10(0.1)],
                 yfmt=lambda v: f"{100 * 10 ** v:.0f}\\%", font_size=18)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        dots_us = VGroup(*[Dot(ax.c2p(np.log10(a), np.log10(b)), radius=0.07, color=REAL) for a, b in zip(h, sd)])
        dots_b = VGroup(*[Dot(ax.c2p(np.log10(a), np.log10(b)), radius=0.07, color=BTC) for a, b in zip(hb, sdb)])
        xs = np.log10(np.array([1, 550]))
        half_us = DashedLine(ax.c2p(xs[0], np.log10(sd[0])), ax.c2p(xs[1], np.log10(sd[0] * np.sqrt(550))),
                             color=GAUSS, stroke_width=2, dash_length=0.08)
        half_b = DashedLine(ax.c2p(xs[0], np.log10(sdb[0])), ax.c2p(np.log10(260), np.log10(sdb[0] * np.sqrt(260))),
                            color=GAUSS, stroke_width=2, dash_length=0.08)
        leg = legend([(REAL, r"US market, 1926--2020"), (BTC, r"Bitcoin, Aug 2017 -- Dec 2020"),
                      (GAUSS, r"slope $\tfrac12$: the square-root law")], font_size=22)
        leg.to_edge(RIGHT, buff=0.5).shift(UP * 1.8)
        fit = VGroup(
            label(r"fitted slopes", font_size=24, color=GREY_A),
            MathTex(rf"\text{{US}}\ {r['slope']:.2f}", font_size=34, color=REAL),
            MathTex(rf"\text{{Bitcoin}}\ {r['slope_btc']:.2f}", font_size=34, color=BTC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(leg, DOWN, buff=0.6).align_to(leg, LEFT)
        ratio = r["sd"][9] / (r["sd"][0] * np.sqrt(252))
        more = wrapped_label(rf"one year: ${100 * r['sd'][9]:.1f}\%$ measured against "
                             rf"${100 * r['sd'][0] * np.sqrt(252):.1f}\%$ from the daily figure: "
                             r"slightly more than the law allows", 3.7, 21, GREY_B)
        more.next_to(fit, DOWN, buff=0.4).align_to(leg, LEFT)
        src = real_data(r"standard deviations of overlapping $h$-day log returns; Bitcoin: Binance BTC/USDT daily")
        with self.voiceover(
            "Now the law itself. On log scales a square root is a straight line of slope one half. Each blue dot is "
            "the spread of the market's return over a horizon from one day to two years. <bookmark mark='a'/> "
            f"They lie on a line of slope {r['slope']:.2f}. Bitcoin, the orange dots, trades at four times the "
            f"volatility, and its slope is {r['slope_btc']:.2f}. <bookmark mark='b'/> A century and a half later, "
            "Regnault's law holds almost exactly, and the word almost will matter: over a year the market's spread is "
            f"{100 * (ratio - 1):.0f} percent more than the daily figure predicts, a first hint that tomorrow is "
            "not quite independent of today. Chapter four measures it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots_us], lag_ratio=0.15), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(half_us), FadeIn(leg[2]))
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots_b], lag_ratio=0.15), Create(half_b),
                      FadeIn(leg[1]))
            self.play(FadeIn(fit))
            vo.wait_until("b")
            self.play(FadeIn(more))
        self.wait(0.4)
        self.clear_scene()

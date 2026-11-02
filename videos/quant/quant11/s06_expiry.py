from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, load, real_data


class Expiry(VoiceoverScene):
    def construct(self):
        self.card()
        self.pin()
        self.dispersion(load("dispersion"))

    def card(self):
        c = chapter_card(5, r"Expiry, pin risk, and dispersion", r"What happens in the last hour, and across a whole "
                         r"index?", part=PART)
        with self.voiceover("Chapter five. Expiry, pin risk, and dispersion."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pin(self):
        S = np.linspace(96, 104, 161)
        g = axes([96, 104], [0, 1], x_length=6.2, y_length=3.8, xlabel=r"underlying near the strike of 100",
                 ylabel=r"call delta", xticks=[96, 98, 100, 102, 104], yticks=[0, 0.5, 1], font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        cols = [ALT, VEGA, THETA]
        labs = [r"a day left", r"an hour left", r"a minute left"]
        taus = [1 / 365, 1 / (365 * 24), 1 / (365 * 24 * 60)]
        lines = VGroup(*[curve(ax, S, bs.greeks(S, 100.0, tau, 0.5)["delta"], c, stroke_width=3) for tau, c in zip(taus, cols)])
        leg = legend(list(zip(cols, labs)), font_size=19).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        gam_day = float(bs.greeks(100.0, 100.0, 1 / 365, 0.5)["gamma"])
        gam_min = float(bs.greeks(100.0, 100.0, 1 / (365 * 24 * 60), 0.5)["gamma"])
        side = VGroup(
            MathTex(r"\Gamma_{\text{ATM}} \approx \frac{1}{S\,\sigma\sqrt{2\pi\,\tau}}", font_size=34, color=GAMMA),
            MathTex(rf"\text{{a day: }} {gam_day:.2f},\quad \text{{a minute: }} {gam_min:.1f}", font_size=28),
            wrapped_label(r"at the strike, gamma grows without bound as expiry nears: delta flips from 0 to 1 on a tiny "
                          r"move, and a hedger trades its whole position back and forth", 4.4, 20, GREY_A),
            wrapped_label(r"pin risk: short an option struck where the stock closes, you do not know until the next "
                          r"day whether you will be assigned; for American calls, exercise early only to capture a "
                          r"dividend worth more than the put's value", 4.4, 20, THETA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Options are most dangerous at the end. At the strike, gamma grows like one over the square root of the "
            f"time left: a day before expiry it is {gam_day:.2f} here; a minute before, {gam_min:.1f}. "
            "<bookmark mark='a'/> Delta becomes a step: a tiny move across the strike flips it from zero to one, and "
            "a hedger must trade the whole position back and forth. <bookmark mark='b'/> Pin risk is the related "
            "problem for a seller: if the stock closes right at the strike, you do not know until the next day "
            "whether you will be assigned, and you hold the overnight risk either way. And for American calls, "
            "there is exactly one reason to exercise early: to capture a dividend worth more than the option's "
            "remaining time value."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.5), FadeIn(leg), FadeIn(side[2]),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def dispersion(self, d):
        t, rho = np.asarray(d["t"]), np.asarray(d["rho"])
        g = axes([1929, 2021], [0, 1], x_length=8.0, y_length=3.8, ylabel=r"average correlation of 40 US industries",
                 xticks=[1940, 1960, 1980, 2000, 2020], xfmt=lambda u: f"{int(u)}", yticks=[0, 0.25, 0.5, 0.75, 1],
                 font_size=17).to_edge(LEFT, buff=0.6).to_edge(DOWN, buff=0.6)
        ax = g.ax
        line = curve(ax, t, rho, VEGA, stroke_width=2.5)
        eq = MathTex(r"\sigma_I^2 = \sum_i w_i^2\sigma_i^2 + \rho\sum_{i \ne j} w_i w_j\,\sigma_i\sigma_j", font_size=34,
                     color=OPT).to_edge(UP, buff=0.5)
        pk = d["peaks"]
        side = VGroup(
            wrapped_label(r"solve for $\rho$ with implied vols: implied correlation. Dispersion sells index volatility "
                          r"and buys single-stock volatility, a bet that correlation will be lower than implied", 4.2, 20,
                          GREY_A),
            label(rf"realized here: median {d['median']:.2f}", font_size=22, color=VEGA),
            label(rf"crises: {pk['1929-33']:.2f} (1929--33), {pk['1987']:.2f} (1987), {pk['2008']:.2f} (2008)",
                  font_size=20, color=THETA),
            label(rf"low: {d['low']:.2f} ({int(d['low_t'])}, the dot-com split)", font_size=20, color=GAMMA),
            wrapped_label(r"correlations rise in crashes, exactly when the short index leg hurts: the dispersion trade "
                          r"is short a crash", 4.2, 20, THETA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.4)
        src = real_data(r"Kenneth French's 49 industries (40 with full histories), monthly, rolling 36 months, 1926--2020")
        with self.voiceover(
            "A whole index can be traded against its parts. An index's variance is the weighted variances of its "
            "members plus a term for their correlations. Put in implied volatilities, solve for the correlation, and "
            "you have implied correlation. Dispersion traders sell index volatility and buy volatility on the "
            "members: a bet that the members will move less together than the index price assumes. "
            "<bookmark mark='a'/> Here is the realized version, from ninety years of American industries. The "
            f"average correlation is usually around {d['median']:.2f}. It spiked in the Depression, in 1987 and in "
            f"2008, and fell to {d['low']:.2f} in {int(d['low_t'])}, when technology and the rest of the market went "
            "separate ways. <bookmark mark='b'/> Correlations rise in crashes, exactly when a short position in index "
            "volatility hurts most. Dispersion is a short crash bet, and it is priced like one."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(src), Create(line), FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

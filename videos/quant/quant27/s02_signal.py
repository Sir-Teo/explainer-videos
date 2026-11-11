from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, LINEAR, MOM, NET, PART, ask, fit_right, illustration, load

NAMES = {"dp": r"dividend-price", "dy": r"dividend yield", "ep": r"earnings-price", "de": r"payout", "svar": r"variance",
         "bm": r"book-to-market", "ntis": r"net issuance", "tbl": r"T-bill rate", "lty": r"long yield",
         "ltr": r"long bond return", "tms": r"term spread", "dfy": r"default yield", "dfr": r"default return",
         "infl": r"inflation", "mkt": r"last month's return"}


class Signal(VoiceoverScene):
    def construct(self):
        s = load("snr")
        self.card()
        self.predictors(s)
        self.four()
        self.cat()
        self.consequences()
        self.question()

    def card(self):
        c = chapter_card(1, r"A low signal-to-noise world", r"Why is finance harder than recognising a cat?", lit=(2019,),
                         part=PART)
        with self.voiceover("Chapter one. Why predicting returns is a different kind of machine-learning problem."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def predictors(self, s):
        rows = sorted(s["predictors"], key=lambda r: -r["r2"])
        xmax = max(0.25, np.ceil(100*max(r["r2"] for r in rows)*5)/5)
        g = axes([0, xmax], [-0.6, len(rows) - 0.4], x_length=6.2, y_length=5.2, xlabel='in-sample $R^2$, \\%', xticks=list(np.linspace(0,xmax,5)), yticks=[], font_size=18).to_edge(
            LEFT, buff=2.6).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for i, r in enumerate(rows):
            y = len(rows) - 1 - i
            v = 100 * r["r2"]
            x0, x1 = ax.c2p(0, y)[0], ax.c2p(v, y)[0]
            bars.add(VGroup(Rectangle(width=max(x1 - x0, 0.01), height=0.24, stroke_width=0, fill_color=LINEAR,
                                      fill_opacity=0.85).move_to([(x0 + x1) / 2, ax.c2p(0, y)[1], 0]),
                            label(NAMES[r["name"]], font_size=20, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.15)))
        side = VGroup(
            MathTex(rf"\text{{best}}:\ {100 * rows[0]['r2']:.2f}\%", font_size=28, color=LINEAR),
            wrapped_label('Fifteen separate in-sample fits to next-month volatility-normalised returns. Updated monthly data need release/vintage clocks. Published OOS comparisons are a separate study.', 3.4, 23, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            f"These original regressions use fifteen monthly predictors, separately, to fit the next month's volatility-normalised market return. <bookmark mark='a'/> The best in-sample R squared is {100*rows[0]['r2']:.2f} percent. The scaling volatility uses preceding returns, excluding the target month. Updated economic observations still need publication and vintage clocks for a deployable forecast. Welch and Goyal's published out-of-sample comparisons against a historical mean are a separate study, rather than these in-sample fits."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.1) for b_ in bars], lag_ratio=0.08), FadeIn(side),
                      run_time=3)
        self.add(illustration(r"Amit Goyal's update of the Welch--Goyal data"))
        self.wait(0.4)
        self.clear_scene()

    def four(self):
        cards = VGroup(
            desk_question(r"the signal is small", 'Competition and costs can reduce exploitable signals. Small predictability is an empirical challenge, not an arbitrage theorem.',
                          width=12.2, font_size=27),
            desk_question(r"the data are few", r"a century of monthly market returns is 1{,}200 observations; ImageNet "
                          r"has fourteen million labelled images. More stocks help, but they move together", width=12.2,
                          font_size=27),
            desk_question(r"the world changes", 'Market relationships and regimes may change. Observed decay does not identify trading as its sole cause.', width=12.2,
                          font_size=27),
            desk_question(r"the cost of error is asymmetric", r"a model that is confidently wrong in a crash can lose "
                          r"more than years of small correct forecasts made", width=12.2, font_size=27),
        ).arrange(DOWN, buff=0.2)
        if cards.height > 7.0:
            cards.scale_to_fit_height(7.0)
        with self.voiceover(
            "Return prediction presents several difficulties. <bookmark mark='a'/> Competition and implementation costs can limit exploitable signals, although small R squared is not a logical necessity. <bookmark mark='b'/> A century of monthly observations supplies only twelve hundred dates, and assets share common movements. <bookmark mark='c'/> Economic relationships and regimes can change; observed decay does not isolate trading as its unique cause. <bookmark mark='d'/> Losses also depend on position sizing and the sizes of mistakes, especially in stressed markets."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def cat(self):
        rng = np.random.default_rng(3)
        t = np.linspace(0, 1, 200)
        sig = 0.5 * np.sin(2 * np.pi * 2 * t)
        panels = VGroup()
        for k, (snr, title, col) in enumerate(((10.0, r"fixed synthetic example: lower noise", GOOD),
                                               (0.1, r"fixed synthetic example: higher noise", BAD))):
            noise = rng.standard_normal(len(t)) * 0.5 / np.sqrt(snr)
            ylim = max(1.0, float(np.ceil(np.max(np.abs(sig+noise)))))
            g = axes([0, 1], [-ylim, ylim], x_length=5.6, y_length=2.8, xticks=[0,.5,1], yticks=[-ylim,0,ylim], font_size=17)
            ax = g.ax
            dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.018, color=col) for x, y in zip(t, sig + noise)])
            panels.add(VGroup(label(title, font_size=23, color=col), VGroup(g, dots, curve(ax, t, sig, WHITE,
                                                                                     stroke_width=2))).arrange(
                DOWN, buff=0.15))
        panels.arrange(RIGHT, buff=0.6).move_to(UP * 0.4)
        foot = wrapped_label('Fixed synthetic sine signal with two noise scales; full points shown. Shrinkage and averaging trade bias against variance. Evaluate forecasts independently, with appropriate risk and execution assumptions.', 12.0, 22,
                             GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "These are fixed synthetic illustrations, rather than measured signal-to-noise estimates for photographs or markets. <bookmark mark='a'/> The left panel has lower noise around a sine signal. <bookmark mark='b'/> The right uses ten times the noise standard deviation, or one hundred times its variance. Each panel displays every point with its full vertical range. Shrinkage, averaging and independent evaluation can help, but no remedy guarantees a useful trading forecast."
        ) as vo:
            self.add(panels[0])
            vo.wait_until("a")
            self.wait(.1)
            vo.wait_until("b")
            self.play(FadeIn(panels[1]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def consequences(self):
        rows = [cmath(r"\mathbb{E}\big[(y - \hat f)^2\big]", r"=", r"\sigma^2_\varepsilon + \text{bias}^2 + \text{variance}",
                      font_size=38, colors={r"\mathbb{E}\big[(y - \hat f)^2\big]": WHITE}),
                cmath(r"R^2_{\text{oos}}", r"=", r"1 - \frac{\sum (r_{i,t} - \hat r_{i,t})^2}{\sum r_{i,t}^2}", font_size=38,
                      colors={r"R^2_{\text{oos}}": HURDLE})]
        whys = [why(r"a forecast's error: irreducible noise, plus bias, plus the variance of an estimate fitted to a "
                    r"finite sample, under the stated squared-loss assumptions; every term matters"),
                why(r"Gu, Kelly and Xiu's yardstick, against a forecast of zero rather than the historical mean: for one "
                    r"asset, a historical-mean benchmark is a different forecasting comparison")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.5, buff=0.5, edge=6.9)
        with self.voiceover(
            "Under squared loss with the usual conditional-mean and training-randomness assumptions, expected error separates into irreducible noise, squared bias and estimation variance. <bookmark mark='a'/> Low signal makes that trade-off important, but does not make variance the only term. <bookmark mark='b'/> Our out-of-sample R squared compares squared error with a zero forecast. A historical-mean benchmark asks a different question. Neither estimate alone identifies attainable Sharpe, and a negative result does not establish that return prediction is impossible."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q=ask(r"In the explicit binary-signal model, population $R^2=0.5\%$ and 500 independent equal-risk bets give what ideal annual Sharpe? Why does arbitrary measured out-of-sample $R^2$ not imply that result?")
        with self.voiceover("Pause and predict. In the explicit binary-signal idealisation, use population R squared of half a percent and five hundred independent equal-risk bets. Calculate the ideal annual Sharpe. Then state why arbitrary measured out-of-sample R squared does not imply that result."):
            self.play(FadeIn(q))
        self.clear_scene()

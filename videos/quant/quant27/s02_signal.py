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
        g = axes([0, 1.0], [-0.6, len(rows) - 0.4], x_length=6.6, y_length=5.2, xlabel=r"in-sample $R^2$ for next "
                 r"month's market return, \%", xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[], font_size=13).to_edge(
            LEFT, buff=2.6).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for i, r in enumerate(rows):
            y = len(rows) - 1 - i
            v = 100 * r["r2"]
            x0, x1 = ax.c2p(0, y)[0], ax.c2p(v, y)[0]
            bars.add(VGroup(Rectangle(width=max(x1 - x0, 0.01), height=0.24, stroke_width=0, fill_color=LINEAR,
                                      fill_opacity=0.85).move_to([(x0 + x1) / 2, ax.c2p(0, y)[1], 0]),
                            label(NAMES[r["name"]], font_size=14, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.15)))
        side = VGroup(
            MathTex(rf"\text{{best}}:\ {100 * rows[0]['r2']:.2f}\%", font_size=28, color=LINEAR),
            wrapped_label(r"Welch and Goyal's fifteen predictors, one at a time, fitted on all of 1930--2020: the "
                          r"in-sample $R^2$, the most flattering number there is. Out of sample, Welch and Goyal (2008) "
                          r"found most of them worse than the historical mean", 3.4, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Start with the market itself. These are the fifteen most studied predictors of the American stock "
            "market's return: valuation ratios, interest rates, credit spreads, inflation, last month's return. "
            "<bookmark mark='a'/> Fit each one to ninety years of monthly data, in sample, the most flattering test "
            "there is. The best explains less than one percent of next month's return. Most explain under a quarter of that. "
            "And Ivo Welch and Amit Goyal showed in 2008 that out of sample most of them did worse than simply "
            "predicting the historical average."
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
            desk_question(r"the signal is small", r"if returns were predictable with high $R^2$, traders would trade on "
                          r"it until they were not: competition keeps the signal near the cost of exploiting it",
                          width=12.2, font_size=19),
            desk_question(r"the data are few", r"a century of monthly market returns is 1{,}200 observations; ImageNet "
                          r"has fourteen million labelled images. More stocks help, but they move together", width=12.2,
                          font_size=19),
            desk_question(r"the world changes", r"a cat today is a cat tomorrow; a pattern in returns, once found and "
                          r"traded, decays (Part 25), and regimes end (Part 26's technical rules)", width=12.2,
                          font_size=19),
            desk_question(r"the cost of error is asymmetric", r"a model that is confidently wrong in a crash can lose "
                          r"more than years of small correct forecasts made", width=12.2, font_size=19),
        ).arrange(DOWN, buff=0.2)
        if cards.height > 7.0:
            cards.scale_to_fit_height(7.0)
        with self.voiceover(
            "Ronen Israel, Bryan Kelly and Tobias Moskowitz asked in 2020 whether machines can learn finance, and listed "
            "why it is hard. <bookmark mark='a'/> The signal is small, and must be: if returns were very predictable, "
            "traders would trade on the prediction until they were not. <bookmark mark='b'/> The data are few: a "
            "century of monthly market returns is twelve hundred observations, where an image benchmark has fourteen "
            "million. <bookmark mark='c'/> The world changes: a pattern, once found and traded, decays, as Part "
            "twenty-five measured. <bookmark mark='d'/> And errors are asymmetric: a model confidently wrong in a crash "
            "can lose more than years of small, correct forecasts made."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def cat(self):
        rng = np.random.default_rng(3)
        t = np.linspace(0, 1, 200)
        sig = 0.5 * np.sin(2 * np.pi * 2 * t)
        panels = VGroup()
        for k, (snr, title, col) in enumerate(((10.0, r"an image: signal-to-noise about 10", GOOD),
                                               (0.1, r"a month's return: about 0.01 to 0.1", BAD))):
            noise = rng.standard_normal(len(t)) * 0.5 / np.sqrt(snr)
            g = axes([0, 1], [-3, 3], x_length=5.6, y_length=2.8, xticks=[], yticks=[], font_size=12)
            ax = g.ax
            dots = VGroup(*[Dot(ax.c2p(x, np.clip(y, -3, 3)), radius=0.018, color=col) for x, y in zip(t, sig + noise)])
            panels.add(VGroup(label(title, font_size=19, color=col), VGroup(g, dots, curve(ax, t, sig, WHITE,
                                                                                     stroke_width=2))).arrange(
                DOWN, buff=0.15))
        panels.arrange(RIGHT, buff=0.6).move_to(UP * 0.4)
        foot = wrapped_label(r"the same white signal under two noise levels (illustration). A flexible model fitted to "
                             r"the right panel learns mostly noise; the remedies are shrinkage, averaging many models, "
                             r"and judging forecasts by what they earn rather than how well they fit", 12.0, 18,
                             GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is what a low signal-to-noise ratio looks like. <bookmark mark='a'/> On the left, a pattern with "
            "little noise around it, like the pixels of a photograph: any flexible model will find it. "
            "<bookmark mark='b'/> On the right, the same pattern buried in noise a hundred times larger, which is "
            "closer to returns. A flexible model fitted here learns mostly the noise. So the remedies of this part are "
            "always the same three: shrink hard, average many models, and judge a forecast by what it earns out of "
            "sample, not by how well it fits."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
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
                    r"finite sample. When the noise dwarfs the signal, the variance term decides everything"),
                why(r"Gu, Kelly and Xiu's yardstick, against a forecast of zero rather than the historical mean: for one "
                    r"asset the sample mean is itself so noisy that beating it says little")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.5, buff=0.5, edge=6.9)
        with self.voiceover(
            "In symbols. <bookmark mark='a'/> A forecast's squared error is the irreducible noise, plus bias, plus the "
            "variance of an estimate fitted to a finite sample. When the noise dwarfs the signal, the variance term "
            "decides everything, and a model that is a little biased but stable usually wins. <bookmark mark='b'/> And "
            "the yardstick: out-of-sample R squared against a forecast of zero, as Gu, Kelly and Xiu define it. For a "
            "single asset the historical mean is itself so noisy that beating it says little."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = ask(r"a model predicts monthly returns on 500 stocks with an out-of-sample $R^2$ of 0.5\%. If the stocks' "
                r"errors were independent, roughly what Sharpe ratio could a long-short portfolio earn? Why is the real one "
                r"lower?")
        with self.voiceover(
            "Pause and predict. A model predicts monthly returns on five hundred stocks with an out-of-sample R squared "
            "of half a percent. If the stocks' errors were independent, roughly what Sharpe ratio could a long-short "
            "portfolio earn, and why is the real one lower?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

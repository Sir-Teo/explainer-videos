from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import BAD, GOOD, HURDLE, OU_C, PART, SPREAD_C, fit_right, load


class Coint(VoiceoverScene):
    def construct(self):
        c = load("coint")
        self.card()
        self.definition()
        self.test()
        self.years(c)
        self.persistence(c)
        self.half_lives(c)
        self.johansen()
        self.twins()
        self.screening(c)
        self.question()

    def card(self):
        c = chapter_card(3, r"Cointegration and the screening problem", r"If two prices are tied together, can a test find "
                         r"the tie?", part=PART)
        with self.voiceover("Chapter three. Part seven introduced cointegration: two wandering series with a combination "
                            "that does not wander. It is the right model for a pair. Finding pairs with it is another "
                            "matter."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def definition(self):
        rows = [cmath(r"\log P_{1,t},\ \log P_{2,t}", r"\sim", r"I(1)", font_size=36),
                cmath(r"s_t", r"=", r"\log P_{1,t} - \beta\log P_{2,t} - \mu\ \sim\ I(0)", font_size=36,
                      colors={r"s_t": SPREAD_C}),
                cmath(r"\Delta\log P_{1,t}", r"=", r"-\alpha_1 s_{t-1} + \dots,\quad \Delta\log P_{2,t} = +\alpha_2 s_{t-1} "
                      r"+ \dots", font_size=30)]
        whys = [why(r"each log price has a unit root: its changes are stationary, its level is not"),
                why(r"Engle and Granger (1987): some combination of the two is stationary; $\beta$ is the hedge ratio, and "
                    r"$s_t$ the spread that pairs trading bets on"),
                why(r"the error-correction representation: at least one of the prices moves to close the gap, which is "
                    r"the economic reason a spread reverts")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The definition. <bookmark mark='a'/> Each log price has a unit root: it wanders. <bookmark mark='b'/> But some "
            "combination, one price minus beta times the other, is stationary: that is the spread, and beta is the "
            "hedge ratio. <bookmark mark='c'/> Granger's representation theorem says that then at least one price moves "
            "to close the gap. That correction is the economic content: something, an arbitrageur or a common cause, "
            "pulls the pair back together."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def test(self):
        rows = [cmath(r"\log P_1", r"=", r"\hat\mu + \hat\beta\log P_2 + \hat s_t", font_size=36),
                cmath(r"\Delta\hat s_t", r"=", r"\rho\,\hat s_{t-1} + \gamma\,\Delta\hat s_{t-1} + e_t", font_size=36),
                cmath(r"t_\rho", r"<", r"-3.34\ \Rightarrow\ \text{cointegrated at }5\%", font_size=34,
                      colors={r"-3.34": HURDLE})]
        whys = [why(r"step one: regress one log price on the other"),
                why(r"step two: an augmented Dickey--Fuller regression on the residual"),
                why(r"the critical value is not the usual $-1.96$, nor Dickey and Fuller's $-2.86$: the residual was fitted "
                    r"to look stationary, so the bar is higher (Engle and Yoo; MacKinnon)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The Engle-Granger test, from Part seven. <bookmark mark='a'/> Regress one log price on the other. "
            "<bookmark mark='b'/> Test the residual for a unit root. <bookmark mark='c'/> The critical value is minus "
            "three point three four, not minus two: the regression chose the hedge ratio that makes the residual look "
            "as stationary as possible, so the test must ask for more."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def years(self, c):
        yrs = np.asarray(c["years"], float)
        fr = 100 * np.asarray(c["frac"], float)
        g = axes([1990.4, 2020.6], [0, 22], x_length=8.0, y_length=4.2, xlabel=r"year",
                 ylabel=r"industry pairs that pass at 5\%, \%", xticks=[1991, 2000, 2010, 2020], yticks=[0, 10, 20],
                 xfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.0 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.22, height=max(abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), 0.01), fill_color=SPREAD_C,
                                  fill_opacity=0.85, stroke_width=0).move_to(ax.c2p(y, v / 2)) for y, v in zip(yrs, fr)])
        fp = 100 * c["false_positive"]
        line = DashedLine(ax.c2p(1990.4, fp), ax.c2p(2020.6, fp), color=BAD, stroke_width=2)
        ll = label(rf"unrelated random walks: {fp:.1f}\%", font_size=16, color=BAD).next_to(ax.c2p(2020.6, fp), UP,
                                                                                         buff=0.1).shift(LEFT * 2.0)
        avg = float(np.mean(fr))
        foot = wrapped_label(rf"{c['n_pairs']} randomly chosen pairs of the 49 industries, one calendar year of daily log "
                             r"total-return indices each; the dashed line: the same test on pairs of independent random "
                             r"walks of the same length", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now screen the industries, one year at a time. <bookmark mark='a'/> In a typical year about "
            f"{avg:.0f} percent of industry pairs pass the test. <bookmark mark='b'/> Run the same test on pairs of "
            f"independent random walks, which share nothing, and {fp:.1f} percent pass: the test's own false-positive "
            "rate. So the industries pass about twice as often as pure noise. Some ties are real, but most of the pairs "
            "a screen finds in any year are there by chance."
        ) as vo:
            self.play(FadeIn(g), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(ll))
        self.wait(0.4)
        self.clear_scene()

    def persistence(self, c):
        avg = float(np.mean(c["frac"]))
        items = [(r"pass next year, given passed this year", c["persist"], SPREAD_C),
                 (r"pass in any year, unconditionally", avg, GREY_B)]
        bars = VGroup()
        for j, (nm, v, col) in enumerate(items):
            r = Rectangle(width=60 * v, height=0.6, fill_color=col, fill_opacity=0.85, stroke_width=0)
            r.move_to([-3.0, 0.9 - 1.3 * j, 0], aligned_edge=LEFT)
            bars.add(VGroup(label(nm, font_size=21, color=col).next_to(r, UP, buff=0.12).align_to(r, LEFT), r,
                            MathTex(rf"{100 * v:.1f}\%", font_size=28).next_to(r, RIGHT, buff=0.2)))
        with self.voiceover(
            "The harder test: does a pair that passes this year pass next year? <bookmark mark='a'/> Of the pairs that "
            f"passed in one year, {100 * c['persist']:.1f} percent passed again the next. <bookmark mark='b'/> For a pair "
            f"chosen at random, the rate is {100 * avg:.1f} percent. Passing once is almost no evidence of passing "
            "again. A screen that selects pairs on this test is selecting, mostly, on noise."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]))
        self.wait(0.4)
        self.clear_scene()

    def half_lives(self, c):
        hl = np.asarray(c["half_lives"], float)
        hl = hl[(hl > 0) & (hl < 30)]
        edges = np.arange(0, 31, 1.5)
        h, _ = np.histogram(hl, edges)
        g = axes([0, 30], [0, float(h.max() * 1.15)], x_length=7.4, y_length=4.0, xlabel=r"half-life of the spread, days",
                 ylabel=r"pairs", xticks=[0, 10, 20, 30], yticks=[], font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=ax.c2p(edges[k + 1], 0)[0] - ax.c2p(edges[k], 0)[0] - 0.02,
                                  height=max(ax.c2p(0, h[k])[1] - ax.c2p(0, 0)[1], 0.005), fill_color=OU_C,
                                  fill_opacity=0.8, stroke_width=0).move_to(ax.c2p((edges[k] + edges[k + 1]) / 2, h[k] / 2))
                        for k in range(len(h))])
        rows = [cmath(r"\hat s_{t+1}", r"=", r"b\,\hat s_t + e", font_size=30),
                cmath(r"t_{1/2}", r"=", r"\frac{\ln 2}{-\ln b}", font_size=32, colors={r"t_{1/2}": OU_C})]
        side = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP * 1.0)
        fit_right(side)
        txt = wrapped_label(rf"the pairs that passed: median half-life {c['half_life_median']:.1f} days, fitted on the same "
                            r"year that selected them", 3.6, 16, GREY_A).next_to(side, DOWN, buff=0.5)
        fit_right(txt)
        with self.voiceover(
            "And the half-lives of the pairs that passed. <bookmark mark='a'/> Fit an autoregression to each spread; the "
            "half-life is log two over minus the log of its coefficient. <bookmark mark='b'/> The median is about "
            f"{c['half_life_median']:.0f} trading days: fast reversion, measured on the same year that picked the pair. "
            "A pair is chosen because its spread happened to revert quickly in that sample, so its measured half-life "
            "is biased short. Selection again."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(side))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(txt))
        self.wait(0.4)
        self.clear_scene()

    def johansen(self):
        rows = [cmath(r"\Delta y_t", r"=", r"\Pi\, y_{t-1} + \textstyle\sum_{k} \Gamma_k \Delta y_{t-k} + e_t", font_size=36),
                cmath(r"\Pi", r"=", r"\alpha\beta^\top,\quad \operatorname{rank}\Pi = r", font_size=36,
                      colors={r"\beta^\top": SPREAD_C}),
                cmath(r"\lambda_{\text{trace}}(r)", r"=", r"-T\textstyle\sum_{i > r} \ln(1 - \hat\lambda_i)", font_size=34),
                cmath(r"n \text{ assets}", r"\Rightarrow", r"\text{many more candidate baskets than pairs}", font_size=32,
                      colors={r"n \text{ assets}": BAD})]
        whys = [why(r"for a basket of $n$ prices: the vector error-correction model, Granger's representation of "
                    r"cointegrated series"),
                why(r"the columns of $\beta$ are the cointegrating portfolios, the spreads; $\alpha$ says how fast each price "
                    r"is pulled back toward them"),
                why(r"Johansen (1991): test the rank by the small eigenvalues of a canonical-correlation problem, one "
                    r"likelihood-ratio test for all $n$ assets at once"),
                why(r"the screening problem grows: every subset of a universe is a candidate basket, and every one tested is "
                    r"a trial")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "Beyond pairs: baskets. <bookmark mark='a'/> For several prices, write the changes as an error-correction "
            "model: each price moves partly in response to how far the system is from its long-run ties. "
            "<bookmark mark='b'/> The matrix of that response factors into speeds and cointegrating portfolios; its rank "
            "is the number of independent spreads. <bookmark mark='c'/> Soren Johansen's test reads the rank from "
            "eigenvalues, one likelihood-ratio test for the whole basket. <bookmark mark='d'/> But the screening problem "
            "only grows: every subset of a universe is a candidate basket, and every basket tested is a trial."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def twins(self):
        rows = [cmath(r"\text{Royal Dutch}", r":", r"\text{Shell}\ =\ 60 : 40", font_size=36,
                      colors={r"\text{Royal Dutch}": SPREAD_C}),
                cmath(r"\text{the price ratio}", r"\neq", r"\text{parity, for years}", font_size=34,
                      colors={r"\text{parity, for years}": BAD}),
                cmath(r"\text{the tie}", r"=", r"\text{a contract, until 2005}", font_size=34)]
        whys = [why(r"two listed shares with a fixed claim on one group's cash flows: the purest pair there is"),
                why(r"Froot and Dabora (1999): the two prices deviated from parity for long periods, by more than ten "
                    r"percent at times, and each moved with its home market"),
                why(r"Long-Term Capital Management held the trade when it failed in 1998, as reported; the gap closed for "
                    r"good only when the two companies unified in 2005")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The purest pair there is. <bookmark mark='a'/> Royal Dutch and Shell were two listed shares with fixed "
            "claims, sixty to forty, on the cash flows of one group. Their prices should have been tied exactly. "
            "<bookmark mark='b'/> Kenneth Froot and Emil Dabora found they deviated from parity for long periods, by "
            "more than ten percent at times, and that each share moved with its own home market. "
            "<bookmark mark='c'/> Long-Term Capital Management held this trade when it failed in 1998, as reported. "
            "The gap closed for good only in 2005, when the companies unified. Even a contract does not make a spread "
            "revert on your schedule."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def screening(self, c):
        cards = VGroup(
            desk_question(r"many tests, few ties", r"1{,}176 industry pairs, or 125{,}000 pairs of 500 stocks, tested at "
                          r"5\%: thousands pass by chance; Part 26's multiple-testing counter applies to pairs too",
                          width=12.4, font_size=19),
            desk_question(r"economics first", r"pairs chosen for a reason (the same product, the same supply chain, two "
                          r"share classes of one company) survive the screen far better than pairs chosen by the test",
                          width=12.4, font_size=19),
            desk_question(r"or no pairs at all", r"a factor model removes what all stocks share, and leaves one residual "
                          r"per stock to revert: Avellaneda and Lee's route, Chapter 5", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The screening problem, and three answers. <bookmark mark='a'/> With a thousand pairs, or a hundred and "
            "twenty-five thousand among five hundred stocks, thousands pass any test by chance: Part twenty-six's counter "
            "applies to pairs. <bookmark mark='b'/> Pairs chosen for a reason, the same product, the same supply chain, "
            "two share classes of one company, survive far better. <bookmark mark='c'/> Or skip pairs altogether: remove "
            "what all assets share with a factor model, and let each asset's residual revert on its own."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"you test 2{,}000 unrelated pairs at the 5\% level and keep those that pass. About how many, and "
                       r"how many of those pass again next year?")
        with self.voiceover(
            "Pause and predict. You test two thousand unrelated pairs at the five percent level and keep the ones that "
            "pass. About how many is that, and how many of them pass again next year?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

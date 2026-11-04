from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, SDF, TRUE, ask, fit_right, illustration, load


class Track(VoiceoverScene):
    def construct(self):
        e = load("envelope")
        self.card()
        self.register(e)
        self.result(e)
        self.paths(e)
        self.breakeven(e)
        self.caveats()
        self.clean()
        self.next_()
        self.counter(e)

    def card(self):
        c = chapter_card(11, r"The shrinkage SDF, registered and opened", r"What did the zoo's best estimate do on unseen "
                         r"data?", lit=(2021,), part=PART)
        with self.voiceover("Chapter eleven. The shrinkage discount factor, committed to before the sealed years are "
                            "opened."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def register(self, e):
        cards = VGroup(
            desk_question(r"the strategy", r"chapter 6's SDF: 154 predictors, the shrinkage chosen by 3-fold "
                          r"cross-validation on 1973--2020, weights fixed in December 2020, scaled to 10\% volatility",
                          width=12.0, font_size=20),
            desk_question(r"its benchmark", r"all 154 predictors in equal weights: no estimation at all", width=12.0,
                          font_size=20),
            desk_question(r"the count", r"twenty values of $\kappa$ were tried for the SDF: twenty trials; one for the "
                          r"benchmark. Placeholder costs: 2\% a year for the SDF, 1\% for equal weights", width=12.0,
                          font_size=20),
            desk_question(r"the envelope", r"the release's sealed months: January 2021 to December 2023, 36 months",
                          width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.24)
        if cards.height > 6.8:
            cards.scale_to_fit_height(6.8)
        with self.voiceover(
            "What is registered. <bookmark mark='a'/> Chapter six's discount factor: a hundred and fifty-four "
            "predictors, the shrinkage chosen by cross-validation on the research window, the weights frozen in "
            "December 2020 and scaled to ten percent volatility. <bookmark mark='b'/> Beside it, a benchmark with no "
            "estimation at all: every predictor in equal weights. <bookmark mark='c'/> Twenty values of kappa were "
            "tried, so the discount factor counts as twenty trials, the benchmark as one. <bookmark mark='d'/> The "
            "data release ends in 2023, so the envelope holds thirty-six months. Everything about the strategy was "
            "fixed, hashed and recorded before the first of those months was read."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def result(self, e):
        rows = e["rows"]
        hx = [-4.4, -1.8, 0.4, 2.6, 4.8]
        heads = [r"", r"research Sharpe", r"2021--23 return", r"2021--23 Sharpe", r"net Sharpe"]
        tab = VGroup(VGroup(*[label(h_, font_size=17, color=GREY_A).move_to([x, 2.0, 0]) for h_, x in zip(heads, hx)]))
        for i, (k, nm, col) in enumerate((("kns_sdf_part25", r"shrinkage SDF", SDF),
                                          ("zoo_equal_weight_part25", r"equal weights", GOOD))):
            r_, h = rows[k]["research"], rows[k]["holdout"]
            y = 1.3 - 0.75 * i
            tab.add(VGroup(label(nm, font_size=20, color=col).move_to([hx[0], y, 0]),
                           MathTex(f"{r_['sharpe']:.2f}", font_size=26).move_to([hx[1], y, 0]),
                           MathTex(rf"{100 * h['mean']:+.1f}\%", font_size=26).move_to([hx[2], y, 0]),
                           MathTex(rf"{h['sharpe']:.2f} \pm {h['sharpe_se']:.2f}", font_size=26, color=col).move_to([hx[3], y, 0]),
                           MathTex(f"{h['sharpe_net']:.2f}", font_size=26, color=GREY_B).move_to([hx[4], y, 0])))
        foot = wrapped_label(r"paper returns of the predictors' original-paper portfolios, before realistic costs: the "
                             r"research Sharpe ratios are in sample (the shrinkage and weights were fitted on the same "
                             r"years), the hold-out's are not", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Open it. <bookmark mark='a'/> In sample, the discount factor's Sharpe ratio was about four and a half, "
            "and equal weights about two. In the sealed years, the discount factor earned thirty-five percent a year "
            "at roughly its target volatility, a Sharpe ratio of about three, and equal weights earned seven percent, "
            "a Sharpe ratio of about two. With three years of data the standard errors are about six tenths. The zoo's "
            "paper returns, combined with shrinkage, kept working after the research window closed."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab[1:]], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def paths(self, e):
        rows = e["rows"]
        g = axes([2021, 2024], [0.9, 2.9], x_length=8.0, y_length=4.4, xlabel=r"year", ylabel=r"\$1, January 2021",
                 xticks=[2021, 2022, 2023, 2024], yticks=[1.0, 1.5, 2.0, 2.5], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        lines = VGroup()
        for k, col in (("kns_sdf_part25", SDF), ("zoo_equal_weight_part25", GOOD)):
            d = np.asarray(rows[k]["holdout_dates"])
            t = d // 100 + (d % 100) / 12
            w = np.asarray(rows[k]["holdout_cum"])
            lines.add(curve(ax, np.r_[2021, t], np.r_[1, w], col, stroke_width=3))
        side = VGroup(legend([(SDF, r"shrinkage SDF"), (GOOD, r"equal weights")], font_size=17),
                      wrapped_label(r"the SDF gained in each of the three years, most in 2021 and 2022, while the market "
                                    r"fell in 2022. Its worst drawdown was about 5\%", 3.6, 16, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The paths. <bookmark mark='a'/> The discount factor rose in all three years, most in 2021 and 2022, the "
            "year the stock market fell, and its worst drawdown was about five percent. Equal weights rose steadily "
            "too, and flattened in 2023."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(side[1]), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def breakeven(self, e):
        rows = e["rows"]
        d = np.asarray(rows["kns_sdf_part25"]["holdout_cum"])
        r = np.r_[d[0] - 1, d[1:] / d[:-1] - 1]
        costs = np.linspace(0, 0.40, 41)
        sr = [(r - c / 12).mean() / (r - c / 12).std() * np.sqrt(12) for c in costs]
        be = float(r.mean() * 12)
        g = axes([0, 0.40], [-0.5, 3.5], x_length=7.2, y_length=4.2, xlabel=r"trading and funding cost, a year",
                 ylabel=r"Sharpe ratio, 2021--23", xticks=[0, 0.1, 0.2, 0.3, 0.4], yticks=[0, 1, 2, 3], font_size=13).to_edge(
            LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, costs, sr, SDF, stroke_width=3.5)
        z = DashedLine(ax.c2p(0, 0), ax.c2p(0.4, 0), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"\text{{break-even cost}} \approx {100 * be:.0f}\%\ \text{{a year}}", font_size=24, color=SDF),
            wrapped_label(r"the hold-out's Sharpe ratio as a cost per year is subtracted. A book of 154 long--short legs, "
                          r"many in small stocks and some turning over monthly, can plausibly cost tens of percent of its "
                          r"capital a year at this leverage; Part 26 estimates it properly", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "How much cost could it bear? Subtract a cost per year and recompute the hold-out's Sharpe ratio. "
            "<bookmark mark='a'/> The line falls steadily and crosses zero near thirty-five percent a year. That sounds "
            "like a lot of room. It is less than it sounds: a hundred and fifty-four long-short legs, many in small "
            "stocks, some turned over every month, levered to ten percent volatility, can plausibly cost tens of "
            "percent of capital a year. The answer depends on numbers this part has not measured."
        ) as vo:
            self.play(FadeIn(g), Create(z))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def caveats(self):
        cards = VGroup(
            desk_question(r"paper, not fund", r"many predictors are equal-weighted, rebalanced monthly, short microcaps; "
                          r"the SDF's largest loading is on short-term reversal. Realistic costs (Novy-Marx and Velikov) "
                          r"would remove a large part of this return, and Part 26 charges them", width=12.0, font_size=20),
            desk_question(r"leverage", r"10\% volatility from 154 long--short legs means gross positions many times "
                          r"capital, with the funding and margin of Parts 21 and 22", width=12.0, font_size=20),
            desk_question(r"what it does show", r"shrinkage plus diversification across the zoo survived three unseen "
                          r"years on paper; that is evidence about the estimator, not yet about a strategy", width=12.0,
                          font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Before anyone gets excited, three caveats. <bookmark mark='a'/> These are paper returns. Many of the "
            "predictors are equal-weighted, rebalanced monthly and short tiny stocks, and the discount factor's largest "
            "loading is short-term reversal. Realistic trading costs would remove a large part of this, and Part "
            "twenty-six charges them. <bookmark mark='b'/> Ten percent volatility from a hundred and fifty-four "
            "long-short legs means gross positions many times the capital, with all the funding and margin of Parts "
            "twenty-one and twenty-two. <bookmark mark='c'/> What it does show is that the estimator, shrinkage across "
            "the whole zoo, survived three unseen years. That is evidence about a method, not yet about a fund."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def clean(self):
        cards = VGroup(
            desk_question(r"why the hold-out needs no correction", r"the 2021--23 Sharpe ratio comes from one look at data "
                          r"no choice was fitted to: its $p$-value is honest as it stands", width=12.0, font_size=20),
            desk_question(r"what does need one", r"the research window's 4.6: chosen among twenty shrinkage values, on "
                          r"154 predictors that were themselves selected by their papers", width=12.0, font_size=20),
            desk_question(r"why the counter still matters", r"if the House opened the envelope for many variants and "
                          r"reported the best, the hold-out would become another research window. One look per "
                          r"registration is what keeps it clean", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "One subtle point. <bookmark mark='a'/> The hold-out's Sharpe ratio needs no multiple-testing correction: "
            "it comes from one look at data that no choice was fitted to. <bookmark mark='b'/> The research window's "
            "four and a half does need one: it was chosen among twenty shrinkage values, on predictors that their own "
            "papers had already selected. <bookmark mark='c'/> And that is why the counter matters even for the "
            "hold-out. If the House opened the envelope for many variants and reported the best, the sealed years "
            "would become just another research window. One look per registration keeps them clean."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def next_(self):
        cards = VGroup(
            desk_question(r"costs (Part 26)", r"the SDF's legs re-priced with spreads, impact, borrow fees and funding; its "
                          r"net row replaces this paper row", width=12.0, font_size=20),
            desk_question(r"machine learning (Part 27)", r"nonlinear SDFs and expected returns from the characteristics "
                          r"behind these predictors, scored on the same envelope", width=12.0, font_size=20),
            desk_question(r"a portfolio (Part 30)", r"the SDF's weights become positions only with constraints: leverage, "
                          r"turnover, capacity and a risk model", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "What happens to this row next. <bookmark mark='a'/> Part twenty-six re-prices every leg with spreads, "
            "impact, borrowing fees and funding, and a net row replaces this paper one. <bookmark mark='b'/> Part "
            "twenty-seven builds nonlinear discount factors from the characteristics behind these predictors, scored "
            "on the same envelope. <bookmark mark='c'/> And Part thirty turns weights into positions, under limits on "
            "leverage, turnover and capacity, with a proper risk model."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def counter(self, e):
        num = MathTex(r"325", font_size=96, color=QC.HOUSE)
        num2 = MathTex(rf"{e['trials']}", font_size=96, color=QC.HOUSE)
        cap = label(r"the trial counter", font_size=24, color=GREY_A).next_to(num, DOWN, buff=0.5)
        foot = wrapped_label(r"twenty for the SDF's grid, one for the benchmark. Every later part adds its own; Part 26 "
                             r"turns the count into a deflated Sharpe ratio", 11.0, 18, GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "And the counter. <bookmark mark='a'/> Twenty trials for the discount factor's grid, one for the "
            "benchmark: from three hundred and twenty-five to three hundred and forty-six. <bookmark mark='b'/> Part "
            "twenty-six turns that count into the correction every backtest needs."
        ) as vo:
            self.play(FadeIn(num), FadeIn(cap))
            vo.wait_until("a")
            self.play(TransformMatchingTex(num, num2))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()

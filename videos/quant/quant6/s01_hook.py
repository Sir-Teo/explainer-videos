from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, EST, GOOD, PART, load, predict, real_data, tbar

ORDER = ["pooled OLS", "clustered by industry", "clustered by month", "two-way clustered", "Fama-MacBeth"]
SHORT = {"pooled OLS": r"pooled OLS", "clustered by industry": r"clustered by\\industry",
         "clustered by month": r"clustered by\\month", "two-way clustered": r"two-way\\clustered",
         "Fama-MacBeth": r"Fama--\\MacBeth"}


class Hook(VoiceoverScene):
    def construct(self):
        p = load("panel")
        fe = load("panel_fe")
        self.title_card()
        self.four(p, fe)
        self.era()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"One regression, five verdicts")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part six. Financial econometrics. The mathematics of the last two parts describes how prices move. This "
            "part is about the harder problem: learning from the one history we have, without fooling ourselves."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def four(self, p, fe):
        res = p["results"]
        g = axes([0, 6], [-1, 6], x_length=6.4, y_length=4.4, ylabel=r"$t$-statistic of the momentum slope",
                 xticks=[], yticks=[0, 2, 4, 6], font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        for i, k in enumerate(ORDER):
            t = res[k]["t"]
            col = ALT if k == "Fama-MacBeth" else (GOOD if abs(t) > 1.96 else BAD)
            b = tbar(ax, i + 0.5, t, col, width=0.55)
            bars.add(b)
            labs.add(Tex(r"\begin{tabular}{c}" + SHORT[k] + r"\end{tabular}", font_size=18, color=GREY_A).next_to(
                ax.c2p(i + 0.5, -1), DOWN, buff=0.1))
            vals.add(MathTex(f"{t:.2f}", font_size=24, color=col).next_to(b, UP, buff=0.08))
        sixth = tbar(ax, 5.5, fe["t_within_cluster"], GREY_C, width=0.55).set_fill(opacity=0.35)
        six_l = Tex(r"\begin{tabular}{c}pooled,\\month effects\end{tabular}", font_size=18, color=GREY_B).next_to(
            ax.c2p(5.5, -1), DOWN, buff=0.1)
        six_v = MathTex(f"{fe['t_within_cluster']:.2f}", font_size=24, color=GREY_B).next_to(sixth, UP, buff=0.08)
        six_q = label(r"chapter 4", font_size=18, color=GREY_B).next_to(six_v, UP, buff=0.08)
        two = DashedLine(ax.c2p(0, 1.96), ax.c2p(6, 1.96), color=GREY_B, stroke_width=2)
        tl = label(r"1.96", font_size=18, color=GREY_B).next_to(ax.c2p(6, 1.96), RIGHT, buff=0.08)
        side = VGroup(
            label(r"does an industry's past year predict its next month?", font_size=22, color=GREY_A),
            label(r"49 industries, 1928--2020, 51{,}858 observations", font_size=20, color=GREY_B),
            MathTex(rf"\hat\beta = {res['pooled OLS']['beta']:.4f} \ \text{{(pooled)}}", font_size=28, color=EST),
            MathTex(rf"\hat\beta = {res['Fama-MacBeth']['beta']:.4f} \ \text{{(Fama--MacBeth)}}", font_size=28, color=ALT),
            wrapped_label(r"same data, same question: the answer depends on which variation the estimator uses and "
                          r"how it counts the noise", 4.4, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Kenneth French's 49 industry portfolios, monthly; the House's \texttt{econ}")
        q = predict(r"A sixth estimate, pooled least squares with a separate intercept for every month, waits in grey. "
                    r"Which of the five will it sit closest to?", width=11.0).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Here is a question an analyst might ask on a Monday morning. Does an industry's return over the past year "
            "predict its return next month? Kenneth French's forty-nine industries, ninety-three years, fifty-two "
            "thousand observations. Run one regression. <bookmark mark='a'/> Ordinary least squares says the slope "
            f"is positive, with a t-statistic of {res['pooled OLS']['t']:.2f}, almost significant. "
            "<bookmark mark='b'/> But industries in the same month share a market shock. Cluster by month, and the "
            f"t-statistic is {res['clustered by month']['t']:.2f}: nothing. <bookmark mark='c'/> Fama and MacBeth's "
            "method, a slope each month, averaged, gives a different slope altogether, "
            f"{res['Fama-MacBeth']['beta'] / res['pooled OLS']['beta']:.0f} times larger, with a t-statistic of "
            f"{res['Fama-MacBeth']['t']:.1f}. <bookmark mark='d'/> Same data, same question, five verdicts. And a sixth, in "
            "grey: least squares with a separate intercept for every month. <bookmark mark='e'/> Pause and predict: "
            "which will it sit closest to? Chapter four shows that none of these numbers is wrong; each answers its own "
            "question."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), FadeIn(side[1]), Create(two), FadeIn(tl), FadeIn(labs))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(vals[0]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[i], DOWN), FadeIn(vals[i])) for i in (1, 2, 3)],
                                  lag_ratio=0.4))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[4], DOWN), FadeIn(vals[4]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]), GrowFromEdge(sixth, DOWN), FadeIn(six_l), FadeIn(six_v), FadeIn(six_q))
            vo.wait_until("e")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def era(self):
        events = [
            (1933, r"Cowles", r"``Can stock market forecasters forecast?'': mostly not"),
            (1969, r"Fama, Fisher, Jensen, Roll", r"stock splits: the first event study"),
            (1973, r"Fama and MacBeth", r"a cross-section each month, then average"),
            (1982, r"Hansen", r"the generalized method of moments (Nobel 2013)"),
            (1987, r"Newey and West", r"standard errors that allow for correlation"),
            (2009, r"Petersen", r"42\% of panel papers did not adjust their errors"),
            (2016, r"Harvey, Liu and Zhu", r"316 factors: demand $t > 3$"),
            (2024, r"Menkveld et al.", r"164 teams, one data set, different answers"),
        ]
        x0, x1 = -6.2, 6.2
        X = lambda y: x0 + (x1 - x0) * (y - 1925) / (2030 - 1925)  # noqa: E731
        line = Line([x0, 0, 0], [x1, 0, 0], color=GREY_D, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(y), -0.06, 0], [X(y), 0.06, 0], color=GREY_D),
                                Text(str(y), font_size=13, color=GREY_D).next_to([X(y), 0, 0], DOWN, buff=0.12))
                         for y in range(1930, 2031, 20)])
        dots, cards = VGroup(), VGroup()
        for i, (yr, who, what) in enumerate(events):
            d = Dot([X(yr), 0, 0], radius=0.08, color=QC.IDEA)
            c = VGroup(label(str(yr), font_size=24, color=QC.IDEA), label(who, font_size=19, color=WHITE),
                       wrapped_label(what, 2.9, 17, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            up = i % 2 == 0
            c.next_to([X(yr), 0, 0], UP if up else DOWN, buff=0.55 if up else 0.75).set_x(
                min(max(X(yr), -5.2), 5.2))
            lead = Line(d.get_center(), c.get_bottom() if up else c.get_top(), color=GREY_C, stroke_width=1,
                        stroke_opacity=0.6)
            dots.add(d)
            cards.add(VGroup(lead, c))
        head = label(r"How we got here", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "How we got here. In 1933 Alfred Cowles asked whether forecasters could forecast: mostly not. "
            "<bookmark mark='a'/> In 1969 Fama, Fisher, Jensen and Roll invented the event study. <bookmark mark='b'/> In "
            "1973 Fama and MacBeth averaged monthly cross-sections. <bookmark mark='c'/> In 1982 Hansen gave GMM; in 1987 "
            "Newey and West, the standard error for correlated data. <bookmark mark='d'/> Then the reckoning: in 2009 "
            "Petersen found forty-two percent of panel papers had not adjusted their standard errors; in 2016 Harvey, "
            "Liu and Zhu counted three hundred and sixteen factors; in 2024 a hundred and sixty-four teams given the same "
            "data disagreed far more than their standard errors said."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(ticks))
            self.play(FadeIn(dots[0]), FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(dots[1]), FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(dots[2]), FadeIn(cards[2]))
            vo.wait_until("c")
            self.play(FadeIn(dots[3]), FadeIn(cards[3]))
            self.play(FadeIn(dots[4]), FadeIn(cards[4]))
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(dots[i]), FadeIn(cards[i])) for i in (5, 6, 7)],
                                  lag_ratio=0.8, run_time=vo.remaining(2.0) - 0.5))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Least squares as geometry; Newey--West, fixed-$b$ and EWC errors; clustering",
            r"Fama--MacBeth and the two-pass test; the five verdicts resolved",
            r"Predictive regressions: Stambaugh's bias, IVX, out-of-sample $R^2$",
            r"Maximum likelihood and GMM; the consumption Euler equation, estimated and rejected",
            r"Event studies (FOMC days); bootstraps for dependent data; Bayes and Gibbs",
            r"Multiple testing; causal designs and double ML; how many years a Sharpe ratio needs",
        ], color=QC.IDEA, font_size=24)
        with self.voiceover(
            "The plan. Least squares as geometry, and the three shapes of dependence that break its standard errors. "
            "Fama-MacBeth, where the verdicts are resolved. Predictive regressions, in and out of sample. Likelihood, "
            "GMM, and the Euler equation, which fails. Event studies on Federal Reserve decision days. Bootstraps, "
            "Bayes, multiple testing, causal designs and double machine learning. And how many years a Sharpe ratio "
            "needs. Everything here lives under the real-world measure, P."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data",))
        with self.voiceover(
            "In the House, this part builds the statistics module: robust standard errors, panel methods, bootstraps "
            "for dependent data, corrections for multiple testing, and double machine learning. <bookmark mark='a'/> "
            "Every number the research desk reports from Part twenty-three onward will pass through it."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

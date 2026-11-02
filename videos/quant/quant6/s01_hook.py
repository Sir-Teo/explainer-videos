from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, EST, GOOD, PART, load, real_data, tbar

ORDER = ["pooled OLS", "clustered by industry", "clustered by month", "two-way clustered", "Fama-MacBeth"]
SHORT = {"pooled OLS": r"pooled OLS", "clustered by industry": r"clustered by\\industry",
         "clustered by month": r"clustered by\\month", "two-way clustered": r"two-way\\clustered",
         "Fama-MacBeth": r"Fama--\\MacBeth"}


class Hook(VoiceoverScene):
    def construct(self):
        p = load("panel")
        self.title_card()
        self.four(p)
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

    def four(self, p):
        res = p["results"]
        g = axes([0, 5], [-1, 6], x_length=6.4, y_length=4.4, ylabel=r"$t$-statistic of the momentum slope",
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
        two = DashedLine(ax.c2p(0, 1.96), ax.c2p(5, 1.96), color=GREY_B, stroke_width=2)
        tl = label(r"1.96", font_size=18, color=GREY_B).next_to(ax.c2p(5, 1.96), RIGHT, buff=0.08)
        side = VGroup(
            label(r"does an industry's past year predict its next month?", font_size=22, color=GREY_A),
            label(r"49 industries, 1928--2020, 51{,}858 observations", font_size=20, color=GREY_B),
            MathTex(rf"\hat\beta = {res['pooled OLS']['beta']:.4f} \ \text{{(pooled)}}", font_size=28, color=EST),
            MathTex(rf"\hat\beta = {res['Fama-MacBeth']['beta']:.4f} \ \text{{(Fama--MacBeth)}}", font_size=28, color=ALT),
            wrapped_label(r"same data, same question: the answer depends on how you weight the months and how you "
                          r"count the noise", 4.4, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Kenneth French's 49 industry portfolios, monthly; the House's \texttt{econ}")
        with self.voiceover(
            "Here is a question an analyst might ask on a Monday morning. Does an industry's return over the past year "
            "predict its return next month? Kenneth French's forty-nine industries, ninety-three years, fifty-two "
            "thousand observations. Run one regression. <bookmark mark='a'/> Ordinary least squares says the slope "
            "is positive, with a t-statistic of one point eight six, almost significant. <bookmark mark='b'/> But "
            "industries in the same month share a market shock. Allow for that, cluster by month, and the "
            "t-statistic is zero point two seven: nothing. <bookmark mark='c'/> Fama and MacBeth's method, which "
            "estimates a slope each month and averages, gives a different slope altogether, eight times larger, "
            "with a t-statistic of five. <bookmark mark='d'/> Same data, same question, five verdicts. By the end "
            "of this part you will know which to believe, and why."
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
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Regression with overlapping data: Newey--West and Hansen--Hodrick errors",
            r"Predictive regressions and Stambaugh's bias",
            r"GMM: the consumption Euler equation, estimated and rejected",
            r"Event studies; panels: pooled, clustered and Fama--MacBeth",
            r"The bootstrap for dependent data; how many years a Sharpe ratio needs",
            r"Bayesian shrinkage; multiple testing; causal inference and double machine learning",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. Regression with overlapping observations, and the standard errors that survive them. "
            "Predictive regressions and Stambaugh's bias. The generalized method of moments, applied to the "
            "consumption Euler equation, which fails. Event studies, and panel methods. The bootstrap for dependent "
            "data, and how many years of data a Sharpe ratio needs. Shrinkage, multiple testing, and the tools of "
            "causal inference."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=9))
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

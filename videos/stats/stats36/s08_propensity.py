from __future__ import annotations

from videos.stats.stats36.common import *  # noqa: F403


class Propensity(VoiceoverScene):
    def construct(self):
        self.card()
        self.balancing()
        self.matching()
        self.subclass()
        self.numbers()
        self.design()

    def card(self):
        card = chapter_card(7, r"Propensity scores", r"One number that balances many", lit=(1983, 1968), part=PART)
        with self.voiceover("Chapter seven. Propensity scores."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def balancing(self):
        rows = [
            cmath(r"e(x)", r"=", r"P(T = 1 \mid X = x)", font_size=34),
            cmath(r"X \perp\!\!\!\perp T", r"\mid", r"e(X)", font_size=34),
            cmath(r"(Y(0), Y(1)) \perp\!\!\!\perp T \mid X", r"\Rightarrow", r"(Y(0), Y(1)) \perp\!\!\!\perp T \mid e(X)", font_size=28),
            cmath(r"\text{so}", r":", r"\text{compare patients with equal } e(x), \text{ whatever their } x", font_size=30),
        ]
        rows[2][-1].set_color(PSC)
        whys = [why(r"the propensity score"), why(r"a balancing score"), why(r"Rosenbaum \& Rubin (1983)"),
                why(r"one dimension instead of many")]
        with self.voiceover(
            "<bookmark mark='a'/> Rosenbaum and Rubin's 1983 idea was to model the treatment instead. The propensity score is "
            "each patient's probability of being treated given their covariates. <bookmark mark='b'/> It is a balancing "
            "score: among patients with the same propensity, the covariates have the same distribution in the two arms, "
            "whatever their values. <bookmark mark='c'/> So if treatment is unconfounded given X, it is unconfounded given "
            "the propensity score alone. <bookmark mark='d'/> Instead of matching patients on many covariates, we can "
            "compare patients with equal propensity: a one-dimensional problem."
        ) as vo:
            intro=label('The true propensity score balances measured covariates',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def matching(self):
        rows = [
            cmath(r"\text{for each treated } i", r":", r"\text{the untreated } j \text{ with the closest } \hat e", font_size=30),
            cmath(r"\widehat{\text{ATT}}", r"=", r"\tfrac{1}{n_1} \textstyle\sum_i (Y_i - Y_{j(i)})", font_size=32),
            cmath(r"\text{with replacement}", r":", r"\text{closer matches; \ dependent pair differences}", font_size=30),
            cmath(r"\text{caliper}", r":", r"\text{drop treated patients with no close match}", font_size=30),
        ]
        rows[1][-1].set_color(PSC)
        whys = [why(r"nearest-neighbour matching"), why(r"the effect on the treated"), why(r"controls can be reused"),
                why(r"enforcing overlap, \ changing the estimand")]
        with self.voiceover(
            "<bookmark mark='a'/> The simplest use is matching. For each treated patient, find the untreated patient "
            "whose estimated propensity is closest. <bookmark mark='b'/> The average difference between the pairs "
            "estimates the effect on the treated, because every pair's treated member is one of the treated. "
            "<bookmark mark='c'/> Allowing controls to be reused permits closer matches, but creates dependent pair "
            "differences. Standard errors must account for that reuse. <bookmark mark='d'/> A caliper drops treated "
            "patients with no close match, which enforces overlap but quietly changes the population the estimate is "
            "about."
        ) as vo:
            intro=label('Matching design and reuse determine the target and uncertainty',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def subclass(self):
        rows = fit_rows(VGroup(
            label(r"William Cochran (1968): \ cut the score into five strata", font_size=26),
            label(r"compare treated and untreated within each, \ then average", font_size=26),
            label(r"his finding: \ five strata remove about 90\% of the bias from a covariate", font_size=26, color=BANDC),
            label(r"the rest remains: \ within a stratum, \ patients still differ", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> An older idea, from William Cochran in 1968, cuts the score into five strata. <bookmark "
            "mark='b'/> Compare treated and untreated within each stratum, then average the five differences. <bookmark "
            "mark='c'/> Cochran showed that five strata remove about ninety percent of the bias due to a covariate, under "
            "conditions he worked out. <bookmark mark='d'/> The other ten percent remains, because within a broad stratum the "
            "treated still have somewhat higher scores than the untreated."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def numbers(self):
        d = load("obs")
        bias_naive = d["naive"]["est"] - d["ate"]
        bias_sub = d["subclass"] - d["ate"]
        rows = [[r"method", r"estimate", r"truth"],
                [r"naive", rf"{d['naive']['est']:.2f}", rf"ATE {d['ate']:.2f}"],
                [r"matching, \ ATT", rf"{d['match_att']:.2f}", rf"ATT {d['att']:.2f}"],
                [r"five strata, \ ATE", rf"{d['subclass']:.2f}", rf"ATE {d['ate']:.2f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.0, row_buff=0.35, colors=[GREY_A, MISSC, BANDC, TAUC]).move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(rf"five strata remove {100 * (1 - bias_sub / bias_naive):.0f}\% of the naive bias here", font_size=24, color=TAUC),
            label(r"the logistic propensity model uses the four covariates, \ linearly", font_size=24, color=GREY_A),
        ), 12.4, 0.35, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the World's observational study. <bookmark mark='b'/> The naive comparison, minus "
            + say(-d["naive"]["est"], 1) + ". <bookmark mark='c'/> Matching each treated patient to its nearest untreated "
            "neighbour on the propensity score: minus " + say(-d["match_att"], 1) + ", close to the true effect on the treated, "
            "minus " + say(-d["att"], 1) + ". <bookmark mark='d'/> Five strata: minus " + say(-d["subclass"], 1) + ", which removes "
            + f"{100 * (1 - bias_sub / bias_naive):.0f}" + " percent of the naive bias, much as Cochran predicted, but not all of "
            "it."
        ) as vo:
            self.add(obs_tag())
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
            self.play(FadeIn(foot))
        self.clear_scene()

    def design(self):
        rows = fit_rows(VGroup(
            label(r"the score is estimated \emph{without looking at outcomes}", font_size=26, color=BANDC),
            label(r"so the analyst can redesign until balance is good, \ like rerandomization, \ without fishing", font_size=26),
            label(r"Rubin (2008): \ `for objective causal inference, \ design trumps analysis'", font_size=26, color=TAUC),
            label(r"next: \ use the score as a weight", font_size=26, color=PSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A real virtue of propensity methods is that the score is built without looking at "
            "the outcomes. <bookmark mark='b'/> The analyst can refine the score, the matches and the strata until "
            "the covariates balance, as with rerandomization, which reduces direct outcome-driven selection. The "
            "analyst must still document the design choices and account for the final design. <bookmark mark='c'/> "
            "Rubin put it in a title in 2008: for objective causal inference, design trumps analysis. <bookmark "
            "mark='d'/> Next, using the score as a weight."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

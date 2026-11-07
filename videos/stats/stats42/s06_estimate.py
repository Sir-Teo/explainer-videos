from __future__ import annotations

import numpy as np

from videos.stats.stats42.common import *  # noqa: F403


class SurveyEstimate(VoiceoverScene):
    def construct(self):
        self.card()
        self.holes()
        self.cc()
        self.impute()
        self.overlap()
        self.balance()
        self.aipw()
        self.board()

    def card(self):
        card = chapter_card(5, r"Case 2: \ imputation and AIPW", r"Income is missing for more than a third", part=PART)
        with self.voiceover("Chapter five. The estimate: imputation for the holes, then a doubly robust estimator."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def holes(self):
        o = load("obs")
        W = World()
        M = W.ministry
        n = 28
        grid = MaskGrid(n, [r"age", r"sex", r"BMI", r"told", r"uses", r"SBP", r"income"], cell_w=0.82, cell_h=0.19,
                        center=[-3.0, -0.3, 0], font_size=18)
        miss = np.asarray(M["income_miss"])[:n]
        side = fit_rows(VGroup(
            label(rf"income withheld: \ {100 * o['income_miss']:.0f}\%", font_size=24),
            label(rf"under 40: \ {100 * o['miss_by']['young']:.0f}\%; \ 60 and over: \ {100 * o['miss_by']['old']:.0f}\%", font_size=24, color=GREY_A),
            label(rf"users: \ {100 * o['miss_by']['users']:.0f}\%; \ non-users: \ {100 * o['miss_by']['non']:.0f}\%", font_size=24, color=USERC),
            label(r"and less often by those with high pressure", font_size=24, color=CASE2),
            label(r"all of it explained by what is seen: \ assume MAR", font_size=24, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Income, one of the four confounders, was withheld by {100 * o['income_miss']:.0f} "
            f"percent of the people surveyed. Here are the first twenty-eight rows. <bookmark mark='b'/> The young withhold "
            f"it far more often: {100 * o['miss_by']['young']:.0f} percent of those under forty, "
            f"{100 * o['miss_by']['old']:.0f} percent of those over sixty. <bookmark mark='c'/> Users, perhaps more engaged "
            f"with the survey's subject, withhold it half as often as non-users. <bookmark mark='d'/> And those with higher "
            f"pressure answer more often too. <bookmark mark='e'/> Every one of these drivers is in the data. If, given them, "
            f"withholding has nothing more to do with income itself, the holes are missing at random, Part forty-one's "
            f"assumption, and they can be filled honestly."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(survey_tag()))
            vo.wait_until("a")
            self.play(*grid.mark(6, miss), FadeIn(side[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k + 1]))
        self.clear_scene()

    def cc(self):
        o = load("obs")
        r = o["res"]["cc_aipw"]
        rows = fit_rows(VGroup(
            label(r"complete cases: \ drop the 37\%", font_size=28, color=NAIVEC),
            label(r"but who is dropped depends on the \emph{outcome}: \ high pressure answers more", font_size=26, color=GREY_A),
            label(r"selection on $Y$ given $T$ and $X$: \ complete-case estimates are biased", font_size=26, color=GREY_A),
            label(rf"in this survey: \ ${r[0]:.2f}$ \ [{r[2]:.2f}, \ {r[3]:.2f}]; \ over repeated surveys, \ see the Board", font_size=26, color=NAIVEC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The easy fix is to drop everyone with a hole. <bookmark mark='b'/> But here whether income "
            f"is seen depends on pressure, the outcome, <bookmark mark='c'/> and Part forty-one showed what that does: a "
            f"complete-case analysis selects on the outcome, and its estimates are biased. <bookmark mark='d'/> In this one "
            f"survey, the complete-case estimate happens to be {say(r[0], 2)}; whether that is luck or method, one survey "
            f"cannot say. The Board will."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def impute(self):
        o = load("obs")
        rows = [
            cmath(r"\log \text{income}", r"\sim", r"\text{age}, \text{sex}, \text{BMI}, \text{told}, T, Y, T \times Y", font_size=32),
            cmath(r"\text{draw}", r":", r"\beta^*, \sigma^* \text{ from their posterior, then each hole}", font_size=30),
            cmath(r"m", r"=", r"40 \text{ completed data sets: \ an AIPW estimate and SE in each}", font_size=30),
            cmath(r"\text{Rubin}", r":", rf"T = W + (1 + 1/m) B; \ \ \text{{fraction of missing information}} = {o['res']['fmi']:.2f}", font_size=30),
        ]
        rows[0][-1].set_color(S.ACCENT)
        whys = [why(r"include the outcome and treatment"), why(r"proper imputation"), why(r"analyse each"), why(r"combine")]
        with self.voiceover(
            f"<bookmark mark='a'/> So impute. The imputation model predicts log income from everything else, including the treatment and the outcome, and their product, to retain associations relevant to the analysis. This product does not by itself establish congeniality with AIPW; the normal imputation model remains a working assumption. Leaving the outcome out would pull every imputed income's association with pressure towards zero. <bookmark mark='b'/> Each imputation is proper: draw the regression's parameters from their posterior, then each missing value. <bookmark mark='c'/> Forty completed data sets, each analysed by the estimator we are about to build. <bookmark mark='d'/> Rubin's rules combine them. The fraction of missing information is {say(o['res']['fmi'], 2)}: although more than a third of incomes are missing, they cost only about an eighth of the information about the effect, because income is only one confounder and the others predict it."
        ) as vo:
            heading = label('Working-model imputation does not guarantee congeniality with AIPW', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def overlap(self):
        o = load("obs")
        ps, t = np.asarray(o["ps"]), np.asarray(o["t"], bool)
        A = axes([0, 1], [-6, 6], x_length=7.4, y_length=4.4, xlabel=r"propensity to use the substitute, \ $\hat e(x)$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[], center=[-2.5, 0.2, 0])
        ax = A.ax
        bins = np.linspace(0, 1, 26)
        hu, _ = np.histogram(ps[t], bins=bins, density=True)
        hn, _ = np.histogram(ps[~t], bins=bins, density=True)
        c = (bins[:-1] + bins[1:]) / 2
        w = bins[1] - bins[0]
        up = VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0], height=max(1e-3, ax.c2p(0, h)[1] - ax.c2p(0, 0)[1]),
                                stroke_width=0, fill_color=USERC, fill_opacity=0.8).move_to(ax.c2p(x, 0), aligned_edge=DOWN) for x, h in zip(c, hu)])
        dn = VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0], height=max(1e-3, ax.c2p(0, 0)[1] - ax.c2p(0, -h)[1]),
                                stroke_width=0, fill_color=GREY_B, fill_opacity=0.7).move_to(ax.c2p(x, 0), aligned_edge=UP) for x, h in zip(c, hn)])
        axis0 = Line(ax.c2p(0, 0), ax.c2p(1, 0), color=GREY_C, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"a logistic propensity model in $\{A, B, I, D\}$", font_size=24, color=PSC),
            label(r"users, \ up", font_size=24, color=USERC),
            label(r"non-users, \ down", font_size=24, color=GREY_A),
            label(rf"range {ps.min():.2f} to {ps.max():.2f}: \ observed overlap; a diagnostic", font_size=24, color=GOODC),
            label(r"fitted propensities clipped to $[0.01,0.99]$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> In each completed data set, fit a logistic model for switching given the four confounders. Here are the fitted propensities from one of them: <bookmark mark='b'/> users above the line, <bookmark mark='c'/> non-users below. <bookmark mark='d'/> Users sit further right, as they should, but the two distributions show observed overlap across much of the range, from {say(ps.min(), 2)} to {say(ps.max(), 2)}. <bookmark mark='e'/> These fitted probabilities diagnose practical overlap in this completed sample; they do not prove population positivity. We clip fitted propensities to point zero one and point nine nine, which bounds weights but can add bias."
        ) as vo:
            self.play(FadeIn(A), FadeIn(axis0))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(up), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(dn), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def balance(self):
        o = load("obs")
        names = o["names"]
        A = axes([-0.1, 0.9], [0, 5.5], x_length=7.4, y_length=4.4, xlabel=r"absolute standardized mean difference",
                 xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[], center=[-2.0, 0.2, 0])
        ax = A.ax
        band_ = Rectangle(width=ax.c2p(0.1, 0)[0] - ax.c2p(-0.1, 0)[0], height=ax.c2p(0, 5.5)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                          fill_color=GOODC, fill_opacity=0.15).move_to(ax.c2p(0, 2.75))
        raw = VGroup(*[Dot(ax.c2p(abs(v), 5 - i), radius=0.09, color=NAIVEC) for i, v in enumerate(o["smd_raw"])])
        wtd = VGroup(*[Dot(ax.c2p(abs(v), 5 - i), radius=0.09, color=GOODC) for i, v in enumerate(o["smd_w"])])
        arrows = VGroup(*[Arrow(ax.c2p(abs(a), 5 - i), ax.c2p(abs(b), 5 - i), buff=0.1, color=GREY_B, stroke_width=2,
                                max_tip_length_to_length_ratio=0.12) for i, (a, b) in enumerate(zip(o["smd_raw"], o["smd_w"]))])
        names_g = VGroup(*[label(nm, font_size=22, color=GREY_A).next_to(ax.c2p(-0.1, 5 - i), LEFT, buff=0.15) for i, nm in enumerate(names)])
        side = fit_rows(VGroup(
            label(r"raw: \ users differ", font_size=24, color=NAIVEC),
            label(r"weighted by $1/\hat e$ and $1/(1 - \hat e)$", font_size=24, color=GOODC),
            label(rf"largest after weighting: \ {max(abs(v) for v in o['smd_w']):.2f}", font_size=24, color=GOODC),
            label(r"mean balance does not establish exchangeability", font_size=24, color=GREY_A),
        ), 3.6, 0.42, [5.0, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The check of Part thirty-six: standardized differences before weighting, in red. Age differs by {say(o['smd_raw'][0], 2)} standard deviations, diagnosis by {say(o['smd_raw'][4], 2)}. <bookmark mark='b'/> Weight each user by one over their propensity and each non-user by one over its complement, and recompute. <bookmark mark='c'/> Every difference falls inside the shaded band; the largest is {say(max((abs(v) for v in o['smd_w'])), 2)}. <bookmark mark='d'/> The weighted users and non-users look alike on the displayed covariate means. This does not establish balance of every distribution or remove hidden confounding."
        ) as vo:
            self.play(FadeIn(A), FadeIn(band_), FadeIn(names_g))
            vo.wait_until("a")
            self.play(FadeIn(raw), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[GrowArrow(a) for a in arrows], FadeIn(wtd), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def aipw(self):
        o = load("obs")
        r = o["res"]["mi_aipw"]
        rows = [
            cmath(r"\hat\psi_i", r"=", r"\hat\mu_1(x_i) - \hat\mu_0(x_i) + \frac{t_i (y_i - \hat\mu_1(x_i))}{\hat e(x_i)} - \frac{(1 - t_i)(y_i - \hat\mu_0(x_i))}{1 - \hat e(x_i)}", font_size=28),
            cmath(r"\hat\tau", r"=", r"\bar{\hat\psi}, \ \ \text{SE} = \text{sd}(\hat\psi) / \sqrt n", font_size=32),
            cmath(r"\text{consistent if}", r":", r"\text{either the outcome models or the propensity model is right}", font_size=30),
            cmath(r"\text{pooled}", r":", rf"\hat\tau = {r[0]:.2f}, \ \text{{SE}} = {r[1]:.2f}, \ \ 90\% \text{{ CI }} [{r[2]:.2f}, \ {r[3]:.2f}]", font_size=32),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Part 36"), why(r"influence-function SE"), why(r"double robustness"), why(r"40 imputations, \ Rubin's rules")]
        with self.voiceover(
            f"<bookmark mark='a'/> The estimator is the augmented inverse probability weighted estimator of Part thirty-six. For each person, the outcome models' predicted difference, corrected by each arm's weighted residual. <bookmark mark='b'/> The estimate is the average, and its standard error comes from the spread of the individual terms, the influence function. <bookmark mark='c'/> It is consistent if either the outcome regressions or the propensity model is right, under the causal identification and overlap assumptions. Before missingness, the uptake law is logistic in these covariates; estimated and clipped propensities after working-model imputation need not equal that true law. Consistency does not alone guarantee this influence-function standard error under arbitrary misspecification. <bookmark mark='d'/> Pooled over the forty imputations: {say(r[0], 2)} millimetres, standard error {say(r[1], 2)}, ninety percent interval from {say(r[2], 2)} to {say(r[3], 2)}. Under the stated causal and missing-data assumptions, the estimated reduction is about two millimetres. Rubin pooling here is a working inference procedure whose calibration is examined on the Board, not an automatic doubly robust missing-data guarantee."
        ) as vo:
            heading = label('Causal, overlap and nuisance conditions support AIPW inference', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = board_rows("naive difference", "collider", "AIPW")
        show_board(self, rows,
                   "<bookmark mark='a'/> The Board, over four hundred surveys drawn from the World's adults. The naive "
                   "difference never covers the true effect of minus three. Adjusting for the collider covers it seven and a half percent "
                   "of the time. <bookmark mark='b'/> AIPW on complete cases covers eighty-one percent: broken, as selection on "
                   "the outcome predicts. <bookmark mark='c'/> AIPW with multiple imputation covers eighty-eight: within "
                   "simulation error of ninety, kept.",
                   [("a", [0, 1]), ("b", [2]), ("c", [3])])

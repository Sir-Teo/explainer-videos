from __future__ import annotations

import numpy as np

from videos.stats.stats36.common import *  # noqa: F403
from videos.stats.stats36.compute import obs_sample, rng, ols_fit, ols_pred


class GComp(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.picture()
        self.numbers()
        self.extrapolate()

    def card(self):
        card = chapter_card(6, r"g-computation", r"Model the outcome, \ then intervene in the model", lit=(1986,), part=PART)
        with self.voiceover("Chapter six. g-computation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\hat\mu_t(x)", r"\approx", r"E[Y \mid T = t, X = x], \ \ t = 0, 1", font_size=32),
            cmath(r"\text{predict}", r":", r"\text{every patient's outcome under both treatments}", font_size=30),
            cmath(r"\hat\tau_{g}", r"=", r"\tfrac1n \textstyle\sum_i \big(\hat\mu_1(x_i) - \hat\mu_0(x_i)\big)", font_size=32),
            cmath(r"\text{valid if}", r":", r"\text{unconfounded, \ overlap, \ and the models are right}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"an outcome model in each arm"), why(r"impute the missing half of the science"),
                why(r"Robins (1986): \ the g-formula"), why(r"the third is the catch")]
        with self.voiceover(
            "<bookmark mark='a'/> The most direct way to compute the adjustment formula is to model the outcome. Fit "
            "a regression of the outcome on the covariates, separately among the treated and the untreated. <bookmark"
            " mark='b'/> Use the two models to predict every patient's outcome under both treatments: conditional "
            "mean outcomes, rather than each individual's missing potential outcome. <bookmark mark='c'/> Average the"
            " predicted differences. James Robins introduced this in 1986, for treatments that change over time, as "
            "the g-formula, g for generalized; with one time point it is also called standardization, or the "
            "T-learner. <bookmark mark='d'/> It is valid if the identifying assumptions hold and the outcome models "
            "are right. The last condition is the catch."
        ) as vo:
            intro=label('Standardization averages fitted conditional means over the target sample',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        s = obs_sample(rng(363), 3000)
        base, t, y = s["X"][:, 0], s["t"], s["y"]
        A = axes([138, 190], [100, 200], x_length=7.4, y_length=4.4, xlabel=r"baseline pressure", ylabel=r"pressure at 12 weeks",
                 xticks=[140, 160, 180], yticks=[100, 150, 200], center=[-2.0, 0.2, 0])
        ax = A.ax
        g = np.random.default_rng(2)
        show = g.choice(len(y), 700, replace=False)
        k = show[(base[show] < 190) & (y[show] > 100) & (y[show] < 200)]
        dots = VGroup(*[Dot(ax.c2p(base[i], y[i]), radius=0.025, color=Y1C if t[i] else Y0C, fill_opacity=0.6) for i in k])
        grid = np.tile(s["X"].mean(0), (100, 1))
        grid[:, 0] = np.linspace(140, 188, 100)
        pred1 = ols_pred(ols_fit(s["X"][t], y[t]), grid)
        pred0 = ols_pred(ols_fit(s["X"][~t], y[~t]), grid)
        l1 = curve(ax, grid[:, 0], pred1, Y1C, 4)
        l0 = curve(ax, grid[:, 0], pred0, Y0C, 4)
        side = fit_rows(VGroup(
            label(r"red: \ treated; \ blue: \ untreated", font_size=22),
            label(r"all four covariates; \ other covariates standardized", font_size=22, color=TAUC),
            label(r"the gap between the lines: \ the effect at each baseline", font_size=22, color=TAUC),
            label(r"the untreated thin out at high pressure, \ the treated at low", font_size=22, color=MISSC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In one dimension it is a picture. Twelve-week pressure against baseline pressure, "
            "treated in red and untreated in blue. <bookmark mark='b'/> Fit a line to each arm. <bookmark mark='c'/> "
            "We fit both arms using all four recorded covariates, and standardize the other three over the same "
            "patients. The gap is the model's standardized effect at each baseline; averaging over baseline gives its"
            " g-computation estimate. <bookmark mark='d'/> Notice where the data are: few untreated patients at high "
            "pressure, few treated at low. There, each line is an extrapolation."
        ) as vo:
            self.add(obs_tag())
            self.play(FadeIn(A), FadeIn(dots), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(l1), Create(l0), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def numbers(self):
        d = load("obs")
        rows = fit_rows(VGroup(
            label(r"four covariates, \ a linear model in each arm", font_size=26),
            label(rf"g-computation: \ ${d['gcomp']:.2f}$", font_size=26, color=BANDC),
            label(rf"the truth: \ ${d['ate']:.2f}$; \ the naive comparison: \ ${d['naive']['est']:.2f}$", font_size=26, color=TRUEC),
            label(r"here the World's outcomes really are nearly linear in the covariates", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> With all four covariates and a linear model in each arm, <bookmark mark='b'/> g-computation "
            "estimates minus " + say(-d["gcomp"], 1) + ", <bookmark mark='c'/> against the true minus " + say(-d["ate"], 1) + "; "
            "the naive comparison said minus " + say(-d["naive"]["est"], 1) + ". <bookmark mark='d'/> It works here because the "
            "World's outcomes really are close to linear in the covariates. When the outcome model is wrong, so is the "
            "answer, and nothing in the procedure warns us."
        ) as vo:
            self.add(obs_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def extrapolate(self):
        rows = fit_rows(VGroup(
            label(r"g-computation leans on the outcome model exactly where overlap is poor", font_size=26),
            label(r"flexible models (forests, \ boosting) reduce the risk of the wrong shape \ldots", font_size=26, color=BANDC),
            label(r"\ldots but bring their own bias, \ and no simple standard error", font_size=26, color=MISSC),
            label(r"the alternative: \ model the treatment instead of the outcome", font_size=26, color=PSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The weakness is that the outcome model is trusted most exactly where there are fewest data "
            "of the other arm to check it. <bookmark mark='b'/> Flexible models such as forests reduce the risk of the wrong "
            "functional form, <bookmark mark='c'/> but they bring regularization bias and no simple standard error, a "
            "problem chapter ten will solve. <bookmark mark='d'/> The alternative strategy models how the treatment was "
            "chosen, not how the outcome is produced."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

from __future__ import annotations

import numpy as np

from videos.stats.stats39.common import *  # noqa: F403


class Confounding(VoiceoverScene):
    def construct(self):
        self.card()
        self.setting()
        self.chart()
        self.why_not()
        self.rsr()
        self.lessons()

    def card(self):
        card = chapter_card(11, r"Spatial confounding", r"Does a spatial random effect adjust for what we did not measure?", lit=(2010,), part=PART)
        with self.voiceover("Chapter eleven. Spatial confounding."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setting(self):
        rows = [
            cmath(r"y(s)", r"=", r"\beta\, x(s) + U(s) + \varepsilon(s)", font_size=32),
            cmath(r"U(s)", r":", r"\text{an unmeasured spatial variable \ (income, \ smoking, \ soil)}", font_size=30),
            cmath(r"\text{hope}", r":", r"\text{model } U \text{ as a GP random effect, \ and } \hat\beta \text{ is adjusted}", font_size=30),
            cmath(r"\text{test}", r":", r"x \text{ and } U \text{ smooth, \ same range, \ correlation } 0.8; \ \beta = 1", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"an exposure--outcome regression"), why(r"Parts 36--37's confounder"), why(r"common in epidemiology"),
                why(r"60 seeded fields, \ $n = 250$")]
        with self.voiceover(
            "<bookmark mark='a'/> A common situation in environmental epidemiology: regress a health outcome on an "
            "exposure, such as pollution, across places. <bookmark mark='b'/> There is almost always an unmeasured spatial "
            "variable, income or smoking, that varies smoothly over the map and affects both. <bookmark mark='c'/> A "
            "widespread hope is that adding a spatial random effect to the regression will soak up the unmeasured "
            "confounder and adjust the exposure's coefficient. <bookmark mark='d'/> A test: sixty seeded fields, where "
            "the exposure and the confounder are smooth fields of the same range with correlation point eight, and the "
            "true coefficient is one."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("confound")
        items = [("confounded", "ols", r"OLS, \ confounded", MISSC), ("confounded", "spatial", r"spatial GLS, \ confounded", AREAC),
                 ("independent", "ols", r"OLS, \ $U$ independent of $x$", GREY_B), ("independent", "spatial", r"spatial GLS, \ $U$ independent", BANDC)]
        A = axes([0, 2.5], [0, 4], x_length=7.4, y_length=4.4, xlabel=r"$\hat\beta$ \ (mean $\pm$ 1 SD over 60 fields)", ylabel=r"",
                 xticks=[0, 0.5, 1, 1.5, 2, 2.5], yticks=[], xfmt=lambda v: f"{v:g}", center=[0.6, 0.0, 0])
        ax = A.ax
        truth = DashedLine(ax.c2p(1, 0), ax.c2p(1, 4), color=TRUEC, stroke_width=2.5)
        marks = []
        for k, (case, est, name, col) in enumerate(items):
            yv = 3.5 - k
            m, s = d[case][est]["mean"], d[case][est]["sd"]
            g = VGroup(Line(ax.c2p(max(m - s, 0), yv), ax.c2p(m + s, yv), color=col, stroke_width=5),
                       Dot(ax.c2p(m, yv), radius=0.1, color=col),
                       label(name, font_size=22, color=col).next_to(ax.c2p(0, yv), LEFT, buff=0.2))
            marks.append(g)
        c, i = d["confounded"], d["independent"]
        with self.voiceover(
            "<bookmark mark='a'/> The gold dashed line is the truth. <bookmark mark='b'/> Ordinary least squares, which "
            "ignores the confounder, averages " + say(c["ols"]["mean"], 2) + ": the true one plus the point eight that the "
            "confounder contributes. <bookmark mark='c'/> The spatial model, generalized least squares with a Matérn "
            "random effect fitted by REML, averages " + say(c["spatial"]["mean"], 2) + ". It is just as biased, and more "
            "precise about its wrong answer. <bookmark mark='d'/> When the spatial variable is independent of the "
            "exposure, both are unbiased, <bookmark mark='e'/> and the spatial model is far more precise, with a standard "
            "deviation of " + say(i["spatial"]["sd"], 2) + " against " + say(i["ols"]["sd"], 2) + ". The random effect "
            "buys efficiency, not adjustment."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(truth))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(marks[k]))
        self.clear_scene()

    def why_not(self):
        rows = [
            cmath(r"\text{GLS}", r":", r"\hat\beta \text{ uses the variation in } x \text{ that } \Sigma \text{ calls cheap}", font_size=30),
            cmath(r"x \text{ smooth}", r":", r"\text{its variation is in the same directions as } U\text{'s}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{the two compete: \ nothing says which is which}", font_size=30),
            cmath(r"\text{Paciorek (2010)}", r":", r"\text{bias falls only if } x \text{ varies at finer scales than } U", font_size=30),
        ]
        rows[3][-1].set_color(BANDC)
        whys = [why(r"a weighted regression"), why(r"Hodges \& Reich (2010)"), why(r"collinearity in disguise"),
                why(r"scale is the lever")]
        with self.voiceover(
            "<bookmark mark='a'/> Why not? Generalized least squares estimates beta from whatever variation in the "
            "exposure the covariance treats as informative. <bookmark mark='b'/> When the exposure is a smooth field, its "
            "variation lies in the same large-scale patterns as the confounder's, as James Hodges and Brian Reich showed in "
            "2010. <bookmark mark='c'/> The random effect and the exposure then compete for the same patterns, and nothing "
            "in the data says which deserves the credit: collinearity in disguise. <bookmark mark='d'/> Christopher "
            "Paciorek showed the same year that the spatial model reduces the bias only when the exposure varies at finer "
            "scales than the confounder, so that local contrasts are unconfounded."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rsr(self):
        rows = fit_rows(VGroup(
            label(r"restricted spatial regression: \ force the random effect orthogonal to $x$", font_size=26, color=TAUC),
            label(r"it returns OLS's point estimate, \ with intervals too narrow", font_size=26, color=MISSC),
            label(r"Hanks et al.\ (2015), \ Khan \& Calder (2022): \ do not use it to protect $\hat\beta$", font_size=26, color=GREY_A),
            label(r"newer proposals \ (spatial+, \ Dupont et al.\ 2022): \ remove $x$'s smooth part first", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A once-popular fix, restricted spatial regression, makes the random effect orthogonal to "
            "the exposure, so the two no longer compete. <bookmark mark='b'/> But that simply hands every shared pattern "
            "to the exposure: it returns the ordinary least squares estimate, confounding and all, with intervals that are "
            "too narrow. <bookmark mark='c'/> Later work, by Ephraim Hanks and colleagues and by Kori Khan and Catherine "
            "Calder, recommends against it. <bookmark mark='d'/> Newer methods, such as Emiko Dupont's spatial plus, first "
            "remove the smooth part of the exposure, so that only its fine-scale variation is used, which is Paciorek's "
            "condition, made into a method."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"a spatial random effect fixes the standard errors, \ not the confounding", font_size=28, color=BANDC),
            label(r"adjustment needs the confounder, \ or a design: \ Parts 35--37", font_size=28, color=TAUC),
            label(r"the Board, \ chapter 14: \ OLS intervals under spatial errors, \ and GLS's", font_size=28, color=GREY_A),
        ), 12.4, 0.7, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lesson. A spatial random effect corrects the standard errors for dependence, which "
            "matters a great deal, as chapter fourteen's Board will show. It does not remove confounding. <bookmark "
            "mark='b'/> That still requires measuring the confounder, or a design that makes it irrelevant, the tools of "
            "Parts thirty-five to thirty-seven. <bookmark mark='c'/> Spatial structure in the residuals is a warning, not "
            "a remedy."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

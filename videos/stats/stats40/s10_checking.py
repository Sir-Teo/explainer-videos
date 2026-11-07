from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403


class Checking(VoiceoverScene):
    def construct(self):
        self.card()
        self.residuals()
        self.veteran()
        self.zph_table()
        self.remedies()
        self.split()

    def card(self):
        card = chapter_card(9, r"Checking Cox", r"Are the hazards really proportional?", lit=(1982, 1994), part=PART)
        with self.voiceover("Chapter nine. Checking Cox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def residuals(self):
        rows = [
            cmath(r"r_i", r"=", r"x_i - \bar x(t_i; \hat\beta)", font_size=32),
            cmath(r"r_i^*", r"=", r"\hat\beta + D\, \hat V r_i", font_size=32),
            cmath(r"E\, r_{ij}^*", r"\approx", r"\beta_j(t_i)", font_size=32),
            cmath(r"\text{test}", r":", r"\text{regress } r^*_j \text{ on } g(t): \ \text{a slope means } \beta_j \text{ changes}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"Schoenfeld (1982): \ one per event"), why(r"scaled using the coefficient covariance"), why(r"Grambsch \& Therneau (1994)"),
                why(r"$g$: \ time, \ log time, \ or KM")]
        with self.voiceover(
            "<bookmark mark='a'/> David Schoenfeld's residuals of 1982: at each event, the failing person's covariate "
            "minus the risk-set average, the terms of the score. <bookmark mark='b'/> Scaled using the estimated coefficient covariance "
            "and added to beta hat, <bookmark mark='c'/> they estimate the coefficient at that event's time, as Patricia "
            "Grambsch and Terry Therneau showed in 1994. <bookmark mark='d'/> If the hazards are proportional, they "
            "scatter around a horizontal line; a trend against time means the effect changes, and a regression on a "
            "function of time gives a test."
        ) as vo:
            heading = label('Scaled residuals diagnose time variation in coefficients', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def veteran(self):
        d = load("veteran")
        zt, zs = np.asarray(d["zt"], float), np.asarray(d["zs"], float)
        A = axes([0, 3], [-2.5, 1.5], x_length=7.4, y_length=4.2, xlabel=r"days \ (log scale)", ylabel=r"$\beta(t)$ for 10 Karnofsky points",
                 xticks=[0, 1, 2, 3], yticks=[-2, -1, 0, 1], xfmt=lambda v: f"{10 ** v:.0f}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        lt = np.log10(np.maximum(zt, 1))
        keep = (zs > -2.5) & (zs < 1.5)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=GREY_B, fill_opacity=0.6) for a, b in zip(lt[keep], zs[keep])])
        bt, bs = np.log10(np.asarray(d["bin_t"], float)), np.asarray(d["bin_s"], float)
        smooth = polyline(ax, bt, bs, HAZC, 4)
        flat = DashedLine(ax.c2p(0, d["beta"][0]), ax.c2p(3, d["beta"][0]), color=SURVC, stroke_width=2)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(3, 0), color=GREY_D, stroke_width=1.5)
        side = fit_rows(VGroup(
            label(r"VA lung cancer trial: \ 137 men, \ 128 deaths", font_size=22),
            label(rf"Cox: \ HR {d['hr_karno10']:.2f} per 10 Karnofsky points \ (blue line)", font_size=22, color=SURVC),
            label(r"orange: means within event-time bins", font_size=22, color=HAZC),
            label(rf"strong early, \ gone later: \ approximate diagnostic $p = {d['zph_p'][0]:.3f}$", font_size=22, color=MISSC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The Veterans' Administration lung cancer trial: a hundred and thirty-seven men with "
            "advanced disease, almost all of whom died. <bookmark mark='b'/> The Karnofsky score measures how well a "
            "patient can function, and Cox's model gives a hazard ratio of " + say(d["hr_karno10"], 2) + " per ten points: fitter patients die more slowly. <bookmark mark='c'/> But the scaled residuals tell a "
            "different story over time. <bookmark mark='d'/> The effect is strong in the first months and fades "
            "towards nothing later; our approximate KM-transformed scaled-residual diagnostic gives a p-value of " + say(d["zph_p"][0], 3) + ". This diagnostic uses a simplified constant covariance and Breslow risk-set residuals, so it is not an "
            "exact reproduction of software’s tie-adjusted Grambsch-Therneau test. The single hazard ratio averages a"
            " large early effect and none at all."
        ) as vo:
            self.add(veteran_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(zero), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(flat), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(dots), Create(smooth), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def zph_table(self):
        d = load("pbc")
        rows = [[r"Mayo model: approximate KM-transform residual diagnostic", r"$\chi^2_1$", r"$p$"]]
        for n, c, p in zip(d["names"], d["zph_chi2"], d["zph_p"]):
            rows.append([n, f"{c:.2f}", f"{p:.3f}"])
        cols = [GREY_A] + [MISSC if p < 0.1 else None for p in d["zph_p"]]
        tab = table_rows(rows, font_size=26, col_buff=1.0, row_buff=0.3, colors=cols).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"no strong violation; \ bilirubin and prothrombin time are borderline", font_size=24, color=GREY_A),
            label(r"power depends on events and departure; clinical size still matters", font_size=24, color=TAUC),
        ), 12.4, 0.3, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The same tests for the Mayo model. <bookmark mark='b'/> These approximate "
            "diagnostics do not provide strong evidence against the assumption; bilirubin and prothrombin time are "
            "borderline, with p-values near point one. <bookmark mark='c'/> Like every goodness-of-fit test, its "
            "power depends on the departure and the available events, and very large samples can detect clinically "
            "trivial changes. Look at the residual plot, and ask whether the change in effect matters."
        ) as vo:
            self.add(pbc_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(r) for r in tab[1:]], FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def remedies(self):
        rows = [
            cmath(r"\text{stratify}", r":", r"h_s(t \mid x) = h_{0s}(t)\, e^{x^\top \beta}: \ \text{a baseline per stratum}", font_size=30),
            cmath(r"\text{time-varying } \beta", r":", r"\beta(t) = \beta_0 + \beta_1 g(t), \ \text{or piecewise}", font_size=30),
            cmath(r"\text{start-stop rows}", r":", r"\text{split follow-up; \ the risk set at } t \text{ uses } x(t)", font_size=30),
            cmath(r"\text{or another estimand}", r":", r"\text{RMST, \ survival at } t \ \text{(chapter 10)}", font_size=30),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"for a nuisance factor"), why(r"an interaction with time"), why(r"Andersen--Gill counting process"),
                why(r"no PH needed")]
        with self.voiceover(
            "<bookmark mark='a'/> What to do. If the offending variable is a nuisance, stratify on it: each stratum "
            "gets its own baseline hazard, and nothing is assumed about how they relate. <bookmark mark='b'/> If its "
            "effect is the point, let the coefficient change with time, smoothly or in pieces. <bookmark mark='c'/> "
            "Time-varying covariates or piecewise effects can be fitted by splitting follow-up into start-stop rows; "
            "the counting-process form of chapter six. <bookmark mark='d'/> Or report an estimand that needs no "
            "proportional hazards at all, the subject of chapter ten."
        ) as vo:
            heading = label('Respond to nonproportionality by changing the model or estimand', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def split(self):
        d = load("veteran")
        rows = [[r"Karnofsky, \ per 10 points", r"hazard ratio", r"95\% CI"],
                [r"one HR for all time", f"{d['hr_karno10']:.2f}", f"{np.exp(d['beta'][0] - 1.96 * d['se'][0]):.2f}--{np.exp(d['beta'][0] + 1.96 * d['se'][0]):.2f}"],
                [rf"first {d['cut']:.0f} days", f"{d['early_hr']:.2f}", f"{d['early_hr'] * np.exp(-1.96 * d['early_se']):.2f}--{d['early_hr'] * np.exp(1.96 * d['early_se']):.2f}"],
                [rf"after {d['cut']:.0f} days", f"{d['late_hr']:.2f}", f"{d['late_hr'] * np.exp(-1.96 * d['late_se']):.2f}--{d['late_hr'] * np.exp(1.96 * d['late_se']):.2f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.2, row_buff=0.36, colors=[GREY_A, SURVC, MISSC, GREY_B]).move_to([0, 0.6, 0])
        foot = label(r"the split: \ each man's follow-up cut at 90 days into two start-stop rows", font_size=24, color=GREY_A).move_to([0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For the veterans, split each man's follow-up at ninety days and give the score a "
            "separate coefficient in each piece. <bookmark mark='b'/> In the first ninety days, ten Karnofsky points cut "
            "the hazard to " + say(d["early_hr"], 2) + " of its value; <bookmark mark='c'/> after ninety days, the ratio is "
            + say(d["late_hr"], 2) + ": a much weaker estimated late association. An interval containing one does not establish that the late "
            "effect is zero."
        ) as vo:
            self.add(veteran_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
        self.clear_scene()

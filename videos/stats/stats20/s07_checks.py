from __future__ import annotations

import numpy as np

from videos.stats.stats20.common import *  # noqa: F403


def spline_est(d):
    for r in d["runs"]:
        s = r["spec"]
        if (s["meds"] == "exclude" and s["energy"] and s["weights"] and s["readings"] == "2+" and s["exposure"] == "day1"
                and s["age_spline"]):
            return r
    raise KeyError


class Checking(VoiceoverScene):
    def construct(self):
        self.card()
        self.residuals()
        self.qq()
        self.age_curve()
        self.interaction()
        self.influence()
        self.summary()

    def card(self):
        card = chapter_card(6, r"Checking it", r"Is the model hiding something?", part=PART)
        with self.voiceover("Chapter six. Checking the model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def residuals(self):
        d = load("checks")
        r = d["rvf"]
        f = np.array([x["fit"] for x in r])
        e = np.array([x["res"] for x in r])
        se = np.array([x["se"] for x in r])
        A = axes([104, 138], [-10, 10], x_length=8.4, y_length=4.2, xlabel=r"fitted pressure, \ mm Hg",
                 ylabel=r"mean residual, \ 20 bins", xticks=[105, 115, 125, 135], yticks=[-10, -5, 0, 5, 10], center=[-1.4, 0.3, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(104, 0), ax.c2p(138, 0), color=GREY_C, stroke_width=1.5)
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=MODEL_C) for a, b in zip(f, e)])
        bars = VGroup(*[Line(ax.c2p(a, b - 2 * s), ax.c2p(a, b + 2 * s), color=MODEL_C, stroke_width=2) for a, b, s in zip(f, e, se)])
        rows = fit_rows(VGroup(
            label(r"each dot: \ 150 adults with similar fitted values", font_size=22),
            label(r"bars: \ $\pm 2$ SE", font_size=22, color=GREY_B),
            label(r"no clear trend: \ the straight lines fit on average", font_size=22, color=HIT),
            label(r"a dip at the top: \ the oldest, \ curvature in age?", font_size=22, color=OBS),
        ), 3.45, 0.4, [5.1, 0.3, 0])
        with self.voiceover(
            "Part 12's checks, in order. <bookmark mark='a'/> First, residuals against fitted values. With three thousand "
            "points a raw scatter is a blur, so each dot is the average residual of a hundred and fifty adults with similar "
            "fitted values, <bookmark mark='b'/> with rough two-standard-error bars. <bookmark mark='c'/> There's no strong "
            "pattern: on average the model's straight lines fit. <bookmark mark='d'/> The highest bins dip below zero, which "
            "could mean the relationship with age isn't straight. We'll look directly."
        ) as vo:
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.05), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars), FadeIn(rows[1]))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def qq(self):
        d = load("checks")
        th, sm = np.asarray(d["qq"]["theory"]), np.asarray(d["qq"]["sample"])
        A = axes([-3, 3], [-3, 5], x_length=5.6, y_length=4.6, xlabel=r"normal quantile", ylabel=r"residual quantile (standardized)",
                 xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[-2, 0, 2, 4], center=[-2.8, 0.2, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(-3, -3), ax.c2p(3, 3), color=GREY_C, stroke_width=1.5)
        m = sm < 5
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=RES) for a, b in zip(th[m], sm[m])])
        rows = fit_rows(VGroup(
            label(rf"skewness {d['skew']:.2f}: \ a long right tail", font_size=24, color=RES),
            label(r"design-based intervals do not require normal individual residuals", font_size=22, color=HIT),
            label(r"an interval for one person's pressure: \ would not be", font_size=22, color=OBS),
            label(r"a log scale would tame the tail, \ at the cost of a harder estimand", font_size=22, color=GREY_A),
        ), 5.4, 0.42, [3.6, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Next, a normal quantile plot of the residuals. They bend upward on the right: a "
            "long right tail, skewness about one, the same tail we saw in chapter four. <bookmark mark='b'/> Does it "
            "matter? Normal individual residuals are not required for a design-based slope interval. Its "
            "approximation depends on the sampled PSUs and regularity, not merely the number of people; thirty masked"
            " PSUs are a modest basis. <bookmark mark='c'/> For predicting one person's pressure, it would: a normal "
            "interval would miss the high values. <bookmark mark='d'/> Modelling log pressure would tame the tail, "
            "but then the estimand becomes a percent change, and the plan asked for millimetres."
        ) as vo:
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.02), FadeIn(rows[0]), run_time=2.0)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def age_curve(self):
        d = load("checks")
        sp = spline_est(load("spec"))
        ages = np.asarray(d["ages"], float)
        A = axes([20, 80], [0, 30], x_length=7.6, y_length=4.2, xlabel=r"age", ylabel=r"pressure relative to age 20, \ mm Hg",
                 xticks=[20, 30, 40, 50, 60, 70, 80], yticks=[0, 10, 20, 30], center=[-1.8, 0.3, 0])
        ax = A.ax
        lin = polyline(ax, ages, d["curve_linear"], GREY_B, 3)
        spl = polyline(ax, ages, d["curve_spline"], MODEL_C, 4)
        knots = VGroup(*[DashedLine(ax.c2p(k, 0), ax.c2p(k, 30), color=GREY_D, stroke_width=1) for k in (25, 40, 55, 70)])
        rows = fit_rows(VGroup(
            label(r"grey: \ the straight line", font_size=22, color=GREY_B),
            label(r"blue: \ a restricted cubic spline, \ knots 25, \ 40, \ 55, \ 70", font_size=22, color=MODEL_C),
            label(rf"flat, \ then steeper: \ Wald $F_{{2,15}} = {d['wald'] / 2:.2f}$, \ $p = {d['wald_p']:.3f}$", font_size=22, color=OBS),
            label(rf"sodium's slope: \ {load('model')['est']:+.2f} $\to$ {sp['est']:+.2f}", font_size=24, color=SALT),
            label(r"this spline barely changes the sodium estimate", font_size=22, color=HIT),
        ), 4.3, 0.4, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The model forced age to be a straight line. Replace it with a restricted cubic "
            "spline, a smooth curve built from cubic pieces joined at four knots and kept straight beyond the outer "
            "ones. <bookmark mark='b'/> The spline is flat in the twenties and thirties and climbs steeply after "
            "that, <bookmark mark='c'/> and the design-based Wald F test on the two extra terms, using fifteen "
            "denominator degrees of freedom, gives a p-value of about point zero two two. <bookmark mark='d'/> But "
            "what happens to sodium's slope? It moves from point zero seven to point zero four. <bookmark mark='e'/> "
            "This particular age adjustment barely changes the sodium coefficient; it does not establish that all "
            "model misspecification is harmless. That's the purpose of a check: not to make the model perfect, but to"
            " see whether its flaws change the answer."
        ) as vo:
            self.play(FadeIn(A), Create(knots), Create(lin), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(spl), FadeIn(rows[1]), run_time=2.0)
            for k, m_ in enumerate("bcde"):
                if k == 0:
                    vo.wait_until(m_)
                    continue
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def interaction(self):
        d = load("checks")
        m = load("model")
        b1 = d["inter_main"]
        at = lambda a: b1 + d["inter"] * (a - 50)  # noqa: E731
        rows = [
            cmath(r"\text{add}", r":", r"\beta_6\,\text{sodium} \times (\text{age} - 50)", font_size=30),
            cmath(r"\hat\beta_6", r"=", rf"{d['inter']:.3f}\ (\text{{SE}}\ {d['inter_se']:.3f})", font_size=30),
            cmath(r"\text{slope at 30, \ at 70}", r":", rf"{at(30):+.2f},\ \ {at(70):+.2f}\ \text{{mm Hg per g}}", font_size=30),
            cmath(r"\text{status}", r":", r"\text{exploratory: \ not in the plan}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"does salt matter more at some ages?"), why(r"$t = -2.6$, \ $p = 0.02$"),
                why(r"the trials: \ older people are \emph{more} salt-sensitive"), why(r"a forking path: \ report it, \ flagged")]
        intro = label('An interaction changes both the main slope and its age dependence', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The model also assumed sodium's slope is the same at every age. Let it vary, with an "
            "interaction between sodium and age. <bookmark mark='b'/> The interaction comes out negative, minus point zero four "
            "per year, with a p-value of two percent. <bookmark mark='c'/> Taken at face value, salt goes with higher pressure "
            "at thirty and lower pressure at seventy, which is the opposite of what trials find: older people are more "
            "sensitive to salt, not less. <bookmark mark='d'/> This wasn't in the plan. It's one of many things we could have "
            "tried, and a p-value of two percent after a search is weak evidence. The report mentions it, labelled "
            "exploratory, with chapter nine's likely explanation: older people with high pressure have often been told to cut "
            "their salt."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.75, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def influence(self):
        d = load("checks")
        rows = [
            cmath(r"\text{Cook's distance}", r":", r"\text{how much each adult moves the fit}", font_size=28),
            cmath(r"\text{drop the top 1\%}", r":", rf"\text{{{d['n_drop']} adults}}", font_size=30),
            cmath(r"\text{sodium's slope}", r":", rf"{d['est']:+.2f} \to {d['est_drop']:+.2f}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{no handful of people drives it}", font_size=30),
        ]
        rows[2][2].set_color(SALT)
        whys = [why(r"Part 12: \ leverage $\times$ residual, \ weighted"), why(r"a check, \ not a new analysis"),
                why(r"well inside one SE"), why(r"robust to the most influential points")]
        intro = label('Sensitivity to influential observations is one diagnostic', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Finally, influence: Part 12's Cook's distance measures how much the fit would move "
            "if each adult were left out. Big survey weights can make a few people very influential. <bookmark "
            "mark='b'/> As a check, not a new analysis, drop the thirty most influential adults, one percent of the "
            "sample. <bookmark mark='c'/> Sodium's slope goes from plus point zero seven to minus point zero two, "
            "well within one standard error. <bookmark mark='d'/> Removing this influential subset changes the "
            "estimate little. That check does not rule out every influential group or model problem."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.75, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def summary(self):
        rows = fit_rows(VGroup(
            label(r"residuals: \ no systematic pattern", font_size=24, color=HIT),
            label(r"a skewed tail: \ normality is not required for design inference", font_size=24, color=HIT),
            label(r"age is curved: \ fixing it leaves sodium unchanged", font_size=24, color=HIT),
            label(r"an unplanned interaction: \ reported, \ flagged, \ not believed yet", font_size=24, color=OBS),
            label(r"no influential handful", font_size=24, color=HIT),
            label(r"these checks do not establish that the model is correct", font_size=26, color=SALT),
        ), 12.4, 0.45, [0, 0, 0])
        intro = label('Diagnostics can reveal problems without proving a model correct', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> So: the residuals show no systematic pattern; <bookmark mark='b'/> the tail does "
            "not itself require normality for design-based inference; <bookmark mark='c'/> the spline suggests "
            "curvature but barely moves sodium; <bookmark mark='d'/> an interaction turned up that we didn't plan, "
            "and it's reported with that label; <bookmark mark='e'/> and no few people drive the result. <bookmark "
            "mark='f'/> These checks leave the main recall-day estimate similar. They cannot prove the model correct "
            "or explain every difference from trials."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

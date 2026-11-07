from __future__ import annotations

import numpy as np

from videos.stats.stats36.common import *  # noqa: F403


class LaLonde(VoiceoverScene):
    def construct(self):
        self.card()
        self.overlap()
        self.estimates()
        self.chart()
        self.placebo()
        self.lessons()

    def card(self):
        card = chapter_card(15, r"LaLonde revisited", r"What forty years of re-analysis taught", lit=(1986, 1999), part=PART)
        with self.voiceover("Chapter fifteen. LaLonde, revisited."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def overlap(self):
        d = load("lalonde2")
        h1, h0 = np.asarray(d["h_t"], float), np.asarray(d["h_c"], float)
        e = np.linspace(0, 1, 21)
        A = axes([0, 1], [0, 0.8], x_length=7.4, y_length=4.2, xlabel=r"estimated propensity", ylabel=r"share",
                 xticks=[0, 0.5, 1], yticks=[0, 0.4, 0.8], center=[-2.0, 0.2, 0])
        ax = A.ax
        b1 = hist_bars(ax, e, h1 / h1.sum(), color=Y1C, opacity=0.5)
        b0 = hist_bars(ax, e, h0 / h0.sum(), color=Y0C, opacity=0.5)
        side = fit_rows(VGroup(
            label(r"trainees vs PSID men: \ propensity model inspired by Dehejia \& Wahba", font_size=22),
            label(rf"{100 * d['share_controls_below_01']:.0f}\% of PSID men: \ $\hat e < 0.1$", font_size=22, color=Y0C),
            label(rf"{100 * d['share_treated_above_05']:.0f}\% of trainees: \ $\hat e > 0.5$", font_size=22, color=Y1C),
            label(rf"only {d['n_kept_controls']} of {d['n_controls']} PSID men inside the trainees' range", font_size=22, color=MISSC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Return to LaLonde's trainees and the survey men, with a teaching propensity model "
            "inspired by Dehejia and Wahba: age, education and their squares, race, marriage, degree, and earnings in"
            " 1974 and 1975 with indicators for zero earnings. <bookmark mark='b'/> Two thirds of the survey men have"
            " a propensity below a tenth: nothing like the trainees. <bookmark mark='c'/> Three quarters of the "
            "trainees have a propensity above a half. <bookmark mark='d'/> The comparison rests on a minority of the "
            "survey men, and, within the overlap, on a few who resemble the trainees closely."
        ) as vo:
            self.add(nsw_tag())
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(b0), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(b1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def estimates(self):
        d = load("lalonde2")
        rows = [[r"method", r"estimate (\$)"],
                [r"the experiment", rf"{d['exp']:,.0f}"],
                [r"raw difference", rf"{d['naive']:,.0f}"],
                [r"OLS with covariates", rf"{d['ols']:,.0f}"],
                [r"regression, \ for the treated", rf"{d['reg_att']:,.0f}"],
                [r"propensity matching", rf"{d['match']:,.0f}"],
                [r"IPW, \ for the treated", rf"{d['ipw_att']:,.0f}"],
                [r"IPW, \ overlap only", rf"{d['ipw_att_overlap']:,.0f}"],
                [r"five strata, \ overlap only", rf"{d['subclass']:,.0f}"]]
        tab = table_rows(rows, font_size=24, col_buff=1.2, row_buff=0.22,
                         colors=[GREY_A, BANDC, MISSC, TAUC, TAUC, PSC, PSC, PSC, PSC]).move_to([0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The experiment says about eighteen hundred dollars. <bookmark mark='b'/> Against "
            "the survey men, the raw difference is negative. Regression with the covariates, and regression used to "
            "predict what the trainees would have earned, give fifteen to sixteen hundred. <bookmark mark='c'/> "
            "Propensity-score matching with one neighbour gives about four hundred; weighting, about thirteen "
            "hundred, or fifteen hundred when restricted to the overlap; five strata on the overlap, about five "
            "hundred. <bookmark mark='d'/> Every one of these is a textbook method, applied as the textbooks say, and"
            " they span more than a thousand dollars, a substantial fraction of the experimental confidence "
            "interval's width. The methods also differ in extrapolation and, after trimming, their target "
            "populations."
        ) as vo:
            self.add(nsw_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[5:]], lag_ratio=0.3))
        self.clear_scene()

    def chart(self):
        d = load("lalonde2")
        names = [("exp", r"experiment", BANDC), ("naive", r"raw", MISSC), ("ols", r"OLS", TAUC), ("reg_att", r"reg.\ ATT", TAUC),
                 ("match", r"matching", PSC), ("ipw_att", r"IPW", PSC), ("ipw_att_overlap", r"IPW, overlap", PSC), ("subclass", r"strata", PSC)]
        A = axes([0, 8], [-1000, 3500], x_length=8.4, y_length=4.4, xlabel=r"", ylabel=r"effect on 1978 earnings (\$)",
                 xticks=[], yticks=[-1000, 0, 1000, 2000, 3000], yfmt=lambda v: rf"{v:,.0f}", center=[-1.6, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(i + 0.5, d[k]), radius=0.1, color=c) for i, (k, _, c) in enumerate(names)])
        labs = VGroup(*[label(n, font_size=16, color=c).rotate(PI / 8).next_to(ax.c2p(i + 0.5, -1000), DOWN, buff=0.25) for i, (_, n, c) in enumerate(names)])
        band = Rectangle(width=ax.c2p(8, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 3109)[1] - ax.c2p(0, 479)[1], stroke_width=0,
                         fill_color=BANDC, fill_opacity=0.12).move_to(ax.c2p(4, (3109 + 479) / 2))
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(8, 0), color=GREY_C, stroke_width=1.5)
        foot = label(r"green band: \ the experiment's 95\% interval", font_size=20, color=BANDC).move_to([4.6, 2.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> As a picture, with the experiment's ninety-five percent interval as the green band."
            " <bookmark mark='b'/> All but one of the adjusted estimates land inside it, which is better than "
            "LaLonde's original methods managed, and matching falls just below; but they still differ materially, and"
            " a researcher with only the survey data would have no way of knowing which to trust."
        ) as vo:
            self.add(nsw_tag())
            self.play(FadeIn(A), FadeIn(band), Create(zero), FadeIn(labs), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dd, scale=0.5) for dd in dots], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Indicate(dots[4]), Indicate(dots[7]))
        self.clear_scene()

    def placebo(self):
        d = load("lalonde2")
        rows = fit_rows(VGroup(
            label(r"a placebo test: \ pretend 1975 earnings are the outcome", font_size=26),
            label(r"the programme cannot have affected them: \ the true effect is zero", font_size=26, color=TAUC),
            label(rf"experiment: \ \${d['placebo_exp']:,.0f}; \ PSID, \ matched on 1974 and earlier: \ {'$-$' if d['placebo_psid'] < 0 else ''}\${abs(d['placebo_psid']):,.0f}", font_size=26, color=Y0C),
            label(r"a small placebo point contrast is diagnostic; \ no formal interval is computed", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Guido Imbens and Yiqing Xu, revisiting the data in 2024, stressed a check that "
            "needs no experiment: a placebo test. Treat earnings in 1975, before the programme, as if they were the "
            "outcome, using only earlier information. <bookmark mark='b'/> The programme cannot have affected them, "
            "so a valid method should find nothing. <bookmark mark='c'/> In the experiment the difference is a couple"
            " of hundred dollars, noise; matched against the survey men, minus a hundred and forty. <bookmark "
            "mark='d'/> These small point contrasts are diagnostic rather than formal pass results; no placebo "
            "interval has been computed. A reassuring placebo does not establish exchangeability for later earnings: "
            "the selection into the programme happened after 1975, when the men chose to enrol, and no pre-programme "
            "check can see that."
        ) as vo:
            self.add(nsw_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"1. \ overlap first: \ look at the propensity scores before estimating anything", font_size=26, color=PSC),
            label(r"2. \ pre-treatment outcomes are the most important covariates", font_size=26, color=TAUC),
            label(r"3. \ overlap helps; \ it does not remove model error or hidden confounding", font_size=26, color=BANDC),
            label(r"4. \ unconfoundedness is a substantive claim: \ test what can be tested, \ bound the rest", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lessons that forty years of re-analysis drew. First, check overlap before "
            "estimating anything: most of the survey men should never have been in the comparison. <bookmark "
            "mark='b'/> Second, outcomes measured before treatment, here earlier earnings, are the most important "
            "covariates of all; without them, the methods fail badly. <bookmark mark='c'/> Third, overlap improves "
            "the basis for comparisons, but does not guarantee estimator agreement or remove hidden confounding. Poor"
            " overlap makes estimates particularly dependent on extrapolation. <bookmark mark='d'/> And fourth, "
            "unconfoundedness is a claim about the world: test what can be tested, with placebos, and bound the rest,"
            " with sensitivity analysis."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

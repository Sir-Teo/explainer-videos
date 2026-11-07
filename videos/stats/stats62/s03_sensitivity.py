from __future__ import annotations

import numpy as np

from videos.stats.stats62.common import *  # noqa: F403


class Sensitivity(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter two. Partial identification and sensitivity: how wrong could the answer be?", 2,
                            r"Sensitivity and bounds", r"How much hidden confounding?", lit=(2006,))
        self.manski()
        self.msm()
        self.nsw()
        self.chart()
        self.inference()
        self.reading()
        self.others()

    def manski(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Without no-unmeasured-confounding, the effect is usually not identified, but it is not "
            "unconstrained either. <bookmark mark='b'/> Charles Manski's bounds, Part thirty-seven's, assume only that "
            "outcomes are bounded: the missing potential outcomes could be anything in their range. <bookmark mark='c'/> "
            "These no-assumption bounds always include zero, so they never sign an effect. <bookmark mark='d'/> Sensitivity "
            "analysis sits between: it indexes a family of assumptions by how much hidden confounding they allow, from none "
            "to unlimited, and reports the answer as a function of that index.",
            [(r"\text{without NUC}", r":", r"\text{not identified, \ but constrained}", 40),
             (r"\text{Manski}", r":", r"\text{only bounded outcomes assumed}", 40),
             (r"\text{the bounds}", r":", r"\text{always contain } 0", 40),
             (r"\text{sensitivity}", r":", r"\text{an index } \Lambda \text{ of hidden confounding}", 40)],
            [r"partial identification", r"Part 37", r"too honest to help", r"the middle ground"],
            colors=[(3, HIDC)])

    def msm(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Tan's marginal sensitivity model bounds how full-data treatment odds can differ from measured-covariate odds. A causal interpretation additionally requires a suitable latent-confounding setup and overlap. <bookmark mark='b'/> Lambda one recovers the no-hidden-selection baseline within that model. <bookmark mark='c'/> The odds restriction implies an interval for each inverse-propensity weight. <bookmark mark='d'/> Our sorting algorithm gives exact extrema of a finite Hajek statistic over that weight box. These are relaxed bounds: they omit conditional data-compatibility restrictions and must not be called the sharp population identified set. Dorn and Guo show why quantile balancing can tighten the earlier Zhao, Small and Bhattacharya approach.",
            [(r"\text{MSM}", r":", r"\Lambda^{-1} \le \frac{e(x, u)/(1 - e(x, u))}{e(x)/(1 - e(x))} \le \Lambda", 38),
             (r"\Lambda = 1", r":", r"\text{no hidden confounding}", 40),
             (r"\text{weights}", r":", r"1 + \tfrac{1 - e}{e}\Lambda^{-1} \le w \le 1 + \tfrac{1 - e}{e}\Lambda", 40),
             (r"\text{finite weight-box extrema}", r":", r"\text{sort the outcomes; \ a threshold rule}", 40)],
            [r"Tan (2006)", r"the baseline", r"a box of weights", r"Zhao, \ Small \& Bhattacharya (2019)"],
            colors=[(0, HIDC)])

    def nsw(self):
        d = load("msm")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Real data: Robert LaLonde's 1986 test of observational methods. The National Supported "
            f"Work program was randomized, and the sample difference in 1978 earnings provides an experimental benchmark estimate: "
            f"{say(d['exp'], 0)} dollars. <bookmark mark='b'/> Replace the experimental controls by {d['n0']} men from the Panel "
            f"Study of Income Dynamics, as an observational study would. <bookmark mark='c'/> The raw difference is "
            f"{say(d['naive'], 0)} dollars; inverse-probability weighting on age, education, race, marriage, degree and earlier "
            f"earnings gives {say(d['ipw'], 0)}. <bookmark mark='d'/> Both have the opposite sign from that benchmark, which itself has sampling uncertainty. How much hidden confounding "
            f"would it take to reconcile the weighted estimate with the experiment?",
            [(r"\text{experiment}", r":", rf"\widehat{{\mathrm{{ATE}}}} = {d['exp']:,.0f}", 40),
             (r"\text{observational}", r":", rf"{d['n1']} \text{{ treated vs }} {d['n0']} \text{{ PSID men}}", 40),
             (r"\text{raw; \ IPW}", r":", rf"{d['naive']:,.0f}; \ \ {d['ipw']:,.0f}", 40),
             (r"\text{question}", r":", r"\text{what } \Lambda \text{ reaches the experiment?}", 40)],
            [r"LaLonde (1986)", r"Dehejia \& Wahba's subsample", r"the wrong sign", r"the sensitivity curve"],
            colors=[(0, GOLDC), (2, NAIVEC)])

    def chart(self):
        d = load("msm")
        R = d["rows"]
        lam = np.asarray([r["lam"] for r in R])
        lo, hi = np.asarray([r["lo"] for r in R]), np.asarray([r["hi"] for r in R])
        A = axes([1, 3], [-5500, 5500], x_length=7.4, y_length=4.6, xlabel=r"$\Lambda$, \ the allowed hidden confounding", ylabel=r"ATE on 1978 earnings (\$)",
                 xticks=[1, 1.5, 2, 2.5, 3], yticks=[-4000, -2000, 0, 2000, 4000], yfmt=lambda v: f"{v:,.0f}", center=[-2.5, 0.1, 0])
        ax = A.ax
        band = Polygon(*[ax.c2p(a, b) for a, b in zip(lam, hi)] + [ax.c2p(a, b) for a, b in zip(lam[::-1], lo[::-1])],
                       stroke_width=0, fill_color=HIDC, fill_opacity=0.3)
        lines = VGroup(polyline(ax, lam, hi, HIDC, 3), polyline(ax, lam, lo, HIDC, 3))
        exp = DashedLine(ax.c2p(1, d["exp"]), ax.c2p(3, d["exp"]), color=GOLDC, stroke_width=2.5)
        zero = DashedLine(ax.c2p(1, 0), ax.c2p(3, 0), color=GREY_B, stroke_width=1.5)
        pt = Dot(ax.c2p(1, d["ipw"]), radius=0.09, color=NAIVEC)
        lam_exp = d["tipping_experimental_estimate"]
        lam_zero = d["tipping_zero"]
        side = side_groups([
            [(rf"red: \ IPW at $\Lambda = 1$, \ {d['ipw']:,.0f}", NAIVEC)],
            [(r"purple: \ relaxed weight-box envelope", HIDC)],
            [(rf"they reach 0 at $\Lambda \approx {lam_zero:.2f}$", GREY_A)],
            [(rf"gold: \ the experiment, \ {d['exp']:,.0f}", GOLDC), (rf"reached at $\Lambda \approx {lam_exp:.2f}$", GOLDC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The sensitivity curve. At Lambda equal to one, the weighted estimate, {say(d['ipw'], 0)} "
            f"dollars. <bookmark mark='b'/> As Lambda grows, the relaxed weight-box envelope widens. <bookmark mark='c'/> They include zero "
            f"once Lambda is about {say(lam_zero, 2)}: a hidden factor that changes the odds of joining the program by "
            f"about {100 * (lam_zero - 1):.0f} percent is enough for this relaxed envelope to reach zero. This is not proof that such a hidden factor exists or that the population effect is zero. <bookmark mark='d'/> They reach the experimental answer at Lambda about "
            f"{say(lam_exp, 2)}. The observational study is fragile in both directions, which is what LaLonde found."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(museum_tag(r"NSW: \ LaLonde (1986); \ Dehejia \& Wahba (1999)")))
            vo.wait_until("a")
            self.play(FadeIn(pt, scale=0.5), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(band), Create(lines), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(exp), FadeIn(side[3]))
        self.clear_scene()

    def reading(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Lambda measures a bound on a specified hidden-selection odds ratio. <bookmark mark='b'/> Dropping a measured variable and refitting can provide a descriptive comparison, but it does not establish the strength or outcome relevance of an unmeasured confounder. <bookmark mark='c'/> This demonstration does not compute a strongest-covariate benchmark or identify motivation as the omitted cause. Propensity clipping and population comparability also matter. <bookmark mark='d'/> Report the sensitivity curve, sampling uncertainty, target and assumptions together, rather than treating one tipping value as a causal conclusion.",
            [(r"\text{benchmark}", r":", r"\text{how much each measured covariate moves the odds}", 38),
             (r"\text{compare}", r":", r"\text{a hidden factor as strong as the strongest measured one}", 38),
             (r"\text{here}", r":", r"\text{earlier earnings; \ motivation, \ unmeasured}", 40),
             (r"\text{report}", r":", r"\text{the curve, \ not a number}", 40)],
            [r"calibration", r"Cinelli \& Hazlett (2020)", r"LaLonde's lesson", r"honesty"],
            colors=[(3, IDC)])

    def others(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Other sensitivity models, each with its own index. <bookmark mark='b'/> Part thirty-six's Rosenbaum bounds, for matched designs, with Gamma. <bookmark mark='c'/> The E-value of Tyler VanderWeele and Peng Ding: the strength of association a confounder would need. <bookmark mark='d'/> Carlos Cinelli and Chad Hazlett's omitted-variable bounds for regression, in partial R squared. <bookmark mark='e'/> And Lambda, for weighting estimators, with sharp bounds and, as Dorn and Guo showed, population-sharp bounds using quantile balancing under the specified assumptions.",
            [(r"sensitivity models:", GREY_A),
             (r"Rosenbaum's $\Gamma$, \ matched designs \ (Part 36)", HIDC),
             (r"the E-value \ (VanderWeele \& Ding 2017)", HIDC),
             (r"partial $R^2$ bounds \ (Cinelli \& Hazlett 2020)", HIDC),
             (r"Tan's $\Lambda$, \ weighting \ (Dorn \& Guo 2023: \ sharper)", IDC)])

    def inference(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Confounding uncertainty and sampling uncertainty are different. The plotted band is the finite weight-box envelope before adding a bootstrap. <bookmark mark='b'/> We now also compute two hundred treatment-stratified bootstrap resamples, refitting feature scaling and logistic propensities and recomputing both endpoints at each Lambda. <bookmark mark='c'/> Lower-endpoint and upper-endpoint percentiles give an illustrative outer interval. This finite bootstrap does not guarantee coverage of a causal ATE under arbitrary misspecification, clipping or poor overlap. Sharp population bounds require further compatibility constraints and their own inference theory. <bookmark mark='d'/> Only one hundred and eighty-five treated observations are present, so sampling uncertainty in both this comparison and the experimental benchmark matters.",
            [(r"\text{bounds}", r":", r"\text{on the estimand, \ before sampling error}", 40),
             (r"\text{bootstrap}", r":", r"\text{resample, \ recompute both bounds}", 40),
             (r"\text{interval}", r":", r"[\,q_{\alpha/2}(\text{lower}), \ q_{1 - \alpha/2}(\text{upper})\,]", 40),
             (r"\text{here}", r":", r"185 \text{ treated: \ wide}", 40)],
            [r"two uncertainties", r"Zhao et al. (2019)", r"valid within $\Lambda$", r"small samples"],
            colors=[(2, IDC)])

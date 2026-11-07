from __future__ import annotations

import numpy as np

from videos.stats.stats24.common import *  # noqa: F403


class Scoring(VoiceoverScene):
    def construct(self):
        self.card()
        self.question()
        self.curves()
        self.forecasters()
        self.calibration()
        self.crps()
        self.murphy()
        self.advice()

    def card(self):
        card = chapter_card(12, r"Proper scoring rules", r"How to grade a probability", lit=(2007,), part=PART)
        with self.voiceover("Chapter twelve. Proper scoring rules."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def question(self):
        rows = [
            cmath(r"\text{forecast}", r":", r"q = P(y = 1), \ \text{then } y \text{ happens}", font_size=30),
            cmath(r"\text{a score}", r":", r"S(q, y), \ \text{lower is better}", font_size=30),
            cmath(r"\text{proper}", r":", r"E_{y \sim p} S(q, y) \ \text{is smallest at } q = p", font_size=30),
            cmath(r"\text{why it matters}", r":", r"\text{an improper score rewards lying}", font_size=30),
        ]
        rows[2][2].set_color(HIT)
        whys = [why(r"every GLM predicts a probability"), why(r"how good was the forecast?"),
                why(r"honesty is the best policy"), why(r"Gneiting \& Raftery (2007)")]
        intro = label('Proper scores reward truthful probability reporting', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Every model in this part predicts a probability or a whole distribution. How should such "
            "a forecast be graded once we see what happened? <bookmark mark='b'/> A scoring rule assigns a penalty to each "
            "forecast and outcome. <bookmark mark='c'/> It is proper if a forecaster who believes the true probability is "
            "p does best, on average, by reporting exactly p. <bookmark mark='d'/> An improper score rewards forecasters "
            "for shading their beliefs, which is the last thing we want from a model or a weather forecaster. Tilmann "
            "Gneiting and Adrian Raftery set out the theory in 2007."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curves(self):
        d = load("scoring")
        q = np.asarray(d["q"])
        A = axes([0, 1], [0, 1.2], x_length=8.0, y_length=4.4, xlabel=r"reported probability $q$ \ (truth $p = 0.3$)",
                 ylabel=r"expected loss", xticks=[0, 0.3, 0.5, 1], yticks=[0, 0.5, 1], center=[-1.6, 0.3, 0])
        ax = A.ax
        lg = np.asarray(d["log"])
        m = lg < 1.2
        cl = curve(ax, q, lg, MODEL, 3.5)
        cb = curve(ax, q, np.asarray(d["brier"]), TEAL, 3.5)
        ca = curve(ax, q, np.asarray(d["abs"]), RES, 3.5)
        truth = DashedLine(ax.c2p(0.3, 0), ax.c2p(0.3, 1.2), color=TRUE, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"blue: \ log score $-\log q_y$: \ minimum at 0.3", font_size=22, color=MODEL),
            label(r"teal: \ Brier $(q - y)^2$: \ minimum at 0.3", font_size=22, color=TEAL),
            label(r"red: \ absolute $|q - y|$: \ minimum at 0", font_size=22, color=RES),
            label(r"the absolute error says: \ round to 0 or 1", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Suppose the truth is a thirty percent chance. The log score, minus the log of the "
            "probability given to what happened, is smallest on average when the forecast is exactly point three. "
            "<bookmark mark='b'/> So is Glenn Brier's squared error, from weather forecasting in 1950. "
            "<bookmark mark='c'/> But the absolute error is smallest at zero: <bookmark mark='d'/> it tells the forecaster "
            "to round every probability to zero or one. It is improper, and so is plain accuracy."
        ) as vo:
            self.play(FadeIn(A), Create(truth))
            for k, (m_, c) in enumerate(zip("abc", (cl, cb, ca))):
                vo.wait_until(m_)
                self.play(Create(c), FadeIn(rows[k]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def forecasters(self):
        d = load("scoring")
        s = d["scores"]
        hdr = [r"\textbf{forecaster}", r"\textbf{log score}", r"\textbf{Brier}", r"\textbf{accuracy}"]
        names = [("logistic", HIT), ("overconfident", RES), ("base rate", GREY_B)]
        body = [[n, f"{s['calibrated' if n == 'logistic' else n]['log']:.3f}", f"{s['calibrated' if n == 'logistic' else n]['brier']:.3f}", f"{100 * s['calibrated' if n == 'logistic' else n]['acc']:.1f}\\%"] for n, _ in names]
        t = table_rows([hdr] + body, font_size=28, col_buff=0.8, row_buff=0.32, colors=[GREY_A] + [c for _, c in names])
        t.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"2,000 new adults: \ told high blood pressure? \ ({100 * d['prevalence']:.1f}\% yes)", font_size=22),
            label(r"overconfident: \ the same model, \ log odds doubled", font_size=22, color=RES),
            label(r"accuracy ranks it below the base rate; \ both proper scores rank it in between", font_size=22, color=GREY_A),
        ), 12.0, 0.25, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A real comparison. Fit a logistic model for being told one has high blood pressure,"
            " using age, body mass and sex, and score its forecasts on two thousand new adults. <bookmark mark='b'/> "
            "The fitted logistic reference model wins on both proper scores in this holdout. We have not assumed its "
            "probabilities are exactly calibrated. <bookmark mark='c'/> An overconfident version, the same model with"
            " its log odds doubled around the average, is worse on both, <bookmark mark='d'/> and the forecaster who "
            "always says the base rate, seventeen percent, is worst. But accuracy, the share of forecasts on the "
            "right side of a half, puts the base rate above the overconfident model, because it only looks at which "
            "side of a half each forecast falls. Accuracy throws the probability away."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(t[0]))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(t[1]))
            vo.wait_until("c")
            self.play(FadeIn(t[2]), FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(t[3]), FadeIn(foot[2]))
        self.clear_scene()

    def calibration(self):
        d = load("extras")
        A = axes([0, 0.9], [0, 0.9], x_length=5.0, y_length=5.0, xlabel=r"predicted probability", ylabel=r"observed rate",
                 xticks=[0, 0.3, 0.6, 0.9], yticks=[0, 0.3, 0.6, 0.9], center=[-2.8, 0.0, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(0.9, 0.9), color=GREY_B, stroke_width=2)
        cal = VGroup(polyline(ax, d["cal"]["pred"], d["cal"]["obs"], HIT, 3),
                     *[Dot(ax.c2p(a, b), radius=0.07, color=HIT) for a, b in zip(d["cal"]["pred"], d["cal"]["obs"])])
        over = VGroup(polyline(ax, d["over"]["pred"], d["over"]["obs"], RES, 3),
                      *[Dot(ax.c2p(a, b), radius=0.07, color=RES) for a, b in zip(d["over"]["pred"], d["over"]["obs"])])
        errorbars = VGroup()
        for key, color in (("cal", HIT), ("over", RES)):
            for x, lo, hi in zip(d[key]["pred"], d[key]["lo"], d[key]["hi"]):
                errorbars.add(Line(ax.c2p(x,lo), ax.c2p(x,hi), color=color, stroke_width=1.5))
        rows = fit_rows(VGroup(
            label(r"deciles of predicted risk, \ 2,000 new adults", font_size=22),
            label(r"green: logistic reference; \ approximate calibration", font_size=22, color=HIT),
            label(r"red: \ overconfident: \ too flat", font_size=22, color=RES),
            label(r"says 86\%, \ sees 54\%", font_size=22, color=RES),
            label(r"the same ranking, \ so the same AUC", font_size=22, color=GREY_A),
        ), 4.8, 0.42, [3.8, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is why. Sort the new adults into ten groups by predicted risk and plot the "
            "observed rate in each against the average prediction. <bookmark mark='b'/> The logistic model's binned "
            "points are reasonably close to the diagonal, with sampling uncertainty. <bookmark mark='c'/> The "
            "overconfident model's run too flat: <bookmark mark='d'/> where it says eighty-six percent, fifty-four "
            "percent have actually been told. <bookmark mark='e'/> Yet it ranks people in exactly the same order, so "
            "its ROC curve and AUC are identical. AUC alone cannot distinguish these probability scales; proper "
            "scores and calibration diagnostics can."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cal), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(over), FadeIn(rows[2]), FadeIn(errorbars))
            for k, m_ in enumerate("de"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()

    def crps(self):
        d = load("scoring")
        c = d["crps"]
        rows = [
            cmath(r"\text{CRPS}(F, y)", r"=", r"\textstyle\int \{F(t) - [t \ge y]\}^2 dt", font_size=30),
            cmath(r"\text{normal } F", r":", r"\sigma\{z(2\Phi(z) - 1) + 2\phi(z) - 1/\sqrt\pi\}", font_size=30),
            cmath(r"\text{truth } N(0, 1)", r":", rf"\sigma = 1: \ {c['right']:.3f}; \ \ 0.5: \ {c['too_narrow']:.3f}; \ \ 2: \ {c['too_wide']:.3f}", font_size=28),
            cmath(r"\text{units}", r":", r"\text{those of } y; \ \text{the absolute error, \ for a point forecast}", font_size=28),
        ]
        rows[2][2].set_color(HIT)
        whys = [why(r"the continuous ranked probability score"), why(r"$z=(y-\mu)/\sigma$, $\sigma>0$"),
                why(r"too narrow and too wide both lose"), why(r"Part 34 grades intervals the same way")]
        intro = label('CRPS scores a whole predictive distribution', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> For a whole predictive distribution, the continuous ranked probability score "
            "integrates the squared gap between the forecast's distribution function and the step at the outcome. "
            "<bookmark mark='b'/> For a normal forecast it has a closed form. <bookmark mark='c'/> When the truth is "
            "standard normal, in a shared simulation of twenty thousand outcomes, the honest forecast scores about "
            "point five six; one twice too narrow scores point six oh; one twice too wide, point six five. Both are "
            "penalized. <bookmark mark='d'/> It is in the units of the outcome, and for a point forecast it reduces "
            "to the absolute error."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def murphy(self):
        rows = [
            cmath(r"\text{Brier}", r"=", r"\text{reliability} - \text{resolution} + \text{uncertainty}", font_size=30),
            cmath(r"\text{reliability}", r":", r"\text{population: E[(P-E[Y\mid P])^2]}", font_size=30),
            cmath(r"\text{resolution}", r":", r"\text{how far the bins' rates spread from the base rate}", font_size=28),
            cmath(r"\text{log score}", r":", r"\text{expected excess } = \mathrm{KL}(p \,\|\, q)", font_size=30),
        ]
        rows[3][-1].set_color(PATH)
        whys = [why(r"Murphy (1973)"), why(r"the calibration plot's distance from the diagonal"),
                why(r"predictive information; \ distinct from AUC"), why(r"Part 22's divergence, \ again")]
        intro = label('Reliability and resolution are different forecast properties', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Murphy's Brier decomposition separates reliability minus resolution plus outcome "
            "uncertainty. In the population, define calibration as the conditional event probability given the "
            "reported forecast. <bookmark mark='b'/> Reliability is the mean squared gap between that conditional "
            "probability and the forecast. <bookmark mark='c'/> Resolution is the variance of those conditional event"
            " probabilities. It measures predictive information and is not numerically the same as AUC. With finite "
            "arbitrary bins, an exact sample decomposition needs forecasts constant within bins or an additional "
            "within-bin term. <bookmark mark='d'/> The log score's expected excess over reporting the true "
            "probability is the Kullback--Leibler divergence; the total expected loss also includes the entropy of "
            "the truth."       ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"compare probability forecasts with proper scores: \ log, \ Brier, \ CRPS", font_size=24, color=HIT),
            label(r"the log loss is negative average log likelihood on new data", font_size=24, color=MODEL),
            label(r"accuracy and AUC ignore calibration; \ report a calibration plot too", font_size=24, color=RES),
            label(r"decisions need costs: \ Part 19's thresholds", font_size=24, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So compare probability forecasts with proper scores. <bookmark mark='b'/> The mean "
            "negative log score is the negative average log likelihood on new data, which ties forecasting back to "
            "everything in Parts 22 to 24. <bookmark mark='c'/> Accuracy and the area under the ROC curve ignore "
            "calibration, so pair them with a calibration plot. <bookmark mark='d'/> And turning a probability into a"
            " decision needs the costs of each mistake, Part 19's thresholds."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

from __future__ import annotations

import numpy as np

from videos.stats.stats14.common import *  # noqa: F403


class Scoring(VoiceoverScene):
    def construct(self):
        self.card()
        self.task()
        self.roc()
        self.auc_meaning()
        self.calibration()
        self.brier()
        self.proper()
        self.threshold()

    def card(self):
        card = chapter_card(11, r"Scoring predictions", r"Ranking, \ calibration, \ and the Brier score", lit=(1950,), part=PART)
        with self.voiceover("Chapter eleven. Scoring predictions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def task(self):
        d = load("scoring")
        rows = fit_rows(VGroup(
            label(r"fit a risk model on 50,000 of the World's adults; \ judge it on 50,000 others", font_size=26),
            label(r"model 1: \ age alone", font_size=26, color=S.ALT),
            label(r"model 2: \ age and the two screening tests (Part 2)", font_size=26, color=OBS),
            label(r"model 1$'$: \ model 1 with every risk's odds multiplied by four", font_size=26, color=RES),
            label(rf"the condition affects {100 * d['prevalence']:.1f}\% of them: \ how good is each forecast?", font_size=24, color=GREY_A),
        ), 12.4, 0.44, [0, 0, 0])
        intro = label('Evaluate forecasts on adults excluded from training', font_size=36)
        with self.voiceover(
            "Logistic regression produces probabilities. How do you judge a probability forecast? <bookmark mark='a'/> Fit risk "
            "models for the World's silent condition on fifty thousand adults, and judge them on fifty thousand others. "
            "<bookmark mark='b'/> Model one uses age alone. <bookmark mark='c'/> Model two adds the results of Part 2's two "
            "screening tests. <bookmark mark='d'/> And a third, deliberately bad, model takes model one's forecasts and "
            "multiplies every risk's odds by four. <bookmark mark='e'/> The condition affects one adult in a hundred. Which "
            "forecasts are good, and in what sense?"
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def roc(self):
        d = load("scoring")
        A = axes([0, 1], [0, 1], x_length=4.8, y_length=4.8, xlabel=r"false-positive rate", ylabel=r"true-positive rate",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], center=[-3.0, 0.1, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_C, stroke_width=2)
        c1 = VMobject(stroke_color=S.ALT, stroke_width=4).set_points_as_corners([ax.c2p(a, b) for a, b in zip(d["fpr"], d["tpr"])])
        c2 = VMobject(stroke_color=OBS, stroke_width=4).set_points_as_corners([ax.c2p(a, b) for a, b in zip(d["fpr2"], d["tpr2"])])
        rows = fit_rows(VGroup(
            label(r"slide a threshold down the forecasts: \ call ``positive'' above it", font_size=24),
            label(r"plot the cases caught against the healthy flagged", font_size=24),
            MathTex(rf"\text{{age alone: \ AUC}} = {d['auc']:.3f}", font_size=30, color=S.ALT),
            MathTex(rf"\text{{age + tests: \ AUC}} = {d['auc_both']:.3f}", font_size=30, color=OBS),
            label(r"the diagonal: \ a coin, \ AUC = 0.5", font_size=22, color=GREY_A),
        ), 6.0, 0.36, [3.4, 0.1, 0])
        with self.voiceover(
            "The first question is ranking: does the model give higher risks to the people who have the condition? "
            "<bookmark mark='a'/> Choose a threshold, and call everyone above it positive. <bookmark mark='b'/> Record the "
            "fraction of cases caught, the true-positive rate, against the fraction of healthy people wrongly flagged, the "
            "false-positive rate, and slide the threshold from top to bottom. That traces the receiver operating "
            "characteristic curve, a name from radar in the Second World War. <bookmark mark='c'/> Age alone gives a curve "
            "bowed modestly above the diagonal: an area under the curve of point seven two five. <bookmark mark='d'/> With the "
            "two tests the curve hugs the top-left corner: point nine nine two. <bookmark mark='e'/> A coin would give the "
            "diagonal, an area of a half."
        ) as vo:
            self.play(FadeIn(A), Create(diag))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 2:
                    self.play(Create(c1), run_time=1.5)
                if k == 3:
                    self.play(Create(c2), run_time=1.5)
                self.play(FadeIn(rows[k]))
        self.clear_scene()

    def auc_meaning(self):
        d = load("scoring")
        rows = [
            cmath(r"\text{AUC}", r"=", r"P(S_1>S_0) + \tfrac12P(S_1=S_0)", font_size=30),
            cmath(r"\text{AUC}", r"=", r"\frac{U}{n_1 n_0}\quad\text{(Mann--Whitney, Part 16)}", font_size=32),
            cmath(r"\text{age alone}", r":", rf"{d['auc']:.3f}", font_size=32),
            cmath(r"\text{model 1}' \text{(odds} \times 4)", r":", rf"{d['auc']:.3f}\ \ \text{{as well!}}", font_size=32),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"a pure ranking measure"), why(r"Hanley \& McNeil (1982)"), why(r"older people rank higher"),
                why(r"same ranking, \ same AUC: \ it cannot see calibration")]
        with self.voiceover(
            "<bookmark mark='a'/> The area under the curve has a lovely meaning: pick one person with the condition and one "
            "without, at random; the AUC is the probability that the model gives the case a higher score, plus half the probability of a tie. <bookmark mark='b'/> "
            "It's the Mann–Whitney statistic of Part 16, scaled. <bookmark mark='c'/> For age alone, point seven two five: "
            "its ranking credit is about three quarters, counting an age tie as half. <bookmark mark='d'/> But the deliberately bad "
            "model, with every risk's odds quadrupled, has exactly the same AUC, because multiplying the odds doesn't change "
            "anyone's rank. The AUC can't tell whether the probabilities mean what they say."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def calibration(self):
        d = load("scoring")
        A = axes([0, 0.11], [0, 0.11], x_length=4.8, y_length=4.8, xlabel=r"forecast risk", ylabel=r"observed frequency",
                 xticks=[0, 0.05, 0.1], yticks=[0, 0.05, 0.1], center=[-3.0, 0.1, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(0.11, 0.11), color=GREY_C, stroke_width=2)
        good = VGroup(*[Dot(ax.c2p(a, b), radius=0.09, color=S.ALT) for a, b in zip(d["cal_pred"], d["cal_obs"])])
        bad = VGroup(*[Dot(ax.c2p(a, b), radius=0.09, color=RES) for a, b in zip(d["cal_pred_bad"], d["cal_obs_bad"]) if a < 0.11])
        rows = fit_rows(VGroup(
            label(r"ten groups by forecast: \ forecast vs outcome", font_size=24),
            label(r"model 1: \ close to the diagonal in these bins", font_size=24, color=S.ALT),
            label(r"model 1$'$: \ every forecast too high, \ by up to fourfold", font_size=24, color=RES),
            label(r"a ``10\%'' should come true one time in ten", font_size=24, color=OBS),
        ), 6.0, 0.36, [3.4, 0.1, 0])
        with self.voiceover(
            "The second question is calibration: do the probabilities mean what they say? <bookmark mark='a'/> Sort the test "
            "set into ten groups by forecast risk, and plot each group's average forecast against the fraction who actually "
            "had the condition. <bookmark mark='b'/> Model one's points lie along the diagonal: when it says two percent, about "
            "two percent have the condition. This binned check is compatible with calibration, subject to sampling error; it does not prove calibration at every forecast value. <bookmark mark='c'/> The odds-quadrupled model's points lie far "
            "to the right: it forecasts too high everywhere, by up to four times. <bookmark mark='d'/> A forecast of ten percent "
            "should come true one time in ten. A doctor, an insurer or a launch director acting on these numbers needs that, and "
            "the AUC doesn't check it."
        ) as vo:
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in good], lag_ratio=0.1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in bad], lag_ratio=0.1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def brier(self):
        d = load("scoring")
        vals = [(r"training prevalence (0.9\%)", d["brier_base"], GREY_B), (r"age alone", d["brier"], S.ALT), (r"odds $\times$ 4", d["brier_bad"], RES),
                (r"age + tests", d["brier_both"], OBS)]
        A = axes([0, 0.0125], [-0.6, 3.6], x_length=6.4, y_length=3.8, xlabel=r"Brier score \ (lower is better)", ylabel=r"",
                 xticks=[0, 0.005, 0.01], yticks=[], center=[1.0, 0.4, 0], xfmt=lambda v: f"{v:.3f}")
        ax = A.ax
        bars, labs = VGroup(), VGroup()
        for i, (nm, v, c) in enumerate(vals):
            yy = 3 - i
            b = Rectangle(width=ax.c2p(v, 0)[0] - ax.c2p(0, 0)[0], height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to(ax.c2p(0, yy), aligned_edge=LEFT)
            bars.add(b)
            labs.add(VGroup(label(nm, font_size=22, color=c).next_to(ax.c2p(0, yy), LEFT, buff=0.25),
                            label(rf"{v:.5f}", font_size=20, color=c).next_to(b, RIGHT, buff=0.12)))
        foot = fit_rows(VGroup(
            MathTex(r"\text{BS} = \frac1n\sum_i (p_i - y_i)^2", font_size=32),
            label(r"Glenn Brier (1950), \ for weather forecasts", font_size=22, color=GREY_A),
        ), 12.4, 0.2, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One number can judge both at once. Glenn Brier's 1950 score for weather forecasts is the "
            "average squared difference between the forecast probability and what happened, one or zero. Lower is better. "
            "<bookmark mark='b'/> A forecaster who always says the training prevalence, point nine percent, scores point zero zero nine nine. "
            "<bookmark mark='c'/> Age alone improves on that only slightly: age is a weak predictor of a rare condition. "
            "<bookmark mark='d'/> The odds-quadrupled model scores worse than the constant training-prevalence forecast, though it ranks "
            "people exactly as well as model one: its miscalibration costs more than its ranking gains. <bookmark mark='e'/> "
            "With correctly encoded screening tests, the score falls to about point zero zero three four five, roughly a third of the baseline."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(foot))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(GrowFromEdge(bars[k], LEFT), FadeIn(labs[k]))
        self.clear_scene()

    def proper(self):
        rows = [
            cmath(r"\mathbb E[(q - y)^2]", r"=", r"(q - p)^2 + p(1 - p)", font_size=34),
            cmath(r"\text{minimized at}", r"\ ", r"q = p:\ \text{forecast what you believe}", font_size=32),
            cmath(r"\text{BS}", r"=", r"\text{reliability} - \text{resolution} + \text{uncertainty}", font_size=32),
            cmath(r"\text{also proper}", r":", r"\text{the log score } -\log q_{y}\ \text{(the deviance!)}", font_size=32),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"forecast $q$ when the true chance is $p$"), why(r"a proper scoring rule: \ honesty is optimal"),
                why(r"Murphy (1973): \ calibration, \ information, \ base rate"), why(r"Good (1952)")]
        with self.voiceover(
            "Why squares? <bookmark mark='a'/> If the true chance is p and you forecast q, your expected Brier score is q minus p "
            "squared, plus a term you can't control. <bookmark mark='b'/> It's smallest when q equals p: the score rewards "
            "forecasting exactly what you believe. That makes it a proper scoring rule. <bookmark mark='c'/> Allan Murphy "
            "showed in 1973 that the population Brier score splits into three parts, conditioning on the forecast: reliability, which is calibration; resolution, how much the "
            "forecasts vary with the outcome; and the uncertainty of the base rate itself. <bookmark mark='d'/> The logarithmic "
            "score, minus the log of the probability given to what happened, is also proper, as I. J. Good noted in 1952. For individual Bernoulli outcomes, summing it gives half the deviance, so maximum likelihood is fitting by the log score. Part 34 returns to "
            "prediction with guarantees."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.0, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def threshold(self):
        d = load("scoring")
        rows = [
            cmath(r"\text{flag if }\ p_i > t", r":", r"\text{trade missed cases against false alarms}", font_size=30),
            cmath(r"\text{best } t", r"=", r"\frac{c_{\text{false alarm}}}{c_{\text{false alarm}} + c_{\text{missed case}}}", font_size=32),
            cmath(r"\text{a miss 99}\times\text{ as bad}", r":", r"t = 1\%", font_size=32),
            cmath(r"\text{so}", r":", r"\text{the threshold is a decision, \ not a statistic}", font_size=30),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"every point of the ROC curve is a threshold"), why(r"zero cost for correct decisions; constant error costs"),
                why(r"flag anyone with a 1\% risk"), why(r"it needs calibrated probabilities")]
        intro = label('Choose a risk threshold from decision costs', font_size=36)
        with self.voiceover(
            "Finally, a forecast becomes an action through a threshold. <bookmark mark='a'/> Flag everyone whose risk exceeds "
            "t, trading missed cases against false alarms; each point on the ROC curve is one threshold. <bookmark mark='b'/> "
            "If a false alarm costs one unit and a missed case costs another, the best threshold is the ratio of the false "
            "alarm's cost to the sum of both. <bookmark mark='c'/> If missing a case is ninety-nine times worse than a false "
            "alarm, flag anyone whose risk exceeds one percent. <bookmark mark='d'/> The threshold is a decision about costs, "
            "not a property of the data, and the rule only works if the probabilities are calibrated. A model with a fine AUC "
            "but inflated risks would flag far too many people."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        del d
        self.clear_scene()

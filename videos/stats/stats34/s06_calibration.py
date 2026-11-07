from __future__ import annotations

import numpy as np

from videos.stats.stats34.common import *  # noqa: F403


def rel_plot(ax, rel, color, rmin=0.05, rmax=0.22, total=None):
    """A reliability diagram's points: one per non-empty bin, area by count, joined by a line."""
    pred, obs, n = (np.asarray(rel[k], float) for k in ("pred", "obs", "n"))
    k = n > 0
    tot = total or n.sum()
    dots = VGroup(*[Dot(ax.c2p(a, b), radius=rmin + (rmax - rmin) * np.sqrt(c / tot), color=color, fill_opacity=0.75)
                    for a, b, c in zip(pred[k], obs[k], n[k])])
    line = polyline(ax, pred[k], obs[k], color, 2.5)
    return VGroup(line, dots)


class Calibration(VoiceoverScene):
    def construct(self):
        self.card()
        self.define()
        self.nb_plot()
        self.why_nb()
        self.methods()
        self.after()
        self.table()
        self.limits()

    def card(self):
        card = chapter_card(5, r"Calibration", r"When 70\% should mean 70\%", lit=(1999,), part=PART)
        with self.voiceover("Chapter five. Calibration."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def define(self):
        rows = [
            cmath(r"\text{calibrated}", r":", r"P\big(Y = 1 \mid \hat p(X) = p\big) = p \ \ \text{for all } p", font_size=30),
            cmath(r"\text{reliability diagram}", r":", r"\text{bin } \hat p; \ \text{plot the share of } Y = 1 \text{ in each bin}", font_size=28),
            cmath(r"\mathrm{ECE}", r"=", r"\textstyle\sum_b \frac{n_b}{n} \big|\bar y_b - \bar p_b\big|", font_size=32),
            cmath(r"\text{accuracy}", r":", r"\text{a different property}", font_size=32),
        ]
        rows[0][-1].set_color(CALC)
        whys = [why(r"Brier (1950); \ Murphy \& Winkler (1977)"), why(r"the weather forecasters' picture"),
                why(r"expected calibration error"), why(r"a model can be accurate and badly calibrated")]
        with self.voiceover(
            "<bookmark mark='a'/> A probability forecaster is calibrated if, among all the cases where it says p, the "
            "event happens a fraction p of the time. Weather forecasters were the first to check: among the days the "
            "forecast said seventy percent chance of rain, did it rain on seventy percent? <bookmark mark='b'/> The "
            "check is a reliability diagram. Group the predictions into bins, and plot each bin's observed frequency "
            "against its average prediction. Calibration puts the points on the diagonal. <bookmark mark='c'/> The "
            "expected calibration error averages the vertical gaps, weighted by how many cases fall in each bin. "
            "<bookmark mark='d'/> Calibration is not accuracy. A classifier can rank cases perfectly and still say ninety "
            "nine percent when it should say sixty."
        ) as vo:
            intro=label('Calibration compares probabilities with outcome frequencies',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def nb_plot(self):
        d = load("calib")
        A = axes([0, 1], [0, 1], x_length=4.6, y_length=4.6, xlabel=r"predicted $\hat p$", ylabel=r"observed share",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], center=[-3.6, 0.3, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_B, stroke_width=2)
        nb = rel_plot(ax, d["rel"]["nb"], MISSC)
        h = np.asarray(d["hist"]["nb"], float)
        H = axes([0, 1], [0, 0.7], x_length=3.6, y_length=2.0, xlabel=r"$\hat p$", ylabel=r"share",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5], center=[2.3, 1.4, 0])
        hb = hist_bars(H.ax, np.linspace(0, 1, 11), h / h.sum(), color=MISSC, opacity=0.6)
        side = fit_rows(VGroup(
            label(r"Gaussian naive Bayes, \ all 30 features", font_size=22),
            label(rf"{100 * (h[0] + h[-1]) / h.sum():.0f}\% of its predictions below 0.1 or above 0.9", font_size=22, color=MISSC),
            label(r"between: \ it says 0.6--0.9, \ observed frequencies in these small bins are near 0.4", font_size=22, color=MISSC),
            label(rf"accuracy {100 * d['acc']['nb']:.1f}\%; \ mean split ECE {d['ece']['nb']:.3f}", font_size=22, color=CALC),
        ), 4.6, 0.35, [3.0, -1.6, 0])
        self.add(label("Pooled reliability curves; ECE averaged within splits", font_size=30).move_to([0, 3.3, 0]))
        with self.voiceover(
            "<bookmark mark='a'/> Here is a famously overconfident classifier on the biopsies: Gaussian naive Bayes, which "
            "models each of the thirty features as normal within each class and independent of the others. Forty random "
            "splits into training, calibration and test sets; the test predictions are pooled. <bookmark mark='b'/> "
            "Ninety-eight percent of its predictions are below a tenth or above nine tenths: it is almost always certain. "
            "<bookmark mark='c'/> In between, where it says sixty, seventy, eighty percent, the cancers turn out to be "
            "malignant less than half the time. <bookmark mark='d'/> Its accuracy is a respectable ninety-four percent; "
            "its calibration is poor."
        ) as vo:
            self.add(bc_tag())
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(nb), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(H), FadeIn(hb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def why_nb(self):
        rows = [
            cmath(r"\log\frac{\hat p}{1 - \hat p}", r"=", r"\log\frac{\pi_1}{\pi_0} + \textstyle\sum_{j=1}^{30} \log\frac{f_{1j}(x_j)}{f_{0j}(x_j)}", font_size=30),
            cmath(r"\text{radius, perimeter, area}", r":", r"\text{one fact, \ counted three times}", font_size=30),
            cmath(r"\text{the log odds}", r":", r"\text{many times too large}", font_size=32),
            cmath(r"\text{the ranking}", r":", r"\text{still good}", font_size=32),
        ]
        rows[2][-1].set_color(MISSC)
        whys = [why(r"independence: \ the evidence adds"), why(r"correlated 0.94--0.998"),
                why(r"overconfident"), why(r"so the accuracy survives")]
        with self.voiceover(
            "<bookmark mark='a'/> The reason is in its formula. Naive Bayes adds up the log likelihood ratios of the "
            "thirty features, as independent pieces of evidence. <bookmark mark='b'/> But the radius, perimeter and "
            "area of a nucleus are one fact measured three ways, and similar families run through the data, so the "
            "same evidence is counted many times. <bookmark mark='c'/> The log odds come out many times too large. "
            "<bookmark mark='d'/> The ordering of the cases, which determines ranking measures such as A U C, is much"
            " less damaged. This is the typical failure: right direction, wrong confidence."
        ) as vo:
            intro=label('Dependent features can multiply evidence in naive Bayes',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def methods(self):
        d = load("calib")
        rows = [
            cmath(r"\text{Platt}", r":", r"\hat p = \big(1 + e^{-(a + b s)}\big)^{-1}, \ \ (a, b) \text{ by logistic regression}", font_size=28),
            cmath(r"\text{isotonic}", r":", r"\hat p = \text{the monotone fit of } y \text{ on } s \ \text{(PAVA)}", font_size=28),
            cmath(r"\text{temperature}", r":", r"\hat p = \sigma(z/T), \ \text{one parameter}", font_size=30),
            cmath(r"\text{here}", r":", rf"\hat T = {d['T']:.1f}", font_size=32),
        ]
        rows[3][-1].set_color(CALC)
        whys = [why(r"Platt (1999), \ for SVMs"), why(r"Zadrozny \& Elkan (2002); \ Part 21's PAVA"),
                why(r"Guo, \ Pleiss, \ Sun \& Weinberger (2017)"), why(r"median fitted temperature across 40 splits")]
        with self.voiceover(
            "<bookmark mark='a'/> Calibration can be repaired after the fact, on a separate calibration set that the "
            "model was not trained on. John Platt's method of 1999, invented to turn support vector machine scores "
            "into probabilities, is a logistic regression of the label on the model's score. <bookmark mark='b'/> "
            "Isotonic calibration, from Bianca Zadrozny and Charles Elkan, fits the best monotone step function of "
            "the score by Part 21's pool-adjacent-violators algorithm, assuming monotonicity but no parametric shape."
            " Equal scores must be pooled before fitting. <bookmark mark='c'/> And temperature scaling, which Chuan "
            "Guo and his colleagues showed in 2017 fixes most of the overconfidence of modern neural networks, "
            "divides the log odds by a single number T. <bookmark mark='d'/> On the biopsies, the fitted temperature "
            "is about eight: naive Bayes's log odds were about eight times too large, roughly as many times as the "
            "evidence was over-counted."
        ) as vo:
            intro=label('Separate calibration data can fit a new probability scale',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def after(self):
        d = load("calib")
        A = axes([0, 1], [0, 1], x_length=4.6, y_length=4.6, xlabel=r"predicted $\hat p$", ylabel=r"observed share",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], center=[-3.6, 0.3, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_B, stroke_width=2)
        nb = rel_plot(ax, d["rel"]["nb"], MISSC)
        iso = rel_plot(ax, d["rel"]["nb_iso"], BANDC)
        rf = rel_plot(ax, d["rel"]["rf"], TREEC)
        side = fit_rows(VGroup(
            label(r"red: \ naive Bayes, \ raw", font_size=22, color=MISSC),
            label(rf"green: \ after isotonic, \ mean split ECE {d['ece']['nb']:.3f} $\to$ {d['ece']['nb_iso']:.3f}", font_size=22, color=BANDC),
            label(r"blue: \ a forest's vote share, \ raw", font_size=22, color=TREEC),
            label(r"forests are \emph{under}confident at the extremes", font_size=22, color=TREEC),
        ), 5.4, 0.42, [3.2, 0.3, 0])
        self.add(label("Pooled reliability curves; ECE averaged within splits", font_size=30).move_to([0, 3.3, 0]))
        with self.voiceover(
            "<bookmark mark='a'/> After isotonic calibration, naive Bayes's points move towards the diagonal, and its"
            " expected calibration error falls from point oh six two to point oh three eight. <bookmark mark='b'/> A "
            "random forest's probability, the share of trees voting malignant, fails the other way. <bookmark "
            "mark='c'/> Averaging many trees pulls predictions in from zero and one, because some trees always "
            "disagree, so a forest says eighty percent for cases that are malignant nearly always: it is "
            "underconfident at the extremes, as Alexandru Niculescu-Mizil and Rich Caruana found for bagged trees in "
            "2005. Isotonic calibration improves the reliability diagram here; finite-data recalibration is not "
            "guaranteed to improve every score."
        ) as vo:
            self.add(bc_tag())
            self.play(FadeIn(A), Create(diag), FadeIn(nb), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(iso), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeOut(nb), FadeOut(iso), FadeIn(rf), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def table(self):
        d = load("calib")
        e, b, a = d["ece"], d["brier"], d["acc"]
        names = [("nb", r"naive Bayes"), ("nb_platt", r"\ + Platt"), ("nb_temp", r"\ + temperature"), ("nb_iso", r"\ + isotonic"),
                 ("rf", r"forest"), ("rf_iso", r"\ + isotonic")]
        rows = [[r"model", r"accuracy", r"mean split ECE", r"Brier"]] + [[n, rf"{100 * a[k]:.1f}\%", rf"{e[k]:.3f}", rf"{b[k]:.3f}"] for k, n in names]
        tab = table_rows(rows, font_size=26, col_buff=0.8, row_buff=0.25,
                         colors=[GREY_A, MISSC, CALC, CALC, BANDC, TREEC, BANDC]).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"calibration barely moves the accuracy: \ it relabels the scale, \ not the order", font_size=24),
            label(r"the Brier score, \ a proper scoring rule, \ rewards both", font_size=24, color=CALC),
        ), 12.4, 0.35, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> All the numbers, averaged over forty splits. Platt and temperature scaling cut naive "
            "Bayes's calibration error by a sixth to a fifth, isotonic by two fifths; the forest's falls by a third. <bookmark "
            "mark='b'/> The accuracies barely move, since recalibration relabels the probability scale without changing the "
            "order of the cases much. <bookmark mark='c'/> The Brier score, the mean squared error of the probabilities, is "
            "a proper scoring rule from Part 24: it rewards both ranking and calibration. It improves by a quarter for naive "
            "Bayes; the forest's, already good, stays where it was."
        ) as vo:
            self.add(bc_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def limits(self):
        rows = fit_rows(VGroup(
            label(r"calibration is an average over cases: \ `of all the patients told 0.8, \ 80\% have cancer'", font_size=26),
            label(r"it says nothing about \emph{this} patient's 0.8", font_size=26, color=MISSC),
            label(r"calibrated within groups? \ multicalibration (H\'ebert-Johnson et al. 2018)", font_size=26, color=GREY_A),
            label(r"next: \ a marginal guarantee under exchangeability", font_size=26, color=CALC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Calibration is a promise about averages: of all the patients told point eight, "
            "eighty percent have cancer. <bookmark mark='b'/> It says nothing about whether this patient's point "
            "eight is right, and a model can be perfectly calibrated overall while badly wrong for every patient in "
            "some subgroup. <bookmark mark='c'/> Demanding calibration within many overlapping groups at once is "
            "multicalibration, proposed in 2018 by Úrsula Hébert-Johnson and her colleagues, and we will meet it "
            "again in Part 63 on fairness. <bookmark mark='d'/> Next, a marginal guarantee for a new exchangeable "
            "case. It does not promise conditional coverage for each individual."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

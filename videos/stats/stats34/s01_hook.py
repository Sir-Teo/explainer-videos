from __future__ import annotations

import numpy as np

from videos.stats.stats34.common import *  # noqa: F403


def nature_box(center, inner, color, width=3.2):
    box = RoundedRectangle(width=width, height=1.3, corner_radius=0.15, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.12).move_to(center)
    t = label(inner, font_size=24, color=color).move_to(box)
    if t.width > width - 0.3:
        t.width = width - 0.3
    x = label(r"$x$", font_size=30).next_to(box, LEFT, buff=0.9)
    y = label(r"$y$", font_size=30).next_to(box, RIGHT, buff=0.9)
    a1 = Arrow(x.get_right(), box.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
    a2 = Arrow(box.get_right(), y.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
    return VGroup(box, t, x, y, a1, a2)


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.boxes()
        self.lessons()
        self.replies()
        self.since()
        self.question()
        self.objectives()

    def story(self):
        tl = timeline(lit=(2001,)).to_edge(UP, buff=0.35)
        hc = history_card(2001, r"Leo Breiman, \ \emph{Statistical Modeling: The Two Cultures}",
                          r"A Berkeley probabilist who spent thirteen years as a consultant, \ predicting ozone levels "
                          r"and classifying chemical compounds, \ comes back to the university and tells statisticians "
                          r"that they have been solving the wrong problem", color=PREDC, width=11.0,
                          font_size=23).move_to([0, 0.9, 0])
        rows = fit_rows(VGroup(
            label(r"`98\% of all statisticians' model the data; \ 2\% use algorithms", font_size=24),
            label(r"his verdict: \ the 98\% have led statistics into `irrelevant theory'", font_size=24, color=MISSC),
        ), 12.0, 0.35, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2001 Leo Breiman published a paper in Statistical Science called Statistical Modeling: "
            "The Two Cultures. Breiman was a probabilist who had left a professorship to work as a consultant for thirteen "
            "years, predicting next-day ozone levels for Los Angeles and identifying chemical compounds from their mass "
            "spectra. When he came back to Berkeley he found his colleagues doing something he no longer recognised as "
            "useful. <bookmark mark='b'/> There are two cultures, he wrote. In one, which he estimated held ninety-eight "
            "percent of statisticians, you assume the data come from a stochastic model and estimate its parameters. In "
            "the other, two percent, you treat the mechanism as unknown and find an algorithm that predicts well. "
            "<bookmark mark='c'/> His verdict was blunt: the commitment to data models had led to irrelevant theory and "
            "questionable conclusions, and kept statisticians away from the most interesting problems of the day."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def boxes(self):
        top = nature_box([-0.6, 2.2, 0], r"nature", GREY_B)
        mid = nature_box([-0.6, 0.0, 0], r"linear regression, \ logistic, \ Cox", TRUEC, width=4.4)
        bot = nature_box([-0.6, -2.2, 0], r"unknown: \ find $f(x) \approx y$", PREDC, width=4.4)
        tags = VGroup(
            label(r"the problem", font_size=20, color=GREY_A).next_to(top, LEFT, buff=0.5),
            label(r"data modelling", font_size=20, color=TRUEC).next_to(mid, LEFT, buff=0.5),
            label(r"algorithmic modelling", font_size=20, color=PREDC).next_to(bot, LEFT, buff=0.5),
        )
        checks = VGroup(
            label(r"checked by: \ goodness of fit, \ residuals", font_size=20, color=TRUEC).next_to(mid, RIGHT, buff=0.4),
            label(r"checked by: \ accuracy on new data", font_size=20, color=PREDC).next_to(bot, RIGHT, buff=0.4),
        )
        for c in list(checks) + list(tags):
            if c.get_right()[0] > 6.9:
                c.width = 6.9 - c.get_left()[0]
            if c.get_left()[0] < -6.9:
                c.width = c.get_right()[0] + 6.9
                c.align_to([-6.9, 0, 0], LEFT)
        with self.voiceover(
            "<bookmark mark='a'/> His picture was a box. Nature takes inputs x, does something inside the box, and "
            "produces responses y. <bookmark mark='b'/> The data modeller fills the box with a model: a linear regression, "
            "a logistic regression, a proportional hazards model, with parameters to estimate and test. The model is "
            "judged by goodness of fit tests and residual plots, which, Breiman argued, rarely reject anything. "
            "<bookmark mark='c'/> The algorithmic modeller leaves the box closed. Find any function f of x that predicts "
            "y well: a decision tree, a neural network, a forest. <bookmark mark='d'/> Judge it by one standard only: its "
            "accuracy on data it has not seen."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(top), FadeIn(tags[0]))
            vo.wait_until("b")
            self.play(FadeIn(mid), FadeIn(tags[1]), FadeIn(checks[0]))
            vo.wait_until("c")
            self.play(FadeIn(bot), FadeIn(tags[2]))
            vo.wait_until("d")
            self.play(FadeIn(checks[1]))
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"\textbf{Rashomon}: \ many different models predict equally well", font_size=26, color=TREEC),
            label(r"\textbf{Occam}: \ simplicity and accuracy can trade off", font_size=26, color=BOOSTC),
            label(r"\textbf{Bellman}: \ more features can be a blessing, \ not a curse", font_size=26, color=PREDC),
            label(r"his examples: \ forests beat logistic regression on medical data", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> He named three lessons. The Rashomon effect, after Kurosawa's film in which four "
            "witnesses tell four different stories of one crime: many quite different models fit the data equally "
            "well, so which one tells the truth? <bookmark mark='b'/> Occam's dilemma: the most accurate predictors, "
            "forests and ensembles, are the least interpretable, and simplicity may cost accuracy in some problems; "
            "this is an empirical tradeoff, not a universal law. <bookmark mark='c'/> And Bellman's dimensionality: "
            "for prediction, more features are often a blessing, not the curse that classical theory fears. <bookmark"
            " mark='d'/> His examples were medical: on a hepatitis survival data set and others, random forests, "
            "which he had just invented, beat logistic regression."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def replies(self):
        cox = history_card(2001, r"D. R. Cox, \ in reply",
                           r"Predictive accuracy is not the only aim. \ Much of statistics is about understanding, \ about "
                           r"which data to collect, \ and about questions where the future does not resemble the past",
                           color=TRUEC, width=6.2, font_size=21).move_to([-3.4, 0.6, 0])
        efr = history_card(2001, r"Bradley Efron, \ in reply",
                           r"`At first glance Leo Breiman's stimulating paper looks like an argument against parsimony and "
                           r"scientific insight, \ and in favor of black boxes with lots of knobs to twiddle. \ At second "
                           r"glance it still looks that way'", color=BOOSTC, width=6.2, font_size=21).move_to([3.4, 0.6, 0])
        bottom = label(r"Breiman's rejoinder: \ `the best available solution to a data problem might be a data model; \ "
                       r"it might also be an algorithmic model'", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.7)
        if bottom.width > 12.6:
            bottom.width = 12.6
        with self.voiceover(
            "<bookmark mark='a'/> The journal printed replies. David Cox agreed that prediction mattered, but said it was "
            "rarely the only aim. Much of statistics is about understanding a process, about deciding which data to "
            "collect, and about questions where the future will not resemble the past, so that a model of the mechanism "
            "is the only thing that transfers. <bookmark mark='b'/> Bradley Efron opened with a sentence that is still "
            "quoted. At first glance, he wrote, Breiman's stimulating paper looks like an argument against parsimony and "
            "scientific insight, and in favor of black boxes with lots of knobs to twiddle. At second glance it still looks "
            "that way. <bookmark mark='c'/> Breiman's rejoinder was more conciliatory than his paper: the best solution to "
            "a data problem might be a data model, and it might be an algorithm. Use whatever works, and check it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cox, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(efr, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(bottom))
        self.clear_scene()

    def since(self):
        rows = fit_rows(VGroup(
            label(r"2009: \ the Netflix Prize, \ won by a blend of hundreds of models", font_size=26),
            label(r"2012: \ deep networks win the ImageNet competition", font_size=26),
            label(r"tabular data: \ boosted trees performed strongly in this benchmark (Grinsztajn et al. 2022)", font_size=26, color=BOOSTC),
            label(r"the algorithms won prediction; \ statistics was asked a new question", font_size=26, color=CALC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the twenty-five years since, prediction contests went Breiman's way. The Netflix"
            " Prize in 2009 was won by a large blend of models. <bookmark mark='b'/> In 2012 a deep convolutional "
            "network won the ImageNet image-recognition competition by a wide margin, and machine learning took over "
            "vision, speech and language. <bookmark mark='c'/> On ordinary tables of data, gradient boosted trees are"
            " still the ones to beat, as Grinsztajn, Oyallon and Varoquaux found in 2022. <bookmark mark='d'/> So the"
            " algorithms won prediction. But that left statistics with a new question, and it is the question of this"
            " part."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def question(self):
        d = load("forest")
        rows = fit_rows(VGroup(
            label(r"569 breast biopsies, \ 30 features of the cell nuclei", font_size=24),
            label(rf"a forest: \ {100 * d['acc_rf']:.1f}\% correct on 169 held-out cases", font_size=24, color=TREEC),
            label(r"this patient: \ `malignant, \ probability 0.83'", font_size=24, color=PREDC),
            label(r"is 0.83 honest? \ how wrong could it be? \ what is it estimating?", font_size=24, color=CALC),
        ), 5.6, 0.45, [3.6, 0.3, 0])
        rng_ = np.random.default_rng(4)
        cells = VGroup()
        for i in range(12):
            r = 0.18 + 0.09 * rng_.random()
            e = Ellipse(width=2 * r * (1 + 0.3 * rng_.random()), height=2 * r, stroke_color=PREDC, stroke_width=2,
                        fill_color=PREDC, fill_opacity=0.15).rotate(rng_.random() * PI)
            e.move_to([-4.6 + 2.6 * rng_.random(), -1.4 + 3.2 * rng_.random(), 0])
            cells.add(e)
        cap = label(r"a fine-needle aspirate, \ digitized", font_size=20, color=GREY_B).move_to([-3.3, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is a problem of Breiman's kind. In the early 1990s William Wolberg, Nick Street "
            "and Olvi Mangasarian digitized the cells of five hundred and sixty-nine breast biopsies at the University of "
            "Wisconsin, and measured thirty features of the nuclei: their radius, texture, concavity and so on. "
            "<bookmark mark='b'/> A random forest trained on four hundred of them classifies the other hundred and "
            "sixty-nine with ninety-four percent accuracy. <bookmark mark='c'/> For a new patient it says: malignant, "
            "probability point eight three. <bookmark mark='d'/> A statistician asks: is point eight three honest? How "
            "wrong could the forest be about this patient? And what, exactly, is the forest estimating?"
        ) as vo:
            self.add(bc_tag())
            self.play(FadeIn(cells), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 34", font_size=34, color=GREY_B), label(r"Prediction with Guarantees", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"explain or predict: \ the Rashomon effect",
            r"forests and boosting as estimators: \ variance, \ importance, \ intervals",
            r"what cross-validation estimates; \ calibration",
            r"conformal prediction: \ split, \ jackknife+, \ CQR, \ under shift, \ sets",
            r"prediction-powered inference; \ interpretation as estimation",
        ], color=PREDC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 16, 19 and 33").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.conformal}, \ \texttt{statkit.ppi}; \ the score ladder").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-four: prediction with guarantees. <bookmark mark='b'/> We'll see why "
            "good predictors do not explain; treat forests and boosting as estimators, with a variance, an importance"
            " measure and confidence intervals; ask what cross-validation actually estimates, and when a probability "
            "can be trusted; then build conformal prediction, which wraps any model, forest or neural network, in "
            "intervals and sets with a marginal finite-sample guarantee under exchangeability and proper separation "
            "of training and calibration; use machine-learning guesses to sharpen a valid estimate, with "
            "prediction-powered inference; and finish with what interpretation methods estimate."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()

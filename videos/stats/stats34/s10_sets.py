from __future__ import annotations

import numpy as np

from explainer.stats import museum
from videos.stats.stats34.common import *  # noqa: F403

SPC = [S.CTRL, S.TREAT, S.ALT]  # setosa, versicolor, virginica


class Sets(VoiceoverScene):
    def construct(self):
        self.card()
        self.lac()
        self.aps()
        self.irises()
        self.examples()
        self.sizes()
        self.mondrian()
        self.cancer()
        self.pvalues()

    def card(self):
        card = chapter_card(9, r"Classification sets", r"Answers that admit doubt", lit=(2020,), part=PART)
        with self.voiceover("Chapter nine. Prediction sets for classification."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def lac(self):
        rows = [
            cmath(r"S_i", r"=", r"1 - \hat p(y_i \mid x_i)", font_size=32),
            cmath(r"C(x)", r"=", r"\{y: \ 1 - \hat p(y \mid x) \le \hat q\}", font_size=32),
            cmath(r"P\big(Y \in C(X)\big)", r"\ge", r"1 - \alpha", font_size=32),
            cmath(r"\text{set size}", r":", r"\text{1 when sure, \ several when not, \ 0 when nothing fits}", font_size=28),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"low probability for the truth: \ a strange case"), why(r"every label that would not be strange"),
                why(r"the quantile lemma again"), why(r"Sadinle, \ Lei \& Wasserman (2019)")]
        with self.voiceover(
            "<bookmark mark='a'/> For classification, the prediction is a set of labels. The simplest score is one minus "
            "the probability the model gave to the true label: a case is strange if the model thought its true class "
            "unlikely. <bookmark mark='b'/> For a new case, include every label whose score would not be strange, that is, "
            "every label whose probability is at least one minus q hat. <bookmark mark='c'/> The quantile lemma guarantees "
            "that the true label is in the set with probability one minus alpha. <bookmark mark='d'/> Mauricio Sadinle, "
            "Lei and Wasserman showed in 2019 that these sets are the smallest on average among all sets with the "
            "coverage. The set's size is itself informative: one label when the model is sure, several when it is not."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def aps(self):
        rows = [
            cmath(r"\text{rank the labels}", r":", r"\hat p_{(1)} \ge \hat p_{(2)} \ge \cdots", font_size=32),
            cmath(r"S_i", r"=", r"\textstyle\sum_{j \text{ ranked above } y_i} \hat p_j + U_i\, \hat p(y_i)", font_size=30),
            cmath(r"C(x)", r"=", r"\text{the top labels until their mass reaches } \hat q", font_size=30),
            cmath(r"\text{aim}", r":", r"\text{coverage closer to conditional}", font_size=32),
        ]
        rows[1][-1].set_color(CALC)
        whys = [why(r"most to least likely"), why(r"$U_i$ uniform: \ exact coverage with ties"),
                why(r"adaptive prediction sets"), why(r"Romano, \ Sesia \& Cand\`es (2020)")]
        with self.voiceover(
            "<bookmark mark='a'/> Smallest on average is not always what we want: such sets can be too small for the hard "
            "cases and too large for the easy ones. Yaniv Romano, Matteo Sesia and Candès proposed adaptive prediction "
            "sets in 2020. Rank the labels from most to least probable. <bookmark mark='b'/> A case's score is the total "
            "probability of the labels ranked above its true label, plus a uniformly random share of the true label's own "
            "probability, which breaks ties and makes the coverage exact. <bookmark mark='c'/> The set for a new case "
            "takes labels in order of probability until their mass reaches q hat. <bookmark mark='d'/> If the model's "
            "probabilities were correct, these sets would have exact conditional coverage; with a real model, they come "
            "closer to it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def irises(self):
        d = load("sets")
        X, y, _ = museum.iris()
        A = axes([4.2, 8.0], [1.9, 4.5], x_length=6.6, y_length=4.6, xlabel=r"sepal length (cm)", ylabel=r"sepal width (cm)",
                 xticks=[5, 6, 7, 8], yticks=[2, 3, 4], center=[-2.4, 0.2, 0])
        ax = A.ax
        jit = np.random.default_rng(1).uniform(-0.03, 0.03, (150, 2))
        dots = VGroup(*[Dot(ax.c2p(a + j0, b + j1), radius=0.055, color=SPC[c], fill_opacity=0.85)
                        for (a, b), c, (j0, j1) in zip(X[:, :2], y, jit)])
        side = fit_rows(VGroup(
            label(r"Fisher's irises, \ sepals only", font_size=22),
            label(r"setosa", font_size=22, color=SPC[0]),
            label(r"versicolor and virginica: \ overlapping", font_size=22, color=SPC[1]),
            label(rf"QDA: \ {100 * d['acc']:.1f}\% correct", font_size=22, color=PREDC),
            label(r"60 to train, \ 45 to calibrate, \ 45 to test; \ 300 splits", font_size=20, color=GREY_A),
        ), 4.4, 0.4, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fisher's irises from Part 31, made harder by using only the sepal measurements. "
            "<bookmark mark='b'/> Setosa stands apart, <bookmark mark='c'/> but versicolor and virginica overlap heavily. "
            "<bookmark mark='d'/> Quadratic discriminant analysis gets only seventy-six percent right. <bookmark mark='e'/> "
            "Sixty flowers train it, forty-five calibrate adaptive prediction sets at ninety percent, and forty-five test "
            "them, over three hundred random splits."
        ) as vo:
            self.add(iris_tag())
            self.play(FadeIn(A), FadeIn(dots))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
        self.clear_scene()

    def examples(self):
        d = load("sets")
        ex = d["example"]
        sp = [r"set.", r"vers.", r"virg."]
        rows = [[r"flower", r"true", r"$\hat p$ (set., vers., virg.)", r"set"]]
        cols = [GREY_A]
        for i in range(len(ex["y"])):
            P = ex["P"][i]
            st = ex["sets"][i]
            rows.append([rf"{i + 1}", sp[ex["y"][i]], rf"{P[0]:.2f}, \ {P[1]:.2f}, \ {P[2]:.2f}",
                         r"\{" + r", \ ".join(sp[c] for c in sorted(st)) + r"\}" if st else r"$\varnothing$"])
            cols.append(BANDC if ex["y"][i] in st else MISSC)
        tab = table_rows(rows, font_size=24, col_buff=0.6, row_buff=0.2, colors=cols).move_to([0, 0.3, 0])
        if tab.height > 6.4:
            tab.height = 6.4
        with self.voiceover(
            "<bookmark mark='a'/> Eight test flowers from one split. The model's three probabilities, and the set. "
            "<bookmark mark='b'/> Each setosa gets the set setosa alone. Flowers the model splits between versicolor and "
            "virginica mostly get both; flower five, at fifty-seven to forty-three, kept only one, because the random "
            "tie-breaking share of the adaptive score happened to be small. All eight are covered here; over many flowers, "
            "about one in ten would not be. The set says what the classifier knows, and what it does not."
        ) as vo:
            self.add(iris_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.25), run_time=4.0)
        self.clear_scene()

    def sizes(self):
        d = load("sets")
        c = np.asarray(d["size_counts"], float)
        A = axes([0, 4], [0, 0.6], x_length=5.4, y_length=4.0, xlabel=r"set size", ylabel=r"share",
                 xticks=[], yticks=[0, 0.25, 0.5], center=[-3.0, 0.3, 0])
        ax = A.ax
        bars = bars_at(ax, np.arange(4) + 0.5, c / c.sum(), 0.7, BANDC)
        labs = VGroup(*[label(rf"{k}", font_size=22, color=GREY_A).next_to(ax.c2p(k + 0.5, 0), DOWN, buff=0.15) for k in range(4)])
        cs = d["class_size"]
        side = fit_rows(VGroup(
            label(rf"coverage: \ {100 * d['cover']:.1f}\%", font_size=22, color=BANDC),
            label(rf"mean set size {d['mean_size']:.2f}", font_size=22),
            label(rf"setosa: \ {cs[0]:.2f} labels on average", font_size=22, color=SPC[0]),
            label(rf"versicolor {cs[1]:.2f}, \ virginica {cs[2]:.2f}", font_size=22, color=SPC[1]),
        ), 4.6, 0.42, [3.8, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Over all the splits, the sets cover " + say(100 * d["cover"], 1) + " percent of test "
            "flowers. <bookmark mark='b'/> Half the sets have a single label, nearly half have two, and a handful have "
            "none or all three. <bookmark mark='c'/> For setosa, the sets almost always contain one label. <bookmark "
            "mark='d'/> For the other two species, they average about one and two thirds: the overlap in the data shows up "
            "as the size of the answer."
        ) as vo:
            self.add(iris_tag())
            self.play(FadeIn(A), FadeIn(labs), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
        self.clear_scene()

    def mondrian(self):
        d = load("sets")
        A = axes([0, 3], [0.8, 1.0], x_length=6.6, y_length=4.2, xlabel=r"true species", ylabel=r"coverage",
                 xticks=[], yticks=[0.8, 0.9, 1.0], yfmt=lambda v: rf"{100 * v:.0f}\%", center=[-2.4, 0.3, 0])
        ax = A.ax
        m_ = VGroup(*[Dot(ax.c2p(i + 0.38, v), radius=0.09, color=PREDC) for i, v in enumerate(d["class_cover"])])
        mo = VGroup(*[Dot(ax.c2p(i + 0.62, v), radius=0.09, color=BANDC) for i, v in enumerate(d["mondrian_cover"])])
        labs = VGroup(*[label(n, font_size=20, color=SPC[i]).next_to(ax.c2p(i + 0.5, 0.8), DOWN, buff=0.15) for i, n in enumerate(d["species"])])
        nine = DashedLine(ax.c2p(0, 0.9), ax.c2p(3, 0.9), color=CALC, stroke_width=2)
        rows = [
            cmath(r"\text{Mondrian}", r":", r"\hat q_c \text{ from class } c\text{'s scores only}", font_size=28),
            cmath(r"P(Y \in C \mid Y = c)", r"\ge", r"1 - \alpha \ \text{each } c", font_size=28),
        ]
        g = VGroup(*[VGroup(*r).arrange(RIGHT, buff=0.2) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.0, 0.8, 0])
        if g.width > 5.2:
            g.width = 5.2
        side = fit_rows(VGroup(
            label(r"blue: \ one threshold for all", font_size=22, color=PREDC),
            label(r"green: \ one per class", font_size=22, color=BANDC),
        ), 4.6, 0.35, [4.0, -1.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Coverage by species is not guaranteed by a single threshold. With one threshold for all "
            "classes, setosa is covered " + f"{100 * d['class_cover'][0]:.0f}" + " percent of the time and virginica "
            + f"{100 * d['class_cover'][2]:.0f}" + ". <bookmark mark='b'/> Vovk's Mondrian conformal prediction, named "
            "after the painter's grid of separate rectangles, calibrates each class separately, using only the "
            "calibration cases of that class to set its own threshold. <bookmark mark='c'/> Then each class is covered at "
            "least ninety percent of the time; here above ninety, since each class has only about fifteen calibration "
            "flowers, and the quantile lemma's rounding is coarse. The same trick gives coverage within any groups fixed in "
            "advance: by sex, by hospital, by age band."
        ) as vo:
            self.add(iris_tag())
            self.play(FadeIn(A), FadeIn(labs), Create(nine))
            vo.wait_until("a")
            self.play(FadeIn(m_), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(g))
            vo.wait_until("c")
            self.play(FadeIn(mo), FadeIn(side[1]))
        self.clear_scene()

    def cancer(self):
        d = load("sets")
        bs = np.asarray(d["bc_sizes"], float)
        tot = bs.sum()
        rows = fit_rows(VGroup(
            label(r"the biopsies: \ logistic regression on three features, \ 95\% sets", font_size=26),
            label(rf"coverage {100 * d['bc_cover']:.1f}\%: \ benign {100 * d['bc_class_cover'][0]:.1f}\%, \ malignant {100 * d['bc_class_cover'][1]:.1f}\%", font_size=26, color=BANDC),
            label(rf"one label: \ {100 * bs[1] / tot:.1f}\%; \ both: \ {100 * bs[2] / tot:.1f}\%; \ none: \ {100 * bs[0] / tot:.1f}\%", font_size=26, color=CALC),
            label(r"an empty set: \ the model's doubt is so large that no label is `unsurprising'", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Back to the biopsies, with a deliberately simple logistic regression on three features "
            "and ninety-five percent sets. <bookmark mark='b'/> The coverage is " + say(100 * d["bc_cover"], 1) + " percent "
            "overall, though malignant cases are covered a little less often than benign: the Mondrian version would fix "
            "that, and for a cancer test it should. <bookmark mark='c'/> Nearly every set has one label. A few contain both "
            "labels, and about two percent are empty. <bookmark mark='d'/> An empty set is the score-based method's way of "
            "spending its five percent: for a case the model puts near fifty-fifty, neither label is probable enough to "
            "pass the threshold. Adaptive sets would return both labels there instead; for a clinic, both is the more "
            "useful answer: send this one to a pathologist."
        ) as vo:
            self.add(bc_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def pvalues(self):
        rows = [
            cmath(r"p(x)", r"=", r"\dfrac{1 + \#\{i: S_i \ge S(x)\}}{n + 1}", font_size=32),
            cmath(r"x \text{ exchangeable}", r"\Rightarrow", r"P\big(p(X) \le u\big) \le u", font_size=32),
            cmath(r"\text{many test cases}", r":", r"\text{BH on the conformal } p\text{-values}", font_size=30),
            cmath(r"\text{FDR}", r"\le", r"q \ \text{(PRDS holds)}", font_size=32),
        ]
        rows[3][-1].set_color(BANDC)
        whys = [why(r"the conformal $p$-value"), why(r"valid for a new case"),
                why(r"Part 33, \ for outlier detection"), why(r"Bates, \ Cand\`es, \ Lei, \ Romano \& Sesia (2023)")]
        with self.voiceover(
            "<bookmark mark='a'/> The same ranks give a p-value for any new case: one plus the number of calibration "
            "scores at least as large as its score, over n plus one. <bookmark mark='b'/> If the new case is exchangeable "
            "with the calibration data, this p-value is valid. A small one says the case is unlike anything seen: an "
            "outlier, a fraud, a new kind of tumour. <bookmark mark='c'/> With many new cases, run Part 33's "
            "Benjamini–Hochberg procedure on their conformal p-values. <bookmark mark='d'/> They share the calibration set "
            "and so are dependent, but Stephen Bates, Candès, Lei, Romano and Sesia proved in 2023 that the dependence is "
            "of the positive kind BH tolerates, so the false discovery rate is controlled."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

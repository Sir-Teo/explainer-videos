from __future__ import annotations

import numpy as np

from videos.stats.stats64.common import *  # noqa: F403


class IRT(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter four. Item response theory: benchmarks as tests, models as test-takers.", 4,
                            r"IRT for benchmarks", r"Not every question is worth the same")
        self.model()
        self.fit()
        self.chart()
        self.info()
        self.tiny()
        self.cautions()

    def model(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Psychometrics met this problem a century ago, with students instead of models. "
            "<bookmark mark='b'/> Item response theory gives each test-taker an ability theta, and each question a "
            "difficulty b and a discrimination a. <bookmark mark='c'/> The chance of a right answer is the logistic "
            "function of a times theta minus b: Allan Birnbaum's two-parameter model, from 1968, a cousin of Part "
            "twenty-five's hierarchical models and of chapter three's Bradley-Terry, with the question as the opponent. "
            "<bookmark mark='d'/> Questions everyone gets right, or no one does, carry no information about who is better.",
            [(r"\text{ability}", r":", r"\theta_m \ \text{for model } m", 40),
             (r"\text{item}", r":", r"a_j \ \text{(discrimination)}, \ b_j \ \text{(difficulty)}", 40),
             (r"P(R_{mj} = 1)", r"=", r"\frac{1}{1 + e^{-a_j(\theta_m - b_j)}}", 40),
             (r"\text{easy or impossible}", r":", r"\text{no information}", 40)],
            [r"psychometrics", r"two item parameters", r"Birnbaum (1968)", r"the item's information"],
            colors=[(2, HONC)])

    def fit(self):
        d = load("irt")
        self.lad_voiceover(
            f"<bookmark mark='a'/> A simulated benchmark: {d['J']:,} questions and {d['M']} models, with abilities and item "
            f"parameters drawn at random. <bookmark mark='b'/> Fit the model to the {d['M']} by {d['J']:,} table of right "
            f"and wrong answers, alternating Newton steps for the items and for the models. <bookmark mark='c'/> The "
            f"fitted abilities correlate {d['theta_corr']:.3f} with the true ones, and the difficulties {d['corr_b']:.2f}. "
            f"<bookmark mark='d'/> Discriminations are harder, a correlation of {d['corr_a']:.2f}: sixty test-takers say "
            f"little about how sharply each question separates them. Part twenty-two's information again: each item has "
            f"only sixty observations.",
            [(r"\text{data}", r":", rf"{d['M']} \times {d['J']:,} \ \text{{right/wrong}}".replace(",", "{,}"), 40),
             (r"\text{fit}", r":", r"\text{alternating Newton (joint ML)}", 40),
             (r"\mathrm{corr}(\hat\theta, \theta)", r"=", rf"{d['theta_corr']:.3f}, \ \ \mathrm{{corr}}(\hat b, b) = {d['corr_b']:.2f}", 40),
             (r"\mathrm{corr}(\hat a, a)", r"=", rf"{d['corr_a']:.2f}", 40)],
            [r"seeded", r"Part 21", r"well determined", r"60 observations per item"],
            colors=[(2, HONC), (3, NAIVEC)])

    def chart(self):
        d = load("irt")
        vals = [(d["rmse_raw"], NAIVEC, r"mean of 100", r"random items"), (d["rmse_irt"], MODA, r"IRT from 100", r"random items"),
                (d["rmse_anchor"], HONC, r"IRT from 100", r"spread anchors")]
        A = axes([-0.6, 2.6], [0, 0.05], x_length=6.4, y_length=4.2, xlabel=r"", ylabel=r"error in the full-benchmark accuracy (RMS)",
                 xticks=None, yticks=[0, 0.01, 0.02, 0.03, 0.04, 0.05], yfmt=lambda v: f"{100 * v:.0f}", center=[-2.8, 0.3, 0])
        ax = A.ax
        bars = VGroup()
        for k, (v, c, n1, n2) in enumerate(vals):
            b = Rectangle(width=0.8, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to(ax.c2p(k, 0), aligned_edge=DOWN)
            nm = VGroup(label(n1, font_size=20, color=c), label(n2, font_size=20, color=c)).arrange(DOWN, buff=0.06)
            bars.add(VGroup(b, label(rf"{100 * v:.1f}", font_size=22, color=c).next_to(b, UP, buff=0.1), nm.next_to(ax.c2p(k, 0), DOWN, buff=0.15)))
        side = side_groups([
            [(r"300 new models, \ each scored on", WHITE), (r"100 of the 1{,}000 questions", WHITE)],
            [(rf"red: \ the plain mean, \ {100 * d['rmse_raw']:.1f} points", NAIVEC)],
            [(rf"blue: \ IRT on random items, \ {100 * d['rmse_irt']:.1f}", MODA)],
            [(rf"green: \ IRT on spread anchors, \ {100 * d['rmse_anchor']:.1f}", HONC), (r"a third less error", HONC)],
        ], pos=(3.6, 0.3, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> The use: evaluating a new model cheaply. Score three hundred new models on only a "
            f"hundred of the thousand questions, and estimate each one's accuracy on all thousand. <bookmark mark='b'/> "
            f"The plain mean of the hundred misses by {100 * d['rmse_raw']:.1f} points, root mean square. <bookmark "
            f"mark='c'/> Estimating the model's ability from the same random hundred, with the fitted item parameters, and "
            f"predicting its accuracy on all the items, misses by {100 * d['rmse_irt']:.1f}. <bookmark mark='d'/> Choosing "
            f"the hundred to span the difficulties, the most discriminating question in each stratum, misses by "
            f"{100 * d['rmse_anchor']:.1f}: a third less error than the plain mean, for the same cost."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(bars[2]), FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def info(self):
        d = load("irt")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Why it works: Fisher information, item by item. <bookmark mark='b'/> An item's "
            f"information about theta is a squared times p times one minus p, largest for discriminating items whose "
            f"difficulty matches the ability. <bookmark mark='c'/> In this benchmark the hundred most informative items, "
            f"for an average model, carry {100 * d['info_top10']:.0f} percent of the total information; "
            f"{100 * d['frac_easy']:.0f} percent of the items are answered correctly by more than ninety-five percent of "
            f"models and carry almost none. <bookmark mark='d'/> Adaptive testing, choosing each next question where the "
            f"current ability estimate is most uncertain, is Part fifty-eight's sequential design applied to exams, and it "
            f"is how computerized tests like the GRE have worked for decades.",
            [(r"I_j(\theta)", r"=", r"a_j^2 \, p_j(\theta)(1 - p_j(\theta))", 40),
             (r"\text{top 100 items}", r":", rf"{100 * d['info_top10']:.0f}\% \ \text{{of the information}}", 40),
             (r"\text{nearly saturated}", r":", rf"{100 * d['frac_easy']:.0f}\% \ \text{{of items}}", 40),
             (r"\text{adaptive testing}", r":", r"\text{ask where it is uncertain}", 40)],
            [r"Part 22", r"at $\theta = 0$", r"wasted questions", r"Part 58"],
            colors=[(1, HONC)])

    def tiny(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The same idea on real benchmarks. <bookmark mark='b'/> Felipe Maia Polo and colleagues' "
            "tinyBenchmarks, in 2024, fitted item response models to the published answers of hundreds of language models. "
            "<bookmark mark='c'/> They found that a hundred curated questions estimate a model's accuracy on the fourteen "
            "thousand of MMLU, a standard knowledge benchmark, with an average error under two points. <bookmark mark='d'/> "
            "The fitted abilities also show what a benchmark measures, and when a benchmark is saturated: when the best "
            "models' abilities sit beyond nearly every question's difficulty.",
            [(r"\text{tinyBenchmarks}", r":", r"\text{IRT on published model answers}", 40),
             (r"\text{MMLU}", r":", r"14{,}000 \to 100 \ \text{questions}", 40),
             (r"\text{error}", r":", r"\text{under 2 points on average}", 40),
             (r"\text{saturation}", r":", r"\text{abilities beyond the items}", 40)],
            [r"Maia Polo et al. (2024)", r"curated anchors", r"their report", r"a benchmark's lifetime"],
            colors=[(2, HONC)])

    def cautions(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Two cautions. <bookmark mark='b'/> The model assumes one ability. Language models have "
            "many, and a model strong at code and weak at history breaks a one-dimensional scale; multidimensional item "
            "response theory, Part thirty-one's factor analysis with logistic links, is the remedy. <bookmark mark='c'/> And "
            "the item parameters were learned from past models. A new kind of model, unlike any in the calibration set, is "
            "Part sixty's distribution shift. <bookmark mark='d'/> Check the small-sample estimate against the full benchmark "
            "now and then.",
            [(r"\text{one ability}", r":", r"\text{too simple}", 40),
             (r"\text{remedy}", r":", r"\text{multidimensional IRT}", 40),
             (r"\text{new kinds of model}", r":", r"\text{distribution shift}", 40),
             (r"\text{so}", r":", r"\text{audit with the full benchmark}", 40)],
            [r"many skills", r"Part 31", r"Part 60", r"a check"],
            colors=[(0, NAIVEC)])

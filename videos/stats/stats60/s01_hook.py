from __future__ import annotations

import numpy as np

from videos.stats.stats60.common import *  # noqa: F403


class Hook(LectureMixin, VoiceoverScene):
    def construct(self):
        self.story()
        self.lesson()
        self.two_threats()
        self.covshift_preview()
        self.board()
        self.taxonomy()
        self.upgrade()
        self.objectives()

    def story(self):
        tl = timeline(lit=(2019,)).to_edge(UP, buff=0.35)
        hc = history_card(2019, r"B. Recht, \ R. Roelofs, \ L. Schmidt \& V. Shankar, \ \emph{Do ImageNet classifiers generalize to ImageNet?}",
                          r"at ICML: \ they rebuilt ImageNet's test set from new images, \ following the original collection "
                          r"process as closely as they could; \ every model they tested lost accuracy, \ between 11 and 14 points "
                          r"of top-1 accuracy", color=NAIVEC, width=11.4, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"not overfitting to a reused test set: \ the ranking of models was preserved", font_size=26, color=GREY_A),
            label(r"but a small, \ invisible change in the distribution of images", font_size=26, color=TGTC),
            label(r"a test set is a sample from one distribution; \ deployment is another", font_size=26, color=NAIVEC),
        ), 12.4, 0.35, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2019 Benjamin Recht, Rebecca Roelofs, Ludwig Schmidt and Vaishaal Shankar rebuilt the "
            "test set of ImageNet, the benchmark on which a decade of image classifiers had been compared. They collected new "
            "images, following the original process as closely as they could. Every model they tested lost accuracy, between "
            "eleven and fourteen points. <bookmark mark='b'/> It was not overfitting to a reused test set: the models kept "
            "their order, and improvements on the old test set still carried over. <bookmark mark='c'/> It was a small, "
            "invisible change in the distribution of images. <bookmark mark='d'/> A test set is a sample from one "
            "distribution, and deployment is another."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lesson(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Every guarantee in this course so far assumed the data come from the distribution we "
            "care about. <bookmark mark='b'/> Two things break that. Some of the data may be wrong: corrupted, mislabelled, "
            "planted by an adversary. <bookmark mark='c'/> Or all of the data may be right, but from a different "
            "distribution than the one where the answer will be used. <bookmark mark='d'/> The first is robustness, the "
            "second is distribution shift, and both have a modern theory with exact rates and practical corrections.",
            [(r"\text{so far}", r":", r"\text{data from the distribution of interest}", 40),
             (r"\text{threat 1}", r":", r"\text{a fraction } \varepsilon \text{ of the data are wrong}", 40),
             (r"\text{threat 2}", r":", r"\text{all data right, \ from } P \ne Q", 40),
             (r"\text{answers}", r":", r"\text{robustness; \ shift correction}", 40)],
            [r"the standing assumption", r"contamination", r"shift", r"this part"],
            colors=[(1, BADC), (2, TGTC)])

    def two_threats(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The two threats in symbols. Huber's contamination model: the data come from one minus "
            "epsilon times P plus epsilon times anything. <bookmark mark='b'/> The strong contamination model is harsher: an "
            "adversary who sees the clean sample replaces an epsilon fraction of it with points of its choosing. <bookmark "
            "mark='c'/> Distribution shift: the training data come from P, the target is Q. <bookmark mark='d'/> With no "
            "assumption linking P and Q nothing can be said; with a structured link, such as covariate shift, label shift, or "
            "invariance across environments, a great deal can.",
            [(r"\text{Huber}", r":", r"(1 - \varepsilon)P + \varepsilon\,\text{anything}", 40),
             (r"\text{strong}", r":", r"\text{an adversary edits } \varepsilon n \text{ points}", 40),
             (r"\text{shift}", r":", r"\text{train on } P, \ \text{use on } Q", 40),
             (r"\text{structure}", r":", r"\text{covariate, \ label, \ invariant}", 40)],
            [r"Part 30", r"the adversarial model", r"the deployment gap", r"chapters 5--9"],
            colors=[(1, BADC), (2, TGTC)])

    def covshift_preview(self):
        d = load("covshift")
        self.lad_voiceover(
            f"<bookmark mark='a'/> A preview on real data. The NHANES survey's {d['N']:,} adults have mean systolic pressure "
            f"{say(d['truth'], 1)}. <bookmark mark='b'/> Draw samples of {d['n']} that over-represent the young, as an online "
            f"panel might: their mean age is {d['mean_age_sample']:.0f}, against {d['mean_age_pop']:.0f} in the population. "
            f"<bookmark mark='c'/> The sample mean pressure is about {say(d['mean_u'], 1)}, and its ninety-five percent interval "
            f"contains the truth in {100 * d['cov_u']:.0f} percent of {d['reps']} samples. <bookmark mark='d'/> Reweighting by "
            f"estimated importance weights recovers {say(d['mean_w'], 1)}, and covers {100 * d['cov_w']:.1f} percent of the "
            f"time: chapter five's method.",
            [(r"\text{NHANES}", r":", rf"\text{{mean SBP}} = {d['truth']:.1f}, \ \ N = {d['N']:,}", 38),
             (r"\text{a young sample}", r":", rf"\text{{mean age }} {d['mean_age_sample']:.0f} \ \text{{vs}} \ {d['mean_age_pop']:.0f}", 38),
             (r"\text{unweighted}", r":", rf"{d['mean_u']:.1f}; \ \text{{covers }} {100 * d['cov_u']:.0f}\%", 38),
             (r"\text{importance-weighted}", r":", rf"{d['mean_w']:.1f}; \ \text{{covers }} {100 * d['cov_w']:.1f}\%", 38)],
            [r"the population", r"an online panel", r"confidently wrong", r"chapter 5"],
            colors=[(2, NAIVEC), (3, FIXC)])

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("shifted sample", "importance-weighted"),
                   f"<bookmark mark='a'/> On the Board: the ordinary interval from the young-skewed sample covers the "
                   f"population's mean pressure {100 * br[0]['achieved']:.0f} percent of the time: broken. <bookmark mark='b'/> "
                   f"The importance-weighted interval covers {100 * br[1]['achieved']:.1f} percent: kept.", [("a", [0]), ("b", [1])])

    def taxonomy(self):
        self.list_voiceover(
            "<bookmark mark='a'/> The plan. <bookmark mark='b'/> Chapters one to four: robustness, from Tukey's depth to "
            "efficient filters, list decoding, and heavy tails. <bookmark mark='c'/> Chapters five and six: covariate shift "
            "and label shift, each with a correction and its price. <bookmark mark='d'/> Chapters seven to nine: protecting "
            "against shifts one cannot name, by robust optimization, invariance, and transfer. <bookmark mark='e'/> And "
            "chapter ten: detecting that a shift has happened at all.",
            [(r"the plan:", GREY_A),
             (r"1--4: \ depth, \ filtering, \ list decoding, \ heavy tails", DEPTHC),
             (r"5--6: \ covariate shift, \ label shift", TGTC),
             (r"7--9: \ DRO, \ invariance, \ transfer", FIXC),
             (r"10: \ detecting shift", SRCC)])

    def upgrade(self):
        cards = [
            upgrade_card(30, r"robust estimators of location and scale, \ in one dimension", r"low dimension; \ Huber's contamination",
                         r"chapters 1--4: \ robustness in many dimensions, \ efficiently"),
            upgrade_card(57, r"weighted conformal under a known shift", r"the weights are known",
                         r"chapters 5--6: \ estimated weights, \ and their price"),
        ]
        VGroup(*cards).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Two promises come due. Part thirty built robust estimators of location and scale in one "
            "dimension; chapters one to four take robustness into many dimensions, with algorithms that run in polynomial "
            "time. <bookmark mark='b'/> Part fifty-seven's weighted conformal assumed the shift's weights were known; "
            "chapters five and six estimate them, and count the price."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 60", font_size=34, color=GREY_B), label(r"Robustness and Distribution Shift", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Tukey's depth; \ efficient robust means in high dimensions; \ list decoding; \ heavy tails",
            r"covariate shift on NHANES; \ label shift on the biopsies; \ their Board rows",
            r"distributionally robust optimization; \ invariance and anchor regression; \ transfer",
            r"detecting shift; \ open problems",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 30, \ 51, \ 57").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.shift}, \ the depth map").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part sixty: robustness and distribution shift. <bookmark mark='b'/> Tukey's depth, efficient "
            "robust means in high dimensions, list decoding and heavy tails; covariate shift on NHANES and label shift on the "
            "breast cancer biopsies; distributionally robust optimization, invariance and anchor regression, and transfer "
            "learning; detecting shift; and open problems."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()

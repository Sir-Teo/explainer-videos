from __future__ import annotations

import numpy as np

from videos.stats.stats64.common import *  # noqa: F403


class Holdout(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter five. Adaptive reuse of test sets, and how to keep a holdout honest.", 5,
                            r"Reusing the test set", r"Every look is a query")
        self.problem()
        self.experiment()
        self.chart()
        self.thresholdout_()
        self.ladder()
        self.contamination()

    def problem(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A test set is meant to be used once. In practice, the same public test set is used to "
            "compare thousands of models, and each new model is designed knowing how the last one scored. <bookmark "
            "mark='b'/> Every decision informed by the test score is a query to the test set. <bookmark mark='c'/> After "
            "enough adaptive queries, the test score measures how well the field has fitted that particular test set, "
            "not the population. Part twenty-eight's model selection, at the scale of a research community. <bookmark "
            "mark='d'/> Cynthia Dwork, Vitaly Feldman, Moritz Hardt, Toniann Pitassi, Omer Reingold and Aaron Roth showed "
            "in 2015, in Science, that differential privacy is the tool that controls it.",
            [(r"\text{a test set}", r":", r"\text{meant to be used once}", 40),
             (r"\text{each decision}", r":", r"\text{a query}", 40),
             (r"\text{adaptive queries}", r":", r"\text{overfit the test set}", 40),
             (r"\text{the fix}", r":", r"\text{answer queries privately}", 40)],
            [r"Part 19", r"adaptivity", r"Part 28 at scale", r"Dwork et al. (2015)"],
            colors=[(2, NAIVEC), (3, HONC)])

    def experiment(self):
        d = load("holdout")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Their experiment, simulated here. <bookmark mark='b'/> {d['d']:,} features and labels "
            f"of pure noise: no classifier can beat fifty percent on new data. <bookmark mark='c'/> The analyst computes "
            f"each feature's correlation with the label on a training set of {d['n']:,}, asks the holdout set for the same "
            f"correlations, keeps the features where the two agree in sign and are both large, and builds a classifier "
            f"from the top k. <bookmark mark='d'/> Then reports the classifier's accuracy on the holdout. Each step is "
            f"reasonable; together they reuse the holdout adaptively.",
            [(r"\text{data}", r":", rf"{d['d']:,} \ \text{{noise features, \ random labels}}".replace(",", "{,}"), 40),
             (r"\text{select}", r":", r"\text{agree on train and holdout}", 40),
             (r"\text{build}", r":", r"\text{sign-vote of the top } k", 40),
             (r"\text{report}", r":", r"\text{holdout accuracy}", 40)],
            [r"truth: 50\%", r"a common workflow", r"a classifier", r"the reused holdout"],
            colors=[(3, NAIVEC)])

    def chart(self):
        d = load("holdout")
        ks = np.log10(d["ks"])
        A = axes([0.9, 2.8], [0.45, 0.68], x_length=7.2, y_length=4.3, xlabel=r"features kept $k$ (log scale)",
                 ylabel=r"reported accuracy, \ mean of 5 runs", xticks=[1, 2], xfmt=lambda v: f"{10 ** v:g}",
                 yticks=[0.5, 0.55, 0.6, 0.65], yfmt=lambda v: f"{100 * v:.0f}\\%", center=[-2.4, 0.2, 0])
        ax = A.ax
        half = DashedLine(ax.c2p(0.9, 0.5), ax.c2p(2.8, 0.5), color=GREY_B, stroke_width=2)

        def line(ys, color, sw=3.5):
            return VGroup(polyline(ax, ks, ys, color, sw), *[Dot(ax.c2p(a, b), radius=0.07, color=color) for a, b in zip(ks, ys)])
        reuse = line(d["reuse"]["holdout"], NAIVEC)
        fresh = line(d["reuse"]["fresh"], WHITE, 2.5)
        thr = line(d["thresholdout"]["holdout"], HONC)
        side = side_groups([
            [(r"grey dashes: \ the truth, \ 50\%", GREY_B)],
            [(rf"red: \ the reused holdout, \ up to {100 * max(d['reuse']['holdout']):.0f}\%", NAIVEC)],
            [(r"white: \ the same classifiers", WHITE), (r"on fresh data", WHITE)],
            [(rf"green: \ Thresholdout, \ {100 * min(d['thresholdout']['holdout']):.0f}--{100 * max(d['thresholdout']['holdout']):.0f}\%", HONC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The truth is fifty percent. <bookmark mark='b'/> The reused holdout reports accuracies "
            f"climbing with k, to {100 * max(d['reuse']['holdout']):.0f} percent: a discovery, apparently. <bookmark "
            f"mark='c'/> On fresh data the same classifiers score fifty percent, as they must. The holdout had been fitted "
            f"through the selection. <bookmark mark='d'/> Answer every query through Thresholdout instead, and the reported "
            f"accuracies stay between {100 * min(d['thresholdout']['holdout']):.0f} and "
            f"{100 * max(d['thresholdout']['holdout']):.0f} percent: much closer to the truth, at the price of noise in each "
            f"answer."
        ) as vo:
            self.play(FadeIn(A), Create(half), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(reuse[0]), FadeIn(VGroup(*reuse[1:])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(fresh[0]), FadeIn(VGroup(*fresh[1:])), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(thr[0]), FadeIn(VGroup(*thr[1:])), FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def thresholdout_(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Thresholdout works like this. <bookmark mark='b'/> Answer each query with the training "
            "set's value, unless it differs from the holdout's value by more than a noisy threshold. <bookmark mark='c'/> "
            "Only then reveal the holdout's value, with Laplace noise added. Most queries reveal nothing about the holdout; "
            "the rest reveal it privately. <bookmark mark='d'/> Because differential privacy composes and is closed under "
            "post-processing, the whole adaptive sequence is private, and private analyses cannot overfit: a model chosen "
            "through private answers generalizes. A holdout of size n can then support roughly n squared adaptive queries, "
            "instead of about n.",
            [(r"\text{if}", r":", r"|v_{\text{train}} - v_{\text{hold}}| < T + \text{noise}, \ \text{return } v_{\text{train}}", 38),
             (r"\text{else}", r":", r"\text{return } v_{\text{hold}} + \mathrm{Laplace}", 40),
             (r"\text{privacy}", r":", r"\text{composition and post-processing}", 40),
             (r"\text{so}", r":", r"\text{privacy implies generalization}", 40)],
            [r"a threshold", r"Part 63's Laplace", r"Part 63", r"Dwork et al. (2015)"],
            colors=[(3, HONC)])

    def ladder(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Competitions have a simpler version. <bookmark mark='b'/> Avrim Blum and Moritz Hardt's "
            "Ladder, in 2015, updates a public leaderboard only when a submission beats the best so far by more than a set "
            "margin, and then rounds the score. <bookmark mark='c'/> Small improvements, which are mostly noise, are not "
            "reported, so the leaderboard leaks little about the test set. <bookmark mark='d'/> They showed that an attacker "
            "can climb an ordinary leaderboard with random submissions, by keeping those that happen to score well, and "
            "that the Ladder stops it.",
            [(r"\text{the Ladder}", r":", r"\text{update only on a clear improvement}", 40),
             (r"\text{and}", r":", r"\text{round the reported score}", 40),
             (r"\text{small gains}", r":", r"\text{not reported}", 40),
             (r"\text{the attack}", r":", r"\text{random submissions, \ kept if lucky}", 40)],
            [r"Blum \& Hardt (2015)", r"less information", r"noise suppressed", r"a boosting attack"],
            colors=[(0, HONC), (3, NAIVEC)])

    def contamination(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The modern form of reuse is worse. <bookmark mark='b'/> Benchmarks are published on the "
            "web, and models are trained on the web, so test questions leak into training data. <bookmark mark='c'/> "
            "Detecting it is Part sixty-three's membership inference, asked of a benchmark: does the model treat these "
            "questions as familiar, more likely than rephrasings of them? <bookmark mark='d'/> The statistical defences are "
            "the classical ones: fresh, private test sets, written after the training data were collected, and rotated "
            "before they leak.",
            [(r"\text{contamination}", r":", r"\text{test questions in training data}", 40),
             (r"\text{detect}", r":", r"\text{membership inference}", 40),
             (r"\text{signal}", r":", r"\text{originals more likely than rephrasings}", 40),
             (r"\text{defence}", r":", r"\text{fresh, \ private, \ rotated tests}", 40)],
            [r"leakage", r"Part 63", r"a test", r"the holdout, \ renewed"],
            colors=[(0, NAIVEC), (3, HONC)])

from __future__ import annotations

import numpy as np

from videos.stats.stats60.common import *  # noqa: F403


class Detect(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter ten. Detecting shift: has the world changed, and does it matter?", 10,
                            r"Detecting shift", r"Two-sample tests in many dimensions", lit=(2012,))
        self.question()
        self.mmd()
        self.chart()
        self.classifier()
        self.power()
        self.harmful()
        self.monitor()

    def question(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Every correction in this part needs to know that a shift happened. Detecting it is a "
            "two-sample test: are the training covariates and the deployment covariates from the same distribution? "
            "<bookmark mark='b'/> In one dimension, Part sixteen's Kolmogorov–Smirnov test answers. <bookmark mark='c'/> In "
            "many, a test must compare whole distributions without estimating their densities. <bookmark mark='d'/> Two "
            "modern answers: compare the distributions' embeddings in a kernel's feature space, or ask whether a classifier "
            "can tell them apart.",
            [(r"H_0", r":", r"P_{\text{train}}(x) = P_{\text{deploy}}(x)", 40),
             (r"\text{one dimension}", r":", r"\text{Kolmogorov--Smirnov}", 40),
             (r"\text{many}", r":", r"\text{no density estimates}", 40),
             (r"\text{two answers}", r":", r"\text{kernel embeddings; \ classifiers}", 40)],
            [r"a two-sample problem", r"Part 16", r"the curse of dimension", r"this chapter"],
            colors=[(3, FIXC)])

    def mmd(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Maximum mean discrepancy compares kernel mean embeddings. <bookmark mark='b'/> For a fixed kernel, within-sample off-diagonal and between-sample averages give an unbiased squared-MMD U statistic, which can be negative. Our pooled, label-invariant bandwidth selection changes this fixed-kernel unbiasedness interpretation. <bookmark mark='c'/> A characteristic kernel separates distinct population laws; consistency also requires a suitable fixed or controlled kernel sequence. <bookmark mark='d'/> Under independent IID samples and the null, pooled labels are exchangeable. A permutation test with conservative handling of ties is level-valid. With three hundred sampled permutations we use the plus-one p-value, whose minimum is one over three hundred and one.",
            [(r"\mathrm{MMD}^2", r"=", r"\|\mu_P - \mu_Q\|^2_{\mathcal H}", 40),
             (r"\widehat{\mathrm{MMD}}{}^2", r"=", r"\overline{k(x, x')} + \overline{k(y, y')} - 2\,\overline{k(x, y)}", 40),
             (r"\text{characteristic } k", r":", r"\mathrm{MMD} = 0 \iff P = Q", 40),
             (r"\text{null}", r":", r"\text{exchangeability + conservative permutation p-values}", 40)],
            [r"Gretton et al. (2012)", r"U-statistics", r"consistent against all", r"Part 16's permutations"],
            colors=[(2, FIXC)])

    def chart(self):
        d = load("detect")
        sh, sm = d["mmd_shift"], d["mmd_same"]
        edges = np.linspace(-0.005, 0.0125, 29)
        A = axes([-0.005, 0.0125], [0, 0.32], x_length=7.4, y_length=4.4, xlabel=r"$\widehat{\mathrm{MMD}}{}^2$ under permutation", ylabel=r"fraction",
                 xticks=[-0.004, 0, 0.004, 0.008, 0.012], yticks=[0, 0.1, 0.2, 0.3], center=[-2.5, 0.2, 0])
        ax = A.ax
        null = np.clip(np.asarray(sh["null"]), -0.005, 0.0125 - 1e-9)
        h = hist_bars(ax, edges, np.histogram(null, edges)[0] / len(null), color=NULLC, opacity=0.5)
        same = DashedLine(ax.c2p(sm["mmd2"], 0), ax.c2p(sm["mmd2"], 0.3), color=GREY_A, stroke_width=2.5)
        arr = Arrow(ax.c2p(0.0095, 0.22), ax.c2p(0.0125, 0.22), color=NAIVEC, buff=0, stroke_width=4)
        arr_l = label(rf"observed {sh['mmd2']:.3f}, \ off the chart", font_size=20, color=NAIVEC).next_to(arr, UP, buff=0.12).align_to(arr, RIGHT)
        side = side_groups([
            [(r"300 young-skewed adults", WHITE), (r"vs \ 300 from the empirical extract", WHITE)],
            [(r"age, \ BMI, \ sex; \ Gaussian kernel", GREY_A)],
            [(r"grey: \ 300 permutations", NULLC)],
            [(r"red: \ the shifted sample", NAIVEC), (rf"$p = {sh['p']:.4f}$, \ the smallest possible", NAIVEC)],
            [(r"dashed: \ two extract samples", GREY_A), (rf"$p = {sm['p']:.2f}$", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> Chapter five's shift, detected. Three hundred adults from the young-skewed sample, against three hundred from the empirical extract, compared on age, body-mass index and sex. <bookmark mark='b'/> The grey bars are the permutation null. <bookmark mark='c'/> The observed statistic, {say(sh['mmd2'], 3)}, is larger than the sampled permutation statistics: a p-value of one over three hundred and one, the smallest three hundred permutations can give. <bookmark mark='d'/> Two independent samples from the empirical extract give a statistic in the middle of the null, with p equal to {say(sm['p'], 2)}: the null is not rejected in this one run. Nonrejection does not prove equality."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"NHANES; \ the selection is simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(h, lag_ratio=0.05), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(GrowArrow(arr), FadeIn(arr_l), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(Create(same), FadeIn(side[4]))
        self.clear_scene()

    def classifier(self):
        d = load("detect")
        self.lad_voiceover(
            "<bookmark mark='a'/> A classifier two-sample test learns to distinguish the groups, then tests independent held-out predictions. <bookmark mark='b'/> With fixed balanced holdout labels, accuracy is not generally an exact binomial proportion. Conditional on the pooled number of positive predictions, the number assigned to the source is hypergeometric under exchangeability. <bookmark mark='c'/> The displayed accuracy and p-value now use that exact conditional randomization law, with the classifier frozen before holdout. <bookmark mark='d'/> Calibrated membership odds, adjusted for the training class proportions and orientation, can also estimate a density ratio. Discrimination accuracy alone does not validate those probabilities.",
            [(r"\text{C2ST}", r":", r"\text{can a classifier tell the samples apart?}", 40),
             (r"H_0", r":", r"U\mid K \sim \mathrm{Hypergeom}(2n,K,n)", 40),
             (r"\text{here}", r":", rf"\text{{accuracy}} = {d['acc']:.2f}, \ \ p = {d['p_acc']:.2g}", 40),
             (r"\text{bonus}", r":", r"\frac{c}{1 - c} \text{ is the density ratio}", 40)],
            [r"Lopez-Paz \& Oquab (2017)", r"a conditional randomization null", r"detected", r"chapter 5's weights"],
            colors=[(2, NAIVEC), (3, FIXC)])

    def harmful(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Detectable covariate change need not increase predictive risk, and a fixed classifier or non-characteristic feature map may miss some changes entirely. <bookmark mark='b'/> Failing Loudly compares detection representations and methods; low-dimensional model outputs often helped on its evaluated shifts, not uniformly on every alternative. <bookmark mark='c'/> Risk increase is a separate, task-relevant null. It usually needs outcome feedback or additional assumptions. <bookmark mark='d'/> Sequential risk monitoring can use anytime-valid methods under the stated bounded-loss or conditional assumptions, with uncertainty in the reference risk accounted for.",
            [(r"\text{any shift}", r":", r"\text{detectability and harmfulness are different}", 40),
             (r"\text{test outputs}", r":", r"\text{outputs can improve power on some shifts}", 40),
             (r"\text{better}", r":", r"H_0: \ R_{\text{deploy}} \le R_{\text{train}} + \epsilon", 40),
             (r"\text{sequentially}", r":", r"\text{anytime-valid risk monitoring}", 40)],
            [r"significance is not importance", r"Rabanser et al. (2019)", r"the harmful-shift test", r"Podkopaev \& Ramdas (2022)"],
            colors=[(2, FIXC)])

    def monitor(self):
        self.list_voiceover(
            "<bookmark mark='a'/> A deployment protocol, assembled from this part and the last two. <bookmark mark='b'/> "
            "Monitor the model's outputs and its error on a trickle of labelled cases, with a confidence sequence. <bookmark "
            "mark='c'/> When the risk rises, test which kind of shift it is: covariates, labels, or the mechanism. <bookmark "
            "mark='d'/> Correct for the kinds that can be corrected, by weights or by label-shift estimation. <bookmark "
            "mark='e'/> And retrain, with transfer from the old data, when the mechanism itself has moved.",
            [(r"a deployment protocol:", GREY_A),
             (r"1. \ monitor outputs and risk, \ anytime-valid \ (Part 58)", SRCC),
             (r"2. \ diagnose: \ covariate, \ label, \ or mechanism?", TGTC),
             (r"3. \ correct: \ importance weights, \ BBSE \ (chapters 5--6)", FIXC),
             (r"4. \ retrain with transfer \ (chapter 9)", DEPTHC)])

    def power(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Detection sample size depends on the alternative, kernel and distribution. <bookmark mark='b'/> For a fixed bounded kernel and balanced samples, the unbiased squared-MMD statistic is order one over n under the null. Its alternative variance and local structure also affect power. <bookmark mark='c'/> Our empirical statistic is large compared with the sampled permutation null. The null scale alone does not justify a universal inverse-effect sample-size law, or extrapolation to a shift a hundred times subtler. <bookmark mark='d'/> Kernel learning can improve power, but it must use independent data or be incorporated into the randomization scheme to preserve validity.",
            [(r"\text{null}", r":", r"\widehat{\mathrm{MMD}}{}^2 = O_p(1/n)", 40),
             (r"\text{detectable}", r":", r"\text{power also depends on alternative variance}", 40),
             (r"\text{here}", r":", r"\widehat{\mathrm{MMD}}^2 \text{ large vs permutation null},\ n=300", 40),
             (r"\text{power}", r":", r"\text{choose the kernel on held-out data}", 40)],
            [r"a degenerate U-statistic", r"a sample-size rule", r"easily detected", r"Liu et al. (2020)"],
            colors=[(1, FIXC)])

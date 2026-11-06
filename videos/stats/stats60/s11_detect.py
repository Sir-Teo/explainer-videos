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
            "<bookmark mark='a'/> Arthur Gretton and co-authors' maximum mean discrepancy, in 2012. A kernel, such as the "
            "Gaussian, maps each distribution to its mean in a feature space. <bookmark mark='b'/> The squared distance "
            "between the two means has an unbiased estimate from within-sample and between-sample kernel averages. <bookmark "
            "mark='c'/> For a characteristic kernel, the distance is zero only if the distributions are equal, so the test "
            "is consistent against every alternative. <bookmark mark='d'/> Its null distribution comes from permuting the "
            "pooled sample, so the test is exact at any sample size.",
            [(r"\mathrm{MMD}^2", r"=", r"\|\mu_P - \mu_Q\|^2_{\mathcal H}", 40),
             (r"\widehat{\mathrm{MMD}}{}^2", r"=", r"\overline{k(x, x')} + \overline{k(y, y')} - 2\,\overline{k(x, y)}", 40),
             (r"\text{characteristic } k", r":", r"\mathrm{MMD} = 0 \iff P = Q", 40),
             (r"\text{null}", r":", r"\text{permutations: \ exact}", 40)],
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
            [(r"300 young-skewed adults", WHITE), (r"vs \ 300 from the population", WHITE)],
            [(r"age, \ BMI, \ sex; \ Gaussian kernel", GREY_A)],
            [(r"grey: \ 300 permutations", NULLC)],
            [(r"red: \ the shifted sample", NAIVEC), (rf"$p = {sh['p']:.4f}$, \ the smallest possible", NAIVEC)],
            [(r"dashed: \ two population samples", GREY_A), (rf"$p = {sm['p']:.2f}$", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> Chapter five's shift, detected. Three hundred adults from the young-skewed sample, against "
            f"three hundred from the population, compared on age, body-mass index and sex. <bookmark mark='b'/> The grey bars "
            f"are the permutation null. <bookmark mark='c'/> The observed statistic, {say(sh['mmd2'], 3)}, is ten times "
            f"larger than any permutation: a p-value of one over three hundred and one, the smallest three hundred "
            f"permutations can give. <bookmark mark='d'/> Two independent samples from the population give a statistic in the "
            f"middle of the null, with p equal to {say(sm['p'], 2)}: no shift, correctly."
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
            f"<bookmark mark='a'/> The second answer, from David Lopez-Paz and Maxime Oquab in 2017: train a classifier to "
            f"tell the two samples apart, and test its accuracy on held-out points. <bookmark mark='b'/> Under no shift, the "
            f"held-out accuracy is a binomial proportion around one half. <bookmark mark='c'/> Here a logistic classifier, "
            f"trained on half of each sample, is right on {100 * d['acc']:.0f} percent of the other half, a p-value of about "
            f"one in ten million. <bookmark mark='d'/> The classifier does double duty: its probabilities are chapter five's "
            f"importance weights. The test that detects the shift also estimates its correction.",
            [(r"\text{C2ST}", r":", r"\text{can a classifier tell the samples apart?}", 40),
             (r"H_0", r":", r"\text{held-out accuracy} \sim \mathrm{Bin}(m, \tfrac12)/m", 40),
             (r"\text{here}", r":", rf"\text{{accuracy}} = {d['acc']:.2f}, \ \ p \approx 10^{{-7}}", 40),
             (r"\text{bonus}", r":", r"\frac{c}{1 - c} \text{ is the density ratio}", 40)],
            [r"Lopez-Paz \& Oquab (2017)", r"a coin's null", r"detected", r"chapter 5's weights"],
            colors=[(2, NAIVEC), (3, FIXC)])

    def harmful(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> With enough data, every deployment shift is detectable, and most do not matter. <bookmark "
            "mark='b'/> Stephan Rabanser, Stephan Günnemann and Zachary Lipton's 2019 comparison, Failing Loudly, found "
            "that testing a model's low-dimensional outputs, such as its predicted class proportions, works better than "
            "testing raw inputs. <bookmark mark='c'/> Better still, ask the question that matters: has the model's risk "
            "increased? <bookmark mark='d'/> Aleksandr Podkopaev and Aaditya Ramdas built sequential tests of exactly that, "
            "for harmful shifts only, with the anytime-valid guarantees of Part fifty-eight.",
            [(r"\text{any shift}", r":", r"\text{always detectable, \ often harmless}", 40),
             (r"\text{test outputs}", r":", r"\text{predicted labels beat raw inputs}", 40),
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
            "<bookmark mark='a'/> How many points does detection need? <bookmark mark='b'/> The unbiased MMD estimate "
            "fluctuates by order one over n under the null, so a shift whose population MMD squared is delta is found once n "
            "is of order one over delta. <bookmark mark='c'/> Here delta was about a tenth, and three hundred points per "
            "sample were plenty; a shift a hundred times subtler would need tens of thousands. <bookmark mark='d'/> The "
            "kernel's bandwidth matters as much as n: choosing it, or learning a deep kernel, on held-out data is how "
            "modern tests gain power, as Feng Liu and co-authors showed in 2020.",
            [(r"\text{null}", r":", r"\widehat{\mathrm{MMD}}{}^2 = O_p(1/n)", 40),
             (r"\text{detectable}", r":", r"\mathrm{MMD}^2 \gg 1/n", 40),
             (r"\text{here}", r":", r"\mathrm{MMD}^2 \approx 0.1, \ \ n = 300", 40),
             (r"\text{power}", r":", r"\text{choose the kernel on held-out data}", 40)],
            [r"a degenerate U-statistic", r"a sample-size rule", r"easily detected", r"Liu et al. (2020)"],
            colors=[(1, FIXC)])

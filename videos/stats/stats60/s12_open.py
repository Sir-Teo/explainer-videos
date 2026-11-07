from __future__ import annotations

from videos.stats.stats60.common import *  # noqa: F403


class OpenProblems(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter eleven. Open problems in robustness and distribution shift.", 11, r"Open problems",
                            r"Where the guarantees stop")
        self.map_()
        self.op_gaps()
        self.op_which()
        self.op_radius()
        self.op_deep()
        self.op_inference()
        self.problems()

    def map_(self):
        hdr = [r"threat", r"assumption", r"method", r"guarantee"]
        body = [
            [r"$\varepsilon$ of the data adversarial", r"isotropic Gaussian", r"exact depth / certified algorithms", r"$O(\varepsilon)+$ sampling term"],
            [r"most data adversarial", r"$\alpha$ inliers, bounded covariance", r"list decoding", r"a list, \ $O(1/\sqrt\alpha)$"],
            [r"heavy tails", r"two moments", r"median of means", r"sub-Gaussian width"],
            [r"covariate shift", r"$P(y \mid x)$ fixed, \ overlap", r"importance weights", r"valid variance + ratio conditions"],
            [r"label shift", r"$P(x \mid y)$ fixed", r"BBSE, \ EM", r"consistent prevalence"],
            [r"unknown shift", r"$Q$ in a ball", r"DRO", r"a risk certificate"],
            [r"interventions", r"causal structure", r"ICP, \ anchors", r"robust to anchor shifts"],
        ]
        cols = [GREY_B, BADC, BADC, DEPTHC, TGTC, TGTC, FIXC, FIXC]
        tab = table_rows([hdr] + body, font_size=24, col_buff=0.6, row_buff=0.28, colors=cols).move_to([0, 0.1, 0])
        if tab.width > 13.4:
            tab.width = 13.4
        heading = label(r"Robustness and shift: assumptions, methods and guarantees", font_size=36).move_to([0, 3.3, 0])
        if heading.width > 12.6:
            heading.width = 12.6
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The part in one table: each threat, the assumption that tames it, the method, and what it "
            "guarantees. <bookmark mark='b'/> A small adversarial fraction, against Gaussian inliers: depth and the filter, "
            "with error free of the dimension. A majority of adversarial points: a list. Heavy tails: median of means. "
            "Covariate shift, with the conditional law fixed and overlap: importance weights. Label shift: BBSE and EM. An "
            "unknown shift in a ball: distributionally robust optimization. And interventions on a causal system: invariance "
            "and anchors."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[1:]], lag_ratio=0.6), run_time=18.0)
        self.wait(1.0)
        self.clear_scene()

    def op_gaps(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Computational gaps are model-specific. <bookmark mark='b'/> For isotropic Gaussian means, information-theoretic contamination error is order epsilon. Strong or total-variation corruption has statistical-query and related restricted-model evidence for a larger efficient-error scale. Huber mixtures instead admit order-epsilon polynomial algorithms, including the 2023 almost-linear-time result. <bookmark mark='c'/> Sparse means, covariance estimation and mixtures have different gaps, assumptions and reductions. Restricted-model lower bounds are not unconditional lower bounds for every polynomial algorithm. <bookmark mark='d'/> Pinning down which gaps follow from standard complexity assumptions remains an active question.",
            [(r"\text{problem 1}", r":", r"\text{statistical-computational gaps}", 40),
             (r"\text{Gaussian mean}", r":", r"\text{Huber } O(\varepsilon);\ \text{strong corruption: SQ barrier}", 36),
             (r"\text{harder problems}", r":", r"\text{gaps only in restricted models}", 40),
             (r"\text{open}", r":", r"\text{which gaps are real}", 40)],
            [r"computation as a resource", r"Diakonikolas, \ Kane \& Stewart (2017)", r"sparse, \ covariance, \ mixtures", r"Part 59's hard phase, \ again"],
            colors=[(3, NAIVEC)])

    def op_which(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Which shift happened? <bookmark mark='b'/> Unlabelled target covariates do not in general distinguish covariate shift, label shift and outcome-mechanism changes. These models impose different assumptions, which can overlap in special cases. <bookmark mark='c'/> Real shifts can combine several changes. ImageNetV2 alone does not identify which conditional mechanism changed. <bookmark mark='d'/> Identification and sharp risk bounds require a specified model, labels, multiple environments or other information; many formulations remain open.",
            [(r"\text{problem 2}", r":", r"\text{identifying the kind of shift}", 40),
             (r"\text{covariate vs label}", r":", r"\text{different, generally untestable without labels}", 40),
             (r"\text{real shifts}", r":", r"\text{mixtures, \ plus a changed mechanism}", 40),
             (r"\text{open}", r":", r"\text{identification, \ or sharp bounds}", 40)],
            [r"the modelling question", r"chapters 5--6", r"the hook", r"Part 37's Manski bounds"],
            colors=[(3, NAIVEC)])

    def op_radius(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The uncertainty set is the essential modeling choice. <bookmark mark='b'/> A risk bound is useful only when the target is actually in that set. <bookmark mark='c'/> Ordinary random-split validation evaluates the same distribution and cannot certify protection from an arbitrary unseen shift. Environment-held-out validation and theoretically calibrated radii can still help under suitable assumptions. <bookmark mark='d'/> Learning useful future-environment sets from limited environments, domain knowledge or drift models remains an active problem.",
            [(r"\text{problem 3}", r":", r"\text{choosing the uncertainty set}", 40),
             (r"\text{radius}", r":", r"\text{usually a guess}", 40),
             (r"\text{cross-validation}", r":", r"\text{validates the wrong distribution}", 40),
             (r"\text{open}", r":", r"\text{sets learned from past environments}", 40)],
            [r"DRO's weak point", r"chapter 7", r"a circularity", r"meta-distributional"],
            colors=[(3, NAIVEC)])

    def op_deep(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem four: robustness at scale. <bookmark mark='b'/> The WILDS benchmark of Pang Wei "
            "Koh and co-authors, in 2021, collected real shifts, across hospitals, cameras and countries, and found large "
            "gaps between in-distribution and out-of-distribution accuracy that no method closed. <bookmark mark='c'/> One "
            "regularity, found by John Miller and co-authors that year: across many models, out-of-distribution accuracy is "
            "close to a linear function of in-distribution accuracy, on a probit scale. <bookmark mark='d'/> A theory of "
            "why, and of which training choices move models off that line, is open, and is Part sixty-four's question.",
            [(r"\text{problem 4}", r":", r"\text{robustness of large models}", 40),
             (r"\text{WILDS}", r":", r"\text{real shifts, \ persistent gaps}", 40),
             (r"\text{accuracy on the line}", r":", r"\Phi^{-1}(\text{OOD}) \approx a + b\,\Phi^{-1}(\text{ID})", 40),
             (r"\text{open}", r":", r"\text{why, \ and how to beat the line}", 40)],
            [r"beyond linear models", r"Koh et al. (2021)", r"Miller et al. (2021)", r"Part 64"],
            colors=[(3, NAIVEC)])

    def op_inference(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Inference under shift needs more than point estimation. <bookmark mark='b'/> Our low-dimensional example includes ratio-fit and reference-sample uncertainty, but its observed coverage is a finite Monte Carlo result under a correctly specified logistic ratio. It is not a guarantee for arbitrary estimated weights. <bookmark mark='c'/> Doubly robust estimation, balance and weighted conformal each require their own support, fitting and error-rate assumptions. <bookmark mark='d'/> Honest inference in high dimensions and under weak overlap requires careful formulation of the estimand and what can be identified.",
            [(r"\text{problem 5}", r":", r"\text{inference under shift}", 40),
             (r"\text{high dimensions}", r":", r"\text{extreme weights, \ small } n_{\text{eff}}", 40),
             (r"\text{partial tools}", r":", r"\text{doubly robust, \ balancing, \ conformal}", 40),
             (r"\text{open}", r":", r"\text{honest intervals with weak overlap}", 40)],
            [r"beyond point predictions", r"chapter 5's price", r"Parts 41 and 57", r"Part 62's overlap problem"],
            colors=[(3, NAIVEC)])

    def problems(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Five open problems. <bookmark mark='b'/> Which statistical-computational gaps in robust "
            "estimation are real. <bookmark mark='c'/> Identifying the kind of shift, or bounding its damage. <bookmark "
            "mark='d'/> Principled uncertainty sets. <bookmark mark='e'/> A theory of robustness for large models. "
            "<bookmark mark='f'/> And honest inference under estimated shift.",
            [(r"Open problems", S.ACCENT),
             (r"1. \ statistical-computational gaps in robust estimation", WHITE),
             (r"2. \ identifying the kind of shift, \ or sharp bounds", WHITE),
             (r"3. \ principled uncertainty sets for DRO", WHITE),
             (r"4. \ robustness and the accuracy line for large models", WHITE),
             (r"5. \ honest inference under estimated shift", WHITE)],
            buff=0.42, font_size=25, head_size=40)

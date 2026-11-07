from __future__ import annotations

from videos.stats.stats59.common import *  # noqa: F403


class OpenProblems(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter ten. Open problems in high-dimensional asymptotics.", 10, r"Open problems",
                            r"Where the exact theory stops")
        self.map_()
        self.op_hard()
        self.op_design()
        self.op_features()
        self.op_finite()
        self.op_uncertainty()
        self.problems()

    def map_(self):
        hdr = [r"question", r"tool", r"answer"]
        body = [
            [r"logistic MLE and LRT", r"leave-one-out, \ AMP", r"bias $\alpha_\star$, \ factor $\kappa\sigma_\star^2/\lambda_\star$"],
            [r"spectra, \ traces of inverses", r"Stieltjes, \ free convolution", r"MP law, \ ridge risk"],
            [r"ridgeless, \ double descent", r"random matrices", r"exact curve, \ peak at $\gamma = 1$"],
            [r"M-estimators", r"two-equation systems", r"rankings reverse"],
            [r"the lasso", r"AMP, \ CGMT", r"state evolution's fixed point"],
            [r"Bayes-optimal error", r"replicas, \ interpolation", r"MMSE; \ hard phases"],
        ]
        cols = [GREY_B, PROPC, SIMC, SIMC, CLASSC, AMPC, AMPC]
        tab = table_rows([hdr] + body, font_size=28, col_buff=0.8, row_buff=0.3, colors=cols).move_to([0, 0.1, 0])
        with self.voiceover(
            (
            "<bookmark mark='a'/> The part in one table. <bookmark mark='b'/> The logistic MLE and its test, by "
            'leave-one-out and message passing: a bias and a rescaling factor. Spectra and traces of inverses, by '
            "Stieltjes transforms and free convolution. Ridgeless regression's exact double-descent curve. "
            "M-estimators, whose rankings reverse. The lasso's exact error, by AMP and Gordon's comparison. And the "
            'Bayes-optimal error, by replicas, with its hard phases.'
        )
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[1:]], lag_ratio=0.6), run_time=16.0)
        self.wait(1.0)
        self.clear_scene()

    def op_hard(self):
        heading = label('A specified statistical-computational gap', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Problem one: the hard phase. <bookmark mark='b'/> In sparse regression, planted "
            'clique and tensor problems, the replica method finds regions where the information to estimate is '
            "present but AMP does not reach it. <bookmark mark='c'/> Restricted models of computation, low-degree "
            'polynomials and statistical query algorithms, fail there too, which is evidence that no efficient '
            "algorithm succeeds. <bookmark mark='d'/> A proof that no polynomial-time algorithm can, under a "
            'standard complexity assumption, is open.'
        ),
            [(r"\text{problem 1}", r":", r"\text{the hard phase}", 40),
             (r"\text{known}", r":", r"\text{information present, \ AMP fails}", 40),
             (r"\text{evidence}", r":", r"\text{low-degree and SQ lower bounds}", 40),
             (r"\text{open}", r":", r"\text{a proof of computational hardness}", 40)],
            [r"statistical-computational gaps", r"chapter 7", r"restricted models", r"Part 50's planted clique"],
            colors=[(3, CLASSC)])

    def op_design(self):
        heading = label('Which design structure remains untreated?', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Another direction is realistic design structure. <bookmark mark='b'/> "
            'Independent-entry universality and arbitrary-covariance Gaussian logistic results already exist, with '
            "specific hypotheses. <bookmark mark='c'/> The biopsy exercise is a fixed-design semi-synthetic stress "
            'test with a finite-fit selection step; its predictor slope is not a coverage validation. <bookmark '
            "mark='d'/> An open question should specify the heavy tails, dependence, structure or nuisance "
            'estimation that remains untreated. A broad assertion that all correlated or structured designs are '
            'unsolved would ignore substantial theory.'
        ),
            [(r"\text{problem 2}", r":", r"\text{realistic designs}", 40),
             (r"\text{known}", r":", r"\text{universality; \ correlated Gaussians}", 40),
             (r"\text{chapter 9}", r":", r"\text{a semi-synthetic stress test, \ not coverage validation}", 40),
             (r"\text{open}", r":", r"\text{heavy-tailed, \ structured designs}", 40)],
            [r"beyond Gaussian", r"partial answers", r"the semi-synthetic test", r"what practice needs"],
            colors=[(3, CLASSC)])

    def op_features(self):
        heading = label('Learning features beyond a frozen layer', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Problem three: learning features. <bookmark mark='b'/> Random features and "
            "kernels are lazy: the first layer never moves. <bookmark mark='c'/> Trained neural networks learn "
            'their features, and the proportional theory of that regime, for even two-layer networks trained by '
            "gradient descent, is only beginning. <bookmark mark='d'/> Exact asymptotics for feature learning, and "
            "inference for its outputs, are open, and are Part sixty-four's frontier."
        ),
            [(r"\text{problem 3}", r":", r"\text{feature learning}", 40),
             (r"\text{known}", r":", r"\text{the lazy regime: \ random features, \ kernels}", 40),
             (r"\text{but}", r":", r"\text{trained networks move their features}", 40),
             (r"\text{open}", r":", r"\text{exact asymptotics for trained networks}", 40)],
            [r"beyond chapter 8", r"Mei \& Montanari", r"a moving target", r"Part 64"],
            colors=[(3, AMPC)])

    def op_finite(self):
        heading = label('Quantifying finite-sample approximation error', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Problem four: how large is large? <bookmark mark='b'/> The predictions are "
            'limits, and at two thousand dimensions chapter five showed close agreement in one numerical example, '
            "not a uniform finite-sample accuracy guarantee. <bookmark mark='c'/> Non-asymptotic versions exist for "
            "convex problems through Gordon's comparison, and for AMP over a growing number of iterations, but with "
            "conservative constants. <bookmark mark='d'/> Sharp finite-sample corrections, so that a practitioner "
            'with n of a few hundred knows how much to trust the formulas, are open.'
        ),
            [(r"\text{problem 4}", r":", r"\text{finite-sample accuracy}", 40),
             (r"\text{observed}", r":", r"\text{one illustrative agreement at }p=2{,}000", 40),
             (r"\text{known}", r":", r"\text{non-asymptotic CGMT and AMP, \ loose constants}", 40),
             (r"\text{open}", r":", r"\text{sharp corrections at } n \text{ of a few hundred}", 40)],
            [r"limits, \ not numbers", r"chapter 5", r"partial", r"what users need"],
            colors=[(3, CLASSC)])

    def op_uncertainty(self):
        heading = label('Inference targets and existing theory', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Uncertainty quantification remains an active research direction. <bookmark "
            "mark='b'/> Exact limiting risk formulas are point predictions in a specified asymptotic model, rather "
            'than exact finite-sample error bars. Cross-validation variability, bootstrap validity and '
            "post-selection inference each have existing positive and negative results. <bookmark mark='c'/> "
            'Selective and conformal procedures already cover several high-dimensional settings. A meaningful new '
            'project should identify a combination of assumptions and goals that those results do not address. '
            "<bookmark mark='d'/> The practical target is a usable guarantee with a clearly defined estimand, "
            'sampling model, selection rule and approximation error.'
        ),
            [(r"\text{problem 5}", r":", r"\text{uncertainty quantification}", 40),
             (r"\text{unsettled}", r":", r"\text{CV variability, \ bootstraps, \ selection}", 40),
             (r"\text{natural}", r":", r"\text{join with Parts 56 and 57}", 40),
             (r"\text{open}", r":", r"\text{a full inference toolkit for } p \asymp n", 40)],
            [r"beyond point predictions", r"chapter 9's warnings", r"selective and conformal", r"the practical goal"],
            colors=[(3, PROPC)])

    def problems(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> Five open problems. <bookmark mark='b'/> A proof of computational hardness in the "
            "hard phase. <bookmark mark='c'/> Exact theory for realistic, correlated and structured designs. "
            "<bookmark mark='d'/> The proportional asymptotics of feature learning. <bookmark mark='e'/> Sharp "
            "finite-sample corrections. <bookmark mark='f'/> And a full toolkit for inference when p grows with n."
        ),
            [(r"Open problems", S.ACCENT),
             (r"1. \ computational hardness in the hard phase", WHITE),
             (r"2. \ realistic, \ correlated and structured designs", WHITE),
             (r"3. \ feature learning in trained networks", WHITE),
             (r"4. \ sharp finite-sample corrections", WHITE),
             (r"5. \ a full inference toolkit when $p \asymp n$", WHITE)],
            buff=0.42, font_size=25, head_size=40)

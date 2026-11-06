from __future__ import annotations

from videos.stats.stats61.common import *  # noqa: F403


class OpenProblems(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter ten. Open problems in optimal transport for statistics.", 10, r"Open problems",
                            r"Where the transport theory stops")
        self.map_()
        self.op_curse()
        self.op_inference()
        self.op_ranks()
        self.op_sampling()
        self.op_generative()
        self.problems()

    def map_(self):
        hdr = [r"object", r"estimator", r"rate or guarantee"]
        body = [
            [r"$W_p$ between laws", r"plug-in, \ exact assignment", r"$n^{-1/d}$: \ cursed"],
            [r"entropic cost, \ $S_\varepsilon$", r"Sinkhorn", r"$n^{-1/2}$, \ constant $\propto e^{c/\varepsilon}$"],
            [r"the Brenier map", r"empirical, \ entropic", r"$n^{-2\alpha/(2\alpha - 2 + d)}$"],
            [r"barycenters", r"quantile averages; \ fixed points", r"explicit in 1D and for Gaussians"],
            [r"ranks and quantiles", r"assignment to a grid", r"exactly distribution-free tests"],
            [r"sampling", r"Langevin as a flow of KL", r"$e^{-2t/C_{\mathrm{LS}}}$"],
            [r"generation", r"flow matching", r"straight with OT pairs"],
        ]
        cols = [GREY_B, NAIVEC2, ENTC, PLANC, TGT, PLANC, FLOWC, FLOWC]
        tab = table_rows([hdr] + body, font_size=26, col_buff=0.7, row_buff=0.28, colors=cols).move_to([0, 0.1, 0])
        if tab.width > 13.4:
            tab.width = 13.4
        with self.voiceover(
            "<bookmark mark='a'/> The part in one table. <bookmark mark='b'/> The Wasserstein distance by its plug-in, cursed "
            "at n to the minus one over d. The entropic cost by Sinkhorn, at the parametric rate with a constant that "
            "explodes as epsilon shrinks. The Brenier map, at the rate of nonparametric regression. Barycenters, explicit on "
            "the line and for Gaussians. Ranks and quantiles, with exactly distribution-free tests. Sampling, as a gradient "
            "flow of the divergence. And generation, by flows made straight by transport."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[1:]], lag_ratio=0.6), run_time=18.0)
        self.wait(1.0)
        self.clear_scene()

    def op_curse(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem one: what to estimate instead. <bookmark mark='b'/> The curse can be escaped by "
            "smoothing, entropic or kernel; by slicing, averaging one-dimensional distances over random directions; or by "
            "projecting onto the few directions where the laws differ most. <bookmark mark='c'/> Jonathan Niles-Weed and "
            "Philippe Rigollet's spiked transport model, in 2022, showed that a low-dimensional difference can be estimated "
            "fast in principle, and gave evidence that no efficient algorithm achieves it. <bookmark mark='d'/> Which "
            "surrogate keeps the geometry that matters, with rates and algorithms that match, is open.",
            [(r"\text{problem 1}", r":", r"\text{surrogates for } W_p", 40),
             (r"\text{routes}", r":", r"\text{smooth, \ slice, \ project}", 40),
             (r"\text{spiked transport}", r":", r"\text{fast statistically, \ maybe not computationally}", 38),
             (r"\text{open}", r":", r"\text{the right surrogate, \ with matching rates}", 40)],
            [r"the curse", r"sliced and max-sliced $W$", r"Niles-Weed \& Rigollet (2022)", r"a statistical-computational gap"],
            colors=[(3, NAIVEC2)])

    def op_inference(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem two: inference. <bookmark mark='b'/> On the line, chapter three's limit theorems "
            "give confidence intervals for the distance. For entropic transport, central limit theorems now hold in any "
            "dimension, from del Barrio, González-Sanz, Loubes and Niles-Weed among others. <bookmark mark='c'/> For the "
            "unregularized distance and the map in two or more dimensions, the fluctuations are known only around the "
            "plug-in's own expectation, and once d is five or more its bias is of a larger order. <bookmark mark='d'/> Honest confidence sets for "
            "the Wasserstein distance, and confidence bands for transport maps, in several dimensions are open.",
            [(r"\text{problem 2}", r":", r"\text{confidence statements}", 40),
             (r"\text{known}", r":", r"d = 1; \ \text{entropic, \ any } d", 40),
             (r"\text{gap}", r":", r"\text{the bias exceeds the fluctuation for } d \ge 5", 40),
             (r"\text{open}", r":", r"\text{intervals for } W_p, \ \text{bands for maps}", 40)],
            [r"beyond estimation", r"del Barrio et al.", r"del Barrio \& Loubes (2019)", r"Part 47's question"],
            colors=[(3, NAIVEC2)])

    def op_ranks(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem three: ranks at scale, and beyond testing. <bookmark mark='b'/> The exact "
            "assignment costs n cubed; entropic ranks are faster but lose exact distribution-freeness. <bookmark mark='c'/> "
            "Vector quantile regression, from Guillaume Carlier, Victor Chernozhukov and Alfred Galichon, extends "
            "conditional quantiles to vector outcomes, with open questions about estimation rates and inference. <bookmark "
            "mark='d'/> A full multivariate rank-based toolkit, with efficient tests, regression and confidence regions that "
            "scale to large n, is open.",
            [(r"\text{problem 3}", r":", r"\text{multivariate ranks at scale}", 40),
             (r"\text{cost}", r":", r"O(n^3) \text{ exact; \ entropic: \ fast, \ not exact}", 40),
             (r"\text{regression}", r":", r"\text{vector quantile regression}", 40),
             (r"\text{open}", r":", r"\text{an efficient, \ scalable rank toolkit}", 40)],
            [r"chapter 7", r"a trade-off", r"Carlier, \ Chernozhukov \& Galichon (2016)", r"Part 16, \ in $\mathbb R^d$"],
            colors=[(3, NAIVEC2)])

    def op_sampling(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem four: the complexity of sampling. <bookmark mark='b'/> For strongly log-concave "
            "targets, upper bounds on the number of gradient queries are sharp in some regimes; Sinho Chewi and co-authors "
            "proved the first matching lower bounds in low dimension. <bookmark mark='c'/> For general targets, with "
            "several modes, sampling can be exponentially hard, and the useful middle ground is not mapped. <bookmark "
            "mark='d'/> The query complexity of sampling, as complete as that of convex optimization, is open: see Chewi's "
            "book on log-concave sampling.",
            [(r"\text{problem 4}", r":", r"\text{how many gradient queries?}", 40),
             (r"\text{log-concave}", r":", r"\text{upper bounds; \ some lower bounds}", 40),
             (r"\text{multimodal}", r":", r"\text{exponentially hard in general}", 40),
             (r"\text{open}", r":", r"\text{a complexity theory like optimization's}", 40)],
            [r"chapter 8", r"Chewi et al.", r"metastability", r"Chewi, \ \emph{Log-Concave Sampling}"],
            colors=[(3, NAIVEC2)])

    def op_generative(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem five: the statistics of generative models. <bookmark mark='b'/> A flow fitted "
            "perfectly to the training sample reproduces the training points: the empirical law is the minimizer. <bookmark "
            "mark='c'/> Nicholas Carlini and co-authors extracted near copies of training images from a diffusion model in "
            "2023. Yet trained models also generalize, producing new, plausible samples. <bookmark mark='d'/> When a "
            "learned flow generalizes rather than memorizes, and how to measure the distance between its samples and the "
            "true law in high dimension, are open, and are Part sixty-four's questions.",
            [(r"\text{problem 5}", r":", r"\text{generalization of generative models}", 40),
             (r"\text{the optimum}", r":", r"\text{the empirical law: \ memorization}", 40),
             (r"\text{observed}", r":", r"\text{some copying, \ much generalization}", 40),
             (r"\text{open}", r":", r"\text{when, \ and how to measure it}", 40)],
            [r"chapter 9", r"the plug-in's fixed point", r"Carlini et al. (2023)", r"Part 64"],
            colors=[(3, NAIVEC2)])

    def problems(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Five open problems. <bookmark mark='b'/> The right surrogate for the Wasserstein distance. "
            "<bookmark mark='c'/> Confidence statements for distances and maps in several dimensions. <bookmark mark='d'/> "
            "Multivariate ranks at scale. <bookmark mark='e'/> The query complexity of sampling. <bookmark mark='f'/> And "
            "when generative models generalize.",
            [(r"Open problems", S.ACCENT),
             (r"1. \ the right surrogate for $W_p$", WHITE),
             (r"2. \ intervals for distances, \ bands for maps, \ $d \ge 2$", WHITE),
             (r"3. \ multivariate ranks at scale", WHITE),
             (r"4. \ the complexity of sampling", WHITE),
             (r"5. \ generalization in generative models", WHITE)],
            buff=0.42, font_size=25, head_size=40)

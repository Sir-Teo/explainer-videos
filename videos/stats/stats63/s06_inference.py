from __future__ import annotations

import numpy as np

from videos.stats.stats63.common import *  # noqa: F403


class Inference(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter five. Private inference: confidence intervals and tests that survive the noise.", 5,
                            r"Private inference", r"Intervals that know about the noise")
        self.problem()
        self.aware()
        self.chart()
        self.board()
        self.beyond()
        self.tests()
        self.public()

    def problem(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> An analyst receives a privatized count, say the number of people in a survey with some "
            "condition, released with Laplace noise. <bookmark mark='b'/> The usual next step is the Wald interval of Part "
            "eleven, the estimate plus or minus 1.96 standard errors, as if the noisy count were the real one. <bookmark "
            "mark='c'/> But the released proportion has two sources of error, sampling and privacy noise, and the Wald "
            "interval accounts for only the first. <bookmark mark='d'/> When the privacy noise is comparable to the "
            "sampling noise, the interval is too short, and its coverage falls below ninety-five percent.",
            [(r"\text{release}", r":", r"\tilde c = c + \mathrm{Lap}(1/\varepsilon)", 40),
             (r"\text{naive}", r":", r"\tilde p \pm 1.96\sqrt{\tilde p(1 - \tilde p)/n}", 40),
             (r"\text{errors}", r":", r"\text{sampling} + \text{privacy noise}", 40),
             (r"\text{when comparable}", r":", r"\text{under-coverage}", 40)],
            [r"a noisy count", r"Part 11's Wald", r"two sources", r"the problem"],
            colors=[(1, BADC)])

    def aware(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The cure is to treat the noise as part of the data-generating process, because its "
            "distribution is published. <bookmark mark='b'/> The variance of the noisy proportion is the sampling variance "
            "plus two over n epsilon, squared. <bookmark mark='c'/> A noise-aware interval uses both. <bookmark mark='d'/> "
            "Vishesh Karwa and Salil Vadhan gave finite-sample private intervals for a normal mean in 2018. More general "
            "recipes include a parametric bootstrap that simulates both the sampling and the privacy noise, studied by "
            "Cecilia Ferrando, Shufan Wang and Daniel Sheldon, and Bayesian inference with the noise in the likelihood.",
            [(r"\text{known noise}", r":", r"\text{part of the model}", 40),
             (r"\mathrm{Var}(\tilde p)", r"=", r"\frac{p(1 - p)}{n} + \frac{2}{(n\varepsilon)^2}", 40),
             (r"\text{noise-aware}", r":", r"\tilde p \pm 1.96\sqrt{\tilde p(1 - \tilde p)/n + 2/(n\varepsilon)^2}", 38),
             (r"\text{general}", r":", r"\text{parametric bootstrap; \ Bayes}", 40)],
            [r"published noise", r"two terms", r"both terms", r"Karwa \& Vadhan (2018); \ Ferrando et al. (2022)"],
            colors=[(2, OKC)])

    def chart(self):
        d = load("inference")
        g = d["grid"]
        ns = sorted({r["n"] for r in g})
        lx = np.log10(ns)
        A = axes([1.9, 3.6], [0.5, 1.0], x_length=7.2, y_length=4.4, xlabel=r"sample size $n$ (log scale)",
                 ylabel=r"coverage of the 95\% interval, \ 1{,}000 runs", xticks=list(np.log10([100, 300, 1000, 3000])),
                 xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yticks=[0.5, 0.75, 0.95], yfmt=lambda v: f"{100 * v:.0f}\\%",
                 center=[-2.4, 0.2, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(1.9, 0.95), ax.c2p(3.6, 0.95), color=GREY_B, stroke_width=2)

        def line(eps, key, color, dash=False):
            ys = [next(r[key] for r in g if r["n"] == n and r["eps"] == eps) for n in ns]
            pl = polyline(ax, lx, ys, color, 3.5)
            if dash:
                pl = DashedVMobject(pl, num_dashes=24)
            return VGroup(pl, *[Dot(ax.c2p(a, b), radius=0.07, color=color) for a, b in zip(lx, ys)]), ys
        n1, yn1 = line(0.1, "naive", BADC)
        a1, ya1 = line(0.1, "aware", OKC)
        n5, yn5 = line(0.5, "naive", BADC, True)
        side = side_groups([
            [(r"a Laplace-noised count, \ $p = 0.3$", WHITE), (r"grey dashes: \ 95\%", GREY_B)],
            [(r"red: \ naive Wald, \ $\varepsilon = 0.1$", BADC), (rf"{100 * yn1[0]:.1f}\% at $n = 100$", BADC)],
            [(r"red dashes: \ naive, \ $\varepsilon = 0.5$", BADC), (r"close: \ noise is small", BADC)],
            [(r"green: \ noise-aware, \ $\varepsilon = 0.1$", OKC), (rf"{100 * min(ya1):.1f}\% to {100 * max(ya1):.1f}\%", OKC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> A simulation: a true proportion of 0.3, a Laplace-noised count, and a thousand runs at "
            f"each sample size and budget. <bookmark mark='b'/> At epsilon of a tenth, the naive interval covers only "
            f"{100 * yn1[0]:.0f} percent of the time with a hundred people, and {100 * yn1[2]:.0f} percent with a thousand. "
            f"The privacy noise has standard deviation fourteen counts, against a sampling standard deviation of about "
            f"four and a half at n of a hundred. <bookmark mark='c'/> At epsilon of a half, the noise is five times smaller, "
            f"and the naive interval nearly works. <bookmark mark='d'/> The noise-aware interval covers between "
            f"{100 * min(ya1):.0f} and {100 * max(ya1):.0f} percent everywhere."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(n1[0]), FadeIn(VGroup(*n1[1:])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(n5[0]), FadeIn(VGroup(*n5[1:])), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(a1[0]), FadeIn(VGroup(*a1[1:])), FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def board(self):
        q = load("inference")
        show_board(self, board_rows("DP-noised", "noise-aware"),
                   f"<bookmark mark='a'/> On the Board, at a thousand people and epsilon of a tenth, over "
                   f"{q['board_reps']:,} runs: the Wald interval that ignores the privacy noise covers "
                   f"{100 * q['board_naive']:.1f} percent of the time: broken. <bookmark mark='b'/> The noise-aware interval "
                   f"covers {100 * q['board_aware']:.1f} percent: kept.", [("a", [0]), ("b", [1])])

    def beyond(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Two subtleties, both familiar. <bookmark mark='b'/> The released proportion can be "
            "negative, or above one, and clipping it to the unit interval is free post-processing for privacy but biases it, "
            "the census problem of the next chapter. <bookmark mark='c'/> And when the data are clipped before release, to "
            "bound the sensitivity of a mean of unbounded values, the clipping introduces a bias the analyst must also model. "
            "Clip too tightly and the bias dominates; too loosely and the noise does. <bookmark mark='d'/> The best clipping "
            "level is a bias-variance trade-off, Part nine's oldest lesson, with the privacy budget in it.",
            [(r"\text{clip the output}", r":", r"\text{free for privacy, \ biased}", 40),
             (r"\text{clip the inputs}", r":", r"\text{bounded sensitivity, \ biased}", 40),
             (r"\text{too tight / too loose}", r":", r"\text{bias / noise}", 40),
             (r"\text{choose}", r":", r"\text{bias-variance, \ with } \varepsilon", 40)],
            [r"post-processing bias", r"sensitivity's price", r"the trade-off", r"Part 9"],
            colors=[(1, BADC)])

    def tests(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Tests behave the same way. <bookmark mark='b'/> A chi-squared test of independence on a "
            "noisy contingency table, computed as if the counts were exact, rejects a true null far more often than five "
            "percent, because the noise looks like dependence. Marco Gaboardi and coauthors showed this in 2016, and "
            "corrected the reference distribution. <bookmark mark='c'/> Jordan Awan and Aleksandra Slavkovic found in 2018 "
            "the uniformly most powerful private test for a binomial proportion, by a privacy-constrained version of the "
            "Neyman-Pearson lemma. <bookmark mark='d'/> Its rejection probability is a smooth function of the count, a "
            "randomized test of Part forty-six: the privacy requirement forces the randomization.",
            [(r"\text{naive } \chi^2", r":", r"\text{too many rejections}", 40),
             (r"\text{corrected}", r":", r"\text{simulate the noisy null}", 40),
             (r"\text{UMP DP test}", r":", r"\text{a private Neyman--Pearson lemma}", 40),
             (r"\phi(x)", r":", r"\text{smooth in } x \ \text{(randomized)}", 40)],
            [r"noise looks like dependence", r"Gaboardi et al. (2016)", r"Awan \& Slavkovi\'c (2018)", r"Part 46"],
            colors=[(0, BADC), (1, OKC)])

    def public(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The deeper point. <bookmark mark='b'/> Older disclosure methods, swapping records between "
            "places or suppressing small cells, were kept secret, because knowing them helped the attacker. <bookmark "
            "mark='c'/> So analysts could not correct for them, and their effect on inference was unknowable. <bookmark "
            "mark='d'/> Differential privacy's noise can be published in full, mechanism and parameters, without weakening "
            "the guarantee. For the first time, a statistical agency's confidentiality protection can be modelled exactly by "
            "its users.",
            [(r"\text{swapping, \ suppression}", r":", r"\text{secret methods}", 40),
             (r"\text{so}", r":", r"\text{uncorrectable bias}", 40),
             (r"\text{DP}", r":", r"\text{published noise}", 40),
             (r"\text{result}", r":", r"\text{inference can model it}", 40)],
            [r"the old way", r"unknowable effects", r"transparency", r"a first"],
            colors=[(2, OKC), (3, OKC)])

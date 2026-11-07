from __future__ import annotations

import numpy as np

from videos.stats.stats61.common import *  # noqa: F403


class Rates(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter three. Empirical rates: how fast does a sample approach its law, in Wasserstein distance?", 3,
                            r"Empirical rates", r"The curse of dimensionality", lit=(1969,))
        self.question()
        self.chart()
        self.why()
        self.intrinsic()
        self.sliced()
        self.one_d()
        self.consequences()

    def question(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Empirical Wasserstein error depends on the order, geometry and tails. Our main rate example concerns W one on bounded regular distributions. <bookmark mark='b'/> On a line, root-n expected W-one error needs a tail-integrability condition; finite first moment alone does not ensure it. <bookmark mark='c'/> For full-dimensional bounded regular laws in dimension at least three, the empirical W-one rate is n to the minus one over d. The critical dimension two has logarithmic effects. <bookmark mark='d'/> Fournier and Guillin give nonasymptotic moment-dependent bounds. Smooth density alone does not remove the empirical measure's quantization barrier, but these are not unconditional two-sided rates for every absolutely continuous law.",
            [(r"\text{question}", r":", r"E\,W_1(\hat\mu_n, \mu) \ \text{as } n \to \infty", 40),
             (r"d = 1", r":", r"\asymp n^{-1/2}", 40),
             (r"d \ge 3", r":", r"\asymp n^{-1/d}", 40),
             (r"\text{sharp}", r":", r"\text{requires moment, support and regularity assumptions}", 40)],
            [r"the plug-in", r"parametric", r"Dudley (1969)", r"Fournier \& Guillin (2015)"],
            colors=[(2, NAIVEC2)])

    def chart(self):
        d = load("rates")
        keys = [("d1", 1, SRC), ("d2", 2, FLOWC), ("d3", 3, PLANC), ("d5", 5, TGT), ("d10", 10, NAIVEC2)]
        A = axes([1.3, 3.3], [-2.1, 0.1], x_length=7.4, y_length=4.4, xlabel=r"sample size $n$ (log scale)", ylabel=r"$E\,W_1$ between two samples",
                 xticks=[np.log10(v) for v in (25, 100, 400, 1600)], xfmt=lambda v: f"{10 ** v:.0f}",
                 yticks=[np.log10(v) for v in (0.01, 0.03, 0.1, 0.3, 1)], yfmt=lambda v: f"{10 ** v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        lines = []
        for k, dd, c in keys:
            ns, W = np.asarray(d[k]["ns"], float), np.asarray(d[k]["W"], float)
            xs, ys = np.log10(ns), np.log10(W)
            lines.append(VGroup(polyline(ax, xs, ys, c, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=c) for a, b in zip(xs, ys)]))
        side = side_groups([
            [(r"two samples from the uniform cube", WHITE), (r"exact assignment", GREY_A)],
            [(rf"$d = 1$: \ slope {d['d1']['slope']:.2f}", SRC), (rf"$d = 2$: \ {d['d2']['slope']:.2f}", FLOWC)],
            [(rf"$d = 3$: \ {d['d3']['slope']:.2f}", PLANC), (rf"$d = 5$: \ {d['d5']['slope']:.2f}", TGT), (rf"$d = 10$: \ {d['d10']['slope']:.2f}", NAIVEC2)],
            [(r"theory: \ $-\tfrac12$, \ $-\tfrac12$ (log), \ $-\tfrac1d$", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> Two independent samples from the uniform distribution on the cube, matched exactly by the "
            f"assignment algorithm, for n from twenty-five to sixteen hundred. <bookmark mark='b'/> On a line, the distance "
            f"falls with slope {say(d['d1']['slope'], 2)} on the log-log scale: one over root n. In the plane, "
            f"{say(d['d2']['slope'], 2)}, the root n rate with a logarithm. <bookmark mark='c'/> In three dimensions the slope "
            f"is {say(d['d3']['slope'], 2)}, in five {say(d['d5']['slope'], 2)}, in ten {say(d['d10']['slope'], 2)}: close to minus "
            f"one over d. <bookmark mark='d'/> In ten dimensions, halving the error takes about a thousand times more data."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ assignments exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(*[Create(l) for l in lines[2:]], FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def why(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Why one over d? <bookmark mark='b'/> n points in a d-dimensional cube sit at typical "
            "distance n to the minus one over d from their nearest neighbours. <bookmark mark='c'/> Matching two independent "
            "samples moves each point at least to a near neighbour of the other sample, so the cost is at least of that "
            "order. <bookmark mark='d'/> The upper bound partitions the cube dyadically and matches mass level by level: a "
            "chaining argument, like Part forty-eight's.",
            [(r"\text{spacing}", r"\asymp", r"n^{-1/d}", 40),
             (r"\text{lower bound}", r":", r"\text{expected nearest-neighbor displacement has this scale}", 40),
             (r"\text{upper bound}", r":", r"\text{dyadic partitions, \ level by level}", 40),
             (r"\text{so}", r":", r"E W_1(\hat\mu_n, \mu) \asymp n^{-1/d}\quad(d\ge3,\ \text{regular cube model})", 40)],
            [r"nearest neighbours", r"no escape", r"Part 48's chaining", r"the curse"],
            colors=[(3, NAIVEC2)])

    def intrinsic(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Intrinsic geometry can improve empirical rates under precise covering and mass conditions, as studied by Weed and Bach. <bookmark mark='b'/> Exact low-dimensional support and noisy concentration near a manifold are different: fixed full-dimensional noise can change the eventual rate, even if smaller samples show a lower-dimensional regime. <bookmark mark='c'/> Smoothness can help suitably smoothed estimators, while the raw empirical measure still has discrete-support error. <bookmark mark='d'/> Lower-complexity adaptation for estimating a transport cost between distinct laws holds under specified cost and support assumptions. It is not a universal rule that the smaller raw dimension always governs every Wasserstein problem.",
            [(r"\text{intrinsic dim } k", r":", r"n^{-1/k}", 40),
             (r"\text{images}", r":", r"\text{low-dimensional, \ in high ambient dimension}", 38),
             (r"\text{smoothness}", r":", r"\text{helps smoothed estimators}", 40),
             (r"W(\hat\mu_n, \hat\nu_n)", r":", r"\text{lower-complexity adaptation under cost/support conditions}", 40)],
            [r"Weed \& Bach (2019)", r"manifold data", r"Niles-Weed \& Berthet (2022)", r"lower complexity adaptation"],
            colors=[(0, PLANC)])

    def one_d(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> One-dimensional asymptotic distributions also need tail and smoothness conditions. <bookmark mark='b'/> Away from equality, squared-W-two estimates can have a nondegenerate normal limit under suitable quantile regularity. With independent samples of sizes n and m, the natural scale uses n m over n plus m, and the variance combines both samples. <bookmark mark='c'/> At equality, this effective size times squared W two can converge to a weighted squared-Brownian-bridge integral when the integral is finite. For one empirical sample against a known law, the scale is n instead. <bookmark mark='d'/> Bootstrap validity depends on the functional, centering and null regime; an off-null theorem should not be reused at equality without checking it.",
            [(r"\mu \ne \nu", r":", r"\sqrt{n_{\rm eff}}\,(\widehat{W}_2^2 - W_2^2) \Rightarrow N(0, \sigma^2)", 40),
             (r"\mu = \nu", r":", r"n_{\rm eff}\widehat{W}_2^2 \Rightarrow \int_0^1 B(u)^2/f(F^{-1}(u))^2\,du", 38),
             (r"\text{like}", r":", r"\text{Cram\'er--von Mises}", 40),
             (r"\text{bootstrap}", r":", r"\text{validity depends on centering and the null regime}", 40)],
            [r"del Barrio et al.", r"a Brownian bridge", r"Part 48", r"Part 47's boundaries"],
            colors=[(0, PLANC)])

    def consequences(self):
        self.list_voiceover(
            "<bookmark mark='a'/> These rates inform method choice. <bookmark mark='b'/> High-dimensional Wasserstein testing can have poor power for some alternatives, but a simple large mean shift can still be easy to detect. <bookmark mark='c'/> An empirical-centered DRO ball needs a radius calibrated for its order, tail assumptions, confidence and effective dimension. For the displayed regular high-dimensional regime, this includes an n-to-minus-one-over-d scale. <bookmark mark='d'/> Smoothing, slicing and projection are useful alternatives. Each changes the estimand or the detectable geometry and requires its own rate statement.",
            [(r"in practice:", GREY_A),
             (r"Wasserstein two-sample tests: \ weak in high dimension", NAIVEC2),
             (r"Wasserstein DRO: \ a radius of order $n^{-1/d}$", TGT),
             (r"so: \ smooth, \ slice, \ or project \ (chapter 4)", ENTC)])

    def sliced(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Sliced transport compares one-dimensional projections. <bookmark mark='b'/> For each direction, compute the projected Wasserstein distance by sorting, and integrate its p-th power over directions before taking the p-th root. <bookmark mark='c'/> Sorting costs n log n per direction. Dimension-independent rate exponents require tail and order assumptions; a root-n statement for a squared or powered discrepancy is not automatically a root-n rate for every sliced distance itself. Finite directions add integration error. <bookmark mark='d'/> Slicing can dilute differences concentrated in a few directions.",
            [(r"SW_p^p(\mu, \nu)", r"=", r"\int_{S^{d-1}} W_p^p(\theta_\#\mu, \theta_\#\nu)\,d\sigma(\theta)", 40),
             (r"\text{cost}", r":", r"O(n\log n) \text{ per direction}", 40),
             (r"\text{rate}", r":", r"\text{order/tail-dependent; \ finite directions add error}", 40),
             (r"\text{price}", r":", r"\text{differences in few directions are diluted}", 40)],
            [r"Rabin et al. (2011); \ Bonneel et al. (2015)", r"sorting", r"Nadjahi et al. (2020)", r"chapter 10's surrogates"],
            colors=[(2, PLANC)])

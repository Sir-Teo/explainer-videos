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
            "<bookmark mark='a'/> The plug-in estimate of a Wasserstein distance replaces each law by its empirical "
            "distribution. How far is the empirical distribution of n points from the law itself? <bookmark mark='b'/> On a "
            "line, the answer is of order one over root n, the usual parametric rate. <bookmark mark='c'/> In d dimensions, "
            "Richard Dudley showed in 1969 that the answer is of order n to the minus one over d, for d at least three. "
            "<bookmark mark='d'/> Nicolas Fournier and Arnaud Guillin gave sharp non-asymptotic versions in 2015: the rate "
            "cannot be beaten for any law with a density, however smooth.",
            [(r"\text{question}", r":", r"E\,W_1(\hat\mu_n, \mu) \ \text{as } n \to \infty", 40),
             (r"d = 1", r":", r"\asymp n^{-1/2}", 40),
             (r"d \ge 3", r":", r"\asymp n^{-1/d}", 40),
             (r"\text{sharp}", r":", r"\text{for every absolutely continuous } \mu", 40)],
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
             (r"\text{lower bound}", r":", r"\text{every point moves at least that far}", 40),
             (r"\text{upper bound}", r":", r"\text{dyadic partitions, \ level by level}", 40),
             (r"\text{so}", r":", r"W_1(\hat\mu_n, \mu) \asymp n^{-1/d}", 40)],
            [r"nearest neighbours", r"no escape", r"Part 48's chaining", r"the curse"],
            colors=[(3, NAIVEC2)])

    def intrinsic(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The rate depends on the data's intrinsic dimension, not the ambient one. Jonathan Weed and "
            "Francis Bach showed in 2019 that if the law lives near a k-dimensional set, the rate is n to the minus one over "
            "k. <bookmark mark='b'/> Images, which live on low-dimensional manifolds inside huge pixel spaces, are therefore "
            "less cursed than their pixel count suggests. <bookmark mark='c'/> Smoothness of the densities does not help the "
            "plug-in, but it helps smoothed estimators. <bookmark mark='d'/> And the distance between two different laws can "
            "be estimated faster than either law: the error of the plug-in for W between mu and nu is governed by the "
            "smaller of the two dimensions, as Hundrieser, Staudt and Munk showed.",
            [(r"\text{intrinsic dim } k", r":", r"n^{-1/k}", 40),
             (r"\text{images}", r":", r"\text{low-dimensional, \ in high ambient dimension}", 38),
             (r"\text{smoothness}", r":", r"\text{helps smoothed estimators}", 40),
             (r"W(\hat\mu_n, \hat\nu_n)", r":", r"\text{the smaller dimension governs}", 40)],
            [r"Weed \& Bach (2019)", r"manifold data", r"Niles-Weed \& Berthet (2022)", r"lower complexity adaptation"],
            colors=[(0, PLANC)])

    def one_d(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> On the line there is a full distribution theory. <bookmark mark='b'/> For two different "
            "laws, the plug-in W two squared is asymptotically normal at rate root n, with a variance computable from the "
            "quantile functions: Eustasio del Barrio and co-authors, from 1999 on. <bookmark mark='c'/> When the two laws are "
            "equal, the limit is not normal: under conditions on the tails, it is the integral of a squared Brownian bridge, weighted by the density, "
            "the cousin of Part forty-eight's Cramér–von Mises statistic. <bookmark mark='d'/> So the bootstrap works away "
            "from the null and needs care at it, a pattern this course has seen at every boundary.",
            [(r"\mu \ne \nu", r":", r"\sqrt n\,(\widehat{W}_2^2 - W_2^2) \Rightarrow N(0, \sigma^2)", 40),
             (r"\mu = \nu", r":", r"n\widehat{W}_2^2 \Rightarrow \int_0^1 B(u)^2/f(F^{-1}(u))^2\,du", 38),
             (r"\text{like}", r":", r"\text{Cram\'er--von Mises}", 40),
             (r"\text{bootstrap}", r":", r"\text{fine away from the null; \ careful at it}", 40)],
            [r"del Barrio et al.", r"a Brownian bridge", r"Part 48", r"Part 47's boundaries"],
            colors=[(0, PLANC)])

    def consequences(self):
        self.list_voiceover(
            "<bookmark mark='a'/> What the curse means in practice. <bookmark mark='b'/> A Wasserstein two-sample test in "
            "high dimension has little power, unless the laws differ grossly. <bookmark mark='c'/> Distributionally robust "
            "optimization with a Wasserstein ball needs a radius of order n to the minus one over d to contain the truth, "
            "which is large. <bookmark mark='d'/> And any method that needs the distance itself must be smoothed, sliced or "
            "projected: chapter four's entropic transport is the main smoothing.",
            [(r"in practice:", GREY_A),
             (r"Wasserstein two-sample tests: \ weak in high dimension", NAIVEC2),
             (r"Wasserstein DRO: \ a radius of order $n^{-1/d}$", TGT),
             (r"so: \ smooth, \ slice, \ or project \ (chapter 4)", ENTC)])

    def sliced(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The simplest escape from the curse is to slice. <bookmark mark='b'/> Project both laws "
            "onto a random direction, compute the one-dimensional distance by sorting, and average over directions: the "
            "sliced Wasserstein distance of Julien Rabin and co-authors, and Nicolas Bonneel and co-authors. <bookmark "
            "mark='c'/> Each slice costs a sort, n log n, and the plug-in converges at the parametric rate in any "
            "dimension. <bookmark mark='d'/> The price is geometry: slicing sees only one direction at a time, and a "
            "difference hidden in a few directions is diluted by all the others.",
            [(r"SW_p^p(\mu, \nu)", r"=", r"\int_{S^{d-1}} W_p^p(\theta_\#\mu, \theta_\#\nu)\,d\sigma(\theta)", 40),
             (r"\text{cost}", r":", r"O(n\log n) \text{ per direction}", 40),
             (r"\text{rate}", r":", r"n^{-1/2}, \ \text{any } d", 40),
             (r"\text{price}", r":", r"\text{differences in few directions are diluted}", 40)],
            [r"Rabin et al. (2011); \ Bonneel et al. (2015)", r"sorting", r"Nadjahi et al. (2020)", r"chapter 10's surrogates"],
            colors=[(2, PLANC)])

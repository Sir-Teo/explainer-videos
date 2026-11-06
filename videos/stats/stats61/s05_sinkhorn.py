from __future__ import annotations

import numpy as np

from videos.stats.stats61.common import *  # noqa: F403


class Sinkhorn(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter four. Entropic transport and Sinkhorn's algorithm: blur the plan, and everything gets easier.", 4,
                            r"Entropic transport", r"Sinkhorn's algorithm", lit=(2013,))
        self.entropic()
        self.plans()
        self.algorithm()
        self.convergence()
        self.bias()
        self.complexity()
        self.divergence()
        self.unbalanced()

    def entropic(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The linear program costs about n cubed operations, too many for large samples, and its "
            "solution is a sparse vertex that jumps as the data move. <bookmark mark='b'/> Marco Cuturi's 2013 idea: add a "
            "multiple epsilon of the plan's negative entropy to the cost. <bookmark mark='c'/> The problem becomes strictly "
            "convex, and its solution has a closed form up to two vectors: the plan is a Gibbs kernel, e to the minus C over "
            "epsilon, scaled on its rows and columns. <bookmark mark='d'/> As epsilon goes to zero it approaches the "
            "transport plan; as epsilon grows it approaches the independent coupling.",
            [(r"\text{LP}", r":", r"O(n^3), \ \text{a sparse, unstable vertex}", 40),
             (r"\text{entropic}", r":", r"\min_{P \in \Pi(a, b)} \langle P, C\rangle - \varepsilon H(P)", 40),
             (r"P^\varepsilon", r"=", r"\mathrm{diag}(u)\,e^{-C/\varepsilon}\,\mathrm{diag}(v)", 40),
             (r"\varepsilon \to 0", r":", r"\text{OT}; \ \ \varepsilon \to \infty: \ ab'", 40)],
            [r"the cost of exactness", r"Cuturi (2013)", r"a Gibbs kernel, \ scaled", r"the two limits"],
            colors=[(2, ENTC)])

    def plans(self):
        d = load("lp")
        sk = d["sinkhorn"]
        P0 = np.asarray(d["P"])
        cells = [(P0, rf"LP: \ cost {d['cost']:.2f}", PLANC)] + [(np.asarray(sk[k]["P"]), rf"$\varepsilon = {k}$: \ {sk[k]['cost']:.2f}", ENTC) for k in ("0.1", "0.5", "2")]
        grids = VGroup()
        for P, t, c in cells:
            g = TransportFlow.plan(P, cell=0.3, color=c)
            grids.add(VGroup(g, label(t, font_size=22, color=c).next_to(g, DOWN, buff=0.2)))
        grids.arrange(RIGHT, buff=0.55).move_to([0, 0.3, 0])
        head = label(r"chapter 1's six sources and seven targets: \ the plan, \ sharp and blurred", font_size=26).to_edge(UP, buff=0.6)
        with self.voiceover(
            f"<bookmark mark='a'/> Chapter one's small problem again. <bookmark mark='b'/> The linear program's plan is sparse, "
            f"twelve nonzero entries, cost {say(d['cost'], 2)}. <bookmark mark='c'/> With epsilon equal to a tenth, the "
            f"entropic plan has the same shape, slightly blurred, at cost {say(sk['0.1']['cost'], 2)}. <bookmark mark='d'/> At "
            f"one half, the blur spreads, cost {say(sk['0.5']['cost'], 2)}; at two, mass goes almost everywhere, cost "
            f"{say(sk['2']['cost'], 2)}. The entropy trades exactness for smoothness."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(grids[0]))
            vo.wait_until("c")
            self.play(FadeIn(grids[1]))
            vo.wait_until("d")
            self.play(FadeIn(grids[2]), FadeIn(grids[3]), run_time=1.5)
        self.clear_scene()

    def algorithm(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Finding the two scaling vectors is Richard Sinkhorn's matrix-scaling problem, from 1964. "
            "<bookmark mark='b'/> Alternate: rescale the rows to match a, then the columns to match b. <bookmark mark='c'/> "
            "Each step is a matrix-vector product, so an iteration costs n squared operations, and runs well on graphics "
            "processors. <bookmark mark='d'/> For small epsilon the numbers under- and overflow, so practice works with the "
            "logarithms, the dual potentials f and g, and log-sum-exp.",
            [(r"\text{Sinkhorn}", r":", r"u \leftarrow a \,/\, (Kv), \ \ v \leftarrow b \,/\, (K'u), \ \ K = e^{-C/\varepsilon}", 38),
             (r"\text{alternating}", r":", r"\text{rows, \ then columns}", 40),
             (r"\text{cost}", r":", r"O(n^2) \text{ per iteration, \ parallel}", 40),
             (r"\text{stable}", r":", r"f_i = -\varepsilon \log\sum_j b_j e^{(g_j - C_{ij})/\varepsilon}", 40)],
            [r"Sinkhorn (1964)", r"Bregman projections", r"GPUs", r"the log domain"],
            colors=[(0, ENTC)])

    def convergence(self):
        d = load("sinkhorn")
        tr = d["traces"]
        A = axes([0, 3.0], [-9.2, 0.6], x_length=7.4, y_length=4.4, xlabel=r"iteration (log scale)", ylabel=r"marginal error",
                 xticks=[0, 1, 2, 3], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, -3, -6, -9], yfmt=lambda v: rf"10^{{{int(v)}}}",
                 center=[-2.5, 0.2, 0])
        ax = A.ax

        def tline(v, c):
            v = np.maximum(np.asarray(v, float), 1e-12)
            xs = np.log10(np.arange(1, len(v) + 1))
            keep = xs <= 3.0
            return polyline(ax, xs[keep], np.log10(v[keep]), c, 3.5)
        l1, l2 = tline(tr["1"], FLOWC), tline(tr["0.1"], ENTC)
        r1 = [r for r in d["rows"] if r["eps"] == 1.0][0]
        r2 = [r for r in d["rows"] if r["eps"] == 0.1][0]
        r3 = [r for r in d["rows"] if r["eps"] == 0.03][0]
        side = side_groups([
            [(r"60 points to 60 points in the plane", WHITE), (r"stop at error $10^{-9}$", GREY_A)],
            [(rf"$\varepsilon = 1$: \ {r1['iters']} iterations", FLOWC)],
            [(rf"$\varepsilon = 0.1$: \ {r2['iters']} iterations", ENTC)],
            [(rf"$\varepsilon = 0.03$: \ {r3['iters']:,}", GREY_A), (r"iterations grow like $1/\varepsilon$", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> How fast does it converge? Sixty points to sixty points, stopping when the marginals are "
            f"right to ten to the minus nine. <bookmark mark='b'/> With epsilon equal to one, the error falls geometrically: "
            f"{r1['iters']} iterations. <bookmark mark='c'/> With a tenth, {r2['iters']}. <bookmark mark='d'/> With three "
            f"hundredths, {r3['iters']:,}: the contraction rate degrades as epsilon shrinks, roughly like one over epsilon. "
            f"Sharpness is paid for in iterations."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(l2), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def bias(self):
        d = load("sinkhorn")
        rows = d["rows"]
        eps = np.asarray([r["eps"] for r in rows])
        cost = np.asarray([r["cost"] for r in rows])
        A = axes([-1.7, 0.6], [2.8, 5.0], x_length=7.4, y_length=4.4, xlabel=r"$\varepsilon$ (log scale)", ylabel=r"transport cost of the plan",
                 xticks=[np.log10(v) for v in (0.03, 0.1, 0.3, 1, 3)], xfmt=lambda v: f"{10 ** v:g}", yticks=[3, 4, 5], center=[-2.5, 0.2, 0])
        ax = A.ax
        line = VGroup(polyline(ax, np.log10(eps), cost, ENTC, 3.5), *[Dot(ax.c2p(a, b), radius=0.07, color=ENTC) for a, b in zip(np.log10(eps), cost)])
        ex = DashedLine(ax.c2p(-1.7, d["exact"]), ax.c2p(0.6, d["exact"]), color=PLANC, stroke_width=2.5)
        side = side_groups([
            [(rf"green: \ the exact cost, \ {d['exact']:.3f}", PLANC)],
            [(r"purple: \ the entropic plan's cost", ENTC), (rf"{cost[-1]:.3f} at $\varepsilon = 0.03$", ENTC)],
            [(r"bias $\approx \tfrac{d}{2}\,\varepsilon\log(1/\varepsilon)$", GREY_A), (r"for smooth problems", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The price of the blur is bias. The exact transport cost of this problem is "
            f"{say(d['exact'], 3)}. <bookmark mark='b'/> The entropic plan's cost exceeds it, by a lot at epsilon three and by "
            f"little at three hundredths, where it is {say(cost[-1], 3)}. <bookmark mark='c'/> For smooth problems the bias "
            f"is of order epsilon times log one over epsilon, times half the dimension: small, and well understood."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(Create(ex), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def complexity(self):
        d = load("sinkhorn")
        ns = np.asarray(d["ns"], float)
        A = axes([1.3, 2.7], [-0.45, 0.6], x_length=7.4, y_length=4.4, xlabel=r"sample size $n$ (log scale)", ylabel=r"between two samples of one law",
                 xticks=[np.log10(v) for v in (25, 50, 100, 200, 400)], xfmt=lambda v: f"{10 ** v:.0f}",
                 yticks=[np.log10(v) for v in (0.5, 1, 2, 3)], yfmt=lambda v: f"{10 ** v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        xs = np.log10(ns)
        lw = VGroup(polyline(ax, xs, np.log10(d["w2sq"]), NAIVEC2, 3.5), *[Dot(ax.c2p(a, np.log10(b)), radius=0.06, color=NAIVEC2) for a, b in zip(xs, d["w2sq"])])
        ls = VGroup(polyline(ax, xs, np.log10(d["sdiv"]), ENTC, 3.5), *[Dot(ax.c2p(a, np.log10(b)), radius=0.06, color=ENTC) for a, b in zip(xs, d["sdiv"])])
        side = side_groups([
            [(rf"two samples from $N(0, I_{d['d']})$", WHITE)],
            [(r"red: \ $W_2^2$", NAIVEC2), (rf"slope {d['slope_w2']:.2f}; \ theory $-2/d = -0.4$", NAIVEC2)],
            [(r"purple: \ Sinkhorn divergence, \ $\varepsilon = 1$", ENTC), (rf"slope {d['slope_sd']:.2f}", ENTC)],
            [(r"free of $d$: \ $n^{-1/2}$, \ up to constants", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The real payoff is statistical. Two samples from the same five-dimensional Gaussian: any "
            f"distance between them is pure estimation error. <bookmark mark='b'/> The squared W two falls with slope "
            f"{say(d['slope_w2'], 2)}, near the theory's minus two over d: the curse. <bookmark mark='c'/> The Sinkhorn "
            f"divergence, with epsilon one, falls with slope {say(d['slope_sd'], 2)}. <bookmark mark='d'/> Aude Genevay and "
            f"co-authors, and Gonzalo Mena and Jonathan Niles-Weed, proved in 2019 that the entropic cost converges at the "
            f"parametric rate in any dimension, with a constant that grows as epsilon shrinks."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated, \ 6 repetitions")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lw), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(ls), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def divergence(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> One fix makes the entropic cost a proper discrepancy. The entropic cost of a law with "
            "itself is not zero. <bookmark mark='b'/> The Sinkhorn divergence subtracts the two self-terms, so it is zero "
            "when the laws are equal and positive otherwise. <bookmark mark='c'/> It interpolates between Wasserstein, as "
            "epsilon goes to zero, and the maximum mean discrepancy with the kernel minus distance, as epsilon grows: "
            "Feydy and co-authors, 2019. <bookmark mark='d'/> The tuning parameter epsilon now has a meaning: the scale "
            "below which geometry is ignored.",
            [(r"\mathrm{OT}_\varepsilon(\mu, \mu)", r"\ne", r"0", 40),
             (r"S_\varepsilon(\mu, \nu)", r"=", r"\mathrm{OT}_\varepsilon(\mu, \nu) - \tfrac12\mathrm{OT}_\varepsilon(\mu, \mu) - \tfrac12\mathrm{OT}_\varepsilon(\nu, \nu)", 34),
             (r"\varepsilon \to 0", r":", r"W; \ \ \varepsilon \to \infty: \ \mathrm{MMD}, \ k = -\|x - y\|", 40),
             (r"\varepsilon", r":", r"\text{the scale below which geometry is ignored}", 38)],
            [r"a bias", r"Genevay et al.; \ Feydy et al.", r"Part 60's MMD", r"a resolution"],
            colors=[(1, ENTC)])

    def unbalanced(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> One more relaxation is often needed. <bookmark mark='b'/> Transport demands that all mass "
            "be moved, so an outlier must be carried, at great cost, wherever it lies; and two measures of different total "
            "mass cannot be compared at all. <bookmark mark='c'/> Unbalanced transport replaces the hard marginal "
            "constraints by penalties, a Kullback–Leibler divergence from each marginal, so mass can be created or destroyed "
            "at a price. <bookmark mark='d'/> Lénaïc Chizat, Gabriel Peyré, Bernhard Schmitzer and François-Xavier "
            "Vialard showed in 2018 that Sinkhorn's algorithm extends with one change: each scaling is raised to a power.",
            [(r"\text{balanced}", r":", r"\text{all mass moves; \ outliers dominate}", 40),
             (r"\text{unbalanced}", r":", r"\min_P \langle P, C\rangle + \tau\,\mathrm{KL}(P\mathbf 1\,\|\,a) + \tau\,\mathrm{KL}(P'\mathbf 1\,\|\,b)", 34),
             (r"\text{effect}", r":", r"\text{mass created or destroyed, \ at a price}", 40),
             (r"\text{Sinkhorn}", r":", r"u \leftarrow \big(a/Kv\big)^{\tau/(\tau + \varepsilon)}", 40)],
            [r"Part 60's outliers", r"soft marginals", r"robust transport", r"Chizat et al. (2018)"],
            colors=[(1, ENTC)])

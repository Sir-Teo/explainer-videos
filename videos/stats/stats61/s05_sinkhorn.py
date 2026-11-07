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
            "<bookmark mark='a'/> Entropic regularization smooths the finite transport optimization problem. Dense assignment has a cubic reference complexity, though exact transport has several algorithms. <bookmark mark='b'/> Our solver minimizes transport cost plus epsilon times KL of the plan relative to the product marginals. For fixed marginals this differs from cost minus epsilon entropy only by a constant, so the minimizer is the same. <bookmark mark='c'/> With positive marginals and finite costs the entropic minimizer is unique and is a row-and-column scaling of the Gibbs kernel. <bookmark mark='d'/> As epsilon vanishes it selects an optimal unregularized plan; as epsilon grows the plan tends to the independent coupling. We distinguish its raw transport cost from its regularized objective.",
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
            [(rf"$\varepsilon = 0.03$: \ {r3['iters']:,}", GREY_A), (r"small $\varepsilon$ slows convergence; \ no universal inverse law", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> How fast does it converge? Sixty points to sixty points, stopping when the marginals are "
            f"right to ten to the minus nine. <bookmark mark='b'/> With epsilon equal to one, the error falls geometrically: "
            f"{r1['iters']} iterations. <bookmark mark='c'/> With a tenth, {r2['iters']}. <bookmark mark='d'/> With three "
            f"hundredths, {r3['iters']:,}: the contraction rate degrades as epsilon shrinks, in a way that depends on costs, marginals and the stopping tolerance. "
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
            [(r"raw plan cost $\ne$ regularized-value bias", GREY_A), (r"finite discrete and continuous expansions differ", GREY_A)],
        ])
        with self.voiceover(
            "<bookmark mark='a'/> The graph shows the raw transport cost of the entropic plan, rather than the entropy-regularized objective. <bookmark mark='b'/> Its excess over the exact discrete optimum decreases as regularization shrinks, with numerical marginal residuals checked. <bookmark mark='c'/> Continuous small-epsilon expansions of the regularized value can have an epsilon-log-one-over-epsilon leading term. That coefficient is not a formula for this finite discrete raw-cost graph. Discrete gaps and continuous smoothness lead to different bias regimes."
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
            [(r"fixed-$\varepsilon$ rate bounds need tail/support conditions", GREY_A)],
        ])
        with self.voiceover(
            "<bookmark mark='a'/> This graph compares two independent empirical samples from the same five-dimensional Gaussian. The population discrepancy is zero. <bookmark mark='b'/> The finite-sample squared-W-two values show a dimension-dependent matching regime. <bookmark mark='c'/> The fixed-epsilon Sinkhorn divergence decreases more quickly over these five sizes and six replicates. Draws and Monte Carlo standard errors are saved; a fitted slope is not a proved asymptotic exponent. <bookmark mark='d'/> Root-n statistical bounds and central limit results exist for fixed regularization under suitable support or tail assumptions. Their constants depend on dimension, tails and epsilon; a zero-discrepancy null can be degenerate and have a different fluctuation scale."
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
        heading = label(r"Debiasing the regularized transport objective", font_size=36).move_to([0, 3.3, 0])
        if heading.width > 12.6:
            heading.width = 12.6
        self.add(heading)
        self.lad_voiceover(
            "<bookmark mark='a'/> The regularized objective need not vanish for a law against itself. <bookmark mark='b'/> Subtracting the two self-objectives gives the Sinkhorn divergence. Its positivity and separation properties require an appropriate cost and kernel, such as the finite-epsilon squared-Euclidean setup here. <bookmark mark='c'/> In our squared-distance convention, the zero-epsilon limit is squared W two. As epsilon grows without bound, the discrepancy tends to squared distance between means, which need not distinguish different laws. With ordinary distance cost the corresponding independent-coupling limit is an energy-distance expression. <bookmark mark='d'/> Thus cost and regularization convention both matter; finite epsilon controls the amount of smoothing.",
            [(r"\mathrm{OT}_\varepsilon(\mu, \mu)", r"\ne", r"0", 40),
             (r"S_\varepsilon(\mu, \nu)", r"=", r"\mathrm{OT}_\varepsilon(\mu, \nu) - \tfrac12\mathrm{OT}_\varepsilon(\mu, \mu) - \tfrac12\mathrm{OT}_\varepsilon(\nu, \nu)", 34),
             (r"\varepsilon \to 0", r":", r"W_2^2; \ \ \varepsilon \to \infty:\ \|E X-E Y\|^2\quad(c=\|x-y\|^2)", 40),
             (r"\varepsilon", r":", r"\text{the scale below which geometry is ignored}", 38)],
            [r"a bias", r"Genevay et al.; \ Feydy et al.", r"Part 60's MMD", r"a resolution"],
            colors=[(1, ENTC)])

    def unbalanced(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Unbalanced transport relaxes mass conservation. <bookmark mark='b'/> Balanced couplings need equal total mass and can pay heavily for distant outliers. <bookmark mark='c'/> Generalized KL penalties for marginal mismatch allow mass creation or destruction, at a price. Adding an entropic plan penalty yields the regularized problem shown. <bookmark mark='d'/> Generalized Sinkhorn updates then raise the marginal rescaling to a power involving both the KL penalty and epsilon. The entropy term is needed for this update; it is not an algorithm for the unregularized expression with epsilon absent.",
            [(r"\text{balanced}", r":", r"\text{all mass moves; \ outliers dominate}", 40),
             (r"\text{unbalanced}", r":", r"\min_{P\ge0} \langle P,C\rangle + \varepsilon\sum_{ij}P_{ij}(\log P_{ij}-1)+\tau\,\mathrm{KL}(P\mathbf 1\,\|\,a) + \tau\,\mathrm{KL}(P'\mathbf 1\,\|\,b)", 34),
             (r"\text{effect}", r":", r"\text{mass created or destroyed, \ at a price}", 40),
             (r"\text{Sinkhorn}", r":", r"u \leftarrow \big(a/Kv\big)^{\tau/(\tau + \varepsilon)}", 40)],
            [r"Part 60's outliers", r"soft marginals", r"robust transport", r"Chizat et al. (2018)"],
            colors=[(1, ENTC)])

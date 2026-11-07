from __future__ import annotations

import numpy as np

from videos.stats.stats61.common import *  # noqa: F403


class Duality(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter one. Kantorovich duality: the transport problem, its prices, and its solution on a line.", 1,
                            r"Kantorovich duality", r"Plans and prices", lit=(1942,))
        self.couplings()
        self.plan_chart()
        self.dual()
        self.prices()
        self.algorithms()
        self.line()
        self.brenier()

    def couplings(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> For discrete distributions, with weights a on n source points and b on m target points, a "
            "coupling is a matrix P with nonnegative entries. <bookmark mark='b'/> Its rows sum to a: every source point "
            "sends all its mass. Its columns sum to b: every target receives what it needs. <bookmark mark='c'/> The cost of "
            "the plan is the sum of P i j times C i j, the cost of moving one unit from i to j. <bookmark mark='d'/> The "
            "set of couplings is a polytope, the transport polytope, and a linear function on it is minimized at a vertex.",
            [(r"P", r"\in", r"\mathbb R_+^{n \times m}", 40),
             (r"P\mathbf 1 = a", r",", r"P'\mathbf 1 = b", 40),
             (r"\text{cost}", r"=", r"\langle P, C\rangle = \sum_{ij} P_{ij}C_{ij}", 40),
             (r"\Pi(a, b)", r":", r"\text{a polytope; \ optimum at a vertex}", 40)],
            [r"a plan", r"the marginals", r"linear", r"Part 21's simplex"],
            colors=[(2, PLANC)])

    def plan_chart(self):
        d = load("lp")
        X, Y, a, b, P = (np.asarray(d[k]) for k in ("X", "Y", "a", "b", "P"))
        A = axes([-2.2, 5.0], [-2.6, 2.8], x_length=6.0, y_length=4.6, xlabel=r"", ylabel=r"", center=[-3.3, -0.2, 0])
        ax = A.ax
        src = VGroup(*[Dot(ax.c2p(*x), radius=0.06 + 0.5 * w, color=SRC) for x, w in zip(X, a)])
        tgt = VGroup(*[Dot(ax.c2p(*y), radius=0.06 + 0.5 * w, color=TGT) for y, w in zip(Y, b)])
        mx = P.max()
        flows = VGroup(*[Line(ax.c2p(*X[i]), ax.c2p(*Y[j]), color=PLANC, stroke_width=1 + 10 * P[i, j] / mx, stroke_opacity=0.8)
                         for i in range(len(X)) for j in range(len(Y)) if P[i, j] > 1e-9])
        grid = TransportFlow.plan(P, cell=0.42, color=PLANC).move_to([3.6, 0.2, 0])
        gl = label(r"the plan $P$: \ 6 sources $\times$ 7 targets", font_size=22).next_to(grid, UP, buff=0.25)
        side = side_groups([
            [(rf"LP optimum: \ cost {d['cost']:.3f}", PLANC)],
            [(rf"{d['nonzero']} nonzero entries", WHITE), (r"$= n + m - 1$: \ a vertex", GREY_A)],
        ], width=5.0, pos=(3.6, -2.6, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> A small example: six blue sources and seven gold targets in the plane, each sized by its "
            f"mass, with squared distance as the cost. <bookmark mark='b'/> The linear program's optimal plan, drawn as green "
            f"flows whose width is the mass moved. Its cost is {say(d['cost'], 3)}. <bookmark mark='c'/> The same plan as a "
            f"matrix: rows are sources, columns targets. <bookmark mark='d'/> Only {d['nonzero']} of its forty-two entries "
            f"are nonzero, exactly n plus m minus one: an optimal vertex of the polytope is sparse, and most sources send "
            f"their mass to one or two places."
        ) as vo:
            self.play(FadeIn(A), FadeIn(src), FadeIn(tgt), FadeIn(simulated_tag(r"simulated; \ LP exact")))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(flows), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(grid), FadeIn(gl))
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def dual(self):
        d = load("lp")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Every linear program has a dual. Here it assigns a number f i to each source and g j to "
            f"each target, <bookmark mark='b'/> subject to f i plus g j being at most the cost C i j for every pair, and "
            f"maximizes the total, a dot f plus b dot g. <bookmark mark='c'/> Strong duality: the two optima are equal. Here "
            f"both are {say(d['cost'], 3)}, and the largest violation of the constraint is ten to the minus fifteen. "
            f"<bookmark mark='d'/> Complementary slackness: mass moves from i to j only where the constraint is tight, f i "
            f"plus g j equal to C i j.",
            [(r"\text{dual}", r":", r"\max_{f, g}\ a'f + b'g", 40),
             (r"\text{subject to}", r":", r"f_i + g_j \le C_{ij} \ \ \forall i, j", 40),
             (r"\text{here}", r":", rf"\text{{primal}} = \text{{dual}} = {d['cost']:.3f}", 40),
             (r"P_{ij} > 0", r"\Rightarrow", r"f_i + g_j = C_{ij}", 40)],
            [r"Kantorovich (1942)", r"potentials", r"strong duality", r"complementary slackness"],
            colors=[(2, PLANC)])

    def prices(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Luis Caffarelli's story, as Cédric Villani retells it, makes the dual a shipping company. You want to move your "
            "earth; a shipper offers to do it, charging f i to load at i and g j to unload at j. <bookmark mark='b'/> You "
            "accept only if no route would be cheaper to do yourself: f i plus g j at most C i j. <bookmark mark='c'/> The "
            "shipper, maximizing revenue under that constraint, earns exactly what the cheapest plan would cost you. "
            "<bookmark mark='d'/> In statistics, the potentials are the useful part: in continuous problems, the optimal map "
            "is read off the gradient of one of them.",
            [(r"\text{the shipper}", r":", r"\text{charges } f_i \text{ to load}, \ g_j \text{ to unload}", 40),
             (r"\text{you accept if}", r":", r"f_i + g_j \le C_{ij}", 40),
             (r"\text{the shipper earns}", r":", r"\text{the optimal cost}", 40),
             (r"\text{statistics}", r":", r"\text{the map from a potential}", 40)],
            [r"Caffarelli, \ via Villani (2009)", r"no cheaper route", r"no duality gap", r"Brenier, \ below"],
            colors=[(2, PLANC)])

    def line(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> On the real line, the problem is solved in closed form. For any convex cost of the "
            "difference, the optimal coupling is the quantile coupling: draw one uniform U and set X to F inverse of U and Y "
            "to G inverse of U. <bookmark mark='b'/> So the Wasserstein distance is the L p distance between the two quantile "
            "functions. <bookmark mark='c'/> For p equal to one, it is also the area between the two distribution "
            "functions. <bookmark mark='d'/> For empirical samples of equal size, the plan pairs the order statistics: sort "
            "both, and match the i-th smallest with the i-th smallest.",
            [(r"\pi^*", r"=", r"\mathrm{law}\big(F^{-1}(U), G^{-1}(U)\big)", 40),
             (r"W_p^p", r"=", r"\int_0^1 |F^{-1}(u) - G^{-1}(u)|^p\,du", 40),
             (r"W_1", r"=", r"\int |F(x) - G(x)|\,dx", 40),
             (r"\text{samples}", r":", r"x_{(i)} \leftrightarrow y_{(i)}", 40)],
            [r"monotone, \ as Monge saw", r"quantile functions", r"CDFs", r"sort and pair"],
            colors=[(1, PLANC)])

    def brenier(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> In several dimensions, convex gradients replace scalar monotone rearrangement. <bookmark mark='b'/> For quadratic cost and laws with finite second moments, absolute continuity of the source ensures a unique optimal transport map almost everywhere, given by the gradient of a convex potential. <bookmark mark='c'/> Such gradients are monotone in the displayed inner-product sense and satisfy cyclic monotonicity. Monotonicity alone does not imply injectivity or an arbitrary no-crossing claim. <bookmark mark='d'/> For half squared-distance cost, the convex potential equals half the source norm squared minus a source Kantorovich potential.",
            [(r"d > 1", r":", r"\text{no ordering}", 40),
             (r"\text{Brenier}", r":", r"T^* = \nabla\varphi, \ \ \varphi \text{ convex}", 40),
             (r"\text{monotone}", r":", r"\langle \nabla\varphi(x) - \nabla\varphi(y), \ x - y\rangle \ge 0", 40),
             (r"\varphi", r"=", r"\tfrac12\|x\|^2 - f(x) \ \ (\text{cost } \tfrac12\|x - y\|^2)", 36)],
            [r"the substitute", r"Brenier (1991)", r"cyclical monotonicity", r"chapter 7's ranks"],
            colors=[(1, PLANC)])

    def algorithms(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Exact discrete transport has several algorithms, with different complexity guarantees. <bookmark mark='b'/> For uniform equal-size clouds an optimal permutation coupling exists by the transport polytope's structure. Other optimal couplings can be mixtures of permutations. Modern Hungarian implementations have cubic worst-case complexity for a dense square assignment problem; the original 1955 implementation was slower. <bookmark mark='c'/> Auction algorithms use price updates and require suitable precision or termination rules. <bookmark mark='d'/> General weighted transport can use network or linear-programming methods. Their costs are not all described by one universal cubic formula.",
            [(r"\text{equal weights}", r":", r"\text{an optimal permutation plan exists}", 40),
             (r"\text{Hungarian}", r":", r"O(n^3), \ \text{Kuhn (1955)}", 40),
             (r"\text{auction}", r":", r"\text{bids raise the dual prices}", 40),
             (r"\text{exact methods}", r":", r"\text{cost depends on algorithm, size and precision}", 40)],
            [r"Birkhoff's theorem", r"K\H{o}nig; \ Egerv\'ary", r"Bertsekas (1979)", r"chapter 4"],
            colors=[(1, PLANC)])

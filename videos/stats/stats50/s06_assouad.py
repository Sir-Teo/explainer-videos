from __future__ import annotations

import numpy as np

from videos.stats.stats50.common import *  # noqa: F403


class Assouad(VoiceoverScene):
    def construct(self):
        self.card()
        self.lemma()
        self.cube()
        self.bumps()
        self.chart()
        self.density()
        self.compare()

    def card(self):
        card = chapter_card(5, r"Assouad's lemma", r"A hypercube of bumps, \ one coin per coordinate", part=PART)
        with self.voiceover("Chapter five. Assouad's lemma: a hypercube of bumps, one coin per coordinate."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def lemma(self):
        rows = [
            cmath(r"\theta_\omega, \ \omega \in \{0, 1\}^m", r":", r"\text{one hypothesis per vertex}", font_size=34),
            cmath(r"\ell(\theta_\omega, \theta_{\omega'})", r"\ge", r"\delta \cdot \#\{j : \omega_j \ne \omega'_j\}: \ \text{vertex-valued Hamming decision loss}", font_size=30),
            cmath(r"\inf_{\hat\omega\in\{0,1\}^m}\max_\omega E_\omega\,\ell(\theta_{\hat\omega},\theta_\omega)", r"\ge", r"\frac{m\,\delta}{2}\, \min_{\omega \sim \omega'} \big(1 - \mathrm{TV}(P_\omega, P_{\omega'})\big)", font_size=32),
            cmath(r"\text{neighbours}", r":", r"m \text{ two-point tests, \ one per coordinate}", font_size=34),
        ]
        rows[2][-1].set_color(LOWC)
        whys = [why(r"Assouad (1983)"), why(r"Hamming-separable losses"), why(r"the lower bound"), why(r"$m$ two-point reductions; independence not required")]
        heading = label('Hamming decision bounds need a reduction factor for squared-loss estimates', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Patrice Assouad's lemma of 1983 indexes hypotheses by the vertices of a hypercube: one hypothesis for each binary string of length m. <bookmark mark='b'/> For a vertex-valued decision, Hamming loss adds over coordinates. For unrestricted estimates under squared loss, reducing the estimate to a vertex requires an additional separation constant. <bookmark mark='c'/> Then the worst-case risk of a vertex-valued decision is at least m delta over two, times one minus the largest total variation between neighbouring vertices. <bookmark mark='d'/> In effect the problem splits into m two-point problems, one per coordinate, each bounded by a two-point testing argument. They need not be independent experiments. Where Fano counts bits, Assouad counts coins."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cube(self):
        W = LowerBoundPacking(center=(-2.6, -0.3, 0), scale=1.0)
        c3 = W.hypercube(3, size=2.4, color=HYPC)
        side = fit_rows(VGroup(
            label(r"$m = 3$: \ 8 hypotheses", font_size=22),
            label(r"edges: \ neighbours, \ one coordinate apart", font_size=22, color=GREY_B),
            label(r"each edge: \ a two-point problem", font_size=22, color=LOWC),
            label(r"an estimate must guess every coordinate", font_size=22, color=HYPC),
            label(r"each guess fails with probability $\approx \tfrac12(1 - \mathrm{TV})$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> With three coordinates, eight hypotheses at the vertices of a cube. <bookmark mark='b'/> "
            "Neighbours, joined by edges, differ in one coordinate. <bookmark mark='c'/> Each edge is a two-point problem. "
            "<bookmark mark='d'/> An estimator implicitly guesses every coordinate, <bookmark mark='e'/> and each guess fails "
            "with probability about half of one minus the total variation between neighbours. The losses add up, so the "
            "bound grows with m."
        ) as vo:
            self.play(FadeIn(exact_tag(r"the lower-bound workbench")))
            vo.wait_until("a")
            self.play(FadeIn(c3[1]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c3[0]), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def bumps(self):
        A = axes([0, 1], [-0.35, 0.35], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"$f_\omega(x)$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[-0.25, 0, 0.25], center=[-2.5, 0.2, 0])
        ax = A.ax
        m = 8
        x = np.linspace(0, 1, 800)
        u = (x * m) % 1
        b = np.where((u > 0) & (u < 1), np.exp(1 - 1 / np.maximum(1 - (2 * u - 1) ** 2, 1e-9)), 0)
        cell = np.minimum((x * m).astype(int), m - 1)
        r = np.random.default_rng(5)
        omegas = [r.integers(0, 2, m) for _ in range(3)]
        cols = [HYPC, UPC, S.ALT]
        curves = [polyline(ax, x, 0.25 * b * (2 * w[cell] - 1), c, 3) for w, c in zip(omegas, cols)]
        side = fit_rows(VGroup(
            label(r"$m$ cells of width $1/m$; \ in cell $j$, \ a bump up or down", font_size=22),
            label(r"schematic heights exaggerated; \ normalize derivatives for actual bounds", font_size=22, color=HYPC),
            label(r"three of the $2^8$ functions", font_size=22, color=UPC),
            label(r"neighbours differ in one bump: \ KL $\asymp n\,m^{-(2s+1)}$", font_size=22, color=LOWC),
            label(r"$m \asymp n^{1/(2s+1)}$: \ risk $\gtrsim m \cdot m^{-(2s+1)} = n^{-2s/(2s+1)}$", font_size=22, color=LOWC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For regression with Hölder smoothness s, cut the interval into m cells and put a bump up or down in each: a binary string chooses the signs. <bookmark mark='b'/> With derivative-normalized bumps, heights of order m to the minus s keep the functions in the designated smoothness ball. The drawn heights are exaggerated schematically for visibility. <bookmark mark='c'/> Here are three of the two hundred and fifty-six functions with eight cells. <bookmark mark='d'/> Neighbours differ in one bump, and their samples have Kullback–Leibler divergence of order n times m to the minus two s plus one. <bookmark mark='e'/> Choosing m of order n to the one over two s plus one keeps that of order one, and Assouad gives an integrated risk of order m times m to the minus two s plus one: n to the minus two s over two s plus one, Stone's global rate."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curves[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(curves[1]), Create(curves[2]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def chart(self):
        d = load("assouad")
        ln = np.log10(d["ns"])
        A = axes([1.8, 5.2], [-7.5, -1.8], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10}$ Assouad's bound",
                 xticks=[2, 3, 4, 5], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[-5, -4, -3, -2], center=[-2.5, 0.2, 0])
        ax = A.ax
        c1 = VGroup(polyline(ax, ln, np.log10(d["s1"]), HYPC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=HYPC) for a, b in zip(ln, np.log10(d["s1"]))])
        c2 = VGroup(polyline(ax, ln, np.log10(d["s2"]), UPC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=UPC) for a, b in zip(ln, np.log10(d["s2"]))])
        sl1 = (np.log10(d["s1"][-1]) - np.log10(d["s1"][0])) / (ln[-1] - ln[0])
        sl2 = (np.log10(d["s2"][-1]) - np.log10(d["s2"][0])) / (ln[-1] - ln[0])
        side = fit_rows(VGroup(
            label(r"Hölder regression, \ the best $m$ for each $n$", font_size=22),
            label(rf"gold: \ $s = 1$: \ slope {sl1:.2f} \ (theory $-2/3$)", font_size=22, color=HYPC),
            label(rf"blue: \ $s = 2$: \ slope {sl2:.2f} \ (theory $-4/5$)", font_size=22, color=UPC),
            label(rf"cells used: \ {', '.join(str(v) for v in d['m1'])} \ for $s = 1$", font_size=22, color=GREY_A),
            label(r"finite-$n$ C2 slopes can differ from the asymptotic exponent", font_size=22, color=ADAPTC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A conservative Assouad bound for explicit smoothness-class constructions in fixed-design Gaussian regression, with the number of cells optimized at each n. <bookmark mark='b'/> For one derivative the slope is {say(sl1, 2)}, against the theory's minus two thirds. <bookmark mark='c'/> For two, {say(sl2, 2)}, against minus four fifths. <bookmark mark='d'/> For smoothness one the optimal cell count grows on the n to the one third scale asymptotically. The computation uses the exact design-point Gaussian KL divergence, rather than replacing it by a continuous integral. <bookmark mark='e'/> The asymptotic exponent improves with smoothness. In this finite range the tightly normalized C-two construction is not yet at its asymptotic slope; integer cell counts and finite-design effects are visible."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def density(self):
        rows = [
            cmath(r"\text{densities on } [0, 1], \ \text{Hölder } s", r":", r"f_\omega = 1 + \textstyle\sum_j (2\omega_j - 1)\, h\, b_j(x), \ \ \int f_\omega = 1", font_size=30),
            cmath(r"\text{KL between neighbours}", r"\asymp", r"n\, h^2 / m = n\, m^{-(2s+1)}", font_size=34),
            cmath(r"\inf \sup E\|\hat f - f\|_2^2", r"\gtrsim", r"n^{-2s/(2s+1)}: \ \text{the kernel estimate's rate is optimal}", font_size=32),
            cmath(r"d \text{ dimensions}", r":", r"m^d \text{ cells: \ } n^{-2s/(2s+d)}: \ \text{Stone's curse, \ proved}", font_size=32),
        ]
        rows[2][-1].set_color(LOWC)
        rows[3][-1].set_color(HYPC)
        whys = [why(r"bumps with zero integral"), why(r"one bump's information"), why(r"Part 29, \ closed"), why(r"the hook's chart, \ explained")]
        heading = label('Mass-preserving normalized bumps yield valid density alternatives', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The same cube works for densities. Add or subtract a bump in each of m cells; bumps with "
            "zero integral keep each function a density. <bookmark mark='b'/> Neighbouring densities differ by one bump, and "
            "the Kullback–Leibler divergence between their samples is of order n h squared over m. <bookmark mark='c'/> "
            "Assouad then gives the integrated squared error rate n to the minus two s over two s plus one: Part "
            "twenty-nine's kernel estimator is rate-optimal, and its question closes. <bookmark mark='d'/> In d dimensions "
            "there are m to the d cells, and the same calculation gives n to the minus two s over two s plus d. The curse of "
            "dimensionality in the hook's chart is this calculation."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def compare(self):
        rows = [[r"method", r"hypotheses", r"good for", r"typical result"],
                [r"Le Cam", r"2", r"one-dimensional features", r"$f(x_0)$: \ $n^{-2s/(2s+1)}$"],
                [r"Fano", r"$M$, \ a packing", r"high dimensions, \ sparsity", r"$s \log(p/s)$"],
                [r"Assouad", r"$2^m$, \ a cube", r"whole functions, \ additive losses", r"$\|f\|_2^2$: \ $n^{-2s/(2s+1)}$"]]
        tab = table_rows(rows, font_size=28, col_buff=0.8, row_buff=0.45, colors=[GREY_B, LOWC, HYPC, UPC])
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.8, 0])
        foot = label(r"all three: \ reduce estimation to testing, \ then bound how well any test can do", font_size=24, color=GREY_A).move_to([0, -1.5, 0])
        foot2 = label(r"Yu (1997), \ `Assouad, \ Fano, \ and Le Cam': \ one framework", font_size=24, color=ADAPTC).move_to([0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The three methods side by side. Le Cam's two points suit one-dimensional features, like a "
            "density at a point. Fano's packings suit high-dimensional problems and sparsity. Assouad's cubes suit whole "
            "functions with losses that add up. <bookmark mark='b'/> All three reduce estimation to testing and then bound "
            "how well any test can do; Bin Yu's 1997 essay, Assouad, Fano and Le Cam, set them out side by side."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

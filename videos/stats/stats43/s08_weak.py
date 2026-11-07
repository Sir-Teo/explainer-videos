from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats43.common import *  # noqa: F403


class WeakConvergence(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.lab()
        self.table()
        self.skorokhod()
        self.tightness()
        self.horse()

    def card(self):
        card = chapter_card(7, r"Weak convergence", r"What does it mean for laws to converge?", lit=(1956,), part=PART)
        with self.voiceover("Chapter seven. Weak convergence: what it means for laws to converge, and how far apart two laws are."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"X_n \Rightarrow X", r"\iff", r"F_n(x) \to F(x) \text{ at every continuity point of } F", font_size=32),
            cmath(r"\phantom{X}", r"\iff", r"E f(X_n) \to E f(X) \ \text{ for all bounded continuous } f", font_size=32),
            cmath(r"\phantom{X}", r"\iff", r"\limsup P(X_n \in C) \le P(X \in C) \ \forall \text{ closed } C", font_size=32),
            cmath(r"\phantom{X}", r"\iff", r"P(X_n \in A) \to P(X \in A) \ \text{ whenever } P(X \in \partial A) = 0", font_size=30),
        ]
        rows[1][-1].set_color(LAWC)
        whys = [why(r"CDFs, \ Part 6"), why(r"test functions"), why(r"the portmanteau theorem"), why(r"continuity sets")]
        with self.voiceover(
            "<bookmark mark='a'/> Part six defined convergence in distribution through CDFs: they converge at every point "
            "where the limit is continuous. The exception matters: one over n converges to zero, but its CDF at zero is zero "
            "for every n, while the limit's is one. <bookmark mark='b'/> The portmanteau theorem gives equivalent forms. "
            "Expectations of every bounded continuous function converge: the definition that works in any metric space. "
            "<bookmark mark='c'/> Probabilities of closed sets can only grow in the limit, <bookmark mark='d'/> and "
            "probabilities of sets whose boundary carries no limiting mass converge. Each form is the right tool somewhere."
        ) as vo:
            heading=label('Weak convergence tests laws through bounded continuous functions',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lab(self):
        d = load("weak")
        A = axes([-3.5, 3.5], [0, 1], x_length=7.4, y_length=4.4, xlabel=r"$z$", ylabel=r"CDF", xticks=[-3, -2, -1, 0, 1, 2, 3],
                 yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        lab = ConvergenceLab(ax, stats.norm.cdf, atoms=d["atoms10"], probs=d["probs10"], color_F=LAWC, color_G=LIMC)
        cF, cG = lab.curve_F(), lab.curve_G()
        k = d["k10"]
        bar = lab.kolmogorov_bar(k["x"], top=k["F"], color=KOLC)
        r = d["rows"][1]
        # the Levy box sits where the gap is widest, between the step and the curve
        box = lab.levy_box(k["x"] - r["levy"] / 2 - 0.02, r["levy"], y=0.5 + (k["F"] - 0.5) / 2, color=LEVYC)
        area = lab.area(color=WASC, opacity=0.4)
        side = fit_rows(VGroup(
            label(r"standardized Binomial(10, 1/2) \ vs \ $\Phi$", font_size=24),
            label(rf"Kolmogorov: \ the largest gap, \ {r['kolmogorov']:.3f}", font_size=24, color=KOLC),
            label(rf"L\'evy: \ the largest box between, \ {r['levy']:.3f}", font_size=24, color=LEVYC),
            label(rf"Wasserstein: \ the area between, \ {r['wasserstein']:.3f}", font_size=24, color=WASC),
            label(rf"Prokhorov: \ in [{r['levy']:.3f}, \ {r['ky_fan']:.3f}]", font_size=24, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> To say how close two laws are, we need distances, and this part's lab uses lattice extrema, analytic normal quantile-cell integrals and numerical bisection, avoiding simulation noise for these binomial comparisons. Here is a standardized binomial with ten trials, as a staircase, against the normal CDF. <bookmark mark='b'/> The Kolmogorov distance is the largest vertical gap between the graphs, {say(r['kolmogorov'], 3)}, at zero, where the staircase jumps over the curve. <bookmark mark='c'/> Paul Lévy's distance is the side of the largest box that can be slid between the two graphs, allowing a little horizontal slack as well as vertical: {say(r['levy'], 3)}. Unlike Kolmogorov's, it metrizes weak convergence, so it is not fooled by one over n. <bookmark mark='d'/> The Wasserstein distance is the area between the graphs, {say(r['wasserstein'], 3)}: the least average distance mass must move to turn one law into the other. <bookmark mark='e'/> And the Lévy–Prokhorov distance, on Polish metric spaces, is pinned between Lévy's below and the Ky Fan distance of the quantile coupling above."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cG), Create(cF), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bar), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(box), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(area), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("weak")
        rows = [[r"$n$", r"Kolmogorov", r"L\'evy", r"Prokhorov $\le$", r"Wasserstein"]] + [
            [f"{r['n']}", f"{r['kolmogorov']:.4f}", f"{r['levy']:.4f}", f"{r['ky_fan']:.4f}", f"{r['wasserstein']:.4f}"] for r in d["rows"]]
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.22, colors=[GREY_A, None, None, None, None]).move_to([0, 0.6, 0])
        rr = d["rows"]
        msg = fit_rows(VGroup(
            label(rf"deterministic numerical distances; several roughly halve as $n$ quadruples \ ({rr[0]['kolmogorov'] / rr[-1]['kolmogorov']:.1f}$\times$ over $40\times$ the trials)", font_size=24, color=S.ACCENT),
            label(r"L\'evy $\le$ Prokhorov $\le$ Ky Fan of a coupling; \ Kolmogorov $\ge$ L\'evy", font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, -2.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The same distances for four, ten, forty and a hundred and sixty trials. <bookmark mark='b'/> The displayed distances shrink as the number of trials grows; several roughly halve when the number of trials quadruples, but the quantile-coupling upper bound is not an exact one-over-root-n law: these are deterministic calculations with numerical tolerances, rather than Monte Carlo estimates. From four trials to a hundred and sixty, the Kolmogorov distance falls {rr[0]['kolmogorov'] / rr[-1]['kolmogorov']:.1f}-fold, close to the square root of forty. <bookmark mark='c'/> The inequalities between them hold at every n, as they must."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(msg[0]))
            vo.wait_until("c")
            self.play(FadeIn(msg[1]))
        self.clear_scene()

    def skorokhod(self):
        A = axes([0, 1], [-3.5, 3.5], x_length=7.4, y_length=4.4, xlabel=r"$u$", ylabel=r"quantile functions $F_n^{-1}(u)$",
                 xticks=[0, 0.5, 1], yticks=[-3, 0, 3], center=[-2.5, 0.2, 0])
        ax = A.ax
        us = np.linspace(0.002, 0.998, 400)
        cols = [GREY_B, LAWC, S.ALT]
        curves = VGroup()
        for n, c in zip([4, 16, 64], cols):
            k = np.arange(n + 1)
            atoms = (k - n / 2) / np.sqrt(n / 4)
            cdf = stats.binom.cdf(k, n, 0.5)
            q = atoms[np.minimum(np.searchsorted(cdf, us, side="left"), n)]
            m = VMobject(stroke_color=c, stroke_width=3)
            pts = []
            prev = None
            for u, v in zip(us, q):
                if prev is not None and v != prev:
                    pts.append(ax.c2p(u, prev))
                pts.append(ax.c2p(u, v))
                prev = v
            m.set_points_as_corners(pts)
            curves.add(m)
        lim = curve(ax, us, stats.norm.ppf(us), LIMC, 4)
        side = fit_rows(VGroup(
            label(r"one uniform $U$ \ for every $n$", font_size=24),
            label(r"$Y_n = F_n^{-1}(U)$ \ has law $F_n$", font_size=24, color=LAWC),
            label(r"$F_n \Rightarrow F$ \ $\Rightarrow$ \ $F_n^{-1}(u) \to F^{-1}(u)$ \ a.e.", font_size=24, color=LIMC),
            label(r"so $Y_n \to Y$ \ almost surely: \ Skorokhod (1956)", font_size=24, color=S.ACCENT),
            label(r"proofs about laws become proofs about variables", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Weak convergence is about laws, not random variables, yet it can always be "
            "represented by variables on a new common space that converge almost surely, without asserting the "
            "original variables do so. Take a single uniform U. <bookmark mark='b'/> For each n, put Y n equal to F n"
            " inverse of U: by chapter two it has law F n. Here are the quantile functions of standardized binomials "
            "with four, sixteen and sixty-four trials. <bookmark mark='c'/> When the laws converge weakly, the "
            "quantile functions converge at almost every u, here to the normal quantile function in gold, <bookmark "
            "mark='d'/> so the Y n converge almost surely. This is Anatoliy Skorokhod's representation theorem. "
            "<bookmark mark='e'/> It turns proofs about laws into proofs about variables: the continuous mapping "
            "theorem of Part six, for instance, becomes a one-line consequence of continuity."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.5), FadeIn(side[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(lim), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def tightness(self):
        A = axes([-6, 6], [0, 1], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"CDF of $N(0, n^2)$", xticks=[-6, -3, 0, 3, 6],
                 yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        xs = np.linspace(-6, 6, 400)
        cols = [LAWC, S.ALT, S.PRIOR, S.ACCENT]
        cs = VGroup(*[curve(ax, xs, stats.norm.cdf(xs / n), c, 3) for n, c in zip([1, 3, 10, 40], cols)])
        half = DashedLine(ax.c2p(-6, 0.5), ax.c2p(6, 0.5), color=BADC, stroke_width=3)
        side = fit_rows(VGroup(
            label(r"$F_n(x) \to \tfrac12$ \ for every $x$", font_size=24, color=BADC),
            label(r"the limit is not a CDF: \ the mass escaped to $\pm\infty$", font_size=24, color=BADC),
            label(r"tight: \ $\forall \varepsilon \ \exists K$: \ $P(|X_n| > K) < \varepsilon$ \ for all $n$", font_size=24, color=GOODC),
            label(r"Prokhorov: \ tight $\iff$ every subsequence has a weakly convergent sub-subsequence", font_size=22, color=GOODC),
            label(r"Helly: \ CDFs always have a subsequence converging, \ perhaps to less than mass one", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Laws can also fail to converge by losing mass. Normal laws with standard deviation n "
            "spread out ever more thinly, and their CDFs converge to one half at every point. <bookmark mark='b'/> One half is "
            "not a CDF: the mass has escaped to plus and minus infinity. <bookmark mark='c'/> The cure is tightness: for every "
            "epsilon, one interval holds all but epsilon of every law in the sequence. <bookmark mark='d'/> Yuri Prokhorov's "
            "theorem: a family of laws is tight exactly when every sequence from it has a weakly convergent subsequence, a "
            "compactness theorem for probability measures. <bookmark mark='e'/> On the line it rests on Helly's selection "
            "theorem: any sequence of CDFs has a subsequence converging at continuity points, though perhaps to a limit of "
            "mass less than one. Tightness is what keeps the mass."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in cs], lag_ratio=0.5), Create(half), FadeIn(side[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def horse(self):
        d = load("horse")
        k, obs, ex = np.asarray(d["k"]), np.asarray(d["obs"]), np.asarray(d["expected"])
        A = axes([-0.6, 4.6], [0, 120], x_length=5.6, y_length=3.4, xlabel=r"deaths in a corps-year", ylabel=r"corps-years",
                 xticks=[0, 1, 2, 3, 4], yticks=[0, 40, 80, 120], center=[-3.4, 0.75, 0])
        ax = A.ax
        bo = bars_at(ax, k - 0.17, obs, 0.32, LAWC, opacity=0.85)
        be = bars_at(ax, k + 0.17, ex, 0.32, LIMC, opacity=0.85)
        tv = d["tv"]
        tab = table_rows([[r"$n$", r"$d_{TV}(\text{Bin}(n, \lambda/n), \text{Poi}(\lambda))$", r"Le Cam: \ $\lambda^2/n$"]] +
                         [[f"{r['n']:,}", f"{r['tv']:.5f}", f"{r['bound']:.5f}"] for r in tv], font_size=20, col_buff=0.4, row_buff=0.12)
        tab.move_to([3.4, 0.9, 0])
        side = fit_rows(VGroup(
            label(rf"{d['deaths']} deaths in {d['N']} corps-years: \ $\hat\lambda = {d['lam']:.2f}$", font_size=22),
            label(rf"pooled 0,1,2+; approximate $\chi^2_1$ reference: \ $\chi^2 = {d['chi2']:.2f}$, \ $p = {d['p']:.2f}$", font_size=22, color=GREY_A),
            label(r"a total-variation limit: \ stronger than weak convergence", font_size=22, color=S.ACCENT),
        ), 12.4, 0.28, [0, -2.75, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A real limit theorem at work. In 1898 Ladislaus Bortkiewicz counted the soldiers of the Prussian cavalry killed by horse kicks: {d['deaths']} deaths over {d['N']} corps-years, a mean of {say(d['lam'], 2)}. <bookmark mark='b'/> The counts, in blue, are compared with a fitted Poisson law, in gold. For an approximate goodness-of-fit reference, pool the rare counts into two or more deaths; the resulting statistic is {say(d['chi2'], 2)}. <bookmark mark='c'/> Why Poisson? A rare-event model with independent, small event probabilities motivates a Poisson approximation. Agreement of this historical table with a fitted Poisson does not establish that independence or equal risks held. Lucien Le Cam's 1960 inequality says how fast: the total variation distance between a sum of independent Bernoullis and the Poisson with the same mean is at most the sum of the squared chances, here lambda squared over n. The table checks it exactly. <bookmark mark='d'/> Total variation bounds every event's probability at once, a stronger kind of convergence than weak convergence."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Bortkiewicz (1898): \ Prussian cavalry, \ 1875--1894")))
            vo.wait_until("a")
            self.play(FadeIn(bo), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(be), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

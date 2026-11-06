from __future__ import annotations

import numpy as np

from videos.stats.stats52.common import *  # noqa: F403


class Laws(VoiceoverScene):
    def construct(self):
        self.card()
        self.stieltjes()
        self.equation()
        self.inversion()
        self.wigner()
        self.universality()

    def card(self):
        card = chapter_card(7, r"Random-matrix laws", r"The Stieltjes transform, \ Marchenko--Pastur and the semicircle", lit=(1967,), part=PART)
        with self.voiceover("Chapter seven. Random-matrix laws: the Stieltjes transform, Marchenko–Pastur and the semicircle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def stieltjes(self):
        rows = [
            cmath(r"F_p", r"=", r"\tfrac1p\textstyle\sum_k \delta_{\lambda_k}: \ \text{the empirical spectral distribution}", font_size=32),
            cmath(r"m(z)", r"=", r"\int \frac{dF(x)}{x - z} = \tfrac1p\,\mathrm{tr}\,(S - zI)^{-1}, \ \ z \in \mathbb C^+", font_size=32),
            cmath(r"f(x)", r"=", r"\lim_{\eta \downarrow 0} \tfrac{1}{\pi}\,\mathrm{Im}\; m(x + i\eta): \ \text{inversion}", font_size=32),
            cmath(r"\text{why}", r":", r"\text{the trace of a resolvent obeys an equation; \ moments need not}", font_size=30),
        ]
        rows[1][-1].set_color(BULKC)
        rows[2][-1].set_color(GOODC)
        whys = [why(r"one point mass per eigenvalue"), why(r"the resolvent's trace"), why(r"Stieltjes (1894)"), why(r"Marchenko \& Pastur (1967)")]
        with self.voiceover(
            "<bookmark mark='a'/> How are such laws found? Put a point mass at each eigenvalue: the empirical spectral "
            "distribution. <bookmark mark='b'/> Its Stieltjes transform, a function of a complex variable z above the real "
            "axis, is the average of one over lambda minus z, which is a normalized trace of the resolvent matrix, S minus z "
            "times the identity, inverted. <bookmark mark='c'/> The density comes back as the limit of the transform's "
            "imaginary part over pi as z approaches the real axis, a formula of Thomas Stieltjes from 1894. <bookmark "
            "mark='d'/> The point is that the resolvent's trace satisfies an equation that can be solved in the limit, where "
            "the moments of the spectrum would need endless combinatorics. That was Vladimir Marchenko and Leonid Pastur's "
            "method in 1967."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def equation(self):
        rows = [
            cmath(r"(S - zI)^{-1}_{kk}", r"=", r"\frac{1}{s_{kk} - z - s_k^\top (S_{(k)} - zI)^{-1} s_k}", font_size=32),
            cmath(r"s_k^\top (S_{(k)} - zI)^{-1} s_k", r"\approx", r"\text{its expectation: \ a quadratic form concentrates}", font_size=30),
            cmath(r"\gamma z\, m^2 + (z + \gamma - 1)\, m + 1", r"=", r"0", font_size=36),
            cmath(r"\text{solve, \ invert}", r":", r"f(x) = \frac{\sqrt{(b - x)(x - a)}}{2\pi\gamma x}, \ \ a, b = (1 \mp \sqrt\gamma)^2", font_size=32),
        ]
        rows[2][-1].set_color(BULKC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Schur complement"), why(r"Part 51's concentration"), why(r"a quadratic for $m$"), why(r"the law of the hook")]
        with self.voiceover(
            "<bookmark mark='a'/> The derivation in outline. Each diagonal entry of the resolvent is, by the Schur complement, "
            "one over a diagonal entry of S, minus z, minus a quadratic form in the rest of the matrix. <bookmark mark='b'/> "
            "That quadratic form is a sum of many weakly dependent terms, and concentrates around its expectation, which is "
            "itself expressed through the Stieltjes transform. <bookmark mark='c'/> So the transform satisfies a quadratic "
            "equation: gamma z m squared, plus z plus gamma minus one times m, plus one, equals zero. <bookmark mark='d'/> "
            "Solving it and inverting gives the Marchenko–Pastur density, with its edges at one plus or minus root gamma, "
            "squared: the law of this part's hook."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def inversion(self):
        d = load("laws")
        x = np.asarray(d["x"])
        A = axes([0, 3.4], [0, 0.95], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"$\frac1\pi\,\mathrm{Im}\, m(x + i\eta)$",
                 xticks=[0, 1, 2, 3], yticks=[0, 0.25, 0.5, 0.75], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"0.2": GREY_B, "0.05": BULKC, "1e-06": TRUEC}
        cs = {k: clip_curve(ax, x, np.asarray(v), cols[k], 4 if k == "1e-06" else 3, ymin=0, ymax=0.95) for k, v in d["stieltjes"].items()}
        a, b = d["edges_mp"]
        lab = SpectrumBulk(ax)
        ea, eb = lab.edge(a, 0.95, color=SPIKEC), lab.edge(b, 0.95, color=SPIKEC)
        side = fit_rows(VGroup(
            label(rf"$\gamma = {d['gamma']}$: \ the Stieltjes transform, \ solved", font_size=22),
            label(r"grey: \ $\eta = 0.2$, \ a blurred spectrum", font_size=22, color=GREY_B),
            label(r"teal: \ $\eta = 0.05$", font_size=22, color=BULKC),
            label(r"white: \ $\eta \to 0$: \ exactly Marchenko--Pastur", font_size=22, color=TRUEC),
            label(rf"gold: \ the edges {a:.3f} and {b:.3f}", font_size=22, color=SPIKEC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The inversion, computed from the quadratic equation's root at ratio one half. <bookmark "
            f"mark='b'/> At a height of point two above the real axis, the imaginary part is a blurred version of the "
            f"spectrum: the transform at height eta is the density smoothed by a Cauchy kernel of width eta. <bookmark "
            f"mark='c'/> At point oh five the shape emerges. <bookmark mark='d'/> In the limit it is exactly the "
            f"Marchenko–Pastur density, statkit checks to within a thousandth, <bookmark mark='e'/> with edges at "
            f"{say(a, 3)} and {say(b, 2)}."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs["0.2"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs["0.05"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs["1e-06"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(ea), Create(eb), FadeIn(side[4]))
        self.clear_scene()

    def wigner(self):
        d = load("laws")
        A = axes([-2.5, 2.5], [0, 0.4], x_length=7.4, y_length=4.4, xlabel=r"eigenvalue of $(G + G^\top)/\sqrt{2n}$", ylabel=r"density",
                 xticks=[-2, -1, 0, 1, 2], yticks=[0, 0.1, 0.2, 0.3, 0.4], center=[-2.5, 0.2, 0])
        ax = A.ax
        lab = SpectrumBulk(ax)
        bars = lab.bars(d["w_edges"], d["w_hist"], color=BULKC)
        law = lab.law(d["w_x"], d["semi"], color=TRUEC)
        e1, e2 = lab.edge(-2, 0.4, color=SPIKEC), lab.edge(2, 0.4, color=SPIKEC)
        side = fit_rows(VGroup(
            label(r"a symmetric $1{,}000 \times 1{,}000$ Gaussian matrix", font_size=22),
            label(r"teal: \ its eigenvalues", font_size=22, color=BULKC),
            label(r"white: \ Wigner's semicircle, \ $\sqrt{4 - x^2}/(2\pi)$", font_size=22, color=TRUEC),
            label(rf"extremes {d['w_min']:.3f} and {d['w_max']:.3f}; \ edges $\pm 2$", font_size=22, color=SPIKEC),
            label(r"from $m^2 + zm + 1 = 0$", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The other classical law. A symmetric matrix of independent Gaussians, a thousand by a "
            f"thousand, scaled by root two n. <bookmark mark='b'/> Its eigenvalues, <bookmark mark='c'/> and Eugene Wigner's "
            f"semicircle of 1955, found while modelling the energy levels of heavy nuclei. <bookmark mark='d'/> The extreme "
            f"eigenvalues are {say(d['w_min'], 3)} and {say(d['w_max'], 3)}, against edges at plus and minus two. <bookmark "
            f"mark='e'/> The same method gives it: the Stieltjes transform satisfies m squared plus z m plus one equals zero."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ the law exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(law), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(e1), Create(e2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def universality(self):
        rows = fit_rows(VGroup(
            label(r"the laws are universal:", font_size=28, color=GREY_A),
            label(r"any i.i.d. entries with mean 0 and variance 1: \ the same semicircle, \ the same MP law", font_size=26, color=BULKC),
            label(r"general $\Sigma$: \ the Marchenko--Pastur equation for $m$, \ solved numerically (Silverstein 1995)", font_size=26, color=BULKC),
            label(r"but heavy tails change the edges: \ with infinite fourth moments, \ outliers escape", font_size=26, color=BADC),
            label(r"and only the bulk is universal: \ the largest eigenvalue is chapter 9's question", font_size=26, color=SPIKEC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> These laws are universal. <bookmark mark='b'/> Any independent entries with mean zero and "
            "variance one give the same semicircle and the same Marchenko–Pastur law in the limit, like a central limit "
            "theorem for spectra. <bookmark mark='c'/> For a general population covariance, Jack Silverstein's equation of "
            "1995 gives the limiting spectrum, solved numerically, which is how nonlinear shrinkage inverts it. <bookmark "
            "mark='d'/> Heavy tails change things at the edges: with infinite fourth moments, the largest eigenvalues escape "
            "the bulk. <bookmark mark='e'/> And the law describes only the bulk. The behaviour of the largest eigenvalue, "
            "which decides whether a spike can be detected, is chapter nine's question."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

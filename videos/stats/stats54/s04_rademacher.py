from __future__ import annotations

import numpy as np

from videos.stats.stats54.common import *  # noqa: F403


class Rademacher(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.theorem()
        self.contraction()
        self.massart()
        self.chart()
        self.networks()
        self.data_dependent()

    def card(self):
        card = chapter_card(3, r"Rademacher complexity", r"How well can a class fit pure noise?", lit=(2002,), part=PART)
        with self.voiceover("Chapter three. Rademacher complexity: how well can a class fit pure noise?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\sigma_i = \pm 1", r":", r"\text{random signs, \ pure noise labels}", font_size=36),
            cmath(r"\hat{\mathfrak R}_n(\mathcal F)", r"=", r"E_\sigma \sup_{f \in \mathcal F} \tfrac1n\textstyle\sum_i \sigma_i f(X_i)", font_size=36),
            cmath(r"\text{read}", r":", r"\text{the best correlation the class can achieve with noise}", font_size=34),
            cmath(r"E\sup_f (R(f) - R_n(f))", r"\le", r"2\,\mathfrak R_n(\mathcal F): \ \text{symmetrization}", font_size=34),
        ]
        rows[1][-1].set_color(BOUNDC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Rademacher variables"), why(r"Koltchinskii; \ Bartlett \& Mendelson (2002)"), why(r"fitting noise"), why(r"Part 48")]
        heading = label('Noise fitting controls a one-sided deviation through symmetrization', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Draw independent random signs. <bookmark mark='b'/> Empirical Rademacher complexity is the expected largest signed correlation that the class can achieve on the observed points. <bookmark mark='c'/> It measures the ability to fit noise on these data. <bookmark mark='d'/> Symmetrization controls the expected one-sided supremum of population minus sample risk by twice the expected complexity. For an absolute supremum one must use the appropriate absolute or enlarged loss class. The distinction matters even for a singleton class, whose one-sided Rademacher complexity is zero."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def theorem(self):
        rows = [
            cmath(r"0\le\ell\le1,\ \forall f,\ \text{w.p. }1-\delta", r":", r"R(f) \le R_n(f) + 2\hat{\mathfrak R}_n(\ell \circ \mathcal F) + 3\sqrt{\log(2/\delta)/(2n)}", font_size=28),
            cmath(r"\text{finite class}", r":", r"\mathfrak R_n \le \sqrt{2\log K/n}: \ \text{Massart's lemma}", font_size=34),
            cmath(r"\text{VC class}", r":", r"\mathfrak R_n \lesssim \sqrt{d/n}: \ \text{via chaining}", font_size=34),
            cmath(r"\text{data-dependent}", r":", r"\hat{\mathfrak R}_n \text{ computed on the sample you have}", font_size=34),
        ]
        rows[0][-1].set_color(BOUNDC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"McDiarmid's inequality"), why(r"Part 48"), why(r"Dudley"), why(r"often much smaller")]
        heading = label('A simultaneous bounded-loss guarantee includes concentration', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> For a fixed measurable class with losses in zero to one, this bound holds simultaneously for all rules with probability one minus delta. It adds empirical loss, twice the empirical complexity of the loss class, and a concentration term. <bookmark mark='b'/> A finite bounded class has complexity at most root two log K over n. <bookmark mark='c'/> For binary VC classes, chaining removes the elementary counting bound's logarithm. <bookmark mark='d'/> The empirical complexity adapts to the sample's geometry, but the probability guarantee still needs the concentration term."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def contraction(self):
        rows = [
            cmath(r"\varphi \ L\text{-Lipschitz}, \ \varphi(0) = 0", r"\Rightarrow", r"\mathfrak R_n(\varphi \circ \mathcal F) \le L\,\mathfrak R_n(\mathcal F)", font_size=32),
            cmath(r"\text{linear}", r":", r"\mathcal F = \{x \mapsto \langle w, x\rangle: \|w\| \le B\}: \ \hat{\mathfrak R}_n \le B\sqrt{\textstyle\sum\|x_i\|^2}/n", font_size=30),
            cmath(r"\text{kernels}", r":", r"\|f\|_{\mathbb H} \le B: \ \hat{\mathfrak R}_n \le B\sqrt{\mathrm{tr}\,K}/n", font_size=34),
            cmath(r"\text{no dimension}", r":", r"\text{only the norm bound } B \text{ and the data's size}", font_size=34),
        ]
        rows[0][-1].set_color(GOODC)
        rows[3][-1].set_color(CLASSC)
        whys = [why(r"Ledoux--Talagrand"), why(r"Cauchy--Schwarz, \ Jensen"), why(r"the same, \ in feature space"), why(r"infinite dimensions allowed")]
        heading = label('Lipschitz losses transfer linear and kernel norm bounds', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The contraction lemma of Michel Ledoux and Michel Talagrand makes this practical: composing "
            "with an L-Lipschitz loss multiplies the Rademacher complexity by at most L, so the loss can be peeled off. "
            "<bookmark mark='b'/> For linear functions with weights of norm at most B, Cauchy–Schwarz and Jensen give B times "
            "the root of the summed squared norms of the data, over n. <bookmark mark='c'/> For a ball in a reproducing-kernel "
            "space, the same with the trace of the kernel matrix. <bookmark mark='d'/> Neither bound involves the dimension: "
            "only the norm of the weights and the size of the data, which is why kernel methods in infinite-dimensional "
            "feature spaces can generalize."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def massart(self):
        rows = [
            cmath(r"\text{Massart's lemma}", r":", r"A \subset \mathbb R^n \text{ finite}, \ \|a\| \le r: \ E\max_{a \in A}\tfrac1n\textstyle\sum\sigma_i a_i \le \frac{r\sqrt{2\log|A|}}{n}", font_size=30),
            cmath(r"\text{proof}", r":", r"\text{each } \sum\sigma_i a_i \text{ is sub-Gaussian (Part 51); \ a max of } |A|", font_size=32),
            cmath(r"\text{VC class}", r":", r"|A| \le (en/d)^d \ \Rightarrow \ \mathfrak R_n \le \sqrt{2d\log(en/d)/n}", font_size=32),
            cmath(r"\text{the bridge}", r":", r"\text{from counting labellings to Rademacher complexity}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Massart (2000)"), why(r"Hoeffding's lemma"), why(r"Sauer--Shelah"), why(r"chapter 2 meets chapter 3")]
        heading = label('A finite set of bounded vectors has a logarithmic maximum penalty', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The link to chapter two is Pascal Massart's finite-class lemma: for a finite set of vectors of norm at most r, the expected maximum correlation with random signs is at most r times the root of two log the set's size, over n. <bookmark mark='b'/> Each correlation is sub-Gaussian by Part fifty-one, and the maximum of finitely many sub-Gaussians is controlled by the log of their number. <bookmark mark='c'/> For a binary VC class with one at most d at most n, the vectors are the class's labellings of the sample, at most e n over d to the d of them, which gives a Rademacher complexity of the root of two d log of e n over d, over n. <bookmark mark='d'/> Counting labellings and fitting noise are the same idea."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("rademacher")
        ln = np.log10(d["ns"])
        A = axes([1.3, 3.0], [-1.6, -0.55], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10}\hat{\mathfrak R}_n$",
                 xticks=[np.log10(25), 2, np.log10(400), np.log10(800)], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[-1.5, -1, -0.75], center=[-2.5, 0.2, 0])
        ax = A.ax
        cl = VGroup(*[Dot(ax.c2p(a, b), radius=0.1, color=TESTC) for a, b in zip(ln, np.log10(d["linear"]))])
        clb = polyline(ax, ln, np.log10(d["linear_bound"]), BOUNDC, 3)
        ck = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=CLASSC) for a, b in zip(ln, np.log10(d["kernel"]))])
        slope = float(np.polyfit(ln, np.log10(d["linear"]), 1)[0])
        side = fit_rows(VGroup(
            label(r"$x_i \in \mathbb R^{10}$, \ $\|w\| \le 1$; \ 2,000 sign vectors", font_size=22),
            label(rf"blue: \ the linear class, \ slope {slope:.2f}", font_size=22, color=TESTC),
            label(r"purple: \ the bound $\sqrt{\sum\|x_i\|^2}/n$: \ nearly exact", font_size=22, color=BOUNDC),
            label(r"gold: \ a Gaussian-kernel ball", font_size=22, color=CLASSC),
            label(r"both shrink like $1/\sqrt n$", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Rademacher complexities computed by simulation over two thousand sign vectors, for data in "
            f"ten dimensions. <bookmark mark='b'/> The linear class with weights of norm one, in blue, falls with slope "
            f"{say(slope, 2)}. <bookmark mark='c'/> The trace bound, in purple, is almost exactly its value: for linear "
            f"classes, Jensen's inequality loses very little. <bookmark mark='d'/> A ball in a Gaussian-kernel space, in "
            f"gold, behaves the same way. <bookmark mark='e'/> Both shrink like one over the root of n."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ bounds exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(cl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(clb), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(ck), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def networks(self):
        rows = [
            cmath(r"\text{deep networks}", r":", r"f(x) = W_L\sigma(W_{L-1}\cdots\sigma(W_1 x))", font_size=34),
            cmath(r"\text{norm-based}", r":", r"\text{margin term}\lesssim \frac{\prod_\ell \|W_\ell\|_{op}}{\gamma\sqrt n}\cdot(\text{layer terms})", font_size=32),
            cmath(r"\text{size-independent}", r":", r"\text{no explicit width factor if the specified norms stay bounded}", font_size=34),
            cmath(r"\text{still}", r":", r"\text{numerically loose for real networks}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"composition, \ layer by layer"), why(r"Bartlett, \ Foster \& Telgarsky (2017)"), why(r"Golowich, \ Rakhlin \& Shamir (2018)"), why(r"chapter 10's puzzle")]
        heading = label('Network margin bounds depend on norms, depth and input scale', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Norm bounds propagate through a network under assumptions on the input radius and the activation's Lipschitz constant. <bookmark mark='b'/> Bartlett, Foster and Telgarsky give a margin bound involving the product of operator norms, divided by the margin and root n, and additional layer terms. This is a margin generalization term, not the unscaled function complexity. <bookmark mark='c'/> Other bounds avoid an explicit width factor when specified norms stay controlled. The norms themselves can grow with width. <bookmark mark='d'/> These are useful structural results, but their numerical values can remain vacuous for trained networks."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def data_dependent(self):
        rows = fit_rows(VGroup(
            label(r"why Rademacher complexity is the modern tool:", font_size=28, color=GREY_A),
            label(r"it adapts to the data's geometry, \ not just the class", font_size=26, color=GOODC),
            label(r"it handles real-valued losses, \ through contraction", font_size=26, color=GOODC),
            label(r"it composes: \ sums, \ convex hulls, \ Lipschitz maps, \ deep networks layer by layer", font_size=26, color=CLASSC),
            label(r"and it underlies margin bounds (chapter 5) \ and localization (chapter 4)", font_size=26, color=BOUNDC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why Rademacher complexity became the standard tool. <bookmark mark='b'/> It adapts to the "
            "geometry of the data at hand, not just the class. <bookmark mark='c'/> It handles real-valued losses through "
            "contraction. <bookmark mark='d'/> It composes: the complexity of a convex hull equals that of the class, and "
            "deep networks can be bounded layer by layer through their weight norms. <bookmark mark='e'/> And it is the "
            "engine of the margin bounds of chapter five and the localization of chapter four."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

from __future__ import annotations

import math

import numpy as np

from videos.stats.stats52.common import *  # noqa: F403


class Perturbation(VoiceoverScene):
    def construct(self):
        self.card()
        self.weyl()
        self.example()
        self.dk()
        self.chart()
        self.wedin()

    def card(self):
        card = chapter_card(6, r"Perturbation theory", r"How far does an eigenvector move?", lit=(1970,), part=PART)
        with self.voiceover("Chapter six. Perturbation theory: how far does an eigenvector move?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def weyl(self):
        rows = [
            cmath(r"\hat\Sigma = \Sigma + E", r":", r"\text{the truth plus a perturbation}", font_size=34),
            cmath(r"|\lambda_k(\hat\Sigma) - \lambda_k(\Sigma)|", r"\le", r"\|E\|_{op}: \ \text{Weyl (1912)}", font_size=34),
            cmath(r"\text{eigenvectors}", r":", r"\text{can move a lot, \ if two eigenvalues are close}", font_size=32),
            cmath(r"\Sigma = \mathrm{diag}(1 + \delta, 1)", r":", r"\text{a tiny } E \text{ can rotate } v_1 \text{ by } 45^\circ", font_size=32),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"estimation error"), why(r"eigenvalues are stable"), why(r"the gap is everything"), why(r"when $\|E\| \approx \delta$")]
        heading = label('Eigenvalues are stable while small gaps make eigenvectors sensitive', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Every spectral method estimates the eigenvectors of a matrix from a noisy version of it: the "
            "truth plus a perturbation. <bookmark mark='b'/> Eigenvalues are stable. Hermann Weyl's inequality of 1912 says each "
            "moves by at most the operator norm of the perturbation. <bookmark mark='c'/> Eigenvectors are not, when two "
            "eigenvalues are close. <bookmark mark='d'/> If the truth is diagonal with entries one plus delta and one, a "
            "perturbation of size delta can rotate the leading eigenvector by forty-five degrees."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def example(self):
        rows = [
            cmath(r"\Sigma + E", r"=", r"\begin{bmatrix} 1 + \delta & \varepsilon \\ \varepsilon & 1 \end{bmatrix}", font_size=36),
            cmath(r"\tan 2\theta", r"=", r"\frac{2\varepsilon}{\delta}: \ \text{the exact rotation of } v_1", font_size=36),
            cmath(r"\varepsilon = \delta/2", r":", r"\theta = 22.5^\circ; \ \ \varepsilon = 5\delta: \ \theta \approx 42^\circ", font_size=34),
            cmath(r"\text{Davis--Kahan}", r":", r"\sin\theta \le 2\varepsilon/\delta: \ \text{right order; \ } 2\times \text{ for small } \varepsilon", font_size=34),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(BNDC2)
        whys = [why(r"two eigenvalues, \ gap $\delta$"), why(r"a $2 \times 2$ rotation"), why(r"the gap decides"), why(r"problem 4")]
        heading = label('A two-dimensional rotation shows why the eigengap matters', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> A two by two example shows why. Take eigenvalues one plus delta and one, and perturb the "
            "off-diagonal entries by epsilon. <bookmark mark='b'/> The new leading eigenvector is rotated by an angle theta "
            "with tangent of two theta equal to two epsilon over delta. <bookmark mark='c'/> With epsilon half the gap, "
            "the rotation is twenty-two and a half degrees; with epsilon five times the gap, about forty-two degrees, nearly "
            "the maximal forty-five. The size of the perturbation relative to the gap is all that matters. <bookmark "
            "mark='d'/> Davis–Kahan's bound, two epsilon over delta for the sine, has the right order: for small "
            "perturbations the true sine is about epsilon over delta, so the bound is off by a factor of two."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def dk(self):
        rows = [
            cmath(r"\text{gap } \delta", r"=", r"\lambda_1(\Sigma) - \lambda_2(\Sigma)", font_size=36),
            cmath(r"\sin\angle(\hat v_1, v_1)", r"\le", r"\frac{2\|E\|_{op}}{\delta}: \ \text{Davis--Kahan}", font_size=36),
            cmath(r"\text{bounded-spectrum Gaussian/sub-Gaussian model}", r":", r"\|E\| \asymp \|\Sigma\|(\sqrt{p/n}+p/n) \ \Rightarrow \ \sin\angle \lesssim \tfrac{\|\Sigma\|}{\delta}\sqrt{p/n}", font_size=30),
            cmath(r"\text{all of spectral clustering}", r":", r"\text{bound } \|E\|, \ \text{then Davis--Kahan}", font_size=32),
        ]
        rows[1][-1].set_color(BNDC2)
        whys = [why(r"the eigengap"), why(r"Davis \& Kahan (1970); \ Yu, \ Wang \& Samworth (2015)"), why(r"Part 51's rate"), why(r"a two-line recipe")]
        heading = label('Davis--Kahan controls an angle by perturbation divided by gap', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The right measure is the eigengap, the distance from the leading eigenvalue to the next. "
            "<bookmark mark='b'/> Chandler Davis and William Kahan's sin theta theorem of 1970, in the convenient form of Yu, "
            "Wang and Samworth from 2015, says the sine of the angle between the estimated and true eigenvectors is at most "
            "twice the perturbation's norm divided by the gap. <bookmark mark='c'/> With a sample covariance, the perturbation "
            "has norm of order the root of p over n, from Part fifty-one, so the angle is small once the gap is large compared "
            "with that. <bookmark mark='d'/> Almost every analysis of a spectral method follows this two-line recipe: bound "
            "the perturbation with a random-matrix inequality, then apply Davis–Kahan."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("dk")
        ell = np.log2([r["ell"] for r in d["rows"]])
        A = axes([-2.2, 3.2], [0, 1.08], x_length=7.4, y_length=4.4, xlabel=rf"spike $\ell$ \ (log scale), \ $n = {d['n']}$, \ $p = {d['p']}$", ylabel=r"$\sin\angle(\hat v_1, v_1)$",
                 xticks=[-2, -1, 0, 1, 2, 3], xfmt=lambda v: f"{2 ** v:g}", yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        sim = VGroup(*[Dot(ax.c2p(a, r["sin"]), radius=0.1, color=LASSOC) for a, r in zip(ell, d["rows"])])
        bnd = VGroup(polyline(ax, ell, [r["bound"] for r in d["rows"]], BNDC2, 4), *[Dot(ax.c2p(a, r["bound"]), radius=0.06, color=BNDC2) for a, r in zip(ell, d["rows"])])
        u = np.linspace(-2.2, 3.2, 200)
        from explainer.stats.kit import hdstat as HS

        g = d["p"] / d["n"]
        bbp = polyline(ax, u, np.sqrt(np.maximum(0, 1 - HS.spike_overlap(2 ** u, g))), TRUEC, 3)
        thr = DashedLine(ax.c2p(math.log2(math.sqrt(g)), 0), ax.c2p(math.log2(math.sqrt(g)), 1.08), color=SPIKEC, stroke_width=2.5)
        r = {x["ell"]: x for x in d["rows"]}
        side = fit_rows(VGroup(
            label(r"$\Sigma = I + \ell\, e_1 e_1^\top$: \ the gap is $\ell$", font_size=22),
            label(rf"purple: \ Davis--Kahan, \ vacuous until $\ell = 4$", font_size=22, color=BNDC2),
            label(rf"blue: \ simulated: \ {r[2.0]['sin']:.2f} at $\ell = 2$, \ {r[8.0]['sin']:.2f} at 8", font_size=22, color=LASSOC),
            label(r"white: \ the exact limit, \ from chapter 8's BBP overlap", font_size=22, color=TRUEC),
            label(rf"gold: \ below $\ell = \sqrt{{p/n}} = {math.sqrt(g):.2f}$, \ ordinary PCA overlap $\to0$ under the model", font_size=22, color=SPIKEC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A test: an identity covariance with one spike of size ell, so the gap is ell. <bookmark mark='b'/> Davis–Kahan's bound, in purple, is valid but crude: it says nothing until the spike reaches four. <bookmark mark='c'/> The simulated sine of the angle, in blue, is {say(r[2.0]['sin'], 2)} at a spike of two and {say(r[8.0]['sin'], 2)} at eight. <bookmark mark='d'/> The white curve is the exact limit from the spiked-model theory of chapter eight, and it runs straight through the simulation. <bookmark mark='e'/> And below a spike of the root of p over n, {say(math.sqrt(g), 2)}, the estimated eigenvector becomes asymptotically orthogonal to the truth: its directional overlap tends to zero in the proportional isotropic-spike model. The full sample can retain information, especially with known structure or a known direction. Davis–Kahan cannot see that threshold; the random-matrix theory can."     ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ curves exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(bnd), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(sim), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(bbp), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(thr), FadeIn(side[4]))
        self.clear_scene()

    def wedin(self):
        rows = fit_rows(VGroup(
            label(r"the same for singular vectors, \ and for subspaces:", font_size=28, color=GREY_A),
            label(r"Wedin (1972): \ $\sin\angle(\hat U, U) \le \sqrt2\,\|E\| / \delta_{\rm sep}$ \ with sample--population singular-value separation", font_size=26, color=BNDC2),
            label(r"spectral clustering: \ the adjacency matrix's top eigenvectors reveal the communities", font_size=26, color=BULKC),
            label(r"matrix completion's initialization; \ PCA's subspace; \ ranking from comparisons", font_size=26, color=BULKC),
            label(r"entrywise versions ($\ell_\infty$ perturbation) \ were substantially sharpened in the late 2010s", font_size=26, color=SPIKEC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The same theory covers singular vectors and whole subspaces. <bookmark mark='b'/> Per-Åke Wedin's theorem of 1972 bounds the angle between singular subspaces of a rectangular matrix by a perturbation-to-separation ratio. Wedin's separation involves the relevant sample and population singular values; a population-gap-only bound needs additional small-perturbation conditions. <bookmark mark='c'/> It underlies spectral clustering, where a network's adjacency matrix is its expected value plus noise and the top eigenvectors reveal the communities. <bookmark mark='d'/> It starts matrix completion algorithms, bounds PCA's estimated subspace, and ranks items from pairwise comparisons. <bookmark mark='e'/> Bounds on individual coordinates of eigenvectors, which say which node belongs to which community, were substantially sharpened in work from the late twenty-tens."        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

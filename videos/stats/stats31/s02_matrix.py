from __future__ import annotations

import numpy as np

from videos.stats.stats31.common import *  # noqa: F403


class DataMatrix(VoiceoverScene):
    def construct(self):
        self.card()
        self.matrix()
        self.mvn()
        self.mahalanobis_def()
        self.whiten()
        self.picture()
        self.qq()
        self.history()

    def card(self):
        card = chapter_card(1, r"The data matrix", r"Means, \ covariances, \ and distance", lit=(1936,), part=PART)
        with self.voiceover("Chapter one. The data matrix."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def matrix(self):
        rows = [
            cmath(r"X", r"=", r"(x_{ij})_{n \times p}: \ \text{rows units, \ columns variables}", font_size=30),
            cmath(r"\bar x", r"=", r"\tfrac1n X^\top \mathbf 1", font_size=32),
            cmath(r"S", r"=", r"\tfrac{1}{n - 1} (X - \mathbf 1 \bar x^\top)^\top (X - \mathbf 1 \bar x^\top)", font_size=30),
            cmath(r"R", r"=", r"D^{-1/2} S D^{-1/2}, \ \ D = \mathrm{diag}(S)", font_size=30),
        ]
        rows[2][2].set_color(PCC)
        whys = [why(r"Part 5's object"), why(r"the mean vector"), why(r"the covariance: \ $p(p+1)/2$ numbers"),
                why(r"the correlation matrix")]
        with self.voiceover(
            "<bookmark mark='a'/> Part 5 introduced the object: the data matrix, n rows of units by p columns of variables. "
            "<bookmark mark='b'/> Its column means form the mean vector. <bookmark mark='c'/> The sample covariance matrix is "
            "the cross-product of the centred data over n minus one: p variances and p times p minus one over two "
            "covariances. <bookmark mark='d'/> Scaling by the standard deviations gives the correlation matrix. Almost "
            "everything in this part is a function of these two summaries."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mvn(self):
        rows = [
            cmath(r"x", r"\sim", r"N_p(\mu, \Sigma): \ f(x) \propto \exp\{-\tfrac12 (x - \mu)^\top \Sigma^{-1} (x - \mu)\}", font_size=28),
            cmath(r"\text{contours}", r":", r"\text{ellipsoids, \ axes along the eigenvectors of } \Sigma", font_size=28),
            cmath(r"(x - \mu)^\top \Sigma^{-1} (x - \mu)", r"\sim", r"\chi^2_p", font_size=30),
            cmath(r"\hat\mu, \hat\Sigma", r":", r"\bar x \text{ and } \tfrac{n-1}{n} S \text{ are the MLEs}", font_size=30),
        ]
        rows[2][2].set_color(PCC)
        whys = [why(r"the multivariate normal, \ Part 5"), why(r"lengths $\propto$ root eigenvalues"),
                why(r"a sum of $p$ independent squared normals"), why(r"Part 22's likelihood")]
        with self.voiceover(
            "<bookmark mark='a'/> The reference model is the multivariate normal, whose density depends on x only through a "
            "quadratic form in the inverse covariance. <bookmark mark='b'/> Its contours are ellipsoids, with axes along the "
            "eigenvectors of sigma and lengths proportional to the root eigenvalues. <bookmark mark='c'/> The quadratic form "
            "itself has a chi-squared distribution with p degrees of freedom: in the right coordinates it is a sum of p "
            "independent squared standard normals. <bookmark mark='d'/> And the sample mean and covariance, with divisor n, "
            "are the maximum likelihood estimates."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mahalanobis_def(self):
        rows = [
            cmath(r"\Delta^2(x, \mu)", r"=", r"(x - \mu)^\top \Sigma^{-1} (x - \mu)", font_size=32),
            cmath(r"\Sigma = I", r":", r"\text{the Euclidean distance}", font_size=30),
            cmath(r"\text{invariant}", r":", r"x \mapsto Ax + b \ \text{changes nothing}", font_size=30),
            cmath(r"\text{meaning}", r":", r"\text{distance in units of the data's own spread, \ in every direction}", font_size=28),
        ]
        rows[0][2].set_color(MAPC)
        whys = [why(r"Mahalanobis (1936)"), why(r"uncorrelated, \ unit variance"), why(r"units and rotations don't matter"),
                why(r"a long ellipse makes some directions cheap")]
        with self.voiceover(
            "<bookmark mark='a'/> That quadratic form is Prasanta Chandra Mahalanobis's distance of 1936: the distance from x "
            "to the centre, measured with the inverse covariance. <bookmark mark='b'/> For uncorrelated variables with unit "
            "variance it is ordinary Euclidean distance. <bookmark mark='c'/> It is unchanged by any change of units or any "
            "invertible linear transformation of the variables. <bookmark mark='d'/> It measures distance in units of the "
            "data's own spread in each direction: along the long axis of the cloud, a long way is not far."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("mahal")
        two = np.asarray(d["two"])
        mu, S = np.asarray(d["mean2"]), np.asarray(d["cov2"])
        A = axes([2.6, 5.9], [0.6, 2.0], x_length=7.0, y_length=4.6, xlabel=r"petal length (cm)", ylabel=r"petal width (cm)",
                 xticks=[3, 4, 5], yticks=[1, 1.5], center=[-2.4, 0.3, 0])
        ax = A.ax
        jit = np.random.default_rng(2).uniform(-0.02, 0.02, (len(two), 2))
        pts = VGroup(*[Dot(ax.c2p(*(v + j)), radius=0.05, color=SP[1]) for v, j in zip(two, jit)])
        e1 = ellipse(ax, mu, S, 1.0, MAPC, 2.5)
        e2 = ellipse(ax, mu, S, 2.0, MAPC, 2)
        e3 = ellipse(ax, mu, S, np.sqrt(9.21), RES, 2)
        circ = Circle(radius=(ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]) * 0.6, stroke_color=GREY_B, stroke_width=2).move_to(ax.c2p(*mu))
        rows = fit_rows(VGroup(
            label(r"50 versicolor irises: \ petal length and width", font_size=22, color=SP[1]),
            label(r"grey circle: \ equal Euclidean distance", font_size=22, color=GREY_B),
            label(r"gold: \ Mahalanobis 1 and 2; \ red: \ the 99\% contour", font_size=22, color=MAPC),
            label(r"long and wide petals go together: \ the ellipse leans", font_size=22),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The fifty versicolor irises from Fisher's paper, petal length against petal width. "
            "<bookmark mark='b'/> A circle of equal Euclidean distance ignores the shape of the cloud. <bookmark mark='c'/> "
            "The Mahalanobis contours follow it: ellipses at distance one and two, and in red the contour enclosing "
            "ninety-nine percent of a normal cloud. <bookmark mark='d'/> Long petals tend to be wide, so the ellipse leans: "
            "a long, wide petal is ordinary, while a long, narrow one, at the same Euclidean distance, is unusual."
        ) as vo:
            self.add(iris_tag())
            self.play(FadeIn(A), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(circ), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(e1), Create(e2), Create(e3), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def qq(self):
        d = load("mahal")
        d2, q = np.asarray(d["d2"]), np.asarray(d["q"])
        A = axes([0, 14], [0, 14], x_length=5.4, y_length=4.6, xlabel=r"$\chi^2_4$ quantile", ylabel=r"ordered $D_i^2$",
                 xticks=[0, 4, 8, 12], yticks=[0, 4, 8, 12], center=[-2.8, 0.3, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(14, 14), color=GREY_B, stroke_width=1.5)
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=SP[1]) for a, b in zip(q, d2)])
        rows = fit_rows(VGroup(
            label(r"all four measurements: \ squared distances from the mean", font_size=22),
            label(r"against $\chi^2_4$ quantiles: \ close to the line", font_size=22, color=SP[1]),
            label(rf"largest {max(d2):.1f}; \ the 97.5\% cut-off is {d['cut']:.1f}", font_size=22, color=RES),
            label(r"the most outlying by Mahalanobis \ $\neq$ \ the farthest by Euclid", font_size=22, color=MAPC),
        ), 4.6, 0.42, [4.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A multivariate normality check in one picture: the squared Mahalanobis distances of all "
            "fifty versicolors, using all four measurements. <bookmark mark='b'/> Plotted against chi-squared quantiles with "
            "four degrees of freedom they follow the line, so a normal model is reasonable. <bookmark mark='c'/> The largest "
            "is twelve and a half, just beyond the ninety-seven and a half percent cut-off, unremarkable in a sample of "
            "fifty. <bookmark mark='d'/> And the most outlying flower in this metric is not the one farthest from the mean in "
            "Euclidean terms: distance depends on direction."
        ) as vo:
            self.add(iris_tag())
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.03), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def history(self):
        rows = fit_rows(VGroup(
            label(r"Mahalanobis built it for anthropometry of castes in Bengal", font_size=24),
            label(r"Fisher's iris paper appeared in the \emph{Annals of Eugenics}", font_size=24, color=RES),
            label(r"the methods outlived the purposes: \ we use them, \ and say where they came from", font_size=24, color=PATH),
            label(r"Mahalanobis also founded the Indian Statistical Institute \ (1931)", font_size=24, color=MAPC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A word on history. Mahalanobis designed his distance to compare body measurements of castes "
            "and communities in Bengal. <bookmark mark='b'/> Fisher's discriminant and the iris data appeared in the Annals "
            "of Eugenics, the journal of a movement whose aims this course does not share. <bookmark mark='c'/> The methods "
            "have long outlived those purposes, and the honest course is to use them while saying plainly where they came "
            "from. <bookmark mark='d'/> Mahalanobis also founded the Indian Statistical Institute and designed India's "
            "national sample surveys, a different legacy."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def whiten(self):
        rows = [
            cmath(r"z", r"=", r"\Sigma^{-1/2} (x - \mu)", font_size=32),
            cmath(r"\mathrm{Cov}(z)", r"=", r"I_p", font_size=32),
            cmath(r"\Delta^2(x, \mu)", r"=", r"\|z\|^2", font_size=32),
            cmath(r"\text{many square roots}", r":", r"\Sigma^{-1/2}, \ L^{-1} \text{ (Cholesky)}, \ \text{any } Q \Sigma^{-1/2}", font_size=28),
        ]
        rows[2][-1].set_color(MAPC)
        whys = [why(r"whitening"), why(r"uncorrelated, \ unit variance"), why(r"Mahalanobis is Euclidean, \ after whitening"), why(r"they differ by a rotation")]
        with self.voiceover(
            "<bookmark mark='a'/> There is a cleaner way to see it. Multiply the centred data by the inverse square "
            "root of the covariance. <bookmark mark='b'/> The new variables are uncorrelated with unit variance: the "
            "cloud has been made round, or whitened. <bookmark mark='c'/> And the Mahalanobis distance is just the "
            "ordinary Euclidean length of the whitened vector. Every Mahalanobis calculation is a Euclidean one in "
            "disguise. <bookmark mark='d'/> Whitening is not unique: the symmetric square root, the inverse Cholesky "
            "factor, or either followed by a rotation all work, because rotations do not change lengths."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

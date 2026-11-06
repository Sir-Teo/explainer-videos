from __future__ import annotations

import numpy as np

from explainer.stats.kit import spatial as SPK
from videos.stats.stats39.common import *  # noqa: F403


def grid_surface(vals, center, width, lo=-2.5, hi=2.5):
    v = np.asarray(vals, float)
    ny, nx = v.shape
    X, Y = np.meshgrid(np.arange(nx) * 1.0, np.arange(ny) * 1.0)
    return FieldSurface(X.ravel(), Y.ravel(), v.ravel(), 1.0, width=width, center=center, lo=lo, hi=hi)


class GMRF(VoiceoverScene):
    def construct(self):
        self.card()
        self.markov()
        self.sparsity()
        self.spde()
        self.condition()
        self.inla()

    def card(self):
        card = chapter_card(8, r"Markov random fields", r"Sparse precision, \ not sparse covariance", lit=(1974, 2011), part=PART)
        with self.voiceover("Chapter eight. Markov random fields."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def markov(self):
        rows = [
            cmath(r"Q", r"=", r"\Sigma^{-1}: \ \text{the precision matrix}", font_size=32),
            cmath(r"Q_{ij} = 0", r"\iff", r"W_i \perp W_j \mid W_{-ij}", font_size=32),
            cmath(r"E[W_i \mid W_{-i}]", r"=", r"-\textstyle\sum_{j \sim i} (Q_{ij}/Q_{ii})\, W_j", font_size=30),
            cmath(r"\text{Besag (1974)}", r":", r"\text{specify the conditionals; \ the joint follows}", font_size=30),
        ]
        rows[1][-1].set_color(FIELDC)
        whys = [why(r"Part 31's partial correlations"), why(r"zeros = conditional independence"), why(r"only neighbours enter"),
                why(r"Hammersley--Clifford")]
        with self.voiceover(
            "<bookmark mark='a'/> A different route to speed works with the precision matrix, the inverse covariance, "
            "rather than the covariance. <bookmark mark='b'/> As in Part thirty-one's graphical models, a zero in the "
            "precision means two values are conditionally independent given all the others. <bookmark mark='c'/> The "
            "conditional mean of each value is then a weighted average of its neighbours alone. <bookmark mark='d'/> Julian "
            "Besag showed in 1974 how to build a valid joint distribution on a lattice from such local conditionals: a "
            "Gaussian Markov random field."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sparsity(self):
        d = load("gmrf")
        Qs = SPK.gmrf_precision(12, 8, 0.35).toarray()
        pat = Qs != 0
        N = pat.shape[0]
        cell = 5.2 / N
        sq = VGroup()
        for i in range(N):
            for j in range(N):
                if pat[i, j]:
                    sq.add(Square(cell * 0.92, stroke_width=0, fill_color=TAUC if i == j else FIELDC, fill_opacity=1)
                           .move_to([-3.4 + (j - (N - 1) / 2) * cell, 0.1 - (i - (N - 1) / 2) * cell, 0]))
        frame = Square(cell * N, stroke_color=GREY_B, stroke_width=1.5).move_to([-3.4, 0.1, 0])
        side = fit_rows(VGroup(
            label(rf"a {d['nx']} $\times$ {d['ny']} lattice: \ $n = {d['n']:,}$", font_size=24),
            label(r"left: \ the precision of a 12 $\times$ 8 one, \ in full", font_size=24, color=FIELDC),
            label(rf"nonzeros: \ {d['nnz']:,} \ of {d['dense']:,}", font_size=24, color=TAUC),
            label(rf"that is {100 * d['nnz'] / d['dense']:.2f}\%: \ each value talks to 12 neighbours", font_size=24, color=BANDC),
            label(r"sparse Cholesky: \ about $O(n^{3/2})$ in two dimensions", font_size=24, color=GREY_A),
        ), 5.2, 0.42, [3.7, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is a lattice of sixty by forty, two thousand four hundred values. <bookmark "
            "mark='b'/> On the left, the whole precision matrix of a small twelve by eight version: a few diagonal "
            "bands, for the neighbours in the same row of the lattice and in the rows above and below. <bookmark "
            "mark='c'/> Of the " + f"{d['dense']:,}" + " entries, only " + f"{d['nnz']:,}" + " are nonzero, <bookmark mark='d'/> "
            "because each value interacts only with the twelve closest. <bookmark mark='e'/> Sparse Cholesky factorization "
            "on a two-dimensional lattice costs about n to the three halves, instead of n cubed."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(frame), FadeIn(sq), FadeIn(side[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k + 2]))
        self.clear_scene()

    def spde(self):
        rows = [
            cmath(r"(\kappa^2 - \Delta)^{\alpha/2}\, W", r"=", r"\text{white noise}, \ \ \alpha = \nu + d/2", font_size=30),
            cmath(r"\text{solution}", r":", r"\text{a Mat\'ern field, \ range } \rho = \sqrt{8\nu}/\kappa", font_size=30),
            cmath(r"\alpha = 2", r":", r"Q = \tau (\kappa^2 I + G)^\top (\kappa^2 I + G), \ \ G = \text{the graph Laplacian}", font_size=28),
            cmath(r"\text{Lindgren, Rue \& Lindstr\"om (2011)}", r":", r"\text{finite elements on any mesh}", font_size=28),
        ]
        rows[2][-1].set_color(FIELDC)
        whys = [why(r"Whittle's SPDE"), why(r"$\nu = 1$ in two dimensions"), why(r"a discretized operator: \ sparse"),
                why(r"the SPDE approach")]
        with self.voiceover(
            "<bookmark mark='a'/> The bridge from Matérn fields to sparse precisions is Whittle's equation from chapter "
            "five. <bookmark mark='b'/> Its solutions are exactly Matérn fields, with the range set by kappa. <bookmark "
            "mark='c'/> Discretize the operator on a grid, and the precision is a square of a sparse matrix built from the "
            "graph Laplacian: this is what made the sparsity pattern we just saw. <bookmark mark='d'/> Finn Lindgren, "
            "Håvard Rue and Johan Lindström showed in 2011 how to do this with finite elements on any triangulated mesh, "
            "including irregular regions and the sphere. A continuous Matérn field, with the speed of a Markov field."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def condition(self):
        d = load("gmrf")
        u, mu = np.asarray(d["u"], float), np.asarray(d["mu"], float)
        nx = d["nx"]
        F1 = grid_surface(u, [-3.3, 0.5, 0], 5.8)
        F2 = grid_surface(mu, [3.3, 0.5, 0], 5.8)
        obs = np.asarray(d["obs"], int)
        pts = F2.dots(obs % nx, obs // nx, WHITE, 0.035)
        t1 = label(r"a GMRF sample \ ($n = 2{,}400$)", font_size=22, color=TRUEC).next_to(F1, UP, buff=0.1)
        t2 = label(r"its conditional mean from 150 noisy values \ (white)", font_size=22, color=FIELDC).next_to(F2, UP, buff=0.1)
        foot = fit_rows(VGroup(
            label(r"conditioning: \ solve $(Q + A^\top A/\sigma_\varepsilon^2)\, \mu = A^\top y/\sigma_\varepsilon^2$ \ with a sparse solver", font_size=22, color=BANDC),
            label(rf"RMSE against the sample: \ {d['rmse']:.2f} \ (the field's SD is 1)", font_size=22, color=GREY_A),
        ), 12.4, 0.25, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the left, a sample from this Markov field, drawn through a sparse Cholesky factor. "
            "<bookmark mark='b'/> On the right, its conditional mean given a hundred and fifty noisy observations, in white. "
            "<bookmark mark='c'/> The conditioning is one sparse linear solve: the precision of the posterior is the prior "
            "precision plus a diagonal term at the observed sites. <bookmark mark='d'/> The reconstruction misses by "
            + say(d["rmse"], 2) + " standard deviations: the large features are recovered, the small ones between "
            "observations are not, and could not be."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(F1), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(F2), FadeIn(t2), FadeIn(pts))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def inla(self):
        rows = fit_rows(VGroup(
            label(r"INLA \ (Rue, \ Martino \& Chopin 2009): \ Laplace approximations, \ nested", font_size=26, color=TAUC),
            label(r"latent Gaussian models: \ a GMRF inside any GLM \ (Parts 24, \ 27)", font_size=26, color=FIELDC),
            label(r"posterior marginals in seconds to minutes, \ where MCMC takes hours", font_size=26, color=BANDC),
            label(r"the price: \ approximate, \ and limited to models with a Gaussian latent layer", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Håvard Rue, Sara Martino and Nicolas Chopin built on the Markov structure an "
            "approximation method called INLA, the integrated nested Laplace approximation of 2009. <bookmark mark='b'/> It "
            "handles latent Gaussian models: a Markov random field, or the SPDE field, inside a generalized linear model, "
            "for counts, rates or binary outcomes. <bookmark mark='c'/> It gives posterior marginals in seconds or minutes "
            "where MCMC, Part twenty-seven, takes hours. <bookmark mark='d'/> The price is that it is an approximation, and "
            "only for models whose latent layer is Gaussian. For spatial epidemiology, it became the standard tool."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

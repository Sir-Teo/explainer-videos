from __future__ import annotations

import numpy as np

from videos.stats.stats27.common import *  # noqa: F403


class Laplace(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.compare()
        self.evidence()
        self.inla()
        self.guide()

    def card(self):
        card = chapter_card(11, r"Laplace and INLA", r"A normal at the mode", lit=(2009,), part=PART)
        with self.voiceover("Chapter eleven. Laplace approximations and INLA."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\hat\theta", r"=", r"\arg\max \log p(\theta \mid y)", font_size=32),
            cmath(r"p(\theta \mid y)", r"\approx", r"N\bigl(\hat\theta, \ [-\nabla^2 \log p(\hat\theta \mid y)]^{-1}\bigr)", font_size=30),
            cmath(r"\text{cost}", r":", r"\text{one optimization and one Hessian}", font_size=30),
            cmath(r"\text{good when}", r":", r"\text{the posterior is nearly normal: \ Part 26's regular BvM setting}", font_size=30),
        ]
        rows[1][2].set_color(HIT)
        whys = [why(r"the posterior mode"), why(r"Laplace (1774), \ Part 22"), why(r"no sampling at all"),
                why(r"bad for skewed, \ bounded or multimodal posteriors")]
        with self.voiceover(
            "<bookmark mark='a'/> The oldest approximation is Laplace's: find the posterior mode, <bookmark "
            "mark='b'/> and replace the posterior by a normal there whose covariance is the inverse of the curvature."
            " <bookmark mark='c'/> One optimization and one Hessian, with no sampling at all. <bookmark mark='d'/> It"
            " is as good as the posterior is normal, so regular fixed-dimensional asymptotics can justify it with "
            "growing data. Skewness, boundaries and multiple modes can make it inaccurate."
        ) as vo:
            intro = label('Laplace fits a Gaussian to local posterior curvature', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def compare(self):
        d = load("laplace")
        group = VGroup()
        anims = []
        for k, key in enumerate(("small", "large")):
            P_ = d[key]
            g, nu, la = np.asarray(P_["grid"]), np.asarray(P_["nuts"]), np.asarray(P_["laplace"])
            A = axes([float(g[0]), float(g[-1])], [0, float(max(nu.max(), la.max())) * 1.15], x_length=5.2, y_length=3.4,
                     xlabel=rf"logistic slope, \ $n = {P_['n']}$", ylabel=r"", xticks=[], yticks=[], center=[-3.3 + 6.6 * k, 0.8, 0])
            c1 = curve(A.ax, g, nu, SAMPLER, 3)
            c2 = DashedVMobject(curve(A.ax, g, la, HIT, 3), num_dashes=40)
            info = label(rf"95\% point: \ NUTS {P_['q95_nuts']:.2f}, \ Laplace {P_['q95_lap']:.2f}", font_size=22,
                         color=RES if key == "small" else HIT).next_to(A, DOWN, buff=0.3)
            group.add(A)
            anims.append((c1, c2, info))
        foot = fit_rows(VGroup(
            label(r"blue: \ NUTS; \ green dashed: \ Laplace at the mode", font_size=22),
            label(r"small $n$: \ a skewed posterior, \ the upper tail missed; \ large $n$: \ the same curve", font_size=22, color=GREY_A),
        ), 12.0, 0.2, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A logistic regression with a normal prior, fitted both ways. <bookmark mark='b'/> "
            "With twenty observations, the posterior for the slope is skewed: its upper tail stretches to five point "
            "five five, while Laplace's symmetric normal has a ninety-fifth percentile of four point seven seven. "
            "<bookmark mark='c'/> With four hundred observations the two curves coincide, and the two methods give "
            "similar answers in this example."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(group), FadeIn(foot[0]))
            vo.wait_until("a")
            for k, m_ in enumerate("bc"):
                vo.wait_until(m_)
                c1, c2, info = anims[k]
                self.play(Create(c1), Create(c2), FadeIn(info))
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def inla(self):
        rows = [
            cmath(r"y \mid x, \theta", r"\sim", r"\text{tractable observation model; \ } x\mid\theta\sim N(0,Q(\theta)^{-1})", font_size=28),
            cmath(r"\tilde p(\theta \mid y)", r"\propto", r"\dfrac{p(y \mid x, \theta)\, p(x \mid \theta)\, p(\theta)}{\tilde p_G(x \mid \theta, y)}\Big|_{x = x^*(\theta)}", font_size=28),
            cmath(r"\text{then}", r":", r"\text{integrate over a few } \theta \text{ points; \ Laplace again for each } x_i", font_size=28),
            cmath(r"\text{use}", r":", r"\text{suitable sparse latent-Gaussian models; \ few hyperparameters}", font_size=30),
        ]
        rows[1][2].set_color(HIT)
        whys = [why(r"latent Gaussian models: \ Part 25's GLMMs"), why(r"a Laplace approximation inside the marginal"),
                why(r"nested: \ hence INLA"), why(r"Rue, Martino \& Chopin (2009); \ Part 39")]
        with self.voiceover(
            "<bookmark mark='a'/> Håvard Rue, Sara Martino and Nicolas Chopin's INLA pushes Laplace's idea far. It "
            "targets latent Gaussian models, Part 25's generalized linear mixed models and their spatial cousins: "
            "thousands of Gaussian latent effects and a handful of hyperparameters. <bookmark mark='b'/> It "
            "approximates the hyperparameters' posterior by dividing the joint density by a Gaussian approximation to"
            " the latent field, evaluated at its mode, <bookmark mark='c'/> integrates over a small grid of "
            "hyperparameter values, and applies Laplace again for each latent effect: integrated nested Laplace "
            "approximation. <bookmark mark='d'/> For suitable sparse latent-Gaussian models with few hyperparameters,"
            " it can be much faster than MCMC. Accuracy and speed depend on the model; Part 39 returns to these "
            "methods."
        ) as vo:
            intro = label('INLA nests approximations for suitable latent Gaussian models', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def evidence(self):
        rows = [
            cmath(r"\log p(y)", r"\approx", r"\log p(y, \hat\theta) + \tfrac d2 \log 2\pi - \tfrac12 \log\det H", font_size=28),
            cmath(r"\text{large } n", r":", r"\text{gives BIC}", font_size=30),
            cmath(r"\text{also}", r":", r"\text{each group's integral in Part 25's GLMMs}", font_size=30),
            cmath(r"\text{better}", r":", r"\text{adaptive quadrature, \ or SMC}", font_size=30),
        ]
        rows[0][-1].set_color(HIT)
        whys = [why(r"Laplace's method for the evidence"), why(r"Part 26, \ chapter six"), why(r"lme4's default"), why(r"chapter nine")]
        with self.voiceover(
            "<bookmark mark='a'/> Laplace's method also approximates the evidence: the joint density at the mode, "
            "times the volume of the normal fitted there, computed from the determinant of the Hessian. <bookmark "
            "mark='b'/> Under regular fixed-dimensional assumptions and a suitable fixed prior, retaining the leading"
            " terms gives BIC. Order-one prior and curvature terms remain in Laplace's expression. <bookmark "
            "mark='c'/> It is also how Part 25 integrated each school's random effect in the mixed logistic model. "
            "<bookmark mark='d'/> When it isn't accurate enough, adaptive quadrature in low dimensions, or chapter "
            "nine's tempered SMC, do better."
        ) as vo:
            intro = label('Laplace evidence retains prior and curvature constants', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def guide(self):
        hdr = [r"\textbf{method}", r"\textbf{exact in the limit?}", r"\textbf{scales to}", r"\textbf{watch for}"]
        body = [[r"grid", r"yes", r"1--3 parameters", r"the curse of dimension"],
                [r"importance sampling", r"yes", r"a good proposal", r"$\hat k > 0.7$"],
                [r"Gibbs", r"yes", r"conjugate pieces", r"dependence"],
                [r"NUTS", r"yes", r"thousands of parameters", r"divergences, \ $\hat R$"],
                [r"SMC", r"yes, \ in particles", r"evidences, \ streams", r"degeneracy"],
                [r"Laplace, \ INLA", r"no", r"latent Gaussian models", r"skewness"],
                [r"VI", r"no", r"millions of parameters", r"too-narrow posteriors"],
                [r"ABC", r"yes if sufficient, zero tolerance", r"simulators only", r"the summaries"]]
        tb = table_rows([hdr] + body, font_size=22, col_buff=0.6, row_buff=0.22, colors=[GREY_A, EXACTC, SAMPLER, SAMPLER, HIT, HIT, VIC, VIC, RES])
        tb.move_to([0, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The whole toolkit on one page. Grids, importance sampling, Gibbs, NUTS and SMC are "
            "exact in the limit of more computation; <bookmark mark='b'/> Laplace, INLA and a fixed variational "
            "family retain approximation error. ABC at fixed summaries and tolerance does too, but sufficient "
            "summaries and vanishing tolerance can recover the full posterior under regularity conditions. <bookmark "
            "mark='c'/> Each has its domain and its characteristic failure, and its own warning sign. Most applied "
            "work today starts with NUTS, and reaches for the others when the model is too big, too slow or has no "
            "likelihood."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r) for r in tb[1:6]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[6:]], lag_ratio=0.2))
        self.wait(2.0)
        self.clear_scene()

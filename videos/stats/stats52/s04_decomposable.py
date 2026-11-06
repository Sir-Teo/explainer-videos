from __future__ import annotations

from videos.stats.stats52.common import *  # noqa: F403


class Decomposable(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.theorem()
        self.examples()
        self.rsc()
        self.rates()

    def card(self):
        card = chapter_card(3, r"Decomposable regularizers", r"One theorem for sparse, \ group and low-rank problems", lit=(2012,), part=PART)
        with self.voiceover("Chapter three. Decomposable regularizers: one theorem for sparse, group and low-rank problems."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\hat\theta", r"=", r"\arg\min \ \mathcal L_n(\theta) + \lambda\,\mathcal R(\theta)", font_size=36),
            cmath(r"\text{a model subspace } \mathcal M", r":", r"\text{where the truth lives \ (a support, \ a column space)}", font_size=32),
            cmath(r"\text{decomposable}", r":", r"\mathcal R(u + v) = \mathcal R(u) + \mathcal R(v), \ u \in \mathcal M, \ v \in \mathcal M^\perp", font_size=32),
            cmath(r"\text{the } \ell_1 \text{ norm}", r":", r"\|u + v\|_1 = \|u\|_1 + \|v\|_1 \text{ for disjoint supports}", font_size=32),
        ]
        rows[2][-1].set_color(BNDC2)
        whys = [why(r"loss plus penalty"), why(r"the structure"), why(r"Negahban et al. (2012)"), why(r"the lasso's case")]
        with self.voiceover(
            "<bookmark mark='a'/> The lasso's proof used two properties, and Sahand Negahban, Pradeep Ravikumar, Martin "
            "Wainwright and Bin Yu saw in 2012 that they are all that is needed. Take any loss plus a penalty. <bookmark "
            "mark='b'/> Suppose the truth lives in a model subspace: a support for sparse vectors, a pair of row and column "
            "spaces for low-rank matrices. <bookmark mark='c'/> The penalty is decomposable if, for a vector in the model "
            "subspace and one in its orthogonal complement, the penalty of the sum is the sum of the penalties. <bookmark "
            "mark='d'/> The l-one norm is the example: vectors with disjoint supports have additive l-one norms, which is "
            "exactly what forced the lasso's error into its cone."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def theorem(self):
        rows = [
            cmath(r"\lambda \ge 2\,\mathcal R^*(\nabla\mathcal L_n(\theta^*))", r"\Rightarrow", r"\Delta \in \mathcal C: \ \mathcal R(\Delta_{\mathcal M^\perp}) \le 3\mathcal R(\Delta_{\mathcal M})", font_size=30),
            cmath(r"\text{restricted strong convexity}", r":", r"\mathcal L_n(\theta^* + \Delta) - \mathcal L_n(\theta^*) - \langle\nabla\mathcal L_n, \Delta\rangle \ge \kappa\|\Delta\|^2", font_size=28),
            cmath(r"\Psi(\mathcal M)", r"=", r"\sup_{u \in \mathcal M} \mathcal R(u)/\|u\|: \ \text{the subspace compatibility}", font_size=32),
            cmath(r"\|\hat\theta - \theta^*\|", r"\lesssim", r"\Psi(\mathcal M)\,\lambda/\kappa", font_size=38),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"$\mathcal R^*$: \ the dual norm"), why(r"RE, \ for any loss, \ on $\mathcal C$"), why(r"$\sqrt s$ for $\ell_1$"), why(r"one theorem")]
        with self.voiceover(
            "<bookmark mark='a'/> The theorem has three ingredients. If lambda is at least twice the dual norm of the loss's "
            "gradient at the truth, the error lies in a cone, just as for the lasso. <bookmark mark='b'/> If the loss is "
            "strongly convex in the directions of that cone, restricted strong convexity, the general form of the restricted "
            "eigenvalue, <bookmark mark='c'/> and if the subspace compatibility constant measures how large the penalty can be "
            "relative to the norm on the model subspace, which is root s for the l-one norm on s coordinates, <bookmark "
            "mark='d'/> then the error is at most a constant times the compatibility constant times lambda over kappa. Every "
            "rate in this part is an instance."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def examples(self):
        rows = [[r"problem", r"penalty $\mathcal R$", r"$\Psi(\mathcal M)$", r"$\lambda \asymp$", r"rate"],
                [r"sparse regression", r"$\|\beta\|_1$", r"$\sqrt s$", r"$\sqrt{\log p / n}$", r"$\sqrt{s\log p/n}$"],
                [r"group sparsity", r"$\sum_g \|\beta_g\|_2$", r"$\sqrt{s_g}$", r"$\sqrt{(m + \log G)/n}$", r"$\sqrt{s_g(m + \log G)/n}$"],
                [r"low rank", r"$\|\Theta\|_*$", r"$\sqrt{2r}$", r"$\sqrt{(p_1 + p_2)/n}$", r"$\sqrt{r(p_1 + p_2)/n}$"],
                [r"sparse GLMs", r"$\|\beta\|_1$", r"$\sqrt s$", r"$\sqrt{\log p / n}$", r"$\sqrt{s\log p/n}$"]]
        tab = table_rows(rows, font_size=26, col_buff=0.55, row_buff=0.45, colors=[GREY_B, LASSOC, BULKC, SPIKEC, GOODC])
        if tab.width > 12.8:
            tab.width = 12.8
        tab.move_to([0, 0.7, 0])
        foot = label(r"$G$ groups of size $m$, \ $s_g$ of them active; \ rank $r$; \ the same proof every time", font_size=24, color=GREY_A).move_to([0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The theorem's instances, row by row. Sparse regression with the l-one norm: compatibility "
            "root s, lambda of order root log p over n, and the lasso's rate. Group sparsity with the group lasso of Part "
            "thirty-two: G groups of size m, s g of them active, and a rate with m plus log G in place of log p. Low-rank "
            "matrices with the nuclear norm, the sum of singular values: compatibility root two r, and a rate of root r times "
            "the dimensions over n. And sparse generalized linear models, where the loss is a log-likelihood and restricted "
            "strong convexity replaces the restricted eigenvalue. <bookmark mark='b'/> The same three-line proof, every time."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def rsc(self):
        rows = [
            cmath(r"\text{logistic loss}", r":", r"\mathcal L_n(\beta) = \tfrac1n\textstyle\sum_i \big(\log(1 + e^{x_i^\top\beta}) - y_i x_i^\top\beta\big)", font_size=30),
            cmath(r"\text{its curvature}", r":", r"\tfrac1n\textstyle\sum_i \pi_i(1 - \pi_i)(x_i^\top\Delta)^2: \ \text{flat where } \pi_i \to 0, 1", font_size=30),
            cmath(r"\text{RSC}", r":", r"\delta\mathcal L \ge \kappa\|\Delta\|^2 - \tau\tfrac{\log p}{n}\|\Delta\|_1^2 \ \text{ for } \|\Delta\| \le 1", font_size=30),
            cmath(r"\text{so}", r":", r"\text{the } \ell_1\text{-penalized logistic regression attains } \sqrt{s\log p/n}", font_size=30),
        ]
        rows[2][-1].set_color(BNDC2)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Part 24's GLM"), why(r"the Fisher information"), why(r"Negahban et al.; \ local only"), why(r"the same theorem")]
        with self.voiceover(
            "<bookmark mark='a'/> One instance deserves a closer look, because the loss is not quadratic: l-one-penalized "
            "logistic regression, Part twenty-four's model with many predictors. <bookmark mark='b'/> Its curvature is a "
            "weighted version of the design's, with weights pi times one minus pi, which vanish when fitted probabilities "
            "approach zero or one. <bookmark mark='c'/> So strong convexity can hold only locally, near the truth, and only "
            "up to a tolerance term of order log p over n times the squared l-one norm: restricted strong convexity, in the "
            "form Negahban and colleagues proved for generalized linear models. <bookmark mark='d'/> It is enough: the "
            "penalized logistic regression attains the same root s log p over n rate as the lasso."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rates(self):
        rows = fit_rows(VGroup(
            label(r"and they are the right rates:", font_size=28, color=GREY_A),
            label(r"$s\log(p/s)/n$ \ is Part 50's Fano lower bound for sparse vectors: \ the lasso is minimax", font_size=26, color=GOODC),
            label(r"$r(p_1 + p_2)/n$ \ matches the degrees of freedom of a rank-$r$ matrix", font_size=26, color=BULKC),
            label(r"the price is the restricted curvature: \ no curvature on the cone, \ no rate", font_size=26, color=BADC),
            label(r"and a computable estimator: \ every one of these is a convex program", font_size=26, color=SPIKEC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> And these are the right rates. <bookmark mark='b'/> s log of p over s, over n, is exactly "
            "Part fifty's Fano lower bound for sparse vectors, so the lasso is minimax up to the log factor's argument. "
            "<bookmark mark='c'/> r times the sum of the dimensions, over n, matches the number of free parameters in a "
            "rank-r matrix. <bookmark mark='d'/> The price is curvature: if the loss is flat in some direction of the cone, no "
            "rate follows. <bookmark mark='e'/> And each estimator is a convex program, so the minimax rates of Part fifty are "
            "achieved here by algorithms that run in polynomial time, unlike sparse PCA's, in chapter ten."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

from __future__ import annotations

import numpy as np

from videos.stats.stats31.common import *  # noqa: F403


def regions(ax, gx, gy, Z, opacity=0.18):
    """Filled runs of equal class on each grid row: one rectangle per run."""
    g = VGroup()
    dx, dy = gx[1] - gx[0], gy[1] - gy[0]
    for i, y in enumerate(gy):
        row = Z[i]
        j = 0
        while j < len(row):
            k = j
            while k + 1 < len(row) and row[k + 1] == row[j]:
                k += 1
            a, b = ax.c2p(gx[j] - dx / 2, y - dy / 2), ax.c2p(gx[k] + dx / 2, y + dy / 2)
            g.add(Rectangle(width=b[0] - a[0], height=b[1] - a[1], stroke_width=0, fill_color=SP[int(row[j])],
                            fill_opacity=opacity).move_to((a + b) / 2))
            j = k + 1
    return g


def boundaries(ax, gx, gy, Z, color, radius=0.022):
    """The class boundary as a dotted contour: a dot wherever neighbouring grid cells (along a row or a column) differ."""
    g = VGroup()
    for i in range(len(gy)):
        for j in range(len(gx) - 1):
            if Z[i, j] != Z[i, j + 1]:
                g.add(Dot(ax.c2p((gx[j] + gx[j + 1]) / 2, gy[i]), radius=radius, color=color))
    for j in range(len(gx)):
        for i in range(len(gy) - 1):
            if Z[i, j] != Z[i + 1, j]:
                g.add(Dot(ax.c2p(gx[j], (gy[i] + gy[i + 1]) / 2), radius=radius, color=color))
    return g


class LDA(VoiceoverScene):
    def construct(self):
        self.card()
        self.fisher()
        self.bayes()
        self.logistic()
        self.picture()
        self.plane()
        self.errors()
        self.history()

    def card(self):
        card = chapter_card(7, r"Discriminant analysis", r"Separating groups you already know", lit=(1936,), part=PART)
        with self.voiceover("Chapter seven. Discriminant analysis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def fisher(self):
        rows = [
            cmath(r"\max_a", r"", r"\dfrac{a^\top B a}{a^\top W a}", font_size=34),
            cmath(r"W^{-1} B a", r"=", r"\lambda a", font_size=32),
            cmath(r"g = 2", r":", r"a \propto W^{-1} (\bar x_1 - \bar x_2)", font_size=30),
            cmath(r"g \text{ groups}", r":", r"\text{up to } \min(g - 1, p) \text{ discriminant directions}", font_size=30),
        ]
        rows[1][-1].set_color(SP[2])
        whys = [why(r"between over within: \ Fisher (1936)"), why(r"MANOVA's eigenproblem"), why(r"chapter three's direction"),
                why(r"Rao (1948)")]
        with self.voiceover(
            "<bookmark mark='a'/> Fisher's question in 1936: which linear combination of the measurements best separates "
            "groups we already know? He maximized the between-group variance relative to the within-group variance. "
            "<bookmark mark='b'/> The answer is an eigenvector of W inverse B, MANOVA's eigenproblem from chapter three. "
            "<bookmark mark='c'/> With two groups it is W inverse times the difference in means, the direction that "
            "maximized Hotelling's t. <bookmark mark='d'/> C. R. Rao extended the idea to many groups in 1948: with g groups "
            "there are up to g minus one discriminant directions."
        ) as vo:
            intro=label('Discriminant directions compare between-group and within-group variation',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bayes(self):
        rows = [
            cmath(r"x \mid g", r"\sim", r"N_p(\mu_g, \Sigma_g), \ \ \text{prior } \pi_g", font_size=30),
            cmath(r"\Sigma_g = \Sigma", r":", r"\log \tfrac{P(g \mid x)}{P(h \mid x)} \ \text{is linear in } x", font_size=30),
            cmath(r"\Sigma_g \text{ free}", r":", r"\text{quadratic in } x: \ \text{QDA}", font_size=30),
            cmath(r"\text{parameters}", r":", r"\text{LDA } p(p+1)/2, \ \ \text{QDA } g \cdot p(p+1)/2", font_size=30),
        ]
        rows[1][-1].set_color(SP[2])
        whys = [why(r"a model for each group"), why(r"LDA: \ Fisher's rule is Bayes's"), why(r"curved boundaries"),
                why(r"bias against variance, \ Part 19")]
        with self.voiceover(
            "<bookmark mark='a'/> There is also a probabilistic route. Suppose each group is normal with its own mean"
            " and covariance. <bookmark mark='b'/> If the covariances are equal, the log odds of one group against "
            "another are linear in x, and the Bayes classifier draws straight boundaries: linear discriminant "
            "analysis, and for two groups it uses Fisher's direction, with the threshold also depending on priors and"
            " losses. <bookmark mark='c'/> Let each group have its own covariance and the boundaries become "
            "quadratic. <bookmark mark='d'/> QDA estimates g times as many covariance parameters, a trade between "
            "bias and variance, Part 19's theme."
        ) as vo:
            intro=label('Gaussian within-group models give linear or quadratic decision rules',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("lda")
        P, y = np.asarray(d["proj"]), np.asarray(d["y"]).astype(int)
        A = axes([-11.5, 8.5], [3.6, 9.8], x_length=8.0, y_length=4.8, xlabel=r"first discriminant", ylabel=r"second discriminant",
                 xticks=[-10, -5, 0, 5], yticks=[4, 6, 8], center=[-1.8, 0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=SP[k]) for (a, b), k in zip(P, y)])
        rows = fit_rows(VGroup(
            label(r"blue setosa, \ green versicolor, \ purple virginica", font_size=22),
            label(rf"first direction: \ {100 * d['share'][0]:.1f}\% of the separation", font_size=22, color=SP[2]),
            label(r"setosa far apart; \ the other two touch", font_size=22),
        ), 3.6, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> All hundred and fifty irises projected onto Rao's two discriminant directions. "
            "<bookmark mark='b'/> The first direction carries ninety-nine percent of the separation; the second adds almost "
            "nothing. <bookmark mark='c'/> Setosa sits far away on its own; versicolor and virginica overlap a little at "
            "their edges."
        ) as vo:
            self.add(iris_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.01), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def plane(self):
        d = load("lda")
        X2, y = np.asarray(d["X2"]), np.asarray(d["y"]).astype(int)
        gx, gy = np.asarray(d["grid_x"]), np.asarray(d["grid_y"])
        Zl, Zq = np.asarray(d["lda2"]).astype(int), np.asarray(d["qda2"]).astype(int)
        A = axes([0.5, 7.5], [-0.2, 2.8], x_length=7.6, y_length=4.8, xlabel=r"petal length (cm)", ylabel=r"petal width (cm)",
                 xticks=[1, 3, 5, 7], yticks=[0, 1, 2], center=[-2.0, 0.2, 0])
        ax = A.ax
        reg = regions(ax, gx, gy, Zl)
        bl = boundaries(ax, gx, gy, Zl, WHITE, 0.018)
        bq = boundaries(ax, gx, gy, Zq, MAPC, 0.024)
        jit = np.random.default_rng(4).uniform(-0.03, 0.03, X2.shape)
        dots = VGroup(*[Dot(ax.c2p(*(v + j)), radius=0.045, color=SP[k]) for v, j, k in zip(X2, jit, y)])
        rows = fit_rows(VGroup(
            label(r"two variables only: \ petal length and width", font_size=22),
            label(r"white: \ LDA's straight boundaries", font_size=22),
            label(r"gold: \ QDA's curves", font_size=22, color=MAPC),
            label(rf"leave-one-out error: \ LDA {100 * d['loo2_lda']:.1f}\%, \ QDA {100 * d['loo2_qda']:.1f}\%", font_size=22, color=SP[2]),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In two dimensions the rules can be drawn. Petal length and width, with the regions LDA "
            "assigns to each species. <bookmark mark='b'/> Its boundaries are straight lines. <bookmark mark='c'/> QDA's "
            "boundaries curve, bending around the tighter setosa cloud and the wider virginica one. "
            "<bookmark mark='d'/> Leaving out each flower in turn, LDA misclassifies four percent and QDA three: with only "
            "two variables, the extra flexibility is affordable."
        ) as vo:
            self.add(iris_tag())
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(reg), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(bq), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def errors(self):
        d = load("lda")
        hdr = [r"\textbf{all four variables}", r"\textbf{training error}", r"\textbf{leave-one-out error}"]
        body = [[r"LDA \ (10 covariance parameters)", f"{100 * d['train_lda']:.1f}\\%", f"{100 * d['loo_lda']:.1f}\\%"],
                [r"QDA \ (30 covariance parameters)", f"{100 * d['train_qda']:.1f}\\%", f"{100 * d['loo_qda']:.1f}\\%"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.0, row_buff=0.35, colors=[GREY_A, SP[2], MAPC])
        tb.move_to([0, 1.0, 0])
        foot = fit_rows(VGroup(
            label(r"both make 3 mistakes out of 150 on the data they were fitted to", font_size=22),
            label(r"left out, \ QDA makes one more: \ its extra 20 covariance parameters buy nothing here", font_size=22, color=MAPC),
            label(r"training error flatters every method: \ Part 19's lesson, \ in many dimensions", font_size=22, color=RES),
        ), 12.0, 0.22, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> With all four measurements, both rules misclassify three of the hundred and fifty "
            "flowers they were fitted to. <bookmark mark='b'/> Leaving each flower out, LDA still errs on three, "
            "while QDA errs on four: its twenty extra covariance parameters do not improve this leave-one-out count. "
            "One mistake of difference is not evidence of a universal ranking. <bookmark mark='c'/> The gap between "
            "training and held-out error is Part 19's lesson, and it grows quickly with the number of variables."
        ) as vo:
            self.add(iris_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def history(self):
        rows = fit_rows(VGroup(
            label(r"Edgar Anderson measured the irises on the Gasp\'e Peninsula, \ studying how species evolve", font_size=24),
            label(r"Fisher used them in `The use of multiple measurements in taxonomic problems'", font_size=24, color=SP[2]),
            label(r"published in the \emph{Annals of Eugenics}, \ which Fisher edited", font_size=24, color=RES),
            label(r"Rao's 1948 multi-group extension: \ anthropometry of Indian castes, \ with Mahalanobis", font_size=24, color=GREY_A),
            label(r"today: \ a standard baseline classifier, \ from medicine to face recognition", font_size=24, color=PATH),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The history, as promised. The botanist Edgar Anderson collected the irises, mostly on the "
            "Gaspé Peninsula in Quebec, to study how species evolve. <bookmark mark='b'/> Fisher used them to illustrate the "
            "discriminant, <bookmark mark='c'/> in a 1936 paper in the Annals of Eugenics, a journal Fisher edited, and "
            "eugenic questions were among the applications he had in mind. <bookmark mark='d'/> Rao's multi-group "
            "extension grew from Mahalanobis's measurements of Indian castes. <bookmark mark='e'/> Today the method is a "
            "standard baseline classifier, used in everything from medical diagnosis to face recognition."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def logistic(self):
        rows = [
            cmath(r"\text{LDA}", r":", r"\text{models } p(x \mid g): \ \text{generative}", font_size=30),
            cmath(r"\text{logistic}", r":", r"\text{models } P(g \mid x) \text{ directly: \ discriminative}", font_size=30),
            cmath(r"\text{normal truth}", r":", r"\text{LDA more efficient, \ model- and separation-dependent efficiency (Efron 1975)}", font_size=28),
            cmath(r"\text{non-normal truth}", r":", r"\text{correct conditional logit can tolerate nonnormal predictors}", font_size=30),
        ]
        rows[2][-1].set_color(SP[2])
        whys = [why(r"the full joint distribution"), why(r"the same linear log-odds"), why(r"uses more of the model"), why(r"uses less, \ risks less")]
        with self.voiceover(
            "<bookmark mark='a'/> Linear discriminant analysis and logistic regression both produce log odds that are"
            " linear in x, but they get there differently. LDA models how the measurements are distributed within "
            "each group. <bookmark mark='b'/> Logistic regression, Part 24, models the probability of the group given"
            " the measurements, and nothing else. <bookmark mark='c'/> If the data really are normal with a common "
            "covariance, Bradley Efron showed in 1975 that LDA is more efficient, with the relative efficiency "
            "depending on separation and the precise model, rather than a fixed sample-size saving. <bookmark "
            "mark='d'/> If they are not, LDA's extra assumptions can mislead it, while logistic regression avoids the"
            " predictor-distribution model if its conditional logit is correctly specified. Neither method is "
            "uniformly safer."
        ) as vo:
            intro=label('Generative and conditional models make different assumptions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

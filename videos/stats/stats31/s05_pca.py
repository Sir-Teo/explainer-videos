from __future__ import annotations

import numpy as np

from videos.stats.stats31.common import *  # noqa: F403


class PCA(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.svd()
        self.mds_link()
        self.biplot()
        self.scree()
        self.units()
        self.how_many()
        self.cautions()

    def card(self):
        card = chapter_card(4, r"Principal components", r"The directions of greatest variance", lit=(1901, 1933), part=PART)
        with self.voiceover("Chapter four. Principal components."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\max_{\|a\| = 1}", r"", r"\mathrm{Var}(a^\top x) = a^\top S a", font_size=32),
            cmath(r"S a", r"=", r"\lambda a: \ \text{the top eigenvector}, \ \text{variance } \lambda_1", font_size=30),
            cmath(r"a_2", r":", r"\text{the best direction orthogonal to } a_1, \ \dots", font_size=30),
            cmath(r"\textstyle\sum_j \lambda_j", r"=", r"\mathrm{tr}\, S: \ \text{total variance, \ shared out}", font_size=30),
        ]
        rows[1][-1].set_color(PCC)
        whys = [why(r"Hotelling (1933)"), why(r"Lagrange: \ Part 21"), why(r"uncorrelated components"),
                why(r"`explained variance' $\lambda_k / \sum \lambda_j$")]
        with self.voiceover(
            "<bookmark mark='a'/> Karl Pearson in 1901 asked for the line closest to a cloud of points; Hotelling in 1933 "
            "asked for the linear combination with the largest variance. They are the same question. Maximize a transpose "
            "S a over unit vectors. <bookmark mark='b'/> A Lagrange multiplier, Part 21, gives S a equals lambda a: the "
            "answer is the top eigenvector, and its variance is the top eigenvalue. <bookmark mark='c'/> The second "
            "component is the best direction orthogonal to the first, and so on; the components are uncorrelated. "
            "<bookmark mark='d'/> The eigenvalues add up to the total variance, so each component's share is its "
            "eigenvalue over the trace."
        ) as vo:
            intro=label('Principal components maximize retained centered variance',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def svd(self):
        rows = [
            cmath(r"X_0", r"=", r"U D V^\top", font_size=34),
            cmath(r"\text{scores}", r"=", r"U D, \ \ \text{loadings} = V, \ \ \lambda_j = d_j^2/(n - 1)", font_size=30),
            cmath(r"\min_{\mathrm{rank}\, B \le k} \|X_0 - B\|_F", r"=", r"\big(\textstyle\sum_{j > k} d_j^2\big)^{1/2}", font_size=28),
            cmath(r"\text{Pearson}", r"=", r"\text{Hotelling}: \ \text{closest plane} = \text{most variance}", font_size=28),
        ]
        rows[2][-1].set_color(PCC)
        whys = [why(r"the centred data, \ Part 4"), why(r"no covariance matrix needed"),
                why(r"Eckart \& Young (1936)"), why(r"Pythagoras")]
        with self.voiceover(
            "<bookmark mark='a'/> In practice, take the singular value decomposition of the centred data, Part 4. "
            "<bookmark mark='b'/> The scores are U D, the loadings are the columns of V, and the variances are the squared "
            "singular values over n minus one; no covariance matrix need ever be formed. <bookmark mark='c'/> Carl Eckart "
            "and Gale Young proved in 1936 that truncating the decomposition gives the best rank-k approximation of the data "
            "in squared error. <bookmark mark='d'/> That is why Pearson's and Hotelling's questions agree: by Pythagoras, "
            "the plane that keeps the most variance is the plane closest to the points."
        ) as vo:
            intro=label('Truncated SVD minimizes squared reconstruction error',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def biplot(self):
        d = load("pca")
        Sc, L = np.asarray(d["scores"]), np.asarray(d["loadings"])
        st = list(d["states"])
        A = axes([-3.5, 3.5], [-3.0, 2.2], x_length=7.6, y_length=5.4, xlabel=r"PC1: \ arrests", ylabel=r"PC2: \ urban",
                 xticks=[-3, 0, 3], yticks=[-2, 0, 2], center=[-2.2, 0.0, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=PCC) for a, b in Sc[:, :2]])
        show = ["California", "Nevada", "Florida", "North Dakota", "Vermont", "Mississippi", "Hawaii", "Rhode Island",
                "North Carolina", "Maine"]
        names = VGroup(*[label(s, font_size=15, color=GREY_A).next_to(dots[st.index(s)], UR, buff=0.04) for s in show])
        arrows = VGroup()
        for j, nm in enumerate(d["names"]):
            tip = ax.c2p(2.6 * L[j, 0], 2.6 * L[j, 1])
            arrows.add(Arrow(ax.c2p(0, 0), tip, buff=0, color=MAPC, stroke_width=3, max_tip_length_to_length_ratio=0.12))
            arrows.add(label(nm, font_size=20, color=MAPC).next_to(tip, normalize(tip - ax.c2p(0, 0)), buff=0.08))
        rows = fit_rows(VGroup(
            label(r"50 states, \ 4 variables, \ standardized", font_size=22),
            label(rf"PC1 ({100 * d['explained'][0]:.0f}\%): \ arrest rates together", font_size=22, color=PCC),
            label(rf"PC2 ({100 * d['explained'][1]:.0f}\%): \ urban population", font_size=22, color=PCC),
            label(r"gold arrows: \ each variable's loadings", font_size=22, color=MAPC),
            label(r"California: high arrest rates, very urban", font_size=22, color=GREY_A),
            label(r"Mississippi: \ high murder, \ rural", font_size=22, color=GREY_A),
        ), 4.0, 0.42, [4.8, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The US arrests data: rates of murder, assault and rape per hundred thousand in each"
            " of the fifty states in 1973, with the percentage of the population living in cities, all standardized. "
            "<bookmark mark='b'/> The first component weights the three crimes almost equally: an overall arrest-rate"
            " score; arrests are a proxy, not measured crime incidence, sixty-two percent of the variance. <bookmark "
            "mark='c'/> The second is mostly the urban percentage, another quarter. <bookmark mark='d'/> Gabriel's "
            "biplot of 1971 draws variable arrows alongside scores. Here arrows are loadings multiplied by two point "
            "six for display, not unscaled reconstruction coordinates. <bookmark mark='e'/> Now each state can be "
            "read: California and Nevada are high on arrest rates and urbanization, North Dakota and Vermont low on "
            "both, Mississippi and the Carolinas high in murder for how rural they are."
        ) as vo:
            self.add(arrests_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.02), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowArrow(a) if isinstance(a, Arrow) else FadeIn(a) for a in arrows], lag_ratio=0.2), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(names), FadeIn(rows[4]), FadeIn(rows[5]))
        self.clear_scene()

    def scree(self):
        d = load("pca")
        ex = np.asarray(d["explained"])
        A = axes([0.4, 4.6], [0, 0.7], x_length=6.0, y_length=4.4, xlabel=r"component", ylabel=r"share of variance",
                 xticks=[1, 2, 3, 4], yticks=[0, 0.2, 0.4, 0.6], yfmt=lambda v: f"{v:.1f}", center=[-2.6, 0.3, 0])
        ax = A.ax
        bars = bars_at(ax, [1, 2, 3, 4], ex, 0.6, PCC, 0.75)
        cum = polyline(ax, [1, 2, 3, 4], np.cumsum(ex) * 0.7, MAPC, 2.5)
        rows = fit_rows(VGroup(
            label(r"the scree plot \ (Cattell 1966)", font_size=22),
            label(rf"{100 * ex[0]:.0f}, \ {100 * ex[1]:.1f}, \ {100 * ex[2]:.1f}, \ {100 * ex[3]:.1f} percent", font_size=22, color=PCC),
            label(rf"two components keep {100 * (ex[0] + ex[1]):.0f}\%", font_size=22, color=MAPC),
            label(r"the elbow after two: \ the rest looks like rubble", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Raymond Cattell's scree plot, named for the rubble at the foot of a cliff: the eigenvalues "
            "in order. <bookmark mark='b'/> Sixty-two, twenty-five, nine and four percent. <bookmark mark='c'/> Two "
            "components keep eighty-seven percent of the variance, so the biplot we just read is a faithful summary of "
            "four-dimensional data. <bookmark mark='d'/> After the second bar the drop flattens: the elbow."
        ) as vo:
            self.add(arrests_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def units(self):
        d = load("pca")
        L = np.asarray(d["iris_loadings"])
        ex, exs = np.asarray(d["iris_explained"]), np.asarray(d["iris_std_explained"])
        hdr = [r"\textbf{irises}", r"\textbf{PC1 share}", r"\textbf{PC2 share}", r"\textbf{PC1 weight on petal length}"]
        body = [[r"raw centimetres", f"{100 * ex[0]:.1f}\\%", f"{100 * ex[1]:.1f}\\%", f"{abs(L[2, 0]):.2f}"],
                [r"standardized", f"{100 * exs[0]:.1f}\\%", f"{100 * exs[1]:.1f}\\%", f"{d['iris_std_loadings'][2][0]:.2f}"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.35, colors=[GREY_A, PCC, MAPC])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"petal length varies most in centimetres, \ so raw PCA is mostly petal length", font_size=22),
            label(r"PCA is not invariant to units: \ covariance or correlation is a choice", font_size=22, color=RES),
            label(r"Mahalanobis distance is invariant; \ principal components are not", font_size=22, color=PATH),
        ), 12.0, 0.25, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A choice that matters. On the irises in raw centimetres, the first component holds "
            "ninety-two and a half percent of the variance, and it is mostly petal length, the measurement with the largest "
            "spread. <bookmark mark='b'/> Standardize the four variables first and the first component drops to seventy-three "
            "percent and weights them more evenly. <bookmark mark='c'/> Principal components depend on units, so analysing "
            "the covariance or the correlation matrix is a decision, not a detail. Mahalanobis distance was invariant to "
            "units; principal components are not."
        ) as vo:
            self.add(iris_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]), FadeIn(foot[2]))
        self.clear_scene()

    def how_many(self):
        rows = [
            cmath(r"\text{Kaiser}", r":", r"\text{keep } \lambda_j > 1 \ \text{(correlation matrix)}", font_size=30),
            cmath(r"\text{scree}", r":", r"\text{keep up to the elbow}", font_size=30),
            cmath(r"\text{parallel analysis}", r":", r"\text{keep } \lambda_j > \text{the same quantile under pure noise}", font_size=28),
            cmath(r"\text{noise}", r":", r"\lambda_{\max} \approx (1 + \sqrt{p/n})^2, \ \text{not } 1", font_size=30),
        ]
        rows[2][-1].set_color(PCC)
        whys = [why(r"Kaiser (1960): \ crude"), why(r"Cattell (1966): \ subjective"), why(r"Horn (1965)"),
                why(r"chapter two's Marchenko--Pastur edge")]
        with self.voiceover(
            "<bookmark mark='a'/> How many components to keep? Henry Kaiser's rule keeps eigenvalues of the "
            "correlation matrix above one, a crude rule. <bookmark mark='b'/> Cattell's elbow is subjective. "
            "<bookmark mark='c'/> John Horn's parallel analysis of 1965 is better: compare each eigenvalue with the "
            "same eigenvalue from data of the same size with no structure at all. <bookmark mark='d'/> And chapter "
            "two told us what that comparison looks like: the largest eigenvalue of pure noise is near one plus root "
            "p over n, squared, not one. Kaiser's rule ignores this sample-noise spread and can overselect in "
            "high-dimensional noise models."
        ) as vo:
            intro=label('Choosing component count requires a signal and noise comparison',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cautions(self):
        rows = fit_rows(VGroup(
            label(r"a component's sign is arbitrary: \ $a$ and $-a$ are equally good", font_size=24),
            label(r"components describe variance, \ not causes", font_size=24, color=RES),
            label(r"high variance is not the same as relevance to an outcome", font_size=24, color=RES),
            label(r"one gross outlier can capture a component: \ Part 30's MCD helps", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Four cautions. The sign of a component is arbitrary: a and minus a are equally good, and "
            "software disagrees. <bookmark mark='b'/> Components describe variance, not mechanisms. <bookmark mark='c'/> A "
            "direction of large variance need not be the one that predicts an outcome; regression on the first few "
            "components can throw away exactly the signal you wanted. <bookmark mark='d'/> And because variance is not "
            "robust, a single gross outlier can claim a whole component. Part 30's minimum covariance determinant gives a "
            "robust covariance to decompose instead."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def mds_link(self):
        rows = [
            cmath(r"\text{PCA}", r":", r"\text{eigenvectors of } X_0^\top X_0 \ (p \times p)", font_size=30),
            cmath(r"\text{classical scaling}", r":", r"\text{eigenvectors of } X_0 X_0^\top \ (n \times n)", font_size=30),
            cmath(r"X_0 V", r"=", r"U D: \ \text{the same coordinates}", font_size=32),
            cmath(r"\text{so}", r":", r"\text{Euclidean distances: PCA scores; roads: approximate Gram embedding}", font_size=28),
        ]
        rows[2][-1].set_color(PCC)
        whys = [why(r"the covariance side"), why(r"the Gram side"), why(r"one SVD, \ two routes"), why(r"Torgerson met Hotelling")]
        with self.voiceover(
            "<bookmark mark='a'/> Principal components come from the eigenvectors of X transpose X, a p by p matrix. "
            "<bookmark mark='b'/> The hook's classical scaling took the eigenvectors of X X transpose, an n by n Gram"
            " matrix built from distances. <bookmark mark='c'/> Both are halves of one singular value decomposition, "
            "so when the distances are Euclidean the scaling coordinates are exactly the principal component scores. "
            "<bookmark mark='d'/> For exactly Euclidean distances this reconstructs PCA scores from unseen "
            "coordinates. Road distances are not exactly Euclidean, so the hook instead uses a positive Gram "
            "approximation."
        ) as vo:
            intro=label('Euclidean classical scaling and PCA share one singular value decomposition',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

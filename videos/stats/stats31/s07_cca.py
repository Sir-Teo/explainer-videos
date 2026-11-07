from __future__ import annotations

import numpy as np

from videos.stats.stats31.common import *  # noqa: F403


class CCA(VoiceoverScene):
    def construct(self):
        self.card()
        self.question()
        self.solution()
        self.data()
        self.scatter_pair()
        self.table()
        self.angles()
        self.overfit()
        self.family()

    def card(self):
        card = chapter_card(6, r"Canonical correlation", r"Two sets of variables, \ one relationship", lit=(1936,), part=PART)
        with self.voiceover("Chapter six. Canonical correlation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def question(self):
        rows = [
            cmath(r"x \in \mathbb R^{p}, \ y \in \mathbb R^{q}", r":", r"\text{two blocks of variables}", font_size=30),
            cmath(r"\max_{a, b}", r"", r"\mathrm{corr}(a^\top x, \ b^\top y)", font_size=32),
            cmath(r"q = 1", r":", r"\text{the multiple correlation } R \text{ of regression}", font_size=30),
            cmath(r"\text{then}", r":", r"\text{the best pair uncorrelated with the first, \ } \dots", font_size=30),
        ]
        rows[1][-1].set_color(CCC)
        whys = [why(r"demography; \ economics"), why(r"Hotelling (1936)"), why(r"Part 12's $R^2$, \ generalized"),
                why(r"$\min(p, q)$ pairs")]
        with self.voiceover(
            "<bookmark mark='a'/> Sometimes the variables come in two blocks: a country's demography, and its economy. "
            "<bookmark mark='b'/> Hotelling asked in 1936 for the linear combination of one block and the linear combination "
            "of the other that are as highly correlated as possible. <bookmark mark='c'/> When the second block is a single "
            "variable, this is just the multiple correlation of regression, Part 12's R. <bookmark mark='d'/> After the first "
            "pair comes the best pair uncorrelated with it, and so on, up to the smaller of the two block sizes."
        ) as vo:
            intro=label('Canonical correlation pairs linear summaries from two variable blocks',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def solution(self):
        rows = [
            cmath(r"K", r"=", r"S_{xx}^{-1/2} S_{xy} S_{yy}^{-1/2}", font_size=32),
            cmath(r"K", r"=", r"U\, \mathrm{diag}(r_1, r_2, \dots)\, V^\top", font_size=32),
            cmath(r"a_k", r"=", r"S_{xx}^{-1/2} u_k, \ \ b_k = S_{yy}^{-1/2} v_k", font_size=30),
            cmath(r"-\big(n - 1 - \tfrac{p + q + 1}{2}\big) \textstyle\sum_{j > k} \log(1 - r_j^2)", r"\approx", r"\chi^2_{(p - k)(q - k)}", font_size=26),
        ]
        rows[1][-1].set_color(CCC)
        whys = [why(r"whiten each block"), why(r"an SVD again"), why(r"the canonical weights"),
                why(r"Gaussian large-sample Bartlett test; nonsingular blocks")]
        with self.voiceover(
            "<bookmark mark='a'/> The answer is, once more, a singular value decomposition. Whiten each block by its "
            "own covariance and form the cross-covariance between the whitened blocks. <bookmark mark='b'/> Its "
            "singular values are the canonical correlations, <bookmark mark='c'/> and its singular vectors, "
            "unwhitened, are the canonical weights. <bookmark mark='d'/> Under joint Gaussian assumptions and "
            "nonsingular within-block covariance, Bartlett's large-sample statistic tests whether all correlations "
            "after the k-th are zero."
        ) as vo:
            intro=label('Whitened cross-covariance singular values are canonical correlations',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def data(self):
        rows = fit_rows(VGroup(
            label(r"50 countries, \ averaged over 1960--1970", font_size=26),
            label(r"demography: \ the share of the population under 15, \ and over 75", font_size=26, color=CCC),
            label(r"economy: \ the savings rate, \ income per head, \ and its growth", font_size=26, color=MAPC),
            label(r"Modigliani's life-cycle hypothesis: \ people save in middle age and spend when young or old", font_size=26, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The data are Arlie Sterling's savings data, made famous by Belsley, Kuh and Welsch: fifty "
            "countries, averaged over the 1960s. <bookmark mark='b'/> One block is demographic: the percentage of the "
            "population under fifteen and over seventy-five. <bookmark mark='c'/> The other is economic: the aggregate "
            "savings rate, disposable income per head, and its growth rate. <bookmark mark='d'/> The question comes from "
            "Franco Modigliani's life-cycle hypothesis: people save in middle age and draw down savings when young or old, so "
            "a country's age structure should be linked to its savings."
        ) as vo:
            self.add(savings_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def scatter_pair(self):
        d = load("cca")
        u, v = np.asarray(d["u"]), np.asarray(d["v"])
        cs = list(d["countries"])
        A = axes([-1.6, 2.8], [-1.6, 2.8], x_length=5.6, y_length=5.0, xlabel=r"$U_1$: \ the demographic variate",
                 ylabel=r"$V_1$: \ the economic variate", xticks=[-1, 0, 1, 2], yticks=[-1, 0, 1, 2], center=[-2.6, 0.0, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=CCC) for a, b in zip(u[:, 0], v[:, 0])])
        order = np.argsort(u[:, 0] + v[:, 0])
        pick = list(order[:3]) + list(order[-4:])
        names = VGroup(*[label(cs[i], font_size=15, color=GREY_A).next_to(dots[i], UR, buff=0.04) for i in pick])
        rows = fit_rows(VGroup(
            label(rf"first canonical correlation $r_1 = {d['r'][0]:.2f}$", font_size=22, color=CCC),
            label(r"$U_1$: \ older populations to the right", font_size=22),
            label(r"$V_1$: \ richer economies at the top", font_size=22, color=MAPC),
            label(r"old, \ rich, \ and saving: \ Western Europe, \ North America", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The first pair of canonical variates, one dot per country. Their correlation is point eight "
            "two. <bookmark mark='b'/> The demographic variate runs from young populations on the left to old ones on the "
            "right. <bookmark mark='c'/> The economic variate runs from poor to rich. <bookmark mark='d'/> At the top right, "
            "the old, rich countries of Western Europe and North America; at the bottom left, young, poor ones. Age "
            "structure and the economy move together, strongly."
        ) as vo:
            self.add(savings_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.03), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(names), FadeIn(rows[3]))
        self.clear_scene()

    def table(self):
        d = load("cca")
        sx, sy = np.asarray(d["structX"]), np.asarray(d["structY"])
        hdr = [r"\textbf{variable}", r"\textbf{corr. with first variate}", r"\textbf{corr. with second}"]
        nm = {"pop15": r"under 15 \ (\%)", "pop75": r"over 75 \ (\%)", "sr": r"savings rate", "dpi": r"income per head",
              "ddpi": r"income growth"}
        body = [[nm[n], f"{sx[i, 0]:+.2f}", f"{sx[i, 1]:+.2f}"] for i, n in enumerate(d["xnames"])]
        body += [[nm[n], f"{sy[i, 0]:+.2f}", f"{sy[i, 1]:+.2f}"] for i, n in enumerate(d["ynames"])]
        tb = table_rows([hdr] + body, font_size=25, col_buff=1.0, row_buff=0.28, colors=[GREY_A, CCC, CCC, MAPC, MAPC, MAPC])
        tb.move_to([0, 1.0, 0])
        t = d["tests"]
        foot = fit_rows(VGroup(
            label(rf"$r_1 = {d['r'][0]:.3f}$, \ Bartlett $p = 7 \times 10^{{-11}}$; \ $r_2 = {d['r'][1]:.3f}$, \ $p = {t[1]['p']:.3f}$", font_size=22, color=CCC),
            label(r"the structure correlations name the variates; \ the raw weights can mislead when variables correlate", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> To interpret a canonical variate, correlate it with the original variables. The "
            "first demographic variate is almost exactly minus the share under fifteen and plus the share over "
            "seventy-five. The first economic variate is mostly income, with savings contributing. <bookmark "
            "mark='b'/> The first canonical correlation is overwhelmingly significant. The second, point three seven,"
            " has an unadjusted approximate p-value of point oh four; interpreting several sequential tests also "
            "raises multiplicity questions. <bookmark mark='c'/> Use these structure correlations, not the raw "
            "weights: when the variables in a block are correlated, as under-fifteen and over-seventy-five are, the "
            "weights can have surprising signs."
        ) as vo:
            self.add(savings_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def angles(self):
        d = load("cca")
        th = np.asarray(d["angles"])
        rows = [
            cmath(r"\cos\theta_k", r"=", r"r_k", font_size=34),
            cmath(r"\theta_k", r":", r"\text{principal angles between the column spaces of } X_0, \ Y_0", font_size=28),
            cmath(r"\theta_1, \theta_2", r"=", rf"{th[0]:.1f}^\circ, \ {th[1]:.1f}^\circ", font_size=32),
            cmath(r"\text{caution}", r":", r"p + q \text{ near } n \Rightarrow r_1 \to 1 \text{ by chance}", font_size=30),
        ]
        rows[2][-1].set_color(CCC)
        whys = [why(r"Jordan (1875)"), why(r"subspaces in $\mathbb R^n$"), why(r"close, \ then nearly orthogonal"),
                why(r"chapter ten again")]
        with self.voiceover(
            "<bookmark mark='a'/> A geometric reading. Each block of centred data spans a subspace of n-dimensional space. "
            "The canonical correlations are the cosines of the principal angles between those two subspaces, found by Camille "
            "Jordan in 1875. <bookmark mark='b'/> The first angle is the smallest angle between any vector in one subspace "
            "and any vector in the other. <bookmark mark='c'/> Here thirty-four degrees, then sixty-nine. "
            "<bookmark mark='d'/> And a caution: when p plus q approaches n, two random subspaces nearly intersect, so the "
            "first canonical correlation approaches one by chance alone."
        ) as vo:
            intro=label('Canonical correlations are cosines of data-column-space angles',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def family(self):
        rows = fit_rows(VGroup(
            label(r"one SVD, \ four methods", font_size=28),
            label(r"principal components: \ the SVD of the data", font_size=24, color=PCC),
            label(r"canonical correlation: \ the SVD of the whitened cross-covariance", font_size=24, color=CCC),
            label(r"discriminant analysis: \ CCA of $x$ with group indicators \ (next chapter)", font_size=24, color=SP[2]),
            label(r"correspondence analysis: \ the SVD of a contingency table's residuals", font_size=24, color=MAPC),
        ), 12.4, 0.55, [0, 0, 0])
        self.add(label("Singular value decomposition connects four multivariate methods",font_size=36).move_to([0,3.3,0]))
        with self.voiceover(
            "<bookmark mark='a'/> Step back and a family appears. <bookmark mark='b'/> Principal components are the SVD of "
            "the data. <bookmark mark='c'/> Canonical correlation is the SVD of the whitened cross-covariance. "
            "<bookmark mark='d'/> Discriminant analysis, next, is canonical correlation between the measurements and a set of "
            "group indicators. <bookmark mark='e'/> And correspondence analysis, Jean-Paul Benzécri's method, is the SVD of a "
            "contingency table's standardized residuals. One decomposition underlies them all."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def overfit(self):
        rows = [
            cmath(r"r_1", r"\uparrow", r"\text{as } p + q \to n, \ \text{even with no relation}", font_size=30),
            cmath(r"\text{regularized CCA}", r":", r"S_{xx} + \lambda_x I, \ \ S_{yy} + \lambda_y I", font_size=30),
            cmath(r"\text{sparse CCA}", r":", r"\text{few non-zero weights}", font_size=30),
            cmath(r"\text{PLS}", r":", r"\max_{\|a\|=\|b\|=1} \mathrm{cov}(a^\top x,b^\top y): \ \text{no inverse}", font_size=30),
        ]
        rows[1][-1].set_color(CCC)
        whys = [why(r"chance correlation"), why(r"Vinod (1976): \ ridge CCA"), why(r"Witten, Tibshirani \& Hastie (2009)"), why(r"Wold's partial least squares")]
        with self.voiceover(
            "<bookmark mark='a'/> With many variables in either block, canonical correlation overfits: the first "
            "correlation creeps towards one even when the blocks are unrelated. <bookmark mark='b'/> The cures echo "
            "chapter ten. Add a ridge to each block's covariance before inverting it. <bookmark mark='c'/> Or ask for"
            " sparse weights, with only a few non-zero. <bookmark mark='d'/> Or maximize covariance with unit-length "
            "weights instead of correlation, which needs no covariance inverse: Herman Wold's partial least squares, "
            "widely used in chemistry and genomics."
        ) as vo:
            intro=label('High-dimensional canonical correlations require regularization',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

from __future__ import annotations

import numpy as np

from videos.stats.stats4.common import *  # noqa: F403


class Vectors(VoiceoverScene):
    def construct(self):
        self.card()
        self.point()
        self.centring()
        self.upgrade()
        self.dof()
        self.data_matrix()

    def card(self):
        card = chapter_card(1, r"Vectors as data", r"A sample of $n$ is one point in $\mathbb R^n$", lit=(1805,), part=PART)
        with self.voiceover("Chapter one. Vectors as data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def point(self):
        d = load("vectors")
        y = np.asarray(d["y"])
        v = y - 160
        ns = NSpace(scale=0.17, center=[-3.0, -1.6, 0], angle=-0.7, tilt=0.4, axis_len=24.0,
                    axis_labels=[r"person 1", r"person 2", r"person 3"])
        vy = ns.vector(v, color=DATA)
        lab = ns.point_label(MathTex(r"\mathbf y - 160\,\mathbf 1", font_size=28, color=DATA), v, offset=(0.6, 0.3))
        coords = VGroup(MathTex(rf"\mathbf y = ({y[0]:.0f},\ {y[1]:.0f},\ {y[2]:.0f})", font_size=36, color=DATA),
                        label(r"three heights, \ one point in $\mathbb R^3$", font_size=24, color=GREY_A))
        coords.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, 2.4, 0])
        big = VGroup(label(r"forty families: \ one point in $\mathbb R^{40}$", font_size=26),
                     label(r"we cannot draw it, \ but lengths, angles and projections work the same", font_size=22,
                           color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        if big.width > 5.8:
            big.width = 5.8
        big.move_to([3.6, 0.4, 0])
        ops = VGroup(MathTex(r"\langle \mathbf x, \mathbf y \rangle = \sum_i x_i y_i", font_size=30),
                     MathTex(r"\|\mathbf y\| = \sqrt{\langle \mathbf y, \mathbf y\rangle}", font_size=30),
                     MathTex(r"\cos\theta = \frac{\langle \mathbf x, \mathbf y\rangle}{\|\mathbf x\|\,\|\mathbf y\|}",
                             font_size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.6, -1.9, 0])
        intro = label("Samples as vectors", font_size=36).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Part 1 had one idea that this whole part builds on. <bookmark mark='a'/> A sample of three heights is "
            "three numbers, and three numbers are one point in three-dimensional space: the first person's height "
            "along one axis, the second's along another, the third's up. <bookmark mark='b'/> Here it is, measured "
            "from a hundred and sixty centimetres. <bookmark mark='c'/> Forty families make one point in forty "
            "dimensions. We can't draw that, but nothing we do depends on drawing it: lengths, angles and "
            "projections work in forty dimensions exactly as they do in three. <bookmark mark='d'/> The inner "
            "product, the length and the angle are all a statistician needs: sums of squares are squared lengths, "
            "and Part 1 showed that correlation is the cosine of an angle."
        ) as vo:
            self.add(ns)
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), FadeIn(coords))
            vo.wait_until("b")
            self.add(vy)
            self.play(NSpace.reveal(vy), FadeIn(lab), ns.turn(0.5, run_time=3.0))
            vo.wait_until("c")
            self.play(FadeIn(big))
            vo.wait_until("d")
            self.play(FadeIn(ops), ns.turn(-0.4, run_time=3.0))
        vy.clear_updaters()
        self.clear_scene()

    def centring(self):
        d = load("vectors")
        y = np.asarray(d["y"]) - 160
        lab = ProjectionLab(np.ones((3, 1)), y, scale=0.17, center=(-3.0, -1.6, 0), axis_len=24.0)
        ns = lab.ns
        rows = [
            cmath(r"P_{\mathbf 1}\mathbf y", r"=", r"\frac{\langle \mathbf 1, \mathbf y\rangle}{\langle \mathbf 1, "
                  r"\mathbf 1\rangle}\,\mathbf 1", r"=", r"\bar y\, \mathbf 1", font_size=34),
            cmath(r"P_{\mathbf 1}", r"=", r"\frac{1}{n}\mathbf 1 \mathbf 1^\top", r"=", r"\frac1n J", font_size=34),
            cmath(r"\mathbf r", r"=", r"(I - \tfrac1n J)\,\mathbf y", r"=", r"\mathbf y - \bar y\,\mathbf 1", font_size=34),
        ]
        rows[0][4].set_color(FIT)
        rows[2][0].set_color(RES)
        whys = [why(r"projection onto the line through $\mathbf 1$"), why(r"as a matrix: \ every entry $1/n$"),
                why(r"centring: \ subtract the projection")]
        intro = label("The mean is a projection", font_size=36).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Now the first projection. <bookmark mark='a'/> The diagonal line through the vector of all ones holds "
            "every sample in which everyone is the same height. <bookmark mark='b'/> Drop a perpendicular from the "
            "data onto it. The foot is the inner product with the ones vector, over its squared length, times the "
            "ones vector: the mean, repeated. <bookmark mark='c'/> As a matrix, that projection is one over n times "
            "the all-ones matrix J. <bookmark mark='d'/> What's left, the data minus its mean, is the residual, at "
            "right angles to the diagonal. Centring data is projecting it away from the ones vector."
        ) as vo:
            self.add(ns)
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.add(lab.space, lab.vy)
            self.play(NSpace.reveal(lab.space, lab.vy))
            vo.wait_until("b")
            self.add(lab.vfit)
            self.play(NSpace.reveal(lab.vfit))
            step = ladder(self, rows, whys, keep=3, top=2.9, x=3.0, buff=0.55, edge=6.9)
            step(0, transform=False)
            vo.wait_until("c")
            step(1, transform=False)
            vo.wait_until("d")
            self.add(lab.vres, lab.angle_mark)
            self.play(NSpace.reveal(lab.vres, lab.angle_mark))
            step(2, transform=False)
            self.play(ns.turn(0.8, run_time=4.0))
        lab.stop()
        self.clear_scene()

    def dof(self):
        d = load("vectors")
        y = np.asarray(d["y"]) - 160
        ns = NSpace(scale=0.15, center=[-3.0, -0.8, 0], angle=-0.7, tilt=0.4, axis_len=24.0)
        u = np.array([1.0, -1.0, 0.0]) / np.sqrt(2)
        w = np.array([1.0, 1.0, -2.0]) / np.sqrt(6)
        pl = ns.plane(u, w, extent=13.0, color=RES, opacity=0.16)
        vr = ns.vector(y - y.mean(), color=RES)
        rows = [
            cmath(r"\mathbf r \perp \mathbf 1", r"\ \Rightarrow\ ", r"\mathbf r \in \text{a hyperplane of dimension } n - 1",
                  font_size=32),
            cmath(r"\operatorname{tr}\!\left(I - \tfrac1n J\right)", r"=", r"n - 1", font_size=34),
            cmath(r"s^2", r"=", r"\frac{\|\mathbf r\|^2}{n - 1}", font_size=38),
        ]
        rows[2][0].set_color(S.EST)
        whys = [why(r"one constraint: \ $\sum_i r_i = 0$"), why(r"$I - P$ is a projection too"),
                why(r"Part 1's $n - 1$, \ explained; \ proved unbiased in Part 8")]
        with self.voiceover(
            "This is where n minus one comes from. <bookmark mark='a'/> The residual is at right angles to the ones "
            "vector, so it's trapped in a plane: the residuals always add to zero. In n dimensions that's a "
            "subspace of dimension n minus one. <bookmark mark='b'/> I minus one over n J is a projection too, onto "
            "that subspace, and its trace is n minus one. <bookmark mark='c'/> That's why the sample variance "
            "divides the squared length of the residual by n minus one: the residual has only n minus one "
            "dimensions to spread out in. Part 8 proves it's exactly unbiased, and the hat matrix's n minus p is "
            "the same idea with p columns instead of one."
        ) as vo:
            self.add(ns, pl, vr)
            self.play(NSpace.reveal(pl, vr))
            step = ladder(self, rows, whys, keep=3, top=2.9, x=2.8, buff=0.6, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            self.play(ns.turn(0.9, run_time=4.0))
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
        for m in (pl, vr):
            m.clear_updaters()
        self.clear_scene()

    def data_matrix(self):
        rows_v = VGroup(
            MathTex(r"X", r"=", r"\begin{pmatrix} 171 & 68 & 41.2 \\ 164 & 55 & 29.8 \\ \vdots & \vdots & \vdots \\ 181 & 80 & 55.1 "
                    r"\end{pmatrix}", font_size=34),
            label(r"$n$ rows (people) \ $\times$ \ $p$ columns (variables)", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.25).move_to([-3.6, 0.6, 0])
        heads = VGroup(*[label(t, font_size=20, color=GREY_B) for t in (r"height", r"weight", r"income (k)")])
        for h_, xx in zip(heads, (-3.9, -3.0, -1.9)):
            h_.move_to([xx, 2.25, 0])
        views = VGroup(
            VGroup(label(r"rows: \ $n$ points in $\mathbb R^p$", font_size=28, color=DATA),
                   label(r"a cloud of people: \ scatter plots, ellipses, \ Part 5", font_size=22, color=GREY_B)),
            VGroup(label(r"columns: \ $p$ vectors in $\mathbb R^n$", font_size=28, color=FIT),
                   label(r"variables as arrows: \ angles are correlations, \ projections are regressions", font_size=22,
                         color=GREY_B)),
        )
        for v in views:
            v.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        views.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.4, 0.9, 0])
        cov = MathTex(r"S", r"=", r"\frac{1}{n-1}\, X_c^\top X_c", font_size=40).move_to([3.0, -1.8, 0])
        cov[0].set_color(EIG)
        cw = label(r"$X_c$: \ each column centred \ ($I - \tfrac1n J$)", font_size=22, color=GREY_B).next_to(cov, DOWN, buff=0.2)
        tag = note(r"illustrative").to_corner(DL, buff=0.3)
        intro = label('Two views of a data matrix', font_size=36)
        with self.voiceover(
            "With several variables, the data become a matrix. <bookmark mark='a'/> One row per person, one column "
            "per variable: height, weight, income. <bookmark mark='b'/> There are two ways to look at it, and "
            "statistics uses both. Read it by rows, and it's n points in p dimensions, a cloud of people, which is "
            "how Part 5 will picture it. <bookmark mark='c'/> Read it by columns, and it's p arrows in n "
            "dimensions, one per variable. In that picture the angle between two centred columns is their "
            "correlation, and regressing one variable on others is projecting one arrow onto the space of the "
            "others. <bookmark mark='d'/> Both views meet in one formula: centre each column, and the sample "
            "covariance matrix is X c transpose X c over n minus one. Every entry is an inner product of two "
            "columns."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(rows_v), FadeIn(heads))
            vo.wait_until("b")
            self.play(FadeIn(views[0], shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(views[1], shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(Write(cov), FadeIn(cw))
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(1, r"correlation is the cosine of the angle between centred vectors, \ drawn for $n = 3$",
                            r"that the picture in $\mathbb R^3$ is the whole story", r"for nonconstant columns it holds in $\mathbb R^n$ for any $n$, \ "
                            r"and regression is a projection between those vectors", width=10.0, font_size=24)
        card.to_edge(UP, buff=0.35)
        rows = [
            cmath(r"r", r"=", r"\cos\theta", r"=", r"\frac{\langle \mathbf x_c, \mathbf y_c\rangle}{\|\mathbf x_c\|\,\|\mathbf y_c\|}",
                  font_size=34),
            cmath(r"b", r"=", r"\frac{\langle \mathbf x_c, \mathbf y_c\rangle}{\|\mathbf x_c\|^2}", r"=",
                  r"r\, \frac{\|\mathbf y_c\|}{\|\mathbf x_c\|}", r"=", r"r\, \frac{s_y}{s_x}", font_size=34),
        ]
        rows[1][0].set_color(FIT)
        whys = [why(r"nonconstant columns; \ Part 1 in $\mathbb R^n$"), why(r"the slope: \ project $\mathbf y_c$ onto $\mathbf x_c$")]
        intro = label('Correlation in any sample dimension', font_size=36)
        with self.voiceover(
            "This is our first upgrade: a result from an earlier part, made more general. <bookmark mark='a'/> Part "
            "1 showed that correlation is the cosine of the angle between centred vectors, drawn with three people. "
            "We can now write the same geometry in "
            "any number of dimensions, because inner products and angles do. <bookmark mark='b'/> And one more "
            "fact comes with it. The slope of the regression of y on x is the coefficient of the projection of the "
            "centred y onto the centred x: the inner product over the squared length. <bookmark mark='c'/> Rewrite it "
            "with the cosine, and the slope is r times the ratio of the standard deviations, which is why Part 1 "
            "warned that correlation is not slope."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(card, shift=DOWN * 0.2))
            step = ladder(self, rows, whys, keep=2, top=-0.5, x=-0.6, buff=0.55, edge=6.9)
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(Indicate(rows[1][6], color=S.ACCENT))
        self.clear_scene()

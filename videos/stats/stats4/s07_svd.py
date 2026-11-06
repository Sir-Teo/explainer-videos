from __future__ import annotations

import numpy as np

from videos.stats.stats4.common import *  # noqa: F403


def image_mob(M, width=5.0, lo=0.0, hi=1.0) -> ImageMobject:
    """Render every matrix entry on one fixed color scale, with nearest resampling."""
    values = (np.asarray(M) - lo) / (hi - lo)
    dark = np.asarray(ManimColor("#0B0F17").to_rgb())
    light = np.asarray(ManimColor(S.WORLD).to_rgb())
    pixels = np.round(255 * (dark + values[..., None] * (light - dark))).astype(np.uint8)
    return (ImageMobject(pixels).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            .scale_to_fit_width(width))


class SVD(VoiceoverScene):
    def construct(self):
        self.card()
        self.geometry()
        self.decomposition()
        self.lowrank()
        self.pca()

    def card(self):
        card = chapter_card(6, r"The singular value decomposition", r"Two orthogonal maps and a stretch", lit=(),
                            part=PART)
        with self.voiceover("Chapter six. The singular value decomposition."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def geometry(self):
        M = np.array([[1.6, 0.9], [0.3, 1.1]])
        U, s, Vt = np.linalg.svd(M)
        # This positive-determinant example admits two proper rotations.
        if np.linalg.det(U) < 0:
            U[:, -1] *= -1
            Vt[-1, :] *= -1
        c0 = np.array([-2.6, -0.4, 0])
        sc = 1.0
        th = np.linspace(0, TAU, 120)
        circle_pts = np.column_stack([np.cos(th), np.sin(th)])

        def shape(T):
            pts = circle_pts @ T.T
            return VMobject(stroke_color=EIG, stroke_width=3).set_points_smoothly([c0 + sc * np.array([a, b, 0]) for a, b in pts])

        def arrows(T):
            return VGroup(*[Arrow(c0, c0 + sc * np.array([*(T @ e), 0]), buff=0, color=c, stroke_width=4,
                                  max_tip_length_to_length_ratio=0.15)
                            for e, c in ((np.array([1.0, 0]), FIT), (np.array([0, 1.0]), RES))])

        grid = VGroup(Line(c0 + LEFT * 3, c0 + RIGHT * 3, color=GREY_D), Line(c0 + DOWN * 3, c0 + UP * 3, color=GREY_D))
        cur_shape, cur_arr = shape(np.eye(2)), arrows(np.column_stack([Vt[0], Vt[1]]))
        caps = [r"the unit circle, \ and the right singular vectors $\mathbf v_1, \mathbf v_2$",
                r"$V^\top$: \ rotate them onto the axes",
                rf"$\Sigma$: \ stretch by $\sigma_1 = {s[0]:.2f}$, \ $\sigma_2 = {s[1]:.2f}$",
                r"$U$: \ rotate again: \ the image of the circle under $M$"]
        cap = label(caps[0], font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        f = MathTex(r"M", r"=", r"U", r"\Sigma", r"V^\top", font_size=48).move_to([4.4, 1.4, 0])
        f[2].set_color(EIG)
        f[3].set_color(S.ACCENT)
        f[4].set_color(EIG)
        f2 = label(r"$U$, $V$ orthogonal; \ $\Sigma$ diagonal, \ $\sigma_1 \ge \sigma_2 \ge \dots \ge 0$", font_size=22,
                   color=GREY_B).next_to(f, DOWN, buff=0.3)
        mt = MathTex(r"M = " + mat_tex(M, "{:.1f}"), font_size=30).move_to([4.4, -0.6, 0])
        with self.voiceover(
            "The spectral theorem is for symmetric matrices. The singular value decomposition is its version for "
            "every matrix, square or not. <bookmark mark='a'/> Watch what a two by two matrix does to the unit "
            "circle. <bookmark mark='b'/> First, an orthogonal matrix V transpose rotates two special perpendicular "
            "directions onto the axes. <bookmark mark='c'/> Then a diagonal matrix stretches along the axes, by the "
            "singular values. <bookmark mark='d'/> Then another orthogonal matrix, U, rotates the result. The circle "
            "has become an ellipse. In general orthogonal maps may also reflect, and rectangular maps can add or remove dimensions; the same decomposition still applies. "
            "<bookmark mark='e'/> In symbols, M equals U Sigma V transpose. The singular values are the square roots "
            "of the eigenvalues of M transpose M, and the columns of V are its eigenvectors."
        ) as vo:
            self.play(FadeIn(grid), Create(cur_shape), FadeIn(cur_arr), FadeIn(cap), FadeIn(mt))
            for k, m in zip(range(1, 4), "bcd"):
                vo.wait_until(m)
                if k == 2:
                    changes = [ApplyMatrix(np.diag(s), mob, about_point=c0) for mob in (cur_shape, cur_arr)]
                else:
                    rotation = Vt if k == 1 else U
                    angle = np.arctan2(rotation[1, 0], rotation[0, 0])
                    changes = [Rotate(mob, angle=angle, about_point=c0) for mob in (cur_shape, cur_arr)]
                self.play(*changes,
                          Transform(cap, label(caps[k], font_size=26, color=GREY_A).to_edge(UP, buff=0.4)), run_time=2.0)
            vo.wait_until("e")
            self.play(Write(f), FadeIn(f2))
        self.clear_scene()

    def decomposition(self):
        rows = [
            cmath(r"M^\top M", r"=", r"V \Sigma^\top\Sigma V^\top", font_size=36),
            cmath(r"M", r"=", r"\sum_{k} \sigma_k\, \mathbf u_k \mathbf v_k^\top", font_size=38),
            cmath(r"M_r", r"=", r"\sum_{k \le r} \sigma_k\, \mathbf u_k \mathbf v_k^\top", font_size=38),
        ]
        rows[2][0].set_color(S.ACCENT)
        whys = [why(r"spectral theorem for the PSD matrix $M^\top M$"), why(r"a sum of rank-one pieces, \ largest first"),
                why(r"keep the first $r$")]
        th = theorem_card(r"Eckart--Young (1936)", r"$M_r$ is a closest matrix of rank at most $r$ to $M$ in Frobenius norm, \ and "
                          r"$\|M - M_r\|_F^2 = \sum_{k > r} \sigma_k^2$", color=S.ACCENT, width=7.4, font_size=24)
        th.to_edge(DOWN, buff=0.5)
        intro = label('A sum of rank-one pieces', font_size=36)
        with self.voiceover(
            "The decomposition comes from the spectral theorem. <bookmark mark='a'/> M transpose M is symmetric and "
            "positive semidefinite, so it's V times the squared singular values times V transpose. "
            "<bookmark mark='b'/> Write M as a sum of rank-one pieces, each a singular value times an outer product, "
            "largest first. <bookmark mark='c'/> Keep only the first r pieces. <bookmark mark='d'/> The theorem of "
            "Carl Eckart and Gale Young, from 1936, says this truncation is the best possible rank-r approximation "
            "to M, and its squared error is the sum of the squared singular values you threw away."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.55)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(th, shift=UP * 0.2))
        self.clear_scene()

    def lowrank(self):
        d = load("svd")
        img = np.asarray(d["img"])
        arrays = [img] + [np.asarray(d[f"approx_{k}"]) for k in d["ks"]]
        lo, hi = min(a.min() for a in arrays), max(a.max() for a in arrays)
        orig = image_mob(img, width=5.4, lo=lo, hi=hi).move_to([-3.6, 1.0, 0])
        ol = label(r"the World's population, \ a $60 \times 100$ matrix", font_size=22, color=S.WORLD).next_to(orig, DOWN, buff=0.15)
        ks = d["ks"]
        approx = {k: image_mob(np.asarray(d[f"approx_{k}"]), width=5.4, lo=lo, hi=hi).move_to([3.4, 1.0, 0]) for k in ks}
        labs = {k: MathTex(rf"r = {k}:\ \ \text{{error }} {d['err'][str(k)]:.2f} = \sqrt{{\textstyle\sum_{{k > {k}}} \sigma_k^2}},\ \ "
                           rf"\text{{storage }} {d['storage'][str(k)]:,}", font_size=24).move_to([3.4, -1.0, 0]) for k in ks}
        s = np.asarray(d["s"])
        A = axes([0, 30], [0, 1.0], x_length=5.4, y_length=1.8, xlabel=r"$k$", ylabel=r"share of $\sum \sigma^2$",
                 xticks=[1, 5, 10, 25], yticks=[0, 0.5, 1], center=[-3.6, -2.6, 0])
        en = np.asarray(d["energy"])[:30]
        ec = curve(A.ax, np.arange(1, 31), en, S.ACCENT, 3)
        tag = simulated_tag(r"simulated: the World's towns, \ log population density", corner=UL)
        color_note = label(rf"shared color scale: ${lo:.2f}$ to ${hi:.2f}$; \ all $60\times100$ entries shown",
                           font_size=20, color=GREY_B)
        if color_note.width > 5.6:
            color_note.width = 5.6
        color_note.move_to([3.4, -2.2, 0])
        intro = label('Compressing the population map', font_size=36)
        with self.voiceover(
            "Here's what that buys. <bookmark mark='a'/> The World's population density, drawn as a sixty by a "
            "hundred matrix: six thousand numbers. <bookmark mark='b'/> Its best rank-one approximation, one column "
            "times one row, is a blur. <bookmark mark='c'/> Rank two, five, ten: the island and its regions emerge. "
            "<bookmark mark='d'/> At rank twenty-five the picture is all but exact, stored in four thousand numbers "
            "instead of six thousand, and every error is exactly the root sum of the discarded squared singular "
            "values, as Eckart and Young promised. <bookmark mark='e'/> Most of the matrix's energy sits in a few "
            "singular values. That's the idea behind principal components in Part 31, and behind the sparse and "
            "low-rank methods of Parts 32 and 52."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(orig), FadeIn(ol))
            vo.wait_until("b")
            cur, cl = approx[ks[0]], labs[ks[0]]
            self.play(FadeIn(cur), FadeIn(cl), FadeIn(color_note))
            vo.wait_until("c")
            for k in ks[1:4]:
                self.play(Transform(cur, approx[k]), Transform(cl, labs[k]), run_time=1.2)
            vo.wait_until("d")
            self.play(Transform(cur, approx[ks[4]]), Transform(cl, labs[ks[4]]), run_time=1.2)
            vo.wait_until("e")
            self.play(FadeIn(A), Create(ec))
        self.clear_scene()

    def pca(self):
        e = load("extras")["pca"]
        rows = [
            cmath(r"X_c", r"=", r"U\Sigma V^\top", font_size=38),
            cmath(r"S", r"=", r"\frac{1}{n-1} X_c^\top X_c", r"=", r"V\, \frac{\Sigma^2}{n-1}\, V^\top", font_size=36),
        ]
        rows[1][4].set_color(EIG)
        whys = [why(r"the SVD of the centred data"), why(r"the spectral decomposition of the covariance")]
        nums = VGroup(
            MathTex(rf"\frac{{\sigma_k^2}}{{n-1}}:\ \ {e['sv2'][0]:.2f},\ {e['sv2'][1]:.2f}", r"\qquad",
                    rf"\text{{eigenvalues of }} S:\ \ {e['eig'][0]:.2f},\ {e['eig'][1]:.2f}", font_size=30),
            label(rf"the first principal axis carries {100 * e['share']:.0f}\% of the families' total variance", font_size=24,
                  color=S.ACCENT),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.7)
        nums[0][0].set_color(SIM)
        nums[0][2].set_color(EIG)
        intro = label('PCA from a data matrix', font_size=36)
        with self.voiceover(
            "The SVD and the spectral theorem are two views of the same thing in statistics. "
            "<bookmark mark='a'/> Take the SVD of the centred data matrix. <bookmark mark='b'/> Then the sample "
            "covariance, X c transpose X c over n minus one, is V times the squared singular values over n minus "
            "one times V transpose: its eigenvectors are the right singular vectors, and its eigenvalues the scaled "
            "squared singular values. <bookmark mark='c'/> For the families the two computations agree, and the "
            f"first principal axis carries {100 * e['share']:.0f} percent of the total variance. Many implementations compute principal components directly from the SVD of the data for numerical stability. Covariance eigensolvers are also used when their size and conditioning make them suitable."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=0.6, edge=6.9)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(nums, shift=UP * 0.2))
        self.clear_scene()

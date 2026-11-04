from __future__ import annotations

import numpy as np

from videos.stats.stats4.common import *  # noqa: F403


def block(label_tex, color, w=1.4, h=1.4) -> VGroup:
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.15)
    return VGroup(r, MathTex(label_tex, font_size=38, color=color).move_to(r))


class Blocks(VoiceoverScene):
    def construct(self):
        self.card()
        self.schur()
        self.inverse()
        self.woodbury()
        self.fwl()
        self.loo()

    def card(self):
        card = chapter_card(8, r"Block matrices", r"Eliminate a block, \ and the Schur complement is what is left",
                            lit=(), part=PART)
        with self.voiceover("Chapter eight. Block matrices."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def schur(self):
        M = VGroup(block("A", SPACE), block("B", GREY_A), block("C", GREY_A), block("D", RES))
        M.arrange_in_grid(2, 2, buff=0.05).move_to([-4.0, 0.6, 0])
        ml = MathTex(r"M =", font_size=40).next_to(M, LEFT, buff=0.2)
        rows = [
            cmath(r"\begin{pmatrix} I & 0 \\ -CA^{-1} & I \end{pmatrix} M", r"=",
                  r"\begin{pmatrix} A & B \\ 0 & D - CA^{-1}B \end{pmatrix}", font_size=30),
            cmath(r"M / A", r"=", r"D - CA^{-1}B", font_size=38),
            cmath(r"\det M", r"=", r"\det A \cdot \det(D - CA^{-1}B)", font_size=34),
        ]
        rows[1][0].set_color(EIG)
        whys = [why(r"block Gaussian elimination"), why(r"the Schur complement of $A$"), why(r"triangular blocks")]
        stat = label(r"for a normal vector: \ $\mathrm{Var}(\mathbf x_2 \mid \mathbf x_1) = \Sigma_{22} - \Sigma_{21}\Sigma_{11}^{-1}"
                     r"\Sigma_{12}$ \ (Part 5)", font_size=24, color=S.ACCENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Statistics constantly splits variables into groups: the ones we observe and the ones we don't, the "
            "parameters we care about and the nuisance ones. Matrices split with them. <bookmark mark='a'/> Write a "
            "matrix in four blocks. <bookmark mark='b'/> Eliminate the lower-left block, exactly as in Gaussian "
            "elimination but a block at a time. <bookmark mark='c'/> What's left in the corner, D minus C A inverse "
            "B, is called the Schur complement of A. <bookmark mark='d'/> The determinant factors through it. "
            "<bookmark mark='e'/> And it has a statistical meaning we'll prove in Part 5: for a normal vector, the "
            "conditional covariance of one group given the other is exactly a Schur complement of the covariance "
            "matrix."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(M), FadeIn(ml))
            step = ladder(self, rows, whys, keep=3, top=2.6, x=1.7, buff=0.55, edge=6.9)
            vo.wait_until("b")
            step(0, transform=False)
            vo.wait_until("c")
            step(1, transform=False)
            vo.wait_until("d")
            step(2, transform=False)
            vo.wait_until("e")
            self.play(FadeIn(stat))
        self.clear_scene()

    def inverse(self):
        d = load("blocks")
        rows = [
            cmath(r"M^{-1}", r"=", r"\begin{pmatrix} A^{-1} + A^{-1}B\,S^{-1}CA^{-1} & -A^{-1}B\,S^{-1} \\ -S^{-1}CA^{-1} & S^{-1} "
                  r"\end{pmatrix}", font_size=30),
        ]
        whys = [why(r"$S = D - CA^{-1}B$")]
        corner = label(r"the lower-right block of $M^{-1}$ is $S^{-1}$: \ inverting a big matrix by inverting small ones",
                       font_size=24, color=GREY_A)
        chk = MathTex(r"\text{checked numerically on a } 6 \times 6 \text{ matrix}", font_size=24, color=SIM)
        VGroup(corner, chk).arrange(DOWN, buff=0.3).move_to([0, -1.4, 0])
        with self.voiceover(
            "Finishing the elimination gives the inverse of a block matrix. <bookmark mark='a'/> Every block of M "
            "inverse is built from A inverse and the inverse of the Schur complement S. <bookmark mark='b'/> In "
            "particular, the lower-right block is just S inverse. Inverting a big matrix reduces to inverting two "
            "small ones, and the compute file checks every block against a direct inverse."
        ) as vo:
            step = ladder(self, rows, whys, keep=1, top=1.6, x=-0.8, buff=0.5, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            self.play(FadeIn(corner), FadeIn(chk))
        _ = d
        self.clear_scene()

    def woodbury(self):
        d = load("blocks")
        rows = [
            cmath(r"(A + UCV)^{-1}", r"=", r"A^{-1} - A^{-1}U\,(C^{-1} + VA^{-1}U)^{-1}\,VA^{-1}", font_size=32),
            cmath(r"(A + \mathbf u\mathbf v^\top)^{-1}", r"=", r"A^{-1} - \frac{A^{-1}\mathbf u\, \mathbf v^\top A^{-1}}"
                  r"{1 + \mathbf v^\top A^{-1}\mathbf u}", font_size=32),
        ]
        rows[0][2].set_color(FIT)
        whys = [why(r"Woodbury (1950): \ the inverse of a low-rank update"), why(r"Sherman--Morrison: \ rank one")]
        cost = VGroup(label(r"a new observation adds $\mathbf x\mathbf x^\top$ to $X^\top X$: \ update the inverse in $O(p^2)$, "
                            r"\ not $O(p^3)$", font_size=24, color=GREY_A),
                      MathTex(rf"\text{{max error vs.\ direct inverse: }} {d['err_sm']:.1e}", font_size=26, color=SIM),
                      label(r"also: \ Gaussian processes and the Kalman filter (Parts 38--39)", font_size=24, color=S.ACCENT))
        cost.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "One block identity deserves its own name. <bookmark mark='a'/> The Woodbury identity gives the inverse "
            "of a matrix plus a low-rank update in terms of the inverse you already have and a small matrix the "
            "size of the update. <bookmark mark='b'/> For a rank-one update it's the Sherman–Morrison formula. "
            "<bookmark mark='c'/> It's why regression can be updated cheaply when one new observation arrives, in p "
            "squared operations instead of p cubed, and it's the engine inside Gaussian process regression and the "
            "Kalman filter later in the degree."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.8, buff=0.7, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(cost, shift=UP * 0.2))
        self.clear_scene()

    def fwl(self):
        e = load("extras")["fwl"]
        rx, ry = np.asarray(e["rx"]), np.asarray(e["ry"])
        rows = [
            cmath(r"\mathbf y", r"=", r"Z\boldsymbol\gamma + \mathbf x\beta + \boldsymbol\varepsilon", font_size=34),
            cmath(r"\hat\beta", r"=", r"\frac{\langle M_Z\mathbf x,\ M_Z\mathbf y\rangle}{\|M_Z\mathbf x\|^2}", font_size=36),
        ]
        rows[1][0].set_color(EXACT)
        whys = [why(r"$Z$: \ intercept and father's height; \ $\mathbf x$: \ mother's"),
                why(r"$M_Z = I - P_Z$: \ the block inverse, \ written as projections")]
        A = axes([-20, 20], [-25, 25], x_length=4.4, y_length=2.9, xlabel=r"mother's height, \ father removed",
                 ylabel=r"child, \ father removed", xticks=[-15, 0, 15], yticks=[-20, 0, 20], center=[-3.8, -2.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.025, color=DATA, fill_opacity=0.7) for a, b in zip(rx, ry) if abs(a) < 20 and abs(b) < 25])
        ln = Line(ax.c2p(-18, -18 * e["b_fwl"]), ax.c2p(18, 18 * e["b_fwl"]), color=EXACT, stroke_width=3)
        nums = VGroup(MathTex(rf"\text{{full regression: }} \hat\beta_{{\text{{mother}}}} = {e['b_full'][2]:.4f}", font_size=28, color=FIT),
                      MathTex(rf"\text{{residual on residual: }} {e['b_fwl']:.4f}", font_size=28, color=EXACT),
                      MathTex(rf"\text{{mother alone: }} {e['b_simple']:.4f}", font_size=28, color=GREY_A),
                      label(r"the same number: \ ``holding the father fixed'', \ made exact", font_size=22, color=GREY_B))
        nums.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, -1.9, 0])
        hc = note(r"Frisch \& Waugh (1933); \ Lovell (1963)").to_corner(DR, buff=0.3)
        tag = simulated_tag(r"simulated: 300 of the World's families", corner=UR)
        with self.voiceover(
            "Block inverses explain one of the most useful facts in regression. <bookmark mark='a'/> Regress a "
            "child's height on both parents. Split the columns into two blocks: the intercept and the father's "
            "height, Z, and the mother's height, x. <bookmark mark='b'/> Work out the mother's coefficient from the "
            "block inverse, and it simplifies to this: remove the father's influence from both the child and the "
            "mother, by projecting it out, then regress residual on residual. <bookmark mark='c'/> Here are the "
            "three hundred residual pairs and their line. <bookmark mark='d'/> Its slope is exactly the mother's "
            "coefficient in the full regression, to every digit. That's the Frisch–Waugh–Lovell theorem, and it's "
            "what holding the father fixed means. Ignoring the father gives a slightly different answer, because in "
            "the World tall mothers tend to marry tall fathers."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc))
            step = ladder(self, rows, whys, keep=2, top=2.9, x=-0.2, buff=0.5, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(dots, lag_ratio=0.003), Create(ln))
            vo.wait_until("d")
            self.play(FadeIn(nums))
        self.clear_scene()

    def loo(self):
        e = load("extras2")["loo"]
        fo, di = np.asarray(e["formula"]), np.asarray(e["direct"])
        rows = [
            cmath(r"\hat y_{i,(-i)}", r"=", r"\text{fit without observation } i", font_size=32),
            cmath(r"y_i - \hat y_{i,(-i)}", r"=", r"\frac{e_i}{1 - h_{ii}}", font_size=40),
        ]
        rows[1][2].set_color(EXACT)
        whys = [why(r"removing a row is a rank-one change to $X^\top X$"), why(r"Sherman--Morrison, \ simplified")]
        A = axes([-25, 25], [-25, 25], x_length=4.0, y_length=4.0, xlabel=r"refit 40 times", ylabel=r"formula",
                 xticks=[-20, 0, 20], yticks=[-20, 0, 20], center=[-3.6, -1.4, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(-25, -25), ax.c2p(25, 25), color=GREY_C, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=EXACT) for a, b in zip(di, fo) if abs(a) < 25 and abs(b) < 25])
        nums = VGroup(MathTex(rf"\text{{max difference: }} {e['err']:.0e}", font_size=28, color=SIM),
                      MathTex(rf"\text{{PRESS}} = \sum_i \Big(\frac{{e_i}}{{1 - h_{{ii}}}}\Big)^2 = {e['press']:.0f}", font_size=28),
                      MathTex(rf"\text{{RSS}} = {e['rss']:.0f}", font_size=28, color=GREY_A),
                      label(r"cross-validation for free: \ one fit, not forty \ (Part 19)", font_size=24, color=S.ACCENT))
        nums.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.2, -1.2, 0])
        with self.voiceover(
            "Sherman–Morrison has a famous consequence for regression. <bookmark mark='a'/> Suppose we want each "
            "observation's prediction from a fit that didn't use it: leave-one-out cross-validation, which seems to "
            "need forty separate regressions. <bookmark mark='b'/> Removing one row changes X transpose X by a rank-one "
            "matrix, and Sherman–Morrison simplifies the whole calculation to one line: the leave-one-out residual "
            "is the ordinary residual divided by one minus its leverage. <bookmark mark='c'/> Refitting forty times "
            "and using the formula agree to twelve digits. <bookmark mark='d'/> Their sum of squares, called PRESS, is "
            "a little larger than the ordinary residual sum of squares, an honest estimate of prediction error, "
            "computed from one fit. Part 19 builds model selection on this idea."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.9, x=0.6, buff=0.5, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(A), Create(diag), FadeIn(dots), FadeIn(nums[0]))
            vo.wait_until("d")
            self.play(FadeIn(nums[1:]))
        self.clear_scene()

from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403


class Lines(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.why_differ()
        self.attenuation()

    def card(self):
        card = chapter_card(8, r"Three lines through one ellipse", r"$Y$ on $X$, \ $X$ on $Y$, \ and the major axis", lit=(1886,),
                            part=PART)
        with self.voiceover("Chapter eight. Three lines through one ellipse."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def three(self):
        d = load("galton")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        mx, my = d["mx"], d["my"]
        g = np.random.Generator(np.random.PCG64(3))
        jx, jy = x + g.uniform(-0.45, 0.45, len(x)), y + g.uniform(-0.45, 0.45, len(y))
        A = axes([62, 75], [60, 77], x_length=4.6, y_length=4.6 * 17 / 13, xlabel=r"mid-parent (in)", ylabel=r"child (in)",
                 xticks=[64, 68, 72], yticks=[62, 66, 70, 74], center=[-3.8, -0.2, 0])
        ax = A.ax
        pts = scatter(ax, jx, jy, color=DATA, radius=0.02, opacity=0.4)
        S_ = np.asarray(d["S"])
        ell = ellipse_curve(ax, [mx, my], S_, 2.0, GREY_B, 2.0, 0.8)
        def line(slope, col):
            x0, x1 = max(62, mx + (60 - my) / slope), min(75, mx + (77 - my) / slope)
            return Line(ax.c2p(x0, my + slope * (x0 - mx)), ax.c2p(x1, my + slope * (x1 - mx)), color=col, stroke_width=3.5)
        l_yx = line(d["b_yx"], LINE_YX)
        l_xy = line(1 / d["b_xy"], LINE_XY)
        l_maj = line(d["major"], LINE_MAJ)
        rows = VGroup(
            MathTex(rf"Y \text{{ on }} X:\ \text{{slope }} r\,\tfrac{{s_y}}{{s_x}} = {d['b_yx']:.2f}", font_size=28, color=LINE_YX),
            label(r"through the ellipse's \emph{vertical} tangent points", font_size=20, color=GREY_B),
            MathTex(rf"X \text{{ on }} Y:\ \text{{slope }} \tfrac{{1}}{{r}}\,\tfrac{{s_y}}{{s_x}} = {1 / d['b_xy']:.2f}", font_size=28, color=LINE_XY),
            label(r"through the \emph{horizontal} tangent points", font_size=20, color=GREY_B),
            MathTex(rf"\text{{major axis: slope }} {d['major']:.2f}", font_size=28, color=LINE_MAJ),
            label(r"the first principal component \ (Part 4)", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, 0.6, 0])
        src = historical_tag(r"Galton (1886)", corner=DR)
        with self.voiceover(
            "There isn't one line through a cloud of points; there are three, and confusing them causes real "
            "mistakes. <bookmark mark='a'/> The regression of child on mid-parent, the conditional mean, has slope "
            f"{d['b_yx']:.2f}. It passes through the points where the ellipse's tangent is vertical: for each x, the "
            "middle of the vertical slice. <bookmark mark='b'/> The regression of mid-parent on child, predicting "
            "parents from children, is a different line, much steeper when drawn on the same axes. It passes through "
            "the horizontal tangent points. <bookmark mark='c'/> And between them lies the major axis of the "
            "ellipse, the direction of greatest spread: Part 4's first principal component. Galton noticed in 1889 "
            "that regression runs both ways, from parents to children and from children back to parents."
        ) as vo:
            self.play(FadeIn(A), FadeIn(pts, lag_ratio=0.001), Create(ell), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(l_yx), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(Create(l_xy), FadeIn(rows[2:4]))
            vo.wait_until("c")
            self.play(Create(l_maj), FadeIn(rows[4:]))
        self.clear_scene()

    def why_differ(self):
        rows = VGroup(
            MathTex(r"\text{the } Y\text{-on-}X \text{ line minimizes squared vertical distances}", font_size=30, color=LINE_YX),
            MathTex(r"\text{the } X\text{-on-}Y \text{ line minimizes squared horizontal distances}", font_size=30, color=LINE_XY),
            MathTex(r"\text{the major axis minimizes squared perpendicular distances}", font_size=30, color=LINE_MAJ),
            MathTex(r"\text{they coincide only when } |r| = 1", font_size=32, color=S.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, 0.8, 0])
        use = VGroup(label(r"predicting $Y$ from $X$: \ use $Y$ on $X$", font_size=26),
                     label(r"measuring a relationship with error in both variables: \ errors-in-variables (Part 23)", font_size=26,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.7)
        intro = label('Three squared-distance objectives', font_size=36)
        with self.voiceover(
            "Why three? Because they answer three questions. <bookmark mark='a'/> The regression of y on x minimizes "
            "the squared vertical distances from the points: the best way to predict y from x. <bookmark mark='b'/> The "
            "regression of x on y minimizes the squared horizontal ones: the best way to predict x from y. "
            "<bookmark mark='c'/> The major axis minimizes squared perpendicular distances, treating the two variables "
            "symmetrically. <bookmark mark='d'/> Only for a perfect correlation do the three agree. "
            "<bookmark mark='e'/> To predict, use the regression of the variable you're predicting. When both "
            "variables are measured with error and you want the underlying relationship, neither regression is right; "
            "that's the errors-in-variables problem of Part 23."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(use))
        self.clear_scene()

    def attenuation(self):
        d = load("extras2")["atten"]
        x, y, w = np.asarray(d["x"]), np.asarray(d["y"]), np.asarray(d["w"])
        keep = (np.abs(x) < 3.9) & (np.abs(w) < 3.9) & (np.abs(y) < 3.9)
        x, y, w = x[keep], y[keep], w[keep]
        A = axes([-4, 4], [-4, 4], x_length=5.0, y_length=5.0, xlabel=r"$X$ \ or \ $W = X + U$", ylabel=r"$Y$",
                 xticks=[-2, 0, 2], yticks=[-2, 0, 2], center=[-3.5, -0.4, 0])
        ax = A.ax
        pt = scatter(ax, x, y, color=LINE_YX, radius=0.018, opacity=0.5, xr=[-4, 4], yr=[-4, 4])
        pw = scatter(ax, w, y, color=S.RESID, radius=0.018, opacity=0.5, xr=[-4, 4], yr=[-4, 4])
        lt = Line(ax.c2p(-3.5, -3.5 * d["b_true"]), ax.c2p(3.5, 3.5 * d["b_true"]), color=LINE_YX, stroke_width=3.5)
        lw = Line(ax.c2p(-4, -4 * d["b_obs"]), ax.c2p(4, 4 * d["b_obs"]), color=S.RESID, stroke_width=3.5)
        rows = [
            cmath(r"\hat\beta_{W}", r"\to", r"\frac{\mathrm{Cov}(X + U, Y)}{\mathrm{Var}(X + U)}", r"=",
                  r"\beta\,\frac{\sigma_X^2}{\sigma_X^2 + \sigma_U^2}", font_size=28),
            cmath(r"\lambda", r"=", r"\frac{\sigma_X^2}{\sigma_X^2 + \sigma_U^2}", r"=", r"0.5", font_size=30),
            cmath(r"\text{slope}", r"=", rf"{d['b_true']:.2f}\ \to\ {d['b_obs']:.2f}", font_size=30),
        ]
        rows[0][4].set_color(S.RESID)
        rows[2][2].set_color(S.RESID)
        whys = [why(r"$U$ independent noise in $X$: \ the covariance survives, \ the variance grows"),
                why(r"the reliability ratio"), why(r"simulated: \ $\sigma_X = \sigma_U = 1$")]
        spear = label(r"Spearman (1904): \ divide a correlation by $\sqrt{\text{reliability}_X\,\text{reliability}_Y}$ \ to undo it",
                      font_size=22, color=GREY_A).to_edge(DOWN, buff=0.4).shift(RIGHT * 2.6)
        if spear.width > 7.4:
            spear.width = 7.4
        tag = note(r"simulated: subset of 1,500; off-panel points omitted; slopes use all draws").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Here's what goes wrong when x is measured with error. <bookmark mark='a'/> In blue, y against the true "
            "x, with slope one. <bookmark mark='b'/> Now we don't see x, only x plus independent noise of the same "
            "size. The cloud spreads sideways, and the fitted slope falls to about a half. <bookmark mark='c'/> The "
            "reason is one line: noise in x leaves the covariance with y unchanged but inflates the variance of x, "
            "so the slope is multiplied by the reliability ratio, the share of x's variance that's real. "
            "<bookmark mark='d'/> Here it's a half. This is regression dilution: errors in the predictor bias the "
            "slope toward zero, and it's the same arithmetic as regression to the mean. <bookmark mark='e'/> "
            "Charles Spearman saw it in 1904 and proposed correcting a correlation for the unreliability of both "
            "measurements."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(pt), Create(lt))
            vo.wait_until("b")
            self.play(*[p.animate.move_to(q.get_center()) for p, q in zip(pt, pw)], run_time=2.5)
            self.play(Create(lw))
            step = ladder(self, rows, whys, keep=3, top=2.6, x=2.9, buff=0.7, edge=6.9)
            vo.wait_until("c")
            step(0, transform=False)
            vo.wait_until("d")
            step(1, transform=False)
            step(2, transform=False)
            vo.wait_until("e")
            self.play(FadeIn(spear))
        self.clear_scene()

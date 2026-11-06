from __future__ import annotations

import numpy as np

from videos.stats.stats4.common import *  # noqa: F403


class Pinv(VoiceoverScene):
    def construct(self):
        self.card()
        self.minimum_norm()
        self.definition()
        self.dummy()
        self.ridge()

    def card(self):
        card = chapter_card(7, r"Generalized inverses", r"When $A^\top A$ has no inverse", lit=(1955,), part=PART)
        with self.voiceover("Chapter seven. Generalized inverses."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def minimum_norm(self):
        d = load("pinv")
        xmin = np.asarray(d["xmin"])
        A = axes([-1.5, 4.5], [-0.5, 3.0], x_length=6.6, y_length=3.85, xlabel=r"$x_1$", ylabel=r"$x_2$",
                 xticks=[0, 2, 4], yticks=[0, 1, 2], center=[-3.0, -0.4, 0])
        ax = A.ax
        line = Line(ax.c2p(-1.5, 2.75), ax.c2p(4.5, -0.25), color=SPACE, stroke_width=4)
        ll = MathTex(r"x_1 + 2x_2 = 4", font_size=28, color=SPACE).next_to(ax.c2p(3.2, 0.4), UR, buff=0.1)
        t = ValueTracker(-1.2)
        moving = always_redraw(lambda: Dot(ax.c2p(t.get_value(), (4 - t.get_value()) / 2), radius=0.08, color=DATA))
        radius_line = always_redraw(lambda: DashedLine(ax.c2p(0, 0),
            ax.c2p(t.get_value(), (4 - t.get_value()) / 2), color=GREY_B, stroke_width=1.5))
        circle = Arc(radius=np.linalg.norm(ax.c2p(*xmin) - ax.c2p(0, 0)), start_angle=0, angle=PI/2,
                     arc_center=ax.c2p(0, 0), stroke_color=GREY_B, stroke_width=1.5)
        best = Dot(ax.c2p(*xmin), radius=0.1, color=FIT)
        perp = DashedLine(ax.c2p(0, 0), ax.c2p(*xmin), color=FIT, stroke_width=2.5)
        info = VGroup(MathTex(r"A = (1\ \ 2),\quad \mathbf b = 4", font_size=32),
                      label(r"one equation, two unknowns: \ infinitely many solutions", font_size=24, color=GREY_A),
                      MathTex(rf"A^+\mathbf b = ({xmin[0]:.1f},\ {xmin[1]:.1f})", font_size=32, color=FIT),
                      label(r"the solution closest to the origin: \ $\perp$ to the solution line", font_size=24,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, 0.6, 0])
        with self.voiceover(
            "The projection formula needs A transpose A to be invertible, which fails when columns are redundant, "
            "or when there are more unknowns than equations. <bookmark mark='a'/> The simplest case: one equation, "
            "x one plus two x two equals four, in two unknowns. Every point on this line is a solution. "
            "<bookmark mark='b'/> Which one should we report? Slide along the line and watch the distance to the "
            "origin. <bookmark mark='c'/> There's a unique closest solution, where the line is tangent to a circle "
            "around the origin: the foot of the perpendicular. <bookmark mark='d'/> That minimum-norm solution is "
            "what the Moore–Penrose pseudoinverse gives: point eight, one point six."
        ) as vo:
            self.play(FadeIn(A), Create(line), FadeIn(ll), FadeIn(info[0]))
            vo.wait_until("a")
            self.play(FadeIn(info[1]))
            vo.wait_until("b")
            self.add(moving, radius_line)
            self.play(t.animate.set_value(4.2), run_time=4.0)
            vo.wait_until("c")
            self.play(t.animate.set_value(float(xmin[0])), run_time=2.0)
            self.play(Create(circle), Create(perp), FadeIn(best))
            vo.wait_until("d")
            self.play(FadeIn(info[2:]))
        moving.clear_updaters()
        radius_line.clear_updaters()
        self.clear_scene()

    def definition(self):
        th = theorem_card(r"The Moore--Penrose pseudoinverse", r"for any $A = U\Sigma V^\top$: \ $A^+ = V\Sigma^+ U^\top$, \ "
                          r"inverting the nonzero singular values and leaving the zeros", who=r"E. H. Moore (1920); \ "
                          r"R. Penrose (1955)", color=FIT, width=8.0, font_size=24).to_edge(UP, buff=0.5)
        props = VGroup(
            MathTex(r"AA^+A = A,\quad A^+AA^+ = A^+,\quad (AA^+)^\top = AA^+,\quad (A^+A)^\top = A^+A", font_size=28),
            MathTex(r"AA^+ \text{ is the projection onto the column space of } A", font_size=30, color=SPACE),
            MathTex(r"\hat{\boldsymbol\beta} = X^+\mathbf y", r"\ :\ ", r"\text{least squares, \ minimum norm}", font_size=30,
                    color=FIT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(th, DOWN, buff=0.5)
        use = label(r"rank-deficient designs (Part 13), \ ridge regression as $\lambda \to 0$ (Part 19)", font_size=24,
                    color=S.ACCENT).to_edge(DOWN, buff=0.6)
        intro = label('An inverse for every matrix', font_size=36)
        with self.voiceover(
            "The general definition comes from the singular value decomposition. <bookmark mark='a'/> Invert every "
            "nonzero singular value, leave the zeros alone, and swap the two rotations: that's A plus, defined for "
            "every matrix. Eliakim Moore found it in 1920 and Roger Penrose rediscovered it in 1955. "
            "<bookmark mark='b'/> Penrose characterized it by four equations. <bookmark mark='c'/> And A times A "
            "plus is always the projection onto the column space of A, so X plus times y is a least-squares "
            "solution even when X transpose X can't be inverted: the one with the smallest norm. "
            "<bookmark mark='d'/> It turns up whenever a design has redundant columns, and as the limit of ridge "
            "regression when the penalty vanishes."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(th, shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(props[0]))
            vo.wait_until("c")
            self.play(FadeIn(props[1:]))
            vo.wait_until("d")
            self.play(FadeIn(use))
        self.clear_scene()

    def dummy(self):
        e = load("extras")["dummy"]
        X = VGroup(MathTex(r"X = \begin{pmatrix} 1 & 1 & 0 & 0 \\ 1 & 0 & 1 & 0 \\ 1 & 0 & 0 & 1 \\ \vdots & \vdots & \vdots & "
                           r"\vdots \end{pmatrix}", font_size=32),
                   label(r"intercept, \ and an indicator for each of 3 regions", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.2)
        X.move_to([-4.2, 1.2, 0])
        trap = VGroup(MathTex(r"\text{col}_1 = \text{col}_2 + \text{col}_3 + \text{col}_4", font_size=28, color=RES),
                      MathTex(rf"\operatorname{{rank}} X = {e['rank']} < 4", font_size=28, color=RES)).arrange(DOWN, buff=0.15)
        trap.next_to(X, DOWN, buff=0.4)
        b1, b2 = e["bmin"], e["alt"]
        sols = VGroup(
            MathTex(r"X^+\mathbf y = (" + ", ".join(f"{v:.2f}" for v in b1) + ")", font_size=28, color=FIT),
            MathTex(r"\text{also: }(" + ", ".join(f"{v:.2f}" for v in b2) + ")", font_size=28, color=GREY_A),
            label(r"both fit exactly as well: \ they differ by a multiple of $(1, -1, -1, -1)$", font_size=22, color=GREY_B),
            MathTex(rf"\beta_{{\text{{region 2}}}} - \beta_{{\text{{region 1}}}} = {e['diff_min']:.2f}\ \text{{in both}}", font_size=30,
                    color=EXACT),
            label(r"estimable: \ the differences between regions, \ which equal the differences of their means", font_size=22,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.8, 0.2, 0])
        for s_ in sols:
            if s_.width > 7.0:
                s_.width = 7.0
        tag = note(r"illustrative: 12 observations in 3 regions").to_corner(DL, buff=0.3)
        intro = label('Redundant indicator columns', font_size=36)
        with self.voiceover(
            "Here's where rank deficiency happens in practice, and it catches beginners every year. "
            "<bookmark mark='a'/> Put an intercept in a regression, and an indicator column for every one of three "
            "regions. <bookmark mark='b'/> The three indicators add up to the intercept column, so the columns are "
            "dependent, X transpose X is singular, and there's no unique answer: the dummy-variable trap. "
            "<bookmark mark='c'/> The pseudoinverse still gives a least-squares solution, the one of minimum norm. "
            "<bookmark mark='d'/> But add any multiple of one, minus one, minus one, minus one, and the fit doesn't "
            "change: another solution, equally good. <bookmark mark='e'/> What doesn't change is any difference "
            f"between regions: region two minus region one is {e['diff_min']:.0f} in every solution, the difference "
            "of the two regions' means. Such combinations are called estimable, and Part 13's designed experiments "
            "are built around them."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(X))
            vo.wait_until("b")
            self.play(FadeIn(trap))
            vo.wait_until("c")
            self.play(FadeIn(sols[0]))
            vo.wait_until("d")
            self.play(FadeIn(sols[1:3]))
            vo.wait_until("e")
            self.play(FadeIn(sols[3:]))
        self.clear_scene()

    def ridge(self):
        e = load("extras3")["ridge"]
        lams, path, pinv = np.asarray(e["lams"]), np.asarray(e["path"]), np.asarray(e["pinv"])
        A = axes([-6, 2], [-5, 60], x_length=7.6, y_length=4.2, xlabel=r"$\log_{10}\lambda$", ylabel=r"coefficient",
                 xticks=[-6, -4, -2, 0, 2], yticks=[0, 20, 40, 60], center=[-1.8, -0.6, 0])
        ax = A.ax
        cols = [GREY_A, S.EST, S.LIK, S.POST]
        cvs = VGroup(*[curve(ax, lams, path[:, j], cols[j], 3) for j in range(4)])
        ends = VGroup(*[Dot(ax.c2p(-6, pinv[j]), radius=0.07, color=EXACT) for j in range(4)])
        leg = legend([(cols[0], r"intercept"), (cols[1], r"region 1"), (cols[2], r"region 2"), (cols[3], r"region 3")],
                     font_size=20).move_to([4.6, 1.8, 0])
        f = MathTex(r"\hat{\boldsymbol\beta}_\lambda = (X^\top X + \lambda I)^{-1} X^\top\mathbf y", r"\ \xrightarrow{\ \lambda \to 0\ }\ ",
                    r"X^+\mathbf y", font_size=30).to_edge(UP, buff=0.35)
        f[2].set_color(EXACT)
        nt = label(r"gold: \ the pseudoinverse solution", font_size=22, color=EXACT).move_to([4.6, 0.4, 0])
        intro = label('The limit of a ridge path', font_size=36)
        with self.voiceover(
            "There's another way to reach the pseudoinverse, and it previews a central idea of modern statistics. "
            "<bookmark mark='a'/> Penalize all coefficients, including the intercept in this example, by adding a positive multiple of the identity to X transpose X. Now it's "
            "always invertible, whatever the rank: that's ridge regression, Hoerl and Kennard's method from 1970. "
            "<bookmark mark='b'/> Follow the coefficients as lambda shrinks. With a big penalty they're squashed "
            "toward zero; as the penalty vanishes, <bookmark mark='c'/> they converge exactly to the pseudoinverse "
            "solution. Adding lambda trades a little bias for a lot of stability, and Part 19 makes that trade the "
            "heart of learning from data."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(A), LaggedStart(*[Create(c) for c in cvs], lag_ratio=0.2), FadeIn(leg), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(ends), FadeIn(nt))
        self.clear_scene()

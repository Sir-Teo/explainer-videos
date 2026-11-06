from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403


class Joint(VoiceoverScene):
    def construct(self):
        self.card()
        self.discrete()
        self.surface()
        self.slicing()
        self.bayes()
        self.dice()

    def card(self):
        card = chapter_card(1, r"Joint, marginal, conditional", r"Three ways to read one table", lit=(1886,), part=PART)
        with self.voiceover("Chapter one. Joint, marginal, conditional."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def discrete(self):
        d = load("galton")
        P, C, T = np.asarray(d["P"]), np.asarray(d["C"]), np.asarray(d["T"])
        # collapse to 4 x 4 bands for a readable table
        pb = [(0, 3), (3, 6), (6, 8), (8, 11)]
        cb = [(0, 4), (4, 7), (7, 10), (10, 14)]
        M = np.array([[T[a:b, c:e].sum() for c, e in cb] for a, b in pb])
        n = M.sum()
        cell = 1.0
        grid = VGroup()
        cells = {}
        for i in range(4):
            for j in range(4):
                sq = Square(side_length=cell, stroke_color=GREY_D, stroke_width=1, fill_color="#121722", fill_opacity=1)
                sq.move_to([-5.0 + j * cell, -1.6 + i * cell, 0])
                t = MathTex(rf"{M[i, j] / n:.3f}", font_size=22).move_to(sq)
                cells[(i, j)] = VGroup(sq, t)
                grid.add(cells[(i, j)])
        rlabs = [r"$\le 65.5$", r"66.5--68.5", r"69.5--70.5", r"$\ge 71.5$"]
        clabs = [r"$\le 64.2$", r"65.2--67.2", r"68.2--70.2", r"$\ge 71.2$"]
        rl = VGroup(*[label(t, font_size=18, color=GREY_B).next_to(cells[(i, 0)], LEFT, buff=0.12) for i, t in enumerate(rlabs)])
        cl = VGroup(*[label(t, font_size=18, color=GREY_B).next_to(cells[(0, j)], DOWN, buff=0.12) for j, t in enumerate(clabs)])
        marg_r = VGroup(*[MathTex(rf"{M[i].sum() / n:.3f}", font_size=22, color=MARG).next_to(cells[(i, 3)], RIGHT, buff=0.25)
                          for i in range(4)])
        marg_c = VGroup(*[MathTex(rf"{M[:, j].sum() / n:.3f}", font_size=22, color=MARG).next_to(cells[(3, j)], UP, buff=0.25)
                          for j in range(4)])
        top = 3
        cond = VGroup(*[MathTex(rf"{M[top, j] / M[top].sum():.3f}", font_size=24, color=COND) for j in range(4)])
        for j, c in enumerate(cond):
            c.move_to([1.6 + j * 1.15, 1.6, 0])
        ch = label(r"$P(\text{child} \mid \text{tallest parents})$", font_size=24, color=COND).next_to(cond, UP, buff=0.25)
        rows = VGroup(
            MathTex(r"p(x, y)", r"\quad \text{joint}", font_size=30),
            MathTex(r"p(x) = \sum_y p(x, y)", r"\quad \text{marginal: add along a row}", font_size=28, color=MARG),
            MathTex(r"p(y \mid x) = \frac{p(x, y)}{p(x)}", r"\quad \text{conditional: a row, renormalized}", font_size=28,
                    color=COND),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.0, -1.2, 0])
        for r in rows:
            r[1].set_color(GREY_B)
        src = historical_tag(r"Galton (1886), grouped into 4 $\times$ 4 bands")
        intro = label('Three distributions in one table', font_size=36)
        with self.voiceover(
            "With two variables there are three different distributions in one table. <bookmark mark='a'/> Group "
            "Galton's children into four bands of mid-parent height and four of child height, and divide by nine "
            "hundred and twenty-eight: the joint distribution, the chance of each combination. <bookmark mark='b'/> "
            "Add along each row and you get the marginal distribution of the mid-parent's height, ignoring the "
            "child. <bookmark mark='c'/> Add down each column and you get the marginal for the child. "
            "<bookmark mark='d'/> Now take just the tallest parents' row and divide it by its total: the "
            "conditional distribution of the child's height, given the tallest parents. It's Part 2's conditioning, "
            "keep a slice and renormalize, applied to a table."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.04), FadeIn(rl), FadeIn(cl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(marg_r), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(marg_c))
            vo.wait_until("d")
            self.play(*[cells[(top, j)][0].animate.set_fill(COND, opacity=0.35) for j in range(4)])
            self.play(TransformFromCopy(VGroup(*[cells[(top, j)][1] for j in range(4)]), cond), FadeIn(ch), FadeIn(rows[2]))
        self.clear_scene()

    def surface(self):
        d = load("slicer")
        gs = GaussianSlicer([d["mx"], d["my"]], d["S"], (154, 185), (152, 200), center=(-2.2, -1.9, 0))
        objs = gs.objects()
        info = VGroup(label(r"the World's mid-parents and sons: \ a bivariate normal fit", font_size=24, color=WORLD),
                      MathTex(r"f(x, y) = \frac{1}{2\pi\sqrt{\det\Sigma}}\, e^{-\frac12 (\mathbf z - \boldsymbol\mu)^\top \Sigma^{-1} "
                              r"(\mathbf z - \boldsymbol\mu)}", font_size=28),
                      label(r"height of the surface: \ density; \ volume under it: \ $1$", font_size=22, color=GREY_B))
        info.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UR, buff=0.4)
        for i_ in info:
            if i_.width > 6.4:
                i_.width = 6.4
        axl = VGroup(label(r"mid-parent", font_size=22, color=GREY_B).move_to([-0.2, -3.4, 0]),
                     label(r"son", font_size=22, color=GREY_B).move_to([-5.6, -2.2, 0]))
        tag = simulated_tag(rf"simulated: the World's {fmt_int(d['n'])} sons")
        with self.voiceover(
            "For continuous variables the table becomes a surface. <bookmark mark='a'/> Here's a fitted model of the joint density of "
            "mid-parent height and a son's height in the World, as a bivariate normal: the height of the surface over "
            "each point is the density there, and the volume underneath is one. <bookmark mark='b'/> Turn it around. "
            "It's a ridge, running diagonally, because tall parents go with tall sons; seen from above, its contour "
            "lines are Galton's ellipses."
        ) as vo:
            self.add(gs.ns, *objs)
            self.play(NSpace.reveal(*objs, run_time=2.0), FadeIn(tag), FadeIn(axl))
            vo.wait_until("a")
            self.play(FadeIn(info))
            vo.wait_until("b")
            self.play(FadeOut(axl), gs.ns.turn(0.9, run_time=5.0))
            self.play(gs.ns.tilt.animate.set_value(1.2), run_time=2.5)
            self.play(gs.ns.tilt.animate.set_value(0.42), gs.ns.angle.animate.set_value(-0.75), run_time=2.5)
        gs.stop()
        self.clear_scene()

    def slicing(self):
        d = load("slicer")
        gs = GaussianSlicer([d["mx"], d["my"]], d["S"], (154, 185), (152, 200), center=(-2.2, -1.9, 0))
        objs = gs.objects()
        cols = [S.EST, S.ACCENT, S.RESID]
        slices = [gs.slice(sl["x0"], color=c) for sl, c in zip(d["slices"], cols)]
        renorm = [gs.slice(sl["x0"], color=c, renorm=True, fill_opacity=0.2) for sl, c in zip(d["slices"], cols)]
        rows = VGroup(*[MathTex(rf"x = {sl['x0']:.0f}:\ \ E[Y \mid x] = {sl['cm']:.1f},\ \ \mathrm{{SD}} = {sl['cs']:.2f}", font_size=26,
                                color=c) for sl, c in zip(d["slices"], cols)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.4)
        emp = VGroup(*[MathTex(rf"\text{{World, }} n = {sl['n']}:\ \ {sl['emp_mean']:.1f},\ \ {sl['emp_sd']:.2f}", font_size=22,
                               color=GREY_A) for sl in d["slices"]])
        emp.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(rows, DOWN, buff=0.35).align_to(rows, LEFT)
        f = MathTex(r"f(y \mid x)", r"=", r"\frac{f(x, y)}{f_X(x)}", r"=", r"\frac{f(x, y)}{\int f(x, y')\, dy'}", font_size=32)
        f.to_edge(DOWN, buff=0.4).shift(RIGHT * 2.6)
        f[0].set_color(COND)
        take = label(r"every slice of a Gaussian is a Gaussian, \ with the same width: \ only the centre moves", font_size=22,
                     color=COND)
        if take.width > 6.4:
            take.width = 6.4
        take.to_corner(UL, buff=0.4)
        with self.voiceover(
            "This is the build of the part: the Gaussian slicer. <bookmark mark='a'/> Fix the mid-parent height at "
            "a hundred and seventy-eight centimetres and cut the surface there. <bookmark mark='b'/> The cut is a "
            "curve, f of x and y with x held fixed, but it isn't a density: its area is the marginal density of x, "
            "not one. <bookmark mark='c'/> Divide by that area, and the slice is rescaled into the conditional "
            "density of the son's height, given the parents. <bookmark mark='d'/> Do it at a hundred and seventy, "
            "and at a hundred and sixty-two. Three slices, three conditional distributions, and the computed means "
            "and standard deviations can be compared with the nearby families in the World; the Gaussian is an approximation. "
            "<bookmark mark='e'/> Notice two things: every slice of a Gaussian is a Gaussian, and they all have the "
            "same width. Only the centre moves as x changes, and it moves along a straight line. That straight "
            "line is the birth of regression, and chapter six proves it."
        ) as vo:
            self.add(gs.ns, *objs)
            self.play(NSpace.reveal(*objs, run_time=1.5))
            vo.wait_until("a")
            self.add(slices[2])
            self.play(NSpace.reveal(slices[2]))
            vo.wait_until("c")
            self.add(renorm[2])
            self.play(NSpace.reveal(renorm[2]), FadeIn(f))
            self.play(FadeIn(rows[2]), FadeIn(emp[2]))
            vo.wait_until("d")
            for k in (1, 0):
                self.add(slices[k], renorm[k])
                self.play(NSpace.reveal(slices[k], renorm[k]), FadeIn(rows[k]), FadeIn(emp[k]))
            vo.wait_until("e")
            self.play(FadeIn(take), gs.ns.turn(0.6, run_time=4.0))
        gs.stop(*slices, *renorm)
        self.clear_scene()

    def bayes(self):
        rows = [
            cmath(r"f(x, y)", r"=", r"f_X(x)\, f(y \mid x)", r"=", r"f_Y(y)\, f(x \mid y)", font_size=36),
            cmath(r"f(x \mid y)", r"=", r"\frac{f(y \mid x)\, f_X(x)}{\int f(y \mid x')\, f_X(x')\, dx'}", font_size=36),
        ]
        rows[1][0].set_color(COND)
        whys = [why(r"slice either way"), why(r"Part 2's Bayes, \ for densities: \ Part 15")]
        indep = label(r"independent \ $\iff$ \ $f(x, y) = f_X(x) f_Y(y)$ \ $\iff$ \ every slice has the same shape", font_size=26,
                      color=S.ACCENT).to_edge(DOWN, buff=0.7)
        intro = label('Slice either way: Bayes for densities', font_size=36)
        with self.voiceover(
            "Two facts follow at once. <bookmark mark='a'/> The joint density can be sliced either way: as the "
            "marginal of x times the conditional of y given x, or the other way round. <bookmark mark='b'/> Equate "
            "them and you have Bayes' theorem for densities, the engine of Part 15. <bookmark mark='c'/> And two "
            "variables are independent exactly when the joint density factors into its marginals, which means every "
            "renormalized slice is the same: knowing x tells you nothing about y."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=2.0, x=-0.6, buff=0.8, edge=6.9)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(indep))
        self.clear_scene()

    def dice(self):
        d = load("extras2")["dice"]
        J = np.asarray(d["J36"])
        cell = 0.62
        o = np.array([-5.4, -2.2, 0])
        grid, cells = VGroup(), {}
        for i in range(6):
            for j in range(6):
                v = int(J[i, j])
                sq = Square(side_length=cell, stroke_color=GREY_D, stroke_width=1, fill_color=COND if v else "#121722",
                            fill_opacity=0.18 * v if v else 1)
                sq.move_to(o + np.array([j * cell, i * cell, 0]))
                t = MathTex(str(v), font_size=22, color=WHITE if v else GREY_D).move_to(sq)
                cells[(i, j)] = VGroup(sq, t)
                grid.add(cells[(i, j)])
        rl = VGroup(*[MathTex(str(i + 1), font_size=22, color=GREY_B).next_to(cells[(i, 0)], LEFT, buff=0.15) for i in range(6)])
        cl = VGroup(*[MathTex(str(j + 1), font_size=22, color=GREY_B).next_to(cells[(0, j)], DOWN, buff=0.15) for j in range(6)])
        an = VGroup(label(r"max", font_size=22, color=GREY_A).next_to(rl, LEFT, buff=0.15),
                    label(r"min", font_size=22, color=GREY_A).next_to(cl, DOWN, buff=0.12))
        unit = MathTex(r"\times \tfrac{1}{36}", font_size=26, color=GREY_B).next_to(rl, UP, buff=0.35)
        mr = VGroup(*[MathTex(str(v), font_size=22, color=MARG).next_to(cells[(i, 5)], RIGHT, buff=0.2) for i, v in enumerate(d["marg_max"])])
        mc = VGroup(*[MathTex(str(v), font_size=22, color=MARG).next_to(cells[(5, j)], UP, buff=0.2) for j, v in enumerate(d["marg_min"])])
        rows = [
            cmath(r"P(\max = k)", r"=", r"\tfrac{2k - 1}{36}", font_size=30),
            cmath(r"E\max = \tfrac{161}{36},\ \ E\min", r"=", r"\tfrac{91}{36}", font_size=30),
            cmath(r"\mathrm{Cov}(\max, \min)", r"=", r"\big(\tfrac{35}{36}\big)^2", font_size=30),
            cmath(r"\operatorname{corr}(\max, \min)", r"=", r"\tfrac{35}{73} \approx 0.48", font_size=32),
        ]
        rows[0][2].set_color(MARG)
        rows[3][2].set_color(S.ACCENT)
        whys = [why(r"the row sums: \ $k$ with $k$, \ plus $2(k - 1)$ pairs"), why(r"and $\max + \min = $ the total, $7$ on average"),
                why(r"exactly, \ with Part 2's engine"), why(r"the zeros above the diagonal are dependence you can see")]
        with self.voiceover(
            "Here's a joint distribution we can compute exactly. Roll two dice, and record the larger and the "
            "smaller. <bookmark mark='a'/> The table counts the thirty-six equally likely rolls. The diagonal has one "
            "way each, a double; below it, two ways each, since either die can be the larger; above it, nothing, "
            "since the minimum can't exceed the maximum. <bookmark mark='b'/> The row sums give the marginal of the "
            "maximum: two k minus one out of thirty-six, climbing toward six. The column sums give the minimum's, the "
            "mirror image. <bookmark mark='c'/> The means add to seven, as they must, since the maximum plus the "
            "minimum is the total. <bookmark mark='d'/> The covariance comes out to exactly thirty-five over "
            "thirty-six, squared, <bookmark mark='e'/> and the correlation to thirty-five over seventy-three, almost a "
            "half. The empty triangle is dependence you can see: knowing the maximum is two rules out most of the "
            "table."
        ) as vo:
            self.play(FadeIn(rl), FadeIn(cl), FadeIn(an), FadeIn(unit))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.02), run_time=2.0)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=2.4, buff=0.62, edge=6.9)
            vo.wait_until("b")
            self.play(FadeIn(mr), FadeIn(mc))
            step(0, transform=False)
            vo.wait_until("c")
            step(1, transform=False)
            vo.wait_until("d")
            step(2, transform=False)
            vo.wait_until("e")
            step(3, transform=False)
        self.clear_scene()

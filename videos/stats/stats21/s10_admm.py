from __future__ import annotations

import numpy as np

from videos.stats.stats21.common import *  # noqa: F403


class ADMM(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.fused()
        self.signal()
        self.residuals()
        self.consensus()
        self.verdict()

    def card(self):
        card = chapter_card(9, r"ADMM", r"Split a hard problem into easy ones", part=PART)
        with self.voiceover("Chapter nine. The alternating direction method of multipliers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\min", r"", r"f(x) + g(z) \ \ \text{s.t.} \ \ Ax + Bz = c", font_size=30),
            cmath(r"x_{k+1}", r"=", r"\arg\min_x f(x) + \tfrac\rho2\|Ax + Bz_k - c + u_k\|^2", font_size=30),
            cmath(r"z_{k+1}", r"=", r"\arg\min_z g(z) + \tfrac\rho2\|Ax_{k+1} + Bz - c + u_k\|^2", font_size=30),
            cmath(r"u_{k+1}", r"=", r"u_k + Ax_{k+1} + Bz_{k+1} - c", font_size=30),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"two easy pieces, \ tied by a constraint"), why(r"handle $f$ alone"), why(r"handle $g$ alone"),
                why(r"the running dual: \ the price of disagreement")]
        intro = label('Split the variables and update the disagreement price', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Some problems are hard only because two easy pieces are tangled together. ADMM untangles "
            "them: give each piece its own variable, x and z, and tie them with a linear constraint. <bookmark mark='b'/> Then "
            "alternate. Minimize over x, handling f alone, with a quadratic penalty pulling it toward agreement with z. "
            "<bookmark mark='c'/> Minimize over z, handling g alone. <bookmark mark='d'/> And update u, a scaled Lagrange "
            "multiplier that accumulates whatever disagreement remains, the price that drives the two toward agreement. The "
            "idea dates from the 1970s; Stephen Boyd and colleagues' 2011 survey made it a standard tool."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fused(self):
        rows = [
            cmath(r"\min_b", r"", r"\tfrac12\|y - b\|^2 + \lambda \textstyle\sum_i |b_i - b_{i-1}|", font_size=30),
            cmath(r"\text{split}", r":", r"z = Db, \ \ D \text{ the differences}", font_size=30),
            cmath(r"b\text{-step}", r":", r"(I + \rho D'D)\,b = y + \rho D'(z - u)", font_size=30),
            cmath(r"z\text{-step}", r":", r"z = S_{\lambda/\rho}(Db + u)", font_size=30),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"the fused lasso (Tibshirani et al. 2005)"), why(r"the penalty is separable in $z$"),
                why(r"a tridiagonal solve: \ $O(n)$"), why(r"soft thresholding, \ again")]
        intro = label('Differences make the fused penalty separable', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Chapter seven's stuck example was a fused lasso: fit a sequence b to data y, penalizing the "
            "absolute jumps between neighbours, so the fit is piecewise constant. Coordinate descent fails because the penalty "
            "couples neighbours. <bookmark mark='b'/> ADMM splits it: let z be the vector of differences. In terms of z the "
            "penalty is separable. <bookmark mark='c'/> The b-step is a linear system whose matrix is tridiagonal, solvable in "
            "linear time. <bookmark mark='d'/> The z-step is soft thresholding. Two easy steps, repeated."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def signal(self):
        d = load("admm")
        y = np.asarray(d["y"])
        t = np.arange(len(y))
        A = axes([0, len(y)], [-2.5, 3.5], x_length=9.6, y_length=4.4, xlabel=r"position", ylabel=r"signal",
                 xticks=[0, 30, 60, 90, 120], yticks=[-2, 0, 2], center=[-0.8, 0.5, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=GREY_B) for a, b in zip(t, y)])
        truth = polyline(ax, t, d["truth"], TRUE, 2.5)
        truth.set_stroke(opacity=0.8)
        cols = {"0.5": GRAD, "3.0": PATH, "20.0": NEWT}
        fits = VGroup(*[polyline(ax, t, d["fits"][k]["b"], c, 3.5) for k, c in cols.items()])
        key = fit_rows(VGroup(
            label(r"grey: \ 120 noisy points; \ gold thin: \ the truth, \ four levels", font_size=22),
            label(r"red: \ $\lambda = 0.5$: \ too many jumps", font_size=22, color=GRAD),
            label(r"gold: \ $\lambda = 3$: \ the broad levels, \ with shrinkage and residual small jumps", font_size=22, color=PATH),
            label(r"blue: \ $\lambda = 20$: \ nearly flat", font_size=22, color=NEWT),
        ), 12.0, 0.2, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's a signal with four levels and noise, a hundred and twenty points, simulated."
            " <bookmark mark='b'/> With a small lambda the fused lasso follows the noise, with many small jumps. "
            "<bookmark mark='c'/> With lambda three it recovers the broad level pattern, with shrinkage and some "
            "remaining small jumps, the lasso's usual bias. <bookmark mark='d'/> With lambda twenty almost every jump"
            " costs too much, and the fit is nearly flat. Choosing lambda is Part 19's job, by cross-validation."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ a piecewise-constant signal", corner=UR))
            self.play(FadeIn(A), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.01), Create(truth), FadeIn(key[0]), run_time=2.0)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                if k:
                    self.play(fits[k - 1].animate.set_stroke(opacity=0.25), Create(fits[k]), FadeIn(key[k + 1]), run_time=1.5)
                else:
                    self.play(Create(fits[k]), FadeIn(key[k + 1]), run_time=1.5)
        self.clear_scene()

    def residuals(self):
        d = load("admm")
        res = np.maximum(np.asarray(d["fits"]["3.0"]["res"]), 1e-12)
        ks = np.arange(1, len(res) + 1)
        A = axes([0, len(res)], [-4, 1], x_length=8.0, y_length=4.2, xlabel=r"ADMM iteration", ylabel=r"$\|Db - z\|$ (log$_{10}$)",
                 xticks=[0, 100, 200, 300, 400], yticks=[-4, -3, -2, -1, 0, 1], center=[-1.6, 0.3, 0])
        ax = A.ax
        ln = polyline(ax, ks, np.log10(res), PATH, 3.5)
        dual = polyline(ax, ks, np.log10(np.maximum(d["fits"]["3.0"]["dual_res"], 1e-15)), NEWT, 2.5)
        rows = fit_rows(VGroup(
            label(r"the primal residual: \ how much $z$ and $Db$ disagree", font_size=22),
            label(r"fast at first, \ then a steady linear decline", font_size=22, color=PATH),
            label(r"a few digits come quickly; \ many digits slowly", font_size=22, color=GREY_A),
            label(r"blue: \ dual residual; \ check both against scaled tolerances", font_size=22, color=NEWT),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How quickly does it settle? Track the primal residual, the disagreement between z "
            "and the differences of b. <bookmark mark='b'/> It falls fast at first, then declines steadily. <bookmark"
            " mark='c'/> That's ADMM's character: a few digits of accuracy come quickly, many digits slowly. "
            "<bookmark mark='d'/> The blue curve is the dual residual, rho times the norm of D transposed applied to "
            "the change in z. A small primal residual alone does not certify optimality. Check both residuals against"
            " appropriately scaled tolerances, and relate numerical accuracy to the statistical task."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(ln), Create(dual), FadeIn(rows[0]), run_time=2.0)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def consensus(self):
        rows = [
            cmath(r"\min", r"", r"\textstyle\sum_{m=1}^M f_m(x_m) + g(z) \ \ \text{s.t.} \ \ x_m = z", font_size=30),
            cmath(r"x_m", r"\leftarrow", r"\arg\min f_m(x) + \tfrac\rho2 \|x - z + u_m\|^2", font_size=30),
            cmath(r"z", r"\leftarrow", r"\operatorname{prox}_{g/(M\rho)}\big(\overline{x + u}\big)", font_size=30),
            cmath(r"u_m", r"\leftarrow", r"u_m + x_m - z", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"$f_m$: \ the loss on machine $m$'s share of the data"), why(r"in parallel, \ each machine alone"),
                why(r"average, \ then apply the penalty"), why(r"each machine's disagreement")]
        intro = label('Local fits share coefficients through a consensus constraint', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Here's the form that made ADMM famous for large data. Spread the data across M "
            "machines, give each its own copy of the coefficients, x m, and require every copy to equal a shared z. "
            "<bookmark mark='b'/> Each machine updates its own copy, using only its own data, all at the same time. "
            "<bookmark mark='c'/> The coordinator averages the copies and applies the penalty's proximal operator. "
            "<bookmark mark='d'/> And each machine updates its disagreement. Only coefficient and multiplier vectors "
            "are exchanged in this scheme. Those messages can still leak information; distributed computation alone "
            "is not a privacy guarantee."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def verdict(self):
        rows = fit_rows(VGroup(
            label(r"ADMM: \ split into pieces, \ each with an easy step", font_size=24, color=PATH),
            label(r"distributed: \ each machine fits its share; \ a consensus step averages", font_size=24, color=NEWT),
            label(r"generalized lasso, \ graphical lasso, \ robust PCA, \ trend filtering", font_size=24, color=TEAL),
            label(r"two-block convex guarantees need regularity; \ speed depends on $\rho$", font_size=22, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> ADMM's strength is that it turns one hard problem into a sequence of easy ones. "
            "<bookmark mark='b'/> The pieces can even live on different computers: each fits its own share of the "
            "data, and a consensus step averages them. <bookmark mark='c'/> It handles the generalized lasso, the "
            "graphical lasso for networks of variables, robust principal components and trend filtering. <bookmark "
            "mark='d'/> For the standard two-block convex formulation, closed proper objectives, an attained saddle "
            "point and adequately solved subproblems give convergence guarantees for fixed positive rho. Arbitrary "
            "nonconvex or multi-block extensions need separate analysis."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

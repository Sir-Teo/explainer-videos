from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)

AA = np.array([[1, 0.75], [1, -0.75], [-1, 0]])


def f(x, y):
    return math.log(sum(math.exp(a[0] * x + a[1] * y - 0.1) for a in AA))


class Convex(VoiceoverScene):
    def construct(self):
        self.card()
        self.descent()
        self.page()

    def card(self):
        card = chapter_card(13, r"Convex optimization in a page", r"Why is convexity the dividing line?",
                            lit=(1939, 1951), extra=((1939, r"Karush"), (1951, r"Kuhn--Tucker")), part=PART)
        with self.voiceover("Chapter thirteen. Convex optimization in a page."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def descent(self):
        c = load("convex")
        head = label(r"Gradient descent against Newton's method", font_size=32).to_edge(UP, buff=0.3)
        sc = 0.95
        O0 = np.array([-2.6, -0.3, 0])

        def T(p):
            return O0 + np.array([p[0] * sc, p[1] * sc, 0])
        levels = [f(*c["xstar"]) + d for d in (0.05, 0.2, 0.5, 1.0, 1.6, 2.4, 3.3)]
        cont = VGroup()
        for lv in levels:
            pts = []
            for th in np.linspace(0, TAU, 160):
                d = np.array([math.cos(th), math.sin(th)])
                lo, hi = 0.0, 8.0
                for _ in range(40):
                    mid = (lo + hi) / 2
                    q = np.array(c["xstar"]) + mid * d
                    if f(*q) < lv:
                        lo = mid
                    else:
                        hi = mid
                pts.append(T(np.array(c["xstar"]) + lo * d))
            cont.add(VMobject(color=GREY_D, stroke_width=1.3).set_points_as_corners(pts + [pts[0]]))
        gd = VMobject(color=NO, stroke_width=2.5).set_points_as_corners([T(p) for p in c["gd"][:45]])
        nt = VMobject(color=YES, stroke_width=3.5).set_points_as_corners([T(p) for p in c["newton"][:6]])
        gdd = VGroup(*[Dot(T(p), radius=0.035, color=NO) for p in c["gd"][:45]])
        ntd = VGroup(*[Dot(T(p), radius=0.06, color=YES) for p in c["newton"][:6]])
        star = Star(n=5, outer_radius=0.13, inner_radius=0.06, color=HEAD, fill_opacity=1).move_to(T(c["xstar"]))
        k_gd = next(i for i, e in enumerate(c["gd_err"]) if e < 1e-10)
        k_nt = next(i for i, e in enumerate(c["newton_err"]) if e < 1e-10)
        side = VGroup(
            label(r"a smooth convex function \\ (log-sum-exp, \ Boyd and Vandenberghe's example, stretched)", font_size=20,
                  color=GREY_A),
            label(r"\textbf{gradient descent}: \ step downhill, \\ with a backtracking line search", font_size=21,
                  color=NO),
            label(rf"zigzags across the narrow valley: \\ {k_gd} steps to within $10^{{-10}}$", font_size=21, color=NO),
            label(r"\textbf{Newton}: \ minimize the local quadratic model, \\ $x \leftarrow x - \nabla^2 f(x)^{-1} \nabla "
                  r"f(x)$", font_size=21, color=YES),
            label(rf"{k_nt} steps: \ quadratic convergence, \\ the digits double each step", font_size=21, color=YES),
            label(r"each Newton step costs a linear solve; \\ in high dimension, \ gradients win \ (\textit{AI, Built} 11)",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Linear programs are the simplest convex problems, and the interior-point method of chapter five already "
            "used the general tool. <bookmark mark='a'/> Here is a smooth convex function of two variables, a "
            "log-sum-exp from Boyd and Vandenberghe's textbook, stretched so its valley is narrow. <bookmark "
            "mark='b'/> Gradient descent steps downhill, choosing each step's length by backtracking. <bookmark "
            "mark='c'/> In a narrow valley the downhill direction points mostly across the valley, not along it, so "
            "the path zigzags: forty steps to reach ten digits. <bookmark mark='d'/> Newton's method fits a quadratic "
            "to the function at the current point, using second derivatives, and jumps to that quadratic's minimum. "
            "<bookmark mark='e'/> Four steps. Near the optimum the number of correct digits doubles with every step. "
            "<bookmark mark='f'/> But each Newton step solves a linear system in the Hessian, which is hopeless with a "
            "billion variables, and that is why the gradient methods of the AI series train neural networks."
        ) as vo:
            hbg = BackgroundRectangle(head, color=config.background_color, fill_opacity=1, buff=0.12)
            self.add(hbg)
            self.play(FadeIn(head), FadeIn(cont), FadeIn(star))
            self.bring_to_front(hbg, head)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(gd), FadeIn(gdd), FadeIn(side[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(nt), FadeIn(ntd), FadeIn(side[4]), run_time=2.0)
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()

    def page(self):
        head = label(r"The page", font_size=36).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"\textbf{convex}: \ every local minimum is global, \ and a certificate exists \ (duality again)",
                  font_size=22, color=YES),
            MathTex(r"\text{KKT:}\quad \nabla f(x) + \sum_i \lambda_i \nabla g_i(x) = 0,\quad \lambda_i \ge 0,\quad "
                    r"\lambda_i\, g_i(x) = 0", font_size=30, color=LAM),
            label(r"Karush (1939), \ Kuhn and Tucker (1951): \ the multipliers are chapter 3's prices, \ generalized",
                  font_size=21, color=GREY_A),
            label(r"the ladder: \ LP $\subset$ convex QP $\subset$ second-order cone $\subset$ SDP \ (chapter 10) "
                  r"$\subset$ convex", font_size=22, color=HEAD),
            label(r"all solvable to $\varepsilon$ in polynomial time, \ by interior points \ (Nesterov and Nemirovski, "
                  r"1994)", font_size=22, color=WHITE),
            label(r"\textbf{non-convex}: \ local minima everywhere; \ NP-hard in general, \ yet neural networks train",
                  font_size=22, color=NO),
            label(r"``the great watershed in optimization isn't between linearity and nonlinearity, \ but convexity and "
                  r"nonconvexity'' \ (Rockafellar, 1993)", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "Convex optimization fits on a page. <bookmark mark='a'/> Minimize a convex function over a convex set, "
            "and every local minimum is a global one, with a dual certificate to prove it. <bookmark mark='b'/> At the "
            "optimum the Karush–Kuhn–Tucker conditions hold: the gradient of the objective is balanced by a "
            "non-negative combination of the gradients of the tight constraints. <bookmark mark='c'/> Those "
            "multipliers are the shadow prices of chapter three, generalized. <bookmark mark='d'/> There is a ladder "
            "of problem classes: linear programs, convex quadratic programs, second-order cone programs, and "
            "semidefinite programs like chapter ten's. <bookmark mark='e'/> Yurii Nesterov and Arkadi Nemirovski "
            "showed that interior-point methods solve all of them to any accuracy in polynomial time. <bookmark "
            "mark='f'/> Without convexity, local minima are everywhere and the general problem is NP-hard, though "
            "neural networks are trained anyway, which is one of the AI series' puzzles. <bookmark mark='g'/> As "
            "Tyrrell Rockafellar put it, the great watershed in optimization is not between linear and non-linear, "
            "but between convex and non-convex."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

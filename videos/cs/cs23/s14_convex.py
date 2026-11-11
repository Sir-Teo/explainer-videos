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
            label('fixed 2D log-sum-exp; \\\\ analytic optimum $(-\\log2/2,0)$; \\ moderate local conditioning', font_size=20,
                  color=GREY_A),
            label(r"\textbf{gradient descent}: \ step downhill, \\ with a backtracking line search", font_size=21,
                  color=NO),
            label(rf"this instance: \ {k_gd} steps to objective gap $<10^{{-10}}$; \ analytic reference", font_size=21, color=NO),
            label(r"\textbf{Newton}: \ minimize the local quadratic model, \\ $x \leftarrow x - \nabla^2 f(x)^{-1} \nabla "
                  r"f(x)$", font_size=21, color=YES),
            label(rf"this instance: \ {k_nt} steps; \ quadratic local convergence needs regularity", font_size=21, color=YES),
            label(r"each Newton step costs a linear solve; \\ in high dimension, \ gradients win \ (\textit{AI, Built} 11)",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            (
            "This small convex example lets us compare actual optimization paths. <bookmark mark='a'/> The "
            'function is a two-dimensional log-sum-exp with the displayed coefficients. Its independent analytic '
            'optimum is minus half log two, zero. This instance is only moderately conditioned near that point. '
            "<bookmark mark='b'/> Gradient descent chooses step lengths by backtracking. <bookmark mark='c'/> "
            'Here it needs forty steps to make objective error less than ten to the minus ten, measured against '
            "the analytic value rather than Newton's last iterate. <bookmark mark='d'/> Newton solves the local "
            "Hessian system to obtain a step. <bookmark mark='e'/> Here it needs four steps. Quadratic local "
            'convergence requires regularity and a sufficiently close starting region; four observations do not '
            "prove a general digits-doubling law. <bookmark mark='f'/> A Newton step costs a linear solve. "
            'Structure, sparsity and dimension decide whether that cost is worthwhile; there is no universal '
            'winner.'
        )
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
            label('convex objective and domain: \\ local minima are global; \\\\ dual attainment needs suitable regularity',
                  font_size=22, color=YES),
            MathTex('\\begin{gathered}g_i(x)\\le0,\\quad\\lambda_i\\ge0,\\quad\\lambda_i g_i(x)=0,\\\\\\nabla f(x)+\\sum_i\\lambda_i\\nabla g_i(x)=0\\end{gathered}', font_size=30, color=LAM),
            label('differentiable convex inequalities; \\ Slater is a sufficient constraint qualification',
                  font_size=21, color=GREY_A),
            label(r"the ladder: \ LP $\subset$ convex QP $\subset$ second-order cone $\subset$ SDP \ (chapter 10) "
                  r"$\subset$ convex", font_size=22, color=HEAD),
            label('complexity depends on representation, \\ barrier/oracle, \\ accuracy and conditioning', font_size=22, color=WHITE),
            label('general nonconvex optimization can be NP-hard; \\ individual instances need separate analysis',
                  font_size=22, color=NO),
            label(r"``the great watershed in optimization isn't between linearity and nonlinearity, \ but convexity and "
                  r"nonconvexity'' \ (Rockafellar, 1993)", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            (
            "Convexity gives powerful guarantees with explicit premises. <bookmark mark='a'/> Every local "
            'minimum of a convex objective on a convex domain is global, but existence of a dual certificate '
            "needs appropriate duality conditions. <bookmark mark='b'/> For differentiable convex inequalities, "
            'KKT includes primal feasibility, nonnegative multipliers, stationarity and complementary slackness. '
            "Slater's condition is one sufficient regularity condition for necessity and strong duality. "
            "<bookmark mark='c'/> The multipliers generalize LP shadow prices. <bookmark mark='d'/> LP, convex "
            'quadratic, second-order cone and semidefinite formulations offer increasingly expressive structured '
            "models. <bookmark mark='e'/> Polynomial complexity claims must specify input representation, an "
            'available barrier or oracle, accuracy and conditioning. Arbitrary convex functions do not '
            "automatically admit a uniform polynomial algorithm. <bookmark mark='f'/> General nonconvex "
            "optimization can be NP-hard; individual nonconvex problems can still be easy. <bookmark mark='g'/> "
            "Rockafellar's convex versus nonconvex watershed is a useful organizing principle, with these "
            'assumptions kept visible.'
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

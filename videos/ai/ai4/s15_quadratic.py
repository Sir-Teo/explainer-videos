from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, HESS, HIST, PART, VALUE, expo, load, log_axes, mant


def saddle_f(x, y):
    return 0.5 * x * x - 0.5 * y * y + 0.25 * y ** 4


class Quadratic(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.valley()
        self.rates()
        self.saddle()

    def card(self):
        card = chapter_card(14, r"Descent on a quadratic; \ saddles", r"How fast can going downhill be?", part=PART)
        with self.voiceover("Chapter fourteen. How fast is downhill?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        col = {r"\eta": C.LR, r"\lambda_i": HESS}
        rows = [
            cmath(r"x_{t+1}", r"=", r"x_t - \eta H x_t = (I - \eta H)\, x_t", font_size=36),
            cmath(r"c_{i,\,t+1}", r"=", r"(1 - \eta \lambda_i)\, c_{i,\,t}", font_size=36),
            cmath(r"\text{converges}", r"\iff", r"\eta < 2 / \lambda_{\max}", font_size=36),
            cmath(r"\text{rate}", r"=", r"\max_i |1 - \eta\lambda_i| \;\ge\; \frac{\kappa - 1}{\kappa + 1}", font_size=36),
        ]
        whys = [why(r"$f = \frac12 x^\top H x$, \ so $\nabla f = H x$", font_size=22),
                why(r"in $H$'s eigenvectors \ (Part 3), \\ each coordinate $c_i$ on its own", font_size=22),
                why(r"$|1 - \eta\lambda_i| < 1$ for every $i$", font_size=22),
                why(r"best at $\eta = 2/(\lambda_{\min} + \lambda_{\max})$; \\ $\kappa = \lambda_{\max}/\lambda_{\min}$", font_size=22)]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-2.4, buff=0.6, edge=6.9)
        head = label(r"gradient descent on a quadratic, \ exactly", font_size=28, color=GREY_A).to_edge(UP, buff=0.3)
        dc = definition_card(r"condition number $\kappa$", r"the ratio of the largest curvature to the smallest, "
                             r"$\lambda_{\max} / \lambda_{\min}$", width=7.0, font_size=21).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Near a minimum every smooth loss looks like a quadratic bowl, and on a bowl gradient descent can be "
            "solved exactly. <bookmark mark='a'/> Each step multiplies the position by I minus eta H. "
            "<bookmark mark='b'/> In the Hessian's eigenvectors that matrix is diagonal, so each coordinate shrinks "
            "on its own, by one minus eta times its eigenvalue. <bookmark mark='c'/> Every factor must be less than one "
            "in size, so the step must be smaller than two over the largest curvature. <bookmark mark='d'/> And the "
            "slowest coordinate sets the pace. The best step balances the two extremes, and the rate is kappa minus "
            "one over kappa plus one, where kappa, the condition number, is the largest curvature over the smallest."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(dc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def valley(self):
        v = load("valley")
        H = np.asarray(v["H"])
        assert np.allclose(np.diag(H), [1.0, 25.0])
        ax = Axes(x_range=[-5, 5, 1], y_range=[-1.2, 1.2, 0.5], x_length=11.0, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to(DOWN * 0.6)

        def f(x, y):
            return 0.5 * (H[0, 0] * x * x + H[1, 1] * y * y)

        cont = contour_lines(ax, f, (-5, 5), (-1.2, 1.2), [0.25 * 2 ** k for k in range(8)], n=(200, 80))
        paths = {}
        for name, col in (("gd", WHITE), ("momentum", C.TRUE_P), ("newton", C.BITS)):
            pts = [ax.c2p(*q) for q in np.asarray(v[name])]
            paths[name] = VMobject(color=col, stroke_width=4).set_points_as_corners(pts)
        dots = {k: Dot(paths[k].get_start(), radius=0.08, color=paths[k].get_color()) for k in paths}
        lab = {"gd": label(rf"gradient descent: \ ${v['gd_steps_to_1pct']}$ steps to get within $1\%$", font_size=24),
               "momentum": label(r"with momentum \ (Part 11)", font_size=24, color=C.TRUE_P),
               "newton": label(r"Newton: \ $-H^{-1}\nabla f$, \ one step", font_size=24, color=C.BITS)}
        VGroup(*lab.values()).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.4)
        curv = label(r"curvatures $1$ and $25$: \ $\kappa = 25$, \ a long, narrow valley", font_size=26,
                     color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is a valley with kappa of twenty-five: it bends twenty-five times more sharply across than along. "
            "<bookmark mark='a'/> The steepest way down points mostly at the opposite wall, so the steps zigzag from "
            f"wall to wall and crawl along the floor: {v['gd_steps_to_1pct']} steps to get within one percent. "
            "<bookmark mark='b'/> Momentum, carrying speed from step to step, does better, and Part 11 derives why. "
            "<bookmark mark='c'/> Newton's step undoes the curvature and lands at the bottom at once."
        ) as vo:
            self.play(Create(ax), LaggedStart(*[Create(c) for c in cont], lag_ratio=0.1), FadeIn(curv), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(dots["gd"]), FadeIn(lab["gd"]))
            self.play(Create(paths["gd"]), MoveAlongPath(dots["gd"], paths["gd"]), run_time=3.5, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(dots["momentum"]), FadeIn(lab["momentum"]))
            self.play(Create(paths["momentum"]), MoveAlongPath(dots["momentum"], paths["momentum"]), run_time=3.0,
                      rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(dots["newton"]), FadeIn(lab["newton"]))
            self.play(Create(paths["newton"]), MoveAlongPath(dots["newton"], paths["newton"]), run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rates(self):
        q = load("quad")
        ks = np.asarray(q["kappas"], float)
        ro, rp = np.asarray(q["rate_opt"]), np.asarray(q["rate_opt_pred"])
        so = np.asarray(q["steps_opt"], float)
        kk = np.logspace(0, 3, 100)
        g1 = axes([0, 3, 1], [0, 1.0, 0.25], x_length=5.0, y_length=3.4, xlabel=r"condition number $\kappa$",
                  ylabel=r"rate: \ shrink factor per step", xticks=[0, 1, 2, 3],
                  xfmt=lambda v: {0: "1", 1: "10", 2: "100", 3: "1000"}[int(v)], yticks=[0, 0.5, 1], center=[-3.5, 0.3, 0])
        pred = curve(g1.ax, np.log10(kk), (kk - 1) / (kk + 1), GREY_B, 2.5)
        meas = VGroup(*[Dot(g1.ax.c2p(math.log10(k), r), radius=0.07, color=GRAD) for k, r in zip(ks, ro)])
        leg1 = VGroup(label(r"$(\kappa - 1)/(\kappa + 1)$", font_size=20, color=GREY_B),
                      label(r"measured", font_size=20, color=GRAD)).arrange(RIGHT, buff=0.4).next_to(g1, DOWN, buff=0.15)
        ok = so > 1
        g2 = log_axes((0, 3), (0, 4), x_length=5.0, y_length=3.4, xlabel=r"condition number $\kappa$",
                      ylabel=r"steps to shrink by $10^6$", center=[3.6, 0.3, 0])
        c2 = VGroup(*[Dot(g2.ax.c2p(math.log10(k), math.log10(s)), radius=0.07, color=GRAD) for k, s in zip(ks[ok], so[ok])])
        lin = curve(g2.ax, np.log10(kk[kk > 1.5]), np.log10(kk[kk > 1.5] / 2 * math.log(1e6)), GREY_B, 2)
        worst = float(np.abs(ro - rp).max())
        etas, fin = np.asarray(q["etas"]), np.asarray(q["final"])
        start = float(np.linalg.norm([-4.5, 0.9]))  # the valley's starting point
        edge = float(etas[np.argmax(fin > start)]) if (fin > start).any() else float("nan")
        stab = label(rf"the valley above: \ the steps grow, not shrink, from $\eta = {edge:.3f}$; \ $2/\lambda_{{\max}} = 0.08$",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(rf"measured on $\tfrac12(x^2 + \kappa y^2)$, \ best fixed step", font_size=26, color=GREY_A)
        head.to_edge(UP, buff=0.35)
        k_big = int(ks[-1])
        verdict = ("match the formula to rounding error" if worst < 1e-6 else "match the formula closely")
        with self.voiceover(
            "Measured on bowls from kappa of one to a thousand: the rates, in orange, "
            f"{verdict}. <bookmark mark='a'/> And the number of steps grows in proportion to kappa: shrinking the "
            f"error a millionfold takes {int(so[-1]):,} steps at kappa of {k_big:,}. <bookmark mark='b'/> Push "
            f"the step past two over the largest curvature, and the valley's steps grow instead of shrinking, here from eta of {edge:.3f}. "
            "Real losses are not quadratics, but this is the calculus behind every learning-rate rule, and Part 11 "
            "builds the faster methods on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), Create(pred), FadeIn(leg1))
            self.play(LaggedStart(*[FadeIn(m) for m in meas], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(lin), LaggedStart(*[FadeIn(m) for m in c2], lag_ratio=0.15), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(stab))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def saddle(self):
        q = load("quad")
        ax = Axes(x_range=[-1.8, 1.8, 0.5], y_range=[-1.5, 1.5, 0.5], x_length=6.0, y_length=5.0, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-3.6, -0.5, 0])
        cont = contour_lines(ax, saddle_f, (-1.8, 1.8), (-1.5, 1.5), np.linspace(-0.24, 1.4, 14), n=(120, 100))
        cols = {"1e-02": C.TRUE_P, "1e-06": GRAD, "1e-10": C.BITS}
        paths = VGroup()
        for k, col in cols.items():
            pts = np.asarray(q[f"path_{k}"])
            paths.add(VMobject(color=col, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in pts]))
        stuck = np.asarray(q["stuck"])
        sp = VMobject(color=WHITE, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in stuck])
        sd = Dot(ax.c2p(0, 0), radius=0.08, color=WHITE)
        leg = VGroup(*[label(rf"$y_0 = 10^{{{int(k.split('e')[1])}}}$", font_size=20, color=c) for k, c in cols.items()],
                     label(r"$y_0 = 0$: \ stuck", font_size=20, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        leg.next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        leg.arrange(RIGHT, buff=0.3).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        y0s = np.asarray(q["y0s"])
        esc, pr = np.asarray(q["esc"], float), np.asarray(q["esc_pred"])
        e = -np.log10(y0s)
        g2 = axes([0, 13, 2], [0, 320, 100], x_length=5.0, y_length=3.4, xlabel=r"$\log_{10}(1/y_0)$",
                  ylabel=r"steps to leave the saddle", xticks=[0, 4, 8, 12], yticks=[0, 100, 200, 300], center=[3.6, -0.2, 0])
        c_pr = curve(g2.ax, e, pr, GREY_B, 2.5)
        c_ms = VGroup(*[Dot(g2.ax.c2p(a, b), radius=0.06, color=GRAD) for a, b in zip(e, esc)])
        slope = float(np.polyfit(e, esc, 1)[0])
        eta = 0.1
        pslope = math.log(10) / math.log(1 + eta)
        f_txt = MathTex(r"f = \tfrac12 x^2 - \tfrac12 y^2 + \tfrac14 y^4", font_size=30).to_edge(UP, buff=0.3).shift(LEFT * 3.4)
        sg = q["stuck_grad"]
        res = label(rf"measured: \ ${slope:.1f}$ steps per factor of ten \ (predicted ${pslope:.1f}$)", font_size=22,
                    color=GRAD).next_to(g2, UP, buff=0.2)
        cite_ = cite(r"Y.~Dauphin et al.\ (2014); \ C.~Jin et al.\ (2017)", corner=DR)
        close = abs(slope - pslope) < 0.1 * pslope
        verdict = "just as predicted" if close else "close to the prediction"
        with self.voiceover(
            "Saddles are where descent stalls. Here's a surface with a saddle at the centre and a minimum above and "
            "below it. <bookmark mark='a'/> Start almost on the line through the saddle, a tiny distance y nought off "
            "it. The walk slides in towards the saddle, where the gradient nearly vanishes, and waits, until the "
            "tiny offset has grown enough to fall off. <bookmark mark='b'/> Near the saddle the offset grows by one "
            "plus eta each step, so the wait grows with the logarithm of one over y nought: measured, "
            f"{slope:.1f} steps for every factor of ten, {verdict}. <bookmark mark='c'/> Start exactly on the line "
            f"and it never leaves: the gradient falls to {mant(sg)} times ten to the minus {expo(sg)}, at a point that "
            "is not a minimum. Only the Hessian, with its negative eigenvalue, tells them apart. In practice the noise "
            "of stochastic gradients kicks a network off; Yann Dauphin and colleagues argued in 2014 that in many "
            "dimensions saddles, more than bad minima, are what slow training."
        ) as vo:
            self.play(Create(ax), LaggedStart(*[Create(c) for c in cont], lag_ratio=0.05), FadeIn(f_txt), FadeIn(sd),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(leg[:3]), LaggedStart(*[Create(p) for p in paths], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(c_pr), LaggedStart(*[FadeIn(m) for m in c_ms], lag_ratio=0.1), FadeIn(res),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(Create(sp), FadeIn(leg[3]), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

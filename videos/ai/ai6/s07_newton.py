from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import (BAD, HIST, HL, chapter, line_in_box, load, page_dots, page_plane, plot, pow10,
                                  sci_tex, side_ladder)

NEWTON, GD = C.REWARD, C.MODEL_Q


class Newton(VoiceoverScene):
    def construct(self):
        chapter(self, 6, r"Newton's method, and lines that run away", r"How do you reach the bottom of the bowl fast?",
                "Chapter six. Newton's method.")
        self.derive()
        self.race()
        self.digits()
        self.runaway()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"\mathbf{z}": NEWTON, "S": NEWTON}
        rows = [
            cmath(r"\boldsymbol\theta_{\text{new}}", "=", r"\boldsymbol\theta - (\nabla^2\ell)^{-1}\,\nabla\ell", font_size=36),
            cmath(r"\boldsymbol\theta_{\text{new}}", "=", r"\boldsymbol\theta + (X^{\top}SX)^{-1}X^{\top}(\mathbf{y} - \mathbf{p})",
                  font_size=36),
            cmath(r"\boldsymbol\theta_{\text{new}}", "=", r"(X^{\top}SX)^{-1}X^{\top}S\,\mathbf{z}", font_size=36,
                  colors={r"\mathbf{z}": NEWTON}),
            cmath(r"\mathbf{z}", "=", r"X\boldsymbol\theta + S^{-1}(\mathbf{y} - \mathbf{p})", font_size=36,
                  colors={r"\mathbf{z}": NEWTON}),
        ]
        whys = [why(r"jump to the bottom \\ of the local parabola"), why(r"Chapter 5's gradient \\ and curvature"),
                why(r"weighted least squares!"), why(r"a working response")]
        step = ladder(self, rows, whys, keep=4, top=2.2, x=-1.5, buff=0.42, edge=6.8)
        hist = history_card(1972, r"Nelder \& Wedderburn", r"generalized linear models, \ all fitted by iteratively "
                            r"reweighted least squares", color=HIST, width=5.6).to_edge(DOWN, buff=0.3)
        head = label(r"Newton's method = iteratively reweighted least squares", font_size=30).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Gradient descent takes small steps. Newton's method uses the curvature too: <bookmark mark='a'/> fit a "
            "parabola to the loss where you stand, and jump to its bottom. <bookmark mark='b'/> With chapter five's "
            "gradient and curvature, the step is X transpose S X, inverted, times X transpose y minus p. "
            "<bookmark mark='c'/> Rearrange, and each step is a weighted least-squares problem, <bookmark mark='d'/> "
            "fitted to a working response. Pages the model is unsure of weigh the most. <bookmark mark='e'/> Nelder "
            "and Wedderburn made this the engine of every generalized linear model, in 1972."
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
            vo.wait_until("e")
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        ir = load("irls")
        p = load("pages")
        X2, y, test = np.asarray(p["X2"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
        LN, LG = np.asarray(ir["lines_newton"]), np.asarray(ir["lines_gd"])
        panels = []
        tr = np.nonzero(~test)[0]
        for k_, (Ls, title, col) in enumerate(((LN, r"Newton", NEWTON), (LG, r"gradient descent", GD))):
            plane = page_plane(x_length=5.0, y_length=3.3, center=[-3.4 + 6.8 * k_, 0.75, 0])
            ax = plane[0]
            dots = page_dots(ax, X2, y, idx=tr, jitter=0.35, radius=0.03, opacity=0.7)
            t = label(title, font_size=28, color=col).next_to(plane, UP, buff=0.1)
            panels.append((plane, dots, t, Ls, col))
        step_t = ValueTracker(0)

        def lines():
            k = int(round(step_t.get_value()))
            g = VGroup()
            for plane, dots, t, Ls, col in panels:
                if k == 0:
                    continue
                g.add(line_in_box(plane[0], Ls[k, :2], float(Ls[k, 2]), color=col, stroke_width=4))
            return g

        def reads():
            k = int(round(step_t.get_value()))
            g = VGroup()
            for i, (plane, dots, t, Ls, col) in enumerate(panels):
                g.add(MathTex(rf"\text{{step }} {k}: \ {Ls[k, 3]:.3f}\ \text{{bits}}", font_size=28, color=col)
                      .next_to(plane, DOWN, buff=0.05))
            return g

        ln, rd = always_redraw(lines), always_redraw(reads)
        # the 70-rate race: the distance to the best loss, log scale
        gap_n = np.maximum(np.asarray(ir["newton_gap"]), 1e-16)
        gd = np.asarray(ir["gd"])
        gx = np.log10(np.maximum(gd[:, 0], 1))
        g70 = plot([0, 4.3, 1], [-16, 0, 4], x_length=7.4, y_length=4.4, xticks=[0, 1, 2, 3, 4], yticks=[0, -4, -8, -12, -16],
                   xfmt=lambda v: pow10(int(v)), yfmt=lambda v: pow10(int(v)), center=[-2.4, -0.5, 0],
                   xlabel=r"steps \ (log scale)")
        a70 = g70.ax
        cn = VMobject(color=NEWTON, stroke_width=4).set_points_as_corners(
            [a70.c2p(math.log10(max(i, 1)), math.log10(v)) for i, v in enumerate(gap_n) if i >= 1])
        cg = VMobject(color=GD, stroke_width=4).set_points_as_corners(
            [a70.c2p(x_, math.log10(max(v, 1e-16))) for x_, v in zip(gx, gd[:, 1]) if v > 1e-16 and x_ > 0])
        g70n = label(r"all $70$ rates: \ loss above the best, \ against steps", font_size=22, color=GREY_A)
        g70n.next_to(g70, UP, buff=0.08).align_to(g70, LEFT)
        nn, it6 = int(ir["n_newton"]), int(ir["gd_iters_to"])
        res = VGroup(label(rf"Newton: \ ${nn}$ steps \ to the last digit", font_size=24, color=NEWTON),
                     label(rf"gradient descent: \ ${it6:,}$ steps \ to $10^{{-6}}$".replace(",", "{,}"), font_size=24,
                           color=GD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, 0.6, 0])
        settle = int(next((k for k in range(1, len(LN)) if abs(LN[k, 3] - LN[-1, 3]) < 1e-3), len(LN) - 1))
        with self.voiceover(
            "Race them, from the same start. <bookmark mark='a'/> After one step, Newton's line is already near the "
            f"answer; after {settle}, it's there. Gradient descent, after the same number of steps, is still swinging into "
            f"place. <bookmark mark='b'/> With all seventy rates, Newton needs {nn} steps to reach the bottom to the "
            f"last digit; gradient descent needs {it6:,} steps to get within a millionth. Near the bottom, Newton "
            "doubles the number of correct digits at every step. The price: a seventy by seventy system to solve "
            "each time, which is why giant models stay with gradients."
        ) as vo:
            for plane, dots, t, Ls, col in panels:
                self.play(FadeIn(plane), FadeIn(dots), FadeIn(t), run_time=0.8)
            self.add(ln, rd)
            vo.wait_until("a")
            for k in range(1, len(LN)):
                self.play(step_t.animate.set_value(k), run_time=0.9)
            vo.wait_until("b")
            ln.clear_updaters()
            rd.clear_updaters()
            self.play(FadeOut(VGroup(*[VGroup(pl, d_, t_) for pl, d_, t_, _, _ in panels], ln, rd)))
            self.play(FadeIn(g70), FadeIn(g70n))
            self.play(Create(cn), Create(cg), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def digits(self):
        ir = load("irls")
        gaps = [g_ for g_ in ir["newton_gap"][1:] if g_ > 0]
        dig = [-math.log10(g_) for g_ in gaps]
        n = len(dig)
        g = plot([0.4, n + 0.6, 1], [0, 16, 4], x_length=6.4, y_length=4.2, xticks=list(range(1, n + 1)),
                 yticks=[0, 4, 8, 12, 16], center=[-2.6, -0.4, 0], xlabel=r"Newton step",
                 ylabel=r"correct digits of the minimum \ ($-\log_{10}$ of the gap)")
        ax = g.ax
        bars = VGroup()
        for k, d in enumerate(dig, 1):
            p0, p1 = ax.c2p(k - 0.32, 0), ax.c2p(k + 0.32, d)
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=NEWTON,
                               fill_opacity=0.85).move_to((p0 + p1) / 2))
        vals = VGroup(*[MathTex(f"{d:.1f}", font_size=22, color=NEWTON).next_to(b, UP, buff=0.06) for b, d in zip(bars, dig)])
        colors = {r"e_{k+1}": NEWTON, r"e_k": NEWTON}
        rows = [cmath(r"e_{k+1}", r"\;\approx\;", r"C\,e_k^2", font_size=40, colors=colors),
                cmath(r"\text{digits}_{k+1}", r"\;\approx\;", r"2\times\text{digits}_k", font_size=40)]
        whys = [why(r"near the bottom: \\ the error squares"), why(r"take $-\log_{10}$")]
        step = side_ladder(self, rows, whys, 3.8, 2.9, keep=2, top=2.4, buff=0.5)
        last = dig[-3:]
        doubling = len(last) == 3 and last[1] > 1.4 * last[0] and last[2] > 1.4 * last[1]
        say = (f"the correct digits go {last[0]:.0f}, {last[1]:.0f}, {last[2]:.0f}: roughly doubling, until the "
               "computer's sixteen digits run out." if doubling else
               f"the correct digits go {last[0]:.0f}, {last[1]:.0f}, {last[2]:.0f}.")
        with self.voiceover(
            "Why is Newton so fast at the end? Near the bottom, the loss is almost exactly a parabola, and each step's "
            "error is about the square of the last one. <bookmark mark='a'/> Square a small number and its zeros "
            "double. <bookmark mark='b'/> On the seventy rates, step by step, " + say
        ) as vo:
            self.play(FadeIn(g))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25), FadeIn(vals), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def runaway(self):
        ir = load("irls")
        pens = np.asarray(ir["pens"])
        norms = np.asarray(ir["norms"])
        losses = np.asarray(ir["losses"])
        sep = bool(ir["separable"])
        lx = -np.log10(pens)  # left: a strong penalty; right: almost none
        g = plot([0.5, 7.5, 1], [0, float(norms.max()) * 1.15, 5], x_length=6.2, y_length=3.8,
                 xticks=list(range(1, 8)), yticks=[0, 5, 10], xfmt=lambda v: f"10^{{-{int(v)}}}", center=[-2.8, -0.4, 0],
                 xlabel=r"the penalty $\lambda$, \ weaker $\longrightarrow$", ylabel=r"length of the weights $\|\mathbf{w}\|$")
        ax = g.ax
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=BAD) for a, b in zip(lx, norms)])
        cv = VMobject(color=BAD, stroke_width=3).set_points_as_corners([ax.c2p(a, b) for a, b in zip(lx, norms)])
        reads = VGroup(
            label(r"all $70$ rates, \ the training pages:", font_size=24, color=GREY_A),
            label(r"every training page right" if sep else r"not every training page right", font_size=24, color=HL),
            label(rf"loss at $\lambda = {sci_tex(pens[-1], 0)}$: \ ${sci_tex(losses[-1])}$ bits per page", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.7, 1.2, 0])
        link = label(r"without a penalty, \ gradient descent's line turns, \ slowly, \\ toward the widest margin: "
                     r"\ Chapter 11's SVM \ (Soudry et al., 2018)", font_size=22, color=GREY_B).move_to([3.5, -1.6, 0])
        if sep:
            say = ("Here's a trap. With all seventy rates, a line separates every training page perfectly. "
                   "<bookmark mark='a'/> Then there's no best line: making the weights longer always makes the "
                   "probabilities more confident and the loss smaller, down toward zero. <bookmark mark='b'/> Weaken the "
                   f"penalty {pens[0] / pens[-1]:,.0f}-fold, and the weights grow from {norms[0]:.1f} to "
                   f"{norms[-1]:.1f}, without end. That's one more reason for a small penalty. "
                   "<bookmark mark='c'/> Run plain gradient descent instead, and the weights grow forever, but their "
                   "direction settles, slowly, on the line with the widest margin: chapter eleven's support vector machine.")
        else:
            say = ("With all seventy rates, no line separates every training page, so the best line exists. "
                   "<bookmark mark='a'/> The penalty still shapes it: <bookmark mark='b'/> weaken it "
                   f"{pens[0] / pens[-1]:,.0f}-fold, and the weights grow from {norms[0]:.1f} to {norms[-1]:.1f}, then "
                   "settle. <bookmark mark='c'/> On separable data they would grow forever.")
        with self.voiceover(say) as vo:
            self.play(FadeIn(g), FadeIn(reads[0]))
            self.play(FadeIn(reads[1]))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(Create(cv), LaggedStart(*[FadeIn(d) for d in pts[1:]], lag_ratio=0.15), run_time=2.0)
            self.play(FadeIn(reads[2]))
            vo.wait_until("c")
            self.play(FadeIn(link))
        self.wait(0.3)
        self.clear_scene()

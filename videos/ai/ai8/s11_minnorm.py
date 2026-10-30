from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import BOUND, HIST, MEAS, TEST, chapter, curve, load, log_axes

PATH, SOL, ROW = C.BITS, C.MODEL_Q, C.TRUE_P


class MinNorm(VoiceoverScene, ThreeDScene):
    def construct(self):
        chapter(self, 10, r"Implicit bias: the smallest fit", r"Of all the perfect fits, which one does training find?",
                "Chapter ten. Implicit bias: the smallest fit.")
        self.picture()
        self.proof()
        self.check()

    # ------------------------------------------------------------------
    def picture(self):
        m = load("minnorm")
        X3, wp, nv = np.asarray(m["X3"]), np.asarray(m["w3p"]), np.asarray(m["null3"])
        path = np.asarray(m["path3"])
        S = 3.2
        ax = ThreeDAxes(x_range=[-1.5, 1.5, 1], y_range=[-1.5, 1.5, 1], z_range=[-1.5, 1.5, 1], x_length=S * 2,
                        y_length=S * 2, z_length=S * 2, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                                       "include_tip": False})
        sol = Line(ax.c2p(*(wp - 1.6 * nv)), ax.c2p(*(wp + 1.6 * nv)), color=SOL, stroke_width=5)
        r1, r2 = X3[0] / np.linalg.norm(X3[0]), X3[1] - (X3[1] @ X3[0]) / (X3[0] @ X3[0]) * X3[0]
        r2 = r2 / np.linalg.norm(r2)
        plane = Surface(lambda u, v: ax.c2p(*(u * r1 + v * r2)), u_range=[-1.4, 1.4], v_range=[-1.4, 1.4],
                        resolution=(8, 8), fill_color=ROW, fill_opacity=0.18, stroke_color=ROW, stroke_width=0.4,
                        stroke_opacity=0.4)
        pts = [ax.c2p(*p) for p in path]
        trail = VMobject(color=PATH, stroke_width=4).set_points_as_corners(pts)
        dots = VGroup(*[Dot3D(p, radius=0.045, color=PATH) for p in pts[:12]])
        star = Dot3D(ax.c2p(*wp), radius=0.09, color=YELLOW)
        o = Dot3D(ax.c2p(0, 0, 0), radius=0.07, color=WHITE)
        perp = DashedLine(ax.c2p(0, 0, 0), ax.c2p(*wp), color=YELLOW, stroke_width=2)
        t1 = label(r"$3$ weights, \ $2$ equations: \ the exact fits form a line", font_size=26, color=SOL)
        t2 = label(r"gradient descent from $0$ \ stays in the plane of the inputs", font_size=26, color=ROW)
        t3 = label(r"and lands on the fit nearest the origin", font_size=26, color=YELLOW)
        VGroup(t1, t2, t3).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.3)
        tag = note(r"illustrative: \ two equations in three unknowns").to_corner(DR, buff=0.25)
        for mob in (t1, t2, t3, tag):
            self.add_fixed_in_frame_mobjects(mob)
            self.remove(mob)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-30 * DEGREES, zoom=1.1)
        with self.voiceover(
            "When a model has more weights than training examples, it can usually fit them all exactly, in "
            "infinitely many ways. Three weights and two equations: <bookmark mark='a'/> every point on this line "
            "fits both exactly. Which one does training pick? <bookmark mark='b'/> Run gradient descent on the "
            "squared error, starting from zero. Every step moves along a combination of the inputs, so the path "
            "never leaves the plane they span. <bookmark mark='c'/> It meets the line of exact fits at one point: "
            "the one nearest the origin, the fit with the smallest weights."
        ) as vo:
            self.play(Create(ax), FadeIn(o), FadeIn(tag))
            self.begin_ambient_camera_rotation(rate=0.07)
            vo.wait_until("a")
            self.play(Create(sol), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(plane), FadeIn(t2))
            self.play(Create(trail), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(star), Create(perp), FadeIn(t3))
        self.stop_ambient_camera_rotation()
        self.wait(0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    def proof(self):
        rows = [
            cmath(r"w_{t+1}", r"=", r"w_t - \eta\, X^\top (X w_t - y)", font_size=36),
            cmath(r"w_t", r"\in", r"\operatorname{row}(X) = \operatorname{span}\{x_1, \dots, x_n\}", font_size=36),
            cmath(r"X w_\infty", r"=", r"y", font_size=36),
            cmath(r"w_\infty", r"=", r"X^\top (X X^\top)^{-1} y = X^{+} y", font_size=36,
                  colors={r"X^\top (X X^\top)^{-1} y = X^{+} y": YELLOW}),
            cmath(r"|w|^2", r"=", r"|w_\infty|^2 + |w - w_\infty|^2 \ \ge\ |w_\infty|^2", font_size=36),
        ]
        whys = [why(r"a gradient step on $\tfrac12 |Xw - y|^2$"),
                why(r"$w_0 = 0$, \ and each step adds $X^\top(\cdot)$"),
                why(r"convex, \ $\eta < 2/\lambda_{\max}$: \ the loss reaches $0$"),
                why(r"the only exact fit in the row space"),
                why(r"any exact fit $w$: \ $w - w_\infty \perp \operatorname{row}(X)$, \ Pythagoras")]
        step = ladder(self, rows, whys, keep=5, top=2.9, x=-2.0, buff=0.42, edge=6.9)
        head = label(r"The proof, \ for $n$ equations in $d > n$ unknowns", font_size=28, color=GREY_A).to_edge(UP, buff=0.25)
        with self.voiceover(
            "The proof is five lines. <bookmark mark='a'/> A gradient step subtracts X transpose times the residual. "
            "<bookmark mark='b'/> Start at zero, and every iterate is a combination of the training inputs: it lives "
            "in the row space of X. <bookmark mark='c'/> With a small enough step, the loss is convex and goes to "
            "zero, so the limit fits every example. <bookmark mark='d'/> Only one exact fit lies in the row space: "
            "X transpose times X X transpose inverse times y, the pseudoinverse solution. <bookmark mark='e'/> And "
            "any other exact fit differs from it by a vector perpendicular to the row space, so by Pythagoras it's "
            "longer. Gradient descent, untold, chose the minimum-norm fit. That's an implicit bias: a preference "
            "the algorithm brings that no loss function asked for."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                step(k)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        m = load("minnorm")
        ts = np.asarray(m["ts"], float)
        d0, d1, nl = np.asarray(m["dist0"]), np.asarray(m["dist1"]), np.asarray(m["null0"])
        G = log_axes((0, math.log10(ts[-1])), (-16, 1), x_length=6.6, y_length=4.4, xticks=[0, 1, 2, 3, 4],
                     yticks=[-15, -10, -5, 0], xlabel=r"steps", ylabel=r"distance from the pseudoinverse solution $X^+y$",
                     center=(-2.6, -0.5, 0))
        ax = G.ax
        lt = np.log10(ts)
        c0 = curve(ax, lt, np.log10(np.maximum(d0, 1e-16)), MEAS, 4)
        c1 = curve(ax, lt, np.log10(np.maximum(d1, 1e-16)), C.SURPRISE, 3.5)
        key = legend([(MEAS, r"from $w_0 = 0$"), (C.SURPRISE, r"from a random $w_0$")], font_size=20)
        key.next_to(G, UP, buff=0.05).align_to(G, RIGHT)
        n, d = int(m["n"]), int(m["d"])
        res = VGroup(
            label(rf"${n}$ equations, \ ${d}$ unknowns", font_size=24),
            label(rf"from $0$: \ distance ${sci(d0[-1], 0)}$", font_size=22, color=MEAS),
            label(rf"part outside the row space: \ ${sci(nl[-1], 0)}$", font_size=22, color=MEAS),
            label(rf"$|w| = {m['norm0']:.3f} = |X^+ y|$", font_size=22, color=MEAS),
            label(rf"from random $w_0$: \ stops ${d1[-1]:.2f}$ away, \ $|w| = {m['norm1']:.2f}$", font_size=22,
                  color=C.SURPRISE),
            label(rf"predicted: \ $|(I - P)\,w_0| = {m['pred_gap']:.2f}$", font_size=22, color=C.SURPRISE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.4, -0.2, 0])
        agree = abs(d1[-1] - m["pred_gap"]) < 1e-6 * max(1.0, m["pred_gap"])
        which = ("exactly the part of the starting point that lay outside the row space, which no step ever "
                 "touches. " if agree else "close to the part of the starting point outside the row space. ")
        with self.voiceover(
            f"Check it with {n} equations in {d} unknowns. <bookmark mark='a'/> From zero, the distance to the "
            "pseudoinverse solution falls until it hits the limits of double precision, and the part of the weights "
            "outside the row space stays at rounding error the whole way. <bookmark mark='b'/> Start somewhere "
            f"else, and descent still fits every equation, but stops {d1[-1]:.2f} away from the minimum-norm fit, "
            + which
            + "So the answer depends on the start too: networks start near zero, with small random weights, and part "
            "nine of this series is about choosing that scale."
        ) as vo:
            self.play(FadeIn(G), FadeIn(res[0]))
            vo.wait_until("a")
            self.play(Create(c0), FadeIn(key[0]), FadeIn(res[1:4]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(key[1]), FadeIn(res[4:]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

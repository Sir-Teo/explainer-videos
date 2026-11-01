from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import (AUSTEN, BAD, DICKENS, GOOD, HIST, HL, chapter, load, plot, sci_tex, side_ladder)
from videos.ai.ai6.compute import toy_ring

GOLD = C.BITS


class Kernels(VoiceoverScene, ThreeDScene):
    def construct(self):
        chapter(self, 10, r"Kernels: lifting without lifting", r"What if no line can do it?",
                "Chapter ten. Kernels.", lit=(1958, 1969))
        self.perceptron()
        self.lift()
        self.trick()
        self.mercer()
        self.representer()

    # ------------------------------------------------------------------
    def perceptron(self):
        k = load("kernel")
        s = load("svm")
        hist = history_card(1958, r"Frank Rosenblatt", r"the perceptron: \ on every mistake, \ add the page to the "
                            r"weights, \ $\mathbf{w} \leftarrow \mathbf{w} + y\,\mathbf{x}$", color=HIST, width=5.6)
        hist.to_corner(UL, buff=0.3)
        nov_statement = (r"if a line separates the data with margin $\gamma$, \ the perceptron "
                         r"makes at most $(R/\gamma)^2$ mistakes")
        if zh():
            from explainer.zh_text import translate

            # Translate the original complete caption before splitting its two
            # clauses, so the squared bound has a real gap above its glyphs.
            nov_statement = VGroup(*[label(row, font_size=21)
                                     for row in translate(nov_statement).split(r"\ ", 1)])
            nov_statement.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        nov = theorem_card(r"Novikoff (1962)", nov_statement, width=5.6, font_size=21).next_to(hist, DOWN, buff=0.25)
        nov.align_to(hist, LEFT)
        P = np.array([[1.0, 1.0], [-1.0, -1.0], [1.0, -1.0], [-1.0, 1.0]])
        t = [1, 1, -1, -1]
        ax = Axes(x_range=[-1.6, 1.6, 1], y_range=[-1.6, 1.6, 1], x_length=3.4, y_length=3.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.6, 1.0, 0])
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.13, color=DICKENS if t_ > 0 else AUSTEN) for p, t_ in zip(P, t)])
        xor = label(r"XOR: \ no line separates them", font_size=24, color=WHITE).next_to(ax, UP, buff=0.15)
        flail = [Line(ax.c2p(-1.6, a), ax.c2p(1.6, b), color=BAD, stroke_width=3) for a, b in
                 ((-1.4, 1.2), (1.3, -0.6), (0.2, 0.3), (-0.9, 1.5))]
        mk = label(rf"perceptron: \ ${k['xor_mistakes_100']}$ mistakes in $100$ passes", font_size=22, color=BAD)
        mk.next_to(ax, DOWN, buff=0.2)
        lift = label(rf"add $x_1 x_2$ as a third number: \ separated after ${k['xor_lift_mistakes']}$ mistakes",
                     font_size=22, color=GOOD).next_to(mk, DOWN, buff=0.12)
        mp = label(r"Minsky \& Papert, \textit{Perceptrons} (1969)", font_size=22, color=GREY_B).to_corner(DL, buff=0.3)
        toy = label(rf"on the separable toy of the next chapter: \ ${s['perc_mistakes']}$ mistake"
                    + ("s" if s["perc_mistakes"] != 1 else "") + rf", \ bound ${s['perc_bound']:.0f}$",
                    font_size=20, color=GREY_A).next_to(nov, DOWN, buff=0.15).align_to(nov, LEFT)
        with self.voiceover(
            "In 1958 Frank Rosenblatt's perceptron learned a line from examples: each time it misclassifies a page, "
            "add that page to the weights. <bookmark mark='a'/> If some line separates the data with a margin, "
            "Novikoff proved it stops after at most R over gamma, squared, mistakes. <bookmark mark='b'/> But some "
            "patterns have no line at all. Exclusive or: <bookmark mark='c'/> the perceptron never stops, "
            f"{k['xor_mistakes_100']} mistakes in a hundred passes. Minsky and Papert's 1969 book made limits like "
            "this famous, and helped bring on a winter for neural networks. <bookmark mark='d'/> There are two ways "
            "out. Learn new features, which is Part 9's story. Or add them by hand: give each point a third number, "
            f"x one times x two, and the perceptron separates XOR after {k['xor_lift_mistakes']} mistakes."
        ) as vo:
            self.play(FadeIn(hist, shift=DOWN * 0.2), Create(ax), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(nov), FadeIn(toy))
            vo.wait_until("b")
            self.play(FadeIn(xor))
            vo.wait_until("c")
            cur = flail[0]
            self.play(Create(cur), run_time=0.5)
            for f in flail[1:]:
                self.play(Transform(cur, f), run_time=0.5)
            self.play(FadeIn(mk), FadeIn(mp))
            vo.wait_until("d")
            self.play(FadeOut(cur), FadeIn(lift))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lift(self):
        k = load("kernel")
        P, y = toy_ring()
        w, b = np.asarray(k["lift_w"]), float(k["lift_b"])
        axes = ThreeDAxes(x_range=[-2.4, 2.4, 1], y_range=[-2.4, 2.4, 1], z_range=[0, 5, 1], x_length=5.4, y_length=5.4,
                          z_length=3.2, axis_config={"stroke_color": GREY_C, "include_ticks": False, "include_tip": False})
        axes.shift(DOWN * 0.3)
        flat = VGroup(*[Dot(axes.c2p(p[0], p[1], 0), radius=0.06, color=AUSTEN if l_ == 0 else DICKENS)
                        for p, l_ in zip(P, y)])
        high = VGroup(*[Dot(axes.c2p(p[0], p[1], p @ p), radius=0.06, color=AUSTEN if l_ == 0 else DICKENS)
                        for p, l_ in zip(P, y)])
        bowl = Surface(lambda u, v: axes.c2p(u * math.cos(v), u * math.sin(v), u * u), u_range=[0, 2.2],
                       v_range=[0, 2 * math.pi], resolution=(14, 32), fill_opacity=0.12, stroke_width=0.4,
                       stroke_color=GREY_D, checkerboard_colors=False, fill_color=GREY_B)

        def zplane(u, v):  # the separating plane found by a hard-margin SVM on the lifted points
            return -(b + w[0] * u + w[1] * v) / w[2]

        cut = Surface(lambda u, v: axes.c2p(u, v, zplane(u, v)), u_range=[-2.3, 2.3], v_range=[-2.3, 2.3],
                      resolution=(2, 2), fill_opacity=0.35, fill_color=GOLD, stroke_width=0, checkerboard_colors=False)
        # where the plane meets the bowl: x1^2 + x2^2 = plane height, a circle (nearly centred, since w1, w2 are small)
        cx, cy = -w[0] / (2 * w[2]), -w[1] / (2 * w[2])
        r2 = cx * cx + cy * cy - b / w[2]
        rr = math.sqrt(max(r2, 0.01))
        circle3 = ParametricFunction(lambda t_: axes.c2p(cx + rr * math.cos(t_), cy + rr * math.sin(t_),
                                                        (cx + rr * math.cos(t_)) ** 2 + (cy + rr * math.sin(t_)) ** 2),
                                     t_range=[0, 2 * math.pi], color=GOLD, stroke_width=5)
        circle0 = ParametricFunction(lambda t_: axes.c2p(cx + rr * math.cos(t_), cy + rr * math.sin(t_), 0),
                                     t_range=[0, 2 * math.pi], color=GOLD, stroke_width=5)
        lf = cmath(r"(x_1, x_2)", r"\;\mapsto\;", r"(x_1,\, x_2,\,", r"x_1^2 + x_2^2", r")", colors={r"x_1^2 + x_2^2": GOLD},
                   font_size=38).to_corner(UL, buff=0.4)
        found = label(rf"the plane: \ a hard-margin SVM on the lifted points, \ ${len(k['lift_sv'])}$ support vectors",
                      font_size=22, color=GOLD).to_corner(DL, buff=0.35)
        no_line = label(r"no straight line separates these", font_size=28, color=GREY_A).to_corner(UR, buff=0.4)
        tag = label(r"illustrative points", font_size=22, color=GREY_B).to_corner(DR, buff=0.3)
        for m_ in (lf, found, no_line, tag):
            self.add_fixed_in_frame_mobjects(m_)
            self.remove(m_)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        with self.voiceover(
            "Here's the same idea with circles. No straight line separates the inside from the ring. "
            "<bookmark mark='a'/> Lift each point to a height equal to its squared distance from the centre. "
            "<bookmark mark='b'/> Now a flat plane separates them: this one was found by the next chapter's "
            "support vector machine, working on the lifted points. <bookmark mark='c'/> Seen from above, the plane "
            "cuts out a circle: a straight line in the lifted space is a curve in the original one."
        ) as vo:
            self.play(FadeIn(flat), FadeIn(no_line), FadeIn(tag))
            vo.wait_until("a")
            self.move_camera(phi=68 * DEGREES, theta=-50 * DEGREES, zoom=0.85, run_time=2.0)
            self.play(Create(axes), FadeIn(bowl), Transform(flat, high), Write(lf), run_time=2.0)
            self.begin_ambient_camera_rotation(rate=0.08)
            vo.wait_until("b")
            self.play(FadeIn(cut), Create(circle3), FadeIn(found))
            vo.wait_until("c")
            self.stop_ambient_camera_rotation()
            self.play(FadeOut(cut), FadeOut(bowl))
            self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=2.0)
            self.play(Transform(flat, VGroup(*[Dot(axes.c2p(p[0], p[1], 0), radius=0.06, color=AUSTEN if l_ == 0 else DICKENS)
                                               for p, l_ in zip(P, y)])), ReplacementTransform(circle3, circle0))
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    def trick(self):
        k = load("kernel")
        colors = {r"K(\mathbf{x}, \mathbf{z})": GOLD}
        rows = [
            cmath(r"\varphi(\mathbf{x})", "=", r"(x_1^2,\ x_2^2,\ \sqrt2\,x_1x_2,\ \sqrt2\,x_1,\ \sqrt2\,x_2,\ 1)",
                  font_size=32, colors=colors),
            cmath(r"\varphi(\mathbf{x})\cdot\varphi(\mathbf{z})", "=",
                  r"x_1^2z_1^2 + x_2^2z_2^2 + 2x_1x_2z_1z_2 + 2x_1z_1 + 2x_2z_2 + 1", font_size=32, colors=colors),
            cmath(r"\varphi(\mathbf{x})\cdot\varphi(\mathbf{z})", "=", r"(\mathbf{x}\cdot\mathbf{z} + 1)^2", "=",
                  r"K(\mathbf{x}, \mathbf{z})", font_size=32, colors=colors),
            cmath(r"e^{-\gamma\|\mathbf{x} - \mathbf{z}\|^2}", "=",
                  r"e^{-\gamma\|\mathbf{x}\|^2}e^{-\gamma\|\mathbf{z}\|^2}\sum_{k=0}^{\infty}\frac{(2\gamma)^k}{k!}"
                  r"(\mathbf{x}\cdot\mathbf{z})^k", font_size=32, colors=colors),
        ]
        whys = [why(r"six features"), why(r"multiply out"), why(r"computed from two numbers"),
                why(r"the Gaussian kernel: \\ every power, \ forever")]
        step = side_ladder(self, rows, whys, -0.4, 6.4, keep=3, top=3.3, buff=0.38)
        chk = label(rf"checked on $1{{,}}000$ random pairs: \ largest difference ${sci_tex(k['poly_err'])}$",
                    font_size=22, color=HL).to_edge(DOWN, buff=0.4)
        errs = np.asarray(k["taylor_err"])
        g = plot([0.5, len(errs) + 0.5, 5], [-8, 0.2, 2], x_length=4.2, y_length=1.5, xticks=[1, 10, 20],
                 yticks=[0, -4, -8], yfmt=lambda v: f"10^{{{int(v)}}}", center=[3.4, -2.55, 0],
                 xlabel=r"1D powers kept", ylabel=r"maximum error on a $61 \times 61$ grid")
        tc = curve(g.ax, np.arange(1, len(errs) + 1), np.log10(errs), GOLD, stroke_width=3)
        domain = note(r"1D: $x,z \in [-1.5,1.5]$, $\gamma=1$", font_size=17).next_to(g, UP, buff=0.06)
        within = next((w_ for lim_, w_ in ((1e-7, "a ten-millionth"), (1e-6, "a millionth"), (1e-5, "a hundred-thousandth"),
                                            (1e-3, "a thousandth")) if errs[-1] < lim_), f"{errs[-1]:.2f}")
        with self.voiceover(
            "The lift can be expensive: with many numbers per point, the lifted features multiply. The kernel trick "
            "avoids it. <bookmark mark='a'/> Take these six features of a point in the plane. <bookmark mark='b'/> "
            "Their dot product, multiplied out, <bookmark mark='c'/> is just x dot z plus one, squared: computed "
            "from the two original numbers, never the six. Any method that only needs dot products, like the "
            "support vector machine, can run in the lifted space for free. <bookmark mark='d'/> The Gaussian "
            "kernel goes further. Expand it, and its features are every power of the coordinates: infinitely many. "
            f"For a one-dimensional check with gamma one, keep the first {len(errs)} powers. On a sixty-one by sixty-one "
            f"grid with both inputs between minus one point five and one point five, the largest error is below {within}."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=GOLD))
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            self.play(FadeIn(chk))
            vo.wait_until("d")
            self.play(FadeOut(chk))
            step(3, transform=False)
            self.play(FadeIn(g), FadeIn(domain), Create(tc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mercer(self):
        k = load("kernel")
        ev, es = np.asarray(k["ev2"]), np.asarray(k["ev_sig"])
        n = len(ev)
        thm = theorem_card(r"positive semidefinite kernels", r"For real symmetric $K$, \ a feature map with "
                           r"$K(\mathbf{x}, \mathbf{z}) = "
                           r"\varphi(\mathbf{x})\cdot\varphi(\mathbf{z})$ exists exactly when every Gram matrix "
                           r"$[K(\mathbf{x}_i, \mathbf{x}_j)]$ has no negative eigenvalues.",
                           who=r"Aronszajn (1950)", width=6.0, font_size=21)
        thm.to_corner(UL, buff=0.3)
        lo = float(min(es.min(), 0)) * 1.1
        hi = float(max(ev.max(), es.max())) * 1.1
        g = plot([0, n, 100], [lo, hi, 100], x_length=6.0, y_length=4.2, xticks=[0, 200, 400], yticks=[-200, 0, 200],
                 center=[3.3, -0.3, 0], xlabel=rf"eigenvalues of the ${n} \times {n}$ Gram matrix, \ largest first",
                 ylabel=r"eigenvalue")
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(n, 0), color=GREY_B, stroke_width=1.5)
        ce = curve(ax, np.arange(n), ev, GOOD, stroke_width=4)
        cs = curve(ax, np.arange(n), es, BAD, stroke_width=3)
        lg = VGroup(label(rf"Gaussian kernel: \ smallest ${sci_tex(k['min_ev2'])}$", font_size=22, color=GOOD),
                    label(rf"$\tanh(\mathbf{{x}}\cdot\mathbf{{z}} - 1)$: \ ${k['n_neg_sig']}$ negative, \ smallest "
                          rf"${k['min_sig']:.0f}$", font_size=22, color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        lg.next_to(thm, DOWN, buff=0.4).align_to(thm, LEFT)
        rounding = abs(k["min_ev2"]) < 1e-9
        smallest = "zero, up to rounding." if rounding else f"{k['min_ev2']:.2g}."
        with self.voiceover(
            "Which similarity scores are allowed? For a real symmetric similarity function, a feature-space "
            "dot product exists exactly when every Gram matrix is positive semidefinite: it has no negative "
            "eigenvalues. "
            f"<bookmark mark='a'/> On the {n} training pages, the Gaussian kernel's smallest eigenvalue is {smallest} "
            "<bookmark mark='b'/> A popular impostor, the hyperbolic tangent of a dot product, has "
            f"{k['n_neg_sig']} negative eigenvalues: no features could produce it, and an SVM built on it is no "
            "longer solving a convex problem."
        ) as vo:
            self.play(FadeIn(thm, shift=DOWN * 0.2), FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(Create(ce), FadeIn(lg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cs), FadeIn(lg[1]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def representer(self):
        k = load("kernel")
        colors = {r"\alpha_i": GOLD, r"f_\perp": BAD}
        rows = [
            cmath(r"\min_f", r"\;\sum_i L\big(y_i, f(\mathbf{x}_i)\big) + \lambda\|f\|^2", font_size=34, colors=colors),
            cmath(r"f", "=", r"\sum_i \alpha_i K(\mathbf{x}_i, \cdot\,) + f_\perp", font_size=34, colors=colors),
            cmath(r"f(\mathbf{x}_j)", "=", r"\sum_i \alpha_i K(\mathbf{x}_i, \mathbf{x}_j) + 0", font_size=34, colors=colors),
            cmath(r"\|f\|^2", "=", r"\Big\|\sum_i \alpha_i K(\mathbf{x}_i, \cdot\,)\Big\|^2 + \|f_\perp\|^2", font_size=34,
                  colors=colors),
        ]
        whys = [why(r"any loss, \ a positive penalty $\lambda > 0$"), why(r"split: \ in the span of the data, \ or not"),
                why(r"$f_\perp$ is invisible \\ at the data"), why(r"$f_\perp$ only costs: \ $f_\perp = 0$")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.2, buff=0.36, edge=6.8)
        thm = theorem_card(r"the representer theorem", r"any minimizer for $\lambda > 0$ is "
                           r"$f = \sum_i \alpha_i K(\mathbf{x}_i, \cdot\,)$: "
                           r"one number per training point", who=r"Kimeldorf \& Wahba (1971); \ Sch\"olkopf, Herbrich \& "
                           r"Smola (2001)", width=6.8, font_size=21).to_edge(DOWN, buff=0.25).to_edge(LEFT, buff=0.3)
        chk = VGroup(label(rf"ridge in ${k['rep_dims']:,}$ random Gaussian features:".replace(",", "{,}"), font_size=21,
                           color=GREY_A),
                     label(rf"the answer outside the data's span: \ ${sci_tex(k['rep_resid'])}$", font_size=21, color=HL),
                     label(rf"kernel ridge on two rates: \ ${100 * k['krr_acc']:.0f}\%$ of held-out pages",
                           font_size=21, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        chk.to_corner(DR, buff=0.35)
        head = label(r"Why one weight per page is enough", font_size=30).to_edge(UP, buff=0.25)
        with self.voiceover(
            "One more guarantee makes kernels practical. <bookmark mark='a'/> Fit any function with any loss, plus "
            "a positive penalty on its squared size. <bookmark mark='b'/> Split the function into a part built from the kernel at the "
            "training points, and a part perpendicular to all of them. <bookmark mark='c'/> At the training points, "
            "the perpendicular part is invisible: it changes no prediction. <bookmark mark='d'/> It only adds to the "
            "size. So it must be zero, and the answer is a weighted sum of kernels at the training points: the "
            "representer theorem. <bookmark mark='e'/> Check it: solve ridge regression in "
            f"{k['rep_dims']:,} explicit random features of the pages, and the answer lies in the span of the "
            "pages' own features, to the last digit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            step(3, transform=False)
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in chk], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

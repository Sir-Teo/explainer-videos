from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, VALUE, bowl, load


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def frame(caption, color):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            return box, label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)

        out = []
        # 1. the derivative: a curve and its tangent
        xs = np.linspace(0.08, 1, 60)
        ax = Axes(x_range=[0, 1, 1], y_range=[0, 4, 1], x_length=TW, y_length=TH - 0.2, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        tan = Line(ax.c2p(0.05, 2 + 2.885 * 0.2), ax.c2p(0.6, 2 - 2.885 * 0.35), color=GRAD, stroke_width=3)
        out.append((VGroup(ax, ax.plot_line_graph(xs, np.log2(1 / xs), add_vertex_dots=False, line_color=C.SURPRISE,
                                                  stroke_width=3), tan), r"the derivative", GRAD))
        # 2. the gradient on contour lines
        ax2 = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=TW, y_length=TH, tips=False,
                   axis_config={"stroke_width": 0})
        cont = contour_lines(ax2, bowl, (-4, 4), (-3, 3), np.linspace(0.4, 3.6, 9), n=(60, 45), stroke_width=1.5)
        out.append((VGroup(cont, Arrow(ax2.c2p(1.6, -1.4), ax2.c2p(2.3, -2.2), buff=0, color=GRAD, stroke_width=4)),
                    r"the gradient", GRAD))
        # 3. a bent grid
        g = VGroup()
        for t in np.linspace(-1, 1, 6):
            g.add(VMobject(color=BLUE_C, stroke_width=1.8).set_points_smoothly(
                [np.array([s + 0.25 * math.sin(2 * t), t + 0.25 * math.sin(2 * s), 0]) for s in np.linspace(-1, 1, 12)]))
            g.add(VMobject(color=BLUE_C, stroke_width=1.8).set_points_smoothly(
                [np.array([t + 0.25 * math.sin(2 * s), s + 0.25 * math.sin(2 * t), 0]) for s in np.linspace(-1, 1, 12)]))
        out.append((g, r"the Jacobian", BLUE_C))
        # 4. forwards vs backwards: a matrix against a row
        out.append((VGroup(Rectangle(width=1.6, height=1.0, fill_color=VALUE, fill_opacity=0.5, stroke_color=VALUE),
                           Rectangle(width=1.6, height=0.22, fill_color=GRAD, fill_opacity=0.7, stroke_color=GRAD))
                    .arrange(DOWN, buff=0.35), r"backwards is cheaper", GRAD))
        # 5. backprop: a chain with values and gradients
        nodes = VGroup(*[Circle(radius=0.2, color=GREY_B, stroke_width=2).move_to([-1.2 + 0.8 * k, 0, 0]) for k in range(4)])
        fw = VGroup(*[Arrow(nodes[k].get_right(), nodes[k + 1].get_left(), buff=0.03, color=VALUE, stroke_width=3)
                      .shift(UP * 0.18) for k in range(3)])
        bw = VGroup(*[Arrow(nodes[k + 1].get_left(), nodes[k].get_right(), buff=0.03, color=GRAD, stroke_width=3)
                      .shift(DOWN * 0.18) for k in range(3)])
        out.append((VGroup(nodes, fw, bw), r"backpropagation", GRAD))
        # 6. the library
        code = code_block(["def backward(self):", "  for t in reversed(order):", "    for p, vjp in t.parents:",
                           "      grads[p] += vjp(g)"], font_size=14, buff=0.08)
        out.append((code, r"our own autodiff", GREY_A))
        # 7. training: down to the counting answer
        d = load("train")
        cv = np.asarray(d["curve"])
        ax3 = Axes(x_range=[0, cv[-1, 0], 500], y_range=[3.0, 5.0, 1], x_length=TW, y_length=TH - 0.2, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out.append((VGroup(ax3, ax3.plot_line_graph(cv[:, 0], np.clip(cv[:, 1], 3, 5), add_vertex_dots=False,
                                                    line_color=GRAD, stroke_width=3),
                           DashedLine(ax3.c2p(0, d["H_cond"]), ax3.c2p(cv[-1, 0], d["H_cond"]), color=C.COUNTING)),
                    rf"descent finds ${d['H_cond']:.2f}$ bits", C.COUNTING))
        # 8. the narrow valley
        v = load("valley")
        gd = np.asarray(v["gd"])
        ax4 = Axes(x_range=[-5, 5, 1], y_range=[-1.2, 1.2, 1], x_length=TW, y_length=TH - 0.4, tips=False,
                   axis_config={"stroke_width": 0})
        out.append((VGroup(*[Ellipse(width=TW * k / 5, height=(TH - 0.4) * k / 5 * 0.2 * 5, color=GREY_C, stroke_width=1.2)
                             for k in (1, 2, 3, 4)],
                           VMobject(color=WHITE, stroke_width=2.5).set_points_as_corners([ax4.c2p(*q) for q in gd[:40]])),
                    r"curvature: \ the zigzag", WHITE))
        tiles = Group()
        for pic, cap, col in out:
            box, c = frame(cap, col)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(r"Part 4, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Zoom in on a smooth function and it becomes a straight line, whose slope is the "
            "derivative. With many inputs, the slopes form the gradient, which points uphill. Up close, a map between "
            "spaces is a matrix, its Jacobian, and the chain rule multiplies those matrices. Multiplying them from the "
            "loss backwards is cheap, and that's backpropagation. We built it in a few lines, checked it, and trained "
            "a model with it. And curvature told us why going downhill can still be slow."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"backpropagation, our library", [9, 13]),
            (r"gradient descent, curvature", [11]),
            (r"Jacobians through depth", [9, 12]),
            (r"saddles and valleys", [8, 11]),
        ], font_size=26)
        with self.voiceover(
            "This is the engine of everything that follows. Our library trains the first neural network of the "
            "series in part nine, and the chain of Jacobians through a deep network decides whether it can learn at "
            "all. Curvature, valleys and saddles come back when we build better optimizers, in part eleven."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 5, \ Randomness in Motion", font_size=40).to_edge(UP, buff=0.35)
        g = np.random.default_rng(1827)
        paths = VGroup()
        for k in range(14):
            steps = g.normal(size=240) * 0.11
            ys = np.cumsum(steps)
            pts = [np.array([-5.5 + 11 * i / 239, y, 0]) for i, y in enumerate(ys)]
            paths.add(VMobject(color=interpolate_color(ManimColor(C.TRUE_P), ManimColor(C.BITS), k / 13),
                               stroke_width=2).set_points_as_corners(pts))
        paths.stretch_to_fit_height(min(paths.height, 4.6)).move_to(DOWN * 0.2)
        tag = label(r"random walks; \ Robert Brown watched pollen jiggle in 1827", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Next time: randomness. Probability distributions that move, random walks that become Brownian motion, "
            "and the noise that diffusion models learn to undo. <bookmark mark='a'/> It's the last piece of "
            "mathematics we need before the models themselves."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.1), FadeIn(tag), run_time=3.0)
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"I.~Goodfellow, Y.~Bengio \& A.~Courville, \textit{Deep Learning} (2016), chapters 4 and 6.5",
            r"A.~Griewank \& A.~Walther, \textit{Evaluating Derivatives}, 2nd ed.\ (2008)",
            r"J.~Nocedal \& S.~J.~Wright, \textit{Numerical Optimization}, 2nd ed.\ (2006), chapters 2--3",
        ]
        papers = [
            r"S.~Linnainmaa, \textit{The Representation of the Cumulative Rounding Error of an Algorithm} (1970)",
            r"D.~E.~Rumelhart, G.~E.~Hinton \& R.~J.~Williams, \textit{Learning Representations by Back-propagating "
            r"Errors} (1986)",
            r"A.~G.~Baydin et al., \textit{Automatic Differentiation in Machine Learning: a Survey} (JMLR 2018)",
            r"Y.~Dauphin et al., \textit{Identifying and Attacking the Saddle Point Problem} (2014)",
            r"A.~Paszke et al., \textit{PyTorch} (2019); \ A.~Karpathy, \textit{micrograd} (2020)",
        ]
        card = reference_card(books, papers)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels). \ Every number on screen is computed and checked; "
                    r"\ schematics and illustrations are labeled.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "Griewank and Walther's Evaluating Derivatives is the book on automatic differentiation, and Baydin's "
            "survey is a good place to start. Thanks for watching, and see you in part five."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))

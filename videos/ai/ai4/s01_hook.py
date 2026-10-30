from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, HIST, PART, VALUE, load


class Hook(VoiceoverScene):
    def construct(self):
        self.recall()
        self.era()
        self.plan()

    # ------------------------------------------------------------------
    def recall(self):
        p = load("params")
        assert p["gpt2"] == 124_439_808 and 4.0e9 < p["qwen3_4b"] < 4.1e9
        colors = {r"q_k": C.MODEL_Q, r"\hat p_k": C.TRUE_P}
        f = cmath(r"\frac{\partial \mathcal{L}}{\partial z_k}", "=", r"q_k", "-", r"\hat p_k", colors=colors,
                  font_size=60).move_to(UP * 0.6)
        cap = label(r"Part 1: \ one derivative, worked out by hand", font_size=30, color=GREY_A).next_to(f, DOWN, buff=0.4)
        # a sea of numbers: each square stands for 54,000 of GPT-2's
        cols, rows = 64, 36
        side = 0.19
        g = np.random.default_rng(3)
        sea = VGroup(*[Square(side_length=side * 0.86, stroke_width=0, fill_color=VALUE,
                              fill_opacity=float(0.25 + 0.6 * g.random()))
                       .move_to([(c - (cols - 1) / 2) * side, (rows - 1) / 2 * side - r * side - 0.25, 0])
                       for r in range(rows) for c in range(cols)])
        n1 = label(rf"GPT-2: \ ${p['gpt2']:,}$ numbers".replace(",", "{,}"), font_size=34, color=WHITE)
        n2 = label(rf"Qwen3-4B: \ ${p['qwen3_4b']:,}$".replace(",", "{,}"), font_size=34, color=WHITE)
        for m in (n1, n2):
            m.add_background_rectangle(color=BACKGROUND, opacity=0.9, buff=0.12).set_z_index(5)
        VGroup(n1, n2).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.35)
        each = label(r"each needs $\partial \mathcal{L} / \partial \theta$, \ every step", font_size=30, color=GRAD)
        each.add_background_rectangle(color=BACKGROUND, opacity=0.9, buff=0.12).set_z_index(5)
        each.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In part one we worked out a single derivative by hand: the gradient of the surprise with respect to the "
            "scores, the model's guess minus the truth. <bookmark mark='a'/> GPT-2 has a hundred and twenty-four "
            "million numbers. Qwen3-4B has four billion. <bookmark mark='b'/> Every step of training needs the "
            "derivative of the loss with respect to every single one of them, and nobody works those out by hand."
        ) as vo:
            self.play(Write(f), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeOut(f), FadeOut(cap), LaggedStart(*[FadeIn(s) for s in sea], lag_ratio=0.0006), run_time=2.0)
            self.play(FadeIn(n1))
            self.play(FadeIn(n2))
            vo.wait_until("b")
            self.play(LaggedStart(*[s.animate.set_fill(GRAD, opacity=float(0.3 + 0.6 * g.random())) for s in sea],
                                  lag_ratio=0.0006), FadeIn(each), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def era(self):
        """How we got here: from Leibniz to eight-bit training, evenly spaced (not to scale)."""
        events = [
            (1684, r"Leibniz prints the calculus; \\ Newton's fluxions"),
            (1788, r"Lagrange: \\ multipliers"),
            (1847, r"Cauchy: \\ gradient descent"),
            (1939, r"Karush; \ Kuhn--Tucker \\ (1951): \ inequalities"),
            (1964, r"Wengert: \\ derivatives by program"),
            (1970, r"Linnainmaa: \\ reverse mode"),
            (1985, r"IEEE 754: \\ floating point"),
            (1986, r"Rumelhart, Hinton, \\ Williams: \ backprop"),
            (2010, r"Theano; \ then TensorFlow, \\ PyTorch, JAX"),
            (2022, r"eight-bit \\ floats for training"),
        ]
        n = len(events)
        xs = np.linspace(-5.9, 5.9, n)
        y0 = -0.2
        axis = Line([-6.6, y0, 0], [6.6, y0, 0], color=GREY_C, stroke_width=3)
        marks, skel = [], VGroup()
        for i, ((yr, txt), x) in enumerate(zip(events, xs)):
            up = i % 2 == 0
            stem = Line([x, y0, 0], [x, y0 + (0.9 if up else -0.9), 0], color=HIST, stroke_width=2.5)
            dot = Dot([x, y0, 0], radius=0.08, color=HIST)
            yl = label(rf"{yr}", font_size=30, color=HIST)
            t = label(txt, font_size=20, color=WHITE)
            words = VGroup(yl, t).arrange(DOWN, buff=0.06)
            words.next_to(stem.get_end(), UP if up else DOWN, buff=0.08)
            keep_in_frame(words, margin=0.12)
            marks.append(VGroup(stem, dot, words))
            skel.add(VGroup(stem.copy().set_stroke(GREY_D), Dot([x, y0, 0], radius=0.06, color=GREY_D),
                            yl.copy().set_color(GREY_D).move_to(yl)))
        head = label(r"How we got here", font_size=42).to_edge(UP, buff=0.3)
        tag = note(r"milestones evenly spaced, \ not to scale").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The mathematics is three centuries older than the computers that run it. Leibniz printed the calculus "
            "in 1684, while Newton had his own, his fluxions. <bookmark mark='a'/> In 1788 Lagrange showed how to "
            "optimize under constraints, <bookmark mark='b'/> and in 1847 Cauchy proposed walking downhill. "
            "<bookmark mark='c'/> Karush, and then Kuhn and Tucker, added inequalities. <bookmark mark='d'/> Then "
            "came programs: in 1964 Wengert had one carry derivatives along with its values, <bookmark mark='e'/> "
            "and in 1970 Linnainmaa ran the chain rule backwards. <bookmark mark='f'/> In 1985 a standard fixed how "
            "computers round, <bookmark mark='g'/> and in 1986 backpropagation made neural networks trainable. "
            "<bookmark mark='h'/> From 2010, libraries did all of it automatically, <bookmark mark='i'/> and some of "
            "today's largest models train with numbers only eight bits long."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tag), FadeIn(skel))
            self.play(FadeIn(marks[0], shift=UP * 0.2))
            for k, mk in enumerate("abcdefghi"):
                vo.wait_until(mk)
                self.play(FadeIn(marks[k + 1], shift=(UP if (k + 1) % 2 == 0 else DOWN) * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Change", font_size=50).to_edge(UP, buff=0.45)
        sub = label(r"the calculus of learning", font_size=30, color=GRAD).next_to(title, DOWN, buff=0.2)
        smap = series_map(current=PART, done=PART - 1).scale(0.78).move_to(DOWN * 0.7)
        obj = objectives_card([
            r"derivatives, \ gradients and Jacobians, \ as best linear approximations; \ the Jacobians of real layers",
            r"forward and reverse mode, \ counted; \ backpropagation by hand; \ our own library, \ its tape, "
            r"\ and a model trained with it",
            r"numbers in a computer: \ formats, \ rounding, \ cancellation, \ log-sum-exp, \ the gradient check",
            r"memory: \ recomputing instead of storing",
            r"curvature: \ Newton, \ Hessian-vector products, \ a trained network's Hessian, \ descent on "
            r"quadratics, \ saddles",
            r"constraints: \ Lagrange, \ KKT, \ duality; \ and differentiating through a fixed point",
        ], font_size=23).move_to(DOWN * 0.45)
        with self.voiceover(
            "This is Part 4 of AI, Built: change, the calculus of learning. <bookmark mark='a'/> In it: derivatives "
            "as the best straight-line approximations, and the derivatives of real layers; <bookmark mark='b'/> the "
            "two ways to run the chain rule, counted; backpropagation by hand, then our own library, and a model "
            "trained with it; <bookmark mark='c'/> what goes wrong with numbers in a computer; <bookmark mark='d'/> "
            "memory; <bookmark mark='e'/> curvature, from Newton's method to the shape of a trained network's "
            "landscape; <bookmark mark='f'/> and optimizing under constraints, which ends with differentiating "
            "through an equation's solution."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeOut(sub), FadeIn(obj.head), FadeIn(obj.rows[0], shift=UP * 0.1))
            for k, mk in enumerate("bcdef"):
                vo.wait_until(mk)
                self.play(FadeIn(obj.rows[k + 1], shift=UP * 0.1))
        self.wait(0.5)
        self.clear_scene()

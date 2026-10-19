from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, MONO, VALUE, load


class Hook(VoiceoverScene):
    def construct(self):
        self.recall()
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
    def plan(self):
        lines = [
            "def backward(self):",
            "    order = topological_order(self)",
            "    grads = {self: 1.0}",
            "    for t in reversed(order):",
            "        g = grads.pop(t)",
            "        for parent, vjp in t.parents:",
            "            grads[parent] += vjp(g)",
        ]
        code = code_block(lines, font_size=24, font=MONO)
        code[0].set_color(GRAD)
        code.move_to(DOWN * 0.9)
        box = SurroundingRectangle(code, color=GREY_D, buff=0.3, corner_radius=0.12)
        sk = label(r"a sketch of the idea; \ the real thing is in Chapter 6", font_size=22, color=GREY_B).next_to(box, DOWN, buff=0.15)
        title = label(r"Part 4: \ Change", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"the chain rule, run backwards", font_size=32, color=GRAD).next_to(title, DOWN, buff=0.25)
        smap = series_map(current=4, done=3).scale(0.85).move_to(DOWN * 0.6)
        with self.voiceover(
            "This part builds the machine that does it. It's a single idea, the chain rule run backwards, and it fits "
            "in a few pages of code. <bookmark mark='a'/> We'll build it, check it, and train a model with "
            "it on part one's books."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            self.play(Create(box), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in code], lag_ratio=0.15),
                      FadeIn(sk), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeOut(VGroup(box, code, sk)), FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()

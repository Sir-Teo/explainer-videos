from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import CHAIN, DIRECT, bit_row, chip, load


class Hook(VoiceoverScene):
    def construct(self):
        self.puzzle()
        self.plan()

    # ------------------------------------------------------------------
    def puzzle(self):
        p = load("parity")
        d16, c16 = float(p["acc_direct16"]), float(p["acc_cot16"])
        bits = np.random.default_rng(17).integers(0, 2, 16)
        run = np.cumsum(bits) % 2
        row = bit_row(bits, size=0.5, buff=0.1).move_to(UP * 1.9)
        q = label(r"Is the number of $1$s odd?", font_size=34).next_to(row, UP, buff=0.4)
        # answering at once: every bit flows into a fixed stack of two layers
        stack = VGroup(*[RoundedRectangle(width=2.6, height=0.5, corner_radius=0.1, stroke_color=DIRECT, stroke_width=2,
                                          fill_color=DIRECT, fill_opacity=0.12) for _ in range(2)]).arrange(UP, buff=0.12)
        stack.move_to([-3.6, -0.6, 0])
        st = label(r"$2$ layers, \ then answer", font_size=22, color=DIRECT).next_to(stack, LEFT, buff=0.25)
        feeds = VGroup(*[Line(b.get_bottom(), stack.get_top(), stroke_width=1.2, color=DIRECT).set_stroke(opacity=0.35) for b in row])
        out1 = chip("?", size=0.55, color=DIRECT).next_to(stack, DOWN, buff=0.45)
        a1 = Arrow(stack.get_bottom(), out1.get_top(), buff=0.06, stroke_width=3, color=DIRECT, max_tip_length_to_length_ratio=0.3)
        r1 = label(rf"right ${100 * d16:.0f}\%$ of the time", font_size=28, color=DIRECT).next_to(out1, DOWN, buff=0.3)
        # writing the running parity: one easy step per bit
        par = VGroup(*[chip(str(int(v)), size=0.5, color=CHAIN) for v in run])
        for c_, b in zip(par, row):
            c_.move_to(b.get_center() + DOWN * 0.95)
        pl = label(r"odd so far?", font_size=22, color=CHAIN).next_to(par, LEFT, buff=0.25)
        ring = SurroundingRectangle(VGroup(row[0], par[0]), color=C.BITS, buff=0.08, stroke_width=3, corner_radius=0.08)
        r2 = label(rf"writing its work first: \ right ${100 * c16:.0f}\%$", font_size=28, color=CHAIN).move_to([2.6, -1.9, 0])
        ans = SurroundingRectangle(par[-1], color=CHAIN, buff=0.06, stroke_width=4)
        tag = note(r"one string shown; \ accuracy on $1{,}000$ new strings").to_corner(DR, buff=0.25)
        coin = "a coin flip" if d16 < 0.6 else "far from reliable"
        with self.voiceover(
            "Here's a puzzle for a small transformer: sixteen bits. Is the number of ones odd? "
            "<bookmark mark='a'/> Trained to answer straight away, our two-layer model is right "
            f"{100 * d16:.0f} percent of the time: {coin}. <bookmark mark='b'/> Now train the very same model to "
            "write its work first: going along the bits, is the count odd so far? Each step is easy, just the last "
            f"answer and one more bit. <bookmark mark='c'/> Its final answer is right {100 * c16:.0f} percent of the "
            "time. Same model, same size. It just got to think out loud."
        ) as vo:
            self.play(FadeIn(q), LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in row], lag_ratio=0.05), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(stack), FadeIn(st), LaggedStart(*[Create(f) for f in feeds], lag_ratio=0.03), run_time=1.2)
            self.play(GrowArrow(a1), FadeIn(out1))
            self.play(FadeIn(r1))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(stack, st, feeds, a1, out1)), r1.animate.scale(0.8).move_to([-3.6, -1.9, 0]))
            self.play(Create(ring), FadeIn(pl))
            for i in range(len(par)):
                if i:
                    self.play(ring.animate.move_to(VGroup(row[i], par[i])), run_time=0.12)
                self.play(FadeIn(par[i], shift=DOWN * 0.1), run_time=0.12)
            self.play(FadeOut(ring))
            vo.wait_until("c")
            self.play(Create(ans), FadeIn(r2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 17: \ Reasoning", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"thinking out loud, \ learning from a checker, \ thinking longer", font_size=30, color=C.BITS)
        sub.next_to(title, DOWN, buff=0.25)
        smap = series_map(current=17, done=16).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "This part is about reasoning: why writing a chain of thought adds computation, how models learn to "
            "reason from nothing but a checker of answers, <bookmark mark='a'/> and what you get by letting them think "
            "longer."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()

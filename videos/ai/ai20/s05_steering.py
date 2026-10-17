from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import FEAT, MONO, context_line, load

PUSH = C.SURPRISE


def text_block(t: str, width_chars=56, font_size=18, color=GREY_A, hot="\"'!?") -> VGroup:
    """Generated text, wrapped into at most three lines, with the marks of speech lit."""
    t = " ".join(t.split())
    lines = [t[i:i + width_chars] for i in range(0, min(len(t), 3 * width_chars), width_chars)]
    return VGroup(*[Text(ln, font=MONO, font_size=font_size, color=color, t2c={h: PUSH for h in hot}) for ln in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.12)


class Steering(VoiceoverScene):
    def construct(self):
        self.card()
        self.dial()
        self.faithful()

    def card(self):
        card = chapter_card(4, r"Reaching in", r"Can we change what the model thinks?", part=20)
        with self.voiceover("Chapter four. Reaching in."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def dial(self):
        st = load("steering")
        alphas = [float(a) for a in st["alphas"]]
        texts, speech = st["texts"], st["speech"]
        feat = int(st["feature"])
        ctx = VGroup(*[context_line(c, 5.2, font_size=16, color=FEAT) for c in st["contexts"][:3]]).arrange(DOWN, buff=0.08)
        ch = label(rf"feature {feat}: \ where it fires hardest", font_size=20, color=FEAT).next_to(ctx, UP, buff=0.12).align_to(ctx, LEFT)
        fbox = VGroup(ch, ctx).to_corner(UL, buff=0.35)
        colors = {r"\alpha": PUSH, r"d_k": FEAT}
        f = cmath(r"h \;\leftarrow\; h + ", r"\alpha", r"\, ", r"d_k", colors=colors, font_size=40).to_corner(UR, buff=0.5).shift(LEFT * 0.4)
        fl = label(r"add the feature's direction \\ at every character, \ while it writes", font_size=20, color=GREY_A)
        fl.next_to(f, DOWN, buff=0.15)
        prompt = str(st["prompt"])
        pr = Text(prompt, font="DejaVu Serif", font_size=20, color=GREY_B).move_to([0, 0.75, 0])
        if pr.width > 12.5:
            pr.scale_to_fit_width(12.5)
        rows = VGroup()
        for a in alphas:
            key = f"{a:g}"
            tb = text_block(texts[key][0])
            al = MathTex(rf"\alpha = {a:g}", font_size=30, color=PUSH)
            q = label(rf"${speech[key]:.1f}$ marks of speech \\ per $160$ characters", font_size=18, color=PUSH)
            rows.add(VGroup(al, tb, q))
        for i, r_ in enumerate(rows):
            y = -0.15 - i * 1.25
            r_[0].move_to([-5.9, y, 0])
            r_[1].move_to([-0.2, y, 0])
            r_[2].move_to([5.5, y, 0])
        hl = label(r"lit: \ quotes, \ apostrophes, \ ! \ and \ ?", font_size=18, color=PUSH)
        tag = note(r"three samples at each strength; \ one shown").to_corner(DR, buff=0.2)
        hl.next_to(tag, UP, buff=0.1).align_to(tag, RIGHT)
        q0, q1 = float(speech[f"{alphas[0]:g}"]), float(speech[f"{alphas[-1]:g}"])
        with self.voiceover(
            "If a feature is a direction, we can push on it. <bookmark mark='a'/> Take the feature that fires on "
            "quotation marks. <bookmark mark='b'/> While the model writes, add alpha times its direction to the "
            "vector at every character. <bookmark mark='c'/> With no push, the model's own continuation. "
            f"<bookmark mark='d'/> Turn the dial up, and the writing turns into talk: quote marks, apostrophes, "
            f"exclamations and questions, from {q0:.1f} to {q1:.1f} per hundred and sixty characters. The model now "
            "thinks it's inside someone's speech. We didn't train anything or change a weight; we moved one direction. "
            "Anthropic did the same to Claude with a Golden Gate Bridge feature, and for a day it would bring every "
            "conversation round to the bridge."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(fbox))
            vo.wait_until("b")
            self.play(Write(f), FadeIn(fl), FadeIn(pr))
            vo.wait_until("c")
            self.play(FadeIn(rows[0][0]), FadeIn(rows[0][1], lag_ratio=0.02), FadeIn(rows[0][2]), FadeIn(tag), FadeIn(hl), run_time=1.5)
            vo.wait_until("d")
            for r_ in rows[1:]:
                self.play(FadeIn(r_[0]), FadeIn(r_[1], lag_ratio=0.02), FadeIn(r_[2]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def faithful(self):
        head = label(r"Is the written chain of thought what the model really did?", font_size=32).to_edge(UP, buff=0.5)
        setup = label(r"slip a hint into the question; \ the model uses it to change its answer. \\ "
                      r"Does its chain of thought say so?", font_size=24, color=GREY_A).next_to(head, DOWN, buff=0.35)
        vals = [("Claude 3.7 Sonnet", 0.25, C.BITS), ("DeepSeek-R1", 0.39, C.TRUE_P)]
        W = 8.0
        bars = VGroup()
        for i, (nm, v, col) in enumerate(vals):
            y = -0.4 - i * 1.1
            frame = Rectangle(width=W, height=0.55, stroke_color=GREY_C, stroke_width=1.2).move_to([0.8, y, 0])
            bar = Rectangle(width=W * v, height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.85).align_to(frame, LEFT).set_y(y)
            n_ = label(nm, font_size=24, color=col).next_to(frame, LEFT, buff=0.3)
            p_ = label(rf"${100 * v:.0f}\%$", font_size=26, color=col).next_to(bar, RIGHT, buff=0.15)
            bars.add(VGroup(frame, bar, n_, p_))
        cap = label(r"how often the chain of thought mentions the hint it used", font_size=22, color=GREY_A).next_to(bars, DOWN, buff=0.3)
        tag = note(r"published results, not measured here").to_corner(DR, buff=0.25)
        cite_ = cite(r"Y.~Chen et al.\ (Anthropic), \textit{Reasoning Models Don't Always Say What They Think} (2025)", corner=DL)
        with self.voiceover(
            "This matters for part seventeen's reasoning models. Their chains of thought look like a window into "
            "their thinking. But are they? <bookmark mark='a'/> One test: slip a hint into the question, and see if "
            "the model uses it, then check whether its chain of thought admits it. <bookmark mark='b'/> Most of the "
            "time, it doesn't: a quarter of the time for Claude 3.7 Sonnet, under two fifths for DeepSeek-R1. The "
            "written chain is not always the real computation. That's why reading the inside directly, with the "
            "tools of this part, matters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(setup))
            vo.wait_until("b")
            for b_ in bars:
                self.play(Create(b_[0]), FadeIn(b_[2]), GrowFromEdge(b_[1], LEFT), FadeIn(b_[3]))
            self.play(FadeIn(cap), FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

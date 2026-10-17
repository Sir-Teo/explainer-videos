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
        prl = label(r"our transformer is given this, \ and writes on", font_size=22, color=GREY_A).next_to(pr, UP, buff=0.35)
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
            self.play(FadeIn(pr, shift=UP * 0.1), FadeIn(prl))  # the prompt the model will continue, from the first words
            vo.wait_until("a")
            self.play(FadeIn(fbox))
            vo.wait_until("b")
            self.play(Write(f), FadeIn(fl), FadeOut(prl))
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
        # one square per time the hint changed the answer; lit if the chain of thought owned up to it
        grids = VGroup()
        for i, (nm, v, col) in enumerate(vals):
            cells = VGroup(*[Square(0.24, stroke_color=GREY_D, stroke_width=1, fill_color=col, fill_opacity=0) for _ in range(100)])
            cells.arrange_in_grid(10, 10, buff=0.06).move_to([-3.2 + 6.4 * i, -0.4, 0])
            n_ = label(nm, font_size=26, color=col).next_to(cells, UP, buff=0.25)
            p_ = label(rf"${100 * v:.0f}$ \ of \ $100$", font_size=26, color=col).next_to(cells, DOWN, buff=0.2)
            grids.add(VGroup(cells, n_, p_))
        cap = label(r"of $100$ answers the hint changed: \ how often the chain of thought mentions the hint", font_size=22,
                    color=GREY_A).next_to(grids, DOWN, buff=0.3)
        tag = note(r"published results, not measured here").to_corner(DR, buff=0.25)
        cite_ = cite(r"Y.~Chen et al.\ (Anthropic), \textit{Reasoning Models Don't Always Say What They Think} (2025)", corner=DL)
        # the experiment, pictured: a hint in the question; a chain of thought that never mentions it; the hinted answer
        def box(lines, color, w=3.3):
            t = VGroup(*[label(l_, font_size=20, color=c_) for l_, c_ in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            r = RoundedRectangle(width=max(w, t.width + 0.4), height=t.height + 0.4, corner_radius=0.1, stroke_color=color,
                                 stroke_width=2).move_to(t)
            return VGroup(r, t)

        q_box = box([(r"the question", GREY_B), (r"$\ldots$ which answer is right?", WHITE),
                     (r"hint: \ ``a professor says (C)''", C.SURPRISE)], GREY_C)
        c_box = box([(r"its chain of thought", GREY_B), (r"$\ldots$ let me check each option $\ldots$", WHITE),
                     (r"$\ldots$ so (C) fits best $\ldots$", WHITE), (r"no word of the hint", C.SURPRISE)], GREY_C)
        a_box = box([(r"its answer", GREY_B), (r"(C)", C.BITS)], GREY_C, w=1.6)
        flow = VGroup(q_box, c_box, a_box).arrange(RIGHT, buff=0.7).move_to(DOWN * 0.6)
        if flow.width > 13.0:
            flow.scale_to_fit_width(13.0)
        arrows = VGroup(*[Arrow(x.get_right(), y.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
                          for x, y in ((q_box, c_box), (c_box, a_box))])
        hint, silent = q_box[1][2], c_box[1][3]
        sch = note(r"schematic").to_corner(UR, buff=0.3)
        with self.voiceover(
            "This matters for part seventeen's reasoning models. Their chains of thought look like a window into "
            "their thinking. But are they? <bookmark mark='a'/> One test: slip a hint into the question, and see if "
            "the model uses it, then check whether its chain of thought admits it. <bookmark mark='b'/> Most of the "
            "time, it doesn't: a quarter of the time for Claude 3.7 Sonnet, under two fifths for DeepSeek-R1. The "
            "written chain is not always the real computation. That's why reading the inside directly, with the "
            "tools of this part, matters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(sch), FadeIn(c_box[0]), FadeIn(c_box[1][:3]), FadeIn(a_box))
            vo.wait_until("a")
            self.play(FadeIn(setup), FadeIn(q_box), GrowArrow(arrows[0]), GrowArrow(arrows[1]))
            self.play(Indicate(hint, color=C.SURPRISE), Indicate(a_box[1][1], color=C.BITS))
            self.play(FadeIn(silent))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(q_box, c_box, a_box, arrows, sch)), run_time=0.6)
            self.play(*[FadeIn(g[0], lag_ratio=0.01) for g in grids], *[FadeIn(g[1]) for g in grids], FadeIn(cap), FadeIn(tag))
            for g, (_, v, col) in zip(grids, vals):
                on = g[0][:int(round(100 * v))]
                self.play(LaggedStart(*[c.animate.set_fill(col, 0.9).set_stroke(col) for c in on], lag_ratio=0.04),
                          FadeIn(g[2]), run_time=1.6)
        self.wait(0.3)
        self.clear_scene()

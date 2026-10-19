from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import load

LO = 0.7  # the bars start at 70% right


class Board(VoiceoverScene):
    def construct(self):
        self.card()
        self.board()

    def card(self):
        card = chapter_card(8, r"The contest", r"Which method wins?", part=6)
        with self.voiceover("Chapter eight. The contest."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def board(self):
        b = load("board")
        p = load("pages")
        n_te = int(np.asarray(p["test"], bool).sum())
        rows = b["rows"]
        W = 2.4  # bar length for 100%
        col2, col70 = -0.6, 3.1
        head = VGroup(label(r"$2$ rates", font_size=28, color=GREY_A).move_to([col2 + W / 2, 2.85, 0]),
                      label(r"all $70$ rates", font_size=28, color=GREY_A).move_to([col70 + W / 2 - 0.4, 2.85, 0]))
        title = label(rf"Right answers on ${n_te}$ held-out pages", font_size=34).to_edge(UP, buff=0.3)
        lines = VGroup()
        acc2 = [r[1] for r in rows if r[1] is not None]
        for k, (name, a2, a70) in enumerate(rows):
            yv = 2.2 - 0.58 * k
            g = VGroup(label(name, font_size=26, color=WHITE).move_to([-0.85, yv, 0], aligned_edge=RIGHT))
            for a, x0, col in ((a2, col2, C.TRUE_P), (a70, col70, C.BITS)):
                if a is None:
                    g.add(VGroup(MathTex(r"\text{---}", font_size=24, color=GREY_D).move_to([x0 + 0.3, yv, 0])))
                    continue
                L = W * (a - LO) / (1 - LO)
                g.add(VGroup(Rectangle(width=max(L, 0.02), height=0.32, stroke_width=0, fill_color=col, fill_opacity=0.85)
                             .move_to([x0 + L / 2, yv, 0]),
                             MathTex(rf"{100 * a:.1f}\%", font_size=24, color=col).move_to([x0 + L + 0.55, yv, 0])))
            lines.add(g)
        scale = label(r"bars start at $70\%$", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25).to_edge(RIGHT, buff=0.4)
        lo2, hi2 = min(acc2), max(acc2)
        best70 = max(r[2] for r in rows if r[2] is not None)
        lesson = label(r"the description of the data mattered more than the method", font_size=30, color=C.BITS)
        lesson.to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Here's the whole contest, scored on the same held-out pages. <bookmark mark='a'/> With two rates, every "
            f"method lands between {100 * lo2:.0f} and {100 * hi2:.0f} percent. The two numbers simply don't hold "
            f"more. <bookmark mark='b'/> With all seventy, the best get {round(best70 * n_te)} of {n_te} right, and "
            "the plain straight line, logistic regression, is among them. <bookmark mark='c'/> That's the lesson of "
            "classical machine learning: the description of the data mattered more than the cleverness of the "
            "method, and choosing seventy small words did most of the work. Deep learning changes that. It learns "
            "the description too."
        ) as vo:
            self.play(FadeIn(title), FadeIn(head), FadeIn(scale))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(g[0], g[1])) for g in lines], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g[2]) for g in lines], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(lesson))
        self.wait(0.3)
        self.clear_scene()

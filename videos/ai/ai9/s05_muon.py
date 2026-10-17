from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import OPT_COLORS, OPT_NAMES, curve, load

MU = OPT_COLORS["muon"]


class Muon(VoiceoverScene):
    def construct(self):
        self.card()
        self.orthogonalize()
        self.result()

    def card(self):
        card = chapter_card(4, r"Muon", r"What if every direction got the same push?", part=9)
        with self.voiceover("Chapter four. Muon."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def orthogonalize(self):
        m = load("muon")
        before, after = np.asarray(m["before"]), np.asarray(m["after"])
        n = len(before)
        ax = Axes(x_range=[0, n, 64], y_range=[0, 1.4, 0.5], x_length=7.6, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-1.8, -0.8, 0])
        xl = label(r"the gradient's $256$ singular values, \ largest first", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        bars_b = VGroup(*[Line(ax.c2p(i + 0.5, 0), ax.c2p(i + 0.5, float(v)), color=GREY_B, stroke_width=2)
                          for i, v in enumerate(before)])
        bars_a = VGroup(*[Line(ax.c2p(i + 0.5, 0), ax.c2p(i + 0.5, float(min(v, 1.4))), color=MU, stroke_width=2)
                          for i, v in enumerate(after)])
        colors = {r"U": GREY_A, r"V^{\top}": GREY_A, r"\Sigma": GREY_B}
        svd = cmath(r"G", "=", r"U", r"\Sigma", r"V^{\top}", colors=colors, font_size=42).move_to([4.2, 2.4, 0])
        orth = cmath(r"\operatorname{orth}(G)", "=", r"U", r"V^{\top}", colors=colors, font_size=42).next_to(svd, DOWN, buff=0.4)
        on = label(r"Part 2's SVD, \ with every \\ singular value set to $1$", font_size=24, color=MU).next_to(orth, DOWN, buff=0.2)
        ns = cmath(r"X \leftarrow aX + b\,(XX^{\top})X + c\,(XX^{\top})^2 X", font_size=30).next_to(on, DOWN, buff=0.5)
        nsl = label(r"Newton--Schulz: \ five matrix products, \ no SVD needed", font_size=22, color=GREY_A)
        nsl.next_to(ns, DOWN, buff=0.15)
        cite_ = cite(r"K.~Jordan et al., \textit{Muon} (2024); \ J.~Liu et al., \textit{Muon is Scalable for LLM Training} (2025)",
                     corner=DR)
        with self.voiceover(
            "Adam treats every weight separately. But the weights of a layer form a matrix, and a matrix has "
            "structure: part two's singular values. <bookmark mark='a'/> Here's a real gradient matrix from the "
            "character model. A few directions dominate; most are tiny. A step along it mostly pushes the few big "
            "directions further. <bookmark mark='b'/> Muon, from 2024, takes the gradient's singular value "
            "decomposition and sets every singular value to one: the same push in every direction. "
            "<bookmark mark='c'/> It doesn't even compute the SVD. Five rounds of a matrix polynomial, Newton–Schulz, "
            "do it approximately and fast."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars_b], lag_ratio=0.004), Write(svd), run_time=2.0)
            vo.wait_until("b")
            self.play(ReplacementTransform(bars_b, bars_a), Write(orth), FadeIn(on), run_time=2.0)
            vo.wait_until("c")
            self.play(Write(ns), FadeIn(nsl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        o = load("optim")
        names = ["sgd", "adamw", "muon"]
        allc = [np.asarray(o[n]) for n in o["names"]]
        top = float(max(c[1, 1] for c in allc)) + 0.2
        bot = float(min(c[-1, 1] for c in allc)) - 0.2
        steps = float(allc[0][-1, 0])
        ax = Axes(x_range=[0, steps, 500], y_range=[bot, top, 0.5], x_length=8.4, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.5, 0])
        xl = label(r"training steps", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yn = label(r"bits per character on held-out text", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        finals = o["finals"]
        rows = VGroup(*[label(rf"{OPT_NAMES[n]}: \ ${finals[n]:.2f}$", font_size=26, color=OPT_COLORS[n]) for n in names])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.7, 1.0, 0])
        lines = [curve(ax, np.asarray(o[n])[1:, 0], np.clip(np.asarray(o[n])[1:, 1], bot, top), OPT_COLORS[n], 3.5)
                 for n in names]
        better = finals["muon"] < finals["adamw"]
        with self.voiceover(
            "On the same character model, with Muon on the hidden matrices and AdamW on the rest: "
            + (f"<bookmark mark='a'/> it reaches {finals['muon']:.2f} bits, ahead of AdamW's {finals['adamw']:.2f}. "
               if better else
               f"<bookmark mark='a'/> it reaches {finals['muon']:.2f} bits, close to AdamW's {finals['adamw']:.2f} on "
               "this small model. ")
            + "Muon has since been scaled up: Moonshot AI reported that it needs about half the compute of AdamW, "
            "and used a version of it to train Kimi K2."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yn), Create(lines[0]), Create(lines[1]), FadeIn(rows[:2]))
            vo.wait_until("a")
            self.play(Create(lines[2]), FadeIn(rows[2]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

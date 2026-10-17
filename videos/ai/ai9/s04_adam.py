from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import OPT_COLORS, OPT_NAMES, curve, load


class Adam(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.race()

    def card(self):
        card = chapter_card(3, r"Momentum and Adam", r"How should each step be shaped?", part=9, lit=(2014,))
        with self.voiceover("Chapter three. Momentum, and Adam."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rules(self):
        cm = {r"m_t": OPT_COLORS["momentum"], r"v_t": OPT_COLORS["adam"], r"g_t": WHITE}
        mom = VGroup(label(r"momentum: \ a running average of gradients", font_size=28, color=OPT_COLORS["momentum"]),
                     cmath(r"m_t", "=", r"\beta\, m_{t-1} + g_t", r",\quad", r"\theta_t = \theta_{t-1} - \eta\, m_t",
                           colors=cm, font_size=36))
        adam = VGroup(label(r"Adam: \ also a running average of squared gradients", font_size=28, color=OPT_COLORS["adam"]),
                      cmath(r"v_t", "=", r"\beta_2\, v_{t-1} + (1 - \beta_2)\, g_t^2", colors=cm, font_size=36),
                      cmath(r"\theta_t = \theta_{t-1} - \eta\,", r"\frac{m_t}{\sqrt{v_t} + \epsilon}", colors=cm,
                            font_size=40))
        adamw = VGroup(label(r"AdamW: \ shrink the weights directly", font_size=28, color=OPT_COLORS["adamw"]),
                       cmath(r"\theta_t \;\mathrel{-}=\; \eta\,\lambda\,\theta_{t-1}", font_size=36))
        for g in (mom, adam, adamw):
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        VGroup(mom, adam, adamw).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(LEFT * 1.6)
        note_ = label(r"each weight gets its own step size: \\ big where gradients are small, \\ small where they're big",
                      font_size=24, color=GREY_A).next_to(adam, RIGHT, buff=0.5)
        keep_in_frame(note_)
        cite_ = cite(r"B.~Polyak (1964); \ D.~Kingma \& J.~Ba (2014); \ I.~Loshchilov \& F.~Hutter (2017)", corner=DR)
        with self.voiceover(
            "Momentum keeps a running average of recent gradients and steps along that. Zigzags cancel; steady "
            "directions add up. <bookmark mark='a'/> Adam, from 2014, also tracks the average squared gradient for "
            "every weight, and divides by its square root. Each weight gets its own step size: large where the "
            "gradients are small, small where they're large. <bookmark mark='b'/> AdamW adds one fix: it shrinks "
            "the weights directly, separately from the gradient. That's the optimizer that trained most of today's "
            "language models."
        ) as vo:
            self.play(FadeIn(mom), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(adam), FadeIn(note_))
            vo.wait_until("b")
            self.play(FadeIn(adamw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        o = load("optim")
        names = [n for n in o["names"] if n != "muon"]
        allc = [np.asarray(o[n]) for n in o["names"]]
        top = float(max(c[1, 1] for c in allc)) + 0.2
        bot = float(min(c[-1, 1] for c in allc)) - 0.2
        steps = float(allc[0][-1, 0])
        ax = Axes(x_range=[0, steps, 500], y_range=[bot, top, 0.5], x_length=8.4, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.5, 0])
        yl = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in np.arange(np.ceil(bot * 2) / 2, top, 0.5)])
        xl = label(r"training steps", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yn = label(r"bits per character on held-out text", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        lines = {n: curve(ax, np.asarray(o[n])[1:, 0], np.clip(np.asarray(o[n])[1:, 1], bot, top), OPT_COLORS[n], 3.5)
                 for n in names}
        finals = o["finals"]
        rows = VGroup(*[label(rf"{OPT_NAMES[n]}: \ ${finals[n]:.2f}$", font_size=26, color=OPT_COLORS[n]) for n in names])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.7, 1.0, 0])
        head = label(r"A small character model \\ on Part 1's books", font_size=26, color=GREY_A).next_to(rows, UP, buff=0.4)
        head.align_to(rows, LEFT)
        keep_in_frame(VGroup(head, rows))
        with self.voiceover(
            "Here they are on a real task: a small character model, like part eight's, trained on the books for "
            "two and a half thousand steps, each optimizer at a good learning rate. <bookmark mark='a'/> Plain SGD "
            "is slowest. Momentum helps. <bookmark mark='b'/> Adam and AdamW are far ahead after the same number of "
            "steps."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn), FadeIn(head))
            vo.wait_until("a")
            for n, r_ in zip(names[:2], rows[:2]):
                self.play(Create(lines[n]), FadeIn(r_), run_time=1.6)
            vo.wait_until("b")
            for n, r_ in zip(names[2:], rows[2:]):
                self.play(Create(lines[n]), FadeIn(r_), run_time=1.6)
        self.wait(0.3)
        self.clear_scene()

from __future__ import annotations

import unicodedata

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import OPT_COLORS, OPT_NAMES, curve, load


class Adam(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.race()
        self.reading()

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
        legend = VGroup(label(r"$m_t$: \ the running average direction", font_size=20, color=OPT_COLORS["momentum"]),
                        label(r"$v_t$: \ the running average squared size", font_size=20, color=OPT_COLORS["adam"]),
                        label(r"$\beta$: \ how long the memory lasts", font_size=20, color=GREY_A),
                        label(r"$\epsilon$: \ a tiny number, \ so we never divide by zero", font_size=20, color=GREY_A))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        syms = gloss(r"the symbols", r"in the formulas on the left:", legend, corner=UR, width=5.2, color=OPT_COLORS["adam"])
        with self.voiceover(
            "Momentum keeps a running average of recent gradients, m, the direction they've been pointing lately, "
            "and steps along that; beta sets how long that memory lasts. Zigzags cancel; steady "
            "directions add up. <bookmark mark='a'/> Adam, from 2014, also tracks the average squared gradient for "
            "every weight, v, its typical size, and divides by its square root, plus a tiny epsilon so it never "
            "divides by zero. Each weight gets its own step size: large where the "
            "gradients are small, small where they're large. <bookmark mark='b'/> AdamW adds one fix: it shrinks "
            "the weights directly, separately from the gradient. That's the optimizer that trained most of today's "
            "language models."
        ) as vo:
            self.play(FadeIn(mom), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(adam), FadeIn(note_), FadeIn(syms))
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

    # ------------------------------------------------------------------
    def reading(self):
        """What the race's numbers read like: SGD and AdamW continuing the same prompt at checkpoints."""
        w, o = load("writing"), load("optim")
        steps = [int(s_) for s_ in w["steps"]]

        def clean(t):
            t = "".join(ch for ch in t if unicodedata.category(ch) not in ("Cc", "Cf", "Mn") or ch == "\n")
            return t.replace("\n", "↵")

        def block(name, k):
            """The prompt in white, then the model's continuation, in two lines of a monospaced font."""
            t = clean(w[f"text_{name}"][k])
            kw = dict(font="DejaVu Sans Mono", font_size=24)
            p_ = Text(w["prompt"], color=WHITE, **kw)
            cw = Text("MMMMMMMMMM", **kw).width / 10  # one character's width
            n1 = (len(w["prompt"]) + len(t)) // 2 - len(w["prompt"])
            n1 = t.rfind(" ", 0, n1 + 1) if t.rfind(" ", 0, n1 + 1) > n1 - 10 else n1  # break at a space if one is near
            l1 = Text(t[:n1].strip(), color=OPT_COLORS[name], **kw)
            l1.next_to(p_, RIGHT, buff=cw * (1 + len(t[:n1]) - len(t[:n1].lstrip())) - cw)
            l1.align_to(p_, DOWN) if not any(ch in "gjpqy," for ch in t[:n1]) else l1.match_y(p_)
            l2 = Text(t[n1:].strip(), color=OPT_COLORS[name], **kw).next_to(VGroup(p_, l1), DOWN, buff=0.16).align_to(p_, LEFT)
            l2.shift(RIGHT * cw * (len(t[n1:]) - len(t[n1:].lstrip())))
            return VGroup(p_, l1, l2)

        heads = {n: label(rf"{OPT_NAMES[n]}", font_size=26, color=OPT_COLORS[n]) for n in ("sgd", "adamw")}
        ys = {"sgd": 2.1, "adamw": 0.45}

        def place(name, k):
            g = block(name, k)
            return g.shift([-3.9 - g[0].get_left()[0], ys[name] - g.get_center()[1], 0])

        for n in heads:
            heads[n].move_to([-5.6, ys[n], 0])
        t = ValueTracker(0)
        bits = {n: always_redraw(lambda n=n: MathTex(
            rf"{float(np.interp(t.get_value(), steps, w[f'bits_{n}'])):.2f}\ \text{{bits/char}}", font_size=24,
            color=OPT_COLORS[n]).next_to(heads[n], DOWN, buff=0.12)) for n in heads}
        prompt = label(rf"both continue ``{w['prompt']}'' \ with the same random draws", font_size=22, color=GREY_A)
        prompt.to_edge(UP, buff=0.25)
        # the race again, small, with a marker at each checkpoint
        top = float(np.asarray(o["sgd"])[1, 1]) + 0.2
        ax = CornerAxes(x_range=[0, steps[-1], 500], y_range=[2.4, top, 0.5], x_length=7.0, y_length=2.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([0.6, -2.4, 0])
        lines = VGroup(*[curve(ax, np.asarray(o[n])[1:, 0], np.asarray(o[n])[1:, 1], OPT_COLORS[n], 3) for n in heads])
        vline = always_redraw(lambda: DashedLine(ax.c2p(t.get_value(), 2.4), ax.c2p(t.get_value(), top), color=GREY_B,
                                                 stroke_width=2))
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}".replace(",", "{,}"), font_size=28,
                                            color=WHITE).next_to(ax, LEFT, buff=0.5))
        xl = label(r"bits per character on held-out text, \ as they train", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.1)
        cur = {n: place(n, 0) for n in heads}
        b = {k: w["bits_sgd"][k] for k in range(len(steps))}
        with self.voiceover(
            "What does a number like that read like? Here both models continue the same few words, with the same "
            "random draws, at checkpoints during training. <bookmark mark='a'/> Before any training, every character "
            f"of the books is equally likely: {b[0]:.1f} bits each, and the text is noise from the whole alphabet. "
            f"<bookmark mark='b'/> After {steps[1]} steps they have spaces, and short words like 'the', 'to' "
            f"and 'and'. <bookmark mark='c'/> By step {steps[3]:,}, most of what they write is word-shaped, and "
            f"<bookmark mark='d'/> by the end, at about {w['bits_adamw'][-1]:.1f} bits, there's punctuation, a line "
            "break, even the start of dialogue. AdamW is ahead at every checkpoint. Since both draw the same random "
            "numbers, their texts rhyme; the difference is how far each one has come down the hill."
        ) as vo:
            self.play(FadeIn(prompt), *[FadeIn(h) for h in heads.values()], Create(ax), FadeIn(xl))
            self.add(*bits.values(), vline, cnt)
            self.play(Create(lines), run_time=1.2)
            vo.wait_until("a")
            self.play(*[FadeIn(cur[n][0]) for n in heads])
            self.play(*[AddTextLetterByLetter(line_) for n in heads for line_ in cur[n][1:]], run_time=1.5)
            for k, mk in zip(range(1, len(steps)), ("b", None, "c", "d")):
                if mk:
                    vo.wait_until(mk)
                nxt = {n: place(n, k) for n in heads}
                self.play(*[FadeTransform(cur[n], nxt[n]) for n in heads], t.animate.set_value(steps[k]), run_time=1.4)
                cur = nxt
        self.wait(0.5)
        self.remove(*bits.values(), vline, cnt)
        self.clear_scene()

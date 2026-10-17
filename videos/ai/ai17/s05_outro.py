from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import CHAIN, DIRECT, RIGHT_C, WRONG_C, bit_row, chip, curve, hit_image, load, mark
from videos.ai.ai18.compute import load as load18


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

        p, r, s = load("parity"), load("rl"), load("sampling")
        bits = np.random.default_rng(17).integers(0, 2, 8)
        b1 = bit_row(bits, size=0.3, buff=0.04, font_size=16)
        b2 = VGroup(*[chip(str(int(v)), size=0.3, color=CHAIN, font_size=16) for v in np.cumsum(bits) % 2]).arrange(RIGHT, buff=0.04)
        par = VGroup(b1, b2).arrange(DOWN, buff=0.12)
        L, T = 3, 5
        at = lambda l, t: np.array([t * 0.55, l * 0.45, 0])
        nodes = VGroup(*[Dot(at(l, t), radius=0.04, color=GREY_B) for l in range(L + 1) for t in range(T)])
        sn = []
        for t in range(T):
            sn += [at(0, t), at(L, t)]
        snake = VGroup(nodes, VMobject(stroke_width=3, color=C.BITS).set_points_as_corners(sn))
        ns = [int(n) for n in p["ns"]]
        bars = VGroup()
        for i, n in enumerate(ns):
            for j, (key, col) in enumerate((("direct", DIRECT), ("cot", CHAIN))):
                v = float(p[f"acc_{key}{n}"])
                bars.add(Rectangle(width=0.3, height=max(1.6 * v, 0.01), stroke_width=0, fill_color=col, fill_opacity=0.9)
                         .move_to([i * 0.9 + j * 0.34, 0.8 * v, 0]))
        grpo = MathTex(r"A_i = \frac{r_i - \bar r}{\sigma_r}", font_size=40, color=C.BITS)
        cv = np.asarray(r["curve"])
        ax = Axes(x_range=[0, float(cv[:, 0].max()), 100], y_range=[0, 1, 0.5], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        climb = VGroup(ax, curve(ax, cv[:, 0], cv[:, 1], CHAIN, 3))
        V, truth = np.asarray(r["vals_before"]), np.asarray(r["truth"])
        R = V == truth[:, None]
        img = hit_image(R[np.argsort(-R.sum(1), kind="stable")], 1.8, 1.8)
        ks = [math.log2(int(k)) for k in s["ks"]]
        bx = Axes(x_range=[0, ks[-1], 1], y_range=[0, 1, 0.5], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        tries = VGroup(bx, curve(bx, ks, [float(v) for v in s["passk"]], C.BITS, 3), curve(bx, ks, [float(v) for v in s["majority"]], C.TRUE_P, 3))
        boxes = VGroup(*[RoundedRectangle(width=0.45, height=0.3, corner_radius=0.05, stroke_color=GREY_B, stroke_width=1.2)
                         for _ in range(5)]).arrange(RIGHT, buff=0.12)
        pm = VGroup(*[mark(k != 2, 22).next_to(b_, DOWN, buff=0.08) for k, b_ in enumerate(boxes)])
        om = mark(True, 22).next_to(boxes[-1], UP, buff=0.08)
        proc = VGroup(boxes, pm, om)
        out = [
            (par, r"thinking out loud", CHAIN),
            (snake, r"$L(k+1)$ steps in a row", C.BITS),
            (bars, r"parity: \ at once vs.\ chain", CHAIN),
            (grpo, r"better than its group?", C.BITS),
            (climb, r"learning from a checker", CHAIN),
            (img, r"$200$ questions, \ $32$ tries", RIGHT_C),
            (tries, r"pass@$k$ and the vote", C.BITS),
            (proc, r"outcome or process", WRONG_C),
        ]
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = frame(cap, col)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(r"Part 17, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Writing out its steps lets a fixed-depth model compute for longer: L layers, once per "
            "token. That's how our two-layer model learned sixteen-bit parity. Reinforcement learning from a checker, "
            "comparing each answer with its group, taught a model to add more reliably than practice alone. And at "
            "answer time, more tries buy more right answers, as long as something can tell which one is right."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"many steps in a row", [18]),
            (r"every token of thought costs time", [19]),
            (r"can we trust the written chain?", [20]),
        ], font_size=26)
        with self.voiceover(
            "Reasoning over many steps is what agents do, in part eighteen. Every token of thought costs time to "
            "write, which is part nineteen. And whether the chain a model writes is really how it got its answer is "
            "a question for the last part."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        b = load18("belief")
        B = np.asarray(b["beliefs"])
        head = label(r"Next: \ Part 18, \ Agents and Worlds", font_size=40).to_edge(UP, buff=0.4)

        def bars(v):
            return VGroup(*[Rectangle(width=0.2, height=max(2.6 * x / B.max(), 0.01), stroke_width=0, fill_color=C.TRUE_P,
                                      fill_opacity=0.9) for x in v]).arrange(RIGHT, buff=0.04, aligned_edge=DOWN).move_to(DOWN * 0.4)

        b0 = bars(B[0])
        doors = VGroup(*[Square(0.2, stroke_width=0, fill_color=GREY_C, fill_opacity=0.8).next_to(b0[int(d)], DOWN, buff=0.15)
                         for d in b["doors"]])
        corridor = Line(b0.get_corner(DL) + DOWN * 0.15, b0.get_corner(DR) + DOWN * 0.15, color=GREY_D, stroke_width=2)
        cap = label(r"where am I? \ a belief, \ sharpened step by step", font_size=24, color=GREY_A).next_to(doors, DOWN, buff=0.35)
        with self.voiceover(
            "Next time: agents. A robot that can't see where it is keeps a belief over every place it might be, "
            "<bookmark mark='a'/> and sharpens it with each step and each glimpse of a door."
        ) as vo:
            self.play(FadeIn(head), FadeIn(b0), Create(corridor), FadeIn(doors), FadeIn(cap))
            vo.wait_until("a")
            for k in (len(B) // 4, len(B) // 2, len(B) - 1):
                self.play(Transform(b0, bars(B[k]).align_to(b0, DOWN)), run_time=0.9)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [r"R.~S.~Sutton \& A.~G.~Barto, \textit{Reinforcement Learning: An Introduction} (2nd ed., 2018)"]
        papers = [
            r"J.~Wei et al., \textit{Chain-of-Thought Prompting Elicits Reasoning} (2022); \ W.~Merrill \& A.~Sabharwal (2024)",
            r"Z.~Shao et al., \textit{DeepSeekMath} (GRPO, 2024); \ DeepSeek-AI, \textit{DeepSeek-R1} (2025)",
            r"H.~Lightman et al., \textit{Let's Verify Step by Step} (2023); \ M.~Chen et al., \textit{Codex} (pass@$k$, 2021)",
            r"X.~Wang et al., \textit{Self-Consistency} (2023); \ C.~Snell et al., \textit{Scaling LLM Test-Time Compute} (2024)",
        ]
        card = reference_card(books, papers)
        data = note(r"Every number here is computed and checked: \ tiny transformers trained on this computer; \ "
                    r"illustrations are labeled.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover("Thanks for watching, and see you in part eighteen."):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))

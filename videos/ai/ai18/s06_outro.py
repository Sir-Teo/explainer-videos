from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai18.compute import load
from videos.ai.ai18.s04_world import gray


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

        def bars(v, col):
            v = np.asarray(v, float)
            return VGroup(*[Rectangle(width=0.06, height=max(1.6 * x / v.max(), 0.01), stroke_width=0, fill_color=col,
                                      fill_opacity=0.9) for x in v]).arrange(RIGHT, buff=0.01, aligned_edge=DOWN)

        b, h, w = load("belief"), load("horizon"), load("world")
        B = np.asarray(b["beliefs"])
        ns = np.log10(np.asarray(h["ns"], float))
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 1, 0.5], x_length=TW, y_length=TH, tips=False, axis_config={"stroke_width": 0})
        out = [
            (bars(B[0], C.TRUE_P), r"not knowing where", C.TRUE_P),
            (bars(B[-1], C.TRUE_P), r"a sharp belief", C.TRUE_P),
            (VGroup(*[VMobject(color=c_, stroke_width=3).set_points_smoothly([ax.c2p(x, y) for x, y in zip(ns, np.asarray(h[f"succ{p:g}"]))])
                      for p, c_ in zip(h["ps"], (C.SURPRISE, C.BITS, C.INTERVAL))]), r"$p^n$", C.BITS),
            (MathTex(r"n_{1/2} \approx \frac{0.69}{1-p}", font_size=44, color=C.BITS), r"long horizons", C.BITS),
            (Group(*[gray(x, 0.55, C.TRUE_P) for x in np.asarray(w["real"])[:10:2]]).arrange(RIGHT, buff=0.04), r"reality", C.TRUE_P),
            (Group(*[gray(x, 0.55, C.BITS) for x in np.asarray(w["imag"])[:10:2]]).arrange(RIGHT, buff=0.04), r"imagination", C.BITS),
            (VGroup(*[Square(0.25, stroke_color=c_, stroke_width=1.2, fill_color=c_, fill_opacity=0.3)
                      for c_ in [C.BITS] * 4 + [C.TRUE_P] * 3]).arrange(RIGHT, buff=0.04), r"see, read, act", WHITE),
            (VMobject(color=C.INTERVAL, stroke_width=3).set_points_smoothly([[x, 0.6 * np.sin(2 * x), 0] for x in np.linspace(-1.4, 1.4, 60)]),
             r"action chunks", C.INTERVAL),
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
        head = label(r"Part 18, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. An agent acts on a belief, updated by Bayes' rule as it moves and senses. Over long "
            "tasks, small errors compound, so reliability per step sets how far it can go, and that reach has been "
            "doubling every seven months. A world model lets it imagine before it acts, until its own errors catch "
            "up with it. And robots now run on models that see, read and move."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"running agents fast and cheaply", [19]),
            (r"seeing what a model knows", [20]),
        ], font_size=26)
        with self.voiceover(
            "Agents run models many times per task, so the next part, on inference, is about making each run fast. "
            "And the last part looks inside the model, to see what it actually knows."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 19, \ Inference", font_size=40).to_edge(UP, buff=0.4)
        draft = VGroup(*[Square(0.4, stroke_color=GREY_B, stroke_width=1.5, fill_color=GREY_B, fill_opacity=0.15) for _ in range(5)])
        draft.arrange(RIGHT, buff=0.08).move_to(UP * 0.4)
        dl = label(r"a small model guesses ahead", font_size=24, color=GREY_A).next_to(draft, UP, buff=0.2)
        checks = VGroup(*[MathTex(r"\checkmark" if i < 3 else r"\times", font_size=34, color=C.INTERVAL if i < 3 else C.SURPRISE)
                          .next_to(d, DOWN, buff=0.2) for i, d in enumerate(draft)])
        cl = label(r"the big model checks them all at once", font_size=24, color=GREY_A).next_to(checks, DOWN, buff=0.3)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Next time: inference. How a small model can guess ahead and a big one check its guesses all at once, "
            "<bookmark mark='a'/> with exactly the same output; and how to store numbers in four bits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(draft), FadeIn(dl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in checks], lag_ratio=0.2), FadeIn(cl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [r"S.~Thrun, W.~Burgard \& D.~Fox, \textit{Probabilistic Robotics} (2005)",
                 r"R.~S.~Sutton \& A.~G.~Barto, \textit{Reinforcement Learning: An Introduction} (2nd ed., 2018)"]
        papers = [
            r"T.~Kwa et al.\ (METR), \textit{Measuring AI Ability to Complete Long Tasks} (2025)",
            r"D.~Ha \& J.~Schmidhuber, \textit{World Models} (2018); \ D.~Hafner et al., \textit{Mastering Diverse Domains through World Models} (2025)",
            r"J.~Bruce et al., \textit{Genie: Generative Interactive Environments} (2024)",
            r"A.~Brohan et al., \textit{RT-2} (2023); \ K.~Black et al., \textit{$\pi_0$: A Vision-Language-Action Flow Model} (2024)",
        ]
        card = reference_card(books, papers)
        data = note(r"Every number here is computed and checked; \ the METR trend as published; \ illustrations are labeled.",
                    font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover("Thanks for watching, and see you in part nineteen."):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))

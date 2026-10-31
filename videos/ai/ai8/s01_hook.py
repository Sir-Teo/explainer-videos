from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import HIST, PART, TEST, TRAIN, curve, load


class Hook(VoiceoverScene):
    def construct(self):
        self.gap()
        self.era()
        self.plan()

    # ------------------------------------------------------------------
    def gap(self):
        g = load("gap")
        ks, tr, te = np.asarray(g["ks"]), np.asarray(g["train_err"]), np.asarray(g["test_err"])
        ax = Axes(x_range=[0, 150, 25], y_range=[0, 0.4, 0.1], x_length=7.0, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.4, -0.4, 0])
        yl = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0.0, 0.1, 0.2, 0.3, 0.4)])
        xl = label(r"$k$: \ how many neighbours vote \ (Part 6)", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yn = label(r"wrong answers", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        c_tr, c_te = curve(ax, ks, tr, TRAIN), curve(ax, ks, te, TEST)
        key = VGroup(label(r"on the pages it learned from", font_size=26, color=TRAIN),
                     label(r"on new pages", font_size=26, color=TEST)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        key.move_to([4.6, 1.6, 0])
        gap = DoubleArrow(ax.c2p(1, tr[0]), ax.c2p(1, te[0]), buff=0, color=WHITE, stroke_width=3,
                          max_tip_length_to_length_ratio=0.12).shift(RIGHT * 0.25)
        gl = label(r"the gap", font_size=28, color=WHITE).next_to(gap.get_top(), RIGHT, buff=0.15)
        q = label(r"Why should anything learned \\ from examples work on new ones?", font_size=32, color=WHITE)
        q.move_to([4.4, -0.8, 0])
        with self.voiceover(
            "In part six, a model that asked only its single nearest neighbour got "
            f"{100 * (1 - tr[0]):.0f} percent of its own training pages right, and only {100 * (1 - te[0]):.0f} percent "
            "of new ones. <bookmark mark='a'/> Let more neighbours vote, and the two error rates meet. "
            "<bookmark mark='b'/> That gap is the central question of machine learning. A model is fitted to "
            "examples. Why should it work on anything else?"
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn))
            self.play(Create(c_tr), Create(c_te), FadeIn(key), run_time=2.0)
            self.play(GrowFromCenter(gap), FadeIn(gl))
            vo.wait_until("a")
            self.play(Indicate(c_te, color=TEST))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def era(self):
        """How we got here: from Hoeffding to memorization in court, evenly spaced (not to scale)."""
        events = [
            (1963, r"Hoeffding: \\ averages concentrate"),
            (1971, r"Vapnik, Chervonenkis: \\ capacity"),
            (1984, r"Valiant: \\ PAC learning"),
            (1992, r"Geman et al.: \\ bias and variance"),
            (1999, r"McAllester: \\ PAC-Bayes"),
            (2002, r"Bartlett, Mendelson: \\ Rademacher"),
            (2017, r"Zhang et al.: \\ random labels"),
            (2019, r"Belkin et al.: \\ double descent"),
            (2020, r"Bartlett et al.: \\ benign overfitting"),
            (2021, r"Carlini et al.: \\ extracting text"),
            (2025, r"bounds for LLMs; \\ memorization in court"),
        ]
        n = len(events)
        xs = np.linspace(-6.0, 6.0, n)
        y0 = -0.2
        axis = Line([-6.7, y0, 0], [6.7, y0, 0], color=GREY_C, stroke_width=3)
        marks, skel = [], VGroup()
        for i, ((yr, txt), x) in enumerate(zip(events, xs)):
            up = i % 2 == 0
            stem = Line([x, y0, 0], [x, y0 + (0.9 if up else -0.9), 0], color=HIST, stroke_width=2.5)
            dot = Dot([x, y0, 0], radius=0.08, color=HIST)
            yl = label(rf"{yr}", font_size=30, color=HIST)
            t = label(txt, font_size=19, color=WHITE)
            words = VGroup(yl, t).arrange(DOWN, buff=0.06)
            words.next_to(stem.get_end(), UP if up else DOWN, buff=0.08)
            keep_in_frame(words, margin=0.12)
            marks.append(VGroup(stem, dot, words))
            skel.add(VGroup(stem.copy().set_stroke(GREY_D), Dot([x, y0, 0], radius=0.06, color=GREY_D),
                            yl.copy().set_color(GREY_D).move_to(yl)))
        head = label(r"How we got here", font_size=42).to_edge(UP, buff=0.3)
        tag = note(r"milestones evenly spaced, \ not to scale").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The question is old, and so are the first answers. In 1963 Wassily Hoeffding showed how tightly an "
            "average of many independent draws gathers around its mean. <bookmark mark='a'/> In 1971 Vladimir Vapnik "
            "and Alexey Chervonenkis turned that into a theory of learning: what a model can learn depends on how "
            "much it could fit. <bookmark mark='b'/> In 1984 Leslie Valiant defined learning itself, probably "
            "approximately correct. <bookmark mark='c'/> In 1992 Geman, Bienenstock and Doursat named the dilemma of "
            "bias against variance; <bookmark mark='d'/> in 1999 David McAllester gave bounds for averages of "
            "models, <bookmark mark='e'/> and in 2002 Bartlett and Mendelson measured capacity by fitting noise. "
            "<bookmark mark='f'/> Then deep learning broke the picture: in 2017 Zhang and colleagues showed networks "
            "memorizing random labels, <bookmark mark='g'/> in 2019 Belkin and colleagues found test error falling "
            "again past the point of fitting everything, <bookmark mark='h'/> and in 2020 Bartlett and colleagues "
            "proved when fitting noise is harmless. <bookmark mark='i'/> From 2021, Carlini and colleagues pulled "
            "training text out of language models, <bookmark mark='j'/> and by 2025 there were bounds that say "
            "something real about large language models, and courts ruling on what they memorize."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tag), FadeIn(skel))
            self.play(FadeIn(marks[0], shift=UP * 0.2))
            for k, mk in enumerate("abcdefghij"):
                vo.wait_until(mk)
                self.play(FadeIn(marks[k + 1], shift=(UP if (k + 1) % 2 == 0 else DOWN) * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Fitting and Generalizing", font_size=50).to_edge(UP, buff=0.45)
        sub = label(r"why models work on data they have never seen", font_size=30, color=TEST).next_to(title, DOWN, buff=0.2)
        smap = series_map(current=PART, done=PART - 1).scale(0.78).move_to(DOWN * 0.7)
        obj = objectives_card([
            r"risk: \ empirical, \ true, \ and the best possible; \ bias and variance, \ derived",
            r"one rule and many: \ Hoeffding, \ the union bound, \ PAC learning",
            r"capacity: \ shattering, \ the VC bound, \ Rademacher complexity, \ margins",
            r"bounds that work for networks: \ PAC-Bayes, \ compression, \ stability",
            r"the puzzles: \ random labels, \ implicit bias, \ double descent, \ benign overfitting, \ flat minima",
            r"when the world moves: \ distribution shift; \ and what language models memorize",
        ], font_size=23).move_to(DOWN * 0.45)
        assumptions = note(r"statistical guarantees assume IID samples; \ book pages illustrate the calculations",
                           font_size=20).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "This is Part 8 of AI, Built: fitting and generalizing, or why models work on data they've never seen. "
            "Statistical guarantees assume independent samples from one distribution; our correlated book pages "
            "illustrate the calculations. "
            "<bookmark mark='a'/> In it: risk, the quantity we really care about, and the best any model could do; "
            "bias and variance, derived; <bookmark mark='b'/> how one rule's score on test data can be trusted, and "
            "what changes when we choose among many; <bookmark mark='c'/> capacity, measured three ways, each with "
            "the guarantee it buys; <bookmark mark='d'/> bounds that still say something for neural networks; "
            "<bookmark mark='e'/> the experiments that broke the classical story, and the explanations since; "
            "<bookmark mark='f'/> and finally what happens when the test data comes from somewhere else, and what a "
            "language model remembers word for word."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub), FadeIn(smap), FadeIn(assumptions))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeOut(sub), FadeIn(obj.head), FadeIn(obj.rows[0], shift=UP * 0.1))
            for k, mk in enumerate("bcdef"):
                vo.wait_until(mk)
                self.play(FadeIn(obj.rows[k + 1], shift=UP * 0.1))
        self.wait(0.5)
        self.clear_scene()

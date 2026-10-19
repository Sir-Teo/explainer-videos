from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import TEST, TRAIN, curve, load


class Hook(VoiceoverScene):
    def construct(self):
        self.gap()
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
    def plan(self):
        title = label(r"Part 8: \ Fitting and Generalizing", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"bias and variance, \ capacity, \ memorizing, \ double descent", font_size=30, color=C.BITS)
        sub.next_to(title, DOWN, buff=0.25)
        smap = series_map(current=8, done=7).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "This part follows that question through the classical answers, bias and variance, and the capacity of a "
            "model, <bookmark mark='a'/> and then to two experiments that broke them: networks that memorize "
            "nonsense, and a curve that comes back down."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()

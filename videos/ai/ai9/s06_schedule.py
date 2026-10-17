from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import SCHED_COLORS, curve, load

NAMES = {"constant": r"constant", "cosine": r"cosine", "wsd": r"warmup--stable--decay"}


class Schedule(VoiceoverScene):
    def construct(self):
        self.card()
        self.schedules()

    def card(self):
        card = chapter_card(5, r"Learning-rate schedules", r"How should the step size change over a run?", part=9)
        with self.voiceover("Chapter five. Learning-rate schedules."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def schedules(self):
        s = load("schedule")
        keys = ["constant", "cosine", "wsd"]
        steps = float(np.asarray(s["constant"])[-1, 0])
        # the three shapes, small, on top
        sax = Axes(x_range=[0, steps, 1000], y_range=[0, 1.1, 0.5], x_length=6.0, y_length=1.6, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.4, 2.2, 0])
        shapes = {k: curve(sax, np.arange(len(s[f"lr_{k}"])) * 20, s[f"lr_{k}"], SCHED_COLORS[k], 3) for k in keys}
        sl = label(r"learning rate", font_size=22, color=GREY_A).next_to(sax, LEFT, buff=0.2)
        # the losses
        allc = {k: np.asarray(s[k]) for k in keys}
        late = {k: c[c[:, 0] >= 0.5 * steps] for k, c in allc.items()}
        bot = float(min(c[:, 1].min() for c in late.values())) - 0.05
        top = float(max(c[:, 1].max() for c in late.values())) + 0.05
        ax = Axes(x_range=[0.5 * steps, steps, 500], y_range=[bot, top, 0.05], x_length=6.0, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-2.4, -1.4, 0])
        yl = VGroup(*[MathTex(f"{v:.2f}", font_size=20, color=GREY_B).next_to(ax.c2p(0.5 * steps, v), LEFT, buff=0.1)
                      for v in np.round(np.linspace(bot + 0.02, top - 0.02, 3), 2)])
        xl = label(r"the second half of training", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        losses = {k: curve(ax, late[k][:, 0], late[k][:, 1], SCHED_COLORS[k], 3.5) for k in keys}
        finals = s["finals"]
        rows = VGroup(*[label(rf"{NAMES[k]}: \ ${finals[k]:.3f}$ bits", font_size=26, color=SCHED_COLORS[k]) for k in keys])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, 0.6, 0])
        why = label(r"the drop comes when the steps shrink: \\ the noise cloud of Chapter 1 contracts", font_size=24,
                    color=C.BITS).next_to(rows, DOWN, buff=0.5).align_to(rows, LEFT)
        cite_ = cite(r"I.~Loshchilov \& F.~Hutter, SGDR (2016); \ S.~Hu et al., MiniCPM (2024)", corner=DR)
        warm = gloss(r"warmup", r"start with tiny steps while the weights \\ are still random, \ so the first updates "
                     r"don't blow up", corner=UR, width=5.4, color=SCHED_COLORS["cosine"])
        ramp = SurroundingRectangle(Line(sax.c2p(0, 0), sax.c2p(0.04 * steps, 1.05)), color=SCHED_COLORS["cosine"], buff=0.08,
                                    corner_radius=0.05, stroke_width=2)
        assert finals["wsd"] < finals["constant"]
        with self.voiceover(
            "The step size itself should change during training. A constant rate is the simplest. "
            "<bookmark mark='a'/> A cosine schedule warms up briefly, starting with tiny steps while the weights are "
            "still random, so the first updates don't blow up. Then it glides smoothly down to zero. "
            "<bookmark mark='b'/> Warmup–stable–decay holds the rate flat for most of the run, and only drops it at "
            "the end. <bookmark mark='c'/> Here they are on the character model. While the rate stays high, the "
            "loss plateaus. When it falls, the loss drops sharply, as the noisy cloud from chapter one shrinks onto "
            "the bottom. <bookmark mark='d'/> Warmup–stable–decay is popular for a practical reason: you can stop "
            "at any point, decay briefly, and get a finished model, without knowing in advance how long you'll train."
        ) as vo:
            self.play(Create(sax), FadeIn(sl), Create(shapes["constant"]), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(shapes["cosine"]))
            self.play(FadeIn(warm, shift=DOWN * 0.2), Create(ramp))
            vo.wait_until("b")
            self.play(FadeOut(warm), FadeOut(ramp))
            self.play(Create(shapes["wsd"]))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(yl), FadeIn(xl))
            self.play(*[Create(losses[k]) for k in keys], run_time=3.0, rate_func=linear)
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()
